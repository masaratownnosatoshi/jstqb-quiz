/*!
 * JSTQB ALTM v3.0 テスト対策くん — 修正版v22
 * 対応: お気に入り機能（保存・読み込み・フィルタリング）の実装
 */

// ====== 初期化・状態 ======
let allQuestions = [];        
let sessionQuestions = [];    
let current = 0;
let correctCount = 0;
let isAnswerChecked = false;

// チャート保持用
let chartChapter = null;
let chartKLevel = null;
let dbChartChapter = null;
let dbChartKLevel = null;

let tempDetails = []; // セッション履歴
let favorites = [];   // ★追加: お気に入りリスト（問題IDの配列）

const OPTION_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'];

document.addEventListener('DOMContentLoaded', () => {
  try {
    // お気に入りデータのロード
    loadFavorites();

    let r = location.hash.replace('#', '');
    if (!r) r = 'home';
    showRoute(r);
    updateTotalCount();

    onClick('#startBtn', startWithFilters);   
    onClick('#submitBtn', submitAnswer);
    onClick('#restartBtn', restart);
    onClick('#goHomeBtn', goHome);
    onClick('#clearDataBtn', clearLocalData);
    
    // ★追加: お気に入りボタンのイベント
    onClick('#favBtn', toggleFavorite);

    window.addEventListener('hashchange', () => {
      let route = location.hash.replace('#', '');
      if (!route) route = 'home';
      showRoute(route);
      if (route === 'dashboard') renderDashboard();
    });

    const anonEl = document.getElementById('anonIdLabel');
    if (anonEl) anonEl.textContent = getActiveUserId();
    
    if (r === 'dashboard') renderDashboard();

  } catch (e) {
    console.error('Init Error:', e);
    alert('アプリの起動中にエラーが発生しました。\n' + e.message);
  }
});

// ====== ルーター ======
function showRoute(route) {
  const sections = document.querySelectorAll('section[data-route]');
  sections.forEach(sec => {
    if (sec.getAttribute('data-route') === route) {
      sec.classList.remove('hidden');
    } else {
      sec.classList.add('hidden');
    }
  });

  const meta = document.getElementById('meta');
  if (meta) {
    if (route === 'quiz') {
      meta.classList.remove('hidden');
    } else {
      meta.classList.add('hidden');
    }
  }
  location.hash = '#' + route;
  window.scrollTo(0, 0);
}

// ====== ユーティリティ ======
function onClick(sel, fn) {
  const el = document.querySelector(sel);
  if (el) el.onclick = fn;
}

function createAnonId() {
  return 'anon-' + Math.random().toString(36).slice(2, 10);
}

function getActiveUserId() {
  const inputEl = document.getElementById('userIdInput');
  const inputVal = inputEl ? inputEl.value.trim() : '';
  const stored = localStorage.getItem('altm_active_user');

  if (inputVal) {
    localStorage.setItem('altm_active_user', inputVal);
    return inputVal;
  }
  if (stored) return stored;
  const anon = createAnonId();
  localStorage.setItem('altm_active_user', anon);
  return anon;
}

// 集合比較（安全版）
function eqSetCompat(selectedArr, correctArr) {
  if (!Array.isArray(selectedArr) || !Array.isArray(correctArr)) return false;
  if (selectedArr.length !== correctArr.length) return false;
  
  const a = new Set(selectedArr.map(String));
  const b = new Set(correctArr.map(String));
  for (const v of a) {
    if (!b.has(v)) return false;
  }
  return true;
}

function shuffleArray(array) {
  const res = array.slice();
  for (let i = res.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [res[i], res[j]] = [res[j], res[i]];
  }
  return res;
}

