# Test Plan: URL Persistence for Lesson Navigation

## Changes Made

### 1. app.py - URL Syncing
- **Line 108-114**: Added code to sync `block_index` from URL to session state
- **Line 129-131**: Added code to include `block_index` in URL when on lesson page

### 2. lesson_viewer.py - Navigation Updates
- **Line 314**: Initialize `current_block_index = 0` when starting a lesson
- **Line 317-321**: Include `block_index` in URL when starting a lesson
- **Line 682-688**: Update URL with `block_index` when clicking "Previous" button
- **Line 695-701**: Update URL with `block_index` when clicking "Next" button
- **Line 707-713**: Update URL with `block_index` when clicking "Quiz" button

## How It Works

1. **When user clicks a lesson**: URL becomes `?page=lesson&lesson_id=xxx&block_index=0`
2. **When user clicks "Next"**: URL updates to `?page=lesson&lesson_id=xxx&block_index=1`, `block_index=2`, etc.
3. **When user refreshes**: The `sync_url_to_session_state()` function reads `block_index` from URL and restores `st.session_state.current_block_index`
4. **Result**: User stays on the same section after refresh

## Testing Instructions for VM

### Test Case 1: Basic Navigation
1. Start the Streamlit app: `streamlit run app.py`
2. Login to your account
3. Go to "📚 My Learning" page
4. Click any lesson to start it
5. Click "Next" button 3 times (should be on section 4)
6. **Verify URL shows**: `?page=lesson&lesson_id=<uuid>&block_index=3`
7. **Refresh the browser (F5)**
8. **Expected**: Still on section 4, not back to section 1
9. **Actual**: ____________________

### Test Case 2: Browser Back/Forward
1. From section 4, click "Next" to go to section 5
2. Click browser back button
3. **Expected**: Should return to section 4
4. **Verify URL shows**: `?page=lesson&lesson_id=<uuid>&block_index=3`
5. Click browser forward button
6. **Expected**: Should return to section 5
7. **Verify URL shows**: `?page=lesson&lesson_id=<uuid>&block_index=4`

### Test Case 3: Direct URL Navigation
1. Copy the URL when on section 4: `http://localhost:8501/?page=lesson&lesson_id=<uuid>&block_index=3`
2. Open a new browser tab
3. Paste the URL
4. **Expected**: Opens directly to section 4 of the lesson
5. **Actual**: ____________________

### Test Case 4: Quiz Navigation
1. Navigate through all sections to the quiz
2. **Verify URL shows**: `?page=lesson&lesson_id=<uuid>&block_index=<last_index>`
3. Refresh the page
4. **Expected**: Still showing the quiz, not back to section 1
5. **Actual**: ____________________

### Test Case 5: URL Cleanup on Exit
1. While viewing a lesson, click "🔙 Back to Lessons"
2. **Verify URL shows**: `?page=learning` (no lesson_id or block_index)
3. **Expected**: Back at lesson list, no orphaned URL parameters
4. **Actual**: ____________________

## Success Criteria

✅ All test cases pass
✅ URL updates correctly as user navigates
✅ Refresh preserves current section
✅ Browser back/forward works correctly
✅ Direct URL sharing works
✅ No console errors

## Rollback Plan

If issues occur, revert these commits:
- app.py lines 108-114, 129-131
- lesson_viewer.py lines 314, 317-321, 682-688, 695-701, 707-713
