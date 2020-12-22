# import PyPDF2

# # creating an object 
# file = open('in1.pdf', 'rb')

# # creating a pdf reader object
# fileReader = PyPDF2.PdfFileReader(file)

# # print the number of pages in pdf file
# print(fileReader.numPages)
# print(fileReader.getPage(0).extractText())


import pdfplumber

pdf = pdfplumber.open('in1.pdf')
page = pdf.pages[0]
text = page.extract_text()
print(text)

# table = page.extract_table()
# print(table)


pdf.close()