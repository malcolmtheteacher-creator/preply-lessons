L = dict(
file='psy_01_marshmallow_a2b1.html', level='A2/B1',
title='The Marshmallow Test',
subtitle='A child can have one sweet now, or two sweets if they wait. What would you do?',
grammar_name='If + will',
intention="you'll tell the story of the marshmallow test and use 'if + will' to talk about choices and results.",
vocab_intro='Eight words, three short activities. Say each answer out loud before you reveal.',
warmup=[
 "Think of something you really want. Can you wait for it, or do you want it now?",
 "What helps you to wait? Is it easy or difficult for you?",
 "Do you think children today can wait as well as children before?"],
vocab=[
 dict(head="What does the word mean?", intro="Read the sentence and say what the bold word means. Then reveal.", items=[
  ("1. I want to <b>wait</b> for the bus. It comes in five minutes.","<b>wait</b> (v) — to stay in one place until something happens."),
  ("2. She has a lot of <b>self-control</b>. She never eats the cake before dinner.","<b>self-control</b> (n) — the power to stop yourself doing something you want to do."),
  ("3. This is a <b>reward</b> for your hard work: a free coffee!","<b>reward</b> (n) — something good you get because you did something well.")]),
 dict(head="Which word is it?", intro="Say the word. The first letter helps you. Then reveal.", items=[
  ("4. Which word means 'at this moment'? <em>(n___)</em>","<b>now</b> (adv) — at the present time. Example: \"I want it now!\""),
  ("5. Which word means 'to test something to learn about it'? <em>(e__________)</em>","<b>experiment</b> (n) — a test that helps people learn something. Example: \"The scientist did an experiment.\""),
  ("6. Which word means 'to look at someone or something carefully for some time'? <em>(w_____)</em>","<b>watch</b> (v) — Example: \"The scientists watched the children through a window.\"")]),
 dict(head="Complete the phrase", intro="Which word completes the phrase?", items=[
  ("7. A child can eat the sweet now, or ______ and get two sweets later. <em>(w___)</em>","<b>wait</b> — wait and get two. Notice: <em>wait for</em> + thing (wait for a bus), <em>wait</em> alone at the end of a sentence."),
  ("8. Later in life, she was <b>successful</b>: she had a good job and a happy family.<br>What does <b>successful</b> mean? (a) very tired &nbsp; (b) doing well in life &nbsp; (c) very young","<b>successful</b> (adj) — answer (b). Doing well; getting what you want in life.")]),
],
vocab_talk=["Use <em>reward</em>, <em>wait</em> and <em>self-control</em> to guess what the experiment is about.","What is a good reward for you? Is it worth waiting for?"],
parts=[
 dict(head="The experiment", text=[
  "In the 1960s, a scientist called Walter Mischel did an experiment at a university in the USA. He worked with children who were three to five years old.",
  "A child sat alone in a small room. On the table there was one marshmallow, a soft white sweet. The adult said: \"You can eat this marshmallow now. But if you wait for me to come back, you will get two marshmallows.\" Then the adult left the room for about fifteen minutes."],
  check=("How old were the children?","What did the adult say?","Three to five years old.","If you wait, you will get two marshmallows. (If you eat now, you get one.)"),
  discuss="What would you do at four years old? What would you do now?"),
 dict(head="What the children did", text=[
  "Some children ate the marshmallow in a few seconds. Other children waited. They sang songs, covered their eyes, or turned their chairs round. One child smelled the marshmallow, then put it down quickly!",
  "About one third of the children waited the whole fifteen minutes and got two marshmallows. The scientists watched them through a window."],
  check=("What did the waiting children do?","How many children waited the full time?","They sang, covered their eyes, or looked away.","About one third."),
  discuss="Which trick do you think works best for waiting? Do you have a trick of your own?"),
 dict(head="Years later", text=[
  "The scientists followed many of the children for years. They said that the children who waited were often more successful later. They did better at school and often had better jobs.",
  "But new research says the story is not so simple. Children from richer families often waited longer, and they also did better at school. Maybe family money, not only self-control, helped them. So what do you think is the real reason?"],
  check=("What did the first research say?","What does new research say?","The children who waited were often more successful.","Family money may be important too; the story is not so simple."),
  discuss="Can a child's life be decided by one small test? Why or why not?"),
],
grammar=dict(title="If + will (real choices)",
 intro="We use <strong>if + present simple, will + verb</strong> to talk about real choices and their results.",
 notes=["<strong>The pattern:</strong><br>• <em>If you wait, you will get two marshmallows.</em><br>• <em>If she eats it now, she won't get another one.</em><br>The <strong>if part</strong> uses the present simple (not will!). The <strong>result</strong> uses will or won't.",
        "<strong>Question form:</strong> <em>What will you do if you feel hungry?</em><br>You can put the <em>if</em> part first or second: <em>I'll wait if I can.</em> (no comma in the second position)."],
 exercises=[
  dict(title="Complete the sentence", intro="Type the missing word.", lines=[
   "1. If you wait, you __ get two sweets. <em>(future)</em>",
   "2. If it rains, we __ stay at home. <em>(negative future: one word)</em>",
   "3. She will be happy if she __ the reward. <em>(verb: get)</em>"],
   answers=["<strong>1.</strong> will","<strong>2.</strong> won't","<strong>3.</strong> gets"]),
  dict(title="Right or wrong?", intro="Two of these sentences are wrong. Type the correct word in the gap.", lines=[
   "1. If I will wait, I will win. &nbsp;→ If I __ , I will win.",
   "2. If she eats it, she won't get two. &nbsp;→ If she __ it, she won't get two.",
   "3. If they will go now, they will be late. &nbsp;→ If they __ now, they will be late."],
   answers=["<strong>1.</strong> wait <em>(not 'will wait')</em>","<strong>2.</strong> eats <em>(this sentence is correct)</em>","<strong>3.</strong> go <em>(not 'will go')</em>"]),
  dict(title="Make your own", intro="Finish the sentence, then say the whole sentence aloud.", lines=[
   "1. If I wait for a month, I __ .",
   "2. If I don't wait, I __ ."],
   answers=["<strong>1.</strong> I will + verb (for example: I will have more money.)","<strong>2.</strong> I won't + verb, or I will + verb (for example: I won't have enough.)"]),
 ],
 closing="Remember: after if, use the present simple. Not 'if I will wait'."),
think=dict(title="Wait or not?", intro="Five choices. Say what you will do and why. Then reveal an idea.",
 items=[
  ("1. A friend offers you £10 today, or £15 next week. Which one do you choose?","<b>Idea.</b> Many people take £10 now. Taking £15 is a bit like the second marshmallow: you must wait."),
  ("2. You can watch one episode tonight, or save the whole season for the weekend. What do you do?","<b>Idea.</b> If you wait, the weekend will be more fun. If you don't wait, you will have a short happy time tonight."),
  ("3. You can buy new shoes now, or save money for a holiday. What do you do?","<b>Idea.</b> Saving is waiting for a bigger reward. Which reward is more important to you?"),
  ("4. A child sees a marshmallow and nobody is looking. Does it matter if the child eats it?","<b>Idea.</b> Perhaps it matters less than people say. The child is only four!"),
  ("5. Can you teach a person self-control, or are some people born with more?","<b>Idea.</b> Many scientists think you can practise it, a bit like a muscle.")],
 extras=[
  dict(head="Imagine this", label="Imagine:", items=[
   "You are the adult in the room. A child begins to cry. Do you come back early?",
   "Your friend says, 'I have no self-control.' What advice will you give? Use 'If you...'."])]),
speak=dict(language="<em>If you wait, you will…</em>, <em>I think…</em>, <em>for example…</em>, <em>That is true, but…</em>, <em>The first thing is…</em>.",
 tasks=[
  ("Task A · Tell the story (3 minutes)",["Tell the marshmallow story to a friend who does not know it. Use these steps: <em>the room → the offer → what the children did → years later → the new research.</em>","Use at least <strong>four key words</strong> (wait, reward, self-control, experiment, watch, successful) and two <strong>if + will</strong> sentences."]),
  ("Task B · What will you do? (3 minutes)",["Talk about something you want. Say what you will do if you wait, and what you will do if you don't."]),
  ("Task C · Your tip (3 minutes)",["Give three tips for people who want better self-control.","<strong>Need an idea? Choose one:</strong><ul style=\"margin:6px 0 0 20px; color:#3a2a5a;\"><li>Saving money.</li><li>Studying every day.</li><li>Eating less sugar.</li><li>Using your phone less.</li><li>Getting up early.</li></ul>"])],
 final=["Is it always good to wait? Can you wait too long?","Is it fair to say a child is 'bad' at self-control from one test?","<strong>Before you go, from memory:</strong> say two sentences with <em>if + will</em> about the marshmallow test. Then explain the experiment in one minute."]),
)
