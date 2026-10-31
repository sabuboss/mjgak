// 모의 면접: 질문 무작위 → 생각 15초 → 답변 60초, 선택 시 브라우저 안에서만 녹음(MediaRecorder). 서버 전송 없음.
(function () {
  var $ = function (id) { return document.getElementById(id); };
  var sel = $("prSet"), qEl = $("prQ"), meta = $("prMeta"), phaseEl = $("prPhase"), timeEl = $("prTime"), bar = $("prBar");
  var btnNext = $("prNext"), btnStart = $("prStart"), btnStop = $("prStop"), recBox = $("prRec"), audio = $("prAudio");
  var exWrap = $("prExWrap"), exEl = $("prEx"), micNote = $("prMicNote");
  var findEl = $("prFind"), findNote = $("prFindNote"), chipEl = $("prChips"), findBox = $("prFindBox");
  var wide = window.matchMedia && matchMedia("(min-width: 561px)").matches;
  // 사용 흐름을 GA4 이벤트로 남긴다(질문·녹음 내용은 보내지 않음) — 실제로 연습까지 가는지 보려고
  function ev(name, p) { try { if (window.gtag) gtag("event", name, p || {}); } catch (e) {} }
  var DATA = null, pool = [], cur = null, timer = null, left = 0, total = 0, phase = "idle";
  var stream = null, rec = null, chunks = [], lastUrl = null;
  var PREP = 15, ANSWER = 60;

  function fmt(s) { return Math.floor(s / 60) + ":" + ("0" + (s % 60)).slice(-2); }
  function esc(s) { var d = document.createElement("div"); d.textContent = s || ""; return d.innerHTML; }
  function tick() {
    left -= 1;
    timeEl.textContent = fmt(Math.max(left, 0));
    bar.style.width = (100 * (total - left) / total) + "%";
    if (left <= 0) { if (phase === "prep") startAnswer(); else if (phase === "answer") stopAnswer(); }
  }
  function run(sec, name) {
    clearInterval(timer); left = total = sec; phase = name;
    phaseEl.textContent = name === "prep" ? "생각하는 시간" : "답변 중";
    timeEl.textContent = fmt(sec); bar.style.width = "0%";
    bar.className = name === "answer" ? "ans" : "";
    timer = setInterval(tick, 1000);
  }
  // 질문 묶음: 공통 / 대학 공개 질문 / 학과(가나다순) 세 갈래로 묶고, 이름 검색·바로가기 칩으로 고른다
  var GROUPS = [["common", "공통"], ["univ", "대학이 공개한 질문"], ["dept", "학과별 질문"]];
  var CHIPS = ["공통", "간호학과", "경영학과", "컴퓨터", "유아교육", "의예과", "심리학과", "기계공학"];
  function kind(s) { return s.id === "common" ? "common" : s.id.split(":")[0]; }
  function short(s) { return s.label.replace(/^학과 · /, "").replace(/^대학 공개 질문 · /, ""); }
  function fill(list) {
    var keep = sel.value;
    sel.innerHTML = "";
    GROUPS.forEach(function (g) {
      var xs = list.filter(function (s) { return kind(s) === g[0]; });
      if (!xs.length) return;
      if (g[0] === "dept") xs.sort(function (a, b) { return short(a).localeCompare(short(b), "ko"); });
      var og = document.createElement("optgroup"); og.label = g[1] + " (" + xs.length + ")";
      xs.forEach(function (s) {
        var o = document.createElement("option"); o.value = s.id; o.textContent = short(s) + " · " + s.items.length + "문항";
        og.appendChild(o);
      });
      sel.appendChild(og);
    });
    if (list.some(function (s) { return s.id === keep; })) sel.value = keep;
  }
  // 줄임말 → 목록에 있는 말
  var ALIAS = [[/컴공/, "컴퓨터"], [/한의대/, "한의예"], [/치대/, "치의예"], [/의대/, "의예"], [/약대/, "약학"], [/간호대/, "간호"],
    [/수의대/, "수의예"], [/교대/, "교육"], [/경영대/, "경영"], [/소프트웨어|소웨/, "소프트웨어"], [/전전/, "전자"], [/기계과/, "기계"]];
  function find() {
    var q = findEl.value.trim().replace(/\s+/g, "");
    ALIAS.forEach(function (a) { q = q.replace(a[0], a[1]); });
    var hit = function (s) { var l = s.label.replace(/\s+/g, ""); return l.indexOf(q) >= 0 || (q.length > 2 && /대$/.test(q) && l.indexOf(q.slice(0, -1)) >= 0); };
    var list = !q ? DATA.sets : DATA.sets.filter(hit);
    if (!list.length) {
      // 없는 대학을 찾으면 앞서 고른 묶음에 머무르지 않고 공통 질문으로 바꿔 준다
      findNote.innerHTML = "‘" + esc(findEl.value.trim()) + "’ 묶음은 없어 <b>공통 질문</b>으로 바꿨습니다. 대학이 질문을 공개하지 않은 곳은 공통·학과 질문으로 연습하세요(학과 이름으로도 찾아 보세요).";
      fill(DATA.sets); sel.value = "common"; pickSet(); return;
    }
    findNote.textContent = q ? list.length + "개 찾음" + (list.length > 1 ? " — 아래 목록에서 고르세요" : "") : "";
    var prev = sel.value;  // fill() 뒤엔 목록 첫 항목이 자동 선택되므로 그 전에 기억
    fill(list);
    if (q && list.every(function (s) { return s.id !== prev; })) {
      // 이름이 검색어로 시작하는 묶음을 먼저(의대 → 수의예과보다 의예과)
      var first = list.filter(function (s) { return short(s).replace(/\s+/g, "").indexOf(q) === 0; })[0] || list[0];
      sel.value = first.id;
    }
    pickSet();
  }
  function chips() {
    chipEl.innerHTML = CHIPS.map(function (k) {
      var s = DATA.sets.filter(function (x) { return x.label.indexOf(k) >= 0; })[0];
      return s ? '<button type="button" class="pr-chip" data-id="' + s.id + '">' + esc(k === "공통" ? "공통 질문" : short(s)) + "</button>" : "";
    }).join("");
  }
  function setOptions() {
    var params = new URLSearchParams(location.search), want = params.get("set");
    fill(DATA.sets); chips();
    var given = want && DATA.sets.some(function (s) { return s.id === want; });
    if (given) sel.value = want;
    // 휴대폰에선 찾기 칸을 접어 두어 첫 화면에 질문 뽑기가 보이게 한다
    findBox.open = wide && !given;
    pickSet();
  }
  function pickSet() {
    var s = DATA.sets.filter(function (x) { return x.id === sel.value; })[0];
    pool = s ? s.items.slice() : [];
    meta.textContent = s ? s.label + " · " + pool.length + "문항 중 무작위" : "";
    try { history.replaceState(null, "", "?set=" + encodeURIComponent(sel.value) + location.hash); } catch (e) {}
  }
  function nextQ() {
    stopRec();
    if (!pool.length) pickSet();
    var i = Math.floor(Math.random() * pool.length);
    cur = pool.splice(i, 1)[0];
    qEl.innerHTML = esc(cur.q);
    exWrap.hidden = true; exWrap.open = false;
    exEl.innerHTML = (cur.ex ? "<p><b>답변 예시</b> " + esc(cur.ex) + "</p>" : "") + (cur.tip ? "<p><b>주의</b> " + esc(cur.tip) + "</p>" : "") +
      (cur.u ? '<p><a href="' + cur.u + '">이 질문이 있는 페이지에서 자세히 보기</a></p>' : "");
    audio.hidden = true;
    btnStart.disabled = false; btnStop.disabled = true;
    run(PREP, "prep");
    ev("practice_draw", { set_id: sel.value });
  }
  function startAnswer() {
    btnStart.disabled = true; btnStop.disabled = false;
    run(ANSWER, "answer");
    if (recBox.checked) startRec();
    ev("practice_answer", { set_id: sel.value, rec: recBox.checked ? 1 : 0 });
  }
  function stopAnswer() {
    clearInterval(timer); phase = "done";
    // 남은 시간 대신 실제로 말한 시간을 보여 준다(60초 안에 끝냈는지 바로 보이게)
    var used = total - Math.max(left, 0);
    timeEl.textContent = fmt(used); bar.style.width = (100 * used / total) + "%";
    phaseEl.textContent = "답변한 시간" + (recBox.checked ? " — ▶ 눌러 다시 듣기" : ""); btnStop.disabled = true;
    ev("practice_done", { set_id: sel.value, sec: used });
    stopRec();
    if (cur && (cur.ex || cur.tip || cur.u)) exWrap.hidden = false;
  }
  function startRec() {
    if (!navigator.mediaDevices || !window.MediaRecorder) { micNote.hidden = false; return; }
    var go = function (s) {
      stream = s; chunks = [];
      try { rec = new MediaRecorder(s); } catch (e) { micNote.hidden = false; return; }
      rec.ondataavailable = function (e) { if (e.data && e.data.size) chunks.push(e.data); };
      rec.onstop = function () {
        if (lastUrl) URL.revokeObjectURL(lastUrl);
        lastUrl = URL.createObjectURL(new Blob(chunks, { type: rec.mimeType || "audio/webm" }));
        audio.src = lastUrl; audio.hidden = phase !== "done";
        // 녹음이 끝나면 마이크를 바로 놓는다(다음 녹음 때 다시 켬)
        if (stream) { stream.getTracks().forEach(function (t) { t.stop(); }); stream = null; }
      };
      rec.start();
      if (phase === "answer") phaseEl.innerHTML = '답변 중 · <span class="pr-rec">● 녹음 중</span>';
    };
    if (stream) go(stream);
    else navigator.mediaDevices.getUserMedia({ audio: true }).then(go).catch(function () { micNote.hidden = false; recBox.checked = false; });
  }
  function stopRec() { if (rec && rec.state === "recording") rec.stop(); }

  btnNext.addEventListener("click", nextQ);
  btnStart.addEventListener("click", function () { if (phase === "prep") startAnswer(); });
  btnStop.addEventListener("click", function () { if (phase === "answer") stopAnswer(); });
  sel.addEventListener("change", pickSet);
  findEl.addEventListener("input", find);
  // 찾은 게 없던 검색어만 남긴다(어느 대학·학과 묶음을 더 만들지 정하려고)
  findEl.addEventListener("change", function () {
    var q = findEl.value.trim();
    if (q && /없어/.test(findNote.textContent)) ev("practice_nofind", { search_term: q.slice(0, 30) });
  });
  chipEl.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest(".pr-chip"); if (!b) return;
    findEl.value = ""; findNote.textContent = ""; fill(DATA.sets); sel.value = b.getAttribute("data-id"); pickSet();
    if (!wide) findBox.open = false;
  });
  exWrap.addEventListener("toggle", function () { if (exWrap.open) ev("practice_example", { set_id: sel.value }); });
  fetch(window.PRACTICE_URL).then(function (r) { return r.json(); }).then(function (d) { DATA = d; setOptions(); })
    .catch(function () { qEl.textContent = "질문을 불러오지 못했습니다. 새로고침해 주세요."; });
})();
