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
const NUMTX = 501
//const destinationAcccount = "0xBce16ea55bB357B038e612b1722A88879c665a31"
const startBalance = "0xfffc3b15f9926687d2c40534fdb564000000000000"
var abiArray = [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes[]","name":"","type":"bytes[]"}],"name":"notify","type":"event"},{"inputs":[{"internalType":"bytes[]","name":"ip","type":"bytes[]"},{"internalType":"uint256","name":"members","type":"uint256"},{"internalType":"address[]","name":"wallets","type":"address[]"}],"name":"addIp","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"chairperson","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes[]","name":"candidates","type":"bytes[]"}],"name":"createCommittee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"selected","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function"}] 

//[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32[]","name":"","type":"bytes32[]"}],"name":"notify","type":"event"},{"inputs":[{"internalType":"bytes32[]","name":"ip","type":"bytes32[]"},{"internalType":"uint256","name":"members","type":"uint256"},{"internalType":"address[]","name":"wallets","type":"address[]"}],"name":"addIp","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"chairperson","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32[]","name":"candidates","type":"bytes32[]"}],"name":"createCommittee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"selected","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"}] 
 
//var CONTRACTDATA = '0x608060405234801561001057600080fd5b50610115806100206000396000f3006080604052600436106049576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff168063bcdfe0d514604e578063e21f37ce14607e575b600080fd5b348015605957600080fd5b50606060ae565b60405180826000191660001916815260200191505060405180910390f35b348015608957600080fd5b50609060e3565b60405180826000191660001916815260200191505060405180910390f35b60007f48656c6c6f20576f726c6400000000000000000000000000000000000000000060008160001916905550600054905090565b600054815600a165627a7a72305820b0a2937f6533d228be0d96647486f95ce839a6f35d9625a73696ae2b9d2dd58b0029'


let rawdata = fs.readFileSync('Votes.json');
let data = JSON.parse(rawdata);
vote= [];
votes=[];
for(let j=0; j<500;j++){
        for(let i=0; i<500;i++){
        //      votes.push(data[j])
                vote.push(web3.utils.asciiToHex(data[j][i]))
        }
        votes.push(vote)
        vote=[]
}


/*for(let j=0; j<10;j++){
        for(let i=0; i<10;i++){
        //      votes.push(data[j])
                vote.push(web3.utils.asciiToHex(data[j][i]))
        }
        votes.push(vote)
        vote=[]
}*/	
//console.log(voters);
	
var address
var temp

    //console.log(contractAddress)
var contractAddress='0x2D45727A40FDa2AC9Fa6460AA2abA9791000959B'
var MyContract = new web3.eth.Contract(abiArray, contractAddress)

contractDatas=[]
for(let k=0; k<500;k++){
   //var DATA= await MyContract.methods.addIp(voters, committeesize, wallets)
   var DATA = await MyContract.methods.createCommittee(votes[k])	
   var CONTRACTDATA = DATA.encodeABI()
   contractDatas.push(CONTRACTDATA)
}

//var DATA = await MyContract.methods.createCommittee(['0x3139322e3136382e322e313135', '0x3139322e3136382e322e313839', '0x3139322e3136382e342e3436', '0x3139322e3136382e322e3830', '0x3139322e3136382e312e323534', '0x3139322e3136382e312e313630', '0x3139322e3136382e322e313536', '0x3139322e3136382e332e3430', '0x3139322e3136382e342e313030', '0x3139322e3136382e332e313439', '0x3139322e3136382e332e3634'])
//var CONTRACTDATA = DATA.encodeABI()
//console.log("reached here");
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
let gas = 0
for (let i = 1; i < NUMTX; i++) {
   gas = gas + 0xff184e72a;
   const txParams = {
  	nonce: '0x00',
  	gasPrice: gas,
  	gasLimit: '0xffffffffff',
	to: '0x2D45727A40FDa2AC9Fa6460AA2abA9791000959B',
	data: contractDatas[i],
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
    fs.writeFileSync('txs-vote.json', b)
} catch(error) {
    console.log(error);
}

console.log('[*] Done! Printing to stdout for sanity')

//console.log(JSON.stringify(genTemplateCopy, null, 4))
//console.log(JSON.stringify(rawTransactions, null, 2))
}
send();
