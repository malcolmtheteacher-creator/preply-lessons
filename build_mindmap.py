#!/usr/bin/env python3
"""
Build Mind Map Script
Extracts lesson data from malcolm_lesson_index.html and generates an iThoughts (.itmz) file.

This script should be run from the gitsite directory after updating the lesson index.
The generated .itmz file is saved to the Assets folder.

Usage:
    python build_mindmap.py

Or run as part of your build process.
"""

import re
import json
import zipfile
import io
import os
from datetime import datetime
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
INDEX_FILE = SCRIPT_DIR / "malcolm_lesson_index.html"
OUTPUT_FILE = SCRIPT_DIR.parent / "Assets" / "Mind Maps" / "Malcolm_Lessons_Map.itmz"
BASE_URL = "https://malcolmtheteacher-creator.github.io/preply-lessons/"

def extract_lesson_data(html_content):
    """Extract the lessonData array from the HTML file."""
    # Find the lessonData array
    pattern = r'window\.lessonData\s*=\s*\[(.*?)\];'
    match = re.search(pattern, html_content, re.DOTALL)
    if not match:
        raise ValueError("Could not find lessonData in HTML file")

    data_str = match.group(1)

    # Parse each lesson object - FIXED: handle escaped quotes in all fields
    lessons = []
    # Match individual lesson objects with escaped quote support
    # Using (?:[^'\\]|\\.)* to match any char except ' and \, OR any escaped char
    lesson_pattern = r"\{\s*filename:\s*'((?:[^'\\]|\\.)*)'\s*,\s*title:\s*'((?:[^'\\]|\\.)*)'\s*,\s*level:\s*'((?:[^'\\]|\\.)*)'\s*,\s*series:\s*'((?:[^'\\]|\\.)*)'\s*,\s*keywords:\s*'((?:[^'\\]|\\.)*)'\s*\}"

    for m in re.finditer(lesson_pattern, data_str):
        lessons.append({
            'filename': m.group(1).replace("\\'", "'"),
            'title': m.group(2).replace("\\'", "'"),
            'level': m.group(3).replace("\\'", "'"),
            'series': m.group(4).replace("\\'", "'"),
            'keywords': m.group(5).replace("\\'", "'")
        })

    return lessons

def categorize_lesson(filename, title):
    """Categorize a lesson based on filename and title patterns."""
    fl = filename.lower()
    tl = title.lower()

    # Skip utility files
    skip_patterns = ['template', 'tracker', 'quicknotes', 'bujo', 'kanban', 'lifebalance', 'teleprompter']
    if any(x in fl for x in skip_patterns):
        return None

    # Dashboards
    if 'dashboard' in fl:
        return {'cat': 'dashboards', 'sub': None}

    # First lessons
    if 'first_lesson' in fl:
        return {'cat': 'first_lessons', 'sub': None}

    # A1 Beginner
    if fl.startswith('a1_') or '_a1_' in fl or 'beginner' in fl:
        return {'cat': 'by_level', 'sub': 'A1 - Beginner'}

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

    # Curious Conversations
    if 'curious_conversations' in fl:
        return {'cat': 'curious_conv', 'sub': None}

    # Grammar Course (numbered lessons)
    match = re.match(r'lesson_(\d{2})', fl)
    if match:
        num = int(match.group(1))
        if num <= 10:
            return {'cat': 'grammar', 'sub': 'A2 - Elementary (1-10)'}
        if num <= 25:
            return {'cat': 'grammar', 'sub': 'B1 - Intermediate (11-25)'}
        if num <= 40:
            return {'cat': 'grammar', 'sub': 'B2 - Upper Int (26-40)'}
        return {'cat': 'grammar', 'sub': 'C1 - Advanced (41-50)'}

    # Professional
    prof_patterns = ['professional', 'business', 'interview', 'kuba', 'presenting', 'workplace', 'leading', 'teams', 'meeting']
    if any(x in fl for x in prof_patterns):
        return {'cat': 'professional', 'sub': None}

    # Breaking News
    if 'breaking_news' in fl or 'spain_rail' in fl:
        return {'cat': 'news', 'sub': None}

    # Writing
    if 'writing' in fl and 'ielts' not in fl:
        return {'cat': 'writing', 'sub': None}

    # Topic-based (young learners themes)
    topic_patterns = ['dinosaur', 'space', 'ocean', 'egypt', 'greece', 'weather', 'explorer', 'gaming', 'erebus', 'ww2', 'world_war', 'human_body', 'ancient']
    if any(x in fl for x in topic_patterns):
        return {'cat': 'topics', 'sub': None}

    # By level from filename or title
    if '_a2' in fl or fl.endswith('a2.html') or ' a2' in tl:
        return {'cat': 'by_level', 'sub': 'A2 - Elementary'}
    if 'b1b2' in fl or '_b1' in fl or ' b1' in tl:
        return {'cat': 'by_level', 'sub': 'B1 - Intermediate'}
    if 'b2c1' in fl or '_b2' in fl:
        return {'cat': 'by_level', 'sub': 'B2 - Upper Intermediate'}
    if '_c1' in fl or fl.endswith('c1.html'):
        return {'cat': 'by_level', 'sub': 'C1 - Advanced'}

    return {'cat': 'other', 'sub': None}

