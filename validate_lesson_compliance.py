"""
Validate lesson compliance with CyberLearn rich lesson standards

Requirements from CLAUDE.md:
- Length: 4,000-15,000 words (RICH lessons - extended for complex topics)
- Mindset coaching: Jim Kwik principles (all 10 principles for RICH lessons)
- Video content: At least one video block (recommended)
- Assessment: Post-assessment questions (minimum 3)
- Content variety: Multiple content block types (minimum 4 types)
- Content blocks: Minimum 5 blocks

Usage:
    python validate_lesson_compliance.py              # Print to console
    python validate_lesson_compliance.py --save-report # Save to timestamped file
    python validate_lesson_compliance.py -s            # Short form

Validates:
✓ Required fields (lesson_id, domain, title, etc.)
✓ Word count (4,000-15,000 for RICH lessons)
✓ Content blocks (min 5, valid types)
✓ Jim Kwik principles (all 10 for RICH lessons, valid values)
✓ Post-assessment (min 3 questions with all required fields)
✓ Video content (recommended)
✓ Content variety (min 4 different block types)
✓ Mindset coaching block (recommended)
✓ Memory aid block (recommended)
✓ Placeholder text detection (TODO, TBD, [INSERT], etc.)
✓ Empty content blocks (excluding video/diagram/quiz)
✓ Very short content blocks (< 10 words, may be incomplete)

Output:
- Per-lesson validation results
- Issues (violations of requirements)
- Warnings (recommendations not met)
- Summary statistics by domain
- Most common issues report
"""

import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple

# Valid content block types from ContentType enum
VALID_CONTENT_TYPES = {
    'explanation', 'video', 'diagram', 'quiz', 'simulation',
    'reflection', 'memory_aid', 'real_world', 'code_exercise', 'mindset_coach'
}

# Valid Jim Kwik principles
VALID_JIM_KWIK_PRINCIPLES = {
    'teach_like_im_10', 'memory_hooks', 'connect_to_what_i_know',
    'active_learning', 'meta_learning', 'minimum_effective_dose',
    'reframe_limiting_beliefs', 'gamify_it', 'learning_sprint',
    'multiple_memory_pathways'
}

# Rich lesson requirements
RICH_LESSON_MIN_WORDS = 4000
RICH_LESSON_MAX_WORDS = 15000  # Extended for complex lessons
MIN_CONTENT_BLOCKS = 5
MIN_POST_ASSESSMENT = 3
MIN_JIM_KWIK_PRINCIPLES = 10  # Rich lessons should use all 10 principles
RECOMMENDED_JIM_KWIK_PRINCIPLES = 10  # Standard is to use all principles

# Placeholder text detection patterns
PLACEHOLDER_PATTERNS = [
    'TODO', 'PLACEHOLDER', '[INSERT', '[ADD', 'TBD', 'TO BE DETERMINED',
    'Coming soon', 'Content coming', 'To be added', 'Will be added',
    'Lorem ipsum', 'Fill in', 'Example text', '[Your text here]',
    'XXX', 'FIXME', 'Sample content', '[Description]', '[Content]',
    '[Text here]', 'Placeholder text', 'Add content here', 'Insert text',
    'This section will', 'Content pending', '[To be completed]',
    'Need to add', 'Write content', '[Update this]'
]

# Content types that may have minimal or no text (use URLs, embedded content)
MINIMAL_TEXT_ALLOWED = {'video', 'diagram', 'quiz', 'simulation'}

