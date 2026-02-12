/*!
 * JSTQB ALTM v3.0 テスト対策くん — 修正版v23 (Part 1/2)
 * 修正: フォルダ構成変更(questions/)への対応、index.jsonパス修正
 */

// ====== 初期化・状態 ======
let sessionQuestions = [];
let current = 0;
let correctCount = 0;
let isAnswerChecked = false;

// チャート・データ保持用
let chartChapter = null;
let chartKLevel = null;
let dbChartChapter = null;
let dbChartKLevel = null;
let tempDetails = [];
let favorites = [];

const OPTION_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'];
let numToAsk = 30; // 1回の出題数デフォルト

document.addEventListener('DOMContentLoaded', () => {
  try {
    loadFavorites();

    let r = location.hash.replace('#', '');
    if (!r) r = 'home';
    showRoute(r);
    
    // 初期ロード：問題数カウント表示
    updateTotalCount();

    onClick('#startBtn', startWithFilters);
    onClick('#submitBtn', submitAnswer);
    onClick('#restartBtn', restart);
    onClick('#goHomeBtn', goHome);
	// ★ここに追加：結果画面の「TOPへ戻る」ボタン
    onClick('#backToTopBtn', goHome);
    onClick('#clearDataBtn', clearLocalData);
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
    alert('アプリ起動エラー: ' + e.message);
  }
});

// ====== ルーター ======
function showRoute(route) {
  document.querySelectorAll('section[data-route]').forEach(sec => {
    if (sec.getAttribute('data-route') === route) {
      sec.classList.remove('hidden');
    } else {
      sec.classList.add('hidden');
    }
  });

  const meta = document.getElementById('meta');
  if (meta) {
    route === 'quiz' ? meta.classList.remove('hidden') : meta.classList.add('hidden');
  }
  location.hash = '#' + route;
  window.scrollTo(0, 0);
}

// ====== ユーティリティ ======
function onClick(sel, fn) {
  const el = document.querySelector(sel);
  if (el) el.onclick = fn;
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
  const anon = 'guest-' + Math.random().toString(36).slice(2, 8);
  localStorage.setItem('altm_active_user', anon);
  return anon;
}

function eqSetCompat(selectedArr, correctArr) {
  if (!Array.isArray(selectedArr) || !Array.isArray(correctArr)) return false;
  if (selectedArr.length !== correctArr.length) return false;
  const a = new Set(selectedArr.map(String));
  const b = new Set(correctArr.map(String));
  for (const v of a) if (!b.has(v)) return false;
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
  if (!originalOpts.length) return q;

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
  newQ.answer = items.map((item, index) => item.isCorrect ? index : -1).filter(i => i !== -1);
  
  return newQ;
}

function resolveRepoUrl(input) {
  if (/^https?:\/\//i.test(input)) return input;
  return new URL(input, document.baseURI).href;
}

// ====== お気に入り機能 ======
function loadFavorites() {
  try {
    const stored = localStorage.getItem('altm_favorites');
    favorites = stored ? JSON.parse(stored) : [];
  } catch (e) { favorites = []; }
}
function saveFavorites() { localStorage.setItem('altm_favorites', JSON.stringify(favorites)); }
function toggleFavorite() {
  const q = sessionQuestions[current];
  if (!q || !q.id) return;
  const index = favorites.indexOf(q.id);
  if (index === -1) favorites.push(q.id);
  else favorites.splice(index, 1);
  saveFavorites();
  updateFavButtonState(q.id);
}
function updateFavButtonState(qId) {
  const btn = document.getElementById('favBtn');
  if (!btn) return;
  if (favorites.includes(qId)) {
    btn.classList.add('active');
    btn.textContent = '★';
  } else {
    btn.classList.remove('active');
    btn.textContent = '☆';
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
    const raw = localStorage.getItem('altm_history_' + (user || 'guest'));
    return raw ? JSON.parse(raw) : [];
  } catch (e) { return []; }
}

function saveHistory(user, session) {
  try {
    const key = 'altm_history_' + (user || 'guest');
    const h = getHistory(user);
    h.unshift(session);
    if (h.length > 100) h.length = 100; 
    localStorage.setItem(key, JSON.stringify(h));
  } catch (e) { console.error(e); }
}

function clearLocalData() {
  if (!confirm("履歴とお気に入りを削除しますか？")) return;
  localStorage.removeItem('altm_history_' + getActiveUserId());
  localStorage.removeItem('altm_favorites');
  favorites = [];
  if (dbChartChapter) dbChartChapter.destroy();
  if (dbChartKLevel) dbChartKLevel.destroy();
  renderDashboard();
  alert("削除しました");
}

function isLastAnswerIncorrect(qId) {
  if (!qId) return false;
  const hist = getHistory(getActiveUserId());
  for (const s of hist) {
    if (s.details) {
      const d = s.details.find(x => x.id === qId);
      if (d) return !d.correct;
    }
  }
  return false;
}

// ====== IndexedDB (キャッシュ用) ======
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
    const req = tx.objectStore(store).get(key);
    req.onsuccess = () => resolve(req.result || null);
    req.onerror = () => reject(req.error);
  });
}
async function idbPut(store, key, value) {
  if (!_db) await openDb();
  return new Promise((resolve, reject) => {
    const tx = _db.transaction(store, 'readwrite');
    const req = tx.objectStore(store).put(value, key);
    req.onsuccess = () => resolve(true);
    req.onerror = () => reject(req.error);
  });
}// ====== データ取得 ======
async function fetchJSON(inputUrl) {
  const finalUrl = resolveRepoUrl(inputUrl);
  try {
    const res = await fetch(finalUrl, { cache: 'no-store' });
    if (!res.ok) return { ok: false, status: res.status, json: null };
    const json = await res.json();
    return { ok: true, status: 200, json: json };
  } catch (e) {
    console.error('Fetch error:', inputUrl, e);
    return { ok: false, status: 0, json: null };
  }
}

