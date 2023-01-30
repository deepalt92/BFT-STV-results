const fs = require('fs')
const Wallet = require('ethereumjs-wallet')
const EthereumTx = require('ethereumjs-tx').Transaction
const Common = require('ethereumjs-common')
const w3 = require("web3")
const readline = require('readline')

// Sample params, can change to do with arguments
//const web3 = new w3(new w3.providers.HttpProvider("http://127.0.0.1:8545"))
const web3 = new w3(new w3.providers.WebsocketProvider("ws://127.0.0.1:8546"))
async function send(){
const NUMTX = 1
//const destinationAcccount = "0xBce16ea55bB357B038e612b1722A88879c665a31"
const startBalance = "0xfffc3b15f9926687d2c40534fdb564000000000000"
var abiArray = [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"","type":"uint256"}],"name":"invoke","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes[]","name":"","type":"bytes[]"}],"name":"notify","type":"event"},{"inputs":[{"internalType":"uint256","name":"votes","type":"uint256"},{"internalType":"uint256","name":"members","type":"uint256"}],"name":"addIp","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"chairperson","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes[]","name":"candidates","type":"bytes[]"}],"name":"createCommittee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"selected","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function"}] 
		
//[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes[]","name":"","type":"bytes[]"}],"name":"notify","type":"event"},{"inputs":[{"internalType":"bytes[]","name":"ip","type":"bytes[]"},{"internalType":"uint256","name":"members","type":"uint256"},{"internalType":"address[]","name":"wallets","type":"address[]"}],"name":"addIp","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"chairperson","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes[]","name":"candidates","type":"bytes[]"}],"name":"createCommittee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"selected","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function"}] 

//[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32[]","name":"","type":"bytes32[]"}],"name":"notify","type":"event"},{"inputs":[{"internalType":"bytes32[]","name":"ip","type":"bytes32[]"},{"internalType":"uint256","name":"members","type":"uint256"},{"internalType":"address[]","name":"wallets","type":"address[]"}],"name":"addIp","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"chairperson","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32[]","name":"candidates","type":"bytes32[]"}],"name":"createCommittee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"selected","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"}] 
 
//var CONTRACTDATA = '0x608060405234801561001057600080fd5b50610115806100206000396000f3006080604052600436106049576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff168063bcdfe0d514604e578063e21f37ce14607e575b600080fd5b348015605957600080fd5b50606060ae565b60405180826000191660001916815260200191505060405180910390f35b348015608957600080fd5b50609060e3565b60405180826000191660001916815260200191505060405180910390f35b60007f48656c6c6f20576f726c6400000000000000000000000000000000000000000060008160001916905550600054905090565b600054815600a165627a7a72305820b0a2937f6533d228be0d96647486f95ce839a6f35d9625a73696ae2b9d2dd58b0029'


let rawdata = fs.readFileSync('BFT-STV.json');
let data = JSON.parse(rawdata);
voters=[]
committeesize=0
wallets=[]	
/*for(let i=0; i<1000;i++){
        voters.push(web3.utils.asciiToHex(data["set500"][0][i]))
	//committeesize=data["set500"][1]
	committeesize=200
//	wallets.push(data["set500"][2][i])
}*/
//console.log(voters);
	
var address
var temp

    //console.log(contractAddress)
    var contractAddress='0x2D45727A40FDa2AC9Fa6460AA2abA9791000959B'
    var MyContract = new web3.eth.Contract(abiArray, contractAddress)
   //var DATA= await MyContract.methods.addIp([0x0000000000000000000000000000000000000000003139322e3136382e312e31, 0x0000000000000000000000000000000000000000003139322e3136382e312e32, 0x0000000000000000000000000000000000000000003139322e3136382e312e33, 0x0000000000000000000000000000000000000000003139322e3136382e312e34, 0x0000000000000000000000000000000000000000003139322e3136382e312e35, 0x0000000000000000000000000000000000000000003139322e3136382e312e36],4,["0x316b88ca91e9e6ae263ef1ed2392450c0b1b5b45", "0x194354333e6572cf185a7ea55e618d184dba673d", "0xb2db94d99562b32d18807d404cafb3bd8c94cfd0", "0x4abb2aaebe6e03186d8104156b57dbd115f4a4ac", "0xdcfb616a22ee4fd30bd56528c8e7fbc2ec40ffd2", "0xd6d2c16373644a35f12dca9cddc7956a077a50df"])
   

   var DATA= await MyContract.methods.addIp(1000, 200)
	
   var CONTRACTDATA = DATA.encodeABI()
   // });

let rawTransactions = []
let allocDict = {}

