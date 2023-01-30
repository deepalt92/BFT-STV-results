const fs = require('fs')
const web3 = require("web3")
let rawdata = fs.readFileSync('Votes.json');
let data = JSON.parse(rawdata);
vote= [];
votes=[];
for(let j=0; j<1000;j++){
	for(let i=0; i<1000;i++){
	//	votes.push(data[j])
		vote.push(web3.utils.asciiToHex(data[j][i]))
	}
	votes.push(vote)
	vote=[]
}


/*for(let j=0; j<1000;j++){
        for(let i=0; i<1000;i++){
                votes[j][i]=web3.utils.asciiToHex(votes[j][i])
                //votes[i].push(web3.utils.asciiToHex(data[0][i]))
        }
}*/
console.dir(votes[999], {'maxArrayLength': null})
//console.log(votes[0]);
