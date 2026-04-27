from __future__ import annotations

import json
import os
import urllib.error
import urllib.request


class LlmClient:
    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY", "").strip()
        self.model = os.getenv("OPENAI_TEXT_MODEL", "gpt-4o-mini")
        endpoint = os.getenv("OPENAI_ENDPOINT")
        endpoint = endpoint.rstrip("/")
        self.is_azure = ".openai.azure.com" in endpoint
        if self.is_azure and not endpoint.endswith("/openai/v1"):
            endpoint = f"{endpoint}/openai/v1"
        elif not self.is_azure and not endpoint.endswith("/v1"):
            endpoint = f"{endpoint}/v1"
        self.base_url = endpoint
        self.disable_proxy = os.getenv("OPENAI_DISABLE_PROXY", "false").lower() == "true"
        self.last_error: str | None = None

    @property
    def enabled(self) -> bool:
        return bool(self.api_key)

    def generate_markdown(self, prompt: str) -> str | None:
        self.last_error = None
        if not self.enabled:
            self.last_error = "OPENAI_API_KEY is not set"
            return None

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You write high-quality Korean SEO blog posts in markdown."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.7,
        }
        req = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "api-key" if self.is_azure else "Authorization": self.api_key
                if self.is_azure
                else f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            opener = (
                urllib.request.build_opener(urllib.request.ProxyHandler({}))
                if self.disable_proxy
                else urllib.request.build_opener()
            )
            with opener.open(req, timeout=60) as response:
                body = json.loads(response.read().decode("utf-8"))
            return body["choices"][0]["message"]["content"].strip()
        except (urllib.error.URLError, KeyError, IndexError, json.JSONDecodeError) as exc:
            self.last_error = str(exc)
            return None
