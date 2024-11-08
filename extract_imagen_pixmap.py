import pymupdf
import glob
from PIL import Image
import io
import os

dir_pdfs = "data/prova_dataset/*.pdf"
out_imgs = "data/imgs/imgs_dataset"

if not os.path.exists(out_imgs):
    os.makedirs(out_imgs)

for file in glob.glob(dir_pdfs ):
    doc = pymupdf.open(file)
    for idx_page, page in enumerate(doc):
        pixels = page.get_pixmap()
        page_image = pixels.tobytes()
        page_image = Image.open(io.BytesIO(page_image))
        name_file = file.split("\\")[-1].split(".")[0]
        page_image.save(f"{out_imgs}\\{name_file}_p_{idx_page}.png")
    



