/*!
 * JSTQB ALTM v3.0 模擬試験（拡張版） — GitHub Pages対応版
 * 修正版：選択肢順序修正、解説表示機能追加
 */

// ====== 初期化・状態 ======
let allQuestions = [];        
let sessionQuestions = [];    
let current = 0;
let correctCount = 0;
let isAnswerChecked = false; // 解説表示中かどうか

const stats = { chapter: new Map(), klevel: new Map() }; 
let userName = '';             
let adaptiveMode = false;      
let numToAsk = 30;             
let tempDetails = [];          

document.addEventListener('DOMContentLoaded', async () => {
  // ルーター初期表示
  showRoute(location.hash.replace('#', '') || 'home');

  // イベント配線
  onClick('#startBtn', startWithFilters);   
  onClick('#submitBtn', submitAnswer);
  onClick('#restartBtn', restart);
  onClick('#goHomeBtn', goHome);
  
  // prev/nextボタンはロジック変更に伴い今回は未使用（必要なら復活可）
  // onClick('#prevBtn', prev);
  // onClick('#nextBtn', next);

  // ハッシュルーター
  window.addEventListener('hashchange', () => {
    const r = location.hash.replace('#', '') || 'home';
    showRoute(r);
    if (r === 'dashboard') renderDashboard();
  });

  // 匿名ID表示
  const anonEl = document.getElementById('anonIdLabel');
  if (anonEl) anonEl.textContent = getActiveUserId();
});

// ====== ルーター ======
function showRoute(route) {
  document.querySelectorAll('section[data-route]').forEach(sec => {
    sec.classList.toggle('hidden', sec.getAttribute('data-route') !== route);
  });
  const meta = document.getElementById('meta');
  if (meta) meta.classList.toggle('hidden', route !== 'quiz');
  location.hash = `#${route}`;
}

// ====== ユーティリティ ======
function onClick(sel, fn) {
  const el = document.querySelector(sel);
  if (el) el.onclick = fn;
}

function createAnonId() { return 'anon-' + Math.random().toString(36).slice(2, 10); }
function getActiveUserId() {
  const input = (document.getElementById('userIdInput')?.value || '').trim();
  const stored = localStorage.getItem('altm_active_user');
  if (input) { localStorage.setItem('altm_active_user', input); return input; }
  if (stored) return stored;
  const anon = createAnonId(); localStorage.setItem('altm_active_user', anon); return anon;
}

function eqSet(aArr, bArr) { 
  if (aArr.length !== bArr.length) return false; 
  const a = new Set(aArr), b = new Set(bArr); 
  for (const v of a) if (!b.has(v)) return false; 
  return true; 
}
function eqSetCompat(selectedArr, answerValue) {
  const bArr = Array.isArray(answerValue) ? answerValue : [answerValue];
  return eqSet(selectedArr, bArr);
}

function reservoirSample(arr, k) {
  const res = [];
  for (let i = 0; i < arr.length; i++) {
    if (i < k) res[i] = arr[i];
    else { const j = Math.floor(Math.random() * (i + 1)); if (j < k) res[j] = arr[i]; }
  }
  return res.slice(0, Math.min(k, arr.length));
}

