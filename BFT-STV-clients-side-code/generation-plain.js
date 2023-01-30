const fs = require('fs')
const Wallet = require('ethereumjs-wallet')
const EthereumTx = require('ethereumjs-tx').Transaction
const Common = require('ethereumjs-common')

// Sample params, can change to do with arguments

const NUMTX = 1
//const destinationAcccount = "0xBce16ea55bB357B038e612b1722A88879c665a31"
const startBalance = "0xfffc3b15f9926687d2c40534fdb564000000000000"
//var CONTRACTABI = eth.contract([{"constant":false,"inputs":[],"name":"Hello","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"message","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"}]);


// the allocation of the accounts and objects
let accounts = []
let rawTransactions = []
let allocDict = {}

// helper function
let getGenesisTemplate = () => {
    return JSON.parse(fs.readFileSync('./genesis_template.json'))
}

// Transaction things
//const txParams = {
  //nonce: '0x00',
  //gasPrice: '0xff184e72a000',
  //gasLimit: '0xfff7100',
  //to: "0xBce16ea55bB357B038e612b1722A88879c665a31",
  //value: '0x1',
  //chainId: 161
//}

const customCommon = Common.default.forCustomChain(
  'mainnet',
  {
    name: 'custom-benchmark-chain',
    networkId: 10,
    chainId: 161,
  },
  'petersburg'
)


console.log("[*] Generating " + NUMTX + " transactions")
//let genesisTemplate = getGenesisTemplate()
//let genTemplateCopy = {...genesisTemplate};
var privkey = fs.readFileSync('priv-keys.log').toString().split("\n");

me = []
const data1 = fs.readFileSync('new.log', 'UTF-8');
const lines1 = data1.split(/\r?\n/);
lines1.forEach((address) => {
        //console.log(address)
        me.push(address)
    });

let gas = 0
for (let i = 0; i < NUMTX; i++) {
    // generate the account and add to the array
    //let a = Wallet.default.generate()
    //accounts.push(a.getPrivateKeyString())

    // add to the genesis alloc
   //allocDict[a.getAddressString()] = startBalance
   //text = a.getAddressString() + "\n"
   //fs.appendFileSync('new.log', text);
   gas = gas + 0xff184e72a000;
   const txParams = {
        nonce: '0x01',
        gasPrice: gas,
        gasLimit: '0xffff7100',
        to: "0x97f22368eea8ca06031bc57fcd3d9169e687584e",
        value: '0x1',
        chainId: 161
   }

    let newTx = {...txParams}
   //read from address from file
    newTx["from"] = me[i]

    // generate the transaction and sign it
    let tx = new EthereumTx(txParams, {common: customCommon})
    var privateKey = Buffer.from(privkey[i], 'hex')
    tx.sign(privateKey)

    rawTransactions.push(
      {
        'hash': tx.hash().toString('hex'),
        'serialized': (tx.serialize()).toString('hex')
      }
    )
}

//console.log('[*] Done!')
//console.log('[*] Generating Genesis')

// write the genesis file
//let genesisTemplate = getGenesisTemplate()
//let genTemplateCopy = {...genesisTemplate};
//genTemplateCopy.alloc = {...allocDict}

//let b = Buffer.from(JSON.stringify(genTemplateCopy, null, 4))

//try {
    //fs.writeFileSync('genesis.json', b)
//} catch(error) {
    //console.log(error);
//}

console.log('[*] Done!')
console.log('[*] Generating Transaction file')

b = Buffer.from(JSON.stringify(rawTransactions))

try {
    fs.writeFileSync('txs-plain.json', b)
} catch(error) {
    console.log(error);
}

console.log('[*] Done! Printing to stdout for sanity')

//console.log(JSON.stringify(genTemplateCopy, null, 4))
console.log(JSON.stringify(rawTransactions, null, 2))

