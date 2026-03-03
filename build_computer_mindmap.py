#!/usr/bin/env python3
"""
Build User Files Mind Map (v2 — with smart grouping)
Generates an iThoughts (.itmz) mindmap of the entire user home directory.

Features:
  - 04_Media items grouped by type (Films, TV, Comics, Books, etc.)
  - gitsite summarised (has its own lesson mindmap)
  - Large flat folders grouped by file extension
  - Every node has a file:// link to the real macOS path
  - Branches alternate left/right
"""

import os
import re
import zipfile
import io
from datetime import datetime
from pathlib import Path
from collections import defaultdict
from urllib.parse import quote

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
HOME = Path("/Users/malcolmtheteacher")
OUTPUT = HOME / "Documents" / "01_Work" / "Assets" / "Mind Maps" / "User_Files_Map.itmz"
REAL_HOME = str(HOME)

# Top-level folders to skip entirely
SKIP_TOPLEVEL = {
    # Hidden / system
    '.Trash', '.android', '.dropbox', '.local', '.matplotlib',
    '.pdf-filler-profiles', '.skills', '.vscode', '.zsh_sessions',
    '.CFUserTextEncoding', '.DS_Store', '.zshrc', '.zsh_history',
    '.claude.json', '.claude',
    'Library',
    # macOS default folders that are empty or just system data
    'Movies',       # Just Apple TV library data
    'Music',        # Just Apple Music library data
    'Public',       # Empty Drop Box folder
    'Pictures',     # Photos library — not browsable content
}

# When a folder has more files than this, group by extension
SUMMARISE_THRESHOLD = 30

# Colour scheme for top-level folders
FOLDER_COLORS = {
    'Documents':    {'color': '2563EB', 'fill': 'DBEAFE', 'icon': '📂'},
    'Desktop':      {'color': '7C3AED', 'fill': 'EDE9FE', 'icon': '🖥️'},
    'Downloads':    {'color': '16A34A', 'fill': 'DCFCE7', 'icon': '⬇️'},
    'Applications': {'color': 'DC2626', 'fill': 'FEE2E2', 'icon': '📱'},
    'Scripts':      {'color': '009688', 'fill': 'E0F2F1', 'icon': '🔧'},
    'Ulysses':      {'color': '607D8B', 'fill': 'ECEFF1', 'icon': '✍️'},
    'Dropbox':      {'color': '2196F3', 'fill': 'E3F2FD', 'icon': '☁️'},
    'Google Drive': {'color': '4CAF50', 'fill': 'E8F5E9', 'icon': '☁️'},
}

DOC_COLORS = {
    '01_Work':          {'color': '2563EB', 'fill': 'DBEAFE', 'icon': '💼'},
    '02_Personal':      {'color': '7C3AED', 'fill': 'EDE9FE', 'icon': '🏠'},
    '03_Learning':      {'color': 'D97706', 'fill': 'FEF3C7', 'icon': '📖'},
    '04_Media':         {'color': 'DC2626', 'fill': 'FEE2E2', 'icon': '🎬'},
    '99_Temporary':     {'color': '9E9E9E', 'fill': 'F5F5F5', 'icon': '⏳'},
    'Paracosm_Project': {'color': '16A34A', 'fill': 'DCFCE7', 'icon': '🧠'},
    'WhisperNotes':     {'color': 'E91E63', 'fill': 'FCE4EC', 'icon': '🎙️'},
}

EXT_ICONS = {
    '.html': '🌐', '.py': '🐍', '.js': '📜', '.css': '🎨',
    '.md': '📝', '.txt': '📄', '.pdf': '📕', '.docx': '📘',
    '.xlsx': '📊', '.pptx': '📽️', '.json': '🔧', '.xml': '📋',
    '.png': '🖼️', '.jpg': '🖼️', '.jpeg': '🖼️', '.gif': '🖼️',
    '.svg': '🎨', '.mp4': '🎬', '.mkv': '🎬', '.avi': '🎬',
    '.mp3': '🎵', '.m4a': '🎵', '.m4b': '🎧', '.flac': '🎵',
    '.epub': '📚', '.cbr': '📚', '.cbz': '📚',
    '.zip': '📦', '.itmz': '🗺️', '.command': '⚙️', '.sh': '⚙️',
    '.app': '📱', '.bike': '📝',
}

