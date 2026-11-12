/* Reading House, room 100 (Philosophy & Psychology): starred books that are on the shelf.
   Every note is written fresh; nothing is copied from the books. sub = sub-shelf (110..190); alias = words used to match the same book in the full list. */
(function(){
var add=[
{id:'kahneman-thinking',w:'1',sub:'150',t:'Thinking, Fast and Slow',a:'Daniel Kahneman',lvl:'C1',topic:'Mind & thinking',pages:500,alias:['fastandslowthinking','thinkingfastandslow'],
 why:['A Nobel-winning psychologist shows that your mind works in two ways, quick gut reaction and slow careful thought, and how each one can fool you.','Full of small experiments you can try on yourself.'],
 q:'Describe a decision you made too quickly. What might slow thinking have changed?'},
{id:'russell-conquest-happiness',w:'1',sub:'150',t:'The Conquest of Happiness',a:'Bertrand Russell',lvl:'B2',topic:'Mind & thinking',pages:250,alias:['conquestofhappiness'],
 why:['A great philosopher looks at the everyday causes of unhappiness, such as worry, envy and boredom, and suggests plain, practical remedies.','Calm, witty and surprisingly modern, though it was written in 1930.'],
 q:'Which of the causes of unhappiness in the book is the most common in your own life?'},
{id:'dobelli-thinking-clearly',w:'1',sub:'150',t:'The Art of Thinking Clearly',a:'Rolf Dobelli',lvl:'B2',topic:'Mind & thinking',pages:300,alias:['artofthinkingclearly'],
 why:['A collection of about a hundred short chapters, each describing one common mistake in the way we think.','You can read one a day, and each gives you something to talk about.'],
 q:'Which thinking mistake in the book do you make most often? Give an example.'},
{id:'wiseman-paranormality',w:'1',sub:'130',t:'Paranormality',a:'Richard Wiseman',lvl:'B2',topic:'Mind & thinking',pages:350,alias:['paranormalitywhy'],
 why:['A psychologist who used to perform magic tests ghosts, psychics and mind-reading, and explains why so many of us believe in them.','Playful and clear, with experiments you could try at home.'],
 q:'Have you ever had an experience that seemed impossible to explain? How would a sceptic explain it?'},
{id:'baggini-pig-eaten',w:'1',sub:'100',t:'The Pig That Wants to Be Eaten',a:'Julian Baggini',lvl:'B2',topic:'Mind & thinking',pages:350,alias:['pigthatwantstobeeaten'],
 why:['A hundred famous thought experiments, each in two or three pages, from a pig that asks to be eaten to a machine that can feel pleasure.','Perfect for short bursts of reading, and each one ends with a question.'],
 q:'Choose one thought experiment from the book and say what you would do in that situation.'},
{id:'gaarder-sophies-world',w:'1',sub:'100',t:"Sophie's World",a:'Jostein Gaarder',lvl:'B2',topic:'Fiction',pages:400,alias:['sophiesworld'],
 why:['A teenage girl receives mysterious letters asking "Who are you?", and through them learns the whole history of philosophy.','A story wrapped round a guided tour, so it never feels like a textbook.'],
 q:'Which philosopher in the book would you most like to meet, and what would you ask?'},
{id:'aurelius-meditations',w:'1',sub:'180',t:'Meditations',a:'Marcus Aurelius',lvl:'C1',topic:'Mind & thinking',pages:200,alias:['marcusaureliusmeditations','meditationsmarcus'],
 why:['The private notes of a Roman emperor, written to remind himself how to stay calm, fair and brave.','Short, direct and still useful: you can read a page and think about it all day.'],
 q:'Pick one line from the book. How would it help you tomorrow?'},
{id:'seneca-letters-stoic',w:'1',sub:'180',t:'Letters from a Stoic',a:'Seneca',lvl:'C1',topic:'Mind & thinking',pages:250,alias:['lettersfromastoic'],
 why:['A Roman writer sends a friend advice on time, friendship, fear and death, in letters that feel personal.','Each letter is short and can be read on its own.'],
 q:'Seneca says we waste time rather than lack it. Do you agree?'},
{id:'plato-republic',w:'1',sub:'180',t:'The Republic',a:'Plato',lvl:'C1',topic:'Politics & society',pages:400,alias:['republicplato','platotherepublic','therepublicplato'],
 why:['A conversation about what justice is, and what a perfectly fair city would look like and who should rule it.','One of the starting points of Western thought, and the source of the famous cave story.'],
 q:'In the cave story, what do the shadows stand for in your own life?'},
{id:'mill-on-liberty',w:'1',sub:'190',t:'On Liberty',a:'John Stuart Mill',lvl:'C1',topic:'Politics & society',pages:150,alias:['onlibertyandotheressays','onliberty'],
 why:['How far may a society control what its people say and do? Mill draws the line, and defends the freedom to hold unpopular opinions.','A short book that people still argue about.'],
 q:'Should anyone be stopped from saying something false or offensive? Where is your line?'},
{id:'russell-problems-philosophy',w:'1',sub:'190',t:'The Problems of Philosophy',a:'Bertrand Russell',lvl:'C1',topic:'Mind & thinking',pages:120,alias:['problemsofphilosophy'],
 why:['A very short, clear introduction to the biggest questions: can we know anything for certain, and is the table in front of you really there?','Written so that a non-specialist can follow it.'],
 q:'How do you know that the room you are in is real?'},
{id:'sartre-nausea',w:'1',sub:'190',t:'Nausea',a:'Jean-Paul Sartre',lvl:'C1',topic:'Fiction',pages:250,alias:['sartrenausea'],
 why:['A lonely historian in a French port town starts to feel that ordinary objects, and existence itself, are strange and disturbing.','A novel that put an idea, existentialism, into a story.'],
 q:'Have you ever looked at something familiar and suddenly felt it was strange? Describe it.'},
{id:'nietzsche-beyond-good-evil',w:'1',sub:'190',t:'Beyond Good and Evil',a:'Friedrich Nietzsche',lvl:'C1',topic:'Mind & thinking',pages:250,alias:['beyondgoodandevil'],
 why:['Sharp, provocative notes that question the idea that our moral rules are simple or eternal.','Demanding, so read a few sections at a time and argue back.'],
 q:'Choose one section and explain what Nietzsche is attacking.'}
];
window.CURATED=(window.CURATED||[]).concat(add);
window.SUB_OVERRIDE={'mcinerny-being-logical':'160'};
window.SUBS={
'100':{name:'General & big questions',blurb:'Introductions, thought experiments and the whole history of philosophy.'},
'110':{name:'Metaphysics',blurb:'What is real? Being, time, free will, mind and matter.'},
'120':{name:'Knowledge',blurb:'How do we know what we know? Truth, belief and certainty.'},
'130':{name:'The mind’s edges',blurb:'Dreams, the paranormal and strange experiences.'},
'140':{name:'Schools of thought',blurb:'Stoics, existentialists, pragmatists and other movements.'},
'150':{name:'Psychology',blurb:'How we think, feel, remember and choose.'},
'160':{name:'Logic & reasoning',blurb:'How to build an argument and spot a bad one.'},
'170':{name:'Ethics',blurb:'Right and wrong, and how to live well.'},
'180':{name:'Ancient & Eastern wisdom',blurb:'Greeks, Romans, medieval thinkers and the great Eastern traditions.'},
'190':{name:'Modern philosophers',blurb:'Descartes to the present day.'}
};
})();
