const fs = require('fs')
const web3 = require("web3")
let rawdata = fs.readFileSync('BFT-STV.json');
let data = JSON.parse(rawdata);
voters=[]
committeesize=0
wallets=[]
for(let i=0; i<1000;i++){
	voters.push(web3.utils.asciiToHex(data["set500"][0][i]))
	committeesize=data["set500"][1]
        wallets.push(data["set500"][2][i])
}
console.log(voters);
//console.log(committeesize);
//console.log(wallets);