async function loadManifest() {
  // ★ルートの index.json を読む
  const result = await fetchJSON('questions/index.json');
  if (!result.ok) {
    console.error("index.json not found.");
    return null;
  }
  let chunks = [];
  if (result.json && Array.isArray(result.json.chunks)) chunks = result.json.chunks;
  else if (Array.isArray(result.json)) chunks = result.json;
  
  await idbPut('manifest', 'index', { chunks: chunks });
  return chunks;
}

async function loadChunk(path) {
  // index.jsonのpath (例: questions/ch1.json) をそのまま使う
  const cached = await idbGet('questionChunks', path);
  if (cached) {
    return Array.isArray(cached) ? cached : (cached.questions || []);
  }
  const result = await fetchJSON(path);
  if (!result.ok) return [];
  
  let arr = [];
  if (Array.isArray(result.json)) arr = result.json;
  else if (result.json && Array.isArray(result.json.questions)) arr = result.json.questions;
  
  await idbPut('questionChunks', path, arr);
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
    const total = chunks.reduce((sum, c) => sum + (c.qCount || 0), 0);
    if (countEl) countEl.textContent = total;
  } catch (e) { console.error(e); }
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

function matchesQuestion(q, cond) {
  if (cond.favOnly && !favorites.includes(q.id)) return false;
  if (cond.calcOnly && (!q.question || !q.question.includes('【計算】'))) return false;

  if (cond.chapters?.length && !cond.chapters.includes(q.chapter)) return false;
  if (cond.categories?.length && !cond.categories.includes(q.category)) return false;
  
  const qK = q.klevel || q.level;
  if (cond.klevels?.length && qK && !cond.klevels.includes(qK)) return false;
  
  return true;
}

// ====== UI構築・メインロジック ======
function startWithFilters() {
  const btn = document.getElementById('startBtn');
  const originalText = btn.textContent;
  
  btn.textContent = '読み込み中...';
  btn.disabled = true;

  current = 0; 
  correctCount = 0; 
  tempDetails = [];
  
  const f = collectFilters();
  const countInput = document.getElementById('numSelect');
  if (countInput) numToAsk = parseInt(countInput.value, 10);

  const cond = {
    chapters: f.chapters, 
    categories: f.cats,
    klevels: f.levels,
    calcOnly: document.getElementById('calcOnlyMode')?.checked,
    favOnly: document.getElementById('favOnlyMode')?.checked
  };

  loadQuestionsByIndex(cond).then(raw => {
    if (!raw.length) throw new Error('条件に合う問題が見つかりません');
    
    let filtered = raw.filter(q => matchesQuestion(q, cond));
    
    if (document.getElementById('adaptiveMode')?.checked) {
      const hist = getHistory(getActiveUserId());
      const wrongIds = new Set();
      hist.forEach(sess => {
        if(sess.details) sess.details.forEach(d => { if(!d.correct) wrongIds.add(d.id); });
      });
      filtered.sort((a, b) => {
        const aW = wrongIds.has(a.id) ? 1 : 0;
        const bW = wrongIds.has(b.id) ? 1 : 0;
        return bW - aW;
      });
    } else {
      filtered = shuffleArray(filtered);
    }

    if (!filtered.length) throw new Error('条件に合致する問題が0問でした。');

    sessionQuestions = filtered.slice(0, numToAsk).map(q => randomizeQuestionOptions(q));
    
    showRoute('quiz');
    renderQuestions();
    
    const scoreEl = document.getElementById('score');
    if (scoreEl) scoreEl.textContent = '0';

  }).catch(e => {
    alert(e.message);
  }).finally(() => {
    btn.textContent = originalText;
    btn.disabled = false;
  });
}

