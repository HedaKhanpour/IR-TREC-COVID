from index import Index
from CsvReader import CsvReader
import time
def main():
    index = Index()
    cord_path = "../cord-19_2020-11-05/"
    csv_reader = CsvReader(cord_path=cord_path)

    i = 0
    timeList = []
    for line in csv_reader.file:
        document = csv_reader.get_next(line)
        if not document == None:
            startTime = time.time()
            index.processDocument(document.get_raw_text(), document.cord_uid)
            processTime = time.time() - startTime
            #print("Processing Time Document " + str(i+1) + ": ", processTime)
            timeList.append(processTime)
        i += 1

        if i == 100:
            print("Breaking at iteration: %d"%i)
            break
    
    csv_reader.file.close()
    print("Average process time: ", sum(timeList) / len(timeList))
    print("***** Program Done *****")




main()
