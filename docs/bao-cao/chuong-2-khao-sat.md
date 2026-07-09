# Chương 2 — Cơ sở lý thuyết và khảo sát liên quan (BẢN NHÁP ĐẦY ĐỦ)

> Nháp hoàn chỉnh 09/07/2026, viết từ `docs/notes-papers.md` (ghi chú đã xác minh
> nguồn của 15 bài). ⚠️ Ghi chú 15 bài được tổng hợp với sự hỗ trợ AI — khi đọc
> full-text 4 bài ⭐, đối chiếu lại số liệu in đậm trong 2.3 trước khi nộp.
> Số [n] theo thứ tự trong `notes-papers.md`, cũng là thứ tự danh mục tham khảo.

Chương này trình bày nền tảng lý thuyết của hai cách tiếp cận kiểm thử GUI được
so sánh trong đồ án (2.1), khảo sát có hệ thống 15 công trình tiêu biểu giai
đoạn 2023–2025 theo ba nhánh (2.2), phân tích sâu bốn công trình đại diện (2.3),
và định vị đóng góp của đồ án trong bức tranh đó (2.4).

## 2.1. Cơ sở lý thuyết

### 2.1.1. Kiểm thử GUI tự động và cách tiếp cận locator-based

Kiểm thử GUI tự động mô phỏng thao tác người dùng trên giao diện (điền form,
bấm nút, đọc kết quả) và so khớp trạng thái quan sát được với kỳ vọng (test
oracle). Trong hệ sinh thái web, mô hình chủ đạo là **script hóa với locator**:
mỗi bước tương tác định vị phần tử qua CSS selector, XPath hoặc thuộc tính
accessibility, rồi gọi hành động trên phần tử đó. Playwright — framework được
dùng làm baseline của đồ án — bổ sung các cơ chế hiện đại như auto-wait (tự chờ
phần tử sẵn sàng), quản lý trình duyệt và tự khởi động ứng dụng được kiểm thử,
giúp loại phần lớn flakiness do timing.

Điểm yếu cấu trúc của mô hình này nằm ở chính locator. Có thể phân ba nguyên
nhân gãy test kinh điển: (i) **đổi hình thức** (màu sắc, theme) — thường vô hại
vì DOM không đổi; (ii) **đổi cấu trúc** (đảo thứ tự cột, chuyển bố cục) — làm
sai mọi selector định vị theo vị trí như `nth-child`; (iii) **đổi nhãn** (đổi
chữ trên nút, placeholder) — làm sai mọi selector neo văn bản như XPath
`text()`. Thực hành tốt (dùng `getByRole`, `data-testid`) giảm được một phần
rủi ro, nhưng không áp dụng được cho các thành phần tùy biến không có nhãn ngữ
nghĩa — icon-button vẽ SVG, widget canvas, hàng danh sách là `div` thuần — nơi
selector cấu trúc gần như là lựa chọn duy nhất. Ba nguyên nhân này chính là ba
loại biến thể giao diện V1/V2/V3 được thiết kế ở Chương 3.

### 2.1.2. Mô hình thị giác–ngôn ngữ và bài toán GUI grounding

**VLM** là mô hình đa phương thức ghép một bộ mã hóa thị giác (vision encoder)
với một mô hình ngôn ngữ lớn, cho phép nhận đầu vào ảnh + văn bản và sinh văn
bản. Với kiểm thử GUI, hai năng lực quan trọng nhất là: **hiểu màn hình** (đọc
screenshot, nhận biết bảng/nút/form và trạng thái của chúng) và **GUI
grounding** — định vị tọa độ của phần tử trên ảnh từ một mô tả ngôn ngữ ("nút
xóa ở hàng đầu tiên"). Grounding là mắt xích quyết định: mọi hành động (click,
điền) đều cần tọa độ đúng.

Một dòng model được huấn luyện chuyên cho GUI đã hình thành: CogAgent, Ferret-UI,
SeeClick, UI-TARS, và họ Qwen-VL. Đồ án dùng **Qwen3-VL** (bản open-weight
235B-A22B); một đặc điểm kỹ thuật đáng lưu ý là họ Qwen-VL trả tọa độ grounding
theo quy ước **chuẩn hóa 0–1000** bất kể chỉ dẫn trong prompt — chi tiết và hệ
quả đo lường được phân tích ở mục 4.7. Trên các model này, một lớp **GUI agent**
đã phát triển (AppAgent, Mobile-Agent, WebVoyager): vòng lặp quan sát màn hình →
suy luận → hành động, nhằm hoàn thành nhiệm vụ mô tả bằng ngôn ngữ tự nhiên.

