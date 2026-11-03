#!/usr/bin/env python3
"""Speak First — A1 everyday-conversation series.

Clones the Short History / Short Stories A2-B1 template (5 tabs:
Key Words → The Conversation → Grammar → Listen → Speak) and swaps in
British-Council-style beginner content: a short everyday conversation in
three parts, vocabulary matching, quick checks, one grammar point with three
exercises, listening tasks (true/false + order the lines), and speaking tasks.

Run from gitsite:  python3 tools/build_speak_first.py
Writes sf_a1_NN_slug.html for every lesson in LESSONS.
"""
import html, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
TEMPLATE = os.path.join(OUT, "short_history_houdini_a2b1.html")
SERIES = "Speak First"

# ----------------------------------------------------------------------------
# CONTENT
# ----------------------------------------------------------------------------
LESSONS = [
{
 "picture": ("sf_a1_01_name_and_job.png", "Anna and Leo meet at a coffee break, both holding cups.", ["Where are they?", "How many people can you see?", "What are they drinking?"]),
 "n": 1, "slug": "name_and_job", "title": "Name and Job",
 "strap": "Two people meet for the first time. Say who you are, and ask the same.",
 "today": "say your name, your country and your job, and ask another person the same three questions. Grammar: <em>I'm</em> and <em>Are you…?</em>",
 "warm_intro": "<strong>Warm up — five words you probably know.</strong> <strong>Do you know it?</strong> Say it out loud and say when you use it. <strong>Is it new?</strong> Good — learn it now. Click Reveal to check.",
 "warm": [
   ("hello", None, "Say it. When do you say it?", "hello — the first word when you see a person."),
   ("thank you", None, "Say it. When do you say it?", "thank you — you say it when a person helps you or gives you something."),
   ("yes / no", None, "Say both. Answer: Are you a student?", "yes = ✅ · no = ❌"),
   ("sorry", None, "Say it. When do you say it?", "sorry — you say it when you make a mistake, or when you do not understand."),
   ("please", None, "Say it. Ask for a coffee.", "please — a polite word when you ask for something: \"A coffee, please.\""),
 ],
 "words": ["a name", "a job", "a company", "an engineer", "a teacher", "a school", "hot", "to meet"],
 "meanings": ["a place where children learn", "a person who makes or fixes machines, roads or bridges", "to see a person for the first time",
              "the word people call you", "a person who helps people learn", "very warm", "the work you do for money", "a business — people work there"],
 "key": [3, 6, 7, 1, 4, 0, 5, 2],   # word i -> meaning index
 "before": ["Which words are about work? Which word is about the weather?", "Two people meet. What are the first three questions? Guess."],
 "conv_intro": "Two people meet at a coffee break. Read each part. Then try the questions from memory, and answer the last one about you.",
 "parts": [
   {"h": "Part 1 — Hello",
    "lines": [("Anna", "Good morning."), ("Leo", "Good morning."), ("Anna", "I'm Anna. What's your name?"),
              ("Leo", "My name is Leo. Nice to meet you."), ("Anna", "Nice to meet you too.")],
    "qs": [("What is the woman's name?", "Anna."), ("What does Leo say after his name?", "\"Nice to meet you.\"")],
    "talk": "And you? Say hello, and say your name — two ways: \"I'm…\" and \"My name is…\""},
   {"h": "Part 2 — Where are you from?",
    "lines": [("Anna", "Where are you from, Leo?"), ("Leo", "I'm from Spain. From Madrid. And you?"), ("Anna", "I'm from Brazil."),
              ("Leo", "Oh, Brazil! Is it hot there?"), ("Anna", "Yes, very hot!")],
    "qs": [("Where is Leo from?", "Spain — from Madrid."), ("Is Brazil cold?", "No. It is very hot.")],
    "talk": "And you? Where are you from? Is it hot or cold there?"},
   {"h": "Part 3 — What do you do?",
    "lines": [("Anna", "What do you do, Leo?"), ("Leo", "I'm an engineer. I work for a big company. And you?"), ("Anna", "I'm a teacher. I work in a school."),
              ("Leo", "Do you like it?"), ("Anna", "Yes, I do. I love it.")],
    "qs": [("What is Leo's job?", "He is an engineer. He works for a big company."), ("Where does Anna work?", "In a school. She is a teacher.")],
    "talk": "And you? What do you do? Do you like it?"},
 ],
 "grammar_tab": "Grammar — I'm / Are you…?",
 "grammar_h": "Grammar: I'm / Are you…?",
 "grammar_intro": "In a first conversation you say who you are. English uses the verb <em>be</em>: <em>am</em> and <em>are</em>.",
 "notes": [
   "<strong>I'm = I am.</strong> Use it for your name, your country and your job: \"<em>I'm</em> Sara.\" \"<em>I'm</em> from Mexico.\" \"<em>I'm</em> a nurse.\"",
   "<strong>Are you…?</strong> = a question. Answer <em>Yes, I am</em> or <em>No, I'm not</em>: \"<em>Are you</em> from Italy?\" — \"No, <em>I'm not</em>. I'm from Poland.\"",
   "<strong>Question words:</strong> \"<em>What's</em> your name?\" (What's = What is) · \"<em>Where are</em> you from?\" · \"<em>What do</em> you do?\" (= your job)",
   "<strong>a or an?</strong> <em>a</em> nurse, <em>a</em> driver — but <em>an</em> engineer, <em>an</em> office. Use <em>an</em> before a, e, i, o, u.",
 ],
 "ex1": {"h": "1. am, are or is?", "intro": "Complete each sentence with <em>am</em>, <em>are</em> or <em>is</em>.",
         "items": [("I ___ Marco.", "am"), ("___ you from Japan?", "Are"), ("What ___ your name?", "is (What's = What is)"), ("Yes, I ___.", "am")]},
 "ex2": {"h": "2. Make the sentence", "intro": "Put the words in order. Then say the sentence out loud.",
         "items": [("from / I'm / Poland", "I'm from Poland."), ("you / are / Where / from?", "Where are you from?"), ("a / I'm / driver", "I'm a driver."), ("an / you / Are / engineer?", "Are you an engineer?")]},
 "ex3": {"h": "3. Complete the conversation", "intro": "Fill each gap with one word. Read the conversation out loud when you finish.",
         "text": "\"Good afternoon. ___ Tom. What's your ___?\" — \"My name ___ Julia. Nice to ___ you.\" — \"Nice to meet you too. ___ you from Spain?\" — \"No, I'm not. I'm ___ Italy.\"",
         "ans": "I'm · name · is · meet · Are · from",
         "tip": "Use <em>I'm</em> for you, and <em>Are you…?</em> to ask."},
 "tf": [("Leo is from Brazil.", False, "Leo is from Spain. Anna is from Brazil."), ("Anna is a teacher.", True, "She works in a school."),
        ("Leo works for a small company.", False, "He works for a big company."), ("Anna likes her job.", True, "She says: \"I love it.\"")],
 "order_part": 1,
 "roleplay": {"scene": "A coffee break. A person you do not know says hello.", "you": "yourself", "partner": "Maria",
   "rounds": [("Hello! I'm Maria.", "your name · nice to meet you", "Hi, I'm Tom. Nice to meet you."),
              ("Nice to meet you too. Where are you from?", "your country", "I'm from Italy. From Milan."),
              ("Oh, nice! What do you do?", "your job", "I'm a driver. / I have a company."),
              ("Interesting. Do you like it?", "yes or no · one thing about it", "Yes, I do. It's busy, but it's good."),
              ("Is it hot in your country now?", "hot or cold", "Yes, it's very hot now.")],
   "quick": [("What's your name?", "I'm Tom. / My name is Tom."), ("Where are you from?", "I'm from Italy."), ("What do you do?", "I'm an engineer."), ("Do you like your job?", "Yes, I do. / No, I don't."),
             ("Is it hot in your city now?", "Yes, it is. / No, it's cold."), ("Are you a teacher?", "No, I'm not. I'm a driver."), ("Nice to meet you.", "Nice to meet you too."), ("What's your city?", "It's Milan.")]},
 "useful": "<strong>Useful language:</strong> \"I'm…\" · \"My name is…\" · \"I'm from…\" · \"I'm a… / I'm an…\" · \"Nice to meet you.\" · \"And you?\"",
 "taskA": {"h": "Task A · Play the conversation", "p": ["You are Leo. Use <strong>your</strong> name, <strong>your</strong> country and <strong>your</strong> job. Follow the steps: <em>hello → your name → \"Nice to meet you\" → where you are from → your job → \"And you?\"</em>", "Then change: you are Anna. Ask the questions."]},
 "taskB": {"h": "Task B · About you (1 minute)", "p": ["Say five sentences about you: your name, your country, your city, your job, and one thing you like. Start the timer and keep talking."]},
 "taskC": {"h": "Task C · Ask me", "p": ["Ask me four questions: my name, where I am from, my job, and \"Do you like it?\" Then ask them again, faster."]},
 "finish": ["Is your job good? Say one good thing about it.", "Which is easy to say: your name, your country or your job? Which is hard?", "<strong>From memory:</strong> say the three questions from today."],
},
{
 "picture": ("sf_a1_02_my_family.png", "Leo shows Anna a photo of his family on his phone.", ["Who are the people?", "How old are the children? Guess.", "Where are Anna and Leo?"]),
 "n": 2, "slug": "my_family", "title": "My Family",
 "strap": "Wife, husband, children, brothers and sisters. Talk about the people in your life.",
 "today": "say who is in your family, and ask another person about their family. Grammar: <em>I have…</em> and <em>his / her</em>.",
 "warm_intro": "<strong>Warm up — five words to remember.</strong> They come from Lesson 1. <strong>Do you know it?</strong> Say what it means and use it in a sentence. <strong>Is it new?</strong> Good — learn it now. Click Reveal to check, and follow the link to read the lesson.",
 "warm": [
   ("a job", "sf_a1_01_name_and_job.html|Name and Job", "What does it mean? Say your job.", "a job — the work you do for money."),
   ("a company", "sf_a1_01_name_and_job.html|Name and Job", "What does it mean? Name one big company.", "a company — a business; people work there."),
   ("to meet", "sf_a1_01_name_and_job.html|Name and Job", "What does it mean? What do you say when you meet a new person?", "to meet — to see a person for the first time. \"Nice to meet you.\""),
   ("an engineer", "sf_a1_01_name_and_job.html|Name and Job", "What does it mean? Say: a or an?", "an engineer — a person who makes or fixes machines, roads or bridges."),
   ("hot", "sf_a1_01_name_and_job.html|Name and Job", "What does it mean? Is it hot in your city now?", "hot — very warm."),
 ],
 "words": ["a wife", "a husband", "a son", "a daughter", "a brother", "parents", "married", "to call"],
 "meanings": ["your mother and father", "a boy — your child", "to speak to a person on the phone", "the woman a man is married to",
              "a girl — your child", "a boy with the same mother and father as you", "the man a woman is married to", "with a wife or a husband"],
 "key": [3, 6, 1, 4, 5, 0, 7, 2],
 "before": ["Which words are people? Which word is an action?", "Two people talk about family. What questions do they ask? Guess two."],
 "conv_intro": "Anna and Leo have lunch together. Read each part. Then try the questions from memory, and answer the last one about you.",
 "parts": [
   {"h": "Part 1 — Are you married?",
    "lines": [("Anna", "Are you married, Leo?"), ("Leo", "Yes, I am. My wife's name is Carla. She's a doctor."), ("Leo", "And you, Anna? Are you married?"),
              ("Anna", "No, I'm not. But I have a boyfriend. His name is Pedro.")],
    "qs": [("What is Leo's wife's name? What is her job?", "Carla. She is a doctor."), ("Is Anna married?", "No, she is not. She has a boyfriend, Pedro.")],
    "talk": "And you? Are you married?"},
   {"h": "Part 2 — Children",
    "lines": [("Anna", "Do you have children?"), ("Leo", "Yes, I do. I have two children, a son and a daughter."), ("Anna", "How old are they?"),
              ("Leo", "My son is fifteen and my daughter is ten."), ("Anna", "Fifteen! What are their names?"), ("Leo", "Marco and Sofia.")],
    "qs": [("How many children does Leo have?", "Two — a son and a daughter."), ("How old is his daughter?", "She is ten. Her name is Sofia.")],
    "talk": "And you? Do you have children? How old are they?"},
   {"h": "Part 3 — Brothers and sisters",
    "lines": [("Leo", "Do you have brothers and sisters?"), ("Anna", "Yes! I have three brothers. It's a big family."), ("Leo", "Three brothers! Do they live in Brazil?"),
              ("Anna", "Two brothers live in Brazil. One brother lives in Portugal."), ("Leo", "And your parents?"), ("Anna", "They live in São Paulo. I call them every Sunday.")],
    "qs": [("How many brothers does Anna have?", "Three. Two live in Brazil and one lives in Portugal."), ("Where do her parents live?", "In São Paulo. She calls them every Sunday.")],
    "talk": "And you? Do you have brothers and sisters? Where do they live?"},
 ],
 "grammar_tab": "Grammar — I have / his, her",
 "grammar_h": "Grammar: I have / his, her",
 "grammar_intro": "To talk about family, you need two small things: <em>have</em>, and the words <em>his</em> and <em>her</em>.",
 "notes": [
   "<strong>I have…</strong> \"I <em>have</em> one sister.\" \"I <em>have</em> two children.\" No children? \"I <em>don't have</em> children.\"",
   "<strong>Do you have…?</strong> Answer <em>Yes, I do</em> or <em>No, I don't</em>: \"<em>Do you have</em> brothers?\" — \"Yes, I do. Two.\"",
   "<strong>he → his · she → her.</strong> \"This is my father. <em>His</em> name is Paul. <em>He's</em> seventy.\" \"This is my sister. <em>Her</em> name is Eva. <em>She's</em> a nurse.\"",
   "<strong>How old…?</strong> \"How old is <em>he</em>?\" — \"He's twenty.\" · \"How old are <em>they</em>?\" — \"They're five and eight.\"",
 ],
 "ex1": {"h": "1. his or her?", "intro": "Complete each sentence with <em>his</em> or <em>her</em>.",
         "items": [("This is my daughter. ___ name is Julia.", "Her"), ("This is my brother. ___ name is Sam.", "His"), ("My wife is a teacher. ___ school is small.", "Her"), ("My son is ten. ___ birthday is in May.", "His")]},
 "ex2": {"h": "2. Make the sentence", "intro": "Put the words in order. Then say the sentence out loud.",
         "items": [("have / children / two / I", "I have two children."), ("you / Do / brothers / have?", "Do you have brothers?"), ("old / How / your / is / son?", "How old is your son?"), ("don't / I / a sister / have", "I don't have a sister.")]},
 "ex3": {"h": "3. Complete the conversation", "intro": "Fill each gap with one word. Read the conversation out loud when you finish.",
         "text": "\"___ you married?\" — \"Yes, I ___. My husband's name ___ David.\" — \"Do you ___ children?\" — \"Yes, I ___. One son. ___ name is Ben. He's six.\"",
         "ans": "Are · am · is · have · do · His",
         "tip": "<em>Do you have…?</em> → <em>Yes, I do.</em> · a boy → <em>his</em>, a girl → <em>her</em>."},
 "tf": [("Leo's wife is a doctor.", True, "\"My wife's name is Carla. She's a doctor.\""), ("Anna is married.", False, "She is not married. She has a boyfriend."),
        ("Leo's son is fifteen.", True, "\"My son is fifteen and my daughter is ten.\""), ("Anna has two brothers.", False, "She has three brothers.")],
 "order_part": 1,
 "roleplay": {"scene": "Lunch with a colleague. She asks about your family.", "you": "yourself", "partner": "Maria",
   "rounds": [("Are you married?", "yes or no · name", "Yes, I am. My wife's name is Elena."),
              ("Do you have children?", "yes or no · how many", "Yes, I do. I have one son."),
              ("How old is he?", "age · name", "He's twenty. His name is Luca."),
              ("Do you have brothers and sisters?", "how many", "I have one sister and two brothers."),
              ("And where do your parents live?", "place · call?", "They live in Rome. I call them every Sunday.")],
   "quick": [("Are you married?", "Yes, I am. / No, I'm not."), ("What's your wife's name?", "Her name is Elena."), ("Do you have children?", "Yes, I do. Two."), ("How old are they?", "They're ten and fifteen."),
             ("Do you have a brother?", "Yes, I have one brother. His name is Paul."), ("Where do your parents live?", "They live in a small town."), ("Who do you call every week?", "I call my mother."), ("Is your family big?", "No, it's small. Three people.")]},
 "useful": "<strong>Useful language:</strong> \"I have…\" · \"I don't have…\" · \"This is my…\" · \"His name is… / Her name is…\" · \"He's / She's … years old.\" · \"They live in…\"",
 "taskA": {"h": "Task A · Play the conversation", "p": ["You are Leo, but with <strong>your</strong> family. Follow the steps: <em>married? → children? → how old? → names? → brothers and sisters? → parents?</em>", "Then change: you are Anna. Ask the questions."]},
 "taskB": {"h": "Task B · My family (1 minute)", "p": ["Say five sentences about your family: married or not, children, their names and ages, brothers and sisters, and where your parents live. Start the timer and keep talking."]},
 "taskC": {"h": "Task C · Ask me", "p": ["Ask me five questions about my family: married, children, how old, brothers and sisters, parents. Listen to my answers, and say one thing you remember."]},
 "finish": ["Is your family big or small? Who is in it?", "Who do you call every week? Why?", "<strong>From memory:</strong> \"This is my son. ___ name is Marco.\" \"This is my daughter. ___ name is Sofia.\" Say both."],
},
{
 "picture": ("sf_a1_03_my_home.png", "Leo on his small balcony with a coffee, the city behind him.", ["Is it a house or a flat?", "What can you see?", "Is it big or small?"]),
 "n": 3, "slug": "my_home", "title": "My Home",
 "strap": "House or flat, big or small, city or town. Talk about where you live.",
 "today": "say where you live and what rooms you have, and ask another person about their home. Grammar: <em>There's…</em> and <em>There are…</em>",
 "warm_intro": "<strong>Warm up — five words to remember.</strong> They come from Lessons 1 and 2. <strong>Do you know it?</strong> Say what it means and use it in a sentence. <strong>Is it new?</strong> Good — learn it now. Click Reveal to check, and follow the link to read the lesson.",
 "warm": [
   ("a wife", "sf_a1_02_my_family.html|My Family", "What does it mean? Say the word for a man.", "a wife — the woman a man is married to. The man is a husband."),
   ("parents", "sf_a1_02_my_family.html|My Family", "What does it mean? Where do your parents live?", "parents — your mother and father."),
   ("married", "sf_a1_02_my_family.html|My Family", "What does it mean? Ask me: married?", "married — with a wife or a husband. \"Are you married?\""),
   ("to call", "sf_a1_02_my_family.html|My Family", "What does it mean? Who do you call every week?", "to call — to speak to a person on the phone."),
   ("a company", "sf_a1_01_name_and_job.html|Name and Job", "What does it mean? Do you work for a company?", "a company — a business; people work there."),
 ],
 "words": ["a flat", "a bedroom", "a kitchen", "a garden", "a balcony", "quiet", "old", "favourite"],
 "meanings": ["the room where you cook", "not new", "the one you like best", "rooms in a big building — people live there",
              "a small place outside a window, high up, where you can sit", "with no noise", "the room where you sleep", "a place outside a house with grass and flowers"],
 "key": [3, 6, 0, 7, 4, 5, 1, 2],
 "before": ["Which words are rooms? Which words describe a place?", "Two people talk about their homes. What questions do they ask? Guess two."],
 "conv_intro": "Anna and Leo talk after work. Read each part. Then try the questions from memory, and answer the last one about you.",
 "parts": [
   {"h": "Part 1 — Where do you live?",
    "lines": [("Anna", "Where do you live, Leo?"), ("Leo", "I live in a flat in the city. Near the station."), ("Anna", "Is it big?"),
              ("Leo", "No, it's small. But it's quiet. I like it.")],
    "qs": [("Does Leo live in a house or a flat?", "In a flat, in the city, near the station."), ("Is the flat big?", "No, it is small. But it is quiet.")],
    "talk": "And you? Do you live in a house or a flat? In a city or a small town?"},
   {"h": "Part 2 — The rooms",
    "lines": [("Anna", "How many rooms?"), ("Leo", "There are two bedrooms, a living room, a kitchen and a bathroom."), ("Anna", "Do you have a balcony?"),
              ("Leo", "Yes, a small balcony. I drink my coffee there every morning. It's my favourite place.")],
    "qs": [("How many bedrooms are there?", "Two."), ("What does Leo do on the balcony?", "He drinks his coffee there every morning.")],
    "talk": "And you? What rooms are in your home? What is your favourite room?"},
   {"h": "Part 3 — Anna's house",
    "lines": [("Leo", "And you, Anna? Where do you live?"), ("Anna", "I live in a house. It's old, but I love it. There's a big garden."), ("Leo", "Nice! Who do you live with?"),
              ("Anna", "With my two dogs. And a cat!"), ("Leo", "Three animals and a garden. Perfect.")],
    "qs": [("Is Anna's house new?", "No, it is old. But she loves it."), ("Who does Anna live with?", "With two dogs and a cat.")],
    "talk": "And you? Who do you live with?"},
 ],
 "grammar_tab": "Grammar — There's / There are",
 "grammar_h": "Grammar: There's / There are",
 "grammar_intro": "To say what is in a place, English uses <em>there is</em> and <em>there are</em>.",
 "notes": [
   "<strong>There's = There is.</strong> One thing: \"<em>There's</em> a bathroom.\" \"<em>There's</em> a big table in the living room.\"",
   "<strong>There are.</strong> Two or more: \"<em>There are</em> three bedrooms.\" \"<em>There are</em> two cars in the garage.\"",
   "<strong>Questions:</strong> \"<em>Is there</em> a garage?\" — \"Yes, there is. / No, there isn't.\" · \"<em>How many</em> rooms <em>are there</em>?\" — \"Five.\"",
   "<strong>live in / live with.</strong> \"I live <em>in</em> a house.\" \"I live <em>in</em> a small town.\" \"I live <em>with</em> my family.\" Alone? \"I live <em>alone</em>.\"",
 ],
 "ex1": {"h": "1. There's or There are?", "intro": "Complete each sentence with <em>There's</em> or <em>There are</em>.",
         "items": [("___ a kitchen.", "There's (one kitchen)"), ("___ two bathrooms.", "There are (two)"), ("___ three bedrooms and a garden.", "There are (three)"), ("___ a small balcony.", "There's (one)")]},
 "ex2": {"h": "2. Make the sentence", "intro": "Put the words in order. Then say the sentence out loud.",
         "items": [("in / I / live / a flat", "I live in a flat."), ("you / do / Where / live?", "Where do you live?"), ("a / there / Is / garden?", "Is there a garden?"), ("with / live / I / my parents", "I live with my parents.")]},
 "ex3": {"h": "3. Complete the conversation", "intro": "Fill each gap with one word. Read the conversation out loud when you finish.",
         "text": "\"Where do you ___?\" — \"I live ___ a house in a small town. There ___ four rooms, and ___ a big garden.\" — \"Who do you live ___?\" — \"With my husband and my two ___.\"",
         "ans": "live · in · are · there's · with · children (or: dogs, cats, sons, daughters)",
         "tip": "One thing → <em>there's</em>. Two or more → <em>there are</em>."},
 "tf": [("Leo lives near the station.", True, "\"I live in a flat in the city. Near the station.\""), ("Leo's flat is big.", False, "It is small, but quiet."),
        ("There are three bedrooms in Leo's flat.", False, "There are two bedrooms."), ("Anna has two dogs and a cat.", True, "\"With my two dogs. And a cat!\"")],
 "order_part": 1,
 "roleplay": {"scene": "A friend visits your city. He asks about your home.", "you": "yourself", "partner": "Sam",
   "rounds": [("Where do you live?", "house or flat · city or town", "I live in a flat in the city."),
              ("Is it big?", "big or small · one more thing", "No, it's small. But it's quiet."),
              ("How many rooms?", "There's… There are…", "There are two bedrooms, a living room, a kitchen and a bathroom."),
              ("Do you have a garden or a balcony?", "yes or no", "Yes, a small balcony."),
              ("Nice. Who do you live with?", "who", "With my wife and my son.")],
   "quick": [("Where do you live?", "I live in a house in a small town."), ("Do you live in a house or a flat?", "In a flat."), ("Is it big?", "No, it's small."), ("How many bedrooms are there?", "There are three."),
             ("Is there a garden?", "Yes, there is. / No, there isn't."), ("What's your favourite room?", "The kitchen."), ("Who do you live with?", "I live with my family."), ("Is your street quiet?", "No, it's noisy.")]},
 "useful": "<strong>Useful language:</strong> \"I live in…\" · \"There's a…\" · \"There are two…\" · \"It's big / small / old / new / quiet.\" · \"My favourite room is…\" · \"I live with…\"",
 "taskA": {"h": "Task A · Play the conversation", "p": ["You are Leo, but with <strong>your</strong> home. Follow the steps: <em>where you live → big or small? → the rooms → a balcony or a garden? → who you live with</em>", "Then change: you are Anna. Ask the questions."]},
 "taskB": {"h": "Task B · My home (1 minute)", "p": ["Say five sentences about your home: house or flat, city or town, the rooms, your favourite room, and who you live with. Start the timer and keep talking."]},
 "taskC": {"h": "Task C · Ask me", "p": ["Ask me five questions about my home: where, house or flat, how many rooms, a garden, who with. Listen to my answers, and say one thing you remember."]},
 "finish": ["What is good about your home? Say one thing.", "Is your street quiet or noisy? Do you like it?", "<strong>From memory:</strong> <em>There's</em> or <em>There are</em>? \"___ a garden.\" \"___ two bedrooms.\" Say both."],
},
{
 "picture": ("sf_a1_04_a_working_day.png", "Six o'clock: Leo in his kitchen with a coffee, the clock says 6:00, the window is dark.", ["Where is Leo?", "What time is it?", "How does he feel? Why?"]),
 "n": 4, "slug": "a_working_day", "title": "A Working Day",
 "strap": "Six o'clock, coffee, traffic, meetings. Talk about your day, and ask about someone else's.",
 "today": "describe your normal day from morning to night, and ask another person about theirs. Grammar: present simple with <em>he / she</em>, and <em>at / on / in</em> with times.",
 "warm_intro": "<strong>Warm up — five words to remember.</strong> They come from Lessons 1 to 3. <strong>Do you know it?</strong> Say what it means and use it in a sentence. <strong>Is it new?</strong> Good — learn it now. Click Reveal to check, and follow the link to read the lesson.",
 "warm": [
   ("a company", "sf_a1_01_name_and_job.html|Name and Job", "What does it mean? Do you work for a company, or do you have one?", "a company — a business; people work there."),
   ("a daughter", "sf_a1_02_my_family.html|My Family", "What does it mean? Say the word for a boy.", "a daughter — a girl; your child. A boy is a son."),
   ("to call", "sf_a1_02_my_family.html|My Family", "What does it mean? Who do you call every week?", "to call — to speak to a person on the phone."),
   ("quiet", "sf_a1_03_my_home.html|My Home", "What does it mean? Is your home quiet?", "quiet — with no noise."),
   ("favourite", "sf_a1_03_my_home.html|My Home", "What does it mean? What is your favourite room?", "favourite — the one you like best."),
 ],
 "words": ["to get up", "traffic", "a meeting", "a customer", "busy", "to finish", "tired", "the weekend"],
 "meanings": ["to stop; to come to the end", "Saturday and Sunday", "people talk about work together, at a table", "with a lot of things to do",
              "cars, buses and lorries on the road", "you need sleep", "to get out of bed in the morning", "a person who buys things from a company"],
 "key": [6, 4, 2, 7, 3, 0, 5, 1],
 "before": ["Which words are about work? Which word is about the road?", "A man gets up at six every day. Why? Guess."],
 "conv_intro": "Leo has a small company. This is his day. Read each part. Then try the questions from memory, and answer the last one about you.",
 "parts": [
   {"h": "Part 1 — Six o'clock",
    "lines": [("", "Leo gets up at six. He doesn't like it, but he has a small company, and the company doesn't sleep. He has a coffee in the kitchen. Carla is still in bed. At seven, he drives to work. The traffic is bad. He listens to the radio and thinks about the day."),
              ("Anna", "Morning, Leo. You look tired."), ("Leo", "I am tired. I get up at six every day."), ("Anna", "Every day? I get up at eight."), ("Leo", "Eight! That's a holiday.")],
    "qs": [("What time does Leo get up? Why?", "At six. He has a small company, and there is a lot of work."), ("How does he go to work?", "By car. He drives, and the traffic is bad.")],
    "talk": "And you? What time do you get up? How do you go to work?"},
   {"h": "Part 2 — Meetings",
    "lines": [("", "Leo's day is meetings. At nine, a meeting with the team. At eleven, a phone call with a customer in Germany. At one, lunch — usually a sandwich at his desk. Anna doesn't like this."),
              ("Anna", "A sandwich again?"), ("Leo", "I don't have time."), ("Anna", "You have thirty minutes. Come to the café."), ("Leo", "OK. Thirty minutes. Not more.")],
    "qs": [("What does Leo usually have for lunch? Where?", "A sandwich, at his desk."), ("Where do Anna and Leo go?", "To the café, for thirty minutes.")],
    "talk": "And you? Are you busy at work? What do you do at lunch?"},
   {"h": "Part 3 — Home",
    "lines": [("", "Leo finishes at seven. At home, he has dinner with Carla and the children. Marco talks about football. Sofia talks about school. After dinner, Leo watches the news, and at eleven he goes to bed."),
              ("", "At the weekend, it is different. He doesn't get up at six. He sleeps until nine, and Carla makes pancakes."),
              ("Carla", "Leo, it's Saturday. Sleep!"), ("Leo", "I can't. My phone…"), ("Carla", "Give me the phone.")],
    "qs": [("What time does Leo finish work? What does he do in the evening?", "At seven. He has dinner with his family, watches the news and goes to bed at eleven."), ("What is different at the weekend?", "He doesn't get up at six. He sleeps until nine.")],
    "talk": "And you? What do you do in the evening? Is your weekend different?"},
 ],
 "grammar_tab": "Grammar — he gets up / at, on, in",
 "grammar_h": "Grammar: he gets up / at, on, in",
 "grammar_intro": "To talk about your day, you need the present simple — and the small words for time.",
 "notes": [
   "<strong>I / you → no -s. He / she → -s.</strong> \"I <em>start</em> at nine.\" \"She <em>starts</em> at eight.\" \"He <em>has</em> lunch at one.\" (have → has)",
   "<strong>Negative:</strong> \"I <em>don't</em> work on Sunday.\" \"He <em>doesn't</em> like meetings.\" (don't / doesn't + verb, no -s)",
   "<strong>Questions:</strong> \"What time <em>do you</em> get up?\" \"What time <em>does he</em> finish?\" \"<em>Do you</em> work on Saturday?\" — \"Yes, I do. / No, I don't.\"",
   "<strong>at / on / in:</strong> <em>at</em> six, <em>at</em> the weekend, <em>at</em> night · <em>on</em> Monday, <em>on</em> Sunday morning · <em>in</em> the morning, <em>in</em> the evening",
 ],
 "ex1": {"h": "1. Put the verb in the right form", "intro": "Use the verb in brackets. Careful with <em>he</em> and <em>she</em>.",
         "items": [("Leo ___ (get up) at six.", "gets up"), ("I ___ (finish) at five.", "finish"), ("She ___ (not / like) meetings.", "doesn't like"), ("___ he ___ (work) on Sunday?", "Does he work")]},
 "ex2": {"h": "2. Make the sentence", "intro": "Put the words in order. Then say the sentence out loud.",
         "items": [("time / What / get up / does / he?", "What time does he get up?"), ("at / I / seven / to work / go", "I go to work at seven."), ("doesn't / She / on Sunday / work", "She doesn't work on Sunday."), ("in / meetings / I / the morning / have", "I have meetings in the morning.")]},
 "ex3": {"h": "3. Complete the conversation", "intro": "Fill each gap with one word. Read the conversation out loud when you finish.",
         "text": "\"What time ___ you start work?\" — \"At nine. I ___ meetings in the morning, and lunch ___ one.\" — \"And your wife?\" — \"She ___ at home. She ___ work on Friday.\"",
         "ans": "do · have · at · works · doesn't",
         "tip": "<em>she works</em> (-s) · <em>she doesn't work</em> (no -s)."},
 "roleplay": {"scene": "Your first week in a new job. A colleague asks about your day.", "you": "yourself", "partner": "Maria",
   "rounds": [("What time do you get up?", "time · early or late?", "I get up at half past six. It's early."),
              ("Do you have breakfast?", "yes or no · what", "Yes, I do. Coffee and bread."),
              ("How do you go to work?", "car, bus, train, walk · how long", "By car. It's thirty minutes. The traffic is bad."),
              ("What do you do at work in the morning?", "meetings, emails, phone calls, customers", "I have meetings, and I call customers."),
              ("What time do you finish?", "time · busy?", "At six. Sometimes seven. It's a busy job."),
              ("And in the evening?", "dinner, family, TV, bed", "I have dinner with my family, and I watch TV. I go to bed at eleven.")],
   "quick": [("What time do you get up?", "I get up at seven."), ("Do you have breakfast?", "Yes, I do. Coffee and toast."), ("How do you go to work?", "By car. / By bus. / I walk."), ("What time do you start work?", "At nine."),
             ("What do you do at lunch?", "I have a sandwich at my desk."), ("What time do you finish?", "At six."), ("What do you do in the evening?", "I have dinner and I watch the news."), ("What time do you go to bed?", "At eleven."),
             ("Do you work at the weekend?", "No, I don't. / Sometimes."), ("What time does your wife get up?", "She gets up at seven.")]},
 "useful": "<strong>Useful language:</strong> \"I get up at…\" · \"I go to work by…\" · \"I have meetings in the morning.\" · \"I finish at…\" · \"In the evening, I…\" · \"At the weekend, I don't…\"",
 "taskA": {"h": "Task A · Tell Leo's day", "p": ["Tell Leo's day in your own words. Use these steps: <em>six o'clock → coffee → the car and the traffic → meetings → a sandwich → dinner with the family → the news → bed → Saturday: pancakes.</em>", "Careful: <strong>he gets up, he has, he finishes</strong>."]},
 "taskB": {"h": "Task B · My day (2 minutes)", "p": ["Tell your normal day from morning to night. Say a time in every sentence: \"At seven, I…\" Start the timer and keep talking."]},
 "taskC": {"h": "Task C · Ask me", "p": ["Ask me six questions about my day: get up, breakfast, work, lunch, finish, evening. Then tell me my day back: \"You get up at… You…\""]},
 "finish": ["Is your day busy? What is the best part of it?", "Leo has a sandwich at his desk. Is this a good idea? What do you do?", "<strong>From memory:</strong> say one sentence with <em>I</em>, and the same sentence with <em>he</em>."],
},
{
 "picture": ("sf_a1_05_the_weekend.png", "Sunday lunch: Leo serves a big fish; Carla, Marco and Sofia are at the table.", ["What day is it? Guess.", "Who is at the table?", "What is on the table?"]),
 "n": 5, "slug": "the_weekend", "title": "The Weekend",
 "strap": "Football, cooking, a guitar. Talk about what you love doing, and what you can't do.",
 "today": "talk about your free time — what you like, how often you do it, and what you can and can't do — and ask another person the same. Grammar: <em>like + -ing</em> and <em>can / can't</em>.",
 "warm_intro": "<strong>Warm up — five words to remember.</strong> They come from Lessons 3 and 4. <strong>Do you know it?</strong> Say what it means and use it in a sentence. <strong>Is it new?</strong> Good — learn it now. Click Reveal to check, and follow the link to read the lesson.",
 "warm": [
   ("to get up", "sf_a1_04_a_working_day.html|A Working Day", "What does it mean? What time do you get up?", "to get up — to get out of bed in the morning."),
   ("busy", "sf_a1_04_a_working_day.html|A Working Day", "What does it mean? Are you busy this week?", "busy — with a lot of things to do."),
   ("tired", "sf_a1_04_a_working_day.html|A Working Day", "What does it mean? Are you tired now?", "tired — you need sleep."),
   ("the weekend", "sf_a1_04_a_working_day.html|A Working Day", "What does it mean? What do you do at the weekend?", "the weekend — Saturday and Sunday."),
   ("a garden", "sf_a1_03_my_home.html|My Home", "What does it mean? Do you have one?", "a garden — a place outside a house with grass and flowers."),
 ],
 "words": ["to play", "to cook", "a recipe", "to swim", "the guitar", "a friend", "slow", "to sing"],
 "meanings": ["to move in water", "not fast", "to make food", "a person you like and know well", "to make music with your voice",
              "to do a sport or a game; to make music", "the words that say how to make a dish", "a music instrument with six strings"],
 "key": [5, 2, 6, 0, 7, 3, 1, 4],
 "before": ["Which words are things you do? Which words are things or people?", "A man is forty-eight and plays football. Is he fast or slow? Guess."],
 "conv_intro": "Leo's weekend, and Anna's. Read each part. Then try the questions from memory, and answer the last one about you.",
 "parts": [
   {"h": "Part 1 — Saturday morning",
    "lines": [("", "Saturday. Leo sleeps until nine. Then he plays football with his friends in the park. He is not very good, but he loves it. After football, they have a coffee and talk. About football, of course."),
              ("Sam", "Leo, you are slow today."), ("Leo", "I'm forty-eight, Sam."), ("Sam", "I'm fifty!"), ("Leo", "Yes, but you don't work sixty hours a week.")],
    "qs": [("What does Leo do on Saturday morning?", "He sleeps until nine, then he plays football with his friends in the park."), ("Is he good at football?", "No, not very good. But he loves it.")],
    "talk": "And you? Do you like sport? What sport? Are you good at it?"},
   {"h": "Part 2 — Sunday lunch",
    "lines": [("", "Sunday is Leo's favourite day. He cooks. Fish, pasta, a big salad. The family eats at two, and lunch is long. In the afternoon, Sofia plays the piano, Marco plays video games, and Carla reads in the garden."),
              ("Carla", "Leo, this fish is very good."), ("Leo", "Thank you. New recipe. From the internet."), ("Marco", "Dad, can I play now?"), ("Leo", "After the plates, Marco.")],
    "qs": [("What does Leo do on Sunday?", "He cooks for the family — fish, pasta, salad. Lunch is long."), ("What does Carla do in the afternoon?", "She reads in the garden.")],
    "talk": "And you? Do you like cooking? What is your favourite day of the week?"},
   {"h": "Part 3 — Monday: Anna's weekend",
    "lines": [("Anna", "What do you do at the weekend, Leo?"), ("Leo", "Football, cooking, family. And you?"), ("Anna", "I swim on Saturday morning. Then I read. I read a lot."),
              ("Leo", "Do you like music?"), ("Anna", "I love music. I play the guitar. Not very well!"), ("Leo", "I can't play anything. But I can sing."), ("Anna", "Really?"), ("Leo", "No. Not really.")],
    "qs": [("What does Anna do on Saturday morning?", "She swims. Then she reads."), ("Can Leo play an instrument? Can he sing?", "No, he can't play anything. And he can't really sing — it's a joke.")],
    "talk": "And you? Do you like music? Can you play an instrument, or sing?"},
 ],
 "grammar_tab": "Grammar — like + -ing / can",
 "grammar_h": "Grammar: like + -ing / can, can't",
 "grammar_intro": "Two small tools for free time: <em>like</em> with <em>-ing</em>, and <em>can</em>.",
 "notes": [
   "<strong>like / love / don't like + -ing.</strong> \"I love <em>cooking</em>.\" \"She likes <em>reading</em>.\" \"I don't like <em>running</em>.\" (swim → swimming, run → running)",
   "<strong>Questions with like:</strong> \"<em>Do you like</em> football?\" \"<em>Do you like</em> cooking?\" — \"Yes, I do. / No, I don't. / I love it!\"",
   "<strong>can / can't</strong> = it is possible for you, or not: \"I <em>can</em> swim.\" \"I <em>can't</em> play the guitar.\" \"<em>Can you</em> cook?\" — \"Yes, I can. / No, I can't.\" No -s with he: \"He <em>can</em> sing.\"",
   "<strong>How often?</strong> \"every Saturday\" · \"on Sunday\" · \"three times a week\" · \"a lot\" · \"never\"",
 ],
 "ex1": {"h": "1. Put the verb in the right form", "intro": "Use the verb in brackets with <em>-ing</em>.",
         "items": [("I like ___ (swim).", "swimming"), ("She loves ___ (read).", "reading"), ("He doesn't like ___ (run).", "running"), ("Do you like ___ (cook)?", "cooking")]},
 "ex2": {"h": "2. Make the sentence", "intro": "Put the words in order. Then say the sentence out loud.",
         "items": [("play / Can / the guitar / you?", "Can you play the guitar?"), ("cooking / I / Sunday / love / on", "I love cooking on Sunday."), ("can't / He / swim", "He can't swim."), ("at / do / What / you / the weekend / do?", "What do you do at the weekend?")]},
 "ex3": {"h": "3. Complete the conversation", "intro": "Fill each gap with one word. Read the conversation out loud when you finish.",
         "text": "\"Do you like ___ (cook)?\" — \"Yes, I love it. I cook ___ Sunday, for the family.\" — \"___ you play the piano?\" — \"No, I ___. But I can sing!\" — \"How ___ do you sing?\" — \"Every day. In the car.\"",
         "ans": "cooking · on · Can · can't · often",
         "tip": "<em>like + -ing</em> · <em>Can you…?</em> → <em>Yes, I can. / No, I can't.</em>"},
 "roleplay": {"scene": "A dinner with new people. The person next to you asks about your free time.", "you": "yourself", "partner": "Maria",
   "rounds": [("What do you do at the weekend?", "two or three things", "I play tennis, and I cook for my family."),
              ("Do you like sport?", "yes or no · which sport · how often", "Yes, I love football. I play every Saturday."),
              ("Do you like cooking?", "yes or no · what you cook", "Yes, I do. I cook pasta and fish."),
              ("Can you play an instrument?", "yes or no · which", "No, I can't. But my daughter can play the piano."),
              ("What about music? What do you like?", "kind of music · when you listen", "I like rock. I listen in the car."),
              ("And your favourite day of the week?", "day · why", "Sunday. I don't work, and lunch is long.")],
   "quick": [("What do you do in your free time?", "I read and I walk."), ("Do you like sport?", "Yes, I do. I play football."), ("How often do you play?", "Every Saturday."), ("Do you like cooking?", "No, I don't. My wife cooks."),
             ("Can you swim?", "Yes, I can."), ("Can you play the guitar?", "No, I can't."), ("Do you like music?", "Yes, I love it."), ("What do you do on Sunday?", "I cook, and I sleep!"),
             ("Do you read a lot?", "No, not a lot. I read the news."), ("What is your favourite day?", "Saturday.")]},
 "useful": "<strong>Useful language:</strong> \"I like / love / don't like + -ing\" · \"I play… every Saturday.\" · \"I can… / I can't…\" · \"Can you…?\" · \"How often do you…?\" · \"three times a week\"",
 "taskA": {"h": "Task A · Tell the weekend", "p": ["Tell Leo's weekend, then Anna's, in your own words. Steps: <em>Saturday: sleep, football, slow, coffee → Sunday: cooking, fish, family, piano, garden → Anna: swimming, reading, the guitar → Leo can't play, can't sing.</em>", "Use <strong>he plays, she reads, he can't</strong>."]},
 "taskB": {"h": "Task B · My free time (2 minutes)", "p": ["Talk about your free time: what you like, how often you do it, one thing you can do well, and one thing you can't do. Start the timer and keep talking."]},
 "taskC": {"h": "Task C · Ask me", "p": ["Ask me six questions about my free time: sport, cooking, music, reading, can you…?, favourite day. Then tell me what you remember: \"You like… You can't…\""]},
 "finish": ["Leo plays football at forty-eight. Is sport important for you? Why?", "Sunday lunch is long in Leo's family. Is lunch long in your family? Who cooks?", "<strong>From memory:</strong> say one thing you love doing, and one thing you can't do."],
},
{
 "picture": ("sf_a1_06_the_airport.png", "Leo at the check-in desk with a small suitcase, giving his passport to the agent.", ["Where is Leo?", "What does he have with him?", "Who is he talking to? What does she say?"]),
 "n": 6, "slug": "the_airport", "title": "The Airport",
 "strap": "Passport, suitcase, boarding pass, and a delay. Everything you say at check-in.",
 "today": "check in at an airport: answer the questions, ask for what you need, and deal with a delay. Grammar: polite questions with <em>Can I…?</em>, <em>Would you like…?</em> and <em>Where can I…?</em>",
 "warm_intro": "<strong>Warm up — five words to remember.</strong> They come from Lessons 4 and 5. <strong>Do you know it?</strong> Say what it means and use it in a sentence. <strong>Is it new?</strong> Good — learn it now. Click Reveal to check, and follow the link to read the lesson.",
 "warm": [
   ("a customer", "sf_a1_04_a_working_day.html|A Working Day", "What does it mean? Do you have customers?", "a customer — a person who buys things from a company."),
   ("a meeting", "sf_a1_04_a_working_day.html|A Working Day", "What does it mean? How many meetings do you have in a week?", "a meeting — people talk about work together, at a table."),
   ("to finish", "sf_a1_04_a_working_day.html|A Working Day", "What does it mean? What time do you finish work?", "to finish — to stop; to come to the end."),
   ("a friend", "sf_a1_05_the_weekend.html|The Weekend", "What does it mean? Say the name of one friend.", "a friend — a person you like and know well."),
   ("slow", "sf_a1_05_the_weekend.html|The Weekend", "What does it mean? Say the opposite.", "slow — not fast."),
 ],
 "words": ["a passport", "a suitcase", "hand luggage", "a boarding pass", "a gate", "delayed", "a window seat", "nervous"],
 "meanings": ["the door in the airport where you get on the plane", "a little afraid, not calm", "a seat next to the window on the plane", "the small book that says who you are; you need it to travel",
              "a small bag you take on the plane with you", "late; not at the normal time", "the paper or phone ticket you show to get on the plane", "a big bag with clothes for a trip"],
 "key": [3, 7, 4, 6, 0, 5, 2, 1],
 "before": ["Which words are things you carry? Which word is about time?", "A man goes to London for a meeting. What can go wrong at the airport? Guess two things."],
 "conv_intro": "Leo flies to London for a meeting with a new customer. Read each part. Then try the questions from memory, and answer the last one about you.",
 "parts": [
   {"h": "Part 1 — Check-in",
    "lines": [("", "Tuesday, six in the morning. Leo is at the airport. He has a meeting in London with a new customer — a big customer. He has a small suitcase and his laptop. He is nervous. His English is not perfect."),
              ("Agent", "Good morning. Where are you flying to?"), ("Leo", "To London."), ("Agent", "Can I see your passport, please?"), ("Leo", "Here you are."),
              ("Agent", "Thank you. Any bags to check in?"), ("Leo", "One suitcase. This is my hand luggage."), ("Agent", "Put the suitcase here, please. Twenty kilos — that's fine.")],
    "qs": [("Why is Leo going to London?", "For a meeting with a new customer — a big one."), ("How many bags does he check in?", "One suitcase. The other bag is hand luggage.")],
    "talk": "And you? Do you fly a lot? Where to? Do you check in a suitcase, or only hand luggage?"},
   {"h": "Part 2 — The seat",
    "lines": [("Agent", "Would you like a window seat or an aisle seat?"), ("Leo", "A window seat, please."), ("Agent", "14A. Here's your boarding pass. Your flight is at 10:40, gate 22."),
              ("Leo", "Gate 22. What time is boarding?"), ("Agent", "At ten."), ("Leo", "Thank you."),
              ("", "Leo goes through security. Belt, watch, shoes. The laptop goes in a box. Then coffee. He needs coffee.")],
    "qs": [("Window or aisle?", "A window seat — 14A."), ("What time is the flight? What time is boarding?", "The flight is at 10:40. Boarding is at ten, at gate 22.")],
    "talk": "And you? Window or aisle? Do you like airports?"},
   {"h": "Part 3 — Delayed",
    "lines": [("", "At 9:50, Leo looks at the screen. Flight 507 to London: DELAYED. New time: 12:10. Two hours. The meeting is at three. Leo calls Anna."),
              ("Leo", "Anna, the flight is delayed. Two hours."), ("Anna", "Don't worry. Call the customer. Say: \"I'm sorry, my flight is delayed. Can we meet at four?\""),
              ("Leo", "In English?"), ("Anna", "In English. You can do it."), ("Leo", "OK. OK."),
              ("", "He calls. The customer says: \"No problem. See you at four.\" Leo smiles. Maybe his English is not so bad.")],
    "qs": [("Why does Leo call Anna?", "The flight is delayed two hours, and the meeting is at three. He doesn't know what to do."), ("What does the customer say?", "\"No problem. See you at four.\"")],
    "talk": "And you? Is your flight ever delayed? What do you do? Do you make phone calls in English?"},
 ],
 "grammar_tab": "Grammar — Can I…? Would you like…?",
 "grammar_h": "Grammar: polite questions",
 "grammar_intro": "At an airport, a hotel or a restaurant, people ask you questions, and you ask for things. These four forms do most of the work.",
 "notes": [
   "<strong>Can I…?</strong> = you want something, politely: \"<em>Can I</em> see your passport?\" \"<em>Can I</em> have a coffee, please?\" Answer: \"Here you are.\" / \"Of course.\"",
   "<strong>Would you like…?</strong> = the other person offers you something: \"<em>Would you like</em> a window seat?\" — \"A window seat, please.\" / \"Yes, please.\" / \"No, thank you.\"",
   "<strong>Where can I…? / What time is…?</strong> \"<em>Where can I</em> get a coffee?\" \"<em>What time is</em> boarding?\" Start with <em>Excuse me</em> to stop a person: \"<em>Excuse me</em>, is this gate 22?\"",
   "<strong>Here you are / Here's your…</strong> = you give something: \"Here you are.\" (your passport) · \"<em>Here's your</em> boarding pass.\"",
 ],
 "ex1": {"h": "1. Which word?", "intro": "Complete each question with <em>Can</em>, <em>Would</em>, <em>Where</em> or <em>What</em>.",
         "items": [("___ I see your passport, please?", "Can"), ("___ you like a window seat?", "Would"), ("___ can I get a taxi?", "Where"), ("___ time is boarding?", "What")]},
 "ex2": {"h": "2. Make the sentence", "intro": "Put the words in order. Then say the question out loud — politely.",
         "items": [("see / I / Can / your ticket?", "Can I see your ticket?"), ("you / a coffee / Would / like?", "Would you like a coffee?"), ("is / What time / the flight?", "What time is the flight?"), ("I / get / Where / can / a taxi?", "Where can I get a taxi?")]},
 "ex3": {"h": "3. Complete the conversation", "intro": "Fill each gap with one word. Read the conversation out loud when you finish.",
         "text": "\"Good afternoon. Where are you ___ to?\" — \"To Rome.\" — \"___ I see your passport, please?\" — \"___ you are.\" — \"Any ___ to check in?\" — \"No, only hand ___.\" — \"OK. ___ your boarding pass. Gate 8.\"",
         "ans": "flying · Can · Here · bags · luggage · Here's",
         "tip": "You give something → <em>Here you are.</em> They give you something → <em>Here's your…</em>"},
 "roleplay": {"scene": "You are at the airport, at the check-in desk.", "you": "the passenger", "partner": "Agent",
   "rounds": [("Good morning. Where are you flying to?", "your city", "To Berlin."),
              ("Can I see your passport, please?", "give it", "Here you are."),
              ("Thank you. Any bags to check in?", "how many · hand luggage", "One suitcase. And this is my hand luggage."),
              ("Would you like a window seat or an aisle seat?", "your choice · please", "An aisle seat, please."),
              ("Here's your boarding pass. Gate 15.", "ask: what time is boarding?", "Thank you. What time is boarding?"),
              ("At half past nine.", "ask: where can I get a coffee?", "And where can I get a coffee?"),
              ("There's a café next to gate 12.", "thank", "Thank you very much.")],
   "quick": [("Where are you flying to?", "To London."), ("Can I see your passport?", "Here you are."), ("Do you have any bags to check in?", "Yes, one suitcase."), ("Window or aisle?", "A window seat, please."),
             ("What time is your flight?", "At 10:40."), ("Which gate?", "Gate 22."), ("Is your flight delayed?", "Yes, two hours."), ("Excuse me, where can I get a coffee?", "There's a café next to gate 20."),
             ("Do you have hand luggage?", "Yes, one small bag."), ("Would you like a coffee?", "Yes, please. / No, thank you.")]},
 "useful": "<strong>Useful language:</strong> \"To London, please.\" · \"Here you are.\" · \"One suitcase and hand luggage.\" · \"A window seat, please.\" · \"What time is boarding?\" · \"Excuse me, where can I…?\" · \"I'm sorry, my flight is delayed.\"",
 "taskA": {"h": "Task A · Tell the story", "p": ["Tell Leo's morning at the airport in your own words. Steps: <em>six o'clock, nervous → check-in: passport, one suitcase → a window seat, gate 22 → security, coffee → DELAYED, two hours → the call to Anna → the call to the customer → \"See you at four.\"</em>"]},
 "taskB": {"h": "Task B · My last trip (2 minutes)", "p": ["Tell me about a trip: where, when, plane or train, a suitcase or hand luggage, window or aisle, and one problem. Start the timer and keep talking."]},
 "taskC": {"h": "Task C · The phone call", "p": ["Your flight is delayed and you have a meeting. Call me. Say who you are, say the problem, and ask for a new time. Then we change: I call you."]},
 "finish": ["Leo is nervous about his English. What do you do when you are nervous?", "What is the worst thing at an airport for you: the queue, the security, or the delay?", "<strong>From memory:</strong> say one question with <em>Can I…?</em> and one with <em>Would you like…?</em>"],
},
{
 "n": 7, "slug": "welcome_to_london", "title": "Welcome to London",
 "picture": ("sf_a1_07_welcome_to_london.png", "Leo at passport control in London, a border officer behind the glass, a sign reading UK BORDER.", ["Where is Leo?", "Who is he talking to?", "What does the sign say?"]),
 "strap": "Passport control, a black taxi, and the rain. The first hour in a new country.",
 "today": "answer the questions at passport control, take a taxi and pay for it, and ask the five big questions yourself. Grammar: <em>Where…? How long…? How much…? How many…?</em>",
 "warm_intro": "<strong>Warm up — five words to remember.</strong> They come from Lessons 4 and 6. <strong>Do you know it?</strong> Say what it means and use it in a sentence. <strong>Is it new?</strong> Good — learn it now. Click Reveal to check, and follow the link to read the lesson.",
 "warm": [
   ("a passport", "sf_a1_06_the_airport.html|The Airport", "What does it mean? Where is your passport now?", "a passport — the small book that says who you are; you need it to travel."),
   ("delayed", "sf_a1_06_the_airport.html|The Airport", "What does it mean? What do you do when your flight is delayed?", "delayed — late; not at the normal time."),
   ("a suitcase", "sf_a1_06_the_airport.html|The Airport", "What does it mean? Big or small — which do you take?", "a suitcase — a big bag with clothes for a trip."),
   ("nervous", "sf_a1_06_the_airport.html|The Airport", "What does it mean? When are you nervous?", "nervous — a little afraid, not calm."),
   ("a customer", "sf_a1_04_a_working_day.html|A Working Day", "What does it mean? Who is Leo's customer?", "a customer — a person who buys things from a company."),
 ],
 "words": ["a queue", "business", "a visit", "to stay", "a taxi", "an address", "a receipt", "change"],
 "meanings": ["the money you get back when you pay too much", "a line of people waiting", "the street and the number of a place", "a car with a driver; you pay for the journey",
              "work; not a holiday", "a paper that says you paid", "to be in a place for some days or nights", "a short time in a place; going to see a person or a place"],
 "key": [1, 4, 7, 6, 3, 2, 5, 0],
 "before": ["Which words are about money? Which word is about waiting?", "At passport control, what questions do they ask? Guess three."],
 "conv_intro": "Leo lands in London. Read each part. Then try the questions from memory, and answer the last one about you.",
 "parts": [
   {"h": "Part 1 — Passport control",
    "lines": [("", "Twelve thirty. The plane lands at London Heathrow. Leo walks and walks — the airport is very big. Then, a queue. A long queue. Passport control."),
              ("Officer", "Good afternoon. Passport, please."), ("Leo", "Here you are."), ("Officer", "What's the purpose of your visit?"), ("Leo", "Business. I have a meeting."),
              ("Officer", "How long are you staying?"), ("Leo", "Three days."), ("Officer", "Where are you staying?"), ("Leo", "At the Park Hotel, in the city."), ("Officer", "Thank you. Enjoy your stay.")],
    "qs": [("Why is Leo in London?", "For business. He has a meeting."), ("How long is he staying, and where?", "Three days, at the Park Hotel.")],
    "talk": "And you? When you travel, is it for business or a holiday? How long do you usually stay?"},
   {"h": "Part 2 — The taxi",
    "lines": [("", "Outside, it is raining. Of course — it's London. Leo finds a black taxi."),
              ("Leo", "The Park Hotel, please."), ("Driver", "The Park Hotel? Which one? There are two."), ("Leo", "Sorry?"), ("Driver", "Do you have the address?"),
              ("Leo", "Yes, one moment. 20 Park Street."), ("Driver", "Ah, Park Street. OK."), ("Leo", "How long is it?"), ("Driver", "Forty minutes. Maybe fifty. The traffic is bad."), ("Leo", "In London too!")],
    "qs": [("Why does the driver ask for the address?", "There are two Park Hotels."), ("How long is the journey?", "Forty or fifty minutes. The traffic is bad.")],
    "talk": "And you? Do you take taxis? Is the traffic bad in your city?"},
   {"h": "Part 3 — Paying",
    "lines": [("", "At the hotel, the taxi stops. The meter says £62."),
              ("Leo", "How much is it?"), ("Driver", "Sixty-two pounds."), ("Leo", "Can I pay by card?"), ("Driver", "Yes, of course."),
              ("Leo", "Can I have a receipt, please? For my company."), ("Driver", "Here you are. Have a good meeting."), ("Leo", "Thank you! How do you know?"), ("Driver", "The suitcase and the face. Business face!")],
    "qs": [("How much is the taxi? How does Leo pay?", "Sixty-two pounds. He pays by card."), ("What does Leo ask for? Why?", "A receipt, for his company.")],
    "talk": "And you? Do you pay by card or cash? Do you ask for receipts?"},
 ],
 "grammar_tab": "Grammar — the big questions",
 "grammar_h": "Grammar: Where…? How long…? How much…? How many…?",
 "grammar_intro": "At passport control and in a taxi, four question words do most of the work. Learn the question and the short answer together.",
 "notes": [
   "<strong>Where…?</strong> = a place. \"<em>Where</em> are you staying?\" — \"At the Park Hotel.\" · \"<em>Where</em> are you going?\" — \"To the city.\"",
   "<strong>How long…?</strong> = time. \"<em>How long</em> are you staying?\" — \"Three days.\" · \"<em>How long</em> is the journey?\" — \"Forty minutes.\"",
   "<strong>How much…?</strong> = money. \"<em>How much</em> is it?\" — \"Sixty pounds.\" · <strong>How many…?</strong> = a number. \"<em>How many</em> bags?\" — \"Two.\"",
   "<strong>Your plans:</strong> \"I'm <em>staying</em> at the Park Hotel.\" \"I'm <em>leaving</em> on Friday.\" \"I'm here <em>for</em> business / <em>for</em> a holiday / <em>for</em> three days.\"",
 ],
 "ex1": {"h": "1. Which question word?", "intro": "Look at the answer. Complete the question with <em>Where</em>, <em>How long</em>, <em>How much</em> or <em>How many</em>.",
         "items": [("___ are you staying? — At the Park Hotel.", "Where"), ("___ are you staying? — Three days.", "How long"), ("___ is it? — Sixty pounds.", "How much"), ("___ bags do you have? — Two.", "How many")]},
 "ex2": {"h": "2. Make the sentence", "intro": "Put the words in order. Then say the sentence out loud.",
         "items": [("staying / are / you / Where?", "Where are you staying?"), ("here / I'm / business / for", "I'm here for business."), ("pay / Can / by card / I?", "Can I pay by card?"), ("a receipt / I / have / Can / please?", "Can I have a receipt, please?")]},
 "ex3": {"h": "3. Complete the conversation", "intro": "Fill each gap with one word. Read the conversation out loud when you finish.",
         "text": "\"What's the ___ of your visit?\" — \"Business. I have a ___.\" — \"How ___ are you staying?\" — \"Two nights. I'm ___ at the City Hotel.\" — \"Do you have the ___?\" — \"Yes: 5 King Street.\"",
         "ans": "purpose · meeting · long · staying · address",
         "tip": "<em>How long?</em> → days or nights. <em>Where?</em> → a place."},
 "roleplay": {"scene": "You arrive in a new country. Passport control.", "you": "the traveller", "partner": "Officer",
   "rounds": [("Good afternoon. Passport, please.", "give it", "Here you are."),
              ("What's the purpose of your visit?", "business or holiday · one detail", "Business. I have two meetings."),
              ("How long are you staying?", "days", "Four days."),
              ("Where are you staying?", "hotel · city", "At the Central Hotel, in the city."),
              ("Is this your first time here?", "yes or no", "No, my second time."),
              ("Thank you. Enjoy your stay.", "thank", "Thank you.")],
   "quick": [("Where are you staying?", "At the Park Hotel."), ("How long are you staying?", "Three days."), ("What's the purpose of your visit?", "Business."), ("How much is the taxi?", "Forty pounds."),
             ("How many bags do you have?", "One."), ("Can I pay by card?", "Yes, of course."), ("Do you have the address?", "Yes. 20 Park Street."), ("How long is the journey?", "Thirty minutes."),
             ("When are you leaving?", "On Friday."), ("Is this your first time in London?", "Yes, it is.")]},
 "useful": "<strong>Useful language:</strong> \"I'm here for business.\" · \"I'm staying at… for three days.\" · \"Do you have the address?\" · \"How long is it?\" · \"How much is it?\" · \"Can I pay by card?\" · \"Can I have a receipt, please?\"",
 "taskA": {"h": "Task A · Tell the story", "p": ["Tell Leo's first hour in London in your own words. Steps: <em>the plane lands → a long queue → the officer's three questions → the rain → the taxi and the address → forty minutes → £62, card, receipt → \"business face\".</em>"]},
 "taskB": {"h": "Task B · Your trip (2 minutes)", "p": ["You arrive in a new city. Tell me: the airport, passport control, the taxi, the hotel. Say how long, how much and where. Start the timer and keep talking."]},
 "taskC": {"h": "Task C · In the taxi", "p": ["I am the driver. Tell me where to go, give me the address, ask how long it is, ask how much, and ask for a receipt. Then we change: you are the driver."]},
 "finish": ["Passport control: are you calm or nervous? Why?", "Taxi or train from the airport? Which is better in your city?", "<strong>From memory:</strong> say the four question words from today, each with a short answer."],
},
{
 "n": 8, "slug": "the_hotel", "title": "The Hotel",
 "picture": ("sf_a1_08_the_hotel.png", "Leo at the hotel reception; the receptionist hands him a key card; a sign reads RECEPTION and a board shows 512.", ["Where is Leo?", "What does the woman give him?", "What number can you see?"]),
 "strap": "A reservation, your name spelled out, a key card and the fifth floor. Check in like you do it every week.",
 "today": "check in at a hotel: give your name, spell it, understand the room number and the floor, and ask about breakfast and wifi. Grammar: spelling, numbers and floors.",
 "warm_intro": "<strong>Warm up — five words to remember.</strong> They come from Lessons 6 and 7. <strong>Do you know it?</strong> Say what it means and use it in a sentence. <strong>Is it new?</strong> Good — learn it now. Click Reveal to check, and follow the link to read the lesson.",
 "warm": [
   ("to stay", "sf_a1_07_welcome_to_london.html|Welcome to London", "What does it mean? Where do you stay in a new city?", "to stay — to be in a place for some days or nights."),
   ("a taxi", "sf_a1_07_welcome_to_london.html|Welcome to London", "What does it mean? How much is a taxi in your city?", "a taxi — a car with a driver; you pay for the journey."),
   ("a receipt", "sf_a1_07_welcome_to_london.html|Welcome to London", "What does it mean? Say the question: Can I have…?", "a receipt — a paper that says you paid."),
   ("a queue", "sf_a1_07_welcome_to_london.html|Welcome to London", "What does it mean? Where are the queues long?", "a queue — a line of people waiting."),
   ("a boarding pass", "sf_a1_06_the_airport.html|The Airport", "What does it mean? Paper or phone — which do you use?", "a boarding pass — the paper or phone ticket you show to get on the plane."),
 ],
 "words": ["a reservation", "reception", "the lift", "a key card", "breakfast", "the password", "to spell", "a floor"],
 "meanings": ["the first meal of the day", "a small room that goes up and down in a building", "a level of a building: first, second, third…", "to say the letters of a word: L-E-O",
              "the desk in a hotel where you check in", "the secret word for the wifi or a computer", "a room you book before you arrive", "the card that opens your room door"],
 "key": [6, 4, 1, 7, 0, 5, 3, 2],
 "before": ["Which words are things? Which words are places in the hotel?", "At a hotel reception, what questions do they ask you? Guess three."],
 "conv_intro": "Leo arrives at the Park Hotel. Read each part. Then try the questions from memory, and answer the last one about you.",
 "parts": [
   {"h": "Part 1 — I have a reservation",
    "lines": [("", "The Park Hotel. Warm, quiet, a big clock in the lobby. Leo goes to reception."),
              ("Receptionist", "Good afternoon. Welcome to the Park Hotel."), ("Leo", "Good afternoon. I have a reservation."), ("Receptionist", "What's the name, please?"), ("Leo", "Leo Navarro."),
              ("Receptionist", "Can you spell that?"), ("Leo", "N-A-V-A-R-R-O."), ("Receptionist", "Thank you. Three nights?"), ("Leo", "Yes, three nights."), ("Receptionist", "Can I see your passport, please?")],
    "qs": [("What does the receptionist ask Leo to spell?", "His family name: Navarro."), ("How many nights is he staying?", "Three nights.")],
    "talk": "And you? Spell your family name. Is it easy or hard for English people?"},
   {"h": "Part 2 — Room 512",
    "lines": [("Receptionist", "Here's your key card. Room 512, on the fifth floor. The lift is on the right."), ("Leo", "Sorry — five, one, two?"), ("Receptionist", "Yes. Five, one, two."),
              ("Leo", "What time is breakfast?"), ("Receptionist", "From seven to ten, in the restaurant on the ground floor."), ("Leo", "And is there wifi?"), ("Receptionist", "Yes. The password is on the card."), ("Leo", "Thank you very much."),
              ("", "Leo takes the lift. Fifth floor. Room 512. The card — click. A big bed, a window, the rain. He sits down. He is very tired.")],
    "qs": [("What floor is the room on?", "The fifth floor. Room 512."), ("What time is breakfast, and where?", "From seven to ten, in the restaurant on the ground floor.")],
    "talk": "And you? What do you ask at a hotel? What is important for you: breakfast, wifi, a quiet room?"},
   {"h": "Part 3 — The call home",
    "lines": [("", "At six, Leo calls Carla."),
              ("Leo", "Hi. I'm at the hotel."), ("Carla", "How is it?"), ("Leo", "Nice. Small room, big bed. It's raining."), ("Carla", "Of course it's raining. It's London."),
              ("Leo", "The meeting is tomorrow at four."), ("Carla", "Are you nervous?"), ("Leo", "A little."), ("Carla", "Your English is good, Leo. Say hello, smile, and ask questions."), ("Leo", "Say hello, smile, ask questions. OK."), ("Carla", "And sleep!"), ("Leo", "Yes, boss.")],
    "qs": [("When is the meeting?", "Tomorrow at four."), ("What is Carla's advice?", "Say hello, smile, ask questions. And sleep.")],
    "talk": "And you? Are you nervous before a meeting? What helps you?"},
 ],
 "grammar_tab": "Grammar — spelling and numbers",
 "grammar_h": "Grammar: spelling, numbers and floors",
 "grammar_intro": "At a hotel you say your name letter by letter, and you hear room numbers, floors and times. Slow and clear wins.",
 "notes": [
   "<strong>Can you spell that?</strong> Say one letter at a time: \"N-A-V-A-R-R-O.\" Two letters the same? \"double R\". The hard letters: <em>A</em> (ay), <em>E</em> (ee), <em>I</em> (eye), <em>G</em> (jee), <em>J</em> (jay), <em>R</em> (ar), <em>W</em> (double-u), <em>Y</em> (why).",
   "<strong>Room numbers:</strong> say the numbers one by one: room 512 = \"five one two\", room 308 = \"three oh eight\". Check: \"Sorry — five, one, two?\"",
   "<strong>Floors:</strong> the <em>ground</em> floor (0), the <em>first</em> floor (1), <em>second</em> (2), <em>third</em> (3), <em>fourth</em> (4), <em>fifth</em> (5), <em>tenth</em> (10). \"My room is <em>on the</em> fifth floor.\"",
   "<strong>Times:</strong> \"Breakfast is <em>from</em> seven <em>to</em> ten.\" \"Check-out is <em>at</em> eleven.\" Questions: \"What time is breakfast?\" \"What time is check-out?\"",
 ],
 "ex1": {"h": "1. Which floor?", "intro": "Write the floor. Careful: the first number of the room is the floor.",
         "items": [("Room 210 is on the ___ floor.", "second"), ("Room 512 is on the ___ floor.", "fifth"), ("Room 105 is on the ___ floor.", "first"), ("The restaurant is on the ___ floor (0).", "ground")]},
 "ex2": {"h": "2. Make the sentence", "intro": "Put the words in order. Then say the sentence out loud.",
         "items": [("spell / Can / that / you?", "Can you spell that?"), ("a reservation / I / have", "I have a reservation."), ("breakfast / What time / is?", "What time is breakfast?"), ("the fifth / My room / on / is / floor", "My room is on the fifth floor.")]},
 "ex3": {"h": "3. Complete the conversation", "intro": "Fill each gap with one word. Read the conversation out loud when you finish — and spell the name.",
         "text": "\"Good evening. I have a ___.\" — \"What's the ___, please?\" — \"Kowalski. K-O-W-A-L-S-K-I.\" — \"Thank you. Here's your key ___. Room 308, on the ___ floor.\" — \"What time is ___?\" — \"From seven to ten.\"",
         "ans": "reservation · name · card · third · breakfast",
         "tip": "Room 3-0-8 → the <em>third</em> floor."},
 "roleplay": {"scene": "You arrive at a hotel in the evening. Reception.", "you": "the guest", "partner": "Receptionist",
   "rounds": [("Good evening. Welcome to the Central Hotel.", "say hello · I have a reservation", "Good evening. I have a reservation."),
              ("What's the name, please?", "your name", "Kowalski. Adam Kowalski."),
              ("Can you spell that?", "spell your family name", "K-O-W-A-L-S-K-I."),
              ("Thank you. How many nights?", "number", "Two nights."),
              ("Can I see your passport, please?", "give it", "Here you are."),
              ("Here's your key card. Room 407, on the fourth floor.", "check the number · ask: breakfast?", "Four, oh, seven? Thank you. What time is breakfast?"),
              ("From seven to ten, on the ground floor.", "ask: wifi?", "And is there wifi?"),
              ("Yes, the password is on the card. Enjoy your stay.", "thank", "Thank you very much.")],
   "quick": [("What's the name, please?", "Navarro. Leo Navarro."), ("Can you spell that?", "N-A-V-A-R-R-O."), ("How many nights?", "Three nights."), ("What floor is room 512 on?", "The fifth floor."),
             ("What time is breakfast?", "From seven to ten."), ("Is there wifi?", "Yes. The password is on the card."), ("Where is the lift?", "On the right."), ("What time is check-out?", "At eleven."),
             ("Spell your city.", "M-I-L-A-N."), ("Say your room number: 308.", "Three, oh, eight.")]},
 "useful": "<strong>Useful language:</strong> \"I have a reservation.\" · \"Can you spell that?\" · \"N-A-V-A-R-R-O.\" · \"Sorry — five, one, two?\" · \"on the fifth floor\" · \"What time is breakfast?\" · \"Is there wifi?\"",
 "taskA": {"h": "Task A · Tell the check-in", "p": ["Tell Leo's check-in in your own words. Steps: <em>reception → the reservation → spell Navarro → three nights → key card, 512, fifth floor → breakfast seven to ten → wifi → the room, the bed, the rain → the call to Carla: say hello, smile, ask questions.</em>"]},
 "taskB": {"h": "Task B · Spell it (2 minutes)", "p": ["Spell out loud: your family name, your street, your company, your city, and your email address. Then say three numbers: your room number at the last hotel, your phone number, your car number."]},
 "taskC": {"h": "Task C · Ask me", "p": ["I am at your hotel. Ask me the reception questions: name, spell it, how many nights, passport. Then give me my room: number, floor, breakfast time, wifi."]},
 "finish": ["What is a good hotel for you: big or small, in the city or quiet?", "Carla says: \"Say hello, smile, ask questions.\" Is this good advice for a meeting in English?", "<strong>From memory:</strong> spell your family name, and say the floor of room 612."],
},
{
 "n": 9, "slug": "a_problem_and_the_way", "title": "A Problem, and the Way",
 "picture": ("sf_a1_09_a_problem_and_the_way.png", "Leo on a London street corner with his phone, a bank on the corner, a sign reading KING STREET, a station opposite.", ["Where is Leo?", "What can you see on the street?", "Is he lost? Guess."]),
 "strap": "No hot water, no towels, and then: how do I get to King Street? Say the problem, and find the way.",
 "today": "say when something is wrong in a hotel room, and ask for and understand directions in the street. Grammar: <em>There's a problem with… / It doesn't work</em>, and <em>Go straight on, turn left, take the second right</em>.",
 "warm_intro": "<strong>Warm up — five words to remember.</strong> They come from Lessons 7 and 8. <strong>Do you know it?</strong> Say what it means and use it in a sentence. <strong>Is it new?</strong> Good — learn it now. Click Reveal to check, and follow the link to read the lesson.",
 "warm": [
   ("reception", "sf_a1_08_the_hotel.html|The Hotel", "What does it mean? What do you say at reception?", "reception — the desk in a hotel where you check in."),
   ("the lift", "sf_a1_08_the_hotel.html|The Hotel", "What does it mean? Lift or stairs — which do you take?", "the lift — a small room that goes up and down in a building."),
   ("to spell", "sf_a1_08_the_hotel.html|The Hotel", "What does it mean? Spell your name.", "to spell — to say the letters of a word."),
   ("an address", "sf_a1_07_welcome_to_london.html|Welcome to London", "What does it mean? Say your work address.", "an address — the street and the number of a place."),
   ("business", "sf_a1_07_welcome_to_london.html|Welcome to London", "What does it mean? Say: I'm here for…", "business — work; not a holiday."),
 ],
 "words": ["a shower", "a towel", "hot water", "to work (a machine)", "straight on", "to turn", "opposite", "the corner"],
 "meanings": ["to go left or right", "not left, not right: in front of you", "on the other side of the street", "the place where two streets meet",
              "water that is not cold, for a shower", "where you wash your body, standing, in the bathroom", "a machine works = it is OK; it doesn't work = it is broken", "a cloth to dry your body"],
 "key": [5, 7, 4, 6, 1, 0, 2, 3],
 "before": ["Which words are in the bathroom? Which words are in the street?", "A hotel room. What can go wrong? Guess three problems."],
 "conv_intro": "Wednesday: the day of the meeting. Read each part. Then try the questions from memory, and answer the last one about you.",
 "parts": [
   {"h": "Part 1 — No hot water",
    "lines": [("", "Wednesday morning. Leo wants a shower before the big day. Cold. Cold! Only cold water. And there are no towels."),
              ("Leo", "Hello, reception? This is room 512. There's a problem with the shower. There's no hot water."), ("Receptionist", "I'm sorry, sir. I'll send someone now."),
              ("Leo", "And there are no towels in the room."), ("Receptionist", "No towels? I'm very sorry. Two minutes."), ("Leo", "Thank you."),
              ("", "Five minutes later: hot water, four towels, and a small box of chocolates. \"Sorry,\" says the card.")],
    "qs": [("What are the two problems?", "No hot water in the shower, and no towels."), ("What does the hotel send?", "Someone to fix it, four towels, and a box of chocolates.")],
    "talk": "And you? Do you have problems in hotels? What do you say?"},
   {"h": "Part 2 — How do I get to King Street?",
    "lines": [("", "Three o'clock. The customer's office is at 40 King Street. Leo asks at reception."),
              ("Leo", "Excuse me. How do I get to King Street?"), ("Receptionist", "It's very near. Go straight on, then turn left at the bank."), ("Leo", "Left at the bank."),
              ("Receptionist", "Then take the second right. That's King Street. The office is opposite the station."), ("Leo", "Second right, opposite the station. How long is it?"),
              ("Receptionist", "Five minutes on foot."), ("Leo", "Perfect. Thank you.")],
    "qs": [("Where is the office?", "On King Street, opposite the station."), ("How long does it take?", "Five minutes on foot.")],
    "talk": "And you? Do you ask people for directions, or do you use your phone?"},
   {"h": "Part 3 — Number 40",
    "lines": [("", "Leo walks. Straight on. The bank — turn left. First right? No — second right. King Street. And there, opposite the station: a glass door, number 40. He is early. He is nervous. He remembers Carla: say hello, smile, ask questions."),
              ("Leo", "Good afternoon. I'm Leo Navarro. I have a meeting with Mr Hill at four."), ("Assistant", "Mr Navarro. Welcome. Please, sit down. Would you like a coffee?"), ("Leo", "Yes, please. Black, no sugar.")],
    "qs": [("Is Leo late or early?", "Early."), ("What does he remember?", "Carla's advice: say hello, smile, ask questions.")],
    "talk": "And you? Are you usually early or late? Do you drink coffee before a meeting?"},
 ],
 "grammar_tab": "Grammar — problems and directions",
 "grammar_h": "Grammar: There's a problem with… / Go straight on",
 "grammar_intro": "Two small toolkits today: one for when something is wrong, one for finding the way.",
 "notes": [
   "<strong>Problems:</strong> \"<em>There's a problem with</em> the shower.\" \"<em>There's no</em> hot water.\" \"<em>There are no</em> towels.\" \"The TV <em>doesn't work</em>.\" Answer you hear: \"I'm sorry. I'll send someone.\"",
   "<strong>Ask the way:</strong> \"<em>How do I get to</em> King Street?\" \"<em>Where is</em> the station?\" \"<em>Is it far?</em>\" — \"No, five minutes on foot.\"",
   "<strong>Directions</strong> use the verb with no <em>you</em>: \"<em>Go</em> straight on.\" \"<em>Turn</em> left at the bank.\" \"<em>Take</em> the second right.\" \"<em>It's</em> on the left.\"",
   "<strong>Where things are:</strong> <em>opposite</em> the station · <em>next to</em> the bank · <em>on the corner</em> · <em>at the end of</em> the street · <em>on the left / on the right</em>",
 ],
 "ex1": {"h": "1. Which word?", "intro": "Complete each direction with <em>Go</em>, <em>Turn</em>, <em>Take</em> or <em>opposite</em>.",
         "items": [("___ straight on.", "Go"), ("___ left at the bank.", "Turn"), ("___ the second right.", "Take"), ("The office is ___ the station.", "opposite")]},
 "ex2": {"h": "2. Make the sentence", "intro": "Put the words in order. Then say the sentence out loud.",
         "items": [("hot water / There's / no", "There's no hot water."), ("doesn't / The shower / work", "The shower doesn't work."), ("get / How / I / do / to the station?", "How do I get to the station?"), ("the / Take / right / first", "Take the first right.")]},
 "ex3": {"h": "3. Complete the conversation", "intro": "Fill each gap with one word. Read the conversation out loud when you finish.",
         "text": "\"Hello, reception? There's a ___ with the TV. It doesn't ___.\" — \"I'm ___, sir. I'll send someone.\" — \"Thank you. And how do I ___ to the bank?\" — \"Go ___ on, and it's on the left, ___ the café.\"",
         "ans": "problem · work · sorry · get · straight · opposite",
         "tip": "<em>doesn't work</em> = broken. <em>opposite</em> = on the other side."},
 "roleplay": {"scene": "Morning in your hotel room. Two problems. Then you need the station.", "you": "the guest", "partner": "Receptionist",
   "rounds": [("Reception, good morning.", "your room number · problem 1", "Good morning. This is room 210. There's a problem with the shower. There's no hot water."),
              ("I'm sorry. I'll send someone now. Anything else?", "problem 2", "Yes. There are no towels in the room."),
              ("I'm very sorry. Five minutes.", "thank · ask the way to the station", "Thank you. And how do I get to the station?"),
              ("Go straight on, turn right at the church, and it's opposite the park.", "say it back", "Straight on, right at the church, opposite the park."),
              ("That's right. It's ten minutes on foot.", "ask: is it far? / thank", "Ten minutes. Thank you very much.")],
   "quick": [("How do I get to the station?", "Go straight on and turn left."), ("Is it far?", "No, five minutes on foot."), ("Where is the bank?", "It's opposite the hotel."), ("What's the problem?", "There's no hot water."),
             ("Does the TV work?", "No, it doesn't work."), ("Where is the office?", "On King Street, opposite the station."), ("Which right — the first or the second?", "The second right."), ("Where is the café?", "On the corner, next to the bank."),
             ("Are you early or late?", "I'm early."), ("Would you like a coffee?", "Yes, please. Black, no sugar.")]},
 "useful": "<strong>Useful language:</strong> \"There's a problem with…\" · \"There's no… / There are no…\" · \"It doesn't work.\" · \"How do I get to…?\" · \"Go straight on. Turn left. Take the second right.\" · \"It's opposite / next to…\" · \"Is it far?\"",
 "taskA": {"h": "Task A · Tell the story", "p": ["Tell Leo's Wednesday in your own words. Steps: <em>cold shower, no towels → the call to reception → chocolates → three o'clock, King Street → straight on, left at the bank, second right → opposite the station → number 40, early, nervous → hello, smile, coffee.</em>"]},
 "taskB": {"h": "Task B · Your street (2 minutes)", "p": ["Give me directions from your home to a shop, a café or the station. Use <em>go straight on, turn, take the first / second, opposite, next to</em>. Start the timer and keep talking."]},
 "taskC": {"h": "Task C · Ask me the way", "p": ["I am at your hotel reception. Ask me the way to three places: the station, a bank, a good restaurant. Say my directions back to me each time."]},
 "finish": ["In a hotel, do you say when something is wrong, or do you say nothing? Why?", "Phone map or asking a person — which is better in a new city?", "<strong>From memory:</strong> give three directions with <em>go</em>, <em>turn</em> and <em>take</em>."],
},
{
 "n": 10, "slug": "dinner_with_the_customer", "title": "Dinner with the Customer",
 "picture": ("sf_a1_10_dinner_with_the_customer.png", "Leo and Mr Hill at a restaurant table by the river; a waiter brings the menu.", ["Where are they?", "Who is the man with Leo? Guess.", "What is on the table?"]),
 "strap": "A table for two, the menu, the starter, the main course, and the bill. The meeting went well — now dinner.",
 "today": "order food and drink in a restaurant, understand the waiter's questions, and ask for the bill. Grammar: <em>I'll have…</em> and <em>Could we have…?</em>",
 "warm_intro": "<strong>Warm up — five words to remember.</strong> They come from Lessons 4, 8 and 9. <strong>Do you know it?</strong> Say what it means and use it in a sentence. <strong>Is it new?</strong> Good — learn it now. Click Reveal to check, and follow the link to read the lesson.",
 "warm": [
   ("a towel", "sf_a1_09_a_problem_and_the_way.html|A Problem, and the Way", "What does it mean? Say the problem: There are no…", "a towel — a cloth to dry your body."),
   ("opposite", "sf_a1_09_a_problem_and_the_way.html|A Problem, and the Way", "What does it mean? What is opposite your home?", "opposite — on the other side of the street."),
   ("straight on", "sf_a1_09_a_problem_and_the_way.html|A Problem, and the Way", "What does it mean? Say a direction with it.", "straight on — not left, not right: in front of you."),
   ("breakfast", "sf_a1_08_the_hotel.html|The Hotel", "What does it mean? What do you have for breakfast?", "breakfast — the first meal of the day."),
   ("a meeting", "sf_a1_04_a_working_day.html|A Working Day", "What does it mean? How was Leo's meeting? Guess.", "a meeting — people talk about work together, at a table."),
 ],
 "words": ["a table", "the menu", "a starter", "a main course", "a dessert", "the bill", "to order", "delicious"],
 "meanings": ["the paper that says how much you pay", "very, very good (food)", "the small first dish", "the list of food in a restaurant",
              "the big dish in the middle of the meal", "to say to the waiter what you want", "the sweet dish at the end", "you sit at it to eat"],
 "key": [7, 3, 2, 4, 6, 0, 5, 1],
 "before": ["Say the three parts of a meal, in order.", "A business dinner. Who pays? Guess."],
 "conv_intro": "The meeting was good. Now Mr Hill takes Leo to dinner. Read each part. Then try the questions from memory, and answer the last one about you.",
 "parts": [
   {"h": "Part 1 — A table for two",
    "lines": [("", "Seven o'clock. The meeting was good. Very good. Now Mr Hill takes Leo to dinner: a small Italian restaurant near the river."),
              ("Waiter", "Good evening. Do you have a reservation?"), ("Mr Hill", "Yes. Hill, a table for two."), ("Waiter", "This way, please. Here's the menu. Would you like something to drink?"),
              ("Mr Hill", "A glass of red wine, please. Leo?"), ("Leo", "Just water for me, please. Sparkling.")],
    "qs": [("How many people are at the table?", "Two: Leo and Mr Hill."), ("What does Leo drink?", "Sparkling water. Mr Hill has a glass of red wine.")],
    "talk": "And you? Wine or water at a business dinner? Why?"},
   {"h": "Part 2 — Are you ready to order?",
    "lines": [("Waiter", "Are you ready to order?"), ("Mr Hill", "Yes. For the starter, the soup, please. And then the fish."), ("Waiter", "And for you, sir?"),
              ("Leo", "I'll have the salad to start. And the pasta, please."), ("Waiter", "The pasta with tomato or with mushrooms?"), ("Leo", "With tomato, please."), ("Waiter", "Thank you."),
              ("", "The food comes. It's delicious. Mr Hill talks about London, about football, about his children. Leo understands almost everything. He asks questions. He smiles.")],
    "qs": [("What does Leo order?", "The salad to start, then the pasta with tomato."), ("What do they talk about?", "London, football, and Mr Hill's children.")],
    "talk": "And you? What do you usually order: meat, fish or pasta? A starter, or just the main course?"},
   {"h": "Part 3 — The bill",
    "lines": [("Mr Hill", "Would you like a dessert?"), ("Leo", "No, thank you. Just a coffee."), ("Mr Hill", "Two coffees, please. And the bill."), ("Leo", "Please, let me pay."),
              ("Mr Hill", "No, no. You are in London. Next time, in your city."), ("Leo", "OK. Next time, my city. Thank you."),
              ("", "Outside, the rain has stopped. Leo walks back to the hotel and calls Carla. \"How was it?\" \"Good,\" he says. \"Very good.\" And then, in English, because he can: \"It was delicious.\"")],
    "qs": [("Who pays? Why?", "Mr Hill. Leo is in London; next time Leo pays, in his city."), ("What does Leo say at the end, in English?", "\"It was delicious.\"")],
    "talk": "And you? Who pays at a business dinner in your country? What do you say at the end of a good dinner?"},
 ],
 "grammar_tab": "Grammar — I'll have… / Could we have…?",
 "grammar_h": "Grammar: ordering food",
 "grammar_intro": "In a restaurant you need one shape for ordering and one shape for asking. Everything else is the menu.",
 "notes": [
   "<strong>I'll have + the food.</strong> \"<em>I'll have</em> the fish.\" \"<em>I'll have</em> the soup to start.\" (I'll = I will — but here it just means: this is my order.)",
   "<strong>For the starter / for the main course:</strong> \"<em>For the starter</em>, the salad. <em>For the main course</em>, the chicken.\" · No starter? \"Just the main course, please.\"",
   "<strong>Could I / Could we have…?</strong> = asking, very politely: \"<em>Could we have</em> the bill, please?\" \"<em>Could I have</em> some water?\" \"<em>Could we have</em> a table by the window?\"",
   "<strong>with / without · a glass of / a bottle of:</strong> \"pasta <em>with</em> tomato\" · \"coffee <em>without</em> sugar\" · \"<em>a glass of</em> wine\" · \"<em>a bottle of</em> water\" · \"<em>a cup of</em> tea\"",
 ],
 "ex1": {"h": "1. Which word?", "intro": "Complete each sentence with <em>I'll</em>, <em>Could</em>, <em>of</em> or <em>with</em>.",
         "items": [("___ have the soup, please.", "I'll"), ("___ we have the bill, please?", "Could"), ("A glass ___ water, please.", "of"), ("Pasta ___ tomato, please.", "with")]},
 "ex2": {"h": "2. Make the sentence", "intro": "Put the words in order. Then say the sentence out loud.",
         "items": [("have / I'll / the fish", "I'll have the fish."), ("ready / Are / to order / you?", "Are you ready to order?"), ("the bill / Could / have / we / please?", "Could we have the bill, please?"), ("for / two / A table / please", "A table for two, please.")]},
 "ex3": {"h": "3. Complete the conversation", "intro": "Fill each gap with one word. Read the conversation out loud when you finish.",
         "text": "\"Are you ___ to order?\" — \"Yes. For the ___, the soup. And then the chicken.\" — \"And to ___?\" — \"A ___ of water, please.\" — \"Would you like a ___?\" — \"No, thank you. Just the ___, please.\"",
         "ans": "ready · starter · drink · glass · dessert · bill",
         "tip": "starter → main course → dessert → the bill."},
 "roleplay": {"scene": "A restaurant. You are with a colleague, and you order for yourself.", "you": "the guest", "partner": "Waiter",
   "rounds": [("Good evening. Do you have a reservation?", "your name · a table for two", "Yes. Kowalski, a table for two."),
              ("This way, please. Here's the menu. Something to drink?", "your drink", "A bottle of sparkling water, please."),
              ("Are you ready to order?", "starter + main course", "Yes. For the starter, the salad. And then the fish."),
              ("With rice or with potatoes?", "choose", "With potatoes, please."),
              ("Would you like a dessert?", "yes or no · coffee?", "No, thank you. Just a coffee, please."),
              ("Anything else?", "ask for the bill", "Could we have the bill, please?")],
   "quick": [("Do you have a reservation?", "Yes. Navarro, a table for two."), ("Would you like something to drink?", "A glass of water, please."), ("Are you ready to order?", "Yes. I'll have the pasta."), ("With tomato or with mushrooms?", "With tomato, please."),
             ("Would you like a starter?", "Yes, the soup, please."), ("Would you like a dessert?", "No, thank you. Just a coffee."), ("How is the food?", "It's delicious."), ("Anything else?", "Could we have the bill, please?"),
             ("Who is paying?", "I am. Please, let me pay."), ("Was the dinner good?", "Yes, very good. Delicious.")]},
 "useful": "<strong>Useful language:</strong> \"A table for two, please.\" · \"I'll have…\" · \"For the starter… / For the main course…\" · \"With tomato, please.\" · \"Could we have the bill, please?\" · \"It's delicious.\" · \"Please, let me pay.\"",
 "taskA": {"h": "Task A · Tell the dinner", "p": ["Tell the dinner in your own words. Steps: <em>seven o'clock, the meeting was good → a table for two → wine and water → soup and fish, salad and pasta → delicious, football, children → no dessert, two coffees → the bill: \"Next time, in your city\" → the call to Carla: \"It was delicious.\"</em>"]},
 "taskB": {"h": "Task B · My favourite restaurant (2 minutes)", "p": ["Tell me about a restaurant you like: where it is, what you order, a starter or not, what you drink, who pays. Start the timer and keep talking."]},
 "taskC": {"h": "Task C · Order from me", "p": ["I am the waiter. Order a full dinner: drink, starter, main course with a choice, dessert or coffee, and the bill. Then we change: you are the waiter, and you ask me the questions."]},
 "finish": ["Business dinner: is it work, or is it fun? What do you talk about?", "In your country, who pays: the host or the guest? Is it polite to say \"Let me pay\"?", "<strong>From memory:</strong> order a starter and a main course, then ask for the bill."],
},
{
 "n": 11, "slug": "the_meeting", "title": "The Meeting",
 "picture": ("sf_a1_11_the_meeting.png", "Leo shakes hands with Mr Hill in a bright London office; Sarah and Tom at the table; a screen reads JANUARY.", ["Where is Leo?", "How many people can you see?", "What does the screen say? Guess why."]),
 "strap": "Introductions, three facts about your company, and a yes. The meeting Leo flew to London for.",
 "today": "introduce people, say three simple facts about your company, and understand a decision. Grammar: <em>we / our</em>, <em>This is…</em>, and <em>Let's…</em>",
 "warm_intro": "<strong>Warm up — five words to remember.</strong> They come from Lessons 4, 9 and 10. <strong>Do you know it?</strong> Say what it means and use it in a sentence. <strong>Is it new?</strong> Good — learn it now. Click Reveal to check, and follow the link to read the lesson.",
 "warm": [
   ("the bill", "sf_a1_10_dinner_with_the_customer.html|Dinner with the Customer", "What does it mean? Ask for it politely.", "the bill — the paper that says how much you pay. \"Could we have the bill, please?\""),
   ("delicious", "sf_a1_10_dinner_with_the_customer.html|Dinner with the Customer", "What does it mean? What is delicious in your country?", "delicious — very, very good (food)."),
   ("to order", "sf_a1_10_dinner_with_the_customer.html|Dinner with the Customer", "What does it mean? Order a main course now.", "to order — to say to the waiter what you want."),
   ("a towel", "sf_a1_09_a_problem_and_the_way.html|A Problem, and the Way", "What does it mean? Say the problem: There are no…", "a towel — a cloth to dry your body."),
   ("a customer", "sf_a1_04_a_working_day.html|A Working Day", "What does it mean? How many customers does your company have?", "a customer — a person who buys things from a company."),
 ],
 "words": ["a colleague", "a manager", "an office", "a team", "a price", "a contract", "to agree", "to start"],
 "meanings": ["to say yes together", "the money you pay for something", "the people you work with, together", "the person who is the boss of a team",
              "a paper both companies sign: the deal", "to begin", "a person who works with you", "the rooms where a company works"],
 "key": [6, 3, 7, 2, 1, 4, 0, 5],
 "before": ["Which words are people? Which words are about money and paper?", "A first meeting with a new customer. What do you say about your company? Say three things."],
 "conv_intro": "Four o'clock, 40 King Street. Read each part. Then try the questions from memory, and answer the last one about you.",
 "parts": [
   {"h": "Part 1 — This is Sarah",
    "lines": [("", "Mr Hill's office is on the third floor, with a big window and a view of the river. Two people are waiting."),
              ("Mr Hill", "Leo, welcome! This is Sarah, our manager. And this is Tom, from our team."), ("Leo", "Nice to meet you, Sarah. Nice to meet you, Tom."), ("Sarah", "Nice to meet you too. How was your flight?"),
              ("Leo", "Long. And late! But I'm here."), ("Tom", "Would you like a coffee, or tea?"), ("Leo", "Coffee, please. Black.")],
    "qs": [("Who are Sarah and Tom?", "Sarah is the manager. Tom is from the team."), ("What does Leo say about his flight?", "Long, and late. But he is here.")],
    "talk": "And you? When you meet people at work, what do you say first?"},
   {"h": "Part 2 — Tell us about your company",
    "lines": [("Mr Hill", "So, Leo. Tell us about your company."), ("Leo", "We have a small company. Forty people. Our office is in the city, near the port. We work with companies in Spain, France and Italy."),
              ("Sarah", "How many customers do you have?"), ("Leo", "About two hundred. Small and big."), ("Tom", "And why London?"), ("Leo", "Because you are a good company. And because I like rain."),
              ("", "Everyone laughs. Leo relaxes. Say hello, smile, ask questions.")],
    "qs": [("How many people are in Leo's company? Where is the office?", "Forty people. The office is in the city, near the port."), ("How many customers does Leo have?", "About two hundred, small and big.")],
    "talk": "And you? Tell me about your company or your work: how many people, where, who are the customers?"},
   {"h": "Part 3 — Let's start in January",
    "lines": [("Mr Hill", "The price is good. The dates are good. Let's start in January."), ("Leo", "January is perfect."), ("Sarah", "We'll send the contract on Monday."),
              ("Leo", "Thank you. Thank you very much."), ("Mr Hill", "No — thank you, Leo. Now: dinner?"),
              ("", "Five thirty. One hour and a half, in English. Leo looks at the river. He did it.")],
    "qs": [("When do they start?", "In January."), ("What will Sarah send, and when?", "The contract, on Monday.")],
    "talk": "And you? What is a good meeting for you? What is a bad meeting?"},
 ],
 "grammar_tab": "Grammar — we, our / This is…",
 "grammar_h": "Grammar: we, our / This is… / Let's…",
 "grammar_intro": "In a meeting you speak for your company, not only for you. That means <em>we</em> and <em>our</em>.",
 "notes": [
   "<strong>we / our / us.</strong> \"<em>We</em> have forty people.\" \"<em>Our</em> office is near the port.\" \"Tell <em>us</em> about your company.\" (we = the people · our = of the company · us = to the people)",
   "<strong>Three facts about a company:</strong> \"We <em>have</em> … people.\" \"We <em>work with</em> companies in …\" \"Our office <em>is in</em> …\" Questions: \"How many people do you have?\" \"Where are your customers?\"",
   "<strong>This is…</strong> to introduce a person: \"<em>This is</em> Sarah, our manager.\" — \"Nice to meet you, Sarah.\" Then a small question: \"How was your flight?\" \"Would you like a coffee?\"",
   "<strong>Let's…</strong> = a decision together: \"<em>Let's</em> start in January.\" \"<em>Let's</em> have dinner.\" \"<em>Let's</em> talk about the price.\"",
 ],
 "ex1": {"h": "1. we, our or us?", "intro": "Complete each sentence with <em>we</em>, <em>our</em> or <em>us</em>.",
         "items": [("___ have forty people.", "We"), ("___ office is near the port.", "Our"), ("Tell ___ about your company.", "us"), ("___ work with companies in France.", "We")]},
 "ex2": {"h": "2. Make the sentence", "intro": "Put the words in order. Then say the sentence out loud.",
         "items": [("is / This / Sarah, / our manager", "This is Sarah, our manager."), ("do / How many / you / have / customers?", "How many customers do you have?"), ("in / start / Let's / January", "Let's start in January."), ("near / Our office / the station / is", "Our office is near the station.")]},
 "ex3": {"h": "3. Complete the conversation", "intro": "Fill each gap with one word. Read the conversation out loud when you finish.",
         "text": "\"Tell us about your ___.\" — \"___ have a small company. Twenty people. ___ office is in Milan.\" — \"How ___ customers do you have?\" — \"About a hundred.\" — \"Good. ___ start in March.\"",
         "ans": "company · We · Our · many · Let's",
         "tip": "<em>We</em> + verb · <em>Our</em> + thing · <em>Let's</em> + verb."},
 "roleplay": {"scene": "A meeting at a new company. They ask about your business.", "you": "yourself", "partner": "Manager",
   "rounds": [("Welcome! This is Anna, our manager.", "nice to meet you · a small question", "Nice to meet you, Anna. How are you?"),
              ("How was your journey?", "one or two words · but I'm here", "Long, but good. I'm here!"),
              ("Tell us about your company.", "three facts: people · office · customers", "We have thirty people. Our office is in the city. We work with companies in Germany and Poland."),
              ("How many customers do you have?", "a number", "About a hundred."),
              ("And why our company?", "one reason", "Because you are a good company. And I like your city."),
              ("The price is good. Let's start next month.", "agree · thank", "Next month is perfect. Thank you very much.")],
   "quick": [("Tell me about your company.", "We have twenty people. Our office is in the city."), ("How many people do you have?", "Forty."), ("Where is your office?", "It's near the port."), ("Who are your customers?", "Small and big companies in Spain and France."),
             ("How was your flight?", "Long, but OK."), ("Would you like a coffee or tea?", "Coffee, please. Black."), ("Who is Sarah?", "She's the manager."), ("When do we start?", "Let's start in January."),
             ("This is Tom, from our team.", "Nice to meet you, Tom."), ("Was the meeting good?", "Yes. Very good. He did it!")]},
 "useful": "<strong>Useful language:</strong> \"This is…, our manager.\" · \"Nice to meet you.\" · \"How was your flight?\" · \"We have… people.\" · \"Our office is in…\" · \"We work with…\" · \"Let's start in…\"",
 "taskA": {"h": "Task A · Tell the meeting", "p": ["Tell the meeting in your own words. Steps: <em>the third floor, the river → this is Sarah, this is Tom → coffee, black → forty people, near the port, Spain, France, Italy → two hundred customers → \"I like rain\" → the price, the dates, January → the contract on Monday → he did it.</em>"]},
 "taskB": {"h": "Task B · My company (2 minutes)", "p": ["Tell me about your company or your work in five sentences: how many people, where the office is, who the customers are, what you do every day, and one thing you like. Start the timer and keep talking."]},
 "taskC": {"h": "Task C · Ask me", "p": ["I am a new customer. Introduce me to two people (\"This is…\"), ask me about my journey, then ask me three questions about my company. Then we change: you are the customer."]},
 "finish": ["Say three facts about your company. Then three facts about a company you like.", "Leo says \"I like rain\" and everyone laughs. Is a joke good in a first meeting? Why, or why not?", "<strong>From memory:</strong> introduce two people, and say one sentence with <em>Let's</em>."],
},
{
 "n": 12, "slug": "a_present_for_carla", "title": "A Present for Carla",
 "picture": ("sf_a1_12_a_present_for_carla.png", "Leo in a bright London shop holding a green-and-blue scarf; the assistant smiles; a sign reads SALE 20%.", ["Where is Leo?", "What is he holding?", "What does the sign say?"]),
 "strap": "A scarf for Carla, a shirt for Marco, a T-shirt for Sofia. Colours, sizes, prices, and \"I'll take it\".",
 "today": "buy something in a shop: say what you are looking for, ask about colours, sizes and prices, and decide. Grammar: <em>I'm looking for…</em>, <em>Do you have this in…?</em>, <em>too big</em>, <em>I'll take it</em>.",
 "warm_intro": "<strong>Warm up — five words to remember.</strong> They come from Lessons 9, 10 and 11. <strong>Do you know it?</strong> Say what it means and use it in a sentence. <strong>Is it new?</strong> Good — learn it now. Click Reveal to check, and follow the link to read the lesson.",
 "warm": [
   ("a colleague", "sf_a1_11_the_meeting.html|The Meeting", "What does it mean? Say the name of one colleague.", "a colleague — a person who works with you."),
   ("a manager", "sf_a1_11_the_meeting.html|The Meeting", "What does it mean? Are you a manager?", "a manager — the person who is the boss of a team."),
   ("a contract", "sf_a1_11_the_meeting.html|The Meeting", "What does it mean? When did you last sign one?", "a contract — a paper both companies sign: the deal."),
   ("the menu", "sf_a1_10_dinner_with_the_customer.html|Dinner with the Customer", "What does it mean? What do you look for first on a menu?", "the menu — the list of food in a restaurant."),
   ("straight on", "sf_a1_09_a_problem_and_the_way.html|A Problem, and the Way", "What does it mean? Give me one direction with it.", "straight on — not left, not right: in front of you."),
 ],
 "words": ["a present", "a scarf", "a size", "a colour", "too big", "to try on", "expensive", "a discount"],
 "meanings": ["not the right size: bigger than you need", "it costs a lot; not cheap", "a thing you give to a person: a gift", "red, blue, green…",
              "small, medium, large", "a lower price: you pay less", "to put on clothes in the shop to see if they are good", "a long cloth for your neck"],
 "key": [2, 7, 4, 3, 0, 6, 1, 5],
 "before": ["Which words are things? Which words are about money?", "Leo has a free morning in London. What does he buy, and for whom? Guess."],
 "conv_intro": "Thursday morning. A free morning, and a big shop on Oxford Street. Read each part. Then try the questions from memory, and answer the last one about you.",
 "parts": [
   {"h": "Part 1 — A scarf for Carla",
    "lines": [("", "The flight home is at six in the evening. Leo has the morning free. A present for Carla, a present for the children. He goes to a big shop on Oxford Street."),
              ("Assistant", "Can I help you?"), ("Leo", "Yes. I'm looking for a scarf. For my wife."), ("Assistant", "What colour?"), ("Leo", "Green. She likes green."),
              ("Assistant", "We have this one — green and blue. It's wool."), ("Leo", "It's beautiful. How much is it?"), ("Assistant", "Forty-five pounds."), ("Leo", "Hmm. It's a little expensive."),
              ("Assistant", "There's a twenty per cent discount today. Thirty-six pounds."), ("Leo", "OK. I'll take it.")],
    "qs": [("What does Leo want, and who is it for?", "A green scarf, for his wife Carla."), ("How much does he pay? Why?", "Thirty-six pounds. There is a 20% discount.")],
    "talk": "And you? Do you buy presents when you travel? For whom?"},
   {"h": "Part 2 — Marco and Sofia",
    "lines": [("", "Now: Marco and Sofia. A football shirt for Marco. A T-shirt for Sofia."),
              ("Leo", "Do you have this shirt in a small size?"), ("Assistant", "Small… yes. Here you are."), ("Leo", "And this T-shirt — do you have it in pink?"),
              ("Assistant", "In pink, only medium."), ("Leo", "Medium is too big. She's ten."), ("Assistant", "What about this one? Pink, size small."),
              ("Leo", "Perfect. Can I have a gift bag?"), ("Assistant", "Of course. Is that everything?"), ("Leo", "Yes. Can I pay by card?")],
    "qs": [("What does Leo buy for Marco?", "A football shirt, size small."), ("Why is medium not good for Sofia?", "It is too big. She is ten.")],
    "talk": "And you? What do you buy for your family when you travel: clothes, chocolate, something from the city?"},
   {"h": "Part 3 — Something for Leo",
    "lines": [("", "One more thing. A shop with a hundred umbrellas. Leo laughs. Of course. London."),
              ("Leo", "Excuse me, how much is this umbrella?"), ("Assistant", "Twelve pounds."), ("Leo", "Do you have it in black?"), ("Assistant", "Black, blue, red…"),
              ("Leo", "Black, please."), ("Assistant", "Would you like to try it?"), ("Leo", "Try an umbrella?"), ("Assistant", "Everybody says that. And then they try it."),
              ("", "He tries it. It works. He is ready for London — on the last day.")],
    "qs": [("What does Leo buy for himself?", "A black umbrella."), ("Why is it funny?", "It is his last day in London. Now he is ready for the rain.")],
    "talk": "And you? What do you always forget when you travel?"},
 ],
 "grammar_tab": "Grammar — in a shop",
 "grammar_h": "Grammar: I'm looking for… / Do you have this in…? / too big",
 "grammar_intro": "Four sentences do almost all the work in a shop. Learn them as one set.",
 "notes": [
   "<strong>I'm looking for + a thing.</strong> \"<em>I'm looking for</em> a scarf.\" \"<em>I'm looking for</em> a present for my son.\" The assistant asks: \"What colour?\" \"What size?\"",
   "<strong>Do you have this in…?</strong> \"<em>Do you have this in</em> blue?\" \"<em>Do you have it in</em> a small size?\" Sizes: <em>small, medium, large</em> (S, M, L).",
   "<strong>too + adjective</strong> = more than you want: \"It's <em>too big</em>.\" \"It's <em>too small</em>.\" \"It's <em>too expensive</em>.\" Softer: \"It's <em>a little</em> expensive.\"",
   "<strong>Decide:</strong> \"<em>I'll take it.</em>\" (yes) · \"I'll think about it.\" (no, politely) · Prices: £12.50 = \"twelve pounds fifty\" · \"Is there a discount?\"",
 ],
 "ex1": {"h": "1. Which word?", "intro": "Complete each sentence with <em>looking</em>, <em>in</em>, <em>too</em> or <em>take</em>.",
         "items": [("I'm ___ for a present for my wife.", "looking"), ("Do you have this ___ blue?", "in"), ("Medium is ___ big.", "too"), ("It's beautiful. I'll ___ it.", "take")]},
 "ex2": {"h": "2. Make the sentence", "intro": "Put the words in order. Then say the sentence out loud.",
         "items": [("much / How / this scarf / is?", "How much is this scarf?"), ("in / Do / this / you / have / a small size?", "Do you have this in a small size?"), ("expensive / a little / It's", "It's a little expensive."), ("take / I'll / it", "I'll take it.")]},
 "ex3": {"h": "3. Complete the conversation", "intro": "Fill each gap with one word. Read the conversation out loud when you finish.",
         "text": "\"Can I ___ you?\" — \"Yes. I'm looking ___ a T-shirt for my son.\" — \"What ___?\" — \"Small, please. And in blue.\" — \"Here you are. It's fifteen pounds.\" — \"Hmm, it's a little ___. Is there a discount?\" — \"Ten per cent today.\" — \"OK, I'll ___ it.\"",
         "ans": "help · for · size · expensive · take",
         "tip": "<em>I'm looking for</em> → what you want. <em>I'll take it</em> → yes."},
 "roleplay": {"scene": "A shop in a new city. You want a present.", "you": "the customer", "partner": "Assistant",
   "rounds": [("Can I help you?", "what you want · who it is for", "Yes. I'm looking for a scarf for my wife."),
              ("What colour?", "a colour · one more detail", "Blue. Or green. She likes both."),
              ("We have this one. It's forty pounds.", "say: a little expensive · ask: discount?", "It's a little expensive. Is there a discount?"),
              ("There's a ten per cent discount today.", "decide", "OK. I'll take it."),
              ("Anything else?", "one more thing · size", "Yes. Do you have this T-shirt in a small size?"),
              ("Small, yes. Here you are. Would you like a gift bag?", "yes · pay by card", "Yes, please. Can I pay by card?")],
   "quick": [("Can I help you?", "Yes. I'm looking for a present."), ("What colour?", "Green, please."), ("What size?", "Medium."), ("How much is this scarf?", "Thirty pounds."),
             ("Is it too big?", "Yes, it's too big. Do you have a small?"), ("Do you have this in black?", "Yes, here you are."), ("Is there a discount?", "Twenty per cent today."), ("Would you like a gift bag?", "Yes, please."),
             ("Can I pay by card?", "Of course."), ("It's forty-five pounds. OK?", "Hmm, it's a little expensive. I'll think about it.")]},
 "useful": "<strong>Useful language:</strong> \"I'm looking for…\" · \"Do you have this in blue / in a small size?\" · \"How much is it?\" · \"It's a little expensive.\" · \"Is there a discount?\" · \"It's too big.\" · \"I'll take it.\" · \"Can I have a gift bag?\"",
 "taskA": {"h": "Task A · Tell the shopping", "p": ["Tell Leo's morning in your own words. Steps: <em>a free morning, Oxford Street → a green scarf, £45, a little expensive, 20% → a football shirt, small → a pink T-shirt, medium is too big → a gift bag, by card → a hundred umbrellas → black, please → \"try an umbrella?\"</em>"]},
 "taskB": {"h": "Task B · Presents (2 minutes)", "p": ["Talk about presents: what you buy when you travel, for whom, where, and how much you pay. Say one thing that was too expensive. Start the timer and keep talking."]},
 "taskC": {"h": "Task C · Buy three things", "p": ["I am the shop assistant. Buy three things: a present for a person in your family, a thing for you, and a thing you forgot at home. Ask about colour, size and price each time."]},
 "finish": ["What is a good present from your city? What is a bad present?", "Leo buys an umbrella on his last day. Say one thing you bought too late.", "<strong>From memory:</strong> say the four shop sentences from today."],
},
{
 "n": 13, "slug": "flying_home", "title": "Flying Home",
 "picture": ("sf_a1_13_flying_home.png", "Night. Leo at his front door with his bag; Carla, Marco and Sofia welcome him home.", ["Where is Leo?", "Who is at the door?", "What is in the bag? Guess."]),
 "strap": "Gate 14, seat 14A, a neighbour who asks questions, and the door at home. Talk about a trip after it happens.",
 "today": "talk about a trip in the past: how it was, what you did, where you stayed, what you bought. Grammar: <em>was / were</em>, <em>How was…?</em>, <em>Did you…?</em>",
 "warm_intro": "<strong>Warm up — five words to remember.</strong> They come from Lessons 11 and 12. <strong>Do you know it?</strong> Say what it means and use it in a sentence. <strong>Is it new?</strong> Good — learn it now. Click Reveal to check, and follow the link to read the lesson.",
 "warm": [
   ("a present", "sf_a1_12_a_present_for_carla.html|A Present for Carla", "What does it mean? What is a good present for you?", "a present — a thing you give to a person: a gift."),
   ("a scarf", "sf_a1_12_a_present_for_carla.html|A Present for Carla", "What does it mean? What colour is yours?", "a scarf — a long cloth for your neck."),
   ("expensive", "sf_a1_12_a_present_for_carla.html|A Present for Carla", "What does it mean? What is expensive in your city?", "expensive — it costs a lot; not cheap."),
   ("a contract", "sf_a1_11_the_meeting.html|The Meeting", "What does it mean? Who sends it in the story?", "a contract — a paper both companies sign: the deal."),
   ("a team", "sf_a1_11_the_meeting.html|The Meeting", "What does it mean? How many people are in your team?", "a team — the people you work with, together."),
 ],
 "words": ["a trip", "to take off", "to land", "a seat belt", "a passenger", "a neighbour", "a view", "home"],
 "meanings": ["the plane goes up into the sky", "a person who travels in a plane, bus or train", "the plane comes down to the ground", "the place where you live: your house, your family",
              "a journey to a place and back", "what you can see from a window or a high place", "the person next to you", "the belt on your seat in a plane or a car"],
 "key": [4, 0, 2, 7, 1, 6, 5, 3],
 "before": ["Which words are about the plane? Which word is the best word of all?", "Leo goes home. What questions does Carla ask? Guess two."],
 "conv_intro": "Thursday evening. The flight home. Read each part. Then try the questions from memory, and answer the last one about you.",
 "parts": [
   {"h": "Part 1 — Gate 14",
    "lines": [("", "Six o'clock. Gate 14. No delay this time. Leo has a green scarf, a football shirt, a pink T-shirt and a black umbrella in his bag. And a contract in his email."),
              ("Announcement", "Flight 508 to Madrid is now boarding. Rows twenty to thirty, please."), ("Leo", "Excuse me, is this the queue for Madrid?"), ("Passenger", "Yes. What row are you?"),
              ("Leo", "Fourteen."), ("Passenger", "Then you wait. They call rows twenty to thirty first."), ("Leo", "Ah. OK. Thank you.")],
    "qs": [("Is the flight delayed this time?", "No. No delay."), ("Which rows board first?", "Rows twenty to thirty. Leo is in row fourteen, so he waits.")],
    "talk": "And you? Do you like flying? Front or back of the plane, window or aisle?"},
   {"h": "Part 2 — Seat 14A",
    "lines": [("", "Seat 14A. Window. Leo puts on his seat belt. The plane takes off. London is small, then it is clouds."),
              ("Neighbour", "Business or holiday?"), ("Leo", "Business. Three days. And you?"), ("Neighbour", "Holiday. I was in London for a week."), ("Leo", "How was it?"),
              ("Neighbour", "Wet! But wonderful. The museums, the parks… And you — how was your trip?"), ("Leo", "Good. Very good. I had a meeting, and it went well. And we went to a restaurant by the river."),
              ("Neighbour", "Nice. Your English is good."), ("Leo", "Thank you. Three days ago, it was terrible.")],
    "qs": [("Why was the neighbour in London? How was it?", "For a holiday, one week. Wet, but wonderful."), ("How was Leo's meeting?", "Very good. It went well.")],
    "talk": "And you? Do you talk to the person next to you on a plane? What do you say?"},
   {"h": "Part 3 — Home",
    "lines": [("", "Ten o'clock at night. The plane lands. Passport, suitcase, taxi. Forty minutes. Then the door, the light, the smell of dinner."),
              ("Carla", "Leo! How was it?"), ("Leo", "It was good. The meeting was good. The hotel was small. London was wet."), ("Carla", "And your English?"),
              ("Leo", "Not bad. I said hello. I smiled. I asked questions."), ("Carla", "I know."), ("Sofia", "Dad! Did you buy something?"), ("Leo", "Maybe."),
              ("", "He opens the bag. A green scarf. A football shirt. A pink T-shirt. And a black umbrella — for the next time.")],
    "qs": [("What was good? What was small, and what was wet?", "The meeting was good. The hotel was small. London was wet."), ("What did Sofia ask?", "\"Did you buy something?\"")],
    "talk": "And you? What do you say when you come home from a trip? What do you bring?"},
 ],
 "grammar_tab": "Grammar — was, were / Did you…?",
 "grammar_h": "Grammar: was, were / How was…? / Did you…?",
 "grammar_intro": "After a trip, everyone asks the same question: <em>How was it?</em> Today you answer it, in the past.",
 "notes": [
   "<strong>was / were</strong> = the past of <em>is / are</em>. \"The meeting <em>was</em> good.\" \"The hotel <em>was</em> small.\" \"The people <em>were</em> nice.\" \"I <em>was</em> in London for three days.\"",
   "<strong>How was…?</strong> \"<em>How was</em> your trip / your flight / the hotel?\" — \"It was great. / It was OK. / It was terrible.\"",
   "<strong>Past verbs:</strong> regular = <em>-ed</em>: \"I <em>asked</em> questions. I <em>smiled</em>. I <em>stayed</em> at the Park Hotel.\" · irregular: <em>had</em> (have), <em>went</em> (go), <em>said</em> (say), <em>bought</em> (buy), <em>took</em> (take).",
   "<strong>Did you…?</strong> for past questions: \"<em>Did you</em> buy something?\" — \"Yes, I did. / No, I didn't.\" \"Where <em>did you</em> stay?\" — \"At a small hotel.\"",
 ],
 "ex1": {"h": "1. was or were?", "intro": "Complete each sentence with <em>was</em> or <em>were</em>.",
         "items": [("The meeting ___ good.", "was"), ("The people ___ very nice.", "were"), ("How ___ your flight?", "was"), ("The hotels ___ expensive.", "were")]},
 "ex2": {"h": "2. Make the sentence", "intro": "Put the words in order. Then say the sentence out loud.",
         "items": [("was / How / your trip?", "How was your trip?"), ("a meeting / I / had / on Wednesday", "I had a meeting on Wednesday."), ("you / Did / buy / a present?", "Did you buy a present?"), ("the restaurant / We / went to / on Tuesday", "We went to the restaurant on Tuesday.")]},
 "ex3": {"h": "3. Complete the conversation", "intro": "Fill each gap with one word. Read the conversation out loud when you finish.",
         "text": "\"How ___ your trip?\" — \"It was good. I ___ a meeting on Monday, and it went well. On Tuesday we ___ to a restaurant.\" — \"___ you buy anything?\" — \"Yes, I ___. A scarf for my wife.\" — \"And the hotel?\" — \"The room ___ small, but the bed was big.\"",
         "ans": "was · had · went · Did · did · was",
         "tip": "have → <em>had</em> · go → <em>went</em> · <em>Did you…?</em> → <em>Yes, I did.</em>"},
 "roleplay": {"scene": "On the plane home. The person next to you asks about your trip.", "you": "yourself", "partner": "Neighbour",
   "rounds": [("Business or holiday?", "answer · how many days", "Business. Four days."),
              ("How was it?", "two words: good / long / wet / busy", "Good. But busy."),
              ("What did you do?", "two things in the past: had a meeting · went to…", "I had two meetings, and we went to a restaurant by the river."),
              ("Where did you stay?", "hotel · one word about it", "At a small hotel near the station. It was quiet."),
              ("Did you buy anything?", "yes or no · what", "Yes, I did. A scarf for my wife."),
              ("Your English is good!", "thank · ask a question back", "Thank you. And you — how was your week?")],
   "quick": [("How was your trip?", "It was good."), ("How was the hotel?", "It was small, but nice."), ("Where did you stay?", "At the Park Hotel."), ("What did you do on Tuesday?", "I had a meeting."),
             ("Did you buy anything?", "Yes, I did. A present for my daughter."), ("Was the flight delayed?", "No, it wasn't."), ("How was the weather?", "It was wet!"), ("Did you go to a restaurant?", "Yes, we went to an Italian restaurant."),
             ("How was your English?", "Not bad. I asked questions."), ("Were the people nice?", "Yes, they were very nice.")]},
 "useful": "<strong>Useful language:</strong> \"It was good / small / wet.\" · \"How was your trip?\" · \"I had a meeting.\" · \"We went to a restaurant.\" · \"I stayed at…\" · \"Did you buy something?\" — \"Yes, I did.\"",
 "taskA": {"h": "Task A · Tell the journey home", "p": ["Tell the journey home in your own words, in the past. Steps: <em>gate 14, no delay → rows twenty to thirty → seat 14A, the plane took off → the neighbour: a week in London, wet but wonderful → the meeting went well → the plane landed, ten o'clock → Carla: how was it? → the bag: scarf, shirt, T-shirt, umbrella.</em>"]},
 "taskB": {"h": "Task B · My last trip (2 minutes)", "p": ["Tell me about your last trip, in the past: where you went, how it was, where you stayed, what you did, what you bought. Start the timer and keep talking."]},
 "taskC": {"h": "Task C · Ask me", "p": ["Ask me six questions about my last trip: where, how long, how it was, where I stayed, what I did, what I bought. Then tell my trip back to me: \"You went to… You stayed at…\""]},
 "finish": ["What was the best part of Leo's trip? What was the worst?", "Leo says: \"Three days ago, my English was terrible.\" What changed? Say two things.", "<strong>From memory:</strong> say three sentences about your last trip with <em>was</em>, <em>had</em> and <em>went</em>."],
},
{
 "n": 14, "slug": "the_phone_call", "title": "The Phone Call",
 "picture": ("sf_a1_14_the_phone_call.png", "Leo at his desk on the phone, smiling; a wall calendar shows MARCH with the 12th circled; the port through the window.", ["Where is Leo?", "What is on the wall?", "What date can you see?"]),
 "strap": "The contract is signed. Now: an invitation, a date, a hotel, and a promise. \"See you in March.\"",
 "today": "make plans on the phone: invite someone, agree a date, and say what you will do. Grammar: <em>I'll…</em>, <em>Will you…?</em>, dates and months.",
 "warm_intro": "<strong>Warm up — five words to remember.</strong> They come from Lessons 11, 12 and 13. <strong>Do you know it?</strong> Say what it means and use it in a sentence. <strong>Is it new?</strong> Good — learn it now. Click Reveal to check, and follow the link to read the lesson.",
 "warm": [
   ("a trip", "sf_a1_13_flying_home.html|Flying Home", "What does it mean? Where was your last trip?", "a trip — a journey to a place and back."),
   ("to land", "sf_a1_13_flying_home.html|Flying Home", "What does it mean? Say the opposite.", "to land — the plane comes down to the ground. The opposite is to take off."),
   ("a passenger", "sf_a1_13_flying_home.html|Flying Home", "What does it mean? Are you a good passenger?", "a passenger — a person who travels in a plane, bus or train."),
   ("a discount", "sf_a1_12_a_present_for_carla.html|A Present for Carla", "What does it mean? Ask for one.", "a discount — a lower price: you pay less. \"Is there a discount?\""),
   ("to agree", "sf_a1_11_the_meeting.html|The Meeting", "What does it mean? Say: Let's…", "to agree — to say yes together. \"Let's start in January.\""),
 ],
 "words": ["to sign", "to send", "a date", "next week", "to invite", "to book", "a calendar", "to visit"],
 "meanings": ["to write your name on a contract", "the week after this week", "to ask a person to come", "to reserve a hotel, a table or a flight",
              "to go and see a person or a place", "the page or the app with the days and months", "a day: the twelfth of March", "to post or email a thing to a person"],
 "key": [0, 7, 6, 1, 2, 3, 5, 4],
 "before": ["Which words are things you do with paper? Which words are about time?", "Leo calls London. Why? Guess two reasons."],
 "conv_intro": "A week later, Monday morning. Read each part. Then try the questions from memory, and answer the last one about you.",
 "parts": [
   {"h": "Part 1 — I have the contract",
    "lines": [("", "A week later. Monday morning. The contract is on Leo's desk. He signs it. Then he calls London."),
              ("Mr Hill", "Leo! Good to hear you."), ("Leo", "Good morning, Mr Hill. I have the contract. I'll sign it today and send it this afternoon."), ("Mr Hill", "Excellent."),
              ("Leo", "And… I'd like to invite you to my city. In March?"), ("Mr Hill", "March! Yes. I'd love to.")],
    "qs": [("What does Leo do with the contract?", "He signs it today and sends it this afternoon."), ("What does he invite Mr Hill to?", "To his city, in March.")],
    "talk": "And you? Do you invite customers to your city? What do you show them?"},
   {"h": "Part 2 — The twelfth",
    "lines": [("Leo", "When is good for you?"), ("Mr Hill", "Let me look at my calendar. The first week of March is busy… What about the twelfth?"), ("Leo", "The twelfth of March. One moment. Yes, the twelfth is fine."),
              ("Mr Hill", "Tuesday the twelfth. I'll fly in the morning."), ("Leo", "I'll meet you at the airport."), ("Mr Hill", "You don't have to."), ("Leo", "I know. But I will."),
              ("", "He writes it in his calendar: 12 March — Mr Hill — airport, 10:30.")],
    "qs": [("What date do they choose?", "Tuesday the twelfth of March."), ("Where will Leo meet him?", "At the airport, at half past ten.")],
    "talk": "And you? What is a busy month for you? What is a quiet month?"},
   {"h": "Part 3 — Carla will cook",
    "lines": [("Mr Hill", "Where will I stay?"), ("Leo", "I'll book a hotel near the port. Small, quiet, good breakfast."), ("Mr Hill", "Like the Park Hotel?"), ("Leo", "Better than the Park Hotel. And on Tuesday evening, dinner. Carla will cook."),
              ("Mr Hill", "Carla will cook?"), ("Leo", "Fish. It's delicious."), ("Mr Hill", "Then I'll bring the wine."), ("Leo", "Deal. See you in March."), ("Mr Hill", "See you in March, Leo."),
              ("", "He puts the phone down. Carla is in the doorway. \"I will cook?\" \"You will cook.\" \"Then you will do the plates.\" \"Deal.\"")],
    "qs": [("Where will Mr Hill stay?", "In a small, quiet hotel near the port. Leo will book it."), ("What will Carla cook, and what will Mr Hill bring?", "Fish. Mr Hill will bring the wine.")],
    "talk": "And you? What do you cook for guests? Who does the plates?"},
 ],
 "grammar_tab": "Grammar — I'll… / dates",
 "grammar_h": "Grammar: I'll… / Will you…? / dates and months",
 "grammar_intro": "Plans and promises use <em>will</em>. Then you need a date to put them on.",
 "notes": [
   "<strong>I'll = I will.</strong> A plan or a promise, now: \"<em>I'll</em> sign it today.\" \"<em>I'll</em> book a hotel.\" \"<em>I'll</em> meet you at the airport.\" \"Carla <em>will</em> cook.\"",
   "<strong>Questions and no:</strong> \"Where <em>will</em> I stay?\" \"<em>Will you</em> come in March?\" — \"Yes, I will. / No, I won't.\" (won't = will not)",
   "<strong>Dates:</strong> \"<em>the twelfth of March</em>\" (12 March) · \"on Tuesday\" · \"on the twelfth\" · \"in March\" · \"at 10:30\" · first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, eleventh, twelfth, twentieth, thirtieth.",
   "<strong>Months:</strong> January, February, March, April, May, June, July, August, September, October, November, December. \"What about the fifth of May?\" \"When is good for you?\"",
 ],
 "ex1": {"h": "1. Which word?", "intro": "Complete each sentence with <em>will</em>, <em>Will</em>, <em>on</em> or <em>in</em>.",
         "items": [("I ___ send the contract today.", "will (I'll)"), ("___ you come in March?", "Will"), ("See you ___ the twelfth.", "on"), ("See you ___ March.", "in")]},
 "ex2": {"h": "2. Make the sentence", "intro": "Put the words in order. Then say the sentence out loud.",
         "items": [("book / I'll / a hotel", "I'll book a hotel."), ("is / When / good / for you?", "When is good for you?"), ("at / I'll / you / the airport / meet", "I'll meet you at the airport."), ("the twelfth / What about / of March?", "What about the twelfth of March?")]},
 "ex3": {"h": "3. Complete the conversation", "intro": "Fill each gap with one word. Read the conversation out loud when you finish.",
         "text": "\"I'd like to ___ you to our office.\" — \"Thank you! When?\" — \"What ___ the fifth of May?\" — \"The fifth is fine. I'll ___ in the morning.\" — \"Great. I'll ___ a hotel for you, and I'll ___ you at the station.\"",
         "ans": "invite · about · fly · book · meet",
         "tip": "<em>I'll</em> + verb = my plan. <em>What about the…?</em> = a date."},
 "roleplay": {"scene": "A phone call. You invite a customer to visit your city.", "you": "yourself", "partner": "Customer",
   "rounds": [("Hello?", "say who you are · why you call", "Hello, it's Adam Kowalski. I have the contract. And I'd like to invite you to our city."),
              ("I'd love to come. When?", "a month · a date", "In April? What about the tenth?"),
              ("The tenth is fine. Where will I stay?", "I'll book…", "I'll book a hotel in the centre. Small and quiet."),
              ("And how do I get from the airport?", "I'll meet you…", "I'll meet you at the airport. Ten o'clock."),
              ("And in the evening?", "dinner plan · who cooks", "Dinner at my home. My wife will cook."),
              ("Perfect. See you then.", "see you on the… / in…", "See you on the tenth of April.")],
   "quick": [("When is good for you?", "What about the twelfth of March?"), ("Where will I stay?", "I'll book a hotel near the port."), ("Will you meet me at the airport?", "Yes, I will."), ("What will Carla cook?", "Fish."),
             ("What will Mr Hill bring?", "The wine."), ("When will you send the contract?", "This afternoon."), ("What date is it today?", "The ninth of September."), ("What month is your birthday?", "In May."),
             ("Will you come to London again?", "Yes, I will. Next year."), ("Who will do the plates?", "Leo will.")]},
 "useful": "<strong>Useful language:</strong> \"I have the contract. I'll sign it today.\" · \"I'd like to invite you to…\" · \"When is good for you?\" · \"What about the twelfth?\" · \"I'll book… / I'll meet you…\" · \"See you in March.\"",
 "taskA": {"h": "Task A · Tell the call", "p": ["Tell the phone call in your own words. Steps: <em>Monday, the contract, he signs it → the call: I'll send it this afternoon → the invitation, March → the calendar: the twelfth → I'll meet you at the airport → a hotel near the port → Carla will cook, fish → I'll bring the wine → deal → \"You will do the plates.\"</em>"]},
 "taskB": {"h": "Task B · Next month (2 minutes)", "p": ["Tell me your plans for next month with <em>I'll</em> and real dates: work, family, one trip, one dinner. Start the timer and keep talking."]},
 "taskC": {"h": "Task C · Call me", "p": ["Phone me. I am your customer. Say why you call, invite me to your city, agree a date, say where I will stay and how I get there, and plan the evening. Then we change: I call you."]},
 "finish": ["What is a good month to visit your city? Why?", "Leo says \"I'll meet you at the airport\" — \"You don't have to.\" — \"I know. But I will.\" Is this good business? Why?", "<strong>From memory:</strong> say three plans with <em>I'll</em>, each with a date."],
},
{
 "n": 15, "slug": "the_visit", "title": "The Visit",
 "picture": ("sf_a1_15_the_visit.png", "A sunny harbour café: Leo points out the port to Mr Hill; ships, the sea, the old church behind.", ["Where are they?", "What is the weather like?", "What can you see behind them?"]),
 "strap": "The twelfth of March. This time Leo is the host: the airport, the city, the port, and dinner at home.",
 "today": "welcome a guest, show them your city, and ask and answer the questions you learned in this whole story. Grammar: the ten questions, all together.",
 "warm_intro": "<strong>Warm up — five words to remember.</strong> They come from Lessons 13 and 14. <strong>Do you know it?</strong> Say what it means and use it in a sentence. <strong>Is it new?</strong> Good — learn it now. Click Reveal to check, and follow the link to read the lesson.",
 "warm": [
   ("to sign", "sf_a1_14_the_phone_call.html|The Phone Call", "What does it mean? What do you sign at work?", "to sign — to write your name on a contract."),
   ("to invite", "sf_a1_14_the_phone_call.html|The Phone Call", "What does it mean? Invite me to dinner.", "to invite — to ask a person to come."),
   ("to book", "sf_a1_14_the_phone_call.html|The Phone Call", "What does it mean? What do you book before a trip?", "to book — to reserve a hotel, a table or a flight."),
   ("a view", "sf_a1_13_flying_home.html|Flying Home", "What does it mean? What is the view from your window?", "a view — what you can see from a window or a high place."),
   ("a seat belt", "sf_a1_13_flying_home.html|Flying Home", "What does it mean? When do you put it on?", "a seat belt — the belt on your seat in a plane or a car."),
 ],
 "words": ["a host", "a guest", "to welcome", "to show", "the port", "a tour", "a toast", "proud"],
 "meanings": ["to say hello to a person who arrives", "a person who visits you", "the place where ships come in", "a short walk or drive to see a place",
              "the person who invites you and looks after you", "happy because of a good thing you did", "to let a person see a thing", "a drink and a few words for a good moment: \"To Leo!\""],
 "key": [4, 1, 0, 6, 2, 3, 7, 5],
 "before": ["Which words are people? Which words are things you do for a guest?", "Mr Hill comes to Leo's city. What does Leo show him? Guess three places."],
 "conv_intro": "The twelfth of March. Leo is the host. Read each part. Then try the questions from memory, and answer the last one about you.",
 "parts": [
   {"h": "Part 1 — Arrivals",
    "lines": [("", "The twelfth of March, half past ten. This time Leo is not the passenger. He is the host. He stands at Arrivals with a coffee — and no umbrella. It's sunny."),
              ("Mr Hill", "Leo!"), ("Leo", "Welcome! How was your flight?"), ("Mr Hill", "Early, and no delay. A miracle."), ("Leo", "Do you have a suitcase?"),
              ("Mr Hill", "Only hand luggage. I learn from you."), ("Leo", "The car is outside. It's twenty minutes to the hotel. No traffic."), ("Mr Hill", "No rain, no traffic. Where am I?")],
    "qs": [("Who is the host now?", "Leo. Mr Hill is the guest."), ("How was Mr Hill's flight? What is the weather like?", "Early, no delay. It is sunny.")],
    "talk": "And you? When a guest arrives, what do you say and do first?"},
   {"h": "Part 2 — The tour",
    "lines": [("", "The hotel is small, quiet, near the port. Then the office: forty people, and a cake. Then a tour of the city: the old town, the port, the sea."),
              ("Mr Hill", "How many ships come here?"), ("Leo", "About twenty a day. Big and small."), ("Mr Hill", "And where is your favourite place?"),
              ("Leo", "There. The café on the corner, opposite the old church. I have my coffee there every morning."), ("Mr Hill", "Every morning?"), ("Leo", "Every morning at half past six."), ("Mr Hill", "You and your six o'clock!")],
    "qs": [("How many ships come to the port?", "About twenty a day."), ("What is Leo's favourite place? When does he go there?", "The café on the corner, opposite the old church. Every morning at half past six.")],
    "talk": "And you? Where do you take a guest in your city? What is your favourite place?"},
   {"h": "Part 3 — Dinner at home",
    "lines": [("", "Seven o'clock. Carla's fish. Marco in his football shirt, Sofia in her pink T-shirt. Mr Hill brings the wine."),
              ("Mr Hill", "Carla, this is delicious."), ("Carla", "Thank you. New recipe. From the internet."), ("Sofia", "Do you like London?"), ("Mr Hill", "Very much. But your city is warmer."),
              ("Marco", "Do you like football?"), ("Mr Hill", "I love it."), ("Leo", "Marco — after the plates."), ("Mr Hill", "A toast. To Leo. Three days in London, and now I can't stop him talking."), ("Leo", "In English!"), ("Carla", "In English."),
              ("", "Leo looks at his family, his guest, his table. Say hello. Smile. Ask questions. It works.")],
    "qs": [("What does Mr Hill bring? What does Carla cook?", "Wine. Carla cooks fish, a new recipe."), ("What is the toast?", "To Leo: three days in London, and now he can't stop talking — in English.")],
    "talk": "And you? Who comes to dinner at your home? What do you say at the end of a good evening?"},
 ],
 "grammar_tab": "Grammar — the ten questions",
 "grammar_h": "Grammar: the ten questions of the story",
 "grammar_intro": "Fifteen chapters, and the same small questions did all the work. Here they are together. Say each one out loud, and answer it about you.",
 "notes": [
   "<strong>With be:</strong> \"Where <em>are</em> you from?\" · \"How <em>was</em> your flight?\" · \"<em>Is</em> it far?\" · \"What time <em>is</em> breakfast?\" — answers: \"I'm from… / It was… / Yes, it is. / At seven.\"",
   "<strong>With do / does / did:</strong> \"What <em>do</em> you do?\" · \"<em>Do</em> you like football?\" · \"What time <em>does</em> he get up?\" · \"<em>Did</em> you buy something?\" — answers: \"Yes, I do. / No, he doesn't. / Yes, I did.\"",
   "<strong>With how:</strong> \"<em>How many</em> ships?\" (a number) · \"<em>How much</em> is it?\" (money) · \"<em>How long</em> are you staying?\" (time) · \"<em>How old</em> is she?\" (age)",
   "<strong>Polite:</strong> \"<em>Can I</em> see your passport?\" · \"<em>Could we</em> have the bill?\" · \"<em>Would you like</em> a coffee?\" · \"<em>Will you</em> come in March?\" — \"Yes, please. / Yes, I will.\"",
 ],
 "ex1": {"h": "1. Which question word?", "intro": "Look at the answer. Complete the question with <em>How</em>, <em>What</em>, <em>Where</em> or <em>Do</em>.",
         "items": [("___ was your flight? — Early, and no delay.", "How"), ("___ do you do? — I have a company.", "What"), ("___ is your favourite place? — The café on the corner.", "Where"), ("___ you like football? — I love it.", "Do")]},
 "ex2": {"h": "2. Make the sentence", "intro": "Put the words in order. Then say the question out loud — and answer it.",
         "items": [("flight / was / How / your?", "How was your flight?"), ("you / Do / a suitcase / have?", "Do you have a suitcase?"), ("ships / How many / come here?", "How many ships come here?"), ("is / your / Where / favourite place?", "Where is your favourite place?")]},
 "ex3": {"h": "3. Complete the conversation", "intro": "Fill each gap with one word. Read the conversation out loud when you finish.",
         "text": "\"___ was your journey?\" — \"Good, no delay.\" — \"___ you have a suitcase?\" — \"No, only hand luggage.\" — \"___ would you like to see?\" — \"The port. How ___ ships come here?\" — \"About twenty a day. ___ you like fish? Carla is cooking.\"",
         "ans": "How · Do · What · many · Do",
         "tip": "<em>How was…?</em> (past) · <em>Do you…?</em> (now) · <em>How many…?</em> (a number)."},
 "roleplay": {"scene": "A guest visits your city. You are the host, from the airport to dinner.", "you": "the host", "partner": "Guest",
   "rounds": [("Hello! Here I am.", "welcome · how was your flight?", "Welcome! How was your flight?"),
              ("Good, thank you. No delay.", "ask: suitcase?", "Do you have a suitcase?"),
              ("Only hand luggage.", "the car · the hotel · how long", "The car is outside. It's twenty minutes to the hotel."),
              ("Nice. What can I see here?", "three places", "The old town, the port and the sea. And the office, of course."),
              ("What is your favourite place?", "answer · why", "The café on the corner. I have my coffee there every morning."),
              ("Thank you for everything.", "invite to dinner · who cooks", "Come to dinner tonight. My wife is cooking fish.")],
   "quick": [("Where are you from?", "I'm from Spain."), ("What do you do?", "I have a small company."), ("How was your flight?", "Early, no delay."), ("Do you have a suitcase?", "Only hand luggage."),
             ("How long is it to the hotel?", "Twenty minutes."), ("How many ships come here?", "About twenty a day."), ("Where is your favourite place?", "The café opposite the church."), ("What time do you get up?", "At half past six."),
             ("Would you like a coffee?", "Yes, please."), ("Did you like London?", "Very much. But it was wet.")]},
 "useful": "<strong>Useful language:</strong> \"Welcome! How was your flight?\" · \"Do you have a suitcase?\" · \"It's twenty minutes to the hotel.\" · \"This is the port / the old town.\" · \"My favourite place is…\" · \"Come to dinner.\" · \"A toast: to…!\"",
 "taskA": {"h": "Task A · Tell the visit", "p": ["Tell the visit in your own words. Steps: <em>the twelfth of March, sunny, no umbrella → Arrivals, no delay → only hand luggage → twenty minutes, no traffic → the hotel, the office, a cake → the port, twenty ships → the café on the corner → Carla's fish, the wine → the toast → in English.</em>"]},
 "taskB": {"h": "Task B · My city tour (2 minutes)", "p": ["A guest is in your city for one day. Tell me the day: where you meet, where you go, what you show, where you eat. Start the timer and keep talking."]},
 "taskC": {"h": "Task C · I am your guest", "p": ["Welcome me at the airport, take me to the hotel, show me three places, and invite me to dinner. Ask me at least five questions on the way."]},
 "finish": ["Leo learned English in fifteen chapters. What can you do now that you could not do at Lesson 1? Say three things.", "Say hello, smile, ask questions. Which is the hardest for you? Which is the easiest?", "<strong>From memory:</strong> ask me the ten questions of the story, one after the other. No looking."],
},
]