function randomizeQuestionOptions(q) {
  const originalOpts = q.options || q.choices || [];
  if (originalOpts.length === 0) return q;

  let correctOriginalIndices = new Set();
  let rawAns = Array.isArray(q.answer) ? q.answer : (q.answer !== undefined ? [q.answer] : []);

  if (rawAns.length > 0 && typeof rawAns[0] === 'string') {
    rawAns.forEach(ansStr => {
      const idx = originalOpts.findIndex(o => String(o).trim() === String(ansStr).trim());
      if (idx !== -1) correctOriginalIndices.add(idx);
    });
  } else {
    rawAns.forEach(idx => correctOriginalIndices.add(parseInt(idx, 10)));
  }

  let items = originalOpts.map((text, index) => ({
    text: text,
    isCorrect: correctOriginalIndices.has(index)
  }));

  items = shuffleArray(items);

  let newQ = { ...q };
  newQ.options = items.map(i => i.text);
  if (newQ.choices) delete newQ.choices;

  newQ.answer = items
    .map((item, index) => item.isCorrect ? index : -1)
    .filter(idx => idx !== -1);

  return newQ;
}

function resolveRepoUrl(input) {
  const base = new URL(document.baseURI);
  if (/^https?:\/\//i.test(input)) return input;
  if (input.startsWith('/')) {
    const sub = input.replace(/^\//, '');
    const repoPath = base.pathname.replace(/\/$/, '');
    const prefix = repoPath ? (repoPath + '/') : '/';
    return base.origin + prefix + sub;
  }
  return new URL(input, base).href;
}

// ====== お気に入り機能 ======
function loadFavorites() {
  try {
    const stored = localStorage.getItem('altm_favorites');
    favorites = stored ? JSON.parse(stored) : [];
  } catch (e) {
    console.error('Favorites load error', e);
    favorites = [];
  }
}

function saveFavorites() {
  localStorage.setItem('altm_favorites', JSON.stringify(favorites));
}

function toggleFavorite() {
  const q = sessionQuestions[current];
  if (!q || !q.id) return;

  const index = favorites.indexOf(q.id);
  if (index === -1) {
    favorites.push(q.id);
  } else {
    favorites.splice(index, 1);
  }
  saveFavorites();
  
  // ボタンの状態更新
  updateFavButtonState(q.id);
}

function updateFavButtonState(qId) {
  const btn = document.getElementById('favBtn');
  if (!btn) return;
  
  if (favorites.includes(qId)) {
    btn.classList.add('active');
    btn.textContent = '★'; // 塗りつぶし星
  } else {
    btn.classList.remove('active');
    btn.textContent = '☆'; // 白抜き星
  }
}


// ====== 履歴・DB関連 ======
function pushTempDetail(q, ok) {
  tempDetails.push({ 
    id: q.id || ('unknown-' + Math.random()), 
    correct: !!ok,
    chapter: q.chapter || "未分類",
    klevel: q.klevel || q.level || "不明",
    ts: Date.now()
  });
}

function getHistory(user) {
  try {
    const key = 'altm_history_' + (user || 'guest');
    const raw = localStorage.getItem(key);
    return raw ? JSON.parse(raw) : [];
  } catch (e) {
    console.error("History load error:", e);
    return [];
  }
}

function saveHistory(user, session) {
  try {
    const key = 'altm_history_' + (user || 'guest');
    const h = getHistory(user);
    h.unshift(session);
    if (h.length > 100) h.length = 100; 
    localStorage.setItem(key, JSON.stringify(h));
  } catch (e) {
    console.error("History save error:", e);
  }
}

function clearLocalData() {
  if (!confirm("学習履歴とお気に入りをすべて削除しますか？\n（グラフや正答率がリセットされます）")) return;
  const user = getActiveUserId();
  const histKey = 'altm_history_' + (user || 'guest');
  localStorage.removeItem(histKey);
  
  // お気に入りも消す場合
  localStorage.removeItem('altm_favorites');
  favorites = [];

  if (dbChartChapter) dbChartChapter.destroy();
  if (dbChartKLevel) dbChartKLevel.destroy();
  
  renderDashboard();
  alert("削除しました");
}

function isLastAnswerIncorrect(qId) {
  if (!qId) return false;
  const user = getActiveUserId();
  const hist = getHistory(user);
  if (!hist || hist.length === 0) return false;

  for (const session of hist) {
    if (session.details && Array.isArray(session.details)) {
      const detail = session.details.find(d => d.id === qId);
      if (detail) {
        return !detail.correct;
      }
    }
  }
  return false;
}

// ====== IndexedDB ======
const DB_NAME = 'ALTM_DB';
const DB_VERSION = 2;
let _db;

function openDb() {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(DB_NAME, DB_VERSION);
    req.onupgradeneeded = (e) => {
      const db = e.target.result;
      if (!db.objectStoreNames.contains('questionChunks')) db.createObjectStore('questionChunks');
      if (!db.objectStoreNames.contains('manifest')) db.createObjectStore('manifest');
    };
    req.onsuccess = () => { _db = req.result; resolve(_db); };
    req.onerror = () => reject(req.error);
  });
}

