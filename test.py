import unittest
from collections import OrderedDict
from main import  parse_input_and_simplify_expenses, get_individual_share

'''
This test case validates the core logic of simplifying common expenses
'''
class TestSplitExpense(unittest.TestCase):

    #test should pass as all the inputs are correct 
    def test_1_should_pass_parse_input_and_simplify_expenses(self):
        simplified_debts = parse_input_and_simplify_expenses(self.names, self.correct_expenses_list, \
                                                             self.currency)
        self.assertDictEqual(simplified_debts, self.expected_simplified_dict
)

    
    '''test will fail with SystemExit as currency value is not passed and hence default is '$'
    but expense list has INR. '''
    def test_2_should_fail_parse_input_and_simplify_expenses_for_incorrect_currency(self):
        with self.assertRaises(SystemExit):
            simplified_debts = parse_input_and_simplify_expenses(self.names, self.correct_expenses_list)

    # test will fail with SystemExit as expense records has 'E' which is not there in names list
    def test_3_should_fail_parse_input_and_simplify_expenses(self):
        with self.assertRaises(SystemExit):
            simplified_debts = parse_input_and_simplify_expenses(self.names, self.incorrect_expenses_list, \
                                                                 self.currency)

    #test should pass to get individual share for each person
    def test_4_should_pass_get_expected_individual_share(self):
        share = get_individual_share(self.names, self.user_common_expenses_map)
        self.assertDictEqual(share, self.expected_individual_share)


    ## Variables to hold test data
    names = ['A', 'B', 'C', 'D']

    # Valid expense list for test case 1
    correct_expenses_list = [
        'A paid INR 100',
        'B paid INR 50',
        'C paid INR 30',
        'D paid INR 20'
    ]

    # user_common_expenses_map created to calculate individual share
    user_common_expenses_map = dict()
    user_common_expenses_map['A'] = 100
    user_common_expenses_map['B'] = 50
    user_common_expenses_map['C'] = 30
    user_common_expenses_map['D'] = 20

    # expected individual share based on 'user_common_expenses_map'
    expected_individual_share = dict()
    expected_individual_share['A'] = 50
    expected_individual_share['B'] = 0
    expected_individual_share['C'] = -20
    expected_individual_share['D'] = -30

    # This is an example of incorrect expense list as it has additional person data 'E' which is not in names
    incorrect_expenses_list = [
        'A paid INR 100',
        'B paid INR 50',
        'C paid INR 30',
        'D paid INR 20',
        'E paid INR 20'
    ]

    # currency to use for this test
    currency = 'INR'

    # expected simplified share of each person to be zero after settling down all expenses
    expected_simplified_dict = OrderedDict()
    expected_simplified_dict['A'] = expected_simplified_dict['B'] = expected_simplified_dict['C'] = expected_simplified_dict['D'] = 0.0

if __name__ == '__main__':
    unittest.main()
