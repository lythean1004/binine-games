# 🎮 빈이네 게임 놀이터

팀 **빈이네**가 생각하고 만든 게임과 배움 프로그램을 한곳에 모은 포트폴리오입니다.
첫 화면에서 하고 싶은 작품을 골라 바로 할 수 있어요. 설치도 로그인도 필요 없어요.

👉 **https://lythean1004.github.io/binine-games/**

## 작품

### 게임

| 작품 | 장르 | 소개 |
|---|---|---|
| 🪙 [코인 점프](https://lythean1004.github.io/binine-games/games/coin-jump/) | 점프맵 | 숲·얼음 동굴·화산 9개 스테이지를 뛰어넘으며 코인을 모으고, 상점에서 색과 모자를 사요 |
| ✈️ [스카이 파이터](https://lythean1004.github.io/binine-games/games/sky-fighter/) | 슈팅 | 세로 슈팅 게임. 3개 스테이지 끝에서 열기구, 폭격기, 비행선 보스와 싸워요 |
| 🧑‍🏫 [칠판 끝말잇기](https://lythean1004.github.io/binine-games/games/word-chain/) | 낱말 | 표준국어대사전 낱말로 컴퓨터와 끝말잇기를 하고, 기차 퀴즈도 풀어요 |
| 🌷 [한 붓 정원사](https://lythean1004.github.io/binine-games/games/garden/) | 퍼즐 | 우물에서 헛간까지 선을 한 번에 그어 모든 꽃에 물을 줘요 |
| 🔄 [중력 뒤집기 러너](https://lythean1004.github.io/binine-games/games/gravity-runner/) | 러너 | 중력을 뒤집어 천장과 바닥을 오가며 8개 스테이지를 달려요 |
| 🏒 [에어하키](https://lythean1004.github.io/binine-games/games/air-hockey/) | 스포츠 | 얼음 링크에서 컴퓨터와 에어하키 대결을 해요 |
| 🧪 [비밀 실험실 탈출](https://lythean1004.github.io/binine-games/games/escape-lab/) | 방탈출 | 독가스가 퍼지기 전에 암호와 수수께끼를 풀고 실험실을 빠져나가요 |
| ⭐ [별게임](https://lythean1004.github.io/binine-games/games/star-road/) | 러너 | 자동차로 도로를 달리며 별을 먹고 장애물을 피해요 |

### 배움 프로그램

| 작품 | 소개 |
|---|---|
| ⠓ [훈맹정음 점자 변환기](https://lythean1004.github.io/binine-games/games/braille/) | 한글을 한국 점자로 바꾸고, 퀴즈로 점자 읽는 법을 익혀요 |
| 🖍️ [세종대왕의 빨간펜](https://lythean1004.github.io/binine-games/games/red-pen/) | 맞춤법 문제와 받아쓰기를 세종대왕이 빨간펜으로 채점해 줘요 |

### 기타 작품

| 작품 | 소개 |
|---|---|
| 🚗 [신차 출시 소식](https://lythean1004.github.io/newcar-news/) | 국내 신차 기사를 차별로 모아 조건으로 찾아보는 페이지 (별도 저장소) |

## 기록은 어디에 저장되나요?

점수, 코인, 상점에서 산 꾸미기는 **지금 쓰는 브라우저**에 저장돼요. 다른 기기나 다른 브라우저에서는 처음부터 시작해요.
코인 점프와 스카이 파이터의 랭킹도 이 기기에서 한 기록만 보여 줘요.

## 안전하게 만든 점

- **보내는 정보 없음:** 로그인, 회원가입, 서버가 없어요. 게임이 인터넷으로 보내는 정보도 없어요.
- **이름 공개 범위:** 만든 사람은 팀 이름 "빈이네"로만 표시해요.
- **접속 제한:** 모든 페이지에 보안 설정(Content-Security-Policy)이 들어 있어요. 페이지는 이 사이트 파일과 구글 글꼴 말고는 어디에도 접속할 수 없어요. 그래서 혹시 이상한 코드가 끼어들어도 밖으로 정보를 보낼 수 없어요.
- **입력한 글자 처리:** 이름이나 단어처럼 직접 입력한 글자는 화면에 글자로만 보여 줘요. 코드로 실행되지 않아요.
- **기록 보관:** 기록은 브라우저 안(localStorage)에만 있어요. 브라우저 기록을 지우면 함께 지워져요.

## 자료 출처

- 칠판 끝말잇기의 낱말과 뜻풀이: 국립국어원 「표준국어대사전」 (2026-10-12 내려받기 자료를 가공해 사용)
- 글꼴: Google Fonts (Jua, Gowun Dodum, Do Hyeon, Nanum Pen Script, Press Start 2P, SIL Open Font License)

## 폴더 구조

```
binine-games/
├─ index.html          첫 화면 (games.json 을 읽어 카드로 보여 줌)
├─ games.json          작품 목록: 이름, 소개, 색, 원본 폴더 위치
├─ games/<작품>/        각 작품의 배포용 복사본 (작품끼리 서로 섞이지 않음)
├─ shared/             웹 버전에만 쓰는 공용 스크립트
└─ tools/sync.py       원본 폴더에서 games/<작품>/ 으로 복사하는 도구
```

각 작품의 **원본은 원래 폴더**에서 따로 만들고 고칩니다. 이 저장소에는 배포용 복사본만 있어요.
`tools/sync.py`는 원본을 읽기만 하고 고치지 않습니다.

## 작품을 고치거나 새로 넣을 때

1. 고친 작품이면 바로 2번으로 갑니다. 새 작품이면 `games.json`의 `works`에 한 덩어리를 추가합니다.
   - `slug`: 주소에 쓰는 영어 이름 (예: `air-hockey`)
   - `category`: `game`(게임) · `learn`(배움 프로그램) · `etc`(기타 작품)
   - `source`: 이 폴더 기준 원본 폴더 위치, `files`: 복사할 파일
   - 다른 곳에 이미 배포된 작품은 `source` 대신 `url`만 적어요
2. 복사합니다: `python tools/sync.py <slug>`
3. 커밋하고 push하면 1~2분 뒤 사이트에 반영돼요.

claude.ai 아티팩트 저장소(랭킹 등)를 쓰는 게임은 `"inject": ["shared/local-records.js"]`를 넣으면
웹에서도 기록이 이 브라우저에 저장되도록 바뀌어요.

---

빈이네가 기획하고 AI와 함께 만들었어요.