async function idbGet(store, key) {
  if (!_db) await openDb();
  return new Promise((resolve, reject) => {
    const tx = _db.transaction(store, 'readonly');
    const os = tx.objectStore(store);
    const rq = os.get(key);
    rq.onsuccess = () => resolve(rq.result || null);
    rq.onerror = () => reject(rq.error);
  });
}

async function idbPut(store, key, value) {
  if (!_db) await openDb();
  return new Promise((resolve, reject) => {
    const tx = _db.transaction(store, 'readwrite');
    const os = tx.objectStore(store);
    const rq = os.put(value, key);
    rq.onsuccess = () => resolve(true);
    rq.onerror = () => reject(rq.error);
  });
}

// ====== データ取得 ======
async function fetchJSON(inputUrl) {
  const finalUrl = resolveRepoUrl(inputUrl);
  try {
    const res = await fetch(finalUrl, { cache: 'no-store' });
    if (res.status === 404) return { ok: false, status: 404, json: null };
    if (!res.ok) return { ok: false, status: res.status, json: null };
    const json = await res.json();
    return { ok: true, status: 200, json: json };
  } catch (e) {
    console.error('[json] fetch error', inputUrl, e);
    return { ok: false, status: 0, json: null };
  }
}

async function loadManifest() {
  const result = await fetchJSON('questions/index.json');
  if (!result.ok) return null;
  let chunks = [];
  if (result.json && Array.isArray(result.json.chunks)) chunks = result.json.chunks;
  else if (Array.isArray(result.json)) chunks = result.json;
  await idbPut('manifest', 'index', { chunks: chunks });
  return chunks;
}

async function loadChunk(path) {
  const cached = await idbGet('questionChunks', path);
  if (cached) {
    if (Array.isArray(cached)) return cached;
    if (cached.questions && Array.isArray(cached.questions)) return cached.questions;
    return [];
  }
  const result = await fetchJSON(path);
  if (!result.ok) return [];
  let arr = [];
  if (Array.isArray(result.json)) arr = result.json;
  else if (result.json && Array.isArray(result.json.questions)) arr = result.json.questions;
  await idbPut('questionChunks', path, result.json);
  return arr;
}

async function updateTotalCount() {
  try {
    const chunks = await loadManifest();
    const countEl = document.getElementById('totalCount');
    if (!chunks || !Array.isArray(chunks)) {
      if(countEl) countEl.textContent = "-";
      return;
    }
    const total = chunks.reduce((sum, chunk) => sum + (chunk.qCount || 0), 0);
    if (countEl) countEl.textContent = total;
  } catch (e) {
    console.error('Counts error:', e);
  }
}

async function loadQuestionsByIndex(conditions) {
  const idxChunks = await loadManifest();
  if (!idxChunks) return [];
  
  let targetChunks = idxChunks.filter(c => {
    const cond = conditions || {};
    if (cond.chapters && cond.chapters.length > 0) {
      if (!cond.chapters.includes(c.chapter)) return false;
    }
    if (cond.categories && cond.categories.length > 0) {
      if (!cond.categories.includes(c.category)) return false;
    }
    return true;
  });

  if (targetChunks.length === 0) targetChunks = idxChunks;

  const all = [];
  for (const c of targetChunks) {
    const part = await loadChunk(c.path);
    if (Array.isArray(part)) all.push(...part);
  }
  return all;
}

