"""
Rich Lesson Content Generator
Creates professional, educational lesson content automatically
"""

import json
import argparse
from uuid import uuid4
from datetime import datetime
from pathlib import Path
import sys

# Content generation prompts for different lesson types
LESSON_TEMPLATES = {
    "fundamentals": {
        "description": "Foundational concept explanation for beginners",
        "word_count": 2000,
        "focus": "Clear explanations, real-world analogies, build from basics"
    },
    "technique": {
        "description": "Attack or defense technique with step-by-step procedures",
        "word_count": 2500,
        "focus": "Practical steps, tools, detection methods, real-world examples"
    },
    "tool": {
        "description": "How to use a specific security tool",
        "word_count": 1500,
        "focus": "Installation, usage, practical examples, common use cases"
    },
    "advanced": {
        "description": "Advanced topic for experienced professionals",
        "word_count": 3000,
        "focus": "Deep technical details, attack chains, defense strategies"
    }
}

# Content generation guide
CONTENT_GUIDE = """
CRITICAL INSTRUCTIONS FOR GENERATING LESSON CONTENT:

1. DEPTH REQUIREMENTS:
   - Minimum {word_count} words of actual technical content
   - Not summaries or outlines - full explanations
   - Include specific examples, not generic statements

2. ANALOGY REQUIREMENTS:
   - Create REAL analogies that actually teach the concept
   - BAD: "Think of X like X in everyday life"
   - GOOD: "Think of a firewall like a nightclub bouncer - checks IDs (authentication),
     decides who gets in (authorization), and maintains a guest list (logging)"

3. MEMORY AIDS:
   - Real mnemonics, not just "Remember: X"
   - Acronyms, visual associations, stories
   - Example: "CIA Triad = Can I Access? (Confidentiality, Integrity, Availability)"

4. STRUCTURE:
   - Start with "why this matters" (motivation)
   - Explain core concepts clearly
   - Provide step-by-step examples
   - Include attack AND defense perspectives
   - End with key takeaways

5. EXAMPLES:
   - Use real-world incidents and case studies
   - Include specific tools, commands, procedures
   - Show both successful attacks and defenses

6. QUIZ QUESTIONS:
   - Test understanding, not memorization
   - Include detailed explanations for each answer
   - Provide memory aids for each question
"""


def generate_content_prompt(title, domain, difficulty, concepts, lesson_type="fundamentals"):
    """Generate a detailed prompt for creating lesson content"""

    template = LESSON_TEMPLATES.get(lesson_type, LESSON_TEMPLATES["fundamentals"])

    prompt = f"""
Create comprehensive educational content for a cybersecurity lesson.

LESSON DETAILS:
- Title: {title}
- Domain: {domain}
- Difficulty: {difficulty}/4 (1=Beginner, 2=Intermediate, 3=Advanced, 4=Expert)
- Key Concepts: {', '.join(concepts)}
- Lesson Type: {lesson_type} ({template['description']})

{CONTENT_GUIDE.format(word_count=template['word_count'])}

FOCUS AREAS FOR THIS LESSON:
{template['focus']}

REQUIRED OUTPUT STRUCTURE:

1. INTRODUCTION BLOCK:
   - Why this topic matters (motivational)
   - Real-world relevance
   - What students will learn

2. MAIN CONTENT (3-5 blocks):
   - Core concept explanations ({template['word_count']}+ words total)
   - Technical depth appropriate for difficulty {difficulty}
   - Real-world examples and case studies
   - Visual aids or diagrams (ASCII art if helpful)

3. PRACTICAL EXAMPLES:
   - Step-by-step procedures
   - Tools and commands (if applicable)
   - Attack scenarios (for offensive topics)
   - Defense strategies (for defensive topics)

4. SIMPLIFIED EXPLANATIONS:
   - ELI10 (Explain Like I'm 10) analogies
   - Must be real comparisons, not placeholder text

5. MEMORY AIDS:
   - Mnemonics and acronyms
   - Visual associations
   - Memory hooks

6. QUIZ QUESTIONS (5-6 questions):
   - Multiple choice
   - Test understanding of key concepts
   - Include detailed explanations
   - Provide memory aids

Format as structured JSON following the CyberLearn lesson schema.
"""

    return prompt


