import pprint
import mnemonic
import time
import bip32utils
import requests
import random
import os
from colored import fg, bg, attr
from decimal import Decimal
from multiprocessing.pool import ThreadPool as Pool
import threading
from Bip39Gen import Bip39Gen
from time import sleep
import ctypes
#from notifypy import Notify
from mnemonic import Mnemonic
from keccak import Keccak
from eccrypto import curve
import hashlib
import hmac
import argparse
import time
from getpass import getpass


timesl = 3 #latency between requests

threads = 1


class Settings():
    title = f"ETHEREUM MINING WALLETS v1.0 | TELEGRAMM: @mining_21_bot"


def makeDir():
    path = 'results'
    if not os.path.exists(path):
        os.makedirs(path)


def userInput():
    print("Welcome to ETHEREUM MINING WALLETS")
    print("==================================================================")
    print("   ")
    print("ETHEREUM BALANCE FINDER by @mining_21_bot")  
    start()


def getInternet():
    try:
        try:
            requests.get('https://www.google.com')
        except requests.ConnectTimeout:
            requests.get('http://1.1.1.1')
        return True
    except requests.ConnectionError:
        return False


lock = threading.Lock()


def sha3_keccak(input_bytes):
    return Keccak().keccak256(input_bytes)

def getBalance3(addr):
    try:
        URL = f'https://api.etherscan.io/api?module=account&action=balancemulti&address={addr}&tag=latest'
        response = requests.get(URL)
        q = response.json()
        return q
    except:
        print('{}BAN IP, USE VPN{}'.format(fg("#FE672A"), attr("reset")))
        time.sleep(10)
        return (getBalance3(addr))


def get_public_from_private(private_key):
    """
    :param private_key: private key as hex
    :return: public key as hex
    """
    public_key = curve.private_to_public(
        int(private_key, 16).to_bytes(length=32, byteorder='big'))
    return public_key.hex()[2:]

def get_address_from_public_key(public_key):
    """
    :param public_key: public key as hex
    :return: address str
    """
    public_keccak = sha3_keccak(bytes.fromhex(public_key)).hex()
    return '0x' + public_keccak[-40:]

def create_pk():
    return curve.new_private_key().hex()

def generate_address_from_pk(pk_hex):
    public_key = get_public_from_private(pk_hex)
    address = get_address_from_public_key(public_key)
    return address

def generateBd():
    adrBd = {}
    for i in range(10):
        new_pk = create_pk()
        new_address = generate_address_from_pk(new_pk)
        adrBd.update([(f'{new_address}', new_pk)])

    return adrBd


def listToString(s):
    # initialize an empty string
    str1 = ","

    # return string
    return (str1.join(s))




def check():
    while True:
        bdaddr = generateBd()
        addys = listToString(list(bdaddr))
        balances = getBalance3(addys)
        with lock:
            for item in balances["result"]:
                addy = item["account"]
                balance = item["balance"]
                balance = int(balance)
                mnemonic_words = bdaddr[addy]
                if balance > 0:
                    print('{}Balance: {} | Address: {} | Mnemonic phrase: {}{}'.format(fg("#008700"), balance, addy, mnemonic_words, attr( "reset")))
                    with open('results/wet.txt', 'a') as w:
                        w.write(
                            f'Address: {addy} | Balance: {balance} | Mnemonic phrase: {mnemonic_words}\n')
                else:
                    print('{}Balance: {} | Address: {} | Mnemonic phrase: {}{}'.format(fg("#008700"), 0, addy, mnemonic_words, attr( "reset")))
        time.sleep(timesl)

                    



def start():
    pool = Pool(threads)
    for _ in range(threads):
        pool.apply_async(check, ())
    pool.close()
    pool.join()

if __name__ == '__main__':
    ctypes.windll.kernel32.SetConsoleTitleW(f"{Settings.title}")
    makeDir()
    getInternet()
    if getInternet() == False:
        print("You have no internet access the generator won't work.")
    else:
        pass
    userInput()
