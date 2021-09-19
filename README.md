# go-dutch

## Contents

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Group Class](#group-class)
- [Group Functions](#group-functions)
- [Suggestions](#suggestions)
- [Authors](#authors)

## Description

Have you ever been in a situation where you hit your head against the wall trying to split your bill with friends after a dinnner at a diner? Well, no worries. The go-dutch library written in Python3 has the sole purpose to make that task easier. It will tell you what payments should be made in a group of people in order to settle debts conveniently.


## Installation

## Usage

## Group Class

- Constructor

  The Group class' constructor has one optional argument, which is an iterable of strings. Each string is a name of a person involved in a group. No duplicate strings are allowed in a group. An empty string is also allowed.

      group = Group (["Joe", "John", "Ryan"])

- Attributes
  - **balances**  
    'balances' is a dictionary with the members as keys and the the net balances as values. The net balance of any new member will be zero initially. The getter function for balances can be used to retrieve the dictionary. A positive value indicates that the member is yet to receive money and a negative value indicates that the individual owes money to the group.

        group.get_balances()  
        -> { "Max": 0, "Ron": 0 }

  - **ledger**  
    'ledger' keeps the record of all transactions that have occurred in the group in the form of a specific namedtuple [Transaction](#transaction). The ledger can be retrieved as follows:

        group.get_ledger()  
        -> [Transaction(payer='Ernie', payees=['Allen'], amount=20, weights=None), Transaction(payer='Ellie', payees=['Joel', 'Allen'], amount=42, weights=[3, 4])]

- Inheritence  
  The group class inherits [collections.abc.Collection](https://docs.python.org/3/library/collections.abc.html#collections.abc.Collection). Consequently, the group objects will have `__len__`, `__contains__`, and `__iter__` attributes. The implementation of functions related to that are modified.  
  The length of the object would return the number of members in the group. One can get the iterator for the keys of balances attribute of the group through `__iter__`. Also, one can skip using 'has_member' function, explained in the GroupFunctions section to check if a member exists in a group, or iterate through it as any iterable.

      if 'Dom' in group:
        # do something
      for mem in group:
        # member


## Group Functions

- **add_member ( string )**  
  'add_member' adds a single individual to the group. No return value.

      group.add_member('Sonya')  

- **extend_members ( iterable of strings )**  
  'extend_members' accepts an iterable of individuals to add to the group. No return value.

      group.extend_members(['Jay', 'Matt'])

- **getters**
  - get_members: returns a list of all the members in the group  

        group.get_members()
  
  - get_balances: returns a dictionary with members of the group mapping to their corresponding net balance in the group

        group.get_balances()
  
  - get_balance(string): returns the net balance of a single member in the group. Raises an error if the member doesn't exist in the group

        group.get_balance('Cathy')  
        -> -5.6  
  
  - get_ledger: returns the ledger of the group, which is a list of [Transactions](#transaction)

        group.get_ledger()  

- **has_member ( string )**  
  'has_member' returns true if the individual exists in the group, and false if not.

        group.has_member('Pam')  
        -> False

- **clear**  
  'clear' removes all the members from the group and all records from the ledger. It refreshes the group. No return value.

      group.clear()

- **remove_settled_member ( string )**
  'remove_settled_member' does exactly as the name suggests. It accepts a member string and removes it from the group only if the member is settled, meaning the member's net balance is zero. Otherwise, the method raises a ValueError, since removing someone yet to settle would make it impossible to settle the rest of the group. No return value.

      group.remove_settled_member('Sean')

- **add_transaction ( payer, payees, amount, weights=None )**  
  'add_transaction' adds a Transaction namedtuple to the ledger and makes changes accordingly to the net balances of the members in the group. No return value.
  The payer is a single string member and payees is a list of string members. All of them must exist in the group. The amount is the float value representing the magnitude of the cost.  
  Weights is an optional argument, a list of floats, that holds exactly the same number of elements as payees. Weights represent the proportions of the costs that are imposed on the payees. The order determines what weight is imposed on which payee. If weights is not provided, it is assumed the amount is imposed equally on all the payees.

      group.add_transaction('Mike', ['Mike', 'Carol', 'Ben'], 45, [1, 3, 5])


  The function appends transactions in order to the ledger. To summarise, the 'Transaction' namedtuple is structured as shown below, corresponding accordingly with the arguments of the 'add_transaction' function.

  ### **Transaction**  

      Transaction = collections.namedtuple("Transaction", "payer, payees, amount, weights")

  | Transaction Attribute  |  Data type        |         Description        |
  | ------- | ------------ |  --------------------------------------------- |
  | payer   | String       |  The member that bears the cost                |
  | payees  | List[String] |  The members that the amount is paid for       |      
  | amount  | float        |  The cash amount involved                      |
  | weights | List[float]  |  The proportions of the amount on each payee   |


- **show_settle_min_flow**  
  'show_settle_min_flow' gives us the list of individual to individual payments that would settle the group with minimum cash flow among the members of the group. The function returns a list of 'Payment' namedtuples with attributes payer, payee and amount. They have similar meanings to that of 'Transaction' namedtuple, except there are no weights, and the payee is a single member string.

      group.show_settle_min_flow()  
      -> [Payment(payer='Ellie', payees='Ellen', amount=20), Payment(payer='Nell', payees='Ellie', amount=12)]

  The 'Payment' namedtuple is structured as follows:

  ### **Payment**  

      Payment = collections.namedtuple("Payment", "payer, payee, amount")

  | Payment Attribute    |    Data type     |      Description      |
  | ------- | ------------ |  ------------------------------------- |
  | payer   | String       |  The member that pays                  |
  | payee   | String       |  The member that the amount is paid to |      
  | amount  | float        |  The cash amount involved              | 

- **settle_min_flow**  
  'settle_min_flow' settles all members, bringing all balances to zero. Consequently, it appends the ledger with the transactions needed to achieve that. It is the same payments, in terms of transactions, that you get from 'show_settle_min_flow'. It simplifies the programmer's job of having to settle the group by executing each payment one by one.

      group.settle_min_flow()

- **show_settle_min_transactions**  
  'show_settle_min_transactions' gives us the list of individual to individual payments that would settle the group with minimum number of transactions among the members of the group. The function returns a list of [Payment](#payment).

      group.show_settle_min_transactions()

- **settle_min_transactions**  
  'settle_min_transactions' settles all members, bringing all balances to zero. Consequently, it appends the ledger with the transactions needed to achieve that. It is the same payments, in terms of transactions, that you get from 'show_settle_min_transactions'. It simplifies the programmer's job of having to settle the group by executing each payment one by one.

      group.settle_min_transactions()


## Suggestions

Any suggestions and concerns are welcome. Fork the repository and ping us through GitHub issues and we would be thankful to incorporate your changes to the library, if favorable.

## Authors

- Chengjia Yu: [GitHub](https://github.com/cyu5)
- Sanjiv Pradhanang: [Portfolio](https://spradha1.github.io/portfolio), [LinkedIn](https://www.linkedin.com/in/sanjiv-pradhanang-a05967b5/), [GitHub](https://github.com/spradha1)