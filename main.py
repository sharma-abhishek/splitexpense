import os
import argparse
import re
import operator
from collections import OrderedDict

# creating parser and returning args to read people and expense file from CLI
def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", dest="people_file", required=True, type=argparse.FileType('r'),
                        help="path to file containing list of people")
    parser.add_argument("-e", dest="expense_file", required=True, type=argparse.FileType('r'),
                        help="path to file containing list of expenses")
    parser.add_argument("--currency", nargs='?', const='$')

    args = parser.parse_args()
    return args

# function to sort dictionary by value
def sortDictByValues(debts):
    sortedDict = OrderedDict()
    for key, value in sorted(debts.iteritems(), key=lambda (k,v): (v,k)):
        sortedDict[key] = value
    return sortedDict

def get_individual_share(names, user_common_expenses_map):
    # calculating 'sum' to find out the total expenses
    sum = 0
    for key, value in user_common_expenses_map.iteritems():
        sum = sum + value

    # calculating average 
    average = (sum / len(names))
    individual_share = dict()

    # finding out individual share
    for name in names:
        share = 0
        if name not in user_common_expenses_map.keys():
            share = -1 * average
        else:
            share = ((user_common_expenses_map[name] - average))

        individual_share[name] = share
    return individual_share


def parse_input_and_simplify_expenses(names, expenses, currency='$'):
    # regex to parse individual line
    regex = '(\w+)\s(\w+)\s(\\' + currency +'\s?)(\d+.?\d{1,2})'  #\s(.*)''
    # compiling regex before as it has to be applied to each line
    compiled_regex = re.compile(regex)
    # creating user amount map dictionary
    user_common_expenses_map = dict()

    # iterating on file line by line
    for record in expenses:
        result = compiled_regex.match(record)
        # if result is None, throw error and exit
        if result is None:
            print ("Something wrong with this record: " + record)
            print "Regex does not match, please match command line args with expense input"
            exit(1)
        # get name out of this expense record
        name = result.group(1)
        # checking if the names in expense list is always available in names list
        if name not in names:
            print ("Name: {" + name + "} not found in list of names: [" + ','.join(names) + "]")
            exit(1)
        amount = float(result.group(4))
        if name in user_common_expenses_map.keys():
            user_common_expenses_map[name] += amount
        else:
            user_common_expenses_map[name] = amount

    # sorting dictionary of debts in order of debts (max to min)
    debts = sortDictByValues(get_individual_share(names, user_common_expenses_map))
    # calculating length to find out person in min_debt (person who will get return the most)
    keys_length = len(debts.keys())
    
    # inner method to simplify debt and print it
    def simplifyDebts(debts):

        # getting keys everytime as order is important here.
        keys = debts.keys()

        # calculating index values and then getting person who is in max and min debt
        start_index = 0
        end_index = keys_length - 1
        max_debt_person = keys[start_index]
        min_debt_person = keys[end_index]

        # getting the amount
        max_debt = debts[max_debt_person]
        min_debt = debts[min_debt_person]

        # if min and max debt are both zero, then we have settled all our expenses
        if (max_debt == 0 and min_debt == 0):
            return debts
        
        # finding out max debiter and crediter and settling their amount first.
        minimum = max(-max_debt, min_debt)
        min_debt = min_debt - minimum
        max_debt = max_debt + minimum

        print (max_debt_person + " pays " + currency + str(minimum) \
                + " to " + min_debt_person)

        # updating the map with the settled amount
        debts[max_debt_person] = max_debt
        debts[min_debt_person] = min_debt

        # sorting the dictionary again to find out the next eligible candidates for settling
        debts = sortDictByValues(debts)

        # calling recusively simplifyDebts till everything gets settled
        return simplifyDebts(debts)
    
    # Simplify debts
    return simplifyDebts(debts)


def main():
    # create parser to read CLI options
    args = create_parser()
    # reading names and filecontent
    names = [x.strip() for x in args.people_file.readlines()]
    filecontent = [x.strip() for x in args.expense_file.readlines()] 
    # specifying the currency the amount is in.
    currency = '$' if (args.currency is None) else args.currency
    # call parse_file_and_simplify_expenses to simplify the expenses
    parse_input_and_simplify_expenses(names, filecontent, currency)


if __name__ == '__main__':
    main()