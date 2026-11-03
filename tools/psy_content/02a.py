L = dict(
file='psy_02_invisible_gorilla_a2b1.html', level='A2/B1',
title='The Invisible Gorilla',
subtitle='You watch a short video and count passes. Will you see the gorilla?',
grammar_name='past continuous and past simple',
intention="you'll tell the story of an attention experiment and use the past continuous and past simple together.",
vocab_intro='Eight words, three short activities. Say each answer out loud before you reveal.',
warmup=[
 "Have you ever not seen something that was right in front of you? What was it?",
 "Can you do two things well at the same time, for example talk and drive?",
 "What do you look at first when you enter a room?"],
vocab=[
 dict(head="What does the word mean?", intro="Read the sentence and say what the bold word means. Then reveal.", items=[
  ("1. Please <b>pay attention</b>. This is important.","<b>pay attention</b> — to listen or look carefully at something."),
  ("2. I didn't <b>notice</b> your new haircut. Sorry!","<b>notice</b> (v) — to see or realise something."),
  ("3. The <b>gorilla</b> in the video walked across the room.","<b>gorilla</b> (n) — a very big, strong animal like a monkey. (In the video, it is a person in a gorilla costume.)")]),
 dict(head="Which word is it?", intro="Say the word. The first letter helps you. Then reveal.", items=[
  ("4. Which word means 'to say the numbers one, two, three…'? <em>(c____)</em>","<b>count</b> (v) — Example: \"Count the passes!\""),
  ("5. Which word means 'to throw a ball to another player'? <em>(p___)</em>","<b>pass</b> (v) — Example: \"She passed the ball to her friend.\""),
  ("6. Which word means 'surprising'? <em>(a_______)</em>","<b>amazing</b> (adj) — Example: \"The result was amazing.\"")]),
 dict(head="Complete the phrase", intro="Which word completes the phrase?", items=[
  ("7. About half of the people didn't ______ the gorilla. <em>(s__)</em>","<b>see</b> — didn't see the gorilla. Also: <em>miss</em> (didn't see) is common: \"They missed it.\""),
  ("8. The students were <b>busy</b> counting. What does <b>busy</b> mean? (a) with a lot to do right now &nbsp; (b) very tired &nbsp; (c) very happy","<b>busy</b> (adj) — answer (a). Doing something and having no time for other things.")]),
],
vocab_talk=["Use <em>count</em>, <em>pass</em> and <em>gorilla</em> to guess what the experiment is.","Why is it difficult to <em>pay attention</em> to two things at once?"],
parts=[
 dict(head="The video", text=[
  "In 1999, two scientists, Daniel Simons and Christopher Chabris, made a short video. In it, six students were passing basketballs. Three students wore white shirts and three wore black shirts.",
  "People watched the video and had one job: count how many times the white team passed the ball. While they were counting, something strange happened. A person in a gorilla costume walked into the middle of the room. The gorilla stopped, hit its chest, and walked out. It was on the screen for about nine seconds."],
  check=("What was the job?","What happened in the middle of the video?","To count the passes of the white team.","A person in a gorilla costume walked in, hit its chest and walked out."),
  discuss="Do you think you would see the gorilla? Why or why not?"),
 dict(head="The surprise", text=[
  "About half of the people did not see the gorilla. They were looking at the screen, and the gorilla was right there. But they were busy with the passes, so they didn't notice it.",
  "When people watched the video again, with no job to do, they saw the gorilla easily. Many said, \"That's a different video!\" It wasn't. Scientists call this inattentional blindness: when you don't notice something because your attention is somewhere else."],
  check=("How many people missed the gorilla?","What do scientists call it?","About half.","Inattentional blindness: not noticing something because you are paying attention to something else."),
  discuss="Have you ever said, 'That's impossible, I didn't see it!'?"),
 dict(head="Why it matters", text=[
  "This idea is important in real life. A driver can look at the road, but not see a cyclist if he is thinking about something else. A person who is using a phone while walking can miss a lamp post!",
  "In one study, doctors who were looking at medical scans missed a small picture of a gorilla on a scan, even when their eyes were looking right at it. The lesson is not that people are stupid. It is that attention is limited: we cannot see everything at once."],
  check=("Give one example from real life.","What is the main lesson?","A driver who doesn't see a cyclist; a person who walks into a lamp post.","Attention is limited: we cannot notice everything at once."),
  discuss="When is it dangerous not to notice something? What can you do about it?"),
],
grammar=dict(title="past continuous and past simple",
 intro="Use the <strong>past continuous</strong> for an action in progress and the <strong>past simple</strong> for a short action that interrupted it.",
 notes=["<strong>The pattern:</strong><br>• <em>I was counting</em> (long action) <em>when the gorilla walked in</em> (short action).<br>• Past continuous: <strong>was / were + verb-ing</strong>.<br>• Past simple: <strong>verb + ed</strong> or an irregular verb (walked, hit, saw).",
        "<strong>Use while and when:</strong><br>• <em>While</em> + past continuous: <em>While they were counting, the gorilla walked in.</em><br>• <em>When</em> + past simple: <em>They were counting when the gorilla walked in.</em><br>With a verb like <em>know, see, like</em> we usually use the past simple only."],
 exercises=[
  dict(title="Past continuous or past simple?", intro="Type the correct form of the verb in brackets.", lines=[
   "1. The students __ (pass) the balls when the gorilla walked in.",
   "2. The gorilla __ (walk) into the room at second 15.",
   "3. While I __ (watch) the video, my friend called me."],
   answers=["<strong>1.</strong> were passing","<strong>2.</strong> walked","<strong>3.</strong> was watching"]),
  dict(title="Two actions", intro="Choose the long action (past continuous) and the short action (past simple). Type the verbs.", lines=[
   "1. I __ (cross) the road when a car __ (appear).",
   "2. She __ (read) a message when the bus __ (arrive)."],
   answers=["<strong>1.</strong> was crossing · appeared","<strong>2.</strong> was reading · arrived"]),
  dict(title="Your sentences", intro="Finish each sentence with your own idea, then say it aloud.", lines=[
   "1. I was walking home when __ .",
   "2. While I was cooking dinner, __ ."],
   answers=["<strong>1.</strong> a short action in the past simple (for example: it started to rain.)","<strong>2.</strong> a short action in the past simple (for example: my phone rang.)"]),
 ],
 closing="Remember: the long action in the past continuous, the short action in the past simple."),
think=dict(title="Did you notice?", intro="Five situations. Say whether the person probably noticed or missed it and why. Then reveal an idea.",
 items=[
  ("1. A man was talking on his phone while he was walking. A friend waved at him from the other side of the road. Did he see her?","<b>Idea.</b> Probably not. His attention was on the phone."),
  ("2. A teacher was writing on the board. A student at the back was drawing. Did the student hear the question?","<b>Idea.</b> Maybe not. The student was busy with the drawing."),
  ("3. A driver was looking for a street name. A child ran out. Did the driver see the child?","<b>Idea.</b> It is possible that the driver missed the child. That is why drivers must pay attention."),
  ("4. You were reading a book on a train. Your station was called. Did you hear it?","<b>Idea.</b> It depends how interesting the book is!"),
  ("5. Is it easier to notice something if you know it is coming?","<b>Idea.</b> Yes. When people know about the gorilla, they see it. Knowing what to look for helps attention.")],
 extras=[
  dict(head="Imagine this", label="Imagine:", items=[
   "You are making a new 'invisible' video. What will you hide in it? What job will you give the watchers?",
   "Your friend is crossing the road and looking at their phone. What will you say to them?"])]),
speak=dict(language="<em>was/were + -ing</em> … <em>when</em> …, <em>First…, then…, in the end…</em>, <em>I think…</em>, <em>That is surprising because…</em>.",
 tasks=[
  ("Task A · Tell the story (3 minutes)",["Tell the gorilla story to a friend. Use these steps: <em>the video → the job → the gorilla → what half of the people did → why it matters.</em>","Use at least <strong>four key words</strong> (attention, notice, count, pass, gorilla, amazing, busy) and two sentences with <strong>was/were + -ing</strong>."]),
  ("Task B · A time you missed it (3 minutes)",["Tell a story about a time you didn't notice something important. Say what you were doing when it happened."]),
  ("Task C · Be safe (3 minutes)",["Give three tips for staying safe when your attention is busy.","<strong>Need an idea? Choose one:</strong><ul style=\"margin:6px 0 0 20px; color:#3a2a5a;\"><li>Crossing the road.</li><li>Driving a car.</li><li>Riding a bike.</li><li>Cooking.</li><li>Studying with a phone next to you.</li></ul>"])],
 final=["Would you be a good eyewitness after an accident? Why or why not?","Is it better to do one thing at a time?","<strong>Before you go, from memory:</strong> say two sentences with <em>was/were + -ing</em> and a past simple verb about the gorilla video. Then explain the experiment in one minute."]),
)
