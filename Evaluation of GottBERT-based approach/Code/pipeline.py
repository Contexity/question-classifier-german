import os
import csv
import re
from spacy.lang.de import German
from transformers import pipeline
from helpers.sentence_segmentation import segment_utterance
from helpers.punctuation_replacement import remove_punctuation
from helpers.predictions import predict
from helpers.simplify_predictions import *
from helpers.clean_file import clean_file

'''
    This code takes as input a csv file (in utf-8 encoding) and returns a csv file with all the information regarding the ground truth and predicted punctuation.
    After every preprocessing step, it saves the data in new csv files in order to be easier to run only a part of the process afterwards.
'''

## 1st step: utterance segmentation
# Initialize segmentation model
segmentation_model = German()  # just the language with no pipeline
config = {"punct_chars": ['.', '!', '?', '..', '...', '....', '.....']} # add custom sentence boundaries
segmentation_model.add_pipe("sentencizer", config=config)

# Open input and output csv files
filename_in_1 = os.path.join(os.path.abspath('..'), "Data", "Dortmund_all.csv") 
filename_out_1 = filename_in_1[:-4]+'_segmentedUtterances.csv'

# Read input file (csv)
csv_file_in = open(filename_in_1) # There is also an option regarding the encoding of the file, so depending on that you can add: encoding='utf-8'
csv_reader = csv.reader(csv_file_in, delimiter=',')

# Write to output file (csv)
csv_file_out = open(filename_out_1, "w", newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file_out, delimiter=',')
csv_writer.writerow(["Utterance"])

for i, row in enumerate(csv_reader):
    if i>0:
        if len(row)==0:
            continue
        sentences = segment_utterance(row[0], segmentation_model)
        for sent in sentences:
            # check if the sentence has only non-alphanumeric characters. If so, don't write it in the output file
            flag = 0
            for letter in sent.text:
                if letter.isalnum():
                    flag = 1
                    break
            if flag==1 and sent.text!=':D' and len(sent.text)!=0:
                csv_writer.writerow([sent.text])

csv_file_in.close()
csv_file_out.close()

## 2nd step: Punctuation replacement by a <mask> in order to be used as input to the GottBERT model
## and 3rd step: Pass all the sentences through gottbert to get predictions of the punctuation
filename_out2 = filename_out_1[:-4]+'_maskedPredictions.csv'

# Read input file (csv)
csv_file_in = open(filename_out_1, encoding='utf-8')
csv_reader = csv.reader(csv_file_in, delimiter=',')

# Write to output file (csv)
csv_file_out = open(filename_out2, "w", newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file_out, delimiter=',')
csv_writer.writerow(["Utterance", "Punctuation", "Simple Punctuation", "Prominent Prediction", "Prominent Score", "Prediction 2", "Score 2", "Prediction 3", "Score 3", "Prediction 4", "Score 4", "Prediction 5", "Score 5"])

# Initialize gottbert's pipeline
predictor = pipeline('fill-mask', model='uklfr/gottbert-base')

# For each sentence
for i, row in enumerate(csv_reader):
    if i>0:
        init_sentence = row[0]
        # Remove punctuation
        sentence, gt, gt_simple = remove_punctuation(init_sentence)
        # Make predictions
        predictions = predict(predictor, sentence)

        new_row = [sentence, gt, gt_simple] + predictions
        csv_writer.writerow(new_row)

csv_file_in.close()
csv_file_out.close()

# 4th step: Convert all the ground truth punctuation and predictions to three categories: 'question', 'EOS', 'other'
filename_out2_cleaned = filename_out2[:-4]+'_cleaned.csv'
filename_out3 = filename_in_1[:-4]+'_allPredictions_test.csv'

# Clean "...masked_predictions.csv" file
clean_file(filename_out2, filename_out2_cleaned)

# Read input file (csv)
csv_file_in = open(filename_out2_cleaned, encoding='utf-8')
csv_reader = csv.reader(csv_file_in, delimiter=',')

# Write to output file (csv)
csv_file_out = open(filename_out3, "w", newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file_out, delimiter=',')
csv_writer.writerow(["Utterance", "Punctuation", "Simple Punctuation", "Prominent Prediction", "Prominent Score", "Prediction 2", "Score 2", "Prediction 3", "Score 3", "Prediction 4", "Score 4", "Prediction 5", "Score 5", "GT Punctuation simplified", "Predicted Punctuation Simplified", "Num of Tokens", "Contains Question Words", "Contains Question Syntax", "New Predicted Punctuation Simplified"])

for i, row in enumerate(csv_reader):
    if i>0:
        sentence, gt_punct, pred1, pred2 = row[0], row[2], row[3], row[5]
        simplified_gt = simplify_gt(gt_punct)
        simplified_pred = simplify_pred(pred1, pred2)
        simplified_pred2, cqw, cqs = check_sentence_syntax(sentence, simplified_pred, pred2)
        tokens = tokenize_sent(row[0])
        new_row = row[:13] + [simplified_gt, simplified_pred, tokens, cqw, cqs, simplified_pred2]
        csv_writer.writerow(new_row)
    if i%100==0:
        print("i=",i)

csv_file_in.close()
csv_file_out.close()