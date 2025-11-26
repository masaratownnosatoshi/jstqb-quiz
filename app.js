
/*!
 * JSTQB ALTM v3.0 模擬試験（拡張版） — GitHub Pages対応版
 * - /questions フォルダからチャンクを統合読み込み
 *   1) /questions/index.json（マニフェスト：{ chunks: [{ path, chapter, category }, ...] }）
 *   2) なければ /questions/chunk-001.json から連番探索（404が続いたら打ち切り）
 * - サブパス安全なURL解決（/jstqb-quiz/ 配下でも /questions/... を正しく解決）
 * - IndexedDBにチャンク/マニフェストをキャッシュ
 * - フィルタ（章/Kレベル/カテゴリ）の正規化＆ゼロ件フォールバック
 * - 履歴の保存（localStorage）＆ダッシュボード
 * - 基本的なクイズ進行（prev/next/submit/restart）
 */

// ====== 初期化・状態 ======
let allQuestions = [];        // 連番フォールバック時や全件読み込み用
let sessionQuestions = [];    // 今回の出題セット（フィルタ・サンプル後）
let current = 0;
let correctCount = 0;

const stats = { chapter: new Map(), klevel: new Map() }; // セッション集計
let userName = '';             // ユーザー名（localStorageキー）
let adaptiveMode = false;      // 弱点優先モード（必要ならUIと連動）
let numToAsk = 30;             // 出題数（UI選択）
let tempDetails = [];          // { id, correct } — セッション詳細

