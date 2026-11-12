/* Reading House: Room 400 (Language). Written by tools/build_library_rooms.py - edit that, not this. */
window.ROOM={id:"400",wing:"4",name:"Language",img:"img/room400.webp",defaultSub:"400",bayInset:[.03,.1,.03],
 pegw:{"400":"roses","410":"rat","420":"rhinos","430":"rams","440":"rowers","450":"rolls","460":"riches","470":"rocks","480":"reefs","490":"ropes"},
 bays:[
  {sub:"410",q:[[158,230],[245,262],[245,572],[158,592]],plaque:[202,205],peg:[200,66,74],word:[200,128]},
  {sub:"420",q:[[268,275],[332,292],[332,562],[268,575]],plaque:[300,255],peg:[298,138,58],word:[298,190]},
  {sub:"430",q:[[350,300],[395,312],[395,552],[350,562]],plaque:[372,290],peg:[372,198,46],word:[372,240]},
  {sub:"440",q:[[490,305],[648,305],[648,565],[490,565]],plaque:[570,296],peg:[572,196,62],word:[572,248]},
  {sub:"450",q:[[692,305],[845,305],[845,565],[692,565]],plaque:[768,296],peg:[768,196,62],word:[768,248]},
  {sub:"460",q:[[888,305],[1050,305],[1050,565],[888,565]],plaque:[968,296],peg:[968,196,62],word:[968,248]},
  {sub:"470",q:[[1140,315],[1188,300],[1188,562],[1140,552]],plaque:[1164,292],peg:[1164,198,46],word:[1164,240]},
  {sub:"480",q:[[1205,292],[1265,270],[1265,578],[1205,565]],plaque:[1236,262],peg:[1242,138,58],word:[1242,190]},
  {sub:"490",q:[[1290,262],[1378,228],[1378,598],[1290,578]],plaque:[1335,212],peg:[1340,64,74],word:[1340,128]}
 ],
 lectern:{sub:"400",poly:"668,535 860,535 860,618 800,632 850,875 690,875 740,632 668,618",plaque:[765,730],peg:[765,488],pegSize:74},
 doors:[
  {to:"300",name:"Society, Money & Education",poly:"0,125 118,150 118,830 0,885",plaque:[62,910],dir:"←"},
  {to:"500",name:"Science & Nature",poly:"1420,150 1536,125 1536,885 1420,830",plaque:[1475,910],dir:"→"},
  {to:"800",name:"Literature & History",poly:"608,880 928,880 928,940 608,940",plaque:[768,910],dir:"↓"}
 ],
 rules:[
  ["470",/lat[ií]n|lengua y|harrius|ille pu|lingua|roman|\brome\b|wheelock|latim/i],
  ["480",/greek|greece|hellen|mytholog|ancient|classical/i],
  ["430",/german|deutsch/i],
  ["440",/french|fran[cç]ais|romains/i],
  ["450",/italian|spanish|español|portugu/i],
  ["490",/hebrew|egypt|hieroglyph|coptic|demotic|semitic|akkadian|chinese|japanese|arabic|russian|korean|sanskrit/i],
  ["460",/dictionar|thesaurus|synonym/i],
  ["410",/linguist|language teaching|language learning|methodolog|silent way|phonet|syntax|semantic|lesson planning/i],
  ["420",/english|grammar|grammer|writing|vocabular|oxford|crowthorne|spelling|punctuat|ielts|toefl|toeic|\bfce\b|\bcae\b|\bcpe\b|\bpet\b|\bket\b|phrasal|idiom|pronunciation|collocation|essay|usage|\bverbs?\b|tenses|preposition|\bwords?\b|speaking|listening|phonics|headway|cutting edge|business result|market leader/i]
 ],
 junk:/torrent downloaded|demonoid|come join us|readme|read me/i,
 subs:{
  "400":{name:"Language in general",blurb:"Dictionaries and books about language itself."},
  "410":{name:"Linguistics",blurb:"How languages work and how they are taught."},
  "420":{name:"English",blurb:"Grammar, words and the craft of writing in English."},
  "430":{name:"German",blurb:"German courses, grammar and dictionaries."},
  "440":{name:"French",blurb:"French courses, grammar and readers."},
  "450":{name:"Italian, Spanish & Portuguese",blurb:"Courses and phrase books for the Romance languages."},
  "460":{name:"Dictionaries",blurb:"Dictionaries and word books of every kind."},
  "470":{name:"Latin",blurb:"Latin courses, readers and the world of Rome."},
  "480":{name:"Greek & the classical world",blurb:"Greek, mythology and the ancient world."},
  "490":{name:"Other languages",blurb:"Hebrew, Egyptian, Chinese and more."}
 }
};
