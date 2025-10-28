"""
Adaptive Learning Engine for CyberLearn.
Implements intelligent lesson recommendation and difficulty adaptation.
"""

from typing import List, Dict, Optional, Tuple
from uuid import UUID
import random
from datetime import datetime

from models.user import UserProfile, SkillLevels
from models.lesson import Lesson, LessonMetadata
from models.progress import LessonProgress, LessonStatus


class AdaptiveEngine:
    """
    Core adaptive learning algorithm that personalizes content delivery
    based on user performance, preferences, and learning science principles.
    """

    def __init__(self):
        self.domain_prerequisites = {
            "fundamentals": [],
            "dfir": ["fundamentals"],
            "malware": ["fundamentals"],
            "active_directory": ["fundamentals"],
            "system": ["fundamentals"],
            "linux": ["fundamentals"],
            "cloud": ["fundamentals", "system"],
            "pentest": ["fundamentals", "active_directory"],
            "redteam": ["pentest", "malware"],
            "blueteam": ["dfir", "malware"],
        }

    def _ordered_domains(self) -> List[str]:
        """Domain ordering used for recommendations and fallbacks"""
        return [
            "fundamentals",
            "dfir",
            "malware",
            "active_directory",
            "system",
            "linux",
            "cloud",
            "pentest",
            "redteam",
            "blueteam",
        ]

    def _prerequisites_met(self, domain: str, user: UserProfile) -> bool:
        """Check if a user meets prerequisite skill thresholds for a domain"""
        prereqs = self.domain_prerequisites.get(domain, [])
        return all(getattr(user.skill_levels, prereq, 0) >= 30 for prereq in prereqs)

    def _get_candidates_for_domain(
        self,
        lessons: List[LessonMetadata],
        domain: str,
        difficulties: List[int],
        user_progress: List[LessonProgress],
    ) -> List[LessonMetadata]:
        """Return candidate lessons for a domain with graceful difficulty fallback"""
        candidates = self._filter_lessons(lessons, domain, difficulties, user_progress)
        if candidates:
            return candidates

        # No candidates within target difficulty – widen the search to any available difficulty
        domain_difficulties = sorted(
            {lesson.difficulty for lesson in lessons if lesson.domain == domain}
        )
        if not domain_difficulties or set(domain_difficulties) == set(difficulties):
            return []

        return self._filter_lessons(lessons, domain, domain_difficulties, user_progress)

    def get_recommended_lesson(
        self,
        user: UserProfile,
        available_lessons: List[LessonMetadata],
        user_progress: List[LessonProgress],
        domain: Optional[str] = None,
    ) -> Optional[UUID]:
        """
        Recommend next lesson based on adaptive algorithm.

        Algorithm considers:
        1. Domain skill level -> difficulty matching
        2. Prerequisites completion
        3. Spaced repetition needs
        4. Learning preferences
        5. Minimum effective dose (core concepts first)
        """

        # Check for lessons needing review (spaced repetition)
        review_lesson = self._check_review_needed(user_progress)
        if review_lesson:
            return review_lesson

        # Filter by domain if specified, else choose optimal domain
        if not domain:
            domain = self._select_optimal_domain(user)

        ordered_domains = self._ordered_domains()
        search_domains = [domain] + [d for d in ordered_domains if d != domain]

        candidates: List[LessonMetadata] = []
        for candidate_domain in search_domains:
            if not self._prerequisites_met(candidate_domain, user):
                continue

            skill_level = getattr(user.skill_levels, candidate_domain, 0)
            target_difficulties = self._get_target_difficulties(skill_level)

            candidates = self._get_candidates_for_domain(
                available_lessons,
                candidate_domain,
                target_difficulties,
                user_progress,
            )

            if candidates:
                break

        if not candidates:
            return None

        # Prioritize core concepts (Minimum Effective Dose principle)
        core_lessons = [l for l in candidates if l.is_core_concept]
        if core_lessons:
            candidates = core_lessons

        # Select best lesson using multi-factor scoring
        selected = self._score_and_select_lesson(candidates, user, user_progress)

        return selected.lesson_id if selected else None

    def _check_review_needed(
        self, user_progress: List[LessonProgress]
    ) -> Optional[UUID]:
        """Check if any lessons are due for spaced repetition review"""
        for progress in user_progress:
            if progress.should_review() and progress.status != LessonStatus.MASTERED:
                return progress.lesson_id
        return None

    def _select_optimal_domain(self, user: UserProfile) -> str:
        """Select domain that needs most attention or is next logical step"""

        # If just starting, begin with fundamentals
        if not user.diagnostic_completed or user.skill_levels.fundamentals < 25:
            return "fundamentals"

        # Find weakest domain that has prerequisites met
        domains = self._ordered_domains()

        domain_scores = []
        for domain in domains:
            skill = getattr(user.skill_levels, domain)

            # Check prerequisites
            if not self._prerequisites_met(domain, user):
                continue

            # Score: lower skill = higher priority
            score = 100 - skill
            domain_scores.append((domain, score))

        if not domain_scores:
            return "fundamentals"

        # Sort by score and return highest priority
        domain_scores.sort(key=lambda x: x[1], reverse=True)
        return domain_scores[0][0]

    def _get_target_difficulties(self, skill_level: int) -> List[int]:
        """Map skill level to appropriate lesson difficulties"""
        if skill_level < 25:
            return [1, 2]  # Beginner + some intermediate
        elif skill_level < 50:
            return [2, 3]  # Intermediate + some advanced
        elif skill_level < 75:
            return [3, 4]  # Advanced + expert
        else:
            return [4]  # Expert only

    def _filter_lessons(
        self,
        lessons: List[LessonMetadata],
        domain: str,
        difficulties: List[int],
        user_progress: List[LessonProgress],
    ) -> List[LessonMetadata]:
        """Filter lessons by domain, difficulty, and prerequisites"""

        completed_ids = {p.lesson_id for p in user_progress if p.status in [
            LessonStatus.COMPLETED, LessonStatus.MASTERED
        ]}

        candidates = []
        for lesson in lessons:
            # Must match domain
            if lesson.domain != domain:
                continue

            # Must match difficulty
            if lesson.difficulty not in difficulties:
                continue

            # Must not be completed (unless needs review)
            if lesson.lesson_id in completed_ids:
                continue

            # Must have prerequisites met
            if not all(prereq in completed_ids for prereq in lesson.prerequisites):
                continue

            candidates.append(lesson)

        return candidates

    def _score_and_select_lesson(
        self,
        candidates: List[LessonMetadata],
        user: UserProfile,
        user_progress: List[LessonProgress],
    ) -> Optional[LessonMetadata]:
        """Score lessons by multiple factors and select best match"""

        if not candidates:
            return None

        # Sort by order_index (curriculum sequence)
        candidates.sort(key=lambda x: x.order_index)

        # Return first in sequence (respects curriculum design)
        return candidates[0]

    def calculate_skill_update(
        self, current_skill: int, lesson_difficulty: int, score: int
    ) -> int:
        """Calculate new skill level after lesson completion"""

        # Base skill gain based on score
        if score >= 90:
            gain = 5
        elif score >= 80:
            gain = 3
        elif score >= 70:
            gain = 2
        elif score >= 60:
            gain = 1
        else:
            gain = 0  # No gain for failing scores

        # Adjust gain based on lesson difficulty
        gain *= lesson_difficulty

        # Diminishing returns at higher skill levels
        if current_skill >= 75:
            gain = int(gain * 0.5)
        elif current_skill >= 50:
            gain = int(gain * 0.75)

        new_skill = min(100, current_skill + gain)
        return new_skill

    def generate_diagnostic_assessment(
        self, num_questions: int = 20
    ) -> Dict[str, List[Dict]]:
        """
        Generate diagnostic assessment questions across all domains.
        Used for initial skill profiling.
        """

        # Real diagnostic questions for each domain with answer options
        diagnostic_questions = {
            "fundamentals": [
                {
                    "question": "What does the CIA triad stand for in cybersecurity?",
                    "options": ["Confidentiality, Integrity, Availability", "Central Intelligence Agency", "Computer, Internet, Application", "Cybersecurity Information Analysis"],
                    "correct": 0,
                    "difficulty": 1
                },
                {
                    "question": "Which principle ensures data is accessible when needed?",
                    "options": ["Confidentiality", "Integrity", "Availability", "Authentication"],
                    "correct": 2,
                    "difficulty": 1
                },
                {
                    "question": "What is the primary purpose of encryption?",
                    "options": ["Speed up data transfer", "Protect confidentiality", "Detect malware", "Backup data"],
                    "correct": 1,
                    "difficulty": 2
                },
            ],
            "dfir": [
                {
                    "question": "What does DFIR stand for?",
                    "options": ["Digital Forensics and Incident Response", "Data Flow Information Report", "Digital File Integrity Review", "Defense and Firewall Investigation"],
                    "correct": 0,
                    "difficulty": 1
                },
                {
                    "question": "Why is chain of custody important in digital forensics?",
                    "options": ["Faster analysis", "Legal admissibility of evidence", "Better documentation", "Easier sharing"],
                    "correct": 1,
                    "difficulty": 2
                },
                {
                    "question": "What is the first step in incident response?",
                    "options": ["Eradication", "Recovery", "Identification/Detection", "Lessons learned"],
                    "correct": 2,
                    "difficulty": 2
                },
            ],
            "malware": [
                {
                    "question": "What is the difference between a virus and a worm?",
                    "options": ["No difference", "Virus needs host file, worm self-replicates", "Worm is less dangerous", "Virus spreads faster"],
                    "correct": 1,
                    "difficulty": 2
                },
                {
                    "question": "What does static malware analysis involve?",
                    "options": ["Running the malware", "Examining code without execution", "Infecting test systems", "Monitoring network traffic"],
                    "correct": 1,
                    "difficulty": 2
                },
                {
                    "question": "What is a rootkit?",
                    "options": ["A password cracker", "Malware that hides at system level", "A network scanner", "An encryption tool"],
                    "correct": 1,
                    "difficulty": 3
                },
            ],
            "active_directory": [
                {
                    "question": "What is Active Directory used for?",
                    "options": ["Website hosting", "Directory services and identity management", "Antivirus scanning", "Network monitoring"],
                    "correct": 1,
                    "difficulty": 1
                },
                {
                    "question": "What is the purpose of Group Policy?",
                    "options": ["Create user groups", "Centrally manage Windows settings", "Share files", "Monitor logins"],
                    "correct": 1,
                    "difficulty": 2
                },
                {
                    "question": "What is Kerberos authentication?",
                    "options": ["Password hashing", "Ticket-based authentication protocol", "Biometric system", "Two-factor authentication"],
                    "correct": 1,
                    "difficulty": 3
                },
            ],
            "pentest": [
                {
                    "question": "What is the purpose of penetration testing?",
                    "options": ["Break systems permanently", "Find and report vulnerabilities", "Install backdoors", "Delete data"],
                    "correct": 1,
                    "difficulty": 1
                },
                {
                    "question": "What are the main phases of a penetration test?",
                    "options": ["Only exploitation", "Reconnaissance, Scanning, Exploitation, Post-exploitation", "Just scanning", "Only reporting"],
                    "correct": 1,
                    "difficulty": 2
                },
                {
                    "question": "What is privilege escalation?",
                    "options": ["Adding more users", "Gaining higher access rights", "Faster logins", "Better passwords"],
                    "correct": 1,
                    "difficulty": 2
                },
            ],
            "redteam": [
                {
                    "question": "How does red team differ from penetration testing?",
                    "options": ["No difference", "Red team simulates real adversaries over longer periods", "Red team is faster", "Red team only tests networks"],
                    "correct": 1,
                    "difficulty": 2
                },
                {
                    "question": "What is social engineering?",
                    "options": ["Network scanning", "Manipulating people to divulge information", "Password cracking", "Virus creation"],
                    "correct": 1,
                    "difficulty": 1
                },
                {
                    "question": "What is lateral movement in a network?",
                    "options": ["Moving files between folders", "Moving between systems after initial compromise", "Upgrading network speed", "Installing updates"],
                    "correct": 1,
                    "difficulty": 3
                },
            ],
            "blueteam": [
                {
                    "question": "What is the role of a blue team?",
                    "options": ["Attack systems", "Defend and monitor systems", "Develop software", "Manage databases"],
                    "correct": 1,
                    "difficulty": 1
                },
                {
                    "question": "What is a SIEM system?",
                    "options": ["Social media platform", "Security Information and Event Management", "Server Infrastructure", "Software Installation Manager"],
                    "correct": 1,
                    "difficulty": 2
                },
                {
                    "question": "What are Indicators of Compromise (IOCs)?",
                    "options": ["System performance metrics", "Evidence of security breach", "User passwords", "Network bandwidth"],
                    "correct": 1,
                    "difficulty": 2
                },
            ],
            "system": [
                {
                    "question": "What is the purpose of privilege escalation in system security?",
                    "options": ["To gain higher-level permissions on a system", "To reduce user access rights", "To encrypt system files", "To monitor network traffic"],
                    "correct": 0,
                    "difficulty": 2
                },
                {
                    "question": "Which Linux file controls sudo permissions?",
                    "options": ["/etc/passwd", "/etc/sudoers", "/etc/shadow", "/etc/hosts"],
                    "correct": 1,
                    "difficulty": 2
                },
                {
                    "question": "What does UAC (User Account Control) do in Windows?",
                    "options": ["Prevents all administrative actions", "Prompts for permission before privileged operations", "Encrypts user files", "Monitors network connections"],
                    "correct": 1,
                    "difficulty": 2
                },
            ],
            "linux": [
                {
                    "question": "What command shows currently running processes in Linux?",
                    "options": ["ls", "ps", "cd", "pwd"],
                    "correct": 1,
                    "difficulty": 1
                },
                {
                    "question": "What does chmod 755 mean in Linux permissions?",
                    "options": ["Owner: rwx, Group: r-x, Others: r-x", "Everyone has full access", "No one can access", "Only root can access"],
                    "correct": 0,
                    "difficulty": 2
                },
                {
                    "question": "Which firewall is commonly used in modern Linux distributions?",
                    "options": ["Windows Firewall", "iptables/nftables", "Norton Firewall", "McAfee Firewall"],
                    "correct": 1,
                    "difficulty": 2
                },
            ],
            "cloud": [
                {
                    "question": "What is the shared responsibility model in cloud security?",
                    "options": ["Cloud provider responsible for everything", "Customer responsible for everything", "Responsibilities split between provider and customer", "Third-party manages all security"],
                    "correct": 2,
                    "difficulty": 2
                },
                {
                    "question": "What does IAM stand for in cloud security?",
                    "options": ["Internet Access Management", "Identity and Access Management", "Infrastructure Administration Module", "Integrated Alert Monitoring"],
                    "correct": 1,
                    "difficulty": 1
                },
                {
                    "question": "What is a common security risk of misconfigured S3 buckets?",
                    "options": ["Too much encryption", "Public exposure of sensitive data", "Excessive monitoring", "Too many backups"],
                    "correct": 1,
                    "difficulty": 2
                },
            ],
        }

        diagnostic = {}
        for domain, questions in diagnostic_questions.items():
            domain_questions = []
            for q in questions:
                domain_questions.append(
                    {
                        "domain": domain,
                        "difficulty": q["difficulty"],
                        "question": q["question"],
                        "options": q["options"],
                        "correct": q["correct"],
                        "type": "multiple_choice",
                    }
                )
            diagnostic[domain] = domain_questions

        return diagnostic

    def score_diagnostic(
        self, responses: Dict[str, List[bool]]
    ) -> SkillLevels:
        """
        Score diagnostic assessment and generate initial skill profile.

        Args:
            responses: Dict mapping domain -> list of correct/incorrect booleans

        Returns:
            SkillLevels object with initial proficiency estimates
        """

        skills = SkillLevels()

        for domain, answers in responses.items():
            if not answers:
                continue

            # Calculate percentage correct
            correct = sum(1 for a in answers if a)
            total = len(answers)
            percentage = (correct / total) * 100

            # Map to skill level (more conservative scoring)
            # Scale down to encourage learning from basics
            if percentage >= 80:
                skill_estimate = min(50, int(percentage * 0.5))  # Even experts start at 50
            elif percentage >= 60:
                skill_estimate = int(percentage * 0.4)  # 60% = 24 skill
            else:
                skill_estimate = int(percentage * 0.3)  # 33% = 10 skill

            # Set skill level
            setattr(skills, domain, skill_estimate)

        return skills

    def should_interleave(self, user: UserProfile) -> bool:
        """Determine if learning should interleave domains (learning science)"""

        # Interleaving beneficial once past beginner stage
        avg_skill = user.skill_levels.get_overall_level()
        return avg_skill >= 30

    def calculate_learning_velocity(
        self, user_progress: List[LessonProgress]
    ) -> float:
        """
        Calculate user's learning velocity (lessons/day).
        Used for adaptive pacing recommendations.
        """

        if not user_progress:
            return 0.0

        completed = [
            p
            for p in user_progress
            if p.status in [LessonStatus.COMPLETED, LessonStatus.MASTERED]
        ]

        if not completed:
            return 0.0

        # Calculate days since first lesson
        earliest = min(p.started_at for p in completed if p.started_at)
        days = (datetime.now() - earliest).days + 1

        return len(completed) / days

    def recommend_study_schedule(
        self, user: UserProfile, velocity: float
    ) -> Dict[str, any]:
        """Generate personalized study schedule recommendation"""

        target_daily_minutes = user.learning_preferences.session_duration

        # Adaptive pacing based on velocity and skill
        if velocity < 0.5:
            # Slow pace - encourage consistency
            recommendation = {
                "sessions_per_week": 5,
                "minutes_per_session": target_daily_minutes,
                "focus": "Build momentum with daily practice",
            }
        elif velocity < 1.0:
            # Good pace - maintain
            recommendation = {
                "sessions_per_week": 6,
                "minutes_per_session": target_daily_minutes,
                "focus": "Maintain your excellent progress",
            }
        else:
            # Fast pace - suggest optimization
            recommendation = {
                "sessions_per_week": 7,
                "minutes_per_session": target_daily_minutes,
                "focus": "Challenge yourself with advanced content",
            }

        return recommendation
