import xlrd 
from decimal import Decimal

def get_data(file name):  
    loc = (file name) 
      
    wb = xlrd.open_workbook(loc) 
    sheet = wb.sheet_by_index(0) 
    sheet.cell_value(0, 0) 
    
    OCR_list = []
    for i in range(sheet.nrows): 
        OCR_list.append((sheet.cell_value(i, 2))) #OCR text is (1,2) Real text is (i,1)
    
    Real_list = []
    for i in range(sheet.nrows):
        Real_list.append((sheet.cell_value(i, 1))) #OCR text is (1,2) Real text is (i,1)
        

    return OCR_list, Real_list
    
def clean(text_list):
    new_list = []
    for line in range(1, len(text_list)):
        line = text_list[line].strip()  # removes trailing and leading spaces
        line = " ".join(line.split())  # removes all whitespace characters, space / tab / newline and form feed
        line = line.lower();
        if line:
            new_list.append(line)
    return new_list

def alignment(Real_clean, OCR_clean):    
    vLength = len(Real_clean) + 1
    wLength = len(OCR_clean) + 1
    
    #First: Createing ScoreMatrix
    ScoreMatrix = []
    
    temp1 = []
    for x in range(wLength):
        temp1.append(0)
    ScoreMatrix.append(temp1)
    
    
    for x in range(1, vLength):
        temp2 = [0]
        ScoreMatrix.append(temp2)
    
    
    for i in range(1, vLength):
        for j in range(1, wLength):
            if Real_clean[i-1] == OCR_clean[j-1]:
                ScoreMatrix[i].append(max(ScoreMatrix[i-1][j], ScoreMatrix[i][j-1], ScoreMatrix[i-1][j-1] + 1))
            else:
                ScoreMatrix[i].append(max(ScoreMatrix[i-1][j], ScoreMatrix[i][j-1], ScoreMatrix[i-1][j-1]))
    
    
    #Creating backtrack matrix
    BackTrack = []
    temp3 = []
    for x in range(wLength):
        temp3.append(1)
    BackTrack.append(temp3)
    
    for x in range(1, vLength):
        temp4 = [-1]
        BackTrack.append(temp4)
    
    for i in range(1, vLength):
        for j in range(1, wLength):
            if ScoreMatrix[i][j] == ScoreMatrix[i-1][j]:
                BackTrack[i].append(-1)
            elif ScoreMatrix[i][j] == ScoreMatrix[i][j-1]:
                BackTrack[i].append(1)
            elif Real_clean[i - 1] == OCR_clean[j - 1]:
                if ScoreMatrix[i][j] == ScoreMatrix[i-1][j-1] + 1:
                    BackTrack[i].append(0)  
    #Backtracking
    btString = ''
    
    i, j = vLength-1, wLength-1
    while i > 0 or j > 0:
        if BackTrack[i][j] == -1:
            i = i - 1
        elif BackTrack[i][j] == 1:
            j = j - 1
        elif BackTrack[i][j] == 0:
            btString = btString + (Real_clean[i-1])
            i = i - 1
            j = j - 1
    
    btString = btString[::-1]
    
    va = ''
    wa = ''
    i, j = vLength - 1, wLength-1
    while i > 0 and j > 0:
        if BackTrack[i][j] == -1:
            va = va + Real_clean[i-1]
            wa = wa + '-'
            i = i - 1
        if BackTrack[i][j] == 1:
            wa = wa + OCR_clean[j-1]
            va = va + '-'
            j = j - 1
        if BackTrack[i][j] == 0:
            va = va + Real_clean[i-1]
            wa = wa + OCR_clean[j-1]
            i = i - 1
            j = j - 1
    
    line_one = va[::-1]
    line_two = wa[::-1]
    
    mismatches = 0
    i = 0
    j = 0
    while i != len(line_one) - 1:
        if line_one[i] != line_two[j]:
            mismatches = mismatches + 1
        i = i + 1
        j = j + 1
    
    #print(mismatches)
    #print(line_one)
    #print(line_two)
    return mismatches, len(Real_clean)

def writeToFile(real_clean, OCR_clean, mismatches, totalChars, percentage):
    
    with open('/tmp/output.tsv', 'wt') as out_file:
    tsv_writer = csv.writer(out_file, delimiter='\t')
    tsv_writer.writerow(['Transcript', 'OCR Transcript', 'Mismatches', 'Total Characters of Transcript', 'Percentage'])
    for i in range(0 , len(OCR_clean)):
    	tsv_writer.writerow([real_clean, OCR_clean, mismatches, totalChars, percentage])

 
def main():
    OCR_list, Real_list = get_data("Evaluate OCR - MS.xlsx")
    OCR_clean = clean(OCR_list)
    Real_clean = clean(Real_list)
    
    #Both OCR_clean and Real_clean are lists of
    #the same length so it doesn't matter which 
    #one you choose to iterate through....
    for i in range(0, len(OCR_clean)):
        mismatches,Real_clean_len = alignment(Real_clean[i], OCR_clean[i])
        
        #print('Number of mismatches: ', mismatches)
        #print('The length of your clean text: ', Real_clean_len)
        percentage = (1 - Decimal(mismatches / Real_clean_len)) * 100   #gets percentage of mismatches in user transcribed text
        # print('Percentage: ', round(percentage, 3))                     #rounds percentage to 3 decimal places
        # print()                                                         #adds empty line between elements
        writeToFile(Real_clean, OCR_clean, mismatches, Real_clean_len, round(percentage, 3))
