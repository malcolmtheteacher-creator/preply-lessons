/* Reading House: Room 600 (Technology, Health & Home). Written by tools/build_library_rooms.py - edit that, not this. */
window.ROOM={id:"600",wing:"6",name:"Technology, Health & Home",img:"img/room600.webp",defaultSub:"600",bayInset:[.03,.1,.03],
 pegw:{"600":"juices","610":"jets","620":"chains","630":"gems","640":"chairs","650":"shells","660":"judges","670":"chicks","680":"chefs","690":"ships"},
 bays:[
  {sub:"610",q:[[160,235],[245,265],[245,575],[160,592]],plaque:[200,215],peg:[205,84,70],word:[205,142]},
  {sub:"620",q:[[265,275],[320,290],[320,562],[265,572]],plaque:[292,258],peg:[290,154,54],word:[290,200]},
  {sub:"630",q:[[335,300],[375,310],[375,553],[335,562]],plaque:[355,292],peg:[350,206,44],word:[350,244]},
  {sub:"640",q:[[605,305],[755,305],[755,562],[605,562]],plaque:[680,296],peg:[678,194,60],word:[678,246]},
  {sub:"650",q:[[800,305],[945,305],[945,562],[800,562]],plaque:[872,296],peg:[870,194,60],word:[870,246]},
  {sub:"660",q:[[990,305],[1140,305],[1140,562],[990,562]],plaque:[1065,296],peg:[1065,194,60],word:[1065,246]},
  {sub:"670",q:[[1238,290],[1290,268],[1290,592],[1238,580]],plaque:[1264,255],peg:[1258,152,50],word:[1258,200]},
  {sub:"680",q:[[1308,262],[1385,232],[1385,615],[1308,598]],plaque:[1347,215],peg:[1345,90,60],word:[1345,146]},
  {sub:"690",q:[[1408,225],[1510,182],[1510,640],[1408,618]],plaque:[1460,165],peg:[1458,46,60],word:[1458,98]}
 ],
 lectern:{sub:"600",poly:"668,535 860,535 860,620 800,634 850,862 690,862 740,634 668,620",plaque:[765,730],peg:[765,490],pegSize:74},
 doors:[
  {to:"800",name:"Literature & History",poly:"0,120 122,150 122,835 0,895",plaque:[62,920],dir:"←"},
  {to:"500",name:"Science & Nature",poly:"430,345 548,345 548,672 430,672",plaque:[488,712],dir:"↑"},
  {to:"700",name:"Arts & Recreation",poly:"608,880 928,880 928,940 608,940",plaque:[768,910],dir:"↓"}
 ],
 rules:[
  ["650",/trad(e|ing|er)|invest|stock|forex|market|hedge|currency|option|business|manag|leadership|money|financ|commodit|quant|wealth|chart|uptick|profit|entrepreneur|indicator|\\bbull\\b|rumor|dtu module|\\brsi\\b|broker|divergence|momentum|security analysis|technical analysis|foreign exchange|buffett|dealing/i],
  ["660",/\bbrew|\bbeer|\bwine|distill|soap|candle|homebrew/i],
  ["630",/garden|\bfarm|\blawn|\bsoil|\bcrop|compost|livestock|insect repell|perennial|special interest|lavender|\\bmint\\b|basil|pruning|shrub|wild plants|fragrant|\\bgrass|\\bherb/i],
  ["640",/cook|recipe|kitchen|food|bak(e|ing)|bread|vegan|vegetarian|dessert|cake|meal|\bdiet|\beat|chef|cuisine|soup|salad|\bmeat|\bfish|slow cooker|clean home|household|flat.belly|weight watchers|pasta|chocolate|sauce|curry|grill|barbecue|bon appetit|italian|olive|coconut|\\braw\\b|\\bfats\\b|veggies|\\bsoy\\b|sweets|culinary|appetite/i],
  ["610",/health|medic|doctor|disease|cancer|\bbody|brain|anatomy|\bdrug|pharma|arthritis|\bherb|fitness|weight|nutrition|yoga|surgery|kidney|sleep|pregnan|muscle|massage|pilates|ayurved|healing|workout|\\bbaby/i],
  ["690",/\bbuild|construction|plumb|\broof|carpent|socket|cupboard|brick|switch|radiator|\\bdecks?\\b|\\btile|\\bwalls?\\b|circuit|carpet|garage|faucet|shower|\\bsinks?\\b|\\bbath|wallpaper|parquet|insulation|shingle|\\bdoor|window|fixings|install|repair|\\bpond|paint effects|curtain|consumer unit|plan a /i],
  ["680",/woodwork|\bcraft|\bdiy\b|do it yourself|furniture|leather/i],
  ["620",/engine|machine|electr|\bcars?\b|aircraft|\btrain|robot|radio|\bgun|mechanic|rocket|solar/i],
  ["670",/manufactur|\bmetal|textile|\bpaper|printing/i]
 ],
 junk:/torrent downloaded|demonoid|come join us|readme|read me/i,
 subs:{
  "600":{name:"Inventions & how things work",blurb:"Technology in general, and books that fit nowhere else."},
  "610":{name:"Medicine & health",blurb:"The body, illness, fitness and staying well."},
  "620":{name:"Engineering & machines",blurb:"Engines, electricity, vehicles and robots."},
  "630":{name:"Farming & gardening",blurb:"Growing food and keeping a garden."},
  "640":{name:"Food & home",blurb:"Cookery books and running a home."},
  "650":{name:"Business & investing",blurb:"Management, trading and the stock market."},
  "660":{name:"Brewing & kitchen chemistry",blurb:"Beer, wine, soap and other things you can make."},
  "670":{name:"Making things",blurb:"Materials and manufacturing."},
  "680":{name:"Handicrafts & DIY",blurb:"Woodwork and things made by hand."},
  "690":{name:"Building & home repairs",blurb:"Houses, repairs and jobs around the home."}
 }
};
