"""
AI-Assisted Content Enhancement Tool
Helps you use AI (Claude/ChatGPT) to generate rich content for lessons
"""

import json
import sys
from pathlib import Path
import argparse

def extract_content_markers(lesson_file):
    """Find all [CONTENT TO BE GENERATED] markers in a lesson"""

    with open(lesson_file, 'r', encoding='utf-8') as f:
        lesson = json.load(f)

    markers = []

    # Check content blocks
    for i, block in enumerate(lesson.get('content_blocks', [])):
        content_text = block.get('content', {}).get('text', '')
        if '[CONTENT TO BE GENERATED]' in content_text:
            markers.append({
                'location': f'content_blocks[{i}]',
                'title': block.get('title', 'Untitled'),
                'type': block.get('type', 'unknown'),
                'current': content_text
            })

    return markers, lesson


def generate_ai_prompt_for_block(lesson, block_info):
    """Generate a detailed AI prompt for a specific content block"""

    prompt = f"""
Generate professional educational content for a cybersecurity lesson content block.

LESSON CONTEXT:
- Title: {lesson['title']}
- Domain: {lesson['domain']}
- Difficulty: {lesson['difficulty']}/4
- Block Title: {block_info['title']}
- Block Type: {block_info['type']}

CONTENT REQUIREMENTS:

1. LENGTH: 500-800 words minimum
2. DEPTH: Technical and detailed, appropriate for difficulty level {lesson['difficulty']}
3. STRUCTURE:
   - Start with clear definition/explanation
   - Provide specific examples
   - Include technical details
   - Show real-world applications
   - If attack technique: Include detection/defense

4. STYLE:
   - Clear and educational
   - No fluff or filler
   - Specific over generic
   - Examples over theory alone

5. INCLUDE:
   - Specific tools/commands (if applicable)
   - Real-world examples or case studies
   - Attack steps (for offensive topics)
   - Defense strategies (always)
   - Common mistakes to avoid

OUTPUT FORMAT:
Provide only the content text (no JSON, no formatting).
Write 500-800 words of technical educational content.

Begin writing now:
"""

    return prompt


def generate_analogy_prompt(lesson, block_info):
    """Generate prompt for creating ELI10 analogy"""

    prompt = f"""
Create a simple, effective analogy to explain this cybersecurity concept to a 10-year-old.

CONCEPT: {block_info['title']} (from {lesson['title']})
DOMAIN: {lesson['domain']}

REQUIREMENTS:
1. Use everyday objects/situations
2. Accurately represent the technical concept
3. Make it memorable
4. 2-3 sentences maximum
5. Don't just say "like X in everyday life" - be specific!

BAD Example: "Think of authentication like authentication in real life"
GOOD Example: "Think of authentication like showing your ID at airport security. The TSA agent checks that the photo matches your face (verifying WHO you are), then your boarding pass determines which gate you can access (authorization - WHAT you can do)."

Create analogy for {block_info['title']}:
"""

    return prompt


def generate_memory_aid_prompt(lesson, block_info):
    """Generate prompt for creating memory aids"""

    prompt = f"""
Create 2-3 effective memory aids (mnemonics) for remembering this concept.

CONCEPT: {block_info['title']}
CONTEXT: {lesson['title']} ({lesson['domain']})

TYPES OF MEMORY AIDS:
1. Acronyms (CIA = Confidentiality, Integrity, Availability)
2. Visual associations (Firewall = Nightclub bouncer)
3. Word play (Kerberoasting = Roasting like cooking/cracking passwords)
4. Analogies (see above)
5. Rhymes or alliteration

Create 2-3 memory aids:
"""

    return prompt


