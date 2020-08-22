#Encryption engine

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


primes = []#Insert your own. Primes used by me not included for security.

#function imports
from random import sample,randint
from math import gcd,log,floor,ceil

[p,q]=sample(set(primes), 2)# Selects p and q as to random primes from given list.

n=p*q#n is the product of the two primes.
ct = (p-1)*(q-1)//gcd(p-1,q-1) #Carmichael's totient function. In this case, it is lcm(p-1,q-1) 


e = 65537 #This number is commonly used for e.
#in the case e and ct are not coprime, compute new p,q.
if gcd(e,ct)!=1:
    raise Exception('e and ct not coprime')

print('Public Key: (%s,%s)' % (n,e))#Prints public key
print('Private key: %s' % hex(modinv(e,ct)))#d is the modular inverse of e in mod ct. (printed in hex)
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
        ret.append(modexp(el,e,n))#adds el^e mod n to return list for each section
    return ret

def decrypt(c):
    rawbin = ''
    for el in c:
       rawbin += format(modexp(el,d,n),'b')[1:]
       #Formats el^d mod n to binary, then removes the leading one for each section.
    return numToTxt(rawbin)#converts back to text










