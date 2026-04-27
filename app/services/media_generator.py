from __future__ import annotations

import base64
import json
import os
import urllib.error
import urllib.request


FALLBACK_PNG_BASE64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO7Z2ioAAAAASUVORK5CYII="


class MediaGenerator:
    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY", "").strip()
        self.model = os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-1")
        endpoint = os.getenv("OPENAI_BASE_URL") or os.getenv("OPENAI_ENDPOINT") or "https://api.openai.com/v1"
        endpoint = endpoint.rstrip("/")
        self.is_azure = ".openai.azure.com" in endpoint
        if self.is_azure and not endpoint.endswith("/openai/v1"):
            endpoint = f"{endpoint}/openai/v1"
        elif not self.is_azure and not endpoint.endswith("/v1"):
            endpoint = f"{endpoint}/v1"
        self.base_url = endpoint
        self.disable_proxy = os.getenv("OPENAI_DISABLE_PROXY", "false").lower() == "true"
        self.last_error: str | None = None
        self.last_used_fallback: bool = False

    @property
    def enabled(self) -> bool:
        return bool(self.api_key)

    def generate_png(self, prompt: str, size: str = "1024x1024") -> bytes:
        self.last_error = None
        self.last_used_fallback = False
        if not self.enabled:
            self.last_error = "OPENAI_API_KEY is not set"
            self.last_used_fallback = True
            return base64.b64decode(FALLBACK_PNG_BASE64)

        payload = {
            "model": self.model,
            "prompt": prompt,
            "size": size,
        }
        req = urllib.request.Request(
            f"{self.base_url}/images/generations",
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
            with opener.open(req, timeout=90) as response:
                body = json.loads(response.read().decode("utf-8"))
            image_b64 = body["data"][0]["b64_json"]
            return base64.b64decode(image_b64)
        except (urllib.error.URLError, KeyError, IndexError, json.JSONDecodeError, ValueError) as exc:
            self.last_error = str(exc)
            self.last_used_fallback = True
            return base64.b64decode(FALLBACK_PNG_BASE64)
