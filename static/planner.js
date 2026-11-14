// 내 면접 일정표: 고른 전형의 1단계 발표일·면접일을 날짜순으로 보여 주고 같은 날 면접 겹침을 표시한다.
// 고른 전형은 주소(?t=)와 이 기기 localStorage 에만 저장한다. 서버 전송 없음.
(function () {
  var $ = function (id) { return document.getElementById(id); };
  var KEY = "mjgak-planner", WD = "일월화수목금토";
  var listEl = $("plList"), qEl = $("plQ"), tl = $("plTimeline"), nEl = $("plN"), warn = $("plWarn"), go = $("plGo"), goN = $("plGoN");
  var DATA = null, byId = {}, picked = [], hintU = null;

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
      // 블로그·대학 페이지에서 ?u= 로 오면 전형이 하나뿐일 때만 바로 담고, 여럿이면 펼쳐서 지원한 전형을 고르게 한다
      if (u) DATA.univs.forEach(function (x) {
        if (x.c !== u) return;
        if (x.t.length === 1) { if (ids.indexOf(x.t[0].id) < 0) ids.push(x.t[0].id); }
        else hintU = x;
      });
    }
    picked = ids.filter(function (id) { return byId[id]; });
    if (u) qEl.value = (DATA.univs.filter(function (x) { return x.c === u; })[0] || {}).n || "";
  }
  function renderList() {
    var q = qEl.value.trim().replace(/\s+/g, "");
    // 안내는 그 대학 전형을 아직 하나도 안 골랐을 때만
    var x0 = function (x) { return x.t.every(function (tr) { return picked.indexOf(tr.id) < 0; }) && x.n.replace(/\s+/g, "").indexOf(q) >= 0; };
    var html = DATA.univs.filter(function (x) { return !q || x.n.replace(/\s+/g, "").indexOf(q) >= 0; }).map(function (x) {
      var on = x.t.filter(function (tr) { return picked.indexOf(tr.id) >= 0; }).length;
      return '<details' + (q || on ? " open" : "") + '><summary>' + esc(x.n) + (on ? "<i>" + on + "개 고름</i>" : "") + "</summary>" +
        x.t.map(function (tr) {
          return '<label><input type="checkbox" value="' + tr.id + '"' + (picked.indexOf(tr.id) >= 0 ? " checked" : "") + '><span>' + esc(tr.n) +
            "<small>면접 " + tr.d.map(label).join(" · ") + (tr.f ? " · 1단계 " + label(tr.f) : "") + "</small></span></label>";
        }).join("") + "</details>";
    }).join("");
    var hu = hintU && x0(hintU) ? hintU : null;
    var hint = hu ? '<p class="note pl-hint"><b>' + esc(hu.n) + '</b> 전형이 ' + hu.t.length + '개입니다. 지원한 전형에 체크하세요.</p>' :
      !q && !picked.length ? '<p class="note pl-hint">위 칸에 대학 이름을 적거나, 아래 대학 이름을 눌러 전형을 펼치세요.</p>' : "";
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
      var past = iso < DATA.today_local;
      if (clash && !past) clashes.push(label(iso) + " " + names.join("·"));  // 지난 날짜 겹침은 위 경고에서 뺀다
      return '<li class="' + (clash ? "clash " : "") + (past ? "past" : "") + '"><div class="pl-d">' + label(iso) + "<small>" + dleft(iso) + "</small></div><div>" +
        (clash ? '<p class="clashnote">같은 날 면접 후보 ' + names.length + "곳 — 내 모집단위 날짜를 확인하세요</p>" : "") +
        list.map(function (e) {
          if (e.k === "cs") return '<p class="ev"><span class="tag cs">수능</span>2027학년도 대학수학능력시험</p>';
          if (e.k === "ev") return '<p class="ev"><span class="tag cs">일정</span><a href="' + e.m.url + '">' + esc(e.m.label) + "</a></p>";
          var multi = e.k === "iv" && e.tr.d.length > 1;
          return '<p class="ev"><span class="tag' + (e.k === "iv" ? " iv" : "") + '">' + (e.k === "iv" ? "면접" : "1단계 발표") + "</span>" +
            '<a href="' + e.u.u + '">' + esc(e.u.n) + "</a> " + esc(e.tr.n) +
            (e.k === "iv" ? more((multi ? "이날: " : "") + (multi ? seg(e.tr.dt, iso) : e.tr.dt)) : (e.tr.ft ? "<small>" + esc(e.tr.ft) + "</small>" : "")) + "</p>";
        }).join("") + "</div></li>";
    }).join("");
    warn.hidden = !clashes.length;
    warn.innerHTML = clashes.length ? "<b>겹칠 수 있는 날</b> " + esc(clashes.join(" / ")) + ". 같은 날이라도 모집단위·시간이 다르면 둘 다 볼 수 있으니, 1단계 발표 때 개인별 고사 시간을 꼭 확인하세요." : "";
  }
  // 모집단위가 길게 늘어선 설명은 두 줄만 보이고 눌러서 펼친다(휴대폰에서 같은 목록이 날마다 반복돼 길어지는 것 방지)
  function more(t) {
    return t.length > 70 ? '<small class="pl-more">' + esc(t) + '</small><button type="button" class="pl-more-btn" aria-expanded="false">전체 보기 ▾</button>' : "<small>" + esc(t) + "</small>";
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
    var mb = e.target.closest && e.target.closest(".pl-more-btn");
    if (mb) {
      var open = mb.previousElementSibling.classList.toggle("open");
      mb.setAttribute("aria-expanded", open); mb.textContent = open ? "접기 ▴" : "전체 보기 ▾"; return;
    }
    var b = e.target.closest && e.target.closest(".pl-add"); if (!b) return;
    var id = b.getAttribute("data-id");
    if (byId[id] && picked.indexOf(id) < 0) { picked.push(id); save(); refresh(); ev("planner_add", { univ_code: id.split(":")[0], from: "upcoming" }); }
  });
  function refresh() { renderList(); renderTimeline(); }

  // 로드맵 3단계(이용자 검증): 일정표를 실제로 쓰는지 보려고 GA 이벤트만 남긴다(개인정보 없음)
  function ev(name, p) { try { if (window.gtag) gtag("event", name, p || {}); } catch (e) {} }
  listEl.addEventListener("change", function (e) {
    var t = e.target; if (!t || t.type !== "checkbox") return;
    if (t.checked) ev("planner_add", { univ_code: String(t.value).split(":")[0] });
    var i = picked.indexOf(t.value);
    if (t.checked && i < 0) picked.push(t.value);
    if (!t.checked && i >= 0) picked.splice(i, 1);
    save(); renderTimeline();
    var s = t.closest("details").querySelector("summary"), on = t.closest("details").querySelectorAll("input:checked").length, u = byId[t.value]._u;
    s.innerHTML = esc(u.n) + (on ? "<i>" + on + "개 고름</i>" : "");
  });
  qEl.addEventListener("input", renderList);
  $("plClear").addEventListener("click", function () { picked = []; save(); refresh(); });
  // 달력에 넣기: 고른 전형의 1단계 발표·면접(후보일)·고사장 공지·최종 발표를 .ics 파일 하나로 만든다(이 기기 안에서만, 서버 전송 없음)
  function ics() {
    var today = DATA.today_local, E = [], seen = {};
    function x(s) { return String(s || "").replace(/\\/g, "\\\\").replace(/;/g, "\\;").replace(/,/g, "\\,").replace(/\r?\n/g, "\\n"); }
    function ymd(iso) { return iso.replace(/-/g, ""); }
    function next(iso) { var d = day(iso); d.setDate(d.getDate() + 1); return d.getFullYear() + ("0" + (d.getMonth() + 1)).slice(-2) + ("0" + d.getDate()).slice(-2); }
    function add(uid, iso, title, desc, url, alarm) {
      if (!iso || iso < today || seen[uid]) return; seen[uid] = 1;
      E.push(["BEGIN:VEVENT", "UID:" + uid + "@mjgak.com", "DTSTAMP:" + new Date().toISOString().replace(/[-:]/g, "").replace(/\.\d+/, ""),
        "DTSTART;VALUE=DATE:" + ymd(iso), "DTEND;VALUE=DATE:" + next(iso), "SUMMARY:" + x(title),
        "DESCRIPTION:" + x(desc + (url ? "\n" + url : "") + "\n날짜는 2027학년도 모집요강 기준이며 바뀔 수 있으니 입학처 공지를 확인하세요. (면접각)"),
        url ? "URL:" + url : ""].concat(alarm ? ["BEGIN:VALARM", "ACTION:DISPLAY", "DESCRIPTION:" + x(title), "TRIGGER:" + alarm, "END:VALARM"] : []).concat(["END:VEVENT"]).filter(Boolean));
    }
    var base = location.origin, us = {};
    picked.forEach(function (id) {
      var tr = byId[id], u = tr._u, link = base + u.u;
      us[u.c] = us[u.c] || { u: u, names: [] }; us[u.c].names.push(tr.n);
      if (tr.f) add(id + "-f", tr.f, "[1단계 발표] " + u.n + " " + tr.n, tr.ft || "", link, "PT9H");
      tr.d.forEach(function (d) {
        var multi = tr.d.length > 1;
        add(id + "-iv-" + d, d, "[면접" + (multi ? " 후보일" : "") + "] " + u.n + " " + tr.n, (multi ? "면접 후보일 중 하루입니다. 내 모집단위 날짜를 확인하세요.\n" + seg(tr.dt, d) : tr.dt), link, "-PT15H");
      });
    });
    Object.keys(us).forEach(function (c) {
      var o = us[c], u = o.u, link = base + u.u + "#dayof", key = function (s) { return String(s).replace(/\s+/g, ""); };
      var rows = (u.nt || []).filter(function (r) { return o.names.some(function (n) { return key(r.tr).indexOf(key(n)) >= 0; }); });
      if (!rows.length) rows = u.nt || [];
      rows.forEach(function (r, i) { add(c + "-nt-" + r.d + "-" + i, r.d, "[고사장·면접 시간 공지] " + u.n, r.what + " · " + r.w, link, "PT9H"); });
      if (u.fin) add(c + "-fin-" + u.fin.d, u.fin.d, "[최종 합격자 발표] " + u.n, u.fin.w, base + u.u + "#after", "PT9H");
    });
    var enc = window.TextEncoder ? new TextEncoder() : null;
    function fold(line) {  // 한 줄 75바이트 제한(한글은 3바이트) — 글자 중간에서 끊지 않는다
      if (!enc || enc.encode(line).length <= 74) return line;
      var out = [], cur = "", n = 0;
      for (var i = 0; i < line.length; i++) {
        var ch = line[i], b = enc.encode(ch).length;
        if (n + b > (out.length ? 73 : 74)) { out.push(cur); cur = ""; n = 0; }
        cur += ch; n += b;
      }
      out.push(cur);
      return out.join("\r\n ");
    }
    var lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//mjgak.com//planner//KO", "CALSCALE:GREGORIAN", "METHOD:PUBLISH", "X-WR-CALNAME:면접각 내 면접 일정", "X-WR-TIMEZONE:Asia/Seoul"];
    E.forEach(function (e) { lines = lines.concat(e); });
    lines.push("END:VCALENDAR");
    return { text: lines.map(fold).join("\r\n") + "\r\n", n: E.length };
  }
  $("plIcs").addEventListener("click", function () {
    var msg = $("plIcsMsg");
    if (!picked.length) { msg.hidden = false; msg.textContent = "먼저 대학 목록에서 지원한 전형을 고르세요."; return; }
    var r = ics();
    if (!r.n) { msg.hidden = false; msg.textContent = "고른 전형의 날짜가 모두 지났습니다."; return; }
    var a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([r.text], { type: "text/calendar;charset=utf-8" }));
    a.download = "면접각-내-면접-일정.ics";
    document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 1000);
    ev("planner_ics", { n: picked.length, events: r.n });
    msg.hidden = false;
    msg.innerHTML = "<b>일정 " + r.n + "개</b>를 달력 파일로 받았습니다. 파일을 열면 휴대폰·PC 달력에 들어가고, 면접 전날 오전 9시에 알림이 옵니다(달력 앱이 알림을 지원할 때). " +
      "구글 캘린더는 PC에서 <b>설정 → 가져오기·내보내기 → 가져오기</b>로 넣으세요. 날짜가 바뀌면 일정표에서 다시 받으세요.";
  });
  $("plPrint").addEventListener("click", function () { ev("planner_print", { n: picked.length }); window.print(); });
  $("plCopy").addEventListener("click", function () {
    ev("planner_copy", { n: picked.length });
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