// helper function
let getGenesisTemplate = () => {
    return JSON.parse(fs.readFileSync('./genesis_template.json'))
}

const customCommon = Common.default.forCustomChain(
  'mainnet',
  {
    name: 'custom-benchmark-chain',
    networkId: 10,
    chainId: 161,
  },
  'petersburg'
)
//});
me=[]
const data1 = fs.readFileSync('new.log', 'UTF-8');
const lines1 = data1.split(/\r?\n/);
lines1.forEach((address) => {
        //console.log(address)
	me.push(address)
    });

//});
var privkey = fs.readFileSync('priv-keys.log').toString().split("\n");
//console.log(privkey[0])
console.log("[*] Generating " + NUMTX + " transactions and accounts")
//let genesisTemplate = getGenesisTemplate()
//let genTemplateCopy = {...genesisTemplate};
//var votes=[[0x0000000000000000000000000000000000000000003139322e3136382e312e32, 0x0000000000000000000000000000000000000000003139322e3136382e312e31, 0x0000000000000000000000000000000000000000003139322e3136382e312e34, 0x0000000000000000000000000000000000000000003139322e3136382e312e33, 0x0000000000000000000000000000000000000000003139322e3136382e312e35, 0x0000000000000000000000000000000000000000003139322e3136382e312e36], [0x0000000000000000000000000000000000000000003139322e3136382e312e31, 0x0000000000000000000000000000000000000000003139322e3136382e312e32, 0x0000000000000000000000000000000000000000003139322e3136382e312e33, 0x0000000000000000000000000000000000000000003139322e3136382e312e34, 0x0000000000000000000000000000000000000000003139322e3136382e312e35, 0x0000000000000000000000000000000000000000003139322e3136382e312e36], [0x0000000000000000000000000000000000000000003139322e3136382e312e32, 0x0000000000000000000000000000000000000000003139322e3136382e312e33, 0x0000000000000000000000000000000000000000003139322e3136382e312e34, 0x0000000000000000000000000000000000000000003139322e3136382e312e31, 0x0000000000000000000000000000000000000000003139322e3136382e312e35, 0x0000000000000000000000000000000000000000003139322e3136382e312e36], [0x0000000000000000000000000000000000000000003139322e3136382e312e36, 0x0000000000000000000000000000000000000000003139322e3136382e312e32, 0x0000000000000000000000000000000000000000003139322e3136382e312e33, 0x0000000000000000000000000000000000000000003139322e3136382e312e34, 0x0000000000000000000000000000000000000000003139322e3136382e312e35, 0x0000000000000000000000000000000000000000003139322e3136382e312e31], [0x0000000000000000000000000000000000000000003139322e3136382e312e31, 0x0000000000000000000000000000000000000000003139322e3136382e312e32, 0x0000000000000000000000000000000000000000003139322e3136382e312e33, 0x0000000000000000000000000000000000000000003139322e3136382e312e34, 0x0000000000000000000000000000000000000000003139322e3136382e312e35, 0x0000000000000000000000000000000000000000003139322e3136382e312e36]]
let gas = 0
for (let i = 0; i < NUMTX; i++) {
   //gas = gas + 0xff184e72a000;
   const txParams = {
  	nonce: '0x01',
  	gasPrice: '0x00',
  	gasLimit: '0xffff7100',
	to: '0x2D45727A40FDa2AC9Fa6460AA2abA9791000959B',
	data: CONTRACTDATA,
  	value: '0x0',
  	chainId: 161
	}

    let newTx = {...txParams}
    // addresses taken from new.log

    newTx["from"] = me[i] 

    // generate the transaction and sign it
    let tx = new EthereumTx(txParams, {common: customCommon})
    
    // sign using the private keys of the generated accounts (remove 0x from the priv key file)
    var privateKey = Buffer.from(privkey[i], 'hex')
    tx.sign(privateKey)

    rawTransactions.push(
      {
        'hash': tx.hash().toString('hex'),
        'serialized': (tx.serialize()).toString('hex')
      }
    )

    //update contract data to vote committee
   //DATA= await MyContract.methods.addIp(votes[i])
   //CONTRACTDATA = DATA.encodeABI()	
}

console.log('[*] Done!')


//console.log('[*] Done!')
console.log('[*] Generating Transaction file')

b = Buffer.from(JSON.stringify(rawTransactions))

try {
    fs.writeFileSync('txs-call.json', b)
} catch(error) {
    console.log(error);
}

console.log('[*] Done! Printing to stdout for sanity')

//console.log(JSON.stringify(genTemplateCopy, null, 4))
//console.log(JSON.stringify(rawTransactions, null, 2))
}
send();
