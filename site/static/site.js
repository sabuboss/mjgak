/* 사이트 검색: search.json 을 받아 부분 일치로 거른다. 서버 없음. 모든 .search 상자에 적용. */
(function () {
  var boxes = document.querySelectorAll(".search");
  if (!boxes.length) return;
  var data = null, loading = null;
  function load(cb) {
    if (data) return cb();
    if (!loading) loading = fetch("/search.json").then(function (r) { return r.json(); }).then(function (d) { data = d; });
    loading.then(cb).catch(function () {});
  }
  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function norm(s) { return s.replace(/\s+/g, "").toLowerCase(); }
  function score(it, terms, q) {
    var t = norm(it.t), c = norm(it.c);
    for (var i = 0; i < terms.length; i++) if (t.indexOf(terms[i]) < 0 && c.indexOf(terms[i]) < 0) return null;
    var s = 10;
    if (it.p) s += 100;                 /* 대학·학과 페이지 항목 우선 */
    if (t.indexOf(q) === 0) s += 50;    /* 앞부분 일치 */
    else if (t.indexOf(q) >= 0) s += 20;
    s -= Math.min(t.length, 60) / 10;   /* 짧은 제목 우선 */
    return s;
  }
  function render(input, list) {
    var raw = input.value.trim();
    if (!raw) { list.hidden = true; list.innerHTML = ""; return; }
    var q = norm(raw), terms = raw.split(/\s+/).map(norm).filter(Boolean);
    var hits = data.map(function (it) { return [score(it, terms, q), it]; }).filter(function (x) { return x[0] !== null; })
      .sort(function (a, b) { return b[0] - a[0]; }).slice(0, 12).map(function (x) { return x[1]; });
    if (!hits.length) { list.innerHTML = '<li><a href="/univ/">일치하는 결과가 없습니다. 대학 목록 보기</a></li><li><a href="/dept/">학과 목록 보기</a></li>'; list.hidden = false; return; }
    list.innerHTML = hits.map(function (it) { return '<li><a href="' + it.u + '">' + esc(it.t) + "<small>" + esc(it.c) + "</small></a></li>"; }).join("");
    list.hidden = false;
  }
  boxes.forEach(function (box) {
    var input = box.querySelector("input"), list = box.querySelector("ul");
    if (!input || !list) return;
    input.addEventListener("input", function () { load(function () { render(input, list); }); });
    input.addEventListener("focus", function () { load(function () { if (input.value) render(input, list); }); });
    input.addEventListener("keydown", function (e) { if (e.key === "Enter") { var a = list.querySelector("a"); if (a && !list.hidden) location.href = a.getAttribute("href"); } });
  });
  document.addEventListener("click", function (e) { if (!e.target.closest(".search")) boxes.forEach(function (b) { var l = b.querySelector("ul"); if (l) l.hidden = true; }); });
})();
