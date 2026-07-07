# Quyết định model VLM + Ước tính chi phí API (GĐ1)

> Nguồn: tài liệu chính thức midscenejs.com (Model Strategy, Configure Your Model) và bảng giá OpenRouter/OpenAI/Alibaba, tra ngày **07/07/2026**. Con số cuối cùng sẽ được xác nhận lại bằng pilot chạy thật (cần API key).

## 1. Quyết định model

**Model chính (chốt): Qwen3-VL** (`MIDSCENE_MODEL_FAMILY=qwen3-vl`), truy cập qua OpenRouter (`qwen/qwen3-vl-plus`) hoặc DashScope international. Model ID chính xác (bản snapshot) sẽ ghim sau lần pilot chạy thật đầu tiên và ghi vào đây + báo cáo.

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

1. Tạo API key (khuyến nghị OpenRouter: https://openrouter.ai — nạp tối thiểu $5).
2. `cd tests-vlm && copy .env.example .env` → điền `MIDSCENE_MODEL_API_KEY`.
3. Chạy app (`cd app && npm run dev`) rồi `cd tests-vlm && npm run pilot`.
4. Ghim model ID snapshot + số token thực tế/call vào file này (mục 1 và 3).
