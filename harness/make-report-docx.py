#!/usr/bin/env python3
"""Assemble the thesis draft DOCX from the markdown chapters in docs/bao-cao/.

Output: docs/bao-cao/bao-cao-doan.docx — cover page, auto-updating TOC field,
chapters 1-5 with figures embedded at their [HÌNH x.y] / *Hình 4.x* anchors,
references and appendices. Layout follows common VN thesis conventions
(Times New Roman 13pt, 1.5 line spacing); adjust to the faculty template when
merging. Run from the repo root: python3 harness/make-report-docx.py
"""

import os
import re

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt, RGBColor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "docs", "bao-cao")
OUT = os.path.join(SRC, "bao-cao-doan.docx")
FIG = os.path.join(ROOT, "results", "figures")
SHOT = os.path.join(ROOT, "results", "screenshots-app-v1")

CHAPTER_FILES = [
    "chuong-1-gioi-thieu.md",
    "chuong-2-khao-sat.md",
    "chuong-3-phuong-phap.md",
    "chuong-4-ket-qua.md",
    "chuong-5-ket-luan.md",
    "tai-lieu-tham-khao.md",
    "phu-luc.md",
]

FIG_CAPTIONS = {
    "fig-rq1-passrate.png": "Hình 4.1 — RQ1: tỉ lệ pass theo biến thể giao diện (18 test × 5 lặp)",
    "fig-rq1-time-cost.png": "Hình 4.2 — RQ1: thời gian thực thi và chi phí API mỗi run",
    "fig-rq2-maintenance.png": "Hình 4.3 — RQ2: chi phí bảo trì khi nâng cấp giao diện V0 → Vx",
    "fig-rq3-detection.png": "Hình 4.4 — RQ3: phát hiện 5 lỗi phân quyền cấy sẵn, đối chứng build sạch",
    "fig-rq4-hitrate-iou.png": "Hình 4.5 — RQ4: hit-rate và IoU theo điều kiện masking",
}

GREY = RGBColor(0x60, 0x60, 0x60)
TOKEN_RE = re.compile(r"(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)")


def base_styles(doc):
    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(13)
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    pf = normal.paragraph_format
    pf.line_spacing = 1.5
    pf.space_after = Pt(6)
    for name, size in (("Heading 1", 16), ("Heading 2", 14), ("Heading 3", 13)):
        st = doc.styles[name]
        st.font.name = "Times New Roman"
        st.font.size = Pt(size)
        st.font.bold = True
        st.font.color.rgb = RGBColor(0, 0, 0)
        st.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    for sec in doc.sections:
        sec.top_margin = Cm(2)
        sec.bottom_margin = Cm(2)
        sec.left_margin = Cm(3)
        sec.right_margin = Cm(2)


def add_runs(par, text, base_bold=False):
    for tok in TOKEN_RE.split(text):
        if not tok:
            continue
        run = par.add_run()
        if tok.startswith("**") and tok.endswith("**"):
            run.text = tok[2:-2]
            run.bold = True
        elif tok.startswith("`") and tok.endswith("`"):
            run.text = tok[1:-1]
            run.font.name = "Consolas"
            run.font.size = Pt(11.5)
        elif tok.startswith("*") and tok.endswith("*") and len(tok) > 2:
            run.text = tok[1:-1]
            run.italic = True
        else:
            run.text = tok
        if base_bold:
            run.bold = True


def add_caption(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text)
    r.italic = True
    r.font.size = Pt(11.5)


def add_image(doc, path, width, caption=None):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(path, width=width)
    if caption:
        add_caption(doc, caption)


def add_note(doc, text):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.italic = True
    r.font.size = Pt(11)
    r.font.color.rgb = GREY


def add_code_block(doc, lines):
    for ln in lines:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.left_indent = Cm(0.5)
        r = p.add_run(ln if ln else " ")
        r.font.name = "Consolas"
        r.font.size = Pt(10.5)


