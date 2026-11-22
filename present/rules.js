// The rule book. Used inside the game and by the printable page (rules.html).
(function (g) {
  const die = (n, c) => { const on = { 1: [4], 2: [0, 8], 3: [0, 4, 8], 4: [0, 2, 6, 8], 5: [0, 2, 4, 6, 8], 6: [0, 2, 3, 5, 6, 8] }[n]; return '<span class="die ' + c + '">' + Array.from({ length: 9 }, (_, i) => '<i class="' + (on.includes(i) ? 'on' : '') + '"></i>').join('') + '</span>'; };
  const R = g.MAP ? g.MAP.regions : {};
  const count = k => g.MAP ? g.MAP.lands.filter(t => t.region === k).length : '';
  const regRows = Object.keys(R).map(k => '<tr><td>' + R[k].name + '</td><td>' + count(k) + ' lands</td><td>' + R[k].bonus + ' armies</td></tr>').join('');
  g.RULES = [
    // 0
    '<div class="cover"><img src="img/rose.png" alt=""><div class="t">ATLAS<br><i>of</i><br>EMPIRES</div><div class="s">The Rules of Play</div><p style="text-align:center;font-style:italic">The game of world conquest<br>for two to six commanders</p></div>',
    // 1
    '<h3>The Object</h3><div class="orn">◆ ◆ ◆</div>' +
    '<p class="drop">The world lies open on the table: fifty lands, gathered into seven great regions, joined by borders and by sea routes. Each commander raises armies, strikes at neighbours and holds what is won. The last commander with armies on the board rules the world and wins the game.</p>' +
    '<p>For a shorter evening, choose <b>The Short War</b> before you begin: the first commander to hold thirty lands at once is the winner.</p>' +
    '<h4>In the box</h4><ul><li>The board: a chart of the world in fifty lands</li><li>Six armies of lacquered pieces, one colour for each commander</li><li>Five dice</li><li>Fifty-two cards: one for every land, and two wild cards</li><li>This book</li></ul>' +
    '<h4>The shape of a turn</h4><ol><li><b>Reinforce</b> — collect new armies and place them.</li><li><b>Attack</b> — as often as you dare, or not at all.</li><li><b>Move</b> — one march between your own lands, then your turn ends.</li></ol>' +
    '<div class="folio">— 1 —</div>',
    // 2
    '<h3>Setting Up</h3><div class="orn">◆ ◆ ◆</div>' +
    '<p class="drop">The first commander to sit down is the host, who chooses how the campaign begins. Each commander picks a colour and receives a starting army:</p>' +
    '<table><tr><th>Commanders</th><th>Armies each</th></tr><tr><td>Two</td><td>45</td></tr><tr><td>Three</td><td>40</td></tr><tr><td>Four</td><td>32</td></tr><tr><td>Five</td><td>27</td></tr><tr><td>Six</td><td>23</td></tr></table>' +
    '<h4>Three ways to begin</h4>' +
    '<p><b>Deal the lands.</b> The fifty lands are dealt out at random with one army on each. Then, in turn, each commander places three more armies at a time on lands of their own until every army stands on the board.</p>' +
    '<p><b>Choose the lands.</b> In turn, each commander claims one empty land with one army until all fifty are taken. The remaining armies are then placed three at a time, as above.</p>' +
    '<p><b>Quick start.</b> Lands and armies are all set out at random and the first turn begins at once.</p>' +
    '<p>Turn order is drawn by lot when the game begins and is shown along the top of the table.</p>' +
    '<div class="folio">— 2 —</div>',
    // 3
    '<h3>Reinforcements</h3><div class="orn">◆ ◆ ◆</div>' +
    '<p class="drop">At the start of your turn you receive new armies. Count the lands you hold and divide by three, ignoring any remainder. You never receive fewer than three.</p>' +
    '<p style="text-align:center;font-style:italic">Fourteen lands bring four armies. Eight lands still bring three.</p>' +
    '<h4>Whole regions</h4><p>If you hold every land in a region when your turn begins, you receive its bonus as well:</p>' +
    '<table><tr><th>Region</th><th>Size</th><th>Bonus</th></tr>' + regRows + '</table>' +
    '<h4>Placing them</h4><p>Place your new armies on any lands you already hold, all in one place or spread about as you please. Click a land to place an army there. The <i>Place 1 · 5 · all</i> switch sets how many go down with each click.</p>' +
    '<p>You may also trade in cards for extra armies now. See <i>The Cards</i>.</p>' +
    '<div class="folio">— 3 —</div>',
    // 4
    '<h3>Battle</h3><div class="orn">◆ ◆ ◆</div>' +
    '<p class="drop">You may attack any enemy land that touches one of yours, across a border or along a dotted sea route. The attacking land must hold at least two armies, because one must always stay behind.</p>' +
    '<h4>The dice</h4><p>The attacker rolls one, two or three dice, but always at least one fewer than the armies in the attacking land. The defender rolls two dice, or one if only one army defends.</p>' +
    '<p>Set the highest attacking die against the highest defending die. The higher number wins and the loser removes one army. <b>A tie goes to the defender.</b> If both sides rolled two or more dice, compare the second-highest pair in the same way.</p>' +
    '<div class="dicerow">' + die(6, 'crimson') + die(4, 'crimson') + die(2, 'crimson') + '&nbsp; against &nbsp;' + die(5, 'navy') + die(4, 'navy') + '</div>' +
    '<p style="text-align:center;font-style:italic">Six beats five: the defender loses one.<br>Four ties four: the attacker loses one.</p>' +
    '<h4>Pressing on</h4><p>After each roll you may roll again, fall back, or turn on another land. <b>Fight to the end</b> keeps rolling for you until the land falls or you can attack no longer.</p>' +
    '<h4>Conquest</h4><p>When the last defender falls, the land is yours. As many armies as the dice you last rolled march in at once, and you may send more after them, so long as one stays behind.</p>' +
    '<div class="folio">— 4 —</div>',
    // 5
    '<h3>The Cards</h3><div class="orn">◆ ◆ ◆</div>' +
    '<p class="drop">If you conquer at least one land during your turn, you draw one card when the turn ends. One card only, however many lands you took.</p>' +
    '<div class="fig"><figure><img src="img/compass.png" alt="">Compass</figure><figure><img src="img/anchor.png" alt="">Anchor</figure><figure><img src="img/crown.png" alt="">Crown</figure></div>' +
    '<p>Each card shows a land and one of three emblems. A <b>set</b> is three cards with the same emblem, or one of each. A wild card completes any set.</p>' +
    '<h4>Trading</h4><p>At the start of your turn you may trade a set for extra armies. Each set traded in the game, by anyone, is worth more than the last:</p>' +
    '<table class="wide"><tr><th>Set</th><th>1st</th><th>2nd</th><th>3rd</th><th>4th</th><th>5th</th><th>6th</th><th>after</th></tr><tr><td>Armies</td><td>4</td><td>6</td><td>8</td><td>10</td><td>12</td><td>15</td><td>+5 each</td></tr></table>' +
    '<p>If one of the three cards shows a land you hold, two extra armies are set down on that land.</p>' +
    '<p>If you begin a turn with five cards or more, you must trade a set before placing any armies.</p>' +
    '<div class="folio">— 5 —</div>',
    // 6
    '<h3>The March</h3><div class="orn">◆ ◆ ◆</div>' +
    '<p class="drop">When you have finished attacking, you may make one march: move as many armies as you like from one of your lands to another, provided the two are joined by an unbroken chain of your own lands. One army must stay behind. Then your turn ends.</p>' +
    '<p>You may also end your turn without marching.</p>' +
    '<h4>Defeating a commander</h4><p>Take a commander\'s last land and they are out of the game. Their cards pass to you. If that leaves you holding six cards or more, you must trade sets at once and place the armies before you fight on.</p>' +
    '<h4>Victory</h4><p>The game ends the moment only one commander remains or, in the Short War, the moment someone holds thirty lands.</p>' +
    '<h4>Round the edge</h4><p>The world is round. Alaska and Kamchatka are neighbours across the strait, and a long sea route joins New Zealand to the Pampas. Both run off one edge of the board and on at the other.</p>' +
    '<div class="folio">— 6 —</div>',
    // 7
    '<h3>At the Table</h3><div class="orn">◆ ◆ ◆</div>' +
    '<h4>On your turn</h4><ul><li>Lands you can use are edged in light. Click one.</li><li>To attack, click your land, then the enemy land beside it.</li><li>To march, click the land to leave, then the land to reach.</li><li>The brass button on the right moves you to the next part of your turn.</li></ul>' +
    '<h4>Round buttons</h4><ul><li><b>Cards</b> opens your hand. It glows when you hold a set.</li><li><b>Flag</b> colours every land by who holds it, or shows the bare chart.</li><li><b>Book</b> opens these rules.</li></ul>' +
    '<h4>If someone must leave</h4><p>The host may click that commander\'s name plate to let the computer play in their place, and click again when they return. A commander who closes the window by mistake can come back: open the game again and sign the same name.</p>' +
    '<h4>Counsel for new commanders</h4><ul><li>A whole region pays every turn. The small ones are easier to keep.</li><li>Guard the lands that touch an enemy; those behind them need only one army.</li><li>Three dice against one is a fine attack. Three against two is a fair one. Fewer is a gamble.</li><li>Take at least one land each turn for the card.</li></ul>' +
    '<div class="folio">— 7 —</div>',
  ];
})(typeof window !== 'undefined' ? window : globalThis);
