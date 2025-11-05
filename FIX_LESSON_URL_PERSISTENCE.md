# Fix: Lesson URL Persistence for Content Block Navigation

## Problem Statement

When viewing a lesson and navigating through content blocks (sections 1, 2, 3, etc.), refreshing the browser would reset the view back to section 1 instead of staying on the current section.

**Example:**
- User opens a lesson (section 1)
- Clicks "Next" 3 times (now at section 4)
- Refreshes browser (F5)
- **Bug**: Returns to section 1
- **Expected**: Should stay at section 4

## Root Cause

The lesson navigation state (`current_block_index`) was stored only in `st.session_state`, which is lost on page refresh. While the URL contained `lesson_id`, it did not include the `block_index`, so there was no way to restore the user's position after a refresh.

## Solution

Add `block_index` as a URL query parameter and sync it bidirectionally:
1. Session state → URL (when user navigates)
2. URL → Session state (when page loads/refreshes)

## Changes Made

### File: [app.py](app.py)

#### 1. Sync block_index FROM URL to session state (lines 108-114)
```python
# Sync content block index from URL if present
if "block_index" in params and params.get("page") == "lesson":
    try:
        block_index = int(params["block_index"])
        st.session_state.current_block_index = block_index
    except (ValueError, TypeError):
        pass  # Invalid block_index, ignore
```

#### 2. Sync block_index FROM session state to URL (lines 129-131)
```python
# Add content block index if available
if "current_block_index" in st.session_state:
    params["block_index"] = str(st.session_state.current_block_index)
```

### File: [ui/pages/lesson_viewer.py](ui/pages/lesson_viewer.py)

#### 3. Initialize block_index when starting lesson (line 314)
```python
st.session_state.current_block_index = 0  # Start from beginning
```

#### 4. Update URL when navigating (lines 317-321, 682-713)
Added `block_index` to `st.query_params.update()` calls for:
- Starting a lesson
- Clicking "Previous" button
- Clicking "Next" button
- Clicking "Quiz" button

Example:
```python
st.query_params.update({
    "page": "lesson",
    "lesson_id": str(lesson.lesson_id),
    "block_index": str(st.session_state.current_block_index)
})
```

## URL Format

### Before Fix
```
http://localhost:8501/?page=lesson&lesson_id=abc123...
```

### After Fix
```
http://localhost:8501/?page=lesson&lesson_id=abc123...&block_index=3
```

## Benefits

1. ✅ **Refresh Persistence**: Users can refresh and stay on their current section
2. ✅ **Browser Navigation**: Back/forward buttons work correctly
3. ✅ **Shareable URLs**: Users can share direct links to specific sections
4. ✅ **Bookmarking**: Users can bookmark their progress in a lesson
5. ✅ **Better UX**: No frustration from losing progress on accidental refresh

## Testing

See [test_url_persistence.md](test_url_persistence.md) for detailed test cases.

**Quick test:**
1. Start a lesson
2. Click "Next" 3 times
3. Verify URL shows `block_index=3`
4. Refresh page (F5)
5. Should still be on section 4 (block_index=3)

## Backward Compatibility

✅ **Fully backward compatible**
- Old URLs without `block_index` still work (defaults to 0)
- No database changes required
- No breaking changes to existing functionality

## Performance Impact

Negligible - only adds one small query parameter to URLs.

## Related Issues

This fix also improves:
- URL shareability (users can share exact section links)
- Browser history navigation (back/forward work correctly)
- Deep linking (can link to specific lesson sections from external sources)

## Files Modified

1. `app.py` - URL syncing logic (2 changes)
2. `ui/pages/lesson_viewer.py` - Navigation button URL updates (4 changes)

Total lines changed: ~30 lines
