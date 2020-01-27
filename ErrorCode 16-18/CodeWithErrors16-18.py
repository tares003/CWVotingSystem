"""
This program is meant to:-
    1 - Read in the file fred.csv -  Done
    2 - Display all the records in the console. -Done
    3 - Display just the details of the third person in the console.
    4 - Please ensure that the resulting file is fully PEP8 compliant.
    5 - Please find the logic errors as well as the syntax errors.

    =============================================================
    The output in the console should look like this:-

    1 Total Votes = 1805
    2 Total Votes = 1666
    3 Total Votes = 2432
    4 Total Votes = 2565
    5 Total Votes = 1696
    6 Total Votes = 2699
    7 Total Votes = 1330
    8 Total Votes = 2029
    9 Total Votes = 2428
    10 Total Votes = 2116
    11 Total Votes = 2144
    12 Total Votes = 1320
    =====================
    ['3', 'Lorrie', 'Nowlan', 'GSU Officer', '956', '666', '310', '500']

    Process finished with exit code 0
    =============================================================

    "A computer lets you make more mistakes faster than any invention in human
     history - with the possible exceptions of handguns and tequila." - Mitch Ratcliffe
"""
# importing the wrong module
# import csvreader
import csv


# The spacing either side of this function is not PEP 8 compliant
def FIND_ROW(row_no, fred):
    i = 0  # Skip the header since the header is still present
    # this_row = list()  # list not List #Typo - No Need for this variable
    print('=====================')
    for line in fred:
        if i == row_no:
            # When hits the row, it should return the row
            return line  # returns the current row
        i += 1


# Indentation error
# return this_row

with open('fred.csv', 'r') as file:  # Missing a colon
    fred = list(csv.reader(file))  # It would easier if being
    for row_no, row in enumerate(fred):
        if row_no == 0:  # First row contains the header info- skip that
            continue
        try:
            #
            print(str(row[0]) + 'Total Votes = %s' % (int(row[4]) + int(row[5])
                                                      + int(row[6]) + int(row[7])))  # Invalid operands
        except ValueError:
            pass
    print(FIND_ROW(3, fred))
