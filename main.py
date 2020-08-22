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


primes = [18532395500947174450709383384936679868383424444311405679463280782405796233163977, 39688644836832882526173831577536117815818454437810437210221644553381995813014959, 44822481511601066098713481453161748979849764719554039096395688045048053310178487, 54875133386847519273109693154204970395475080920935355580245252923343305939004903, 40979218404449071854385509743772465043384063785613460568705289173181846900181503, 56181069873486948735852120493417527485226565150317825065106074926567306630125961, 19469495355310348270990592580191998639221450743640952620236903851789700309402857, 34263233064835421125264776608163440537925705997962346596977803462033841059628723, 14759984361802021245410475928101669395348791811705709117374129427051861355011151, 67120333368520272532940669112228025474970578938046280618394371551488988323794243, 282755483533707287054752184321121345766861480697448703443857012153264407439766013042402571, 370332600450952648802345609908335058273399487356359263038584017827194636172568988257769601, 463199005416013829210323411514132845972525641604435693287586851332821637442813833942427923, 374413471625854958269706803072259202131399386829497836277471117216044734280924224462969371, 664869143773196608462001772779382650311673568542237852546715913135688434614731717844868261, 309133826845331278722882330592890120369379620942948199356542318795450228858357445635314757, 976522637021306403150551933319006137720124048624544172072735055780411834104862667155922841, 635752334942676003169313626814655695963315290125751655287486460091602385142405742365191277, 625161793954624746211679299331621567931369768944205635791355694727774487677706013842058779, 204005728266090048777253207241416669051476369216501266754813821619984472224780876488344279, 2074722246773485207821695222107608587480996474721117292752992589912196684750549658310084416732550077, 2367495770217142995264827948666809233066409497699870112003149352380375124855230068487109373226251983, 1814159566819970307982681716822107016038920170504391457462563485198126916735167260215619523429714031, 5371393606024775251256550436773565977406724269152942136415762782810562554131599074907426010737503501, 6513516734600035718300327211250928237178281758494417357560086828416863929270451437126021949850746381, 5628290459057877291809182450381238927697314822133923421169378062922140081498734424133112032854812293, 2908511952812557872434704820397229928450530253990158990550731991011846571635621025786879881561814989, 2193992993218604310884461864618001945131790925282531768679169054389241527895222169476723691605898517, 5202642720986189087034837832337828472969800910926501361967872059486045713145450116712488685004691423, 7212610147295474909544523785043492409969382148186765460082500085393519556525921455588705423020751421]

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










