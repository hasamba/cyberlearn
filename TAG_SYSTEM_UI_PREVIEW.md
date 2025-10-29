# Tag System - UI Preview

## Visual Overview of Tag System Interface

This document shows what the tag system looks like in the CyberLearn UI.

---

## 1. Navigation - Sidebar

```
┌─────────────────────────────────┐
│  🛡️ CyberLearn                  │
├─────────────────────────────────┤
│  Welcome, yaniv!                │
│  Level 5 - Advanced             │
│                                 │
│  Progress to Next Level         │
│  ████████░░░░░░░░░ 65%          │
│  14,250 XP / 22,000 XP          │
│                                 │
│  🔥 7 Day Streak                │
├─────────────────────────────────┤
│  🏠 Dashboard                   │
│  📚 My Learning                 │
│  👤 Profile                     │
│  🏆 Achievements                │
│  🏷️ Manage Tags        ← NEW!  │
├─────────────────────────────────┤
│  🚪 Logout                      │
└─────────────────────────────────┘
```

---

## 2. Tag Management Page

### View Tags Tab

```
┌──────────────────────────────────────────────────────────────────┐
│  Tag Management                                                   │
│  Organize lessons with colored tags for easy filtering            │
├──────────────────────────────────────────────────────────────────┤
│  [View Tags] [Create Tag] [Tag Statistics]                       │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  All Tags                                                         │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐    │
│  │ 🔵 Built-In    │  │ 🟣 Advanced    │  │ 🔴 PWK Course  │    │
│  │ Core platform  │  │ High difficulty│  │ OSCP aligned   │    │
│  │ 🔒 System Tag  │  │ 🔒 System Tag  │  │ 🔒 System Tag  │    │
│  └────────────────┘  └────────────────┘  └────────────────┘    │
│                                                                   │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐    │
│  │ 🟠 Eric Z Tools│  │ 🟢 SANS-Aligned│  │ ⚪ User Content│    │
│  │ Forensic tools │  │ SANS courses   │  │ User created   │    │
│  │ 🔒 System Tag  │  │ 🔒 System Tag  │  │ 🔒 System Tag  │    │
│  └────────────────┘  └────────────────┘  └────────────────┘    │
│                                                                   │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐    │
│  │ 🩷 Community   │  │ 🏆 Cert Prep   │  │ 🎯 My Course   │    │
│  │ Community made │  │ Certification  │  │ Custom course  │    │
│  │ 🔒 System Tag  │  │ 🔒 System Tag  │  │ ✏️ Custom Tag  │    │
│  │                │  │                │  │ [Edit] [Delete]│    │
│  └────────────────┘  └────────────────┘  └────────────────┘    │
└──────────────────────────────────────────────────────────────────┘
```

### Create Tag Tab

```
┌──────────────────────────────────────────────────────────────────┐
│  Create New Tag                                                   │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Tag Name*                                                        │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ e.g., My Course, HTB Challenges                            │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  Color*                                                           │
│  ┌──────┐                                                        │
│  │ 🎨   │  #3B82F6                                              │
│  └──────┘                                                        │
│                                                                   │
│  Icon (emoji)                                                     │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 🏷️                                                          │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  Description                                                      │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ What does this tag represent?                              │ │
│  │                                                             │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  [Create Tag]                                                     │
│                                                                   │
│  ─────────────────────────────────────────────────────────────  │
│  Tag Best Practices                                               │
│  • Use clear names: "PWK Course" instead of "PWK"               │
│  • Choose distinct colors: Make tags distinguishable            │
│  • Add descriptions: Help others understand tag purpose         │
└──────────────────────────────────────────────────────────────────┘
```

### Tag Statistics Tab