# ── Media categorisation rules ──────────────────────────────────────────────
# Each rule: (category_name, icon, color, fill, match_function)
# match_function receives (name, full_path, is_dir, ext) → bool

VIDEO_EXTS = {'.mp4', '.mkv', '.avi', '.mov', '.wmv', '.m4v'}
AUDIO_EXTS = {'.mp3', '.m4a', '.m4b', '.flac', '.wav', '.ogg', '.aac'}
BOOK_EXTS = {'.epub', '.mobi', '.azw3', '.pdf'}
COMIC_EXTS = {'.cbr', '.cbz'}
IMAGE_EXTS = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.tiff'}

TV_PATTERNS = [
    r'S\d{2}', r'Season', r'Series',  # S01, Season 1
]

def _is_tv(name):
    return any(re.search(p, name, re.IGNORECASE) for p in TV_PATTERNS)

def _is_film(name, ext):
    """Detect films: video files or folders with year + resolution patterns."""
    film_patterns = [
        r'\(\d{4}\)',       # (2024)
        r'\b\d{4}\b.*1080p', r'\b\d{4}\b.*720p', r'\b\d{4}\b.*WEB',
        r'WEBRip', r'BluRay', r'DVDRip', r'IMAX',
    ]
    return (ext in VIDEO_EXTS or
            any(re.search(p, name, re.IGNORECASE) for p in film_patterns))

def categorise_media_item(name, full_path, is_dir):
    """Categorise a single item in 04_Media into a group."""
    nl = name.lower()
    ext = Path(name).suffix.lower()

    # ── TV Series (check before films — TV patterns override) ────────
    if _is_tv(name) and not 'film' in nl:
        return 'tv_series'

    # ── Films & Movies ───────────────────────────────────────────────
    if _is_film(name, ext) and not _is_tv(name):
        return 'films'

    # ── Comic Books & Graphic Novels ─────────────────────────────────
    comic_kw = ['comic', 'surfer', 'sandman', 'tintin', 'herge',
                'mort', 'matrix comics', 'hitchhiker', 'death',
                'graphic novel']
    if ext in COMIC_EXTS or any(k in nl for k in comic_kw):
        return 'comics'

    # ── Audiobooks ───────────────────────────────────────────────────
    audiobook_kw = ['audiobook', 'audio book', 'collection']
    if (any(k in nl for k in audiobook_kw) or
            (is_dir and ext == '' and 'm4b' in nl)):
        return 'audiobooks'
    if ext == '.m4b':
        return 'audiobooks'

    # ── Philosophy / Intellectual ────────────────────────────────────
    phil_kw = ['watts', 'philosophy', 'epicurus', 'stoic', 'marcus aurelius',
               'ancient rome', 'spqr', 'roman emperor', 'rule of law']
    if any(k in nl for k in phil_kw):
        return 'philosophy'

    # ── Books & eBooks ───────────────────────────────────────────────
    book_kw = ['dune', 'discworld', 'pratchett', 'orwell', 'bauer',
               'pagels', 'learn python', 'chatgpt', 'dummies',
               'bbc classics', 'egypt']
    if ext in BOOK_EXTS or any(k in nl for k in book_kw):
        return 'books'

    # ── Teaching Resources (audio for lessons) ───────────────────────
    teach_kw = ['ic_b1', 'ic_b2', 'ic_c1', 'le_listening', 'thorsten',
                'teaching method', 'transcript', 'elevator pitch']
    if any(k in nl for k in teach_kw):
        return 'teaching'

    # ── Games / ROMs ─────────────────────────────────────────────────
    if 'game' in nl or 'rom' in nl:
        return 'games'

    # ── Projects / Apps ──────────────────────────────────────────────
    proj_kw = ['lifebalance', 'simplemind', 'profile picture',
               'st benedict', 'calibre', 'loaded', 'media library']
    if any(k in nl for k in proj_kw):
        return 'projects'

    # ── Music / Audio (loose mp3s etc.) ──────────────────────────────
    if ext in AUDIO_EXTS:
        return 'audio'

    # ── Images ───────────────────────────────────────────────────────
    if ext in IMAGE_EXTS:
        return 'images'

    # ── Fallback ─────────────────────────────────────────────────────
    return 'other'


