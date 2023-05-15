# LatticeCrypto

## About
This project is an implementation of following paper-  
`https://ieeexplore.ieee.org/abstract/document/10078405`

It involves communication between laptop and Raspberry Pi for actuating the signature scheme as designed in above paper.
We use ubuntu OS for all algorithms involving key generation, signing, verfication etc.

## Setup Config.py (src)

- (N) number of IOT devices
- (f) degree of polynomial - power of 2
- (p) large prime number
- (K_min, K_max) range of positive integer < sqrt(p)


## How to Run

1. Generate Keys  
`python key_gen.py`  
Move keys0.json to keys.json at location of server directory.  
Move keys*i*.json, to the location of *$i^{th}$* client directory.

2. Run server on some PORT (eg. 8080)   
   `python server.py PORT`

3. Run client on the same PORT. Pass the IP_ADDRESS of Server as argument. Use ***127.0.0.1*** to test locally.  
   `python client.py PORT IP_ADDRESS`

4. Enter message at client terminal prompt.
