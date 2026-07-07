# Setup máy mới & tiếp tục công việc (handoff)

> Cập nhật cuối: **07/07/2026, cuối ngày** — dùng file này khi pull repo về máy khác để tiếp tục không gián đoạn.

## 1. Trạng thái hiện tại (đang ở đâu)

- **GĐ1 ✔ + GĐ2 ✔** (tag `app-v1.0`, app đã freeze). **GĐ3: xong toàn bộ phần mã nguồn**, chỉ còn phần "chạy thật bằng VLM" đang **chờ API key OpenRouter**. Chi tiết từng mục: `KeHoach_DoAn.md` mục 7.
- Nhánh/tag trên remote `https://github.com/cpk/doanai` (private): `master` (nhánh làm việc), tag `app-v1.0`, branch `rq3-seeded-bugs` (5 lỗi phân quyền cố ý cho RQ3 — KHÔNG merge vào master).
- Đã kiểm chứng trên máy cũ: baseline 22/22 pass trên V0 (3 lần liên tiếp); RBAC locator 8/8 pass trên master, phát hiện 5/5 lỗi trên branch seeded; harness self-test OK; masking capture+mask OK.

## 2. Việc tiếp theo (theo thứ tự)

1. **Có API key OpenRouter** (nạp ~$5) → tạo `tests-vlm/.env` từ `.env.example`, điền `MIDSCENE_MODEL_API_KEY`.
2. Chạy pilot: `cd tests-vlm && npm run pilot` → ghim model ID snapshot + token thực tế/call vào `docs/pilot-model-cost.md` (mục 1 và 3).
3. Chạy xanh VLM suite trên V0: `cd tests-vlm && npx playwright test tests` (tinh chỉnh prompt nếu test nào flaky — ghi lại mọi chỉnh sửa để tính maintenance cost).
4. RBAC VLM trên build lỗi: `git checkout rq3-seeded-bugs` → chạy `npx playwright test tests/rbac` ở tests-vlm → kỳ vọng R1–R5 fail (= phát hiện); quay về `git checkout master`.
5. Benchmark RQ4: `cd masking && npm run benchmark` (dùng chung `.env` của tests-vlm).
6. Bổ sung đếm token/cost vào `harness/run-matrix.mjs` sau khi thấy format report thật của Midscene (`tests-vlm/midscene_run/report/`).

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
