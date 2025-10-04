"""
MongoDB models for tasks, creatives, and analysis results.
"""
from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from enum import Enum
from pydantic import BaseModel, Field, field_validator


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    PARSING = "PARSING"
    PARSED = "PARSED"
    ANALYZING = "ANALYZING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class PolicyCheckStatus(str, Enum):
    PENDING = "PENDING"
    CHECKING = "CHECKING"
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
    hooks: List[Union[str, Dict[str, Any]]] = Field(default_factory=list)  # Allow both strings and dicts
    core_idea: Optional[str] = None
    theme: Optional[str] = None
    message: Optional[str] = None
    recommendations: Optional[str] = None
    video_prompt: Optional[str] = None
    
    @field_validator('hooks', mode='before')
    @classmethod
    def validate_hooks(cls, v):
        """Ensure hooks is a list, even if LLM returns something else."""
        if v is None:
            return []
        if isinstance(v, str):
            return [v]
        if not isinstance(v, list):
            return []
        return v


class PolicyTask(BaseModel):
    """Task for video policy compliance checking."""
    task_id: str
    video_url: Optional[str] = None
    video_path: Optional[str] = None
    platform: str = "facebook"
    status: PolicyCheckStatus = PolicyCheckStatus.PENDING
    
    # Results
    policy_result: Optional[Dict[str, Any]] = None
    html_report: Optional[str] = None
    will_pass_moderation: Optional[bool] = None
    risk_level: Optional[str] = None
    violations_count: Optional[int] = None
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    error: Optional[str] = None
    
    class Config:
        use_enum_values = True


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
    aggregation_error: Optional[str] = None  # Error during aggregation (task still completed)
    html_report: Optional[str] = None  # HTML report for frontend display

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    error: Optional[str] = None  # Critical error (task failed)

    class Config:
        use_enum_values = True


# ============================================================================
# Chat MVP Models
# ============================================================================

class ChatSessionStatus(str, Enum):
    """Chat session status."""
    ACTIVE = "active"
    FINAL = "final"


class CreativeObjective(str, Enum):
    """Creative objective for brief."""
    INSTALL = "install"
    LEAD = "lead"
    PURCHASE = "purchase"
    SIGNUP = "signup"
    TRAFFIC = "traffic"


class CreativePlatform(str, Enum):
    """Platform for creative."""
    TIKTOK = "tiktok"
    INSTAGRAM = "instagram"
    YOUTUBE = "youtube"


class CreativeFormat(str, Enum):
    """Format for creative."""
    REELS = "reels"
    SHORTS = "shorts"
    TIKTOK = "tiktok"
    FEED = "feed"


class BriefState(BaseModel):
    """Brief state with known fields."""
    product_offer: Optional[str] = None
    audience: Optional[str] = None
    objective: Optional[CreativeObjective] = None
    platform: Optional[CreativePlatform] = None
    format: Optional[CreativeFormat] = None
    aspect_ratio: str = "9:16"
    duration_s: Optional[int] = None
    cta: Optional[str] = None

    class Config:
        use_enum_values = True


class ChatSession(BaseModel):
    """Chat session for brief collection."""
    session_id: str
    task_id: Optional[str] = None  # Optional link to Step-1 task
    status: ChatSessionStatus = ChatSessionStatus.ACTIVE
    known: BriefState = Field(default_factory=BriefState)
    completeness: float = 0.0
    missing_fields: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        use_enum_values = True


class ChatMessage(BaseModel):
    """Chat message in a session."""
    session_id: str
    role: str  # "user" or "assistant"
    text: str
    ts: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        use_enum_values = True
