---
name: assessment-generator
description: Generate high-quality post-assessment questions for CyberLearn lessons
version: 1.0
auto_invoke: true
---

# Assessment Generator Skill

Create comprehensive, technically accurate assessment questions that test understanding and reinforce learning.

## When to Use

Automatically invoke when:
- User asks to "add assessment questions"
- Generating new lesson content
- Enhancing existing lessons
- Improving question quality
- User wants more questions for specific difficulty

## Assessment Question Requirements

### Required Fields (CRITICAL)

Every question MUST have ALL these fields:

```json
{
  "question_id": "unique-identifier",     // REQUIRED - Unique within lesson
  "question": "Question text?",           // REQUIRED - Clear, specific
  "options": ["A", "B", "C", "D"],       // REQUIRED - 4 options
  "correct_answer": 1,                    // REQUIRED - 0-based index
  "explanation": "Why this is correct",   // REQUIRED - Educational
  "type": "multiple_choice",              // REQUIRED - Always this value
  "difficulty": 2                         // REQUIRED - 1, 2, or 3
}
```

**Missing ANY field will cause validation error!**

### Difficulty Levels

- **Difficulty 1 (Beginner)**: Recall, recognition, basic concepts
  - "What command shows user accounts?"
  - "Which file contains password hashes?"
  - Focus on definitions and basic usage

- **Difficulty 2 (Intermediate)**: Application, analysis, interpretation
  - "Given this log entry, what attack is occurring?"
  - "How would you investigate this scenario?"
  - Focus on practical application

- **Difficulty 3 (Advanced)**: Synthesis, evaluation, expert judgment
  - "Which forensic approach would be most effective and why?"
  - "Compare and contrast these two techniques"
  - Focus on expert decision-making

## Question Writing Best Practices

### 1. Clear and Specific Questions

**Good**:
```
"In the /etc/shadow file, what does the value '!!' in the password field indicate?"
```

**Bad**:
```
"What does !! mean?"
```

### 2. Realistic Scenarios

**Good**:
```
"You discover a user account 'webadmin' with UID 0 in /etc/passwd. What is the primary security concern?"
```

**Bad**:
```
"What is bad about UID 0?"
```

### 3. Educational Explanations

**Good**:
```
"Explanation": "UID 0 grants root privileges. Any account with UID 0 has full system access, even if the username isn't 'root'. This is a common persistence technique used by attackers to maintain elevated access while appearing as a normal service account."
```

**Bad**:
```
"Explanation": "Because UID 0 is root"
```

### 4. Plausible Distractors

**Good Options**:
```
"options": [
  "/var/log/auth.log - Authentication events",
  "/var/log/secure - Login attempts",        // Different name, same concept
  "/var/log/messages - General system logs",  // Related but wrong
  "/var/log/kernel.log - Kernel messages"     // Plausible but incorrect
]
```

**Bad Options**:
```
"options": [
  "/var/log/auth.log",
  "/var/log/notreal.log",    // Obviously fake
  "/etc/passwd",             // Completely unrelated
  "auth.log"                 // Missing path
]
```

## Question Types by Domain

### DFIR Questions

Focus on:
- Artifact locations
- Timeline reconstruction
- Evidence interpretation
- Forensic tools usage

**Example**:
```json
{
  "question_id": "dfir-auth-001",
  "question": "During an investigation, you find the following entry in /var/log/auth.log:\n\n'May 15 03:47:23 server sshd[12345]: Failed password for invalid user admin from 192.168.1.100 port 52847 ssh2'\n\nWhat does this indicate?",
  "options": [
    "Successful SSH login as admin",
    "Failed SSH login attempt for non-existent user 'admin'",
    "System administrator logged in remotely",
    "Firewall blocked SSH connection"
  ],
  "correct_answer": 1,
  "explanation": "The log shows 'Failed password for invalid user admin', meaning the user 'admin' doesn't exist on the system. This is a common brute-force pattern where attackers try default usernames. The source IP 192.168.1.100 should be investigated for additional failed attempts.",
  "type": "multiple_choice",
  "difficulty": 2
}
```

### Malware Questions

Focus on:
- Malware behavior
- Static/dynamic analysis
- Indicators of compromise
- Anti-analysis techniques

