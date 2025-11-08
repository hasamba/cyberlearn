"""
Deep content quality validation for CyberLearn lessons.

This script validates that Jim Kwik principles are ACTUALLY IMPLEMENTED
in the lesson content, not just listed in metadata.

Checks for:
1. teach_like_im_10: Simple language, analogies, no excessive jargon
2. memory_hooks: Mnemonics, acronyms, visual associations
3. connect_to_what_i_know: References to prior knowledge
4. active_learning: Hands-on exercises, practice tasks
5. meta_learning: Reflection on learning process
6. minimum_effective_dose: Focused, not overwhelming
7. reframe_limiting_beliefs: Confidence building, encouragement
8. gamify_it: Challenges, progression, engagement
9. learning_sprint: Structured flow, clear progression
10. multiple_memory_pathways: Visual, auditory, kinesthetic variety
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

# Jargon detection patterns
JARGON_PATTERNS = [
    r'\bsynergize\b',
    r'\bleverag(e|ing)\b',
    r'\bparadigm\b',
    r'\boperationalize\b',
    r'\bmeasurable action\b',
    r'\brepeatable practice\b',
    r'\bgrounded in\b',
    r'\bclarifies how to\b',
    r'\btranslate.*commitments\b',
    r'\bbaseline data\b',
    r'\bescalation triggers\b',
]

# Simple language indicators
SIMPLE_LANGUAGE_PATTERNS = [
    r'like (a|an|the) ',  # Analogies: "like a hotel", "like a key ring"
    r'think of .* as ',    # Comparisons: "think of it as"
    r'imagine ',           # Visualization
    r'for example',        # Concrete examples
    r'in simple terms',
    r'in other words',
    r'basically',
    r'\(.*\?+.*\)',       # Questions in parentheses: "(WHO are you?)"
]

class ContentQualityResult:
    def __init__(self, lesson_file: str):
        self.lesson_file = lesson_file
        self.principle_checks: Dict[str, Dict[str, any]] = {}
        self.overall_score = 0
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.suggestions: List[str] = []

    def add_principle_check(self, principle: str, implemented: bool, evidence: List[str], issues: List[str]):
        self.principle_checks[principle] = {
            'implemented': implemented,
            'evidence': evidence,
            'issues': issues
        }

    def calculate_score(self):
        """Calculate overall quality score (0-100)."""
        if not self.principle_checks:
            return 0

        implemented_count = sum(1 for p in self.principle_checks.values() if p['implemented'])
        self.overall_score = int((implemented_count / len(self.principle_checks)) * 100)
        return self.overall_score

    def print_report(self, verbose: bool = False):
        filename = os.path.basename(self.lesson_file)
        score = self.calculate_score()

        if score >= 80:
            grade = "[EXCELLENT]"
        elif score >= 60:
            grade = "[GOOD]"
        elif score >= 40:
            grade = "[FAIR]"
        else:
            grade = "[POOR]"

        print(f"\n{'='*80}")
        print(f"{grade} {score}% - {filename}")
        print(f"{'='*80}")

        if verbose:
            for principle, check in self.principle_checks.items():
                status = "[PASS]" if check['implemented'] else "[FAIL]"
                print(f"\n{status} {principle}")

                if check['evidence']:
                    print("  Evidence:")
                    for ev in check['evidence'][:2]:  # Show first 2 pieces of evidence
                        # Remove problematic unicode characters
                        clean_ev = ev[:100].encode('ascii', 'ignore').decode('ascii')
                        print(f"    - {clean_ev}...")

                if check['issues']:
                    print("  Issues:")
                    for issue in check['issues'][:2]:  # Show first 2 issues
                        print(f"    [!] {issue}")

        # Summary
        implemented = sum(1 for p in self.principle_checks.values() if p['implemented'])
        total = len(self.principle_checks)
        print(f"\nPrinciples Implemented: {implemented}/{total}")

        if self.suggestions:
            print("\nSuggestions for Improvement:")
            for suggestion in self.suggestions[:3]:
                print(f"  - {suggestion}")


def count_jargon(text: str) -> int:
    """Count jargon phrases in text."""
    count = 0
    for pattern in JARGON_PATTERNS:
        count += len(re.findall(pattern, text, re.IGNORECASE))
    return count


def count_simple_language(text: str) -> int:
    """Count simple language indicators in text."""
    count = 0
    for pattern in SIMPLE_LANGUAGE_PATTERNS:
        count += len(re.findall(pattern, text, re.IGNORECASE))
    return count


def find_analogies(text: str) -> List[str]:
    """Find analogies and comparisons in text."""
    analogies = []

    # Look for "like a/an/the" patterns
    matches = re.finditer(r'([^.!?]*like (a|an|the) [^.!?]+[.!?])', text, re.IGNORECASE)
    for match in matches:
        analogies.append(match.group(1).strip())

    # Look for "think of ... as" patterns
    matches = re.finditer(r'([^.!?]*think of [^.!?]+ as [^.!?]+[.!?])', text, re.IGNORECASE)
    for match in matches:
        analogies.append(match.group(1).strip())

    return analogies[:5]  # Return up to 5 analogies


def validate_teach_like_im_10(lesson: dict) -> Tuple[bool, List[str], List[str]]:
    """Check if lesson uses simple language and analogies."""
    evidence = []
    issues = []

    # Combine all text content
    all_text = []
    for block in lesson.get('content_blocks', []):
        if isinstance(block.get('content'), dict):
            text = block['content'].get('text', '')
            all_text.append(text)

    combined_text = ' '.join(all_text)

    # Count jargon vs simple language
    jargon_count = count_jargon(combined_text)
    simple_count = count_simple_language(combined_text)

    # Find analogies
    analogies = find_analogies(combined_text)

    # Assess
    if simple_count > jargon_count and len(analogies) > 0:
        evidence.append(f"Found {simple_count} simple language indicators")
        evidence.extend([f"Analogy: {a}" for a in analogies[:2]])
        return True, evidence, issues
    else:
        issues.append(f"High jargon count: {jargon_count} jargon phrases found")
        issues.append(f"Low simple language: {simple_count} indicators found")
        if len(analogies) == 0:
            issues.append("No analogies or comparisons found")
        return False, evidence, issues


def validate_memory_hooks(lesson: dict) -> Tuple[bool, List[str], List[str]]:
    """Check for mnemonics, acronyms, memory aids."""
    evidence = []
    issues = []

    # Check for memory_aid blocks
    memory_blocks = [b for b in lesson.get('content_blocks', []) if b.get('type') == 'memory_aid']

    if memory_blocks:
        evidence.append(f"Found {len(memory_blocks)} memory_aid blocks")

        # Look for mnemonics
        for block in memory_blocks:
            text = block.get('content', {}).get('text', '')
            if 'mnemonic' in text.lower() or 'acronym' in text.lower():
                # Extract first mnemonic
                lines = text.split('\n')
                for line in lines:
                    if 'mnemonic' in line.lower():
                        evidence.append(f"Mnemonic found: {line.strip()[:80]}")
                        break

        return True, evidence, issues
    else:
        issues.append("No memory_aid blocks found")
        return False, evidence, issues


def validate_connect_to_what_i_know(lesson: dict) -> Tuple[bool, List[str], List[str]]:
    """Check for references to prior knowledge."""
    evidence = []
    issues = []

    # Combine all text
    all_text = []
    for block in lesson.get('content_blocks', []):
        if isinstance(block.get('content'), dict):
            text = block['content'].get('text', '')
            all_text.append(text)

    combined_text = ' '.join(all_text)

    # Look for connection phrases
    connection_patterns = [
        r'remember (from|that|when)',
        r'(as|like) we (saw|learned|discussed)',
        r'building on',
        r'similar to',
        r'just like',
        r'you (already|may) know',
        r'familiar with',
    ]

    connections_found = []
    for pattern in connection_patterns:
        matches = re.findall(f'([^.!?]*{pattern}[^.!?]+)', combined_text, re.IGNORECASE)
        # Handle both string and tuple matches
        for match in matches[:2]:
            if isinstance(match, tuple):
                connections_found.append(match[0] if match else '')
            else:
                connections_found.append(match)

    # Check prerequisites
    prereqs = lesson.get('prerequisites', [])

    if connections_found or len(prereqs) > 0:
        if connections_found:
            evidence.extend([f"Connection: {c.strip()[:80]}" for c in connections_found[:2]])
        if len(prereqs) > 0:
            evidence.append(f"Has {len(prereqs)} prerequisite lessons")
        return True, evidence, issues
    else:
        issues.append("No connections to prior knowledge found")
        issues.append("No prerequisite lessons specified")
        return False, evidence, issues


def validate_active_learning(lesson: dict) -> Tuple[bool, List[str], List[str]]:
    """Check for hands-on exercises and practice tasks."""
    evidence = []
    issues = []

    # Check for active content types
    active_blocks = [b for b in lesson.get('content_blocks', [])
                     if b.get('type') in ['code_exercise', 'simulation', 'quiz']]

    if len(active_blocks) >= 2:
        evidence.append(f"Found {len(active_blocks)} active learning blocks")
        for block in active_blocks[:2]:
            evidence.append(f"Block type: {block.get('type')}")
        return True, evidence, issues
    elif len(active_blocks) == 1:
        evidence.append(f"Found 1 active learning block: {active_blocks[0].get('type')}")
        issues.append("Only 1 active learning block (recommended: 2+)")
        return True, evidence, issues
    else:
        issues.append("No code_exercise, simulation, or quiz blocks found")
        return False, evidence, issues


def validate_meta_learning(lesson: dict) -> Tuple[bool, List[str], List[str]]:
    """Check for reflection on learning process."""
    evidence = []
    issues = []

    # Check for reflection blocks
    reflection_blocks = [b for b in lesson.get('content_blocks', []) if b.get('type') == 'reflection']

    if reflection_blocks:
        evidence.append(f"Found {len(reflection_blocks)} reflection blocks")

        # Check if reflection asks about learning process
        for block in reflection_blocks:
            text = block.get('content', {}).get('text', '')
            if any(phrase in text.lower() for phrase in ['how did you', 'what did you learn', 'learning process', 'understand']):
                evidence.append("Reflection includes meta-learning prompts")
                break

        return True, evidence, issues
    else:
        issues.append("No reflection blocks found")
        return False, evidence, issues


def validate_minimum_effective_dose(lesson: dict) -> Tuple[bool, List[str], List[str]]:
    """Check if lesson is focused, not overwhelming."""
    evidence = []
    issues = []

    # Check concept count
    concepts = lesson.get('concepts', [])
    concept_count = len(concepts)

    # Check content block count
    content_blocks = lesson.get('content_blocks', [])
    block_count = len(content_blocks)

    # Check word count
    total_words = 0
    for block in content_blocks:
        if isinstance(block.get('content'), dict):
            text = block['content'].get('text', '')
            total_words += len(text.split())

    # Assess
    if concept_count <= 8 and block_count <= 15:
        evidence.append(f"Focused: {concept_count} concepts, {block_count} content blocks")
        evidence.append(f"Word count: ~{total_words} words")
        return True, evidence, issues
    else:
        if concept_count > 8:
            issues.append(f"Too many concepts: {concept_count} (recommended: ≤8)")
        if block_count > 15:
            issues.append(f"Too many content blocks: {block_count} (recommended: ≤15)")
        return False, evidence, issues


def validate_reframe_limiting_beliefs(lesson: dict) -> Tuple[bool, List[str], List[str]]:
    """Check for confidence building and encouragement."""
    evidence = []
    issues = []

    # Check for mindset_coach blocks
    mindset_blocks = [b for b in lesson.get('content_blocks', []) if b.get('type') == 'mindset_coach']

    if mindset_blocks:
        evidence.append(f"Found {len(mindset_blocks)} mindset_coach blocks")

        # Check for encouraging language
        for block in mindset_blocks:
            text = block.get('content', {}).get('text', '')
            encouraging_phrases = ['you can', 'celebrate', 'confidence', 'grow', 'journey', 'progress']
            found_phrases = [p for p in encouraging_phrases if p in text.lower()]
            if found_phrases:
                evidence.append(f"Encouraging language: {', '.join(found_phrases[:3])}")
                break

        return True, evidence, issues
    else:
        issues.append("No mindset_coach blocks found")
        return False, evidence, issues


def validate_gamify_it(lesson: dict) -> Tuple[bool, List[str], List[str]]:
    """Check for challenges, progression, engagement."""
    evidence = []
    issues = []

    # Check for quiz blocks (challenges)
    quiz_blocks = [b for b in lesson.get('content_blocks', []) if b.get('type') == 'quiz']

    # Check for post-assessment
    post_assessment = lesson.get('post_assessment', [])

    # Look for engaging language
    all_text = []
    for block in lesson.get('content_blocks', []):
        if isinstance(block.get('content'), dict):
            text = block['content'].get('text', '')
            all_text.append(text)
    combined_text = ' '.join(all_text)

    engaging_patterns = [
        r'challenge',
        r'achievement',
        r'level up',
        r'mission',
        r'goal',
        r'complete',
        r'succeed',
    ]

    engaging_count = sum(len(re.findall(pattern, combined_text, re.IGNORECASE)) for pattern in engaging_patterns)

    if len(quiz_blocks) > 0 or len(post_assessment) >= 3 or engaging_count >= 3:
        if quiz_blocks:
            evidence.append(f"Found {len(quiz_blocks)} quiz blocks (challenges)")
        if post_assessment:
            evidence.append(f"Post-assessment with {len(post_assessment)} questions")
        if engaging_count >= 3:
            evidence.append(f"Engaging language: {engaging_count} instances")
        return True, evidence, issues
    else:
        issues.append("Limited gamification elements")
        return False, evidence, issues


def validate_learning_sprint(lesson: dict) -> Tuple[bool, List[str], List[str]]:
    """Check for structured flow and clear progression."""
    evidence = []
    issues = []

    # Check content block variety and flow
    content_blocks = lesson.get('content_blocks', [])
    block_types = [b.get('type') for b in content_blocks]

    # Good flow: explanation → exercise → reflection/quiz
    has_explanation = 'explanation' in block_types
    has_practice = any(t in block_types for t in ['code_exercise', 'simulation'])
    has_reflection = any(t in block_types for t in ['reflection', 'quiz'])

    # Check estimated time (should be sprint-sized: 30-60 mins)
    estimated_time = lesson.get('estimated_time', 0)

    if has_explanation and has_practice and has_reflection:
        evidence.append("Clear progression: Learn → Practice → Reflect")
        evidence.append(f"Estimated time: {estimated_time} minutes")

        if 30 <= estimated_time <= 60:
            evidence.append("Sprint-sized lesson (30-60 minutes)")

        return True, evidence, issues
    else:
        missing = []
        if not has_explanation:
            missing.append("explanation")
        if not has_practice:
            missing.append("practice/exercise")
        if not has_reflection:
            missing.append("reflection/quiz")

        issues.append(f"Incomplete flow - missing: {', '.join(missing)}")
        return False, evidence, issues


def validate_multiple_memory_pathways(lesson: dict) -> Tuple[bool, List[str], List[str]]:
    """Check for visual, auditory, kinesthetic variety."""
    evidence = []
    issues = []

    content_blocks = lesson.get('content_blocks', [])
    block_types = set(b.get('type') for b in content_blocks)

    # Categorize by pathway
    visual = {'diagram', 'memory_aid'}
    auditory = {'video'}
    kinesthetic = {'code_exercise', 'simulation', 'quiz'}

    pathways_used = []
    if visual & block_types:
        pathways_used.append('visual')
        evidence.append(f"Visual: {', '.join(visual & block_types)}")
    if auditory & block_types:
        pathways_used.append('auditory')
        evidence.append(f"Auditory: {', '.join(auditory & block_types)}")
    if kinesthetic & block_types:
        pathways_used.append('kinesthetic')
        evidence.append(f"Kinesthetic: {', '.join(kinesthetic & block_types)}")

    if len(pathways_used) >= 2:
        evidence.append(f"Multiple pathways: {', '.join(pathways_used)}")
        return True, evidence, issues
    else:
        issues.append(f"Only {len(pathways_used)} pathway(s) used (recommended: 2+)")
        issues.append("Missing: " + ', '.join(['visual', 'auditory', 'kinesthetic'] - set(pathways_used)))
        return False, evidence, issues


VALIDATORS = {
    'teach_like_im_10': validate_teach_like_im_10,
    'memory_hooks': validate_memory_hooks,
    'connect_to_what_i_know': validate_connect_to_what_i_know,
    'active_learning': validate_active_learning,
    'meta_learning': validate_meta_learning,
    'minimum_effective_dose': validate_minimum_effective_dose,
    'reframe_limiting_beliefs': validate_reframe_limiting_beliefs,
    'gamify_it': validate_gamify_it,
    'learning_sprint': validate_learning_sprint,
    'multiple_memory_pathways': validate_multiple_memory_pathways,
}


def validate_lesson_content_quality(lesson_file: str, verbose: bool = False) -> ContentQualityResult:
    """Validate content quality of a lesson."""
    result = ContentQualityResult(lesson_file)

    if not os.path.exists(lesson_file):
        result.errors.append(f"File not found: {lesson_file}")
        return result

    try:
        with open(lesson_file, 'r', encoding='utf-8') as f:
            lesson = json.load(f)
    except Exception as e:
        result.errors.append(f"Could not load lesson: {e}")
        return result

    # Get claimed principles
    claimed_principles = lesson.get('jim_kwik_principles', [])

    # Validate each claimed principle
    for principle in claimed_principles:
        if principle in VALIDATORS:
            validator = VALIDATORS[principle]
            implemented, evidence, issues = validator(lesson)
            result.add_principle_check(principle, implemented, evidence, issues)

            if not implemented:
                result.suggestions.append(f"Improve {principle}: {issues[0] if issues else 'See details'}")

    return result


def main():
    """Validate content quality for sample lessons."""
    print("="*80)
    print("CONTENT QUALITY VALIDATION")
    print("="*80)
    print("\nThis script validates that Jim Kwik principles are ACTUALLY")
    print("implemented in lesson content, not just listed in metadata.\n")

    # Test on a few representative lessons
    test_lessons = [
        "content/lesson_fundamentals_01_authentication_vs_authorization_RICH.json",
        "content/lesson_dfir_168_common_attacks_against_azure_and_m365_RICH.json",
    ]

    results = []
    for lesson_file in test_lessons:
        if os.path.exists(lesson_file):
            result = validate_lesson_content_quality(lesson_file, verbose=True)
            results.append(result)
            result.print_report(verbose=True)

    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)

    if results:
        avg_score = sum(r.overall_score for r in results) / len(results)
        print(f"\nAverage Quality Score: {avg_score:.1f}%")

        print("\n[INTERPRETATION]")
        print("  80-100%: Excellent - Principles well implemented")
        print("  60-79%:  Good - Most principles implemented")
        print("  40-59%:  Fair - Some principles missing")
        print("  0-39%:   Poor - Major improvements needed")

    print("\n" + "="*80)


if __name__ == "__main__":
    main()
