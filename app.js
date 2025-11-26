
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
let allQuestions = [];        // 参考：全問題（連番フォールバック時に使用可）
let sessionQuestions = [];    // 今回の出題セット（フィルタ・サンプル後）
let current = 0;
let correctCount = 0;

const stats = { chapter: new Map(), klevel: new Map() }; // セッション集計
let userName = '';             // ユーザー名（localStorageキー）
let adaptiveMode = false;      // 弱点優先モード
let numToAsk = 30;             // 出題数（UI選択）
let tempDetails = [];          // { id, correct } — セッション詳細

document.addEventListener('DOMContentLoaded', async () => {
  // ルーター初期表示
  showRoute(location.hash.replace('#', '') || 'home');

  // イベント配線
  document.getElementById('startBtn').onclick = startWithFilters; // async版
  document.getElementById('prevBtn').onclick = prev;
  document.getElementById('nextBtn').onclick = next;
  document.getElementById('submitBtn').onclick = submitAnswer;
  document.getElementById('restartBtn').onclick = restart;
  const gh = document.getElementById('goHomeBtn');
  if (gh) gh.onclick = goHome;

  // ハッシュルーター
  window.addEventListener('hashchange', () => {
    const r = location.hash.replace('#', '') || 'home';
    showRoute(r);
    if (r === 'dashboard') renderDashboard();
  });

  // 旧：questions.json 単体読み込み → 廃止
  // 新：/questions チャンク読み込み（初期化時は未ロード。開始時にフィルタに応じてロード）

  // 匿名ID表示（ダッシュボード）
  document.getElementById('anonIdLabel').textContent = getActiveUserId();
});

