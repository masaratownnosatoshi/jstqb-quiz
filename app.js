/*!
 * JSTQB ALTM v3.0 模擬試験（拡張版） — 修正版v4
 * 対応: 構文エラーの完全回避（記述の展開・簡略化）
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

// DB取得（安全に展開）
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

// DB保存（安全に展開）
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
  // データ形式の揺れを吸収
  if (result.json && Array.isArray(result.json.chunks)) {
    chunks = result.json.chunks;
  } else if (Array.isArray(result.json)) {
    chunks = result.json;
  }

  await idbPut('manifest', 'index', { chunks: chunks });
  return chunks;
}

async function loadChunk(path) {
  // キャッシュ確認
  const cached = await idbGet('questionChunks', path);
  if (cached) {
    if (Array.isArray(cached)) return cached;
    if (cached.questions && Array.isArray(cached.questions)) return cached.questions;
    return [];
  }

  // 取得
  const result = await fetchJSON(path);
  if (!result.ok) return [];

  let arr = [];
  // データ形式の揺れを吸収
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
  
  // フィルタリング
  let targetChunks = idxChunks.filter(c => {
    const cond = conditions || {};
    const chOK = !cond.chapter  || c.chapter === cond.chapter;
    const catOK = !cond.category || c.category === cond.category;
    return chOK && catOK;
  });

  if (targetChunks.length === 0) {
    // 該当なしなら全件対象にする（フォールバック）
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
  // querySelectorAllの結果を配列に変換
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
    if (qCh !== cCh) chOK = false;
  }

  // カテゴリの判定
  let catOK = true;
  if (cond.category) {
    const qCat = (q.category || '').trim();
    const cCat = (cond.category || '').trim();
    if (qCat !== cCat) catOK = false;
  }

  // Kレベルの判定
  let kOK = true;
  if (cond.klevel) {
    const qK = (q.klevel || '').trim();
    const cK = (cond.klevel || '').trim();
    if (qK !== cK) kOK = false;
  }

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
    alert('問題データが正しく読み込めませんでした。');
    return;
  }
  
  // リセット
  isAnswerChecked = false;
  if (feedbackEl) feedbackEl.classList.add('hidden');
  if (submitBtn) {
    submitBtn.textContent = '回答する';
    submitBtn.disabled = false;
  }

  // メタ情報表示
  if (idxEl) idxEl.textContent = (current + 1) + ' / ' + questions.length;
  if (chapterEl) chapterEl.textContent = q.chapter || '';
  if (levelEl) levelEl.textContent = q.klevel || q.level || '';
  
  // 問題文表示
  const qText = q.question || q.text || q.title || '(問題文)';
  if (textEl) textEl.textContent = qText;

  // 選択肢生成 (ABC対応)
  if (choicesEl) {
    choicesEl.innerHTML = '';
    
    // 選択肢配列の取得
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

      // 隠しラジオ/チェックボックス
      const input = document.createElement('input');
      input.type = isMulti ? 'checkbox' : 'radio';
      input.name = 'answer';
      input.value = String(i);
      input.style.display = 'none';

      // ABCタグ
      const tagSpan = document.createElement('span');
      tagSpan.className = 'option-tag';
      tagSpan.textContent = OPTION_LABELS[i] || '?';

      // 選択肢テキスト
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
  const q = sessionQuestions[current];
  if (!q) return;

  const feedbackEl = document.getElementById('feedback');
  const correctEl = document.getElementById('correctAnswer');
  const explainEl = document.getElementById('explanation');
  const judgeEl = document.getElementById('judgeResult');
  const submitBtn = document.getElementById('submitBtn');
  const scoreEl = document.getElementById('score');

  // 解説表示中なら「次へ」
  if (isAnswerChecked) {
    if (current < sessionQuestions.length - 1) {
      current++;
      renderQuestions(sessionQuestions);
    } else {
      finishSession();
    }
    return;
  }

  // 選択チェック
  const inputs = Array.from(document.querySelectorAll('input[name="answer"]'));
  const selected = inputs.filter(i => i.checked).map(i => parseInt(i.value, 10));
  
  if (selected.length === 0) {
    alert('選択肢を選んでください');
    return;
  }

  // 正解インデックス計算
  let opts = [];
  if (Array.isArray(q.options)) opts = q.options;
  else if (Array.isArray(q.choices)) opts = q.choices;

  let correctIndices = [];
  let rawAnswer = [];
  if (Array.isArray(q.answer)) rawAnswer = q.answer;
  else rawAnswer = [q.answer];

  // 正解が文字列(文章)ならインデックスに変換
  if (rawAnswer.length > 0 && typeof rawAnswer[0] === 'string') {
    correctIndices = rawAnswer.map(ansStr => opts.indexOf(ansStr)).filter(idx => idx !== -1);
  } else {
    correctIndices = rawAnswer.map(v => parseInt(v, 10));
  }
  correctIndices.sort((a, b) => a - b);

  // 判定
  const ok = eqSetCompat(selected, correctIndices);
  pushTempDetail(q.id || current, ok);
  
  if (ok) {
    correctCount++;
    if (scoreEl) scoreEl.textContent = correctCount;
  }
  
  // 集計
  if (q.chapter) {
    const oldVal = stats.chapter.get(q.chapter) || 0;
    stats.chapter.set(q.chapter, oldVal + (ok ? 1 : 0));
  }
  const lvl = q.klevel || q.level;
  if (lvl) {
    const oldVal = stats.klevel.get(lvl) || 0;
    stats.klevel.set(lvl, oldVal + (ok ? 1 : 0));
  }

  // --- 結果表示 ---
  if (judgeEl) {
    if (ok) {
      judgeEl.textContent = '正解！';
      judgeEl.className = 'judge-correct'; 
    } else {
      judgeEl.textContent = 'ざんねん…';
      judgeEl.className = 'judge-incorrect';
    }
  }

  // 正解の「記号(A,B...)」と「文章」を表示
  const correctLabels = correctIndices.map(i => OPTION_LABELS[i]).join(', ');
  const correctTextFull = correctIndices.map(i => opts[i]).join('<br>');

  if (correctEl) {
    correctEl.innerHTML = ''; // クリア

    // 1. 記号部分 (A, B...)
    const labelSpan = document.createElement('span');
    labelSpan.style.fontSize = '1.2em';
    labelSpan.style.fontWeight = 'bold';
    labelSpan.style.marginRight = '8px';
    labelSpan.textContent = correctLabels;
    
    // 2. 改行
    const br = document.createElement('br');

    // 3. 正解の文章部分
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
}

// ====== 開始処理 ======
function startWithFilters() {
  current = 0; 
  correctCount = 0; 
  tempDetails = [];
  const cond = getCurrentConditionsFromUI();
  
  loadQuestionsByIndex(cond).then(raw => {
    if (!raw || !raw.length) { 
      alert('条件に合う問題が見つかりませんでした。\n(index.jsonの読み込みに失敗しているか、条件が厳しすぎます)'); 
      return; 
    }
    
    const filtered = raw.filter(q => matchesQuestion(q, cond));
    if (!filtered.length) { 
      alert('選択された条件に合致する問題がありませんでした。'); 
      return; 
    }

    sessionQuestions = reservoirSample(filtered, numToAsk);
    showRoute('quiz');
    renderQuestions(sessionQuestions);
    
    const scoreEl = document.getElementById('score');
    if (scoreEl) scoreEl.textContent = '0';
  });
}

function getCurrentConditionsFromUI() {
  const f = collectFilters();
  const cond = {
    chapter: f.chapters[0] || null,
    category: f.cats[0] || null,
    klevel: f.levels[0] || null,
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
  
  if (finalCorrect) finalCorrect.textContent = correctCount;
  if (totalQuestions) totalQuestions.textContent = sessionQuestions.length;
  if (finalRate) {
    const rate = Math.round((correctCount / sessionQuestions.length) * 100);
    finalRate.textContent = rate;
  }
  
  renderDashboard(); 
}

function renderDashboard() {
  const user = getActiveUserId();
  const hist = getHistory(user);
  const listEl = document.getElementById('historyList');
  if (!listEl) return;
  listEl.innerHTML = '';
  
  hist.forEach((h, idx) => {
    const li = document.createElement('li');
    const dateStr = new Date(h.ts).toLocaleString();
    li.textContent = (idx + 1) + '. 正答 ' + h.correct + '/' + h.total + ' - ' + dateStr;
    listEl.appendChild(li);
  });
}

function restart() { 
  startWithFilters(); 
}

function goHome() { 
  showRoute('home'); 
}