function renderQuestions() {
  const q = sessionQuestions[current];
  if (!q) return;

  isAnswerChecked = false;
  document.getElementById('feedback')?.classList.add('hidden');
  const sBtn = document.getElementById('submitBtn');
  if(sBtn) { sBtn.textContent = '回答する'; sBtn.disabled = false; }
  
  document.getElementById('progress').textContent = (current + 1) + ' / ' + sessionQuestions.length;
  document.getElementById('chapter').textContent = q.chapter || '';
  document.getElementById('level').textContent = q.klevel || q.level || '';
  document.getElementById('questionText').textContent = q.question || '';

  document.querySelectorAll('.retry-alert').forEach(e => e.remove());
  if (q.id && isLastAnswerIncorrect(q.id)) {
    const h2 = document.getElementById('questionText');
    const badge = document.createElement('div');
    badge.className = 'retry-alert';
    badge.textContent = '以前間違えた問題です';
    h2.parentNode.insertBefore(badge, h2);
  }
  updateFavButtonState(q.id);

  const cEl = document.getElementById('choices');
  cEl.innerHTML = '';
  let opts = q.options || q.choices || [];
  const isMulti = q.multi || q.type === '複数選択';

  opts.forEach((optText, i) => {
    const div = document.createElement('div');
    div.style.padding = '8px 0';
    const lbl = document.createElement('label');
    lbl.style.display = 'flex'; 
    lbl.style.alignItems = 'center'; 
    lbl.style.cursor = 'pointer';

    const inp = document.createElement('input');
    inp.type = isMulti ? 'checkbox' : 'radio';
    inp.name = 'answer';
    inp.value = String(i);
    inp.style.marginRight = '8px';
    inp.style.transform = 'scale(1.2)';

    const tag = document.createElement('span');
    tag.className = 'option-tag';
    tag.textContent = OPTION_LABELS[i] || '?';

    const txt = document.createElement('span');
    txt.className = 'option-content';
    txt.textContent = optText;
    txt.style.flex = '1';

    lbl.append(inp, tag, txt);
    div.appendChild(lbl);
    cEl.appendChild(div);
  });
}

function submitAnswer() {
  const q = sessionQuestions[current];
  if (!q) return;
  const sBtn = document.getElementById('submitBtn');

  if (isAnswerChecked) {
    if (current < sessionQuestions.length - 1) {
      current++;
      renderQuestions();
    } else {
      finishSession();
    }
    return;
  }

  const inputs = Array.from(document.querySelectorAll('input[name="answer"]:checked'));
  if (!inputs.length) { alert('選択肢を選んでください'); return; }
  
  const selected = inputs.map(i => parseInt(i.value, 10));
  
  let opts = q.options || q.choices || [];
  let rawAns = Array.isArray(q.answer) ? q.answer : [q.answer];
  let correctIndices = [];

  if (rawAns.length > 0 && typeof rawAns[0] === 'string') {
    correctIndices = rawAns.map(s => opts.findIndex(o => String(o).trim() === String(s).trim())).filter(i => i !== -1);
  } else {
    correctIndices = rawAns.map(v => parseInt(v, 10));
  }
  
  const ok = eqSetCompat(selected, correctIndices);
  pushTempDetail(q, ok);
  if (ok) {
    correctCount++;
    document.getElementById('score').textContent = correctCount;
  }

  const judge = document.getElementById('judgeResult');
  if (ok) {
    judge.textContent = '正解！'; judge.className = 'judge-correct';
  } else {
    judge.textContent = '不正解...'; judge.className = 'judge-incorrect';
  }

  const correctLabels = correctIndices.map(i => OPTION_LABELS[i]).join(', ');
  const correctTexts = correctIndices.map(i => opts[i]).join('<br>');
  document.getElementById('correctAnswer').innerHTML = 
    `<span style="font-size:1.2em;font-weight:bold;margin-right:8px">${correctLabels}</span><br><span style="font-size:0.9em;color:#555">${correctTexts}</span>`;
  
  document.getElementById('explanation').textContent = q.explanation || '解説なし';
  document.getElementById('feedback').classList.remove('hidden');

  sBtn.textContent = (current < sessionQuestions.length - 1) ? '次の問題へ' : '結果を見る';
  
  document.querySelectorAll('input[name="answer"]').forEach(i => i.disabled = true);
  isAnswerChecked = true;
}

