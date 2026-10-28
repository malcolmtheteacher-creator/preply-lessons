L = dict(
file='psy_04_can_you_trust_memory_a2b1.html', level='A2/B1',
title='Can You Trust Your Memory?',
subtitle='People watch a car accident. One word in a question changes what they remember.',
grammar_name='past simple',
intention="you'll tell the story of a memory experiment using the past simple, with regular and irregular verbs.",
vocab_intro='Eight words, three short activities. Say each answer out loud before you reveal.',
warmup=[
 "What is your earliest memory? How sure are you that it is true?",
 "Do you remember things better with photos, or is your memory good without them?",
 "Have you and a friend ever remembered the same event in different ways?"],
vocab=[
 dict(head="What does the word mean?", intro="Read the sentence and say what the bold word means. Then reveal.", items=[
  ("1. I <b>remember</b> my first day at school very well.","<b>remember</b> (v) — to keep something in your mind from the past."),
  ("2. She <b>forgot</b> her keys, so she couldn't open the door.","<b>forget</b> (v) — the opposite of remember. Past: <em>forgot</em>."),
  ("3. The <b>witness</b> saw the accident and told the police what happened.","<b>witness</b> (n) — a person who sees something happen, for example a crime or an accident.")]),
 dict(head="Which word is it?", intro="Say the word. The first letter helps you. Then reveal.", items=[
  ("4. Which word means 'a sudden crash between two cars'? <em>(a_______)</em>","<b>accident</b> (n) — Example: \"There was an accident on the motorway.\""),
  ("5. Which word means 'moving at a high speed'? <em>(f___)</em>","<b>fast</b> (adj/adv) — Example: \"The car was going very fast.\" The opposite is <em>slow</em>."),
  ("6. Which word means 'broken pieces of window or bottle'? <em>(g____)</em>","<b>glass</b> (n) — Example: \"There was broken glass on the road.\"")]),
 dict(head="Complete the phrase", intro="Which word completes the phrase?", items=[
  ("7. Do you remember what you ______ yesterday? <em>(d__)</em>","<b>did</b> — past simple of <em>do</em>. Irregular verbs: do → did, see → saw, go → went."),
  ("8. A <b>question</b> can change your memory.<br>What does <b>question</b> mean? (a) a sentence you ask to get information &nbsp; (b) a kind of answer &nbsp; (c) a story","<b>question</b> (n) — answer (a). Something that you ask to learn something.")]),
],
vocab_talk=["Use <em>witness</em>, <em>accident</em> and <em>remember</em> to guess what the experiment is.","Which verbs in the lesson are irregular? Say the past forms: see, go, say, do."],
parts=[
 dict(head="The film", text=[
  "In 1974, a scientist called Elizabeth Loftus did an experiment in the USA. Students watched short films of car accidents. After each film, the scientists asked questions.",
  "One question was: 'How fast were the cars going?' But there was a trick. For some students, the question used the word 'hit'. For other students, the question used the word 'smashed'. Everything else was the same."],
  check=("What did the students watch?","What was the trick?","Short films of car accidents.","The question used a different word: 'hit' or 'smashed'."),
  discuss="Would one word change your memory? What do you think?"),
 dict(head="The result", text=[
  "The students who heard 'smashed' said the cars were going faster. They said about 41 miles an hour. The students who heard 'hit' said about 34 miles an hour. It was the same film!",
  "One week later, the students came back. The scientists asked, 'Did you see any broken glass?' There was no broken glass in the film. But about one third of the 'smashed' students said yes. Only about one in seven of the 'hit' students said yes."],
  check=("What speed did the 'smashed' group say?","What did the students say about broken glass a week later?","About 41 miles an hour; the 'hit' group said about 34.","The 'smashed' group often said they saw broken glass, but there was none."),
  discuss="Why do you think the word 'smashed' changed the memory?"),
 dict(head="Why it matters", text=[
  "Memory is not like a video. When we remember something, we build the memory again, and new information can change it. This can happen with words, with photos, or with other people's stories.",
  "This is very important in a police station or in a court. A witness can be very sure about a memory, and still be wrong. Good police officers ask questions carefully, without leading words."],
  check=("Is memory like a video?","Why is this important in court?","No. We build the memory again each time.","A witness can feel sure and still be wrong."),
  discuss="Do you trust your memory? Are some memories more reliable than others?"),
],
grammar=dict(title="past simple (regular and irregular)",
 intro="Use the <strong>past simple</strong> to talk about finished actions in the past.",
 notes=["<strong>Regular verbs:</strong> add <strong>-ed</strong> — <em>watch → watched, ask → asked, remember → remembered</em>.<br><strong>Irregular verbs:</strong> change the word — <em>see → saw, go → went, say → said, forget → forgot, do → did</em>.",
        "<strong>Questions and negatives:</strong> use <strong>did / didn't + the base verb</strong>.<br>• <em>Did you see any glass?</em> — <em>No, I didn't see any glass.</em><br>• Not: <em>Did you saw</em>. After did, the verb stays in the base form."],
 exercises=[
  dict(title="Past simple", intro="Type the past simple form of the verb.", lines=[
   "1. The students __ (watch) a film.",
   "2. They __ (see) a car accident.",
   "3. One week later, they __ (say) they saw broken glass."],
   answers=["<strong>1.</strong> watched","<strong>2.</strong> saw","<strong>3.</strong> said"]),
  dict(title="Questions and negatives", intro="Type the missing word.", lines=[
   "1. __ you see any broken glass? <em>(question; one word)</em>",
   "2. There __ any glass in the film. <em>(negative of was; one word)</em>",
   "3. She didn't __ (forget) the answer."],
   answers=["<strong>1.</strong> Did","<strong>2.</strong> wasn't","<strong>3.</strong> forget <em>(after didn't, base form)</em>"]),
  dict(title="Your story", intro="Finish each sentence with your own idea, then say it aloud.", lines=[
   "1. Yesterday I __ .",
   "2. I didn't __ ."],
   answers=["<strong>1.</strong> a past simple verb (for example: went to the supermarket.)","<strong>2.</strong> a base verb (for example: forget my keys.)"]),
 ],
 closing="Remember: after did or didn't, use the base verb. Not 'did you saw'."),
think=dict(title="What do you remember?", intro="Five situations. Say whether the memory could be wrong, and why. Then reveal an idea.",
 items=[
  ("1. You remember a childhood holiday very clearly, but you have only seen the photos. Is your memory real?","<b>Idea.</b> It may be partly a memory of the photos. Photos can change what we remember."),
  ("2. Two friends remember the same party in different ways. Who is right?","<b>Idea.</b> Maybe both are partly right. Memory is not exact."),
  ("3. A witness says, 'I am 100% sure.' Is she right?","<b>Idea.</b> Being sure does not mean being right. Sure and correct are different."),
  ("4. A teacher asks, 'Did you see the thief's red hat?' (there was no hat). What may happen?","<b>Idea.</b> Some students may remember a red hat later. The question gives them new information."),
  ("5. How can you remember things better?","<b>Idea.</b> Write it down soon. Say it aloud. Sleep well.")],
 extras=[
  dict(head="Imagine this", label="Imagine:", items=[
   "You are a police officer. What will you say to a witness at the start of the interview? Which words will you not use?",
   "You and your friend remember an old argument differently. How will you decide who is right?"])]),
speak=dict(language="<em>Yesterday I…</em>, <em>First…, then…, after that…</em>, <em>I didn't…</em>, <em>I think…</em>, <em>That is surprising because…</em>",
 tasks=[
  ("Task A · Tell the story (3 minutes)",["Tell the Loftus story to a friend. Use these steps: <em>the film → the question → the two words → the speeds → a week later → why it matters.</em>","Use at least <strong>four key words</strong> (remember, witness, accident, question, glass, forget) and six <strong>past simple</strong> verbs."]),
  ("Task B · A memory (3 minutes)",["Tell a story about a memory you are not sure about. Say what you remember, and what you are not sure about."]),
  ("Task C · Good questions (3 minutes)",["You are a police officer. Make five fair questions for a witness of a bike accident.","<strong>Need an idea? Choose one:</strong><ul style=\"margin:6px 0 0 20px; color:#3a2a5a;\"><li>A stolen bag.</li><li>A car crash.</li><li>A fight in the street.</li><li>A lost child.</li><li>A burglary.</li></ul>"])],
 final=["Is it a problem that memory changes?","Would you like to remember everything perfectly?","<strong>Before you go, from memory:</strong> say three sentences about the experiment in the past simple. Then tell the story in one minute."]),
)
