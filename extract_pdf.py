import fitz
import os

pdf_path = "Project Report.pdf"
doc = fitz.open(pdf_path)

os.makedirs("extracted_images", exist_ok=True)

# Extract images
image_count = 0
for page_num in range(doc.page_count):
    page = doc[page_num]
    images = page.get_images(full=True)
    for img_idx, img in enumerate(images):
        xref = img[0]
        try:
            pix = fitz.Pixmap(doc, xref)
            if pix.n >= 5:
                pix = fitz.Pixmap(fitz.csRGB, pix)
            img_filename = f"extracted_images/page{page_num+1}_img{img_idx+1}.png"
            pix.save(img_filename)
            image_count += 1
        except Exception as e:
            pass

# Extract text - write to file with utf-8 encoding
with open("extracted_text.txt", "w", encoding="utf-8") as f:
    for page_num in range(doc.page_count):
        page = doc[page_num]
        text = page.get_text()
        f.write(f"\n{'='*80}\nPAGE {page_num + 1}\n{'='*80}\n{text}\n")

print(f"Done. Extracted {image_count} images and text from {doc.page_count} pages.")