function finishSession() {
  saveHistory(getActiveUserId(), { 
    correct: correctCount, 
    total: sessionQuestions.length, 
    ts: Date.now(), 
    details: tempDetails 
  });
  
  showRoute('results');
  
  document.getElementById('finalCorrect').textContent = correctCount;
  document.getElementById('totalQuestions').textContent = sessionQuestions.length;
  const rate = Math.round((correctCount / sessionQuestions.length) * 100);
  document.getElementById('finalRate').textContent = rate;
  
  const msg = document.getElementById('passFailMessage');
  if (rate >= 65) {
    msg.textContent = "合格ラインクリア！素晴らしい！";
    msg.className = "result-message pass-msg";
  } else {
    msg.textContent = "あと少し！復習して再挑戦しましょう";
    msg.className = "result-message fail-msg";
  }
  
  renderDashboard();
  drawResultCharts(tempDetails, 'chapterChart', 'kChart');
}

// ====== チャート・ダッシュボード ======
function drawResultCharts(data, chId, kId) {
  if (typeof Chart === 'undefined') return;
  
  const agg = (keyProp) => {
    const map = {};
    data.forEach(d => {
      const k = d[keyProp] || '不明';
      if (!map[k]) map[k] = { t: 0, c: 0 };
      map[k].t++;
      if (d.correct) map[k].c++;
    });
    return map;
  };

  const draw = (cid, stats, inst) => {
    const ctx = document.getElementById(cid);
    if (!ctx) return null;
    if (inst) inst.destroy();
    const lbls = Object.keys(stats);
    const vals = lbls.map(k => stats[k].t === 0 ? 0 : Math.round((stats[k].c / stats[k].t) * 100));
    return new Chart(ctx, {
      type: 'bar',
      data: {
        labels: lbls,
        datasets: [{ label: '正答率(%)', data: vals, backgroundColor: '#2b5797' }]
      },
      options: { scales: { y: { beginAtZero: true, max: 100 } } }
    });
  };

  if (chId === 'chapterChart') {
    chartChapter = draw(chId, agg('chapter'), chartChapter);
    chartKLevel = draw(kId, agg('klevel'), chartKLevel);
  } else {
    dbChartChapter = draw(chId, agg('chapter'), dbChartChapter);
    dbChartKLevel = draw(kId, agg('klevel'), dbChartKLevel);
  }
}

function renderDashboard() {
  const hist = getHistory(getActiveUserId());
  const list = document.getElementById('historyList');
  if (list) {
    list.innerHTML = '';
    hist.slice(0, 10).forEach((h, i) => {
      const li = document.createElement('li');
      li.textContent = `${i+1}. 正答 ${h.correct}/${h.total} (${new Date(h.ts).toLocaleDateString()})`;
      list.appendChild(li);
    });
  }

  let totalAns = 0, totalCor = 0, allD = [];
  hist.forEach(h => {
    totalAns += h.total;
    totalCor += h.correct;
    if (h.details) allD = allD.concat(h.details);
  });

  document.getElementById('totalAnswered').textContent = totalAns;
  document.getElementById('totalCorrect').textContent = totalCor;
  document.getElementById('totalRate').textContent = totalAns ? Math.round((totalCor/totalAns)*100) : 0;

  // 弱点分析
  const chStats = {};
  allD.forEach(d => {
    const k = d.chapter || '未分類';
    if (!chStats[k]) chStats[k] = { t:0, c:0 };
    chStats[k].t++;
    if (d.correct) chStats[k].c++;
  });
  const weak = Object.keys(chStats)
    .map(k => ({ n: k, r: (chStats[k].c/chStats[k].t)*100 }))
    .sort((a,b) => a.r - b.r)
    .slice(0, 3);
  
  const wEl = document.getElementById('weakAreas');
  if(wEl) {
    wEl.innerHTML = '';
    weak.forEach(w => {
      const li = document.createElement('li');
      li.textContent = `${w.n} (${Math.round(w.r)}%)`;
      wEl.appendChild(li);
    });
  }

  if (allD.length) drawResultCharts(allD, 'chapterChartAll', 'kChartAll');
}

function restart() { startWithFilters(); }
function goHome() { showRoute('home'); }