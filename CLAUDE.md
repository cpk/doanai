# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Đồ án tốt nghiệp (UIT – ĐHQG TP.HCM): **"Ứng dụng Vision-Language Model (VLM) trong Kiểm thử Tự động Giao diện Người dùng Phần mềm"** (Vision-Language Models for Automated Software UI Testing). Thời gian thực hiện: 07/07/2026 → 20/09/2026.

Đề tài này là lựa chọn **đã chốt** giữa 2 đề cương GVHD đưa ra: chọn "Vision-Language Models for GUI Testing" (đề tài này), không chọn "Semantic UI Testing using Vision Transformers".

Ba tài liệu gốc, đọc theo thứ tự khi cần bối cảnh:
1. `DeCuong_VLM_GUI_Testing_TongQuat.docx` — đề cương chính thức (mục tiêu, phạm vi, kế hoạch 5 mốc). Đọc .docx bằng python-docx (đã cài, chạy qua `py`).
2. `NghienCuu Step1-4 VLM GUI Testing.pdf` — hướng dẫn của GVHD: từ khóa tìm kiếm, **15 bài báo SOTA phải khảo sát** (4 bài đọc kỹ: Survey IEEE TSE 2024, GPTDroid ICSE'24, VLM-web-GUI ICSME'24, VisionDroid), 3 research gap, 4 RQ, **5 contribution bắt buộc của sản phẩm cuối**. Trích text PDF bằng pypdf (đã cài).
3. `KeHoach_DoAn.md` — kế hoạch thực hiện chi tiết theo tuần (07/07→20/09/2026), quyết định kỹ thuật đã chốt, cấu trúc repo dự kiến, DoD từng giai đoạn. **Cập nhật trạng thái ở mục 7 của file này khi hoàn thành công việc.**

**Ngôn ngữ làm việc:** trao đổi với người dùng và viết báo cáo/tài liệu bằng tiếng Việt; code, comment và tên file bằng tiếng Anh.

## Research Design (đã chốt trong đề cương)

Mục tiêu cốt lõi: **so sánh thực nghiệm định lượng** giữa hai phương pháp kiểm thử GUI trên cùng một ứng dụng mẫu:

1. **Baseline (locator-based):** Playwright (đã chốt, không dùng Selenium/WinAppDriver; desktop chỉ là hướng phát triển), 15–20 test case định vị phần tử bằng CSS selector/XPath.
2. **VLM-based (vision-centric):** Midscene.js + VLM đa phương thức (Claude/GPT-4o hoặc tương đương) qua API, cùng 15–20 test case đó viết lại bằng ngôn ngữ tự nhiên. **Không** huấn luyện/fine-tune mô hình; **ghim model ID cố định** suốt thực nghiệm.

Bốn câu hỏi nghiên cứu (thứ tự theo hướng dẫn GVHD): RQ1 robustness khi giao diện thay đổi; RQ2 chi phí bảo trì (diff LOC, thời gian, chi phí API); RQ3 phát hiện lỗi phân quyền hiển thị (role-based UI); RQ4 trade-off masking ↔ độ chính xác định vị. RQ3/RQ4 ghi "mở rộng" trong đề cương nhưng là Contribution 4-5 bắt buộc theo GVHD — kế hoạch làm đủ cả bốn.

Cấu trúc thực nghiệm:
- **Ứng dụng web mẫu** tự xây với form nhập liệu, danh sách, tìm kiếm, CRUD, và một số thành phần tùy biến gây khó cho locator truyền thống. Dữ liệu hoàn toàn là mock data.
- **15–20 test case phân bố đều 4 nhóm:** form nhập liệu; danh sách/tìm kiếm; CRUD; thành phần tùy biến không nhãn ngữ nghĩa.
- **2–3 biến thể giao diện** (đổi theme màu, bố cục, biểu tượng) để đo độ bền vững (robustness) — cả hai bộ test chạy lại trên từng biến thể.
- **Mỗi test chạy lặp 3–5 lần** (VLM non-deterministic) để đo cả flakiness, không chỉ pass/fail một lần.
- **Chỉ số đo:** tỉ lệ pass trên giao diện gốc và từng biến thể; độ ổn định (flakiness); thời gian thực thi; chi phí API (token, tiền, độ trễ); chi phí bảo trì = số test case phải sửa + diff LOC khi giao diện thay đổi (cùng một người sửa cả hai bộ theo quy trình thống nhất để tránh thiên lệch).

Hai nội dung mở rộng (tùy thời gian, mức "khảo sát bước đầu"):
- **Che dữ liệu nhạy cảm:** tiền xử lý ảnh (blur/pixelation theo tọa độ biết trước) trước khi gửi screenshot lên VLM API, rồi đánh giá trade-off che giấu ↔ độ chính xác định vị của VLM.
- **Kiểm thử phân quyền hiển thị (role-based UI access):** 2 vai trò người dùng, dùng VLM xác minh phần tử của vai trò quyền cao không hiển thị nhầm cho vai trò quyền thấp; **chạy đối chứng cả bằng Playwright**. Chỉ ở mức front-end/visual, không kiểm thử backend.

Dự phòng rủi ro (đã ghi trong đề cương): pilot ước lượng ngân sách API; ghim model ID; khóa phiên bản Midscene.js bằng lockfile; fallback VLM mã nguồn mở chạy cục bộ (Qwen2.5-VL, UI-TARS).

Sản phẩm cam kết gồm cả mã nguồn công khai (app mẫu, hai bộ test, script đo lường) + tài liệu tái lập thực nghiệm. Quyết định còn để mở duy nhất: mức độ đi sâu của phần bảo mật (thống nhất với GVHD).

## Current State & Repository Structure

Repo đã init git (GĐ1 xong 07/07/2026, chưa có remote). Cấu trúc: `app/` (Vite + React + TS — app thực nghiệm), `tests-locator/` (Playwright baseline), `tests-vlm/` (Midscene.js v1.10.3 + pilot), `masking/`, `harness/`, `results/`, `docs/` (đề cương, hướng dẫn GVHD, `notes-papers.md` — ghi chú 15 bài đã xác minh, `pilot-model-cost.md` — quyết định model + chi phí).

Commands:
- App: `cd app && npm run dev` → http://localhost:5173
- Test VLM/pilot: `cd tests-vlm && npm run pilot` (cần `.env` theo `.env.example`; app phải đang chạy)
- Test baseline: `cd tests-locator && npx playwright test`

Quyết định kỹ thuật đã chốt (GĐ1): model VLM = **Qwen3-VL** (`MIDSCENE_MODEL_FAMILY=qwen3-vl`); GPT-4o/Claude bị loại (docs Midscene: GPT kém UI grounding, Claude không hỗ trợ). Cấu hình qua bộ biến `MIDSCENE_MODEL_*` (không dùng `OPENAI_API_KEY` cũ). **Không bật `MIDSCENE_CACHE`** khi chạy thực nghiệm — làm sai lệch đo flakiness. Môi trường: Node 18.8 (cảnh báo EBADENGINE nhưng chạy được; cân nhắc lên Node 20 LTS nếu gặp lỗi runtime), Python qua `py`, không có `gh` CLI.

## Key References

Các công trình khảo sát trong Nội dung 1: AppAgent, Mobile-Agent, CogAgent, Ferret-UI, SeeClick, WebVoyager; tài liệu Midscene.js, Playwright, WinAppDriver; OWASP Top 10 (Broken Access Control, Sensitive Data Exposure).
