"""빈이네 포트폴리오: 원본 게임 폴더에서 배포용 복사본을 가져온다.

사용법 (binine-games 폴더에서):
    python tools/sync.py              # games.json 의 모든 작품
    python tools/sync.py coin-jump    # 한 작품만

규칙
- 원본 폴더는 절대 고치지 않는다. 읽어서 games/<slug>/ 로 복사만 한다.
- 복사 전에 games/<slug>/ 를 비우므로, 한 작품의 갱신이 다른 작품에 영향을 주지 않는다.
- "inject" 에 적힌 공용 스크립트는 복사본의 <head> 에만 끼워 넣는다.
"""
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GAMES = ROOT / "games"


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
    low = html.lower()
    # claude.ai 아티팩트로 만든 게임은 문서 머리(doctype, charset, viewport)가 없어서 채워 준다
    head = []
    if "<!doctype" not in low[:200]:
        head.append('<!doctype html>\n<html lang="ko">')
    if "charset" not in low:
        head.append('<meta charset="utf-8">')
    if 'name="viewport"' not in low:
        head.append('<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">')
    head += [f'<script src="../../{s}"></script>' for s in work.get("inject", [])]
    if head:
        i = low.find("<head>")
        if i >= 0 and "<!doctype" in low[:200]:
            i += len("<head>")
            html = html[:i] + "\n" + "\n".join(head) + html[i:]
        else:
            html = "\n".join(head) + "\n" + html
        page.write_text(html, encoding="utf-8")

    size = sum(f.stat().st_size for f in dst.rglob("*") if f.is_file())
    print(f"[{slug}] 복사 완료 ({size / 1024 / 1024:.1f}MB) <- {src}")


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
