import sqlite3
import random

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()

# SQL -----------------------------------------------------------------------------------------------------------------------


def insert_account(number_of_account, ccnumber, PIN, balance):
    cur.execute(
        f'INSERT INTO card VALUES ({number_of_account}, {str(ccnumber)}, {str(PIN)}, {balance});')
    conn.commit()


def delete_account(card_number, PIN):
    cur.execute(
        f'DELETE FROM card WHERE number = {card_number} AND PIN = {PIN};')
    conn.commit()


def create_table():
    cur.execute("""CREATE TABLE IF NOT EXISTS card (
    id INTEGER,
    number TEXT,
    pin TEXT,
    balance INTEGER DEFAULT 0);""")
    conn.commit()


def legitcheck(card_number, PIN):
    cur.execute(f'SELECT number = {str(card_number)} AND pin = {str(PIN)} FROM card;')
    if str(cur.fetchall()).find('1') != -1:
        return True
    False


def balance(card_number, PIN):
    cur.execute(
        f'SELECT balance FROM card WHERE number = {str(card_number)} AND pin = {str(PIN)};')
    print(str(cur.fetchone()).strip('(').strip(')').strip(','))


def add_income(card_number, PIN, income):
    cur.execute(f'SELECT balance FROM card WHERE number = {str(card_number)} AND pin = {str(PIN)};')
    result = list(cur.fetchone())
    money = result[0] + income
    cur.execute(f'UPDATE card SET balance = {money} WHERE number = {card_number} AND pin = {PIN};')
    conn.commit()

# OPTIONS -----------------------------------------------------------------------------------------------------------


def option_one():
    account = BankAccount()
    print(
        f"""\nYour card has been created
Your card number:
{account.ccnumber}
Your card PIN:
{account.PIN}\n""")
    insert_account(account.number_of_account, account.ccnumber,account.PIN, account.balance)


def option_two(card_number, PIN):

    global number

    if legitcheck(card_number, PIN) == True:
        print('\nYou have successfully logged in! \n')

        while True:
            choice = int(input("""\n1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit \n"""))
            if choice == 1:
                balance(card_number, PIN)

            elif choice == 2:
                income = int(input('\nEnter income: \n'))
                add_income(card_number, PIN, income)
                print('\nIncome was added!\n')
            elif choice == 3:
                choice3(card_number, PIN)
            elif choice == 4:
                print('\nThe account has been closed! \n')
                delete_account(card_number, PIN)
                break
            elif choice == 5:
                print('\nYou have successfully logged out!\n')
                break

            elif choice == 0:
                number = 0
                break

    else:
        print('\nWrong card number or PIN! \n')


def choice3(card_number, PIN):
    cur.execute(f'SELECT balance FROM card WHERE number = {str(card_number)} AND pin = {str(PIN)};')
    balance = list(cur.fetchone())[0]
    print('\nTransfer')
    where_to = int(input('Enter card number:'))
    cur.execute(f'SELECT number = {where_to} FROM card;')
    temp = str(cur.fetchall()).find('1')

    if temp == -1:
        print('Such a card does not exist.\n')

    if BankAccount.luhn_algoritm(where_to) == False:
        print('Probably you made a mistake in the card number. Please try again!\n')

    elif int(card_number) == where_to:
        print("You can't transfer money to the same account!\n")    
      
    else:
        how_much = int(input('Enter how much money you want to transfer: \n')) 

        if how_much > balance:
            print('Not enough money!\n')
            
        else:
            print('Success!\n')
            cur.execute(f'SELECT balance FROM card WHERE number = {where_to};')

            second_balance = list(cur.fetchone())[0]
            print(balance - how_much, card_number)
            print(second_balance + how_much, where_to)
            cur.execute(f'UPDATE card SET balance = {balance - how_much} WHERE number = {card_number}')
            cur.execute(f'UPDATE card SET balance = {second_balance + how_much} WHERE number = {where_to}')
            conn.commit()
            
# CLASS -------------------------------------------------------------------------------------------------------------------------

class BankAccount:
    create_table()
    cur.execute('SELECT id FROM card')
    number_of_account = len(cur.fetchall())

    def __init__(self):
        self.ccnumber = self.ccnumber_generator()
        self.PIN = self.PIN_generator()
        self.balance = 0
        create_table()

    @staticmethod
    def PIN_generator():
        a = random.randint(1, 9)
        b = random.randint(0, 9)
        c = random.randint(0, 9)
        d = random.randint(0, 9)
        PIN = a * 1000 + b * 100 + c * 10 + d
        return PIN

    @staticmethod
    def ccnumber_generator():
        while True:
            card_number = str(random.randint(4000000000000000, 4000010000000000))
            if BankAccount.luhn_algoritm(card_number) == True:
                BankAccount.number_of_account = + 1
                return card_number

    @staticmethod
    def luhn_algoritm(card_number):
        suma = 0
        card_list = [x for x in str(card_number)]
        for i in range(0, 16):
            if i == 15:
                suma += int(card_list[i])
                break
            x = int(card_list[i])
            if (i + 1) % 2 == 1:
                 x *= 2
            if x > 9:
                x -= 9
            suma += x

        if suma == 60:
            return True
        return False

# MAIN PART ---------------------------------------------------------------------------------------------------------------------

while __name__ == "__main__":
    create_table()
    number = int(input("""\n1. Create an account
2. Log into account
0. Exit \n"""))

    if number == 1:
        option_one()

    elif number == 2:
        card_number = input('Enter your card number: \n')
        PIN = input('Enter your PIN: \n')
        option_two(card_number, PIN)

    if number == 0:
        print('\nBye!')
        break
