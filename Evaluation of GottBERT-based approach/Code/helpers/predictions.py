import os
import csv
from transformers import pipeline

def predict(predictor, sentence):
    result = predictor(sentence)
    pred_dict = {}
    predictions = []
    # some tokens have the same "token_str". In that case, group them and sum their scores
    for i, item in enumerate(result):
        token_str = item["token_str"]
        if pred_dict.get(token_str)==None:
            pred_dict[token_str] = item["score"]
        else:
            pred_dict[token_str] += item["score"]
    # Sort the predictions in descending order based on their score
    sorted_dict = dict(sorted(pred_dict.items(), key=lambda item: item[1], reverse=True))
    # Keep the results in a list, with up to five elements
    for i, key in enumerate(sorted_dict.keys()):
        if i<5:
            predictions.append(key)
            predictions.append(sorted_dict[key])
    for i in range(len(predictions), 10):
        predictions.append("")
        predictions.append("")

    return predictions

if __name__=='__main__':
    filename_in = os.path.join(os.path.abspath(os.path.join('..', '..')), "Data", "Dortmund_all_segmentedUtterances_masked")
    filename_out = filename_in[:-4]+'Predictions.csv'

    # Read input file (csv)
    csv_file_in = open(filename_in)
    csv_reader = csv.reader(csv_file_in, delimiter=',')

    # Write to output file (csv)
    csv_file_out = open(filename_out, "w", newline='', encoding='utf-8')
    csv_writer = csv.writer(csv_file_out, delimiter=',')
    csv_writer.writerow(["Utterance", "Punctuation", "Simple Punctuation", "Prominent Prediction", "Prominent Score", "Prediction 2", "Score 2", "Prediction 3", "Score 3", "Prediction 4", "Score 4", "Prediction 5", "Score 5"])

    predictor = pipeline('fill-mask', model='uklfr/gottbert-base')

    import time
    start = time.time()
    for i, row in enumerate(csv_reader):
        if i>0:
            new_row = row + predict(predictor, row[0])
            csv_writer.writerow(new_row)
    end = time.time()
    csv_file_in.close()
    csv_file_out.close()

    print(end-start)