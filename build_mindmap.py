#!/usr/bin/env python3
"""
Build Mind Map Script (v4.0 — Website-Aligned Structure)
Extracts lesson data from malcolm_lesson_index.html and generates an iThoughts (.itmz) file.

Structure mirrors the website homepage (malcolmhyndman.com):
  1. Core Pathways — A1 Pathway, General English, Speaking Pathway
  2. Conversation & Discussion — Curious Conversations, Speaking Naturally
  3. Professional & Business — Professional Skills, Business Meetings, Bootcamp, Strategic Storytelling
  4. Advanced Discourse — Speaking Naturally Teens, Commanding Discourse, Bestiary, Beyond Perfect
  5. Skills & Exam Prep — Cambridge, Pronunciation, Listening, Quick Fix
  6. IELTS Preparation — Task 1, Task 2, Writing Pathway, Reading
  7. Religious Studies — Full secondary curriculum
  8. The Memory Palace — Art of Memory, Our Island Story, Philosophy, Epicurean, Dewey, Bestiary
  9. Tools — PowerUp, MandalArt, Speaking Practice, etc.
  10. Standalone Lessons — Dewey decimal classification (100–900)

Dashboards are placed inside their parent course, not in a separate branch.

Run from the gitsite directory after updating the lesson index.
"""

import re
import json
import zipfile
import io
import os
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).parent
INDEX_FILE = SCRIPT_DIR / "malcolm_lesson_index.html"
OUTPUT_FILE = SCRIPT_DIR.parent / "Assets" / "Mind Maps" / "Malcolm_Lessons_Map.itmz"
BASE_URL = "https://malcolmtheteacher-creator.github.io/preply-lessons/"


# ---------------------------------------------------------------------------
# Category configuration — mirrors website homepage sections
# ---------------------------------------------------------------------------
PATH_CONFIG = {
    # ── 1. Core Pathways ─────────────────────────────────────────────────
    'a1_pathway':      {'icon': '🌱', 'title': 'A1 English Pathway',           'order': 1,  'color': '2563EB', 'fill': 'DBEAFE'},
    'grammar':         {'icon': '📚', 'title': 'General English (A2→C1)',      'order': 2,  'color': '2563EB', 'fill': 'DBEAFE'},
    'speaking_path':   {'icon': '🎙️', 'title': 'Speaking Pathway (A2→C1)',     'order': 3,  'color': '2563EB', 'fill': 'DBEAFE'},

    # ── 2. Conversation & Discussion ─────────────────────────────────────
    'curious_conv':    {'icon': '💭', 'title': 'Curious Conversations',        'order': 4,  'color': 'D97706', 'fill': 'FEF3C7'},
    'speaking_nat':    {'icon': '🗣️', 'title': 'Speaking Naturally',           'order': 5,  'color': 'D97706', 'fill': 'FEF3C7'},

    # ── 3. Professional & Business ───────────────────────────────────────
    'professional':    {'icon': '💼', 'title': 'Professional & Business',      'order': 6,  'color': '16A34A', 'fill': 'DCFCE7'},

    # ── 4. Advanced Discourse ────────────────────────────────────────────
    'adv_discourse':   {'icon': '🎯', 'title': 'Advanced Discourse',           'order': 7,  'color': '7C3AED', 'fill': 'EDE9FE'},

    # ── 5. Skills & Exam Prep ────────────────────────────────────────────
    'cambridge':       {'icon': '🎓', 'title': 'Cambridge Exams',              'order': 8,  'color': '64748B', 'fill': 'F1F5F9'},
    'pronunciation':   {'icon': '🔊', 'title': 'Pronunciation Pathway',        'order': 9,  'color': '64748B', 'fill': 'F1F5F9'},
    'listening':       {'icon': '🎧', 'title': 'Listening Practice',            'order': 10, 'color': '64748B', 'fill': 'F1F5F9'},
    'quick_fix':       {'icon': '⚡', 'title': 'Quick Fix Matrix',             'order': 11, 'color': '64748B', 'fill': 'F1F5F9'},
    'ote':             {'icon': '🏅', 'title': 'OTE Exam Prep',                'order': 12, 'color': '64748B', 'fill': 'F1F5F9'},

    # ── 6. IELTS Preparation ────────────────────────────────────────────
    'ielts':           {'icon': '📝', 'title': 'IELTS Preparation',            'order': 13, 'color': 'DC2626', 'fill': 'FEE2E2'},

    # ── 7. Religious Studies ─────────────────────────────────────────────
    'rs':              {'icon': '🕊️', 'title': 'Religious Studies',             'order': 14, 'color': '1A5C3A', 'fill': 'D1FAE5'},

    # ── 8. The Memory Palace ─────────────────────────────────────────────
    'memory':          {'icon': '🧠', 'title': 'Art of Memory',                'order': 15, 'color': 'D4A843', 'fill': '1A2744'},
    'history':         {'icon': '🏰', 'title': 'Our Island Story',             'order': 16, 'color': 'C9A84C', 'fill': '1A2744'},
    'philosophy':      {'icon': '🏛️', 'title': 'Western Philosophy',           'order': 17, 'color': '8AB4D6', 'fill': '1A2744'},
    'epicurean':       {'icon': '🌿', 'title': 'The Epicurean Path',           'order': 18, 'color': '4A7C59', 'fill': '1A2744'},
    'dewey_palace':    {'icon': '🗂️', 'title': 'Dewey Memory Palace',          'order': 19, 'color': '7B5EA7', 'fill': '1A2744'},
    'bestiary':        {'icon': '🦁', 'title': 'The Bestiary',                 'order': 20, 'color': 'D4A843', 'fill': '1A2744'},

    # ── 9. Tools ─────────────────────────────────────────────────────────
    'tools':           {'icon': '🔧', 'title': 'Tools',                        'order': 21, 'color': '475569', 'fill': 'F1F5F9'},

    # ── 10. Other Courses ────────────────────────────────────────────────
    'teens':           {'icon': '🎮', 'title': 'Teens Course',                 'order': 22, 'color': 'E91E63', 'fill': 'FCE4EC'},
    'academic':        {'icon': '🎓', 'title': 'Academic & IB English',        'order': 23, 'color': '5D6D7E', 'fill': 'EBF5FB'},
    'writing':         {'icon': '✍️', 'title': 'Writing & Essay Skills',       'order': 24, 'color': '16A085', 'fill': 'E8F8F5'},
    'news':            {'icon': '📰', 'title': 'Breaking News English',        'order': 25, 'color': 'C0392B', 'fill': 'FDEDEC'},
    'first_lessons':   {'icon': '👋', 'title': 'First Lesson Assessments',     'order': 26, 'color': '1ABC9C', 'fill': 'E8F6F3'},

    # ── 11. Standalone — Dewey Decimal ───────────────────────────────────
    'standalone':      {'icon': '📖', 'title': 'Standalone Lessons (by Topic)','order': 27, 'color': '6B7280', 'fill': 'F3F4F6'},
}

