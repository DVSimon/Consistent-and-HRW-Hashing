import csv


def parse(fp):
    with open(fp, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
        csvdata = list(csv_reader)
        return csvdata


#
# tester = parse('causes-of-death.csv')
# print(len(tester) -1)