# Universal Rich Lesson Generator Prompt

**Copy the prompt below and replace `[LESSON_TOPIC]` with your actual topic.**

---

# Generate CyberLearn Rich Lesson: [LESSON_TOPIC]

You are an expert cybersecurity instructor creating a comprehensive, engaging lesson for the CyberLearn adaptive learning platform. Generate a complete lesson JSON file following ALL requirements below.

## Lesson Topic
**Topic:** [LESSON_TOPIC]
**Domain:** [Choose: fundamentals, dfir, malware, active_directory, system, cloud, pentest, red_team, blue_team, osint, threat_hunting, linux, ai_security, iot_security, web3_security]
**Difficulty:** [Choose: 1=Beginner, 2=Intermediate, 3=Advanced]
**Order Index:** [Integer: position in domain sequence]

## Critical Requirements

### 1. JSON Structure
Generate a complete JSON file with this exact structure:

```json
{
  "lesson_id": "[GENERATE NEW UUID v4]",
  "domain": "[DOMAIN FROM LIST ABOVE]",
  "title": "[Clear, Descriptive Title]",
  "subtitle": "[Optional: Additional context]",
  "difficulty": [1-3],
  "estimated_time": [30-60 minutes],
  "order_index": [INTEGER],
  "prerequisites": [
    "[UUID of prerequisite lesson 1]",
    "[UUID of prerequisite lesson 2]"
  ],
  "concepts": [
    "[Key concept 1]",
    "[Key concept 2]",
    "[Key concept 3]",
    "[Maximum 6-8 concepts]"
  ],
  "learning_objectives": [
    "[Objective 1: Use action verbs - Analyze, Evaluate, Apply, Create]",
    "[Objective 2: Be specific and measurable]",
    "[Objective 3: Relate to real-world application]"
  ],
  "post_assessment": [
    {
      "question_id": "[GENERATE NEW UUID]",
      "question": "[Question text]",
      "options": [
        "[Option A]",
        "[Option B]",
        "[Option C]",
        "[Option D]"
      ],
      "correct_answer": [0-3],
      "difficulty": [1-3],
      "type": "multiple_choice",
      "explanation": "[Why this is correct and others are wrong]"
    }
    // Minimum 3 questions required
  ],
  "jim_kwik_principles": [
    "teach_like_im_10",
    "memory_hooks",
    "connect_to_what_i_know",
    "active_learning",
    "meta_learning",
    "minimum_effective_dose",
    "reframe_limiting_beliefs",
    "gamify_it",
    "learning_sprint",
    "multiple_memory_pathways"
  ],
  "content_blocks": [
    // See content block requirements below
  ],
  "tags": [
    "[Optional: Course tags, career path tags]"
  ]
}
```

### 2. Content Requirements

**Length:** 4,000-15,000 words total across all content blocks

**Minimum Structure:**
- **12-15 content blocks** using diverse types
- **4+ different content block types**
- **6-8 key concepts** (avoid information overload)

### 3. Required Content Blocks

#### Block 1: Opening Explanation (teach_like_im_10)
```json
{
  "type": "explanation",
  "content": {
    "text": "## Introduction to [TOPIC]\n\n[START WITH WHY IT MATTERS]\n\n[USE SIMPLE LANGUAGE - Think 'hotel analogy' not 'enterprise-grade operational paradigm']\n\n[AVOID JARGON: No 'grounded in repeatable practice', 'measurable action', 'operationalize', 'synergize', 'leverage paradigm']\n\n[INCLUDE ANALOGY]: Think of [TOPIC] like [EVERYDAY EXAMPLE]...\n\n[BREAK DOWN COMPLEX CONCEPT]: Let's break this down:\n1. [Simple step 1]\n2. [Simple step 2]\n3. [Simple step 3]\n\n[Key Insight]: [One-line takeaway]"
  }
}
```

#### Block 2: Video Content (multiple_memory_pathways - auditory)
```json
{
  "type": "video",
  "content": {
    "text": "https://www.youtube.com/watch?v=[RELEVANT_VIDEO_ID] — [Description of what video covers and why it's relevant to this lesson]"
  }
}
```

