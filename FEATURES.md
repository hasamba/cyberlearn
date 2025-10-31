# CyberLearn Platform - Master Features List

**Last Updated:** 2025-10-31
**Current Version:** 1.0
**Total Features Tracked:** 1 planned, 0 in progress, 8 completed

---

## How to Use This File

1. **Add new features** under the appropriate category
2. **Update status** as you work: `[ ]` → `[IN PROGRESS]` → `[✓]`
3. **Add notes** with implementation details, blockers, or decisions
4. **Link to PRs/commits** when features are completed
5. **Archive completed features** periodically to keep this file focused

---

## Status Legend

- `[ ]` - Planned (not started)
- `[IN PROGRESS]` - Currently being worked on
- `[✓]` - Completed
- `[BLOCKED]` - Blocked by dependency or issue
- `[DEFERRED]` - Postponed to future release

---

## Feature Categories

- [Content & Curriculum](#content--curriculum)
- [Learning Experience](#learning-experience)
- [Gamification & Engagement](#gamification--engagement)
- [User Management](#user-management)
- [Analytics & Reporting](#analytics--reporting)
- [Technical Infrastructure](#technical-infrastructure)
- [UI/UX Improvements](#uiux-improvements)
- [Integration & API](#integration--api)
- [Security & Privacy](#security--privacy)
- [Admin & Content Creation](#admin--content-creation)

---

## Content & Curriculum

### Lesson Content

- [✓] **Feature:** Add AI Security Domain
  - **Status:** COMPLETED 2025-10-31
  - **Priority:** High
  - **Description:** Create new "ai_security" domain in the platform to house AI/ML security lessons
  - **Completed:**
    - [✓] Added ai_security, iot_security, web3_security to SkillLevels model
    - [✓] Created database migration (add_emerging_tech_domains.py)
    - [✓] Added domains to UI (dashboard, lesson viewer)
    - [✓] Created 10 OWASP LLM Top 10 lessons (order_index 4-13)
    - [✓] Tagged all lessons with "Package: OWASP AI Top 10"
    - [✓] Updated documentation
  - **Commit:** PR #15 merged, commits 202df1a, 04915dd
  - **Result:** 13 AI Security lessons (3 foundation + 10 OWASP), fully integrated

---

## Learning Experience

### Adaptive Learning

- [✓] **Feature:** Enhanced User Skill Assessment Questionnaire
  - **Status:** COMPLETED 2025-10-31
  - **Priority:** High
  - **Description:** Redesign the new user onboarding assessment to accurately evaluate user skill levels across all domains, providing better initial lesson recommendations and adaptive learning paths
  - **Completed:**
    - [✓] Comprehensive assessment covering all 15 domains
    - [✓] Multiple choice question format (93 questions total)
    - [✓] Questions distributed across difficulty levels (40% beginner, 40% intermediate, 20% advanced)
    - [✓] Domain-specific diagnostic questions covering all 15 domains
    - [✓] Results processing:
      - [✓] Calculate skill level (0-100) for each domain
      - [✓] Weighted scoring by difficulty (Beginner 20%, Intermediate 40%, Advanced 40%)
      - [✓] Domain-by-domain breakdown with difficulty analysis
    - [✓] Results visualization:
      - [✓] Overall score percentage
      - [✓] Domain breakdown with expandable details
      - [✓] Skill level labels (Novice, Beginner, Intermediate, Advanced)
    - [✓] Option to retake assessment (accessible from sidebar)
    - [✓] Save results to database (user_assessments table)
    - [✓] Update user skill_levels based on assessment scores
  - **Technical Details:**
    - **Question pool**: 60-80 diagnostic questions total (5-7 per domain)
    - **Question difficulty**: Mix of beginner (40%), intermediate (40%), advanced (20%)
    - **Scoring algorithm**:
      - Beginner questions correct → Skill level 1-2
      - Intermediate questions correct → Skill level 3-4
      - Advanced questions correct → Skill level 5
      - Account for confidence levels (self-assessment)
    - **Database**:
      - `assessment_questions` table (domain, difficulty, question_text, options, correct_answer)
      - `user_assessments` table (user_id, assessment_date, domain_scores, recommendations)
    - **UI flow**:
      1. Welcome screen explaining assessment purpose
      2. Domain-by-domain questioning (progress bar)
      3. Results screen with visualizations
      4. Personalized learning path recommendations
      5. Start learning button
  - **Use Cases:**
    - New user onboarding: Establish baseline skill levels
    - Career changers: Identify transferable skills and gaps
    - Experienced professionals: Skip basics, jump to advanced content
    - Progress tracking: Retake assessment to measure improvement
    - Curriculum personalization: Adaptive recommendations based on assessment
  - **Question Examples:**
    - **Fundamentals**: "What is the difference between symmetric and asymmetric encryption?"
    - **DFIR**: "Which Volatility plugin would you use to analyze network connections in a memory dump?"
    - **Malware**: "What is the primary purpose of packing malware?"
    - **AD**: "What authentication protocol does Kerberoasting exploit?"
    - **Red Team**: "What is the main advantage of using domain fronting for C2?"
  - **Implementation:**
    - Database schema: assessment_questions, user_assessments, assessment_responses (3 tables)
    - 93 diagnostic questions across all 15 domains
    - UI: ui/pages/assessment.py (complete assessment flow)
    - Scoring: Weighted by difficulty + base percentage correct
    - Results saved to user_assessments table with JSON domain_scores
    - User skill_levels updated automatically after assessment
    - Accessible from sidebar "Skill Assessment" button
    - Replaces old diagnostic.py page
  - **User Flow:**
    1. Welcome screen with domain overview and tips
    2. Domain-by-domain assessment with progress bar
    3. 93 questions total (varies by domain: 7 for major, 5 for emerging)
    4. Results screen with overall score and domain breakdown
    5. Save button updates skill levels and stores assessment record
    6. Retake button allows reassessment anytime
  - **Commits:**
    - bddbdd3 (database schema and questions)
    - 732496b (UI completion)
  - **Result:** Fully functional comprehensive assessment covering all 15 domains with 93 questions

### Personalization

- [✓] **Feature:** Hide/Unhide Lessons with Management Page
  - **Status:** COMPLETED 2025-10-31
  - **Priority:** Medium
  - **Description:** Allow users to hide lessons from the main UI (lesson catalog, recommendations), with a dedicated "Hidden Lessons" page where users can view and unhide lessons
  - **Completed:**
    - [✓] Added "hidden" boolean column to lessons table (default: 0)
    - [✓] "Hide Lesson" button in lesson viewer
    - [✓] Hidden lessons excluded from:
      - [✓] Domain lesson lists (get_lessons_by_domain with include_hidden parameter)
      - [✓] Search results (with optional "Include hidden" toggle)
    - [✓] "Hidden Lessons" page accessible from sidebar navigation
    - [✓] Hidden lessons page shows:
      - [✓] List of all hidden lessons with title, domain, difficulty, order_index
      - [✓] "Unhide" button for each lesson
      - [✓] Bulk "Unhide All" button
      - [✓] Domain emoji and difficulty indicators
    - [✓] Count of hidden lessons displayed on page
  - **Technical Details:**
    - **Database:** Added `hidden` column (BOOLEAN, default 0) to lessons table via add_hidden_column.py
    - **UI components:**
      - Hidden Lessons page: ui/pages/hidden_lessons.py
      - Hide button: ui/pages/lesson_viewer.py (line 533-544)
      - Navigation: app.py (lines 166-168, 426-428)
    - **Filter logic:**
      - get_lessons_by_domain() checks for hidden column and excludes by default
      - Search page has optional "Include hidden lessons" checkbox
  - **Use Cases:**
    - User wants to focus on specific domains/topics
    - Remove outdated or irrelevant content from view
    - Temporarily hide completed lessons to reduce clutter
    - Hide user-imported lessons that don't fit learning path
  - **Commit:** fe5778a
  - **Files:**
    - add_hidden_column.py (migration script)
    - ui/pages/hidden_lessons.py (management page)
    - test_hide_functionality.py (test script)
    - utils/database.py (updated get_lessons_by_domain)
    - ui/pages/lesson_viewer.py (hide button)
    - ui/pages/search.py (include hidden toggle)
    - app.py (navigation integration)
  - **Result:** Fully functional hide/unhide system with 411 lessons initially visible
  - **Estimated Effort:** Completed in 1 day (as estimated)

### User Notes & Annotations

- [ ] **Feature:** Lesson User Notes with Rich Content Support
  - **Priority:** High
  - **Description:** Allow users to add personal notes throughout each lesson, with support for text, URLs, screenshots/images, and embedded videos. Notes are accessible on every page/section within a lesson, enabling progressive learning documentation
  - **Acceptance Criteria:**
    - [ ] Notes interface available on every lesson page/section
    - [ ] Rich content support:
      - [ ] Plain text notes (markdown support)
      - [ ] URL attachments (with link preview)
      - [ ] Screenshot/image uploads (drag-and-drop)
      - [ ] Embedded videos (YouTube, Vimeo, direct uploads)
      - [ ] Code snippets with syntax highlighting
    - [ ] Notes organization:
      - [ ] Timestamped entries (auto-saved)
      - [ ] Attached to specific lesson content blocks
      - [ ] Searchable across all lessons
      - [ ] Exportable (Markdown, PDF)
    - [ ] Notes UI features:
      - [ ] Collapsible notes panel (sidebar or bottom)
      - [ ] Add note button on each content block
      - [ ] Rich text editor (WYSIWYG)
      - [ ] Image paste from clipboard
      - [ ] Video URL embed with preview
    - [ ] Notes management:
      - [ ] Edit/delete existing notes
      - [ ] Filter notes by lesson, domain, date
      - [ ] Tag notes with custom labels
      - [ ] Pin important notes to top
    - [ ] Notes visibility:
      - [ ] Private (default) - only visible to user
      - [ ] Option to share notes with other users (future)
  - **Technical Details:**
    - **Database schema:**
      ```sql
      CREATE TABLE lesson_notes (
        note_id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        lesson_id TEXT NOT NULL,
        content_block_index INTEGER,  -- NULL for general lesson notes
        note_text TEXT,
        note_html TEXT,  -- rendered HTML for rich content
        attachments JSON,  -- Array of {type, url, filename}
        created_at TIMESTAMP,
        updated_at TIMESTAMP,
        is_pinned BOOLEAN DEFAULT FALSE,
        tags JSON,  -- Array of custom tag strings
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (lesson_id) REFERENCES lessons(lesson_id)
      );
      ```
    - **Attachments JSON structure:**
      ```json
      [
        {"type": "url", "url": "https://example.com", "title": "Resource"},
        {"type": "image", "url": "/uploads/notes/abc123.png", "filename": "screenshot.png"},
        {"type": "video", "url": "https://youtube.com/watch?v=xyz", "provider": "youtube"}
      ]
      ```
    - **API endpoints:**
      - `POST /api/lessons/{lesson_id}/notes` - Create note
      - `GET /api/lessons/{lesson_id}/notes` - Get all notes for lesson
      - `PUT /api/notes/{note_id}` - Update note
      - `DELETE /api/notes/{note_id}` - Delete note
      - `POST /api/notes/{note_id}/upload` - Upload image/file
      - `GET /api/users/{user_id}/notes` - Get all user notes across lessons
    - **File storage:**
      - Image uploads: `/uploads/notes/{user_id}/{note_id}/`
      - Max file size: 10MB per image, 100MB per video
      - Supported formats: PNG, JPG, GIF, MP4, MOV, AVI
    - **Rich text editor:** Consider using TipTap, Quill, or Streamlit's native markdown editor
    - **Video embedding:** Support YouTube, Vimeo, Loom with oEmbed API for previews
  - **Use Cases:**
    - **During learning:** User reads lesson on Kerberoasting, pastes commands they tried in lab, attaches screenshot of successful attack
    - **Resource collection:** User adds links to related blog posts, research papers, tool documentation
    - **Lab documentation:** User embeds video walkthrough of their CTF solution for future reference
    - **Study notes:** User summarizes key concepts in their own words, adds mnemonic devices
    - **Troubleshooting:** User documents errors encountered and solutions found
    - **Progress tracking:** User notes what they understood vs. what needs review
  - **UI/UX Considerations:**
    - **Notes panel placement:** Sidebar (desktop) or bottom sheet (mobile)
    - **Inline notes:** Small icon next to each content block to add contextual note
    - **Visual distinction:** Different background color for notes section
    - **Auto-save:** Save notes as user types (debounced, every 2 seconds)
    - **Image preview:** Click to expand, lightbox view
    - **Video preview:** Embedded player with controls
    - **Export:** Generate PDF with lesson content + user notes for offline study
  - **Security Considerations:**
    - Validate image uploads (check file signatures, not just extensions)
    - Sanitize HTML input to prevent XSS
    - Limit upload file sizes and types
    - Virus scan uploaded files (if possible)
    - Rate limit API endpoints to prevent abuse
  - **Accessibility:**
    - Alt text for images
    - Keyboard navigation for notes panel
    - Screen reader support for note content
    - High contrast mode for notes UI
  - **Notes:** This feature transforms passive learning into active documentation. Users can build personal knowledge bases as they progress. Consider adding note templates (e.g., "Lab Result", "Key Concept", "Question"). Future: Allow users to share notes publicly or with study groups.
  - **Dependencies:** User authentication system (to associate notes with users), file upload infrastructure
  - **Estimated Effort:** Large (2+ weeks)
  - **Future Enhancements:**
    - AI-powered note suggestions based on lesson content
    - Collaborative notes (shared notes within study groups)
    - Note version history
    - Link notes across lessons (knowledge graph)
    - Note templates and formatting presets
    - Voice note recording

### Practice & Labs
- [ ] **Feature:** [Add feature here]

---

## Gamification & Engagement

### Achievements & Badges
- [ ] **Feature:** [Add feature here]

### Leaderboards
- [ ] **Feature:** [Add feature here]

### Challenges & Events
- [ ] **Feature:** [Add feature here]

---

## User Management

### Authentication
- [ ] **Feature:** [Add feature here]

### User Profiles
- [ ] **Feature:** [Add feature here]

### Social Features
- [ ] **Feature:** [Add feature here]

---

## Analytics & Reporting

### Learning Analytics
- [ ] **Feature:** [Add feature here]

### Progress Tracking
- [ ] **Feature:** [Add feature here]

### Reports & Dashboards
- [ ] **Feature:** [Add feature here]

---

## Technical Infrastructure

### Performance
- [ ] **Feature:** [Add feature here]

### Database
- [ ] **Feature:** [Add feature here]

### Deployment
- [ ] **Feature:** [Add feature here]

---

## UI/UX Improvements

### Navigation

- [✓] **Feature:** Global Lesson Search
  - **Status:** COMPLETED 2025-10-31
  - **Priority:** High
  - **Description:** Implement search functionality that searches across all domains by keyword, matching against lesson titles and descriptions/content
  - **Acceptance Criteria:**
    - [ ] Search bar in main UI (header/sidebar)
    - [ ] Search across all domains simultaneously
    - [ ] Search fields:
      - [ ] Lesson title (primary match)
      - [ ] Learning objectives
      - [ ] Concepts
      - [ ] Content blocks text (secondary match)
    - [ ] Real-time search results (type-ahead/autocomplete)
    - [ ] Search results page showing:
      - [ ] Lesson title with search term highlighted
      - [ ] Domain badge
      - [ ] Difficulty indicator
      - [ ] Brief snippet showing context of match
      - [ ] Tags (Career Path, Course, Package)
    - [ ] Filter search results by:
      - [ ] Domain (multi-select)
      - [ ] Difficulty (1-3)
      - [ ] Tags
      - [ ] Completion status (not started, in progress, completed)
    - [ ] Sort results by:
      - [ ] Relevance (default)
      - [ ] Title (A-Z)
      - [ ] Difficulty
      - [ ] Order index
    - [ ] "No results" message with suggestions
    - [ ] Search history (recent searches)
  - **Technical Details:**
    - **Search method:** SQLite FTS (Full-Text Search) or simple LIKE query
    - **Indexed fields:** title, learning_objectives, concepts, content_blocks.text
    - **Query example:**
      ```sql
      SELECT * FROM lessons
      WHERE hidden = FALSE
      AND (title LIKE '%keyword%'
           OR learning_objectives LIKE '%keyword%'
           OR concepts LIKE '%keyword%')
      ORDER BY
        CASE
          WHEN title LIKE '%keyword%' THEN 1
          ELSE 2
        END
      ```
    - **Performance:** Consider FTS5 virtual table for large content searches
    - **UI component:** Streamlit search input with results dataframe
  - **Use Cases:**
    - User searches "Kerberos" → finds AD lessons about Kerberoasting
    - User searches "memory forensics" → finds DFIR and malware lessons
    - User searches "docker" → finds Linux, Cloud, and System lessons
    - User searches by tool name (e.g., "Volatility", "Mimikatz")
  - **Completed:**
    - [✓] Search across title, concepts, learning objectives
    - [✓] Filter by domain (15 domains)
    - [✓] Filter by difficulty (1-3)
    - [✓] Filter by tags (18 tags)
    - [✓] Filter by completion status (logged-in users)
    - [✓] Sort by Relevance, Title, Difficulty, Domain
    - [✓] Popular search suggestions (9 terms)
    - [✓] Direct navigation to lessons
    - [✓] Added to sidebar navigation
  - **Commit:** bddbdd3
  - **File:** ui/pages/search.py
  - **Result:** Fully functional search across all 411 lessons

### Visual Design
- [ ] **Feature:** [Add feature here]

### Accessibility
- [ ] **Feature:** [Add feature here]

---

## Integration & API

### External Integrations
- [ ] **Feature:** [Add feature here]

### API Development
- [ ] **Feature:** [Add feature here]

### Content Import/Export

- [✓] **Feature:** Single/Multiple JSON Lesson File Upload
  - **Status:** COMPLETED 2025-10-31
  - **Priority:** High
  - **Description:** Allow users to browse and upload one or multiple lesson JSON files through the UI, which are automatically validated, tagged as "User Content", and populated into the database
  - **Completed:**
    - [✓] File browser UI component (Streamlit file_uploader with accept_multiple_files)
    - [✓] File validation against Pydantic Lesson model with detailed error messages
    - [✓] Automatic tagging with "User Content" tag on successful import
    - [✓] Duplicate lesson detection (by lesson_id)
    - [✓] Success/error feedback with validation messages per file
    - [✓] Imported lessons immediately available in lesson catalog
    - [✓] File size limit (5MB per file)
    - [✓] Upload summary with metrics (success/errors/duplicates)
  - **Implementation:**
    - UI: ui/pages/upload_lessons.py
    - File validation using Pydantic ValidationError parsing
    - Detailed error reporting with field-level messages
    - Auto-tagging with "Package: User Content"
    - Accessible from sidebar "Upload Lessons" button
  - **Commit:** 1c5afe3
  - **Result:** Full upload functionality with comprehensive validation

- [✓] **Feature:** Lesson Package Import/Export (ZIP)
  - **Status:** COMPLETED 2025-10-31
  - **Priority:** High
  - **Description:** Enable import and export of lesson packages as ZIP files containing multiple JSON lesson files. Imported packages are automatically unpacked, validated, populated into database, and tagged with the ZIP filename (without .zip extension)
  - **Completed:**
    - [✓] **Export functionality:**
      - [✓] Select multiple lessons from catalog (multi-select with domain filter)
      - [✓] Export to ZIP file with custom package name
      - [✓] Include metadata file (package.json) with package info
      - [✓] Download ZIP with st.download_button
    - [✓] **Import functionality:**
      - [✓] File browser for selecting ZIP file (max 50MB)
      - [✓] Automatic extraction and validation of all JSON files in ZIP
      - [✓] Create package tag from ZIP filename (auto-title-case, random color, 📦 icon)
      - [✓] Apply package tag to all imported lessons
      - [✓] Also apply "User Content" tag to all imported lessons
      - [✓] Duplicate detection across all lessons in package
      - [✓] Batch validation with detailed error report per file
      - [✓] Success summary showing imported lesson count
  - **Implementation:**
    - UI: ui/pages/lesson_packages.py (two-tab interface)
    - ZIP handling: Python zipfile module with in-memory BytesIO
    - Package tag creation: Auto-generated in tags table with next available tag_id
    - Metadata file: package.json with package_name, version, created_date, lesson_count, lesson_ids
    - Export naming: lesson_{domain}_{order_index:03d}_{title}.json
    - Accessible from sidebar "Lesson Packages" button
  - **Commit:** 3cdbe42
  - **Result:** Full import/export with package tags and metadata
  - **Dependencies:** Requires "User Content" tag system (already exists), extends single file upload feature
  - **Estimated Effort:** Large (1+ week)

---

## Security & Privacy

### Security Features
- [ ] **Feature:** [Add feature here]

### Privacy & Compliance
- [ ] **Feature:** [Add feature here]

### Data Protection
- [ ] **Feature:** [Add feature here]

---

## Admin & Content Creation

### Content Management
- [ ] **Feature:** [Add feature here]

### Admin Tools
- [ ] **Feature:** [Add feature here]

### Bulk Operations
- [ ] **Feature:** [Add feature here]

---

## Completed Features Archive

Move completed features here periodically to keep the main list focused on upcoming work.

### 2025-10-30

- [✓] **Feature:** Many-to-Many Lesson Tagging System
  - **Priority:** High
  - **Description:** Flexible tagging system allowing multiple tags per lesson and multiple lessons per tag, supporting Career Path, Course, and Package categorization
  - **Completed:** 2025-10-30
  - **PR/Commit:** Multiple PRs (#11, #12, #13)
  - **Acceptance Criteria:**
    - [✓] Database schema with lesson_tags junction table
    - [✓] Tag model with name, icon (emoji), color, category
    - [✓] 17 system tags created (Career Path, Course, Package categories)
    - [✓] Auto-tagging functionality in load_all_lessons.py
    - [✓] Course-specific tags: Eric Zimmerman Tools, 13Cubed courses (Memory, Endpoints, Linux)
    - [✓] Template database includes all tags pre-populated
    - [✓] UI displays tags correctly with emojis and colors
  - **Technical Details:**
    - **Database:** `tags` table + `lesson_tags` junction table
    - **Tag Categories:** career_path, course, package
    - **System Tags:** 10 Career Path (SOC Analyst, Pentester, Red Teamer, etc.), 5 Course tags, 2 Package tags
    - **Auto-tagging:** DFIR lessons 11-24 → Eric Zimmerman Tools, 11-41 → 13Cubed Memory, 42-70 → 13Cubed Endpoints, 71-111 → 13Cubed Linux
  - **Files Modified:**
    - `database.py` - Added Tag model and lesson_tags table
    - `load_all_lessons.py` - Added auto_tag_lessons() function
    - `add_all_tags.py` - Script to populate system tags
    - `add_13cubed_tags.py` - Script to add course-specific tags
    - `cyberlearn_template.db` - Updated with all tags
  - **Notes:** Solved Unicode encoding issues with emoji printing on Windows (cp1252 codec). Template database ships ready with all tags - no manual scripts needed on VM.

- [✓] **Feature:** Linux Forensics Course (41 Rich Lessons)
  - **Priority:** High
  - **Description:** Complete Linux forensics curriculum based on 13Cubed "Investigating Linux Devices" course, covering foundations through advanced memory forensics
  - **Completed:** 2025-10-30
  - **PR/Commit:** PR #13 (60 lessons), plus earlier PRs for lessons 71-80
  - **Acceptance Criteria:**
    - [✓] 41 lessons created (DFIR order_index 71-111)
    - [✓] Organized into 9 modules (Foundations, Advanced Logging, File Systems, Persistence, Evidence Collection, Timelining, Memory Forensics, Live Response, Case Studies)
    - [✓] All lessons validated and loaded into database
    - [✓] Course tag applied: "Course: 13Cubed-Investigating Linux Devices"
    - [✓] Proper prerequisites chaining
    - [✓] Difficulty progression (beginner → intermediate → advanced)
  - **Module Breakdown:**
    - Module 1: Linux Foundations (7 lessons) - Distributions, file hierarchy, permissions, users, shells, logs
    - Module 2: Advanced Logging (3 lessons) - auditd, Sysmon for Linux, VMware ESXi
    - Module 3: File Systems (7 lessons) - ext2/3/4, Sleuth Kit, timestomping, Btrfs/XFS, ZFS
    - Module 4: Persistence (4 lessons) - systemd, cron, SSH keys, rootkits
    - Module 5: Evidence Collection (4 lessons) - dd/dcfldd, AVML, UAC, virtualized environments
    - Module 6: Timelining (3 lessons) - mactime, Plaso/log2timeline, comprehensive timeline lab
    - Module 7: Memory Forensics (8 lessons) - Volatility 3, process analysis, bash history, network, code injection, dumping, plugins, case study
    - Module 8: Live Response (2 lessons) - UAC walkthrough, best practices
    - Module 9: Case Studies (3 lessons) - Disk analysis, memory analysis, capstone lab
  - **Technical Details:**
    - All lessons include post_assessment with question_id and explanation fields
    - Fixed validation errors across all 41 lessons
    - Tagged with "Course: 13Cubed-Investigating Linux Devices" (🐧, teal #14B8A6)
  - **Files Created:**
    - 41 JSON files: `content/lesson_dfir_71.json` through `content/lesson_dfir_111.json`
    - `fix_pr13_lessons.py` - Bulk validation fix script
    - `lesson_ideas.json` - Course specification with full module structure
  - **Notes:** This represents the largest single course addition to CyberLearn, nearly doubling DFIR content from 30 to 93 lessons

---

## Future Ideas (Not Yet Planned)

Use this section for brainstorming features that aren't fully scoped yet:

- Idea: Mobile app version
- Idea: Offline mode for lessons
- Idea: Collaborative learning (study groups)
- Idea: Live instructor-led sessions
- Idea: Integration with CTF platforms
- Idea: Resume/CV builder based on completed lessons
- Idea: Job board integration
- Idea: Mentor matching system

---

## Notes & Decisions

### Architecture Decisions
- Using SQLite for simplicity (may migrate to PostgreSQL for scale)
- Streamlit for frontend (rapid development, may migrate to React later)
- FastAPI for backend API layer

### Content Strategy
- Target 80-100 rich lessons minimum (8-12 per domain)
- Current: 275 lessons loaded, 45 rich lessons completed
- Focus on quality over quantity (4,000-5,500 words per lesson)

### Release Planning
- Version 1.0: Core learning platform with 9 domains
- Version 2.0: Advanced gamification and social features
- Version 3.0: Enterprise features (teams, organizations, SSO)

---

## Contributing

When adding features to this list:
1. Use the feature template provided
2. Assign priority based on user impact and business value
3. Break large features into smaller, trackable sub-features
4. Update status regularly as work progresses
5. Archive completed features to keep list manageable

---

**Quick Stats:**
- Total lessons planned: 124 (lesson_ideas.csv)
- Total lessons created: 275 (cyberlearn.db)
- Rich lessons completed: 45
- Domains: 12 (9 core + 3 emerging tech)
- Tags: 17 system tags
