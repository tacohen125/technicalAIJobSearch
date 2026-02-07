# Likert Screening Tutor

A Claude AI skill for preparing candidates for Likert-scale behavioral screenings used in corporate hiring processes, primarily Google's Hiring Assessment format.

## Overview

This skill helps candidates prepare for automated behavioral assessments that use Likert-scale questions and situational judgment scenarios. These assessments are increasingly common in tech hiring and use automated pattern-matching to evaluate cultural fit and professional behaviors.

**No personalization required** — this skill works out of the box.

### Key Features

- **Practice Questions**: Generate customized practice sessions with 20-100 questions across 8 behavioral categories
- **Automated Scoring**: Evaluate answers against known successful candidate patterns with detailed feedback
- **Consistency Checks**: Identify contradictions in responses to similar questions (a key scoring metric)
- **Timed Mode**: Simulate real assessment conditions (~20-25 seconds per question)
- **Strategic Guidance**: Learn the scoring patterns and best practices for 85%+ alignment
- **Red Flag Detection**: Identify problematic responses that suggest poor ethics, lone-wolf tendencies, or rigidity
- **Category Analysis**: Breakdown of performance across all 8 assessment dimensions

## Table of Contents

- [Assessment Background](#assessment-background)
- [Question Types](#question-types)
- [Eight Assessment Categories](#eight-assessment-categories)
- [How It Works](#how-it-works)
  - [Mode A: Generate Practice Questions](#mode-a-generate-practice-questions)
  - [Mode B: Grade/Evaluate Answers](#mode-b-gradeevaluate-answers)
  - [Mode C: Study/Review](#mode-c-studyreview)
- [Key Strategic Principles](#key-strategic-principles)
- [Using the Skill](#using-the-skill)
- [Understanding the Scorecard](#understanding-the-scorecard)
- [Common Mistakes to Avoid](#common-mistakes-to-avoid)

## Assessment Background

This skill focuses on Likert-scale behavioral screenings, particularly **Google's Hiring Assessment (GHA)** format, which is representative of this assessment type.

### Key Facts About Google's Hiring Assessment (GHA)

- **Duration**: ~30 minutes, 75-100 questions
- **Format**: One question per screen, no going back to previous questions
- **Response scale**: 5-point Likert (Strongly Disagree → Strongly Agree) for behavioral statements; multiple-choice for situational judgment
- **Scoring**: Automated pattern-matching against successful past applicant benchmarks
- **Consistency checks**: Similar questions rephrased throughout to detect inconsistency
- **Mixed items**: Some questions score you; others are test items for future assessments (you won't know which)
- **Result timeline**: Typically 24-72 hours
- **Retest cooldown**: 6 months if you fail; results valid for 2 years if you pass
- **Confidentiality**: Candidates agree not to record, screenshot, or share actual questions

### Why This Assessment Matters

Companies use these assessments to:
- Screen candidates at scale before investing in interviews
- Evaluate cultural fit and professional maturity
- Identify candidates whose values align with company principles
- Reduce unconscious bias in early-stage screening

**Passing this assessment is often a hard gate** — you cannot proceed to interviews without it, regardless of your technical qualifications.

## Question Types

### Type 1: Behavioral Likert Statements (~70% of questions)

A statement about workplace behavior. Rate your agreement on a 5-point scale:
- **Strongly Disagree**
- **Disagree**
- **Neutral**
- **Agree**
- **Strongly Agree**

**Example:**
> "I prefer to work independently rather than rely on others for project completion."

**Strategic Note**: Successful candidates use Strongly Agree or Strongly Disagree ~90-95% of the time. Neutral signals indecisiveness.

### Type 2: Situational Judgment Scenarios (~30% of questions)

A workplace scenario with 4-5 possible actions. Select the **best** course of action (and sometimes the **worst**).

**Example:**
> Your teammate missed a deadline for a critical deliverable. What do you do?
> - A) Report the issue to your manager immediately
> - B) Offer to help them complete it and understand what went wrong
> - C) Let them handle it themselves; it's their responsibility
> - D) Take over the task completely to ensure it gets done

**Strategic Note**: The best answers typically balance collaboration, initiative, and accountability.

## Eight Assessment Categories

All questions map to these behavioral dimensions. The skill's question bank (`references/question_bank.md`) is organized by category:

### 1. Ethics & Integrity
Honesty, doing the right thing even when no one is watching, handling confidential information, admitting mistakes, following rules.

**Example traits assessed:**
- Will you cut corners under pressure?
- Do you admit mistakes openly?
- Do you protect confidential information?

### 2. Collaboration & Teamwork
Working across teams, valuing diverse perspectives, supporting colleagues, sharing credit, building consensus.

**Example traits assessed:**
- Do you work well with diverse teams?
- Do you share credit for successes?
- Do you seek input from others?

### 3. Communication
Clarity, active listening, adapting message to audience, giving/receiving feedback, transparency.

**Example traits assessed:**
- Do you communicate proactively?
- Do you listen to understand, not just respond?
- Can you adapt your message to different audiences?

### 4. Adaptability & Resilience
Handling ambiguity, pivoting under pressure, learning from failure, staying calm in uncertainty.

**Example traits assessed:**
- Do you thrive in ambiguous situations?
- Do you learn from failures?
- Can you pivot quickly when plans change?

### 5. Leadership & Initiative
Stepping up without formal authority, mentoring, influencing others, taking ownership.

**Example traits assessed:**
- Do you take initiative without being asked?
- Do you mentor and support others?
- Can you influence without authority?

### 6. Organizational Skills & Structured Thinking
Prioritization, planning, data-driven decisions, managing competing deadlines, breaking down complex problems.

**Example traits assessed:**
- Do you prioritize effectively?
- Do you use data to make decisions?
- Can you break down complex problems?

### 7. User/Customer Focus
Putting the end user first, thinking about impact, advocating for user needs, understanding customer pain points.

**Example traits assessed:**
- Do you consider user impact in decisions?
- Do you advocate for customer needs?
- Do you seek to understand user pain points?

### 8. Continuous Learning & Growth Mindset
Seeking feedback, improving, intellectual humility, embracing new ideas, acknowledging knowledge gaps.

**Example traits assessed:**
- Do you actively seek feedback?
- Do you admit when you don't know something?
- Are you curious and eager to learn?

## How It Works

The skill operates in three modes depending on your needs:

### Mode A: Generate Practice Questions

When you ask for practice questions:

**What You'll Get:**
1. Customized question sets (20 for quick practice, 75 for full mock)
2. Balanced coverage across all 8 categories
3. Mix of Likert statements (~70%) and situational judgment (~30%)
4. 3-5 consistency-check pairs (same concept, different wording)
5. Randomized order (paired questions are not adjacent)

**Optional Timed Mode:**
- Simulates real assessment pace (~20-25 seconds per question)
- Builds muscle memory for quick, confident responses
- Prevents overthinking

**Workflow:**
1. Specify number of questions (default: 20 quick, 75 full)
2. Choose timed or untimed mode
3. Answer questions one at a time (or in batches)
4. Receive automated scoring when complete (Mode B)

### Mode B: Grade/Evaluate Answers

When grading your practice session (or submitted answers):

**What You'll Get:**
1. **Overall Alignment Score**: Percentage match against successful candidate patterns (target: 85%+)
2. **Category Breakdown**: Performance across all 8 dimensions
3. **Consistency Score**: How well your responses align on paired questions
4. **Flagged Items**: Specific problematic answers with explanations
5. **Improvement Recommendations**: Targeted advice for weak areas

**Evaluation Criteria:**
- ✅ **Alignment**: Does your answer match known value preferences?
- ✅ **Decisiveness**: Did you use Strongly Agree/Disagree (~90-95% recommended)?
- ✅ **Consistency**: Do paired questions have consistent responses?
- ❌ **Red Flags**: Answers suggesting poor ethics, lone-wolf tendencies, rigidity, or avoidance of accountability

**Sample Scorecard:**
```
Overall Alignment: 87% ✅
Decisiveness: 92% (used Strongly Agree/Disagree on 69/75 questions) ✅
Consistency: 4/5 pairs matched ⚠️

Category Breakdown:
- Ethics & Integrity: 95% ✅
- Collaboration & Teamwork: 88% ✅
- Communication: 82% ⚠️
- Adaptability & Resilience: 90% ✅
- Leadership & Initiative: 85% ✅
- Organizational Skills: 78% ⚠️
- User/Customer Focus: 92% ✅
- Continuous Learning: 88% ✅

Flagged Items:
- Q17: Selected "Neutral" on collaboration question (suggests indecisiveness)
- Q34: Inconsistent with Q12 (both assess adaptability but opposite responses)
- Q56: Selected lone-wolf answer over collaborative approach

Recommendations:
1. Practice collaboration questions - you showed some lone-wolf tendencies
2. Be more decisive - avoid "Neutral" responses
3. Review paired questions to understand consistency patterns
```

### Mode C: Study/Review

When you want to understand the assessment:

**What You'll Get:**
1. Explanation of format and scoring approach
2. Walkthrough of example questions with ideal answer reasoning
3. Key strategic principles from `references/scoring_guide.md`
4. How corporate values map to question categories

**Use This Mode To:**
- Understand why certain answers score better
- Learn the patterns behind successful responses
- Review before taking a real assessment
- Clarify any confusing aspects

## Key Strategic Principles

These principles are derived from hundreds of community reports of successful candidates:

### 1. Be Decisive (~90-95% Extreme Responses)
**Use Strongly Agree or Strongly Disagree ~90-95% of the time.**

Why? Neutral signals indecisiveness. Successful candidates are confident in their professional values.

**Example:**
- ❌ "I sometimes prefer to work independently" → Neutral
- ✅ "I prefer collaboration but can work independently when needed" → Strongly Agree

### 2. Be Consistent (Paired Questions Must Match)
**The same concept rephrased differently must get the same strength of response.**

This is a core scoring metric. The assessment intentionally asks similar questions in different ways to check consistency.

**Example Pair:**
- Q15: "I take initiative even when it's not my responsibility" → Strongly Agree
- Q67: "I wait for clear direction before starting new work" → Strongly Disagree
(These assess the same trait — initiative — from opposite angles)

### 3. Read Carefully (Watch for Negation)
**Some questions use negation ("I avoid X unless Y") — misreading flips your answer.**

**Example:**
- "I avoid seeking feedback unless explicitly asked"
  - If you value feedback → Strongly Disagree (you DON'T avoid it)
  - Misread as positive statement → wrong answer

### 4. Think Like a Collaborative Leader
**These assessments value people who take initiative AND collaborate.**

Never choose lone-wolf answers. The ideal candidate:
- Takes ownership and initiative
- Seeks input and collaborates
- Supports teammates
- Balances independence with teamwork

**Example:**
- ❌ "I prefer to solve problems myself rather than involve others"
- ✅ "I take ownership while seeking input from relevant stakeholders"

### 5. Ethics Are Non-Negotiable
**Any answer suggesting you'd bend rules, cut corners, or hide mistakes is a strong red flag.**

**Example Red Flags:**
- ❌ "Sometimes rules need to be bent to meet deadlines"
- ❌ "I only admit mistakes when directly asked"
- ❌ "I prioritize results over process"

**Correct Approach:**
- ✅ "I follow established processes even under pressure"
- ✅ "I proactively admit and correct mistakes"
- ✅ "I balance speed with quality and integrity"

### 6. Trust Your Professional Instincts
**The questions test baseline professional maturity. If an answer seems obviously right, it probably is.**

Don't overthink. Your gut reaction to professional behavior questions is usually aligned with what's expected.

### 7. Don't Overthink (~20 Seconds Per Question)
**Each question should take ~20 seconds. Your first instinct is usually correct.**

Overthinking leads to:
- Inconsistent responses (you rationalize different answers to similar questions)
- Less decisive responses (you hedge with Neutral)
- Anxiety and fatigue

**Practice timed mode to build confidence in quick responses.**

## Using the Skill

### With Claude Code (CLI)

1. **Copy the skill to your skills directory:**
   ```bash
   cp -r likert-screening-tutor ~/.claude/skills/
   ```

2. **Use in conversation:**

   **Quick practice session (20 questions):**
   ```
   /likert-screening-tutor
   Give me 20 practice questions
   ```

   **Full timed mock assessment (75 questions):**
   ```
   /likert-screening-tutor
   I want to do a full 75-question mock assessment with timed mode
   ```

   **Study mode:**
   ```
   /likert-screening-tutor
   Explain how the Google Hiring Assessment works and what strategies I should use
   ```

   **Grade previous answers:**
   ```
   /likert-screening-tutor
   I took a practice assessment elsewhere. Can you evaluate my answers?
   [paste answers]
   ```

### With Claude AI (Browser)

1. **Package the skill:**
   ```bash
   cd /path/to/ai-assisted-job-search
   python utils/package_skill.py likert-screening-tutor
   ```

2. **Upload to Claude.ai:**
   - Go to [claude.ai](https://claude.ai)
   - Settings → Capabilities → Skills → "+ Add" → "Upload a skill"
   - Select `likert-screening-tutor.skill`

3. **Use in conversation:**
   - Type `/likert-screening-tutor` to activate
   - Follow the same usage patterns as CLI above

## Understanding the Scorecard

After completing a practice session, you'll receive a detailed scorecard. Here's how to interpret it:

### Overall Alignment Score
**Target: 85%+ for strong performance**

- **90%+**: Excellent — you're well-aligned with successful candidate patterns
- **85-89%**: Good — minor improvements needed
- **80-84%**: Fair — focus on flagged categories
- **<80%**: Needs work — review strategic principles and retake practice

### Decisiveness Score
**Target: 90-95% extreme responses (Strongly Agree/Disagree)**

Measures how often you used strong positions vs. Neutral.

- **90%+**: Excellent — confident and decisive
- **80-89%**: Good — slightly too many Neutral responses
- **<80%**: Needs work — shows indecisiveness

### Consistency Score
**Target: 100% of paired questions match**

Shows alignment on questions that test the same trait from different angles.

- **100%**: Perfect — consistent values
- **80%+**: Good — minor inconsistencies (review flagged pairs)
- **<80%**: Concerning — suggests rushing or not understanding questions

### Category Breakdown
**Target: 80%+ in all categories**

Identifies specific behavioral dimensions where you're strong or weak.

**If you score low in a category:**
1. Review the question bank for that category (`references/question_bank.md`)
2. Study the scoring guide for that dimension (`references/scoring_guide.md`)
3. Retake practice focusing on that category

### Flagged Items
**Target: 0 red flags**

Lists specific problematic answers with explanations.

**Common flag types:**
- **Ethical concerns**: Suggested cutting corners, hiding mistakes
- **Lone-wolf tendencies**: Chose independence over collaboration
- **Rigidity**: Showed inflexibility or resistance to change
- **Indecisiveness**: Used Neutral on important questions
- **Inconsistency**: Contradicted earlier answers

**How to address:**
- Understand WHY the answer was flagged
- Review similar questions with the correct reasoning
- Retake practice to confirm improvement

## Common Mistakes to Avoid

### 1. Using "Neutral" Too Often
**Mistake**: Hedging with Neutral to avoid seeming extreme.
**Reality**: Neutral signals indecisiveness. Successful candidates are ~90-95% Strongly Agree/Disagree.

### 2. Inconsistent Responses to Paired Questions
**Mistake**: Not recognizing that different questions assess the same trait.
**Fix**: Read carefully and maintain consistent values throughout.

### 3. Choosing Lone-Wolf Answers
**Mistake**: "I prefer to solve problems myself" thinking it shows initiative.
**Reality**: Companies value collaborative initiative, not solo heroes.

### 4. Overthinking Questions
**Mistake**: Spending 60+ seconds analyzing each question, rationalizing different answers.
**Fix**: Trust your first instinct. Real assessment is ~20-25 seconds per question.

### 5. Trying to "Game" the System
**Mistake**: Trying to figure out what the "right" answer is rather than being authentic.
**Reality**: Consistency checks catch gaming. Answer according to your genuine professional values.

### 6. Not Practicing Timed Mode
**Mistake**: Only doing untimed practice, then panicking during real assessment.
**Fix**: Do at least one full 75-question timed mock before the real thing.

### 7. Ignoring Ethics Questions
**Mistake**: Choosing results over integrity ("Sometimes rules need to be bent").
**Reality**: Ethics is an automatic disqualifier. Always choose integrity.

## Tips for Success

### Before the Assessment
- [ ] Complete at least one full 75-question mock in timed mode
- [ ] Review all 8 categories and understand what each assesses
- [ ] Achieve 85%+ alignment score on practice
- [ ] Achieve 90%+ decisiveness score on practice
- [ ] Get 100% consistency on paired questions
- [ ] Read through the scoring guide to understand patterns

### During the Assessment
- [ ] Read each question carefully (watch for negation)
- [ ] Trust your first professional instinct
- [ ] Use Strongly Agree/Disagree ~90-95% of the time
- [ ] Stay consistent with your values throughout
- [ ] Don't overthink — ~20-25 seconds per question
- [ ] Remember you can't go back, so commit to each answer

### After the Assessment
- Results typically come in 24-72 hours
- If you pass: Results are valid for 2 years
- If you don't pass: 6-month cooldown before retesting
- Use this skill to prepare better for the retest if needed

## Reference Files

The skill uses two key reference files (no customization needed):

### `references/question_bank.md`
Complete practice question bank organized by category:
- 10-15 questions per category
- Mix of Likert statements and situational judgment
- Includes consistency-check pairs
- Tagged by difficulty and common pitfalls

### `references/scoring_guide.md`
Comprehensive scoring rubric:
- Ideal answer patterns for each category
- Common red flags and why they're problematic
- Consistency check logic
- Strategic guidance derived from successful candidate data

---

**[← Back to Main README](../README.md)**