function collectFilters() {
  const chapters = Array.from(document.querySelectorAll('.chapterFilter:checked')).map(i => i.value);
  const levels   = Array.from(document.querySelectorAll('.levelFilter:checked')).map(i => i.value);
  const cats     = Array.from(document.querySelectorAll('.categoryFilter:checked')).map(i => i.value);
  return { chapters, levels, cats };
}

// ====== フィルタ判定（お気に入り対応） ======
function matchesQuestion(q, cond) {
  // お気に入りモード
  if (cond.favOnly) {
    // IDがfavorites配列になければ除外
    if (!favorites.includes(q.id)) return false;
  }

  // 計算モード
  if (cond.calcOnly) {
    if (!q.question || !q.question.includes('【計算】')) {
      return false;
    }
  }

  if (cond.chapters && cond.chapters.length > 0) {
    const qCh = (q.chapter || '').trim();
    if (!cond.chapters.some(sel => sel === qCh)) return false;
  }
  if (cond.categories && cond.categories.length > 0) {
    const qCat = (q.category || '').trim();
    if (!cond.categories.some(sel => sel === qCat)) return false;
  }
  if (cond.klevels && cond.klevels.length > 0) {
    const qK = (q.klevel || q.level || '').trim();
    if (qK && !cond.klevels.some(sel => sel === qK)) return false;
  }
  return true;
}

// ====== UI構築 ======
function renderQuestions(questions) {
  const q = questions[current];
  const textEl = document.getElementById('questionText');
  const choicesEl = document.getElementById('choices');
  const idxEl = document.getElementById('progress');
  const feedbackEl = document.getElementById('feedback');
  const submitBtn = document.getElementById('submitBtn');
  const chapterEl = document.getElementById('chapter');
  const levelEl = document.getElementById('level');

  if (!q) {
    alert('問題データがありません。');
    return;
  }
  
  isAnswerChecked = false;
  if (feedbackEl) feedbackEl.classList.add('hidden');
  if (submitBtn) {
    submitBtn.textContent = '回答する';
    submitBtn.disabled = false;
  }

  if (idxEl) idxEl.textContent = (current + 1) + ' / ' + questions.length;
  if (chapterEl) chapterEl.textContent = q.chapter || '';
  if (levelEl) levelEl.textContent = q.klevel || q.level || '';
  
  document.querySelectorAll('.retry-alert').forEach(e => e.remove());

  if (q.id && isLastAnswerIncorrect(q.id)) {
    const badge = document.createElement('div');
    badge.className = 'retry-alert';
    badge.textContent = '以前間違えた問題です';
    textEl.parentNode.insertBefore(badge, textEl);
  }

  // お気に入りボタンの更新
  updateFavButtonState(q.id);

  const qText = q.question || q.text || q.title || '(問題文)';
  if (textEl) textEl.textContent = qText;

  if (choicesEl) {
    choicesEl.innerHTML = '';
    let opts = [];
    if (Array.isArray(q.options)) opts = q.options;
    else if (Array.isArray(q.choices)) opts = q.choices;

    const isMulti = q.multi || q.type === '複数選択';

    opts.forEach((optText, i) => {
      const div = document.createElement('div');
      div.style.padding = '8px 0';
      const label = document.createElement('label');
      label.style.display = 'flex';
      label.style.alignItems = 'center'; 
      label.style.cursor = 'pointer';

      const input = document.createElement('input');
      input.type = isMulti ? 'checkbox' : 'radio';
      input.name = 'answer';
      input.value = String(i);
      input.style.marginRight = '8px';
      input.style.transform = 'scale(1.2)'; 

      const tagSpan = document.createElement('span');
      tagSpan.className = 'option-tag';
      tagSpan.textContent = OPTION_LABELS[i] || '?';

      const textSpan = document.createElement('span');
      textSpan.className = 'option-content';
      textSpan.textContent = optText;
      textSpan.style.flex = '1';

      label.appendChild(input);
      label.appendChild(tagSpan);
      label.appendChild(textSpan);
      div.appendChild(label);
      choicesEl.appendChild(div);
    });
  }
}