def create_lesson_structure(title, domain, difficulty, concepts, order_index=1):
    """Create the basic lesson JSON structure"""

    lesson_id = str(uuid4())

    lesson = {
        "lesson_id": lesson_id,
        "domain": domain,
        "title": title,
        "subtitle": f"Understanding {concepts[0] if concepts else title}",
        "difficulty": difficulty,
        "estimated_time": 25 + (difficulty * 5),  # 25-45 minutes based on difficulty
        "order_index": order_index,
        "prerequisites": [],
        "learning_objectives": [
            f"Understand {concept}" for concept in concepts[:4]
        ],
        "content_blocks": [],
        "pre_assessment": None,
        "post_assessment": [],
        "mastery_threshold": 80,
        "jim_kwik_principles": [
            "teach_like_im_10",
            "memory_hooks",
            "connect_to_what_i_know",
            "active_learning",
            "meta_learning"
        ],
        "base_xp_reward": 100 * difficulty,
        "badge_unlock": None,
        "is_core_concept": difficulty <= 2,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "author": "CyberLearn Content Generator",
        "version": "2.0"
    }

    return lesson


def add_content_block(lesson, block_type, title, content_text, simplified="", memory_aids=None, real_world=""):
    """Add a content block to the lesson"""

    block = {
        "block_id": str(uuid4()),
        "type": block_type,
        "title": title,
        "content": {
            "text": content_text
        },
        "simplified_explanation": simplified,
        "memory_aids": memory_aids or [],
        "real_world_connection": real_world,
        "reflection_prompt": "What questions do you have about this topic?",
        "is_interactive": False,
        "xp_reward": 0
    }

    lesson["content_blocks"].append(block)


def add_quiz_question(lesson, question, options, correct_idx, explanation, memory_aid=""):
    """Add a quiz question to the lesson"""

    quiz = {
        "question_id": f"q{len(lesson['post_assessment']) + 1}",
        "type": "multiple_choice",
        "question": question,
        "options": options,
        "correct_answer": correct_idx,
        "explanation": explanation,
        "difficulty": lesson["difficulty"],
        "memory_aid": memory_aid,
        "points": 10
    }

    lesson["post_assessment"].append(quiz)


