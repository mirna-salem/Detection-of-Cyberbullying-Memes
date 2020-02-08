import pandas as pd

Mirna_df = pd.read_csv('Mirna.csv',  encoding='latin-1')
Obsmara_df = pd.read_csv('Obsmara.csv',  encoding='latin-1')
Jorge_df = pd.read_csv('Jorge.csv',  encoding='latin-1')

#BULLYING BASED ON TEXT ONLY
M_textOnly = Mirna_df.iloc[:,6]
O_textOnly = Obsmara_df.iloc[:,7]
J_textOnly = Jorge_df.iloc[:,1]

text_only_list = []
for i in range(0, 398):
    temp = [M_textOnly[i], O_textOnly[i], J_textOnly[i]]
    text_only_list.append(temp)


final_text_only = []
for i in range(0,len(text_only_list)):
    b_count = 0
    for j in range(0, len(text_only_list[i])):
        if text_only_list[i][j] == 1:
            b_count += 1
    if b_count >= 2:
        final_text_only.append(1)
    else:
        final_text_only.append(0)

#BULLYING BASED ON TEXT AND IMAGE
M_text_image = Mirna_df.iloc[:,7]
O_text_image = Obsmara_df.iloc[:,8]
J_text_image = Jorge_df.iloc[:,2]

text_image_list = []
for i in range(0, 398):
    temp = [M_text_image[i], O_text_image[i], J_text_image[i]]
    text_image_list.append(temp)


final_text_image = []
for i in range(0,len(text_image_list)):
    b_count = 0
    for j in range(0, len(text_image_list[i])):
        if text_image_list[i][j] == 1:
            b_count += 1
    if b_count >= 2:
        final_text_image.append(1)
    else:
        final_text_image.append(0)

#All the OCR Text Transcriptions are the same so I just chose mine
#This text comes from the OCR Transcription!
Text = Mirna_df.iloc[:,2]

final_df_text_only = pd.DataFrame()
final_df_text_only['Text'] = Text
final_df_text_only['Bullying?'] = final_text_only  
final_df_text_only.to_csv('Text_Only_400.csv', mode='w',header = True)

final_df_text_and_image = pd.DataFrame()
final_df_text_and_image['Text'] = Text
final_df_text_and_image['Bullying?'] = final_text_image
final_df_text_and_image.to_csv('Text_and_Image_400.csv', mode='w',header = True)