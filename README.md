# VLM for GUI Testing Automation — Đồ án tốt nghiệp

So sánh thực nghiệm định lượng giữa kiểm thử GUI **locator-based** (Playwright) và **VLM-based** (Midscene.js) trên cùng một ứng dụng web với các biến thể giao diện có kiểm soát. Đo 3 trục: độ bền vững (robustness), chi phí bảo trì (maintenance cost), chi phí vận hành (thời gian/token). Mở rộng: masking dữ liệu nhạy cảm trên screenshot (RQ4) và kiểm thử phân quyền hiển thị UI (RQ3).

## Cấu trúc

| Thư mục | Nội dung |
|---------|----------|
| `docs/` | Đề cương, hướng dẫn GVHD, ghi chú 15 bài báo, báo cáo |
| `app/` | Ứng dụng web thực nghiệm (React + Vite) + biến thể giao diện V0–V3 |
| `tests-locator/` | Bộ test baseline Playwright (locator-based) |
| `tests-vlm/` | Bộ test Midscene.js (ngôn ngữ tự nhiên) + pilot |
| `masking/` | Tiền xử lý ảnh che PII + grounding benchmark (RQ4) |
| `harness/` | Runner ma trận thực nghiệm, thu thập CSV |
| `results/` | Số liệu, biểu đồ |

## Chạy nhanh

```bash
# App thực nghiệm
cd app && npm install && npm run dev   # http://localhost:5173

# Pilot VLM (cần .env — xem tests-vlm/.env.example)
cd tests-vlm && npm install && npm run pilot
```

Kế hoạch chi tiết: `KeHoach_DoAn.md`. Yêu cầu: Node.js >= 18 (khuyến nghị 20 LTS).