class LessonValidator:
    """Validator for lesson compliance"""

    def __init__(self):
        self.issues = []
        self.warnings = []

    def validate_lesson(self, lesson_data: dict, filename: str) -> Tuple[bool, List[str], List[str]]:
        """
        Validate a single lesson for compliance

        Returns:
            (is_compliant, issues, warnings)
        """
        self.issues = []
        self.warnings = []

        # Check required fields
        self._check_required_fields(lesson_data)

        # Count words
        word_count = self._count_words(lesson_data)

        # Check content blocks
        self._check_content_blocks(lesson_data, word_count)

        # Check Jim Kwik principles
        self._check_jim_kwik_principles(lesson_data)

        # Check post assessment
        self._check_post_assessment(lesson_data)

        # Check for video content
        self._check_video_content(lesson_data)

        # Check content variety
        self._check_content_variety(lesson_data)

        # Check for placeholder text
        self._check_placeholder_text(lesson_data)

        is_compliant = len(self.issues) == 0

        return is_compliant, self.issues.copy(), self.warnings.copy()

    def _check_required_fields(self, lesson: dict):
        """Check all required fields are present"""
        required_fields = [
            'lesson_id', 'domain', 'title', 'difficulty', 'order_index',
            'prerequisites', 'concepts', 'estimated_time', 'learning_objectives',
            'post_assessment', 'jim_kwik_principles', 'content_blocks'
        ]

        for field in required_fields:
            if field not in lesson:
                self.issues.append(f"Missing required field: {field}")

    def _count_words(self, lesson: dict) -> int:
        """Count total words in lesson content"""
        total_words = 0

        if 'content_blocks' not in lesson:
            return 0

        for block in lesson['content_blocks']:
            if 'content' in block:
                content = block['content']

                # Handle string content (old format)
                if isinstance(content, str):
                    total_words += len(content.split())

                # Handle dict content with 'text' key (new format)
                elif isinstance(content, dict) and 'text' in content:
                    total_words += len(content['text'].split())

        return total_words

    def _check_content_blocks(self, lesson: dict, word_count: int):
        """Check content blocks compliance"""
        if 'content_blocks' not in lesson:
            return

        blocks = lesson['content_blocks']

        # Check minimum number of blocks
        if len(blocks) < MIN_CONTENT_BLOCKS:
            self.issues.append(
                f"Too few content blocks: {len(blocks)} (minimum: {MIN_CONTENT_BLOCKS})"
            )

        # Check word count for RICH lessons
        if '_RICH.json' in str(lesson.get('title', '')):
            if word_count < RICH_LESSON_MIN_WORDS:
                self.issues.append(
                    f"Word count too low: {word_count} words (minimum: {RICH_LESSON_MIN_WORDS} for RICH lessons)"
                )
            elif word_count > RICH_LESSON_MAX_WORDS:
                self.warnings.append(
                    f"Word count very high: {word_count} words (typical maximum: {RICH_LESSON_MAX_WORDS})"
                )

        # Check content block types are valid
        for i, block in enumerate(blocks):
            if 'type' not in block:
                self.issues.append(f"Content block {i} missing 'type' field")
            elif block['type'] not in VALID_CONTENT_TYPES:
                self.issues.append(
                    f"Content block {i} has invalid type: '{block['type']}' "
                    f"(valid types: {', '.join(sorted(VALID_CONTENT_TYPES))})"
                )

    def _check_jim_kwik_principles(self, lesson: dict):
        """Check Jim Kwik principles compliance"""
        if 'jim_kwik_principles' not in lesson:
            return

        principles = lesson['jim_kwik_principles']

        # Check for RICH lessons: should have all 10 principles
        if len(principles) < MIN_JIM_KWIK_PRINCIPLES:
            self.issues.append(
                f"Too few Jim Kwik principles: {len(principles)} (required: {MIN_JIM_KWIK_PRINCIPLES} for RICH lessons)"
            )
        elif len(principles) > MIN_JIM_KWIK_PRINCIPLES:
            self.warnings.append(
                f"More than {MIN_JIM_KWIK_PRINCIPLES} Jim Kwik principles: {len(principles)} (standard is {MIN_JIM_KWIK_PRINCIPLES})"
            )

        # Check principles are valid
        for principle in principles:
            if principle not in VALID_JIM_KWIK_PRINCIPLES:
                self.warnings.append(
                    f"Unknown Jim Kwik principle: '{principle}' "
                    f"(valid: {', '.join(sorted(VALID_JIM_KWIK_PRINCIPLES))})"
                )

    def _check_post_assessment(self, lesson: dict):
        """Check post assessment compliance"""
        if 'post_assessment' not in lesson:
            return

        assessment = lesson['post_assessment']

        # Check minimum number of questions
        if len(assessment) < MIN_POST_ASSESSMENT:
            self.issues.append(
                f"Too few assessment questions: {len(assessment)} (minimum: {MIN_POST_ASSESSMENT})"
            )

        # Check each question has required fields
        for i, question in enumerate(assessment):
            required = ['question_id', 'question', 'options', 'correct_answer',
                       'explanation', 'difficulty', 'type']

            for field in required:
                if field not in question:
                    self.issues.append(
                        f"Assessment question {i} missing '{field}' field"
                    )

    def _check_video_content(self, lesson: dict):
        """Check if lesson includes video content"""
        if 'content_blocks' not in lesson:
            return

        has_video = any(
            block.get('type') == 'video'
            for block in lesson['content_blocks']
        )

        if not has_video:
            self.warnings.append(
                "No video content block found (recommended for RICH lessons)"
            )

    def _check_content_variety(self, lesson: dict):
        """Check content block variety"""
        if 'content_blocks' not in lesson:
            return

        block_types = set(
            block.get('type')
            for block in lesson['content_blocks']
        )

        # Should have at least 4 different content types
        if len(block_types) < 4:
            self.warnings.append(
                f"Low content variety: only {len(block_types)} different block types "
                f"(recommended: 4+)"
            )

        # Should include mindset_coach block
        if 'mindset_coach' not in block_types:
            self.warnings.append(
                "No mindset coaching block found (recommended for learner motivation)"
            )

        # Should include memory_aid block
        if 'memory_aid' not in block_types:
            self.warnings.append(
                "No memory aid block found (recommended for retention)"
            )

    def _check_placeholder_text(self, lesson: dict):
        """Check for placeholder text in content blocks"""
        if 'content_blocks' not in lesson:
            return

        for i, block in enumerate(lesson['content_blocks']):
            block_type = block.get('type', 'unknown')
            content = block.get('content', {})

            # Extract text from content
            if isinstance(content, dict):
                text = content.get('text', '')
            elif isinstance(content, str):
                text = content
            else:
                text = ''

            if not text:
                # Empty text is acceptable for certain content types
                if block_type not in MINIMAL_TEXT_ALLOWED:
                    self.warnings.append(
                        f"Content block {i} ({block_type}) has empty text content"
                    )
                continue

            # Check for placeholder patterns (case-insensitive)
            text_upper = text.upper()
            for pattern in PLACEHOLDER_PATTERNS:
                if pattern.upper() in text_upper:
                    self.issues.append(
                        f"Content block {i} ({block_type}) contains placeholder text: '{pattern}'"
                    )
                    break  # Only report first match per block

            # Check for very short content (likely incomplete)
            word_count = len(text.split())
            if word_count < 10 and block_type not in MINIMAL_TEXT_ALLOWED:
                self.warnings.append(
                    f"Content block {i} ({block_type}) has very short content: {word_count} words "
                    f"(may be incomplete)"
                )


