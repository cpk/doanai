# Quyết định model VLM + Ước tính chi phí API (GĐ1)

> Nguồn: tài liệu chính thức midscenejs.com (Model Strategy, Configure Your Model) và bảng giá OpenRouter/OpenAI/Alibaba, tra ngày **07/07/2026**. Con số cuối cùng sẽ được xác nhận lại bằng pilot chạy thật (cần API key).

## 1. Quyết định model

**Model chính (chốt + đã ghim sau pilot thật 08/07/2026): `qwen/qwen3-vl-235b-a22b-instruct`** (`MIDSCENE_MODEL_FAMILY=qwen3-vl`), truy cập qua OpenRouter. Đây là bản snapshot cố định dùng suốt thực nghiệm.

> Đính chính so với dự kiến GĐ1: OpenRouter **không** có `qwen/qwen3-vl-plus` (bản proprietary chỉ tồn tại trên Alibaba DashScope). Danh sách open-weight Qwen3-VL trên OpenRouter gồm các bản 8B/30B-A3B/32B/235B-A22B (instruct & thinking). Đã chọn bản flagship **235B-A22B instruct** để ưu tiên độ chính xác grounding (mục tiêu cốt lõi của đề tài); bản non-thinking để đo flakiness sạch. Xem mục 6.

Căn cứ:
- Docs Midscene xếp Qwen3-VL trong nhóm khuyến nghị mặc định (visual grounding tốt, vượt Qwen2.5-VL).
- Giá rẻ hơn GPT-4o ~10 lần ở input; dễ đăng ký từ VN qua OpenRouter.
- Là VLM mã nguồn mở → nhất quán với phương án dự phòng "self-host khi cần bảo mật dữ liệu" đã ghi trong đề cương.

**Các phương án bị loại / dự phòng:**
| Model | Kết luận | Lý do |
|---|---|---|
| GPT-4o / GPT-5.x | ❌ Loại làm grounding | Docs Midscene ghi rõ các model OpenAI "perform poorly" ở UI localization; chỉ phù hợp vai trò planning |
| Claude | ❌ Loại | Không nằm trong danh sách model được Midscene hỗ trợ chính thức |
| UI-TARS 1.5 7B | 🔁 Dự phòng + so sánh phụ | Rẻ nhất ($0.10/$0.20), chuyên GUI, nhưng docs không khuyến nghị làm mặc định |
| Gemini 3.5 Flash | 🔁 Dự phòng | Docs Midscene đánh giá localization tốt nhất, nhưng hệ sinh thái key/billing phức tạp hơn cho sinh viên |
| Doubao Seed | ❌ Loại | Khuyến nghị mạnh trong docs nhưng đăng ký Volcengine từ VN bất tiện |

**Lưu ý so với đề cương:** đề cương ghi "Claude, GPT-4o hoặc tương đương" — thực tế khảo sát kỹ thuật (GĐ1) cho thấy 2 model này không phù hợp/không được hỗ trợ bởi Midscene; "tương đương" ở đây chốt là Qwen3-VL. Cần báo lại GVHD trong buổi trao đổi tuần 1 (đây là kết quả khảo sát, đúng tinh thần Nội dung 1).

## 2. Bảng giá (USD / 1M token, tra 07/07/2026)

| Model | Input | Output | Nguồn |
|---|---|---|---|
| Qwen3-VL-Plus | $0.20 | $1.60 | Alibaba Model Studio (qua CloudPrice; có tiered pricing theo context — tra lại bảng chính thức khi chạy) |
| Qwen2.5-VL-72B | $0.80 | $1.00 | OpenRouter |
| UI-TARS-1.5-7B | $0.10 | $0.20 | OpenRouter (ByteDance) |
| GPT-4o (tham chiếu) | $2.50 | $10.00 | OpenRouter (OpenAI đã bỏ niêm yết, thay bằng GPT-5.x: $2.50/$15.00) |

## 3. Ước tính khối lượng token toàn thực nghiệm

Giả định (xác nhận lại bằng pilot): mỗi call Midscene gửi 1 screenshot 1280×800 ≈ 1.300 image token + context ≈ **2.000 input token/call**, ~150 output token/call; mỗi test case ≈ 7 call (5 action + 2 assert).

| Hạng mục | Lượt | Input tokens | Output tokens |
|---|---|---|---|
| Ma trận chính (20 test × 4 UI × 5 lặp = 400 lượt test) | ~2.800 call | ~5,6M | ~0,42M |
| RQ3 phân quyền (~10 kịch bản × 2 role × 5 lặp) | ~700 call | ~1,4M | ~0,1M |
| RQ4 grounding benchmark (50 mô tả × 2 ảnh × 3 lặp) | ~300 call | ~0,6M | ~0,05M |
| Dev/debug/pilot (hệ số ×1,4) | — | ~3,0M | ~0,23M |
| **Tổng** | | **~10,6M** | **~0,8M** |

## 4. Chi phí ước tính theo model

| Model | Chi phí ước tính | So với ngân sách $50 |
|---|---|---|
| **Qwen3-VL-Plus (chính)** | 10,6×$0.20 + 0,8×$1.60 ≈ **$3,4** | ✅ ~7% |
| Qwen2.5-VL-72B | ≈ $9,3 | ✅ ~19% |
| UI-TARS-1.5-7B | ≈ $1,2 | ✅ ~2% |
| GPT-4o (nếu đã dùng) | ≈ $34,5 | ⚠️ ~69% |

