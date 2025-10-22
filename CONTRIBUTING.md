# Contributing to CyberLearn

Thank you for your interest in contributing to CyberLearn! This document provides guidelines for contributing to the project.

## 🎯 Ways to Contribute

### 1. Content Creation (Lessons)
- Create new cybersecurity lessons
- Improve existing lesson content
- Add memory aids and real-world examples
- Ensure all Jim Kwik principles are represented

### 2. Code Contributions
- Fix bugs
- Add new features
- Improve performance
- Enhance UI/UX
- Add tests

### 3. Documentation
- Improve existing documentation
- Add tutorials and guides
- Fix typos and clarify explanations
- Translate documentation

### 4. Testing & Feedback
- Test the platform with real learners
- Report bugs and issues
- Suggest improvements
- Share user feedback

## 📋 Getting Started

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/cyberlearn.git
   cd cyberlearn
   ```
3. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes**
5. **Test your changes**
   ```bash
   python setup.py
   streamlit run app.py
   ```
6. **Commit and push**
   ```bash
   git add .
   git commit -m "Description of changes"
   git push origin feature/your-feature-name
   ```
7. **Create a Pull Request**

## 📚 Creating New Lessons

### Step 1: Copy Template
```bash
cp content/lesson_template.json content/your_lesson.json
```

### Step 2: Fill in Content

Use `content/sample_lesson_cia_triad.json` as a reference.

**Required elements:**
- Unique lesson_id (generate with `python -c "import uuid; print(uuid.uuid4())"`)
- Title and learning objectives
- 5-8 content blocks
- At least 5 quiz questions
- All 10 Jim Kwik principles represented

### Step 3: Quality Checklist

Before submitting, ensure your lesson has:

- [ ] Mindset coaching introduction
- [ ] Clear explanations with simplified (ELI10) versions
- [ ] Visual diagrams or ASCII art
- [ ] At least 3 memory aids (mnemonics/metaphors)
- [ ] Real-world connections for each major concept
- [ ] Interactive simulation or hands-on exercise
- [ ] Meta-learning reflection prompts
- [ ] 5-10 quiz questions with explanations
- [ ] Appropriate difficulty level
- [ ] Accurate estimated time (test with users)

### Step 4: Load and Test

```python
import json
from uuid import UUID
from utils.database import Database
from models.lesson import Lesson

db = Database()
with open('content/your_lesson.json', 'r') as f:
    data = json.load(f)
data['lesson_id'] = UUID(data['lesson_id'])
data['prerequisites'] = [UUID(p) for p in data['prerequisites']]
lesson = Lesson(**data)
db.create_lesson(lesson)
db.close()
```

Then test in the application.

## 🐛 Reporting Bugs

When reporting bugs, please include:

1. **Description**: Clear description of the issue
2. **Steps to Reproduce**: Exact steps to reproduce the bug
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happens
5. **Environment**:
   - OS (Windows/Linux/Mac)
   - Python version
   - Browser (for UI issues)
6. **Screenshots**: If applicable
7. **Logs**: Error messages from terminal

## 💻 Code Style Guidelines

### Python
- Follow PEP 8 style guide
- Use type hints (Pydantic models)
- Write docstrings for all functions/classes
- Keep functions focused and small (<50 lines)
- Use meaningful variable names

### Example:
```python
def calculate_xp(
    base_xp: int,
    score: int,
    time_spent: int,
    streak: int
) -> int:
    """
    Calculate XP earned with bonuses applied.

    Args:
        base_xp: Base XP for lesson
        score: Quiz score (0-100)
        time_spent: Time in seconds
        streak: Current streak days

    Returns:
        Total XP with all multipliers applied
    """
    # Implementation
    pass
```

### Documentation
- Use Markdown for all docs
- Include code examples
- Keep language clear and concise
- Use emojis for visual clarity (but not excessively)

## 🔍 Review Process

1. **Automated Checks**: Code must pass linting and tests
2. **Manual Review**: Maintainers review for quality and fit
3. **Testing**: Changes must be tested locally
4. **Documentation**: Updates to docs if needed
5. **Approval**: At least one maintainer approval required

## 📝 Commit Message Guidelines

Use clear, descriptive commit messages:

```
[Type] Short description

Longer explanation if needed

Examples:
- [Feature] Add video content support to lesson viewer
- [Fix] Correct XP calculation for streak bonus
- [Docs] Update QUICK_START with troubleshooting
- [Content] Add DFIR lesson on chain of custody
- [Refactor] Simplify adaptive engine recommendation logic
```

## 🌟 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Credited in release notes
- Acknowledged in the application (optional)

## 📜 Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards others

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Publishing others' private information
- Unprofessional conduct

## ❓ Questions?

- Check existing documentation first
- Open an issue for clarification
- Join discussions in GitHub Discussions

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for helping make cybersecurity education accessible to everyone! 🛡️🎓**