function resolveRepoUrl(input) {
  const base = new URL(document.baseURI);
  if (/^https?:\/\//i.test(input)) return input;

  if (input.startsWith('/')) {
    const sub = input.replace(/^\//, '');
    const repoPath = base.pathname.replace(/\/$/, '');
    const prefix = repoPath ? `${repoPath}/` : '/';
    return `${base.origin}${prefix}${sub}`;
  }
  return new URL(input, base).href;
}

// ====== 履歴関連 ======
function pushTempDetail(qid, ok) { tempDetails.push({ id: qid, correct: !!ok }); }
function getHistory(user) { const key = `altm_history_${user || 'guest'}`; const raw = localStorage.getItem(key); return raw ? JSON.parse(raw) : []; }
function saveHistory(user, session) { const key = `altm_history_${user || 'guest'}`; const h = getHistory(user); h.unshift(session); if (h.length > 100) h.length = 100; localStorage.setItem(key, JSON.stringify(h)); }

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
      if (!db.objectStoreNames.contains('aggregateHistory')) db.createObjectStore('aggregateHistory');
      if (!db.objectStoreNames.contains('manifest')) db.createObjectStore('manifest');
    };
    req.onsuccess = () => { _db = req.result; resolve(_db); };
    req.onerror = () => reject(req.error);
  });
}
async function idbGet(store, key) { if (!_db) await openDb(); return new Promise((resolve, reject)=>{ const tx=_db.transaction(store,'readonly'); const os=tx.objectStore(store); const rq=os.get(key); rq.onsuccess=()=>resolve(rq.result||null); rq.onerror=()=>reject(rq.error); }); }
async function idbPut(store, key, value) { if (!_db) await openDb(); return new Promise((resolve, reject)=>{ const tx=_db.transaction(store,'readwrite'); const os=tx.objectStore(store); const rq=os.put(value, key); rq.onsuccess=()=>resolve(true); rq.onerror=()=>reject(rq.error); }); }

// ====== データ取得 ======
async function fetchJSON(inputUrl) {
  const finalUrl = resolveRepoUrl(inputUrl);
  try {
    const res = await fetch(finalUrl, { cache: 'no-store' });
    if (res.status === 404) return { ok: false, status: 404, json: null, url: finalUrl };
    if (!res.ok) return { ok: false, status: res.status, json: null, url: finalUrl };
    const json = await res.json();
    return { ok: true, status: 200, json, url: finalUrl };
  } catch (e) {
    console.error('[json] fetch error', inputUrl, e);
    return { ok: false, status: 0, json: null, url: finalUrl };
  }
}

async function loadManifest() {
  const cached = await idbGet('manifest', 'index');
  if (cached && Array.isArray(cached.chunks)) return cached.chunks;

  const { ok, status, json } = await fetchJSON('questions/index.json');
  if (!ok) return null;
  
  const chunks = Array.isArray(json?.chunks) ? json.chunks : (Array.isArray(json) ? json : []);
  await idbPut('manifest', 'index', { chunks });
  return chunks;
}

async function loadChunk(path) {
  const cached = await idbGet('questionChunks', path);
  if (cached) return Array.isArray(cached) ? cached : (Array.isArray(cached?.questions) ? cached.questions : []);

  const { ok, json } = await fetchJSON(path);
  if (!ok) return [];
  const arr = Array.isArray(json) ? json : (Array.isArray(json?.questions) ? json.questions : []);
  await idbPut('questionChunks', path, json);
  return arr;
}

async function discoverSequentialChunks(baseDir = '/questions', max = 500, pad = 3) {
  const list = [];
  let consecutive404 = 0;
  const MAX_404 = 10;
  for (let i = 1; i <= max; i++) {
    const num = String(i).padStart(pad, '0');
    const rel = `${baseDir.replace(/^\//, '')}/chunk-${num}.json`;
    const path = resolveRepoUrl(rel);
    try {
      const head = await fetch(path, { method: 'GET', cache: 'no-store' });
      if (head.status === 404) {
        consecutive404++;
        if (consecutive404 >= MAX_404) break;
        continue;
      }
      if (!head.ok) continue;
      list.push({ path: `/${rel}` });
      consecutive404 = 0;
    } catch (e) {
      console.warn('[discover] error', path, e);
    }
  }
  return list;
}

function collectFilters() {
  const chapters = [...document.querySelectorAll('.chapterFilter:checked')].map(i => i.value);
  const levels   = [...document.querySelectorAll('.levelFilter:checked')].map(i => i.value);
  const cats     = [...document.querySelectorAll('.categoryFilter:checked')].map(i => i.value);
  return { chapters, levels, cats };
}

