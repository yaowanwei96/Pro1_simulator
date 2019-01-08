# --*-- coding:utf8 --*--

from __future__ import print_function

flag = False

list = []
data = []
pc = 0

#寄存器初始化
R = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]


class Instruct(object):
    name = ""
    def __init__(self):
        pass

#读文件函数
def read_file():
    data = []
    file_name='sample_int.txt'
    for line in open(file_name):
        line = line.split();
        data.append(line)
    return data

#反汇编
def disassembly(instruction,pc):
    #print(instruction)
    global flag
    global list
    global data

    inst = Instruct()
    code = ""
    opcode = instruction[0][0:6]
    rs1 = instruction[0][6:11]
    rt1 = instruction[0][11:16]
    rd1 = instruction[0][16:21]
    shamt1 = instruction[0][21:26]
    func1 = instruction[0][26:32]
    offset1 = instruction[0][16:32]

    rs = str(int(instruction[0][6:11],2))
    rt = str(int(instruction[0][11:16],2))
    rd = str(int(instruction[0][16:21],2))
    shamt = str(int(instruction[0][21:26],2))
    func = str(int(instruction[0][26:32],2))
    offset = str(int((instruction[0][16:32]),2))
    inst.addr = 64 + pc * 4

    if flag:
        if instruction[0].startswith("1"):
            code = str(int(instruction[0], 2)- 2**32)
        else:
            code = str(int(instruction[0],2))
    else:
        inst.rt = rt
        inst.rs = rs
        inst.rd = rd
        inst.shamt = shamt

        if opcode == "000010":
            inst.name = "J"
            inst.imm = int(instruction[0][6:32], 2)*4
            code = "J #"+str(int(instruction[0][6:32], 2)*4)
        elif opcode=="000000" and func1=="001000":
            inst.name = "JR"
            code = "JR R"+rs
        elif opcode=="000100":
            inst.name = "BEQ"
            inst.imm = int(instruction[0][16:32], 2)*4
            code = "BEQ R"+rs+", R"+rt+", #"+str(int((instruction[0][16:32]),2)*4)
        elif opcode=="000001" and rt1=="00000":
            inst.name = "BLTZ"
            inst.imm = int(instruction[0][16:32], 2)*4
            code = "BLTZ R"+rs+", #"+str(int((instruction[0][16:32]),2)*4)
        elif opcode=="000111" and rt1=="00000":
            inst.name = "BGTZ"
            inst.imm = int(instruction[0][16:32], 2)*4
            code = "BGTZ R"+rs+", #"+str(int((instruction[0][16:32]),2)*4)
        elif opcode=="000000" and shamt1=="00000" and func1=="100000":
            inst.name = "ADD"
            code = "ADD R"+rd+", R"+rs+", R"+rt
        elif opcode=="000000" and shamt1=="00000" and func1=="100010":
            inst.name = "SUB"
            code = "SUB R"+rd+", R"+rs+", R"+rt
        elif opcode=="000000" and func1=="001101":
            flag = True
            code = "BREAK"
        elif opcode=="101011":
            inst.name = "SW"
            inst.imm = int(instruction[0][16:32], 2)
            code = "SW R"+rt+", "+offset+"(R"+rs+")"
        elif opcode=="100011":
            inst.name = "LW"
            inst.imm = int(instruction[0][16:32], 2)
            code = "LW R"+rt+", "+offset+"(R"+rs+")"
        elif instruction[0] == "00000000000000000000000000000000":
            code = "NOP"
        elif opcode=="000000" and func1=="000000":
            inst.name = "SLL"
            code = "SLL R"+rd+", R"+rt+", #"+shamt
        elif opcode=="000000" and func1=="000010" and rs1=="00000":
            inst.name = "SRL"
            code = "SRL R"+rd+", R"+rt+", #"+shamt
        elif opcode=="000000" and func1=="000011" and rs1=="00000":
            inst.name = "SRA"
            code = "SRA R"+rd+", R"+rt+", #"+shamt
        elif opcode=="011100" and func1=="000010" and shamt1=="00000":
            inst.name = "MUL"
            code = "MUL R"+rd+", R"+rs+", #"+rt
        elif opcode=="000000" and func1=="100100" and shamt1=="00000":
            inst.name = "AND"
            code = "AND R"+rd+", R"+rs+", #"+rt
        elif opcode=="000000" and func1=="100111" and shamt1=="00000":
            inst.name = "NOR"
            code = "NOR R"+rd+", R"+rs+", #"+rt
        elif opcode=="000000" and func1=="101010" and shamt1=="00000":
            inst.name = "SLT"
            code = "SLT R"+rd+", R"+rs+", #"+rt
        elif opcode=="110000":
            inst.name = "ADDI"
            inst.imm = int(instruction[0][16:32], 2)
            code = "ADD R"+rt+", R"+rs+", #"+offset
        elif opcode=="110001":
            inst.name = "SUBI"
            inst.imm = int(instruction[0][16:32], 2)
            code = "SUB R"+rt+", R"+rs+", #"+offset
        elif opcode=="100001":
            inst.name = "MULI"
            inst.imm = int(instruction[0][16:32], 2)
            code = "MUL R"+rt+", R"+rs+", #"+offset
        elif opcode=="110010":
            inst.name = "ANDI"
            inst.imm = int(instruction[0][16:32], 2)
            code = "AND R"+rt+", R"+rs+", #"+offset
        elif opcode=="110011":
            inst.name = "NORI"
            inst.imm = int(instruction[0][16:32], 2)
            code = "NOR R"+rt+", R"+rs+", #"+offset
        elif opcode=="110101":
            inst.name = "SLTI"
            inst.imm = int(instruction[0][16:32], 2)
            code = "SLT R"+rt+", R"+rs+", #"+offset

    inst.code = code
    # print(code)
    if flag and code!="BREAK":
        inst.imm = code
        data.append(inst)
    else:
        list.append(inst)
    return code

