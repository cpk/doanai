# Ghi chú 15 bài báo SOTA (theo Step 2 hướng dẫn GVHD)

> Mẫu ghi chú: Problem → Method → Result → Limitation (+ Liên quan đồ án).
> ⭐ = 4 bài GVHD yêu cầu đọc kỹ Method + Evaluation. Cập nhật thêm nhận xét cá nhân khi đọc full-text.
> Nguồn đã được xác minh qua arXiv/ACM DL/IEEE (07/2026). Ghi chú sinh với sự hỗ trợ AI — khi đọc kỹ từng bài, đối chiếu lại số liệu trước khi trích vào báo cáo.

### ⭐ 1. Software Testing with Large Language Models: Survey, Landscape, and Vision
- **Nguồn**: Junjie Wang et al. — IEEE Transactions on Software Engineering (TSE), vol. 50, no. 4, pp. 911–936, 2024. DOI: 10.1109/TSE.2024.3368208. arXiv: 2307.07221.
- **Problem**: Thiếu một bức tranh tổng thể, có hệ thống về cách LLM đang được dùng trong software testing.
- **Method**: Survey có hệ thống trên 102 công trình dùng LLM cho testing, phân tích theo hai trục: (1) góc nhìn testing task (mapping theo vòng đời kiểm thử: unit test generation, test oracle, GUI testing, program repair...) và (2) góc nhìn LLM (model nào, prompt engineering, cách kết hợp với kỹ thuật truyền thống như mutation testing, differential testing). Từ đó tổng hợp landscape và đề xuất roadmap các hướng nghiên cứu mở.
- **Result**: 102 papers được phân loại; hai task được nghiên cứu nhiều nhất là test case preparation và program repair; phần lớn công trình dùng prompt engineering (zero/few-shot) thay vì fine-tuning; paper duy trì repo GitHub (LLM-Testing/LLM4SoftwareTesting) cập nhật liên tục.
- **Limitation**: Chỉ bao phủ công trình đến ~đầu 2024, chưa phản ánh làn sóng VLM/GUI agent mới và không có đánh giá thực nghiệm định lượng nào của riêng nhóm tác giả.
- **Liên quan đồ án**: Dùng làm khung taxonomy cho chương Related Work, định vị hướng "VLM-based GUI testing" (Midscene.js) trong bức tranh chung LLM4Testing và trích các challenge (oracle, cost) mà đồ án đo lường định lượng.

### ⭐ 2. Make LLM a Testing Expert: Bringing Human-like Interaction to Mobile GUI Testing via Functionality-aware Decisions (GPTDroid)
- **Nguồn**: Zhe Liu et al. — ICSE 2024. DOI: 10.1145/3597503.3639180. arXiv: 2310.15780.
- **Problem**: Automated GUI testing truyền thống (random/rule-based/learning-based) đạt coverage thấp vì không hiểu ngữ nghĩa chức năng của app như tester con người.
- **Method**: Formulate mobile GUI testing thành bài toán Q&A — LLM "chat" với app: pipeline trích thông tin GUI page (từ view hierarchy, dạng text) và trạng thái app đưa vào prompt, LLM sinh action/script kiểm thử, thực thi trên thiết bị rồi feedback kết quả ngược lại LLM theo vòng lặp. Điểm nhấn là functionality-aware memory prompting: lưu trí nhớ dài hạn về các chức năng đã khám phá để LLM suy luận theo chức năng (function-oriented) thay vì chỉ theo từng màn hình.
- **Result**: Đánh giá trên 93 app từ Google Play: vượt baseline tốt nhất 32% về activity coverage, phát hiện nhiều hơn 31% bug với tốc độ nhanh hơn; phát hiện 53 bug mới trên Google Play, trong đó 35 bug được nhà phát triển xác nhận/sửa.
- **Limitation**: Hoàn toàn text-based (dựa view hierarchy/metadata), không "nhìn" pixel nên bỏ sót thông tin thị giác và phụ thuộc chất lượng accessibility tree.
- **Liên quan đồ án**: Là đại diện tiêu biểu của nhánh LLM text-based (tương tự triết lý locator/DOM-based), làm điểm đối chiếu khái niệm với nhánh VLM vision-based mà đồ án so sánh qua cặp Playwright vs Midscene.js.