def generate_placeholder_rich_lesson(title, domain, difficulty, concepts, order_index=1):
    """
    Generate a lesson with rich structure but content that needs AI enhancement.
    This is a starting point that users can customize.
    """

    lesson = create_lesson_structure(title, domain, difficulty, concepts, order_index)

    # Add introduction block
    add_content_block(
        lesson,
        "mindset_coach",
        "Why This Matters",
        f"You're about to learn {title}, a critical concept in {domain}. "
        f"This knowledge is used by security professionals daily and understanding it "
        f"will give you practical skills you can apply immediately.",
        simplified=f"This lesson teaches {concepts[0]} - one of the building blocks of cybersecurity.",
        memory_aids=[
            f"{title} is fundamental to {domain}",
            "This concept is used in real-world security operations"
        ],
        real_world=f"Organizations use {concepts[0]} to protect their systems and data."
    )

    # Add main concept blocks
    for i, concept in enumerate(concepts[:3]):
        add_content_block(
            lesson,
            "explanation",
            f"{concept.title()}",
            f"**{concept.title()}** is a key concept in {domain}.\n\n"
            f"[CONTENT TO BE GENERATED]\n\n"
            f"This section should explain:\n"
            f"- What {concept} is and why it matters\n"
            f"- How it works technically\n"
            f"- Real-world examples and use cases\n"
            f"- Common mistakes and best practices\n\n"
            f"Minimum 500 words of detailed technical content.",
            simplified=f"Think of {concept} like... [ADD REAL ANALOGY HERE]",
            memory_aids=[
                f"Key point about {concept}",
                f"Remember: {concept} is used for..."
            ],
            real_world=f"In practice, {concept} is essential for..."
        )

    # Add summary block
    add_content_block(
        lesson,
        "memory_aid",
        "Key Takeaways",
        "**Summary of Key Points:**\n\n" + "\n".join([
            f"- {concept}: [Key insight]" for concept in concepts
        ]),
        simplified="Remember these core concepts and you'll understand the fundamentals.",
        memory_aids=[f"Remember: {c}" for c in concepts[:3]]
    )

    # Add sample quiz questions
    add_quiz_question(
        lesson,
        f"What is {concepts[0] if concepts else 'the main concept'}?",
        [
            "[Option A - correct answer]",
            "[Option B - incorrect]",
            "[Option C - incorrect]",
            "[Option D - incorrect]"
        ],
        0,
        f"{concepts[0]} is [detailed explanation of why A is correct and others are wrong].",
        f"Remember: {concepts[0]} = [memory aid]"
    )

    add_quiz_question(
        lesson,
        f"Why is {title} important?",
        [
            "[Option A - incorrect]",
            "[Option B - correct answer about importance]",
            "[Option C - incorrect]",
            "[Option D - incorrect]"
        ],
        1,
        f"[Detailed explanation of why this concept is important]",
        "Think: [Memory aid]"
    )

    return lesson


def save_lesson(lesson, output_dir="content"):
    """Save lesson to JSON file"""

    Path(output_dir).mkdir(exist_ok=True)

    # Create filename from title
    domain = lesson["domain"]
    title_slug = lesson["title"].lower().replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_")
    order = lesson["order_index"]

    filename = f"lesson_{domain}_{order:02d}_{title_slug}.json"
    filepath = Path(output_dir) / filename

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(lesson, f, indent=2, ensure_ascii=False)

    return filepath


def interactive_mode():
    """Interactive lesson creation"""

    print("=" * 60)
    print("Rich Lesson Content Generator - Interactive Mode")
    print("=" * 60)
    print()

    # Get lesson details
    print("📚 Lesson Details:")
    domain = input("  Domain (fundamentals/dfir/malware/active_directory/pentest/red_team/blue_team): ").strip()
    title = input("  Lesson Title: ").strip()
    difficulty = int(input("  Difficulty (1-4): ").strip())
    concepts_str = input("  Key Concepts (comma-separated): ").strip()
    concepts = [c.strip() for c in concepts_str.split(",")]
    order = int(input("  Order Index: ").strip() or "1")

    print()
    print("📝 Lesson Type:")
    print("  1. Fundamentals (foundational concepts)")
    print("  2. Technique (attack/defense procedures)")
    print("  3. Tool (how to use specific tool)")
    print("  4. Advanced (expert-level deep dive)")
    lesson_type_idx = input("  Choose type (1-4): ").strip() or "1"
    lesson_types = ["fundamentals", "technique", "tool", "advanced"]
    lesson_type = lesson_types[int(lesson_type_idx) - 1]

    print()
    print("🔧 Generating lesson structure...")

    # Generate lesson
    lesson = generate_placeholder_rich_lesson(title, domain, difficulty, concepts, order)

    # Save
    filepath = save_lesson(lesson)

    print(f"✅ Created: {filepath}")
    print()
    print("📄 Content Template Generated")
    print("=" * 60)
    print()
    print("NEXT STEPS:")
    print()
    print("1. EDIT THE CONTENT:")
    print(f"   Open: {filepath}")
    print("   Replace [CONTENT TO BE GENERATED] sections with real content")
    print()
    print("2. CONTENT REQUIREMENTS:")
    print(f"   - {LESSON_TEMPLATES[lesson_type]['word_count']}+ words minimum")
    print("   - Real analogies (not 'like X in everyday life')")
    print("   - Specific examples and case studies")
    print("   - Memory techniques that actually work")
    print()
    print("3. USE THE GUIDE:")
    prompt = generate_content_prompt(title, domain, difficulty, concepts, lesson_type)
    prompt_file = filepath.parent / f"{filepath.stem}_PROMPT.txt"
    with open(prompt_file, 'w') as f:
        f.write(prompt)
    print(f"   Content guide saved to: {prompt_file}")
    print("   Use this as reference when writing content")
    print()
    print("4. LOAD INTO DATABASE:")
    print("   python load_all_lessons.py")
    print()
    print("=" * 60)

    return filepath


