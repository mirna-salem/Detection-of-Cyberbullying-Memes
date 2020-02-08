import csv
import pandas as pd
import re
from decimal import Decimal

tsv = []
with open("FP_data.tsv") as fd:
    rd = csv.reader(fd, delimiter="\t", quotechar='"')
    for row in rd:
        tsv.append(row)

entries = []    
for i in range(len(tsv)):
    entries.append(tsv[i])
  
    
#2,5,8
checking_majority = []

for i in range(0,len(tsv)):
    classifications = []
    
    for j in range(len(tsv[i])):
        if j == 2:
            classifications.append(tsv[i][j])
        elif j == 5:
            classifications.append(tsv[i][j])
        elif j == 8:
            classifications.append(tsv[i][j])
            
    checking_majority.append(classifications)

#Getting Majority Yes or No's, 1st index is not relevant
majority_binary = []
for i in range(0,len(checking_majority)):
    yes_count = 0
    for j in checking_majority[i]:
        if j == 'Yes':
            yes_count += 1
        
    if yes_count >= 2:
        majority_binary.append(1)
    else:
        majority_binary.append(0)

#Calculating Average Severity  col. 3,6,9  
average_severity = []
all_severities = []
for i in range(0,len(entries)):
    severities = []
    for j in range(len(entries[i])):
        if j == 3:
            if entries[i][j].lower() == 'none':
                severities.append(0)
            else:
                severities.append(entries[i][j])
        elif j == 6:
            if entries[i][j].lower() == 'none':
                severities.append(0)
            else:
                severities.append(entries[i][j])
        elif j == 9:
            if entries[i][j].lower() == 'none':
                severities.append(0)
            else:
                severities.append(entries[i][j])
    all_severities.append(severities)

for i in range(0, len(all_severities)):
    avg = 0
    for j in range(len(all_severities[i])):
        try:
            avg += int(all_severities[i][j])
        except ValueError:
            avg += 0
    avg = avg/3
    average_severity.append(round(avg, 3))

#Getting Users and Posts
users = []
posts = []
for i in range(0,len(tsv)):
    users.append(tsv[i][0])
    posts.append(tsv[i][1])


final_clean_posts = []
patterns = ['<.*?>', 'A:', 'Q:','[^A-Za-z0-9]+', '039']
for i in range(0, len(posts)):
    count = 0
    for j in patterns:
        if count == 0:
            final_clean_posts.append(re.sub(j, ' ', posts[i]))
        elif count > 0:
            final_clean_posts[i] = re.sub(j, ' ', final_clean_posts[i])
            final_clean_posts[i] = final_clean_posts[i].strip()
        count += 1

    
with open('Formspring.csv', 'wt', encoding="utf-8",newline='') as out_file:
    tsv_writer = csv.writer(out_file, delimiter=',', lineterminator='\n')
    tsv_writer.writerow(['post', 'bully'])
    for i in range(1,len(entries)):
        tsv_writer.writerow([final_clean_posts[i], majority_binary[i]])

                