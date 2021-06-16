import os
import csv
from spacy.lang.de import German

def segment_utterance(sentence, model):
    sentences = []
    doc = model(sentence)
    sentences = list(doc.sents)
    
    return sentences

if __name__=='__main__':
    # Initialize segmentation model
    model = German()  # just the language with no pipeline
    config = {"punct_chars": ['.', '!', '?', '..', '...', '....', '.....']} # add custom sentence boundaries
    model.add_pipe("sentencizer", config=config)

    filename_in = os.path.join(os.path.abspath(os.path.join('..', '..')), "Data", "Dortmund_all")
    filename_out = filename_in[:-4]+'_segmentedUtterances.csv'

    # Read input file (csv)
    csv_file_in = open(filename_in)
    csv_reader = csv.reader(csv_file_in, delimiter=',')

    # Write to output file (csv)
    csv_file_out = open(filename_out, "w", newline='')
    csv_writer = csv.writer(csv_file_out, delimiter=',')
    csv_writer.writerow(["Utterance"])

    for i, row in enumerate(csv_reader):
        if i>0:
            sentences = segment_utterance(row[0], model)
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