#### Block 3: Technical Deep Dive (explanation)
```json
{
  "type": "explanation",
  "content": {
    "text": "## Deep Dive: [ASPECT OF TOPIC]\n\n[DETAILED TECHNICAL EXPLANATION - 800-1500 words]\n\n### [Sub-topic 1]\n[Technical details, examples, use cases]\n\n### [Sub-topic 2]\n[Technical details, real-world scenarios]\n\n### [Sub-topic 3]\n[Common patterns, best practices]\n\n**Real-World Example:**\n[Specific company, incident, or case study with actual details]\n\nIn 2019, [Company] experienced [incident] because [technical reason]...\n\n**Technical Details:**\n[Commands, configurations, code snippets where applicable]"
  }
}
```

#### Block 4: Diagram (multiple_memory_pathways - visual)
```json
{
  "type": "diagram",
  "content": {
    "text": "## Visual Architecture\n\n```\n[CREATE ASCII DIAGRAM]\n\nExample:\n  User → Authentication Server → Database\n    ↓           ↓                    ↓\n  Input     Verify Creds      Check Perms\n    ↓           ↓                    ↓\n  Submit    Compare Hash       Return Status\n```\n\n**Key Components:**\n- [Component 1]: [Description]\n- [Component 2]: [Description]\n- [Component 3]: [Description]\n\n**Flow Explanation:**\n1. [Step 1 with arrows]\n2. [Step 2 with data flow]\n3. [Step 3 with results]"
  }
}
```

#### Block 5: Memory Aid (memory_hooks)
```json
{
  "type": "memory_aid",
  "content": {
    "text": "## Memory Techniques\n\n### Mnemonic: [ACRONYM]\n\n**[CREATE MEMORABLE ACRONYM]**\n\n- [LETTER] – [Concept it represents]\n- [LETTER] – [Concept it represents]\n- [LETTER] – [Concept it represents]\n- [LETTER] – [Concept it represents]\n- [LETTER] – [Concept it represents]\n\n**Memory Hook:** Think of [ACRONYM] like [VISUAL ASSOCIATION]...\n\nExample: \"AAA\" like AAA batteries - powers security!\n\n### Alternative Mnemonic: [SECOND ACRONYM]\n\n[Create second mnemonic for different aspect]\n\n**Practice Technique:**\n- Say the acronym out loud 3 times\n- Write it down on a sticky note\n- Explain it to someone else\n- Use it in your daily stand-ups"
  }
}
```