MEDIA_CATEGORIES = {
    'films':      {'icon': '🎬', 'title': 'Films & Movies',          'color': 'B91C1C', 'fill': 'FEE2E2', 'order': 1},
    'tv_series':  {'icon': '📺', 'title': 'TV Series',               'color': '92400E', 'fill': 'FEF3C7', 'order': 2},
    'comics':     {'icon': '💥', 'title': 'Comics & Graphic Novels', 'color': '7C3AED', 'fill': 'EDE9FE', 'order': 3},
    'books':      {'icon': '📚', 'title': 'Books & eBooks',          'color': '1E40AF', 'fill': 'DBEAFE', 'order': 4},
    'audiobooks': {'icon': '🎧', 'title': 'Audiobooks',              'color': '065F46', 'fill': 'D1FAE5', 'order': 5},
    'philosophy': {'icon': '🏛️', 'title': 'Philosophy & History',    'color': '78350F', 'fill': 'FEF3C7', 'order': 6},
    'teaching':   {'icon': '🎓', 'title': 'Teaching Resources',      'color': '1D4ED8', 'fill': 'DBEAFE', 'order': 7},
    'games':      {'icon': '🎮', 'title': 'Games & ROMs',            'color': '059669', 'fill': 'D1FAE5', 'order': 8},
    'audio':      {'icon': '🎵', 'title': 'Music & Audio',           'color': 'DB2777', 'fill': 'FCE7F3', 'order': 9},
    'images':     {'icon': '🖼️', 'title': 'Images',                  'color': 'D97706', 'fill': 'FEF3C7', 'order': 10},
    'projects':   {'icon': '🔧', 'title': 'Projects & Tools',        'color': '475569', 'fill': 'F1F5F9', 'order': 11},
    'other':      {'icon': '📁', 'title': 'Other',                   'color': '6B7280', 'fill': 'F3F4F6', 'order': 99},
}

# ── Special folder handling ─────────────────────────────────────────────────
# Folders that should be summarised with a single node rather than expanded
SUMMARY_FOLDERS = {
    'gitsite': '🌐 Lesson Site — 1,100+ HTML lessons (see Lesson Mindmap)',
}

now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def to_file_url(sandbox_path):
    rel = os.path.relpath(sandbox_path, HOME)
    real_path = os.path.join(REAL_HOME, rel)
    return "file://" + quote(real_path, safe='/:@')


def escape_xml(text):
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&apos;'))


def human_size(nbytes):
    if nbytes < 1024:
        return f"{nbytes} B"
    for unit in ['KB', 'MB', 'GB', 'TB']:
        nbytes /= 1024
        if nbytes < 1024:
            return f"{nbytes:.1f} {unit}"
    return f"{nbytes:.1f} PB"


def get_dir_stats(path):
    count = 0
    total = 0
    try:
        for root, dirs, files in os.walk(path, followlinks=False):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for f in files:
                if f.startswith('.'):
                    continue
                count += 1
                try:
                    total += os.path.getsize(os.path.join(root, f))
                except OSError:
                    pass
    except PermissionError:
        pass
    return count, total


def get_ext_icon(filename):
    ext = Path(filename).suffix.lower()
    return EXT_ICONS.get(ext, '📄')


def make_topic(text, level=0, children="", link="",
               color=None, fill=None, shape=None, folded=True,
               position=None, note=None):
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

    inner = ''
    if note:
        inner += f'<note>{escape_xml(note)}</note>'
    inner += children

    if inner:
        return f'<topic {attr_str}>{inner}</topic>'
    return f'<topic {attr_str}/>'


def should_skip(name, is_toplevel=False):
    if name.startswith('.'):
        return True
    if is_toplevel and name in SKIP_TOPLEVEL:
        return True
    if name.endswith('.photoslibrary') or name.endswith('.musiclibrary') or name.endswith('.tvlibrary'):
        return True
    return False


