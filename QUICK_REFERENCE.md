# 🚀 Quick Reference: Batch Lesson Generation

## ⚡ Super Quick Start

### 1. Get API Key
```
https://console.anthropic.com/ → Create API Key
```

### 2. Set Environment Variable
**Windows:**
```cmd
set ANTHROPIC_API_KEY=your-key-here
```

**Linux/Mac:**
```bash
export ANTHROPIC_API_KEY='your-key-here'
```

### 3. Run Generation
**Windows:**
```cmd
generate_lessons_quick_start.bat
```

**Linux/Mac:**
```bash
./generate_lessons_quick_start.sh
```

## 📋 What Gets Generated

- **228 lessons** across 15 domains
- **~4,000-6,000 words** per lesson
- **Complete JSON** with all required fields
- **Cost:** ~$30-40 total
- **Time:** 6-12 hours (unattended)

## 📁 Output Files

```
content/
├── lesson_malware_22_static_malware_analysis_RICH.json
├── lesson_malware_23_dynamic_malware_analysis_RICH.json
├── lesson_pentest_15_web_app_penetration_testing_RICH.json
├── lesson_dfir_72_windows_memory_forensics_RICH.json
└── ... (228 total files)

batch_generation_status.json  ← Progress tracker
```

## 🔍 Check Progress

```bash
# View status
cat batch_generation_status.json

# Count generated lessons
ls content/*.json | wc -l

# Check for failures
grep "failed" batch_generation_status.json
```

## ✅ After Generation

### 1. Validate
```bash
python scripts/validate_lesson_compliance.py
```

### 2. Load to Database
```bash
python scripts/sync_lessons.py
```

### 3. Test in App
```bash
streamlit run app.py
```

### 4. Update CSV
Mark lessons as "completed" in lesson_ideas.csv

### 5. Deploy
```bash
git add content/*.json
git commit -m "Add 228 new lessons via batch generation"
git push

# On VM:
bash update_vm.sh
```

## 🐛 Troubleshooting

### "API Key not set"
```bash
echo $ANTHROPIC_API_KEY  # Check if set
export ANTHROPIC_API_KEY='your-key'  # Set it
```

### "Module not found: anthropic"
```bash
pip install anthropic
```

### "Rate limit exceeded"
- Wait 60 seconds and retry
- Or increase sleep time in script (line 215)

### JSON Parse Errors
- Check `debug_lesson_XXX.txt` files
- Review API response
- Regenerate specific lesson

## 📊 Domains Being Generated

| Domain | Lessons | Priority |
|--------|---------|----------|
| AI Security | 46 | 🔴 Highest |
| Pentest | 27 | 🔴 High |
| DFIR | 26 | 🔴 High |
| Fundamentals | 20 | 🟡 Medium |
| Malware | 18 | 🟡 Medium |
| System | 18 | 🟡 Medium |
| Red Team | 11 | 🟢 Lower |
| Cloud | 11 | 🟢 Lower |
| Others | 51 | 🟢 Lower |

## 💰 Cost Breakdown

| Item | Amount |
|------|--------|
| Per Lesson | ~$0.13 |
| 228 Lessons | ~$30-40 |
| Time per Lesson | ~3 minutes |
| Total Time | ~11 hours |

## 🎯 Success Metrics

**Target:**
- ✅ 95%+ success rate
- ✅ All required fields present
- ✅ Valid JSON structure
- ✅ 4,000+ words per lesson
- ✅ "Teach Me Like I'm 10" section

**Review Sample:**
- Check 10 random lessons
- Verify technical accuracy
- Test assessments

## 📞 Get Help

1. **Read documentation:**
   - BATCH_GENERATION_README.md
   - SESSION_SUMMARY.md

2. **Check status:**
   - batch_generation_status.json

3. **Debug failures:**
   - debug_lesson_*.txt files

4. **Test single lesson:**
   - Use /lesson-generator skill in Claude Code

## ⏭️ Next Session

**If generation complete:**
- ✅ Validate all lessons
- ✅ Load to database
- ✅ Test in Streamlit
- ✅ Get user feedback
- ✅ Iterate on quality

**If generation failed:**
- Review failures
- Fix issues
- Regenerate failed lessons
- Adjust script parameters

---

**🎉 You're ready to generate 228 lessons!**

Just run: `./generate_lessons_quick_start.sh`
