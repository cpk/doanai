# Kế hoạch thực hiện đồ án — VLM for GUI Testing Automation

> Tổng hợp từ 3 nguồn: đề cương (`DeCuong_VLM_GUI_Testing_TongQuat.docx`), hướng dẫn GVHD (`NghienCuu Step1-4 VLM GUI Testing.pdf`), và mục tiêu: **một sản phẩm đủ hoàn thiện để bảo vệ tốt nghiệp trước 20/09/2026**.
> Cập nhật trạng thái vào file này sau mỗi tuần.

## 1. Sản phẩm cuối cùng (defense package)

Bám đúng **5 Contribution** GVHD đã chốt ở Step 4:

| # | Sản phẩm | Trả lời | Contribution |
|---|----------|---------|--------------|
| 1 | Ứng dụng web mẫu + 3 biến thể giao diện có kiểm soát, công khai GitHub | — | C1 (benchmark tái sử dụng) |
| 2 | Hai bộ test song song (Playwright locator-based & Midscene.js VLM-based) + harness đo 3 trục: robustness / maintenance cost / operating cost | — | C2 (pipeline đánh giá) |
| 3 | Bộ số liệu thực nghiệm định lượng (CSV + biểu đồ) | RQ1, RQ2 | C3 |
| 4 | Module masking ảnh + đánh giá trade-off bảo mật ↔ độ chính xác định vị | RQ4 | C4 |
| 5 | Bộ test phân quyền hiển thị UI theo vai trò (VLM vs locator) | RQ3 | C5 |
| 6 | Báo cáo đồ án (5 chương) + slide + demo | tất cả | — |

4 RQ (theo hướng dẫn GVHD, Step 3):
- **RQ1** — VLM-based cải thiện độ bền vững (tỉ lệ pass) đến mức nào khi giao diện thay đổi (theme, bố cục, biểu tượng)?
- **RQ2** — Chi phí bảo trì test suite (diff LOC/config, thời gian, chi phí API) của 2 phương pháp khác nhau thế nào khi giao diện thay đổi?
- **RQ3** — VLM phát hiện lỗi hiển thị theo phân quyền (role-based UI access) chính xác ra sao so với locator-based?
- **RQ4** — Masking dữ liệu nhạy cảm trên screenshot ảnh hưởng thế nào đến độ chính xác định vị phần tử của VLM?

## 2. Quyết định kỹ thuật (chốt để bắt tay làm)

- **App mẫu**: React + Vite + TypeScript, SPA "quản lý cửa hàng mini" — đủ 4 nhóm chức năng: form nhập liệu (thêm/sửa sản phẩm), danh sách + tìm kiếm/lọc, CRUD, và **thành phần tùy biến không nhãn ngữ nghĩa** (icon-button vẽ SVG không aria-label, rating stars, canvas widget). Có **màn hồ sơ khách hàng chứa PII giả** (tên, SĐT, email, số thẻ mock) phục vụ RQ4. **Login giả lập 2 vai trò** Admin/Staff (Admin thấy thêm: nút Delete, trang Settings, cột giá vốn) phục vụ RQ3. Không backend thật — mock data JSON + localStorage.
- **Biến thể giao diện** (điều khiển bằng query param/env `?variant=`): `V0` gốc → `V1` đổi theme màu + dark mode; `V2` đổi bố cục (sidebar→topbar, đổi vị trí nút, đổi thứ tự cột); `V3` đổi biểu tượng + nhãn (icon khác, đổi text nút "Add"→"Create", đổi placeholder). Mỗi biến thể là 1 nhánh CSS/config, **không đổi logic** — đảm bảo "controlled UI variants" như GVHD yêu cầu.
- **Baseline**: Playwright Test (TypeScript), selector kiểu CSS/XPath cố định (cố ý KHÔNG dùng getByRole/text-based để phản ánh đúng "locator brittleness" — ghi rõ lựa chọn này trong báo cáo, kèm 1 phụ lục thảo luận nếu dùng locator tốt nhất thì sao).
- **VLM**: Midscene.js v1.10.3 tích hợp Playwright. **Đã chốt (GĐ1, 07/07): model chính = Qwen3-VL** (`MIDSCENE_MODEL_FAMILY=qwen3-vl`, qua OpenRouter/DashScope) — GPT-4o bị docs Midscene đánh giá kém về UI grounding, Claude không được hỗ trợ; xem `docs/pilot-model-cost.md`. Model ID snapshot ghim sau pilot chạy thật (chờ API key). Fallback/so sánh phụ: UI-TARS-1.5; dự phòng bảo mật: Qwen-VL self-host.
- **Harness đo**: Node script chạy matrix `{2 phương pháp} × {V0..V3} × {n=5 lần lặp}`, ghi JSON/CSV: pass/fail, thời gian, token in/out, cost ước tính. Biểu đồ vẽ bằng Python (matplotlib) từ CSV.
- **RQ4 đo bằng grounding benchmark riêng** (không sửa lõi Midscene): script chụp screenshot các màn hình chính → tạo bản masked (blur/pixelate vùng PII theo tọa độ biết trước bằng `sharp`) → gọi VLM yêu cầu trả tọa độ phần tử theo 30–50 mô tả ngôn ngữ tự nhiên → so IoU/hit-rate giữa ảnh gốc và ảnh masked.
- **Quy trình đo maintenance cost (RQ2)**: với mỗi biến thể V1–V3, sửa từng bộ test đến khi pass lại toàn bộ; đếm (a) số test case phải sửa, (b) diff LOC (git diff --stat), (c) thời gian sửa (ghi log). Cùng một người sửa, sửa baseline trước VLM sau, theo checklist thống nhất.

