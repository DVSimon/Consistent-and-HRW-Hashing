import sys
import requests
import csv_parser
import hashlib
import json

servers = ['http://127.0.0.1:5000','http://127.0.0.1:5001','http://127.0.0.1:5002','http://127.0.0.1:5003']


def main():
    records = csv_parser.parse(sys.argv[1])
    recordnumber = 0
    for record in records:
        k = record[0] + ':' + record[2] + ':' + record[3]
        serverchoice = getServer(k)
        key = hashlib.sha1(k.encode('utf-8')).hexdigest()
        url = serverchoice + '/api/v1/entries'
        value = ','.join(map(str, record))
        r = requests.post(url, json={key: value})
        recordnumber += 1
    print('Uploaded all ' + str(recordnumber) + ' entries.')
    print('Verifying the data.')
    for server in servers:
        print('GET ' + server)
        print('{')
        serverurl = server + '/api/v1/entries'
        r = requests.get(serverurl)
        print(json.dumps(json.loads(r.text), indent=3))
        print('}\n')
    print('Finished.')

def getServer(key):
    serverlist = {}
    for server in servers:
        ks = key + server
        keynode = ks.encode('utf-8')
        weight = int(hashlib.sha1(keynode).hexdigest(), 16)
        serverlist[server] = weight
    largestweightserver = max(serverlist, key=serverlist.get)
    return largestweightserver



if __name__ == "__main__":
    main()