LEVEL_COLORS = {
    'A1': {'color': '27AE60', 'fill': 'E8FDF0'},
    'A2': {'color': '2ECC71', 'fill': 'EAFAF1'},
    'B1': {'color': 'F39C12', 'fill': 'FEF9E7'},
    'B2': {'color': 'E67E22', 'fill': 'FDF2E9'},
    'C1': {'color': 'E74C3C', 'fill': 'FDEDEC'},
    'C2': {'color': '9B59B6', 'fill': 'F5EEF8'},
}


# ---------------------------------------------------------------------------
# Lesson data extraction
# ---------------------------------------------------------------------------
def extract_lesson_data(html_content):
    """Extract the lessonData array from the HTML file."""
    pattern = r'window\.lessonData\s*=\s*\[(.*?)\];'
    match = re.search(pattern, html_content, re.DOTALL)
    if not match:
        raise ValueError("Could not find lessonData in HTML file")

    data_str = match.group(1)
    lessons = []
    lesson_pattern = (
        r"\{\s*filename:\s*'((?:[^'\\]|\\.)*)'"
        r"\s*,\s*title:\s*'((?:[^'\\]|\\.)*)'"
        r"\s*,\s*level:\s*'((?:[^'\\]|\\.)*)'"
        r"\s*,\s*series:\s*'((?:[^'\\]|\\.)*)'"
        r"\s*,\s*keywords:\s*'((?:[^'\\]|\\.)*)'\s*\}"
    )

    for m in re.finditer(lesson_pattern, data_str):
        lessons.append({
            'filename': m.group(1).replace("\\'", "'"),
            'title':    m.group(2).replace("\\'", "'"),
            'level':    m.group(3).replace("\\'", "'"),
            'series':   m.group(4).replace("\\'", "'"),
            'keywords': m.group(5).replace("\\'", "'"),
        })

    return lessons