// ====== 回答ロジック ======
function submitAnswer() {
  try {
    const q = sessionQuestions[current];
    if (!q) return;

    const feedbackEl = document.getElementById('feedback');
    const correctEl = document.getElementById('correctAnswer');
    const explainEl = document.getElementById('explanation');
    const judgeEl = document.getElementById('judgeResult');
    const submitBtn = document.getElementById('submitBtn');
    const scoreEl = document.getElementById('score');

    if (isAnswerChecked) {
      if (current < sessionQuestions.length - 1) {
        current++;
        renderQuestions(sessionQuestions);
      } else {
        finishSession();
      }
      return;
    }

    const inputs = Array.from(document.querySelectorAll('input[name="answer"]'));
    const selected = inputs.filter(i => i.checked).map(i => parseInt(i.value, 10));
    
    if (selected.length === 0) {
      alert('選択肢を選んでください');
      return;
    }

    let opts = [];
    if (Array.isArray(q.options)) opts = q.options;
    else if (Array.isArray(q.choices)) opts = q.choices;

    let correctIndices = [];
    let rawAnswer = [];
    if (Array.isArray(q.answer)) rawAnswer = q.answer;
    else if (q.answer !== undefined) rawAnswer = [q.answer];

    if (rawAnswer.length > 0 && typeof rawAnswer[0] === 'string') {
      correctIndices = rawAnswer.map(ansStr => {
        return opts.findIndex(opt => String(opt).trim() === String(ansStr).trim());
      }).filter(idx => idx !== -1);
    } else {
      correctIndices = rawAnswer.map(v => parseInt(v, 10));
    }
    correctIndices.sort((a, b) => a - b);

    const ok = eqSetCompat(selected, correctIndices);
    pushTempDetail(q, ok);
    
    if (ok) {
      correctCount++;
      if (scoreEl) scoreEl.textContent = correctCount;
    }
    
    if (judgeEl) {
      if (ok) {
        judgeEl.textContent = '正解！';
        judgeEl.className = 'judge-correct'; 
      } else {
        judgeEl.textContent = 'ざんねん…';
        judgeEl.className = 'judge-incorrect';
    }
    }

    const correctLabels = correctIndices.map(i => OPTION_LABELS[i] || '?').join(', ');
    const correctTextFull = correctIndices.map(i => opts[i] || '').join('<br>');

    if (correctEl) {
      correctEl.innerHTML = ''; 
      const labelSpan = document.createElement('span');
      labelSpan.style.fontSize = '1.2em';
      labelSpan.style.fontWeight = 'bold';
      labelSpan.style.marginRight = '8px';
      labelSpan.textContent = correctLabels;
      const br = document.createElement('br');
      const textSpan = document.createElement('span');
      textSpan.style.fontSize = '0.9em';
      textSpan.style.color = '#555';
      textSpan.innerHTML = correctTextFull; 
      correctEl.appendChild(labelSpan);
      correctEl.appendChild(br);
      correctEl.appendChild(textSpan);
    }

    if (explainEl) {
      explainEl.textContent = q.explanation || '（解説データがありません）';
    }
    if (feedbackEl) {
      feedbackEl.classList.remove('hidden');
    }
    
    if (submitBtn) {
      if (current < sessionQuestions.length - 1) {
        submitBtn.textContent = '次の問題へ';
      } else {
        submitBtn.textContent = '結果を見る';
      }
    }

    isAnswerChecked = true;
    inputs.forEach(i => i.disabled = true);

  } catch (e) {
    console.error('Submit Error:', e);
    alert('回答処理中にエラーが発生しました。\n詳細: ' + e.message);
  }
}

