---
name: markdown-formatter
description: Format lesson content with proper markdown, code blocks, and visual elements
version: 1.0
auto_invoke: true
---

# Markdown Formatter Skill

Ensure consistent, readable markdown formatting in CyberLearn lesson content blocks.

## When to Use

Automatically invoke when:
- Generating new lesson content
- Updating existing lessons
- User requests "format lesson X"
- Content appears poorly formatted
- Converting plain text to rich markdown

## Markdown Standards for CyberLearn

### Content Block Text Field

All content in `content_blocks` must be in the `text` field:

```json
{
  "type": "explanation",
  "content": {
    "text": "# Markdown content here\n\nFormatted text..."
  }
}
```

### Heading Hierarchy

Use proper heading levels:

```markdown
# Main Topic (H1) - Used for major sections

## Subsection (H2) - Used for key concepts

### Detail (H3) - Used for specific topics

#### Minor Point (H4) - Rarely used
```

**Example**:
```markdown
# Linux File Permissions Overview

## The Permission Model

### Read (r) Permission

#### Special Cases for Directories
```

### Code Blocks

Always use fenced code blocks with language specification:

**Bash/Shell Commands**:
````markdown
```bash
ls -la /var/log
cat /etc/passwd
auditctl -l
```
````

**Python Scripts**:
````markdown
```python
import os
import sys

def parse_log(logfile):
    with open(logfile, 'r') as f:
        return f.readlines()
```
````

**Configuration Files**:
````markdown
```conf
# /etc/audit/auditd.conf
log_file = /var/log/audit/audit.log
log_format = ENRICHED
freq = 50
```
````

**JSON**:
````markdown
```json
{
  "user": "admin",
  "uid": 1000,
  "shell": "/bin/bash"
}
```
````

**Log Output**:
````markdown
```log
May 15 14:32:11 server sshd[1234]: Failed password for invalid user admin
May 15 14:32:15 server sshd[1234]: Connection closed by 192.168.1.100
```
````

### Lists

**Unordered Lists**:
```markdown
- Item 1
- Item 2
  - Nested item 2a
  - Nested item 2b
- Item 3
```

**Ordered Lists**:
```markdown
1. First step
2. Second step
3. Third step
   - Sub-point
   - Another sub-point
4. Fourth step
```

**Checklist** (for exercises):
```markdown
- [ ] Task to complete
- [ ] Another task
- [x] Completed task
```

### Emphasis and Formatting

```markdown
**Bold** - For important terms, commands
*Italic* - For emphasis, variable names
`code` - For inline commands, file paths, technical terms
***Bold Italic*** - For critical warnings
```

**Example**:
```markdown
The **auditd** framework uses the `/var/log/audit/audit.log` file to store events. You can search logs with the `ausearch` command.

*Note*: Always backup logs before analysis!

***WARNING***: Do not modify live audit logs during investigation.
```

### Tables

Use tables for structured comparisons:

```markdown
| Permission | Symbol | Numeric | Description |
|------------|--------|---------|-------------|
| Read       | r      | 4       | View file contents |
| Write      | w      | 2       | Modify file |
| Execute    | x      | 1       | Run as program |
```

### Blockquotes

Use for important notes, tips, warnings:

```markdown
> **Tip**: Use `ausearch -i` for human-readable timestamps.

> **Warning**: This command will delete all logs!

> **Jim Kwik Memory Hook**: Remember permissions with "Read = 4, Write = 2, eXecute = 1" (RWX 421)
```

### Horizontal Rules

Separate major sections:

```markdown
---

Content after separator
```

## ASCII Art Diagrams

Use ASCII art for visual learning:

### System Architecture:
```markdown
```text
┌─────────────────────────────────────┐
│      Linux Audit Framework          │
├─────────────────────────────────────┤
│  auditd (daemon)                    │
│    ↓                                │
│  audit.rules (configuration)        │
│    ↓                                │
│  kernel audit subsystem             │
│    ↓                                │
│  /var/log/audit/audit.log           │
└─────────────────────────────────────┘
```
```

### File Structure:
```markdown
```text
/var/log/
├── auth.log          # Authentication events
├── syslog            # System messages
├── kern.log          # Kernel messages
└── audit/
    └── audit.log     # Audit framework logs
```
```

### Process Flow:
```markdown
```text
User Login Attempt
    ↓
PAM Authentication
    ↓
Success? ───No──→ Log to auth.log (failed)
    ↓
   Yes
    ↓
Create Session
    ↓
Log to wtmp, lastlog
    ↓
Shell Started
```
```

