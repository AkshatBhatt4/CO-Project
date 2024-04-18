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


#I Type
def lw(code,pc):
    imm = code[-32:-20]
    rd = code[-12:-7]
    rs1 = code[-20:-15]
    add = hex(bintodecs(registers[rs1]) + bintodecs(sext(imm)))
    while(len(add)<10):
        add = "0x" + "0" + add[2:]
    registers[rd] = memory[add]
    return pc+4

def addi(code,pc):
    imm = sext(code[-32:-20])
    rd = code[-12:-7]
    rs1 = code[-20:-15]
    value = bintodecs(registers[rs1]) + bintodecs(imm)
    registers[rd] = decimaltobinary_32(value)
    return pc+4

def jalr(code,pc):
    imm = sext(code[-32:-20])
    rd = code[-12:-7]
    rs1 = code[-20:-15]
    temp = decimaltobinary_32(pc + 4)
    registers[rd] = temp
    pc = bintodecs(registers[rs1]) + bintodecs(imm)
    if pc%2==1:
        pc = pc - 1
    return pc

#S Type
def sw(code,pc):
    imm = code[-32:-25] + code[-12:-7]
    rs1 = code[-20:-15]
    rs2 = code[-25:-20]
    add = bintodecs(registers[rs1]) + bintodecs(sext(imm))
    add = hex(add)
    while(len(add)<10):
        add = "0x" + "0" + add[2:]
    memory[add] = registers[rs2]
    return pc+4

#B Type
def B_type(code,pc):
    funct3 = code[-15:-12]
    imm = code[-32] + code[-8] + code[-31:-25] + code[-12:-8] + '0'
    imm = sext(imm)
    imm = bintodecs(imm)

    rs1 = code[-20:-15]
    rs2 = code[-25:-20]
    if funct3 == "000":
        pc = beq(rs1,rs2,imm,pc)
    if funct3 == "001":
        pc = bne(rs1,rs2,imm,pc)
    if funct3 == "100":
        pc = blt(rs1,rs2,imm,pc)
    if funct3 == "101":
        pc = bge(rs1,rs2,imm,pc)
    return pc

def beq(rs1,rs2,imm,pc):
    if bintodecs(registers[rs1])==bintodecs(registers[rs2]):
        pc = pc + imm
    else:
        pc = pc + 4
    return pc

def bne(rs1,rs2,imm,pc):
    if bintodecs(registers[rs1])!=bintodecs(registers[rs2]):
        pc = pc + imm
    else:
        pc = pc + 4
    return pc

def blt(rs1,rs2,imm,pc):
    if bintodecs(registers[rs1])<bintodecs(registers[rs2]):
        pc = pc + imm
    else:
        pc = pc + 4
    return pc

def bge(rs1,rs2,imm,pc):
    if bintodecs(registers[rs1])>=bintodecs(registers[rs2]):
        pc = pc + imm
    else:
        pc = pc + 4
    return pc


#U Type
def auipc(code,pc):
    imm = code[-32:-12] + "000000000000"
    imm = bintodecs(imm)
    rd = code[-12:-7]
    temp = pc + imm
    temp = decimaltobinary_32(temp)
    registers[rd] = temp
    return pc+4

def lui(code,pc):
    imm = code[-32:-12] + "000000000000"
    rd = code[-12:-7]
    registers[rd] = imm
    return pc+4

#J Type
def jal(code,pc):
    imm = code[-32] + code[-20:-12] + code[-21] + code[-31:-21] + "0"
    rd = code[-12:-7]
    temp = pc + 4
    temp = decimaltobinary_32(temp)
    registers[rd] = temp
    pc = pc + bintodecs(sext(imm))
    if pc%2==1:
        pc = pc - 1
    return pc

#Reg print and main
def RegPrint(l):
    s=""
    for i in registers.keys():
        s=s+("0b"+registers[i]+" ")
    s+="\n"
    l.append(s)


def Main(registers,memory,pc_dic):
    pc=0
    while True:
        OpCode=pc_dic[pc][-7:]

        if pc_dic[pc] == "00000000000000000000000001100011":
            RegPrint(l)
            break
        
        #R Type
        if(OpCode=="0110011"):
            pc=R_type(pc_dic[pc],pc)
            registers['pc']=decimaltobinary_32(pc)
        #I Type
        elif(OpCode=="0000011"):
            pc=lw(pc_dic[pc],pc)
            registers['pc']=decimaltobinary_32(pc)
        elif(OpCode=="0010011"):
            pc=addi(pc_dic[pc],pc)
            registers['pc']=decimaltobinary_32(pc)
        elif(OpCode=="1100111"):
            pc=jalr(pc_dic[pc],pc)
            registers['pc']=decimaltobinary_32(pc)
        #S Type
        elif(OpCode=="0100011"):
            pc=sw(pc_dic[pc],pc)
            registers['pc']=decimaltobinary_32(pc)
        #B Type
        elif(OpCode=="1100011"):
            pc=B_type(pc_dic[pc],pc)
            registers['pc']=decimaltobinary_32(pc)
        #U Type
        elif(OpCode=="0110111"):
            pc=lui(pc_dic[pc],pc)
            registers['pc']=decimaltobinary_32(pc)
        elif(OpCode=="0010111"):
            pc=auipc(pc_dic[pc],pc)
            registers['pc']=decimaltobinary_32(pc)
        #J Type
        elif(OpCode=="1101111"):
            pc=jal(pc_dic[pc],pc)
            registers['pc']=decimaltobinary_32(pc)
        RegPrint(l)

