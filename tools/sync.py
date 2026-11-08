"""빈이네 포트폴리오: 원본 게임 폴더에서 배포용 복사본을 가져온다.

사용법 (binine-games 폴더에서):
    python tools/sync.py              # games.json 의 모든 작품
    python tools/sync.py coin-jump    # 한 작품만

규칙
- 원본 폴더는 절대 고치지 않는다. 읽어서 games/<slug>/ 로 복사만 한다.
- 복사 전에 games/<slug>/ 를 비우므로, 한 작품의 갱신이 다른 작품에 영향을 주지 않는다.
- 모든 복사본의 <head> 맨 앞에 보안 설정(CSP, Referrer-Policy)을 넣는다.
- "inject" 에 적힌 공용 스크립트, "replace" 에 적힌 글자 바꾸기는 복사본에만 적용한다.
"""
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GAMES = ROOT / "games"

# 보안 설정: 게임이 이 사이트 파일과 구글 글꼴 말고는 아무 데도 접속하거나 보내지 못하게 막는다.
# (첫 화면 index.html 에도 같은 값이 들어 있다. 바꿀 때는 둘 다 바꿀 것)
CSP = (
    "default-src 'self'; "
    "script-src 'self' 'unsafe-inline'; "
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
    "font-src 'self' https://fonts.gstatic.com data:; "
    "img-src 'self' data: blob:; "
    "media-src 'self' data: blob:; "
    "connect-src 'self'; "
    "object-src 'none'; "
    "base-uri 'self'; "
    "form-action 'none'"
)
SECURITY_META = [
    f'<meta http-equiv="Content-Security-Policy" content="{CSP}">',
    '<meta name="referrer" content="strict-origin-when-cross-origin">',
]


def copy_work(work: dict) -> None:
    slug = work["slug"]
    src = (ROOT / work["source"]).resolve()
    dst = GAMES / slug
    if not src.is_dir():
        raise SystemExit(f"[{slug}] 원본 폴더가 없어요: {src}")

    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True)

    for item in work["files"]:
        frm, to = (item["from"], item["to"]) if isinstance(item, dict) else (item, item)
        s, d = src / frm, dst / to
        if s.is_dir():
            shutil.copytree(s, d)
        elif s.is_file():
            shutil.copy2(s, d)
        else:
            raise SystemExit(f"[{slug}] 파일이 없어요: {s}")

    page = dst / "index.html"
    html = page.read_text(encoding="utf-8")

    for old, new in work.get("replace", {}).items():
        if old not in html:
            print(f"[{slug}] 주의: 바꿀 글자 '{old}' 를 찾지 못했어요")
        html = html.replace(old, new)

    low = html.lower()
    head = []
    if "charset" not in low:
        head.append('<meta charset="utf-8">')
    head += SECURITY_META
    if 'name="viewport"' not in low:
        head.append('<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">')
    head += [f'<script src="../../{s}"></script>' for s in work.get("inject", [])]
    # 모든 작품에 "🏠 놀이터" 돌아가기 버튼 (위치는 games.json 의 "home" 으로 바꿈)
    home = work.get("home", "bottom-left")
    if home != "none":
        head.append(f'<script src="../../shared/home-button.js" data-pos="{home}"></script>')
    block = "\n".join(head) + "\n"

    m_head = re.search(r"<head(\s[^>]*)?>", html, re.I)  # <header> 와 헷갈리지 않게
    m_doctype = re.match(r"\s*<!doctype[^>]*>", html, re.I)
    if m_head:
        # 이미 있는 charset 보다 앞에 오면 안 되므로, charset 줄이 있으면 그 뒤에 넣는다
        m_cs = re.search(r"<meta[^>]*charset[^>]*>", html, re.I)
        at = m_cs.end() if m_cs and m_cs.start() > m_head.end() else m_head.end()
        html = html[:at] + "\n" + block + html[at:]
    elif m_doctype:
        html = html[:m_doctype.end()] + '\n<html lang="ko">\n' + block + html[m_doctype.end():]
    else:
        # claude.ai 아티팩트로 만든 게임은 문서 머리(doctype)가 없어서 채워 준다
        html = '<!doctype html>\n<html lang="ko">\n' + block + html

    page.write_text(html, encoding="utf-8")
    size = sum(f.stat().st_size for f in dst.rglob("*") if f.is_file())
    print(f"[{slug}] 복사 완료 ({size / 1024 / 1024:.1f}MB) <- {src.name}")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    data = json.loads((ROOT / "games.json").read_text(encoding="utf-8"))
    works = [w for w in data["works"] if "source" in w]
    wanted = sys.argv[1:]
    if wanted:
        unknown = set(wanted) - {w["slug"] for w in works}
        if unknown:
            raise SystemExit(f"games.json 에 없는 작품: {', '.join(sorted(unknown))}")
        works = [w for w in works if w["slug"] in wanted]
    for w in works:
        copy_work(w)


if __name__ == "__main__":
    main()
