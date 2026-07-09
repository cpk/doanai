# Hướng dẫn chuẩn bị & vận hành buổi bảo vệ (demo — thuyết trình — phản biện)

> File này là bản gốc trong repo; gói mang đi nằm ở thư mục `doanai-bao-ve/`
> (tự dựng lại bằng: `bash harness/make-defense-package.sh`). Cấu trúc gói:
> `01-bao-cao/` · `02-slide/` · `03-so-lieu-hinh/` · `04-phan-bien/` ·
> `05-demo-offline/` · `06-ma-nguon/` + file hướng dẫn này.

## PHẦN A — Cài đặt để demo trực tiếp (làm TRƯỚC ngày bảo vệ)

Máy demo lý tưởng là chính máy đang làm đồ án (mọi thứ đã cài). Nếu dùng máy
khác, cài từ đầu ~15 phút:

1. **Cài Node.js ≥ 20** (LTS): https://nodejs.org (macOS: `brew install node`;
   Windows: `winget install OpenJS.NodeJS.LTS`).
2. **Lấy mã nguồn** — một trong hai cách:
   - Có mạng: `git clone https://github.com/cpk/doanai.git && cd doanai`
   - Không mạng: giải nén `06-ma-nguon/doanai-src.zip` trong gói này rồi `cd` vào.
3. **Cài dependencies** (4 package độc lập):
   ```bash
   (cd app && npm install)
   (cd tests-locator && npm install && npx playwright install chromium)
   (cd tests-vlm && npm install)
   ```
4. **Kiểm tra không cần API key** — baseline phải xanh 30/30 (~40 giây):
   ```bash
   cd tests-locator && npx playwright test
   ```
5. **(Chỉ nếu muốn demo VLM sống)** tạo `tests-vlm/.env` từ `.env.example`,
   điền `MIDSCENE_MODEL_API_KEY` (key OpenRouter). Chạy thử 1 lần trước ở nhà:
   ```bash
   cd tests-vlm && npx playwright test tests/group-a-forms.spec.ts -g "A2"
   ```
   (~40–60 giây, tốn <$0.01.) **Không demo VLM sống nếu chưa chạy thử trước.**
6. **Chuẩn bị fallback:** quay video màn hình 1 lần chạy bước 5 (phòng khi
   phòng bảo vệ không có mạng) — lưu vào `05-demo-offline/` của gói.

## PHẦN B — Checklist mang theo ngày bảo vệ

- [ ] Laptop đã cài sẵn theo Phần A, pin đầy + sạc; tắt notification.
- [ ] Gói `doanai-bao-ve/` (bản mới nhất) trong máy + USB dự phòng.
- [ ] Slide đã mở sẵn; app đã chạy sẵn (Phần C bước 1); 2 tab report offline mở sẵn.
- [ ] Bản in `bao-cao-doan.docx` (nếu khoa yêu cầu) + bản in `HUONG-DAN` này.
- [ ] Điện thoại phát 4G dự phòng nếu định demo VLM sống.

## PHẦN C — Mở mọi thứ (thứ tự thao tác, làm trước giờ G ~20 phút)

1. **Chạy app demo:** `cd app && npm run dev` → mở 4 tab trình duyệt:
   - http://localhost:5173 (V0 — đăng nhập `admin`/`admin123`)
   - http://localhost:5173/products?variant=v1 · `?variant=v2` · `?variant=v3`
2. **Mở slide:** `02-slide/slide-bao-ve.pptx` (PowerPoint/Google Slides) — trình
   chiếu từ slide 1; 6 slide backup nằm sau trang "Slide dự phòng (Q&A)".
3. **Mở 2 report offline** (bằng chứng VLM, không cần mạng):
   `05-demo-offline/vlm-suite-report.html` (cả suite 27/27) và report test đơn —
   mỗi bước có screenshot + prompt + toạ độ VLM trả về.
4. **Mở sẵn 2 file số liệu** (cho phản biện): `03-so-lieu-hinh/analysis-summary.md`
   và `03-so-lieu-hinh/rq2-maintenance.md`.
5. Terminal đứng sẵn ở thư mục repo (để chạy demo Phần D).