# ---------------------------------------------------------------------------
# Build media folder with smart grouping
# ---------------------------------------------------------------------------
def build_media_xml(media_path, level=2, color=None, fill=None):
    """Build XML for 04_Media with items grouped by category."""
    groups = defaultdict(list)  # cat_key → [(name, full_path, is_dir)]

    try:
        entries = sorted(os.listdir(media_path))
    except PermissionError:
        return ''

    for name in entries:
        if name.startswith('.'):
            continue
        full = os.path.join(media_path, name)
        if os.path.islink(full):
            continue
        is_dir = os.path.isdir(full)
        cat = categorise_media_item(name, full, is_dir)
        groups[cat].append((name, full, is_dir))

    children_xml = []
    sorted_cats = sorted(groups.keys(),
                         key=lambda c: MEDIA_CATEGORIES.get(c, {}).get('order', 99))

    for cat_key in sorted_cats:
        items = groups[cat_key]
        cat_cfg = MEDIA_CATEGORIES.get(cat_key, MEDIA_CATEGORIES['other'])

        item_nodes = []
        for name, full, is_dir in sorted(items, key=lambda x: x[0].lower()):
            icon = get_ext_icon(name) if not is_dir else '📁'
            count, size = get_dir_stats(full) if is_dir else (0, 0)

            if is_dir:
                if count > 0:
                    label = f"{icon} {name} ({count} files, {human_size(size)})"
                else:
                    label = f"{icon} {name}"
            else:
                try:
                    fsize = os.path.getsize(full)
                    label = f"{get_ext_icon(name)} {name} ({human_size(fsize)})"
                except OSError:
                    label = f"{get_ext_icon(name)} {name}"

            item_nodes.append(make_topic(
                label, level=level + 1, link=to_file_url(full),
                color=cat_cfg['color'], fill=cat_cfg['fill'],
                shape='rounded-rect',
            ))

        # Category branch
        cat_label = f"{cat_cfg['icon']} {cat_cfg['title']} ({len(items)})"
        children_xml.append(make_topic(
            cat_label, level=level, children=''.join(item_nodes),
            link=to_file_url(media_path),
            color=cat_cfg['color'], fill=cat_cfg['fill'],
            shape='rounded-rect',
        ))

    total_count, total_size = get_dir_stats(media_path)
    return make_topic(
        f"🎬 04_Media ({total_count} files, {human_size(total_size)})",
        level=level, children=''.join(children_xml),
        link=to_file_url(media_path),
        color=color or 'DC2626', fill=fill or 'FEE2E2',
        shape='rounded-rect',
    )


