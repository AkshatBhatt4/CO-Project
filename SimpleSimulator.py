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
        if filler < 0:
            print("number out of Range")
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
        if filler < 0:
            print("Number out of Range")
            s='-1'
            return s
        s = filler*"1" + s
        return s
def RegPrint():
    for i in registers.keys():
        print(registers[i],end=" ")
    print()

def pcPrint(pc):
    print(decimaltobinary_32(pc))
    return

def RType(code,pc):
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
            pc=or_functioin(rd,rs1,rs2,pc)
        elif(funct3=="111"):
            pc=and_function(rd,rs1,rs2,pc)
    return pc

def BType(code,pc):
    funct3=code[-15:-12]
    imm=code[-12:-7]
    rs1=code[-20:-15]
    rs2=code[-25:-20]
    if(funct3=="000"):
        pc=beq(rs1,rs2,imm,pc)
    elif(funct3=="001"):
        pc=bne(rs1,rs2,imm,pc)
    elif(funct3=="100"):
        pc=blt(rs1,rs2,imm,pc)
    elif(funct3=="101"):
        pc=bge(rs1,rs2,imm,pc)
    return pc

def Main(pc):
    while(1):
        OpCode=statements[pc][-7:]
        if (pc>=(len(statements)-1)*4):
            RegPrint()
        #R Type
        elif(OpCode=="0110011"):
            pc=RType(statements[pc],pc)
        #I Type
        elif(OpCode=="0000011"):
            pc=lw(statements[pc],pc)
        elif(OpCode=="0010011"):
            pc=addi(statements[pc],pc)
        elif(OpCode=="1100111"):
            pc=jalr(statements[pc],pc)
        #S Type
        elif(OpCode=="0100011"):
            pc=sw(statements[pc],pc)
        #B Type
        elif(OpCode=="1100011"):
            pc=BType(statements[pc],pc)
        #U Type
        elif(OpCode=="0110111"):
            pc=lui(statements[pc],pc)
        elif(OpCode=="0010111"):
            pc=auipc(statements[pc],pc)
        #J Type
        elif(OpCode=="1101111"):
            pc=jal(statements[pc],pc)
        pcPrint(pc)
        RegPrint()
        
statements = {}
var = 0
while(1):
    try:
        line=input()
        if (line!=""):
            statements[var]=line
            var+=4
    except EOFError:
        break
pc =0
registers={'00000':'0000000000000000',
'00001':'0000000000000000',
'00010':'0000000000000000',
'00011':'0000000000000000',
'00100':'0000000000000000',
'00101':'0000000000000000',
'00110':'0000000000000000',
'00111':'0000000000000000',
'01000':'0000000000000000',
'01001':'0000000000000000',
'01010':'0000000000000000',
'01011':'0000000000000000',
'01100':'0000000000000000',
'01101':'0000000000000000',
'01110':'0000000000000000',
'01111':'0000000000000000',
'10000':'0000000000000000',
'10001':'0000000000000000',
'10010':'0000000000000000',
'10011':'0000000000000000',
'10100':'0000000000000000',
'10101':'0000000000000000',
'10110':'0000000000000000',
'10111':'0000000000000000',
'11000':'0000000000000000',
'11001':'0000000000000000',
'11010':'0000000000000000',
'11011':'0000000000000000',
'11100':'0000000000000000',
'11101':'0000000000000000',
'11110':'0000000000000000',
'11111':'0000000000000000'}
Main(pc)
