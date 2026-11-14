const $ = (id) => document.getElementById(id);

let last = -1;
let cfg = {};
let cfgStr = "";
let cur = { title: "", artist: "", album: "" };
let pos = 0,
  dur = 0,
  at = 0,
  playing = false;

function setText(id, text) {
  const el = $(id),
    span = el.firstChild;
  span.textContent = text;
  span.style.animation = "none";

  requestAnimationFrame(() => {
    const overflow = span.scrollWidth - el.clientWidth;
    if (cfg.scroll_text && overflow > 0) {
      const startPause = 1.5;
      const endPause = 3.5;
      const moveTime = overflow / cfg.scroll_speed;
      const total = startPause + moveTime + endPause + moveTime;

      const t1 = (startPause / total) * 100;
      const t2 = ((startPause + moveTime) / total) * 100;
      const t3 = ((startPause + moveTime + endPause) / total) * 100;

      const animName = "marquee_" + id + "_" + Date.now();
      let styleEl = document.getElementById("kf_" + id);
      if (!styleEl) {
        styleEl = document.createElement("style");
        styleEl.id = "kf_" + id;
        document.head.appendChild(styleEl);
      }
      styleEl.textContent = `
        @keyframes ${animName} {
          0%, ${t1.toFixed(2)}% { transform: translateX(0); }
          ${t2.toFixed(2)}%, ${t3.toFixed(2)}% { transform: translateX(-${overflow}px); }
          100% { transform: translateX(0); }
        }
      `;

      span.style.animation = `${animName} ${total.toFixed(2)}s linear infinite`;
    }
  });
}

function sizeVinyl() {
  if (cfg.style !== "vinyl") return;
  const rect = $("info").offsetHeight + 32;
  const r = document.documentElement.style;
  r.setProperty("--rect", rect + "px");
  r.setProperty("--vsize", Math.round((rect * cfg.vinyl_scale) / 100) + "px");
}

function fitAll() {
  setText("title", cur.title);
  setText("artist", cur.artist);
  setText("album", cur.album);
  sizeVinyl();
}

async function loadConfig() {
  let c;
  try {
    c = await (await fetch("/config")).json();
  } catch (e) {
    return;
  }
  const str = JSON.stringify(c);
  if (str === cfgStr) return;

  cfgStr = str;
  cfg = c;
  const r = document.documentElement.style;
  r.setProperty("--font", cfg.font);
  r.setProperty("--size", cfg.font_size + "px");
  r.setProperty("--text", cfg.text_color);
  r.setProperty("--accent", cfg.accent_color);
  r.setProperty("--bg", cfg.bg_color);
  r.setProperty("--radius", cfg.radius + "px");
  r.setProperty("--cover", cfg.cover_size + "px");
  r.setProperty("--textw", cfg.text_width + "px");
  r.setProperty("--barh", cfg.bar_height + "px");
  r.setProperty("--spin", cfg.spin_seconds + "s");
  r.setProperty("--width", cfg.container_width + "px");
  const vinyl = cfg.style === "vinyl";
  $("card").classList.toggle("vinyl", vinyl);
  $("card").classList.toggle("spin", cfg.vinyl_spin);
  $("cover").classList.toggle("off", !cfg.show_cover);
  $("album").classList.toggle("off", !cfg.show_album);
  $("bar").classList.toggle("off", !cfg.show_progress);
  $("card").classList.toggle("vinyl-style", cfg.vinyl_style);
  $("custom").textContent = cfg.custom_css || "";
  fitAll();
}

async function tick() {
  let s;
  try {
    s = await (await fetch("/info")).json();
  } catch (e) {
    return;
  }
  const card = $("card");
  pos = s.position;
  dur = s.duration;
  playing = s.playing;
  at = performance.now();
  if (s.id !== last) {
    last = s.id;
    card.classList.add("swap");
    setTimeout(() => {
      cur = { title: s.title, artist: s.artist, album: s.album };
      fitAll();
      if (s.has_cover) $("cover").src = "/cover?id=" + s.id;
      card.classList.remove("swap");
    }, 400);
  }
  card.classList.toggle("playing", s.playing);
  card.classList.toggle(
    "hidden",
    !(s.title && (s.playing || !cfg.hide_paused)),
  );
}

function frame() {
  const t = pos + (playing ? (performance.now() - at) / 1000 : 0);
  const f = dur > 0 ? Math.min(1, Math.max(0, t / dur)) : 0;
  $("fill").style.width = f * 100 + "%";
  requestAnimationFrame(frame);
}

loadConfig().then(() => {
  setInterval(loadConfig, 2000);
  setInterval(tick, 1000);
  tick();
  frame();
});
