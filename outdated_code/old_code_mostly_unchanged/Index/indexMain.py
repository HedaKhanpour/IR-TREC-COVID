from index import Index
from CsvReader import CsvReader
import time

def count_documents(path_metadata):
    cnt = 0
    with open(path_metadata, "r", encoding="utf-8") as f:
        cnt = len(list(f))-1
    return cnt

def main():
    index = Index()
    cord_path = "../cord-19_2020-11-05/"
    cord_path = "../cord-19_2020-07-16/"
    csv_reader = CsvReader(cord_path=cord_path)
    index_path = "../dataComplete_2020-07-16/"
    total_doc_count = count_documents(cord_path + "metadata.csv")
    i = 0
    for line in csv_reader.file:
        document = csv_reader.get_next(line)
        if not document == None:
            index.processDocument(document.get_raw_text(), document.cord_uid, index_path)
        i += 1

        if (i % 1000) == 0:
            print("Processed documents: {} / {}".format(i, total_doc_count))

    print("Processed documents: {} / {}".format(i, total_doc_count))
    csv_reader.file.close()
    print("***** Program Done *****")


main()