function matchesQuestion(q, cond) {
  const chOK = !cond.chapter || String(q.chapter) === String(cond.chapter) || (q.chapter||'').trim() === (cond.chapter||'').trim();
  const catOK = !cond.category || (q.category||'').trim() === (cond.category||'').trim();
  const kOK  = !cond.klevel || (q.klevel||'').trim() === (cond.klevel||'').trim();
  return chOK && catOK && kOK;
}
function filterQuestions(questions, cond) {
  const filtered = questions.filter(q => matchesQuestion(q, cond));
  if (filtered.length) return filtered;
  if (cond.chapter) {
    const relaxed = questions.filter(q => String(q.chapter) === String(cond.chapter));
    if (relaxed.length) return relaxed;
  }
  return questions;
}

async function loadQuestionsByIndex(conditions = {}) {
  const idxChunks = await loadManifest();
  let targetChunks = [];

  if (Array.isArray(idxChunks) && idxChunks.length) {
    targetChunks = idxChunks.filter(c => {
      const chOK = !conditions.chapter  || c.chapter === conditions.chapter;
      const catOK = !conditions.category || c.category === conditions.category;
      return chOK && catOK;
    });
    if (!targetChunks.length) targetChunks = idxChunks;
  } else {
    targetChunks = await discoverSequentialChunks('/questions', 500, 3);
  }

  const all = [];
  for (const c of targetChunks) {
    const part = await loadChunk(c.path);
    if (!Array.isArray(part)) continue;
    all.push(...part);
  }
  return all;
}

// ====== セッション & UI ======
function getCurrentConditionsFromUI() {
  const f = collectFilters();
  const cond = {
    chapter: f.chapters[0] || null,
    category: f.cats[0] || null,
    klevel: f.levels[0] || null,
  };
  const countEl = document.getElementById('numSelect'); // 修正: ID合わせ
  if (countEl && countEl.value) {
    const n = parseInt(countEl.value, 10);
    if (!Number.isNaN(n) && n > 0) numToAsk = n;
  }
  return cond;
}

function showError(msg) {
  alert(msg);
}
function clearMessage() {
  // 必要ならエラーメッセージエリアを消す処理
}

// === 問題描画（修正版） ===
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
    showError('問題がありません。');
    return;
  }
  
  // 画面状態のリセット
  isAnswerChecked = false;
  if (feedbackEl) feedbackEl.classList.add('hidden');
  if (submitBtn) {
    submitBtn.textContent = '回答する';
    submitBtn.disabled = false;
  }

  // メタ情報
  if (idxEl) idxEl.textContent = `${current + 1} / ${questions.length}`;
  if (chapterEl) chapterEl.textContent = q.chapter || '';
  if (levelEl) levelEl.textContent = q.klevel || '';

  // 問題文
  if (textEl) textEl.textContent = q.text || q.title || '(問題文)';

  // 選択肢生成
  if (choicesEl) {
    choicesEl.innerHTML = '';
    const opts = Array.isArray(q.options) ? q.options : (Array.isArray(q.choices) ? q.choices : []);
    
    opts.forEach((optText, i) => {
      const div = document.createElement('div');
      div.style.padding = '8px 0';
      
      const label = document.createElement('label');
      label.style.display = 'flex';
      label.style.alignItems = 'center';
      label.style.cursor = 'pointer';

      const input = document.createElement('input');
      input.type = q.multi ? 'checkbox' : 'radio';
      input.name = 'answer';
      input.value = String(i);
      input.style.marginRight = '10px';

      const span = document.createElement('span');
      span.textContent = optText;

      label.appendChild(input);
      label.appendChild(span);
      div.appendChild(label);
      choicesEl.appendChild(div);
    });
  }
}

function renderDashboard() {
  const user = getActiveUserId();
  const hist = getHistory(user);
  const listEl = document.getElementById('historyList');
  if (!listEl) return;
  listEl.innerHTML = '';
  hist.forEach((h, idx) => {
    const li = document.createElement('li');
    li.textContent = `${idx + 1}. 正答 ${h.correct}/${h.total} - ${new Date(h.ts).toLocaleString()}`;
    listEl.appendChild(li);
  });
  // ※チャート描画ロジックは省略（必要ならChart.jsコードを追加）
}

