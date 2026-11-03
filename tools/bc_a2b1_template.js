function showTab(i) {
    document.querySelectorAll('.tab-btn').forEach((b, j) => b.classList.toggle('active', i === j));
    document.querySelectorAll('.tab-content').forEach((c, j) => c.classList.toggle('active', i === j));
    window.scrollTo({ top: 0, behavior: 'smooth' });
}
function tf(btn, correct) {
    const row = btn.parentElement;
    row.querySelectorAll('button').forEach(b => b.classList.remove('right', 'wrong'));
    btn.classList.add(correct ? 'right' : 'wrong');
}
let timerInterval = null;
let timeRemaining = 180;
let currentDuration = 180;
function setDuration(btn, minutes) {
    if (timerInterval) { clearInterval(timerInterval); timerInterval = null; }
    document.querySelectorAll('.duration-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    currentDuration = minutes * 60;
    timeRemaining = currentDuration;
    updateDisplay();
    document.querySelector('.timer').classList.remove('warning', 'danger');
}
function updateDisplay() {
    const m = Math.floor(timeRemaining / 60);
    const s = timeRemaining % 60;
    document.getElementById('timer-display').textContent = m + ':' + (s < 10 ? '0' : '') + s;
}
function resetTimer() {
    if (timerInterval) { clearInterval(timerInterval); timerInterval = null; }
    timeRemaining = currentDuration;
    updateDisplay();
    document.querySelector('.timer').classList.remove('warning', 'danger');
}
function startTimer() {
    if (timerInterval) return;
    timerInterval = setInterval(() => {
        timeRemaining--;
        updateDisplay();
        const t = document.querySelector('.timer');
        if (timeRemaining <= 10) { t.classList.add('danger'); t.classList.remove('warning'); }
        else if (timeRemaining <= 30) { t.classList.add('warning'); t.classList.remove('danger'); }
        else { t.classList.remove('warning', 'danger'); }
        if (timeRemaining <= 0) {
            clearInterval(timerInterval);
            timerInterval = null;
            document.getElementById('timer-display').textContent = 'Time is up';
        }
    }, 1000);
}
