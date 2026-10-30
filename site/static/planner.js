// 내 면접 일정표: 고른 전형의 1단계 발표일·면접일을 날짜순으로 보여 주고 같은 날 면접 겹침을 표시한다.
// 고른 전형은 주소(?t=)와 이 기기 localStorage 에만 저장한다. 서버 전송 없음.
(function () {
  var $ = function (id) { return document.getElementById(id); };
  var KEY = "mjgak-planner", WD = "일월화수목금토";
  var listEl = $("plList"), qEl = $("plQ"), tl = $("plTimeline"), nEl = $("plN"), warn = $("plWarn"), go = $("plGo"), goN = $("plGoN");
  var DATA = null, byId = {}, picked = [];

  function esc(s) { var d = document.createElement("div"); d.textContent = s || ""; return d.innerHTML; }
  function day(iso) { var p = iso.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function label(iso) { var d = day(iso); return (d.getMonth() + 1) + "/" + d.getDate() + "(" + WD[d.getDay()] + ")"; }
  function dleft(iso) {
    var n = Math.round((day(iso) - day(DATA.today_local)) / 864e5);
    return n === 0 ? "오늘" : n > 0 ? "D-" + n : "지남";
  }
  // 여러 날짜가 섞인 설명에서 그날 조각만 고른다 ("11/21(토) 인문… · 11/22(일) 자연…")
  function seg(dt, iso) {
    var d = day(iso), key = (d.getMonth() + 1) + "/" + d.getDate();
    var re = new RegExp("(^|[^0-9])" + key.replace("/", "\/") + "(?![0-9])");
    var hit = dt.split(/\s·\s/).filter(function (x) { return re.test(x); });
    return hit.length ? hit.join(" · ") : dt;
  }
  function save() {
    try { localStorage.setItem(KEY, picked.join(",")); } catch (e) {}
    try { history.replaceState(null, "", picked.length ? "?t=" + encodeURIComponent(picked.join(",")) : location.pathname); } catch (e) {}
  }
  function load() {
    var p = new URLSearchParams(location.search), t = p.get("t"), u = p.get("u"), ids = [];
    if (t) ids = t.split(",");
    else {
      try { ids = (localStorage.getItem(KEY) || "").split(","); } catch (e) { ids = []; }
      if (u) DATA.univs.forEach(function (x) { if (x.c === u) x.t.forEach(function (tr) { if (ids.indexOf(tr.id) < 0) ids.push(tr.id); }); });
    }
    picked = ids.filter(function (id) { return byId[id]; });
    if (u) qEl.value = (DATA.univs.filter(function (x) { return x.c === u; })[0] || {}).n || "";
  }
  function renderList() {
    var q = qEl.value.trim().replace(/\s+/g, "");
    var html = DATA.univs.filter(function (x) { return !q || x.n.replace(/\s+/g, "").indexOf(q) >= 0; }).map(function (x) {
      var on = x.t.filter(function (tr) { return picked.indexOf(tr.id) >= 0; }).length;
      return '<details' + (q || on ? " open" : "") + '><summary>' + esc(x.n) + (on ? "<i>" + on + "개 고름</i>" : "") + "</summary>" +
        x.t.map(function (tr) {
          return '<label><input type="checkbox" value="' + tr.id + '"' + (picked.indexOf(tr.id) >= 0 ? " checked" : "") + '><span>' + esc(tr.n) +
            "<small>면접 " + tr.d.map(label).join(" · ") + (tr.f ? " · 1단계 " + label(tr.f) : "") + "</small></span></label>";
        }).join("") + "</details>";
    }).join("");
    var hint = !q && !picked.length ? '<p class="note pl-hint">위 칸에 대학 이름을 적거나, 아래 대학 이름을 눌러 전형을 펼치세요.</p>' : "";
    listEl.innerHTML = html ? hint + html : '<p class="note">찾는 대학이 없습니다. 이 일정표에는 2027 모집요강을 확인한 대학만 있습니다.</p>';
  }
  function renderTimeline() {
    nEl.textContent = goN.textContent = picked.length;
    go.hidden = !picked.length;
    var ev = {};
    function add(iso, o) { (ev[iso] = ev[iso] || []).push(o); }
    picked.forEach(function (id) {
      var tr = byId[id], u = tr._u;
      if (tr.f) add(tr.f, { k: "f", u: u, tr: tr });
      tr.d.forEach(function (d) { add(d, { k: "iv", u: u, tr: tr }); });
    });
    if (!picked.length) { tl.innerHTML = upcoming(); warn.hidden = true; return; }
    add(DATA.csat, { k: "cs" });
    (DATA.events || []).forEach(function (m) { add(m.date, { k: "ev", m: m }); });
    var clashes = [];
    tl.innerHTML = Object.keys(ev).sort().map(function (iso) {
      var list = ev[iso], ivU = {};
      list.forEach(function (e) { if (e.k === "iv") ivU[e.u.c] = e.u.n; });
      var names = Object.keys(ivU).map(function (c) { return ivU[c]; }), clash = names.length > 1;
      if (clash) clashes.push(label(iso) + " " + names.join("·"));
      var past = iso < DATA.today_local;
      return '<li class="' + (clash ? "clash " : "") + (past ? "past" : "") + '"><div class="pl-d">' + label(iso) + "<small>" + dleft(iso) + "</small></div><div>" +
        (clash ? '<p class="clashnote">같은 날 면접 후보 ' + names.length + "곳 — 내 모집단위 날짜를 확인하세요</p>" : "") +
        list.map(function (e) {
          if (e.k === "cs") return '<p class="ev"><span class="tag cs">수능</span>2027학년도 대학수학능력시험</p>';
          if (e.k === "ev") return '<p class="ev"><span class="tag cs">일정</span><a href="' + e.m.url + '">' + esc(e.m.label) + "</a></p>";
          var multi = e.k === "iv" && e.tr.d.length > 1;
          return '<p class="ev"><span class="tag' + (e.k === "iv" ? " iv" : "") + '">' + (e.k === "iv" ? "면접" : "1단계 발표") + "</span>" +
            '<a href="' + e.u.u + '">' + esc(e.u.n) + "</a> " + esc(e.tr.n) +
            (e.k === "iv" ? "<small>" + (multi ? "이날: " : "") + esc(multi ? seg(e.tr.dt, iso) : e.tr.dt) + "</small>" : (e.tr.ft ? "<small>" + esc(e.tr.ft) + "</small>" : "")) + "</p>";
        }).join("") + "</div></li>";
    }).join("");
    warn.hidden = !clashes.length;
    warn.innerHTML = clashes.length ? "<b>겹칠 수 있는 날</b> " + esc(clashes.join(" / ")) + ". 같은 날이라도 모집단위·시간이 다르면 둘 다 볼 수 있으니, 1단계 발표 때 개인별 고사 시간을 꼭 확인하세요." : "";
  }
  // 아직 고른 전형이 없을 때: 오늘부터 2주 안의 1단계 발표·면접을 날짜별로 미리 보여 준다(바로 담기 가능)
  function upcoming() {
    var end = new Date(day(DATA.today_local).getTime() + 14 * 864e5), ev = {};
    function add(iso, o) { if (iso >= DATA.today_local && day(iso) <= end) (ev[iso] = ev[iso] || []).push(o); }
    DATA.univs.forEach(function (u) {
      u.t.forEach(function (tr) {
        if (tr.f) add(tr.f, { k: "f", u: u, tr: tr });
        tr.d.forEach(function (d) { add(d, { k: "iv", u: u, tr: tr }); });
      });
    });
    var days = Object.keys(ev).sort();
    if (!days.length) return '<li class="note">대학 목록에서 지원한 전형을 고르세요.</li>';
    return '<li class="note pl-up-head"><b>앞으로 2주 동안의 1단계 발표·면접</b> — 지원한 전형의 <b>담기</b>를 누르거나 대학 목록에서 고르면 내 일정표가 만들어집니다.</li>' +
      days.map(function (iso) {
        var seen = {};
        var items = ev[iso].filter(function (e) { var k = e.k + e.tr.id; if (seen[k]) return false; seen[k] = 1; return true; });
        return '<li><div class="pl-d">' + label(iso) + "<small>" + dleft(iso) + "</small></div><div>" +
          items.map(function (e) {
            return '<p class="ev"><span class="tag' + (e.k === "iv" ? " iv" : "") + '">' + (e.k === "iv" ? "면접" : "1단계 발표") + "</span>" +
              '<a href="' + e.u.u + '">' + esc(e.u.n) + "</a> " + esc(e.tr.n) +
              ' <button type="button" class="pl-add" data-id="' + e.tr.id + '">담기</button></p>';
          }).join("") + "</div></li>";
      }).join("");
  }
  tl.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest(".pl-add"); if (!b) return;
    var id = b.getAttribute("data-id");
    if (byId[id] && picked.indexOf(id) < 0) { picked.push(id); save(); refresh(); }
  });
  function refresh() { renderList(); renderTimeline(); }

  listEl.addEventListener("change", function (e) {
    var t = e.target; if (!t || t.type !== "checkbox") return;
    var i = picked.indexOf(t.value);
    if (t.checked && i < 0) picked.push(t.value);
    if (!t.checked && i >= 0) picked.splice(i, 1);
    save(); renderTimeline();
    var s = t.closest("details").querySelector("summary"), on = t.closest("details").querySelectorAll("input:checked").length, u = byId[t.value]._u;
    s.innerHTML = esc(u.n) + (on ? "<i>" + on + "개 고름</i>" : "");
  });
  qEl.addEventListener("input", renderList);
  $("plClear").addEventListener("click", function () { picked = []; save(); refresh(); });
  $("plPrint").addEventListener("click", function () { window.print(); });
  $("plCopy").addEventListener("click", function () {
    var url = location.href, b = this;
    var done = function () { b.textContent = "복사됨"; setTimeout(function () { b.textContent = "링크 복사"; }, 1500); };
    if (navigator.clipboard) navigator.clipboard.writeText(url).then(done, function () { prompt("이 주소를 복사하세요", url); });
    else prompt("이 주소를 복사하세요", url);
  });

  fetch(window.PLANNER_URL).then(function (r) { return r.json(); }).then(function (d) {
    DATA = d;
    var now = new Date();
    DATA.today_local = now.getFullYear() + "-" + ("0" + (now.getMonth() + 1)).slice(-2) + "-" + ("0" + now.getDate()).slice(-2);
    d.univs.forEach(function (u) { u.t.forEach(function (tr) { tr._u = u; byId[tr.id] = tr; }); });
    load(); save(); refresh();
  }).catch(function () { listEl.innerHTML = '<p class="note">일정 데이터를 불러오지 못했습니다. 새로고침해 주세요.</p>'; });
})();
