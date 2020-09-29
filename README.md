# pdf-watermarker
Simple program adds a watermark pdf of choice onto all pages of another pdf

## What I learned
* Use of OOP
* Building GUI's using pyqt5 and qt designer
* Handling of PDF files as well as recognising different file types
* Manipulation of PDF files, using PYPDF2

## Installation
1. Requires python 3.6+ to run. Python can be installed from [here](https://www.python.org/downloads/)
2. Clone the repository by opening your command line/terminal and run: 
```git clone https://github.com/Rolv-Apneseth/pdf-watermarker.git```
    * Note: if you don't have git, it can be downloaded from [here](https://git-scm.com/downloads).
3. Install the requirements for the program.
    * In your terminal, navigate to the cloned directory and run: ```pip install -r requirements.txt```
4. To run the actual program, navigate further into the pdf-watermarker folder and run: ```python3 main.py```

## Usage
1. First, choose a PDF file to watermark other PDFs with. To do this, click on the choose pdf button and navigate to the desired file. (Or type out it's absolute path in the entry box). Then, click confirm.
2. The second window allows you to add PDF files to be watermarked. All currently selected PDFs will have their paths shown on the window.
3. Add a PDF by:
    * Clicking the add pdf button, which allows you to select a single file.
    * Clicking the add all from folder button, which allows you to choose a directory from which all files with the extension .pdf will be added to the list.
    ** If you want to remove a chosen PDF from the list, select it and click remove pdf
4. Click on select output folder to select which directory all the watermarked images will be placed in.
5. Click on watermark pdfs to execute the script and watermark the selected pdfs.
6. The outcome pop up will appear if the script was executed successfully. Click ok to end the program.

Don't worry about losing files as this program merely makes a watermarked copy of the given PDF files.