# ---------------------------------------------------------------------------
# Build a large-file folder grouped by extension
# ---------------------------------------------------------------------------
def build_grouped_folder_xml(folder_path, level=2, color=None, fill=None,
                             max_individual=20):
    """
    For folders with many files (like gitsite), group by extension
    and show individual files only for small groups.
    """
    folder_name = os.path.basename(folder_path)

    try:
        entries = sorted(os.listdir(folder_path))
    except PermissionError:
        return ''

    dirs = []
    files = []
    for e in entries:
        if e.startswith('.'):
            continue
        full = os.path.join(folder_path, e)
        if os.path.islink(full):
            continue
        if os.path.isdir(full):
            dirs.append(e)
        elif os.path.isfile(full):
            files.append(e)

    children_xml = []

    # Subdirectories first
    for d in dirs:
        full = os.path.join(folder_path, d)
        if d == '.git':
            children_xml.append(make_topic(
                "📦 .git (repository)", level=level + 1,
                link=to_file_url(full),
                color='6B7280', fill='F3F4F6', shape='rounded-rect',
            ))
            continue
        if d.endswith('.app'):
            children_xml.append(make_topic(
                f"📱 {d}", level=level + 1,
                link=to_file_url(full),
                color=color, fill=fill, shape='rounded-rect',
            ))
            continue

        # Recurse into subdirectories (but use grouped if large)
        sub_count, _ = get_dir_stats(full)
        if sub_count > SUMMARISE_THRESHOLD:
            sub_xml = build_grouped_folder_xml(
                full, level=level + 1, color=color, fill=fill,
            )
        else:
            sub_xml = build_folder_xml(
                full, level=level + 1, max_depth=5,
                color=color, fill=fill,
            )
        if sub_xml:
            children_xml.append(sub_xml)

    # Group files by extension
    if len(files) > max_individual:
        ext_groups = defaultdict(list)
        for f in files:
            ext = Path(f).suffix.lower() or '(no ext)'
            ext_groups[ext].append(f)

        for ext, ext_files in sorted(ext_groups.items(), key=lambda x: -len(x[1])):
            icon = EXT_ICONS.get(ext, '📄')
            total_size = sum(
                os.path.getsize(os.path.join(folder_path, f))
                for f in ext_files
                if os.path.exists(os.path.join(folder_path, f))
            )

            # If small group, list files individually inside the extension node
            if len(ext_files) <= max_individual:
                file_nodes = []
                for f in sorted(ext_files):
                    fp = os.path.join(folder_path, f)
                    try:
                        sz = human_size(os.path.getsize(fp))
                    except OSError:
                        sz = ''
                    file_nodes.append(make_topic(
                        f"{icon} {f} ({sz})" if sz else f"{icon} {f}",
                        level=level + 2, link=to_file_url(fp),
                        color=color, fill=fill, shape='rounded-rect',
                    ))
                children_xml.append(make_topic(
                    f"{icon} {len(ext_files)} {ext} files ({human_size(total_size)})",
                    level=level + 1, children=''.join(file_nodes),
                    link=to_file_url(folder_path),
                    color=color, fill=fill, shape='rounded-rect',
                ))
            else:
                children_xml.append(make_topic(
                    f"{icon} {len(ext_files)} {ext} files ({human_size(total_size)})",
                    level=level + 1, link=to_file_url(folder_path),
                    color=color, fill=fill, shape='rounded-rect',
                ))
    else:
        # Small enough to list individually
        for f in files:
            fp = os.path.join(folder_path, f)
            icon = get_ext_icon(f)
            try:
                size = human_size(os.path.getsize(fp))
                label = f"{icon} {f} ({size})"
            except OSError:
                label = f"{icon} {f}"
            children_xml.append(make_topic(
                label, level=level + 1, link=to_file_url(fp),
                color=color, fill=fill, shape='rounded-rect',
            ))

    total = len(dirs) + len(files)
    return make_topic(
        f"📁 {folder_name} ({total})",
        level=level, children=''.join(children_xml),
        link=to_file_url(folder_path),
        color=color, fill=fill, shape='rounded-rect',
    )


