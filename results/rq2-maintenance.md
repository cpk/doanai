# RQ2 — Chi phí bảo trì test khi giao diện thay đổi

> Ngày đo: 09/07/2026. Quy trình chuẩn hóa tự động theo đề cương (bản cập nhật
> 09/07/2026): AI coding agent sửa tối thiểu, đo số test phải sửa + diff LOC +
> thời gian phục hồi; thời gian sẽ đo bổ sung trên branch riêng (xem mục 4).

## 1. Thiết lập

- Điểm xuất phát: bộ test locator (Playwright, 18 test) và bộ test VLM (Midscene.js, 18 test)
  cùng xanh 100% trên giao diện gốc V0.
- Khi "nâng cấp giao diện" lên từng biến thể V1/V2/V3 (chỉ đổi trình bày, không đổi logic —
  `app/src/variants.ts`), đo trên mỗi bộ test:
  1. **Số test hỏng** (từ ma trận RQ1, label `gd4-main`, deterministic qua 5 lần lặp);
  2. **Số test phải sửa + diff LOC** để bộ test xanh lại 18/18 trên biến thể đó;
  3. Thời gian sửa (chưa đo — mục 4).
- Quy tắc sửa tối thiểu: **chỉ đổi selector/assertion**, không refactor, không đổi cấu trúc
  test, không thêm helper. Mỗi biến thể sửa trên branch riêng từ `master`:
  - `rq2-fix-v2` (commit `bc5f071`) — xác nhận `APP_VARIANT=v2` → 18/18 pass.
  - `rq2-fix-v3` (commit `3eb8809`) — xác nhận `APP_VARIANT=v3` → 18/18 pass.
- Diff LOC lấy từ `git diff --stat master..<branch>` (chỉ tính file test).

## 2. Kết quả

| Biến thể | Thay đổi giao diện | Bộ test | Test hỏng | Test phải sửa | Diff LOC (+/−) | File phải sửa |
|---|---|---|---:|---:|---:|---:|
| V1 | Dark theme (đổi màu) | Locator | 0/18 | 0 | 0 | 0 |
| V1 | | VLM | 0/18 | 0 | 0 | 0 |
| V2 | Topbar + đảo cột/toolbar/icon | Locator | **9/18** | **9** | **24 (12+/12−)** | 4 |
| V2 | | VLM | 0/18 | 0 | 0 | 0 |
| V3 | Đổi icon + nhãn nút/placeholder | Locator | **6/18** | **6** | **22 (11+/11−)** | 3 |
| V3 | | VLM | 0/18 | 0 | 0 | 0 |
| **Tổng V1–V3** | | **Locator** | **15** | **15** | **46 (23+/23−)** | — |
| **Tổng V1–V3** | | **VLM** | **0** | **0** | **0** | — |

Ghi chú cách đếm: "Diff LOC" = tổng dòng thêm + dòng xóa theo `git diff`; vì mọi sửa đổi là
thay-thế-tại-chỗ một dòng nên 12+/12− tương ứng 12 dòng bị sửa (V2), 11 dòng (V3).

### Chi tiết V2 (9 test sửa — gãy do đảo vị trí cấu trúc)

Nguyên nhân: V2 đảo thứ tự cột (`actions` lên cột 1, `name` → cột 2, `sku` → cột 4,
`stock` → cột 5, `rating` → cột 8) và đảo thứ tự icon hành động (edit→view→delete).
Mọi selector `td:nth-child(n)` / `.icon-btn:nth-child(n)` trỏ sai ô.

| Test | Sửa |
|---|---|
| A3 | cột name 1→2 trong assertion |
| B1 | cột name 1→2 trong assertion |
| C1 | cột sku 2→4 |
| C2 | ô actions 8→1, icon edit 2→1, cột name 1→2, cột stock 6→5 |
| C3, C4 | ô actions 8→1 (hằng `ACTIONS_CELL`), cột name 1→2 |
| D1 | ô actions 8→1, icon view 1→2 |
| D2 | cột rating 7→8 |
| D5 | ô actions của staff 7→1 |

### Chi tiết V3 (6 test sửa — gãy do đổi nhãn)

Nguyên nhân: V3 đổi nhãn `Add product` → `Create item`, `Save` → `Confirm`; mọi XPath
neo theo text nút (`//button[text()='...']`) không khớp nữa.

| Test | Sửa |
|---|---|
| A3, A4, A5, C1, D2 | XPath `Add product` → `Create item` và `Save` → `Confirm` |
| C2 | XPath `Save` → `Confirm` |

### Phía VLM: 0 chi phí bảo trì

Bộ test VLM (ngôn ngữ tự nhiên) pass **18/18 trên cả V1, V2, V3 mà không sửa dòng nào**
(RQ1, label `gd4-main`, 5 lặp/biến thể, flakiness = 0). Chi phí bảo trì = 0 test,
0 LOC, 0 phút. Đây chính là kết quả trung tâm của RQ2: chi phí bảo trì chuyển từ
"sửa script" (locator) sang "chi phí API mỗi lần chạy" (VLM ~$0.050/run, ~7–10 phút/run).

## 3. Threats to validity (riêng cho phép đo này)

- Phần sửa locator do AI (Claude Code) thực hiện, không phải sinh viên: hai chỉ số
  **số test sửa** và **diff LOC** gần như bất biến theo người sửa (sửa tối thiểu là duy nhất
  về mặt nội dung), nhưng **thời gian sửa** thì không → chưa báo cáo thời gian (mục 4).
- Sửa "tối thiểu để pass" giữ nguyên phong cách selector cố định (nth-child/XPath text) —
  một maintainer thực tế có thể refactor sang locator bền hơn (getByRole), nhưng như vậy
  sẽ đổi bản chất bộ baseline và làm nhiễu phép so sánh.
- Biến thể là thay đổi trình bày có kiểm soát, một chiều (V0 → Vx), trên một ứng dụng mẫu.

## 4. Chỉ số thời gian — cách đo đã chốt trong đề cương (09/07/2026)

Đề cương (bản chưa nộp, đã cập nhật 09/07/2026) định nghĩa lại quy trình bảo trì:
việc sửa do **cùng một quy trình chuẩn hóa, tự động** thực hiện (AI coding agent với
chỉ dẫn cố định "sửa tối thiểu để pass lại, chỉ đổi selector/assertion, không
refactor"), áp dụng đồng nhất cho cả hai bộ test; chỉ số **thời gian** = thời gian
tác nhân chuẩn hóa phục hồi bộ test (đo bằng máy, tái lập được). Hạn chế — thời gian
agent không đại diện công sức sửa thủ công của kỹ sư — ghi trong Threats to Validity.

Việc còn lại: **đo thời gian phục hồi của agent** trong điều kiện chuẩn (branch mới
`rq2-agent-v2`/`rq2-agent-v3`, ghi wall-clock từ lúc nhận danh sách test fail đến khi
18/18), điền vào bảng mục 2; đối chiếu nội dung sửa với `rq2-fix-v2`/`rq2-fix-v3` để
kiểm tra tính ổn định của quy trình. Trình bày thiết kế này với GVHD theo
`docs/gvhd-trao-doi.md` mục 1 (kèm phương án dự phòng nếu GVHD muốn số liệu người thật).
