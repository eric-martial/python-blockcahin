# IMPORTS
from functools import reduce
import hashlib as hl
import json

# Initialization
MINING_REWARD = 10

genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': [],
    'proof': 100
}
blockchain = [genesis_block]
open_transactions = []
owner = 'Eddy'
participants = {'Eddy'}

########################################################################################
# Blockchain Functions


def hash_block(block):
    return hl.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()


def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def get_balance(participant):
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    # Take in account transactions that have not been added to the blocks
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)

    amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)

    tx_receiver = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
    amount_received = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_receiver, 0)

    return amount_received - amount_sent


# Proof of work
def valid_proof(transactions, last_hash, proof):
    guess = (str(transactions) + str(last_hash) + str(proof)).encode('utf-8')
    guess_hash = hl.sha256(guess).hexdigest()
    print(guess_hash)
    return guess_hash[0:2] == '00'


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0

    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    
    return proof


def add_transaction(recipient, sender=owner, amount=1.0):
    """ 
        Append  a new value as well as the last blockchain value to the blockchain
        Arguments:
            :sender: The sender of the coins
            :recipient: The recipient of the coins
            :amount: The amount of coins sent with the transaction (default = 1.0)
    """
    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False


def verify_blockchain():
    for idx, block in enumerate(blockchain):
        if idx == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[idx - 1]):
            return False
        if not valid_proof(block['transactions'][:-1], block['previous_hash'], block['proof']):
            print('Proof of work is invalid')
            return False
    return True


def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']


def get_transaction_value():
    tx_recipient = input('Please enter the recipient name: ')
    tx_amount = float(input('Please enter your transaction amount: '))
    return (tx_recipient, tx_amount)


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    
    proof = proof_of_work()

    reward_transaction = {
        'sender': 'MINING',
        'recipient': owner,
        'amount': MINING_REWARD    
    }
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': copied_transactions,
        'proof': proof
    }
    blockchain.append(block)
    return True


def print_blockchain_elements():
    for block in blockchain:
        print(block)


########################################################################################
# Main Program

wating_for_input = True

while wating_for_input:
    print('Chose an option')
    print('1: Add a new transaction value')
    print('2: Mine a new block')
    print('3: Output the blockchain blocks')
    print('4: Output participants')
    print('h: Manipulate the chain')
    print('q: Quit')

    user_choice = input("Enter your option: ")

    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        if add_transaction(recipient, amount=amount):
            print('Transaction added successfully :)')
        else:
            print('Transaction failed :(')
        print(open_transactions)
    elif user_choice == '2':
        if mine_block():
            open_transactions = []
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == '4':
        for participant in participants:
            print(participant)
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_hash': '',
                'index': 0,
                'transactions': [{'sender': 'Ilo', 'recipient': 'eric', 'amount': 3.4}]
            }
    elif user_choice == 'q':
        wating_for_input = False
    else:
        print('Please chose existed options')
else:
    print('By !')
