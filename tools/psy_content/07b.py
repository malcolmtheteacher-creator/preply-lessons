L = dict(
file='psyp_07_replication_crisis_b2c1.html', level='B2/C1', series='Psychology Questions: Going Deeper', tag='PSYCHOLOGY FOR PROFESSIONALS', anchor='#deeper',
title='Can We Repeat the Result?',
subtitle='When a field tries to reproduce its own findings and fails more often than it expected, what should it conclude?',
grammar_name='nominalisation',
intention="you'll evaluate the replication crisis and its remedies, and use nominalisation to write about research in a compact, academic register.",
warmup=[
 "Think of a finding you were taught as established that you later saw challenged. How did it change how you read the literature?",
 "How much of your field's published literature would you expect to replicate?",
 "Who bears the responsibility for unreliable findings: researchers, journals, funders or the incentives?"],
vocab=[
 dict(head="What does the bold word mean here?", intro="Read the sentence aloud and say what you think the bold word means from the context, then reveal.", items=[
  ("1. <b>P-hacking</b> is the practice of trying different analyses until a result crosses the threshold for significance.","<b>p-hacking</b> (n) — adjusting analyses, exclusions or outcomes until p < .05 is reached. Related: <em>researcher degrees of freedom</em>."),
  ("2. <b>Publication bias</b> means that journals favour positive findings, so the literature overstates the effects.","<b>publication bias</b> (n) — the tendency for significant results to be published more than null ones. Also <em>the file-drawer problem</em>."),
  ("3. A <b>registered report</b> is peer-reviewed and accepted in principle before the data are collected, so the result cannot affect publication.","<b>registered report</b> (n) — a journal format that judges the question and method before the results are known.")]),
 dict(head="Which word means…?", intro="Say the word before you reveal. The first letter is given.", items=[
  ("4. Which word means \"the size of a difference or relationship, independent of sample size\"? <em>(e_____ s___)</em>","<b>effect size</b> (n) — Example: \"The replications found an effect size about half that of the originals.\""),
  ("5. Which word means \"a statistical test that you decide in advance\"? <em>(c______________)</em>","<b>confirmatory</b> (adj) — a <em>confirmatory analysis</em> tests a pre-specified hypothesis; <em>exploratory</em> analyses generate new ones."),
  ("6. Which word means \"relating to the ability of other teams to get the same results from the same data\"? <em>(r_____________)</em>","<b>reproducible</b> (adj) — <em>Reproducibility</em> (same data, same analysis) differs from <em>replicability</em> (new data, same question).")]),
 dict(head="Complete the phrase", intro="These words go with particular partners. Complete each chunk.", items=[
  ("7. A single underpowered study can easily produce a ______ positive. <em>(f____)</em>","<b>false</b> positive — a result that looks significant but is not real."),
  ("8. The original finding did not ______ in larger, preregistered samples. <em>(h___ u_)</em>","<b>hold up</b> (v) — to remain valid when tested again. Also: <em>stand up to scrutiny</em>."),
  ("9. The journal's policy ______ authors to share their data and code. <em>(e________)</em>","<b>encourages</b> (v) — to give support or incentive. Compare <em>requires</em>, <em>mandates</em>.")]),
 dict(head="Choose the best meaning", intro="Read the sentence, choose a, b or c, then reveal.", items=[
  ("10. The result may depend on a <b>moderator</b> that the original authors did not measure.<br>(a) a person who leads a discussion &nbsp; (b) a variable that changes the strength or direction of an effect &nbsp; (c) a kind of statistical error","<b>moderator</b> (n) — answer (b). Example: age or culture may moderate an effect. A failed replication may reflect an unrecognised moderator.")]),
],
vocab_talk=["Using <em>p-hacking</em>, <em>publication bias</em> and <em>effect size</em>, explain in your own words how a literature can look stronger than the evidence.","Which of the ten words are about researchers' behaviour, which about journals and which about statistics? Sort them and say why."],
parts=[
 dict(head="The warnings", text=[
  "In 2011, two events shook social psychology. One was the publication, in a leading journal, of a series of experiments claiming that people could sense future events. Few colleagues believed it, but the studies had followed the standard rules. The question that followed was uncomfortable: if the field's methods can publish this, what else do they publish?",
  "The second was a paper by Joseph Simmons, Leif Nelson and Uri Simonsohn showing that flexible analysis can make almost anything look significant. By making a handful of apparently reasonable choices about sample size, exclusions and outcome measures, they 'demonstrated' that listening to a particular song made participants younger by about eighteen months. Later surveys of researchers suggested that some of these questionable practices were common, and many were barely seen as wrong."],
  check=("Why did the 2011 experiments cause concern?","What did Simmons and colleagues demonstrate?","Because methods that followed the standard rules had published an implausible claim.","That flexible analysis can produce a significant result for something absurd."),
  discuss="Where is the line between legitimate flexibility in analysis and p-hacking?"),
 dict(head="The big test", text=[
  "In 2015, the Open Science Collaboration, a group of around 270 researchers, attempted to replicate 100 studies published in 2008 in three leading journals. Although 97 of the originals had reported significant results, only about 36 of the replications did, and the average effect size was roughly half of the original. The results varied by sub-field: studies in cognitive psychology replicated more often than those in social psychology.",
  "The interpretation has been contested. Some argued that the replications differed from the originals in ways that mattered, or that a single failure is weak evidence. Others pointed out that the pattern fits what publication bias and low statistical power would produce. The most careful reading is that the field's published effects were, on average, overestimated, and that some of them are probably not real."],
  check=("What did the project find?","Why is the interpretation contested?","Only about 36 of 100 replications were significant, and effect sizes were about half the originals'.","Because replications may differ in important ways, and one failure is weak evidence; but the pattern also fits publication bias and low power."),
  discuss="How should a single failed replication change your confidence in an original finding?"),
 dict(head="Reform", text=[
  "The response has been unusually practical. Researchers now preregister hypotheses and analysis plans, so a confirmatory test is distinguished from an exploratory one. Registered reports commit a journal to publish a study based on its question and method, regardless of the result. Large multi-lab projects test effects across many samples at once, and journals increasingly encourage or require open data and code.",
  "None of this is free. Larger samples are costly, and early-career researchers who report null results may find them harder to publish. Yet there is cautious evidence of improvement: preregistered studies report fewer significant results and smaller effects, which is exactly what we would expect if earlier results were inflated. Many researchers argue the crisis has become, in effect, a revolution in credibility."],
  check=("What does a registered report do?","What cost does reform bring?","It commits the journal to publish a study based on its question and method, before the results are known.","Larger samples cost more, and null results may still be harder to publish, especially for early-career researchers."),
  discuss="Which incentives would you change first: journals, funders or universities?"),
],
grammar=dict(title="nominalisation",
 intro="Nominalisation turns verbs and adjectives into nouns. It is the engine of academic and professional writing: it lets you pack a process or a quality into a short noun phrase and make it the subject of a sentence.",
 notes=["<strong>Common transformations:</strong><br>• <em>fail → failure</em>: \"The study <em>failed</em> to replicate\" → \"The <em>failure</em> to replicate raised concerns.\"<br>• <em>analyse → analysis</em>, <em>publish → publication</em>, <em>select → selection</em>, <em>reliable → reliability</em>, <em>flexible → flexibility</em><br>• <em>researchers changed their methods</em> → <em>a change in methods</em> / <em>a shift in practice</em>",
        "<strong>Why use it?</strong><br>• To avoid long clauses: <em>The fact that researchers selected outcomes selectively caused distortion</em> → <em>Selective reporting caused distortion.</em><br>• To link ideas: <em>The flexibility of analysis leads to inflated effects.</em><br>• Be careful: too many nominalisations make writing heavy. Mix them with clear verbs."],
 exercises=[
  dict(title="Make the noun", intro="Type the noun form of the word in brackets.", lines=[
   "1. The __ (fail) to replicate the study raised concerns.",
   "2. Greater __ (transparent) has improved trust in research.",
   "3. The __ (select) of outcomes after seeing the data is a problem."],
   answers=["<strong>1.</strong> failure","<strong>2.</strong> transparency","<strong>3.</strong> selection"]),
  dict(title="Fix the form", intro="Each sentence needs the noun form. Type it.", lines=[
   "1. Researchers publish only positive results. → The __ (publish) of only positive results distorts the literature.",
   "2. The test is reliable. → The __ (reliable) of the test is high.",
   "3. People analysed the data in several ways. → The __ (analyse) of the data in several ways raised the risk of false positives."],
   answers=["<strong>1.</strong> publication","<strong>2.</strong> reliability","<strong>3.</strong> analysis"]),
  dict(title="Compress the sentence", intro="Complete the new sentence so that it means the same as the first.", lines=[
   "1. Researchers decided in advance how they would analyse the data, and this reduced bias. → __ the analysis in advance reduced bias.",
   "2. Journals have begun to require data sharing, and this is a significant development. → The __ to require data sharing is significant.",
   "3. It is hard to repeat these studies, and this limits progress. → The __ of repeating these studies limits progress."],
   answers=["<strong>1.</strong> Specifying <em>(or \"Planning\", \"Fixing\")</em>","<strong>2.</strong> decision <em>(or \"move\", \"shift\")</em>","<strong>3.</strong> difficulty"]),
 ],
 closing="Keep these ready for the Speak tab, where you will describe the causes and consequences of unreliable research in a compact way."),
think=dict(title="How much would you believe it?", intro="Five claims. Say how far you would trust each and what you would want to see. Then reveal.",
 items=[
  ("1. \"Psychology has been shown to be unreliable.\"","<b>Too broad.</b> Replicability varies by sub-field and method; some effects are very robust. The accurate claim is that many published effects were overestimated."),
  ("2. \"A failed replication means the original was wrong.\"","<b>Not necessarily.</b> The replication could differ in sample, context or power; but repeated failures should lower confidence."),
  ("3. \"Preregistration solves the problem.\"","<b>Helps, does not solve.</b> It separates exploratory from confirmatory work, but it cannot fix poor measurement or weak theory."),
  ("4. \"The crisis shows the scientific method is working.\"","<b>Partly.</b> Science corrects itself, but slowly and with costs; correction depends on incentives that reward checking."),
  ("5. \"Larger samples are always better.\"","<b>An oversimplification.</b> Large samples reduce error but not bias; a large, badly measured study can still mislead.")],
 extras=[
  dict(head="A thought experiment", label="Imagine this:", items=[
   "You are the editor of a journal. You can change one policy to improve reliability. Which one and why?",
   "A well-known effect you teach has failed to replicate twice. What do you tell your students?"]),
  dict(head="Build the strongest case for the other side", label="Argue against yourself:", items=[
   "Defend the claim that the crisis is overstated, then defend the claim that it is understated. Use at least two nominalisations in each."])]),
speak=dict(language="use nominalisation: <em>the failure to replicate</em>, <em>the flexibility of analysis</em>, <em>the publication of null results</em>. For evidence: \"What's striking is…\", \"The evidence suggests…\", \"That depends on…\", \"It may well be that…\".",
 tasks=[
  ("Task A · Explain the crisis (4 minutes)",["Explain to a colleague from another discipline why psychology went through a crisis of replication and what has changed. Move through the arc: <em>the 2011 warnings → p-hacking → the 100-study project → how it was contested → reforms.</em>","Use at least <strong>three nominalisations</strong> and at least <strong>five key words</strong> (p-hacking, publication bias, registered report, effect size, confirmatory, reproducible, false positive, hold up, moderator, encourage)."]),
  ("Task B · Advise a lab (4 minutes)",["A new research group asks for five practical rules to make their work credible. Give your rules and justify each one."]),
  ("Task C · Your own field (4 minutes)",["Talk about one finding in your area that you think needs more checking, and how you would test it.","<strong>Stuck for an idea? Pick one of these and run with it:</strong><ul style=\"margin:6px 0 0 20px; color:#3a2a5a;\"><li>A popular intervention with weak evidence.</li><li>A classic effect that is taught in every textbook.</li><li>A screening tool used widely in practice.</li><li>A neuroimaging claim.</li><li>A finding that has become a media story.</li></ul>"])],
 final=["Should journals publish replications with the same prominence as new findings?","What should a practitioner do with a finding whose replication status is uncertain?","Has the crisis changed how you read papers?","<strong>Before you go, from memory:</strong> give one sentence with a nominalisation for <em>fail</em>, one for <em>select</em> and one for <em>publish</em>. Then, without looking back, explain why a literature can overstate an effect."]),
)
