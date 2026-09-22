(function () {
  // Mobile nav
  var menuBtn = document.querySelector('.menu-btn');
  var nav = document.getElementById('site-nav');
  if (menuBtn && nav) {
    menuBtn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Pre-select the submission path from ?path=
  var params = new URLSearchParams(window.location.search);
  var path = params.get('path');
  if (path) {
    var radio = document.querySelector('input[name="path"][value="' + path + '"]');
    if (radio) radio.checked = true;
  }

  // Chloe, the FAQ assistant
  var FAQ = window.OMS_FAQ || [];
  var launch = document.getElementById('chat-launch');
  var panel = document.getElementById('chat-panel');
  if (!launch || !panel) return;
  var log = panel.querySelector('.chat-log');
  var form = panel.querySelector('.chat-form');
  var input = form.querySelector('input');
  var started = false;

  function el(tag, cls, html) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html != null) n.innerHTML = html;
    return n;
  }
  function scroll() { log.scrollTop = log.scrollHeight; }
  function say(html, who) {
    log.appendChild(el('div', 'msg' + (who === 'me' ? ' me' : ''), html));
    scroll();
  }
  function escapeHtml(s) {
    return s.replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function chips(list) {
    var wrap = el('div', 'chips');
    list.forEach(function (item) {
      var b = el('button', null, escapeHtml(item.q));
      b.type = 'button';
      b.addEventListener('click', function () { ask(item.q, item); });
      wrap.appendChild(b);
    });
    log.appendChild(wrap);
    scroll();
  }
  function reply(html, followUps) {
    var t = el('div', 'typing', 'Chloe is typing…');
    log.appendChild(t); scroll();
    setTimeout(function () {
      t.remove();
      say(html);
      if (followUps && followUps.length) chips(followUps);
    }, 550);
  }
  function others(exclude) {
    return FAQ.filter(function (f) { return f !== exclude && f.chip; }).slice(0, 3);
  }
  function match(text) {
    var t = text.toLowerCase();
    var best = null, bestScore = 0;
    FAQ.forEach(function (f) {
      var score = 0;
      f.keys.forEach(function (k) { if (t.indexOf(k) !== -1) score += k.length; });
      if (score > bestScore) { best = f; bestScore = score; }
    });
    return best;
  }
  function ask(text, known) {
    say(escapeHtml(text), 'me');
    var hit = known || match(text);
    if (hit) {
      reply(hit.a, others(hit));
    } else {
      reply('Good question. I don\'t have that answer on hand, but our team does. <a href="/submit/">Send us a message</a> and someone will get back to you, or pick one of these:', FAQ.filter(function (f) { return f.chip; }).slice(0, 4));
    }
  }
  function openChat() {
    panel.classList.add('open');
    launch.setAttribute('aria-expanded', 'true');
    if (!started) {
      started = true;
      say('Hi, I\'m Chloe. Ask me anything about publishing with OMS Books, or tap a question below.');
      chips(FAQ.filter(function (f) { return f.chip; }));
    }
    setTimeout(function () { input.focus(); }, 50);
  }
  function closeChat() {
    panel.classList.remove('open');
    launch.setAttribute('aria-expanded', 'false');
  }
  launch.querySelectorAll('button').forEach(function (b) {
    b.addEventListener('click', function () {
      panel.classList.contains('open') ? closeChat() : openChat();
    });
  });
  panel.querySelector('.chat-close').addEventListener('click', closeChat);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && panel.classList.contains('open')) closeChat();
  });
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var v = input.value.trim();
    if (!v) return;
    input.value = '';
    ask(v);
  });
})();
