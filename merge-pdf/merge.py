from pypdf import PdfWriter
from PIL import Image
import os

for fname in os.listdir(os.getcwd()):
  forCreate = False
  if os.path.isdir(fname):
    print("Directory ", fname)
    new_path = os.path.join(os.getcwd(), fname)
    merger = PdfWriter()
    image_list = []
    pdf_path = os.path.join(new_path, "image.pdf")
    for pdf_file in sorted(os.listdir(new_path)):
      pdf_merge = os.path.join(new_path, pdf_file)
      if (pdf_file.endswith(".jpg") or pdf_file.endswith(".jpeg")) and os.path.isfile(pdf_merge):
        image_list.append(Image.open(pdf_merge))
      if pdf_file.endswith(".pdf") and os.path.isfile(pdf_merge):
        forCreate = True
        merger.append(pdf_merge)
    if forCreate == True:
      if len(image_list) > 0:
        image_list[0].save(pdf_path, "PDF", resolution=100.0, save_all=True, append_images=image_list[1:])
        merger.append(pdf_path)
      merger.write(os.path.join(new_path,"result.pdf"))
      merger.close()