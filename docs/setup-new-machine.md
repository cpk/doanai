# Setup máy mới & tiếp tục công việc (handoff)

> Cập nhật cuối: **09/07/2026** (máy Windows, sau khi hoàn tất toàn bộ phần chạy tự động của GĐ4) — dùng file này khi mở session/máy mới để tiếp tục không gián đoạn.

## 1. Trạng thái hiện tại (đang ở đâu)

- **GĐ1 ✔ + GĐ2 ✔ + GĐ3 ✔ (toàn bộ, kể cả phần chạy thật). GĐ4: phần chạy tự động ✔ xong sớm 09/07** — số liệu chính thức RQ1/RQ3/RQ4 đã nằm đủ trong repo. Chi tiết từng mốc: `KeHoach_DoAn.md` mục 7.
- **Số liệu chính thức (tất cả deterministic, flakiness=0, temp=0, cache tắt):**
  - RQ1 (`results/raw/matrix-runs.csv`, label `gd4-main`, 2×4×5): locator V0 18/18, V1 18/18, **V2 9/18, V3 12/18**; VLM **18/18 cả 4 biến thể**. VLM ~93 call, **$0.050/run**, ~7–10 phút/run vs locator ~3s (V0/V1) / ~32s (V2/V3 do test fail chờ timeout).
  - RQ3 (label `gd4-rbac-clean` + `gd4-rbac-seeded`, 2 phương pháp × 5 lặp mỗi build): cả locator lẫn VLM detection **5/5** (R1–R5 fail đủ 5/5 lần trên seeded), false alarm **0/3** (R6–R8 + clean build 8/8). VLM RBAC $0.0052/run.
  - RQ4 (`masking/generated/grounding-results.csv` + `raw-calls.jsonl`): hit-rate **100% cả 3 điều kiện** (orig/blur/pixel); IoU giảm nhẹ và chỉ trên màn PII (c01 0.764→0.709, c03 0.806→0.730). $0.112/360 call.
- **Model ghim: `qwen/qwen3-vl-235b-a22b-instruct`** qua OpenRouter, $0.20/M in + $0.88/M out. Tổng chi phí API đến nay ≈ **$1.5** / ngân sách $50.
- 2 phát hiện phương pháp luận cho Chương 4 / Threats to Validity: **viewport-bound perception** (`docs/pilot-model-cost.md` mục 7) và **Qwen grounding trả tọa độ chuẩn hóa 0–1000** (mục 8).
- Nhánh/tag trên remote `https://github.com/cpk/doanai` (private): `master`, tag `app-v1.0`, branch `rq3-seeded-bugs` (KHÔNG merge vào master; đã đồng bộ tooling từ master tại `4daf158`).
- ⚠️ `tests-vlm/.env` (key OpenRouter) là gitignored — **máy mới phải tạo lại từ `.env.example`** (quan trọng nhất: `MIDSCENE_MODEL_API_KEY`; `masking/benchmark.mjs` cũng đọc chung file này). Key hiện tại đã dán qua chat AI — **xoay key sau khi xong toàn bộ thực nghiệm**. KHÔNG cần key cho: locator suite, phân tích CSV, vẽ biểu đồ, viết báo cáo.

## 2. Việc tiếp theo (theo thứ tự) — bắt đầu từ đây

> **Cập nhật 09/07 (máy Mac):** mục 2.1 bước 1 ✔ (V2 = 9 test/24 LOC trên `rq2-fix-v2`, V3 = 6 test/22 LOC trên `rq2-fix-v3` — xem `results/rq2-maintenance.md`), mục 2.2 ✔ (`harness/make-figures.py` → `results/figures/` + `results/analysis-summary.md`), mục 2.3 ✔ (`docs/chuong4-draft.md`). **Cập nhật thêm 09/07 (chiều):** đề cương .docx (chưa nộp) đã sửa theo hướng "quy trình bảo trì chuẩn hóa tự động" — không cần sinh viên sửa tay/bấm giờ nữa; phương án (a)/(b) bên dưới chỉ còn là bối cảnh lịch sử + dự phòng. Còn lại: đo thời gian phục hồi của agent (`rq2-agent-v2/v3`) và trình bày thiết kế với GVHD theo `docs/gvhd-trao-doi.md`.

Phần chạy tự động GĐ3+GĐ4 đã xong hết (RQ1/RQ3/RQ4 — số liệu ở mục 1). Còn lại của GĐ4:

### 2.1. RQ2 — maintenance cost (việc chính còn lại; phương án lai đã phân tích 09/07)

Bối cảnh: VLM suite **không hỏng test nào** trên V1–V3 → phía VLM: 0 test sửa / 0 LOC / 0 phút (bản thân đây là kết quả RQ2). Chỉ còn đo phía locator: **V2 hỏng 9 test, V3 hỏng 6 test** (V1 không hỏng — xem CSV label `gd4-main`).

