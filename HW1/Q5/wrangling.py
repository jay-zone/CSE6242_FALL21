"""
cse6242 s21
wrangling.py - utilities to supply data to the templates.

This file contains a pair of functions for retrieving and manipulating data
that will be supplied to the template for generating the table. """
import csv

def username():
    return 'mcampo6'

def data_wrangling():

    with open('data/movies.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        table = list()
        # Feel free to add any additional variables
        ...
        
        # Read in the header
        for header in reader:
            break
        
        # Read in each row

        for row in reader:

            table.append(row)

            # Only read first 100 data rows - [2 points] Q5.a
            if len(table) >99:
                break


        import operator
        # Order table by the last column - [3 points] Q5.b
        #table2 = sorted(table, key = operator.itemgetter(2))
        table2 = sorted(table, key=lambda x: float(x[2]), reverse=True)
    
    return header, table2