def add_table(doc, rows):
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    cells = [r for i, r in enumerate(cells) if i != 1]  # drop the |---| separator
    ncols = max(len(r) for r in cells)
    table = doc.add_table(rows=len(cells), cols=ncols)
    table.style = "Table Grid"
    for i, row in enumerate(cells):
        for j in range(ncols):
            cell = table.cell(i, j)
            cell.text = ""
            par = cell.paragraphs[0]
            par.paragraph_format.line_spacing = 1.0
            par.paragraph_format.space_after = Pt(2)
            txt = row[j] if j < len(row) else ""
            add_runs(par, txt, base_bold=(i == 0))
            for run in par.runs:
                run.font.size = Pt(11.5)
    doc.add_paragraph()


def hinh3_images(doc, text):
    """Replace chapter-3 [HÌNH 3.x ...] placeholders with real screenshots."""
    if text.startswith("[HÌNH 3.2"):
        add_image(doc, os.path.join(SHOT, "products-v0.png"), Inches(5.8),
                  "Hình 3.2 — Giao diện gốc V0, trang Products (vai trò admin)")
        return True
    if text.startswith("[HÌNH 3.3"):
        labels = [("products-v0.png", "V0 — gốc"), ("products-v1.png", "V1 — dark theme"),
                  ("products-v2.png", "V2 — topbar + đảo cột/icon"), ("products-v3.png", "V3 — đổi icon/nhãn")]
        for fn, lab in labels:
            add_image(doc, os.path.join(SHOT, fn), Inches(4.6))
            add_caption(doc, lab)
        add_caption(doc, "Hình 3.3 — Bốn biến thể giao diện có kiểm soát")
        return True
    return False


def render_paragraph(doc, text):
    if text.startswith("[HÌNH") or text.startswith("[BẢNG"):
        if hinh3_images(doc, text):
            return
        add_note(doc, "⟪Chỗ chèn: " + text.strip("[]") + "⟫")
        return
    p = doc.add_paragraph()
    add_runs(p, text)
    for png, caption in FIG_CAPTIONS.items():
        if png in text:
            add_image(doc, os.path.join(FIG, png), Inches(5.9), caption)


def render_markdown(doc, path):
    lines = open(path, encoding="utf-8").read().splitlines()
    buf, bullets, notes, table, code = [], [], [], [], None
    i = 0

    def flush():
        nonlocal buf, bullets, notes, table
        if buf:
            render_paragraph(doc, " ".join(buf)); buf = []
        if bullets:
            for b in bullets:
                p = doc.add_paragraph(style="List Bullet")
                add_runs(p, b)
            bullets = []
        if notes:
            add_note(doc, " ".join(notes)); notes = []
        if table:
            add_table(doc, table); table = []

    while i < len(lines):
        ln = lines[i]
        s = ln.strip()
        if code is not None:
            if s.startswith("```"):
                add_code_block(doc, code); code = None
            else:
                code.append(ln)
            i += 1; continue
        if s.startswith("```"):
            flush(); code = []
        elif not s or s == "---":
            flush()
        elif s.startswith("#"):
            flush()
            level = min(len(s) - len(s.lstrip("#")), 3)
            title = s.lstrip("#").strip()
            title = re.sub(r"\s*\((BẢN NHÁP[^)]*|KHUNG CHI TIẾT[^)]*)\)", "", title)
            h = doc.add_heading("", level=level)
            add_runs(h, title)
        elif s.startswith(">"):
            if buf or bullets or table:
                flush()
            notes.append(s.lstrip("> ").strip())
        elif s.startswith("|"):
            if buf or bullets or notes:
                flush()
            table.append(s)
        elif re.match(r"^[-*]\s+", s):
            if buf or table or notes:
                flush()
            bullets.append(re.sub(r"^[-*]\s+", "", s))
        elif re.match(r"^\d+\.\s+", s) and not buf:
            if table or notes:
                flush()
            bullets.append(s)
        elif bullets and ln.startswith(("  ", "\t")):
            bullets[-1] += " " + s
        else:
            if bullets or table or notes:
                flush()
            buf.append(s)
        i += 1
    flush()


