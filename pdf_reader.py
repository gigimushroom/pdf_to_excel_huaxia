import re
import pdfplumber
import sys
from os import listdir
from os.path import isfile, join
import csv

"""
date = report[1]
hawb = report[2]
mawb = report[3]
dest = report[4]
chargeable = report[5]
charges = report[6]
unit_price = report[7]
packages = report[8]
weight = report[9]
"""
def read_pdf_as_text(file_name):
    pdf = pdfplumber.open(file_name)
    page = pdf.pages[0]
    text = page.extract_text()
    pdf.close()
    return text

def parse_report(text):
    d = {}

    lines = text.splitlines()

    # find ETD
    dates = lines[23]
    res = re.findall(r'\d\d-(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-\d\d', dates)

    d[1] = res[0]

    # find MAWB, HAWB
    wbs = lines[21].split()
    d[2] = wbs[-1]
    d[3] = wbs[-2]

    # find destination
    start = dates.find(res[0]) + len(res[0])
    end = dates.find(res[1])
    d[4] = dates[start:end].strip() + 'China'

    # Find chargeable, packages, weight
    #print('5,8,9:', lines[19])
    items = lines[19].split()
    d[9] = ''.join(items[:2])
    # 用倒数Index 因为中间可能出现体积
    d[5] = ''.join(items[-4:-2])
    d[8] = ''.join(items[-2:])
    
    # find total charge
    price_no = 26 if 'CHARGES' in lines[24] else 27
    price_line = lines[price_no]
    price = price_line.split()[-1]
    d[6] = price

    # find unit price: 1.85/kg
    unit_price = price_line.split()[-4]
    d[7] = unit_price
    return d
    
def run():
    text = read_pdf_as_text('input/in4.pdf')
    print(text)
    report = parse_report(text)
    print(report)

def eval_folder(folder='input'):
    onlyfiles = [join(folder, f) for f in listdir(folder) if isfile(join(folder, f))]
    reports = []
    for f in onlyfiles:
        print('Processing..', f)
        report = parse_report(read_pdf_as_text(f))
        #print(report)
        reports.append(report)
    
    return reports

def csv_writer(reports):
    with open('output/result.csv', "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        # write headers
        header = ['日期','Invoice No.','总运单号','清关公司','Chargable Weight','Freight','单价','麻袋数',
            '毛重','泡重产生的额外费用','提单重量','重量差','提单号']
        writer.writerow(header)
        
        # contents
        for report in reports:
            l = []
            for i in range(1, 10):
                l.append(report[i])
                
            # writerow requires a list
            writer.writerow(l)
    
reports = eval_folder()
csv_writer(reports)

# run()