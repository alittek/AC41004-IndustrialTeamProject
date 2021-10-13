import random
import string

def random_password():
    randpass = ''
    for i in range(6):
        randinteger = random.randint(97, 122) # generate random number for ASCII chart picking only letters
        lowerupper = random.randint (0, 1)
        randinteger = randinteger - 32 if lowerupper == 1 else randinteger # randomly choose lower or upper case letters
        randpass = (randpass) + (chr(randinteger)) # convert number to ASCii chart letter
    for i in range(2):
        randinteger = random.randint(33, 47)
        randpass += chr(randinteger) 
    return randpass
