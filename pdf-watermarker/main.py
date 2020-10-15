import sys
import PyPDF2
import os
from PyQt5 import QtCore, QtGui, QtWidgets

import assets.select_watermark_ui
import assets.select_pdfs_ui
import assets.outcome_ui


class Watermarker(assets.select_watermark_ui.Ui_watermarkWindow):

    def __init__(self):
        self.watermark_pdf = None
        self.pdfs = []
        self.folder = None

    # FUNCTIONALITY
    def wm_pdfs(self):
        """Function which carries out the watermarking of all pages of given pdfs file with a watermark pdf"""

        output = PyPDF2.PdfFileWriter()

        # Context managers used instead of open close statements to avoid causing problems by not being able to close opened pdf files
        # First block opens watermark pdf and gets it's first page to use as the watermark for all other pdfs
        with open(self.watermark_pdf, "rb") as watermark_file:
            self.watermark_pdf = PyPDF2.PdfFileReader(watermark_file)
            watermark_page = self.watermark_pdf.getPage(0)

            for pdf in self.pdfs:
                # Done to get just the name of the pdf file and not it's full directory or .pdf extension
                pdf_name = pdf.split("/")[-1][:-4]

                # Checks if user specified an output folder, and sets output path accordingly
                if self.folder:
                    wm_pdf = os.path.join(self.folder,
                                          f"{pdf_name}(Watermarked).pdf")
                else:
                    wm_pdf = "".join([pdf, " (Watermarked).pdf"])

                # Second block opens the current pdf in the for loop so it's pages can be watermarked
                with open(pdf, 'rb') as input_file:
                    input_pdf = PyPDF2.PdfFileReader(input_file)

                    # Only creates file if file of same name does not already exist, to avoid issues with appending more pages to an existing file
                    if not os.path.exists(wm_pdf):
                        # Third block opens current output file so the watermarked pages can be merged and writen to this file
                        with open(wm_pdf, 'wb') as watermarked_file:

                            for i in range(input_pdf.getNumPages()):
                                pdf_page = input_pdf.getPage(i)
                                pdf_page.mergePage(watermark_page)
                                output.addPage(pdf_page)

                            output.write(watermarked_file)
                    else:
                        print(
                            f"Please ensure that the file:\n{pdf}\ndoes not already have a watermarked version in the selected output folder.")
                        raise FileExistsError

    def choose_file_path(self):
        """QFileDialog pop up allows you to select a file, and that file path is returned"""

        path = QtWidgets.QFileDialog.getOpenFileName()
        return path[0]

    def choose_folder_path(self):
        """QFileDialog pop up allows you to select a folder, and that file path is returned"""

        path = QtWidgets.QFileDialog.getExistingDirectory()
        return path

    # BUTTON FUNCTIONS

    def onClicked_pathButton(self):
        self.lineEdit.setText(self.choose_file_path())

    def onClicked_confirmButton(self):
        self.watermark_pdf = self.lineEdit.text()

        # Checks file path given exists and is a pdf file
        if os.path.exists(self.watermark_pdf) and self.watermark_pdf.endswith(".pdf"):
            watermarkWindow.hide()
            self.start_pdfs_window()

    def onClicked_addButton(self):
        file = self.choose_file_path()
        row = self.pdfs_ui.pdfLlistWidget.currentRow()

        # Adds selected pdf file to self.pdfs list if they are pdf files, are not already in self.pdfs
        if file.endswith(".pdf") and file not in self.pdfs:
            self.pdfs_ui.pdfLlistWidget.insertItem(row, file)
            self.pdfs.append(file)

    def onClicked_addDirectoryButton(self):
        directory = self.choose_folder_path()
        row = self.pdfs_ui.pdfLlistWidget.currentRow()

        # Same as previous function but is used to add all pdf files from a chosen directory instead of just a single pdf at a time
        if os.path.isdir(directory):
            for file in os.listdir(directory):
                if file.endswith(".pdf") and file not in self.pdfs:
                    self.pdfs_ui.pdfLlistWidget.insertItem(
                        row, directory + file)
                    file_path = os.path.join(directory, file)
                    self.pdfs.append(file_path)

    def onClicked_removeButton(self):
        row = self.pdfs_ui.pdfLlistWidget.currentRow()

        # If there is a valid item in the list selected, removes this item from the list and from self.pdfs
        try:
            file = self.pdfs_ui.pdfLlistWidget.item(row).text()
            self.pdfs_ui.pdfLlistWidget.takeItem(row)
            self.pdfs.remove(file)
        except (AttributeError, ValueError):
            pass

    def onClicked_okButton(self):
        # If files have been selected, calls wm_pdfs function to watermark selected pdfs
        if self.pdfs:
            self.wm_pdfs()
            self.pdfs_window.close()
            self.start_outcome_window()

    def onClicked_folderButton(self):
        path = self.choose_folder_path()

        # Makes selected folder into the output folder for watermarked pdfs, if it is a valid directory path
        if os.path.isdir(path):
            self.folder = path

    def onClicked_exitButton(self):
        self.outcome_window.close()

    # GUI WINDOWS ------------------------------------------------------------

    def start_watermark_window(self):
        """Window to select pdf file which will be used as a watermark. Note that watermark must be first page of pdf."""

        self.pathButton.clicked.connect(self.onClicked_pathButton)
        self.confirmButton.clicked.connect(self.onClicked_confirmButton)

    def start_pdfs_window(self):
        """Window to select pdf files to be watermarked"""

        self.pdfs_window = QtWidgets.QDialog()
        self.pdfs_ui = assets.select_pdfs_ui.Ui_pdfsDialog()
        self.pdfs_ui.setupUi(self.pdfs_window)
        self.pdfs_ui.addButton.clicked.connect(self.onClicked_addButton)
        self.pdfs_ui.removeButton.clicked.connect(self.onClicked_removeButton)
        self.pdfs_ui.okButton.clicked.connect(self.onClicked_okButton)
        self.pdfs_ui.folderButton.clicked.connect(self.onClicked_folderButton)
        self.pdfs_ui.addDirectoryButton.clicked.connect(
            self.onClicked_addDirectoryButton)
        self.pdfs_window.show()

    def start_outcome_window(self):
        self.outcome_window = QtWidgets.QDialog()
        self.outcome_ui = assets.outcome_ui.Ui_outcomeDialog()
        self.outcome_ui.setupUi(self.outcome_window)
        self.outcome_ui.exitButton.clicked.connect(self.onClicked_exitButton)
        self.outcome_window.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    watermarkWindow = QtWidgets.QMainWindow()
    watermarker = Watermarker()
    watermarker.setupUi(watermarkWindow)
    watermarker.start_watermark_window()
    watermarkWindow.show()
    sys.exit(app.exec_())
