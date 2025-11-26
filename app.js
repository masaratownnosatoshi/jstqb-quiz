/*!
 * JSTQB ALTM v3.0 模擬試験（拡張版） — 修正版v5
 * 対応: フィルタリング時のプロパティ名揺れ吸収 (level / klevel)
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
  // 初期ロード
  let r = location.hash.replace('#', '');
  if (!r) r = 'home';
  showRoute(r);

  onClick('#startBtn', startWithFilters);   
  onClick('#submitBtn', submitAnswer);
  onClick('#restartBtn', restart);
  onClick('#goHomeBtn', goHome);

  window.addEventListener('hashchange', () => {
    let route = location.hash.replace('#', '');
    if (!route) route = 'home';
    showRoute(route);
    if (route === 'dashboard') renderDashboard();
  });

  const anonEl = document.getElementById('anonIdLabel');
  if (anonEl) anonEl.textContent = getActiveUserId();
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

function eqSetCompat(selectedArr, answerValue) {
  // 配列化して比較
  let bArr = Array.isArray(answerValue) ? answerValue : [answerValue];
  
  if (selectedArr.length !== bArr.length) return false;

  // 文字列として比較
  const a = new Set(selectedArr.map(String));
  const b = new Set(bArr.map(String));

  for (const v of a) {
    if (!b.has(v)) return false;
  }
  return true;
}

function reservoirSample(arr, k) {
  const res = [];
  for (let i = 0; i < arr.length; i++) {
    if (i < k) {
      res[i] = arr[i];
    } else {
      const j = Math.floor(Math.random() * (i + 1));
      if (j < k) res[j] = arr[i];
    }
  }
  return res.slice(0, Math.min(k, arr.length));
}

function resolveRepoUrl(input) {
  const base = new URL(document.baseURI);
  // httpから始まる場合はそのまま
  if (/^https?:\/\//i.test(input)) return input;

  // 絶対パス風の指定 (/questions/...)
  if (input.startsWith('/')) {
    const sub = input.replace(/^\//, '');
    const repoPath = base.pathname.replace(/\/$/, '');
    const prefix = repoPath ? (repoPath + '/') : '/';
    return base.origin + prefix + sub;
  }
  // 相対パス
  return new URL(input, base).href;
}

// ====== 履歴・DB関連 ======
function pushTempDetail(qid, ok) {
  tempDetails.push({ id: qid, correct: !!ok });
}

function getHistory(user) {
  const key = 'altm_history_' + (user || 'guest');
  const raw = localStorage.getItem(key);
  return raw ? JSON.parse(raw) : [];
}

function saveHistory(user, session) {
  const key = 'altm_history_' + (user || 'guest');
  const h = getHistory(user);
  h.unshift(session);
  if (h.length > 100) h.length = 100;
  localStorage.setItem(key, JSON.stringify(h));
}

// IndexedDB設定
const DB_NAME = 'ALTM_DB';
const DB_VERSION = 2;
let _db;

function openDb() {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(DB_NAME, DB_VERSION);
    req.onupgradeneeded = (e) => {
      const db = e.target.result;
      if (!db.objectStoreNames.contains('questionChunks')) {
        db.createObjectStore('questionChunks');
      }
      if (!db.objectStoreNames.contains('manifest')) {
        db.createObjectStore('manifest');
      }
    };
    req.onsuccess = () => {
      _db = req.result;
      resolve(_db);
    };
    req.onerror = () => reject(req.error);
  });
}

// DB取得
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

// DB保存
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
    if (res.status === 404) {
      return { ok: false, status: 404, json: null };
    }
    if (!res.ok) {
      return { ok: false, status: res.status, json: null };
    }
    const json = await res.json();
    return { ok: true, status: 200, json: json };
  } catch (e) {
    console.error('[json] fetch error', inputUrl, e);
    return { ok: false, status: 0, json: null };
  }
}

async function loadManifest() {
  // キャッシュ確認
  const cached = await idbGet('manifest', 'index');
  if (cached && cached.chunks && Array.isArray(cached.chunks)) {
    return cached.chunks;
  }

  // 取得
  const result = await fetchJSON('questions/index.json');
  if (!result.ok) return null;

  let chunks = [];
  if (result.json && Array.isArray(result.json.chunks)) {
    chunks = result.json.chunks;
  } else if (Array.isArray(result.json)) {
    chunks = result.json;
  }

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
  if (Array.isArray(result.json)) {
    arr = result.json;
  } else if (result.json && Array.isArray(result.json.questions)) {
    arr = result.json.questions;
  }

  await idbPut('questionChunks', path, result.json);
  return arr;
}

async function loadQuestionsByIndex(conditions) {
  const idxChunks = await loadManifest();
  if (!idxChunks) return [];
  
  // マニフェスト段階でのフィルタリング
  let targetChunks = idxChunks.filter(c => {
    const cond = conditions || {};
    // ※注意: index.jsonには "klevel" がある前提
    const chOK = !cond.chapter  || c.chapter === cond.chapter;
    const catOK = !cond.category || c.category === cond.category;
    // klevelはindex.jsonに無い場合もあるので、あればチェック
    let kOK = true;
    if (cond.klevel && c.klevel) {
       if (c.klevel !== cond.klevel) kOK = false;
    }
    return chOK && catOK && kOK;
  });

  if (targetChunks.length === 0) {
    // 該当なしなら念のため全件ロードして、後で詳細フィルタにかける
    targetChunks = idxChunks;
  }

  const all = [];
  for (const c of targetChunks) {
    const part = await loadChunk(c.path);
    if (Array.isArray(part)) {
      all.push(...part);
    }
  }
  return all;
}

function collectFilters() {
  const chapters = Array.from(document.querySelectorAll('.chapterFilter:checked')).map(i => i.value);
  const levels   = Array.from(document.querySelectorAll('.levelFilter:checked')).map(i => i.value);
  const cats     = Array.from(document.querySelectorAll('.categoryFilter:checked')).map(i => i.value);
  return { chapters, levels, cats };
}

function matchesQuestion(q, cond) {
  // 章の判定
  let chOK = true;
  if (cond.chapter) {
    const qCh = (q.chapter || '').trim();
    const cCh = (cond.chapter || '').trim();
    if (qCh !==