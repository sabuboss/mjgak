/* 홈 검색: search.json 을 받아 제목을 부분 일치로 거른다. 서버 없음. */
(function () {
  var input = document.getElementById("q"), list = document.getElementById("qr");
  if (!input || !list) return;
  var data = null;
  function load(cb) {
    if (data) return cb();
    fetch("/mjgak/search.json").then(function (r) { return r.json(); }).then(function (d) { data = d; cb(); }).catch(function () {});
  }
  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function render(q) {
    q = q.trim();
    if (!q) { list.hidden = true; list.innerHTML = ""; return; }
    var terms = q.split(/\s+/);
    var hits = data.filter(function (it) { return terms.every(function (t) { return it.t.indexOf(t) >= 0 || it.c.indexOf(t) >= 0; }); }).slice(0, 12);
    if (!hits.length) { list.innerHTML = '<li><a href="/mjgak/category/intro/">일치하는 질문이 없습니다. 전체 목록 보기</a></li>'; list.hidden = false; return; }
    list.innerHTML = hits.map(function (it) { return '<li><a href="' + it.u + '">' + esc(it.t) + "<small>" + esc(it.c) + "</small></a></li>"; }).join("");
    list.hidden = false;
  }
  input.addEventListener("input", function () { load(function () { render(input.value); }); });
  input.addEventListener("focus", function () { load(function () {}); });
  document.addEventListener("click", function (e) { if (!e.target.closest(".search")) list.hidden = true; });
})();
