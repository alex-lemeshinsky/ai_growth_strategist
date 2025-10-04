# Error Handling Improvements

## 🎯 Problem
Task was failing completely if:
1. One creative analysis failed
2. LLM aggregation returned unexpected data format
3. Pydantic validation failed on aggregated results

## ✅ Solutions Implemented

### 1. Flexible Data Models
**File:** `src/db/models.py`

- **`AggregatedAnalysis.hooks`**: Changed from `List[Dict]` to `List[Union[str, Dict]]`
  - Now accepts both strings and dictionaries
  - Added `@field_validator` to handle edge cases (None, single string, non-list)

```python
hooks: List[Union[str, Dict[str, Any]]] = Field(default_factory=list)

@field_validator('hooks', mode='before')
@classmethod
def validate_hooks(cls, v):
    if v is None: return []
    if isinstance(v, str): return [v]
    if not isinstance(v, list): return []
    return v
```

### 2. Graceful Aggregation Failure
**File:** `src/services/task_service.py`

- Task completes successfully even if aggregation fails
- Individual creative analyses are **always saved**
- Aggregation error stored in `aggregation_error` field (not `error`)

```python
try:
    aggregated = await _aggregate_analysis(analyses)
except Exception as e:
    logger.warning(f"⚠️ Aggregation failed, but saving individual analyses: {e}")
    aggregation_error = str(e)

# Task still marked as COMPLETED with partial results
```

### 3. Robust Individual Analysis
**File:** `src/services/task_service.py`

- One failed creative doesn't break the entire task
- Detailed logging for each creative
- Summary statistics: `X successful, Y failed`

```python
for idx, ad in enumerate(raw_ads, 1):
    try:
        # Analyze creative
        analyses.append(analysis)
        logger.info(f"✅ Successfully analyzed {ad_id}")
    except Exception as e:
        logger.error(f"❌ Error analyzing {ad_id}: {e}")
        failed_count += 1
        continue  # Continue with other creatives

logger.info(f"📊 Analysis summary: {len(analyses)} successful, {failed_count} failed")
```

### 4. Safe Data Extraction from LLM
**File:** `src/services/task_service.py`

Added helper functions to safely extract data from LLM responses:

```python
def _safe_get_list(key, default=None):
    val = result.get(key, default or [])
    if val is None: return []
    if isinstance(val, str): return [val]
    if isinstance(val, list): return val
    return []

def _safe_get_dict(key, default=None):
    val = result.get(key, default or {})
    if isinstance(val, dict): return val
    return {}
```

### 5. Enhanced Task Model
**File:** `src/db/models.py`

Added separate error fields:
- `error` - Critical error (task FAILED completely)
- `aggregation_error` - Non-critical error (task COMPLETED with partial results)

```python
class Task(BaseModel):
    # ...
    aggregated_analysis: Optional[AggregatedAnalysis] = None
    aggregation_error: Optional[str] = None  # ← New field
    error: Optional[str] = None
```

## 📊 Result

### Before:
```
1 creative fails → ❌ Entire task FAILED
Aggregation fails → ❌ Entire task FAILED
Lost all progress and data
```

### After:
```
1 creative fails → ⚠️  Continue with others
Aggregation fails → ⚠️  Save individual analyses, mark aggregation_error
Task: ✅ COMPLETED (with warnings if any)
All successful analyses are preserved
```

## 🧪 Testing

```bash
# Run test pipeline
python test_full_pipeline.py

# The script now shows:
# - Number of successful/failed creative analyses
# - Aggregation warnings (if any)
# - Individual creative results (always available)
# - Aggregated insights (if aggregation succeeded)
```

## 📋 Task Status Logic

| Scenario | Status | Data Saved |
|----------|--------|------------|
| All creatives analyzed, aggregation OK | `COMPLETED` | ✅ Full results |
| Some creatives failed, aggregation OK | `COMPLETED` | ✅ Partial results |
| Some creatives analyzed, aggregation failed | `COMPLETED` | ✅ Individual analyses only |
| All creatives failed | `FAILED` | ❌ No analysis data |
| Critical error (file not found, etc.) | `FAILED` | ❌ No data |

## 🎯 Key Principles

1. **Fail gracefully** - Save what you can
2. **Be informative** - Log detailed errors
3. **Continue processing** - One failure shouldn't stop everything
4. **Validate defensively** - Don't trust LLM output format
5. **Preserve data** - Always save successful analyses
