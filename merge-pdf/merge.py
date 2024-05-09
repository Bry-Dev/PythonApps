from pypdf import PdfWriter
import os

merger = PdfWriter()
forCreate = False
for fname in os.listdir(os.getcwd()):
  if os.path.isdir(fname):
    print("Directory ", fname)
    new_path = os.path.join(os.getcwd(), fname)
    for pdf_file in os.listdir(new_path):
      pdf_merge = os.path.join(new_path, pdf_file)
      if pdf_file.endswith(".pdf") and os.path.isfile(pdf_merge):
        forCreate = True
        merger.append(pdf_merge)
if forCreate == True:
  merger.write("result.pdf")
merger.close()