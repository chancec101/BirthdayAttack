import hashlib
import random

def BadHash44(msg):
        
	msg = msg.encode()
	hashMsg = hashlib.sha256(msg).hexdigest()

	return hashMsg[0:11]

def find_collision():

    n = 256
    file = open("hash.csv", "w")

    x0 = random.getrandbits(n)
    x0 = hex(x0)[2:]

    while len(x0) != 64:
        x0 = "0" + x0
                
    x = x0
    x_prime = x
    
    i = 0
    while i < 2**(n/2):
        
        x = BadHash44(x)
        x_prime = BadHash44(BadHash44(x_prime))
        if x == x_prime:
            break

        i += 1
        
    x_prime = x
    x = x0
    
    for j in range(i):

        file.write(f"{x}, {BadHash44(x)}\n")
        file.write(f"{x_prime}, {BadHash44(x_prime)}\n")

        if BadHash42(x) == BadHash44(x_prime):
            
            print(f"x hash: {BadHash44(x)}")
            print(f"x prime hash: {BadHash44(x_prime)}")

            file.close()

            return x, x_prime
        
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
