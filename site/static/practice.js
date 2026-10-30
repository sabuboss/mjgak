// 모의 면접: 질문 무작위 → 생각 15초 → 답변 60초, 선택 시 브라우저 안에서만 녹음(MediaRecorder). 서버 전송 없음.
(function () {
  var $ = function (id) { return document.getElementById(id); };
  var sel = $("prSet"), qEl = $("prQ"), meta = $("prMeta"), phaseEl = $("prPhase"), timeEl = $("prTime"), bar = $("prBar");
  var btnNext = $("prNext"), btnStart = $("prStart"), btnStop = $("prStop"), recBox = $("prRec"), audio = $("prAudio");
  var exWrap = $("prExWrap"), exEl = $("prEx"), micNote = $("prMicNote");
  var findEl = $("prFind"), findNote = $("prFindNote"), chipEl = $("prChips");
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
  function find() {
    var q = findEl.value.trim().replace(/\s+/g, "");
    var list = !q ? DATA.sets : DATA.sets.filter(function (s) { return s.label.replace(/\s+/g, "").indexOf(q) >= 0; });
    if (!list.length) {
      findNote.innerHTML = "‘" + esc(findEl.value.trim()) + "’ 묶음이 없습니다. 대학이 질문을 공개하지 않았다면 <b>공통 질문</b>이나 지원 학과 질문으로 연습하세요.";
      fill(DATA.sets); return;
    }
    findNote.textContent = q ? list.length + "개 찾음" + (list.length > 1 ? " — 아래 목록에서 고르세요" : "") : "";
    fill(list);
    if (q && list.every(function (s) { return s.id !== sel.value; })) sel.value = list[0].id;
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
    if (want && DATA.sets.some(function (s) { return s.id === want; })) sel.value = want;
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
  }
  function startAnswer() {
    btnStart.disabled = true; btnStop.disabled = false;
    run(ANSWER, "answer");
    if (recBox.checked) startRec();
  }
  function stopAnswer() {
    clearInterval(timer); phase = "done";
    phaseEl.textContent = recBox.checked ? "끝 — ▶ 눌러 내 답변 다시 듣기" : "끝"; btnStop.disabled = true;
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
  chipEl.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest(".pr-chip"); if (!b) return;
    findEl.value = ""; findNote.textContent = ""; fill(DATA.sets); sel.value = b.getAttribute("data-id"); pickSet();
  });
  fetch(window.PRACTICE_URL).then(function (r) { return r.json(); }).then(function (d) { DATA = d; setOptions(); })
    .catch(function () { qEl.textContent = "질문을 불러오지 못했습니다. 새로고침해 주세요."; });
})();
