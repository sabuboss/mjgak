/* 홈 전용: 다가오는 1단계 발표·면접 카드.
   /planner/data.json 을 읽어 이용자 기기 날짜 기준 오늘부터 14일 안의 일정을 날짜별 카드(최대 6장)로 보여 준다.
   (일정표 planner.js 의 upcoming() 과 같은 규칙) 실패하거나 일정이 없으면 처음 넣어 둔 '일정표 보기' 카드가 그대로 남는다. */
(function () {
  var box = document.getElementById("upc");
  if (!box || !window.fetch) return;
  var P = box.getAttribute("data-pfx") || "up", src = box.getAttribute("data-src") || "/planner/data.json";
  var WD = "일월화수목금토", MAX_DAYS = 6, MAX_ITEMS = 3;
  function esc(s) { var d = document.createElement("div"); d.textContent = s || ""; return d.innerHTML; }
  function day(iso) { var p = iso.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function isoOf(d) { return d.getFullYear() + "-" + ("0" + (d.getMonth() + 1)).slice(-2) + "-" + ("0" + d.getDate()).slice(-2); }
  var now = new Date(), t0 = new Date(now.getFullYear(), now.getMonth(), now.getDate()), today = isoOf(t0);
  var end = isoOf(new Date(t0.getFullYear(), t0.getMonth(), t0.getDate() + 14));

  fetch(src).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); }).then(function (d) {
    var ev = {};
    function add(iso, k, u, tr) {
      if (!iso || iso < today || iso > end) return;
      var g = ev[iso] = ev[iso] || {}, key = k + "|" + u.c;
      (g[key] = g[key] || { k: k, u: u, tr: [] }).tr.push(tr.n);
    }
    (d.univs || []).forEach(function (u) {
      (u.t || []).forEach(function (tr) {
        add(tr.f, "f", u, tr);
        (tr.d || []).forEach(function (x) { add(x, "iv", u, tr); });
      });
    });
    var days = Object.keys(ev).sort().slice(0, MAX_DAYS);
    if (!days.length) return;
    box.innerHTML = days.map(function (iso, i) {
      var dd = day(iso), n = Math.round((dd - t0) / 864e5);
      var items = Object.keys(ev[iso]).map(function (k) { return ev[iso][k]; })
        .sort(function (a, b) { return a.k === b.k ? (a.u.n < b.u.n ? -1 : 1) : (a.k === "f" ? -1 : 1); });
      var nf = items.filter(function (x) { return x.k === "f"; }).length, ni = items.length - nf;
      var count = (nf ? "1단계 발표 " + nf + "곳" : "") + (nf && ni ? " · " : "") + (ni ? "면접 " + ni + "곳" : "");
      var more = items.length - MAX_ITEMS;
      return '<article class="' + P + "-uc " + P + "-uc-" + i + '">' +
        '<p class="' + P + '-uc-d"><b>' + (n === 0 ? "오늘" : "D-" + n) + "</b> " + (dd.getMonth() + 1) + "월 " + dd.getDate() + "일(" + WD[dd.getDay()] + ")</p>" +
        '<p class="' + P + '-uc-c">' + count + "</p><ul>" +
        items.slice(0, MAX_ITEMS).map(function (x) {
          return '<li><span class="' + P + "-uc-k" + (x.k === "iv" ? " " + P + "-uc-iv" : "") + '">' + (x.k === "iv" ? "면접" : "1단계") + "</span>" +
            '<a href="' + x.u.u + '">' + esc(x.u.n) + "</a>" + (x.tr.length > 1 ? " <small>전형 " + x.tr.length + "개</small>" : "") + "</li>";
        }).join("") + "</ul>" +
        (more > 0 ? '<a class="' + P + '-uc-more" href="/planner/">+ ' + more + "곳 더 보기</a>" : "") + "</article>";
    }).join("");
  }).catch(function () { /* 처음 넣어 둔 '일정표 보기' 카드를 그대로 둔다 */ });
})();
