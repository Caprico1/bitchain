import requests
import time
import json
import os
from argparse import ArgumentParser

def request_blockchain(address, depth, parent=None):
    r = requests.get("https://blockchain.info/rawaddr/{}".format(address))
    j_data = json.loads(r.text)


    # print(j_data['txs'][0])
    #
    # exit()
    report_creation(address)


    write_to_file(address, j_data, parent=True)

    wrap_up_report(address)

    wallets = get_all_transaction_wallets(j_data)


    for wallet in wallets:

        request_blockchain(wallet, depth-1)


    ## do file saving to json for backlogging

    ## Create report to show an easily digestible table of where an address is sending coin

def write_to_file(address, data, parent=None):

    if parent is None:
        with open('reports/{}/parent_address_{}.json'.format(address, address), 'a') as f:
            json.dump(data, f)
    else:
        with open('reports/{}/{}.json'.format(address, address), 'a') as f:
            json.dump(data, f)

def report_creation(address):
    if not os.path.exists('reports'):
        os.mkdir('reports')
    os.mkdir('reports/{}'.format(address))


def wrap_up_report(address):
    with open('reports/{}/map.txt'.format(address), 'a') as f:
            f.write('{}\n'.format(address))



def get_all_transaction_wallets(data):
    wallets = []

    for transaction in data['txs']:
        print(transaction)
        exit()
        if transaction['prev_out']['spent'] == "True":
            wallets.append(transaction['addr'])
        else:
            pass
    return wallets

def bitchain(address, depth):

    request_blockchain(address=address, depth=depth, parent=True)

parser = ArgumentParser(description="Follow the chain based on an BTC address")

parser.add_argument('--address', help="Bitcoin address to enumerate")
parser.add_argument('--depth', help="How many transactions to go through per\
    address found \n NOTE: this will be a lot if there are a ton of transactions/wallets")

args = parser.parse_args()

address = args.address
depth = args.depth

print("Let's go exploring ...")
time.sleep(1)
bitchain(address, depth)
