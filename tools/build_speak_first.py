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
    o.append(f'    <p class="crosslink">Lesson {n} of the series. {" · ".join(links)}</p>\n')
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
