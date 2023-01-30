pragma solidity ^0.8.13;
pragma experimental ABIEncoderV2;

contract Committee {
   
//     bytes [] committee;
     address public chairperson;
     //mapping(uint => uint) private id;
     mapping(bytes => bool) hasIp;
     mapping(bytes => bool) hasCalled;
     mapping(address => bytes) WallettoIP;
     //changed here
     mapping(uint => bytes []) ballots; //mapping between ballot number and the vote transferrable to the next round
     mapping(bytes => uint) votes;
     mapping(bytes32 => uint) rest;
     mapping(uint => uint) ballot_index;
     bytes [] public selected;
     bytes [] surplus_current;
     uint32 [] private digits;
     bytes32 [] hashes;
     uint member;
     mapping(bytes => uint) transfer_vote;
     //mapping(string => uint) deficit_current;
     mapping(bytes => uint) tot_surplus;
     mapping(uint => uint) indexers;
     uint c_ballot;
     uint threshold;
     uint size;
     uint select;
     uint transfer;
     uint k;
     uint rest_tot;
     uint quota;
     uint min;
     uint eliminatedcount;
     /*uint vote_s1;
     uint vote_s2;
     uint vote_s3;
     uint vote_s4;
     */
     bytes [] gcandidates;
     uint round;
     uint partition;
     uint numVotes;
     bool val;
     bool excess;
     bool eliminated;
     bool elect;
     mapping(bytes => bool) elected;
     event notify(bytes []);
     event invoke(uint);
     constructor() {
     
      chairperson = msg.sender;
      c_ballot = 0;
      numVotes = 0;
      
     }
      //max number of voters and the expected size of the committe is parsed
     function addIp (uint votes, uint members) public {
        //delete committee;
         require(
            msg.sender == chairperson,
            "Only chairperson can give right to vote."
        );
        
        size = votes; //1000
        
        member = members/4; //200/4=50
        partition = size/4; //1000/4=250
        size=size/8; //125
 
        threshold = partition - (partition - 1)/3; //1
        emit invoke(threshold);
        quota=(threshold/(member+1))+1;
        //members is the number of participants per committee
       
     }
  
     //create committee - each partition of voters vote on a disjoint set of candidates

     function createCommittee(bytes [] calldata candidates) public {
         
         for(uint i=0; i<candidates.length; i++){
                ballots[c_ballot].push(candidates[i]);
                votes[candidates[i]]=0;
                transfer_vote[candidates[i]]=0;
                elected[candidates[i]]=false;
               
         }
         //
        if(ballots[c_ballot].length !=0){
          c_ballot=c_ballot + 1;
        }

         if(c_ballot == threshold){
             //start doing stv
             for(uint a=0; a<c_ballot; a++){
                ballot_index[a]=0;
             }
             round = 0;
             eliminatedcount=0;
             //first preference vote calculation
             for (uint a = 0; a<c_ballot; a++){
                    votes[ballots[a][round]]=votes[ballots[a][round]]+1;
            }
             
             //do until the number of seats-members is filled - error happens in this loop
            while((selected.length < member) && round<size){
                 
                 //loop through ballot and count votes
                elect = false;
                excess = false;
                eliminated = false;
                //////////////////////////////add changes from here/////  
                val=next_pref();
                  if(val==true){
                      elect = true;
                  }

                //require(round < 0, "Reverting after first while loop");  
                if(elect == false){
                   //remove least voted
                   min = 100000;
                   //minimum vote of all candidates (non elected) is eliminated
                   for (uint a = 0; a<c_ballot; a++){
                     for(uint x=ballot_index[c_ballot]; x<size; x++){
                       if((votes[ballots[a][x]] < min) && !elected[ballots[a][x]]){
                           min = votes[ballots[a][x]];
                       }
                     }
                    }
                    eliminate();
                }


                if((size-eliminatedcount)==member){
                    break;
                }

                round = round + 1;
             }             
             ////////////////////////to add the remainder of members///////
               min = minimum();
              while((size-eliminatedcount) >member){
              for (uint a = 0; a<c_ballot; a++){
                   for(uint x=0; x<size; x++){
                    if(votes[ballots[a][x]]==min && (size-eliminatedcount) >member && votes[ballots[a][x]]!=10000000){
                            votes[ballots[a][x]]=10000000;
                            eliminatedcount=eliminatedcount+1;
                            min = minimum();
                    }
                   }
               }
              }
                //assign already non elected and non eliminated candidates to the seats and exit the loop.
                if((size - eliminatedcount) == member){
                    for(uint a = 0; a<c_ballot; a++){
                        for(uint x=0; x<size; x++){
                            if(votes[ballots[a][x]]!=10000000 && !elected[ballots[a][x]] && (selected.length)<member){
                                selected.push(ballots[a][x]);
                                elected[ballots[a][x]]=true;
                            }
                        }
                    }
                }
             //if the committee member is elected in selected don't use him again//
            emit notify(selected);
            
            //resetting values for the next election
            for(uint it=0; it<c_ballot; it++){

                for(uint r; r<ballots[it].length; r++){
                        votes[ballots[it][r]]=0;
                        transfer_vote[ballots[it][r]]=0;
                        //elected[ballots[it][r]] = false;   
                }

                 ballot_index[it]=0;
                delete ballots[it];
            }

            delete selected;
            eliminatedcount =0;
            round = 0;
            c_ballot=0;
            elect = false;
            excess = false;
            eliminated = false;
         }
 
         
     }

function minimum() private returns (uint mins){
    mins = 100000;
                   //minimum vote of all candidates is eliminated
               for (uint a = 0; a<c_ballot; a++){
                    for(uint x=0; x<size; x++){
                       if((votes[ballots[a][x]] < mins) && !elected[ballots[a][x]]){
                           mins = votes[ballots[a][x]];
                       }
                    }
                }
    return mins;
}
function next_pref() private returns (bool elec){

    for(uint it=0; it<c_ballot; it++){

        for(uint r; r<ballots[it].length; r++){
          
            transfer_vote[ballots[it][r]]=0;
            tot_surplus[ballots[it][r]]=0;   
        }

    }
   
    for(uint s=0; s<hashes.length; s++){
            rest[hashes[s]] = 0;
    }
    //surplus_current.length=0;
    delete surplus_current;
    elect=false;
    excess=false;
    //require(round < 0, "Reverting after first while loop");
    if(selected.length < member){
   
    for(uint s=0; s<c_ballot; s++){
        for(uint x=ballot_index[s]; x<size; x++){
            if(votes[ballots[s][x]]>=quota && votes[ballots[s][x]]!=10000000 && elected[ballots[s][x]] == false){
                  elected[ballots[s][x]] = true;
                  selected.push(ballots[s][x]);
                  elect = true;
                  transfer = votes[ballots[s][x]] - quota;
                  votes[ballots[s][x]]=quota;
                  transfer_vote[ballots[s][x]] = transfer;
                        //current preference that yield the surplus vote -
                        //keep tabs of the current round and the surplus candidate (current pref -> surplus candidate)
                   surplus_current.push(ballots[s][x]);
                   ballot_index[c_ballot]=x;
                   excess = true;

            }
           
        }
    }
   
     
    if(excess){
    //break the surplus ballots to those that have the same surplus elected candidate
    for(uint a=0; a< c_ballot; a++){
       indexers[a]=7000;
   }
     for(uint j=0; j<c_ballot; j++){
        for(k=0; k<surplus_current.length; k++){
            if(keccak256(abi.encodePacked(ballots[j][ballot_index[j]]))==keccak256(abi.encodePacked(surplus_current[k]))){
                tot_surplus[ballots[j][ballot_index[j]]] = tot_surplus[ballots[j][ballot_index[j]]] + 1;
                uint x = 1;
                if((ballot_index[j]+x)<(size -1)){
                while((elected[ballots[j][ballot_index[j]+x]] || votes[ballots[j][ballot_index[j]+x]]==10000000) && (ballot_index[j]+x)<(size -2)){
                    x = x + 1;
                }
               
                if(!elected[ballots[j][ballot_index[j]+x]] && (ballot_index[j]+x)<size){
                    rest[keccak256(abi.encodePacked(ballots[j][ballot_index[j]],ballots[j][ballot_index[j]+x]))] = rest[keccak256(abi.encodePacked(ballots[j][ballot_index[j]],ballots[j][ballot_index[j]+x]))] + 1;
                    hashes.push(keccak256(abi.encodePacked(ballots[j][ballot_index[j]],ballots[j][ballot_index[j]+x])));
                    //mapping for ballot number => current indexer
                    indexers[j]=ballot_index[j]+x;
                   
                }
                }
                    //ballot_index[c_ballot]=ballot_index[c_ballot]+x;
            }
        }
    }
 
               
    //divide and add the transfered votes
    for(uint j=0; j< c_ballot; j ++){
        for(uint x=1; x<(size-1); x++){

            if((ballot_index[j]+x) < size && rest[keccak256(abi.encodePacked(ballots[j][ballot_index[j]],ballots[j][ballot_index[j]+x]))] != 0 && !elected[ballots[j][ballot_index[j]+x]] && tot_surplus[ballots[j][ballot_index[j]]]!=0 && votes[ballots[j][ballot_index[j]]]!=10000000 && votes[ballots[j][ballot_index[j]+x]]!=10000000){
 
                votes[ballots[j][ballot_index[j]+x]] = votes[ballots[j][ballot_index[j]+x]] + transfer_vote[ballots[j][ballot_index[j]]]*rest[keccak256(abi.encodePacked(ballots[j][ballot_index[j]],ballots[j][ballot_index[j]+x]))]/tot_surplus[ballots[j][ballot_index[j]]];

                //next_pref(ballots[j][r+x],next_round,votes[ballots[j][r+x]]);
                rest[keccak256(abi.encodePacked(ballots[j][ballot_index[j]],ballots[j][ballot_index[j]+x]))] = 0;
        
            }
        }
    }
   //////////////////////////
   //moving the indexer to next
   for(uint a=0; a< c_ballot; a++){
       if(indexers[a]!=7000){
           ballot_index[a]=indexers[a];
       }
   }
  //////////////////////////
    }
   
    }
    return elect;
}

function eliminate() private {
uint x;
for(uint s=0; s<hashes.length; s++){
    rest[hashes[s]] = 0;
}
for (uint a = 0; a<c_ballot; a++){
    for(uint m=ballot_index[a]; m<size; m++){
        if(votes[ballots[a][m]] == min && !elected[ballots[a][m]] && votes[ballots[a][m]] != 10000000 && !eliminated){
            //if 0 just eliminate
            if(votes[ballots[a][m]] == 0){
                votes[ballots[a][m]] = 10000000;
                eliminated=true;
                eliminatedcount=eliminatedcount+1;
                //if it is the current index being eliminated
                 x=1;
                if((m == ballot_index[a]) && (m<size-1)){
                    while((elected[ballots[a][m+x]] || votes[ballots[a][m+x]]==10000000) && (m+x)<(size -1)){
                        x=x+1;
                    }
                    if(!elected[ballots[a][m+x]] && votes[ballots[a][m+x]]!=10000000){
                        ballot_index[a]=m+x;
                    }
                }
                break;
            }
            //////////////////////////otherwise/////////////
            x = 1;
           if(m<(size-1)){
              while((elected[ballots[a][m+x]] || votes[ballots[a][m+x]]==10000000) && (m+x)<(size -1)){
                 x = x + 1;
              }
              if(!elected[ballots[a][m+x]] && (m+x)<size){
                 rest[keccak256(abi.encodePacked(ballots[a][m],ballots[a][m+x]))] = rest[keccak256(abi.encodePacked(ballots[a][m],ballots[a][m+x]))] + 1;
                 hashes.push(keccak256(abi.encodePacked(ballots[a][m],ballots[a][m+x])));
              }
           }
        }
    }
}
//transfer to the next preferences
for(uint a = 0; a<c_ballot; a++){
    x=0;
    //uint next_r;                
    while(x<(size-1) && !eliminated){
        if(rest[keccak256(abi.encodePacked(ballots[a][x],ballots[a][x+1]))] != 0 && votes[ballots[a][x]]!=10000000 && votes[ballots[a][x+1]]!=10000000 && !elected[ballots[a][x]]){
            if(votes[ballots[a][x]]!=0){
            votes[ballots[a][x+1]] = votes[ballots[a][x+1]] + min*rest[keccak256(abi.encodePacked(ballots[a][x],ballots[a][x+1]))]/(votes[ballots[a][x]]);
            //next_r=x+1;
            //next_pref(ballots[a][x+1],next_r,votes[ballots[a][x+1]]);
            ballot_index[a]=x+1;
            }
            rest[keccak256(abi.encodePacked(ballots[a][x],ballots[a][x+1]))] = 0;
            votes[ballots[a][x]] = 10000000;
            eliminatedcount=eliminatedcount+1;
            eliminated = true;
        }
        x=x+1;
    }
}
}
}
