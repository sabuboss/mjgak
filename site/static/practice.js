// 모의 면접: 질문 무작위 → 생각 15초 → 답변 60초, 선택 시 브라우저 안에서만 녹음(MediaRecorder). 서버 전송 없음.
(function () {
  var $ = function (id) { return document.getElementById(id); };
  var sel = $("prSet"), qEl = $("prQ"), meta = $("prMeta"), phaseEl = $("prPhase"), timeEl = $("prTime"), bar = $("prBar");
  var btnNext = $("prNext"), btnStart = $("prStart"), btnStop = $("prStop"), recBox = $("prRec"), audio = $("prAudio");
  var exWrap = $("prExWrap"), exEl = $("prEx"), micNote = $("prMicNote");
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
  function setOptions() {
    var params = new URLSearchParams(location.search), want = params.get("set");
    sel.innerHTML = "";
    DATA.sets.forEach(function (s) {
      var o = document.createElement("option"); o.value = s.id; o.textContent = s.label + " (" + s.items.length + "문항)";
      sel.appendChild(o);
    });
    if (want && DATA.sets.some(function (s) { return s.id === want; })) sel.value = want;
    pickSet();
  }
  function pickSet() {
    var s = DATA.sets.filter(function (x) { return x.id === sel.value; })[0];
    pool = s ? s.items.slice() : [];
    meta.textContent = s ? s.label + " · " + pool.length + "문항 중 무작위" : "";
    try { history.replaceState(null, "", "?set=" + encodeURIComponent(sel.value)); } catch (e) {}
  }
  function nextQ() {
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
    phaseEl.textContent = "끝 — 다시 들어 보세요"; btnStop.disabled = true;
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
        audio.src = lastUrl; audio.hidden = false;
      };
      rec.start();
    };
    if (stream) go(stream);
    else navigator.mediaDevices.getUserMedia({ audio: true }).then(go).catch(function () { micNote.hidden = false; recBox.checked = false; });
  }
  function stopRec() { if (rec && rec.state === "recording") rec.stop(); }

  btnNext.addEventListener("click", nextQ);
  btnStart.addEventListener("click", function () { if (phase === "prep") startAnswer(); });
  btnStop.addEventListener("click", function () { if (phase === "answer") stopAnswer(); });
  sel.addEventListener("change", pickSet);
  fetch(window.PRACTICE_URL).then(function (r) { return r.json(); }).then(function (d) { DATA = d; setOptions(); })
    .catch(function () { qEl.textContent = "질문을 불러오지 못했습니다. 새로고침해 주세요."; });
})();
