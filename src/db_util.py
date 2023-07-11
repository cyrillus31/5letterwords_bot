import csv


with open("db/all5letterwords.txt", "r", newline="", encoding="utf-8") as file:
    reader = csv.reader(file, delimiter=",")
    with open("db/word.csv", "w", newline="", encoding="utf-8") as csvfile:
        all_words = next(reader)
        all_words = [word.strip() for word in all_words]
        writer = csv.writer(csvfile, delimiter=",")
        for word in all_words:
            writer.writerow([0, word.strip()])

