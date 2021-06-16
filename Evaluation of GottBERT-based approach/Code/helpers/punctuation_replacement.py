import os
import csv
import re

def rreplace(s, old, new):
    return (s[::-1].replace(old[::-1],new[::-1], 1))[::-1]

def remove_punctuation(sentence):
    ''' Remove punctuation at the end of a sentence, namely punctuation that is used as a sentence boundary

    Replace the punctuation with a <mask> token in order to be able to be used as an input to a BERT model
    Write the punctuation to a different cell in order to be used as the ground truth label
    
    Special cases:
    - If the sentence has no ending punctuation, then put '.' in the ground truth cell. In that case the mask
      is placed at the end of the sentence, unless there is an emoticon at the end, so the mask is placed before that.
      e.g.-emoticons: :), :(, ;), :-), :-(, ;-), :_)'''

    # We suppose that no punctuation appears more than one time per sentence, because of the sentence segmentation step we've taken
    result = re.findall(r'\?+\!+|\?+|\!+|\.+', sentence)
    if len(result)>1:   # in this case replace the last occurrence
        print("WARNING: In sentence '", sentence, "' more than one occurence has been found")
        masked_sentence = rreplace(sentence, result[len(result)-1], ' <mask>')  # replace only the last occurrence of this symbol
        #masked_sentence = sentence.replace(result[len(result)-1], ' <mask>')
        gt = result[len(result)-1]
    elif len(result)==1:
        masked_sentence = rreplace(sentence, result[0], ' <mask>')
        #masked_sentence = sentence.replace(result[0], ' <mask>')
        gt = result[0]
    else:
        # If there isn't an emoticon at the end of a sentence, then place the mask at the end, otherwise put it before the emoticon
        matches = re.findall(r':\)+|:\(+|;\)+|:-\)+|:-\(+|;-\)+|:_\)+', sentence)
        if len(matches)!=0:
            match = matches[-1]
            start_index = sentence.rfind(match)
            if start_index+len(match) == len(sentence):
                masked_sentence = sentence[:start_index] + "<mask> " + sentence[start_index:]
            else:
                masked_sentence = sentence + " <mask>"
        else:
            masked_sentence = sentence + " <mask>"
        gt = '[.]'

    # Except from the current punctuation, return the simpler, more standard version of it
    gt_simple = gt
    if gt=='[.]':
        gt_simple = '.'
    else:
        # target cases: '.', '!', '?', '...'
        res1 = re.search(r'\?+\!+', gt)
        res2 = re.search(r'\?+', gt)
        res3 = re.search(r'\!+', gt)
        res4 = re.search(r'\.\.+', gt)
        if res1 != None:
            gt_simple = gt.replace(gt, '?')
        elif res2 != None:
            gt_simple = gt.replace(gt, '?')
        elif res3 != None:
            gt_simple = gt.replace(gt, '!')
        elif res4 != None:
            gt_simple = gt.replace(gt, '...')

    return masked_sentence, gt, gt_simple

if __name__=='__main__':
    filename_in = os.path.join(os.path.abspath(os.path.join('..', '..')), "Data", "Dortmund_all_segmentedUtterances")
    filename_out = filename_in[:-4]+'_masked.csv'

    # Read input file (csv)
    csv_file_in = open(filename_in)
    csv_reader = csv.reader(csv_file_in, delimiter=',')

    # Write to output file (csv)
    csv_file_out = open(filename_out, "w", newline='')
    csv_writer = csv.writer(csv_file_out, delimiter=',')
    csv_writer.writerow(["Utterance", "Punctuation", "Simple Punctuation"])

    for i, row in enumerate(csv_reader):
        if i>0:
            sentence, gt, gt_simple = remove_punctuation(row[0])
            csv_writer.writerow([sentence, gt, gt_simple])

    csv_file_in.close()
    csv_file_out.close()