import json


# function to add to JSON
def write_json(data, filename='genesis.json'):
    with open(filename,'w') as f:
        json.dump(data, f, indent=4)

#def write_text(filename='new1.log'):
    #with open('new1.log', 'r+') as x:
        #for line in x:


with open('genesisd.json', 'r+') as json_file:
        data = json.load(json_file)

        temp = data["alloc"]
        with open('new.log', 'r+') as x:
            for line in x:
        # python object to be appended
                        #y = {"0x1111111":{"balance":"0x50505050"}}
                line = line.rstrip('\n')
                y = {line:{"balance":"0x446c3b15f9926687d2c40534fdb564000000000000"}}
                temp.update(y)


    # appending data to emp_details

write_json(data)
#print(json.dumps(temp, indent=4))

