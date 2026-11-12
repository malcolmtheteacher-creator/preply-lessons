/* Reading House: Room 100 (Philosophy & Psychology): where things are on the painted picture (1536 x 1024) */
window.ROOM={id:'100',wing:'1',name:'Philosophy & Psychology',img:'img/room100.webp',defaultSub:'100',
 pegw:{'100':'hot sauce','110':'toads','120':'tennis','130':'atoms','140':'dress','150':'atlas','160':'duchess','170':'taxi','180':'divas','190':'deep sea'},
 bays:[
 {sub:'110',q:[[47,258],[148,288],[148,572],[47,587]],plaque:[100,135]},
 {sub:'120',q:[[165,300],[243,318],[243,566],[165,574]],plaque:[205,195]},
 {sub:'130',q:[[252,322],[308,335],[308,554],[252,560]],plaque:[283,245]},
 {sub:'140',q:[[583,330],[718,330],[718,553],[583,553]],plaque:[650,268]},
 {sub:'150',q:[[748,330],[885,330],[885,553],[748,553]],plaque:[815,268]},
 {sub:'160',q:[[913,330],[1045,330],[1045,553],[913,553]],plaque:[980,268]},
 {sub:'170',q:[[1115,328],[1172,314],[1172,556],[1115,562]],plaque:[1146,240]},
 {sub:'180',q:[[1180,305],[1250,282],[1250,570],[1180,578]],plaque:[1214,200]},
 {sub:'190',q:[[1262,252],[1340,225],[1340,590],[1262,583]],plaque:[1300,155]}
],
lectern:{sub:'100',poly:'700,520 850,520 850,810 725,810',plaque:[772,662],peg:[772,488],pegSize:80},
 doors:[
 {to:'200',name:'Religion & Mythology',poly:'352,305 528,305 528,640 352,640',plaque:[440,670],dir:'↑'},
 {to:'000',name:'General Works & Computing',poly:'1392,150 1525,150 1525,800 1392,800',plaque:[1448,840],dir:'→'}
],
 rules:[
 ['190',/descartes|kant\b|hegel|nietzsche|hume\b|locke\b|spinoza|leibniz|heidegger|sartre|wittgenstein|schopenhauer|kierkegaard|bertrand russell|^russell|mill\b|rousseau|hobbes|berkeley|husserl|derrida|foucault|rawls|popper|quine|frege|dennett/i],
 ['180',/plato|aristotle|socrat|greek|roman|augustine|aquinas|anselm|medieval|confuc|\btao|buddh|seneca|marcus aurelius|epictetus|epicur|cicero|plotinus|stoic|presocratic|vedanta|upanishad|bhagavad/i],
 ['160',/\blogic|argument|fallac|reasoning|paradox|critical thinking|lateral thinking|clear.*thinking/i],
 ['170',/ethic|moral|virtue|justice|good life|metaethic/i],
 ['110',/metaphysic|ontolog|causation|free will|personal identity|\bbeing\b|\btime\b/i],
 ['120',/epistemolog|knowledge|\btruth\b|\bbelief|skeptic|sceptic|certainty/i],
 ['130',/paranormal|psychic|occult|astrolog|dream|ghost|\bmagic|spirit|tarot|reincarnat|afterlife|hypnos|telepath|lucid/i],
 ['140',/existential|pragmat|empiric|idealis|phenomenolog|positiv|utilitar|marxis|liberalis|postmodern|critical theory|structuralis/i],
 ['150',/psycholog|therapy|freud|jung|cognitive|behavio|emotion|\bbrain|personality|happiness|memory|habit|anxiety|depress|thinking|\bflow\b|\blove\b|\bself\b|motivation|\bmind\b|persuasion|influence|intelligence|mindful|meditat/i]
],
 junk:/omnifocus|lightroom|photoshop|option trading|yoga poses|eat right|mudras|chakra|investing|delivering happiness|good business|landscape photography/i,
 subs:{
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
}
};