if len(sys.argv) < 3:
    sys.exit("Input file path and output file path are required")

input = sys.argv[1]
output = sys.argv[2]

if not os.path.exists(input):
    sys.exit("Input file does not exist")

with open(input,"r") as f:
    if not f:
        sys.exit("Input file is empty")
    x = f.readlines()
    pc_dic = {}
    var = 0
    for line in x:
        if line[-1]=='\n':
            pc_dic[var] = line[:-1]
            var += 4
        else:
            pc_dic[var] = line
            var+=4

registers={
    'pc':'00000000000000000000000000000100',
    '00000':'00000000000000000000000000000000',
    '00001':'00000000000000000000000000000000',
    '00010':'00000000000000000000000100000000',
    '00011':'00000000000000000000000000000000',
    '00100':'00000000000000000000000000000000',
    '00101':'00000000000000000000000000000000',
    '00110':'00000000000000000000000000000000',
    '00111':'00000000000000000000000000000000',
    '01000':'00000000000000000000000000000000',
    '01001':'00000000000000000000000000000000',
    '01010':'00000000000000000000000000000000',
    '01011':'00000000000000000000000000000000',
    '01100':'00000000000000000000000000000000',
    '01101':'00000000000000000000000000000000',
    '01110':'00000000000000000000000000000000',
    '01111':'00000000000000000000000000000000',
    '10000':'00000000000000000000000000000000',
    '10001':'00000000000000000000000000000000',
    '10010':'00000000000000000000000000000000',
    '10011':'00000000000000000000000000000000',
    '10100':'00000000000000000000000000000000',
    '10101':'00000000000000000000000000000000',
    '10110':'00000000000000000000000000000000',
    '10111':'00000000000000000000000000000000',
    '11000':'00000000000000000000000000000000',
    '11001':'00000000000000000000000000000000',
    '11010':'00000000000000000000000000000000',
    '11011':'00000000000000000000000000000000',
    '11100':'00000000000000000000000000000000',
    '11101':'00000000000000000000000000000000',
    '11110':'00000000000000000000000000000000',
    '11111':'00000000000000000000000000000000'}
memory= {
    "0x00010000": "00000000000000000000000000000000",
    "0x00010004": "00000000000000000000000000000000",
    "0x00010008": "00000000000000000000000000000000",
    "0x0001000c": "00000000000000000000000000000000",
    "0x00010010": "00000000000000000000000000000000",
    "0x00010014": "00000000000000000000000000000000",
    "0x00010018": "00000000000000000000000000000000",
    "0x0001001c": "00000000000000000000000000000000",
    "0x00010020": "00000000000000000000000000000000",
    "0x00010024": "00000000000000000000000000000000",
    "0x00010028": "00000000000000000000000000000000",
    "0x0001002c": "00000000000000000000000000000000",
    "0x00010030": "00000000000000000000000000000000",
    "0x00010034": "00000000000000000000000000000000",
    "0x00010038": "00000000000000000000000000000000",
    "0x0001003c": "00000000000000000000000000000000",
    "0x00010040": "00000000000000000000000000000000",
    "0x00010044": "00000000000000000000000000000000",
    "0x00010048": "00000000000000000000000000000000",
    "0x0001004c": "00000000000000000000000000000000",
    "0x00010050": "00000000000000000000000000000000",
    "0x00010054": "00000000000000000000000000000000",
    "0x00010058": "00000000000000000000000000000000",
    "0x0001005c": "00000000000000000000000000000000",
    "0x00010060": "00000000000000000000000000000000",
    "0x00010064": "00000000000000000000000000000000",
    "0x00010068": "00000000000000000000000000000000",
    "0x0001006c": "00000000000000000000000000000000",
    "0x00010070": "00000000000000000000000000000000",
    "0x00010074": "00000000000000000000000000000000",
    "0x00010078": "00000000000000000000000000000000",
    "0x0001007c": "00000000000000000000000000000000"}
l=[]

Main(registers, memory, pc_dic)

with open(output, "w") as f:
    for line in l:
        f.write(line)
    for i in memory.keys():
        f.write(i+":0b"+memory[i]+"\n")
sys.exit()
