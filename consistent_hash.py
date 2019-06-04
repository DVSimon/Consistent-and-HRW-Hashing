# place all into list, check if hash(key) > largest node hash, if it is then return
# the smallest hash server value server as the address, if not then find the smallest
# hash server value that is greater than the hash(key)!
#

import json
import sys
import requests
import csv_parser
import hashlib
import numpy as np


servers = ['http://127.0.0.1:5000','http://127.0.0.1:5001','http://127.0.0.1:5002','http://127.0.0.1:5003']
# ring = []

def populateRingServers():
    ring = {}
    for server in servers:
        serverHash = int(hashlib.sha1(server.encode('utf-8')).hexdigest(), 16)
        ring[server] = serverHash
    # ring.sort()
    return ring

def matchKeyNode(k, r):
    keyHash = int(hashlib.sha1(k.encode('utf-8')).hexdigest(), 16)
    if keyHash in r:
        return keyHash
    elif keyHash > max(r):
        hashedValue = min(r)
        return hashedValue
    else:
        hashedValue = r[r > keyHash].min()
        return hashedValue


def findServer(serverHash, serverDict):
    for address, servhash in serverDict.items():
        if serverHash == servhash:
            return address


def main():
    # populate ring with server hashes
    ring = populateRingServers()
    # print(ring)
    # creating sorted array to find smallest server hash value that is greater than hashed key
    ringArray = []
    for key, value in ring.items():
        ringArray.append(value)
    ringArray.sort()
    ringArray = np.array(ringArray)
    # print(ringArray)
    records = csv_parser.parse(sys.argv[1])
    recordnumber = 0

    for record in records:
        k = record[0] + ':' + record[2] + ':' + record[3]
        # for each record find corresponding server based on hash, returned server hash must be smallest
        # server hash that is greater than keyhash, if it is bigger then all then it should loop to smallest server hash
        serverHash = matchKeyNode(k, ringArray)
        # after finding this, search the dictionary for corresponding server address to post
        serverAddress = findServer(serverHash, ring)
        keyHash = hashlib.sha1(k.encode('utf-8')).hexdigest()
        url = serverAddress + '/api/v1/entries'
        value = ','.join(map(str, record))
        r = requests.post(url, json={keyHash: value})
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


if __name__ == "__main__":
    main()