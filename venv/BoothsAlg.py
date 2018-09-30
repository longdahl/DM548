import numpy as np

def booths_alg(Q,M):
    real_result = Q*M
    bit_length = get_bit_representation(Q,M)
    twos_Q = to_twoscomplement(bit_length,Q)
    twos_M = to_twoscomplement(bit_length,M)
    A = "0"*bit_length
    Qneg1 = "0"
    count = bit_length
    print(" "*(bit_length//2) + "A" + " "*int((bit_length*1.2)) + "Q" + " "*int((bit_length*0.6)) + "Q-1" + " "*int((bit_length*0.6)) + "M")
    print(A + "  " + twos_Q + "  " + Qneg1 + "  " + twos_M + "  initial values")
    while(count >0):
        Q0 = twos_Q[bit_length-1:bit_length]
        if Qneg1 == Q0:
            pass
        elif Q0 == "0":
            A = twos_addition(A,twos_M)
            print(A + "  " + twos_Q + "  " + Qneg1 + "  " + twos_M + " A <- A+M")
        else:
            A = twos_subtract(A,twos_M)
            print(A + "  " + twos_Q + "  " + Qneg1 + "  " + twos_M + " A <- A-M")
        A, twos_Q, Qneg1 = arithmetic_shift(A, twos_Q, bit_length)
        count -=1
        print(A + "  " + twos_Q + "  " + Qneg1 + "  " + twos_M + " Shift. Count is " + str(count))
    r = A + twos_Q
    r_dec = to_decimal(r, bit_length*2)
    print("The result is: " +str(r_dec))
    return r_dec == real_result #return true or false for testing

#support methods

def to_twoscomplement(bits, value):
    if value < 0:
        value = ( 1<<bits ) + value
    formatstring = '{:0%ib}' % bits
    return formatstring.format(value)

def to_decimal(bin, bits):
        while len(bin) < bits:
            bin = "0" + bin
        if bin[0] == "0":
            return int(bin, 2)
        else:
            return -1 * (int(''.join('1' if x == '0' else '0' for x in bin), 2) + 1)


def get_bit_representation(Q,M):
    x = 0
    #find largest absolute value, if they are equal the positive number sets the max bit representation (due to less positive numbers in twos-comp)
    if abs(Q) == abs(M):
        if Q > M:
            x = Q
        else: #if they are equal the choice is irrelevant
            x = M
    elif abs(Q) > abs(M):
        x = Q
    else:
        x = M
    #find the shortest bit representation of the number
    k=2
    bit_length = 2
    while (k <= abs(x)):
        #if x < 0 and k==abs(x):
            #break
        k = k*2 #increasing k by a power of 2
        bit_length+=1
    return bit_length


def arithmetic_shift(A,twos_Q,bit_length):
    new_A = A[0] + A[0:bit_length-1]
    new_twos_Q = A[bit_length-1] + twos_Q[0:bit_length-1]
    new_Qneg1 = twos_Q[bit_length-1]

    return new_A,new_twos_Q,new_Qneg1

def flip_and_add1(M):
    tailzeros = 1
    newM = ""
    for c in M[::-1]:
        if c == "0" and tailzeros == 1:
            newM = c + newM
        elif c == "0" and tailzeros == 0:
            newM = "1" + newM
        elif c == "1":
            if tailzeros == 1:
                newM = c + newM
            else:
                newM = "0" + newM
            tailzeros = 0
    return newM

def twos_subtract(A,M):

    #flip to make negative
    #make int
    #add 1
    flipped_M = flip_and_add1(M)
    new_A = twos_addition(A,flipped_M)
    return new_A
def twos_addition(A,M):
    carry = 0
    new_A = ""
    for a,b in zip(A[::-1],M[::-1]):
        a = int(a)
        b = int(b)
        s = a+b+carry
        if (s % 2 == 1):
            new_A = "1" + new_A
            if s == 3:
                carry = 1
            else:
                carry = 0
        else:
            new_A = "0" + new_A
            if s == 0:
                carry = 0
            else:
                carry = 1
    return new_A


#booths_alg(3,7)

#test method

def test_booths_alg():
    for i in range(100):
        Q = int(np.random.randint(-100, 100, 1))
        M = int(np.random.randint(-100, 100, 1))
        if booths_alg(Q,M) == False:
            print("the alg fails with the values "+ str(Q) + " and " + str(M))
            break
    print("it works")

test_booths_alg()
