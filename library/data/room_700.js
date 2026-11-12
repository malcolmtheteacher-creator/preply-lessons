/* Reading House: Room 700 (Arts & Recreation). Written by tools/build_library_rooms.py - edit that, not this. */
window.ROOM={id:"700",wing:"7",name:"Arts & Recreation",img:"img/room700.webp",defaultSub:"700",bayInset:[.03,.1,.03],
 pegw:{"700":"cases","710":"cats","720":"coins","730":"combs","740":"cars","750":"eagles","760":"coaches","770":"cakes","780":"caves","790":"cups"},
 bays:[
  {sub:"710",q:[[152,222],[234,248],[234,572],[152,590]],plaque:[195,190],peg:[205,62,74],word:[205,128]},
  {sub:"720",q:[[250,262],[308,280],[308,560],[250,570]],plaque:[280,238],peg:[282,118,58],word:[282,174]},
  {sub:"730",q:[[325,292],[362,302],[362,548],[325,556]],plaque:[345,278],peg:[345,176,46],word:[345,232]},
  {sub:"740",q:[[598,300],[748,300],[748,550],[598,550]],plaque:[672,290],peg:[672,190,62],word:[672,250]},
  {sub:"750",q:[[792,300],[945,300],[945,550],[792,550]],plaque:[868,290],peg:[868,190,62],word:[868,250]},
  {sub:"760",q:[[988,300],[1138,300],[1138,550],[988,550]],plaque:[1063,290],peg:[1063,190,62],word:[1063,250]},
  {sub:"770",q:[[1223,300],[1280,285],[1280,562],[1223,555]],plaque:[1250,272],peg:[1248,178,46],word:[1248,232]},
  {sub:"780",q:[[1300,270],[1375,245],[1375,580],[1300,568]],plaque:[1338,236],peg:[1340,118,58],word:[1340,180]},
  {sub:"790",q:[[1400,225],[1508,185],[1508,605],[1400,585]],plaque:[1455,190],peg:[1450,60,74],word:[1450,130]}
 ],
 lectern:{sub:"700",poly:"720,530 905,530 905,610 840,625 880,850 745,850 790,625 720,610",plaque:[812,700],peg:[812,480],pegSize:74},
 doors:[
  {to:"000",name:"General Works & Computing",poly:"0,110 105,140 105,790 0,850",plaque:[60,880],dir:"←"},
  {to:"600",name:"Technology, Health & Home",poly:"418,285 530,285 530,655 418,655",plaque:[474,700],dir:"↑"}
 ],
 rules:[
  ["770",/photo|camera|lighting|lightroom|exposure|portrait|close-ups|snapshots/i],
  ["780",/music|\bsong|guitar|piano|\bband|jazz|opera|beatles|album/i],
  ["790",/football|sport|\bgame|chess|\bfilm|movie|television|cinema|theat|dance|golf|cricket|olymp|\brace\b|graphic novel|star trek|star wars|discworld/i],
  ["730",/\bsew|fabric|stitch|\bknit|quilt|textile|embroider|crochet/i],
  ["710",/fashion|dress|trouser|pattern|sizechart|garment|couture|bodice|\bblock|skirt|tailor/i],
  ["740",/draw|sketch|manga|cartoon|anim|pencil|figure|gesture|anatomy|comic|wrinkles|rough stuff|illustrat/i],
  ["750",/paint|watercolo|acrylic|\boils?\b|colou?r/i],
  ["760",/logo|letterhead|graphic|typograph|design|\bveer|\bprint|layout|brand|lettering|calligraph/i],
  ["720",/architect|building|\bhous|\bhome\b|cathedral|decor|interior/i]
 ],
 junk:/torrent downloaded|demonoid|come join us|readme|read me/i,
 subs:{
  "700":{name:"Art in general",blurb:"Art history, and books that fit nowhere else."},
  "710":{name:"Fashion design",blurb:"Clothes, patterns and how garments are cut."},
  "720":{name:"Architecture & the home",blurb:"Buildings, houses and interiors."},
  "730":{name:"Sewing & textiles",blurb:"Sewing, knitting, quilting and fabric."},
  "740":{name:"Drawing & cartoons",blurb:"Drawing people, animals, manga and comics."},
  "750":{name:"Painting & colour",blurb:"Watercolour, oils and how colour works."},
  "760":{name:"Graphic design",blurb:"Logos, lettering, layout and print."},
  "770":{name:"Photography",blurb:"Cameras, light and taking better pictures."},
  "780":{name:"Music",blurb:"Musicians, instruments and songs."},
  "790":{name:"Sport, games & screen",blurb:"Football, chess, film, television and comics."}
 }
};