### Timeline:
```markdown
```text
Attack Timeline:
─────────────────────────────────────────────────────────
03:15 AM  → Brute force begins (auth.log: 500 attempts)
03:47 AM  → Successful login (wtmp: user 'admin')
03:48 AM  → Privilege escalation (sudo su -)
03:50 AM  → Persistence (create user 'backup' UID 0)
03:52 AM  → Anti-forensics (rm /var/log/*, history -c)
04:00 AM  → Connection closed
```
```

## Content Block Formatting Examples

### Explanation Block

```json
{
  "type": "explanation",
  "content": {
    "text": "# Understanding /etc/shadow\n\nThe `/etc/shadow` file stores **encrypted password hashes** and account aging information. Each line represents one user account.\n\n## Field Structure\n\nShadow file format:\n```\nusername:password:lastchange:min:max:warn:inactive:expire:reserved\n```\n\n**Example entry**:\n```\nroot:$6$xyz123...:19089:0:99999:7:::\n```\n\n### Field Breakdown\n\n1. **Username**: Account name (matches /etc/passwd)\n2. **Password**: Encrypted hash or special values:\n   - `$6$...` - SHA-512 hash\n   - `!` or `!!` - Account locked\n   - `*` - Account disabled\n3. **Last Change**: Days since epoch of last password change\n\n> **Forensic Tip**: Compare lastchange with wtmp entries to detect password changes during compromise."
  }
}
```

### Code Exercise Block

```json
{
  "type": "code_exercise",
  "content": {
    "text": "# Hands-On: Analyzing /etc/shadow\n\n## Exercise Objectives\n\n- [ ] Identify locked accounts\n- [ ] Find accounts with weak aging policies\n- [ ] Detect suspicious password changes\n\n## Step 1: Extract Password Hashes\n\n```bash\n# View shadow file (requires root)\nsudo cat /etc/shadow\n\n# Extract just usernames and hash types\nsudo awk -F: '{print $1, $2}' /etc/shadow\n```\n\n## Step 2: Find Locked Accounts\n\n```bash\n# Find accounts with ! or !!\nsudo grep -E '^[^:]+:!!' /etc/shadow\n```\n\n**Expected Output**:\n```\nguest:!!:19089:0:99999:7:::\ntestuser:!:19100:0:99999:7:::\n```\n\n## Step 3: Analyze Password Aging\n\n```bash\n# Check aging for specific user\nsudo chage -l username\n```\n\n> **Real-World Application**: Attackers often modify password aging to prevent password expiration on compromised accounts."
  }
}
```

### Real-World Block

```json
{
  "type": "real_world",
  "content": {
    "text": "# Case Study: APT29 Persistence via Shadow Manipulation\n\n## Incident Overview\n\n**Target**: Financial services company\n**Attack Group**: APT29 (Cozy Bear)\n**Date**: March 2023\n\n## Attack Timeline\n\n```text\nDay 1 (03:15 UTC) → Initial access via phishing\nDay 1 (04:30 UTC) → Privilege escalation (CVE-2023-xxxxx)\nDay 2 (02:00 UTC) → Persistence mechanism deployed\nDay 5 (--:-- UTC) → Discovery by SOC team\n```\n\n## Persistence Technique\n\nAttackers created a backdoor account:\n\n```bash\n# /etc/passwd entry\nsysupdate:x:1001:1001:System Update Service:/var/lib/sysupdate:/bin/bash\n\n# /etc/shadow entry (modified)\nsysupdate:$6$malicious_hash:19200:0:99999:7:::\n```\n\n**Detection Methods**:\n\n1. **Baseline comparison**: Account didn't exist in previous backup\n2. **Naming pattern**: Designed to blend in (sysupdate)\n3. **Creation time**: `/etc/shadow` lastchange = 19200 (incident timeframe)\n4. **sudo access**: Attackers added entry to `/etc/sudoers.d/`\n\n## Key Takeaways\n\n> **Lesson**: Attackers use legitimate-looking account names\n> **Detection**: Monitor /etc/passwd and /etc/shadow for changes\n> **Prevention**: Implement file integrity monitoring (AIDE, Tripwire)\n\n**Tools Used in Investigation**:\n- `diff` - Compare current vs. baseline\n- `stat` - Check file modification times\n- `ausearch` - Find audit trail of account creation"
  }
}
```

### Memory Aid Block

```json
{
  "type": "memory_aid",
  "content": {
    "text": "# Jim Kwik Memory Techniques for Linux Permissions\n\n## Mnemonic: \"RWX 421\"\n\n**R**ead = **4** (think: **4** eyes to read)\n**W**rite = **2** (think: **2** hands to write)\ne**X**ecute = **1** (think: **1** foot to run/execute)\n\n## Visual Association: Permission Table\n\n```text\n┌───────────┬────────┬─────────┐\n│ Permission│ Binary │ Decimal │\n├───────────┼────────┼─────────┤\n│    r--    │  100   │    4    │\n│    -w-    │  010   │    2    │\n│    --x    │  001   │    1    │\n│    rwx    │  111   │    7    │\n│    rw-    │  110   │    6    │\n│    r-x    │  101   │    5    │\n└───────────┴────────┴─────────┘\n```\n\n## Story Method: The 755 House\n\nImagine a house (file) with **three rooms** (owner/group/others):\n\n1. **Owner's room (7)**: Full access - read, write, execute\n2. **Group room (5)**: Read and enter - read, execute\n3. **Public lobby (5)**: Read and enter - read, execute\n\n**755 = rwxr-xr-x** - Owner controls everything, others can view and use but not modify.\n\n> **Active Learning**: Practice with `chmod 755 file` and verify with `ls -l`"
  }
}
```

## Formatting Best Practices

### 1. Consistent Spacing

```markdown
# Heading

Content paragraph with proper spacing.

Another paragraph after blank line.

## Next Section

- List item 1
- List item 2
```

### 2. Code Block Language Tags

Always specify language for syntax highlighting:

```markdown
```bash
# Good - has language tag
ls -la
```

```
# Bad - no language tag
ls -la
```
```

### 3. Inline Code for Technical Terms

```markdown
Good: Use the `auditctl` command to configure rules.
Bad: Use the auditctl command to configure rules.

Good: Edit `/etc/audit/rules.d/audit.rules` file.
Bad: Edit /etc/audit/rules.d/audit.rules file.
```

### 4. Escape Special Characters

```markdown
Use \* for literal asterisk
Use \` for literal backtick
Use \\ for literal backslash
```

### 5. Line Length

- Keep lines under 120 characters where possible
- Use line breaks for readability
- Don't break code blocks mid-command

## Common Formatting Errors

### ❌ Error 1: Missing Language Tags

```markdown
Bad:
```
ls -la /var/log
```

Good:
```bash
ls -la /var/log
```
```

### ❌ Error 2: Inconsistent Heading Levels

```markdown
Bad:
# Topic
#### Detail (skipped H2, H3)

Good:
# Topic
## Subtopic
### Detail
```

### ❌ Error 3: Inline Code in Headers

```markdown
Bad:
## The `auditctl` Command

Good:
## The auditctl Command
```

### ❌ Error 4: No Blank Lines

```markdown
Bad:
Paragraph 1
Paragraph 2

Good:
Paragraph 1

Paragraph 2
```

## Integration with Other Skills

- Used by **lesson-generator** for content creation
- Works with **content-enhancer** for formatting improvements
- Coordinates with **lesson-validator** for markdown validation
- Integrates with **lesson-updater** for formatting updates

## Validation Checklist

Before finalizing lesson content:

- ✅ All code blocks have language tags
- ✅ Headings follow proper hierarchy (H1 → H2 → H3)
- ✅ Technical terms use inline code (`term`)
- ✅ File paths use inline code (`/path/to/file`)
- ✅ Commands use code blocks with ```bash
- ✅ Lists have consistent formatting
- ✅ Tables are properly formatted
- ✅ Blockquotes used for tips/warnings
- ✅ ASCII diagrams are clear and aligned
- ✅ No trailing whitespace
- ✅ Blank lines between sections
- ✅ Content wrapped in {"text": "..."} format

## Quick Reference Templates

### Command Reference Template:
```markdown
# Command: `command-name`

## Syntax
```bash
command-name [options] [arguments]
```

## Common Options

| Option | Description |
|--------|-------------|
| `-a`   | Option A    |
| `-b`   | Option B    |

## Examples

```bash
# Example 1: Basic usage
command-name file.txt

# Example 2: With options
command-name -a -b file.txt
```

## Forensic Use Cases

1. **Scenario 1**: Description
2. **Scenario 2**: Description
```

### Concept Explanation Template:
```markdown
# Concept Name

## Overview

Brief description of the concept.

## How It Works

```text
[ASCII diagram showing process]
```

## Key Points

- Point 1
- Point 2
- Point 3

## Real-World Example

Practical application description.

> **Memory Hook**: Mnemonic or association
```

Use these templates for consistent, professional formatting across all lessons.
