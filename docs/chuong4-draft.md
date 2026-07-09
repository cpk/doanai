# Chương 4 — Kết quả thực nghiệm và thảo luận (BẢN NHÁP)

> Bản nháp sinh ngày 09/07/2026 từ số liệu chính thức trong repo. Mọi con số đều
> tái lập được: bảng tổng hợp `results/analysis-summary.md` và 5 hình
> `results/figures/` do `harness/make-figures.py` sinh từ
> `results/raw/matrix-runs.csv` + `masking/generated/grounding-results.csv`.
> Chỗ đánh dấu ⚠️ TODO cần bổ sung/quyết định trước khi đưa vào báo cáo chính thức.

## 4.1. Thiết lập thực nghiệm

- **Ứng dụng đo:** "Mini Shop Manager" (Vite + React + TS, mock data), 2 vai trò
  đăng nhập (admin/staff), trang hồ sơ khách hàng chứa PII giả. Ứng dụng đóng băng
  tại tag `app-v1.0`; 4 biến thể trình bày V0 (gốc), V1 (dark theme), V2 (topbar +
  đảo thứ tự cột/toolbar/icon hành động), V3 (đổi bộ icon + nhãn nút/placeholder)
  cấu hình tập trung tại `app/src/variants.ts` — chỉ đổi trình bày, không đổi logic.
- **Hai bộ test đối xứng 1–1, mỗi bộ 18 test** chia 4 nhóm: A form nhập liệu (5),
  B danh sách/tìm kiếm (4), C CRUD (4), D thành phần tùy biến không nhãn ngữ nghĩa (5).
  - *Baseline (locator-based):* Playwright, selector CSS/XPath cố định (nth-child,
    XPath neo text) — chủ ý đại diện cho lớp test giòn phổ biến trong thực tế.
  - *VLM-based:* Midscene.js v1.10.3 + model ghim `qwen/qwen3-vl-235b-a22b-instruct`
    (OpenRouter, `MIDSCENE_MODEL_FAMILY=qwen3-vl`), test viết bằng ngôn ngữ tự nhiên,
    temperature = 0, cache tắt, không huấn luyện/fine-tune.
- **Quy trình đo:** harness `harness/run-matrix.mjs` chạy ma trận
  {phương pháp} × {biến thể} × {5 lần lặp}, ghi từng test-result kèm wall-clock,
  số AI call, token in/out và chi phí API (giá ghim $0.20/M in, $0.88/M out) vào
  `results/raw/matrix-runs.csv`. Viewport cố định 1280×1100 cho cả hai bộ
  (lý do: mục 4.7). Môi trường: Node 24 LTS, Playwright 1.61, Chromium.

## 4.2. RQ1 — Độ bền vững khi giao diện thay đổi

*Hình:* `fig-rq1-passrate.png`, `fig-rq1-time-cost.png` (label `gd4-main`, 2×4×5 = 720 dòng).

| Phương pháp | V0 | V1 (theme) | V2 (bố cục) | V3 (icon/nhãn) |
|---|---|---|---|---|
| Locator | 18/18 | 18/18 | **9/18 (50%)** | **12/18 (67%)** |
| VLM | 18/18 | 18/18 | **18/18** | **18/18** |

- **Flakiness = 0 ở cả hai phương pháp:** kết quả giống hệt qua 5 lần lặp trên mọi
  ô của ma trận. Với VLM, tính tất định có được nhờ temperature = 0 + tắt cache;
  đây là điểm đáng chú ý vì lo ngại ban đầu (đề cương) là VLM non-deterministic.
- Locator "miễn nhiễm" với đổi theme (V1: DOM không đổi) nhưng gãy đúng ở những
  thay đổi cấu trúc (V2: mọi selector `nth-child` trỏ sai ô) và nhãn (V3: XPath neo
  text nút không khớp). Phân bố test gãy theo nhóm: V2 gãy A×1, B×1, C×4, D×3;
  V3 gãy A×3, C×2, D×1 — nhóm CRUD/custom-widget (vốn phải dùng selector cấu trúc
  vì không có nhãn ngữ nghĩa) chịu ảnh hưởng nặng nhất.
