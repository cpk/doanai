#!/usr/bin/env bash
# Build the self-contained defense package (USB-ready folder) from the repo.
# Usage: bash harness/make-defense-package.sh [dest]   (default: ~/Desktop/doanai-bao-ve)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="${1:-$HOME/Desktop/doanai-bao-ve}"

# Selective cleanup: regenerate only what this script owns, preserving
# user-added content (recorded demo video, an unpacked+installed doanai-src,
# a filled-in .env) that a blanket rm -rf would destroy.
rm -rf "$DEST/01-bao-cao" "$DEST/02-slide" "$DEST/03-so-lieu-hinh" "$DEST/04-phan-bien"
rm -f "$DEST/HUONG-DAN.md" \
      "$DEST/05-demo-offline/vlm-suite-report.html" \
      "$DEST/05-demo-offline/vlm-test-A3-report.html" \
      "$DEST/05-demo-offline/README.md" \
      "$DEST/06-ma-nguon/doanai-src.zip" \
      "$DEST/06-ma-nguon/README.md"
mkdir -p "$DEST"/{01-bao-cao,02-slide,03-so-lieu-hinh,04-phan-bien,05-demo-offline,06-ma-nguon}

# 01 — report documents
cp "$ROOT/docs/bao-cao/bao-cao-doan.docx" "$DEST/01-bao-cao/"
cp "$ROOT/docs/DeCuong_VLM_GUI_Testing_TongQuat.docx" "$DEST/01-bao-cao/"

# 02 — slides (deck + speaker outline with talk tracks)
cp "$ROOT/docs/bao-cao/slide-bao-ve.pptx" "$DEST/02-slide/"
cp "$ROOT/docs/bao-cao/slide-bao-ve.md" "$DEST/02-slide/noi-dung-tung-slide.md"

# 03 — figures and official numbers
cp -R "$ROOT/results/figures" "$DEST/03-so-lieu-hinh/figures"
cp -R "$ROOT/results/screenshots-app-v1" "$DEST/03-so-lieu-hinh/screenshots-app-v1"
cp -R "$ROOT/masking/screens" "$DEST/03-so-lieu-hinh/masking-screens"
cp "$ROOT/results/analysis-summary.md" "$DEST/03-so-lieu-hinh/"
cp "$ROOT/results/rq2-maintenance.md" "$DEST/03-so-lieu-hinh/"
cp "$ROOT/results/raw/matrix-runs.csv" "$DEST/03-so-lieu-hinh/"
cp "$ROOT/masking/generated/grounding-results.csv" "$DEST/03-so-lieu-hinh/"

# 04 — Q&A material only (files the run-of-show question map points at).
# Working/AI-development artifacts (chapter markdown drafts, the writing
# coordinator, advisor-meeting notes) stay in the repo — the DOCX already
# carries all submitted content.
cp "$ROOT/docs/bao-cao/phu-luc.md" "$DEST/04-phan-bien/"
cp "$ROOT/docs/notes-papers.md" "$ROOT/docs/pilot-model-cost.md" "$DEST/04-phan-bien/"

# 05 — offline demo evidence: the merged 27/27 suite report + one single test
MERGED=$(ls -t "$ROOT"/tests-vlm/midscene_run/report/playwright-merged-*.html | head -1)
SINGLE=$(ls -S "$ROOT"/tests-vlm/midscene_run/report/playwright-A3--*.html | head -1)
cp "$MERGED" "$DEST/05-demo-offline/vlm-suite-report.html"
cp "$SINGLE" "$DEST/05-demo-offline/vlm-test-A3-report.html"
cat > "$DEST/05-demo-offline/README.md" <<'EOF'
# Demo offline (không cần mạng, không cần API key)

- `vlm-suite-report.html` — report Midscene của cả suite VLM (mở bằng trình
  duyệt): từng test, từng bước AI kèm screenshot mà VLM đã "nhìn".
- `vlm-test-A3-report.html` — report một test đơn (A3, thêm sản phẩm) — gọn để
  chiếu khi demo (kịch bản D3 trong HUONG-DAN.md).
- Đặt thêm vào đây: `demo-vlm-live.mp4` — video quay sẵn một lần chạy VLM sống
  (tự quay theo Phần A bước 6 của HUONG-DAN.md).
EOF

# 06 — source snapshot (no node_modules; offline install fallback)
git -C "$ROOT" archive --format=zip -o "$DEST/06-ma-nguon/doanai-src.zip" HEAD
cat > "$DEST/06-ma-nguon/README.md" <<'EOF'
# Mã nguồn (snapshot từ git HEAD, không kèm node_modules)

Dùng khi máy demo không có mạng để clone GitHub: giải nén rồi làm theo
PHẦN A của HUONG-DAN.md (vẫn cần mạng lần đầu để `npm install`;
nếu hoàn toàn offline, demo bằng 05-demo-offline/).
EOF

cp "$ROOT/docs/bao-cao/huong-dan-bao-ve.md" "$DEST/HUONG-DAN.md"

# The deliverables must not carry the repo owner's GitHub account name.
python3 "$ROOT/harness/scrub-defense-package.py" "$DEST"

echo "Defense package built at: $DEST"
du -sh "$DEST"
du -sh "$DEST"/*/ | sed 's|'"$DEST"'/||'
