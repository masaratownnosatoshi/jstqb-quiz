/*!
 * JSTQB ALTM v3.0 模擬試験（拡張版） — 修正版v2
 * 対応: ABCラベル表示 / シナリオ改行 / 正解の記号表示
 */

// ====== 初期化・状態 ======
let allQuestions = [];        
let sessionQuestions = [];    
let current = 0;
let correctCount = 0;
let isAnswerChecked = false;

const stats = { chapter: new Map(), klevel: new Map() }; 
let userName = '';             
let adaptiveMode = false;      
let numToAsk = 30;             
let tempDetails = [];          

// ABCラベル用の配列
const OPTION_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];

document.addEventListener('DOMContentLoaded', async () => {
  showRoute(location.hash.replace('#', '') || 'home');
  onClick('#startBtn', startWithFilters);   
  onClick('#submitBtn', submitAnswer);
  onClick('#restartBtn', restart);
  onClick('#goHomeBtn', goHome);

  window.addEventListener('hashchange', () => {
    const r = location.hash.replace('#', '') || 'home';
    showRoute(r);
    if (r === 'dashboard') renderDashboard();
  });

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

function eqSetCompat(selectedArr, answerValue) {
  const bArr = Array.isArray(answerValue) ? answerValue : [answerValue];
  // 配列の中身が文字列でも数値でも比較できるように
  if (selectedArr.length !== bArr.length) return false;
  const a = new Set(selectedArr.map(String));
  const b = new Set(bArr.map(String));
  for (const v of a) if (!b.has(v)) return false;
  return true;
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

// ====== 履歴・DB関連（省略なし） ======
function pushTempDetail(qid, ok) { tempDetails.push({ id: qid, correct: !!ok }); }
function getHistory(user) { const key = `altm_history_${user || 'guest'}`; const raw = localStorage.getItem(key); return raw ? JSON.parse(raw) : []; }
function saveHistory(user, session) { const key = `altm_history_${user || 'guest'}`; const h = getHistory(user); h.unshift(session); if (h.length > 100) h.length = 100; localStorage.setItem(key, JSON.stringify(h)); }

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
  const { ok, json } = await fetchJSON('questions/index.json');
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

async function loadQuestionsByIndex(conditions = {}) {
  const idxChunks = await loadManifest();
  if (!idxChunks) return []; // マニフェスト必須
  
  let targetChunks = idxChunks.filter(c => {
    const chOK = !conditions.chapter  || c.chapter === conditions.chapter;
    const catOK = !conditions.category || c.category === conditions.category;
    return chOK && catOK;
  });
  if (!targetChunks.length) targetChunks = idxChunks;

  const all = [];
  for (const c of targetChunks) {
    const part = await loadChunk(c.path);
    if (!Array.isArray(part)) continue;
    all.push(...part);
  }
  return all;
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
    alert('問題がありません。');
    return;
  }
  
  // リセット
  isAnswerChecked = false;
  if (feedbackEl) feedbackEl.classList.add('hidden');
  if (submitBtn) {
    submitBtn.textContent = '回答する';
    submitBtn.disabled = false;
  }

  // メタ情報
  if (idxEl) idxEl.textContent = `${current + 1} / ${questions.length}`;
  if (chapterEl) chapterEl.textContent = q.chapter || '';
  if (levelEl) levelEl.textContent = q.klevel || q.level || '';
  if (textEl) textEl.textContent = q.question || q.text || q.title || '(問題文)';

  // 選択肢生成 (ABC対応)
  if (choicesEl) {
    choicesEl.innerHTML = '';
    const opts = Array.isArray(q.options) ? q.options : (Array.isArray(q.choices) ? q.choices : []);
    const isMulti = q.multi || q.type === '複数選択';

    opts.forEach((optText, i) => {
      const div = document.createElement('div');
      div.style.padding = '8px 0';
      
      const label = document.createElement('label');
      label.style.display = 'flex';
      label.style.alignItems = 'center'; // 上揃えではなく中央揃え（複数行の場合は調整可）
      label.style.cursor = 'pointer';

      // 隠しラジオ/チェックボックス
      const input = document.createElement('input');
      input.type = isMulti ? 'checkbox' : 'radio';
      input.name = 'answer';
      input.value = String(i);
      input.style.display = 'none'; // デザインされたタグを使うので隠す

      // ABCタグ
      const tagSpan = document.createElement('span');
      tagSpan.className = 'option-tag';
      tagSpan.textContent = OPTION_LABELS[i] || '?';

      // 選択肢テキスト
      const textSpan = document.createElement('span');
      textSpan.className = 'option-content'; // CSSで選択時のスタイル当てる用
      textSpan.textContent = optText;
      textSpan.style.flex = '1';

      // 構成: [Input(Hidden)] [Label: [Tag(A)] [Text] ]
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
  const q = sessionQuestions[current];
  if (!q) return;

  const feedbackEl = document.getElementById('