- VLM pass 100% trên cả 4 biến thể mà không sửa gì: mô tả ngôn ngữ tự nhiên
  ("nút Delete của dòng đầu tiên", "cột SKU") bất biến với vị trí cột, thứ tự icon
  và cả việc đổi nhãn nút (model đọc ngữ nghĩa màn hình thay vì khớp chuỗi).
- **Giá của độ bền vững đó:** VLM ~437–538 s/run so với locator ~3 s (V0/V1);
  chi phí API ~$0.050/run (~93 AI call, ~232k token). Locator trên V2/V3 mất ~32 s
  do các test hỏng chờ hết timeout — bản thân thời gian chạy cũng là một tín hiệu
  "suite đang gãy" ở phía locator.

**Trả lời RQ1:** với thay đổi thuần trình bày, bộ test VLM bền vững hơn hẳn
(100% so với 50–67% ở biến thể cấu trúc/nhãn); đổi lại chậm hơn ~2 bậc độ lớn và
phát sinh chi phí API mỗi lần chạy.

## 4.3. RQ2 — Chi phí bảo trì

*Hình:* `fig-rq2-maintenance.png`; chi tiết: `results/rq2-maintenance.md`.

Quy trình: sửa tối thiểu bộ locator cho pass lại 18/18 trên từng biến thể
(chỉ đổi selector/assertion, không refactor), mỗi biến thể một branch riêng
(`rq2-fix-v2` = commit `bc5f071`, `rq2-fix-v3` = commit `3eb8809`); đo số test
phải sửa + diff LOC bằng `git diff --stat`.

| Biến thể | Locator: test sửa | Locator: diff LOC (+/−) | VLM: test sửa | VLM: diff LOC |
|---|---:|---:|---:|---:|
| V1 | 0 | 0 | 0 | 0 |
| V2 | 9 | 24 (12+/12−) | 0 | 0 |
| V3 | 6 | 22 (11+/11−) | 0 | 0 |
| **Tổng** | **15** | **46** | **0** | **0** |

- Phía VLM, "chi phí bảo trì" khi giao diện đổi là **0** trên cả 3 biến thể —
  nhưng bản chất kinh tế của hai phương pháp khác nhau: locator trả chi phí
  **một lần, khi giao diện đổi** (công sửa script); VLM trả chi phí **mỗi lần
  chạy** ($0.050/run + 7–10 phút). Điểm hòa vốn phụ thuộc tần suất đổi giao diện
  so với tần suất chạy CI. ⚠️ TODO: có thể thêm 1 đoạn ước lượng break-even
  minh họa (ví dụ: 46 LOC ≈ X phút công so với N run × $0.05).
- Chỉ số **thời gian phục hồi bộ test**: theo đề cương (bản cập nhật 09/07/2026),
  việc bảo trì do cùng một quy trình chuẩn hóa tự động thực hiện (AI coding agent,
  chỉ dẫn sửa-tối-thiểu cố định) nên thời gian đo được là thời gian phục hồi của
  quy trình đó — tái lập được, không phụ thuộc người sửa. ⚠️ TODO: đo trên branch
  `rq2-agent-v2`/`rq2-agent-v3` rồi điền số vào đây (VLM = 0 phút, không phải sửa).

**Trả lời RQ2:** trên 3 biến thể có kiểm soát, bộ locator cần sửa 15 lượt test /
46 LOC để phục hồi, bộ VLM cần 0; chi phí của VLM dịch chuyển từ "bảo trì" sang
"vận hành" (API + thời gian chạy).

## 4.4. RQ3 — Phát hiện lỗi phân quyền hiển thị (role-based UI)

*Hình:* `fig-rq3-detection.png` (label `gd4-rbac-clean`, `gd4-rbac-seeded`).

Thiết kế: 8 kịch bản RBAC (R1–R8) chạy bằng cả hai phương pháp trên (i) build
sạch (`master`) và (ii) build cấy 5 lỗi phân quyền hiển thị cố ý (branch
`rq3-seeded-bugs`: phần tử của admin lộ ra với staff — nút Delete, cột Cost,
trang Settings, …); mỗi tổ hợp lặp 5 lần.