function startWithFilters() {
  const btn = document.getElementById('startBtn');
  const originalText = btn.textContent;
  
  try {
    btn.textContent = '読み込み中...';
    btn.disabled = true;

    current = 0; 
    correctCount = 0; 
    tempDetails = [];
    const cond = getCurrentConditionsFromUI();
    
    loadQuestionsByIndex(cond).then(raw => {
      if (!raw || !raw.length) { 
        alert('条件に合う問題が見つかりませんでした。'); 
        return; 
      }
      
      const filtered = raw.filter(q => matchesQuestion(q, cond));
      if (!filtered.length) { 
        alert('選択された条件に合致する問題がありませんでした。\n（お気に入りがない、または計算問題がないカテゴリかもしれません）'); 
        return; 
      }

      const shuffledAll = shuffleArray(filtered);
      sessionQuestions = shuffledAll.slice(0, numToAsk);
      sessionQuestions = sessionQuestions.map(q => randomizeQuestionOptions(q));

      showRoute('quiz');
      renderQuestions(sessionQuestions);
      
      const scoreEl = document.getElementById('score');
      if (scoreEl) scoreEl.textContent = '0';
    }).finally(() => {
      btn.textContent = originalText;
      btn.disabled = false;
    });

  } catch (e) {
    console.error('Start Error:', e);
    alert('問題の読み込みに失敗しました。');
    btn.textContent = originalText;
    btn.disabled = false;
  }
}

function getCurrentConditionsFromUI() {
  const f = collectFilters();
  const calcOnly = document.getElementById('calcOnlyMode')?.checked || false;
  // ★追加: お気に入りチェック
  const favOnly = document.getElementById('favOnlyMode')?.checked || false;

  const cond = {
    chapters: f.chapters, 
    categories: f.cats,
    klevels: f.levels,
    calcOnly: calcOnly,
    favOnly: favOnly, // 渡す
  };
  const countEl = document.getElementById('numSelect'); 
  if (countEl && countEl.value) {
    numToAsk = parseInt(countEl.value, 10);
  }
  return cond;
}

function finishSession() {
  const user = getActiveUserId();
  saveHistory(user, { 
    correct: correctCount, 
    total: sessionQuestions.length, 
    ts: Date.now(), 
    details: tempDetails 
  });
  
  showRoute('results');
  
  const finalCorrect = document.getElementById('finalCorrect');
  const totalQuestions = document.getElementById('totalQuestions');
  const finalRate = document.getElementById('finalRate');
  const msgEl = document.getElementById('passFailMessage');
  
  const rate = totalQuestions ? Math.round((correctCount / sessionQuestions.length) * 100) : 0;

  if (finalCorrect) finalCorrect.textContent = correctCount;
  if (totalQuestions) totalQuestions.textContent = sessionQuestions.length;
  if (finalRate) finalRate.textContent = rate;
  
  if (msgEl) {
    if (rate >= 65) {
      msgEl.textContent = "おめでとう！この調子でがんばりましょう！";
      msgEl.className = "result-message pass-msg";
    } else {
      msgEl.textContent = "ざんねん…間違えた箇所の復習をしましょう";
      msgEl.className = "result-message fail-msg";
    }
  }
  
  renderDashboard();
  drawResultCharts(tempDetails, 'chapterChart', 'kChart');
}