def interactive_enhancement(lesson_file):
    """Interactive mode to enhance lesson with AI assistance"""

    print("=" * 70)
    print("AI-Assisted Content Enhancement")
    print("=" * 70)
    print()

    markers, lesson = extract_content_markers(lesson_file)

    if not markers:
        print("✅ No content markers found - lesson already complete!")
        return

    print(f"📄 Lesson: {lesson['title']}")
    print(f"📊 Found {len(markers)} sections needing content")
    print()

    for i, marker in enumerate(markers, 1):
        print(f"\n{'='*70}")
        print(f"Section {i}/{len(markers)}: {marker['title']}")
        print(f"Type: {marker['type']}")
        print('='*70)
        print()

        print("Choose what to generate:")
        print("  1. Main content (500-800 words)")
        print("  2. ELI10 analogy")
        print("  3. Memory aids")
        print("  4. All of the above")
        print("  5. Skip this section")
        print()

        choice = input("Your choice (1-5): ").strip()

        if choice == '5':
            continue

        print()
        print("=" * 70)
        print("COPY THIS PROMPT TO CLAUDE/CHATGPT:")
        print("=" * 70)
        print()

        if choice in ['1', '4']:
            print(generate_ai_prompt_for_block(lesson, marker))
            print()
            print("-" * 70)
            print()

        if choice in ['2', '4']:
            print("ANALOGY PROMPT:")
            print(generate_analogy_prompt(lesson, marker))
            print()
            print("-" * 70)
            print()

        if choice in ['3', '4']:
            print("MEMORY AIDS PROMPT:")
            print(generate_memory_aid_prompt(lesson, marker))
            print()

        print("=" * 70)
        print()
        input("Press Enter when you've generated and copied the content...")
        print()

    print()
    print("=" * 70)
    print("✅ Enhancement prompts generated!")
    print("=" * 70)
    print()
    print("NEXT STEPS:")
    print(f"1. Open: {lesson_file}")
    print("2. Replace [CONTENT TO BE GENERATED] with AI-generated content")
    print("3. Run: python load_all_lessons.py")
    print("4. Test: streamlit run app.py")


def batch_generate_prompts(lesson_files_pattern):
    """Generate all prompts for multiple lessons and save to file"""

    lesson_files = list(Path('.').glob(lesson_files_pattern))

    print(f"Found {len(lesson_files)} lessons to process")

    all_prompts = []

    for lesson_file in lesson_files:
        markers, lesson = extract_content_markers(lesson_file)

        if not markers:
            continue

        for marker in markers:
            prompt_data = {
                'file': str(lesson_file),
                'lesson_title': lesson['title'],
                'section': marker['title'],
                'prompts': {
                    'content': generate_ai_prompt_for_block(lesson, marker),
                    'analogy': generate_analogy_prompt(lesson, marker),
                    'memory_aids': generate_memory_aid_prompt(lesson, marker)
                }
            }
            all_prompts.append(prompt_data)

    # Save to file
    output_file = 'ai_prompts_batch.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_prompts, f, indent=2)

    print(f"\n✅ Saved {len(all_prompts)} prompts to: {output_file}")
    print()
    print("You can now:")
    print("1. Open ai_prompts_batch.json")
    print("2. Use each prompt with Claude/ChatGPT")
    print("3. Copy generated content back to lesson files")


def main():
    parser = argparse.ArgumentParser(description="AI-assisted lesson content enhancement")

    parser.add_argument('lesson_file', nargs='?',
                       help='Lesson JSON file to enhance')

    parser.add_argument('--batch', '-b',
                       help='Generate prompts for multiple lessons (glob pattern)')

    parser.add_argument('--list', '-l', action='store_true',
                       help='List lessons needing enhancement')

    args = parser.parse_args()

    if args.list:
        # Find all lessons with content markers
        lesson_files = Path('content').glob('lesson_*.json')
        needs_enhancement = []

        for lesson_file in lesson_files:
            try:
                markers, lesson = extract_content_markers(lesson_file)
                if markers:
                    needs_enhancement.append((lesson_file, lesson['title'], len(markers)))
            except:
                pass

        if needs_enhancement:
            print("\nLessons needing content enhancement:")
            print("=" * 70)
            for file, title, count in needs_enhancement:
                print(f"  {file.name}")
                print(f"    Title: {title}")
                print(f"    Sections needing content: {count}")
                print()
        else:
            print("\n✅ All lessons have complete content!")

    elif args.batch:
        batch_generate_prompts(args.batch)

    elif args.lesson_file:
        interactive_enhancement(args.lesson_file)

    else:
        parser.print_help()
        print()
        print("Examples:")
        print("  # Enhance a single lesson interactively")
        print("  python enhance_with_ai.py content/lesson_pentest_01_methodology.json")
        print()
        print("  # List all lessons needing enhancement")
        print("  python enhance_with_ai.py --list")
        print()
        print("  # Generate prompts for all lessons in batch")
        print("  python enhance_with_ai.py --batch 'content/lesson_*.json'")


if __name__ == "__main__":
    main()
