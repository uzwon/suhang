# 게임 에셋

```
web/
├── assets/
│   ├── atlas.js            스프라이트 이름 → 시트 위치 (자동 생성)
│   ├── sprites/
│   │   ├── tiles.png       바닥 · 벽 (스테이지별 3세트)
│   │   ├── characters.png  의사 · 환자 · 그림자
│   │   ├── objects.png     가구 · 아이템 · 문 · 단말기
│   │   └── ui.png          하트 · 아이콘 · 말풍선 · 방향키
│   └── fonts/              Galmuri11 도트 글꼴 (SIL OFL 1.1, OFL.txt 참고)
├── sprites.js              스프라이트 로더 (Sprites.draw / Sprites.anim / Sprites.icon)
└── script.js               게임 로직 + 화면 그리기
```

## 그리는 방식

- 도트 1픽셀을 화면 2픽셀로 그린다. 타일은 16x16 도트 = 화면 32x32.
- 맵과 캐릭터는 528x320 크기의 도트 해상도 Canvas 에 그린 뒤 2배로 확대한다.
  이름표, HUD, 미니게임 창은 확대한 다음 원래 해상도로 그린다.
- 코드에서는 이름으로만 부른다.

```js
Sprites.draw(ctx, "doctor_down_0", x, y);                    // 기준점(발밑)이 (x, y)
Sprites.draw(ctx, "ghost_0", x, y, { tint: "#9277ff" });     // 흰 도트에 색 입히기
Sprites.anim("generator_on", time, 8);                       // 애니메이션 현재 프레임 이름
```

## 도트 고치기

도트 원본은 `tools/build_sprites.py` 안에 문자 격자로 들어 있다 (한 글자 = 한 픽셀).
격자를 고친 뒤 아래 명령을 실행하면 PNG 와 `atlas.js` 가 다시 만들어진다.

```
python tools/build_sprites.py
python tools/build_sprites.py --preview preview.png   # 전체 스프라이트 확대 미리보기
```

PNG 를 Aseprite, Piskel 같은 도트 툴로 직접 고쳐도 된다.
단, 그 뒤에 `build_sprites.py` 를 실행하면 PNG 가 덮어써지니 둘 중 한 방식만 쓰는 게 좋다.

## 외부 도트로 바꾸기

1. 새 시트를 `sprites/` 에 넣고 `atlas.js` 의 `sheets` 에 등록한다.
2. `frames` 에서 바꿀 스프라이트의 `[시트, x, y, 폭, 높이, 기준점 x, 기준점 y]` 를 새 위치로 고친다.
3. 크기가 16px 타일 기준이 아니면 `script.js` 의 그리는 위치도 함께 맞춘다.

외부 에셋을 쓸 때는 라이선스(재배포 가능 여부, 출처 표기)를 꼭 확인하자.

## Streamlit 에서 실행할 때

`components.html` 은 상대 경로 파일을 못 읽기 때문에 `main.py` 가
CSS/JS 를 HTML 안에 넣고, PNG 와 글꼴은 data URI 로 바꿔서 넘긴다.
`sprites/` 폴더에 PNG 를 추가하면 자동으로 함께 넘어간다.