# Category configuration with colors for iThoughts
# Colors are in hex format without #
PATH_CONFIG = {
    'grammar':       {'icon': '📚', 'title': 'Grammar Course (A2→C1)',    'order': 1,  'color': '4A90D9', 'fill': 'E8F4FD'},
    'ielts':         {'icon': '📝', 'title': 'IELTS Exam Prep',           'order': 2,  'color': 'D94A4A', 'fill': 'FDE8E8'},
    'cambridge':     {'icon': '🎓', 'title': 'Cambridge (CAE/CPE)',       'order': 3,  'color': '9B59B6', 'fill': 'F5EEF8'},
    'speaking':      {'icon': '🗣️', 'title': 'Speaking Naturally',        'order': 4,  'color': '27AE60', 'fill': 'E8FDF0'},
    'curious_conv':  {'icon': '💭', 'title': 'Curious Conversations',     'order': 5,  'color': 'E67E22', 'fill': 'FEF5E7'},
    'by_level':      {'icon': '📈', 'title': 'By Level',                  'order': 6,  'color': '3498DB', 'fill': 'EBF5FB'},
    'professional':  {'icon': '💼', 'title': 'Professional English',      'order': 7,  'color': '34495E', 'fill': 'EBEDEF'},
    'writing':       {'icon': '✍️', 'title': 'Writing Skills',            'order': 8,  'color': '16A085', 'fill': 'E8F8F5'},
    'topics':        {'icon': '🌍', 'title': 'Topic-Based Speaking',      'order': 9,  'color': 'F39C12', 'fill': 'FEF9E7'},
    'news':          {'icon': '📰', 'title': 'Breaking News',             'order': 10, 'color': 'C0392B', 'fill': 'FDEDEC'},
    'first_lessons': {'icon': '👋', 'title': 'First Lesson Assessments',  'order': 11, 'color': '1ABC9C', 'fill': 'E8F6F3'},
    'dashboards':    {'icon': '🎛️', 'title': 'Course Dashboards',         'order': 12, 'color': '8E44AD', 'fill': 'F4ECF7'},
    'other':         {'icon': '🎯', 'title': 'Other Lessons',             'order': 99, 'color': '7F8C8D', 'fill': 'F2F3F4'}
}

# Level colors for lesson badges
LEVEL_COLORS = {
    'A1': {'color': '27AE60', 'fill': 'E8FDF0'},  # Green
    'A2': {'color': '2ECC71', 'fill': 'EAFAF1'},  # Light green
    'B1': {'color': 'F39C12', 'fill': 'FEF9E7'},  # Orange
    'B2': {'color': 'E67E22', 'fill': 'FDF2E9'},  # Dark orange
    'C1': {'color': 'E74C3C', 'fill': 'FDEDEC'},  # Red
    'C2': {'color': '9B59B6', 'fill': 'F5EEF8'},  # Purple
}

def get_lesson_num(filename):
    """Extract lesson number for sorting."""
    match = re.search(r'lesson_(\d+)', filename, re.IGNORECASE)
    if match:
        return int(match.group(1))
    match = re.search(r'(\d+)', filename)
    if match:
        return int(match.group(1))
    return 999

