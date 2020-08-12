import sys
import PyPDF2
import glob

if str(sys.argv[2]) == "all":
    inputs = glob.iglob("*.pdf")
else:
    inputs = sys.argv[2:]

watermark = str(sys.argv[1])
watermark_file = open(watermark, "rb")
watermark_pdf = PyPDF2.PdfFileReader(watermark_file)
watermark_page = watermark_pdf.getPage(0)

def wm_pdf(input_pdfs):
    output = PyPDF2.PdfFileWriter()
    for pdf in input_pdfs:
        watermarked_file = open("(Watermarked) "+pdf, 'wb')
        input_file = open(pdf, 'rb')
        input_pdf = PyPDF2.PdfFileReader(input_file)
        for i in range(input_pdf.getNumPages()):
            pdf_page = input_pdf.getPage(i)
            pdf_page.mergePage(watermark_page)
            output.addPage(pdf_page)
        input_file.close()
    output.write(watermarked_file)
    input_file.close()
    watermarked_file.close()


wm_pdf(inputs)

watermark_file.close()


