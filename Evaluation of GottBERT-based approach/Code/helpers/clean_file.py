import csv

def clean_file(filename_in, filename_out):
    # Read input file (csv)
    csv_file_in = open(filename_in, encoding='utf-8')
    csv_reader = csv.reader(csv_file_in, delimiter=',')

    # Write to output file (csv)
    csv_file_out = open(filename_out, "w", newline='', encoding='utf-8')
    csv_writer = csv.writer(csv_file_out, delimiter=',')

    # Write all the lines in a new file, except from those that contain some weird characters (e.g. NUL)
    flag=0
    placeholder = 0
    while flag==0:
        try:
            for id, row in enumerate(csv_reader):
                csv_writer.writerow(row)
            flag=1
        except Exception as e:
            placeholder = placeholder + id
            print(Exception,"in line",placeholder)

    return 1