#打印寄存器数据
def printRegister(ff):
    global R
    ff.write("Registers\n")
    ff.write("R00:\t"+str(R[0])+"\t"+str(R[1])+"\t"+str(R[2])+"\t"+str(R[3])+"\t"+str(R[4])+"\t"+str(R[5])+"\t"+str(R[6])+"\t"+str(R[7])+"\t"+str(R[8])+"\t"+str(R[9])+"\t"+str(R[10])+"\t"+str(R[11])+"\t"+str(R[12])+"\t"+str(R[13])+"\t"+str(R[14])+"\t"+str(R[15])+"\n")
    ff.write("R16:\t"+str(R[16])+"\t"+str(R[17])+"\t"+str(R[18])+"\t"+str(R[19])+"\t"+str(R[20])+"\t"+str(R[21])+"\t"+str(R[22])+"\t"+str(R[23])+"\t"+str(R[24])+"\t"+str(R[25])+"\t"+str(R[26])+"\t"+str(R[27])+"\t"+str(R[28])+"\t"+str(R[29])+"\t"+str(R[30])+"\t"+str(R[31])+"\n")

#打印data数据
def printData(ff):
    global data
    ff.write("Data\n")
    for i in range(len(data)):
        if i % 8 == 0 :
            if i!=0 : ff.write("\n")
            ff.write(str(data[i].addr)+":\t")
        if i % 8 == 7:
            ff.write(str(data[i].imm))
        else:
            ff.write(str(data[i].imm) + "\t")

