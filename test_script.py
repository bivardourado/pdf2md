import pymupdf4llm
import fitz

doc = fitz.open("test.pdf")
print("Pages:", len(doc))
text = pymupdf4llm.to_markdown(doc, pages=[0])
print(text[:100])
