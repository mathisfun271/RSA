#Encryption engine
#function imports
from random import sample,randint,randrange, getrandbits
from math import gcd,log,floor,ceil
def is_prime(n, k=128):
    """ Test if a number is prime
        Args:
            n -- int -- the number to test
            k -- int -- the number of tests to do
        return True if n is prime
    """
    # Test if n is not even.
    # But care, 2 is prime !
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    # find r and s
    s = 0
    r = n - 1
    while r & 1 == 0:
        s += 1
        r //= 2
    # do k tests
    for _ in range(k):
        a = randrange(2, n - 1)
        x = pow(a, r, n)
        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                x = pow(x, 2, n)
                if x == 1:
                    return False
                j += 1
            if x != n - 1:
                return False
    return True


def generate_prime_candidate(length):
    """ Generate an odd integer randomly
        Args:
            length -- int -- the length of the number to generate, in bits
        return a integer
    """
    # generate random bits
    p = getrandbits(length)
    # apply a mask to set MSB and LSB to 1
    p |= (1 << length - 1) | 1
    return p


def generate_prime_number(length=1024):
    """ Generate a prime
        Args:
            length -- int -- length of the prime to generate, in          bits
        return a prime
    """
    p = 4
    # keep generating while the primality test fail
    while not is_prime(p, 128):
        p = generate_prime_candidate(length)
    return p




