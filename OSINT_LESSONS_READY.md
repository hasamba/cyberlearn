# OSINT Lessons - Ready to Load

## Summary

All 5 OSINT lessons have been fixed and are ready to load into the database. The validation errors have been resolved.

## What Was Fixed

### Validation Errors Resolved:

1. **Missing post_assessment fields**
   - Added `question_id` (UUID) to all questions
   - Added `type` field (set to `multiple_choice`) to all questions

2. **Invalid jim_kwik_principles**
   - Replaced invalid enum values with valid ones:
     - `spaced_repetition` → `learning_sprint`
     - `visualization` → `memory_hooks`
     - `real_world_application` → `connect_to_what_i_know`
     - `mistakes_as_learning` → `reframe_limiting_beliefs`
     - `teach_others` → `teach_like_im_10`
     - `chunking_information` → `minimum_effective_dose`

### Files Fixed:

1. `content/lesson_osint_01_fundamentals_ethics_RICH.json` ✓
2. `content/lesson_osint_02_google_dorking_RICH.json` ✓
3. `content/lesson_osint_03_social_media_intelligence_RICH.json` ✓
4. `content/lesson_osint_04_dns_infrastructure_RICH.json` ✓
5. `content/lesson_osint_05_shodan_iot_search_RICH.json` ✓

### New Tool Created:

- `fix_osint_lessons.py` - Automated script to fix OSINT lesson validation errors

## What to Run on Your VM

### Step 1: Pull Latest Changes

```bash
cd /path/to/cyberlearn
git pull
```

### Step 2: Load Lessons into Database

```bash
python load_all_lessons.py
```

**Expected Output:**
```
Loading lessons from content/...
Loaded lesson_osint_01_fundamentals_ethics_RICH.json
Loaded lesson_osint_02_google_dorking_RICH.json
Loaded lesson_osint_03_social_media_intelligence_RICH.json
Loaded lesson_osint_04_dns_infrastructure_RICH.json
Loaded lesson_osint_05_shodan_iot_search_RICH.json
...
Successfully loaded X lessons
```

### Step 3: Verify OSINT Lessons in Database

```bash
sqlite3 cyberlearn.db "SELECT lesson_id, title, domain FROM lessons WHERE domain='osint' ORDER BY order_index;"
```

**Expected Output:**
```
a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d|OSINT Fundamentals & Ethics|osint
[4 more OSINT lessons]
```

### Step 4: Start Streamlit App

```bash
streamlit run app.py
```

### Step 5: Verify in UI

1. Go to "My Learning" page
2. You should now see the "OSINT" tab
3. Click on the OSINT tab
4. You should see all 5 OSINT lessons listed:
   - OSINT Fundamentals & Ethics
   - Google Dorking & Advanced Search
   - Social Media Intelligence (SOCMINT)
   - DNS & Infrastructure OSINT
   - Shodan & IoT Search Engines

## Current Status

- ✅ **5 OSINT lessons created** (lessons 1-5)
- ✅ **All validation errors fixed**
- ✅ **Domain added to adaptive_engine.py**
- ✅ **Domain added to models/user.py**
- ✅ **Migration script created** (add_osint_threat_hunting_domains.py)
- ✅ **UI updated** (dashboard.py, diagnostic.py, lesson_viewer.py)
- ✅ **All changes committed and pushed to git**

## Next Steps (Future Work)

### Remaining OSINT Lessons (5 more needed):

6. **Email & Identity OSINT** - Hunter.io, Have I Been Pwned, email formats
7. **Image & Geolocation OSINT** - EXIF data, reverse image search, geolocation
8. **Maltego & Relationship Mapping** - Graph analysis, transform usage
9. **Darknet & Paste Site Monitoring** - Tor, breach forums, paste monitoring
10. **OSINT Automation & Frameworks** - Recon-ng, SpiderFoot, custom scripts

### Threat Hunting Domain (10 lessons needed):

1. **Threat Hunting Fundamentals** - Hypothesis-driven hunting, MITRE ATT&CK
2. **Threat Hunting Methodologies** - Crown Jewels Analysis, TTP-based hunting
3. **Windows Event Log Analysis** - Sysmon, event IDs, PowerShell logging
4. **Network Traffic Analysis for Hunters** - Zeek logs, C2 detection
5. **Memory Forensics for Threat Hunting** - Volatility, in-memory malware
6. **Endpoint Detection & Response (EDR)** - CrowdStrike, Carbon Black, Defender ATP
7. **Threat Intelligence Integration** - IOC feeds, TIP platforms, automated enrichment
8. **Advanced Persistent Threat (APT) Hunting** - APT techniques, long-term persistence
9. **Hunting with SIEM & Data Lakes** - Splunk/ELK hunting queries, anomaly detection
10. **Purple Team Exercises** - Collaborative red/blue team threat hunting

## Troubleshooting

### If OSINT lessons still don't load:

1. **Check for validation errors:**
   ```bash
   python load_all_lessons.py 2>&1 | grep -A 5 "osint"
   ```

2. **Run comprehensive_fix.py (if needed):**
   ```bash
   python comprehensive_fix.py
   python load_all_lessons.py
   ```

3. **Check database directly:**
   ```bash
   sqlite3 cyberlearn.db
   SELECT COUNT(*) FROM lessons WHERE domain='osint';
   .exit
   ```

### If OSINT tab doesn't show in UI:

1. **Verify lesson_viewer.py has OSINT:**
   ```bash
   grep -n "osint" ui/pages/lesson_viewer.py
   ```
   Should show line with `("osint", "OSINT")`

2. **Restart Streamlit:**
   ```bash
   # Stop streamlit (Ctrl+C)
   streamlit run app.py
   ```

3. **Clear browser cache** and refresh

## Git Commit Log

```
a236be2 Fix OSINT lesson validation errors
91b2cae Add OSINT and Threat Hunting tabs to My Learning page
2aa2bfa Add OSINT and Threat Hunting domains to UI
3681f7a Fix post_assessment difficulty validation in 5 OSINT lessons
81e8cd6 Fix estimated_time validation errors in 8 pentest lessons
```

## Success Criteria

You'll know everything worked when:

- ✅ `python load_all_lessons.py` completes without OSINT-related errors
- ✅ Database shows 5 OSINT lessons: `SELECT COUNT(*) FROM lessons WHERE domain='osint';` returns 5
- ✅ OSINT tab appears in My Learning page
- ✅ All 5 OSINT lessons are visible and clickable
- ✅ Opening an OSINT lesson shows full content with videos, exercises, assessments

---

**All changes committed:** a236be2 (Fix OSINT lesson validation errors)
**Pushed to:** https://github.com/hasamba/cyberlearn.git
**Date:** 2025-10-29
