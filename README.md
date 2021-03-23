# transferbulk
A python script to transfer assets to addresses based on a csv (exported from Google Sheets or Excel)

Expects:
```in.csv``` which is csv file with four fields (asset, qty, address, ipfs) 

Usage:
```
python3 transferbulk.py
OR
./transferbulk.py
```

Requirements:
* An active synced node on the same machine with ```rpcuser``` and ```rpcpassword``` in ```raven.conf``` matching the code.
* Sufficient RVN funds to make the transfers


## Testing
* Spin up a node (https://tronblack.medium.com/ravencoin-how-to-run-full-nodes-85f92d2ebc1a)
* Stop the node with ```raven-cli stop```
* Run the node as testnet with ```ravend -testnet -daemon```
* Let the testnet node sync.
* Get a new address with ```raven-cli -testnet getnewaddress```
* Send some testnet RVN to the new address.
* Send some issued tokens to the new address.
* Edit the Google sheet, and export as in.csv
* Copy the in.csv to the same folder as transferbulk
* Run ```./transferbulk.py```
* Check out.csv to see results of the bulk send.

