# Setup máy mới & tiếp tục công việc (handoff)

> Cập nhật cuối: **08/07/2026, tối** (máy Mac, sau khi VLM suite xanh toàn bộ trên V0) — dùng file này khi mở session/máy mới để tiếp tục không gián đoạn.

## 1. Trạng thái hiện tại (đang ở đâu)

- **GĐ1 ✔ + GĐ2 ✔** (tag `app-v1.0`, app đã freeze). **GĐ3: VLM suite ĐÃ XANH TOÀN BỘ trên V0 — 27/27 (08/07 tối, 8.7 phút)**; baseline xác nhận lại **30/30** sau khi đổi viewport. Hai fix đã áp dụng: viewport 1280×1100 (cả 2 suite, đối xứng) + B4 dùng `aiInput` `mode:'clear'`. Phát hiện "viewport-bound perception" ghi ở `docs/pilot-model-cost.md` mục 7. Chi tiết từng mục: `KeHoach_DoAn.md` mục 7.
- **Model đã ghim: `qwen/qwen3-vl-235b-a22b-instruct`** qua OpenRouter (lưu ý: `qwen3-vl-plus` KHÔNG tồn tại trên OpenRouter — proprietary, chỉ có trên DashScope). Giá thật: $0.20/M in, $0.88/M out; pilot ≈ $0.0019/lần. Số liệu token/call: `docs/pilot-model-cost.md` mục 6.
- `tests-vlm/.env` đã có trên máy Mac này (key OpenRouter, gitignored). Máy khác: tạo lại từ `.env.example`. ⚠️ Key này đã bị dán vào chat AI — **xoay key sau khi xong thực nghiệm**.
- Lịch sử: lần chạy VLM đầu trên V0 (08/07 chiều, viewport 800px) được 19/27 — 8 test đỏ (A1, A3, A5, B4, C1, C3, C4, D2) đều đã xanh sau 2 fix nói trên; chi tiết chẩn đoán: `docs/pilot-model-cost.md` mục 7.
- Nhánh/tag trên remote `https://github.com/cpk/doanai` (private): `master`, tag `app-v1.0`, branch `rq3-seeded-bugs` (KHÔNG merge vào master).
- Máy Mac: Node 20.11, deps đã cài cho `app/` + `tests-vlm/` + `tests-locator/`, Playwright Chromium đã cài. `masking/` CHƯA `npm install` trên máy này.

## 2. Việc tiếp theo (theo thứ tự) — bắt đầu từ đây

**Đã xong 08/07 tối (các bước 1–6 của kế hoạch cũ):** 2 fix (viewport 1280×1100 cả hai config + B4 `mode:'clear'`) → VLM suite **27/27** trên V0, baseline **30/30**, phát hiện viewport-bound perception ghi ở `docs/pilot-model-cost.md` mục 7, đã commit mốc.

**Còn lại (theo thứ tự):**

1. ✅ (08/07 tối, máy Windows) RBAC VLM trên build lỗi: đã merge master vào `rq3-seeded-bugs` (commit `4daf158`, đã push) rồi chạy qua harness (`--methods vlm --suite rbac --label rq3-seeded-vlm-verify`): **R1–R5 fail đúng thiết kế (phát hiện 5/5), R6–R8 pass**; $0.0052/run. Số liệu nằm trong `results/raw/matrix-runs.csv`.
2. ✅ (08/07 tối) Benchmark RQ4 hoàn tất: hit-rate 100% cả 3 điều kiện, IoU giảm nhẹ trên màn PII (orig 0.737 / blur 0.722 / pixel 0.706 toàn cục), $0.112/360 call → `masking/generated/grounding-results.csv` + `raw-calls.jsonl`. Lưu ý 2 cạm bẫy đã sửa (chuẩn tọa độ 0–1000 của Qwen + item dưới fold): `docs/pilot-model-cost.md` mục 8. Nếu capture lại: cần app chạy (`cd app && npm run dev`), viewport 1280×1100.
3. ✅ (08/07, máy Windows) Token/cost đã vào harness: `harness/token-log.mjs` parse dòng stats (`model, …, prompt-tokens, N, completion-tokens, N, total-tokens, N, cost-ms, N`) từ **mọi** file `tests-vlm/midscene_run/log/*.log` (bản Mac ghi vào `ai-call.log`, source v1.10.3 dùng topic `ai:profile:stats` → quét cả hai); mỗi run VLM thêm 5 cột `run_ai_calls, run_prompt_tokens, run_completion_tokens, run_ai_ms, run_cost_usd` vào `matrix-runs.csv` (locator để trống). Lần chạy VLM đầu tiên qua harness: kiểm tra cột token có số ≠ 0 (nếu 0 sẽ có WARNING trên console).
4. Sau đó vào GĐ4: chạy ma trận chính `harness/run-matrix.mjs --methods locator,vlm --variants v0,v1,v2,v3 --repeats 5`.

Việc sinh viên tự làm song song: đọc kỹ full-text 4 bài ⭐ (khung notes có sẵn trong `docs/notes-papers.md`); điền placeholder GVHD/họ tên/MSSV trong đề cương .docx.

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
