/* Reading House: Room 000 (General Works & Computing): where things are on the painted picture (1536 x 1024) */
window.ROOM={id:'000',wing:'0',name:'General Works & Computing',img:'img/room000.webp',defaultSub:'000',
 pegw:{'000':'seesaw','010':'daisy','020':'nose','030':'mouse','040':'rose','050':'lasso','060':'cheese','070':'goose','080':'vase','090':'bus'},
 bays:[
  {sub:'010',q:[[198,240],[292,258],[292,538],[198,548]],plaque:[245,196],peg:[245,70,76],word:[245,128]},
  {sub:'020',q:[[305,262],[360,270],[360,540],[305,543]],plaque:[332,236],peg:[332,138,60],word:[332,186]},
  {sub:'030',q:[[372,283],[413,290],[413,530],[372,533]],plaque:[394,270],peg:[394,188,48],word:[394,228]},
  {sub:'040',q:[[628,300],[757,300],[757,525],[628,525]],plaque:[692,290],peg:[690,204,64],word:[690,252]},
  {sub:'050',q:[[788,290],[915,290],[915,525],[788,525]],plaque:[851,290],peg:[850,204,64],word:[850,252]},
  {sub:'060',q:[[945,295],[1080,295],[1080,525],[945,525]],plaque:[1012,290],peg:[1010,204,64],word:[1010,252]},
  {sub:'070',q:[[1150,262],[1192,252],[1192,532],[1150,530]],plaque:[1171,268],peg:[1172,186,48],word:[1172,226]},
  {sub:'080',q:[[1208,242],[1262,230],[1262,540],[1208,535]],plaque:[1235,238],peg:[1233,144,60],word:[1233,192]},
  {sub:'090',q:[[1283,200],[1368,182],[1368,555],[1283,548]],plaque:[1325,198],peg:[1322,80,74],word:[1322,134]}
 ],
lectern:{sub:'000',poly:'695,512 855,512 855,578 805,600 850,800 710,800 760,600 695,578',plaque:[775,660],peg:[775,466],pegSize:74},
 doors:[
  {to:'100',name:'Philosophy & Psychology',poly:'0,95 150,105 150,790 0,850',plaque:[75,880],dir:'←'},
  {to:'800',name:'Literature & History',poly:'455,265 585,265 585,625 455,625',plaque:[520,668],dir:'↑'},
  {to:'700',name:'Arts & Recreation',poly:'1405,95 1536,80 1536,860 1405,790',plaque:[1470,885],dir:'→'}
 ],
 rules:[
  ['090',/star trek|asimov|fiction|novel|\bsf\b|stories/i],
  ['060',/threads|stitch|sew|knit|quilt|crochet|dynamic graphics|computer arts|digital camera|photograph|photo\b|creative|art and design|\bdesign|craft|interior|embroider/i],
  ['020',/linux|network|router|cisco|security|apache|server|firewall|hack|crypt|ubuntu|debian|tcp|wireless|lpi\b|mysql|postgres/i],
  ['010',/python|java|jquery|\bcss\b|html|\bphp\b|\bsql\b|database|algorithm|software|developer|programming|\bcode|coding|\bweb\b|computer|pc format|\bapc\b|apple|\bmac\b|windows|ajax|rails|\bxml\b|javascript|wordpress|excel|office|techradar|wired|\bit\b/i],
  ['030',/encyclop|dictionary|companion|handbook|almanac|history of knowledge|cambridge ancient|reference|\bguide\b|oxford|world book/i],
  ['040',/new scientist|archaeolog|scientific american|\bnature\b|discover|geographic|science|astronomy|\bfocus\b|how it works|\bspace\b|fortean|physics|biolog|nasa/i],
  ['050',/history|heritage|smithsonian|bbc music|world war|military|museum|literature|poetry|opera|classic|american history|\bart\b|cultur/i],
  ['070',/spectator|\breason\b|economist|atlantic|new yorker|\btime\b|newsweek|politic|prospect|guardian|\bnation\b|\bweek\b|foreign|harper|shares|investor|money|business|forbes|fortune|news|week/i],
  ['080',/health|fitness|recipe|food|cook|pregnan|parent|baby|garden|travel|vogue|living|\bevo\b|maxim|cosmopolitan|woman|home|car and driver|yacht|registry|high times|\bq magazine|kerrang|hgtv|us weekly|people|men's|style|fashion|golf|sport|motor|auto|cinema|music|film|game|magazine/i]
 ],
 junk:/torrent downloaded|demonoid|come join us|readme/i,
 subs:{
  '000':{name:'General & curiosities',blurb:'Odd one-offs and everything that does not fit elsewhere.'},
  '010':{name:'Computing, programming & the web',blurb:'Code, websites, databases and computer magazines.'},
  '020':{name:'Linux, networks & security',blurb:'Servers, networking, system administration and security.'},
  '030':{name:'Encyclopedias & reference',blurb:'Encyclopedias, companions, dictionaries and handbooks.'},
  '040':{name:'Science & nature magazines',blurb:'New Scientist, archaeology and other science magazines.'},
  '050':{name:'History & culture magazines',blurb:'History, music, art and culture.'},
  '060':{name:'Craft, design & photography',blurb:'Sewing, knitting, graphic design and photography magazines.'},
  '070':{name:'News & ideas magazines',blurb:'Politics, money, business and current affairs.'},
  '080':{name:'Life, hobbies & entertainment',blurb:'Health, food, cars, music, travel and everyday life.'},
  '090':{name:'Stories & oddments',blurb:'Science-fiction magazines and story collections.'}
 }
};
