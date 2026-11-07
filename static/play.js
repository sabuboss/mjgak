// 면접 카드 챌린지: 하루 3장 → 생각 15초·답변 60초 → 스스로 체크 → 경험치·레벨·연속 기록.
// 기록은 localStorage 에만 둔다(서버 전송 없음). 질문·답변 내용은 통계로 보내지 않는다.
(function () {
  var $ = function (id) { return document.getElementById(id); };
  var KEY = "mjgak_play_v1", PREP = 15, ANSWER = 60, MIN_SEC = 20, PER_DAY = 3;
  var TITLES = ["첫 카드", "목소리 예열", "결론부터", "장면으로 말하기", "60초 정리", "꼬리질문 대비", "흔들림 없는 답", "면접장 준비 완료"];
  var CHECKS = ["결론부터", "내 경험", "배운 점", "시간"];
  var WEAK_TIP = [
    "첫 문장에 답부터 말해 보세요. \"저는 ○○라고 생각합니다\"로 시작하면 됩니다.",
    "활동 이름만 말하지 말고, 그때 한 일 하나를 장면처럼 말해 보세요(언제·무엇을·어떻게).",
    "마지막 한 문장을 \"그래서 ○○를 배웠고, 대학에서 ○○로 이어 가고 싶습니다\"로 맺어 보세요.",
    "답변이 길거나 너무 짧습니다. 결론 1문장 + 경험 2~3문장 + 배운 점 1문장이면 40~50초입니다."
  ];
  var BADGES = [
    ["first", "첫 카드", "카드 한 장을 기록했다", function (s) { return s.total >= 1; }],
    ["day1", "오늘의 3장", "하루 미션을 처음 끝냈다", function (s) { return countDone(s) >= 1; }],
    ["streak3", "3일 연속", "3일 연속으로 미션을 끝냈다", function (s) { return s.best >= 3; }],
    ["streak7", "7일 연속", "7일 연속으로 미션을 끝냈다", function (s) { return s.best >= 7; }],
    ["cards30", "카드 30장", "서로 다른 질문 30개에 답했다", function (s) { return Object.keys(s.seen).length >= 30; }],
    ["perfect5", "4체크 다섯 번", "4개를 모두 체크한 답변 5번", function (s) { return s.perfect >= 5; }],
    ["ontime10", "시간 지킴이", "20~60초 안에 끝낸 답변 10번", function (s) { return s.ontime >= 10; }]
  ];
  function ev(name, p) { try { if (window.gtag) gtag("event", name, p || {}); } catch (e) {} }

  // ---- 날짜(기기 시각 기준) ----
  function ymd(d) { return d.getFullYear() + "-" + ("0" + (d.getMonth() + 1)).slice(-2) + "-" + ("0" + d.getDate()).slice(-2); }
  function dayShift(n) { var d = new Date(); d.setHours(12, 0, 0, 0); d.setDate(d.getDate() + n); return d; }
  function today() { return ymd(new Date()); }

  // ---- 저장 ----
  var memOnly = false;
  function blank() { return { v: 1, xp: 0, set: "common", seen: {}, days: {}, mission: null, best: 0, miss: [0, 0, 0, 0], perfect: 0, ontime: 0, total: 0, badges: {} }; }
  function load() {
    try {
      var s = JSON.parse(localStorage.getItem(KEY) || "null");
      if (s && s.v === 1) {
        var b = blank(); for (var k in b) if (!(k in s) || typeof s[k] !== typeof b[k] || s[k] === null) s[k] = b[k];
        // 저장소 값이 화면 HTML 에 숫자로 들어가므로 숫자로만 받는다
        ["xp", "best", "perfect", "ontime", "total"].forEach(function (f) { s[f] = Math.max(0, Math.floor(+s[f]) || 0); });
        s.miss = [0, 1, 2, 3].map(function (i) { return Math.max(0, Math.floor(+(s.miss || [])[i]) || 0); });
        for (var d in s.days) s.days[d] = { n: Math.max(0, Math.floor(+(s.days[d] || {}).n) || 0), done: !!(s.days[d] || {}).done };
        if (typeof s.set !== "string") s.set = "common";
        return s;
      }
    } catch (e) { memOnly = true; }
    return blank();
  }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) { memOnly = true; } }
  var S = load();

  // ---- 계산 ----
  function hash(t) { var h = 5381; for (var i = 0; i < t.length; i++) h = ((h << 5) + h + t.charCodeAt(i)) | 0; return (h >>> 0).toString(36); }
  function level(xp) { var L = 1; while (xp >= 30 * L * (L + 1)) L++; return L; }
  function title(L) { return L <= TITLES.length ? TITLES[L - 1] : "면접각 고수"; }
  function countDone(s) { var n = 0; for (var k in s.days) if (s.days[k].done) n++; return n; }
  function streak() {
    var i = S.days[today()] && S.days[today()].done ? 0 : -1, n = 0;
    while (S.days[ymd(dayShift(i))] && S.days[ymd(dayShift(i))].done) { n++; i--; }
    return n;
  }
  function fmt(s) { return Math.floor(s / 60) + ":" + ("0" + (s % 60)).slice(-2); }

  // ---- 화면 요소 ----
  var sel = $("gmSet"), slots = $("gmSlots"), card = $("gmCard"), meta = $("gmMeta"), qEl = $("gmQ");
  var timerBox = $("gmTimerBox"), barBox = $("gmBarBox"), phaseEl = $("gmPhase"), timeEl = $("gmTime"), bar = $("gmBar");
  var bGo = $("gmGo"), bAns = $("gmAns"), bStop = $("gmStop"), bSkip = $("gmSkip"), bNext = $("gmNext"), bMore = $("gmMore");
  var form = $("gmCheck"), ckTime = $("gmCkTime"), timeNote = $("gmTimeNote"), said = $("gmSaid");
  var after = $("gmAfter"), gain = $("gmGain"), exWrap = $("gmExWrap"), exEl = $("gmEx"), done = $("gmDone");

  var DATA = null, byId = {}, cur = null, extra = false, phase = "idle", timer = null, left = 0, total = 0, spoke = 0, retry = false;

  function setOf(id) { return byId[id] || byId.common; }
  function itemOf(c) {
    var s = setOf(c.s);
    for (var i = 0; i < s.items.length; i++) if (s.items[i].q === c.q) return s.items[i];
    return null;
  }
  // 아직 답하지 않은 질문을 먼저, 오늘 이미 뽑은 질문은 빼고 고른다
  function pick(setId, avoid) {
    var s = setOf(setId), fresh = [], all = [];
    s.items.forEach(function (it) {
      if (avoid.indexOf(it.q) >= 0) return;
      all.push(it); if (!S.seen[hash(it.q)]) fresh.push(it);
    });
    var pool = fresh.length ? fresh : all.length ? all : s.items;
    return { s: s.id, q: pool[Math.floor(Math.random() * pool.length)].q, ok: false };
  }
  function newMission() {
    var cards = [], avoid = [];
    for (var i = 0; i < PER_DAY; i++) { var c = pick(S.set, avoid); avoid.push(c.q); cards.push(c); }
    S.mission = { d: today(), cards: cards }; save();
  }
  function ensureMission() {
    var m = S.mission;
    var started = m && m.d === today() && m.cards.some(function (c) { return c.ok; });
    if (!m || m.d !== today()) return newMission();
    // 질문 데이터가 바뀌어 사라진 카드는 새로 뽑는다
    m.cards.forEach(function (c, i) { if (!c.ok && !itemOf(c)) m.cards[i] = pick(c.s, m.cards.map(function (x) { return x.q; })); });
    if (!started && m.cards.some(function (c) { return c.s !== S.set; })) newMission();
    save();
  }
  function missionIndex() { for (var i = 0; i < S.mission.cards.length; i++) if (!S.mission.cards[i].ok) return i; return -1; }

  // ---- 그리기 ----
  function renderHud() {
    var L = level(S.xp), lo = 30 * (L - 1) * L, hi = 30 * L * (L + 1);
    $("gmLv").textContent = "Lv." + L; $("gmTitle").textContent = title(L);
    $("gmXpBar").style.width = Math.round(100 * (S.xp - lo) / (hi - lo)) + "%";
    $("gmXpText").textContent = S.xp + " / " + hi + " XP";
    $("gmStreak").textContent = streak();
    $("gmToday").textContent = S.mission.cards.filter(function (c) { return c.ok; }).length + "/" + PER_DAY;
  }
  function renderSlots() {
    var idx = extra ? -1 : missionIndex();
    slots.innerHTML = "";
    S.mission.cards.forEach(function (c, i) {
      var li = document.createElement("li");
      li.className = "gm-slot" + (c.ok ? " ok" : i === idx ? " now" : "");
      li.innerHTML = "<b>" + (c.ok ? "✓" : i + 1) + "</b><span>" + (c.ok ? "완료" : i === idx ? "지금" : "대기") + "</span>";
      slots.appendChild(li);
    });
  }
  function renderStats() {
    var w = $("gmWeek"), DOW = ["일", "월", "화", "수", "목", "금", "토"];
    w.innerHTML = "";
    for (var i = -6; i <= 0; i++) {
      var d = dayShift(i), k = ymd(d), on = S.days[k] && S.days[k].done, part = S.days[k] && S.days[k].n;
      var el = document.createElement("span");
      el.className = "gm-day" + (on ? " on" : part ? " part" : "") + (i === 0 ? " today" : "");
      el.innerHTML = "<i>" + (on ? "✓" : part ? part : "") + "</i><small>" + (i === 0 ? "오늘" : DOW[d.getDay()]) + "</small>";
      el.title = k + (on ? " 미션 완료" : part ? " " + part + "장" : "");
      w.appendChild(el);
    }
    $("gmNums").innerHTML =
      "<li><b>" + S.total + "</b>번 답변</li><li><b>" + Object.keys(S.seen).length + "</b>개 질문</li>" +
      "<li><b>" + S.best + "</b>일 최고 연속</li><li><b>" + S.perfect + "</b>번 4체크</li>";
    var weak = $("gmWeak");
    if (S.total >= 3) {
      var m = 0; for (var j = 1; j < 4; j++) if (S.miss[j] > S.miss[m]) m = j;
      if (S.miss[m] > 0) {
        weak.hidden = false;
        weak.innerHTML = "자주 놓친 체크: <b>" + CHECKS[m] + "</b> (" + S.miss[m] + "번) — " + WEAK_TIP[m];
      } else { weak.hidden = false; weak.innerHTML = "지금까지 4개 체크를 한 번도 놓치지 않았습니다. 더 어려운 학과 질문 묶음에도 도전해 보세요."; }
    } else weak.hidden = true;
    var ul = $("gmBadges"); ul.innerHTML = "";
    BADGES.forEach(function (b) {
      var li = document.createElement("li"), on = !!S.badges[b[0]];
      li.className = "gm-badge" + (on ? " on" : "");
      li.innerHTML = "<b>" + (on ? "★ " : "☆ ") + b[1] + "</b><small>" + b[2] + "</small>";
      ul.appendChild(li);
    });
  }
  function show(el, on) { el.hidden = !on; }
  function setPhase(p) {
    phase = p;
    show(timerBox, p === "prep" || p === "answer"); show(barBox, p === "prep" || p === "answer");
    show(bGo, p === "idle"); show(bAns, p === "prep"); show(bSkip, p === "idle" || p === "prep"); show(bStop, p === "answer");
    show($("gmBtns"), p === "idle" || p === "prep" || p === "answer");
    show(form, p === "check"); show(after, p === "after");
  }
  function renderCard() {
    renderHud(); renderSlots(); renderStats();
    var idx = missionIndex();
    if (!extra && idx < 0) {
      show(card, false); show(done, true);
      var st = streak();
      $("gmDoneText").textContent = (st >= 2 ? st + "일 연속 완료 중입니다. " : "") + "내일 또 3장을 하면 연속 기록이 이어집니다. 더 하고 싶으면 한 장씩 더 연습할 수 있습니다(연속 기록과 별개로 경험치는 받습니다).";
      return;
    }
    show(card, true); show(done, false);
    if (!cur) cur = extra ? pick(S.set, S.mission.cards.map(function (c) { return c.q; })) : S.mission.cards[idx];
    var s = setOf(cur.s);
    meta.textContent = (extra ? "한 장 더" : "오늘의 카드 " + (idx + 1) + " / " + PER_DAY) + " · " + s.label.replace(/^자주 나오는 /, "");
    qEl.className = "gm-q back";
    qEl.textContent = "카드를 뒤집으면 질문이 나오고 생각 15초가 시작됩니다.";
    bGo.disabled = false; bSkip.textContent = "다른 카드로";
    setPhase("idle");
  }

  // ---- 타이머 ----
  function run(sec, name) {
    clearInterval(timer); left = total = sec;
    setPhase(name);
    phaseEl.textContent = name === "prep" ? "생각하는 시간 — 결론 한 문장만 정하세요" : "답변 중 — 소리 내어 말하세요";
    timeEl.textContent = fmt(sec); bar.style.width = "0%"; bar.className = name === "answer" ? "ans" : "";
    timer = setInterval(function () {
      left -= 1; timeEl.textContent = fmt(Math.max(left, 0));
      bar.style.width = (100 * (total - left) / total) + "%";
      if (left <= 0) { if (phase === "prep") startAnswer(); else if (phase === "answer") stopAnswer(); }
    }, 1000);
  }
  function flip() {
    var it = itemOf(cur); if (!it) { cur = null; renderCard(); return; }
    qEl.className = "gm-q"; qEl.textContent = it.q;
    run(PREP, "prep"); ev("play_flip");
    into(card);
  }
  // 휴대폰에서 카드가 화면 밖(또는 위 고정 메뉴 밑)에 있으면 보이게 올린다
  function into(el) {
    try { var r = el.getBoundingClientRect(); if (r.top < 60 || r.top > innerHeight * 0.5) el.scrollIntoView({ block: "start", behavior: "smooth" }); } catch (e) {}
  }
  function startAnswer() { run(ANSWER, "answer"); }
  function stopAnswer() {
    clearInterval(timer);
    spoke = total - Math.max(left, 0);
    if (spoke < MIN_SEC) {
      setPhase("after"); retry = true;
      gain.innerHTML = "답변이 <b>" + spoke + "초</b>로 짧아 기록하지 않았습니다. 결론 → 경험 → 배운 점 순서로 20초 이상 말해 보세요.";
      exWrap.hidden = true; bNext.textContent = "이 카드 다시 하기";
      return;
    }
    var ontime = left > 0;
    form.reset(); ckTime.checked = ontime; ckTime.disabled = true;
    timeNote.textContent = ontime ? "(" + spoke + "초 — 자동 체크)" : "(60초가 다 됐어요 — 다음엔 50초 안에)";
    said.textContent = "답변 " + spoke + "초" + (ontime ? "" : " · 시간 초과");
    setPhase("check");
  }

  // ---- 기록 ----
  function record(e) {
    e.preventDefault();
    var boxes = form.querySelectorAll("input[name=c]"), n = 0, msgs = [];
    for (var i = 0; i < boxes.length; i++) { if (boxes[i].checked) n++; else S.miss[i]++; }
    var xp = 10 + 5 * n;
    S.total++; S.seen[hash(cur.q)] = 1;
    if (n === 4) S.perfect++;
    if (ckTime.checked) S.ontime++;
    var day = S.days[today()] || (S.days[today()] = { n: 0, done: false });
    if (!extra) {
      cur.ok = true; day.n++;
      if (missionIndex() < 0 && !day.done) {
        day.done = true; xp += 20; msgs.push("오늘의 3장 완료 +20");
        var st = streak(); if (st > S.best) S.best = st;
        if (st >= 3) { xp += 10; msgs.push(st + "일 연속 +10"); }
        ev("play_mission_done", { streak: st });
      }
    }
    var before = level(S.xp); S.xp += xp; var after_ = level(S.xp);
    if (after_ > before) msgs.push("레벨 업! Lv." + after_ + " " + title(after_));
    BADGES.forEach(function (b) { if (!S.badges[b[0]] && b[3](S)) { S.badges[b[0]] = today(); msgs.push("배지 ★ " + b[1]); } });
    save(); ev("play_record", { checks: n, extra: extra ? 1 : 0 });

    var it = itemOf(cur) || { ex: "", tip: "", u: "" };
    gain.innerHTML = "<b class=\"gm-plus\">+" + xp + " XP</b> " + msgs.map(function (m) { return "<span class=\"gm-msg\">" + m + "</span>"; }).join(" ");
    exEl.innerHTML = "";
    if (it.ex) { var p = document.createElement("p"); p.className = "gm-exans"; p.textContent = it.ex; exEl.appendChild(p); }
    if (it.tip) { var t = document.createElement("p"); t.className = "gm-tip"; t.textContent = "주의할 점: " + it.tip; exEl.appendChild(t); }
    if (it.u) { var a = document.createElement("a"); a.href = it.u; a.textContent = "이 질문 자세히 보기 ›"; exEl.appendChild(a); }
    exWrap.open = false; exWrap.hidden = !exEl.childNodes.length;
    bNext.textContent = !extra && missionIndex() < 0 ? "결과 보기" : "다음 카드";
    retry = false; setPhase("after");
    renderHud(); renderSlots(); renderStats();
  }
  function next() {
    if (retry) { retry = false; flip(); return; }
    cur = null; renderCard();
    into(card.hidden ? done : card);
  }
  function skip() {
    clearInterval(timer);
    var avoid = S.mission.cards.map(function (c) { return c.q; });
    var c = pick(cur.s, avoid);
    if (!extra) { var idx = missionIndex(); S.mission.cards[idx] = c; save(); }
    cur = c; renderCard();
  }

  // ---- 시작 ----
  function fillSets() {
    var common = DATA.sets.filter(function (s) { return s.id === "common"; });
    var depts = DATA.sets.filter(function (s) { return s.id !== "common"; }).sort(function (a, b) { return a.label.localeCompare(b.label, "ko"); });
    sel.innerHTML = "";
    common.forEach(function (s) { var o = document.createElement("option"); o.value = s.id; o.textContent = "공통 질문 · " + s.items.length + "장"; sel.appendChild(o); });
    var og = document.createElement("optgroup"); og.label = "학과별 질문 (" + depts.length + ")";
    depts.forEach(function (s) { var o = document.createElement("option"); o.value = s.id; o.textContent = s.label + " · " + s.items.length + "장"; og.appendChild(o); });
    sel.appendChild(og);
    if (!byId[S.set]) S.set = "common";
    sel.value = S.set;
  }
  sel.addEventListener("change", function () {
    S.set = sel.value; save(); clearInterval(timer);
    var started = S.mission.cards.some(function (c) { return c.ok; });
    if (!started) newMission();
    cur = null; renderCard();
    if (started) meta.textContent += " · 바꾼 묶음은 남은 카드를 '다른 카드로' 넘기거나 내일부터 적용됩니다";
    ev("play_set", { set: S.set.split(":")[0] });
  });
  bGo.addEventListener("click", flip);
  bAns.addEventListener("click", startAnswer);
  bStop.addEventListener("click", stopAnswer);
  bSkip.addEventListener("click", skip);
  bNext.addEventListener("click", next);
  bMore.addEventListener("click", function () { extra = true; cur = null; renderCard(); });
  form.addEventListener("submit", record);
  $("gmReset").addEventListener("click", function () {
    if (!confirm("레벨·경험치·연속 기록·배지를 모두 지울까요? 되돌릴 수 없습니다.")) return;
    try { localStorage.removeItem(KEY); } catch (e) {}
    S = blank(); extra = false; cur = null; clearInterval(timer);
    fillSets(); newMission(); renderCard();
  });
  // 날짜가 바뀐 채로 탭을 다시 열면 새 미션으로
  document.addEventListener("visibilitychange", function () {
    if (!document.hidden && DATA && S.mission && S.mission.d !== today() && phase === "idle") { extra = false; cur = null; ensureMission(); renderCard(); }
  });

  fetch(window.PLAY_URL || "/play/questions.json").then(function (r) { return r.json(); }).then(function (d) {
    DATA = d; d.sets.forEach(function (s) { byId[s.id] = s; });
    fillSets(); ensureMission(); renderCard();
    if (memOnly) meta.textContent += " · 이 브라우저는 기록 저장이 막혀 있어, 페이지를 닫으면 기록이 사라집니다";
  }).catch(function () {
    meta.textContent = "질문을 불러오지 못했습니다.";
    qEl.textContent = "인터넷 연결을 확인하고 새로고침해 주세요.";
  });
})();
