#!/usr/bin/env python3


import hashlib as hasher
import datetime as date


class Block:

    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hasher.sha256()
        sha.update(bytes(
            str(self.index) +
            str(self.timestamp) +
            str(self.data) +
            str(self.previous_hash), encoding='utf-8'))
        return sha.hexdigest()


def create_genesis_block():
    return Block(0, date.datetime.now(), "Genesis Block", "0")


def next_block(last_block: Block):
    index = last_block.index + 1
    timestamp = date.datetime.now()
    data = "Hey! I'm Block " + str(index)
    hash = last_block.hash
    return Block(index, timestamp, data, hash)


# Create the blockchain and add the genesis block
blockchain = [create_genesis_block()]
previous_block = blockchain[0]

num_of_blocks_to_add = 20

# Add blocks to the chain
for _ in range(0, num_of_blocks_to_add):
    block_to_add = next_block(previous_block)
    blockchain.append(block_to_add)
    previous_block = block_to_add
    # Tell every about it!
    print("Block #{} has been added to the blockchain!".format(block_to_add.index))
    print('Hash:{}\n'.format(block_to_add.hash))