# ---------------------------------------------------------------------------
# Standard folder builder (for smaller folders)
# ---------------------------------------------------------------------------
def build_folder_xml(folder_path, level=1, max_depth=6, color=None, fill=None,
                     parent_is_media=False):
    """Recursively build XML for a folder."""
    if level > max_depth:
        count, size = get_dir_stats(folder_path)
        if count > 0:
            return make_topic(
                f"... {count} more files ({human_size(size)})",
                level=level, link=to_file_url(folder_path),
                color=color, fill=fill, shape='rounded-rect',
            )
        return ''

    try:
        entries = sorted(os.listdir(folder_path))
    except PermissionError:
        return make_topic(
            "🔒 (access denied)", level=level,
            color='9E9E9E', fill='F5F5F5', shape='rounded-rect',
        )

    dirs = []
    files = []
    for e in entries:
        if should_skip(e):
            continue
        full = os.path.join(folder_path, e)
        if os.path.islink(full):
            continue
        if os.path.isdir(full):
            dirs.append(e)
        elif os.path.isfile(full):
            files.append(e)

    folder_name = os.path.basename(folder_path)

    # .git — single node
    if folder_name == '.git':
        return make_topic(
            "📦 .git (repository)", level=level,
            link=to_file_url(folder_path),
            color='6B7280', fill='F3F4F6', shape='rounded-rect',
        )

    # .app bundles
    if folder_name.endswith('.app'):
        return make_topic(
            f"📱 {folder_name}", level=level,
            link=to_file_url(folder_path),
            color=color, fill=fill, shape='rounded-rect',
        )

    # Library bundles
    for ext in ['.photoslibrary', '.musiclibrary', '.tvlibrary',
                '.localized', '.conjureDesktop']:
        if folder_name.endswith(ext):
            count, size = get_dir_stats(folder_path)
            return make_topic(
                f"📦 {folder_name} ({count} items, {human_size(size)})",
                level=level, link=to_file_url(folder_path),
                color=color, fill=fill, shape='rounded-rect',
            )

    # Large folder → use grouped builder
    total_items = len(dirs) + len(files)
    if len(files) > SUMMARISE_THRESHOLD:
        return build_grouped_folder_xml(
            folder_path, level=level, color=color, fill=fill,
        )

    # Normal folder — list contents
    children_xml = []

    for d in dirs:
        full = os.path.join(folder_path, d)
        if d == '.git':
            children_xml.append(make_topic(
                "📦 .git (repository)", level=level + 1,
                link=to_file_url(full),
                color='6B7280', fill='F3F4F6', shape='rounded-rect',
            ))
            continue
        if d.endswith('.app'):
            children_xml.append(make_topic(
                f"📱 {d}", level=level + 1,
                link=to_file_url(full),
                color=color, fill=fill, shape='rounded-rect',
            ))
            continue

        sub_xml = build_folder_xml(
            full, level=level + 1, max_depth=max_depth,
            color=color, fill=fill,
        )
        if sub_xml:
            children_xml.append(sub_xml)

    for f in files:
        fp = os.path.join(folder_path, f)
        icon = get_ext_icon(f)
        try:
            size = os.path.getsize(fp)
            size_str = f" ({human_size(size)})"
        except OSError:
            size_str = ""
        children_xml.append(make_topic(
            f"{icon} {f}{size_str}", level=level + 1,
            link=to_file_url(fp),
            color=color, fill=fill, shape='rounded-rect',
        ))

    count = len(dirs) + len(files)
    return make_topic(
        f"📁 {folder_name} ({count})",
        level=level, children=''.join(children_xml),
        link=to_file_url(folder_path),
        color=color, fill=fill, shape='rounded-rect',
    )