def cover_page(doc):
    def center(text, size, bold=False, before=0, after=6):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(before)
        p.paragraph_format.space_after = Pt(after)
        r = p.add_run(text)
        r.bold = bold
        r.font.size = Pt(size)

    center("ĐẠI HỌC QUỐC GIA TP. HỒ CHÍ MINH", 14, bold=True)
    center("TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN", 14, bold=True)
    center("[KHOA — điền theo template]", 13, after=60)
    center("KHÓA LUẬN TỐT NGHIỆP", 18, bold=True, before=40)
    center("ỨNG DỤNG VISION-LANGUAGE MODEL", 17, bold=True, before=30)
    center("TRONG KIỂM THỬ TỰ ĐỘNG GIAO DIỆN NGƯỜI DÙNG PHẦN MỀM", 17, bold=True)
    center("(Vision-Language Models for Automated Software UI Testing)", 13, after=60)
    center("Sinh viên thực hiện: [HỌ TÊN — MSSV]", 13, before=50)
    center("Giảng viên hướng dẫn: [HỌ TÊN GVHD]", 13)
    center("TP. Hồ Chí Minh, [tháng]/2026", 13, before=60)
    doc.add_page_break()


def toc_page(doc):
    h = doc.add_heading("MỤC LỤC", level=1)
    h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p = doc.add_paragraph()
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), r'TOC \o "1-3" \h \z \u')
    run = OxmlElement("w:r")
    t = OxmlElement("w:t")
    t.text = "Nhấp chuột phải vào đây → Update Field để tạo/cập nhật mục lục."
    run.append(t)
    fld.append(run)
    p._p.append(fld)
    add_note(doc, "Ghi chú bản nháp: mục lục là trường TOC tự động — mở file bằng "
                  "Word/Google Docs rồi cập nhật trường để hiển thị.")
    doc.add_page_break()


def abstract_page(doc):
    doc.add_heading("TÓM TẮT", level=1)
    for para in [
        "Đồ án thực hiện một nghiên cứu thực nghiệm so sánh định lượng giữa kiểm thử "
        "GUI dựa trên bộ định vị truyền thống (Playwright) và kiểm thử dựa trên mô hình "
        "thị giác–ngôn ngữ (Midscene.js + Qwen3-VL) trên cùng một ứng dụng web mẫu, cùng "
        "một bộ 18 kịch bản kiểm thử, với bốn biến thể giao diện được kiểm soát chủ động "
        "và mỗi phép đo lặp năm lần.",
        "Kết quả chính: bộ test VLM đạt tỉ lệ pass 100% trên mọi biến thể giao diện và "
        "không cần sửa dòng mã nào (chi phí bảo trì bằng 0), trong khi bộ test locator rơi "
        "còn 50–67% trên các biến thể đổi cấu trúc/nhãn và cần sửa 15 lượt test / 46 dòng "
        "mã để phục hồi; đổi lại, mỗi lượt chạy VLM tốn ~7–10 phút và ~0,05 USD so với ~3 "
        "giây và 0 USD của locator, với độ ổn định tuyệt đối ở cả hai phương pháp. Hai "
        "khảo sát mở rộng cho thấy VLM phát hiện đủ 5/5 lỗi phân quyền hiển thị cấy sẵn "
        "không báo động giả, và việc che dữ liệu nhạy cảm trên ảnh chụp màn hình không làm "
        "giảm khả năng định vị phần tử của mô hình.",
        "Toàn bộ ứng dụng mẫu, hai bộ kiểm thử, hạ tầng đo lường và số liệu được công khai "
        "để tái lập.",
    ]:
        doc.add_paragraph(para)
    add_note(doc, "⟪Bản nháp — sinh viên rà và biên tập lại tóm tắt theo giọng văn của mình.⟫")
    doc.add_page_break()


def main():
    doc = Document()
    base_styles(doc)
    cover_page(doc)
    toc_page(doc)
    abstract_page(doc)
    for i, fn in enumerate(CHAPTER_FILES):
        render_markdown(doc, os.path.join(SRC, fn))
        if i < len(CHAPTER_FILES) - 1:
            doc.add_page_break()
    doc.save(OUT)
    print("wrote", OUT, os.path.getsize(OUT) // 1024, "KB")


if __name__ == "__main__":
    main()
