import fitz  # PyMuPDF


def extract_pdf_outline(pdf_path):
    doc = fitz.open(pdf_path)

    # 获取目录信息
    toc = doc.get_toc()

    # 打印目录信息
    print("PDF Outline:")
    for item in toc:
        title = item[1]
        dest = item[2]
        level = item[0]
        indent = "  " * (level - 1)
        print(f"{indent}{title}, Destination: {dest}")

    doc.close()


def extract_pdf_bookmarks(pdf_path):
    doc = fitz.open(pdf_path)

    # 获取书签信息
    bookmarks = doc.get_bookmarks()

    # 打印书签信息
    print("PDF Bookmarks:")
    for level, (_, title, page_num, _) in bookmarks:
        indent = "  " * (level - 1)
        print(f"{indent}{title}, Page: {page_num}")

    doc.close()


def links_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    # 获取链接信息
    for i in range(1, 15):
        page = doc[i]
        for link in page.get_links():
            rect = link.get("rect", [])  # 超链接的矩形区域
            if len(rect) == 4:
                url = link.get("uri", "")  # 获取链接的URL
                text = page.get_text("text", clip=rect)  # 从链接区域提取文本
                print(f"Page: {i}, URL: {url}, Text: {text}")
            else:
                print(rect)
    doc.close()


# 替换为你的PDF文件路径
pdf_file_path = r"./DATA/Resource/CC2022PART2R1.pdf"

# extract_pdf_outline(pdf_file_path)
links_pdf(pdf_file_path)
# extract_pdf_bookmarks(pdf_file_path)