### ⭐ 3. Leveraging Large Vision-Language Model For Better Automatic Web GUI Testing (VETL)
- **Nguồn**: Siyi Wang, Sinan Wang, Yujia Fan, Xiaolei Li, Yepang Liu — ICSME 2024 (Research Track). arXiv: 2410.12157.
- **Problem**: Web GUI testing tự động gặp khó ở hai điểm: sinh text input có nghĩa theo ngữ cảnh và chọn đúng GUI element trong trang web phức tạp, động.
- **Method**: VETL là kỹ thuật web GUI testing đầu tiên dẫn hướng bởi LVLM, gồm 3 thành phần: (1) sinh text input dựa trên scene understanding của LVLM từ screenshot, không cần trích xuất chính xác thuộc tính text trong DOM; (2) chọn element được formulate thành visual question-answering — LVLM bắt liên kết logic giữa input box và element liên quan qua chỉ dẫn thị giác; (3) exploration được điều phối bởi module multi-armed bandit với chiến lược curiosity-oriented để cân bằng explore/exploit không gian state/action.
- **Result**: Trên các benchmark website, VETL khám phá nhiều hơn 25% unique web actions so với WebExplor (SOTA lúc đó); áp dụng lên website thương mại thực tế, phát hiện các functional bug được maintainer xác nhận.
- **Limitation**: Quy mô đánh giá còn hạn chế và paper không báo cáo chi tiết chi phí gọi LVLM hay độ ổn định giữa các lần chạy.
- **Liên quan đồ án**: Là công trình gần đồ án nhất (VLM cho web GUI testing), cung cấp luận cứ rằng vision-based selection tránh phụ thuộc DOM — đúng giả thuyết robustness mà đồ án kiểm chứng định lượng với Midscene.js trước các biến thể giao diện.

### ⭐ 4. Vision-driven Automated Mobile GUI Testing via Multimodal Large Language Model (VisionDroid / Trident)
- **Nguồn**: Zhe Liu et al. — arXiv: 2407.03037 (v1, 07/2024). Lưu ý: bản v2 (12/2024) đổi tên thành "Seeing is Believing: Vision-driven Non-crash Functional Bug Detection for Mobile Apps", tool đổi tên VisionDroid → Trident; tại thời điểm tra cứu vẫn là preprint.
- **Problem**: GUI testing truyền thống chỉ bắt được crash bug có tín hiệu bất thường rõ ràng, bỏ lọt non-crash functional bug (hành vi sai, hiển thị lệch) vốn chỉ nhận ra được qua tín hiệu thị giác và logic chuyển trang.
- **Method**: Pipeline vision-driven dùng MLLM (GPT-4V): (1) trích GUI text và align với screenshot thành vision prompt để MLLM hiểu ngữ cảnh GUI; (2) function-aware explorer dùng MLLM khám phá app theo hướng chức năng, sâu hơn thay vì ngẫu nhiên; (3) logic-aware bug detector cắt lịch sử exploration thành các đoạn logic liền mạch rồi prompt MLLM làm test oracle phát hiện bug. Bản v2 (Trident) tái cấu trúc thành 3 agent phối hợp: Explorer, Monitor, Detector.
- **Result**: (Số liệu v2) Trên benchmark 590 non-crash bug, so với 12 baseline: tăng 14%–112% recall và 108%–147% precision so với baseline tốt nhất; phát hiện 43 bug mới trên Google Play, 31 bug đã được sửa (v1: 29 bug mới, 19 confirmed/fixed).
- **Limitation**: Phụ thuộc MLLM thương mại (chi phí, độ trễ, non-determinism) và oracle dựa trên suy luận của model nên vẫn có false positive đáng kể (precision v1 chỉ 50–76%).
- **Liên quan đồ án**: Minh chứng mạnh nhất cho năng lực "nhìn để phát hiện sai lệch UI" của VLM — trực tiếp hỗ trợ phần đo robustness của Midscene.js trước biến thể giao diện và gợi ý thiết kế oracle cho kiểm thử phân quyền UI.

### 5. Fill in the Blank: Context-aware Automated Text Input Generation for Mobile GUI Testing (QTypist)
- **Nguồn**: Zhe Liu et al. — ICSE 2023, pp. 1355–1367. DOI: 10.1109/ICSE48619.2023.00119. arXiv: 2212.04732.
- **Problem**: Nhiều màn hình app yêu cầu text input hợp lệ mới đi tiếp được, là nút thắt lớn của coverage trong automated GUI testing.
- **Method**: QTypist dùng LLM theo kiểu prompt "fill in the blank": trích ngữ cảnh GUI (tên trường, trang, app) thành prompt để LLM sinh text input có ngữ nghĩa phù hợp, tích hợp được vào các tool testing tự động sẵn có.
- **Result**: Trên 106 app từ Google Play, passing rate đạt 87%, cao hơn 93% so với baseline tốt nhất; khi tích hợp vào các tool testing tự động, giúp tăng đáng kể page/activity coverage.
- **Limitation**: Chỉ giải quyết khâu text input (không quyết định action/oracle) và dựa trên metadata text của GUI thay vì thị giác.
- **Liên quan đồ án**: Gợi ý cách xử lý các form input trong test script của cả hai pipeline (Playwright và Midscene.js), và liên quan trực tiếp đến phần mở rộng masking dữ liệu nhạy cảm khi sinh input tự động.

