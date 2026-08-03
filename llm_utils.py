"""
Shared LLM utility — single abstraction for API calls.
Currently defaults to DeepSeek API (OpenAI-compatible endpoint).

Usage:
  from llm_utils import call_llm, call_llm_json

  text = call_llm("Explain thermodynamics", system="Be brief.", max_tokens=100)
  data = call_llm_json("Extract edges from this text...")
"""
import json, os, re, urllib.request


def call_llm(prompt, system="You output only valid JSON.",
             model=None, api_key=None, temperature=0.0, max_tokens=500,
             base_url=None):
    """Call an LLM API and return the raw text response.

    Defaults to DeepSeek Chat with DEEPSEEK_API_KEY env var.
    Override model/api_key/base_url for other providers (any OpenAI-compatible API).

    Args:
        prompt: user message content
        system: system message content
        model: model name (default: "deepseek-chat")
        api_key: API key (default: $DEEPSEEK_API_KEY)
        temperature: sampling temperature (default: 0.0)
        max_tokens: max tokens in response
        base_url: API endpoint (default: DeepSeek v1/chat/completions)

    Returns:
        Raw text from the model's response.

    Raises:
        ValueError: if no API key is available
        urllib.error.URLError: on network failure
    """
    model = model or "deepseek-chat"
    api_key = api_key or os.environ.get("DEEPSEEK_API_KEY", "")
    base_url = base_url or "https://api.deepseek.com/v1/chat/completions"

    if not api_key:
        raise ValueError(
            "No API key provided. Pass api_key= or set DEEPSEEK_API_KEY env var."
        )

    data = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }).encode("utf-8")

    req = urllib.request.Request(
        base_url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )

    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read())

    return result["choices"][0]["message"]["content"].strip()


def call_llm_json(prompt, **kwargs):
    """call_llm() + strip markdown fences + JSON.parse.

    Returns:
        Parsed JSON object (dict, list, etc.).
        Returns None if JSON parsing fails.
    """
    raw = call_llm(prompt, **kwargs)

    # Strip markdown code fences
    raw = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.MULTILINE)
    raw = re.sub(r"\s*```\s*$", "", raw, flags=re.MULTILINE)
    raw = raw.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None