#### Block 6: Hands-On Exercise (active_learning, multiple_memory_pathways - kinesthetic)
```json
{
  "type": "code_exercise",
  "content": {
    "text": "## Hands-On Exercise: [EXERCISE NAME]\n\n**Objective:** [What you'll learn by doing this]\n\n**Prerequisites:**\n- [Tool/software needed]\n- [Access/permissions required]\n- [Prior knowledge needed]\n\n**Step-by-Step Instructions:**\n\n### Step 1: [Setup]\n```bash\n# [Command with explanation]\n[ACTUAL COMMAND HERE]\n\n# Expected output:\n[SHOW ACTUAL OUTPUT]\n```\n\n### Step 2: [Main Task]\n```bash\n# [Command with explanation]\n[ACTUAL COMMAND HERE]\n\n# What to look for:\n[KEY INDICATORS]\n```\n\n### Step 3: [Analysis]\n[INTERPRET THE RESULTS]\n\n**Common Issues:**\n- Error: [Common error message] → Fix: [Solution]\n- Problem: [Common issue] → Troubleshoot: [Steps]\n\n**Challenge:** Can you [ADVANCED TASK]?\n\n**Success Criteria:**\n✓ [What success looks like]\n✓ [Expected result]\n✓ [How to verify]"
  }
}
```

#### Block 7: Real-World Application (real_world, connect_to_what_i_know)
```json
{
  "type": "real_world",
  "content": {
    "text": "## Case Study: [REAL INCIDENT/COMPANY]\n\n**Background:**\nIn [YEAR], [COMPANY/ORGANIZATION] faced [SECURITY CHALLENGE]...\n\n**The Attack/Incident:**\n[DETAILED DESCRIPTION OF WHAT HAPPENED]\n\n**Technical Details:**\n- [Vulnerability exploited]\n- [Attack vector used]\n- [Tools/techniques employed]\n- [Timeline of events]\n\n**What Went Wrong:**\n1. [Mistake 1 and why it mattered]\n2. [Mistake 2 and consequences]\n3. [Mistake 3 and impact]\n\n**Lessons Learned:**\n- [Key takeaway 1]\n- [Key takeaway 2]\n- [Key takeaway 3]\n\n**How This Relates to [TOPIC]:**\n[CONNECTION TO LESSON CONTENT]\n\n**Prevention:**\nIf they had implemented [LESSON CONCEPTS], they could have...\n\n**Additional Examples:**\n- [Brief example 2 from different company]\n- [Brief example 3 from different context]\n\n**Your Turn:**\nThink about your organization - where are similar vulnerabilities?"
  }
}
```

#### Block 8: Interactive Quiz (active_learning, gamify_it)
```json
{
  "type": "quiz",
  "content": {
    "text": "## Knowledge Check: [TOPIC AREA]\n\n**Challenge:** Test your understanding before moving forward!\n\n### Question 1: [SCENARIO-BASED QUESTION]\n[DESCRIBE REALISTIC SCENARIO]\n\nWhat should you do?\nA) [Option A]\nB) [Option B]\nC) [Option C]\nD) [Option D]\n\n**Think it through:** Consider [HINT ABOUT KEY CONCEPT]...\n\n### Question 2: [TECHNICAL QUESTION]\n[ASK ABOUT SPECIFIC TECHNICAL DETAIL]\n\nA) [Option A]\nB) [Option B]\nC) [Option C]\nD) [Option D]\n\n### Question 3: [APPLICATION QUESTION]\n[HOW WOULD YOU APPLY THIS IN PRACTICE?]\n\nA) [Option A]\nB) [Option B]\nC) [Option C]\nD) [Option D]\n\n**Discuss:** Talk through your answers with a peer before checking post-assessment."
  }
}
```

#### Block 9: Advanced Simulation (active_learning)
```json
{
  "type": "simulation",
  "content": {
    "text": "## Advanced Lab: [LAB NAME]\n\n**Scenario:**\nYou are a [ROLE] at [COMPANY TYPE]. Your team just detected [SITUATION]...\n\n**Your Mission:**\n[CLEAR OBJECTIVE WITH SUCCESS CRITERIA]\n\n**Available Resources:**\n- [Tool 1]: [Purpose]\n- [Tool 2]: [Purpose]\n- [Data/logs]: [What you have access to]\n\n**Step 1: Initial Assessment**\n[WHAT TO CHECK FIRST]\n\n```bash\n# Commands you might use:\n[COMMAND 1]\n[COMMAND 2]\n```\n\n**Step 2: Investigation**\n[DEEPER ANALYSIS STEPS]\n\n**Step 3: Action**\n[WHAT TO DO WITH FINDINGS]\n\n**Step 4: Documentation**\n[WHAT TO RECORD AND WHY]\n\n**Debrief Questions:**\n- What would you do differently?\n- What additional tools would help?\n- How could this be automated?\n\n**Bonus Challenge:**\n[OPTIONAL ADVANCED SCENARIO]"
  }
}
```

#### Block 10: Connection to Prior Knowledge (connect_to_what_i_know)
```json
{
  "type": "explanation",
  "content": {
    "text": "## Building on What You Know\n\n**Remember from [PREVIOUS LESSON/TOPIC]:**\nWe learned about [PREVIOUS CONCEPT]...\n\n**Now We're Adding:**\n[HOW THIS LESSON EXTENDS THAT KNOWLEDGE]\n\n**The Connection:**\n[PREVIOUS CONCEPT] + [NEW CONCEPT] = [COMBINED UNDERSTANDING]\n\nThink of it like building a house:\n- [Previous lesson] = Foundation\n- [This lesson] = Walls and structure\n- [Next lesson will be] = Roof and finishing\n\n**Similar Concepts:**\nThis is similar to [FAMILIAR CONCEPT FROM OUTSIDE SECURITY]...\n\n**Analogy:**\nJust like how [EVERYDAY EXAMPLE] works, [TECHNICAL CONCEPT] operates by..."
  }
}
```

#### Block 11: Reflection (meta_learning)
```json
{
  "type": "reflection",
  "content": {
    "text": "## Reflection: Learning About Learning\n\n**Pause and Think:**\n\n### About the Content:\n- What was the most surprising thing you learned?\n- Which concept do you feel most confident about?\n- What still feels unclear?\n\n### About Your Learning Process:\n- Which learning method worked best for you? (Reading, doing, watching, discussing)\n- What would you do differently if learning this topic again?\n- How will you remember this a month from now?\n\n### Application Planning:\n- When will you use this skill in the next week?\n- Who can you teach this to? (Teaching solidifies learning)\n- What metric will prove you've mastered this?\n\n### Next Steps:\n- [ ] Review the mnemonic daily for 3 days\n- [ ] Complete the hands-on exercise in your own environment\n- [ ] Explain this concept to a colleague\n- [ ] Apply this in a real project\n- [ ] Schedule follow-up practice in 2 weeks\n\n**Journal Prompt:**\nWrite 2-3 sentences about how this changes your approach to [TOPIC AREA]."
  }
}
```

#### Block 12: Mindset Coaching (reframe_limiting_beliefs)
```json
{
  "type": "mindset_coach",
  "content": {
    "text": "## Mindset Coach: You've Got This!\n\n**Acknowledge the Challenge:**\n[TOPIC] can feel overwhelming at first. That's completely normal! Every expert was once exactly where you are now.\n\n**Celebrate Your Progress:**\nYou just learned:\n- ✓ [Key concept 1]\n- ✓ [Key concept 2]\n- ✓ [Key concept 3]\n\nThat's real progress!\n\n**Reframe Common Fears:**\n\n❌ \"This is too complex for me\"\n✅ \"This is complex AND I'm learning it step by step\"\n\n❌ \"I'll never be as good as the experts\"\n✅ \"Every expert started as a beginner, and I'm building expertise daily\"\n\n❌ \"I should already know this\"\n✅ \"Learning new things is how I grow - this is exciting!\"\n\n**Growth Mindset Reminder:**\nYour brain is literally creating new neural pathways right now. Each time you practice, those pathways get stronger.\n\n**Next Session:**\nWhen you continue learning:\n1. **Start with the mnemonic** - Recall the [ACRONYM]\n2. **Review one hands-on exercise** - Muscle memory matters\n3. **Teach someone else** - Best way to solidify knowledge\n\n**You're Not Alone:**\nThousands of cybersecurity professionals learned this exact same material. You're part of a community of learners.\n\n**Keep the Momentum:**\n- Small wins compound over time\n- Consistency beats intensity\n- Progress > Perfection\n\n**Remember:** The fact that you're here, learning this, already puts you ahead. Keep going!"
  }
}
```

#### Block 13: Advanced Topics Preview (gamify_it, learning_sprint)
```json
{
  "type": "explanation",
  "content": {
    "text": "## What's Next: Level Up! 🎯\n\n**Congratulations!** You've completed [TOPIC]. You're now ready for:\n\n### Next Lesson Preview:\n**[NEXT LESSON TITLE]**\n[BRIEF TEASER OF WHAT'S COMING]\n\n### Advanced Topics to Explore:\n1. **[Advanced Topic 1]** - [Why it matters]\n2. **[Advanced Topic 2]** - [Real-world application]\n3. **[Advanced Topic 3]** - [Career benefit]\n\n### Skills You Unlocked:\n- ✅ [Skill 1]: [What you can now do]\n- ✅ [Skill 2]: [How this helps in practice]\n- ✅ [Skill 3]: [Career advancement value]\n\n### Your Learning Path:\n```\n[PREVIOUS LESSON] → [THIS LESSON] → [NEXT LESSON] → [FUTURE LESSON]\n     ✅                  ✅              ⬆️ You are here\n```\n\n### Continue the Journey:\n- **Immediate:** Take the post-assessment below\n- **This Week:** Complete the hands-on exercise in your environment\n- **This Month:** Apply this in a real project\n- **This Quarter:** Teach this to someone else\n\n### Track Your Progress:\nYou've earned **[XP AMOUNT]** XP for completing this lesson!\n\n**Domain Progression:**\n[DOMAIN] Level: [CURRENT LEVEL]\nProgress to next level: [PROGRESS BAR CONCEPT]\n\nNext milestone: [ACHIEVEMENT TO UNLOCK]\n\n**Keep Learning!** 🚀"
  }
}
```

### 4. Post-Assessment Requirements

**Create exactly 3-6 assessment questions** that test understanding:

```json
{
  "question_id": "[NEW UUID]",
  "question": "[SCENARIO-BASED QUESTION - Not just recall]",
  "options": [
    "[Correct answer with clear reasoning]",
    "[Common misconception to test understanding]",
    "[Plausible distractor]",
    "[Another plausible distractor]"
  ],
  "correct_answer": 0,
  "difficulty": [1-3],
  "type": "multiple_choice",
  "explanation": "The correct answer is [OPTION] because [DETAILED EXPLANATION]. Option B is wrong because [WHY]. Option C is incorrect because [WHY]. Option D is misleading because [WHY]. [ADD REFERENCE TO LESSON CONTENT]."
}
```

**Question Quality Checklist:**
- ✅ Scenario-based (not just "What is X?")
- ✅ Tests application, not just recall
- ✅ All options are plausible
- ✅ Explanation teaches additional concepts
- ✅ References specific lesson content
- ✅ Appropriate difficulty for lesson level

### 5. Jim Kwik Principles Implementation Checklist

**CRITICAL:** Each principle MUST be actually implemented in content, not just listed!

- ✅ **teach_like_im_10**: Used analogies, avoided jargon, simple language
- ✅ **memory_hooks**: Created mnemonics in memory_aid block
- ✅ **connect_to_what_i_know**: Referenced prior lessons, used familiar concepts
- ✅ **active_learning**: Included code_exercise, simulation, quiz blocks (2+ active blocks)
- ✅ **meta_learning**: Included reflection block about learning process
- ✅ **minimum_effective_dose**: Limited to 6-8 concepts, 12-15 blocks
- ✅ **reframe_limiting_beliefs**: Included mindset_coach block with encouragement
- ✅ **gamify_it**: Used engaging language, challenges, progression tracking
- ✅ **learning_sprint**: Clear flow (explain → practice → reflect), 30-60 min
- ✅ **multiple_memory_pathways**: Included video (auditory), diagram (visual), code_exercise (kinesthetic)

### 6. Content Quality Standards

**Language:**
- ✅ Simple, clear explanations (teach like I'm 10)
- ✅ NO jargon: Avoid "operationalize", "synergize", "grounded in repeatable practice", "measurable action", "leverage paradigm"
- ✅ Analogies to everyday concepts
- ✅ Active voice, conversational tone
- ✅ Technical accuracy with accessibility

**Examples:**
- ✅ Real companies, real incidents, real tools
- ✅ Specific dates, CVE numbers, attack names
- ✅ Actual commands, configurations, code
- ✅ Screenshots/ASCII diagrams where helpful

**Engagement:**
- ✅ Questions throughout to promote thinking
- ✅ Challenges and exercises
- ✅ Encouragement and confidence building
- ✅ Clear progression and wins

### 7. Technical Requirements

**UUIDs:**
- Generate valid UUID v4 for lesson_id
- Generate unique UUIDs for each question_id
- Format: `xxxxxxxx-xxxx-4xxx-xxxx-xxxxxxxxxxxx`

**Prerequisites:**
- Use actual UUIDs if known, or leave empty array `[]`
- Format as strings: `["uuid1", "uuid2"]`

**Estimated Time:**
- 30-60 minutes (learning sprint principle)
- Match the actual content volume

**Tags:**
- Optional but helpful: `["Career Path: SOC Analyst", "Course: SANS-FOR500"]`

### 8. Validation Checklist

Before submitting, verify:

- [ ] Valid JSON syntax (no trailing commas, proper quotes)
- [ ] lesson_id is valid UUID v4
- [ ] All 10 Jim Kwik principles listed AND implemented
- [ ] 3+ post_assessment questions with all required fields
- [ ] 12-15 content blocks with 4+ different types
- [ ] Memory aid block with actual mnemonic
- [ ] Code exercise block with actual commands
- [ ] Reflection block with meta-learning prompts
- [ ] Mindset coach block with encouragement
- [ ] Video block with real YouTube URL (or relevant video)
- [ ] Diagram block with ASCII art
- [ ] 4,000+ words total across all blocks
- [ ] No jargon (checked for: operationalize, synergize, grounded in, measurable action)
- [ ] Simple language with analogies
- [ ] Real-world examples with specific details
- [ ] estimated_time is 30-60 minutes

## Output Format

Generate the complete JSON file, properly formatted, with:
1. All required fields
2. All content blocks (12-15 blocks)
3. All assessment questions (3-6 questions)
4. All Jim Kwik principles implemented in content
5. 4,000-15,000 words of high-quality educational content

**IMPORTANT:** Actually write out all the content - don't use placeholders like "[INSERT CONTENT HERE]" or "TODO". Every content block should have complete, rich, educational content.

---

## Example Topic Substitution

**Instead of:** `Topic: [LESSON_TOPIC]`

**Use:** `Topic: SQL Injection Vulnerabilities and Prevention`

**Instead of:** `[DOMAIN FROM LIST ABOVE]`

**Use:** `pentest`

**Instead of:** `[DIFFICULTY]`

**Use:** `2` (Intermediate)

---

Generate the complete, production-ready lesson JSON now. Be thorough, educational, and engaging!
