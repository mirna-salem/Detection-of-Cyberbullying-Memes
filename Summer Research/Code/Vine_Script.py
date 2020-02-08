import pandas as pd
import re

df = pd.read_csv('vine ordered labeled.csv',  encoding='latin-1')

newDf = pd.DataFrame()

newDf['Unit Ids'] = df['_unit_id']
newDf['Owner Name'] = df['username']
newDf['Owner_Post_Date'] = df['creationtime']
newDf['comments_combined'] = df.iloc[:,2:661].apply(lambda x: ' '.join(x.astype(str)), axis=1)

#BULLYING COLUMN 
#If it's "nonBll", append 0
#If it's "bullying", append 1
bullying = []
temp = df.iloc[:,673] 
for i in range(0, len(temp)):
    if temp[i][0] == 'n':
        bullying.append(0)
    else:
        bullying.append(1)
        
newDf['Bullying?'] = bullying
newDf['Bullying Confidence'] = df['question2:confidence']

bullying_confidence = []
for i in range (0, len(newDf['Bullying Confidence'])):
    if newDf['Bullying Confidence'][i] >= .75:
        bullying_confidence.append(newDf['Bullying?'][i])


#COMMENTS COLUMN
#Removes html tags
cleanr = re.compile('<.*?>')
clean_text = lambda x: re.sub(cleanr, '', x)
newDf['comments_combined'] = newDf['comments_combined'].apply(clean_text)
newDf['Owner Name'] = newDf['Owner Name'].apply(clean_text)

comments = []
for i in range (0, len(newDf['Bullying Confidence'])):
    if newDf['Bullying Confidence'][i] >= .75:
        comments.append(newDf['comments_combined'][i])

final_clean_posts = []
patterns = ['<.*?>', '\([^)]*\)','[^A-Za-z0-9]+', 'empety']
for i in range(0, len(comments)):
    count = 0
    for j in patterns:
        if count == 0:
            final_clean_posts.append(re.sub(j, '', comments[i]))
        elif count > 0:
            final_clean_posts[i] = re.sub(j, ' ', final_clean_posts[i])
            final_clean_posts[i] = final_clean_posts[i].strip()
        count += 1

    
final_df = pd.DataFrame()
final_df['Text'] = final_clean_posts
final_df['Bullying?'] = bullying_confidence   
final_df.to_csv('Final_Vine.csv', mode='w',header = False)
