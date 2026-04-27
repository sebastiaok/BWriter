from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List


@dataclass
class UserInput:
    topic: str
    target_audience: str
    tone: str
    length: str
    product_info: str
    image_style: str
    thumbnail_style: str
    candidate_keywords: int = 12
    selected_keywords_count: int = 3


@dataclass
class KeywordBundle:
    topic: str
    keyword: str
    matched_product: str
    search_intent: str
    reason: str


@dataclass
class ContentBrief:
    keyword: str
    title: str
    persona: str
    goal: str
    unique_angle: str
    sections: List[str]


@dataclass
class GeneratedPost:
    keyword: str
    title: str
    markdown: str
    faq: List[Dict[str, str]]


@dataclass
class ImageAsset:
    keyword: str
    section: str
    prompt: str
    file_name: str
    alt_text: str


@dataclass
class ThumbnailAsset:
    keyword: str
    copy: str
    variants: List[str]


@dataclass
class FinalPackage:
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    keyword: str = ""
    brief: ContentBrief | None = None
    post: GeneratedPost | None = None
    images: List[ImageAsset] = field(default_factory=list)
    thumbnail: ThumbnailAsset | None = None
    metadata: Dict[str, str] = field(default_factory=dict)
    review_report: Dict[str, str] = field(default_factory=dict)