## PHẦN D — Kịch bản demo ~4 phút (chèn sau slide 12 hoặc khi hội đồng yêu cầu)

**D1. App + biến thể (45s).** Tab V0: đăng nhập admin, chỉ bảng/nút Delete/cột
Cost. Chuyển tab V2: "cùng chức năng, chỉ đảo bố cục — cột Actions nhảy từ vị
trí 8 lên 1". Tab V3: "nút Add product thành Create item".

**D2. Locator gãy trên V2 — chạy sống (60s).** Terminal:
```bash
cd tests-locator && APP_VARIANT=v2 npx playwright test tests/group-a-forms.spec.ts tests/group-b-list-search.spec.ts tests/group-c-crud.spec.ts tests/group-d-custom-widgets.spec.ts --reporter=line
```
→ hiện `9 failed / 9 passed` sau ~45s. Chỉ vào log: "selector trỏ sai ô — đúng
50% suite gãy như số liệu RQ1".

**D3. VLM pass trên V2 — bằng report offline (60s).** Mở
`vlm-suite-report.html`, mở test A3: chỉ từng bước "the primary button in the
toolbar that adds a new product" + screenshot VLM đã nhìn → "không selector nào,
mô tả ý định — nên V2/V3 không làm nó gãy". (Nếu có mạng + hội đồng muốn xem
sống: `cd tests-vlm && APP_VARIANT=v2 npx playwright test tests/group-a-forms.spec.ts -g "A3"` ~60–90s.)

**D4. Chốt (15s).** Quay lại slide 13 (trade-off): "locator 3 giây nhưng gãy khi
UI đổi; VLM 8 phút + $0.05 nhưng sống sót 100% — hai chế độ chi phí."

## PHẦN E — Bản đồ phản biện (câu hỏi → mở gì)

| Hội đồng hỏi về | Mở | Ghi chú |
|---|---|---|
| "VLM có nhìn cả trang không?" / viewport | Slide backup **B1**; `04-phan-bien/pilot-model-cost.md` mục 7 | phát hiện viewport-bound |
| Độ tin cậy phép đo RQ4 / tọa độ | Slide **B2**; `pilot-model-cost.md` mục 8 | attempt sai được giữ làm tư liệu |
| Vì sao Qwen3-VL, không phải GPT-4o/Claude | Slide **B3**; `pilot-model-cost.md` mục 1 | docs Midscene + bảng giá |
| "AI sửa test thì RQ2 còn ý nghĩa gì?" | Slide **B4**; `03-so-lieu-hinh/rq2-maintenance.md` mục 4 | 2 lần đo độc lập trùng diff từng dòng |
| "Baseline cố tình yếu?" | Slide **B5** | worst-case có chủ ý; nhóm D không có nhãn ngữ nghĩa |
| Chi phí tiền/token | Slide **B6**; `analysis-summary.md` bảng chi phí | tổng ≈ $1.5/$50 |
| Số liệu thô "cho tôi xem" | `03-so-lieu-hinh/matrix-runs.csv` | mỗi test-result 1 dòng, cột label |
| Chi tiết 1 bài báo trong 15 bài | `04-phan-bien/notes-papers.md` | Problem/Method/Result/Limitation từng bài |
| Lỗi phân quyền cấy thế nào | `04-phan-bien/phu-luc.md` Phụ lục C | 5 bug ↔ R1–R5; branch `rq3-seeded-bugs` |
| Tái lập thế nào | `04-phan-bien/phu-luc.md` Phụ lục A | 1 lệnh sinh lại toàn bộ hình/bảng |

## PHẦN F — Sự cố & cách thoát

- **Mất mạng:** demo D2 (locator) vẫn chạy được (không cần mạng); D3 dùng report
  offline; bỏ demo VLM sống.
- **App không chạy:** dùng screenshot trong `03-so-lieu-hinh/screenshots-app-v1/`
  thay cho D1.
- **Máy chiếu lỗi font slide:** dùng bản PDF xuất sẵn từ pptx (xuất trước ở nhà,
  để cạnh file pptx).
- **Hết giờ:** bỏ D2/D3, chỉ D1 + slide 13; mọi số liệu đã nằm trên slide 8–12.