def egcd(a,b): #extended gcd function (not my own)
    if a == 0:
        return (b,0,1)
    else:
        g,y,x = egcd(b%a,a)
        return (g,x-(b//a)*y,y)

def modinv(a,m): #modular inverse function (not my own)
    g,x,y = egcd(a,m)
    if g!=1:
        raise Exception('modular inverse does not exist')
    else:
        return x%m

def modexp(b,e,m): #modular exponentation optimization (not my own)
    X = b
    E = e
    Y = 1
    while E > 0:
        if E % 2 == 0:
            X = (X * X) % m
            E = E//2
        else:
            Y = (X * Y) % m
            E = E - 1
    return Y

b64char= {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25, 'A': 26, 'B': 27, 'C': 28, 'D': 29, 'E': 30, 'F': 31, 'G': 32, 'H': 33, 'I': 34, 'J': 35, 'K': 36, 'L': 37, 'M': 38, 'N': 39, 'O': 40, 'P': 41, 'Q': 42, 'R': 43, 'S': 44, 'T': 45, 'U': 46, 'V': 47, 'W': 48, 'X': 49, 'Y': 50, 'Z': 51, '0': 52, '1': 53, '2': 54, '3': 55, '4': 56, '5': 57, '6': 58, '7': 59, '8': 60, '9': 61, '@': 62, '+': 63}
b64num = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i', 9: 'j', 10: 'k', 11: 'l', 12: 'm', 13: 'n', 14: 'o', 15: 'p', 16: 'q', 17: 'r', 18: 's', 19: 't', 20: 'u', 21: 'v', 22: 'w', 23: 'x', 24: 'y', 25: 'z', 26: 'A', 27: 'B', 28: 'C', 29: 'D', 30: 'E', 31: 'F', 32: 'G', 33: 'H', 34: 'I', 35: 'J', 36: 'K', 37: 'L', 38: 'M', 39: 'N', 40: 'O', 41: 'P', 42: 'Q', 43: 'R', 44: 'S', 45: 'T', 46: 'U', 47: 'V', 48: 'W', 49: 'X', 50: 'Y', 51: 'Z', 52: '0', 53: '1', 54: '2', 55: '3', 56: '4', 57: '5', 58: '6', 59: '7', 60: '8', 61: '9', 62: '@', 63: '+'}

def numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]

def decToB64(dec):
    ret = ''
    if dec == 0:
        return 'a'
    while dec:
        ret+=b64num[int(dec % 64)]
        dec //= 64  
    return ret[::-1]

def b64ToDec(b64):
    ret = 0
    for n,el in enumerate(b64[::-1]):
        ret += b64char[el]*64**n
    return ret


print('How long would you like the keys, in bits? Recomended at least 300, typical secure RCA encryption is 1024+. They will be displayed in base 64.')
keyLen = int(input('Length: '))
if keyLen<80:
    raise Exception('Key must be at least 80 bits')

print('Generating Primes...')
p = generate_prime_number(floor(keyLen/2)+16)
q = generate_prime_number(ceil(keyLen/2)-16)

n=p*q#n is the product of the two primes.
ct = (p-1)*(q-1)//gcd(p-1,q-1) #Carmichael's totient function. In this case, it is lcm(p-1,q-1) 


e = 65537 #This number is commonly used for e.
#in the case e and ct are not coprime, compute new p,q.
if gcd(e,ct)!=1:
    raise Exception('e and ct not coprime')

print('Public Key: (%s,%s)' % (decToB64(n),decToB64(e)))#Prints public key
print('Private key: %s' % decToB64(modinv(e,ct)))#d is the modular inverse of e in mod ct. (printed in hex)
#only public keys saved as variables

ct,p,q=None,None,None
#Voids p,q, and ct for security purposes, they can no longer be used. 


#Graph theory based codes for all lowercase letters, space and period
#Given based on the relative frequency of each character in normal English
#bins and char are simply inverses.
bins = {' ': '00', 'e': '0100', 't': '0101', 'a': '0110', 'r': '0111', 'i': '1000', 'o': '1001', 'n': '1010', 's': '10110', 'h': '10111', 'd': '11000', 'l': '11001', 'u': '11010', 'w': '110110', 'm': '110111', 'f': '111000', 'c': '111001', 'g': '111010', 'y': '111011', 'p': '111100', '.': '111101', 'b': '1111100', 'k': '1111101', 'v': '11111100', 'j': '11111101', 'x': '11111110', 'q': '111111110', 'z': '111111111'}
char = {'00': ' ', '0100': 'e', '0101': 't', '0110': 'a', '0111': 'r', '1000': 'i', '1001': 'o', '1010': 'n', '10110': 's', '10111': 'h', '11000': 'd', '11001': 'l', '11010': 'u', '110110': 'w', '110111': 'm', '111000': 'f', '111001': 'c', '111010': 'g', '111011': 'y', '111100': 'p', '111101': '.', '1111100': 'b', '1111101': 'k', '11111100': 'v', '11111101': 'j', '11111110': 'x', '111111110': 'q', '111111111': 'z'}

#Max encryption length (n). When it is reached, a new element will begin.
#-1 to compensate for a leading one to distingish leading zeros
#Without this, say " i" (001000) and  "i" (1000) both represent 8.
#Adding a leading 1 makes them 72 (1001000) and 24 (11000) respectively
maxenc = floor(log(n)/log(2))-1

def txtToNum(s):#converts plaintext to raw binary string
    s = s.lower()#Remove capitol letters
    ret = ''
    for el in s:
        try:
            ret+=bins[el]#adds binary digits for each character
        except:1#does nothing if charater isn't in library
    return ret

def numToTxt(bi):#converts raw binary string to plaintext
    pos = 0
    ret = ''
    for x in range(0,len(bi)+1):
        try:#attemts to add charater from library.
            ret += char[bi[pos:x]]
            pos = x#resets index
        except:1#moves on if none found
    ret2 = ''
    k = 1
    for rChar in ret:#Capitalizes first string and character 2nd after period
        if k==1:
            ret2+=rChar.upper()
        else:
            ret2+=rChar
        if rChar=='.':
            k=2
        elif k>0:
            k-=1
    return ret2

def maxencMessage():#gives a message on the max encryption length for one section.
    print('About %s characters on average' % round(log(n)/log(2)/4.2963157894736845))

def encrypt(m):#Encrypts text. Public keys not needed, saved as variables
    if type(m) == str:#splits into sections less than the max single encryption length.
        rawbin = txtToNum(m) #raw binary
        numAr = []
        for x in range(0,ceil(len(rawbin)/maxenc)):
            numAr.append(int('1'+rawbin[maxenc*x:maxenc*(x+1)],2))#adds leading 1
    elif type(m) == int:#Works with raw integers too.
        numAr = [m]
    ret = []
    for el in numAr:
        if el>=n:#Checks if too large (automatically avoided if string imput)
            raise Exception('Encoding material too large')
        ret.append(decToB64(modexp(el,e,n)))#adds el^e mod n to return list for each section
    return '&'.join(ret)

def decrypt(c,privKey):
    if type(privKey) == str:
        privKey = b64ToDec(privKey)
    if type(c) == str:
        c = c.split('&')
        for x in range(0,len(c)):
            c[x]= b64ToDec(c[x])
    rawbin = ''
    for el in c:
       rawbin += format(modexp(el,privKey,n),'b')[1:]
       #Formats el^d mod n to binary, then removes the leading one for each section.
    return numToTxt(rawbin)#converts back to text










