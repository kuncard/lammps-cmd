# LAMMPS Manual Search

> LAMMPS 手册检索引擎 —— 知识图谱 × 混合检索，自然语言秒查 LAMMPS 命令文档。

基于 [docs.lammps.org](https://docs.lammps.org) 的 911 篇文档构建，结合 **BM25 关键词检索**、**语义向量检索**（`all-mpnet-base-v2`）和 **知识图谱**（910 节点、3,214 条边），通过 RRF 融合排序。

```
"how to control temperature in NVT"  →  fix_nh, fix_langevin, Howto_thermostat
"boundry condition"                   →  boundary          (拼写纠错)
"nvt pdamp default"                   →  fix_nh            (缩写展开)
```

---

## 快速开始

```bash
git clone https://github.com/kuncard/lammps-search.git
cd lammps-search
pip install -r requirements.txt
python app.py --port 8760
```

首次启动自动构建 BM25 索引（约 30 秒）并下载 `all-mpnet-base-v2` 模型（约 420 MB）。

| 页面 | 功能 |
|------|------|
| `http://localhost:8760` | 搜索界面（关键词高亮、分类筛选、移动端适配） |
| `http://localhost:8760/graph` | 知识图谱可视化（910 节点、3,214 边，vis.js） |
| `http://localhost:8760/api/search` | JSON API |

> 网络慢可以先用 BM25-only 模式，跳过模型下载：
> ```bash
> python app.py --port 8760 --skip-vector
> ```
> 向量索引后续手动构建：`python vector_index.py --build`

---

## API

```bash
curl -X POST http://localhost:8760/api/search \
  -H "Content-Type: application/json" \
  -d '{"question": "how to control temperature in NVT", "top_k": 5}'
```

返回示例：

```json
{
  "question": "how to control temperature in NVT",
  "query_type": "natural",
  "query_tokens": ["control", "temperature", "nvt"],
  "results": [
    {
      "cmd_id": "fix_nh",
      "title": "fix nvt command",
      "section": "Description",
      "text": "These commands perform time integration...",
      "url": "https://docs.lammps.org/fix_nh.html",
      "bm25_rank": 3,
      "vec_rank": 1,
      "rrf_score": 0.0313
    }
  ]
}
```

每个结果包含 `cmd_id`、`url`、`text`，可直接注入下游 LLM。

---

## 命令行

```bash
# 纯 BM25（零额外依赖，命令名检索首选）
python skills/lammps-kg/scripts/search_lammps.py search "fix nvt Tdamp"

# 语义搜索（需要 numpy + sentence-transformers）
python skills/lammps-kg/scripts/search_lammps.py search "how to control temperature" --vector

# 节点详情
python skills/lammps-kg/scripts/search_lammps.py detail fix_nh

# 图谱邻居
python skills/lammps-kg/scripts/search_lammps.py neighbors fix_nh

# 命令补全
python skills/lammps-kg/scripts/search_lammps.py suggest "ther"

# 索引健康检查
python skills/lammps-kg/scripts/search_lammps.py health

# 评测
python evaluate.py                 # 纯 BM25
python evaluate.py --vector        # BM25 + Vector
```

---

## 架构

### 检索管线

```
用户查询
  │
  ├── ABBREV 展开          nvt → "fix_nh fix_nvt Nose-Hoover thermostat"
  ├── PHRASE_MAP 展开      "control temperature" → "thermostat fix_nh ..."
  ├── QueryExpander        图谱节点标题/ID → 同义词扩展
  ├── 拼写纠错             trigram 重叠 + Levenshtein ≤ 2, confidence > 0.7
  └── 查询分类             command / natural / param
         │
    ┌────┴────┐
    ▼         ▼
  BM25     Vector (mpnet 768d)
    │         │
    └────┬────┘
         ▼
    RRF 融合（k 值动态调整）
         │
         ▼
    Graph Boost（rerank / expand）
         │
         ▼
    Top-K 结果（按 cmd_id 去重）
```

### 查询分类策略

| 类型 | 触发条件 | RRF k 值 | 说明 |
|------|---------|----------|------|
| **command** | 包含已知命令名 或 `_` 复合词 | 80 | BM25 主导，精确匹配优先 |
| **param** | 包含参数关键词（default, pdamp, cutoff...） | 60 | 均衡模式 |
| **natural** | 包含疑问词（how, what, why...）或其他 | 20 | Vector 主导，语义匹配 |

### 数据处理流程

```
docs.lammps.org
  │
  ▼
scrape_all.py               →  lammps_kb/  (911 篇 .md)
  │
  ├── build_full_graph.py   →  graph_data_full.json  (910 节点, 3,214 边)
  │     ├── 规则匹配（Related Commands + Restrictions）: 2,007 边
  │     ├── LLM 提取（DeepSeek）:                        849 边
  │     └── 双确认（Rule ∩ LLM）:                        14 边
  │
  └── chunker.py            →  6,925 chunks  (full + section + sliding_window)
        │
        ├── BM25Index       →  bm25_index.json
        └── VectorIndex     →  embeddings.npy  (all-mpnet-base-v2, 768d)
               │
               └── HybridRetriever  →  RRF 融合 + Graph Boost
```

---

## 评测

### CLI `--vector` 模式（108 条手工评测）

| 类别 | Top-3 | 说明 |
|----------|-------|------|
| exact_command | 100% | 精确命令名 |
| compound | 100% | 复合命令（如 `fix nvt Tdamp 0.5 0.5`） |
| comparative | 100% | 对比问句 |
| spelling_error | 100% | 拼写错误纠正 |
| command_lookup | 94% | 自然语言描述 → 命令 |
| abbreviation | 83% | 缩写展开 |
| parameter_lookup | 67% | 参数查询 |
| beginner | 62% | 新手入门问题 |
| troubleshooting | 60% | 排错场景 |
| natural_language | 50% | 自然语言查询 |
| conceptual | 50% | 概念性问题 |
| **总体** | **79%** | |

> 纯 BM25 为 **69%**。natural_language、conceptual 等语义类别在纯 BM25 下仅 33-50%，开启 `--vector` 后大幅提升。

### Flask API 模式（47 条手工评测）

| 模式 | Top-3 |
|------|-------|
| BM25 + Vector + Graph Boost | **94%** |

---

## 两套检索路径

两套入口共享同一知识图谱，检索策略不同：

| 维度 | Flask API (`app.py`) | CLI (`search_lammps.py`) |
|------|---------------------|--------------------------|
| 索引粒度 | Chunk-level（6925 chunks） | Graph-node-level（910 nodes） |
| 预处理 | ABBREV + PHRASE_MAP + SpellCorrector | 上述全部 + QueryExpander + Stemming |
| 融合方式 | RRF + Graph Rerank（保守，适合 UI） | RRF + Graph Expand（允许邻居节点进入结果） |
| 使用场景 | Web 搜索、API 调用 | 终端查询、评测 |

---

## 项目结构

```
lammps-search/
├── app.py                     Flask 主程序
├── bm25_index.py              BM25 索引 + 查询分类 + 展开
├── tokenizer.py               分词器（复合词拆分 + 停用词）
├── spell.py                   拼写纠错（trigram + Levenshtein）
├── chunker.py                 文档分块（full + section + sliding_window）
├── vector_index.py            向量索引（all-mpnet-base-v2, 768d）
├── hybrid_search.py           RRF 融合 + Graph Boost
├── query_expander.py          图谱节点 → 查询词映射
├── abbrev.py                  共享 ABBREV + PHRASE_MAP 词典
├── llm_utils.py               LLM API 抽象层
├── logging_setup.py           日志配置
├── build_full_graph.py        知识图谱构建（规则 + LLM + 验证）
├── fix_isolated_llm.py        LLM 后处理补边（消除孤立点）
├── scrape_all.py              文档抓取（全量 + 增量）
├── evaluate.py                评测脚本
├── generate_queries.py        从图谱边自动生成评测查询
├── index.html                 搜索界面
├── graph.html                 图谱可视化页面（vis.js CDN）
├── graph_data_full.json       预构建知识图谱（910 节点, 3,214 边）
├── golden_queries_hand.json   手工评测集（108 条）
├── golden_queries_auto.json   图谱自动生成评测集（31 条）
├── lammps_kb/                 911 篇 markdown 文档 + 本地索引
├── skills/lammps-kg/scripts/
│   └── search_lammps.py       CLI 入口
├── tests/                     48 条测试
└── requirements.txt
```

---

## 维护更新

LAMMPS 发布新版本后：

```bash
# 1. 增量抓取
python scrape_all.py --diff

# 2. 重建图谱 + 索引
python build_full_graph.py           # 规则构建（含 ATC 隐式边）
python bm25_index.py --build
python vector_index.py --build

# 3. LLM 补边（需要 DEEPSEEK_API_KEY，消除孤立点）
python fix_isolated_llm.py --api-key $env:DEEPSEEK_API_KEY

# 4. 验证
python evaluate.py --vector
python -m pytest tests/ -q
```

> **注意**：HowTo 教程页面在 `scrape_all.py` 中可能抓取不到正文（Sphinx section ID 不匹配），导致 `build_full_graph.py --use-llm` 无法提取边。`fix_isolated_llm.py` 会从 docs.lammps.org 实时获取内容来补全。

---

## License

MIT
