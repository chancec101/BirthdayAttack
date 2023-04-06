import hashlib
import random
import operator

'''Function to get the first 44 bits of SHA-256'''
def BadHash44(msg):
        
	msg = msg.encode()
	hashMsg = hashlib.sha256(msg).hexdigest()

	return hashMsg[0:11]

'''Function to find a hash collision'''
def find_collision():

    n = 256     # stores length of input message
    file = open("hash.csv", "w")    # file to store hash data

    x0 = random.getrandbits(n)  # generate random 256 bit value
    x0 = hex(x0)[2:]    # convert to hex

    # loop to make sure length of hex message is 265 bits
    while len(x0) != 64:
        x0 = "0" + x0
                
    x = x0
    x_prime = x

    hash_dict = {}  #dictionary to store hash data
    
    i = 0
    while i < 2**(n/2):

        #create hash chain and check if they match
        x = BadHash44(x)
        x_prime = BadHash44(BadHash44(x_prime))
        if x == x_prime:
            break

        i += 1
        
    x_prime = x
    x = x0
    
    for j in range(i):

        hash_dict[x] = BadHash44(x)
        hash_dict[x_prime] = BadHash44(x_prime)

        # if matching hash, collision found
        if BadHash44(x) == BadHash44(x_prime):
            
            print(f"x hash: {BadHash44(x)}")
            print(f"x prime hash: {BadHash44(x_prime)}")

            # sort hash data
            new_dict = sorted(hash_dict.items(), key=operator.itemgetter(1))
            new_dict = dict(new_dict)

            #write hashes to file 
            for key, value in new_dict.items():
                file.write(f"{key} -> {value}\n")


            file.close()

            return x, x_prime
        
        # update hash
        x = BadHash44(x)
        x_prime = BadHash44(x_prime)
    
    return None, None # No collision found

# Test the function
x, x_prime = find_collision()
if x is None:
    print("No collision found.")
else:
    print("Collision found:")
    print(f"x: {x}")
    print(f"x_prime: {x_prime}")