### 6. LLMDroid: Enhancing Automated Mobile App GUI Testing Coverage with Large Language Model Guidance
- **Nguồn**: Chenxu Wang, Tianming Liu, Yanjie Zhao, Minghui Yang, Haoyu Wang — Proc. ACM Softw. Eng. (PACMSE), FSE 2025. DOI: 10.1145/3715763.
- **Problem**: Gọi LLM cho từng bước testing quá đắt và chậm, trong khi các tool testing truyền thống bị chững coverage ở các chức năng khó chạm tới.
- **Method**: Framework 2 giai đoạn: Autonomous Exploration (tool testing sẵn có tự chạy, LLM chỉ tóm tắt các page đã khám phá) và chuyển sang LLM Guidance khi tăng trưởng coverage chậm lại để LLM dẫn hướng tới chức năng chưa khám phá — tối thiểu số lần gọi LLM.
- **Result**: Áp lên 3 tool Android testing open-source, đánh giá trên 14 app top Google Play: tăng trung bình 26.16% code coverage và 29.31% activity coverage; phân tích chi phí: hiệu năng tối ưu với GPT-4o ở $4.77/giờ, phương án rẻ đạt 78% hiệu năng với chỉ $0.18/giờ.
- **Limitation**: Chỉ nhắm mục tiêu coverage (không giải quyết test oracle/verification) và đánh giá giới hạn ở 14 app Android.
- **Liên quan đồ án**: Là hình mẫu trực tiếp cho phương pháp đo chi phí API theo $/giờ và trade-off chi phí–hiệu quả giữa các model, áp dụng được cho phần so sánh chi phí Playwright (0 API) vs Midscene.js.

### 7. AUITestAgent: Automatic Requirements Oriented GUI Function Testing
- **Nguồn**: Yongxiang Hu et al. (Fudan University + Meituan) — arXiv: 2407.09018, 07/2024 (preprint; code: github.com/bz-lab/AUITestAgent).
- **Problem**: Kiểm thử chức năng GUI theo yêu cầu (requirements-oriented) vẫn phải viết/duy trì script thủ công, thiếu tool tự động hóa trọn vẹn cả tương tác lẫn verification từ yêu cầu bằng ngôn ngữ tự nhiên.
- **Method**: Tool GUI testing điều khiển bằng natural language đầu tiên cho mobile app: tách test requirement thành phần interaction (thực thi bởi các agent được tổ chức động) và phần verification (chiến lược multi-dimensional data extraction từ interaction trace để đối chiếu với yêu cầu).
- **Result**: Trên benchmark tự xây, chất lượng sinh interaction vượt các tool hiện có và đạt 94% accuracy ở khâu verification; triển khai thực tế tại Meituan phát hiện 4 functional bug mới qua 10 lần regression test trong 2 tháng.
- **Limitation**: Benchmark do nhóm tự thiết kế quanh nghiệp vụ Meituan nên khả năng tổng quát hóa sang app/web khác chưa được kiểm chứng.
- **Liên quan đồ án**: Cách viết test bằng ngôn ngữ tự nhiên rồi tách interaction/verification rất giống API của Midscene.js (ai/aiAssert), cung cấp mẫu thiết kế test case và metric verification accuracy cho đồ án.

### 8. GUI Testing Arena: A Unified Benchmark for Advancing Autonomous GUI Testing Agent (GTArena)
- **Nguồn**: Kangjia Zhao et al. (Zhejiang University, Om AI Research) — arXiv: 2412.18426, 12/2024 (preprint; code: github.com/ZJU-ACES-ISE/ChatUITest).
- **Problem**: Chưa có môi trường chuẩn hóa, công bằng để đánh giá trọn vẹn năng lực của các MLLM/agent trong automated GUI testing (khác với GUI task automation thông thường).
- **Method**: GTArena chia quy trình testing thành 3 subtask — test intention generation, test task execution, GUI defect detection — và xây benchmark dataset gồm 3 loại dữ liệu: app di động thực, app bị inject defect nhân tạo, và dữ liệu synthetic, để đánh giá thống nhất nhiều MLLM.
- **Result**: Kết quả thực nghiệm cho thấy ngay cả các model tiên tiến nhất cũng không làm tốt đồng đều cả 3 subtask, chỉ ra khoảng cách lớn giữa năng lực hiện tại và yêu cầu thực tế.
- **Limitation**: Tập trung vào mobile app; chưa bao phủ web GUI và các yếu tố chi phí/độ ổn định khi chạy lặp lại.
- **Liên quan đồ án**: Ý tưởng inject defect/biến thể có kiểm soát vào app để đo năng lực phát hiện của VLM chính là phương pháp luận đồ án dùng khi tạo các biến thể giao diện web để đo robustness của Playwright vs Midscene.js.
