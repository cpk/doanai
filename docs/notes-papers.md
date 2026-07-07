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


### 9. Temac: Multi-Agent Collaboration for Automated Web GUI Testing
- **Nguồn**: Chenxu Liu (Peking University; đồng tác giả Tao Xie) — arXiv: 2506.00520, 2025 (preprint).
- **Problem**: Kiểm thử GUI web tự động khó sinh chuỗi hành động liên tục, có ý nghĩa để khám phá sâu các chức năng phức tạp; LLM đơn lẻ kém hiệu quả và tỷ lệ thực thi GUI task thành công thấp.
- **Method**: Chiến lược lai hai pha: chạy công cụ kiểm thử truyền thống để khám phá rộng; khi coverage chững lại, các LLM-based agent cộng tác tổng hợp thông tin thành knowledge base, suy luận các chức năng chưa được phủ và điều khiển hành động có mục tiêu tới các state chưa khám phá.
- **Result**: Cải thiện code coverage trung bình 12,5%–60,3% so với các baseline SOTA trên 6 web app mã nguồn mở; phát hiện 445 unique failure trên 20 web app thực tế.
- **Limitation**: Preprint chưa qua peer review; chi phí LLM nhiều vòng gọi và tính tái lập chưa được báo cáo chi tiết.
- **Liên quan đồ án**: Minh họa hướng "LLM bổ trợ công cụ truyền thống" — đúng trục so sánh locator-based vs AI-driven, gợi ý dùng coverage/failure làm metric đối chứng bên cạnh robustness và chi phí API.

### 10. NaviQAte: Functionality-guided Web Application Navigation
- **Nguồn**: Mobina Shahbandeh et al. (nhóm Mesbah, UBC) — arXiv: 2409.10741, 2024 (preprint).
- **Problem**: Các approach điều hướng web hiện có (như WebCanvas) đòi hỏi mô tả task rất chi tiết, kém thích ứng với môi trường web động khi chỉ có mô tả chức năng ở mức trừu tượng.
- **Method**: Tái công thức hóa web exploration thành bài toán Q&A để sinh chuỗi hành động không cần tham số chi tiết; chiến lược 3 pha dùng GPT-4o cho quyết định phức tạp và GPT-4o mini cho task đơn giản, kết hợp đầu vào đa phương thức (text + ảnh).
- **Result**: Success rate 44,23% cho user task navigation và 38,46% cho functionality navigation, cải thiện 15% và 33% so với WebCanvas.
- **Limitation**: Success rate tuyệt đối vẫn dưới 50%, cho thấy điều hướng theo chức năng trên web thực tế còn rất khó.
- **Liên quan đồ án**: Bằng chứng định lượng về mức trần độ tin cậy của tác tử VLM/LLM khi điều hướng web bằng ngôn ngữ tự nhiên — cần lưu ý khi đánh giá Midscene.js so với Playwright script cố định.

### 11. Feature-Driven End-to-End Test Generation (AutoE2E)
- **Nguồn**: Parsa Alian et al. (UBC) — ICSE 2025 (Research Track). DOI: 10.1109/ICSE55347.2025.00141. arXiv: 2408.01894.
- **Problem**: Viết test E2E cho web app thủ công tốn công, còn kỹ thuật sinh test tự động hiện có tạo test rời rạc, thiếu ngữ nghĩa theo tính năng.
- **Method**: AutoE2E dùng LLM suy luận các feature tiềm năng của web app rồi dịch thành test scenario thực thi được; đề xuất benchmark E2EBench đo feature coverage của test suite E2E.
- **Result**: Feature coverage trung bình 79%, vượt baseline tốt nhất 558% (tương đối).
- **Limitation**: Giới hạn ở web app; feature coverage 79% cho thấy vẫn bỏ sót ~1/5 tính năng.
- **Liên quan đồ án**: Gợi ý chiều mở rộng "AI sinh test theo tính năng" và khái niệm feature coverage — có thể dùng làm metric phụ khi so sánh chất lượng test Playwright vs Midscene.js.

