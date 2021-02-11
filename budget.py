from typing import List

# object of a financial category with which you can perform financial operations
class Category:
    def __init__(self, name):
        self.name = name
        self.category_amount = 0
        self.ledger = []
    
    def __str__(self) -> str:
        res = ''
        res += self.name.center(30, '*') + '\n'

        # add each description and it's amount to result string
        for obj in self.ledger:
            desc_str = obj['description'][0:23].ljust(23, ' ')
            amount = obj['amount']
            amount_str = f'{amount:.2f}'[0:7].rjust(7, ' ')
            res += (desc_str + amount_str + '\n')

        # add total to result string
        res += f'Total: {self.category_amount:.2f}'

        return res

    def deposit(self, amount: int, desc: str='') -> bool:
        self.category_amount += amount
        self.add_to_ledger(amount, desc, 'deposit')

    def withdraw(self, amount: int, desc: str='') -> bool:
        if(amount > 0 and self.check_funds(amount)):
            self.add_to_ledger(amount, desc, 'withdraw')
            self.category_amount -= amount
            return True

        return False

    def add_to_ledger(self, amount: int, desc: str, action: str) -> None:
        if action == 'withdraw':
            self.ledger.append({ "amount": -amount, "description": desc })
        else:
            self.ledger.append({ "amount": amount, "description": desc })

    def get_balance(self) -> int:
        return self.category_amount
    
    def transfer(self, amount: int, category: str) -> bool:
        category.deposit(amount, f'Transfer from {self.name}')
        valid_transaction = self.withdraw(amount, f'Transfer to {category.name}')

        return True if valid_transaction else False
    
    def check_funds(self, amount: int) -> bool:
        return True if amount <= self.category_amount else False

# method to plot out spending of different categories
def create_spend_chart(categories: List[Category]) -> str:
    category_data = {}
    withdrawal_total: int = 0

    # loop through category to find percentages
    for category in categories:
        name: str = category.name
        withdraw_amount: int = 0

        for item in category.ledger:
            if item['amount'] < 0:
                withdraw_amount += -item['amount']
                withdrawal_total += -item['amount']

        category_data[name]: str = withdraw_amount
    
    # Heading and max word length initialized
    res = 'Percentage spent by category\n'
    max_item_len = 0

    # loop from 100 to 0 with a step of -10 to find the percentage for each category and plot it on the graph
    for i in range(100, -10, -10):
        line = f'{i}| '.rjust(5, ' ')

        for key, withdraw in category_data.items():
            percentage = withdraw / withdrawal_total * 100
            if len(key) > max_item_len:
                max_item_len = len(key)
            if percentage  >= i:
                line += 'o'.ljust(3, ' ')
            else:
                line += '   '
        
        res += line + '\n'
    
    # Add a dashed line to separate the data points and naming on the graph
    dashed_line = '    '.ljust(len(categories) * 3 + 5, '-')
    res += dashed_line + '\n'

    # loop through the names and input the characters in vertical order
    for i in range(0, max_item_len):
        res += ''.ljust(5, ' ')

        for item in category_data.keys():
            if len(item) > i:
                res += item[i].ljust(3, ' ')
            else:
                res += ''.ljust(3, ' ')

        # add new line if not on the last row
        if i != max_item_len - 1:
            res += '\n'

    return res