### 2.1.3. Kiểm thử GUI bằng ngôn ngữ tự nhiên với Midscene.js

Midscene.js là framework mã nguồn mở cho phép viết kịch bản kiểm thử web bằng
ngôn ngữ tự nhiên trên nền Playwright, qua họ API `aiTap`, `aiInput`,
`aiAssert`, `aiNumber`, `aiQuery`... Mỗi lời gọi chụp screenshot hiện thời, gửi
kèm mô tả tới VLM; framework tách hai vai trò **planning** (hiểu ý định, quyết
định hành động) và **grounding** (định vị tọa độ trên ảnh), rồi thực thi hành
động qua Playwright. Cấu hình `MIDSCENE_MODEL_FAMILY` cho phép framework áp
dụng đúng quy ước riêng của từng họ model (định dạng prompt, quy ước tọa độ).
Đồ án chọn Midscene.js vì: hỗ trợ web chính thức, tách lớp model rõ ràng (ghim
được model qua biến môi trường), và có cơ chế tường minh để tắt cache — điều
kiện cần để đo flakiness trung thực.

### 2.1.4. Khía cạnh bảo mật liên quan

Hai mục trong OWASP Top 10 làm nền cho phần mở rộng của đồ án. **Broken Access
Control** — lớp lỗi phổ biến nhất — có một biểu hiện front-end: phần tử giao
diện của vai trò quyền cao (nút xóa, trang quản trị, cột dữ liệu nhạy cảm) hiển
thị nhầm cho vai trò quyền thấp; RQ3 kiểm thử đúng lớp biểu hiện này. **Sensitive
Data Exposure** đặt ra vấn đề đặc thù cho kiểm thử bằng VLM: screenshot gửi lên
API bên thứ ba có thể chứa PII (họ tên, số thẻ, liên hệ) — dữ liệu rời khỏi hạ
tầng nội bộ ngay trong quá trình kiểm thử; RQ4 khảo sát giải pháp che ảnh trước
khi gửi và cái giá phải trả về độ chính xác định vị.

## 2.2. Khảo sát 15 công trình liên quan (2023–2025)

Mười lăm công trình được GVHD chỉ định khảo sát được tổ chức theo ba nhánh, dựa
trên **tín hiệu đầu vào** mà phương pháp sử dụng — đây cũng là trục phân biệt
bản chất giữa hai phương pháp đồ án so sánh.

### 2.2.1. Nhánh khảo sát nền (survey)

**[1] Survey LLM4Testing (IEEE TSE 2024)** phân loại có hệ thống 102 công trình
dùng LLM cho kiểm thử phần mềm theo hai trục (nhiệm vụ kiểm thử × cách dùng
LLM), cho thấy phần lớn dùng prompt engineering thay vì fine-tuning — nhất quán
với lựa chọn "không huấn luyện model" của đồ án. **[15] Survey vision-based GUI
testing (ACM CSUR)** khảo sát 271 bài giai đoạn tiền-LLM, ghi nhận computer
vision dần thay thế/bổ sung cách trích xuất từ source code/layout vì "cái trích
xuất được" khác "cái thực sự hiển thị" — chính là luận điểm gốc của hướng
vision-based, nhưng hoàn thành trước làn sóng VLM đa phương thức nên không phủ
các công cụ như Midscene.

### 2.2.2. Nhánh LLM text-based (đầu vào là DOM/metadata)

Điểm chung của nhánh này: LLM nhận **văn bản** trích từ view hierarchy /
accessibility tree / DOM — cùng "chất liệu" với locator truyền thống, nên kế
thừa cả điểm mạnh (đầy đủ, chính xác) lẫn điểm yếu (không thấy những gì chỉ hiện
ra bằng pixel) của chất liệu đó.

- **[2] GPTDroid (ICSE 2024)** ⭐ — phân tích sâu tại 2.3.
- **[5] QTypist (ICSE 2023)** giải nút thắt text input: prompt "điền vào chỗ
  trống" sinh input hợp ngữ cảnh từ metadata GUI, nâng passing rate lên 87% và
  cải thiện coverage cho các tool sẵn có; chỉ giải quyết khâu input, không đụng
  đến oracle.
- **[6] LLMDroid (FSE 2025)** tối ưu chi phí: tool truyền thống chạy chính, LLM
  chỉ can thiệp khi coverage chững; đáng chú ý là phân tích chi phí theo $/giờ
  (GPT-4o $4,77/giờ; phương án rẻ đạt 78% hiệu năng với $0,18/giờ) — hình mẫu
  trực tiếp cho cách đồ án đo chi phí vận hành.
