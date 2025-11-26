
/*!
 * JSTQB ALTM v3.0 模擬試験（拡張版） — GitHub Pages対応 完成版
 * - /questions フォルダからチャンクを統合読み込み
 *   1) /questions/index.json（マニフェスト）を優先
 *   2) なければ /questions/chunk-001.json から連番探索（404が続いたら打ち切り）
 * - IndexedDBにチャンク/マニフェストをキャッシュ
 * - フィルタ（章/Kレベル/カテゴリ）
 * - 弱点優先モード（カテゴリ+章+Kレベルの合成重み）※最低限の骨子を用意
 * - 履歴の保存（localStorage）＆ダッシュボード（Chart.jsがあれば棒グラフ）
 * - GitHub Pages のサブパス（/jstqb-quiz/）に安全対応
 */

/* ===================== 初期化・状態 ===================== */
let allQuestions = [];        // 全問題
let sessionQuestions = [];    // 今回の出題セット
let current = 0;
let correctCount = 0;

const stats = { chapter: new Map(), klevel: new Map() }; // セッション集計
let adaptiveMode = false;      // 弱点優先モード（未使用でも骨子あり）
let numToAsk = 30;             // 出題数（UI選択）
let tempDetails = [];          // { id, correct } — セッション詳細
let _db;                       // IndexedDB ハンドル

document.addEventListener('DOMContentLoaded', async () => {
  // ルーティング初期表示
  showRoute(location.hash.replace('#', '') || 'home');

  // イベント配線
  queryById('startBtn')?.addEventListener('click', startWithFilters); // async版
  queryById('prevBtn')?.addEventListener('click', prev);
  queryById('nextBtn')?.addEventListener('click', next);
  queryById('submitBtn')?.addEventListener('click', submitAnswer);
  queryById('restartBtn')?.addEventListener('click', restart);
  queryById('goHomeBtn')?.addEventListener('click', goHome);

  // ハッシュルーター
  window.addEventListener('hashchange', () => {
    const r = location.hash.replace('#', '') || 'home';
    showRoute(r);
    if (r === 'dashboard') renderDashboard();
  });

  // 匿名ID表示（ダッシュボード）
  const anonEl = queryById('anonIdLabel');
  if (anonEl) anonEl.textContent = getActiveUserId();
});

/* ===================== ルーター ===================== */
function showRoute(route) {
  document.querySelectorAll('section[data-route]').forEach(sec => {
    sec.classList.toggle('hidden', sec.getAttribute('data-route') !== route);
  });
  queryById('meta')?.classList.toggle('hidden', route !== 'quiz');
  if (location.hash !== `#${route}`) location.hash = `#${route}`;
}

/* ===================== DOMユーティリティ ===================== */
function queryById(id) {
  return document.getElementById(id) ||
         document.querySelector(`#${id}`) ||
         document.querySelector(`[data-id="${id}"]`);
}

/* ===================== 匿名ID ===================== */
function createAnonId() { return 'anon-' + Math.random().toString(36).slice(2, 10); }
function getActiveUserId() {
  const input = (queryById('userIdInput')?.value || '').trim();
  const stored = localStorage.getItem('altm_active_user');
  if (input) { localStorage.setItem('altm_active_user', input); return input; }
  if (stored) return stored;
  const anon = createAnonId(); localStorage.setItem('altm_active_user', anon); return anon;
}

/* ===================== 比較ユーティリティ ===================== */
function eqSet(aArr, bArr) { if (aArr.length !== bArr.length) return false; const a = new Set(aArr), b = new Set(bArr); for (const v of a) if (!b.has(v)) return false; return true; }
function eqSetCompat(selectedArr, answerValue) {
  const bArr = Array.isArray(answerValue) ? answerValue : [answerValue];
  return eqSet(selectedArr, bArr);
}

/* ===================== サンプリング ===================== */
function reservoirSample(arr, k) {
  const res = [];
  for (let i = 0; i < arr.length; i++) {
    if (i < k) res[i] = arr[i];
    else { const j = Math.floor(Math.random() * (i + 1)); if (j < k) res[j] = arr[i]; }
  }
  return res.slice(0, Math.min(k, arr.length));
}