#计算
def simulator(ist):
    global list
    global data
    global R
    global pc
    print(ist.name)
    if ist.name == "J":
        pc = int((ist.imm - 64) /4) - 1
    elif ist.name == "JR":
        pc = R[int(ist.rs)]
    elif ist.name == "BEQ":
        if R[int(ist.rs)] == R[int(ist.rt)] :
            pc = pc + int(ist.imm/4)
    elif ist.name == "BLTZ":
        if R[int(ist.rs)] < 0:
            pc = pc + int(ist.imm / 4)
    elif ist.name == "BGTZ":
        if R[int(ist.rs)] > 0:
            pc = pc + int(ist.imm / 4)
    elif ist.name == "ADD":
        R[int(ist.rd)] = int(R[int(ist.rs)]) + int(R[int(ist.rt)])
    elif ist.name == "SUB":
        R[int(ist.rd)] = int(R[int(ist.rs)]) - int(R[int(ist.rt)])
    elif ist.name == "BREAK":
        return
    elif ist.name == "SW":
        for d in data:
            if d.addr == R[int(ist.rs)]+int(ist.imm):
                d.imm = R[int(ist.rt)]
    elif ist.name == "LW":
        for d in data:
            if d.addr == R[int(ist.rs)]+int(ist.imm):
                R[int(ist.rt)]= d.imm
    elif ist.name == "SLL":
        R[int(ist.rd)] = R[int(ist.rt)] << int(ist.shamt)
    elif ist.name == "SRL":
        R[int(ist.rd)] = R[int(ist.rt)] >> int(ist.shamt)
    elif ist.name == "SRA":
        R[int(ist.rd)] = R[int(ist.rt)] >> int(ist.shamt)
    elif ist.name == "NOP":
        return
    elif ist.name == "MUL":
        R[int(ist.rd)] = int(R[int(ist.rs)]) * int(R[int(ist.rt)])
    elif ist.name == "AND":
        R[int(ist.rd)] = R[int(ist.rs)] and R[int(ist.rt)]
    elif ist.name == "NOR":
        R[int(ist.rd)] = not(R[int(ist.rs)] or R[int(ist.rt)])
    elif ist.name == "SLT":
        if R[int(ist.rs)] < R[int(ist.rt)]:
            R[int(ist.rd)] = 1
        else:
            R[int(ist.rd)] = 0
    elif ist.name == "ADDI":
        R[int(ist.rt)] = R[int(ist.rs)] + int(ist.imm)
    elif ist.name == "SUBI":
        R[int(ist.rt)] = R[int(ist.rs)] - int(ist.imm)
    elif ist.name == "MULI":
        R[int(ist.rt)] = R[int(ist.rs)] * int(ist.imm)
    elif ist.name == "ANDI":
        R[int(ist.rt)] = R[int(ist.rs)] and int(ist.imm)
    elif ist.name == "NORI":
        R[int(ist.rt)] = not(R[int(ist.rs)] or int(ist.imm))
    elif ist.name == "SLTI":
        if R[int(ist.rs)] < int(ist.imm):
            R[int(ist.rd)] = 1
        else:
            R[int(ist.rd)] = 0


if __name__ == '__main__':

    sample = read_file()
    address = 64
    pc = 0
    f = open("disassembly_int.txt","w")
    for pc in range(len(sample)):
        instruction= disassembly(sample[pc],pc)
        if flag:
            f.write(sample[pc][0] + "\t" + str(address + pc * 4) + "\t" + instruction + "\n")
        else:
            f.write(sample[pc][0][0:6]+" "+sample[pc][0][6:11]+" "+sample[pc][0][11:16]+" "+sample[pc][0][16:21]+" "+sample[pc][0][21:26]+" "+sample[pc][0][26:32]+"\t"+str(address+pc*4)+"\t"+instruction+"\n")

    f.close()

    pc = int(0)
    count = 1
    ff = open("simulation_int.txt", "w")
    while pc < len(list):

        ff.write("--------------------")
        ff.write("\nCycle:"+str(count)+"\t"+ str(pc * 4 + 64) + "\t" + list[pc].code + "\n\n")
        simulator(list[pc])
        printRegister(ff)
        ff.write("\n")
        printData(ff)
        ff.write("\n\n")
        if list[pc].code=="BREAK":
            break ;
        print("\n")
        pc = pc + 1
        count = count + 1


    ff.close()