- **[9] Temac (2025, preprint)** phối hợp đa agent LLM khi coverage bão hòa,
  tăng 12,5–60,3% code coverage trên 6 web app; chi phí nhiều vòng gọi và tính
  tái lập chưa được báo cáo — đúng loại số liệu đồ án bổ sung.
- **[10] NaviQAte (2024, preprint)** điều hướng web theo mô tả chức năng trừu
  tượng: success rate 44,2% (user task) / 38,5% (functionality) — bằng chứng
  định lượng rằng agent tự trị trên web thực tế còn xa mức tin cậy; lưu ý này
  giúp phân biệt "agent tự khám phá" (khó) với "thực thi kịch bản có cấu trúc
  bằng NL" (bài toán của Midscene, dễ hơn đáng kể).
- **[13] ITeM (ISSTA 2025)** migrate test giữa các app bằng cách trích **ý định
  (intention)** của test rồi hiện thực hóa trên app đích — luận điểm lý thuyết
  sát nhất với giả thuyết của đồ án: test mô tả theo ý định bền vững hơn test
  gắn với widget/locator khi giao diện thay đổi.
- **[14] Guardian (ISSTA 2024)** chuyển các phần việc xác định (lọc action hợp
  lệ, khôi phục state) từ LLM sang chương trình symbolic ở runtime — kiến trúc
  "LLM plan + symbolic kiểm soát" tương đồng cách Midscene tách planning/
  grounding, và gợi ý khung phân tích lỗi (planning sai vs grounding sai).

### 2.2.3. Nhánh VLM vision-based (đầu vào là screenshot)

Điểm chung: model "nhìn" pixel, độc lập với DOM — đúng phương pháp đồ án đánh
giá.

- **[3] VETL (ICSME 2024)** ⭐ và **[4] VisionDroid/Trident** ⭐ — phân tích sâu
  tại 2.3.
- **[7] AUITestAgent (2024, preprint)** — công cụ kiểm thử GUI mobile điều khiển
  bằng ngôn ngữ tự nhiên, tách phần tương tác và phần kiểm chứng
  (verification đạt 94% accuracy trên benchmark riêng; đã phát hiện 4 bug thực
  tại Meituan); cách tách interaction/verification rất giống cặp API
  `ai`/`aiAssert` của Midscene mà đồ án sử dụng.
- **[8] GTArena (2024, preprint)** — benchmark thống nhất cho GUI testing agent,
  chia quy trình thành 3 nhiệm vụ con và dùng cả **app bị cấy lỗi nhân tạo**;
  kết quả cho thấy các model mạnh nhất vẫn không đều tay trên cả 3 nhiệm vụ.
  Phương pháp "cấy lỗi có kiểm soát để đo khả năng phát hiện" chính là cách đồ
  án xây build seeded-bugs cho RQ3.
- **[11] AutoE2E (ICSE 2025)** — LLM suy luận feature của web app rồi sinh test
  E2E, đạt feature coverage 79%; gợi ý chiều mở rộng "AI sinh test" (đồ án giữ
  test do người thiết kế để bảo đảm tính đối xứng của so sánh).
- **[12] Nghiên cứu MLLM làm oracle cho non-crash bug (2024, preprint)** — bug
  detection rate 49%, nhưng chính các tác giả chỉ ra ba rủi ro: suy giảm hiệu
  năng, tính ngẫu nhiên nội tại và false positive — đúng ba rủi ro đồ án kiểm
  soát bằng temperature 0, đo flakiness qua 5 lần lặp, và bộ kịch bản đối chứng
  chống báo động giả (R6–R8).

### 2.2.4. Bảng tổng hợp

[BẢNG 2.1 — 15 công trình × {nền tảng; tín hiệu vào (text/vision); nhiệm vụ;
có so sánh đối chứng locator-vs-VLM?; có đo chi phí bảo trì?; có xét bảo mật?}.
Ba cột cuối gần như trống toàn bộ ở 15 hàng — trực quan hóa ba khoảng trống;
hàng cuối "Đồ án này" đánh dấu đủ ba cột. Dựng bảng khi ghép vào template.]

## 2.3. Phân tích sâu bốn công trình đại diện

**[1] Software Testing with LLMs: Survey, Landscape, and Vision (TSE 2024).**
Khảo sát 102 công trình, lập bản đồ theo vòng đời kiểm thử và theo cách dùng
LLM. Ba điểm rút ra cho đồ án: (i) taxonomy của khảo sát được dùng làm khung
định vị — đồ án nằm ở giao của "GUI testing" và "LLM as evaluator/executor";
(ii) khảo sát xác nhận đa số công trình dùng model qua prompt, không fine-tune —
trùng thiết kế đồ án; (iii) các thách thức mở mà khảo sát nêu (test oracle, chi
phí) chính là hai trục đo của đồ án. Giới hạn: dữ liệu đến đầu 2024, chưa phủ
làn sóng VLM/GUI-agent — khoảng thời gian mà 14 bài còn lại lấp vào.