# ---------------------------------------------------------------------------
# Smart categorisation engine (v4 — website-aligned)
# ---------------------------------------------------------------------------
def categorize_lesson(filename, title, series='', level='', keywords=''):
    """
    Categorise a lesson to match the website homepage structure.

    Strategy (layered, in priority order):
      1. Skip utility files (templates, trackers, etc.)
      2. Dashboards → place inside their parent course
      3. Prefix-based course detection (most reliable)
      4. Series field matching (fallback)
      5. Filename keyword patterns
      6. Dewey-style topic classification for everything else
    """
    fl = filename.lower()
    tl = title.lower()
    sl = series.lower().strip()
    lv = level.upper().strip()

    # ── 1. Skip utility / non-lesson files ─────────────────────────────
    skip_patterns = [
        'template', 'tracker', 'quicknotes', 'bujo', 'kanban',
        'lifebalance', 'teleprompter', 'test_lesson_delete',
        'placeholder', 'website_with_tabs', 'index.html',
        'quick_fix_index', 'lesson_index',
    ]
    if any(x in fl for x in skip_patterns):
        return None

    # ── 2. Dashboards → parent course (with 📊 prefix) ────────────────
    if 'dashboard' in fl or 'pathway' in fl and 'lesson' not in fl:
        if 'a1' in fl and 'pathway' in fl:
            return {'cat': 'a1_pathway', 'sub': '📊 Dashboard'}
        if 'general_english' in fl or ('lesson_' in fl and 'dashboard' in fl):
            return {'cat': 'grammar', 'sub': '📊 Dashboard'}
        if 'speaking_pathway' in fl:
            return {'cat': 'speaking_path', 'sub': '📊 Dashboard'}
        if 'speaking_naturally_teens' in fl:
            return {'cat': 'adv_discourse', 'sub': '📊 Dashboard'}
        if 'speaking_naturally' in fl:
            return {'cat': 'speaking_nat', 'sub': '📊 Dashboard'}
        if 'curious_conversation' in fl:
            return {'cat': 'curious_conv', 'sub': '📊 Dashboard'}
        if 'ielts' in fl:
            return {'cat': 'ielts', 'sub': '📊 Dashboard'}
        if 'cambridge' in fl or 'cae' in fl or 'cpe' in fl:
            return {'cat': 'cambridge', 'sub': '📊 Dashboard'}
        if 'memory' in fl or 'art_of_memory' in fl:
            return {'cat': 'memory', 'sub': '📊 Dashboard'}
        if 'wp_' in fl or 'philosophy' in fl:
            return {'cat': 'philosophy', 'sub': '📊 Dashboard'}
        if 'epicurean' in fl:
            return {'cat': 'epicurean', 'sub': '📊 Dashboard'}
        if 'quick_fix' in fl or 'qf_' in fl:
            return {'cat': 'quick_fix', 'sub': '📊 Dashboard'}
        if 'professional' in fl or 'pss' in fl:
            return {'cat': 'professional', 'sub': '📊 Dashboard'}
        if 'business_bootcamp' in fl:
            return {'cat': 'professional', 'sub': '📊 Dashboard'}
        if 'business_meeting' in fl:
            return {'cat': 'professional', 'sub': '📊 Dashboard'}
        if 'strategic_storytelling' in fl:
            return {'cat': 'professional', 'sub': '📊 Dashboard'}
        if 'teen' in fl:
            return {'cat': 'teens', 'sub': '📊 Dashboard'}
        if 'news' in fl:
            return {'cat': 'news', 'sub': '📊 Dashboard'}
        if 'ois' in fl:
            return {'cat': 'history', 'sub': '📊 Dashboard'}
        if 'rs_' in fl or 'religious' in fl:
            return {'cat': 'rs', 'sub': '📊 Dashboard'}
        if 'pronunciation' in fl:
            return {'cat': 'pronunciation', 'sub': '📊 Dashboard'}
        if 'commanding_discourse' in fl:
            return {'cat': 'adv_discourse', 'sub': '📊 Dashboard'}
        if 'beyond_perfect' in fl:
            return {'cat': 'adv_discourse', 'sub': '📊 Dashboard'}
        if 'discourse_bestiary' in fl:
            return {'cat': 'adv_discourse', 'sub': '📊 Dashboard'}
        if 'ote' in fl:
            return {'cat': 'ote', 'sub': '📊 Dashboard'}
        # Generic dashboard — skip rather than miscategorise
        if 'dashboard' in fl:
            return None

    # ── 3. Prefix-based course detection ───────────────────────────────

    # ▸ CORE PATHWAYS

    # A1 Pathway (a1p_ prefix — 50 lessons)
    if fl.startswith('a1p_') or fl.startswith('a1_pathway'):
        num = _extract_num(fl)
        if num <= 10:
            return {'cat': 'a1_pathway', 'sub': 'Unit 1: Foundations (1-10)'}
        if num <= 20:
            return {'cat': 'a1_pathway', 'sub': 'Unit 2: Daily Life (11-20)'}
        if num <= 30:
            return {'cat': 'a1_pathway', 'sub': 'Unit 3: Expressing Ideas (21-30)'}
        if num <= 40:
            return {'cat': 'a1_pathway', 'sub': 'Unit 4: Out & About (31-40)'}
        return {'cat': 'a1_pathway', 'sub': 'Unit 5: Moving Forward (41+)'}

    # Speaking Pathway (sp_ prefix — 75 lessons + prep packs)
    sp_match = re.match(r'sp_(prep_)?([abc]\d)_(\d+)', fl)
    if sp_match:
        is_prep = sp_match.group(1) is not None
        sp_level = sp_match.group(2).upper()
        sp_num = int(sp_match.group(3))
        prefix = 'Prep: ' if is_prep else ''

        if sp_level == 'A2':
            if sp_num <= 5:
                return {'cat': 'speaking_path', 'sub': f'{prefix}A2 Module 1: Foundations (1-5)'}
            if sp_num <= 10:
                return {'cat': 'speaking_path', 'sub': f'{prefix}A2 Module 2: Building Blocks (6-10)'}
            if sp_num <= 15:
                return {'cat': 'speaking_path', 'sub': f'{prefix}A2 Module 3: Expanding Range (11-15)'}
            return {'cat': 'speaking_path', 'sub': f'{prefix}A2 Module 4: Mastery (16-20)'}

        if sp_level == 'B1':
            if sp_num <= 25:
                return {'cat': 'speaking_path', 'sub': f'{prefix}B1 Module 1: Core Skills (21-25)'}
            if sp_num <= 30:
                return {'cat': 'speaking_path', 'sub': f'{prefix}B1 Module 2: Structuring (26-30)'}
            if sp_num <= 35:
                return {'cat': 'speaking_path', 'sub': f'{prefix}B1 Module 3: Discussion (31-35)'}
            return {'cat': 'speaking_path', 'sub': f'{prefix}B1 Module 4: Fluency (36-40)'}

        if sp_level == 'B2':
            if sp_num <= 45:
                return {'cat': 'speaking_path', 'sub': f'{prefix}B2 Module 1: Sophistication (41-45)'}
            if sp_num <= 50:
                return {'cat': 'speaking_path', 'sub': f'{prefix}B2 Module 2: Nuance (46-50)'}
            if sp_num <= 55:
                return {'cat': 'speaking_path', 'sub': f'{prefix}B2 Module 3: Idiom & Style (51-55)'}
            return {'cat': 'speaking_path', 'sub': f'{prefix}B2 Module 4: Mastery (56-60)'}

        if sp_level == 'C1':
            if sp_num <= 6:
                return {'cat': 'speaking_path', 'sub': f'{prefix}C1 Commanding Discourse (1-6)'}
            if sp_num <= 65:
                return {'cat': 'speaking_path', 'sub': f'{prefix}C1 Module 1: Transition (61-65)'}
            if sp_num <= 70:
                return {'cat': 'speaking_path', 'sub': f'{prefix}C1 Module 2: Expertise (66-70)'}
            return {'cat': 'speaking_path', 'sub': f'{prefix}C1 Module 3: Mastery (71-75)'}

    # Grammar Course (lesson_XX pattern — the original 50-lesson series)
    grammar_match = re.match(r'lesson_(\d{2})', fl)
    if grammar_match:
        num = int(grammar_match.group(1))
        if num <= 10:
            return {'cat': 'grammar', 'sub': 'A2 Elementary (1-10)'}
        if num <= 25:
            return {'cat': 'grammar', 'sub': 'B1 Intermediate (11-25)'}
        if num <= 40:
            return {'cat': 'grammar', 'sub': 'B2 Upper Intermediate (26-40)'}
        return {'cat': 'grammar', 'sub': 'C1 Advanced (41-50)'}

    # General Grammar Course files
    if fl.startswith('general_lesson_'):
        return {'cat': 'grammar', 'sub': 'General Lessons'}

    if fl.startswith('grammar_'):
        return {'cat': 'grammar', 'sub': 'Grammar Topics'}

    # ▸ CONVERSATION & DISCUSSION

    # Curious Conversations
    if 'curious_conversations' in fl or 'curious conversations' in tl:
        if 'series2' in fl or 'series_2' in fl:
            return {'cat': 'curious_conv', 'sub': 'Series 2'}
        return {'cat': 'curious_conv', 'sub': 'Series 1'}

    if 'real_conversations' in fl:
        return {'cat': 'curious_conv', 'sub': 'Real Conversations'}

    # Speaking Naturally
    if 'speaking_naturally_teens' in fl:
        return {'cat': 'adv_discourse', 'sub': 'Speaking Naturally: Teens'}
    if 'speaking_naturally_advanced' in fl:
        return {'cat': 'speaking_nat', 'sub': 'Advanced'}
    if 'speaking_naturally' in fl:
        return {'cat': 'speaking_nat', 'sub': 'Adults'}

    # B2/C1 Conversations (bc_ prefix)
    if fl.startswith('bc_'):
        return {'cat': 'curious_conv', 'sub': 'B2/C1 Conversations'}

    # ▸ PROFESSIONAL & BUSINESS

    # Strategic Storytelling
    if 'strategic_storytelling' in fl or 'storytelling_' in fl:
        return {'cat': 'professional', 'sub': 'Strategic Storytelling'}

    # Business Bootcamp (8 lessons)
    if fl.startswith('business-bootcamp') or fl.startswith('business_bootcamp'):
        return {'cat': 'professional', 'sub': 'Business Bootcamp'}

    # Business Meetings (5 lessons)
    biz_meetings_files = [
        'closing_meetings_following_up', 'first_impressions_small_talk',
        'giving_opinions_suggestions', 'handling_questions_buying_time',
        'problems_and_solutions',
    ]
    if any(fl.startswith(f) for f in biz_meetings_files):
        return {'cat': 'professional', 'sub': 'Business Meeting Essentials'}

    # Professional Speaking Skills (pss_ prefix)
    if fl.startswith('pss_'):
        return {'cat': 'professional', 'sub': 'Professional Speaking Skills'}

    # ▸ ADVANCED DISCOURSE

    # Commanding Discourse
    if 'commanding_discourse' in fl or fl.startswith('sp_c1_0'):
        # sp_c1_01 through sp_c1_06 are Commanding Discourse
        sp_c1_match = re.match(r'sp_c1_0([1-6])', fl)
        if sp_c1_match:
            return {'cat': 'adv_discourse', 'sub': 'Commanding Discourse'}

    # Beyond Perfect (bp_ prefix or full name)
    if 'beyond_perfect' in fl or fl.startswith('bp_'):
        return {'cat': 'adv_discourse', 'sub': 'Beyond Perfect'}

    # Discourse Bestiary (distinct from Memory Palace bestiary)
    if 'discourse_bestiary' in fl:
        return {'cat': 'adv_discourse', 'sub': 'Discourse Bestiary'}

    # ▸ SKILLS & EXAM PREP

    # Quick Fix lessons (qf_ prefix)
    if fl.startswith('qf_'):
        if 'falsefriend' in fl or 'false_friend' in fl:
            for lang in ['french', 'italian', 'spanish', 'german', 'portuguese',
                         'polish', 'turkish', 'dutch', 'czech', 'korean',
                         'japanese', 'arabic', 'russian']:
                if lang in fl:
                    return {'cat': 'quick_fix', 'sub': f'False Friends: {lang.title()}'}
            return {'cat': 'quick_fix', 'sub': 'False Friends: Other'}
        if 'grammar' in fl:
            return {'cat': 'quick_fix', 'sub': 'Grammar Fixes'}
        if 'vocab' in fl:
            return {'cat': 'quick_fix', 'sub': 'Vocabulary Fixes'}
        if 'pronun' in fl:
            return {'cat': 'quick_fix', 'sub': 'Pronunciation Fixes'}
        if 'colloc' in fl:
            return {'cat': 'quick_fix', 'sub': 'Collocation Fixes'}
        if 'spell' in fl:
            return {'cat': 'quick_fix', 'sub': 'Spelling Fixes'}
        return {'cat': 'quick_fix', 'sub': 'General Fixes'}

    # Cambridge exams
    if 'cambridge' in fl or 'cae' in fl or 'cpe' in fl:
        return {'cat': 'cambridge', 'sub': None}

    # Pronunciation (includes pron_ prefix lessons)
    if 'pronunciation' in fl or fl.startswith('pron_'):
        return {'cat': 'pronunciation', 'sub': None}

    # Listening
    if fl.startswith('general_listening_') or 'listening_lesson' in fl or 'listening-lesson' in fl:
        return {'cat': 'listening', 'sub': None}

    # Discussion lessons (discuss_ prefix — standalone B2/C1 discussion topics)
    if fl.startswith('discuss_'):
        return {'cat': 'curious_conv', 'sub': 'Discussion Topics'}

    # Brave Lessons / Debate series (bl_ prefix)
    if fl.startswith('bl_'):
        return {'cat': 'curious_conv', 'sub': 'Brave Lessons'}

    # OTE exam prep
    if fl.startswith('ote_') or 'ote ' in tl:
        return {'cat': 'ote', 'sub': None}

    # ▸ IELTS PREPARATION

    if 'ielts_lesson_' in fl and 'task_1' not in fl and 'reading' not in fl:
        return {'cat': 'ielts', 'sub': 'Writing Task 2'}
    if 'ielts_task_1' in fl or 'ielts_task1' in fl:
        return {'cat': 'ielts', 'sub': 'Writing Task 1'}
    if 'ielts_reading' in fl or 'ielts-reading' in fl:
        return {'cat': 'ielts', 'sub': 'Reading'}
    if 'ielts_speaking' in fl:
        return {'cat': 'ielts', 'sub': 'Speaking'}
    if 'ielts_writing_pathway' in fl:
        return {'cat': 'ielts', 'sub': 'Writing Pathway'}
    if 'ielts_essay' in fl:
        return {'cat': 'ielts', 'sub': 'Essay Practice'}
    if 'ielts' in fl:
        return {'cat': 'ielts', 'sub': 'Other Resources'}

    # ▸ RELIGIOUS STUDIES

    if fl.startswith('rs_'):
        # Sub-categorise by year/key stage if possible
        if 'ks3' in fl or 'y7' in fl or 'y8' in fl or 'y9' in fl:
            return {'cat': 'rs', 'sub': 'KS3 (Years 7-9)'}
        if 'gcse' in fl or 'y10' in fl or 'y11' in fl:
            return {'cat': 'rs', 'sub': 'GCSE (Years 10-11)'}
        if 'alevel' in fl or 'a_level' in fl or 'y12' in fl or 'y13' in fl:
            return {'cat': 'rs', 'sub': 'A-Level (Years 12-13)'}
        return {'cat': 'rs', 'sub': None}

    # ▸ THE MEMORY PALACE

    # Western Philosophy (wp_ prefix — 50 lessons)
    if fl.startswith('wp_'):
        num = _extract_num(fl)
        if num <= 10:
            return {'cat': 'philosophy', 'sub': 'Ancient Greece (1-10)'}
        if num <= 20:
            return {'cat': 'philosophy', 'sub': 'Hellenistic & Roman (11-20)'}
        if num <= 30:
            return {'cat': 'philosophy', 'sub': 'Medieval (21-30)'}
        if num <= 40:
            return {'cat': 'philosophy', 'sub': 'Early Modern (31-40)'}
        return {'cat': 'philosophy', 'sub': 'Modern (41-50)'}

    # Epicurean course (epicurean_ prefix — 30 lessons)
    if fl.startswith('epicurean_'):
        num = _extract_num(fl)
        if num <= 10:
            return {'cat': 'epicurean', 'sub': 'Foundations (1-10)'}
        if num <= 20:
            return {'cat': 'epicurean', 'sub': 'Deep Dives (11-20)'}
        return {'cat': 'epicurean', 'sub': 'Legacy & Influence (21+)'}

    # Stoicism
    if 'stoicism' in fl:
        return {'cat': 'philosophy', 'sub': 'Stoicism'}

    # Our Island Story / History (ois_ prefix — 20 lessons)
    if fl.startswith('ois_'):
        num = _extract_num(fl)
        if num <= 10:
            return {'cat': 'history', 'sub': 'Early Britain (1-10)'}
        if num <= 20:
            return {'cat': 'history', 'sub': 'Medieval (11-20)'}
        return {'cat': 'history', 'sub': 'Early Modern (21+)'}

    # Art of Memory course (lesson-XX-* + memory keywords in title)
    if (fl.startswith('lesson-') and ('memory' in tl or 'art of memory' in tl
         or 'pao' in tl or 'peg' in tl or 'palace' in tl or 'dominic' in tl
         or 'ben system' in tl or 'major system' in tl)):
        num = _extract_num(fl)
        if num <= 5:
            return {'cat': 'memory', 'sub': 'Foundations (1-5)'}
        if num <= 10:
            return {'cat': 'memory', 'sub': 'Number Systems (6-10)'}
        if num <= 15:
            return {'cat': 'memory', 'sub': 'Practical Applications (11-15)'}
        if num <= 20:
            return {'cat': 'memory', 'sub': 'Academic & Language (16-20)'}
        if num <= 25:
            return {'cat': 'memory', 'sub': 'Advanced Techniques (21-25)'}
        return {'cat': 'memory', 'sub': 'Mastery & Competition (26-30)'}

    # Dewey Memory Palace
    if fl.startswith('dewey-') or fl.startswith('dewey_'):
        return {'cat': 'dewey_palace', 'sub': None}

    # Bestiary (memory system)
    if 'bestiary' in fl and 'discourse' not in fl:
        return {'cat': 'bestiary', 'sub': None}

    # Memory-related standalone files
    if ('art-of-memory' in fl or 'art_of_memory' in fl or 'memory-books' in fl
            or 'memory_lesson' in fl or 'memory_palace' in fl):
        return {'cat': 'memory', 'sub': 'Resources & Guides'}

    # ▸ OTHER COURSES

    # Professional (broader patterns + scenario lessons)
    if fl.startswith('lessons/scenario') or fl.startswith('scenario'):
        return {'cat': 'professional', 'sub': 'Professional Scenarios'}

    prof_patterns = [
        'professional', 'business', 'interview', 'kuba',
        'presenting', 'workplace', 'leading', 'teams', 'meeting',
    ]
    if any(x in fl for x in prof_patterns):
        return {'cat': 'professional', 'sub': None}

    # Writing & Essays (non-IELTS)
    if ('essay' in fl or 'writing' in fl or 'sentence_' in fl) and 'ielts' not in fl:
        return {'cat': 'writing', 'sub': None}

    # Breaking News
    if 'breaking_news' in fl or 'spain_rail' in fl:
        return {'cat': 'news', 'sub': None}

    # IB / Academic English
    if 'ib_' in fl or fl.startswith('ib ') or 'academic' in fl or 'sat_' in fl:
        return {'cat': 'academic', 'sub': None}

    # Teens
    if 'teens' in fl or 'teen' in fl:
        return {'cat': 'teens', 'sub': None}

    # First lessons / assessments
    if 'first_lesson' in fl or 'diagnostic' in fl:
        return {'cat': 'first_lessons', 'sub': None}

    # ▸ TOOLS

    tool_patterns = [
        'tenses_guide', 'parts_of_speech', 'past_participle',
        'speed_reading', 'speaking-practice', 'preply_screen_share',
        'concorso', 'powerup', 'mandalart', 'countdownart',
    ]
    if any(x in fl for x in tool_patterns):
        return {'cat': 'tools', 'sub': None}

    if fl.startswith('skills_'):
        return {'cat': 'tools', 'sub': 'Skills Lessons'}

    if 'review_sheet' in fl or 'lesson_review' in fl:
        return {'cat': 'tools', 'sub': 'Review Sheets'}

    # ── Series field matching (fallback) ─────────────────────────────
    if sl:
        if 'grammar' in sl:
            return {'cat': 'grammar', 'sub': 'From Series'}
        if 'ielts' in sl:
            return {'cat': 'ielts', 'sub': 'From Series'}
        if 'speaking naturally' in sl:
            return {'cat': 'speaking_nat', 'sub': 'From Series'}
        if 'curious conversation' in sl:
            return {'cat': 'curious_conv', 'sub': 'From Series'}
        if 'cambridge' in sl:
            return {'cat': 'cambridge', 'sub': None}
        if 'beginner' in sl:
            return {'cat': 'a1_pathway', 'sub': 'From Series'}
        if 'teen' in sl:
            return {'cat': 'teens', 'sub': None}
        if 'professional' in sl or 'business' in sl:
            return {'cat': 'professional', 'sub': None}

    # A1 beginner detection (broader)
    if fl.startswith('a1_') or '_a1_' in fl or 'beginner' in fl:
        return {'cat': 'a1_pathway', 'sub': 'Standalone A1'}

    # Topic-based / young learners
    topic_patterns = [
        'dinosaur', 'space', 'ocean', 'egypt', 'greece', 'weather',
        'explorer', 'gaming', 'erebus', 'ww2', 'world_war', 'human_body',
        'ancient', 'comic_book', 'comic book', 'horse_riding', 'equestrian',
        'artemis', 'moon', 'path_of_titans', 'tennis',
    ]
    if any(x in fl for x in topic_patterns):
        return {'cat': 'standalone', 'sub': '700: Daily Life & Lifestyle'}

    if fl.startswith('explore_'):
        return {'cat': 'standalone', 'sub': '600: Arts, Life & Reflection'}

    # Levelled conversation/topic lessons
    if 'b2c1' in fl or 'c1c2' in fl:
        return {'cat': 'curious_conv', 'sub': 'B2/C1 Conversations'}
    if fl.endswith('b1b2.html') or '_b1b2' in fl:
        return {'cat': 'curious_conv', 'sub': 'B1/B2 Conversations'}

    # Seasonal
    if 'christmas' in fl or 'new_year' in fl:
        return {'cat': 'standalone', 'sub': '600: Arts, Life & Reflection'}

    # Standalone topic lessons
    if 'boredom' in fl or 'new_year_plans' in fl:
        return {'cat': 'curious_conv', 'sub': None}

    # ── Dewey-style topic classification (catch-all) ─────────────────
    topic = _classify_topic(fl, tl)
    return {'cat': 'standalone', 'sub': topic}


