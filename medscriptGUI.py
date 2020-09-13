'''MedScript GUI 
beta version 0.1
bug : progressbar
'''

import PySimpleGUI as sg
from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import NameObject, createStringObject
import io ,sys, getopt,os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pyfiglet import Figlet
import time , random

def RemoveWaterMarkAndMetadata(pdfFileName):
   #Banner Code
    custom_fig = Figlet(font='epic')
    print(custom_fig.renderText('By Moulay'))
   #End Banner Code
    print('==========================Disclaimer==========================')
    print(' This script is for educational purposes only')
    print('==============================================================')
    print('=====================Script Usage=============================')
    print('usage : python medscript.py -i <inputfile> ')
    print('the new pdf will be saved in the same folder as the script')
    print('==============================================================')
    SavedFileName = os.path.splitext(os.path.basename(pdfFileName))[0]
    print("Your File name :"+ SavedFileName)
    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)

    #canvas.roundRect(left, bottom, width, height, radius):
    can.setFillColorRGB(255,255,255) #fill with white color
    can.roundRect(5, 3, 800, 20, 4, stroke=0, fill=1)

    can.save()

    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open(pdfFileName, "rb")) #FileName input m pdfFile
    output = PdfFileWriter()
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)

    # finally, write "output" to a real file

    NewFileName = SavedFileName+"_medscript_.pdf"
    outputStream = open(NewFileName, "wb")
    output.addMetadata({'/Producer': 'HP ScanJet Pro 2500'}) #you can change this and add more metadata
    output.write(outputStream)
    outputStream.close()
    print("Removed WaterMark and MetaData :"+ NewFileName)

    pass


sg.theme('Dark')  # please make your windows colorful
radio_choices = ['one pdf file', 'multiple pdf Files']
r_keys = ['-R1-', '-R2-']

while True:
    progressDur = 1000 #usually one pdf file would took less then 1s
    if len(sys.argv) == 1:
        window =sg.Window('MedScript WaterMark Remover',
                        [[sg.Text('Choose pdf')],
                        [sg.Input(key='_FILES_'), sg.FilesBrowse(file_types=(("PDF Files", "*.pdf"),))],
                        [sg.Open('Hide WaterMark'), sg.Cancel()],
                        [sg.ProgressBar(progressDur, orientation='h', size=(35, 15), key='progbar')],
                        ])
        event, values = window.Read(close=True)
        fname = values['_FILES_'].split(';')
    else:
        fname = sys.argv[1]

    if event == 'Cancel':
        sg.popup("Bye !!!!", "Canceled By the user")
        raise SystemExit("Cancelling: no filename supplied")
        break
    else:
        if  fname !=['']:
            
            FilesList = values['_FILES_'].split(';')
            NumberOfFiles = len(FilesList)
            progressDur = NumberOfFiles * progressDur
            i = 0
            for FileElement in FilesList:
                window.Element('progbar').UpdateBar(i + 500) 
                RemoveWaterMarkAndMetadata(FileElement)
                window.Element('progbar').UpdateBar(i + 500) 
                sg.popup('File saved in the same folder as the program')
        else:
            sg.popup('You did not choose any File yet')
    if event == 'Quit':
        break


