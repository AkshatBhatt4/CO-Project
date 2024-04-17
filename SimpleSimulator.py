import sys
import os

#Functions for Numbers
def decimaltobinary_32(num):
    num=int(num)
    if num >= 0:
        a = num
        s = ""
        while a != 0:
            b = a%2
            s = s + str(b)
            a = a//2
        s = s[::-1]
        filler = 32 - len(s)
        if filler <= 0:
            #print("number out of Range")
            s='-1'
            return s
        s = filler*"0" + s
        return s
    else:
        z = abs(num)
        s = ""
        cnt = 1
        temp = z
        while temp != 0:
            cnt += 1
            temp = temp//2
        a = (2**cnt) - z
        while a != 0:
            b = a%2
            s = s + str(b)
            a = a//2
        s = s[::-1]
        filler = 32 - len(s)
        if filler <= 0:
            #print("Number out of Range")
            s='-1'
            return s
        s = filler*"1" + s
        return s
    
def bintodecu(binary):
    c=0
    s=0
    while(c<len(binary)):
        s=s+((2**(c))*int(binary[len(binary)-1-c]))
        c=c+1
    return s
    
def bintodecs(binary):
    is_neg = binary[0] == '1'

    if is_neg:
        pos = ''.join('1' if bit == '0' else '0' for bit in binary)
        pos = "00" + bin(int(pos, 2) + 1)[2:]
    else:
        pos = binary

    decimal = int(pos, 2)
    if is_neg:
        decimal = -decimal

    return decimal

def sext(imm):
    while len(imm)<32:
        if imm[0] == '0':
            imm = '0' + imm
        else:
            imm = '1' + imm
    return imm

#R Type
def R_type(code,pc):
    rd=code[-12:-7]
    rs1=code[-20:-15]
    rs2=code[-25:-20]
    funct3=code[-15:-12]
    if(code[-32:-25]=="0100000"):
        pc=sub(rd,rs1,rs2,pc)
    else:
        if(funct3=="000"):
            pc=add(rd,rs1,rs2,pc)
        elif(funct3=="001"):
            pc=sll(rd,rs1,rs2,pc)
        elif(funct3=="010"):
            pc=slt(rd,rs1,rs2,pc)
        elif(funct3=="011"):
            pc=sltu(rd,rs1,rs2,pc)
        elif(funct3=="100"):
            pc=xor(rd,rs1,rs2,pc)
        elif(funct3=="101"):
            pc=srl(rd,rs1,rs2,pc)
        elif(funct3=="110"):
            pc=or_func(rd,rs1,rs2,pc)
        elif(funct3=="111"):
            pc=and_func(rd,rs1,rs2,pc)
    return pc

def add(rd,rs1,rs2,pc):
    n1 = bintodecs(registers[rs1])
    n2 = bintodecs(registers[rs2])
    x = (n1 + n2)
    y = decimaltobinary_32(x) 
    if len(y) > 32:
        registers[rd] = y[-32:]
    else:
        registers[rd] = y
    return(pc+4)

def sub(rd,rs1,rs2,pc):
    x=registers[rs1]
    y=registers[rs2]
    z=bintodecs(x)-bintodecs(y)
    registers[rd]=decimaltobinary_32(z)
    return pc+4

def slt(rd,rs1,rs2,pc):
    x=registers[rs1]
    y=registers[rs2]
    if(bintodecs(x)<bintodecs(y)):
        registers[rd]=decimaltobinary_32(1)
    return pc+4

def sltu(rd,rs1,rs2,pc):
    x=registers[rs1]
    y=registers[rs2]
    if(bintodecu(x)<bintodecu(y)):
        registers[rd]=decimaltobinary_32(1)
    return pc+4

def xor(rd,rs1,rs2,pc):
    registers[rd]=decimaltobinary_32(bintodecs(registers[rs1])^bintodecs(registers[rs2]))
    return pc+4

def or_func(rd,rs1,rs2,pc):
    registers[rd]=decimaltobinary_32(bintodecs(registers[rs1])|bintodecs(registers[rs2]))
    return pc+4

def and_func(rd,rs1,rs2,pc):
    registers[rd]=decimaltobinary_32(bintodecs(registers[rs1])& bintodecs(registers[rs2]))
    return pc+4

def sll(rd,rs1,rs2,pc):
    registers[rd]=decimaltobinary_32(bintodecs(registers[rs1])*(2**bintodecu(registers[rs2][-5:])))
    return pc+4

def srl(rd,rs1,rs2,pc):
    registers[rd]=decimaltobinary_32(bintodecs(registers[rs1])//(2**bintodecu(registers[rs2][-5:])))
    return pc+4