### 12. A Study of Using Multimodal LLMs for Non-Crash Functional Bug Detection in Android Apps
- **Nguồn**: Bangyan Ju et al. — arXiv: 2407.19053, 2024 (preprint).
- **Problem**: Kiểm thử GUI truyền thống đạt code coverage tốt nhưng thiếu test oracle hiệu quả để phát hiện non-crash functional bug.
- **Method**: Nghiên cứu thực nghiệm dùng multimodal LLM làm test oracle (tận dụng domain knowledge từ corpus huấn luyện), đánh giá trên 71 non-crash functional bug đã ghi nhận.
- **Result**: Bug detection rate 49%, vượt các công cụ hiện có; phát hiện thêm 24 bug chưa từng biết trên 64 app Android, 4 bug được developer xác nhận/sửa.
- **Limitation**: Chính tác giả chỉ ra performance degradation, randomness nội tại và false positive làm giảm độ tin cậy của LLM-as-oracle.
- **Liên quan đồ án**: Non-determinism và false positive của oracle dựa trên VLM là đúng rủi ro đồ án phải đo khi dùng aiAssert của Midscene.js thay cho assertion cứng của Playwright.

### 13. Intention-based GUI Test Migration for Mobile Apps using Large Language Models (ITeM)
- **Nguồn**: Shaoheng Cao et al. (Nanjing University) — Proc. ACM Softw. Eng. (PACMSE), **ISSTA 2025** (lưu ý: danh sách GVHD ghi FSE, đã xác minh lại là ISSTA 2025). DOI: 10.1145/3728978.
- **Problem**: Các approach migrate GUI test giữa các app coi đây là bài toán widget-matching nên thất bại khi interaction logic của cùng chức năng khác nhau giữa các app.
- **Method**: Framework 2 giai đoạn dựa trên LLM: (1) cơ chế transition-aware sinh test intention từ test nguồn; (2) cơ chế dynamic reasoning hiện thực hóa intention trên app đích.
- **Result**: Trên 35 app Android với 280 test migration task, vượt các approach SOTA về cả effectiveness lẫn efficiency (số liệu chi tiết trong bản full).
- **Limitation**: Giới hạn ở app Android, phụ thuộc chất lượng suy luận intention của LLM.
- **Liên quan đồ án**: Ý tưởng "test theo intention thay vì theo widget/locator" chính là luận điểm lý thuyết cho giả thuyết Midscene.js (mô tả ngôn ngữ tự nhiên) bền vững hơn Playwright locator trước biến thể giao diện — bài sát nhất với khái niệm chi phí bảo trì (RQ2).

### 14. Guardian: A Runtime Framework for LLM-based UI Exploration
- **Nguồn**: Dezhi Ran et al. (PKU/UTD) — ISSTA 2024. DOI: 10.1145/3650212.3680334.
- **Problem**: LLM kém trong tuân thủ chặt instruction và re-planning khi khám phá UI theo mục tiêu, làm giảm hiệu quả dù prompt tinh vi.
- **Method**: Computation offloading: chuyển các phần việc xác định (lọc action không hợp lệ, thu hẹp action space, khôi phục UI state) từ LLM sang chương trình symbolic ở runtime, buộc LLM chỉ plan trên action space đã kiểm soát.
- **Result**: Với ChatGPT trên benchmark FestiVal (58 task, 23 app): success rate 48,3% và average completion proportion 64,0%, cải thiện tương đối 154% và 132% so với SOTA.
- **Limitation**: Success rate tuyệt đối vẫn <50%; đánh giá gắn với một LLM trên app Android.
- **Liên quan đồ án**: Kiến trúc "LLM plan + symbolic program kiểm soát runtime" tương đồng cách Midscene.js tách planning/grounding; gợi ý phân tích lỗi của VLM-agent theo nguyên nhân (planning sai vs grounding sai) khi đo robustness.

### 15. Vision-Based Mobile App GUI Testing: A Survey
- **Nguồn**: Shengcheng Yu et al. (Nanjing University/ETH) — arXiv: 2310.13518 (10/2023); được nhận đăng tại ACM Computing Surveys, DOI: 10.1145/3773027.
- **Problem**: Kiểm thử GUI truyền thống dựa trên source code/layout file gặp khoảng cách giữa "cái trích xuất được" và "cái GUI thực sự hiển thị".
- **Method**: Khảo sát hệ thống 271 bài báo (92 bài thuần vision-based) về GUI test generation, record & replay, testing framework..., phân tích cách computer vision thay thế/bổ sung giải pháp truyền thống.
- **Result**: Bản đồ tài liệu trước làn sóng LLM, cho thấy vision-based approach dần chiếm vị trí quan trọng và chỉ ra các khoảng trống nghiên cứu.
- **Limitation**: Hoàn thành trước khi VLM đa phương thức bùng nổ (2023), không phủ các GUI-agent hiện đại như UI-TARS hay Midscene.
- **Liên quan đồ án**: Nền "related work" giai đoạn pre-LLM để lập luận vì sao vision-based tiến hóa thành VLM-based và vì sao cần so sánh định lượng mới trên web.