def build_itmz_xml(lessons):
    """Build the XML content for the .itmz file with iThoughts styling."""
    # Categorize all lessons
    categories = {}
    for lesson in lessons:
        cat_info = categorize_lesson(lesson['filename'], lesson['title'])
        if not cat_info:
            continue

        cat = cat_info['cat']
        sub = cat_info['sub']

        if cat not in categories:
            categories[cat] = {'lessons': [], 'subs': {}}

        if sub:
            if sub not in categories[cat]['subs']:
                categories[cat]['subs'][sub] = []
            categories[cat]['subs'][sub].append(lesson)
        else:
            categories[cat]['lessons'].append(lesson)

    # Sort categories by order
    sorted_cats = sorted(categories.keys(), key=lambda x: PATH_CONFIG.get(x, {}).get('order', 99))

    # Build XML
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    def escape_xml(text):
        """Escape special XML characters."""
        return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&apos;')

    def make_topic(text, level=0, children="", link="", color=None, fill=None, shape=None, folded=True):
        """Create a topic XML element with iThoughts styling."""
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

        # Add timestamps for iThoughts
        attrs.append(f'created="{now}"')
        attrs.append(f'modified="{now}"')

        attr_str = ' '.join(attrs)

        if children:
            return f'<topic {attr_str}>{children}</topic>'
        else:
            return f'<topic {attr_str}/>'

    # Build category topics
    category_xml = []

    for cat_key in sorted_cats:
        cat = categories[cat_key]
        config = PATH_CONFIG.get(cat_key, {'icon': '📄', 'title': cat_key, 'color': '7F8C8D', 'fill': 'F2F3F4'})
        cat_title = f"{config['icon']} {config['title']}"

        # Sort lessons
        cat['lessons'].sort(key=lambda x: get_lesson_num(x['filename']))
        for sub_lessons in cat['subs'].values():
            sub_lessons.sort(key=lambda x: get_lesson_num(x['filename']))

        # Build subcategory content
        sub_content = []

        # Subcategories first
        for sub_name, sub_lessons in sorted(cat['subs'].items()):
            lesson_topics = []
            for lesson in sub_lessons:
                url = BASE_URL + lesson['filename']
                lesson_title = lesson['title']

                # Get level-specific color or use category color
                level = lesson.get('level', '').upper()
                level_style = LEVEL_COLORS.get(level, {'color': config['color'], 'fill': config['fill']})

                if level:
                    lesson_title += f" [{level}]"

                lesson_topics.append(make_topic(
                    lesson_title,
                    level=3,
                    link=url,
                    color=level_style['color'],
                    fill=level_style['fill'],
                    shape='rounded-rect'
                ))

            sub_topic = make_topic(
                f"📂 {sub_name} ({len(sub_lessons)})",
                level=2,
                children=''.join(lesson_topics),
                color=config['color'],
                fill=config['fill'],
                shape='rounded-rect'
            )
            sub_content.append(sub_topic)

        # Direct lessons (no subcategory)
        for lesson in cat['lessons']:
            url = BASE_URL + lesson['filename']
            lesson_title = lesson['title']

            level = lesson.get('level', '').upper()
            level_style = LEVEL_COLORS.get(level, {'color': config['color'], 'fill': config['fill']})

            if level:
                lesson_title += f" [{level}]"

            sub_content.append(make_topic(
                lesson_title,
                level=2,
                link=url,
                color=level_style['color'],
                fill=level_style['fill'],
                shape='rounded-rect'
            ))

        total_count = len(cat['lessons']) + sum(len(s) for s in cat['subs'].values())
        category_xml.append(make_topic(
            f"{cat_title} ({total_count})",
            level=1,
            children=''.join(sub_content),
            color=config['color'],
            fill=config['fill'],
            shape='rounded-rect'
        ))

    # Root topic with special styling
    total_lessons = sum(len(c['lessons']) + sum(len(s) for s in c['subs'].values()) for c in categories.values())
    root_content = ''.join(category_xml)
    root = make_topic(
        f"📖 Malcolm's Lessons ({total_lessons})",
        level=0,
        children=root_content,
        color='667EEA',
        fill='E8EAFD',
        shape='rounded-rect',
        folded=False
    )

    # Full XML document in iThoughts format
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<map version="1.0">
<xmap-content content-version="12" generator-name="Python build_mindmap.py" generator-version="2.0" timestamp="{now}">
{root}
</xmap-content>
</map>'''

    return xml

def create_itmz(xml_content, output_path):
    """Create an .itmz file (which is a ZIP containing mapdata.xml)."""
    # Create ZIP file in memory
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('mapdata.xml', xml_content.encode('utf-8'))

    # Write to file
    os.makedirs(output_path.parent, exist_ok=True)
    with open(output_path, 'wb') as f:
        f.write(buffer.getvalue())

    return output_path

def main():
    """Main function to build the mind map."""
    print(f"📖 Building Mind Map from {INDEX_FILE}")

    # Read the HTML file
    if not INDEX_FILE.exists():
        print(f"❌ Error: {INDEX_FILE} not found")
        return 1

    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Extract lesson data
    lessons = extract_lesson_data(html_content)
    print(f"✅ Found {len(lessons)} lessons")

    # Build XML
    xml_content = build_itmz_xml(lessons)

    # Create .itmz file
    output = create_itmz(xml_content, OUTPUT_FILE)
    print(f"✅ Created {output}")
    print(f"📍 File size: {output.stat().st_size:,} bytes")

    return 0

if __name__ == "__main__":
    exit(main())
