import csv

bul = []
nonBul = []

with open('Clean_Spring_Semester.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        if row[1] == '0':
            nonBul.append(row)
        elif row[1] == '1':
            bul.append(row)

#pos = bullying
#neg = not bullying
            
with open('pos.csv', 'w',newline='') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerows(bul)

with open('neg.csv', 'w',newline='') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerows(nonBul)