// ====== ルーター ======
function showRoute(route) {
  document.querySelectorAll('section[data-route]').forEach(sec => {
    sec.classList.toggle('hidden', sec.getAttribute('data-route') !== route);
  });
  document.getElementById('meta').classList.toggle('hidden', route !== 'quiz');
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
async function fetchJSON(url) {
  const res = await fetch(url, { cache: 'no-store' });
  if (res.status === 404) return { ok: false, status: 404, json: null };
  if (!res.ok) return { ok: false, status: res.status, json: null };
  try {
    const json = await res.json();
    return { ok: true, status: 200, json };
  } catch (e) {
    console.error('[json] parse error', url, e);
    return { ok: false, status: 0, json: null };
  }
}

// マニフェスト：/questions/index.json を優先（なければnull）
async function loadManifest() {
  const cached = await idbGet('manifest', 'index');
  if (cached && Array.isArray(cached.chunks)) return cached.chunks;

  const { ok, status, json } = await fetchJSON('/questions/index.json');
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
  const { ok, json, status } = await fetchJSON(path);
  if (!ok) {
    if (status !== 404) console.error('[chunk] 取得失敗', path, status);
    return [];
  }
  const arr = Array.isArray(json) ? json : (Array.isArray(json?.questions) ? json.questions : []);
  await idbPut('questionChunks', path, json);
  return arr;
}

// 連番探索（マニフェスト無し時）— 存在するチャンクのリストを作る
async function discoverSequentialChunks(baseDir = '/questions', max = 500, pad = 3) {
  const list = [];
  let consecutive404 = 0;
  const MAX_404 = 10;
  for (let i = 1; i <= max; i++) {
    const num = String(i).padStart(pad, '0'); // 001, 002...
    const path = `${baseDir}/chunk-${num}.json`;
    const head = await fetch(path, { method: 'GET', cache: 'no-store' });
    if (head.status === 404) {
      consecutive404++;
      if (consecutive404 >= MAX_404) break;
      continue;
    }
    if (!head.ok) continue;
    list.push({ path }); // メタ（chapter/category）は不明 → 後で問題側で絞り込み
    consecutive404 = 0;
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

// ====== プール準備：フィルタに応じてチャンクを選び・読み込み ======
async function preparePoolByFilters(chapters, categories, levels) {
  // 1) マニフェスト取得 or 連番探索
  const manifestChunks = await loadManifest();
  let targets = [];

  if (manifestChunks && manifestChunks.length) {
    // マニフェストに chapter/category メタが有る場合は前段絞り込み、無ければ全件
    const hasMeta = !!manifestChunks[0] && (manifestChunks[0].chapter || manifestChunks[0].category);
    targets = hasMeta
      ? manifestChunks.filter(c => chapters.includes(c.chapter) && categories.includes(c.category))
      : manifestChunks;
  } else {
    targets = await discoverSequentialChunks('/questions', 500, 3);
  }

  // 2) 対象チャンクを読み込み → 問題側で最終フィルタ
  let pool = [];
  for (const t of targets) {
    const qs = await loadChunk(t.path);
    // 問題オブジェクトのフィールド：chapter/level/category による絞り込み
    const filtered = qs.filter(q => chapters.includes(q.chapter) && categories.includes(q.category) && levels.includes(q.level));
    pool = pool.concat(filtered);
    // 大量ロードを避けるため余裕分で打ち切り
    if (pool.length >= numToAsk * 2) break;
  }
  // マニフェストがメタ無しで全読み込みした場合、最後にフィルタを適用
  if (!manifestChunks || (manifestChunks && manifestChunks.length && !(manifestChunks[0].chapter || manifestChunks[0].category))) {
    pool = pool.filter(q => chapters.includes(q.chapter) && categories.includes(q.category) && levels.includes(q.level));
  }
  return dedupeById(pool);
}

function dedupeById(arr) {
  const seen = new Set();
  const out = [];
  for (const q of arr) {
    const id = q?.id;
    if (!id || seen.has(id)) continue;
    seen.add(id);
    out.push(q);
  }
  return out;
}

// ====== 適応（カテゴリ＋章＋Kレベルの合成重み） ======
const ADAPTIVE_WEIGHTS = { category: 0.6, chapter: 0.25, klevel: 0.15 };

async function getAggregateHistory(userId) {
  const h = await idbGet('aggregateHistory', userId);
  return h || { byCategory:{}, byChapter:{}, byKlevel:{} };
}
async function saveAggregateHistory(userId, data) { await idbPut('aggregateHistory', userId, data); }
async function updateAggregateHistory(userId, category, chapter, level, isCorrect) {
  const h = await getAggregateHistory(userId);
  const inc = (obj, key) => { obj[key] ??= { attempts:0, correct:0 }; obj[key].attempts += 1; if (isCorrect) obj[key].correct += 1; };
  inc(h.byCategory, category); inc(h.byChapter, chapter); inc(h.byKlevel, level);
  await saveAggregateHistory(userId, h);
}
async function adaptiveWeightsForUser(userId) {
  const h = await getAggregateHistory(userId);
  const rate = (v) => v.attempts ? (v.correct / v.attempts) : 0;
  const wCat = new Map();
  Object.entries(h.byCategory).forEach(([k,v]) => { wCat.set(k, Math.max(0.1, 1 - rate(v))); });
  const wCh = new Map(); Object.entries(h.byChapter).forEach(([k,v]) => { wCh.set(k, Math.max(0.1, 1 - rate(v))); });
  const wKl = new Map(); Object.entries(h.byKlevel).forEach(([k,v]) => { wKl.set(k, Math.max(0.1, 1 - rate(v))); });
  return { wCat, wCh, wKl };
}
function blendWeightsForQuestion(q, wCat, wCh, wKl) {
  const a = ADAPTIVE_WEIGHTS.category * (wCat.get(q.category) ?? 0.5);
  const b = ADAPTIVE_WEIGHTS.chapter  * (wCh.get(q.chapter)  ?? 0.5);
  const c = ADAPTIVE_WEIGHTS.klevel   * (wKl.get(q.level)    ?? 0.5);
  return Math.max(0.1, a + b + c);
}
async function sampleWithAdaptive(pool, n, userId) {
  const { wCat, wCh, wKl } = await adaptiveWeightsForUser(userId);
  const items = pool.map(q => ({ q, w: blendWeightsForQuestion(q, wCat, wCh, wKl) }));
  const res = [];
  while (res.length < Math.min(n, items.length)) {
    const total = items.reduce((s, it) => s + it.w, 0);
    let r = Math.random() * total;
    let i = 0;
    for (; i < items.length; i++) { r -= items[i].w; if (r <= 0) break; }
    res.push(items[i].q);
    items.splice(i, 1);
  }
  return res;
}

// ====== 開始：フィルタ・適応モード・サンプリング（async） ======
async function startWithFilters() {
  userName = getActiveUserId();
  adaptiveMode = document.getElementById('adaptiveMode').checked;
  numToAsk = Number(document.getElementById('numSelect').value);

  const { chapters, levels, cats } = collectFilters();
  let pool = await preparePoolByFilters(chapters, cats, levels);

  if (!pool.length) { alert('選択条件に合致する問題がありません。条件を見直してください。'); return; }

  sessionQuestions = adaptiveMode
    ? await sampleWithAdaptive(pool, numToAsk, userName)
    : reservoirSample(pool, numToAsk);

  current = 0; correctCount = 0; tempDetails = [];

  showRoute('quiz');
  initSessionStats(sessionQuestions);
  renderQuestion();
}

// ====== セッション集計初期化 ======
function initSessionStats(qs) {
  stats.chapter.clear();
  stats.klevel.clear();
  qs.forEach(q => {
    if (!stats.chapter.has(q.chapter)) stats.chapter.set(q.chapter, {correct:0, total:0});
    if (!stats.klevel.has(q.level))    stats.klevel.set(q.level,    {correct:0, total:0});
  });
}

// ====== 描画 ======
function renderQuestion() {
  const q = sessionQuestions[current];
  document.getElementById('progress').textContent = `${current+1} / ${sessionQuestions.length}`;
  document.getElementById('score').textContent = correctCount;
  document.getElementById('chapter').textContent = `章：${q.chapter}（${q.type}/${q.category}）`;
  document.getElementById('level').textContent   = `Kレベル：${q.level}`;
  document.getElementById('questionText').textContent = q.question;

  const form = document.getElementById('optionsForm'); form.innerHTML = '';
  const isMulti = q.type === '複数選択' || Array.isArray(q.answer);
  q.options.forEach((opt, i) => {
    const id = `opt-${i}`;
    const input = document.createElement('input'); input.type = isMulti ? 'checkbox' : 'radio'; input.name = 'option'; input.id = id; input.value = opt;
    const label = document.createElement('label'); label.htmlFor = id; label.textContent = opt; label.prepend(input);
    form.appendChild(label);
  });

  document.getElementById('feedback').classList.add('hidden');
  document.getElementById('correctAnswer').textContent = '';
  document.getElementById('explanation').textContent = '';
  document.getElementById('prevBtn').disabled = current === 0;
  document.getElementById('nextBtn').disabled = true;
}

// ====== 回答処理 ======
async function submitAnswer() {
  const q = sessionQuestions[current];
  const selected = [...document.querySelectorAll('#optionsForm input[name="option"]')]
                   .filter(i => i.checked)
                   .map(i => i.value);
  if (!selected.length) { alert('選択してください'); return; }

  const ok = eqSetCompat(selected, q.answer);

  const cStat = stats.chapter.get(q.chapter); cStat.total += 1;
  const kStat = stats.klevel.get(q.level);   kStat.total += 1;
  if (ok) { correctCount += 1; cStat.correct += 1; kStat.correct += 1; }

  // 正解表示（ラベル付き）
  const answerArr = Array.isArray(q.answer) ? q.answer : [q.answer];
  const ansText = answerArr.map(a => a).join(' / ');
  document.getElementById('correctAnswer').textContent = ansText;
  document.getElementById('explanation').textContent = q.explanation || '(解説なし)';
  document.getElementById('feedback').classList.remove('hidden');
  document.getElementById('nextBtn').disabled = false;
  document.getElementById('score').textContent = correctCount;

  // 履歴（セッション詳細）— 後で保存
  pushTempDetail(q.id, ok);

  // 集計（適応用）
  await updateAggregateHistory(userName, q.category, q.chapter, q.level, ok);
}

// ====== 移動・結果 ======
function next() { if (current < sessionQuestions.length - 1) { current += 1; renderQuestion(); } else { showResults(); } }
function prev() { if (current > 0) { current -= 1; renderQuestion(); } }
function showResults() {
  showRoute('results');
  document.getElementById('finalCorrect').textContent = correctCount;
  document.getElementById('totalQuestions').textContent = sessionQuestions.length;
  const rateP = Math.round((correctCount / sessionQuestions.length) * 100);
  document.getElementById('finalRate').textContent = rateP;

  finalizeAndSaveSession();
  renderHistoryList();
  renderSessionCharts();
}

// ====== セッション保存 ======
function finalizeAndSaveSession() {
  const byChapter = {}; stats.chapter.forEach((v, k) => { byChapter[k] = { answered: v.total, correct: v.correct }; });
  const byKlevel = {};  stats.klevel.forEach((v, k) => { byKlevel[k] = { answered: v.total, correct: v.correct }; });
  const filters = {
    numToAsk,
    chapters: [...document.querySelectorAll('.chapterFilter:checked')].map(i => i.value),
    klevels:  [...document.querySelectorAll('.levelFilter:checked')].map(i => i.value),
    categories:[...document.querySelectorAll('.categoryFilter:checked')].map(i => i.value),
    adaptive: adaptiveMode
  };
  const session = { ts: Date.now(), filters, total: sessionQuestions.length, correct: correctCount, byChapter, byKlevel, details: tempDetails.slice() };
  saveHistory(userName, session);
  tempDetails = [];
}

// ====== 履歴表示 ======
function renderHistoryList() {
  const ul = document.getElementById('historyList'); if (!ul) return;
  const h = getHistory(userName); ul.innerHTML = '';
  h.slice(0, 10).forEach(s => {
    const li = document.createElement('li');
    const d = new Date(s.ts);
    const rate = s.total ? Math.round((s.correct / s.total) * 100) : 0;
    li.textContent = `${d.toLocaleString()}：${s.correct}/${s.total}（${rate}%） [章=${(s.filters?.chapters||[]).join(',')} K=${(s.filters?.klevels||[]).join(',')}]`;
    ul.appendChild(li);
  });
}

// ====== グラフ（セッション） ======
function renderSessionCharts() {
  if (typeof Chart !== 'function') return;
  const byChapterObj = {}; stats.chapter.forEach((v, k) => { byChapterObj[k] = { answered: v.total, correct: v.correct }; });
  const byKlevelObj = {};  stats.klevel.forEach((v, k) => { byKlevelObj[k] = { answered: v.total, correct: v.correct }; });
  const rate = (c, a) => a ? Math.round((c / a) * 100) : 0;
  const chapterLabels = Object.keys(byChapterObj); const chapterRates = chapterLabels.map(k => rate(byChapterObj[k].correct, byChapterObj[k].answered));
  const kLabels = Object.keys(byKlevelObj); const kRates = kLabels.map(k => rate(byKlevelObj[k].correct, byKlevelObj[k].answered));
  window._charts = window._charts || {}; ['chapterChart','kChart'].forEach(id => { if (window._charts[id]) { try { window._charts[id].destroy(); } catch(e){} } });
  const chapterCanvas = document.getElementById('chapterChart'); if (chapterCanvas && chapterLabels.length) {
    window._charts['chapterChart'] = new Chart(chapterCanvas, { type: 'bar', data: { labels: chapterLabels, datasets: [{ label: '正答率(%)', data: chapterRates, backgroundColor: '#4b8bff' }] }, options: { scales: { y: { beginAtZero: true, max: 100 } } } });
  }
  const kCanvas = document.getElementById('kChart'); if (kCanvas && kLabels.length) {
    window._charts['kChart'] = new Chart(kCanvas, { type: 'bar', data: { labels: kLabels, datasets: [{ label: '正答率(%)', data: kRates, backgroundColor: '#7c4dff' }] }, options: { scales: { y: { beginAtZero: true, max: 100 } } } });
  }
}

// ====== ダッシュボード ======
function aggregateHistory(h) {
  const acc = { totalAnswered: 0, totalCorrect: 0, byChapter: {}, byKlevel: {} };
  h.forEach(s => {
    acc.totalAnswered += s.total; acc.totalCorrect += s.correct;
    for (const [ch, obj] of Object.entries(s.byChapter || {})) {
      acc.byChapter[ch] ??= { answered: 0, correct: 0 };
      acc.byChapter[ch].answered += obj.answered; acc.byChapter[ch].correct += obj.correct;
    }
    for (const [k, obj] of Object.entries(s.byKlevel || {})) {
      acc.byKlevel[k] ??= { answered: 0, correct: 0 };
      acc.byKlevel[k].answered += obj.answered; acc.byKlevel[k].correct += obj.correct;
    }
  });
  return acc;
}
function renderDashboard() {
  const uid = getActiveUserId(); document.getElementById('anonIdLabel').textContent = uid;
  const h = getHistory(uid); const acc = aggregateHistory(h);
  const rateAll = acc.totalAnswered ? Math.round((acc.totalCorrect / acc.totalAnswered) * 100) : 0;
  document.getElementById('totalAnswered').textContent = acc.totalAnswered;
  document.getElementById('totalCorrect').textContent = acc.totalCorrect;
  document.getElementById('totalRate').textContent = rateAll;
  const rate = (c, a) => a ? Math.round((c / a) * 100) : 0;
  const weak = Object.entries(acc.byChapter).map(([k, v]) => ({ k, r: rate(v.correct, v.answered), a: v.answered }))
    .concat(Object.entries(acc.byKlevel).map(([k, v]) => ({ k, r: rate(v.correct, v.answered), a: v.answered })));
  weak.sort((a,b) => a.r - b.r || b.a - a.a);
  const ul = document.getElementById('weakAreas'); ul.innerHTML = '';
  weak.filter(w => w.a >= 5).slice(0, 5).forEach(w => { const li = document.createElement('li'); li.textContent = `${w.k}：正答率 ${w.r}%（回答 ${w.a}）`; ul.appendChild(li); });

  if (typeof Chart === 'function') { renderBarChart('chapterChartAll', acc.byChapter); renderBarChart('kChartAll', acc.byKlevel); }
}
function renderBarChart(canvasId, dataObj) {
  const labels = Object.keys(dataObj);
  const rate = (c, a) => a ? Math.round((c / a) * 100) : 0;
  const rates = labels.map(k => rate(dataObj[k].correct, dataObj[k].answered));
  window._charts = window._charts || {};
  if (window._charts[canvasId]) { try { window._charts[canvasId].destroy(); } catch(e){} }
  const el = document.getElementById(canvasId); if (!el || !labels.length) return;
  window._charts[canvasId] = new Chart(el, { type: 'bar', data: { labels, datasets: [{ label: '正答率(%)', data: rates, backgroundColor: '#4b8bff' }] }, options: { scales: { y: { beginAtZero: true, max: 100 } } } });
}

// ====== TOP戻る／再スタート／削除 ======
function goHome() { const ok = confirm('試験を中断してTOPへ戻りますか？（回答済みは保持されます）'); if (!ok) return; showRoute('home'); }
function restart() { showRoute('home'); }
const clearBtn = document.getElementById('clearDataBtn');
if (clearBtn) {
  clearBtn.addEventListener('click', async () => {
    const uid = getActiveUserId();
    if (confirm('この端末のあなたの履歴データを削除します。よろしいですか？')) {
      localStorage.removeItem(`altm_history_${uid}`);
      // ついでに適応用集計もクリア
      if (!_db) await openDb();
      const tx = _db.transaction('aggregateHistory', 'readwrite');
      tx.objectStore('aggregateHistory').delete(uid);
      alert('削除しました');
      renderDashboard();
    }
  });
}
// app.js end
