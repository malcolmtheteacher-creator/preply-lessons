/* Reading House: Room 200 (Religion & Mythology). Written by tools/build_library_rooms.py - edit that, not this. */
window.ROOM={id:"200",wing:"2",name:"Religion & Mythology",img:"img/room200.webp",defaultSub:"200",bayInset:[.03,.1,.03],
 pegw:{"200":"noisy zoo","210":"nuts","220":"neon sea","230":"new mouse","240":"nurse","250":"hen lasso","260":"hen chess","270":"onyx","280":"navy sea","290":"Anubis"},
 bays:[
  {sub:"210",q:[[30,215],[135,238],[135,580],[30,598]],plaque:[85,175],peg:[92,40,70],word:[92,100]},
  {sub:"220",q:[[157,250],[228,268],[228,565],[157,578]],plaque:[192,228],peg:[195,78,58],word:[195,140]},
  {sub:"230",q:[[247,285],[298,297],[298,555],[247,562]],plaque:[272,262],peg:[272,150,46],word:[272,205]},
  {sub:"240",q:[[545,300],[700,300],[700,555],[545,555]],plaque:[622,290],peg:[620,172,62],word:[620,252]},
  {sub:"250",q:[[745,300],[903,300],[903,555],[745,555]],plaque:[824,290],peg:[826,172,62],word:[826,252]},
  {sub:"260",q:[[950,300],[1100,300],[1100,555],[950,555]],plaque:[1025,290],peg:[1027,172,62],word:[1027,252]},
  {sub:"270",q:[[1168,300],[1200,292],[1200,558],[1168,553]],plaque:[1184,278],peg:[1184,172,46],word:[1184,246]},
  {sub:"280",q:[[1215,275],[1265,258],[1265,570],[1215,560]],plaque:[1240,242],peg:[1240,112,58],word:[1240,200]},
  {sub:"290",q:[[1287,250],[1362,215],[1362,592],[1287,575]],plaque:[1325,200],peg:[1322,36,70],word:[1322,142]}
 ],
 lectern:{sub:"200",poly:"668,530 864,530 864,612 800,628 850,810 690,810 740,628 668,612",plaque:[768,700],peg:[768,484],pegSize:74},
 doors:[
  {to:"300",name:"Society, Money & Education",poly:"357,290 480,290 480,660 357,660",plaque:[418,700],dir:"↑"},
  {to:"800",name:"Literature & History",poly:"1412,150 1536,105 1536,895 1412,820",plaque:[1470,925],dir:"→"},
  {to:"100",name:"Philosophy & Psychology",poly:"608,880 928,880 928,940 608,940",plaque:[768,910],dir:"↓"}
 ],
 rules:[
  ["290",/buddh|\bzen\b|hindu|\btao|dalai|yoga|karma|sakya|confuc|tibet/i],
  ["280",/islam|muslim|quran|koran|prophet|muhammad|mecca/i],
  ["260",/\bjew|judai|torah|talmud|kabbal|rabbi/i],
  ["220",/bible|gospel|testament|biblical|psalm|genesis|hebrew|hebraisch/i],
  ["250",/myth|legend|folklore|goddess|\bgods\b/i],
  ["230",/christ|church|jesus|catholic|\bpope|saint|protestant|luther|vatican/i],
  ["240",/spiritual|prayer|\bsoul|meditat|mindful|heaven|angel|miracle/i],
  ["270",/history|crusade|reformation|inquisition|archaeolog|ritual|origins/i],
  ["210",/\bgod\b|atheis|delusion|faith|belief|believ|religion|spell/i]
 ],
 junk:/torrent downloaded|demonoid|come join us|readme|read me/i,
 subs:{
  "200":{name:"Religion in general",blurb:"Big questions about belief, and books that fit nowhere else."},
  "210":{name:"God, faith & doubt",blurb:"Arguments for and against belief."},
  "220":{name:"The Bible",blurb:"Bibles, biblical languages and books about the Bible."},
  "230":{name:"Christianity",blurb:"The Christian faith, its churches and its thinkers."},
  "240":{name:"Spiritual life",blurb:"Prayer, meditation and the inner life."},
  "250":{name:"Myths & legends",blurb:"Greek, Roman and world mythology."},
  "260":{name:"Judaism",blurb:"Jewish faith, history and thought."},
  "270":{name:"History of religion",blurb:"How religions began, spread and changed."},
  "280":{name:"Islam",blurb:"The Muslim faith, its history and its world."},
  "290":{name:"Eastern religions",blurb:"Buddhism, Hinduism, Zen and the Tao."}
 }
};
