from math import floor,log,ceil

n=int(input('n value (normally first): '))
try:
    e=int(input('e value (normally 2nd). Leave blank for default, 65537: '))
except:
    e=65537

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

bins = {' ': '00', 'e': '0100', 't': '0101', 'a': '0110', 'r': '0111', 'i': '1000', 'o': '1001', 'n': '1010', 's': '10110', 'h': '10111', 'd': '11000', 'l': '11001', 'u': '11010', 'w': '110110', 'm': '110111', 'f': '111000', 'c': '111001', 'g': '111010', 'y': '111011', 'p': '111100', '.': '111101', 'b': '1111100', 'k': '1111101', 'v': '11111100', 'j': '11111101', 'x': '11111110', 'q': '111111110', 'z': '111111111'}


def txtToNum(s):#converts plaintext to raw binary string
    s = s.lower()#Remove capitol letters
    ret = ''
    for el in s:
        try:
            ret+=bins[el]#adds binary digits for each character
        except:1#does nothing if charater isn't in library
    return ret

maxenc = floor(log(n)/log(2))-1
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

m = input('Text to encrypt: ')
print(encrypt(m))
