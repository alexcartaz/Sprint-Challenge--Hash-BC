import hashlib
import requests

import sys

from uuid import uuid4

from timeit import default_timer as timer

import datetime
import math
from random import randrange

def check_if_new_proof_on_chain(last_proof):
    r = requests.get(url=node + "/last_proof")
    data = r.json()
    print('***proof check****')
    print('last proof: ' + str(last_proof))
    print('data: ' + str(data))
    return data.get('proof') != last_proof

def proof_of_work(last_proof):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...999123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    """

    print("Searching for next proof")
    proof_counter = randrange(200) + 1
    proof = 0 + (1000000 * (proof_counter-1))
    startTime = datetime.datetime.now()
    while valid_proof(last_proof, proof) is False and valid_proof(last_proof, -proof) is False:
        proof += 1
        
        if proof >= proof_counter*1000000:
            proof_counter += 1
            didGetSolved = check_if_new_proof_on_chain(last_proof)
            currentTime = datetime.datetime.now()
            delta = math.floor(currentTime.timestamp() - startTime.timestamp())
            print("Elapsed: " + str(delta))
            if didGetSolved == True:
                print("Too slow: someone else solved")
                return proof
    endTime = datetime.datetime.now()
    finalTime = math.floor(endTime.timestamp() - startTime.timestamp())
    print("Proof found: " + str(proof))
    print("Time taken: " + str(finalTime))
    if valid_proof(last_proof, proof) is False:
        return -proof
    else:
        return proof


def valid_proof(last_proof, proof):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the last hash match the first six characters of the proof?

    IE:  last_hash: ...999123456, new hash 123456888...
    """
    last_proof_encode = f'{last_proof}'.encode()
    last_hash = hashlib.sha256(last_proof_encode).hexdigest()

    guess_proof_encode = f'{proof}'.encode()
    guess_hash = hashlib.sha256(guess_proof_encode).hexdigest()

    if last_hash[-6:] == guess_hash[:6]:
        print('last hash: ' + last_hash)
        print('guess hash: ' + guess_hash)

    return last_hash[-6:] == guess_hash[:6]


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-coin.herokuapp.com"

    coins_mined = 0

    # Load or create ID
    f = open("blockchain/my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()
    #'b4b7f11e8d7443c482ebbc2976e1219b'
    if len(id) == 0:
        f = open("blockchain/my_id.txt", "w")
        # Generate a globally unique ID
        id = str(uuid4()).replace('-', '')
        print("Created new ID: " + id)
        f.write(id)
        f.close()
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        data = r.json()
        new_proof = proof_of_work(data.get('proof'))

        post_data = {"proof": new_proof,
                     "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))