```
┌──────────────────────────────────────────────────────────────────┐
│  Tag Usage Statistics                                             │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Built-In        ████████████████████████████████████ 140       │
│  Advanced        ████████████████░░░░░░░░░░░░░░░░░░  45        │
│  PWK Course      ████████████░░░░░░░░░░░░░░░░░░░░░░  32        │
│  Eric Z Tools    ██████████░░░░░░░░░░░░░░░░░░░░░░░░  28        │
│  SANS-Aligned    ████████░░░░░░░░░░░░░░░░░░░░░░░░░░  21        │
│  Cert Prep       ██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░  18        │
│  User Content    ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  12        │
│  Community       ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   5        │
│                                                                   │
│  ─────────────────────────────────────────────────────────────  │
│  Detailed Breakdown                                               │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 🔵 Built-In: 140 lessons                                   │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 🟣 Advanced: 45 lessons                                    │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 🔴 PWK Course: 32 lessons                                  │ │
│  └────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

---

## 3. Lesson Browser with Tags

### Filter Controls

```
┌──────────────────────────────────────────────────────────────────┐
│  📚 Browse Lessons                                                │
├──────────────────────────────────────────────────────────────────┤
│  Filter by Tags                                                   │
│                                                                   │
│  Select tags to filter lessons:                                  │
│  ┌────────────────────────────────────────┐  ┌──────────────┐  │
│  │ 🔵 Built-In        ▼                   │  │ ☐ Match ALL  │  │
│  │ 🟣 Advanced                            │  │   tags       │  │
│  │ 🔴 PWK Course                          │  └──────────────┘  │
│  │ (select multiple...)                   │                     │
│  └────────────────────────────────────────┘                     │
│                                                                   │
│  Active Filters:                                                  │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐              │
│  │🔵 Built-In  │ │🟣 Advanced  │ │🔴 PWK Course│              │
│  └─────────────┘ └─────────────┘ └─────────────┘              │
└──────────────────────────────────────────────────────────────────┘
```

### Lesson Cards with Tags

```
┌──────────────────────────────────────────────────────────────────┐
│  Found 32 lessons                                                 │
├──────────────────────────────────────────────────────────────────┤
│  📂 DFIR (12 lessons)                           [Expanded ▼]     │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Windows Registry Forensics                                │ │
│  │  Domain: DFIR | Difficulty: ⭐⭐ | Time: 45 min            │ │
│  │  ┌───────────┐ ┌───────────┐ ┌──────────────┐            │ │
│  │  │🔵 Built-In│ │🟣 Advanced│ │🔴 PWK Course │            │ │
│  │  └───────────┘ └───────────┘ └──────────────┘            │ │
│  │                                                 ✅          │ │
│  │                                             Completed       │ │
│  │  [📖 Review Lesson]                                        │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  MFT Timeline Analysis                                     │ │
│  │  Domain: DFIR | Difficulty: ⭐⭐⭐ | Time: 60 min          │ │
│  │  ┌───────────┐ ┌───────────────┐ ┌──────────────┐        │ │
│  │  │🔵 Built-In│ │🟠 Eric Z Tools│ │🟢 SANS-Aligned│       │ │
│  │  └───────────┘ └───────────────┘ └──────────────┘        │ │
│  │                                                 🟡          │ │
│  │                                            In Progress      │ │
│  │  [▶️ Continue Lesson]                                      │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Volatility 3 Memory Forensics                            │ │
│  │  Domain: DFIR | Difficulty: ⭐⭐⭐ | Time: 60 min          │ │
│  │  ┌───────────┐ ┌───────────┐ ┌──────────────┐            │ │
│  │  │🔵 Built-In│ │🟣 Advanced│ │🟢 SANS-Aligned│           │ │
│  │  └───────────┘ └───────────┘ └──────────────┘            │ │
│  │                                                 🔵          │ │
│  │                                             Not Started     │ │
│  │  [🚀 Start Lesson]                                         │ │
│  └────────────────────────────────────────────────────────────┘ │
├──────────────────────────────────────────────────────────────────┤
│  📂 Pentest (8 lessons)                         [Collapsed ▶]   │
├──────────────────────────────────────────────────────────────────┤
│  📂 Red Team (12 lessons)                       [Collapsed ▶]   │
└──────────────────────────────────────────────────────────────────┘
```

---

## 4. My Learning Page - View Mode Selector

```
┌──────────────────────────────────────────────────────────────────┐
│  📚 My Learning                                                   │
├──────────────────────────────────────────────────────────────────┤
│  View Mode:  ◉ 📂 By Domain    ○ 🏷️ By Tags                    │
│  ─────────────────────────────────────────────────────────────  │
│                                                                   │
│  [When "By Domain" selected: Shows domain tabs]                  │
│  [When "By Tags" selected: Shows tag-based browser above]        │
└──────────────────────────────────────────────────────────────────┘
```

---

## 5. Tag System in Action - Example Workflow

### Scenario: User wants to find all PWK Course lessons

**Step 1**: Click 📚 My Learning

**Step 2**: Toggle to 🏷️ By Tags view

**Step 3**: Select "PWK Course" tag from dropdown

**Result**:
```
┌──────────────────────────────────────────────────────────────────┐
│  Found 32 lessons                                                 │
│                                                                   │
│  Active Filters: ┌──────────────┐                                │
│                  │🔴 PWK Course │                                │
│                  └──────────────┘                                │
│                                                                   │
│  All 32 PWK-aligned lessons displayed across domains:            │
│  • DFIR: 8 lessons                                               │
│  • Pentest: 12 lessons                                           │
│  • Red Team: 10 lessons                                          │
│  • Active Directory: 2 lessons                                   │
│                                                                   │
│  Each lesson card shows:                                          │
│  • Colored tag badges                                             │
│  • Progress status (completed/in-progress/not started)           │
│  • Domain, difficulty, time                                       │
│  • Action button (start/continue/review)                          │
└──────────────────────────────────────────────────────────────────┘
```

---

## 6. Color Scheme Reference

### System Tag Colors

- 🔵 **Blue (#3B82F6)**: Built-In (default platform content)
- 🟣 **Purple (#8B5CF6)**: Advanced (high difficulty)
- 🔴 **Red (#EF4444)**: PWK Course (OSCP prep)
- 🟠 **Orange (#F59E0B)**: Eric Zimmerman Tools
- 🟢 **Green (#10B981)**: SANS-Aligned
- ⚪ **Gray (#6B7280)**: User Content
- 🩷 **Pink (#EC4899)**: Community
- 🏆 **Teal (#14B8A6)**: Certification Prep

### Custom Tags
Users can choose any hex color for custom tags, with recommended distinct colors:
- 🟡 Yellow (#FBBF24)
- 🔵 Cyan (#06B6D4)
- 💜 Violet (#A855F7)
- 🟤 Brown (#92400E)

---

## 7. Mobile/Responsive View

Tag badges stack vertically on narrow screens:

```
┌──────────────────────┐
│ Lesson Title         │
│                      │
│ 🔵 Built-In          │
│ 🟣 Advanced          │
│ 🔴 PWK Course        │
│                      │
│ Status: ✅ Completed │
│ [Review]             │
└──────────────────────┘
```

---

## 8. Empty States

### No Tags Available
```
┌──────────────────────────────────────────────────────────────────┐
│  No tags available. Visit the Tag Management page to create tags.│
│  [Go to Tag Management]                                           │
└──────────────────────────────────────────────────────────────────┘
```

### No Lessons Match Filter
```
┌──────────────────────────────────────────────────────────────────┐
│  ⚠️ No lessons match the selected tags.                          │
│                                                                   │
│  Try:                                                             │
│  • Selecting different tags                                       │
│  • Unchecking "Match ALL tags"                                   │
│  • Clearing filters to see all lessons                           │
└──────────────────────────────────────────────────────────────────┘
```

---

## Summary

The tag system provides:

1. **Visual Organization**: Colored badges make tags immediately recognizable
2. **Flexible Filtering**: Multi-select with AND/OR logic
3. **Easy Management**: Full CRUD interface for tags
4. **Statistics**: Track tag usage across lessons
5. **Seamless Integration**: Works alongside existing domain view

**Navigation Flow:**
```
Login → Sidebar → 🏷️ Manage Tags → Create/Edit tags
                → 📚 My Learning → 🏷️ By Tags → Filter → Browse → Start Lesson
```

**User Benefits:**
- Find lessons faster with multi-dimensional filtering
- Organize personal learning paths
- Track certification prep progress
- Browse community/user content separately
- See advanced content at a glance

---

**Ready to use? Run the migration and see it in action!**

```bash
python add_tags_system.py
streamlit run app.py
```