// ====== クイズ進行 ======
async function startWithFilters() {
  try {
    current = 0;
    correctCount = 0;
    tempDetails = [];

    const cond = getCurrentConditionsFromUI();
    const raw = await loadQuestionsByIndex(cond);

    if (!raw || !raw.length) {
      showError('条件に合致する問題が見つかりません。');
      return;
    }

    const filtered = filterQuestions(raw, cond);
    if (!filtered.length) {
      showError('条件に合致する問題がありません。');
      return;
    }

    sessionQuestions = reservoirSample(filtered, numToAsk);
    showRoute('quiz');
    renderQuestions(sessionQuestions);
    
    // スコア初期化
    const scoreEl = document.getElementById('score');
    if (scoreEl) scoreEl.textContent = '0';

  } catch (e) {
    console.error(e);
    showError('データ読み込みエラー');
  }
}

function getSelectedAnswers() {
  const inputs = [...document.querySelectorAll('input[name="answer"]')];
  const selected = inputs.filter(i => i.checked).map(i => parseInt(i.value, 10));
  return selected;
}

// === 回答・解説ロジック（修正版） ===
function submitAnswer() {
  const q = sessionQuestions[current];
  if (!q) return;

  const feedbackEl = document.getElementById('feedback');
  const correctEl = document.getElementById('correctAnswer');
  const explainEl = document.getElementById('explanation');
  const judgeEl = document.getElementById('judgeResult');
  const submitBtn = document.getElementById('submitBtn');
  const scoreEl = document.getElementById('score');

  // 【A】解説表示中なら「次へ」
  if (isAnswerChecked) {
    if (current < sessionQuestions.length - 1) {
      current++;
      renderQuestions(sessionQuestions);
    } else {
      finishSession();
    }
    return;
  }

  // 【B】回答判定
  const selected = getSelectedAnswers();
  if (selected.length === 0) {
    alert('選択肢を選んでください');
    return;
  }

  const correctIndices = Array.isArray(q.correctIndices)
    ? q.correctIndices
    : (Array.isArray(q.answer) ? q.answer : [q.answer]).map(v => parseInt(v, 10));

  const ok = eqSetCompat(selected, correctIndices);
  pushTempDetail(q.id || current, ok);
  
  if (ok) {
    correctCount++;
    if (scoreEl) scoreEl.textContent = correctCount;
  }

  // 集計
  if (q.chapter) stats.chapter.set(q.chapter, (stats.chapter.get(q.chapter) || 0) + (ok ? 1 : 0));
  if (q.klevel) stats.klevel.set(q.klevel, (stats.klevel.get(q.klevel) || 0) + (ok ? 1 : 0));

  // --- 解説表示 ---
  if (judgeEl) {
    if (ok) {
      judgeEl.textContent = '正解！';
      judgeEl.className = 'judge-correct'; // CSS用クラス
    } else {
      judgeEl.textContent = 'ざんねん…';
      judgeEl.className = 'judge-incorrect';
    }
  }

  // 正解テキスト
  const opts = Array.isArray(q.options) ? q.options : (Array.isArray(q.choices) ? q.choices : []);
  const correctText = correctIndices.map(i => opts[i]).join(', ');
  if (correctEl) correctEl.textContent = correctText;

  // 解説文
  if (explainEl) explainEl.textContent = q.explanation || '（解説データがありません）';

  // UI更新
  if (feedbackEl) feedbackEl.classList.remove('hidden');
  
  if (submitBtn) {
    if (current < sessionQuestions.length - 1) {
      submitBtn.textContent = '次の問題へ';
    } else {
      submitBtn.textContent = '結果を見る';
    }
  }

  // ロック
  isAnswerChecked = true;
  document.querySelectorAll('input[name="answer"]').forEach(i => i.disabled = true);
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
  
  // 結果画面の描画
  document.getElementById('finalCorrect').textContent = correctCount;
  document.getElementById('totalQuestions').textContent = sessionQuestions.length;
  document.getElementById('finalRate').textContent = Math.round((correctCount / sessionQuestions.length) * 100);
  
  renderDashboard(); // グラフ更新等はDashboard側で代用（簡易実装）
}

function restart() {
  startWithFilters();
}

function goHome() {
  showRoute('home');
}