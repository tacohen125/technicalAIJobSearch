---
name: likert-screening-tutor
description: "Prepares candidates for Likert-scale behavioral screenings used in corporate hiring processes (primarily Google's Hiring Assessment format). Use this skill when the user requests: (1) Practice questions simulating Likert-scale behavioral statements and situational judgment scenarios, (2) Grading or evaluating their answers against known scoring patterns, (3) Understanding how these assessments work and strategic approaches, (4) Timed mock assessment sessions, (5) Consistency checks across repeated/rephrased questions, or (6) Any preparation related to behavioral/situational hiring assessments. Covers question categories: ethics, collaboration, communication, adaptability, leadership, organizational skills, structured thinking, and handling ambiguity."
---

# Likert-Scale Behavioral Screening Preparation

## Assessment Overview

This skill focuses on Likert-scale behavioral screenings, particularly Google's Hiring Assessment (GHA) format, which is representative of this assessment type. Key facts about the GHA:

- **Duration**: ~30 minutes, 75-100 questions
- **Format**: One question per screen, no going back
- **Response scale**: 5-point Likert (Strongly Disagree → Strongly Disagree) for behavioral statements; multiple-choice for situational judgment
- **Scoring**: Automated pattern-matching against successful past applicant benchmarks
- **Consistency checks**: Similar questions rephrased throughout to detect inconsistency
- **Mixed items**: Some questions score you; others are test items for future assessments (you won't know which)
- **Result timeline**: Typically 24-72 hours
- **Retest cooldown**: 6 months if you fail; results valid for 2 years if you pass
- **Confidentiality**: Candidates agree not to record, screenshot, or share actual questions

## Two Question Types

### Type 1: Behavioral Likert Statements
A statement about workplace behavior. Rate your agreement: Strongly Disagree / Disagree / Neutral / Agree / Strongly Agree.

### Type 2: Situational Judgment Scenarios
A workplace scenario with 4-5 possible actions. Select the best (and sometimes worst) course of action.

## Eight Assessment Categories

All questions map to these categories. See `references/question_bank.md` for the full practice question bank organized by category.

1. **Ethics & Integrity** — Honesty, doing the right thing even when no one is watching, handling confidential information
2. **Collaboration & Teamwork** — Working across teams, valuing diverse perspectives, supporting colleagues
3. **Communication** — Clarity, active listening, adapting message to audience, giving/receiving feedback
4. **Adaptability & Resilience** — Handling ambiguity, pivoting under pressure, learning from failure
5. **Leadership & Initiative** — Stepping up without formal authority, mentoring, influencing others
6. **Organizational Skills & Structured Thinking** — Prioritization, planning, data-driven decisions
7. **User/Customer Focus** — Putting the end user first, thinking about impact
8. **Continuous Learning & Growth Mindset** — Seeking feedback, improving, intellectual humility

## Workflow

### Mode A: Generate Practice Questions

When the user asks for practice questions:

1. Ask how many questions they want (default: 20 for a quick session, 75 for a full mock)
2. Ask if they want timed mode (real assessment pace ≈ ~20-25 seconds per question)
3. Read `references/question_bank.md` for the master question bank
4. Select questions ensuring:
   - Balanced coverage across all 8 categories
   - Mix of Type 1 (Likert) and Type 2 (Situational Judgment) — roughly 70/30 split
   - Include 3-5 consistency-check pairs (same concept, different wording)
   - Randomize order so paired questions are not adjacent
5. Present questions one at a time (or in batches if user prefers)
6. After all answers collected, proceed to grading (Mode B)

### Mode B: Grade / Evaluate Answers

When grading answers (either from a practice session or user-submitted responses):

1. Read `references/scoring_guide.md` for the complete scoring rubric
2. For each answer, evaluate:
   - **Alignment**: Does the answer match known value preferences (based on Google's scoring patterns)?
   - **Decisiveness**: Strong responses (Strongly Agree/Disagree) are preferred over neutral — 90-95% of answers from successful candidates used extreme responses
   - **Consistency**: Flag any contradictions across paired questions
   - **Red flags**: Identify answers suggesting poor ethics, lone-wolf tendencies, rigidity, or avoidance of accountability
3. Produce a scorecard:
   - Overall alignment percentage (target: 85%+)
   - Category-by-category breakdown
   - Consistency score
   - Flagged items with explanations
   - Specific improvement recommendations

### Mode C: Study / Review

When the user wants to understand the assessment:

1. Explain the format and scoring approach
2. Walk through example questions with reasoning for ideal answers
3. Share the key strategic advice from `references/scoring_guide.md`
4. Discuss how corporate values (using Google as the primary example) map to question categories

## Key Strategic Principles

These are derived from hundreds of community reports of successful candidates:

1. **Be decisive**: Use Strongly Agree or Strongly Disagree ~90-95% of the time. Neutral signals indecisiveness.
2. **Be consistent**: The same concept rephrased differently must get the same strength of response. This is a core scoring metric.
3. **Read carefully**: Some questions use negation ("I avoid X unless Y") — misreading flips your answer.
4. **Think like a collaborative leader**: These assessments value people who take initiative AND collaborate. Never choose lone-wolf answers.
5. **Ethics are non-negotiable**: Any answer suggesting you'd bend rules, cut corners, or hide mistakes is a strong red flag.
6. **Trust your professional instincts**: The questions test baseline professional maturity. If an answer seems obviously right, it probably is.
7. **Don't overthink**: Each question should take ~20 seconds. Your first instinct on professional behavior questions is usually correct.