def validate_all_lessons(content_dir: Path = Path('content')) -> Dict:
    """
    Validate all lessons in content directory

    Returns summary statistics
    """

    lesson_files = sorted(content_dir.glob('lesson_*.json'))

    print(f"=== CyberLearn Lesson Compliance Validation ===\n")
    print(f"Found {len(lesson_files)} lesson files\n")
    print("=" * 80)

    validator = LessonValidator()

    stats = {
        'total': len(lesson_files),
        'compliant': 0,
        'non_compliant': 0,
        'total_issues': 0,
        'total_warnings': 0,
        'by_domain': defaultdict(lambda: {'compliant': 0, 'non_compliant': 0})
    }

    non_compliant_lessons = []

    for lesson_file in lesson_files:
        try:
            with open(lesson_file, 'r', encoding='utf-8') as f:
                lesson = json.load(f)

            is_compliant, issues, warnings = validator.validate_lesson(
                lesson, lesson_file.name
            )

            domain = lesson.get('domain', 'unknown')

            if is_compliant:
                stats['compliant'] += 1
                stats['by_domain'][domain]['compliant'] += 1
                if warnings:
                    print(f"\n[OK] {lesson_file.name}")
                    print(f"    Title: {lesson.get('title', 'N/A')}")
                    print(f"    Warnings: {len(warnings)}")
                    for warning in warnings:
                        print(f"      [!] {warning}")
            else:
                stats['non_compliant'] += 1
                stats['by_domain'][domain]['non_compliant'] += 1
                stats['total_issues'] += len(issues)

                non_compliant_lessons.append({
                    'filename': lesson_file.name,
                    'title': lesson.get('title', 'N/A'),
                    'domain': domain,
                    'issues': issues,
                    'warnings': warnings
                })

                print(f"\n[FAIL] {lesson_file.name}")
                print(f"       Title: {lesson.get('title', 'N/A')}")
                print(f"       Domain: {domain}")
                print(f"       Issues: {len(issues)}")
                for issue in issues:
                    print(f"         [X] {issue}")
                if warnings:
                    print(f"       Warnings: {len(warnings)}")
                    for warning in warnings:
                        print(f"         [!] {warning}")

            stats['total_warnings'] += len(warnings)

        except Exception as e:
            print(f"\n[ERROR] {lesson_file.name}: {e}")
            stats['non_compliant'] += 1
            stats['total_issues'] += 1

    # Print summary
    print("\n" + "=" * 80)
    print("\n=== Validation Summary ===\n")
    print(f"Total lessons validated: {stats['total']}")
    print(f"Compliant: {stats['compliant']} ({stats['compliant']/stats['total']*100:.1f}%)")
    print(f"Non-compliant: {stats['non_compliant']} ({stats['non_compliant']/stats['total']*100:.1f}%)")
    print(f"Total issues: {stats['total_issues']}")
    print(f"Total warnings: {stats['total_warnings']}")

    # Print by domain
    print("\n=== Compliance by Domain ===\n")
    for domain, counts in sorted(stats['by_domain'].items()):
        total = counts['compliant'] + counts['non_compliant']
        compliance_rate = counts['compliant'] / total * 100 if total > 0 else 0
        print(f"{domain:20s}: {counts['compliant']:3d}/{total:3d} compliant ({compliance_rate:5.1f}%)")

    # Print top issues
    if non_compliant_lessons:
        print("\n=== Non-Compliant Lessons Summary ===\n")

        # Count issue types
        issue_types = defaultdict(int)
        for lesson in non_compliant_lessons:
            for issue in lesson['issues']:
                # Extract issue type (first part before colon)
                issue_type = issue.split(':')[0] if ':' in issue else issue
                issue_types[issue_type] += 1

        print("Most common issues:")
        for issue_type, count in sorted(issue_types.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {count:3d}x {issue_type}")

    return stats


if __name__ == "__main__":
    import sys

    # Check for command line arguments
    save_report = '--save-report' in sys.argv or '-s' in sys.argv

    if save_report:
        # Redirect output to file
        import io
        from datetime import datetime

        output = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = output

        try:
            stats = validate_all_lessons()

            # Restore stdout
            sys.stdout = old_stdout

            # Save to file
            report_filename = f"lesson_compliance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(report_filename, 'w', encoding='utf-8') as f:
                f.write(output.getvalue())

            print(f"Report saved to: {report_filename}")
            print(f"\nSummary:")
            print(f"  Total lessons: {stats['total']}")
            print(f"  Compliant: {stats['compliant']} ({stats['compliant']/stats['total']*100:.1f}%)")
            print(f"  Non-compliant: {stats['non_compliant']} ({stats['non_compliant']/stats['total']*100:.1f}%)")
            print(f"  Total issues: {stats['total_issues']}")
            print(f"  Total warnings: {stats['total_warnings']}")

        except Exception as e:
            sys.stdout = old_stdout
            print(f"Error generating report: {e}")
    else:
        validate_all_lessons()
        print("\nTip: Use --save-report or -s to save this report to a file")
