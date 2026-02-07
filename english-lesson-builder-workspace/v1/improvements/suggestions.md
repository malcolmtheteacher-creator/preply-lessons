# V1 Improvements: Spaced Repetition Integration

## Critical Issue Identified

The english-lesson-builder skill (v5.0-5.1) had a **critical omission**: Spaced repetition was acknowledged in the anti-patterns table as a research-backed best practice ("Gold Standard #2" from Dunlosky et al.), but was **NOT IMPLEMENTED** in any archetype structure.

This created logical incoherence: the Speaking Pathway course (which the skill should generate) demonstrates full spaced repetition implementation, but the skill itself didn't include the mechanisms to create it.

## Changes Made in V5.2

### 1. Added Spaced Repetition as 10th Non-Negotiable ✅
- Elevated from "acknowledged but not implemented" to mandatory principle
- Added detailed mechanism explanation (forgetting curve, optimal intervals)
- Provided clear implementation guidance: Recall Zone retrieving 2-3 items from previous lessons at +3, +7, +14, +21 intervals
- Referenced Speaking Pathway (COURSE_ARCHITECTURE.md) as gold standard

### 2. Updated ALL Archetypes to Include Recall Zone ✅

**Archetype 1: Curious Conversations** (6 tabs → 7 tabs)
- Added Tab 6: Recall Zone
- Shifted Retrieval Wrap-Up to Tab 7

**Archetype 2: Knowledge Building** (7 tabs → 8 tabs)
- Added Tab 7: Recall Zone (recalls grammar structures from previous lessons)
- Shifted Retrieval Test to Tab 8

**Archetype 3: Skills Training** (7 tabs → 8 tabs)
- Added Tab 7: Recall Zone (recalls frameworks/techniques with interleaved application)
- Shifted Retrieval Debrief to Tab 8

**Archetype 4: Exam Strategy** (7 tabs → 8 tabs)
- Added Tab 7: Recall Zone (recalls exam strategies for cumulative mastery)
- Shifted Retrieval Debrief to Tab 8

### 3. Updated Student Output Ratio: 80% → 70%+ ✅
- Changed throughout all archetypes for consistency with Speaking Pathway
- Updated Core Rule, Quality Gates, and all tab requirements
- This aligns with Speaking Pathway's "70% Production" principle

### 4. Added "I can..." Self-Assessment Statements ✅
- Integrated into final tab of ALL archetypes
- Provides specific, measurable self-assessment criteria
- Example: "I can use [structure] to [specific communicative function]"
- Links to learning intentions for accountability

### 5. Added Speaking Skill Domains Taxonomy ✅
- Documented six domains from Speaking Pathway:
  1. Fluency & Flow
  2. Interaction & Response
  3. Discourse & Structure
  4. Opinion & Argument
  5. Description & Explanation
  6. Register & Appropriacy
- Provides classification system for speaking techniques
- Ensures progressive coverage across courses

### 6. Added File Naming Conventions ✅
- For course sequences: `sp_[level]_[number]_[topic].html`
- For standalone lessons: `[archetype]_[level]_[topic].html`
- For review lessons: append `_review` or `_spiral`
- Examples provided for clarity

### 7. Updated Pedagogy Checklist ✅
- Added: "Includes RECALL ZONE retrieving items from PREVIOUS lessons?"
- Added: "Includes 'I can...' self-assessment statement?"
- Changed: "Student output ratio ≥ 70%?" (was 80%)
- Now all 10 Non-Negotiables are checkable

### 8. Added "Speaking Pathway as Gold Standard" Section ✅
- Explicitly positions Speaking Pathway as reference implementation
- Lists what it demonstrates (full spaced repetition, optimal spacing, etc.)
- Clarifies relationship: archetypes provide structural flexibility, but same principles apply

### 9. Updated Version History ✅
- Added v5.2 entry documenting all changes
- Marked as "CRITICAL UPDATE" to emphasize importance
- Explained the fix addresses Gold Standard #2 omission

### 10. Added Failure History Entry ✅
- Documented v5.0-5.1 spaced repetition omission
- Explained the logical incoherence (Speaking Pathway had it, skill didn't)
- Prevents future similar omissions

## Expected Impact

### On Evaluation Metrics:
1. **Spaced Repetition Assertion**: v0 will FAIL (no Recall Zone), v1 should PASS
2. **Student Output Ratio**: Both should pass, but v1 is now consistent with Speaking Pathway
3. **"I can..." Statements**: v0 will FAIL (missing), v1 should PASS
4. **File Naming**: v1 provides explicit guidance
5. **Overall Coherence**: v1 aligns with Speaking Pathway gold standard

### On Lesson Quality:
- Lessons will now combat the forgetting curve systematically
- Students will consolidate learning across lessons, not just within lessons
- Self-assessment becomes explicit and measurable
- Course designers have clear taxonomy and naming conventions

## Philosophical Coherence Restored

The skill now has **logical coherence** between:
- Research principles cited (Dunlosky et al. - spaced repetition as Gold Standard #2)
- Anti-patterns table (spacing > cramming)
- Speaking Pathway implementation (full spaced repetition across 75 lessons)
- What the skill actually generates (Recall Zones in every lesson)

V5.2 fixes the critical gap where the skill acknowledged spaced repetition as best practice but didn't implement it.

## Notes for Future Versions

1. **Recall Zone flexibility**: The placement of Recall Zone can vary by archetype, but it MUST exist
2. **Standalone lessons**: When no lesson number is provided, include placeholder for Malcolm to specify items
3. **Review lessons**: Every 5th lesson can be Recall Zone-focused (see Speaking Pathway model)
4. **Optimal spacing**: +3, +7, +14, +21 is research-backed, but can adapt to course length

## Testing Recommendations

Test cases should verify:
1. Recall Zone appears in generated lessons
2. Spacing intervals are calculated correctly when lesson number is provided
3. "I can..." statements are specific and measurable
4. Student output ratio reflects 70%+ throughout
5. File naming follows conventions