def _extract_num(filename):
    """Pull the first number from a filename for sub-sorting."""
    m = re.search(r'(\d+)', filename)
    return int(m.group(1)) if m else 999


def _classify_topic(filename, title):
    """
    Dewey-style topic classification for standalone lessons.

    Groups lessons by subject matter using title + filename keywords.
    Designed to catch future lessons too — keywords are broad enough
    that a new lesson on 'The Ethics of Surveillance' would land in
    'Society & Ethics' without needing a code change.

    Classification (inspired by Dewey but adapted for ELT):
      100 — Psychology & Behaviour
      200 — Society & Ethics
      300 — Politics & Power
      400 — Language & Communication
      500 — Science & Technology
      600 — Arts, Life & Reflection
      700 — Daily Life & Lifestyle
      800 — Work & Career
      900 — General / Unclassified
    """
    combined = filename + ' ' + title

    # ── 100: Psychology & Behaviour ────────────────────────────────────
    psych_kw = [
        'psychology', 'psycholog', 'behaviour', 'behavior', 'cognitive',
        'bias', 'impression', 'imposter', 'syndrome', 'decision',
        'pattern', 'believe', 'nudge', 'invisible hand', 'madness',
        'crowd', 'smart people', 'risk', 'fear', 'warning', 'ignore',
        'paradox', 'choice', 'motivation', 'drives us', 'split-second',
        'reading people', 'first impression', 'morning people', 'night owl',
        'forgetting', 'memory', 'brain', 'mindset', 'habit',
    ]
    if any(kw in combined for kw in psych_kw):
        return '100: Psychology & Behaviour'

    # ── 200: Society & Ethics ──────────────────────────────────────────
    society_kw = [
        'cancel culture', 'social media', 'digital ethics', 'ethics',
        'believe', 'religion', 'third place', 'belonging', 'community',
        'friend', 'friendship', 'resolution', 'selfish', 'parents',
        'generation', 'things we leave', 'behind', 'dating', 'love',
        'gender', 'equality', 'justice', 'moral', 'values',
        'pets', 'animal', 'welfare',
    ]
    if any(kw in combined for kw in society_kw):
        return '200: Society & Ethics'

    # ── 300: Politics & Power ──────────────────────────────────────────
    politics_kw = [
        'politic', 'power', 'trade war', 'tariff', 'greenland',
        'soft power', 'operation', 'resolve', 'war', 'conflict',
        'democracy', 'propaganda', 'media', 'news', 'government',
        'law', 'legal', 'rights', 'playing the room', 'strategic',
        'trust', 'negotiate', 'diplomacy',
    ]
    if any(kw in combined for kw in politics_kw):
        return '300: Politics & Power'

    # ── 400: Language & Communication ──────────────────────────────────
    language_kw = [
        'accent', 'speakerism', 'native speaker', 'rhetorical',
        'literary', 'rhetoric', 'communication', 'speaking',
        'conversation', 'listening', 'language', 'text analysis',
        'paper 1', 'discourse', 'eloquen', 'persuasi',
        'yes doesn', 'teacher conversation',
    ]
    if any(kw in combined for kw in language_kw):
        return '400: Language & Communication'

    # ── 500: Science & Technology ──────────────────────────────────────
    science_kw = [
        'ai ', 'artificial intelligence', 'robot', 'technology', 'tech',
        'computer', 'science', 'statistic', 'numbers game', 'data',
        'food tech', 'quality', 'innovation', 'fusion', 'experiment',
        'bullshit jobs',
    ]
    if any(kw in combined for kw in science_kw):
        return '500: Science & Technology'

    # ── 600: Arts, Life & Reflection ───────────────────────────────────
    arts_kw = [
        'book', 'art ', 'arts', 'music', 'film', 'movie', 'story',
        'creative', 'painting', 'museum', 'culture', 'tradition',
        'celebration', 'festival', 'christmas', 'seasonal',
        'growing older', 'simple pleasures', 'small things',
        'lost art', 'doing nothing', 'joy',
    ]
    if any(kw in combined for kw in arts_kw):
        return '600: Arts, Life & Reflection'

    # ── 700: Daily Life & Lifestyle ────────────────────────────────────
    daily_kw = [
        'daily', 'routine', 'hobby', 'free time', 'food', 'cooking',
        'travel', 'holiday', 'adventure', 'pet ', 'family', 'home',
        'health', 'sport', 'shopping', 'weather', 'monday morning',
        'work week', '4-day', '4_day', 'lifestyle',
    ]
    if any(kw in combined for kw in daily_kw):
        return '700: Daily Life & Lifestyle'

    # ── 800: Work & Career ─────────────────────────────────────────────
    work_kw = [
        'career', 'job', 'work ', 'leap', 'reinvention', 'interview',
        'profession', 'business', 'office', 'meeting', 'corporate',
        'pressure', 'problem solving', 'under pressure',
    ]
    if any(kw in combined for kw in work_kw):
        return '800: Work & Career'

    # ── 900: Language & Learning (catch remaining ELT lessons) ────────
    learning_kw = [
        'learn', 'lesson', 'teach', 'experience', 'limerick', 'poem',
        'writer', 'weapon', 'used to be', 'people we',
        'yes doesn',
    ]
    if any(kw in combined for kw in learning_kw):
        return '400: Language & Communication'

    # ── 900: General ───────────────────────────────────────────────────
    return '900: General'


