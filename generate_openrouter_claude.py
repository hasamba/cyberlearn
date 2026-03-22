"""
Generate 10 CyberLearn lessons using OpenRouter (Claude model)
"""
import csv, json, os, sys, time
from pathlib import Path
from openai import OpenAI

OPENROUTER_KEY = os.environ.get("OPENROUTER_API_KEY", "")
LESSON_IDEAS_CSV = 'lesson_ideas.csv'
CONTENT_DIR = 'content'
STATUS_FILE = 'batch_generation_status.json'
COUNT = 10

PROMPT_TEMPLATE = """Generate a comprehensive cybersecurity lesson in JSON format based on these specifications:

**Lesson Details:**
- Lesson Number: {lesson_number}
- Domain: {domain}
- Title: {title}
- Difficulty: {difficulty} (1=beginner, 2=intermediate, 3=advanced)
- Order Index: {order_index}
- Topics: {topics}
- Prerequisites: {prerequisites}
- Tags: {tags}

**Requirements:**

1. Generate a complete lesson JSON with ALL required fields
2. Content should be 4,000-6,000 words total across all content blocks
3. Include these content block types:
   - mindset_coach (opening)
   - explanation (main technical content)
   - explanation (Teach Me Like I'm 10 section)
   - code_exercise (hands-on practice)
   - real_world (case studies)
   - memory_aid (mnemonics)
   - reflection (critical thinking)
   - mindset_coach (closing)

4. Post-assessment: 3-5 multiple choice questions with:
   - question_id (unique string)
   - question (string)
   - options (array of 4 strings)
   - correct_answer (integer 0-3)
   - explanation (detailed string)
   - type: "multiple_choice"
   - difficulty (1-3)

5. Jim Kwik principles (use ONLY these exact strings):
   - "teach_like_im_10"
   - "active_learning"
   - "memory_hooks"
   - "connect_to_what_i_know"
   - "minimum_effective_dose"
   - "multiple_memory_pathways"
   - "learning_sprint"
   - "reframe_limiting_beliefs"
   - "gamify_it"
   - "meta_learning"

6. ALL content blocks must have this structure:
   {{
     "type": "valid_type",
     "content": {{
       "text": "markdown content here"
     }}
   }}

7. Generate a unique UUID for lesson_id using this format: xxxxxxxx-xxxx-4xxx-xxxx-xxxxxxxxxxxx

8. Estimated time: 30-60 minutes

9. Return ONLY the JSON, no additional text or markdown formatting.

Generate the complete lesson JSON now:"""

def load_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, 'r') as f:
            return json.load(f)
    return {'completed': [], 'failed': [], 'skipped': []}

def save_status(status):
    with open(STATUS_FILE, 'w') as f:
        json.dump(status, f, indent=2)

def get_pending_lessons(status, count):
    planned = []
    with open(LESSON_IDEAS_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            if r.get('status', '').strip().lower() == 'planned':
                planned.append(r)
    
    pending = []
    for lesson in planned:
        ln = lesson.get('lesson_number', '')
        domain = lesson.get('domain', '')
        order_index = lesson.get('order_index', '01')
        title_slug = lesson.get('title', '').lower().replace(' ', '_').replace('(', '').replace(')', '').replace(':', '').replace('/', '_')[:50]
        filename = f"lesson_{domain}_{order_index}_{title_slug}_RICH.json"
        filepath = Path(CONTENT_DIR) / filename
        
        if ln in status['completed']:
            continue
        if filepath.exists():
            status['completed'].append(ln)
            save_status(status)
            continue
        pending.append(lesson)
        if len(pending) >= count:
            break
    
    return pending

def generate_lesson(client, lesson_spec, status):
    ln = lesson_spec.get('lesson_number', '')
    domain = lesson_spec.get('domain', '')
    order_index = lesson_spec.get('order_index', '01')
    title = lesson_spec.get('title', '')
    title_slug = title.lower().replace(' ', '_').replace('(', '').replace(')', '').replace(':', '').replace('/', '_')[:50]
    filename = f"lesson_{domain}_{order_index}_{title_slug}_RICH.json"
    filepath = Path(CONTENT_DIR) / filename

    print(f"  ⚙ [{ln}] {title}")

    prompt = PROMPT_TEMPLATE.format(
        lesson_number=ln,
        domain=domain,
        title=title,
        difficulty=lesson_spec.get('difficulty', '1'),
        order_index=order_index,
        topics=lesson_spec.get('topics', 'N/A'),
        prerequisites=lesson_spec.get('prerequisites', '[]'),
        tags=lesson_spec.get('tags', '')
    )

    try:
        response = client.chat.completions.create(
            model="anthropic/claude-3-5-sonnet",
            max_tokens=16000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        text = response.choices[0].message.content.strip()
        
        # Strip markdown code fences if present
        if text.startswith('```'):
            lines = text.split('\n')
            text = '\n'.join(lines[1:])
            if text.endswith('```'):
                text = text[:-3].strip()
        
        lesson_json = json.loads(text)
        
        # Add defaults for missing fields
        if 'jim_kwik_principles' not in lesson_json:
            lesson_json['jim_kwik_principles'] = ["teach_like_im_10", "active_learning", "memory_hooks"]
        if 'estimated_time' not in lesson_json:
            lesson_json['estimated_time'] = 45
        if 'content_blocks' not in lesson_json:
            for alt in ['blocks', 'sections', 'lessons']:
                if alt in lesson_json:
                    lesson_json['content_blocks'] = lesson_json[alt]
                    break
        
        required = ['lesson_id', 'domain', 'title', 'difficulty', 'order_index',
                    'post_assessment', 'content_blocks']
        missing = [f for f in required if f not in lesson_json]
        if missing:
            print(f"    ✗ Missing fields: {missing}")
            status['failed'].append(ln)
            save_status(status)
            return False
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(lesson_json, f, indent=2, ensure_ascii=False)
        
        print(f"    ✓ Saved: {filename}")
        status['completed'].append(ln)
        save_status(status)
        return True

    except json.JSONDecodeError as e:
        print(f"    ✗ JSON parse error: {e}")
        status['failed'].append(ln)
        save_status(status)
        return False
    except Exception as e:
        print(f"    ✗ Error: {e}")
        status['failed'].append(ln)
        save_status(status)
        return False

def main():
    client = OpenAI(
        api_key=OPENROUTER_KEY,
        base_url="https://openrouter.ai/api/v1"
    )
    
    status = load_status()
    pending = get_pending_lessons(status, COUNT)
    
    print(f"Generating {len(pending)} lessons...")
    
    domains = {}
    for l in pending:
        d = l.get('domain', 'unknown')
        domains[d] = domains.get(d, 0) + 1
    print("Domains:", domains)
    
    success = 0
    fail = 0
    
    for i, lesson in enumerate(pending, 1):
        print(f"\n[{i}/{len(pending)}]")
        if generate_lesson(client, lesson, status):
            success += 1
        else:
            fail += 1
        if i < len(pending):
            time.sleep(5)
    
    print(f"\n=== DONE: {success} success, {fail} failed ===")
    print("DOMAINS:", json.dumps(domains))
    
    status2 = load_status()
    all_planned = []
    with open(LESSON_IDEAS_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        all_planned = [r for r in reader if r.get('status', '').strip().lower() == 'planned']
    remaining = len([l for l in all_planned if l.get('lesson_number') not in status2['completed']])
    print(f"REMAINING_PENDING:{remaining}")
    
    return success, fail, domains, remaining

if __name__ == '__main__':
    main()