| Phương pháp | Detection (R1–R5 trên build lỗi) | False alarm (R6–R8 + build sạch) | Chi phí |
|---|---|---|---|
| Locator | **5/5**, fail đủ 5/5 lặp | 0 | $0, ~2 s/run |
| VLM | **5/5**, fail đủ 5/5 lặp | 0 | $0.0052/run, ~50–75 s/run |

- Cả hai phương pháp đạt detection 100%, không báo động giả, hoàn toàn ổn định
  qua 5 lặp. Trên lớp lỗi "phần tử quyền cao hiển thị nhầm cho vai trò quyền thấp"
  (OWASP Broken Access Control, khía cạnh front-end), khả năng phát hiện là
  tương đương; VLM không thể hiện lợi thế phát hiện trên app mẫu này, nhưng cũng
  không thua kém — trong khi kịch bản VLM viết bằng mô tả tự nhiên ("staff không
  được thấy nút Delete") nên kế thừa luôn độ bền vững trước thay đổi giao diện
  đã đo ở RQ1.
- Giới hạn phạm vi: chỉ kiểm thử hiển thị front-end, không kiểm thử API/backend.

**Trả lời RQ3:** VLM dùng được như một cơ chế kiểm thử phân quyền hiển thị với
độ chính xác ngang baseline (5/5 detection, 0 false alarm) ở chi phí ~$0.005/run.

## 4.5. RQ4 — Trade-off che dữ liệu nhạy cảm ↔ độ chính xác định vị

*Hình:* `fig-rq4-hitrate-iou.png` (`masking/generated/grounding-results.csv`,
360 call = 40 item × 3 điều kiện × 3 lặp, $0.112).

Thiết kế: 40 mục tiêu định vị trên 4 màn hình (login, products-admin và 2 trang
hồ sơ khách hàng chứa PII); ảnh gửi VLM ở 3 điều kiện: gốc, blur, pixelate
(mask theo tọa độ PII biết trước, bằng sharp). Đo hit-rate (tâm dự đoán rơi vào
ground-truth box) và IoU.

| Màn hình | Gốc | Blur | Pixelate |
|---|---|---|---|
| login (không mask) | 100% / 0.876 | 100% / 0.863 | 100% / 0.861 |
| products-admin (không mask) | 100% / 0.656 | 100% / 0.651 | 100% / 0.652 |
| customer-c01 (PII, có mask) | 100% / 0.764 | 100% / 0.737 | 100% / 0.709 |
| customer-c03 (PII, có mask) | 100% / 0.806 | 100% / 0.779 | 100% / 0.730 |

- **Hit-rate 100% ở cả 3 điều kiện**, kết quả tất định qua 3 lặp: masking không
  làm VLM mất khả năng tìm đúng phần tử.
- IoU giảm nhẹ và **chỉ trên 2 màn có mask** (tối đa −0.076, pixelate > blur),
  hai màn không mask giữ nguyên (đối chứng nội bộ, loại trừ nhiễu do điều kiện chạy).
  Mức giảm không đổi hit-rate → suy giảm chỉ ở độ khít của box, không ở khả năng
  định vị.

**Trả lời RQ4:** trong phạm vi khảo sát bước đầu này, có thể che PII trước khi
gửi screenshot lên VLM API mà **không** đánh đổi khả năng định vị phần tử;
trade-off chỉ xuất hiện dưới dạng IoU giảm nhẹ tại đúng vùng bị che.

## 4.6. Thảo luận chung

1. **Trade-off trung tâm (robustness ↔ thời gian/chi phí):** VLM đổi ~2 bậc độ
   lớn về thời gian chạy và $0.05/run lấy (i) pass 100% trên mọi biến thể trình bày
   và (ii) chi phí bảo trì bằng 0 khi giao diện đổi. Locator gần như miễn phí và
   tức thời khi giao diện ổn định, nhưng mất 33–50% suite khi đổi bố cục/nhãn và
   cần can thiệp tay (15 lượt test / 46 LOC) để phục hồi.
2. **Tính tất định của VLM ở temperature = 0** (flakiness = 0 trên 720 + 160 dòng
   đo + 360 call grounding) cho thấy lo ngại "VLM non-deterministic" có thể kiểm
   soát được ở tầng cấu hình — nhưng chỉ trong điều kiện model ghim cố định và
   input ổn định; không khái quát sang model/provider khác.
3. **Chi phí tuyệt đối nhỏ nhưng cấu trúc chi phí khác nhau:** toàn bộ thực nghiệm
   (~$1.5) nằm dưới xa ngân sách $50; điểm quyết định khi áp dụng thực tế không
   phải giá một run mà là tần suất chạy CI × thời gian chờ 7–10 phút/suite.
4. **Hai phát hiện phương pháp luận** (chi tiết `docs/pilot-model-cost.md` mục 7–8)
   có giá trị thực hành khi tích hợp VLM vào kiểm thử: (i) perception của VLM là
   viewport-bound — locator truy vấn DOM toàn trang còn VLM chỉ "thấy" screenshot;
   (ii) quy ước tọa độ grounding của model (Qwen3-VL: 0–1000) thắng chỉ dẫn trong
   prompt — harness phải theo model, và phải tách bạch "lỗi model" với "lỗi harness"
   trước khi kết luận.

## 4.7. Threats to Validity

1. **Construct — viewport là biến nhiễu:** VLM chỉ nhận thức phần nội dung lọt
   viewport (1280×1100, đã cố định và báo cáo tường minh); kết quả không khái quát
   sang trang dài hơn viewport nếu không có cơ chế cuộn + tổng hợp.
2. **Construct — chấm điểm grounding phụ thuộc parser:** attempt 1 của RQ4 sai do
   harness chấm sai chuẩn tọa độ 0–1000 của Qwen (tư liệu:
   `grounding-results-invalid-attempt1.csv`); kết quả công bố dùng parser đã sửa
   và lưu raw answer để audit.
3. **Internal — baseline chủ ý dùng selector giòn:** suite locator dùng
   nth-child/XPath-text cố định, đại diện cho lớp test giòn phổ biến; một baseline
   dùng best practice (`getByRole`, `data-testid`) sẽ bền hơn trước V2/V3 — kết quả
   RQ1/RQ2 phải đọc trong phạm vi lớp selector này. ⚠️ TODO: cân nhắc 1 đoạn
   định vị rõ "worst-case baseline" hay bổ sung biến thể baseline bền (nếu còn giờ).
4. **External — một ứng dụng, một model:** app mẫu nhỏ (12 dòng dữ liệu, mock),
   một model duy nhất (Qwen3-VL 235B qua OpenRouter), biến thể giao diện là thay
   đổi có kiểm soát một chiều; không khái quát sang app phức tạp, model khác hay
   redesign lớn.
5. **Internal — bảo trì bằng quy trình tự động (RQ2):** việc sửa do một AI coding
   agent chuẩn hóa thực hiện (thiết kế trong đề cương, nhằm chống thiên lệch giữa
   hai bộ và tái lập được). Hai chỉ số số-test-sửa và diff-LOC gần như bất biến
   theo tác nhân sửa (quy tắc sửa tối thiểu); riêng **thời gian phục hồi** là thời
   gian của tác nhân tự động, KHÔNG đại diện cho công sức bảo trì thủ công của kỹ
   sư kiểm thử — chỉ dùng để so sánh tương đối giữa hai bộ test trong cùng quy trình.
6. **Conclusion — kết quả tất định che khuất phương sai tiềm ẩn:** flakiness = 0
   đo được ở temperature = 0 với input tĩnh; thay đổi nhỏ về render (font, AA,
   độ phân giải) hoặc provider routing có thể tạo phương sai chưa quan sát được.

---

⚠️ TODO tổng khi chuyển vào báo cáo chính thức: (1) chèn hình từ
`results/figures/` + đánh số bảng/hình theo template của khoa; (2) chốt mục thời
gian RQ2 theo ý GVHD; (3) đối chiếu thuật ngữ với Chương 2 (khảo sát 15 bài) và
trích dẫn lại các bài liên quan khi thảo luận (GPTDroid, VisionDroid/Trident,
survey TSE 2024...).