/* ===================== GitHub Pages サブパス対応 URL解決 ===================== */
/**
 * - 入力が "https://..." 完全URLならそのまま
 * - 入力が "/questions/..." の絶対パスなら オリジン + サブパス配下に補正
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

/* ===================== 履歴（localStorage） ===================== */
function pushTempDetail(qid, ok) { tempDetails.push({ id: qid ?? String(Math.random()), correct: !!ok }); }
function getHistory(user) { const key = `altm_history_${user || 'guest'}`; const raw = localStorage.getItem(key); return raw ? JSON.parse(raw) : []; }
function saveHistory(user, session) { const key = `altm_history_${user || 'guest'}`; const h = getHistory(user); h.unshift(session); if (h.length > 100) h.length = 100; localStorage.setItem(key, JSON.stringify(h)); }

/* ===================== IndexedDB ===================== */
const DB_NAME = 'ALTM_DB';
const DB_VERSION = 2;
async function openDb() {
  if (_db) return _db;
  _db = await new Promise((resolve, reject) => {
    const req = indexedDB.open(DB_NAME, DB_VERSION);
    req.onupgradeneeded = (e) => {
      const db = e.target.result;
      if (!db.objectStoreNames.contains('questionChunks')) db.createObjectStore('questionChunks');
      if (!db.objectStoreNames.contains('aggregateHistory')) db.createObjectStore('aggregateHistory');
      if (!db.objectStoreNames.contains('manifest')) db.createObjectStore('manifest');
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
  return _db;
}
async function idbGet(store, key) { const db = await openDb(); return new Promise((resolve, reject)=>{ const tx=db.transaction(store,'readonly'); const os=tx.objectStore(store); const rq=os.get(key); rq.onsuccess=()=>resolve(rq.result||null); rq.onerror=()=>reject(rq.error); }); }
async function idbPut(store, key, value) { const db = await openDb(); return new Promise((resolve, reject)=>{ const tx=db.transaction(store,'readwrite'); const os=tx.objectStore(store); const rq=os.put(value, key); rq.onsuccess=()=>resolve(true); rq.onerror=()=>reject(rq.error); }); }

/* ===================== JSONフェッチ（サブパス安全） ===================== */
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

/* ===================== マニフェスト・チャンク ===================== */
// マニフェスト：/questions/index.json を優先（なければ null）
async function loadManifest() {
  const cached = await idbGet('manifest', 'index');
  if (cached && Array.isArray(cached.chunks)) return cached.chunks;

  const { ok, status, json } = await fetchJSON('questions/index.json'); // 相対指定
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
    const path = resolveRepoUrl(rel);
    try {
      const head = await fetch(path, { method: 'GET', cache: 'no-store' });
      if (head.status === 404) {
        consecutive404++;
        if (consecutive404 >= MAX_404) break;
        continue;
      }
      if (!head.ok) continue;
      list.push({ path: `/${rel}` }); // 内部保持は "/questions/chunk-001.json"
      consecutive404 = 0;
    } catch (e) {
      console.warn('[discover] fetch error', path, e);
    }
  }
  return list;
}

/* ===================== UIフィルタ収集 ===================== */
function collectFilters() {
  const chapters = [...document.querySelectorAll('.chapterFilter:checked')].map(i => i.value);
  const levels   = [...document.querySelectorAll('.levelFilter:checked')].map(i => i.value);
  const cats     = [...document.querySelectorAll('.categoryFilter:checked')].map(i => i.value);
  // 出題数（数値UIがあれば拾う）
  const numSel = queryById('numSelect');
  numToAsk = Number(numSel?.value || numToAsk || 30);
  adaptiveMode = !!queryById('adaptiveChk')?.checked;
  return { chapters, levels, cats };
}

/* ===================== 正規化・フィルタロジック ===================== */
function normStr(v) { return typeof v === 'string' ? v.trim() : v; }
function strEq(a, b) { return normStr(a) === normStr(b); }
function inList(value, list) {
  if (!list || list.length === 0) return true; // 条件未指定なら通す
  return list.some(v => strEq(value, v) || String(value) === String(v));
}
function normalizeQuestionShape(q) {
  // 柔軟にフィールド名を合わせる（推測）
  const chapter = q.chapter ?? q.section ?? q.unit ?? q['章'] ?? q['第'] ?? '';
  const category = q.category ?? q.domain ?? q['カテゴリ'] ?? q['カテゴリー'] ?? '';
  const klevel = q.klevel ?? q.kLevel ?? q.k ?? q['K'] ?? '';
  const id = q.id ?? q.qid ?? q.key ?? `${chapter}:${(q.question || q.text || q.stem || '').slice(0,20)}:${Math.random().toString(36).slice(2,6)}`;
  const text = q.question ?? q.text ?? q.stem ?? q['問題'] ?? '';
  const options = q.options ?? q.choices ?? q['選択肢'] ?? [];
  const answer = q.answer ?? q.answers ?? q['正解'] ?? [];
  const multi = Array.isArray(answer);
  const explanation = q.explanation ?? q.explain ?? q['解説'] ?? '';
  return { ...q, id, chapter, category, klevel, text, options, answer, multi, explanation };
}

function filterQuestionsCore(questions, cond) {
  // 章・カテゴリ・Kレベルで絞り込み（条件が空なら通す）
  return questions.filter(q => {
    const chOK = inList(q.chapter, cond.chapters);
    const catOK = inList(q.category, cond.cats);
    const kOK = inList(q.klevel, cond.levels);
    return chOK && catOK && kOK;
  });
}

/* ===================== 読み込み（index.jsonを活かす） ===================== */
async function loadQuestionsByIndex(conditions = {}) {
  // 1) マニフェスト取得
  let chunks = await loadManifest();

  // 2) マニフェストが無ければ連番探索
  if (!chunks) {
    console.warn('[load] マニフェストなし → 連番探索にフォールバック');
    chunks = await discoverSequentialChunks('/questions', 500, 3); // { path: "/questions/chunk-001.json" } 形式
    // 連番探索には chapter/category が無い → 後段で問題側フィルタ
  }

  // 3) チャンクの事前フィルタ（index.jsonにメタがある場合のみ）
  let targetChunks = chunks;
  if (Array.isArray(chunks) && chunks.length && 'chapter' in chunks[0]) {
    const pre = chunks.filter(c => {
      const chOK = inList(c.chapter, conditions.chapters);
      const catOK = inList(c.category, conditions.cats);
      return chOK && catOK;
    });
    targetChunks = pre.length ? pre : chunks; // 0件なら全件
  }

  // 4) チャンク読み込み → 正規化 → 統合
  const all = [];
  for (const c of targetChunks) {
    const path = c.path || c; // 柔軟対応
    const arr = await loadChunk(path);
    for (const raw of arr) {
      all.push(normalizeQuestionShape(raw));
    }
  }

  // 5) 後段フィルタ（Kレベルや、連番探索時の章・カテゴリ反映）
  const filtered = filterQuestionsCore(all, conditions);

  // 重複除去（idベース）
  const seen = new Set();
  const deduped = [];
  for (const q of filtered) {
    if (seen.has(q.id)) continue;
    seen.add(q.id);
    deduped.push(q);
  }

  console.log('[load] questions loaded:', { total: all.length, afterFilter: deduped.length });
  return deduped;
}

/* ===================== メッセージ表示 ===================== */
function showError(msg) {
  const el = queryById('message') || queryById('info') || queryById('notice');
  if (el) { el.textContent = msg; el.style.display = 'block'; }
  else alert(msg);
}
function clearMessage() {
  const el = queryById('message') || queryById('info') || queryById('notice');
  if (el) { el.textContent = ''; el.style.display = 'none'; }
}

/* ===================== レンダリング ===================== */
function renderMeta() {
  const total = sessionQuestions.length;
  queryById('progressLabel')?.setAttribute('data-total', String(total));
  queryById('progressLabel')?.setAttribute('data-current', String(current + 1));
  const meta = queryById('metaText') || queryById('progressLabel');
  if (meta) meta.textContent = `Q ${current + 1} / ${total}　正答: ${correctCount}`;
}
function renderQuestion(q) {
  clearMessage();
  renderMeta();

  const qTextEl =
    queryById('questionText') ||
    document.querySelector('[data-role="question-text"]') ||
    document.querySelector('#question .text') ||
    queryById('question'); // 最後のフォールバック

  if (qTextEl) qTextEl.textContent = q.text || '(問題文がありません)';

  const optEl =
    queryById('optionsList') ||
    document.querySelector('[data-role="options-list"]') ||
    document.querySelector('#question .options') ||
    queryById('choices') ||
    queryById('optionsContainer');

  if (optEl) {
    optEl.innerHTML = '';
    const isMulti = q.multi === true;
    const name = 'choice';
    const kind = isMulti ? 'checkbox' : 'radio';

    // options は配列（文字列 or {label,value}）を想定
    const opts = Array.isArray(q.options) ? q.options : [];
    if (opts.length === 0) {
      const input = document.createElement('input');
      input.type = 'text';
      input.placeholder = '解答を入力';
      input.id = 'freeTextAnswer';
      optEl.appendChild(input);
    } else {
      opts.forEach((o, idx) => {
        const label = typeof o === 'string' ? o : (o.label ?? o.text ?? String(o.value ?? idx + 1));
        const value = typeof o === 'string' ? o : (o.value ?? label);
        const id = `opt_${idx}`;

        const li = document.createElement('div');
        li.className = 'optionRow';

        const inp = document.createElement('input');
        inp.type = kind;
        inp.name = isMulti ? 'choices' : name;
        inp.value = String(value);
        inp.id = id;

        const lab = document.createElement('label');
        lab.setAttribute('for', id);
        lab.textContent = label;

        li.appendChild(inp);
        li.appendChild(lab);
        optEl.appendChild(li);
      });
    }
  }

  // 付随メタ表示
  const metaEl = queryById('questionMeta');
  if (metaEl) {
    metaEl.textContent = `章: ${q.chapter || '-'} / カテゴリ: ${q.category || '-'} / Kレベル: ${q.klevel || '-'}`;
  }
}

/* ===================== ナビゲーション ===================== */
function renderCurrent() {
  const total = sessionQuestions.length;
  if (total === 0) {
    showError('選択条件に合致する問題がありません。データ取得やパス設定を確認してください。');
    showRoute('home');
    return;
  }
  current = Math.max(0, Math.min(current, total - 1));
  renderQuestion(sessionQuestions[current]);
}
function prev() {
  if (current > 0) { current--; renderCurrent(); }
}
function next() {
  const total = sessionQuestions.length;
  if (current < total - 1) { current++; renderCurrent(); }
}

/* ===================== 解答処理 ===================== */
function readSelectedAnswers() {
  // 複数選択（checkbox）
  const checked = [...document.querySelectorAll('input[name="choices"]:checked')].map(el => el.value);
  if (checked.length) return checked;

  // 単一選択（radio）
  const sel = document.querySelector('input[name="choice"]:checked');
  if (sel) return [sel.value];

  // 自由入力
  const free = queryById('freeTextAnswer')?.value;
  if (free) return [free.trim()];

  return [];
}

function submitAnswer() {
  const q = sessionQuestions[current];
  const selected = readSelectedAnswers();

  // 正解（配列 or 文字列）
  const ansArr = Array.isArray(q.answer) ? q.answer.map(String) : [String(q.answer)];
  const ok = eqSetCompat(selected.map(String), ansArr);

  if (ok) correctCount++;
  pushTempDetail(q.id, ok);

  // 軽いフィードバック表示
  const feedbackEl = queryById('feedback') || queryById('message');
  if (feedbackEl) {
    feedbackEl.style.display = 'block';
    feedbackEl.textContent = ok ? '正解！' : `不正解。正解: ${Array.isArray(q.answer) ? q.answer.join(', ') : String(q.answer)}`;
  }

  // 次へ
  next();
}

/* ===================== セッション開始・再開 ===================== */
async function startWithFilters() {
  try {
    const cond = collectFilters();
    const loaded = await loadQuestionsByIndex(cond);

    // 0件対策：章だけ緩める → さらに全件
    let pool = loaded;
    if (pool.length === 0) {
      console.warn('[start] 0件 → 条件緩和（章のみ）');
      const condRelax = { chapters: cond.chapters, cats: [], levels: [] };
      pool = filterQuestionsCore(allQuestions.length ? allQuestions : loaded, condRelax);
      if (pool.length === 0) {
        console.warn('[start] それでも0件 → 全件');
        pool = allQuestions.length ? allQuestions : loaded;
      }
    }

    // 出題数
    numToAsk = Number(queryById('numSelect')?.value || numToAsk || 30);

    // セッション問題選定（ランダム）
    sessionQuestions = reservoirSample(pool, numToAsk);
    allQuestions = loaded; // 参考保持
    current = 0;
    correctCount = 0;
    tempDetails = [];
    stats.chapter.clear();
    stats.klevel.clear();

    showRoute('quiz');
    renderCurrent();
  } catch (e) {
    console.error(e);
    showError('問題データの読み込みに失敗しました。index.jsonやquestions配下の配置・パスを確認してください。');
  }
}

function restart() {
  current = 0;
  correctCount = 0;
  tempDetails = [];
  stats.chapter.clear();
  stats.klevel.clear();
  renderCurrent();
}

function goHome() {
  showRoute('home');
}

/* ===================== ダッシュボード（履歴/Chart.js） ===================== */
function renderDashboard() {
  const user = getActiveUserId();
  const history = getHistory(user);

  const listEl = queryById('historyList');
  if (listEl) {
    listEl.innerHTML = '';
    if (history.length === 0) {
      listEl.textContent = '履歴はまだありません。';
    } else {
      history.forEach((h, idx) => {
        const li = document.createElement('div');
        li.className = 'historyRow';
        li.textContent = `${idx + 1}. ${h.date} - 正答 ${h.correct}/${h.total} (${Math.round((h.correct/h.total)*100)}%)`;
        listEl.appendChild(li);
      });
    }
  }

  // Chart.js が存在する場合のみ描画
  const ctx = queryById('historyChart')?.getContext?.('2d');
  if (ctx && typeof Chart !== 'undefined') {
    const labels = history.map((h, i) => `#${i + 1}`);
    const data = history.map(h => Math.round((h.correct / h.total) * 100));
    // eslint-disable-next-line no-undef
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels,
        datasets: [{ label: '正答率(%)', data, backgroundColor: '#4caf50' }]
      },
      options: {
        responsive: true,
        scales: { y: { beginAtZero: true, max: 100 } }
      }
    });
  }
}

/* ===================== セッション終了保存（必要に応じ呼び出し） ===================== */
function finishSession() {
  const user = getActiveUserId();
  const total = sessionQuestions.length;
  const session = {
    date: new Date().toISOString(),
    total,
    correct: correctCount,
    details: tempDetails.slice(0, 200) // ほどほどに
  };
  saveHistory(user, session);

  // 結果表示
  const resEl = queryById('resultSummary') || queryById('message');
  if (resEl) {
    const pct = total ? Math.round((correctCount / total) * 100) : 0;
    resEl.textContent = `結果: ${correctCount} / ${total}（${pct}%）`;
  }
  showRoute('dashboard');
}

/* ===================== キーボード操作（任意） ===================== */
document.addEventListener('keydown', (ev) => {
  if (location.hash === '#quiz') {
    if (ev.key === 'ArrowLeft') prev();
    else if (ev.key === 'ArrowRight') next();
    else if (ev.key === 'Enter') submitAnswer();
  }
