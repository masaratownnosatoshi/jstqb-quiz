
// app.js start
/*!
 * JSTQB ALTM v3.0 模擬試験（拡張版）
 * - /questions フォルダからチャンクを統合読み込み
 *   1) /questions/index.json（マニフェスト）を優先
 *   2) なければ /questions/chunk-001.json から連番探索（404が続いたら打ち切り）
 * - IndexedDBにチャンク/マニフェストをキャッシュ
 * - フィルタ（章/Kレベル/カテゴリ）
 * - 弱点優先モード（カテゴリ+章+Kレベルの合成重み）
 * - 履歴の保存（localStorage）＆ダッシュボード
 * - Chart.js で棒グラフ
 */

// ====== 初期化・状態 ======
let allQuestions = [];        // 参考：全問題（チャンク統合）
let sessionQuestions = [];    // 今回の出題セット（フィルタ・サンプル後）
let current = 0;
let correctCount = 0;

const stats = { chapter: new Map(), klevel: new Map() }; // セッション集計
let userName = '';             // ユーザー名（localStorageキー）
let adaptiveMode = false;      // 弱点優先モード（未使用時はfalseのまま）
let numToAsk = 30;             // 出題数（UI選択）
let tempDetails = [];          // { id, correct } — セッション詳細

document.addEventListener('DOMContentLoaded', async () => {
  // ルーター初期表示
  showRoute(location.hash.replace('#', '') || 'home');

  // イベント配線
  const startBtn   = document.getElementById('startBtn');
  const prevBtn    = document.getElementById('prevBtn');
  const nextBtn    = document.getElementById('nextBtn');
  const submitBtn  = document.getElementById('submitBtn');
  const restartBtn = document.getElementById('restartBtn');
  const gh         = document.getElementById('goHomeBtn');

  if (startBtn)  startBtn.onclick  = startWithFilters; // async版
  if (prevBtn)   prevBtn.onclick   = prev;
  if (nextBtn)   nextBtn.onclick   = next;
  if (submitBtn) submitBtn.onclick = submitAnswer;
  if (restartBtn)restartBtn.onclick= restart;
  if (gh)        gh.onclick        = goHome;

  // ハッシュルーター
  window.addEventListener('hashchange', () => {
    const r = location.hash.replace('#', '') || 'home';
    showRoute(r);
    if (r === 'dashboard') renderDashboard();
  });

  // 匿名ID表示（ダッシュボード）
  const anonLabel = document.getElementById('anonIdLabel');
  if (anonLabel) anonLabel.textContent = getActiveUserId();

  // 必要UIがなければ生成（最低限動作保証）
  ensureQuizUI();
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

// 匿名ID生成と取得（未入力ならanon）
function createAnonId() { return 'anon-' + Math.random().toString(36).slice(2, 10); }
function getActiveUserId() {
  const input = (document.getElementById('userIdInput')?.value || '').trim();
  const stored = localStorage.getItem('altm_active_user');
  if (input) { localStorage.setItem('altm_active_user', input); return input; }
  if (stored) return stored;
  const anon = createAnonId(); localStorage.setItem('altm_active_user', anon); return anon;
}

// ====== ユーティリティ ======
function eqSet(aArr, bArr) { if (aArr.length !== bArr.length) return false; const a = new Set(aArr), b = new Set(bArr); for (const v of a) if (!b.has(v)) return false; return true; }
// 後方互換：answerが配列/文字列どちらでもOK
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

  // 相対指定（index.json 内で path が "/questions/..." でも fetchJSON が補正）
  const { ok, status, json } = await fetchJSON('questions/index.json');
  if (!ok) {
    if (status !== 404) console.warn('[manifest] 取得失敗', status);
    return null; // 連番フォールバックへ
  }
  // 形式柔軟化：{chunks:[...]} or 直接配列
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

// ====== データ統合 & 問題生成 ======
function normalizeStr(v) { return typeof v === 'string' ? v.trim() : v; }
function matchQuestion(q, cond) {
  const ch = normalizeStr(q.chapter ?? q.Chapter ?? q.章);
  const kl = normalizeStr(q.klevel ?? q.kLevel ?? q.K ?? q.Kレベル);
  const ct = normalizeStr(q.category ?? q.Category ?? q.カテゴリ);

  const wantCh = cond.chapters?.length ? cond.chapters.map(normalizeStr) : null;
  const wantKl = cond.levels?.length   ? cond.levels.map(normalizeStr)   : null;
  const wantCt = cond.cats?.length     ? cond.cats.map(normalizeStr)     : null;

  const chOK = !wantCh || (ch && wantCh.includes(ch));
  const klOK = !wantKl || (kl && wantKl.includes(kl));
  const ctOK = !wantCt || (ct && wantCt.includes(ct));

  return chOK && klOK && ctOK;
}

// index.json（chunks）を条件で前フィルタし、必要チャンクのみ取得
async function loadQuestionsByIndex(conditions = {}) {
  let manifest = await loadManifest();

  // マニフェストがない場合は連番探索
  if (!manifest || !Array.isArray(manifest) || manifest.length === 0) {
    console.warn('[manifest] なし。連番探索に切り替えます。');
    manifest = await discoverSequentialChunks('/questions', 200, 3);
  }

  // chunks: [{ path, chapter, category }, ...] を条件で前フィルタ
  const filteredChunks = Array.isArray(manifest) ? manifest.filter(ch => {
    const chOK = !conditions.chapters?.length || (ch.chapter && conditions.chapters.includes(ch.chapter));
    const ctOK = !conditions.cats?.length     || (ch.category && conditions.cats.includes(ch.category));
    return chOK && ctOK;
  }) : [];

  const targetChunks = filteredChunks.length ? filteredChunks : manifest;

  // チャンク取得＆統合
  const all = [];
  for (const c of targetChunks) {
    const path = c.path || c; // 連番探索の場合は {path} ではなく string の可能性に対応
    const arr = await loadChunk(path);
    if (Array.isArray(arr)) all.push(...arr);
  }

  // 全件を保持（フォールバックに使う）
  allQuestions = all.slice();

  // 問題側の詳細フィルタ適用
  const after = all.filter(q => matchQuestion(q, conditions));

  return after.length ? after : all; // ゼロ件なら全件へフォールバック
}

// ====== セッション生成・レンダリング ======
function ensureQuizUI() {
  const meta = document.getElementById('meta');
  if (!meta) return;

  // 既存要素がなければ生成（最低限）
  if (!document.getElementById('questionText')) {
    const qt = document.createElement('div');
    qt.id = 'questionText';
    qt.style.margin = '0.5rem 0';
    meta.appendChild(qt);
  }
  if (!document.getElementById('choices')) {
    const ch = document.createElement('div');
    ch.id = 'choices';
    meta.appendChild(ch);
  }
  if (!document.getElementById('message')) {
    const ms = document.createElement('div');
    ms.id = 'message';
    ms.style.color = '#b00';
    ms.style.marginTop = '0.5rem';
    meta.appendChild(ms);
  }
}

function showMessage(text) {
  const el = document.getElementById('message');
  if (el) { el.textContent = text || ''; el.style.display = text ? 'block' : 'none'; }
}

function renderQuestion(idx) {
  const q = sessionQuestions[idx];
  if (!q) { showMessage('問題がありません。フィルタ条件またはデータ配置を確認してください。'); return; }
  showMessage('');

  const qt = document.getElementById('questionText');
  const cs = document.getElementById('choices');

  if (qt) qt.textContent = q.text || q.question || q.title || `Q${idx + 1}`;

  if (cs) {
    cs.innerHTML = '';
    const opts = (
      Array.isArray(q.choices) ? q.choices :
      Array.isArray(q.options) ? q.options :
      Array.isArray(q.answers) ? q.answers.map(a => (typeof a === 'string' ? a : a.text ?? a.label)) :
      []
    );
    // 単一/複数選択の推定（answerが配列なら複数）
    const multi = Array.isArray(q.answer);
    opts.forEach((label, i) => {
      const id = `choice-${idx}-${i}`;
      const w = document.createElement('div');
      w.className = 'choice';
      w.innerHTML = `
        <label for="${id}">
          <input type="${multi ? 'checkbox' : 'radio'}" name="choice-${idx}" id="${id}" value="${i}">
          ${label ?? `選択肢${i+1}`}
        </label>
      `;
      cs.appendChild(w);
    });
  }

  // メタ表示（進捗）
  const meta = document.getElementById('meta');
  if (meta) {
    const progId = 'progressInfo';
    let prog = document.getElementById(progId);
    if (!prog) { prog = document.createElement('div'); prog.id = progId; meta.appendChild(prog); }
    prog.textContent = `問題 ${idx + 1} / ${sessionQuestions.length}　正答: ${correctCount}`;
  }
}

async function startWithFilters() {
  try {
    const f = collectFilters();
    // ここで numToAsk を UI から取得したい場合は適宜調整
    const cond = { chapters: f.chapters, levels: f.levels, cats: f.cats };

    showRoute('quiz');
    showMessage('読み込み中…');
    const data = await loadQuestionsByIndex(cond);
    if (!data || data.length === 0) {
      showMessage('選択条件に合致する問題がありません。index.jsonやquestions配下の配置・パスを確認してください。');
      return;
    }

    // サンプリング（重複なし）
    sessionQuestions = reservoirSample(data, numToAsk);
    current = 0;
    correctCount = 0;
    tempDetails = [];
    stats.chapter.clear();
    stats.klevel.clear();

    showMessage('');
    renderQuestion(current);
  } catch (e) {
    console.error(e);
    showMessage('問題データの読み込みに失敗しました。ネットワークまたはパス設定を確認してください。');
  }
}

function readSelectedAnswers(idx) {
  const multi = Array.isArray(sessionQuestions[idx]?.answer);
  const inputs = [...document.querySelectorAll(`input[name="choice-${idx}"]`)];
  const pickedIdx = inputs.filter(i => i.checked).map(i => Number(i.value));
  // answer の型に合わせて比較しやすい形へ
  if (multi) return pickedIdx;
  return pickedIdx.length ? [pickedIdx[0]] : [];
}

function submitAnswer() {
  const q = sessionQuestions[current];
  if (!q) return;

  const picked = readSelectedAnswers(current);

  // 正答の表現を統一：インデックス配列 or ラベル配列を許容
  let correct;
  if (Array.isArray(q.answer)) {
    correct = q.answer;
  } else if (typeof q.answer === 'number') {
    correct = [q.answer];
  } else if (typeof q.answer === 'string') {
    correct = [q.answer];
  } else {
    correct = []; // 不明な形式
  }

  let ok;
  // もし正答がインデックス配列ならそのまま比較、文字列ならラベル比較
  const opts = Array.isArray(q.choices) ? q.choices :
               Array.isArray(q.options) ? q.options :
               Array.isArray(q.answers) ? q.answers.map(a => (typeof a === 'string' ? a : a.text ?? a.label)) : [];

  if (typeof correct[0] === 'number') {
    ok = eqSetCompat(picked, correct);
  } else {
    const pickedLabels = picked.map(i => opts[i]);
    ok = eqSetCompat(pickedLabels, correct);
  }

  pushTempDetail(q.id ?? q.uuid ?? `${current}`, ok);
  if (ok) correctCount++;

  // 集計（章・Kレベル）
  const ch = normalizeStr(q.chapter ?? q.Chapter ?? q.章);
  const kl = normalizeStr(q.klevel ?? q.kLevel ?? q.K ?? q.Kレベル);
  stats.chapter.set(ch, (stats.chapter.get(ch) || 0) + (ok ? 1 : 0));
  stats.klevel.set(kl, (stats.klevel.get(kl) || 0) + (ok ? 1 : 0));

  next();
}

function next() {
  if (current < sessionQuestions.length - 1) {
    current++;
    renderQuestion(current);
  } else {
    // セッション完了
    const user = getActiveUserId();
    saveHistory(user, {
      date: new Date().toISOString(),
      total: sessionQuestions.length,
      correct: correctCount,
      details: tempDetails.slice(0, 200) // 量を制限
    });
    showRoute('dashboard');
    renderDashboard();
  }
}

function prev() {
  if (current > 0) {
    current--;
    renderQuestion(current);
  }
}

function restart() {
  current = 0;
  correctCount = 0;
  tempDetails = [];
  showRoute('home');
}

function goHome() { showRoute('home'); }

// ====== ダッシュボード（簡易版） ======
function renderDashboard() {
  const user = getActiveUserId();
  const hist = getHistory(user);

  const sec = document.querySelector('section[data-route="dashboard"]') || document.body;
  let box = document.getElementById('dashboardBox');
  if (!box) { box = document.createElement('div'); box.id = 'dashboardBox'; sec.appendChild(box); }

  if (!hist.length) {
    box.innerHTML = '<p>履歴がありません。</p>';
    return;
  }

  const last = hist[0];
  box.innerHTML = `
    <p>最新セッション: ${new Date(last.date).toLocaleString()}</p>
    <p>正答 ${last.correct} / 出題 ${last.total}</p>
  `;
}
