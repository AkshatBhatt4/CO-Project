def decimaltobinary_12(num):
    num=int(num)
    if num >= 0:
        a = num
        s = ""
        while a != 0:
            b = a%2
            s = s + str(b)
            a = a//2
        s = s[::-1]
        filler = 12 - len(s)
        if filler < 0:
            print("num out of Range")
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
        filler = 12 - len(s)
        if filler < 0:
            print("num out of Range")
            s='-1'
            return s
        s = filler*"1" + s
        return s
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

def i_type(instruction,code):
    if instruction == "lw":
        rd,rs = code.split(",")
        imm,rs = rs.split("(")
        rs = rs[0:-1]
    else:
        rd,rs,imm =code.split(",")
    if rd not in register or rs not in register:
        return "Register Error"
    imm = decimaltobinary_12(imm)
    output = imm
    output += register[rs]
    output += opcode[instruction][1]
    output += register[rd]
    output += opcode[instruction][2]
    return output
def u_type(instruction,code):
        rd,imm=code.split(",")
        if rd not in register:
            return "Register Error"
        imm=decimaltobinary_32(imm)
        imm = imm[::-1]
        imm=imm[12:]
        imm = imm[::-1]
        output = imm
        output += register[rd]
        output += opcode[instruction][1]
        return output


opcode={"add":("r","0000000","000","0110011"),"sub":("r","0100000","000","0110011"),"sll":("r","0000000","001","0110011"),"slt":("r","0000000","010","0110011"),"sltu":("r","0000000","011","0110011"),"xor":("r","0000000","100","0110011"),"srl":("r","0000000","101","0110011"),"or":("r","0000000","110","0110011"),"and":("r","0000000","111","0110011")
        ,"lw":("i","010","0000011"),"addi":("i","000","0010011"),"sltiu":("i","011","0010011"),"jalr":("i","000","1100111")
        ,"sw":("s","010","0100011")
        ,"beq":("b","000","1100011"),"bne":("b","001","1100011"),"blt":("b","100","1100011"),"bge":("b","101","1100011"),"bltu":("b","110","1100011"),"bgeu":("b","111","1100011")
        ,"lui":("u","0110111"),"auipc":("u","0010111")
        ,"jal":("j","1101111")}
register={
    'zero':'00000',  
    'ra':'00001', 
    'sp':'00010',    
    'gp':'00011',
    'tp':'00100',
    't0':'00101',
    't1':'00110',
    't2':'00111',
    's0':'01000',
    's1':'01001',
    'a0':'01010',
    'a1':'01011',
    'a2':'01100',
    'a3':'01101',
    'a4':'01110',
    'a5':'01111',
    'a6':'10000',
    'a7':'10001',
    's2':'10010',
    's3':'10011',
    's4':'10100',
    's5':'10101',
    's6':'10110',
    's7':'10111',
    's8':'11000',
    's9':'11001',
    's10':'11010',
    's11':'11011',
    't3':'11100',
    't4':'11101',
    't5':'11110',
    't6':'11111',}

with open("INPUT.TXT","r") as f:
    Code=[]
    Codeline=[]
    final2=[]
    A=f.readlines()
    for i in A:
        for j in i.split():
            Code.append(j)
        a=len(Code)
        Codeline.append(Code[a-2])
        Codeline.append(Code[a-1])
        f=0
        g=1
    while g<len(Codeline):
        final=[]
        final.append(Codeline[f])
        final.append(Codeline[g])
        final2.append(final)
        f+=2
        g+=2


with open ("OUTPUT.TXT","w") as f:
    for i in final2:
        types = opcode[i[0]][0]
        if types == "r":
            f.write(r_type(i[0],i[1]))
            f.write("\n")
        elif types == "i":
            f.write(i_type(i[0],i[1]))
            f.write("\n")
        elif types == "s":
            f.write(s_type(i[0],i[1]))
            f.write("\n")
        elif types == "r":
            f.write(r_type(i[0],i[1]))
            f.write("\n")
        elif types == "j":
            f.write(j_type(i[0],i[1]))
            f.write("\n")
        elif types == "u":
            f.write(u_type(i[0],i[1]))
            f.write("\n")
        elif types == "b":
            f.write(b_type(i[0],i[1]))
            f.write("\n")
        else:
            f.write("Instruction Error")
            f.write("\n")
    
    if final2[-1] != ["beq", "zero,zero,0"]:
        f.write("Missing Virtual Halt\n")
    
    for i in range(0,len(final2)-1):
        if i == ["beq", "zero,zero,0"]:
            f.write("Virtual Halt in the Middle\n")