### Pentest Questions

Focus on:
- Attack vectors
- Exploitation techniques
- Post-exploitation
- Mitigation strategies

### Cloud Questions

Focus on:
- Cloud-specific artifacts
- API logging
- Identity and access management
- Container forensics

## Question Quantity Guidelines

### Minimum Requirements
- **Every lesson**: Minimum 3 questions
- **Rich lessons**: 4-6 questions recommended
- **Complex topics**: 5-7 questions

### Difficulty Distribution

For a lesson with 5 questions:
- **Beginner lesson**: 3 easy, 2 medium
- **Intermediate lesson**: 1 easy, 3 medium, 1 hard
- **Advanced lesson**: 1 medium, 3 hard, 1 expert-level

## Question ID Naming Convention

Use descriptive, unique IDs:

```
<domain>-<topic>-<number>
```

**Examples**:
- `dfir-auth-001` - DFIR authentication question 1
- `dfir-auth-002` - DFIR authentication question 2
- `malware-analysis-001` - Malware analysis question 1
- `pentest-enum-001` - Pentest enumeration question 1

**Benefits**:
- Easy to reference in documentation
- Clear topic organization
- Prevents duplicates
- Enables question tracking

## Generating Assessment Questions

### Process

1. **Analyze lesson content**:
   - Identify key concepts
   - Note important commands/tools
   - Extract critical facts
   - Review real-world examples

2. **Determine difficulty distribution**:
   - Match lesson difficulty
   - Balance easy/medium/hard
   - Ensure minimum 3 questions

3. **Write questions**:
   - Start with key learning objectives
   - Create realistic scenarios
   - Write clear, specific questions
   - Craft plausible distractors

4. **Write explanations**:
   - Explain WHY answer is correct
   - Reference lesson content
   - Provide additional context
   - Help reinforce learning

5. **Validate structure**:
   - All required fields present
   - question_id is unique
   - correct_answer is valid index (0-3)
   - difficulty matches question complexity

## Example Generation Workflow

**User**: "Generate assessment questions for lesson 78 (Linux auditd)"

**Assessment Generator**:

```
📋 GENERATING ASSESSMENT QUESTIONS

Lesson: Linux auditd Framework for Forensics
Difficulty: 2 (Intermediate)
Target: 5 questions

Distribution:
- 1 easy (difficulty 1) - Basic auditd concepts
- 3 medium (difficulty 2) - Practical application
- 1 hard (difficulty 3) - Advanced analysis

Analyzing lesson content...
✓ Key concepts: auditd architecture, rules, logs, analysis
✓ Important commands: auditctl, ausearch, aureport
✓ Real-world examples: Login monitoring, file integrity

Generating questions...

Question 1 (Easy):
- Topic: Basic auditd architecture
- Tests: Component recognition
- ID: dfir-auditd-001

Question 2 (Medium):
- Topic: Writing audit rules
- Tests: Rule syntax understanding
- ID: dfir-auditd-002

Question 3 (Medium):
- Topic: Log analysis
- Tests: Interpreting ausearch output
- ID: dfir-auditd-003

Question 4 (Medium):
- Topic: Practical application
- Tests: Choosing appropriate rules
- ID: dfir-auditd-004

Question 5 (Hard):
- Topic: Advanced investigation
- Tests: Complex timeline reconstruction
- ID: dfir-auditd-005

✅ 5 questions generated
✅ All required fields present
✅ Difficulty distribution: 1-1, 2-3, 3-1

Preview:
----------------------------------------
Question 1 (Easy): What is the primary purpose of the Linux auditd framework?
Correct: Monitor and log security-relevant events
Explanation: auditd is the Linux Audit daemon that monitors system calls and logs security events...

Question 2 (Medium): Which auditctl rule would monitor all file accesses in /etc/passwd?
Correct: -w /etc/passwd -p rwxa -k passwd-watch
Explanation: The -w flag specifies file to watch, -p specifies permissions (read/write/execute/attribute)...

[... etc]
```

## Quality Checklist

Before finalizing assessment questions:

- ✅ All required fields present (question_id, type, difficulty)
- ✅ Questions test learning objectives
- ✅ Distractors are plausible
- ✅ Explanations are educational
- ✅ No grammatical errors
- ✅ Difficulty matches complexity
- ✅ question_ids are unique
- ✅ correct_answer is valid index
- ✅ Questions vary in topic coverage
- ✅ Realistic scenarios used

## Common Mistakes to Avoid

### ❌ Missing Required Fields
```json
{
  "question": "What is auditd?",
  "options": ["A", "B", "C", "D"],
  "correct_answer": 0
  // Missing: question_id, type, difficulty, explanation
}
```

### ❌ Vague Questions
```
"What is important about /etc/shadow?"
```

### ❌ Obvious Distractors
```
"options": [
  "/var/log/auth.log",
  "banana",           // Obviously wrong
  "12345",            // Not even a path
  "yes"               // Doesn't make sense
]
```

### ❌ Minimal Explanations
```
"explanation": "Because it's correct"
```

### ❌ Duplicate question_ids
```json
[
  {"question_id": "q1", ...},
  {"question_id": "q1", ...}  // Duplicate!
]
```

## Integration with Other Skills

- Used by **lesson-generator** for new lessons
- Works with **content-enhancer** for adding questions
- Coordinates with **lesson-validator** for validation
- Integrates with **lesson-updater** for question updates

## Template for Manual Question Writing

Use this template when writing questions manually:

```json
{
  "question_id": "<domain>-<topic>-<number>",
  "question": "Clear, specific question text?",
  "options": [
    "Option A - correct answer with detail",
    "Option B - plausible distractor",
    "Option C - related but wrong",
    "Option D - common misconception"
  ],
  "correct_answer": 0,
  "explanation": "Detailed explanation of why option A is correct, including context from the lesson and additional learning value. Reference specific tools, commands, or concepts.",
  "type": "multiple_choice",
  "difficulty": 2
}
```

## Advanced Features

### Scenario-Based Questions

For advanced lessons, create multi-part scenarios:

```json
{
  "question_id": "dfir-scenario-001",
  "question": "SCENARIO: You're investigating a compromised server. Analysis shows:\n\n1. /var/log/auth.log has 5,000 failed SSH attempts from 10.0.0.50\n2. A new user 'sysbackup' with UID 0 exists in /etc/passwd\n3. .bash_history for this user shows: rm -rf /var/log/*, history -c\n\nWhat is the MOST likely attack progression?",
  "options": [
    "Brute force → privilege escalation → log clearing",
    "Brute force → persistence → anti-forensics",
    "Password guessing → account creation → system backup",
    "DDoS attack → system compromise → data exfiltration"
  ],
  "correct_answer": 1,
  "explanation": "The evidence shows: (1) Brute force attack from 10.0.0.50, (2) Persistence via UID 0 account named to appear legitimate, (3) Anti-forensic techniques (log deletion, history clearing). This is a classic post-compromise pattern where attackers maintain access and cover their tracks.",
  "type": "multiple_choice",
  "difficulty": 3
}
```

### Command Output Interpretation

```json
{
  "question_id": "dfir-cmd-001",
  "question": "Given this ausearch output:\n\ntype=USER_AUTH msg=audit(1652611234.567:890): pid=1234 uid=0 auid=1000 msg='op=PAM:authentication acct=\"root\" exe=\"/usr/bin/sudo\" res=failed'\n\nWhat does this indicate?",
  "options": [
    "Successful sudo command by user ID 1000",
    "Failed attempt to authenticate as root via sudo by user ID 1000",
    "System boot authentication failure",
    "Root user failed to log in via SSH"
  ],
  "correct_answer": 1,
  "explanation": "The audit log shows: auid=1000 (actual user ID is 1000), acct=\"root\" (attempting to become root), exe=\"/usr/bin/sudo\" (via sudo), res=failed (authentication failed). This indicates user 1000 tried to run a sudo command but entered the wrong password or lacks sudo privileges.",
  "type": "multiple_choice",
  "difficulty": 2
}
```

## Performance Metrics

Track question effectiveness:
- Average completion time
- Success rate
- Common wrong answers
- Question difficulty calibration

Use analytics to improve future questions.
