/* IELTS Writing Task 2 course: a slim bar on every course page
   (back to the course, where you are, next lesson) and a "next" card at the end. */
(function () {
  var COURSE = 'ielts_course_index.html';
  var L = [ // [file, short title, number]
    ['ielts_lesson_1_academic_paragraphs', 'Introductions', '1'],
    ['ielts_lesson_2_marking_criteria', 'What examiners count', '2'],
    ['ielts_lesson_3_body_paragraphs', 'Body paragraphs', '3'],
    ['ielts_lesson_4_time_management', 'Time and planning', '4'],
    ['ielts_lesson_4b_generating_ideas', 'Finding ideas fast', '4b'],
    ['ielts_lesson_5_conclusions_linking', 'Conclusions and linking', '5'],
    ['ielts_lesson_6_opinion_essays', 'Opinion essays', '6'],
    ['ielts_lesson_7_discussion_essays', 'Discussion essays', '7'],
    ['ielts_lesson_8_advantages_disadvantages', 'Advantages and disadvantages', '8'],
    ['ielts_lesson_9_problem_solution', 'Problem and solution', '9'],
    ['ielts_lesson_10_two_part_questions', 'Two-part questions', '10'],
    ['ielts_lesson_11_vocabulary_collocations', 'Vocabulary and collocations', '11'],
    ['ielts_lesson_12_complex_sentences', 'Complex sentences', '12'],
    ['ielts_lesson_13_cohesion_coherence', 'Cohesion and flow', '13'],
    ['ielts_lesson_14_paraphrasing_variety', 'Paraphrasing', '14'],
    ['ielts_lesson_15_common_mistakes', 'Common mistakes', '15'],
    ['ielts_lesson_16_timed_practice_1', 'Timed essay 1', '16'],
    ['ielts_lesson_17_timed_practice_2', 'Timed essay 2', '17'],
    ['ielts_lesson_18_exam_simulation', 'Full writing test', '18'],
    ['ielts_lesson_19_feedback_analysis', 'Your improvement plan', '19'],
    ['ielts_lesson_20_final_strategies', 'Final strategies', '20']
  ];
  var W = { // workshop -> [label, matching full lesson]
    bc_ielts_paragraphs_examples_b2c1: ['Short workshop: paragraphs and examples', 'ielts_lesson_3_body_paragraphs'],
    bc_ielts_conclusions_b2c1: ['Short workshop: conclusions', 'ielts_lesson_5_conclusions_linking'],
    bc_ielts_opinion_essay_b2c1: ['Short workshop: opinion essays', 'ielts_lesson_6_opinion_essays'],
    bc_ielts_discussion_essay_b2c1: ['Short workshop: discussion essays', 'ielts_lesson_7_discussion_essays'],
    bc_ielts_advantages_disadvantages_b2c1: ['Short workshop: advantages and disadvantages', 'ielts_lesson_8_advantages_disadvantages'],
    bc_ielts_problem_solution_b2c1: ['Short workshop: problem and solution', 'ielts_lesson_9_problem_solution'],
    bc_ielts_two_part_questions_b2c1: ['Short workshop: two-part questions', 'ielts_lesson_10_two_part_questions'],
    bc_ielts_task1_graphs_b2c1: ['Task 1 workshop: graphs and processes', null]
  };
  var id = location.pathname.split('/').pop().replace(/\.html$/, '');
  var i = -1;
  for (var k = 0; k < L.length; k++) if (L[k][0] === id) i = k;
  var ws = W[id];
  if (i < 0 && !ws) return;
  var hasOwnNav = !!document.querySelector('a.nav-button');

  var css = document.createElement('style');
  css.textContent =
    '.icn{box-sizing:border-box;max-width:1100px;margin:0 auto 14px;display:flex;align-items:center;gap:10px 16px;flex-wrap:wrap;' +
    'background:#fff;border:1px solid #d9dcef;border-radius:12px;padding:9px 14px;font:15px/1.4 "Segoe UI",system-ui,-apple-system,sans-serif;color:#334}' +
    '.icn a{color:#4b3fa8;text-decoration:none;font-weight:600}.icn a:hover{text-decoration:underline}' +
    '.icn .icn-where{flex:1;min-width:150px;color:#556;text-align:center}.icn .icn-where b{color:#223}' +
    '.icn-end{box-sizing:border-box;max-width:1100px;margin:28px auto 18px;background:#f4f3ff;border:1px solid #d9dcef;border-radius:14px;' +
    'padding:18px 20px;font:16px/1.5 "Segoe UI",system-ui,-apple-system,sans-serif;color:#334;display:flex;flex-wrap:wrap;gap:12px 20px;align-items:center;justify-content:space-between}' +
    '.icn-end a.icn-go{background:#5b4fc4;color:#fff;text-decoration:none;font-weight:600;padding:10px 18px;border-radius:10px}' +
    '.icn-end a.icn-back{color:#4b3fa8;font-weight:600;text-decoration:none}' +
    '@media(max-width:600px){.icn .icn-where{order:3;flex-basis:100%;text-align:left}}' +
    '@media print{.icn,.icn-end{display:none}}';
  document.head.appendChild(css);

  function a(href, text, cls) {
    var e = document.createElement('a'); e.href = href + '.html'; e.textContent = text; if (cls) e.className = cls; return e;
  }
  function span(html, cls) { var e = document.createElement('span'); e.innerHTML = html; if (cls) e.className = cls; return e; }

  var bar = document.createElement('nav');
  bar.className = 'icn'; bar.setAttribute('aria-label', 'Course');
  bar.appendChild(a(COURSE.replace(/\.html$/, ''), '← IELTS Writing Task 2 course'));
  var next = null, label;
  if (i >= 0) {
    label = 'Lesson <b>' + L[i][2] + '</b> of 21 · ' + L[i][1];
    next = L[i + 1] || null;
  } else {
    label = '<b>' + ws[0] + '</b>';
  }
  bar.appendChild(span(label, 'icn-where'));
  if (i >= 0 && next && !hasOwnNav) bar.appendChild(a(next[0], 'Next: ' + next[1] + ' →'));
  if (ws && ws[1]) {
    for (var j = 0; j < L.length; j++) if (L[j][0] === ws[1]) bar.appendChild(a(L[j][0], 'Full lesson ' + L[j][2] + ' →'));
  }

  var end = document.createElement('div');
  end.className = 'icn-end';
  if (i >= 0 && next) {
    end.appendChild(span('Finished this lesson? Next is <b>Lesson ' + next[2] + ': ' + next[1] + '</b>.'));
    end.appendChild(a(next[0], 'Go to Lesson ' + next[2] + ' →', 'icn-go'));
  } else if (i >= 0) {
    end.appendChild(span('That is the last lesson in the course. Well done, and good luck in the exam.'));
  } else if (ws[1]) {
    for (var m = 0; m < L.length; m++) if (L[m][0] === ws[1]) {
      end.appendChild(span('Want to go deeper? <b>Lesson ' + L[m][2] + ': ' + L[m][1] + '</b> is the full version of this topic.'));
      end.appendChild(a(L[m][0], 'Open Lesson ' + L[m][2] + ' →', 'icn-go'));
    }
  } else {
    end.appendChild(span('This workshop is part of the IELTS writing course.'));
  }
  end.appendChild(a(COURSE.replace(/\.html$/, ''), 'All lessons in the course', 'icn-back'));

  function place() {
    document.body.insertBefore(bar, document.body.firstChild);
    var last = document.body.lastElementChild;
    while (last && last.tagName === 'SCRIPT') last = last.previousElementSibling;
    if (last && last.nextSibling) document.body.insertBefore(end, last.nextSibling); else document.body.appendChild(end);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', place); else place();
})();
