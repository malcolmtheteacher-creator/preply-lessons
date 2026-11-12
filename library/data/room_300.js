/* Reading House: Room 300 (Society, Money & Education). Written by tools/build_library_rooms.py - edit that, not this. */
window.ROOM={id:"300",wing:"3",name:"Society, Money & Education",img:"img/room300.webp",defaultSub:"300",bayInset:[.03,.1,.03],
 pegw:{"300":"Moses","310":"maids","320":"moons","330":"mums","340":"mares","350":"moles","360":"matches","370":"mugs","380":"movies","390":"mops"},
 bays:[
  {sub:"310",q:[[42,205],[148,240],[148,585],[42,605]],plaque:[95,172],peg:[100,46,70],word:[100,104]},
  {sub:"320",q:[[172,250],[250,275],[250,572],[172,588]],plaque:[212,222],peg:[212,90,58],word:[212,146]},
  {sub:"330",q:[[268,285],[328,300],[328,562],[268,575]],plaque:[298,262],peg:[292,160,46],word:[292,208]},
  {sub:"340",q:[[413,302],[613,302],[613,572],[413,572]],plaque:[512,290],peg:[512,178,62],word:[512,234]},
  {sub:"350",q:[[665,302],[868,302],[868,572],[665,572]],plaque:[767,290],peg:[767,178,62],word:[767,234]},
  {sub:"360",q:[[923,302],[1123,302],[1123,572],[923,572]],plaque:[1023,290],peg:[1023,178,62],word:[1023,234]},
  {sub:"370",q:[[1168,300],[1200,290],[1200,578],[1168,572]],plaque:[1184,285],peg:[1184,202,44],word:[1184,246]},
  {sub:"380",q:[[1215,280],[1275,258],[1275,592],[1215,580]],plaque:[1245,250],peg:[1244,152,54],word:[1244,200]},
  {sub:"390",q:[[1290,255],[1375,215],[1375,612],[1290,595]],plaque:[1332,205],peg:[1335,96,66],word:[1335,152]}
 ],
 lectern:{sub:"300",poly:"658,533 858,533 858,618 798,632 848,862 688,862 738,632 658,618",plaque:[762,730],peg:[762,488],pegSize:74},
 doors:[
  {to:"400",name:"Language",poly:"1412,150 1536,110 1536,890 1412,830",plaque:[1472,915],dir:"→"},
  {to:"200",name:"Religion & Mythology",poly:"608,880 928,880 928,940 608,940",plaque:[768,910],dir:"↓"}
 ],
 rules:[
  ["310",/archaeolog|anthropolog|neolithic|egypt|pharaon|hieroglyph|prehistor|\btribe|demotic/i],
  ["370",/^[a-z0-9]+(-[a-z0-9]+){2,}|pairwork|audio ?script|phonetic|preposition|\bnouns?\b|adjective|maths|teach|lesson|classroom|school|learn|ielts|toefl|grammar|vocabular|\besl\b|\befl\b|celta|student|english|pronunciation|spelling|worksheet|answers|quiz|puzzle|educat|toddler|literac|tefl|verb|tense|word|timetable|pellmanism|skills|reading|writing/i],
  ["330",/econom|money|capital|market|wealth|financ|business|bank|\bdebt|invest|rich|poor/i],
  ["340",/\blaw\b|legal|crime|criminal|justice|court|murder|police|prison|mafia/i],
  ["350",/\bwar\b|military|army|terror|soldier|weapon/i],
  ["320",/politic|government|democra|president|chomsky|republic|liberal|conservativ|washington|election|power|contract|state\b|nation/i],
  ["390",/folk|fairy|custom|etiquette|\btales?\b|tradition|costume|peter rabbit|junie b|little prince|quidditch|a story about|cinderella|first grader|\bdragon/i],
  ["380",/transport|railway|communicat|media|journalis|commerce|newspaper/i],
  ["360",/social|poverty|welfare|drug|feminis|gender|\brace\b|racis|immigra|society|women|famil|parent|baby/i],
  ["300",/zzzz/i]
 ],
 junk:/torrent downloaded|demonoid|come join us|readme|read me/i,
 subs:{
  "300":{name:"People & society",blurb:"How people live together, and books that fit nowhere else."},
  "310":{name:"Archaeology & early peoples",blurb:"Digging up the past, and how early societies lived."},
  "320":{name:"Politics",blurb:"Power, government and political ideas."},
  "330":{name:"Economics & money",blurb:"How money, markets and work really behave."},
  "340":{name:"Law & crime",blurb:"Courts, justice and true crime."},
  "350":{name:"War & the military",blurb:"Armies, conflicts and terrorism."},
  "360":{name:"Social questions",blurb:"Poverty, health, gender, race and how societies cope."},
  "370":{name:"Education & teaching",blurb:"Teaching, learning and English-language classroom material."},
  "380":{name:"Trade, travel & media",blurb:"Commerce, transport and communication."},
  "390":{name:"Children's stories & folk tales",blurb:"Fairy tales, picture books and stories for younger readers."}
 }
};
