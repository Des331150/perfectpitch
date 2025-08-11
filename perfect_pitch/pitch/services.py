import pymupdf


def extract_text(filepath: str):
    doc = pymupdf.open("sample.pdf")
    out = open("output.txt", "wb")
    for page in doc:
        text = page.get_text().encode("utf-8")
        out.write(text)
    out.close()