## 3. Cấu trúc repo (tạo ở tuần 1, git init tại F:\ai)

```
F:\ai\
├── docs/            # đề cương, hướng dẫn GVHD, ghi chú 15 bài báo, báo cáo, slide
│   └── notes-papers.md   # mỗi bài: Problem/Method/Result/Limitation (GVHD yêu cầu cập nhật liên tục)
├── app/             # React app + variants (V0-V3)
├── tests-locator/   # Playwright test suite
├── tests-vlm/       # Midscene.js test suite
├── masking/         # tiền xử lý ảnh + grounding benchmark (RQ4)
├── harness/         # runner ma trận thực nghiệm, thu CSV
└── results/         # số liệu thô, CSV, biểu đồ, bảng cho Chương 4
```

## 4. Lịch thực hiện theo tuần (07/07 → 20/09/2026)

Khớp 5 mốc trong đề cương; mỗi mốc có Definition of Done (DoD).

### Giai đoạn 1 — Tuần 1 (07–13/07): Nghiên cứu + khởi động ⏳
- Đọc **kỹ** 4 bài GVHD đánh dấu: #1 Survey IEEE TSE 2024, #2 GPTDroid (ICSE'24), #3 VLM web GUI testing (ICSME'24), #4 VisionDroid (arXiv 2407.03037). Đọc abstract+intro 11 bài còn lại. Ghi `docs/notes-papers.md` theo mẫu Problem/Method/Result/Limitation.
- `git init`, tạo cấu trúc repo, scaffold app (Vite), push GitHub (private, public khi bảo vệ).
- **Pilot VLM**: cài Midscene.js, chạy 2–3 lệnh NL trên trang demo bất kỳ với 2–3 model ứng viên → chọn + ghim model, ước lượng chi phí toàn thực nghiệm (mục tiêu < $50).
- **DoD**: notes 15 bài xong; repo chạy `npm run dev`; đã chốt model ID + bảng ước tính chi phí.

### Giai đoạn 2 — Tuần 2–3 (14–27/07): App + baseline tests
- Tuần 2: hoàn thiện app V0 (4 nhóm chức năng + login 2 role + trang PII) + mock data; dựng V1–V3.
- Tuần 3: viết 15–20 test Playwright (phân bố 4 nhóm ~4-5 case/nhóm), chạy xanh trên V0; **tag `app-v1.0`** — freeze app từ đây (mọi thay đổi sau chỉ ở biến thể).
- **DoD**: `npx playwright test` pass 100% trên V0; 4 biến thể chuyển được bằng `?variant=`; demo được từng biến thể.

### Giai đoạn 3 — Tuần 4–7 (28/07–24/08): VLM tests + 2 khảo sát mở rộng
- Tuần 4–5: viết 15–20 test Midscene.js tương ứng 1-1 với baseline (NL instruction + assertion `aiAssert`); chạy xanh trên V0; harness chạy lặp + log token/cost hoạt động.
- Tuần 6: module masking (`sharp`) + grounding benchmark 30–50 mô tả trên ảnh gốc/masked (RQ4).
- Tuần 7: bộ test RBAC — ~6–10 kịch bản hiện diện/vắng mặt phần tử theo role, hiện thực **cả 2 phương pháp**; cài sẵn 3–5 "lỗi phân quyền" cố ý (seeded bugs) vào một build riêng để đo tỉ lệ phát hiện (RQ3).
- **DoD**: cả 2 suite xanh trên V0; harness xuất CSV đúng schema; benchmark RQ4 + suite RQ3 chạy được end-to-end.
- ⚠️ Đệm: nếu tuần 7 trễ, RQ3 seeded-bugs có thể rút còn 3 kịch bản — không được cắt RQ1/RQ2.

### Giai đoạn 4 — Tuần 8–9 (25/08–07/09): Thực nghiệm chính thức + phân tích
- Tuần 8: chạy ma trận chính thức `2 × 4 × 5 lần` (khóa model, khóa app); đo maintenance cost theo quy trình mục 2; chạy RQ3 + RQ4.
- Tuần 9: phân tích số liệu, vẽ biểu đồ (pass-rate theo biến thể, box-plot thời gian, bảng cost, bảng diff LOC); viết nháp Chương 4; **2–3 ngày buffer** cho chạy lại nếu số liệu bất thường.
- **DoD**: `results/` đầy đủ CSV + hình; bảng trả lời từng RQ có số cụ thể.

