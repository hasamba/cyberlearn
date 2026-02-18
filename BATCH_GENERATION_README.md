# Batch Lesson Generation Guide

This guide explains how to automatically generate the remaining 228 planned lessons using the Anthropic Claude API.

## Overview

The `batch_generate_lessons.py` script:
- ✅ Reads lesson specifications from `lesson_ideas.csv`
- ✅ Generates comprehensive 4,000-6,000 word lessons
- ✅ Validates all required fields
- ✅ Saves lessons to `content/` directory
- ✅ Tracks progress and handles failures gracefully
- ✅ Supports resume after interruption

## Prerequisites

### 1. Get Anthropic API Key

1. Sign up at https://console.anthropic.com/
2. Generate an API key
3. Note: You'll need API credits (~$50-100 for 228 lessons)

### 2. Set Environment Variable

**Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY = "your-api-key-here"
```

**Windows (Command Prompt):**
```cmd
set ANTHROPIC_API_KEY=your-api-key-here
```

**Linux/Mac:**
```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

**Persistent (add to .bashrc/.zshrc):**
```bash
echo 'export ANTHROPIC_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

### 3. Install Anthropic SDK

```bash
pip install anthropic
```

## Usage

### Run Batch Generation

```bash
cd "path/to/57.14_Learning_app"
python batch_generate_lessons.py
```

### What Happens

1. Script analyzes `lesson_ideas.csv`
2. Shows summary of lessons to generate
3. Asks for confirmation
4. Generates lessons one by one (with progress updates)
5. Saves each lesson as JSON in `content/` directory
6. Tracks progress in `batch_generation_status.json`

### Output

```
================================================================================
CyberLearn Batch Lesson Generator
================================================================================

Found 228 planned lessons
Already completed: 5
Failed: 0
To generate: 223

Lessons by domain:
  ai_security: 46 lessons
  pentest: 27 lessons
  dfir: 26 lessons
  ...

================================================================================
Start batch generation? (yes/no): yes

================================================================================
Generating lessons...
================================================================================

[1/228] Domain: malware
  ⚙ Generating lesson #602: Static Malware Analysis with IDA Pro
    ✓ Saved: lesson_malware_22_static_malware_analysis_RICH.json

[2/228] Domain: malware
  ⚙ Generating lesson #603: Dynamic Malware Analysis Sandbox Setup
    ✓ Saved: lesson_malware_23_dynamic_malware_analysis_RICH.json

...

--- Progress: 10/228 (4%) ---
    Success: 9, Failed: 1

...

================================================================================
BATCH GENERATION COMPLETE
================================================================================
Total lessons processed: 228
Successfully generated: 225
Failed: 3
Success rate: 98%

Lesson files saved to: content/
```

## Progress Tracking

The script creates `batch_generation_status.json`:

```json
{
  "completed": ["602", "603", "604", ...],
  "failed": ["650"],
  "skipped": []
}
```

### Resume After Interruption

If the script is interrupted:
- Progress is saved automatically
- Re-run the script - it will skip completed lessons
- Only generates remaining lessons

### Handle Failed Lessons

If a lesson fails:
- Check `debug_lesson_<number>.txt` for the API response
- Review the error message
- Fix the issue (if needed)
- Remove the lesson number from `failed` array in status file
- Re-run the script

## Estimated Costs

**Anthropic Claude Sonnet 4 Pricing:**
- Input: $3.00 / million tokens
- Output: $15.00 / million tokens

**Per Lesson Estimate:**
- Input: ~2,000 tokens (prompt)
- Output: ~8,000 tokens (lesson content)
- Cost per lesson: ~$0.13

**Total for 228 Lessons:**
- Total cost: ~$30-40
- Time: 6-12 hours (with rate limiting)

**Note:** Actual costs may vary based on lesson complexity.

## Advanced Options

### Generate Specific Domains Only

Edit the script to filter lessons:

```python
# In main(), after loading lessons:
lessons = [l for l in lessons if l['domain'] in ['malware', 'pentest']]
```

### Adjust Rate Limiting

Change the sleep time between requests:

```python
# In main(), after generate_lesson():
time.sleep(2)  # Change to 1 for faster, 5 for safer
```

### Change Model

Use a different Claude model:

```python
# In generate_lesson():
message = client.messages.create(
    model="claude-opus-4-20250514",  # More expensive, higher quality
    # OR
    model="claude-haiku-4-20250318",  # Cheaper, faster, less detailed
    ...
)
```

## Quality Assurance

### After Generation

1. **Review Sample Lessons:**
   - Check 5-10 random lessons for quality
   - Verify content structure
   - Ensure technical accuracy

2. **Validate All Lessons:**
   ```bash
   python scripts/validate_lesson_compliance.py
   ```

3. **Load into Database:**
   ```bash
   python scripts/sync_lessons.py
   ```

4. **Test in Streamlit:**
   ```bash
   streamlit run app.py
   ```

### Known Issues

**Issue:** JSON parsing errors
- **Cause:** API returns markdown-wrapped JSON
- **Fix:** Script automatically strips markdown, check debug file

**Issue:** Missing required fields
- **Cause:** API didn't generate complete JSON
- **Fix:** Regenerate that specific lesson

**Issue:** Rate limits
- **Cause:** Too many requests
- **Fix:** Increase sleep time between requests

## Manual Alternative

If batch generation fails, you can still use the lesson-generator skill manually:

```bash
# In Claude Code session
/lesson-generator

# Then provide lesson specification from lesson_ideas.csv
```

## Troubleshooting

### "Module not found: anthropic"

```bash
pip install anthropic
```

### "ANTHROPIC_API_KEY not set"

Check environment variable:
```bash
echo $ANTHROPIC_API_KEY  # Linux/Mac
echo %ANTHROPIC_API_KEY%  # Windows CMD
$env:ANTHROPIC_API_KEY   # Windows PowerShell
```

### "API Error: Rate limit exceeded"

Wait a few minutes and retry, or increase sleep time in script.

### "Permission denied" on file save

Check that `content/` directory exists and is writable:
```bash
mkdir -p content
chmod 755 content  # Linux/Mac
```

## Next Steps After Generation

1. ✅ All 228 lessons generated
2. ✅ Validate with `validate_lesson_compliance.py`
3. ✅ Load into database with `sync_lessons.py`
4. ✅ Test in Streamlit app
5. ✅ Update `lesson_ideas.csv` status to "completed"
6. ✅ Commit to git repository
7. ✅ Deploy to VM with `update_vm.sh`

## Support

For issues or questions:
- Check debug_lesson_*.txt files
- Review batch_generation_status.json
- Inspect failed lesson specifications in lesson_ideas.csv
- Test single lesson generation with lesson-generator skill first