Phương án lai (AI làm phần khách quan, người làm phần thời gian):
1. **Claude sửa bộ locator** cho V2, V3 trên branch riêng (`rq2-fix-v2`, `rq2-fix-v3`), quy tắc **sửa tối thiểu để pass lại** (chỉ đổi selector/assertion, không refactor, không đổi cấu trúc test) → thu 2 chỉ số khách quan: **số test phải sửa + diff LOC** (`git diff --stat`). Hai chỉ số này không phụ thuộc ai gõ phím.
2. **Chỉ số thời gian sửa** — 2 lựa chọn, ⚠️ **hỏi ý GVHD trước khi chốt**:
   - (a) Sinh viên tự sửa lại từ đầu trên branch khác (không nhìn bản Claude sửa), tự bấm giờ từng biến thể → đúng đề cương "cùng một người sửa cả hai bộ theo quy trình thống nhất".
   - (b) Bỏ/hạ cấp chỉ số thời gian, ghi minh bạch trong Threats to Validity rằng việc bảo trì có AI hỗ trợ.
3. Xác nhận sau khi sửa: `cd tests-locator` rồi `APP_VARIANT=v2 npx playwright test tests/group-*` phải 18/18 (tương tự v3). Ghi số liệu vào `results/rq2-maintenance.md`.

Lệnh mở đầu khi tiếp tục với Claude Code ở máy mới: **"đọc docs/setup-new-machine.md mục 2.1, làm bước 1 của RQ2 (sửa locator cho V2/V3 trên branch riêng, đo số test sửa + diff LOC)"**.

### 2.2. Phân tích số liệu + biểu đồ (tuần 9 — làm được ngay, KHÔNG cần API key)

Nguồn: `results/raw/matrix-runs.csv` (label `gd4-*`) + `masking/generated/grounding-results.csv`. Cần: pass-rate theo biến thể ×2 phương pháp (RQ1), bảng detection/false-alarm (RQ3), hit-rate + IoU theo điều kiện (RQ4), bảng chi phí (token/$/wall-clock per run). Vẽ bằng Python matplotlib (chạy qua `py`) → lưu `results/figures/`. Claude làm tự động được toàn bộ mục này.

### 2.3. Nháp Chương 4

Khung: kết quả từng RQ (số ở mục 1) + thảo luận trade-off (robustness ↔ thời gian/chi phí) + Threats to Validity (viewport confounder, tọa độ 0–1000, single-app/single-model, AI-assisted maintenance nếu chọn 2.1-2b).

**Việc sinh viên tự làm song song:** đọc kỹ full-text 4 bài ⭐ (khung notes trong `docs/notes-papers.md`); điền placeholder GVHD/họ tên/MSSV trong đề cương .docx; **trao đổi GVHD 2 việc**: chốt cách đo thời gian RQ2 (mục 2.1) + báo kết quả khảo sát đổi model sang Qwen3-VL (`docs/pilot-model-cost.md` mục 1).

## 3. Setup máy mới (Windows)

```powershell
# 1. Yêu cầu: Node >= 20 (Playwright 1.61 không chạy Node < 18.19; máy cũ dùng Node 24 LTS)
winget install OpenJS.NodeJS.LTS
# (tùy chọn, để push/PR) winget install GitHub.cli ; gh auth login --web

# 2. Clone
git clone https://github.com/cpk/doanai.git
cd doanai

# 3. Cài dependencies (4 package độc lập, KHÔNG có root package.json)
cd app          ; npm install ; cd ..
cd tests-locator; npm install ; npx playwright install chromium ; cd ..
cd tests-vlm    ; npm install ; cd ..
cd masking      ; npm install ; cd ..

# 4. Kiểm tra môi trường OK (không cần API key):
cd tests-locator && npx playwright test        # kỳ vọng 30/30 pass (18 + 4 smoke + 8 RBAC)
```

Lưu ý:
- **`tests-vlm/.env` không nằm trong git** (chứa API key). Tạo mới từ `.env.example` trên mỗi máy; key lấy từ tài khoản OpenRouter của mình. Không commit key.
- Suite test tự khởi động app qua `webServer` của Playwright — không cần chạy `npm run dev` trước (trừ khi chạy `masking/capture` hoặc muốn xem app: `cd app && npm run dev` → http://localhost:5173, đăng nhập `admin/admin123` hoặc `staff/staff123`).
- Python chỉ cần khi đọc lại .docx/.pdf gốc (python-docx, pypdf) hoặc vẽ biểu đồ GĐ4 (matplotlib) — chưa cần cho các bước trên.
- Bối cảnh đầy đủ cho AI assistant (Claude Code): đã có trong `CLAUDE.md` ở repo root — mở project là dùng được ngay.

## 4. Quy ước cần nhớ khi tiếp tục

- **Không sửa logic app** (đã freeze tại `app-v1.0`); thay đổi giao diện chỉ qua `app/src/variants.ts`; lỗi cố ý chỉ ở branch `rq3-seeded-bugs`.
- **Không bật `MIDSCENE_CACHE`**; giữ `MIDSCENE_MODEL_TEMPERATURE=0`; ghim model ID trong suốt thực nghiệm.
- Mọi chỉnh sửa test khi lên biến thể V1–V3 phải ghi lại (số test sửa, diff LOC, thời gian) — đó là dữ liệu RQ2, quy trình ở `KeHoach_DoAn.md` mục 2.
- Số liệu chính thức ghi vào `results/raw/matrix-runs.csv` qua harness (đừng ghi tay); cột `label` dùng để tách các đợt chạy.