# ---------------------------------------------------------------------------
# Main mindmap builder
# ---------------------------------------------------------------------------
def build_mindmap():
    print(f"🗺️  Building User Files Mind Map v2 (Smart Grouping) from {HOME}")

    entries = sorted(os.listdir(HOME))
    section_xml = []
    idx = 0

    visible_dirs = []
    visible_files = []
    symlinks = []

    for e in entries:
        if should_skip(e, is_toplevel=True):
            continue
        full = os.path.join(HOME, e)
        if os.path.islink(full):
            symlinks.append(e)
        elif os.path.isdir(full):
            visible_dirs.append(e)
        elif os.path.isfile(full):
            visible_files.append(e)

    for d in visible_dirs:
        full = os.path.join(HOME, d)
        style = FOLDER_COLORS.get(d, {'color': '6B7280', 'fill': 'F3F4F6', 'icon': '📁'})
        side = 'right' if idx % 2 == 0 else 'left'
        count, size = get_dir_stats(full)

        print(f"  {style['icon']} {d}: {count} files, {human_size(size)}")

        if d == 'Documents':
            doc_children = []
            try:
                doc_entries = sorted(os.listdir(full))
            except PermissionError:
                doc_entries = []

            for de in doc_entries:
                if de.startswith('.'):
                    continue
                de_full = os.path.join(full, de)
                if not os.path.isdir(de_full) and not os.path.isfile(de_full):
                    continue

                doc_style = DOC_COLORS.get(de, style)

                # ── Special: 04_Media → smart categorisation ──────────
                if de == '04_Media' and os.path.isdir(de_full):
                    media_xml = build_media_xml(
                        de_full, level=2,
                        color=doc_style.get('color', style['color']),
                        fill=doc_style.get('fill', style['fill']),
                    )
                    if media_xml:
                        doc_children.append(media_xml)
                    continue

                if os.path.isdir(de_full):
                    # Check for special summary folders inside 01_Work
                    sub_xml = build_folder_xml(
                        de_full, level=2, max_depth=5,
                        color=doc_style.get('color', style['color']),
                        fill=doc_style.get('fill', style['fill']),
                    )
                    if sub_xml:
                        doc_children.append(sub_xml)
                else:
                    icon = get_ext_icon(de)
                    try:
                        fsize = os.path.getsize(de_full)
                        size_str = f" ({human_size(fsize)})"
                    except OSError:
                        size_str = ""
                    doc_children.append(make_topic(
                        f"{icon} {de}{size_str}",
                        level=2, link=to_file_url(de_full),
                        color=style['color'], fill=style['fill'],
                        shape='rounded-rect',
                    ))

            section_xml.append(make_topic(
                f"{style['icon']} {d} ({count} files, {human_size(size)})",
                level=1, children=''.join(doc_children),
                link=to_file_url(full),
                color=style['color'], fill=style['fill'],
                shape='rounded-rect', position=side,
            ))
        else:
            folder_xml = build_folder_xml(
                full, level=2, max_depth=5,
                color=style['color'], fill=style['fill'],
            )
            children_xml = folder_xml if folder_xml else ''

            section_xml.append(make_topic(
                f"{style['icon']} {d} ({count} files, {human_size(size)})",
                level=1, children=children_xml,
                link=to_file_url(full),
                color=style['color'], fill=style['fill'],
                shape='rounded-rect', position=side,
            ))

        idx += 1

    # Cloud storage
    if symlinks:
        link_children = []
        for s in symlinks:
            s_full = os.path.join(HOME, s)
            st = FOLDER_COLORS.get(s, {'color': '6B7280', 'fill': 'F3F4F6', 'icon': '☁️'})
            link_children.append(make_topic(
                f"{st['icon']} {s} (cloud link)",
                level=2, link=to_file_url(s_full),
                color=st['color'], fill=st['fill'], shape='rounded-rect',
            ))

        side = 'right' if idx % 2 == 0 else 'left'
        section_xml.append(make_topic(
            f"☁️ Cloud Storage ({len(symlinks)})",
            level=1, children=''.join(link_children),
            color='2196F3', fill='E3F2FD',
            shape='rounded-rect', position=side,
        ))
        idx += 1

    # Root-level files
    if visible_files:
        file_children = []
        for f in visible_files:
            f_full = os.path.join(HOME, f)
            icon = get_ext_icon(f)
            try:
                fsize = os.path.getsize(f_full)
                size_str = f" ({human_size(fsize)})"
            except OSError:
                size_str = ""
            file_children.append(make_topic(
                f"{icon} {f}{size_str}",
                level=2, link=to_file_url(f_full),
                color='6B7280', fill='F3F4F6', shape='rounded-rect',
            ))

        side = 'right' if idx % 2 == 0 else 'left'
        section_xml.append(make_topic(
            f"📄 Root Files ({len(visible_files)})",
            level=1, children=''.join(file_children),
            color='6B7280', fill='F3F4F6',
            shape='rounded-rect', position=side,
        ))

    # Total stats
    total_files = 0
    for d in visible_dirs:
        full = os.path.join(HOME, d)
        c, _ = get_dir_stats(full)
        total_files += c
    total_files += len(visible_files)

    root = make_topic(
        f"🏠 malcolmtheteacher ({total_files:,} files)",
        level=0, children=''.join(section_xml),
        link=to_file_url(str(HOME)),
        color='667EEA', fill='E8EAFD',
        shape='rounded-rect', folded=False,
    )

    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<map version="1.0">
<xmap-content content-version="12" generator-name="Python build_user_mindmap.py" generator-version="2.0" timestamp="{now}">
{root}
</xmap-content>
</map>'''

    return xml


def create_itmz(xml_content, output_path):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('mapdata.xml', xml_content.encode('utf-8'))

    os.makedirs(output_path.parent, exist_ok=True)
    with open(output_path, 'wb') as f:
        f.write(buffer.getvalue())
    return output_path


def main():
    xml = build_mindmap()
    output = create_itmz(xml, OUTPUT)
    print(f"\n✅ Created {output}")
    print(f"📍 File size: {output.stat().st_size:,} bytes")
    return 0


if __name__ == "__main__":
    exit(main())