# ----------------------------------------------------------------------------
# BUILD
# ----------------------------------------------------------------------------

EXTRA_CSS = """
.scene { display:block; width:100%; max-width:760px; margin:0 auto 14px; border-radius:14px; box-shadow:0 6px 18px rgba(0,0,0,.10); }
.scene-ph { max-width:760px; margin:0 auto 14px; padding:40px 20px; border-radius:14px; background:#f1eefb; color:#9a93ad; text-align:center; font-size:0.95rem; }
.story-chunk .who { font-weight: 700; color: #764ba2; }
.story-chunk p.prose { color: #3a3a4a; }
.rp-line { padding: 6px 0; }
.rp-line .you { color: #8a5a00; font-style: italic; }
"""


def esc(s): return html.escape(s, quote=True)
def fname(L): return f"sf_a1_{L['n']:02d}_{L['slug']}.html"
LET = "ABCDEFGH"
GAP = '<input type="text" placeholder="...">'

def reveal_btn(target_id=None, label="Reveal answers"):
    if target_id:
        return f'<button class="reveal-btn" onclick="document.getElementById(\'{target_id}\').classList.toggle(\'show\')">{label}</button>'
    return f'<button class="reveal-btn" onclick="this.nextElementSibling.classList.toggle(\'show\')">{label}</button>'

