/* Reading House: Room 500 (Science & Nature). Written by tools/build_library_rooms.py - edit that, not this. */
window.ROOM={id:"500",wing:"5",name:"Science & Nature",img:"img/room500.webp",defaultSub:"500",bayInset:[.03,.1,.03],
 pegw:{"500":"laces","510":"lights","520":"lions","530":"limes","540":"lyres","550":"lilies","560":"lodges","570":"locks","580":"leaves","590":"lips"},
 bays:[
  {sub:"510",q:[[155,235],[235,262],[235,580],[155,598]],plaque:[196,215],peg:[200,82,70],word:[200,140]},
  {sub:"520",q:[[255,270],[315,288],[315,570],[255,585]],plaque:[286,258],peg:[285,152,54],word:[285,198]},
  {sub:"530",q:[[330,300],[375,310],[375,560],[330,570]],plaque:[352,290],peg:[346,206,44],word:[346,244]},
  {sub:"540",q:[[455,305],[630,305],[630,572],[455,572]],plaque:[542,292],peg:[541,178,62],word:[541,232]},
  {sub:"550",q:[[688,305],[866,305],[866,572],[688,572]],plaque:[776,292],peg:[775,178,62],word:[775,232]},
  {sub:"560",q:[[927,305],[1104,305],[1104,572],[927,572]],plaque:[1015,292],peg:[1016,178,62],word:[1016,232]},
  {sub:"570",q:[[1232,290],[1290,265],[1290,598],[1232,585]],plaque:[1262,252],peg:[1258,152,50],word:[1258,200]},
  {sub:"580",q:[[1308,262],[1385,232],[1385,612],[1308,598]],plaque:[1347,215],peg:[1345,92,60],word:[1345,146]},
  {sub:"590",q:[[1408,225],[1510,180],[1510,640],[1408,615]],plaque:[1460,165],peg:[1458,46,60],word:[1458,98]}
 ],
 lectern:{sub:"500",poly:"668,538 860,538 860,624 800,638 850,875 690,875 740,638 668,624",plaque:[765,735],peg:[765,492],pegSize:74},
 doors:[
  {to:"400",name:"Language",poly:"0,120 122,150 122,835 0,895",plaque:[62,920],dir:"←"},
  {to:"600",name:"Technology, Health & Home",poly:"608,880 928,880 928,940 608,940",plaque:[768,910],dir:"↓"}
 ],
 rules:[
  ["560",/dinosaur|fossil|prehistor|extinct/i],
  ["520",/\bspace\b|astronom|universe|cosmos|planet|\bstars?\b(?! wars| trek)|galax|hawking|history of time|telescope|\bmoon\b|solar system/i],
  ["510",/\bmath|algebra|geometr|calculus|number|equation/i],
  ["530",/physic|quantum|relativ|einstein|energy|chaos|complexity/i],
  ["540",/chemi|periodic|molecul/i],
  ["550",/\bearth\b|geolog|\brocks?\b|mineral|crystal|\bgem|volcan|weather|climate|ocean|earthquake/i],
  ["590",/animal|\bbirds?\b|insect|mammal|panda|\bdogs?\b|\bcats?\b|wolf|whale|\bzoo\b|wildlife|\bapes?\b|\bbees?\b|shark|horse/i],
  ["580",/plant|\btrees?\b|flower|garden|\bherbs?\b|botan|fruit|vegetable|forest/i],
  ["570",/\bevolution|darwin|\bgenes?\b|\bdna\b|biolog|\bcell|ecolog|species|\bnature\b|\blife\b/i]
 ],
 junk:/torrent downloaded|demonoid|come join us|readme|read me/i,
 subs:{
  "500":{name:"Science in general & other books",blurb:"Big-picture science, and everything else kept in this room."},
  "510":{name:"Mathematics",blurb:"Numbers, shapes, puzzles and proofs."},
  "520":{name:"Space & astronomy",blurb:"Stars, planets and the universe."},
  "530":{name:"Physics",blurb:"Energy, time, matter and how things move."},
  "540":{name:"Chemistry",blurb:"Elements, reactions and what things are made of."},
  "550":{name:"Earth & weather",blurb:"Rocks, oceans, volcanoes and climate."},
  "560":{name:"Fossils & prehistoric life",blurb:"Dinosaurs and the deep past."},
  "570":{name:"Life & evolution",blurb:"Genes, cells, ecology and how life changes."},
  "580":{name:"Plants",blurb:"Trees, flowers, herbs and gardens."},
  "590":{name:"Animals",blurb:"Mammals, birds, insects and sea life."}
 }
};
