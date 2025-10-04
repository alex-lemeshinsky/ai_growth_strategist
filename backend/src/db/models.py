"""
MongoDB models for tasks, creatives, and analysis results.
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    PARSING = "PARSING"
    PARSED = "PARSED"
    ANALYZING = "ANALYZING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class CreativeAnalysis(BaseModel):
    """Detailed analysis of a single creative."""
    creative_id: str
    ad_archive_id: str
    page_name: Optional[str] = None
    
    # Video analysis results
    hook: Optional[Dict[str, Any]] = None
    visual_style: Optional[Dict[str, Any]] = None
    on_screen_text: List[Dict[str, Any]] = Field(default_factory=list)
    product_showcase: Optional[Dict[str, Any]] = None
    cta: List[Dict[str, Any]] = Field(default_factory=list)
    pains: List[Dict[str, Any]] = Field(default_factory=list)
    value_props: List[Dict[str, Any]] = Field(default_factory=list)
    audio: Optional[Dict[str, Any]] = None
    storyboard: List[Dict[str, Any]] = Field(default_factory=list)
    scores: Optional[Dict[str, Any]] = None
    summary: Optional[str] = None
    
    # Meta
    video_url: Optional[str] = None
    cached_video_path: Optional[str] = None
    analyzed_at: Optional[datetime] = None


class AggregatedAnalysis(BaseModel):
    """Aggregated analysis across all creatives."""
    pain_points: List[str] = Field(default_factory=list)
    concepts: List[str] = Field(default_factory=list)
    visual_trends: Dict[str, Any] = Field(default_factory=dict)
    hooks: List[Dict[str, Any]] = Field(default_factory=list)
    core_idea: Optional[str] = None
    theme: Optional[str] = None
    message: Optional[str] = None
    recommendations: Optional[str] = None
    video_prompt: Optional[str] = None


class Task(BaseModel):
    """Task for parsing and analyzing competitor ads."""
    task_id: str
    url: str
    status: TaskStatus = TaskStatus.PENDING
    
    # Results
    page_name: Optional[str] = None
    page_id: Optional[str] = None
    total_ads: Optional[int] = None
    creatives_file: Optional[str] = None
    
    # Analysis results
    creatives_analyzed: List[CreativeAnalysis] = Field(default_factory=list)
    aggregated_analysis: Optional[AggregatedAnalysis] = None
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    error: Optional[str] = None
    
    class Config:
        use_enum_values = True