def build(L, prev, nxt, css, js):
    n = L["n"]
    o = []
    o.append(f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="series" content="{SERIES}">
<title>{SERIES}: {esc(L["title"])} · A1</title>
<style>{css}{EXTRA_CSS}</style>
</head>
<body>
<div class="container">
    <header>
        <span class="tag">{SERIES.upper()} · A1 · 50 min</span>
        <h1>{esc(L["title"])}</h1>
        <p>{esc(L["strap"])}</p>
    </header>
""")
    links = []
    if prev: links.append(f'<a href="{fname(prev)}">← Lesson {prev["n"]}: {esc(prev["title"])}</a>')
    if nxt: links.append(f'<a href="{fname(nxt)}">Lesson {nxt["n"]}: {esc(nxt["title"])} →</a>')
    o.append(f'    <p class="crosslink"><a href="speak_first_dashboard.html">Speak First</a> · Lesson {n} of 15. {" · ".join(links)}</p>\n')
    o.append(f"""
    <nav class="tab-nav">
        <button class="tab-btn active" onclick="showTab(0)">Key Words</button>
        <button class="tab-btn" onclick="showTab(1)">The Conversation</button>
        <button class="tab-btn" onclick="showTab(2)">{L["grammar_tab"]}</button>
        <button class="tab-btn" onclick="showTab(3)">Role Play</button>
        <button class="tab-btn" onclick="showTab(4)">Speak</button>
    </nav>
""")
    # ---- TAB 0 KEY WORDS
    o.append(f"""
    <div class="tab-content active">
        <div class="card">
            <div class="intention"><strong>Today:</strong> {L["today"]}</div>

            <div class="note" style="border-left:4px solid #764ba2;">
                {L["warm_intro"]}
            </div>
""")
    for word, link, prompt, meaning in L["warm"]:
        src = ""
        if link:
            href, name = link.split("|")
            src = f' <span style="font-size:0.82rem; color:#9a93ad; font-weight:400;">— from <a href="{href}" style="color:#764ba2; font-weight:600;">{esc(name)}</a></span>'
        o.append(f"""            <div class="word-card">
                <div class="word">{esc(word)}{src}</div>
                <div class="prompt">{esc(prompt)}</div>
                {reveal_btn(label="Reveal")}
                <div class="meaning">{esc(meaning)}</div>
            </div>
""")
    o.append(f"""
            <h2>Now — the words for today's conversation</h2>
            <p>These are the new words for <em>{esc(L["title"])}</em>. Match each word (1–8) to its meaning (A–H). Say your answers out loud — "I think 1 is D" — then check.</p>
            <div class="match-grid">
                <div class="match-col">
                    <h4>Words</h4>
                    <ol>
""")
    for w in L["words"]: o.append(f"                        <li>{esc(w)}</li>\n")
    o.append("""                    </ol>
                </div>
                <div class="match-col">
                    <h4>Meanings</h4>
                    <ul style="list-style:none; padding-left:0;">
""")
    for i, m in enumerate(L["meanings"]): o.append(f"                        <li>{LET[i]}. {esc(m)}</li>\n")
    key = L["key"]
    assert sorted(key) == list(range(8)), "key must be a permutation"
    k1 = " · ".join(f"<strong>{i+1} = {LET[key[i]]}</strong> ({esc(L['words'][i])})" for i in range(4))
    k2 = " · ".join(f"<strong>{i+1} = {LET[key[i]]}</strong> ({esc(L['words'][i])})" for i in range(4, 8))
    o.append(f"""                    </ul>
                </div>
            </div>
            {reveal_btn("matchAns")}
            <div class="answers" id="matchAns">
                <p>{k1}</p>
                <p>{k2}</p>
            </div>

            <h3>Now talk — out loud</h3>
            <div class="discuss">
                <strong>Before we read:</strong>
                <ul>
""")
    for b in L["before"]: o.append(f"                    <li>{b}</li>\n")
    o.append("""                </ul>
            </div>
        </div>
    </div>
""")
    # ---- TAB 1 CONVERSATION
    o.append(f"""
    <div class="tab-content">
        <div class="card">
            <h2>The conversation, in three parts</h2>
""")
    if L.get("picture"):
        src, alt, qs = L["picture"]
        o.append(f'            <img class="scene" src="{src}" alt="{esc(alt)}" onerror="ph(this)">\n')
        o.append('            <div class="discuss"><strong>Look at the picture. Say:</strong><ul>' + "".join(f"<li>{esc(q)}</li>" for q in qs) + "</ul></div>\n")
    o.append(f"""
            <p>{esc(L["conv_intro"])}</p>
""")
    for p in L["parts"]:
        o.append(f"""
            <h3>{esc(p["h"])}</h3>
            <div class="story-chunk">
""")
        for who, text in p["lines"]:
            if who:
                o.append(f'                <p><span class="who">{esc(who)}:</span> {esc(text)}</p>\n')
            else:
                o.append(f'                <p class="prose">{esc(text)}</p>\n')
        o.append("""            </div>
            <div class="check">
                <div class="q">Quick check — answer from memory, then reveal:</div>
""")
        for i, (q, a) in enumerate(p["qs"]): o.append(f"                <p>{i+1}. {esc(q)}</p>\n")
        o.append(f"                {reveal_btn()}\n                <div class=\"answers\">\n")
        for i, (q, a) in enumerate(p["qs"]): o.append(f"                    <p><strong>{i+1}.</strong> {esc(a)}</p>\n")
        o.append(f"""                </div>
            </div>
            <div class="discuss">
                <strong>Talk about it:</strong>
                <ul><li>{esc(p["talk"])}</li></ul>
            </div>
""")
    o.append("""        </div>
    </div>
""")
    # ---- TAB 2 GRAMMAR
    o.append(f"""
    <div class="tab-content">
        <div class="card">
            <h2>{L["grammar_h"]}</h2>
            <p>{L["grammar_intro"]}</p>
""")
    for note in L["notes"]: o.append(f'            <div class="note">\n                {note}\n            </div>\n')
    e1 = L["ex1"]
    o.append(f"""
            <h3>{e1["h"]}</h3>
            <p>{e1["intro"]}</p>
            <div class="gap-fill">
""")
    for i, (q, a) in enumerate(e1["items"]):
        o.append(f'                <p>{i+1}. {esc(q).replace("___", GAP)}</p>\n')
    o.append(f"                {reveal_btn('g1')}\n                <div class=\"answers\" id=\"g1\">\n")
    for i, (q, a) in enumerate(e1["items"]): o.append(f"                    <p><strong>{i+1}.</strong> {esc(a)}</p>\n")
    o.append("                </div>\n            </div>\n")
    e2 = L["ex2"]
    o.append(f"""
            <h3>{e2["h"]}</h3>
            <p>{e2["intro"]}</p>
            <div class="gap-fill">
""")
    for i, (q, a) in enumerate(e2["items"]): o.append(f"                <p>{i+1}. {esc(q)}</p>\n")
    o.append(f"                {reveal_btn('g2')}\n                <div class=\"answers\" id=\"g2\">\n")
    for i, (q, a) in enumerate(e2["items"]): o.append(f"                    <p><strong>{i+1}.</strong> {esc(a)}</p>\n")
    o.append("                </div>\n            </div>\n")
    e3 = L["ex3"]
    text = esc(e3["text"]).replace("___", GAP)
    o.append(f"""
            <h3>{e3["h"]}</h3>
            <p>{e3["intro"]}</p>
            <div class="gap-fill">
                <p>{text}</p>
                {reveal_btn('g3')}
                <div class="answers" id="g3">
                    <p>{esc(e3["ans"])}</p>
                    <p>{e3["tip"]}</p>
                </div>
            </div>
        </div>
    </div>
""")
    # ---- TAB 3 ROLE PLAY
    R = L["roleplay"]
    o.append(f"""
    <div class="tab-content">
        <div class="card">
            <h2>Role Play</h2>
            <p>{esc(R["scene"])}</p>
            <div class="note"><strong>Round 1 — you are {esc(R["you"])}.</strong> Read your partner's line, then say your own line from the cue in <em>italics</em>. Use your real answers. Then click to compare with a model.</div>
            <div class="check">
""")
    for partner, cue, model in R["rounds"]:
        o.append(f'                <p class="rp-line"><span class="who" style="font-weight:700;color:#764ba2">{esc(R["partner"])}:</span> {esc(partner)}<br><span class="who" style="font-weight:700;color:#764ba2">You:</span> <span class="you">{esc(cue)}</span></p>\n')
    o.append(f"                {reveal_btn(label='Show a model')}\n                <div class=\"answers\">\n")
    for partner, cue, model in R["rounds"]:
        o.append(f"                    <p><strong>{esc(R['partner'])}:</strong> {esc(partner)}<br><strong>You:</strong> {esc(model)}</p>\n")
    o.append(f"""                </div>
            </div>
            <div class="note"><strong>Round 2 — change roles.</strong> Now you are {esc(R["partner"])}. Ask the questions, and listen to the answers. Then say one thing you remember.</div>

            <h3>Quick-fire questions</h3>
            <p>Answer fast, in full sentences. No time to think. Then check a model answer for the ones that were hard.</p>
            <div class="check">
""")
    for i, (q, model) in enumerate(R["quick"]): o.append(f"                <p>{i+1}. {esc(q)}</p>\n")
    o.append(f"                {reveal_btn(label='Show model answers')}\n                <div class=\"answers\">\n")
    for i, (q, model) in enumerate(R["quick"]): o.append(f"                    <p><strong>{i+1}.</strong> {esc(model)}</p>\n")
    o.append("""                </div>
            </div>
        </div>
    </div>
""")
    # ---- TAB 4 SPEAK
    o.append(f"""
    <div class="tab-content">
        <div class="card">
            <h2>Speak</h2>
            <p>Do all three tasks out loud. Use the timer to keep talking.</p>

            <div class="note">{L["useful"]}</div>

            <div class="timer">
                <span>Time remaining: <strong><span id="timer-display">1:00</span></strong></span>
                <div class="timer-controls">
                    <button class="duration-btn active" onclick="setDuration(this, 1)">1 min</button>
                    <button class="duration-btn" onclick="setDuration(this, 2)">2 min</button>
                    <button class="duration-btn" onclick="setDuration(this, 3)">3 min</button>
                    <button class="timer-btn" onclick="startTimer()">Start</button>
                    <button class="timer-btn secondary" onclick="resetTimer()">Reset</button>
                </div>
            </div>
""")
    for T in (L["taskA"], L["taskB"], L["taskC"]):
        o.append(f'\n            <div class="speak-prompt">\n                <span class="speak-label">{esc(T["h"])}</span>\n')
        for p in T["p"]: o.append(f"                <p>{p}</p>\n")
        o.append("            </div>\n")
    o.append("""
            <div class="final-discussion">
                <h3>To finish</h3>
                <ol>
""")
    for f_ in L["finish"]: o.append(f"                    <li>{f_}</li>\n")
    o.append(f"""                </ol>
            </div>
        </div>
    </div>

    <footer>
        {SERIES} · {esc(L["title"])} · A1
    </footer>
</div>

<script>{js}
function ph(img){{ var d=document.createElement("div"); d.className="scene-ph"; d.textContent="Picture: " + img.getAttribute("src"); img.replaceWith(d); }}</script>
</body>
</html>
""")
    out = "".join(o)
    out = out.replace("let timeRemaining = 180;", "let timeRemaining = 60;").replace("let currentDuration = 180;", "let currentDuration = 60;")
    return out

if __name__ == "__main__":
    t = open(TEMPLATE, encoding="utf-8").read()
    css = re.search(r"<style>(.*?)</style>", t, re.S).group(1)
    js = re.search(r"<script>(.*?)</script>", t, re.S).group(1)
    for i, L in enumerate(LESSONS):
        prev = LESSONS[i-1] if i > 0 else None
        nxt = LESSONS[i+1] if i+1 < len(LESSONS) else None
        path = os.path.join(OUT, fname(L))
        with open(path, "w", encoding="utf-8") as f:
            f.write(build(L, prev, nxt, css, js))
        print("wrote", os.path.basename(path), os.path.getsize(path), "bytes")
