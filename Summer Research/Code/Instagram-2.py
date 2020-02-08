import pandas as pd
import re

df = pd.read_csv('Ordered_insta_10plus_40.csv',  encoding='latin-1')

newDf = pd.DataFrame()

newDf['Unit Ids'] = df['_unit_id']
newDf['Owner_Post_Date'] = df['cptn_time']
newDf['owner_post'] = df['owner_cmnt']
newDf['comments_combined'] = df.iloc[:,1:196].apply(lambda x: ' '.join(x), axis=1)
newDf['Bullying?'] = df.iloc[:,216]
newDf['Aggression?'] = df.iloc[:,214]

#Removes html tags
cleanr = re.compile('<.*?>')
clean_text = lambda x: re.sub(cleanr, '', x)
newDf['comments_combined'] = newDf['comments_combined'].apply(clean_text)

aggression_binary = [] #This is majority list
lc = 0
y = 0
for i in range(0, len(newDf['Aggression?'])):
    if newDf['Aggression?'][i][0].lower() == 'a':
        y += 1
        lc = lc + 1
    else:
        lc = lc + 1
        
    if lc == 5 and y >= 3:
        aggression_binary.append(1)
        lc = 0
        y = 0
    elif lc ==5 and y < 3:
        aggression_binary.append(0)
        lc = 0
        y = 0
        
bullying_binary = [] #This is majority list
lc = 0
y = 0
for i in range(0, len(newDf['Bullying?'])):
    if newDf['Bullying?'][i][0].lower() == 'b':
        y += 1
        lc = lc + 1
    else:
        lc = lc + 1
        
    if lc == 5 and y >= 3:
        bullying_binary.append(1)
        lc = 0
        y = 0
    elif lc ==5 and y < 3:
        bullying_binary.append(0)
        lc = 0
        y = 0

newDf.to_csv('instaOutput.csv')

#gets all distinct unit ids
unique_ui = []
unique_ui.append(newDf['Unit Ids'][0])
for i in range(1, len(newDf['Unit Ids'])):
    if newDf['Unit Ids'][i-1] != newDf['Unit Ids'][i]:
        unique_ui.append(newDf['Unit Ids'][i])

unique_ownerpost = []
unique_ownerpost.append(newDf['owner_post'][0])
for i in range(1, len(newDf['Unit Ids'])):
    if newDf['Unit Ids'][i-1] != newDf['Unit Ids'][i]:
        unique_ownerpost.append(newDf['owner_post'][i])
        
unique_comments = []
unique_comments.append(newDf['comments_combined'][0])
for i in range(1, len(newDf['Unit Ids'])):
    if newDf['Unit Ids'][i-1] != newDf['Unit Ids'][i]:
        unique_comments.append(newDf['comments_combined'][i])
        
unique_ownerpostdate = []
unique_ownerpostdate.append(newDf['Owner_Post_Date'][0])
for i in range(1, len(newDf['Unit Ids'])):
    if newDf['Unit Ids'][i-1] != newDf['Unit Ids'][i]:
        unique_ownerpostdate.append(newDf['Owner_Post_Date'][i])


majority_df = pd.DataFrame()
majority_df['Unit_Ids'] = unique_ui
majority_df['Owner_Post'] = unique_ownerpost
majority_df['Owner Post Date'] = unique_ownerpostdate
majority_df['Comments_Combined'] = unique_comments
majority_df['Bullying Majority'] = bullying_binary
majority_df['Aggression Majority'] = aggression_binary

majority_df.to_csv('insta_majority2.csv')
