# Tài liệu tham khảo (BẢN NHÁP — định dạng lại theo quy định khoa khi nộp)

> Thứ tự [1]–[15] khớp `docs/notes-papers.md` và các trích dẫn trong Chương 2/4.
> Nguồn đã xác minh qua arXiv/ACM DL/IEEE (07/2026); kiểm tra lại DOI khi nộp.

[1] J. Wang et al., "Software Testing with Large Language Models: Survey,
Landscape, and Vision," IEEE Transactions on Software Engineering, vol. 50,
no. 4, pp. 911–936, 2024. DOI: 10.1109/TSE.2024.3368208.

[2] Z. Liu et al., "Make LLM a Testing Expert: Bringing Human-like Interaction
to Mobile GUI Testing via Functionality-aware Decisions (GPTDroid)," in Proc.
ICSE 2024. DOI: 10.1145/3597503.3639180.

[3] S. Wang, S. Wang, Y. Fan, X. Li, Y. Liu, "Leveraging Large Vision-Language
Model for Better Automatic Web GUI Testing (VETL)," in Proc. ICSME 2024.
arXiv: 2410.12157.

[4] Z. Liu et al., "Vision-driven Automated Mobile GUI Testing via Multimodal
Large Language Model (VisionDroid)," arXiv: 2407.03037, 2024 (bản v2: "Seeing
is Believing...", công cụ đổi tên Trident; preprint tại thời điểm tra cứu).

[5] Z. Liu et al., "Fill in the Blank: Context-aware Automated Text Input
Generation for Mobile GUI Testing (QTypist)," in Proc. ICSE 2023,
pp. 1355–1367. DOI: 10.1109/ICSE48619.2023.00119.

[6] C. Wang, T. Liu, Y. Zhao, M. Yang, H. Wang, "LLMDroid: Enhancing Automated
Mobile App GUI Testing Coverage with Large Language Model Guidance," Proc. ACM
Softw. Eng. (FSE 2025). DOI: 10.1145/3715763.

[7] Y. Hu et al., "AUITestAgent: Automatic Requirements Oriented GUI Function
Testing," arXiv: 2407.09018, 2024 (preprint).

[8] K. Zhao et al., "GUI Testing Arena: A Unified Benchmark for Advancing
Autonomous GUI Testing Agent (GTArena)," arXiv: 2412.18426, 2024 (preprint).

[9] C. Liu et al., "Temac: Multi-Agent Collaboration for Automated Web GUI
Testing," arXiv: 2506.00520, 2025 (preprint).

[10] M. Shahbandeh et al., "NaviQAte: Functionality-guided Web Application
Navigation," arXiv: 2409.10741, 2024 (preprint).

[11] P. Alian et al., "Feature-Driven End-to-End Test Generation (AutoE2E),"
in Proc. ICSE 2025. DOI: 10.1109/ICSE55347.2025.00141.

[12] B. Ju et al., "A Study of Using Multimodal LLMs for Non-Crash Functional
Bug Detection in Android Apps," arXiv: 2407.19053, 2024 (preprint).

[13] S. Cao et al., "Intention-based GUI Test Migration for Mobile Apps using
Large Language Models (ITeM)," Proc. ACM Softw. Eng. (ISSTA 2025).
DOI: 10.1145/3728978.

[14] D. Ran et al., "Guardian: A Runtime Framework for LLM-based UI
Exploration," in Proc. ISSTA 2024. DOI: 10.1145/3650212.3680334.

[15] S. Yu et al., "Vision-Based Mobile App GUI Testing: A Survey," ACM
Computing Surveys. DOI: 10.1145/3773027. arXiv: 2310.13518.

## Công cụ, mô hình và tiêu chuẩn

[16] Playwright — tài liệu chính thức. https://playwright.dev (phiên bản dùng
trong thực nghiệm: 1.61).

[17] Midscene.js — tài liệu chính thức (Model Strategy; Configure Your Model).
https://midscenejs.com (phiên bản: 1.10.3).

[18] Qwen Team, Alibaba, "Qwen3-VL" — model card bản open-weight
`qwen3-vl-235b-a22b-instruct` (truy cập qua OpenRouter; giá tra 08/07/2026:
$0.20/1M token vào, $0.88/1M token ra).

[19] OWASP Foundation, "OWASP Top 10" — Broken Access Control; Sensitive Data
Exposure. https://owasp.org/Top10/

[20] Mã nguồn và dữ liệu của đồ án: https://github.com/cpk/doanai (chuyển
public khi bảo vệ; tag `app-v1.0`, các nhánh bằng chứng `rq2-*`,
`rq3-seeded-bugs`).

> Ghi chú khi hoàn thiện: các bài AppAgent, Mobile-Agent, CogAgent, Ferret-UI,
> SeeClick, WebVoyager, UI-TARS được nhắc mức khái quát ở mục 2.1.2 — nếu quy
> định khoa yêu cầu trích dẫn đầy đủ mọi tên riêng, bổ sung mục cho từng bài
> (đều có trên arXiv).
