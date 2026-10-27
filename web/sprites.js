// ============================================================
// 스프라이트 에셋 로더
// ============================================================
// assets/atlas.js 에 적힌 스프라이트 시트(PNG)를 불러와서
// "doctor_down_0" 같은 이름으로 도트를 그릴 수 있게 해 준다.
// 도트 원본은 tools/build_sprites.py 에서 만든다.

const Sprites = (() => {
  const atlas = window.SPRITE_ATLAS;
  const images = {};
  const tintCache = new Map();

  // Streamlit 에서는 main.py 가 PNG 를 data URI 로 바꿔서 넣어 준다.
  function url(path) {
    return (window.ASSET_URLS && window.ASSET_URLS[path]) || path;
  }

  function load() {
    const jobs = Object.entries(atlas.sheets).map(
      ([name, path]) =>
        new Promise((resolve, reject) => {
          const image = new Image();
          image.onload = () => {
            images[name] = image;
            resolve();
          };
          image.onerror = () => reject(new Error(path + " 파일을 불러오지 못했습니다."));
          image.src = url(path);
        }),
    );
    return Promise.all(jobs);
  }

  function frame(name) {
    const data = atlas.frames[name];
    if (!data) {
      throw new Error("스프라이트가 없습니다: " + name);
    }
    const [sheet, x, y, w, h, ax, ay] = data;
    return { sheet, x, y, w, h, ax, ay };
  }

  // ----------------------------------------------------------
  // (x, y) 위치에 스프라이트의 기준점이 오도록 그린다.
  // options.scale : 확대 배율 (기본 1)
  // options.tint  : 흰색 도트에 입힐 색 ("#9277ff" 등)
  // options.alpha : 투명도
  // ----------------------------------------------------------
  function draw(ctx, name, x, y, options = {}) {
    const f = frame(name);
    const scale = options.scale || 1;
    const dx = Math.round(x - f.ax * scale);
    const dy = Math.round(y - f.ay * scale);
    const alpha = options.alpha === undefined ? 1 : options.alpha;
    if (alpha <= 0) {
      return;
    }
    ctx.globalAlpha = alpha;
    if (options.tint) {
      ctx.drawImage(tinted(name, options.tint), dx, dy, f.w * scale, f.h * scale);
    } else {
      ctx.drawImage(images[f.sheet], f.x, f.y, f.w, f.h, dx, dy, f.w * scale, f.h * scale);
    }
    ctx.globalAlpha = 1;
  }

  // 흰색·회색으로 찍은 도트에 색을 곱해서 새 도트를 만든다 (그림자 색 입히기)
  function tinted(name, color) {
    const key = name + color;
    if (!tintCache.has(key)) {
      const f = frame(name);
      const canvas = document.createElement("canvas");
      canvas.width = f.w;
      canvas.height = f.h;
      const g = canvas.getContext("2d");
      g.drawImage(images[f.sheet], f.x, f.y, f.w, f.h, 0, 0, f.w, f.h);
      g.globalCompositeOperation = "multiply";
      g.fillStyle = color;
      g.fillRect(0, 0, f.w, f.h);
      g.globalCompositeOperation = "destination-in";
      g.drawImage(images[f.sheet], f.x, f.y, f.w, f.h, 0, 0, f.w, f.h);
      tintCache.set(key, canvas);
    }
    return tintCache.get(key);
  }

  // 애니메이션의 현재 프레임 이름 (fps 는 초당 프레임 수)
  function anim(name, time, fps) {
    const frames = atlas.anims[name];
    return frames[Math.floor(time * fps) % frames.length];
  }

  function animFrames(name) {
    return atlas.anims[name];
  }

  // HTML 안에 스프라이트를 아이콘으로 넣을 때 쓰는 <span>
  function icon(name, scale = 2, extraClass = "") {
    const f = frame(name);
    const sheet = images[f.sheet];
    const style = [
      `width:${f.w * scale}px`,
      `height:${f.h * scale}px`,
      `background-image:url("${url(atlas.sheets[f.sheet])}")`,
      `background-size:${sheet.naturalWidth * scale}px ${sheet.naturalHeight * scale}px`,
      `background-position:${-f.x * scale}px ${-f.y * scale}px`,
    ].join(";");
    return `<span class="sprite ${extraClass}" style='${style}'></span>`;
  }

  return { load, draw, frame, anim, animFrames, icon };
})();
