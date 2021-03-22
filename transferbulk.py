#!/usr/bin/env python3
# Script to transfer assets on the Ravencoin platform
# Reads from a csv file
# Template Google Spreadsheet at:  
#   https://docs.google.com/spreadsheets/d/1sSQOpp6NVt73ICfo_jSTZkpA1O_lBzqhIo1MpyElq0c
# In Google Sheets: File->Download As->.csv
# Prerequisite: 
#    * ravend daemon to be running
#    # sudo apt-get install python3-pip
#    * pip3 install python-bitcoinrpc
# In order to use metadata, you must install be running IPFS
#



import random
import os
import subprocess
import csv
import json
import hashlib


#Set this to your raven-cli program
cli = "raven-cli"

#UNCOMMENT OUT YOUR MODE
mode =  ""
rpc_port = 8766

#Uncomment for testnet
mode =  "-testnet"
rpc_port = 18766

#Uncomment for regtest
#mode =  "-regtest"
#rpc_port = 18443


in_csv_file = "in.csv"
out_csv_file = "out.csv"

#Set this information in your raven.conf file (in datadir, not testnet3)
#Match the user and password in this file.
#rpcuser=rpcuser
#rpcpassword=rpcpass555

rpcuser = 'rpcuser'
rpcpassword = 'rpcpass555'


def transfer(asset, qty, address, ipfs_hash = ''):
    cmd = cli + " " + mode + " transfer " + asset + " " + str(qty) + " " + "\"" + address + "\"" + " " + "\"\"" + " " + ipfs_hash

    print(cmd)
    os.system(cmd)  


def rpc_call(params):
    process = subprocess.Popen([cli, mode, params], stdout=subprocess.PIPE)
    out, err = process.communicate()
    return(out)

def do_transfer(asset, qty, address, ipfs_hash = ''):
    rpc_connection = get_rpc_connection()
    print("RPC Transfer: " + asset + " " + str(qty) + " " + "\"" + address + "\"" + " " + "\"\"" + " " + ipfs_hash)
    txid = rpc_connection.transfer(asset, qty, address, ipfs_hash)
    return(txid)

def get_address():
    rpc_connection = get_rpc_connection()
    new_address = rpc_connection.getnewaddress()
    print("New address: " + new_address)
    return(new_address)


def generate_blocks(n):
    rpc_connection = get_rpc_connection()
    hashes = rpc_connection.generate(n)
    return(hashes)

def get_rpc_connection():
    from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
    connection = "http://%s:%s@127.0.0.1:%s"%(rpcuser, rpcpassword, rpc_port)
    print("Connection: " + connection)
    rpc_connection = AuthServiceProxy(connection)
    return(rpc_connection)

# def add_to_ipfs(file):
#     print("Adding to IPFS")
#     import ipfsapi
#     api = ipfsapi.connect('127.0.0.1', 5001)
#     res = api.add(file)
#     print(res)
#     return(res['Hash'])


if mode == "-regtest":  #If regtest then mine our own blocks
    import os
    os.system(cli + " " + mode + " generate 400")


with open(in_csv_file, "r") as csvfile:
    #print(rpc_call('getbestblockhash'))
    csvreader = csv.DictReader(csvfile)
    csvwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for trans in csvreader:
        txid = do_transfer(trans['asset'], trans['qty'], trans['address'], trans['ipfs'])
        print(txid + " " + trans['asset'] + trans['qty'] + " " + trans['address'])

