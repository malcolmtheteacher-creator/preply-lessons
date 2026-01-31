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

    # Parse each lesson object
    lessons = []
    # Match individual lesson objects
    lesson_pattern = r"\{\s*filename:\s*'([^']+)',\s*title:\s*'([^']*)',\s*level:\s*'([^']*)',\s*series:\s*'([^']*)',\s*keywords:\s*'([^']*)'\s*\}"

    for m in re.finditer(lesson_pattern, data_str):
        lessons.append({
            'filename': m.group(1),
            'title': m.group(2).replace("\\'", "'"),  # Unescape quotes
            'level': m.group(3),
            'series': m.group(4),
            'keywords': m.group(5)
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

# Category configuration
PATH_CONFIG = {
    'grammar': {'icon': '📚', 'title': 'Grammar Course (A2→C1)', 'order': 1},
    'ielts': {'icon': '📝', 'title': 'IELTS Exam Prep', 'order': 2},
    'cambridge': {'icon': '🎓', 'title': 'Cambridge (CAE/CPE)', 'order': 3},
    'speaking': {'icon': '🗣️', 'title': 'Speaking Naturally', 'order': 4},
    'curious_conv': {'icon': '💭', 'title': 'Curious Conversations', 'order': 5},
    'by_level': {'icon': '📈', 'title': 'By Level', 'order': 6},
    'professional': {'icon': '💼', 'title': 'Professional English', 'order': 7},
    'writing': {'icon': '✍️', 'title': 'Writing Skills', 'order': 8},
    'topics': {'icon': '🌍', 'title': 'Topic-Based Speaking', 'order': 9},
    'news': {'icon': '📰', 'title': 'Breaking News', 'order': 10},
    'first_lessons': {'icon': '👋', 'title': 'First Lesson Assessments', 'order': 11},
    'dashboards': {'icon': '🎛️', 'title': 'Course Dashboards', 'order': 12},
    'other': {'icon': '🎯', 'title': 'Other Lessons', 'order': 99}
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
    """Build the XML content for the .itmz file."""
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

    def make_topic(title, level=0, children="", link="", folded="true"):
        """Create a topic XML element."""
        link_attr = f' link="{escape_xml(link)}"' if link else ''
        fold_attr = f' folded="{folded}"' if level > 0 else ''
        return f'<topic text="{escape_xml(title)}"{link_attr}{fold_attr}>{children}</topic>'

    # Build category topics
    category_xml = []

    for cat_key in sorted_cats:
        cat = categories[cat_key]
        config = PATH_CONFIG.get(cat_key, {'icon': '📄', 'title': cat_key})
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
                if lesson['level']:
                    lesson_title += f" [{lesson['level']}]"
                lesson_topics.append(make_topic(lesson_title, level=3, link=url))

            sub_topic = make_topic(f"📂 {sub_name} ({len(sub_lessons)})", level=2,
                                  children=''.join(lesson_topics), folded="true")
            sub_content.append(sub_topic)

        # Direct lessons
        for lesson in cat['lessons']:
            url = BASE_URL + lesson['filename']
            lesson_title = lesson['title']
            if lesson['level']:
                lesson_title += f" [{lesson['level']}]"
            sub_content.append(make_topic(lesson_title, level=2, link=url))

        total_count = len(cat['lessons']) + sum(len(s) for s in cat['subs'].values())
        category_xml.append(make_topic(f"{cat_title} ({total_count})", level=1,
                                       children=''.join(sub_content), folded="true"))

    # Root topic
    total_lessons = sum(len(c['lessons']) + sum(len(s) for s in c['subs'].values()) for c in categories.values())
    root_content = ''.join(category_xml)
    root = make_topic(f"📖 Malcolm's Lessons ({total_lessons})", level=0, children=root_content)

    # Full XML document
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<map version="1.0">
<xmap-content content-version="12" generator-name="Python build_mindmap.py" generator-version="1.0" timestamp="{now}">
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