**[2] GPTDroid (ICSE 2024).** Đặt kiểm thử GUI mobile thành bài toán hỏi–đáp:
trích thông tin trang GUI từ view hierarchy thành văn bản, LLM sinh hành động,
thực thi rồi phản hồi ngược — kèm bộ nhớ dài hạn theo chức năng
(functionality-aware memory). Kết quả nổi bật (**32%** hơn baseline tốt nhất về
activity coverage, **31%** nhiều bug hơn, 35 bug mới được xác nhận trên Google
Play) chứng minh giá trị của việc LLM "hiểu ngữ nghĩa chức năng". Nhưng toàn bộ
pipeline là **text-based**: không nhìn pixel, phụ thuộc chất lượng accessibility
tree — nghĩa là cùng họ hạn chế với locator truyền thống. Trong khung của đồ án,
GPTDroid đại diện cho "cận trên" của nhánh text-based, làm điểm đối chiếu khái
niệm với nhánh vision-based.

**[3] VETL (ICSME 2024).** Công trình web GUI testing đầu tiên dẫn hướng bởi
LVLM: sinh text input từ hiểu cảnh (scene understanding) trên screenshot; chọn
phần tử bằng visual question-answering thay vì trích thuộc tính DOM chính xác;
điều phối khám phá bằng multi-armed bandit. Kết quả: hơn **25%** unique web
action so với WebExplor, tìm được bug thật được maintainer xác nhận. VETL là
công trình gần đồ án nhất (VLM + web) và cung cấp luận cứ rằng lựa chọn phần tử
bằng thị giác tránh phụ thuộc DOM. Điều VETL **không** trả lời — và đồ án trả
lời — là: so với một baseline locator trên cùng bộ kịch bản, độ bền vững hơn bao
nhiêu, chi phí gọi model và độ ổn định giữa các lần chạy ra sao (paper không báo
cáo hai số liệu sau).

**[4] VisionDroid/Trident (preprint 2024).** Nhắm lớp **non-crash functional
bug** — hành vi sai chỉ nhận ra được bằng mắt: pipeline vision-driven trên
GPT-4V gồm explorer định hướng chức năng và bug detector suy luận trên các đoạn
lịch sử khám phá (bản v2 tái cấu trúc thành 3 agent Explorer–Monitor–Detector).
Kết quả trên benchmark 590 bug: recall tăng **14–112%**, precision tăng
**108–147%** so với baseline tốt nhất; 43 bug mới trên Google Play. Đây là minh
chứng mạnh nhất cho năng lực "nhìn để phát hiện sai lệch UI" — nền tảng cho
thiết kế oracle thị giác của RQ3. Đồng thời, hạn chế của nó (precision v1 chỉ
50–76%, tức false positive đáng kể; phụ thuộc MLLM thương mại) giải thích vì
sao đồ án đưa cả kịch bản đối chứng R6–R8 và build sạch vào thiết kế RQ3 — và
kết quả 0 báo động giả của đồ án (trên ứng dụng đơn giản hơn nhiều) cần được
diễn giải trong tương quan đó.

## 2.4. Định vị đóng góp của đồ án

Bức tranh khảo sát cho thấy hai nhánh phương pháp đã trưởng thành về **năng
lực** (coverage, phát hiện bug) nhưng còn trống về **bằng chứng so sánh đối
chứng**: chưa ai đặt locator-based và VLM-based cạnh nhau trên cùng một bộ test,
cùng một ứng dụng, với thay đổi giao diện được kiểm soát chủ động, và đo đồng
thời robustness — chi phí bảo trì — chi phí vận hành. Đồ án không đề xuất công
cụ hay model mới; đóng góp của nó là **bằng chứng thực nghiệm** lấp đúng ba
khoảng trống: (1) so sánh cặp có kiểm soát trên 4 biến thể giao diện; (2) định
lượng chi phí bảo trì theo giao thức chuẩn hóa, tái lập được; (3) hai khảo sát
bảo mật đầu tiên trong ngữ cảnh này — masking PII trước khi gửi VLM API (RQ4) và
dùng VLM kiểm thử phân quyền hiển thị (RQ3). Phương pháp đạt các mục tiêu đó
được trình bày ở chương tiếp theo.
