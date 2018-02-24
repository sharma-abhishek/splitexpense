#### Assumptions:

- The name should not have spaces (since regex is used in the solution)
- The default currency is `$`, if there is any other currency being used in expenses, please use --currency to provide currency value
- This program will exit
    - if the command line args does not match the regex
    - if the name in expense record is not in the people list
- The solution is implemented to ease and minimize individual transaction to settle his/her contribution in expenses.


#### Solution:

[![asciicast](https://asciinema.org/a/KjxbYOfawrNBUoVlT59BfKSPi.png)](https://asciinema.org/a/KjxbYOfawrNBUoVlT59BfKSPi)

#### Instruction to compile and run:
- This script is developed using Python 2.7.10. So, to run this, your system must have the correct version of python installed.
- To run this script, navigate your terminal to the project directory where `main.py` is. And, use below command to run this script:
 ```
$ python main.py -p <path_to_people_file> -e <path_to_expense_file> --currency <currency>
 ```

 - Script CLI Options:
 ```
 usage: python main.py [-h] -p PEOPLE_FILE -e EXPENSE_FILE [--currency [CURRENCY]]
 ```
##### NOTE: Please make sure the currency that is passed in above command matches with each expense record in expense file. The mismatch will cause abrupt termination of script 

#### Test cases (Unit Test)

This project also has testcase (`test.py`) which validates the core logic of simplifying expenses with all valid and invalid input data scenarios. There are four testcases:

- `TestCase 1` : This test case pass list of names, expenses and currency with appropriate data and test case validates whether all the debts are cleared or not by checking each individual debt to be zero after the function `parse_input_and_simplify_expenses` runs.

- `TestCase 2` : This test case should raise `SystemExit` as currency value is not passed hence defaults to `$`. However, the expenses are in `INR`.

- `TestCase 3` : This test case should raise `SystemExit` as we pass invalid expenses (containing an extra person which is not in `names` list)

- `TestCase 4` : This test cases should pass as it calculates individual share by passing the `user_common_expenses_map` which holds person contribution to common expenses

##### To run test cases, use following command from project directory (containing `test.py`):
```
$ python test.py
```