→ Với Qwen3-VL, hoàn toàn đủ ngân sách để tăng số lần lặp lên n=5 và chạy lại khi có sự cố. Kể cả chạy song song thêm UI-TARS làm model so sánh phụ, tổng vẫn < $10.

**Cảnh báo đo lường:** chi phí thực bị chi phối bởi image token — quy tắc quy đổi khác nhau giữa provider. Harness phải đọc `usage` từ API response để đếm token thật thay vì ước theo công thức.

## 5. Việc còn lại để đóng pilot (cần người dùng)

1. ✅ Tạo API key OpenRouter (đã có, cấu hình trong `tests-vlm/.env`).
2. ✅ `.env` đã tạo với `MIDSCENE_MODEL_*` trỏ tới model ghim.
3. ✅ Chạy `npm run pilot` — PASS.
4. ✅ Ghim model ID + số token thật (mục 1 và 6).

## 6. Pilot thật — số liệu đo được (08/07/2026)

- **Model ghim:** `qwen/qwen3-vl-235b-a22b-instruct` qua OpenRouter, `temperature=0`, cache TẮT.
- **Giá thật OpenRouter (tra 08/07/2026):** input **$0.20/M**, output **$0.88/M**, image ~$0 (gộp vào prompt token). Rẻ hơn giả định `qwen3-vl-plus` cũ ($1.60/M output) → chi phí thực nghiệm thực tế còn thấp hơn ước tính mục 4.
- **Kết quả pilot:** đăng nhập bằng NL (admin/admin123) + đọc bảng Products → PASS (19.6s wall-clock, 5 AI call).

| AI call | in tokens | out tokens | latency |
|---|---|---|---|
| aiInput username | 1 551 | 36 | 4.8s |
| aiInput password | 1 551 | 36 | 2.5s |
| aiTap submit | 1 551 | 36 | 1.2s |
| aiAssert "Products table" | 1 759 | 86 | 2.1s |
| aiNumber "count rows" | 1 745 | 137 | 2.9s |
| **Tổng** | **8 157** | **331** | — |

- **Token/call trung bình:** ~1 630 in / ~66 out (khớp tốt giả định mục 3: ~2 000 in/call).
- **Chi phí pilot 1 lần:** 8 157×$0.20/M + 331×$0.88/M ≈ **$0.0019** (~1/5 cent).
- **Ước tính lại toàn thực nghiệm** theo token/call thật + giá thật: ~10,6M in + 0,8M out ≈ 10,6×$0.20 + 0,8×$0.88 ≈ **$2,8** → vẫn ✅ ~6% ngân sách $50.

**Quan sát grounding (ghi cho Threats to Validity):** ở call `aiNumber`, VLM đếm **9 dòng** trong khi bảng có **12**. ~~Ban đầu nghi là sai số đếm/định vị trên bảng dày~~ — đã chẩn đoán lại sau lần chạy full suite: đây KHÔNG phải lỗi grounding mà là **nhận thức bị giới hạn viewport**, xem mục 7.

## 7. Phát hiện phương pháp luận: VLM perception là viewport-bound (08/07/2026)

Lần chạy VLM suite đầu tiên trên V0 cho 19/27 (RBAC 8/8 xanh; 8 test main đỏ: A1, A3, A5, B4, C1, C3, C4, D2). Chẩn đoán bằng đo đạc:

- **7/8 test đỏ có chung một nguyên nhân:** viewport 1280×800 chỉ hiển thị **9/12** dòng bảng Products (trang cao 976px, mỗi dòng 47px). VLM đếm đúng những gì nó **thấy trong screenshot** → `aiNumber` trả 9 thay vì 12, và trả **cùng giá trị 9 ở mọi lần lặp** (temperature=0) — tức là **deterministic, không phải flaky**. D2 fail vì dòng "Premium Coffee Beans" nằm dưới fold. Quan sát "đếm 9/12" ở pilot (mục 6) chính là hiện tượng này.
- **B4 là bug viết test, không liên quan:** `aiInput` với `value: ''` không xóa ô search — cần `mode: 'clear'` (đã sửa).
- **Baseline không bị ảnh hưởng** vì locator đếm DOM, không đếm pixel.

**Cách xử lý (đã áp dụng):** tăng viewport lên **1280×1100** trong cả hai config (`tests-vlm` + `tests-locator`, giữ đối xứng điều kiện thí nghiệm) để toàn bộ bảng lọt trọn một screenshot. Phương án "giữ 800px + cuộn trước khi đếm" bị loại: sau khi cuộn, các dòng đầu ra khỏi màn hình — đếm vẫn thiếu.

**Ý nghĩa cho báo cáo (Chương 4 / Threats to Validity):**
- Khác biệt bản chất giữa hai phương pháp: **locator truy vấn DOM (toàn trang), VLM truy vấn ảnh chụp (chỉ phần nhìn thấy)**. Mọi phép đo dạng "đếm/kiểm tra toàn cục" bằng VLM đều ngầm giả định nội dung lọt trọn viewport.
- Kích thước viewport là **biến nhiễu (confounder)** của thực nghiệm so sánh — phải cố định và báo cáo tường minh; kết quả VLM không khái quát sang trang dài hơn viewport nếu không có cơ chế cuộn + tổng hợp.
- Fail do viewport là **deterministic** ở temperature=0 — nếu không chẩn đoán, dễ quy nhầm thành "VLM không chính xác" thay vì "VLM không nhìn thấy"; ảnh hưởng cách diễn giải pass rate ở RQ1.