# ---------------------------------------------------------------------------
# Sorting helper
# ---------------------------------------------------------------------------
def get_lesson_num(filename):
    """Extract lesson number for display sorting."""
    m = re.search(r'(?:lesson[_-]?)(\d+)', filename, re.IGNORECASE)
    if m:
        return int(m.group(1))
    m = re.search(r'_(\d+)', filename)
    if m:
        return int(m.group(1))
    m = re.search(r'(\d+)', filename)
    if m:
        return int(m.group(1))
    return 999


# ---------------------------------------------------------------------------
# XML / iThoughts generation
# ---------------------------------------------------------------------------
def build_itmz_xml(lessons):
    """Build the XML content for the .itmz file with iThoughts styling."""
    categories = {}
    skipped = 0

    for lesson in lessons:
        cat_info = categorize_lesson(
            lesson['filename'],
            lesson['title'],
            series=lesson.get('series', ''),
            level=lesson.get('level', ''),
            keywords=lesson.get('keywords', ''),
        )
        if not cat_info:
            skipped += 1
            continue

        cat = cat_info['cat']
        sub = cat_info['sub']

        if cat not in categories:
            categories[cat] = {'lessons': [], 'subs': {}}

        if sub:
            categories[cat]['subs'].setdefault(sub, []).append(lesson)
        else:
            categories[cat]['lessons'].append(lesson)

    # Sort categories by configured order
    sorted_cats = sorted(
        categories.keys(),
        key=lambda x: PATH_CONFIG.get(x, {}).get('order', 99),
    )

    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    def escape_xml(text):
        return (text
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&apos;'))

    def make_topic(text, level=0, children="", link="",
                   color=None, fill=None, shape=None, folded=True,
                   position=None):
        attrs = [f'text="{escape_xml(text)}"']
        if link:
            attrs.append(f'link="{escape_xml(link)}"')
        if color:
            attrs.append(f'color="#{color}"')
        if fill:
            attrs.append(f'fill-color="#{fill}"')
        if shape:
            attrs.append(f'shape="{shape}"')
        if position is not None:
            attrs.append(f'position="{position}"')
        if level > 0 and folded:
            attrs.append('folded="1"')
        attrs.append(f'created="{now}"')
        attrs.append(f'modified="{now}"')
        attr_str = ' '.join(attrs)
        if children:
            return f'<topic {attr_str}>{children}</topic>'
        return f'<topic {attr_str}/>'

    # ── Group categories into website sections for the mindmap ────────
    SECTIONS = [
        ('🗺️ Core Pathways',            ['a1_pathway', 'grammar', 'speaking_path'],
         '2563EB', 'DBEAFE'),
        ('💬 Conversation & Discussion', ['curious_conv', 'speaking_nat'],
         'D97706', 'FEF3C7'),
        ('💼 Professional & Business',   ['professional'],
         '16A34A', 'DCFCE7'),
        ('🎯 Advanced Discourse',        ['adv_discourse'],
         '7C3AED', 'EDE9FE'),
        ('🔧 Skills & Exam Prep',        ['cambridge', 'pronunciation', 'listening', 'quick_fix', 'ote'],
         '64748B', 'F1F5F9'),
        ('📝 IELTS Preparation',         ['ielts'],
         'DC2626', 'FEE2E2'),
        ('🕊️ Religious Studies',          ['rs'],
         '1A5C3A', 'D1FAE5'),
        ('🧠 The Memory Palace',         ['memory', 'history', 'philosophy', 'epicurean', 'dewey_palace', 'bestiary'],
         'D4A843', '1A2744'),
        ('🔧 Tools',                     ['tools'],
         '475569', 'F1F5F9'),
        ('📚 Other Courses',             ['teens', 'academic', 'writing', 'news', 'first_lessons'],
         '6B7280', 'F3F4F6'),
        ('📖 Standalone (by Topic)',     ['standalone'],
         '6B7280', 'F3F4F6'),
    ]

    section_xml = []

    for idx, (section_title, cat_keys, section_color, section_fill) in enumerate(SECTIONS):
        # Alternate branches: even index → right (1), odd index → left (2)
        side = 1 if idx % 2 == 0 else 2
        # Collect all categories in this section that have lessons
        section_cats = [k for k in cat_keys if k in categories]
        if not section_cats:
            continue

        section_children = []
        section_total = 0

        for cat_key in section_cats:
            cat = categories[cat_key]
            config = PATH_CONFIG.get(
                cat_key,
                {'icon': '📄', 'title': cat_key, 'color': section_color, 'fill': section_fill},
            )

            # Sort lessons within each bucket
            cat['lessons'].sort(key=lambda x: get_lesson_num(x['filename']))
            for sub_lessons in cat['subs'].values():
                sub_lessons.sort(key=lambda x: get_lesson_num(x['filename']))

            sub_content = []

            # Subcategories first (sorted)
            for sub_name, sub_lessons in sorted(cat['subs'].items()):
                lesson_topics = []
                for lesson in sub_lessons:
                    url = BASE_URL + lesson['filename']
                    lesson_title = lesson['title']
                    lv_display = lesson.get('level', '').upper()
                    level_style = LEVEL_COLORS.get(
                        lv_display, {'color': config['color'], 'fill': config['fill']},
                    )
                    if lv_display:
                        lesson_title += f" [{lv_display}]"

                    lesson_topics.append(make_topic(
                        lesson_title, level=3, link=url,
                        color=level_style['color'], fill=level_style['fill'],
                        shape='rounded-rect',
                    ))

                sub_topic = make_topic(
                    f"📂 {sub_name} ({len(sub_lessons)})",
                    level=2, children=''.join(lesson_topics),
                    color=config['color'], fill=config['fill'],
                    shape='rounded-rect',
                )
                sub_content.append(sub_topic)

            # Direct lessons (no subcategory)
            for lesson in cat['lessons']:
                url = BASE_URL + lesson['filename']
                lesson_title = lesson['title']
                lv_display = lesson.get('level', '').upper()
                level_style = LEVEL_COLORS.get(
                    lv_display, {'color': config['color'], 'fill': config['fill']},
                )
                if lv_display:
                    lesson_title += f" [{lv_display}]"

                sub_content.append(make_topic(
                    lesson_title, level=2, link=url,
                    color=level_style['color'], fill=level_style['fill'],
                    shape='rounded-rect',
                ))

            total = len(cat['lessons']) + sum(len(s) for s in cat['subs'].values())
            section_total += total

            # If section has only one category, flatten (don't nest)
            if len(section_cats) == 1:
                section_children = sub_content
            else:
                # Multiple courses in this section — nest under course name
                cat_title = f"{config['icon']} {config['title']} ({total})"
                section_children.append(make_topic(
                    cat_title, level=1, children=''.join(sub_content),
                    color=config['color'], fill=config['fill'],
                    shape='rounded-rect',
                ))

        section_xml.append(make_topic(
            f"{section_title} ({section_total})",
            level=1, children=''.join(section_children),
            color=section_color, fill=section_fill,
            shape='rounded-rect',
            position=side,
        ))

    # Root node
    total_lessons = sum(
        len(c['lessons']) + sum(len(s) for s in c['subs'].values())
        for c in categories.values()
    )
    root = make_topic(
        f"📖 Malcolm's Lessons ({total_lessons})",
        level=0, children=''.join(section_xml),
        color='667EEA', fill='E8EAFD',
        shape='rounded-rect', folded=False,
    )

    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<map version="1.0">
<xmap-content content-version="12" generator-name="Python build_mindmap.py" generator-version="4.0" timestamp="{now}">
{root}
</xmap-content>
</map>'''

    return xml, categories, skipped


# ---------------------------------------------------------------------------
# File creation
# ---------------------------------------------------------------------------
def create_itmz(xml_content, output_path):
    """Create an .itmz file (ZIP containing mapdata.xml)."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('mapdata.xml', xml_content.encode('utf-8'))

    os.makedirs(output_path.parent, exist_ok=True)
    with open(output_path, 'wb') as f:
        f.write(buffer.getvalue())

    return output_path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    """Build the mind map with a full categorisation report."""
    print(f"📖 Building Mind Map v4.0 (Website-Aligned) from {INDEX_FILE}")

    if not INDEX_FILE.exists():
        print(f"❌ Error: {INDEX_FILE} not found")
        return 1

    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        html_content = f.read()

    lessons = extract_lesson_data(html_content)
    print(f"✅ Found {len(lessons)} lessons")

    xml_content, categories, skipped = build_itmz_xml(lessons)

    # Print categorisation report
    print(f"\n{'─' * 60}")
    print(f"  CATEGORISATION REPORT (v4.0 — Website-Aligned)")
    print(f"{'─' * 60}")

    total = 0
    for cat_key in sorted(categories.keys(),
                          key=lambda x: PATH_CONFIG.get(x, {}).get('order', 99)):
        config = PATH_CONFIG.get(cat_key, {'icon': '📄', 'title': cat_key})
        count = (len(categories[cat_key]['lessons'])
                 + sum(len(s) for s in categories[cat_key]['subs'].values()))
        total += count
        print(f"  {config.get('icon', '📄')} {config.get('title', cat_key):40s} {count:>4d}")

        # Show subcategories
        for sub_name in sorted(categories[cat_key]['subs'].keys()):
            sub_count = len(categories[cat_key]['subs'][sub_name])
            print(f"      └─ {sub_name:36s} {sub_count:>4d}")

    print(f"{'─' * 60}")
    print(f"  Total categorised: {total}")
    print(f"  Skipped (utility): {skipped}")
    print(f"{'─' * 60}")

    # Warn about standalone/general lessons
    standalone = categories.get('standalone', {'lessons': [], 'subs': {}})
    general = standalone.get('subs', {}).get('900: General', [])
    if general:
        print(f"\n  ⚠️  {len(general)} lessons in Standalone > 900: General:")
        for l in general[:10]:
            print(f"      • {l['filename']} — {l['title']}")
        if len(general) > 10:
            print(f"      ... and {len(general) - 10} more")
        print(f"  Tip: Add keywords to _classify_topic() to categorise these\n")

    output = create_itmz(xml_content, OUTPUT_FILE)
    print(f"✅ Created {output}")
    print(f"📍 File size: {output.stat().st_size:,} bytes")

    return 0


if __name__ == "__main__":
    exit(main())
