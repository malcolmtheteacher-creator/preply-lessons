#!/usr/bin/env python3
"""Reorder the flat dashboards into grouped sections.

Everyday Echoes, Modern Life and English at Work were single lists of 25-30
cards. This regroups each one under headings, in the same style as the Life in
English dashboard, without touching the cards themselves.

Run again after adding lessons — any lesson not listed below is collected into
a final "More" section rather than being silently dropped.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent

PLANS = {
    "everyday_echoes_dashboard.html": [
        ("🚉", "Getting around", "Stations, airports, taxis and finding your way.",
         ["At the Museum", "At the Airport", "At the Train Station", "Taking a Taxi",
          "Asking for Directions", "Buying Tickets for a Show"]),
        ("🍽️", "Eating, shopping and spending", "Ordering, choosing, returning and haggling.",
         ["Ordering at a Café", "At the Restaurant", "Buying Clothes", "Haggling at a Market",
          "Planning a Holiday"]),
        ("🩺", "Looking after yourself", "Doctors, chemists, the gym and the hairdresser's.",
         ["At the Doctor's", "At the Pharmacy", "At the Vet", "Joining a Gym",
          "At the Hairdresser's"]),
        ("🧾", "Sorting something out", "Banks, complaints, repairs and paperwork.",
         ["At the Bank", "Making a Complaint", "Reporting Something Lost", "Car Trouble",
          "Checking into a Hotel", "At the Library", "Renting a Flat"]),
        ("💬", "Getting on with people", "Small talk, invitations, and the neighbours.",
         ["Talking About the Weather", "Talking About Sport", "A Wedding Invitation",
          "A Noisy Neighbour", "A Leaving Party"]),
        ("💼", "Work", "The interview, and the first day.",
         ["A Job Interview", "First Day at Work"]),
    ],
    "modern_life_dashboard.html": [
        ("📱", "Screens and the group chat", "Phones, posts, and the people in the thread.",
         ["The Group Chat", "The Screen-Time Talk", "A Photo of You", "The Comparison Trap",
          "The Thing You Shared", "The Comment Row", "The Group Admin"]),
        ("🛡️", "Not being taken for a ride", "Scams, sellers, refunds and standing your ground.",
         ["The Scam Call", "The Bad Seller", "The Café Poster", "The Review They Want Down",
          "The Delivery Gone Wrong", "The AI Mistake"]),
        ("🫂", "Being a good friend", "Turning up, saying sorry, telling the truth.",
         ["Back in Touch", "Bad News", "The Apology", "The Honest Review", "The Collab"]),
        ("💷", "Money between friends", "The awkward conversations about who pays.",
         ["The Holiday Budget", "The Money You Lent", "The Big Favour"]),
        ("🏠", "Sharing a space", "One table, two people — and the flat next door.",
         ["Working From Home", "The Neighbour's Noise"]),
        ("💻", "Meeting people online", "First calls, and when the technology fails you.",
         ["The First Phone Call", "The Frozen Interview"]),
    ],
    "english_at_work_dashboard.html": [
        ("🗣️", "In the room", "Meetings, presentations and working a crowd.",
         ["Speaking Up in the Meeting", "Chairing the Meeting", "The Presentation",
          "Working the Room"]),
        ("📈", "Asking for what you want", "Cases, deals, reviews and credit.",
         ["Asking to Work From Home", "Negotiating", "The Performance Review",
          "Taking the Credit"]),
        ("🤝", "Hard conversations with colleagues", "Feedback, friction, and clearing the air.",
         ["The Difficult Conversation", "The Joke", "The Truce", "The Reference",
          "Promoted Over a Friend"]),
        ("🛑", "Protecting your own time", "Saying no, pricing the extra, chasing what you're owed.",
         ["Saying No to Your Boss", "The Changing Brief", "The Unpaid Invoice"]),
        ("🩺", "In the consulting room", "Doing your own clinical job in English.",
         ["The Consultation", "Breaking the News"]),
        ("⚠️", "When it goes wrong", "Mistakes, anger, and people who aren't coping.",
         ["The Mistake", "The Client Who Shouts", "Not Coping at Work",
          "The Colleague Who Cries"]),
        ("🚪", "Starting and leaving", "Interviews, handovers, resignations and redundancy.",
         ["The Interview", "Your Younger Boss", "The Handover", "Resigning", "Made Redundant"]),
    ],
}

CARD_RE = re.compile(r'    <a class="lcard".*?</a>\n', re.S)
TITLE_RE = re.compile(r'<div class="lt">(.*?)</div>')


def regroup(path, plan):
    html = (HERE / path).read_text(encoding="utf-8")
    cards = CARD_RE.findall(html)
    by_title = {}
    for c in cards:
        m = TITLE_RE.search(c)
        if m:
            by_title[m.group(1).replace("&amp;", "&").strip()] = c
    if not cards:
        print(f"  ! no cards found in {path}"); return

    used, out = set(), []
    for emoji, name, blurb, titles in plan:
        rows = [by_title[t] for t in titles if t in by_title]
        missing = [t for t in titles if t not in by_title]
        if missing:
            print(f"  ! {path}: not on the page — {missing}")
        if not rows:
            continue
        used.update(t for t in titles if t in by_title)
        out.append(f'    <div class="pathhead">{emoji} {name} — {blurb}</div>\n')
        out.extend(rows)
        out.append("\n")

    leftover = [t for t in by_title if t not in used]
    if leftover:
        print(f"  + {path}: {len(leftover)} ungrouped -> 'More' section: {leftover}")
        out.append('    <div class="pathhead">✨ More</div>\n')
        out.extend(by_title[t] for t in leftover)
        out.append("\n")

    # replace the old flat block: from the first pathhead (or first card) to the last card
    start = html.index('    <div class="pathhead">')
    last_card_end = html.rindex("</a>\n") + len("</a>\n")
    html = html[:start] + "".join(out) + html[last_card_end:]
    # collapse any run of blank lines so re-running doesn't slowly grow the file
    html = re.sub(r"\n{3,}", "\n\n", html)
    (HERE / path).write_text(html, encoding="utf-8")

    n_cards = html.count('class="lcard"')
    n_groups = html.count('class="pathhead"')
    ok = n_cards == len(cards)
    print(f"  {path}: {n_cards} cards in {n_groups} groups "
          f"{'✓' if ok else '— CARD COUNT CHANGED (was %d)' % len(cards)}")


if __name__ == "__main__":
    for path, plan in PLANS.items():
        regroup(path, plan)
