from __future__ import annotations

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class VideoAsset(BaseModel):
    url: str
    cached_path: Optional[str] = None
    duration_s: Optional[float] = None


class TextVariant(BaseModel):
    locale_hint: Optional[str] = None
    body: Optional[str] = None
    title: Optional[str] = None
    caption: Optional[str] = None
    cta_text: Optional[str] = None


class VideoFacts(BaseModel):
    creative_id: str
    page_name: Optional[str]
    is_active: bool
    active_days: Optional[int]
    publisher_platform: List[str] = Field(default_factory=list)
    start_date: Optional[str] = None
    end_date: Optional[str] = None

    text_primary: Optional[str] = None
    title_primary: Optional[str] = None
    caption_primary: Optional[str] = None

    variants: List[TextVariant] = Field(default_factory=list)
    assets: List[VideoAsset] = Field(default_factory=list)


class AnalysisScores(BaseModel):
    hook: Optional[float] = None
    cta: Optional[float] = None
    product_visibility: Optional[float] = None
    message_density: Optional[float] = None
    structure: Optional[float] = None
    music_fit: Optional[float] = None
    overall: Optional[float] = None


class HookItem(BaseModel):
    time_s: Optional[float] = None
    tactic: Optional[str] = None
    desc: Optional[str] = None
    strength: Optional[float] = None


class CTAItem(BaseModel):
    text: Optional[str] = None
    channels: List[str] = Field(default_factory=list)
    time_s: Optional[float] = None
    strength: Optional[float] = None


class PainItem(BaseModel):
    text: Optional[str] = None
    timecodes: List[float] = Field(default_factory=list)
    severity: Optional[float] = None


class ValuePropItem(BaseModel):
    text: Optional[str] = None
    timecodes: List[float] = Field(default_factory=list)
    strength: Optional[float] = None


class StoryboardItem(BaseModel):
    scene: Optional[int] = None
    start_s: Optional[float] = None
    end_s: Optional[float] = None
    what_we_see: Optional[str] = None
    what_we_hear: Optional[str] = None


class ConceptStyle(BaseModel):
    style: Optional[str] = None
    effects: List[str] = Field(default_factory=list)
    captions: Dict[str, Any] = Field(default_factory=dict)


class ProductShowcase(BaseModel):
    type: Optional[str] = None
    scenes: List[int] = Field(default_factory=list)
    features: List[str] = Field(default_factory=list)
    clarity_score: Optional[float] = None


class MusicInfo(BaseModel):
    bpm: Optional[float] = None
    mood: Optional[str] = None
    notes: Optional[str] = None


class AnalysisResult(BaseModel):
    creative_id: str
    meta: Dict[str, Any] = Field(default_factory=dict)
    scores: AnalysisScores = Field(default_factory=AnalysisScores)
    hooks: List[HookItem] = Field(default_factory=list)
    cta: List[CTAItem] = Field(default_factory=list)
    pains: List[PainItem] = Field(default_factory=list)
    value_props: List[ValuePropItem] = Field(default_factory=list)
    concept_style: ConceptStyle = Field(default_factory=ConceptStyle)
    storyboard: List[StoryboardItem] = Field(default_factory=list)
    product_showcase: ProductShowcase = Field(default_factory=ProductShowcase)
    music: MusicInfo = Field(default_factory=MusicInfo)
    summary: Optional[str] = None
    overall_rank_score: Optional[float] = None
