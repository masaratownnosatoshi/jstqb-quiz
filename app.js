/*!
 * JSTQB ALTM v3.0 模擬試験（拡張版） — 修正版v3
 * 対応: シンタックスエラー回避（DOM操作への書き換え）、改行のHTML対応
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

// ====== 履歴・DB関連 ======
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
    const res = await fetch(finalUrl