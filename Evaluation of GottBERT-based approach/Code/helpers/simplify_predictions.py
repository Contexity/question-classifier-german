import os
import csv
import re
import requests

look_up_table = {
    '.': 'EOS',
    '!': 'EOS',
    '?': 'question'
}

def simplify_gt(gt_punct):
    # Convert ground truth values
    if gt_punct=='.' or gt_punct=='...' or gt_punct=='!':
        new_gt = 'EOS'
    else:
        new_gt = 'question'

    return new_gt

def simplify_pred(pred1, pred2=None):
    ''' Convert predicted values '''

    # Check them alone. Because of the possible None value, it's difficult to check them together with the others
    result1 = re.search(r'\.+|\!+', pred1)
    result2 = re.search(r'\?+\!+|\?+', pred1)
    if result1!=None:
        if pred1[result1.start():result1.end()]==pred1:
            return 'EOS'
    if result2!=None:
        if pred1[result2.start():result2.end()]==pred1:
            return 'question'

    if pred1=='</s>' or pred1=='[...]':
        new_pred = 'EOS'
    else:
        if len(pred1)==0:   # empty cell, check pred2 if exists
            if pred2!=None:
                new_pred = simplify_pred(pred2)
            else:
                new_pred = "other"
        else:
            if look_up_table.get(pred1[0])!=None:
                new_pred = look_up_table[pred1[0]]
            else:
                if len(pred1)>1:
                    if look_up_table.get(pred1[1])!=None:
                        new_pred = look_up_table[pred1[1]]
                    else:
                        if pred2!=None:
                            new_pred = simplify_pred(pred2)
                        else:
                            new_pred = "other"
                else:
                    if pred2!=None:
                        new_pred = simplify_pred(pred2)
                    else:
                        new_pred = "other"

    return new_pred

def check_sentence_syntax(sentence, simplified_pred, pred2):

    parameters = {"text": sentence}

    try:
        response = requests.get("http://localhost:11111/api/analyze-text", params=parameters)
        containsQuestionWords = response.json()[0]["containsQuestionWords"]
        containsQuestionSyntax = response.json()[0]["containsQuestionSyntax"]
    except Exception as e:
        print("Exception because of the following response: ", response.text)
        return simplified_pred, "False", "False"

    new_simplified_pred = simplified_pred
    simplified_pred2 = simplify_pred(pred2)
    if simplified_pred=='EOS' and ((containsQuestionWords or containsQuestionSyntax) and simplified_pred2=='question'):
        new_simplified_pred = 'question'

    return new_simplified_pred, containsQuestionWords, containsQuestionSyntax

def tokenize_sent(sentence):
    return len(sentence.split())-1

if __name__=='__main__':
    filename_in = os.path.join(os.path.abspath(os.path.join('..', '..')), "Data", "Dortmund_all_segmentedUtterances_maskedPredictions_cleaned")
    filename_out = 'Dortmund_all_allPredictions'

    # Read input file (csv)
    csv_file_in = open(filename_in, encoding='utf-8')
    csv_reader = csv.reader(csv_file_in, delimiter=',')

    # Write to output file (csv)
    csv_file_out = open(filename_out, "w", newline='', encoding='utf-8')
    csv_writer = csv.writer(csv_file_out, delimiter=',')
    csv_writer.writerow(["Utterance", "Punctuation", "Simple Punctuation", "Prominent Prediction", "Prominent Score", "Prediction 2", "Score 2", "Prediction 3", "Score 3", "Prediction 4", "Score 4", "Prediction 5", "Score 5", "GT Punctuation simplified", "Predicted Punctuation Simplified", "Num of Tokens", "Contains Question Words", "Contains Question Syntax", "New Predicted Punctuation Simplified"])

    for i, row in enumerate(csv_reader):
        if i>=1:
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