function drawResultCharts(sourceData, chapterCanvasId, kLevelCanvasId) {
  if (typeof Chart === 'undefined') {
    console.warn('Chart.js is not loaded.');
    return;
  }

  const chapterStats = {};
  const kLevelStats = {};

  sourceData.forEach(d => {
    const ch = d.chapter || '未分類';
    if (!chapterStats[ch]) chapterStats[ch] = { total: 0, correct: 0 };
    chapterStats[ch].total++;
    if (d.correct) chapterStats[ch].correct++;

    const lvl = d.klevel || '不明';
    if (!kLevelStats[lvl]) kLevelStats[lvl] = { total: 0, correct: 0 };
    kLevelStats[lvl].total++;
    if (d.correct) kLevelStats[lvl].correct++;
  });

  const draw = (canvasId, statsObj, labelText, instanceVar) => {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;
    if (instanceVar) instanceVar.destroy();

    const labels = Object.keys(statsObj);
    const data = labels.map(k => {
      const s = statsObj[k];
      return s.total === 0 ? 0 : Math.round((s.correct / s.total) * 100);
    });

    return new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: labelText + ' 正答率 (%)',
          data: data,
          backgroundColor: 'rgba(43, 87, 151, 0.6)',
          borderColor: 'rgba(43, 87, 151, 1)',
          borderWidth: 1
        }]
      },
      options: {
        scales: { y: { beginAtZero: true, max: 100 } },
        responsive: true
      }
    });
  };

  if (chapterCanvasId === 'chapterChart') {
    chartChapter = draw(chapterCanvasId, chapterStats, '章別', chartChapter);
    chartKLevel = draw(kLevelCanvasId, kLevelStats, 'Kレベル別', chartKLevel);
  } else {
    dbChartChapter = draw(chapterCanvasId, chapterStats, '章別 (累計)', dbChartChapter);
    dbChartKLevel = draw(kLevelCanvasId, kLevelStats, 'Kレベル別 (累計)', dbChartKLevel);
  }
}

function renderDashboard() {
  const user = getActiveUserId();
  const hist = getHistory(user);
  
  const listEl = document.getElementById('historyList');
  if (listEl) {
    listEl.innerHTML = '';
    hist.forEach((h, idx) => {
      const li = document.createElement('li');
      const dateStr = new Date(h.ts).toLocaleString();
      li.textContent = (idx + 1) + '. 正答 ' + h.correct + '/' + h.total + ' - ' + dateStr;
      listEl.appendChild(li);
    });
  }

  let totalAns = 0;
  let totalCor = 0;
  let allDetails = [];

  hist.forEach(h => {
    const t = h.total || 0;
    const c = h.correct || 0;
    totalAns += t;
    totalCor += c;
    if (h.details) {
      allDetails = allDetails.concat(h.details);
    }
  });

  const elAns = document.getElementById('totalAnswered');
  const elCor = document.getElementById('totalCorrect');
  const elRate = document.getElementById('totalRate');
  
  if (elAns) elAns.textContent = totalAns;
  if (elCor) elCor.textContent = totalCor;
  if (elRate) {
    const r = totalAns === 0 ? 0 : Math.round((totalCor / totalAns) * 100);
    elRate.textContent = r;
  }

  const chStats = {};
  allDetails.forEach(d => {
    const ch = d.chapter || '未分類';
    if (!chStats[ch]) chStats[ch] = { t: 0, c: 0 };
    chStats[ch].t++;
    if (d.correct) chStats[ch].c++;
  });
  
  const weakList = Object.keys(chStats).map(k => {
    return {
      name: k,
      rate: chStats[k].t === 0 ? 0 : (chStats[k].c / chStats[k].t) * 100
    };
  }).sort((a, b) => a.rate - b.rate);

  const weakEl = document.getElementById('weakAreas');
  if (weakEl) {
    weakEl.innerHTML = '';
    if (weakList.length === 0) {
      weakEl.textContent = "データなし";
    } else {
      weakList.slice(0, 3).forEach(w => {
        const li = document.createElement('li');
        li.textContent = `${w.name} (${Math.round(w.rate)}%)`;
        weakEl.appendChild(li);
      });
    }
  }

  if (allDetails.length > 0) {
    drawResultCharts(allDetails, 'chapterChartAll', 'kChartAll');
  }
}

function restart() { 
  startWithFilters(); 
}

function goHome() { 
  showRoute('home'); 
}