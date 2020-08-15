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
        """Function which carries out the watermarking of all pages of given pdfs file with a watermark pdf"""

        output = PyPDF2.PdfFileWriter()

        #Context managers used instead of open close statements to avoid causing problems by not being able to close opened pdf files
        #First block opens watermark pdf and gets it's first page to use as the watermark for all other pdfs
        with open(watermark_pdf, "rb") as watermark_file:
            watermark_pdf = PyPDF2.PdfFileReader(watermark_file)
            watermark_page = watermark_pdf.getPage(0)

            for pdf in input_pdfs:
                #Done to get just the name of the pdf file and not it's full directory
                pdf_name = pdf.split("/")[-1]

                #Checks if user specified an output folder, and sets output path accordingly
                if folder:
                    wm_pdf = "".join([folder, "/", pdf_name[:-4], " (Watermarked).pdf"])
                else:
                    wm_pdf = "".join([pdf[:-4], " (Watermarked).pdf"])

                #Second block opens the current pdf in the for loop so it's pages can be watermarked
                with open(pdf, 'rb') as input_file:
                    input_pdf = PyPDF2.PdfFileReader(input_file)

                    #Third block opens current output file so the watermarked pages can be merged and writen to this file
                    with open(wm_pdf, 'wb') as watermarked_file:

                        for i in range(input_pdf.getNumPages()):
                            pdf_page = input_pdf.getPage(i)
                            pdf_page.mergePage(watermark_page)
                            output.addPage(pdf_page)

                        output.write(watermarked_file)


    def choose_file_path(self):
        """QFileDialog pop up allows you to select a file, and that file path is returned"""

        path = QtWidgets.QFileDialog.getOpenFileName()
        return path[0]


    def choose_folder_path(self):
        """QFileDialog pop up allows you to select a folder, and that file path is returned"""

        path = QtWidgets.QFileDialog.getExistingDirectory()
        return path


    #Button Functions
    def onClicked_pathButton(self):
        self.lineEdit.setText(self.choose_file_path())


    def onClicked_confirmButton(self):
        self.watermark_pdf = self.lineEdit.text()

        #Checks file path given exists and is a pdf file
        if os.path.exists(self.watermark_pdf) and self.watermark_pdf.endswith(".pdf"):
            watermarkWindow.close()
            self.start_pdfs_window()


    def onClicked_addButton(self):
        file = self.choose_file_path()
        row = self.pdfs_ui.pdfLlistWidget.currentRow()

        #Adds selected pdf file to self.pdfs list if they arepdf files, are not already in self.pdfs and are not the watermark pdf itself
        if file.endswith(".pdf") and not file == self.watermark_pdf and file not in self.pdfs:
            self.pdfs_ui.pdfLlistWidget.insertItem(row, file)
            self.pdfs.append(file)


    def onClicked_addDirectoryButton(self):
        directory = self.choose_folder_path()
        row = self.pdfs_ui.pdfLlistWidget.currentRow()

        #Same as previous function but is used to add all pdf files from a chosen directory instead of just a single pdf at a time
        if os.path.isdir(directory):
            for file in os.listdir(directory):
                if file.endswith(".pdf") and not file == self.watermark_pdf and file not in self.pdfs:
                    self.pdfs_ui.pdfLlistWidget.insertItem(row, directory + file)
                    self.pdfs.append(file)


    def onClicked_removeButton(self):
        row = self.pdfs_ui.pdfLlistWidget.currentRow()

        #If there is a valid item in the list selected, removes this item from the list and from self.pdfs
        if not self.pdfs_ui.pdfLlistWidget.item(row) == None:
            file = self.pdfs_ui.pdfLlistWidget.item(row).text()
            if file in self.pdfs:
                self.pdfs.remove(file)

        self.pdfs_ui.pdfLlistWidget.takeItem(row)


    def onClicked_okButton(self):
        #If files have been selected, calls wm_pdfs function to watermark selected pdfs
        if not self.pdfs == []:
            self.wm_pdfs(self.pdfs, self.folder, self.watermark_pdf)


    def onClicked_folderButton(self):
        path = self.choose_folder_path()

        #Makes selected folder into the output folder for watermarked pdfs, if it is a valid directory path
        if os.path.isdir(path):
            self.folder = path


    #GUI
    def start_watermark_window(self):
        """Window to select pdf file which will be used as a watermark. Note that watermark must be first page of pdf."""

        self.pathButton.clicked.connect(self.onClicked_pathButton)
        self.confirmButton.clicked.connect(self.onClicked_confirmButton)


    #Dialogs
    def start_pdfs_window(self):
        """Window to select pdf files to be watermarked"""

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
