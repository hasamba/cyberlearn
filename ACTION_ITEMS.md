# CyberLearn - Action Items Summary

## Immediate Actions (Run on VM)

### 1. Sync Database (Remove deleted lessons)
```bash
python sync_database.py
```
This will show you which lessons are in the database but no longer have files, and ask if you want to delete them.

### 2. Load OSINT Lessons (5 lessons waiting)
```bash
python reload_osint_simple.py
```
This will load the 5 OSINT lessons that are fixed and ready.

### 3. Verify Current State
```bash
python list_lessons.py
```
This will show all lessons by domain and counts.

---

## Creating New Lessons with ChatGPT

### Quick Start:

1. **Open** [`CHATGPT_LESSON_PROMPT.md`](CHATGPT_LESSON_PROMPT.md)
2. **Copy** the full prompt template
3. **Fill in** the bracketed sections with your lesson details:
   - Domain (osint, threat_hunting, red_team, etc.)
   - Lesson number and title
   - Difficulty (1-3)
   - Concepts to cover
4. **Paste** into ChatGPT
5. **Save** output to `content/lesson_[domain]_[number]_[title]_RICH.json`
6. **Run** `python comprehensive_fix.py` to fix any validation errors
7. **Commit and push** to git
8. **On VM**: `git pull` then `python load_all_lessons.py`

### Example for Next Lesson (OSINT 6):

```
[Copy from CHATGPT_LESSON_PROMPT.md and fill in:]

**Domain**: osint
**Lesson Number**: 6
**Title**: Email & Username Intelligence
**Difficulty**: 2
**Order Index**: 6
**Prerequisites**: ["84542765-253e-4b68-b230-3abfb6d16f54", "0f402fa2-4c57-4fb4-a93a-530a4b1ec4db"]
**Estimated Time**: 50 minutes
**Concepts to Cover**:
- Email format enumeration (Hunter.io, RocketReach)
- Username OSINT (Sherlock, WhatsMyName)
- Have I Been Pwned integration
- Email header analysis and tracking
- Disposable email detection
- Professional email intelligence
```

[Then paste the full prompt template below this]

---

## Current Lesson Priorities

### Priority 1: OSINT Domain (5 more lessons needed)
- **Status**: 5 lessons ready to load, need 5 more (6-10)
- **Next lessons**: Email OSINT, Image/Geolocation, Maltego, Dark Web, Automation
- **See**: [`NEXT_LESSONS_PLAN.md`](NEXT_LESSONS_PLAN.md) for detailed outlines

### Priority 2: Threat Hunting Domain (10 lessons needed)
- **Status**: Domain infrastructure exists, NO lessons created yet
- **Next lessons**: All 10 lessons (Fundamentals → Purple Team)
- **See**: [`NEXT_LESSONS_PLAN.md`](NEXT_LESSONS_PLAN.md) for detailed outlines

### Priority 3: Red Team Consolidation
- **Status**: Two domains (red_team: 5, redteam: 7) need merging
- **Action**: Audit, consolidate, add 1-5 more to reach 12 total

---

## Quick Reference Files

| File | Purpose |
|------|---------|
| [`CHATGPT_LESSON_PROMPT.md`](CHATGPT_LESSON_PROMPT.md) | Full prompt template for ChatGPT lesson creation |
| [`NEXT_LESSONS_PLAN.md`](NEXT_LESSONS_PLAN.md) | Detailed plan for next 18-20 lessons |
| [`CLAUDE.md`](CLAUDE.md) | Full project documentation and guidelines |
| [`OSINT_LESSONS_READY.md`](OSINT_LESSONS_READY.md) | OSINT lessons deployment guide |

---

## Utility Scripts

### On Windows (your host):
- `python comprehensive_fix.py` - Fix validation errors in all lessons
- `python regenerate_osint_uuids.py` - Regenerate UUIDs for OSINT lessons
- `python fix_osint_lessons.py` - Fix OSINT validation issues

### On VM (production):
- `python list_lessons.py` - List all lessons by domain
- `python sync_database.py` - Remove orphaned lessons from database
- `python reload_osint_simple.py` - Force reload OSINT lessons
- `python force_load_domain.py [domain]` - Force reload any domain
- `python diagnose_osint.py` - Diagnose OSINT loading issues
- `python load_all_lessons.py` - Load all lessons from content/

---

## Workflow Summary

### Creating a Single Lesson:

```
1. Use ChatGPT with prompt template → Generate JSON
2. Save to content/lesson_[domain]_[number]_[title]_RICH.json
3. Run: python comprehensive_fix.py
4. Commit: git add content/ && git commit -m "Add [title]" && git push
5. On VM: git pull && python load_all_lessons.py
6. Verify: python list_lessons.py
```

### Creating a Batch (3-5 lessons):

```
1. Generate 3-5 lessons with ChatGPT
2. Save all to content/ directory
3. Run: python comprehensive_fix.py (fixes all at once)
4. Commit: git add content/ && git commit -m "Add [domain] lessons 6-10" && git push
5. On VM: git pull && python force_load_domain.py [domain]
6. Verify: python list_lessons.py
```

---

## Current Status

**Last Updated**: 2025-10-29

**Total Lessons**: 108 lessons (after sync)

**Domains Complete** (8-12 lessons):
- ✅ active_directory (11)
- ✅ blueteam (11)
- ✅ cloud (10)
- ✅ dfir (11)
- ✅ fundamentals (11)
- ✅ linux (13)
- ✅ malware (10)
- ✅ pentest (9)
- ✅ system (10)

**Domains Incomplete**:
- ⚠️ **osint** (0 in DB, 5 ready to load, need 5 more)
- ⚠️ **red_team** (5 lessons, need 3-7 more)
- ⚠️ **redteam** (7 lessons, consolidate with red_team)
- ❌ **threat_hunting** (0 lessons, need 8-12)

**Target**: 130-140 lessons across 12 domains

---

## Git Repository

**Current Branch**: main
**Remote**: https://github.com/hasamba/cyberlearn.git

**Recent Commits**:
- Add ChatGPT lesson prompt template
- Add comprehensive next lessons plan
- Add database sync script
- Regenerate unique UUIDs for OSINT lessons
- Fix OSINT lesson validation errors

---

## Questions or Issues?

1. **OSINT lessons not loading**: Run `python diagnose_osint.py`
2. **Validation errors**: Run `python comprehensive_fix.py`
3. **Database out of sync**: Run `python sync_database.py`
4. **Need lesson examples**: Check `content/lesson_*_RICH.json` files
5. **ChatGPT prompt unclear**: See [`CHATGPT_LESSON_PROMPT.md`](CHATGPT_LESSON_PROMPT.md)

---

## Next Session Checklist

- [ ] Run `python sync_database.py` on VM
- [ ] Run `python reload_osint_simple.py` on VM
- [ ] Verify with `python list_lessons.py`
- [ ] Create OSINT lesson 6 with ChatGPT
- [ ] Decide: Continue OSINT or start Threat Hunting?
