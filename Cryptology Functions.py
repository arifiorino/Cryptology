printing=1
def Print(*args, sep=' ', end='\n'):
        if printing:
                print(sep.join([str(e) for e in args]), end=end)
#############################################################################
##########################*************************##########################
##########################**********BASES**********##########################
##########################*************************##########################
#############################################################################

def encodeBase(num, base=2, padding=8):
        r=''        
        for x in range(padding-1,-1,-1):
                a=0
                while base**x<=num:
                        a+=1
                        num-=base**x
                if a>9:
                        r+=chr(a-10+ord('A'))
                else:
                        r+=str(a)                
        return r
def decodeBase(string, base=2):
        n=0
        r=0
        for s in string[::-1]:
                if s.isalpha():
                        r+=(base**n)*(ord(s)+10-ord('A'))
                else:
                        r+=(base**n)*int(s)
                n+=1
        return r
def translateBase(num, base1=16, base2=2, padding=8):
	return encodeBase(decodeBase(num, base1), base2, padding)

Print(translateBase('FF'))

###############################################################################
##########################***************************##########################
##########################**********BASE 64**********##########################
##########################***************************##########################
###############################################################################

base64Table=list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/')
def encode64(string, padding=6):
        a=''
        for s in string:
                a+=encodeBase(ord(s))
        r=''
        for x in range(0,len(a),padding):
                r+=base64Table[decodeBase(a[x:x+padding])]
        return r
def decode64(string, padding1=6, padding2=8):
        a=''
        for s in string:
                a+=encodeBase(''.join(base64Table).find(s),2,padding1)
        r=''
        for x in range(0,len(a),padding2):
                r+=chr(decodeBase(a[x:x+padding2]))		
        return r

p='Vm0wd2QyUXlVWGxXYTFwT1ZsZG9WRmx0ZUV0WFJteFZVMjA1VjAxV2JETlhhMk0xVjBaS2MySkVUbGhoTWsweFZtcEdTMk15U2tWVWJHaG9UV3N3ZUZadGNFZFRNbEpJVm10c2FWSnRhRzlVVm1oRFZWWmFkR05GZEZSTlZUVkpWbTEwYTFkSFNrZGpTRUpYWVRGd2FGWkZSUQ'
while len(p)>5:
        p=decode64(p)
Print(p)
        
###########################################################################
##########################***********************##########################
##########################**********XOR**********##########################
##########################***********************##########################
###########################################################################


def XOR(num1, num2): #Inputs hex, then to binary, then 
        num1, num2=translateBase(num1), translateBase(num2)
        i=0
        b=''
        for i in range(min(len(num1),len(num1))):
                b+=str(int(num1[i]!=num2[i]))
        return translateBase(b, 2, 16, 2)

def encryptXOR(string, key): #Also functions as decryption
        r=''
        Print(string)
        for i in range(len(string)):
                char=encodeBase(ord(string[i]), 16, 2)
                keyChar=encodeBase(ord(key[i%len(key)]), 16, 2)
                r+=chr(decodeBase(XOR(char, keyChar),16))
#                Print(XOR(char, keyChar), end=" ")
        return r

p=encryptXOR("His palms are sweaty, knees weak, arms are heavy, there's vomit on his sweater already, mom's spaghetti.",'?')
encryptXOR('wVLO^SRL^MZLHZ^KFTQZZLHZ^T^MRL^MZWZ^IFKWZMZLIPRVKPQWVLLHZ^KZM^SMZ^[FRPRLLO^XWZKKV','?')

###################################################################################
##########################*******************************##########################
##########################**********MSSQL CRACK**********##########################
##########################*******************************##########################
###################################################################################

def MSSQLDecode(password):
        r=''
        for char in password.split(' '):
                c=XOR(char, 'A5')
                c=c[::-1]
                r+=chr(decodeBase(c, 16))
                
        return r
def MSSQLEncode(password):
        r=[]
        for char in password:
                c=encodeBase(ord(char), 16, 2)
                c=c[::-1]
                r.append(XOR(c, 'A5'))
        return ' '.join(r)
Print(MSSQLDecode('B1 93 E2 F6 C6 B6 11 F3 32 4D'))

##################################################################
##############**************************************##############
##############**********MAPPING DECRYPTION**********##############
##############**************************************##############
##################################################################

def findAll(string, substring):
        r=[]
        last=0
        while string[last:].find(substring)!=-1:
                r.append(last+string[last:].find(substring))
                last=r[-1]+1
        return r

def mappingDecrypt(encrypted, allStr):
        for startPos in range(len(allStr)-len(encrypted)+1): #iterate thru find string
                section=allStr[startPos:startPos+len(encrypted)+1]
                r=''
                finished=0
                for index in range(len(encrypted)):
                        if len(set([section[i] for i in findAll(encrypted, encrypted[index])]))>1:
                                finished=1
                                break
                        else:
                                r+=section[index]
                if not finished:
                        Print(r)
                        
