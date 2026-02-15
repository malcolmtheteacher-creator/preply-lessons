#!/usr/bin/env python3
"""
Build Mind Map Script (v3.0 — Smart Categorisation)
Extracts lesson data from malcolm_lesson_index.html and generates an iThoughts (.itmz) file.

Categorisation strategy (layered, in priority order):
  1. Skip utility files (templates, trackers, etc.)
  2. Dashboards get their own branch
  3. Prefix-based course detection (a1p_, wp_, qf_, epicurean_, ois_, etc.)
  4. Series field from lesson metadata (fallback when prefix doesn't match)
  5. Filename keyword patterns (ielts, cambridge, speaking_naturally, etc.)
  6. Title/level heuristics for remaining lessons
  7. Anything truly uncategorised → "Standalone Lessons" grouped by level

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
# Category configuration — order controls mindmap layout
# ---------------------------------------------------------------------------
PATH_CONFIG = {
    # Core structured courses
    'grammar':       {'icon': '📚', 'title': 'Grammar Course (A2-C1)',     'order': 1,  'color': '4A90D9', 'fill': 'E8F4FD'},
    'a1_pathway':    {'icon': '🌱', 'title': 'A1 Pathway (Beginner)',      'order': 2,  'color': '27AE60', 'fill': 'E8FDF0'},
    'speaking_path': {'icon': '🎙️', 'title': 'Speaking Pathway (A2-C1)',   'order': 3,  'color': '00897B', 'fill': 'E0F2F1'},
    'speaking':      {'icon': '🗣️', 'title': 'Speaking Naturally',         'order': 4,  'color': '2ECC71', 'fill': 'EAFAF1'},
    'curious_conv':  {'icon': '💭', 'title': 'Curious Conversations',      'order': 5,  'color': 'E67E22', 'fill': 'FEF5E7'},
    'b2c1_conv':     {'icon': '💬', 'title': 'B2/C1 Conversations',        'order': 6,  'color': 'FF7043', 'fill': 'FBE9E7'},

    # Exam prep
    'ielts':         {'icon': '📝', 'title': 'IELTS Exam Prep',            'order': 7,  'color': 'D94A4A', 'fill': 'FDE8E8'},
    'cambridge':     {'icon': '🎓', 'title': 'Cambridge (CAE/CPE)',        'order': 8,  'color': '9B59B6', 'fill': 'F5EEF8'},
    'ote':           {'icon': '🏅', 'title': 'OTE Exam Prep',              'order': 9,  'color': 'AF7AC5', 'fill': 'F5EEF8'},

    # Specialist courses
    'quick_fix':     {'icon': '⚡', 'title': 'Quick Fix',                  'order': 10, 'color': 'E74C3C', 'fill': 'FDEDEC'},
    'philosophy':    {'icon': '🏛️', 'title': 'Philosophy Courses',         'order': 11, 'color': '8E44AD', 'fill': 'F4ECF7'},
    'history':       {'icon': '🏰', 'title': 'History Courses',            'order': 12, 'color': 'A0522D', 'fill': 'FBF0E6'},
    'memory':        {'icon': '🧠', 'title': 'Art of Memory',              'order': 13, 'color': '2980B9', 'fill': 'D6EAF8'},
    'professional':  {'icon': '💼', 'title': 'Professional English',       'order': 14, 'color': '34495E', 'fill': 'EBEDEF'},
    'writing':       {'icon': '✍️', 'title': 'Writing & Essay Skills',     'order': 15, 'color': '16A085', 'fill': 'E8F8F5'},
    'topics':        {'icon': '🌍', 'title': 'Topic-Based / Young Learners','order': 16, 'color': 'F39C12', 'fill': 'FEF9E7'},
    'news':          {'icon': '📰', 'title': 'Breaking News',              'order': 17, 'color': 'C0392B', 'fill': 'FDEDEC'},
    'teens':         {'icon': '🎮', 'title': 'Teens Course',               'order': 18, 'color': 'E91E63', 'fill': 'FCE4EC'},
    'rs':            {'icon': '🕊️', 'title': 'Religious Studies (KS3)',     'order': 19, 'color': '607D8B', 'fill': 'ECEFF1'},
    'academic':      {'icon': '🎓', 'title': 'Academic & IB English',      'order': 20, 'color': '5D6D7E', 'fill': 'EBF5FB'},

    # Utility & navigation
    'first_lessons': {'icon': '👋', 'title': 'First Lesson Assessments',   'order': 21, 'color': '1ABC9C', 'fill': 'E8F6F3'},
    'dashboards':    {'icon': '🎛️', 'title': 'Course Dashboards',          'order': 22, 'color': '8E44AD', 'fill': 'F4ECF7'},
    'tools':         {'icon': '🔧', 'title': 'Pronunciation & Grammar Tools','order': 23, 'color': '95A5A6', 'fill': 'F2F4F4'},

    # Catch-all
    'standalone':    {'icon': '🎯', 'title': 'Standalone Lessons',         'order': 24, 'color': '7F8C8D', 'fill': 'F2F3F4'},
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
# Smart categorisation engine
# ---------------------------------------------------------------------------
def categorize_lesson(filename, title, series='', level='', keywords=''):
    """
    Categorise a lesson using a layered strategy:
      1. Skip utility files
      2. Dashboards
      3. Prefix-based course matching (most reliable)
      4. Series field matching
      5. Filename keyword patterns
      6. Title/level heuristics
      7. Fallback → standalone (grouped by level)
    """
    fl = filename.lower()
    tl = title.lower()
    sl = series.lower().strip()
    lv = level.upper().strip()

    # ── 1. Skip utility / non-lesson files ─────────────────────────────────
    skip_patterns = [
        'template', 'tracker', 'quicknotes', 'bujo', 'kanban',
        'lifebalance', 'teleprompter', 'test_lesson_delete',
        'placeholder', 'website_with_tabs',
    ]
    if any(x in fl for x in skip_patterns):
        return None

    # ── 2. Dashboards ──────────────────────────────────────────────────────
    if 'dashboard' in fl:
        # Try to associate dashboards with their course
        if 'a1' in fl:
            return {'cat': 'dashboards', 'sub': 'A1 Pathway'}
        if 'grammar' in fl or 'lesson_' in fl:
            return {'cat': 'dashboards', 'sub': 'Grammar Course'}
        if 'ielts' in fl:
            return {'cat': 'dashboards', 'sub': 'IELTS'}
        if 'speaking_pathway' in fl or 'sp_' in fl:
            return {'cat': 'dashboards', 'sub': 'Speaking Pathway'}
        if 'speaking' in fl:
            return {'cat': 'dashboards', 'sub': 'Speaking Naturally'}
        if 'cambridge' in fl or 'cae' in fl or 'cpe' in fl:
            return {'cat': 'dashboards', 'sub': 'Cambridge'}
        if 'memory' in fl or 'art_of_memory' in fl:
            return {'cat': 'dashboards', 'sub': 'Art of Memory'}
        if 'philosophy' in fl or 'wp_' in fl:
            return {'cat': 'dashboards', 'sub': 'Philosophy'}
        if 'quick_fix' in fl or 'qf_' in fl:
            return {'cat': 'dashboards', 'sub': 'Quick Fix'}
        if 'professional' in fl or 'pss' in fl:
            return {'cat': 'dashboards', 'sub': 'Professional'}
        if 'teen' in fl:
            return {'cat': 'dashboards', 'sub': 'Teens'}
        if 'curious' in fl:
            return {'cat': 'dashboards', 'sub': 'Curious Conversations'}
        if 'news' in fl:
            return {'cat': 'dashboards', 'sub': 'Breaking News'}
        return {'cat': 'dashboards', 'sub': 'General'}

    # ── 3. Prefix-based course detection ───────────────────────────────────
    # This is the most reliable method: known filename prefixes → courses

    # A1 Pathway course
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

    # Speaking Pathway course (sp_ prefix — 75 lessons A2→C1 + prep packs)
    # Filename pattern: sp_[prep_]<level>_<num>_<topic>.html
    # Numbering: A2 (01-20), B1 (21-40), B2 (41-60), C1 (01-06 + 61-75)
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

    # B2/C1 Conversations (bc_ prefix)
    if fl.startswith('bc_'):
        return {'cat': 'b2c1_conv', 'sub': None}

    # Business Bootcamp (8 lessons — from business_bootcamp_dashboard)
    if fl.startswith('business-bootcamp') or fl.startswith('business_bootcamp'):
        if 'dashboard' not in fl:
            return {'cat': 'professional', 'sub': 'Business Bootcamp'}

    # Business Meetings (5 lessons — from business_meetings_dashboard)
    biz_meetings_files = [
        'closing_meetings_following_up', 'first_impressions_small_talk',
        'giving_opinions_suggestions', 'handling_questions_buying_time',
        'problems_and_solutions',
    ]
    if any(fl.startswith(f) for f in biz_meetings_files):
        return {'cat': 'professional', 'sub': 'Business Meeting Essentials'}

    # Quick Fix lessons (qf_ prefix)
    if fl.startswith('qf_'):
        if 'falsefriend' in fl or 'false_friend' in fl:
            # Sub-categorise by L1 language
            if 'french' in fl:
                return {'cat': 'quick_fix', 'sub': 'False Friends: French'}
            if 'italian' in fl:
                return {'cat': 'quick_fix', 'sub': 'False Friends: Italian'}
            if 'spanish' in fl:
                return {'cat': 'quick_fix', 'sub': 'False Friends: Spanish'}
            if 'german' in fl:
                return {'cat': 'quick_fix', 'sub': 'False Friends: German'}
            if 'portuguese' in fl:
                return {'cat': 'quick_fix', 'sub': 'False Friends: Portuguese'}
            if 'polish' in fl:
                return {'cat': 'quick_fix', 'sub': 'False Friends: Polish'}
            if 'turkish' in fl:
                return {'cat': 'quick_fix', 'sub': 'False Friends: Turkish'}
            if 'dutch' in fl:
                return {'cat': 'quick_fix', 'sub': 'False Friends: Dutch'}
            if 'czech' in fl:
                return {'cat': 'quick_fix', 'sub': 'False Friends: Czech'}
            if 'korean' in fl:
                return {'cat': 'quick_fix', 'sub': 'False Friends: Korean'}
            if 'japanese' in fl:
                return {'cat': 'quick_fix', 'sub': 'False Friends: Japanese'}
            if 'arabic' in fl:
                return {'cat': 'quick_fix', 'sub': 'False Friends: Arabic'}
            if 'russian' in fl:
                return {'cat': 'quick_fix', 'sub': 'False Friends: Russian'}
            return {'cat': 'quick_fix', 'sub': 'False Friends: Other'}
        if 'grammar' in fl:
            return {'cat': 'quick_fix', 'sub': 'Grammar Fixes'}
        if 'vocab' in fl:
            return {'cat': 'quick_fix', 'sub': 'Vocabulary Fixes'}
        if 'pronun' in fl:
            return {'cat': 'quick_fix', 'sub': 'Pronunciation Fixes'}
        return {'cat': 'quick_fix', 'sub': 'General Fixes'}

    # Western Philosophy course (wp_ prefix)
    if fl.startswith('wp_'):
        num = _extract_num(fl)
        if num <= 10:
            return {'cat': 'philosophy', 'sub': 'Western Philosophy: Ancient Greece (1-10)'}
        if num <= 20:
            return {'cat': 'philosophy', 'sub': 'Western Philosophy: Hellenistic & Roman (11-20)'}
        if num <= 30:
            return {'cat': 'philosophy', 'sub': 'Western Philosophy: Medieval (21-30)'}
        if num <= 40:
            return {'cat': 'philosophy', 'sub': 'Western Philosophy: Early Modern (31-40)'}
        return {'cat': 'philosophy', 'sub': 'Western Philosophy: Modern (41-50)'}

    # Epicurean course (epicurean_ prefix)
    if fl.startswith('epicurean_'):
        num = _extract_num(fl)
        if num <= 10:
            return {'cat': 'philosophy', 'sub': 'Epicurean: Foundations (1-10)'}
        if num <= 20:
            return {'cat': 'philosophy', 'sub': 'Epicurean: Deep Dives (11-20)'}
        return {'cat': 'philosophy', 'sub': 'Epicurean: Legacy & Influence (21+)'}

    # Stoicism
    if 'stoicism' in fl:
        return {'cat': 'philosophy', 'sub': 'Stoicism'}

    # Our Island Story / History (ois_ prefix)
    if fl.startswith('ois_'):
        num = _extract_num(fl)
        if num <= 10:
            return {'cat': 'history', 'sub': 'Our Island Story: Early Britain (1-10)'}
        if num <= 20:
            return {'cat': 'history', 'sub': 'Our Island Story: Medieval (11-20)'}
        return {'cat': 'history', 'sub': 'Our Island Story: Early Modern (21+)'}

    # Art of Memory course (lesson-XX-* pattern + memory keywords)
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

    # Memory-related standalone files
    if ('art-of-memory' in fl or 'art_of_memory' in fl or 'memory-books' in fl
            or 'bestiary' in fl or fl.startswith('dewey-')
            or fl.startswith('dewey_') or 'memory_lesson' in fl
            or 'memory_palace' in fl):
        if 'dewey' in fl:
            return {'cat': 'memory', 'sub': 'Dewey Memory Palace'}
        return {'cat': 'memory', 'sub': 'Resources & Guides'}

    # Religious Studies
    if fl.startswith('rs_'):
        return {'cat': 'rs', 'sub': None}

    # Professional Speaking Skills
    if fl.startswith('pss_'):
        return {'cat': 'professional', 'sub': 'Professional Speaking Skills'}

    # OTE exam prep
    if fl.startswith('ote_') or 'ote ' in tl:
        return {'cat': 'ote', 'sub': None}

    # Grammar Course (lesson_XX pattern — the original numbered series)
    match = re.match(r'lesson_(\d{2})', fl)
    if match:
        num = int(match.group(1))
        if num <= 10:
            return {'cat': 'grammar', 'sub': 'A2 - Elementary (1-10)'}
        if num <= 25:
            return {'cat': 'grammar', 'sub': 'B1 - Intermediate (11-25)'}
        if num <= 40:
            return {'cat': 'grammar', 'sub': 'B2 - Upper Intermediate (26-40)'}
        return {'cat': 'grammar', 'sub': 'C1 - Advanced (41-50)'}

    # General Grammar Course files
    if fl.startswith('general_lesson_'):
        return {'cat': 'grammar', 'sub': 'General Lessons'}

    # First lessons / assessments
    if 'first_lesson' in fl or 'diagnostic' in fl:
        return {'cat': 'first_lessons', 'sub': None}

    # ── 4. Series field matching ───────────────────────────────────────────
    if sl:
        if 'grammar' in sl:
            return {'cat': 'grammar', 'sub': 'From Series: Grammar'}
        if 'ielts' in sl:
            return {'cat': 'ielts', 'sub': 'From Series'}
        if 'speaking naturally' in sl:
            return {'cat': 'speaking', 'sub': 'From Series'}
        if 'curious conversation' in sl:
            return {'cat': 'curious_conv', 'sub': None}
        if 'cambridge' in sl:
            return {'cat': 'cambridge', 'sub': None}
        if 'beginner' in sl:
            return {'cat': 'a1_pathway', 'sub': 'From Series: Beginner'}
        if 'teen' in sl:
            return {'cat': 'teens', 'sub': None}
        if 'professional' in sl or 'business' in sl:
            return {'cat': 'professional', 'sub': None}

    # ── 5. Filename keyword patterns ───────────────────────────────────────

    # IELTS
    if 'ielts_lesson_' in fl and 'task_1' not in fl and 'reading' not in fl:
        return {'cat': 'ielts', 'sub': 'Writing Task 2'}
    if 'ielts_task_1' in fl or 'ielts_task1' in fl:
        return {'cat': 'ielts', 'sub': 'Writing Task 1'}
    if 'ielts_reading' in fl:
        return {'cat': 'ielts', 'sub': 'Reading'}
    if 'ielts_speaking' in fl:
        return {'cat': 'ielts', 'sub': 'Speaking'}
    if 'ielts' in fl:
        return {'cat': 'ielts', 'sub': 'Other Resources'}

    # Cambridge
    if 'cambridge' in fl or 'cae' in fl or 'cpe' in fl:
        return {'cat': 'cambridge', 'sub': None}

    # Speaking Naturally
    if 'speaking_naturally_teens' in fl:
        return {'cat': 'speaking', 'sub': 'Teens'}
    if 'speaking_naturally_advanced' in fl:
        return {'cat': 'speaking', 'sub': 'Advanced'}
    if 'speaking_naturally' in fl:
        return {'cat': 'speaking', 'sub': 'Adults'}
    if 'speaking_pathway' in fl:
        return {'cat': 'speaking', 'sub': 'Resources'}

    # Curious Conversations
    if 'curious_conversations' in fl or 'curious conversations' in tl:
        return {'cat': 'curious_conv', 'sub': None}

    # Professional
    prof_patterns = [
        'professional', 'business', 'interview', 'kuba',
        'presenting', 'workplace', 'leading', 'teams', 'meeting',
    ]
    if any(x in fl for x in prof_patterns):
        return {'cat': 'professional', 'sub': None}

    # Essay & Writing
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

    # Topic-based / young learners
    topic_patterns = [
        'dinosaur', 'space', 'ocean', 'egypt', 'greece', 'weather',
        'explorer', 'gaming', 'erebus', 'ww2', 'world_war', 'human_body',
        'ancient', 'comic_book', 'comic book', 'horse_riding', 'equestrian',
        'artemis', 'moon', 'path_of_titans', 'tennis',
    ]
    if any(x in fl for x in topic_patterns):
        return {'cat': 'topics', 'sub': None}

    # Levelled topic/conversation lessons (filename has level suffix like _b2c1, _c1)
    # These are standalone speaking/conversation lessons at a specific level
    if fl.startswith('explore_'):
        return {'cat': 'topics', 'sub': 'Explore Series'}
    if fl.startswith('skills_'):
        return {'cat': 'tools', 'sub': 'Skills Lessons'}
    if fl.startswith('grammar_'):
        return {'cat': 'grammar', 'sub': 'Grammar Topics'}
    if fl.startswith('general_listening_'):
        return {'cat': 'tools', 'sub': 'Listening Practice'}

    # Levelled conversation/topic lessons with b2c1 or c1c2 in filename
    if 'b2c1' in fl or 'c1c2' in fl:
        return {'cat': 'b2c1_conv', 'sub': None}
    # B1/B2 levelled topic conversations (suffix pattern)
    if fl.endswith('b1b2.html') or '_b1b2' in fl:
        return {'cat': 'b2c1_conv', 'sub': None}

    # New Year / Christmas / seasonal
    if 'christmas' in fl or 'new_year' in fl:
        return {'cat': 'topics', 'sub': 'Seasonal'}

    # Review sheets (associated with other lessons)
    if 'review_sheet' in fl or 'lesson_review' in fl:
        return {'cat': 'tools', 'sub': 'Review Sheets'}

    # Real Conversations series
    if 'real_conversations' in fl:
        return {'cat': 'curious_conv', 'sub': None}

    # Standalone topic lessons identifiable by title patterns
    if 'boredom' in fl or 'new_year_plans' in fl:
        return {'cat': 'curious_conv', 'sub': None}

    # Tools: pronunciation, grammar guides, tenses reference
    tool_patterns = [
        'pronunciation', 'tenses_guide', 'parts_of_speech',
        'past_participle', 'speed_reading', 'speaking-practice',
        'preply_screen_share', 'concorso',
    ]
    if any(x in fl for x in tool_patterns):
        return {'cat': 'tools', 'sub': None}

    # ── 6. A1 beginner detection (broader) ─────────────────────────────────
    if fl.startswith('a1_') or '_a1_' in fl or 'beginner' in fl:
        return {'cat': 'a1_pathway', 'sub': 'Standalone A1'}

    # ── 7. Dewey-style topic classification ─────────────────────────────
    # Instead of dumping remaining lessons into level buckets, classify by
    # TOPIC using title + filename keywords so that lessons on similar
    # subjects sit together — like a library shelf.
    topic = _classify_topic(fl, tl)

    # Detect level for the sub-label
    detected_level = lv
    if not detected_level:
        if '_a1' in fl or fl.endswith('a1.html') or fl.startswith('a1'):
            detected_level = 'A1'
        elif '_a2' in fl or fl.endswith('a2.html') or ' a2' in tl:
            detected_level = 'A2'
        elif 'b1b2' in fl or '_b1' in fl or ' b1' in tl:
            detected_level = 'B1'
        elif 'b2c1' in fl or '_b2' in fl or ' b2' in tl:
            detected_level = 'B2'
        elif '_c1' in fl or fl.endswith('c1.html') or ' c1' in tl:
            detected_level = 'C1'
        elif '_c2' in fl or fl.endswith('c2.html'):
            detected_level = 'C2'

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
      600 — Arts & Culture
      700 — Daily Life & Lifestyle
      800 — Work & Career
      900 — General / Unclassified
    """
    # Combine filename + title for matching (both already lowered)
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

    # ── 600: Arts & Culture ────────────────────────────────────────────
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
# XML / iThoughts generation  (unchanged logic, cleaner code)
# ---------------------------------------------------------------------------
def build_itmz_xml(lessons):
    """Build the XML content for the .itmz file with iThoughts styling."""
    # Categorise all lessons (now using full metadata)
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
                   color=None, fill=None, shape=None, folded=True):
        attrs = [f'text="{escape_xml(text)}"']
        if link:
            attrs.append(f'link="{escape_xml(link)}"')
        if color:
            attrs.append(f'color="#{color}"')
        if fill:
            attrs.append(f'fill-color="#{fill}"')
        if shape:
            attrs.append(f'shape="{shape}"')
        if level > 0 and folded:
            attrs.append('folded="1"')
        attrs.append(f'created="{now}"')
        attrs.append(f'modified="{now}"')
        attr_str = ' '.join(attrs)
        if children:
            return f'<topic {attr_str}>{children}</topic>'
        return f'<topic {attr_str}/>'

    # Build category topics
    category_xml = []

    for cat_key in sorted_cats:
        cat = categories[cat_key]
        config = PATH_CONFIG.get(
            cat_key,
            {'icon': '📄', 'title': cat_key, 'color': '7F8C8D', 'fill': 'F2F3F4'},
        )
        cat_title = f"{config['icon']} {config['title']}"

        # Sort lessons within each bucket
        cat['lessons'].sort(key=lambda x: get_lesson_num(x['filename']))
        for sub_lessons in cat['subs'].values():
            sub_lessons.sort(key=lambda x: get_lesson_num(x['filename']))

        sub_content = []

        # Subcategories first (sorted by name for consistency)
        for sub_name, sub_lessons in sorted(cat['subs'].items()):
            lesson_topics = []
            for lesson in sub_lessons:
                url = BASE_URL + lesson['filename']
                lesson_title = lesson['title']
                lv = lesson.get('level', '').upper()
                level_style = LEVEL_COLORS.get(
                    lv, {'color': config['color'], 'fill': config['fill']},
                )
                if lv:
                    lesson_title += f" [{lv}]"

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
            lv = lesson.get('level', '').upper()
            level_style = LEVEL_COLORS.get(
                lv, {'color': config['color'], 'fill': config['fill']},
            )
            if lv:
                lesson_title += f" [{lv}]"

            sub_content.append(make_topic(
                lesson_title, level=2, link=url,
                color=level_style['color'], fill=level_style['fill'],
                shape='rounded-rect',
            ))

        total = len(cat['lessons']) + sum(len(s) for s in cat['subs'].values())
        category_xml.append(make_topic(
            f"{cat_title} ({total})",
            level=1, children=''.join(sub_content),
            color=config['color'], fill=config['fill'],
            shape='rounded-rect',
        ))

    # Root node
    total_lessons = sum(
        len(c['lessons']) + sum(len(s) for s in c['subs'].values())
        for c in categories.values()
    )
    root = make_topic(
        f"📖 Malcolm's Lessons ({total_lessons})",
        level=0, children=''.join(category_xml),
        color='667EEA', fill='E8EAFD',
        shape='rounded-rect', folded=False,
    )

    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<map version="1.0">
<xmap-content content-version="12" generator-name="Python build_mindmap.py" generator-version="3.0" timestamp="{now}">
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
    print(f"📖 Building Mind Map from {INDEX_FILE}")

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
    print(f"  CATEGORISATION REPORT")
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

    # Warn about standalone/unlevelled lessons
    standalone = categories.get('standalone', {'lessons': [], 'subs': {}})
    unlevelled = standalone.get('subs', {}).get('Unlevelled', [])
    if unlevelled:
        print(f"\n  ⚠️  {len(unlevelled)} lessons in Standalone > Unlevelled:")
        for l in unlevelled[:10]:
            print(f"      • {l['filename']}")
        if len(unlevelled) > 10:
            print(f"      ... and {len(unlevelled) - 10} more")
        print(f"  Tip: Add a series or level to these in the lesson index\n")

    output = create_itmz(xml_content, OUTPUT_FILE)
    print(f"✅ Created {output}")
    print(f"📍 File size: {output.stat().st_size:,} bytes")

    return 0


if __name__ == "__main__":
    exit(main())
