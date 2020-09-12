from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import NameObject, createStringObject
import io ,sys, getopt,os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pyfiglet import Figlet

def main(argv):
   inputfile = ''
   if sys.argv[1] == '-h':
        print( 'python medscript.py -i <inputfile> ')
        sys.exit()
   elif sys.argv[1]=='-i':
        inputfile = sys.argv[2]
        RemoveWaterMarkAndMetadata(inputfile)
   if sys.argv[1]=="-list":
      print("LOL")
      arrayArgument = sys.argv
      number = 2
      ArrayLength = len(sys.argv)
      for number in range(ArrayLength):
         if number >=2: #skip script name and parma name
            RemoveWaterMarkAndMetadata(arrayArgument[number])

  

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
if __name__ == "__main__":
   main(sys.argv[1:])