/* A1 Pathway — shared lesson behaviour.
   Loaded by every a1p_*.html page. Adds four things the lessons were missing:
     1. answers that survive a refresh (localStorage)
     2. "I can" statements the student ticks, instead of pre-ticked ones
     3. a way to get to the next lesson
     4. a listen button on every pronunciation guide
   Everything degrades quietly: if storage or speech is unavailable, the page
   still works exactly as it did before. */
(function () {
  "use strict";

  var LESSONS = [["a1p_01_introductions.html","Hello! Introductions"],["a1p_02_where_are_you_from.html","Where Are You From?"],["a1p_03_what_do_you_do.html","What Do You Do?"],["a1p_04_numbers_basics.html","Numbers & Basics"],["a1p_05_review_foundation.html","REVIEW: Foundation Check"],["a1p_06_family_people.html","Family & People"],["a1p_07_daily_routines.html","Daily Routines"],["a1p_08_food_drinks.html","Food & Drinks Basics"],["a1p_09_where_is_it.html","Where Is It?"],["a1p_09b_prepositions_drag_drop.html","Where Is It? — Drag & Drop"],["a1p_10_review_unit1.html","REVIEW: Unit 1 Complete"],["a1p_11_what_did_you_do.html","What Did You Do?"],["a1p_12_yesterdays_story.html","Yesterday's Story"],["a1p_13_going_shopping.html","Going Shopping"],["a1p_14_making_plans.html","Making Plans"],["a1p_15_review_past_future.html","REVIEW: Past & Future"],["a1p_16_can_you_help.html","Can You Help?"],["a1p_17_asking_directions.html","Asking for Directions"],["a1p_18_how_often.html","How Often?"],["a1p_19_describing_things.html","Describing Things"],["a1p_20_review_unit2_complete.html","REVIEW: Unit 2 Complete"],["a1p_21_right_now.html","Right Now!"],["a1p_22_bigger_better.html","Bigger & Better"],["a1p_23_giving_opinions.html","Giving Opinions"],["a1p_24_the_best.html","The Best!"],["a1p_25_review_expressing_ideas.html","REVIEW: Expressing Ideas"],["a1p_26_must_should.html","Must & Should"],["a1p_27_telling_stories.html","Telling Stories"],["a1p_28_have_you_ever.html","Have You Ever...?"],["a1p_29_making_suggestions.html","Making Suggestions"],["a1p_30_review_unit3_complete.html","REVIEW: Unit 3 Complete"],["a1p_31_restaurant.html","At the Restaurant"],["a1p_32_phone_calls.html","Making Phone Calls"],["a1p_33_first_conditional.html","If I Had Time..."],["a1p_34_questions.html","Questions, Questions!"],["a1p_35_review_social_skills.html","REVIEW: Social Skills"],["a1p_36_weather.html","Talking About Weather"],["a1p_37_health_body.html","Health & Body"],["a1p_38_travel_transport.html","Travel & Transport"],["a1p_39_could_would.html","Could & Would"],["a1p_40_review_unit4_complete.html","REVIEW: Unit 4 Complete"],["a1p_41_conversation_management.html","Conversation Management"],["a1p_42_describing_experiences.html","Describing Experiences"],["a1p_43_present_perfect_vs_past.html","Present Perfect vs Past"],["a1p_44_making_invitations.html","Making Invitations"],["a1p_45_review_advanced_integration.html","REVIEW: Advanced Integration"],["a1p_46_used_to.html","Used To"],["a1p_47_discussing_future_plans.html","Discussing Future Plans"],["a1p_48_giving_advice.html","Giving Advice"],["a1p_49_connected_speech.html","Connected Speech"],["a1p_50_pathway_complete.html","A1 PATHWAY COMPLETE"]];

  var FILE = (location.pathname.split("/").pop() || "").replace(/\.html$/, "");
  if (!FILE) FILE = "a1p_unknown";
  var NS = "a1p:" + FILE + ":";

  /* ---------- storage, with a working no-op fallback ---------- */
  var store = (function () {
    try {
      var k = "__a1p_probe__";
      window.localStorage.setItem(k, "1");
      window.localStorage.removeItem(k);
      return window.localStorage;
    } catch (e) {
      return null;
    }
  })();
  function get(k) { try { return store && store.getItem(NS + k); } catch (e) { return null; } }
  function set(k, v) { try { if (store) store.setItem(NS + k, v); } catch (e) {} }
  function drop() {
    if (!store) return;
    try {
      var kill = [];
      for (var i = 0; i < store.length; i++) {
        var key = store.key(i);
        if (key && key.indexOf(NS) === 0) kill.push(key);
      }
      kill.forEach(function (k) { store.removeItem(k); });
    } catch (e) {}
  }

  /* ---------- 1. keep what the student writes ---------- */
  function fieldsToSave() {
    return Array.prototype.slice.call(
      document.querySelectorAll('textarea, input[type="text"], input:not([type])')
    );
  }
  function keyFor(el, i) {
    return el.id || el.name || ("field" + i);
  }
  function wireSaving() {
    var fields = fieldsToSave();
    fields.forEach(function (el, i) {
      var k = keyFor(el, i);
      var saved = get(k);
      if (saved !== null && saved !== undefined && el.value === "") el.value = saved;
      var t;
      el.addEventListener("input", function () {
        clearTimeout(t);
        t = setTimeout(function () { set(k, el.value); flash(); }, 400);
      });
    });
    return fields.length;
  }

  var badge;
  function flash() {
    if (!badge) return;
    badge.textContent = "Saved";
    badge.style.opacity = "1";
    clearTimeout(flash._t);
    flash._t = setTimeout(function () { badge.style.opacity = "0"; }, 1400);
  }

  /* ---------- 2. "I can" statements the student earns ---------- */
  function wireICan() {
    var boxes = document.querySelectorAll(".i-can-statement");
    var n = 0;
    Array.prototype.forEach.call(boxes, function (box, bi) {
      if (box.getAttribute("data-a1p-done")) return;
      var html = box.innerHTML;
      if (html.indexOf("\u2705") === -1) return;
      var parts = html.split("\u2705");
      var lead = parts.shift();
      var rebuilt = lead;
      parts.forEach(function (chunk, ci) {
        /* a statement ends at its first line break; anything after that
           (the next item's separator, or a closing flourish like
           "I AM READY FOR INTERMEDIATE ENGLISH!") stays outside the label */
        var trail = "";
        var cut = chunk.match(/^([\s\S]*?)((?:\s*<br\s*\/?>\s*)+[\s\S]*)$/i);
        if (cut) { chunk = cut[1]; trail = cut[2]; }
        var id = "ican-" + bi + "-" + ci;
        var on = get(id) === "1";
        rebuilt +=
          '<label class="a1p-ican" data-key="' + id + '">' +
          '<input type="checkbox" ' + (on ? "checked" : "") + ">" +
          "<span>" + chunk + "</span></label>" + trail;
        n++;
      });
      box.innerHTML = rebuilt;
      box.setAttribute("data-a1p-done", "1");
    });
    document.addEventListener("change", function (e) {
      var lab = e.target.closest && e.target.closest("label.a1p-ican");
      if (!lab) return;
      set(lab.getAttribute("data-key"), e.target.checked ? "1" : "0");
      flash();
    });
    return n;
  }

  /* ---------- 3. a way onward ---------- */
  function wireNav() {
    var idx = -1;
    for (var i = 0; i < LESSONS.length; i++) {
      if (LESSONS[i][0] === FILE + ".html") { idx = i; break; }
    }
    if (idx === -1) return false;   /* not in the sequence: skip the arrows, keep the footer */
    var prev = idx > 0 ? LESSONS[idx - 1] : null;
    var next = idx < LESSONS.length - 1 ? LESSONS[idx + 1] : null;

    var bar = document.createElement("nav");
    bar.className = "a1p-nav";
    bar.innerHTML =
      (prev
        ? '<a class="a1p-nav-link" href="' + prev[0] + '"><span class="a1p-nav-dir">\u2190 Previous</span>' +
          '<span class="a1p-nav-title">' + prev[1] + "</span></a>"
        : '<span class="a1p-nav-link a1p-nav-empty"></span>') +
      '<a class="a1p-nav-hub" href="a1_pathway_dashboard.html">All 50 lessons</a>' +
      (next
        ? '<a class="a1p-nav-link a1p-nav-next" href="' + next[0] + '"><span class="a1p-nav-dir">Next \u2192</span>' +
          '<span class="a1p-nav-title">' + next[1] + "</span></a>"
        : '<span class="a1p-nav-link a1p-nav-empty"></span>');

    document.body.appendChild(bar);
    return true;
  }

  /* the save note + clear control, shown on every lesson whether or not it
     sits in the numbered sequence */
  function wireFoot() {
    if (!store) return;                      /* nothing is being saved, so say nothing */
    var foot = document.createElement("div");
    foot.className = "a1p-foot";
    foot.innerHTML =
      '<span class="a1p-foot-note">Your answers are saved on this device. ' +
      '<button type="button" class="a1p-clear">Clear my answers for this lesson</button></span>' +
      '<span class="a1p-saved" aria-live="polite"></span>';
    document.body.appendChild(foot);
    badge = foot.querySelector(".a1p-saved");
    foot.querySelector(".a1p-clear").addEventListener("click", function () {
      if (!confirm("Clear everything you have written in this lesson? This cannot be undone.")) return;
      drop();
      location.reload();
    });
  }

  /* ---------- 4. let them hear the word ---------- */
  function wireSpeech() {
    if (!("speechSynthesis" in window)) return 0;
    var voice = null;
    function pickVoice() {
      var vs = window.speechSynthesis.getVoices() || [];
      voice =
        vs.filter(function (v) { return v.lang === "en-GB"; })[0] ||
        vs.filter(function (v) { return /^en[-_]/i.test(v.lang); })[0] || null;
    }
    pickVoice();
    window.speechSynthesis.onvoiceschanged = pickVoice;

    function say(word) {
      try {
        window.speechSynthesis.cancel();
        var u = new SpeechSynthesisUtterance(word);
        u.rate = 0.8;
        u.lang = "en-GB";
        if (voice) u.voice = voice;
        window.speechSynthesis.speak(u);
      } catch (e) {}
    }

    var n = 0;
    Array.prototype.forEach.call(document.querySelectorAll("p > strong, p > span.word"), function (s) {
      var p = s.parentNode;
      if (p.getAttribute("data-a1p-say")) return;
      if (s !== p.firstChild) return;
      var after = (s.nextSibling && s.nextSibling.nodeValue) || "";
      if (after.replace(/^\s+/, "").charAt(0) !== "=") return;   // only "Word = respelling" lines
      var word = (s.textContent || "").trim();
      if (!word || word.length > 34) return;
      var b = document.createElement("button");
      b.type = "button";
      b.className = "a1p-say";
      b.setAttribute("aria-label", "Listen to " + word);
      b.title = "Listen to " + word;
      b.textContent = "\uD83D\uDD0A";
      b.addEventListener("click", function () { say(word); });
      p.insertBefore(b, s);
      p.setAttribute("data-a1p-say", "1");
      n++;
    });
    return n;
  }

  /* ---------- styles ---------- */
  function styles() {
    var css = document.createElement("style");
    css.textContent = [
      ".a1p-say{background:none;border:0;cursor:pointer;font-size:1em;line-height:1;padding:0 6px 0 0;opacity:.65;transition:opacity .15s;}",
      ".a1p-say:hover,.a1p-say:focus{opacity:1;}",
      "label.a1p-ican{display:inline-flex;align-items:flex-start;gap:.55em;cursor:pointer;text-align:left;}",
      "label.a1p-ican input{margin:.18em 0 0;width:1.25em;height:1.25em;flex:none;cursor:pointer;accent-color:#2e7d32;box-shadow:0 0 0 2px rgba(255,255,255,.35);border-radius:3px;}",
      "label.a1p-ican span{flex:1;}",
      ".a1p-nav{display:flex;gap:12px;align-items:stretch;max-width:1000px;margin:34px auto 0;padding:0 20px;",
        "font-family:'Segoe UI',Tahoma,Geneva,Verdana,sans-serif;}",
      ".a1p-nav-link{flex:1;display:flex;flex-direction:column;gap:2px;padding:14px 16px;border:1px solid #dfe3ea;",
        "border-radius:10px;background:#fff;text-decoration:none;color:#1a1a2e;transition:border-color .15s,box-shadow .15s;}",
      ".a1p-nav-link:hover{border-color:#667eea;box-shadow:0 2px 10px rgba(102,126,234,.16);}",
      ".a1p-nav-next{text-align:right;}",
      ".a1p-nav-empty{border:0;background:none;box-shadow:none;}",
      ".a1p-nav-dir{font-size:.78em;letter-spacing:.04em;text-transform:uppercase;color:#667eea;font-weight:700;}",
      ".a1p-nav-title{font-weight:600;}",
      ".a1p-nav-hub{display:flex;align-items:center;padding:14px 18px;border-radius:10px;background:#667eea;color:#fff;",
        "text-decoration:none;font-weight:600;white-space:nowrap;}",
      ".a1p-nav-hub:hover{background:#5568d3;}",
      ".a1p-foot{max-width:1000px;margin:12px auto 40px;padding:0 20px;display:flex;justify-content:space-between;",
        "align-items:center;gap:12px;font-family:'Segoe UI',Tahoma,Geneva,Verdana,sans-serif;font-size:.85em;color:#6b7280;}",
      ".a1p-clear{background:none;border:0;color:#6b7280;text-decoration:underline;cursor:pointer;font:inherit;padding:0;}",
      ".a1p-clear:hover{color:#c0392b;}",
      ".a1p-saved{opacity:0;transition:opacity .3s;color:#2e7d32;font-weight:600;}",
      "@media(max-width:700px){.a1p-nav{flex-direction:column;}.a1p-nav-next{text-align:left;}",
        ".a1p-nav-empty{display:none;}.a1p-foot{flex-direction:column;align-items:flex-start;}}",
      "@media print{.a1p-nav,.a1p-foot,.a1p-say{display:none;}}"
    ].join("");
    document.head.appendChild(css);
  }

  function boot() {
    try {
      styles();
      wireNav();
      wireFoot();
      wireSaving();
      wireICan();
      wireSpeech();
    } catch (e) {
      if (window.console) console.warn("a1p_lesson.js:", e);
    }
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