def batch_mode(batch_file):
    """Generate multiple lessons from a batch file"""

    print("=" * 60)
    print("Batch Lesson Generation")
    print("=" * 60)

    # Read batch configuration
    with open(batch_file, 'r') as f:
        if batch_file.endswith('.json'):
            lessons_config = json.load(f)
        else:
            import yaml
            lessons_config = yaml.safe_load(f)

    generated = []

    for lesson_config in lessons_config:
        title = lesson_config["title"]
        domain = lesson_config["domain"]
        difficulty = lesson_config["difficulty"]
        concepts = lesson_config["concepts"]
        order = lesson_config.get("order_index", 1)

        print(f"\n📝 Generating: {title}")

        lesson = generate_placeholder_rich_lesson(title, domain, difficulty, concepts, order)
        filepath = save_lesson(lesson)

        print(f"   ✅ Created: {filepath}")
        generated.append(filepath)

    print()
    print("=" * 60)
    print(f"✅ Generated {len(generated)} lessons")
    print("=" * 60)

    return generated


def main():
    parser = argparse.ArgumentParser(description="Generate rich lesson content")

    parser.add_argument("--interactive", "-i", action="store_true",
                       help="Interactive mode - answer questions to create lesson")

    parser.add_argument("--batch", "-b", type=str,
                       help="Batch mode - generate from JSON/YAML file")

    parser.add_argument("--title", "-t", type=str,
                       help="Lesson title")

    parser.add_argument("--domain", "-d", type=str,
                       help="Domain (fundamentals, red_team, etc.)")

    parser.add_argument("--difficulty", type=int, choices=[1,2,3,4],
                       help="Difficulty (1-4)")

    parser.add_argument("--concepts", "-c", type=str,
                       help="Key concepts (comma-separated)")

    parser.add_argument("--order", "-o", type=int, default=1,
                       help="Order index")

    parser.add_argument("--output", type=str, default="content",
                       help="Output directory")

    args = parser.parse_args()

    if args.interactive:
        interactive_mode()

    elif args.batch:
        batch_mode(args.batch)

    elif args.title and args.domain and args.difficulty and args.concepts:
        # Command-line mode
        concepts = [c.strip() for c in args.concepts.split(",")]

        print(f"Generating lesson: {args.title}")
        lesson = generate_placeholder_rich_lesson(
            args.title,
            args.domain,
            args.difficulty,
            concepts,
            args.order
        )

        filepath = save_lesson(lesson, args.output)
        print(f"✅ Created: {filepath}")

        # Generate content guide
        prompt = generate_content_prompt(args.title, args.domain, args.difficulty, concepts)
        prompt_file = Path(args.output) / f"{filepath.stem}_PROMPT.txt"
        with open(prompt_file, 'w') as f:
            f.write(prompt)
        print(f"📄 Content guide: {prompt_file}")

    else:
        parser.print_help()
        print()
        print("Examples:")
        print("  # Interactive mode")
        print("  python create_rich_lesson.py --interactive")
        print()
        print("  # Command-line mode")
        print('  python create_rich_lesson.py -t "Kerberos Authentication" -d active_directory -c "TGT,TGS,KDC,Tickets" --difficulty 3')
        print()
        print("  # Batch mode")
        print("  python create_rich_lesson.py --batch lessons_to_generate.json")


if __name__ == "__main__":
    main()
