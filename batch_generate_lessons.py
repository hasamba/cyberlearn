"""
Batch Lesson Generator for CyberLearn
Reads lesson_ideas.csv and generates comprehensive lessons using Anthropic API
"""

import csv
import json
import os
import time
from pathlib import Path
import anthropic

# Configuration
API_KEY = os.environ.get('ANTHROPIC_API_KEY')  # Set this environment variable
LESSON_IDEAS_CSV = 'lesson_ideas.csv'
CONTENT_DIR = 'content'
STATUS_FILE = 'batch_generation_status.json'

# Lesson generation prompt template
LESSON_GENERATION_PROMPT = """Generate a comprehensive cybersecurity lesson in JSON format based on these specifications:

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
   - "teach_like_im_10" (MANDATORY - include dedicated "Teach Me Like I'm 10" section)
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
    """Load generation status"""
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, 'r') as f:
            return json.load(f)
    return {'completed': [], 'failed': [], 'skipped': []}

def save_status(status):
    """Save generation status"""
    with open(STATUS_FILE, 'w') as f:
        json.dump(status, f, indent=2)

def get_planned_lessons():
    """Get all planned lessons from CSV"""
    with open(LESSON_IDEAS_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [r for r in reader if r.get('status', '').strip().lower() == 'planned']

def generate_lesson(client, lesson_spec, status):
    """Generate a single lesson using Claude API"""
    lesson_number = lesson_spec['lesson_number']

    # Check if already processed
    if lesson_number in status['completed']:
        print(f"  ✓ Already completed: #{lesson_number}")
        return True
    if lesson_number in status['skipped']:
        print(f"  ⊘ Previously skipped: #{lesson_number}")
        return False

    # Build filename
    domain = lesson_spec['domain']
    order_index = lesson_spec['order_index']
    title_slug = lesson_spec['title'].lower().replace(' ', '_').replace('(', '').replace(')', '').replace(':', '').replace('/', '_')[:50]
    filename = f"lesson_{domain}_{order_index}_{title_slug}_RICH.json"
    filepath = Path(CONTENT_DIR) / filename

    # Skip if file already exists
    if filepath.exists():
        print(f"  ✓ File exists: {filename}")
        status['completed'].append(lesson_number)
        save_status(status)
        return True

    print(f"  ⚙ Generating lesson #{lesson_number}: {lesson_spec['title']}")

    try:
        # Format prompt
        prompt = LESSON_GENERATION_PROMPT.format(
            lesson_number=lesson_number,
            domain=lesson_spec['domain'],
            title=lesson_spec['title'],
            difficulty=lesson_spec['difficulty'],
            order_index=lesson_spec['order_index'],
            topics=lesson_spec.get('topics', 'N/A'),
            prerequisites=lesson_spec.get('prerequisites', '[]'),
            tags=lesson_spec.get('tags', 'Built-In')
        )

        # Call Claude API
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=16000,
            temperature=0.7,
            messages=[{"role": "user", "content": prompt}]
        )

        # Extract JSON from response
        response_text = message.content[0].text

        # Try to parse as JSON
        try:
            # Remove markdown code blocks if present
            if response_text.startswith('```'):
                response_text = response_text.split('```')[1]
                if response_text.startswith('json'):
                    response_text = response_text[4:]

            lesson_json = json.loads(response_text)

            # Validate required fields
            required_fields = ['lesson_id', 'domain', 'title', 'difficulty', 'order_index',
                             'prerequisites', 'concepts', 'estimated_time', 'learning_objectives',
                             'post_assessment', 'jim_kwik_principles', 'content_blocks', 'tags']

            missing = [f for f in required_fields if f not in lesson_json]
            if missing:
                print(f"    ✗ Missing fields: {missing}")
                status['failed'].append(lesson_number)
                save_status(status)
                return False

            # Save lesson
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(lesson_json, f, indent=2, ensure_ascii=False)

            print(f"    ✓ Saved: {filename}")
            status['completed'].append(lesson_number)
            save_status(status)
            return True

        except json.JSONDecodeError as e:
            print(f"    ✗ JSON parse error: {e}")
            # Save response for debugging
            debug_file = f"debug_lesson_{lesson_number}.txt"
            with open(debug_file, 'w', encoding='utf-8') as f:
                f.write(response_text)
            print(f"    ℹ Debug output saved to {debug_file}")
            status['failed'].append(lesson_number)
            save_status(status)
            return False

    except anthropic.APIError as e:
        print(f"    ✗ API Error: {e}")
        status['failed'].append(lesson_number)
        save_status(status)
        return False

    except Exception as e:
        print(f"    ✗ Unexpected error: {e}")
        status['failed'].append(lesson_number)
        save_status(status)
        return False

def main():
    """Main batch generation process"""
    print("=" * 80)
    print("CyberLearn Batch Lesson Generator")
    print("=" * 80)

    # Check API key
    if not API_KEY:
        print("\n✗ ERROR: ANTHROPIC_API_KEY environment variable not set!")
        print("\nSet it with:")
        print("  export ANTHROPIC_API_KEY='your-api-key'  # Linux/Mac")
        print("  set ANTHROPIC_API_KEY=your-api-key      # Windows")
        return

    # Initialize
    client = anthropic.Anthropic(api_key=API_KEY)
    status = load_status()
    lessons = get_planned_lessons()

    print(f"\nFound {len(lessons)} planned lessons")
    print(f"Already completed: {len(status['completed'])}")
    print(f"Failed: {len(status['failed'])}")
    print(f"To generate: {len(lessons) - len(status['completed'])}")

    # Group by domain
    by_domain = {}
    for lesson in lessons:
        domain = lesson['domain']
        by_domain.setdefault(domain, []).append(lesson)

    print(f"\nLessons by domain:")
    for domain, domain_lessons in sorted(by_domain.items(), key=lambda x: -len(x[1])):
        print(f"  {domain}: {len(domain_lessons)} lessons")

    # Confirm before proceeding
    print(f"\n{'=' * 80}")
    response = input("Start batch generation? (yes/no): ")
    if response.lower() not in ['yes', 'y']:
        print("Cancelled.")
        return

    # Process lessons
    print(f"\n{'=' * 80}")
    print("Generating lessons...")
    print(f"{'=' * 80}\n")

    success_count = 0
    fail_count = 0

    for i, lesson in enumerate(lessons, 1):
        print(f"[{i}/{len(lessons)}] Domain: {lesson['domain']}")

        if generate_lesson(client, lesson, status):
            success_count += 1
        else:
            fail_count += 1

        # Rate limiting: wait between requests
        if i < len(lessons):
            time.sleep(2)  # 2 seconds between requests

        # Progress update every 10 lessons
        if i % 10 == 0:
            print(f"\n--- Progress: {i}/{len(lessons)} ({i*100//len(lessons)}%) ---")
            print(f"    Success: {success_count}, Failed: {fail_count}\n")

    # Final summary
    print(f"\n{'=' * 80}")
    print("BATCH GENERATION COMPLETE")
    print(f"{'=' * 80}")
    print(f"Total lessons processed: {len(lessons)}")
    print(f"Successfully generated: {success_count}")
    print(f"Failed: {fail_count}")
    print(f"Success rate: {success_count*100//len(lessons)}%")

    if fail_count > 0:
        print(f"\nFailed lessons: {status['failed']}")
        print("Check debug_lesson_*.txt files for details")

    print(f"\nLesson files saved to: {CONTENT_DIR}/")
    print(f"Status file: {STATUS_FILE}")
    print("\nNext steps:")
    print("  1. Review generated lessons")
    print("  2. Load into database with: python scripts/sync_lessons.py")
    print("  3. Test in Streamlit app")

if __name__ == '__main__':
    main()
