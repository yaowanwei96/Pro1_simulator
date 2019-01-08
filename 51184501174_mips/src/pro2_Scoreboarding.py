# --*-- coding:utf8 --*--

from __future__ import print_function

flag = False

list = []
data = []
pc = 0

#定义list
IF_Unit_wait = ""
IF_Unit_excute = None
Pre_Issue_Buffer = []
Pre_ALU_Queue = []
Post_ALU_Buffer = None
Pre_ALUB_Queue = []
Post_ALUB_Buffer = None
Pre_MEM_Queue = []
Post_MEM_Buffer = None

Branch_ins = ["J","JR","BEQ","BLTZ","BGTZ","BREAK","NOP"]
ALU_ins = ["ADD","ADDI","SUB","SUBI","NOR","NORI","AND","ANDI","SLT","SLTI"]
ALUB_ins = ["SLL","SRL","SRA","MUL","MULI"]
Mem_ins = ["LW","SW"]


#寄存器初始化
R = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Register_state = ["","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""]



class Instruct(object):
    name = ""
    def __init__(self):
        pass

class Function_unit(object):
    name = ""
    Busy = False
    Op = ""
    Fi = 0
    Fj = 0
    Fk = 0
    Qj = ""
    Qk = ""
    Rj = False
    Rk = False

    def __init__(self):
        pass



#读文件函数
def read_file():
    data = []
    file_name='sample.txt'
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
    ff.write("R00:\t"+str(R[0])+"\t"+str(R[1])+"\t"+str(R[2])+"\t"+str(R[3])+"\t"+str(R[4])+"\t"+str(R[5])+"\t"+str(R[6])+"\t"+str(R[7])+"\nR08:"+"\t"+str(R[8])+"\t"+str(R[9])+"\t"+str(R[10])+"\t"+str(R[11])+"\t"+str(R[12])+"\t"+str(R[13])+"\t"+str(R[14])+"\t"+str(R[15])+"\n")
    ff.write("R16:\t"+str(R[16])+"\t"+str(R[17])+"\t"+str(R[18])+"\t"+str(R[19])+"\t"+str(R[20])+"\t"+str(R[21])+"\t"+str(R[22])+"\t"+str(R[23])+"\nR24:"+"\t"+str(R[24])+"\t"+str(R[25])+"\t"+str(R[26])+"\t"+str(R[27])+"\t"+str(R[28])+"\t"+str(R[29])+"\t"+str(R[30])+"\t"+str(R[31])+"\n")

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

#判断-registerState这张表中是否别的write有占用
def WAWFlag(insWAW):
    if insWAW.name == "J":
        return True
    elif insWAW.name == "JR":
        return True
    elif insWAW.name == "BEQ":
        return True
    elif insWAW.name == "BLTZ":
        return True
    elif insWAW.name == "BGTZ":
        return True
    elif insWAW.name == "ADD":
        return Register_state[int(insWAW.rd)] == ""
    elif insWAW.name == "ADDI":
        return Register_state[int(insWAW.rt)] == ""
    elif insWAW.name == "SUB":
        return Register_state[int(insWAW.rd)] == ""
    elif insWAW.name == "MUL":
        return Register_state[int(insWAW.rd)] == ""
    elif insWAW.name == "MULI":
        return Register_state[int(insWAW.rt)] == ""
    elif insWAW.name == "AND":
        return Register_state[int(insWAW.rd)] == ""
    elif insWAW.name == "ANDI":
        return Register_state[int(insWAW.rt)] == ""
    elif insWAW.name == "SW":
        return True
    elif insWAW.name == "LW":
        return True
    elif insWAW.name == "SLL":
        return Register_state[int(insWAW.rd)] == ""
    elif insWAW.name == "SLT":
        return Register_state[int(insWAW.rd)] == ""
    elif insWAW.name == "SLTI":
        return Register_state[int(insWAW.rt)] == ""
    elif insWAW.name == "SRL":
        return Register_state[int(insWAW.rd)] == ""
    elif insWAW.name == "SRA":
        return Register_state[int(insWAW.rd)] == ""
    elif insWAW.name == "NOR":
        return Register_state[int(insWAW.rd)] == ""
    elif insWAW.name == "NORI":
        return Register_state[int(insWAW.rt)] == ""


def WARFlag(insWAR):
    if insWAR.name == "J":
        return True
    elif insWAR.name == "JR":
        return Register_state[insWAR.rs] == ""
    elif insWAR.name == "BEQ":
        return True
    elif insWAR.name == "BLTZ":
        return True
    elif insWAR.name == "BGTZ":
        return True
    elif insWAR.name == "ADD":
        return Register_state[insWAR.rs] == "" or Register_state[insWAR.rt] == ""
    elif insWAR.name == "ADDI":
        return Register_state[insWAR.rs] == "" or Register_state[insWAR.offset] == ""
    elif insWAR.name == "SUB":
        return Register_state[insWAR.rs] == "" or Register_state[insWAR.rt] == ""
    elif insWAR.name == "MUL":
        return Register_state[insWAR.rs] == "" or Register_state[insWAR.rt] == ""
    elif insWAR.name == "AND":
        return Register_state[insWAR.rs] == "" or Register_state[insWAR.rt] == ""
    elif insWAR.name == "ANDI":
        return Register_state[insWAR.rs] == "" or Register_state[insWAR.offset] == ""
    elif insWAR.name == "SW":
        return True
    elif insWAR.name == "LW":
        return True
    elif insWAR.name == "SLL":
        #rt sa
        return Register_state[insWAR.rt] == ""
    elif insWAR.name == "SLT":
        return Register_state[insWAR.rd] == ""
    elif insWAR.name == "SLTI":
        return Register_state[insWAR.rt] == ""
    elif insWAR.name == "SRL":
        return Register_state[insWAR.rd] == ""
    elif insWAR.name == "SRA":
        return Register_state[insWAR.rd] == ""
    elif insWAR.name == "NOR":
        return Register_state[insWAR.rd] == ""
    elif insWAR.name == "NORI":
        return Register_state[insWAR.rt] == ""


def before_issue(index):
    pass




def scoreboarding():
    global pc

    #取指令
    Pre_Issue_Buffer_length = len(Pre_Issue_Buffer)
    Pre_ALU_Queue_length = len(Pre_ALU_Queue)
    Pre_ALUB_Queue_length = len(Pre_ALUB_Queue)
    Pre_MEM_Queue_length = len(Pre_MEM_Queue)
    Post_ALU_Buffer_length = len(Post_ALU_Buffer)
    Post_ALUB_Buffer_length = len(Post_ALUB_Buffer)
    Post_MEM_Buffer_lenth = len(Post_MEM_Buffer)

    count_if = 0#取指令的条数
    for i in range(4-Pre_Issue_Buffer_length):
        if list[pc].name == "J" or list[pc].name == "JR" or list[pc].name == "BEQ" or list[pc].name == "BLTZ" or list[pc].name == "BGTZ" :
            IF_Unit_wait = list[pc]
            pc = pc + 1
            break
        elif list[pc].name == "BREAK" or list[pc].name == "NOP":
            pc = pc + 1
            break
        else:
            Pre_Issue_Buffer.append(list[pc])
            pc = pc + 1
            count_if = count_if + 1
            if count_if >= 2:
                break

    #issue发射指令---先得到Pre_Issue_Buffer的原来的长度，然后取指令，然后判断
    count_issue = 0
    for i in range(len(Pre_Issue_Buffer_length)):#Pre_Issue_Buffer_le前一个周期的size，只需要处理前一周期的部分指令
        #没有WAW和WAR冒险，可以进行发射
        if (WAWFlag(Pre_Issue_Buffer[i])==True) and (WARFlag(Pre_Issue_Buffer[i])==True):
            if count_issue>3:#一个周期只能发射4条指令
                break
            elif (Pre_Issue_Buffer[i].name in ALU_ins) and len(Pre_ALU_Queue)<2:
                Pre_ALU_Queue.append(Pre_Issue_Buffer[i])
                Pre_Issue_Buffer.remove(i)
                count_issue = count_issue + 1
            elif (Pre_Issue_Buffer[i].name in ALUB_ins) and len(Pre_ALUB_Queue)<2:
                Pre_ALUB_Queue.append(Pre_Issue_Buffer[i])
                Pre_Issue_Buffer.remove(i)
                count_issue = count_issue + 1
            elif (Pre_Issue_Buffer[i].name in Mem_ins) and len(Pre_MEM_Queue)<2:
                Pre_MEM_Queue.append(Pre_Issue_Buffer[i])
                Pre_Issue_Buffer.remove(i)
                count_issue = count_issue + 1
        #else:#不能发射---查看后面周期是否完成---不能发射就不操作


    #ALU---执行部分






    #WB


    pass


def printScore(ff):
    global R
    ff.write("IF Unit:\n")
    if IF_Unit_excute == None and IF_Unit_wait == None :
        ff.write("	Waiting Instruction: \n")
        ff.write("	Executed Instruction: \n")
    elif IF_Unit_excute == None and IF_Unit_wait != None :
        ff.write("	Waiting Instruction: "+ IF_Unit_wait.code + "\n")
        ff.write("	Executed Instruction: \n")
    elif IF_Unit_excute != None and IF_Unit_wait == None :
        ff.write("	Waiting Instruction: \n")
        ff.write("	Executed Instruction: "+ IF_Unit_excute.code + "\n")
    elif IF_Unit_wait != None and IF_Unit_wait != None :
        ff.write("	Waiting Instruction: "+ IF_Unit_wait.code + "\n")
        ff.write("	Waiting Instruction: "+ IF_Unit_excute.code + "\n")


    ff.write("Pre-Issue Buffer:\n")

    if len(Pre_Issue_Buffer) == 0:
        ff.write("	Entry 0:\n")
        ff.write("	Entry 1:\n")
        ff.write("	Entry 2:\n")
        ff.write("	Entry 3:\n")
    elif len(Pre_Issue_Buffer) == 1:
        ff.write("	Entry 0:[" + Pre_Issue_Buffer[0].code + "]\n")
        ff.write("	Entry 1:\n")
        ff.write("	Entry 2:\n")
        ff.write("	Entry 3:\n")
    elif len(Pre_Issue_Buffer) == 2:
        ff.write("	Entry 0:[" + Pre_Issue_Buffer[0].code + "]\n")
        ff.write("	Entry 1:[" + Pre_Issue_Buffer[1].code + "]\n")
        ff.write("	Entry 2:\n")
        ff.write("	Entry 3:\n")
    elif len(Pre_Issue_Buffer) == 3:
        ff.write("	Entry 0:[" + Pre_Issue_Buffer[0].code + "]\n")
        ff.write("	Entry 1:[" + Pre_Issue_Buffer[1].code + "]\n")
        ff.write("	Entry 2:[" + Pre_Issue_Buffer[2].code + "]\n")
        ff.write("	Entry 3:\n")
    elif len(Pre_Issue_Buffer) == 4:
        ff.write("	Entry 0:[" + Pre_Issue_Buffer[0].code + "]\n")
        ff.write("	Entry 1:[" + Pre_Issue_Buffer[1].code + "]\n")
        ff.write("	Entry 2:[" + Pre_Issue_Buffer[2].code + "]\n")
        ff.write("	Entry 3:[" + Pre_Issue_Buffer[3].code + "]\n")

    ff.write("Pre-ALU Queue:\n")
    if len(Pre_ALU_Queue) == 0 :
        ff.write("	Entry 0:\n")
        ff.write("	Entry 1:\n")
    elif len(Pre_ALU_Queue) == 1 :
        ff.write("	Entry 0:[" + Pre_ALU_Queue[0].code + "]\n")
        ff.write("	Entry 1:\n")
    elif len(Pre_ALU_Queue) == 2 :
        ff.write("	Entry 0:[" + Pre_ALU_Queue[0].code + "]\n")
        ff.write("	Entry 1:[" + Pre_ALU_Queue[1].code + "]\n")

    if Post_ALU_Buffer == None:
        ff.write("Post-ALU Buffer:\n")
    else:
        ff.write("Post-ALU Buffer:["+Post_ALU_Buffer.code+"]\n")

    ff.write("Pre-ALUB Queue:\n")
    if len(Pre_ALUB_Queue) == 0 :
        ff.write("	Entry 0:\n")
        ff.write("	Entry 1:\n")
    elif len(Pre_ALUB_Queue) == 1 :
        ff.write("	Entry 0:[" + Pre_ALUB_Queue[0].code + "]\n")
        ff.write("	Entry 1:\n")
    elif len(Pre_ALUB_Queue) == 2 :
        ff.write("	Entry 0:[" + Pre_ALUB_Queue[0].code + "]\n")
        ff.write("	Entry 1:[" + Pre_ALUB_Queue[1].code + "]\n")


    if Post_ALUB_Buffer == None:
        ff.write("Post-ALUB Buffer:\n")
    else:
        ff.write("Post-ALUB Buffer:["+Post_ALUB_Buffer.code+"]\n")


    ff.write("Pre-MEM Queue:\n")
    if len(Pre_MEM_Queue) == 0 :
        ff.write("	Entry 0:\n")
        ff.write("	Entry 1:\n")
    elif len(Pre_MEM_Queue) == 1 :
        ff.write("	Entry 0:[" + Pre_MEM_Queue[0].code + "]\n")
        ff.write("	Entry 1:\n")
    elif len(Pre_MEM_Queue) == 2 :
        ff.write("	Entry 0:[" + Pre_MEM_Queue[0].code + "]\n")
        ff.write("	Entry 1:[" + Pre_MEM_Queue[1].code + "]\n")

    if Post_MEM_Buffer == None:
        ff.write("Post-MEM Buffer:\n")
    else:
        ff.write("Post-MEM Buffer:["+Post_MEM_Buffer.code+"]\n")



# if __name__ == '__main__':
#
#     sample = read_file()
#     address = 64
#     pc = 0
#     f = open("disassembly1.txt","w")
#     for pc in range(len(sample)):
#         instruction= disassembly(sample[pc],pc)
#         if flag:
#             f.write(sample[pc][0] + "\t" + str(address + pc * 4) + "\t" + instruction + "\n")
#         else:
#             f.write(sample[pc][0][0:6]+" "+sample[pc][0][6:11]+" "+sample[pc][0][11:16]+" "+sample[pc][0][16:21]+" "+sample[pc][0][21:26]+" "+sample[pc][0][26:32]+"\t"+str(address+pc*4)+"\t"+instruction+"\n")
#
#     f.close()
#
#     pc = int(0)
#     count = 1
#     ff = open("simulation111.txt", "w")
#     while pc < len(list):
#         ff.write("--------------------")
#         ff.write("\nCycle:"+str(count)+"\n\n")
#         scoreboarding()
#         printScore(ff)
#         printRegister(ff)
#         ff.write("\n")
#         printData(ff)
#         ff.write("\n\n")
#         if list[pc].code=="BREAK":
#             break ;
#         print("\n")
#         count = count + 1
#