### Giai đoạn 5 — Tuần 10–11 (08–20/09): Báo cáo + bảo vệ
- Viết báo cáo: Ch1 Giới thiệu (gap từ Step 3), Ch2 Related Work (15 bài Step 2), Ch3 Thiết kế hệ thống & phương pháp, Ch4 Kết quả thực nghiệm (RQ1–4), Ch5 Kết luận (map 5 contribution) + Threats to Validity.
- Slide 15–20 trang + kịch bản demo trực tiếp (chạy 1 test VLM pass trên V2 trong khi Playwright fail) + video demo dự phòng.
- Dọn repo, viết README tái lập (setup, env var API key, lệnh chạy từng thực nghiệm), public GitHub.
- **DoD**: báo cáo hoàn chỉnh nộp GVHD trước ~13/09 để kịp 1 vòng sửa.

## 5. Ánh xạ báo cáo ↔ nguồn liệu

| Chương | Nội dung | Lấy từ |
|--------|----------|--------|
| 1 | Bối cảnh, gap, RQ, đóng góp | Step 1 + 3 + 4 của GVHD |
| 2 | Related work | 15 bài Step 2 + `notes-papers.md` |
| 3 | App, biến thể, 2 suite, harness, masking, RBAC | mục 2–3 file này |
| 4 | Kết quả RQ1–4, thảo luận, threats to validity | `results/` |
| 5 | Kết luận, 5 contribution, hạn chế, hướng phát triển | Step 4 |

## 6. Rủi ro vận hành (ngoài phần đã ghi trong đề cương)

- Chi phí API vượt: pilot tuần 1 phải ra con số $/test-run; nếu > ngân sách → giảm n=5 xuống n=3 hoặc chuyển Qwen2.5-VL.
- Midscene không tương thích model chọn: kiểm tra ngay trong pilot, trước khi viết suite.
- App freeze muộn làm domino: mốc `app-v1.0` (27/07) là mốc cứng — nếu thiếu tính năng phụ thì cắt, không dời.
- Số liệu "quá đẹp" hoặc "quá xấu" một phía: kiểm tra lại thiết kế locator/prompt trước khi kết luận; ghi vào Threats to Validity thay vì giấu.

## 7. Trạng thái (cập nhật hàng tuần)

- [x] GĐ1: Nghiên cứu + pilot (13/07) — **hoàn thành 07/07** trừ 2 việc chờ người dùng:
  - Ghi chú 15/15 bài ✔ (`docs/notes-papers.md`; đính chính: ITeM là ISSTA'25, VETL arXiv 2410.12157, VisionDroid→Trident)
  - Repo + scaffold app ✔ (dev server đã xác minh chạy); pilot script + fixture Midscene ✔
  - Chốt model Qwen3-VL + bảng chi phí (~$3-10, dưới xa ngân sách $50) ✔ (`docs/pilot-model-cost.md`)
  - ⏳ Chờ user: API key (OpenRouter) để chạy pilot thật + ghim model ID snapshot (cần trước GĐ3)
  - Push GitHub: user chủ động yêu cầu sau — hiện chỉ commit local, KHÔNG tự push
  - 📖 Việc tự đọc của sinh viên: đọc kỹ full-text 4 bài ⭐ (notes đã có sẵn khung)
- [x] GĐ2: App + baseline (27/07) — **hoàn thành 07/07, tag `app-v1.0`**
  - App "Mini Shop Manager" đủ 4 nhóm chức năng + login Admin/Staff + trang PII giả ✔
  - 4 biến thể V0–V3 qua `?variant=` (giữ nguyên khi điều hướng) ✔ — screenshot tại `results/screenshots-app-v1/`
  - 18 test Playwright baseline (A:5 form, B:4 list/search, C:4 CRUD, D:5 custom widget) + 4 smoke test biến thể — **22/22 pass trên V0, 3 lần chạy liên tiếp không flaky** ✔
  - Chạy trên biến thể: `APP_VARIANT=v1 npx playwright test` (helper `appUrl()` tự gắn query param)
  - ⚠️ Môi trường: đã nâng Node 18.8 → **24 LTS** (winget) vì Playwright 1.61 không load được config TS trên Node < 18.19
  - App freeze từ tag `app-v1.0`; thay đổi sau này chỉ ở biến thể/seeded-bug build (GĐ3)
- [ ] GĐ3: VLM suite + RQ3/RQ4 (24/08)
- [ ] GĐ4: Thực nghiệm + phân tích (07/09)
- [ ] GĐ5: Báo cáo + slide + repo public (20/09)