document.addEventListener('DOMContentLoaded', async () => {
  // ルーター初期表示
  showRoute(location.hash.replace('#', '') || 'home');

  // イベント配線
  onClick('#startBtn', startWithFilters);   // async
  onClick('#prevBtn', prev);
  onClick('#nextBtn', next);
  onClick('#submitBtn', submitAnswer);
  onClick('#restartBtn', restart);
  onClick('#goHomeBtn', goHome);

  // ハッシュルーター
  window.addEventListener('hashchange', () => {
    const r = location.hash.replace('#', '') || 'home';
    showRoute(r);
    if (r === 'dashboard') renderDashboard();
  });

  // 匿名ID表示（ダッシュボード）
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

function eqSet(aArr, bArr) { if (aArr.length !== bArr.length) return false; const a = new Set(aArr), b = new Set(bArr); for (const v of a) if (!b.has(v)) return false; return true; }
function eqSetCompat(selectedArr, answerValue) {
  const bArr = Array.isArray(answerValue) ? answerValue : [answerValue];
  return eqSet(selectedArr, bArr);
}

// シャッフル（レザボアは採用済みのため補助として残す）
function reservoirSample(arr, k) {
  const res = [];
  for (let i = 0; i < arr.length; i++) {
    if (i < k) res[i] = arr[i];
    else { const j = Math.floor(Math.random() * (i + 1)); if (j < k) res[j] = arr[i]; }
  }
  return res.slice(0, Math.min(k, arr.length));
}

/**
 * GitHub Pages のサブパス（例: /jstqb-quiz/）でも安全にURLを解決
 * - 入力が "https://..." の完全URLならそのまま
 * - 入力が "/questions/..." の先頭スラッシュで始まる絶対パスなら
 *   オリジン + サブパス配下に補正して返す
 * - 入力が相対パス（"questions/..." や "./..."）なら document.baseURI 基準で解決
 */
function resolveRepoUrl(input) {
  const base = new URL(document.baseURI); // 例: https://masaratownnosatoshi.github.io/jstqb-quiz/
  if (/^https?:\/\//i.test(input)) return input;

  if (input.startsWith('/')) {
    const sub = input.replace(/^\//, ''); // "questions/..."
    const repoPath = base.pathname.replace(/\/$/, ''); // "/jstqb-quiz" または ""
    const prefix = repoPath ? `${repoPath}/` : '/';
    return `${base.origin}${prefix}${sub}`; // → https://.../jstqb-quiz/questions/...
  }
  return new URL(input, base).href;
}

// ====== 履歴関連（localStorage） ======
function pushTempDetail(qid, ok) { tempDetails.push({ id: qid, correct: !!ok }); }
function getHistory(user) { const key = `altm_history_${user || 'guest'}`; const raw = localStorage.getItem(key); return raw ? JSON.parse(raw) : []; }
function saveHistory(user, session) { const key = `altm_history_${user || 'guest'}`; const h = getHistory(user); h.unshift(session); if (h.length > 100) h.length = 100; localStorage.setItem(key, JSON.stringify(h)); }

// ====== IndexedDB（チャンク/マニフェスト/集計） ======
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

// ====== チャンク/マニフェスト読み込み ======
async function fetchJSON(inputUrl) {
  const finalUrl = resolveRepoUrl(inputUrl);
  try {
    const res = await fetch(finalUrl, { cache: 'no-store' });
    if (res.status === 404) {
      console.error('[json] 404 Not Found:', finalUrl);
      return { ok: false, status: 404, json: null, url: finalUrl };
    }
    if (!res.ok) {
      console.error(`[json] HTTP ${res.status}:`, finalUrl);
      return { ok: false, status: res.status, json: null, url: finalUrl };
    }
    try {
      const json = await res.json();
      return { ok: true, status: 200, json, url: finalUrl };
    } catch (e) {
      console.error('[json] parse error', finalUrl, e);
      return { ok: false, status: 0, json: null, url: finalUrl };
    }
  } catch (e) {
    console.error('[json] fetch error', inputUrl, e);
    return { ok: false, status: 0, json: null, url: finalUrl };
  }
}

// マニフェスト：questions/index.json を優先（なければnull）
async function loadManifest() {
  const cached = await idbGet('manifest', 'index');
  if (cached && Array.isArray(cached.chunks)) return cached.chunks;

  // 相対指定（index.json の path が "/questions/..." でも補正される）
  const { ok, status, json } = await fetchJSON('questions/index.json');
  if (!ok) {
    if (status !== 404) console.warn('[manifest] 取得失敗', status);
    return null; // 連番フォールバックへ
  }
  const chunks = Array.isArray(json?.chunks) ? json.chunks
                : (Array.isArray(json) ? json : []);
  await idbPut('manifest', 'index', { chunks });
  return chunks;
}

// チャンクロード：配列 or {questions:[...]} 両対応
async function loadChunk(path) {
  const cached = await idbGet('questionChunks', path);
  if (cached) {
    const arr = Array.isArray(cached) ? cached : (Array.isArray(cached?.questions) ? cached.questions : []);
    return arr;
  }
  const { ok, json, status, url } = await fetchJSON(path);
  if (!ok) {
    if (status !== 404) console.error('[chunk] 取得失敗:', path, status, url);
    return [];
  }
  const arr = Array.isArray(json) ? json : (Array.isArray(json?.questions) ? json.questions : []);
  await idbPut('questionChunks', path, json);
  return arr;
}

// 連番探索（マニフェスト無し時）— 存在するチャンクのリストを作る（サブパス対応）
async function discoverSequentialChunks(baseDir = '/questions', max = 500, pad = 3) {
  const list = [];
  let consecutive404 = 0;
  const MAX_404 = 10;
  for (let i = 1; i <= max; i++) {
    const num = String(i).padStart(pad, '0'); // 001, 002...
    const rel = `${baseDir.replace(/^\//, '')}/chunk-${num}.json`; // "questions/chunk-001.json"
    const path = resolveRepoUrl(rel); // サブパス補正済みの完全URL
    try {
      const head = await fetch(path, { method: 'GET', cache: 'no-store' });
      if (head.status === 404) {
        consecutive404++;
        if (consecutive404 >= MAX_404) break;
        continue;
      }
      if (!head.ok) continue;
      list.push({ path: `/${rel}` }); // 内部では "/questions/chunk-001.json" の形式で保持
      consecutive404 = 0;
    } catch (e) {
      console.warn('[discover] fetch error', path, e);
    }
  }
  return list;
}

// ====== フィルタ取得 ======
function collectFilters() {
  const chapters = [...document.querySelectorAll('.chapterFilter:checked')].map(i => i.value);
  const levels   = [...document.querySelectorAll('.levelFilter:checked')].map(i => i.value);
  const cats     = [...document.querySelectorAll('.categoryFilter:checked')].map(i => i.value);
  return { chapters, levels, cats };
}

// ====== フィルタ正規化＆マッチング ======
function normalizeStr(v) { return typeof v === 'string' ? v.trim() : v; }
function matchesQuestion(q, cond) {
  const chOK = !cond.chapter || String(q.chapter) === String(cond.chapter) || normalizeStr(q.chapter) === normalizeStr(cond.chapter);
  const catOK = !cond.category || normalizeStr(q.category) === normalizeStr(cond.category);
  const kOK  = !cond.klevel || normalizeStr(q.klevel) === normalizeStr(cond.klevel);
  return chOK && catOK && kOK;
}
function filterQuestions(questions, cond) {
  const filtered = questions.filter(q => matchesQuestion(q, cond));
  if (filtered.length) return filtered;

  // ゼロ件なら章のみ、さらにゼロ件なら全件
  if (cond.chapter) {
    const relaxed = questions.filter(q => String(q.chapter) === String(cond.chapter));
    if (relaxed.length) return relaxed;
  }
  return questions;
}

// ====== index.json を活かした条件に応じた読み込み ======
async function loadQuestionsByIndex(conditions = {}) {
  const idxChunks = await loadManifest();
  let targetChunks = [];

  if (Array.isArray(idxChunks) && idxChunks.length) {
    // index.jsonのメタ（chapter/category）で前フィルタ
    targetChunks = idxChunks.filter(c => {
      const chOK = !conditions.chapter  || c.chapter === conditions.chapter;   // 例: "第1章"
      const catOK = !conditions.category || c.category === conditions.category; // 例: "金融"
      return chOK && catOK;
    });
    if (!targetChunks.length) {
      console.warn('[load] 条件に一致するチャンクがありません。条件を緩めて全チャンクへ');
      targetChunks = idxChunks;
    }
  } else {
    console.warn('[load] マニフェストがないため連番探索にフォールバック');
    targetChunks = await discoverSequentialChunks('/questions', 500, 3);
  }

  const all = [];
  for (const c of targetChunks) {
    const part = await loadChunk(c.path);
    if (!Array.isArray(part)) {
      console.warn('[load] JSON形式が配列でないためスキップ:', c.path);
      continue;
    }
    all.push(...part);
  }
  console.log('[load] questions loaded:', all.length);
  return all;
}

// ====== セッション構築 & UI ======
function getCurrentConditionsFromUI() {
  const f = collectFilters();
  // 簡易仕様：UIから複数選択されている場合は先頭のみ採用（必要ならAND/ORに変更）
  const cond = {
    chapter: f.chapters[0] || null,   // "第1章" など
    category: f.cats[0] || null,
    klevel: f.levels[0] || null,
  };
  // 出題数（numToAsk）は必要ならUIから取得
  const countEl = document.getElementById('numToAsk');
  if (countEl && countEl.value) {
    const n = parseInt(countEl.value, 10);
    if (!Number.isNaN(n) && n > 0) numToAsk = n;
  }
  return cond;
}

function showError(msg) {
  const el = document.getElementById('message');
  if (el) {
    el.textContent = msg;
    el.classList.remove('hidden');
  } else {
    alert(msg);
  }
}

function clearMessage() {
  const el = document.getElementById('message');
  if (el) el.classList.add('hidden');
}

// 問題描画（あなたのDOM構造に合わせて必要なら調整）
function renderQuestions(questions) {
  const q = questions[current];
  const textEl = document.getElementById('questionText');
  const choicesEl = document.getElementById('choices');
  const idxEl = document.getElementById('questionIndex');

  if (!q) {
    showError('問題がありません。条件を見直すか、データ配置を確認してください。');
    return;
  }
  clearMessage();

  if (idxEl) idxEl.textContent = `${current + 1} / ${questions.length}`;
  if (textEl) textEl.textContent = q.text || q.title || '(問題文)';
  if (choicesEl) {
    choicesEl.innerHTML = '';
    const opts = Array.isArray(q.options) ? q.options : (Array.isArray(q.choices) ? q.choices : []);
    for (let i = 0; i < opts.length; i++) {
      const li = document.createElement('li');
      const input = document.createElement('input');
      input.type = q.multi ? 'checkbox' : 'radio';
      input.name = 'answer';
      input.value = String(i);
      const label = document.createElement('label');
      label.textContent = opts[i];
      li.appendChild(input);
      li.appendChild(label);
      choicesEl.appendChild(li);
    }
  }
}

function renderDashboard() {
  // 履歴の簡易レンダリング（必要ならChart.js連携）
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
      showError('選択条件に合致する問題がありません。（index.jsonやquestions配下の配置・パスを確認）');
      return;
    }

    // フィルタ（Kレベル等）適用
    const filtered = filterQuestions(raw, cond);
    if (!filtered.length) {
      showError('選択条件に合致する問題がありません。条件を緩めてください。');
      return;
    }

    // 出題セット作成（レザボアサンプリング）
    sessionQuestions = reservoirSample(filtered, numToAsk);

    showRoute('quiz');
    renderQuestions(sessionQuestions);
  } catch (e) {
    console.error(e);
    showError('問題データの読み込みに失敗しました。ネットワークまたはパス設定を確認してください。');
  }
}

function prev() {
  if (current > 0) {
    current--;
    renderQuestions(sessionQuestions);
  }
}

function next() {
  if (current < sessionQuestions.length - 1) {
    current++;
    renderQuestions(sessionQuestions);
  }
}

function getSelectedAnswers() {
  const inputs = [...document.querySelectorAll('input[name="answer"]')];
  const selected = inputs.filter(i => i.checked).map(i => parseInt(i.value, 10));
  return selected;
}

function submitAnswer() {
  const q = sessionQuestions[current];
  if (!q) return;

  const selected = getSelectedAnswers();
  const correctIndices = Array.isArray(q.correctIndices)
    ? q.correctIndices
    : (Array.isArray(q.answer) ? q.answer : [q.answer]).map(v => parseInt(v, 10));

  const ok = eqSetCompat(selected, correctIndices);
  pushTempDetail(q.id || current, ok);
  if (ok) correctCount++;

  // セッション内の簡易集計（章/Kレベル）
  if (q.chapter) stats.chapter.set(q.chapter, (stats.chapter.get(q.chapter) || 0) + (ok ? 1 : 0));
  if (q.klevel) stats.klevel.set(q.klevel, (stats.klevel.get(q.klevel) || 0) + (ok ? 1 : 0));

  // 次へ
  if (current < sessionQuestions.length - 1) {
    current++;
    renderQuestions(sessionQuestions);
  } else {
    finishSession();
  }
}

function finishSession() {
  const user = getActiveUserId();
  saveHistory(user, {
    correct: correctCount,
    total: sessionQuestions.length,
    ts: Date.now(),
    details: tempDetails
  });
  showRoute('dashboard');
  renderDashboard();
}

function restart() {
  // セッション再開（同条件で再作成してクイズへ）
  startWithFilters();
}

function goHome() {
  showRoute('home');
}
