import sys
import PyPDF2
import glob
import os
from PyQt5 import QtCore, QtGui, QtWidgets

import select_watermark_ui
import select_pdfs_ui


class Watermarker(select_watermark_ui.Ui_watermarkWindow):

    watermark_pdf = None
    pdfs = []
    folder = None

    #Functionality
    def wm_pdfs(self, input_pdfs, folder, watermark_pdf):
        output = PyPDF2.PdfFileWriter()

        with open(watermark_pdf, "rb") as watermark_file:
            watermark_pdf = PyPDF2.PdfFileReader(watermark_file)
            watermark_page = watermark_pdf.getPage(0)

            for pdf in input_pdfs:
                pdf_name = pdf.split("/")[-1]

                if folder:
                    wm_pdf = "".join([folder, "/", pdf_name[:-4], " (Watermarked).pdf"])
                else:
                    wm_pdf = "".join([pdf[:-4], " (Watermarked).pdf"])

                with open(pdf, 'rb') as input_file:
                    input_pdf = PyPDF2.PdfFileReader(input_file)

                    with open(wm_pdf, 'wb') as watermarked_file:

                        for i in range(input_pdf.getNumPages()):
                            pdf_page = input_pdf.getPage(i)
                            pdf_page.mergePage(watermark_page)
                            output.addPage(pdf_page)

                        output.write(watermarked_file)


    def choose_file_path(self):
        path = QtWidgets.QFileDialog.getOpenFileName()
        return path[0]


    def choose_folder_path(self):
        path = QtWidgets.QFileDialog.getExistingDirectory()
        return path


    #Button Functions
    def onClicked_pathButton(self):
        self.lineEdit.setText(self.choose_file_path())


    def onClicked_confirmButton(self):
        self.watermark_pdf = self.lineEdit.text()

        if os.path.exists(self.watermark_pdf) and self.watermark_pdf.endswith(".pdf"):
            watermarkWindow.close()
            self.start_pdfs_window()


    def onClicked_addButton(self):
        file = self.choose_file_path()
        row = self.pdfs_ui.pdfLlistWidget.currentRow()

        if file.endswith(".pdf") and not file == self.watermark_pdf and file not in self.pdfs:
            self.pdfs_ui.pdfLlistWidget.insertItem(row, file)
            self.pdfs.append(file)


    def onClicked_addDirectoryButton(self):
        directory = self.choose_folder_path()
        row = self.pdfs_ui.pdfLlistWidget.currentRow()

        if os.path.isdir(directory):
            for file in os.listdir(directory):
                if file.endswith(".pdf") and not file == self.watermark_pdf and file not in self.pdfs:
                    self.pdfs_ui.pdfLlistWidget.insertItem(row, directory + file)
                    self.pdfs.append(file)


    def onClicked_removeButton(self):

        row = self.pdfs_ui.pdfLlistWidget.currentRow()

        if not self.pdfs_ui.pdfLlistWidget.item(row) == None:
            file = self.pdfs_ui.pdfLlistWidget.item(row).text()
            if file in self.pdfs:
                self.pdfs.remove(file)

        self.pdfs_ui.pdfLlistWidget.takeItem(row)


    def onClicked_okButton(self):
        if not self.pdfs == []:
            self.wm_pdfs(self.pdfs, self.folder, self.watermark_pdf)


    def onClicked_folderButton(self):
        path = self.choose_folder_path()
        if os.path.isdir(path):
            self.folder = path


    #GUI
    def start_watermark_window(self):
        self.pathButton.clicked.connect(self.onClicked_pathButton)
        self.confirmButton.clicked.connect(self.onClicked_confirmButton)


    #Dialogs
    def start_pdfs_window(self):
        self.pdfs_window = QtWidgets.QDialog()
        self.pdfs_ui = select_pdfs_ui.Ui_pdfsDialog()
        self.pdfs_ui.setupUi(self.pdfs_window)
        self.pdfs_ui.addButton.clicked.connect(self.onClicked_addButton)
        self.pdfs_ui.removeButton.clicked.connect(self.onClicked_removeButton)
        self.pdfs_ui.okButton.clicked.connect(self.onClicked_okButton)
        self.pdfs_ui.folderButton.clicked.connect(self.onClicked_folderButton)
        self.pdfs_ui.addDirectoryButton.clicked.connect(self.onClicked_addDirectoryButton)
        self.pdfs_window.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    watermarkWindow = QtWidgets.QMainWindow()
    watermarker = Watermarker()
    watermarker.setupUi(watermarkWindow)
    watermarker.start_watermark_window()
    watermarkWindow.show()
    sys.exit(app.exec_())
