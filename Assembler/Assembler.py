import re, sys
file = open(str(sys.argv[1]), 'r')
LC = 0

# In-built MOT table
# Format:
# Symbol(8-bytes)  |  Value(4-bytes)  |  Length(2-bytes)  |  Relocation(1-byte)
MOT = {
    "AR":   ["1A", 2, "RR"],
    "A":    ["5A", 4, "RX"],
    "AP":   ["FA", 6, "SS"],
    "AH":   ["4A", 4, "RX"],
    "ALR":  ["1E", 2, "RR"],
    "BR":   ["BCR", 2, "RR"],
    "BNE":  ["BC", 4, "RX"],
    "BALR": ["05", 2, "RR"],
    "BAL":  ["45", 4, "RX"],
    "BASR": ["0D", 2, "RR"],
    "BAS":  ["4D", 4, "RX"],
    "BCR":  ["07", 2, "RR"],
    "BC":   ["47", 4, "RX"],
    "C":    ["59", 4, "RX"],
    "LR":   ["18", 2, "RR"],
    "L":    ["58", 4, "RX"],
    "LA":   ["41", 4, "RX"],
    "ST":   ["50", 4, "RX"],
    "SR":   ["1B", 2, "RR"],
}

POT = ["DROP", "END", "EQU", "START", "USING", "DS", "DC", "LTORG"]
# Pass 1 generated data structures
ST = {}
LT = {}
BT = {}
# Structure of BT :
# availability(1-byte)  |  contents
for i in range(1, 16):
    BT[i] = ["N", "-"]

code = []


def helper(ch):
    if ch == "H":
        return 2
    if ch == "F" or ch == "A":
        return 4
    if ch == "D":
        return 8


def alignLC(length):
    global LC
    if(not(LC % length == 0)):
        # e.g. if LC = 25 and length = 4
        # then LC = 25 + 4 - (1)
        LC = LC+length-(LC % length)


def adjustBytes(label):
    rep = 'b'*(8-len(label))
    return "\"{}{}\"".format(label, rep)


def literalStorage():
    global LC
    global LT
    for lit in LT:
        alignLC(LT[lit][1])
        if LT[lit][0] == "-":
            LT[lit] = [hex(LC), LT[lit][1], LT[lit][2]]
            LC += int(LT[lit][1])


def util_DC_DS(item, label):
    global LC
    global ST
    global LT
    try:
        for ch in ["F", "H", "D"]:
            # It's a constant value...
            if item.startswith(ch):
                code.append(re.search("'(.*)'", item).group(1))
                length = helper(ch)
                # Check for alignment
                alignLC(length)
                # Add the new label into the Symbol Table
                if label not in ST:
                    label = adjustBytes(label)
                    ST[label] = [hex(LC), length, 'R']
                LC = LC+length
                return
            # If we have defined some storage space....
            elif item.endswith(ch):
                # print('label {} is DS type'.format(label))
                # count the required storage locations....
                locs = int(re.search("(.*){}".format(ch), item).group(1))
                length = helper(ch)
                # Check for alignment
                alignLC(length)
                # Add the new label into the Symbol Table
                if label not in ST:
                    label = adjustBytes(label)
                    ST[label] = [hex(LC), length, 'R']
                LC += (length*locs)
                return
            # It's a literal... Put it in literal table..
            elif item.startswith("={}".format(ch)):
                # print("{} is a literal".format(item))
                length = helper(ch)
                # Check for alignment
                alignLC(length)
                if item not in LT:
                    LT[item[1:]] = [hex(LC), length, "R"]
                LC += length
                code.append(re.search("'(.*)'", item).group(1))
                return

    except Exception as e:
        print('Exception :', e)


count = 0
index_reg = 0
base_reg = 0
base_content = 0

while True:
    count += 1
    line = file.readline().strip()
    if not line:
        break
    print(count, '  :  ', line)
    line = line.split(' ')
    for item in line:
        # print(item)
        if item in POT:
            # print("{} in POT".format(item))
            # Do some operation
            if item == "START":
                LC = int(line[-1])
                label = line[0]
                rep = 'b'*(8-len(label))
                label = "\"{}{}\"".format(label, rep)
                if label not in ST:
                    ST[label] = [hex(LC), 1, "R"]
                break

            if item == "EQU":
                label = line[0]
                label = adjustBytes(label)
                if(line[-1] == '*'):
                    ST[label] = [hex(LC), 1, "R"]
                else:
                    ST[label] = [hex(int(line[-1])), 1, "A"]
                break

            if item == "DS" or item == "DC":
                util_DC_DS(line[-1], line[0])
                break

            # Assign storage space to all literals in LT
            if item == "LTORG":
                LC += 4
                literalStorage()

            if item == "END":
                literalStorage()
                break

        # instruction from MOT table
        elif item in MOT:
            # Do some operation
            # print("{} in MOT".format(item))
            if line.index(item) == 1:
                label = line[0]
                label = adjustBytes(label)
                ST[label] = [hex(LC), 4, "R"]
            mystr = item + " "
            LC += MOT[item][1]
            # If the argument before comma is numeric then it is a register value...
            try:
                # if literal add it...
                if(line[-3].isnumeric()):
                    mystr += line[-3]+" , "
                else:
                    mystr += "__ , "
            except Exception as e:
                mystr += "__ , "
                pass
            if(line[-1].isnumeric()):
                mystr += line[-1]
            else:
                val = str(line[-1])
                # It can be some literal or some variable....
                for ch in ["F", "H", "D", "A"]:
                    if val.startswith("={}".format(ch)):
                        length = helper(ch)
                        if val not in LT:
                            LT[val[1:]] = ["-", length, "R"]
                        break
            mystr += "__"
            mystr += " ( {} , {} )".format(index_reg, base_reg)
            code.append(mystr)
            break
        # else:
        #     if item == ',':
        #         continue
        #     if item in ST or item in LT:
        #         continue

    # print("LC is: {}".format(LC))
    # print("Line {}: {}".format(count, line))

print("\n\t\t ------ Pass 1 Output ------\n")
print("Total length of the program is {} bytes".format(str(LC)))
print("\n\t\t Intermediate Code \n")
for i in code:
    print(i)

print("\n\t\t\t  Symbol Table(ST)\n")
print("--------------------------------------------------------------------")
print("|Symbol\t\t\tValue\t\tLength\t\tRecolation |")
print("--------------------------------------------------------------------")
for i in ST:
    print("|"+i+"\t\t"+str(ST[i][0])+"\t\t" +
          str(ST[i][1])+"\t\t"+ST[i][2]+"\t   |")

print("--------------------------------------------------------------------")

print("\n\t\t\tLiteral Table(LT)\n")
print("--------------------------------------------------------------------")
print("|Literal\t\tValue\t\tLength\t\tRecolation |")
print("--------------------------------------------------------------------")
for i in LT:
    if len(i) > 5:
        print("|"+i+"\t\t"+str(LT[i][0])+"\t\t" +
              str(LT[i][1])+"\t\t"+str(LT[i][2])+"\t   |")
    else:
        print("|"+i+"\t\t\t"+str(LT[i][0])+"\t\t" +
              str(LT[i][1])+"\t\t"+str(LT[i][2])+"\t   |")
print("--------------------------------------------------------------------")
file.close()

# ---------------------  Pass 2 code ------------------


def pass2AlignLC(item):
    global LC
    global LT
    global ST
    try:
        for ch in ["F", "H", "D"]:
            # It's a constant value...
            if item.startswith(ch):
                val = re.search("'(.*)'", item).group(1).strip().split(',')
                for v in val:
                    length = helper(ch)
                    # Check for alignment
                    alignLC(length)
                    st = str(LC) + '\t' + hex(int(v))
                    machine_code.append(st)
                    LC += length
            # If we have defined some storage space....
            elif item.endswith(ch):
                # count the required storage locations....
                locs = int(re.search("(.*){}".format(ch), item).group(1))
                length = helper(ch)
                # Check for alignment
                alignLC(length)
                return length*locs
            # It's a literal... Put it in literal table..
            elif item.startswith("={}".format(ch)):
                length = helper(ch)
                # Check for alignment
                alignLC(length)
                return length

    except Exception as e:
        print('Exception :', e)


def solveRegister(op):
    mystr = ""
    val = 0
    if(op.isnumeric()):
        mystr += op
        val = int(op)
    else:
        if op in ST:
            mystr += str(int(ST[op][0], 0))
            val = int(ST[op][0], 0)
        elif op[1:] in LT:
            mystr += str(int(LT[op][0], 0))
            val = int(ST[op][0], 0)
    return [val, mystr]


def solveIndex(op):
    base, offset = "", ""
    # If there is some A(label) or Symbol(label)...
    if ("(" in op and ")" in op) and "=" not in op:
        label = op[op.index("(")+1:op.index(")")]
        op = op[:op.index("(")]
        if adjustBytes(op) in ST:
            base, offset = map(str, determineBase(
                int(ST[adjustBytes(op)][0], 0)))
        index = str(int(ST[adjustBytes(label)][0], 0))
        return [int(offset)+int(base), "{} ( {} , {} )".format(offset, index, base)]
    elif op in ST:
        base, offset = map(str, determineBase(int(ST[op][0], 0)))
    elif op[1:] in LT:
        base, offset = map(str, determineBase(int(LT[op[1:]][0], 0)))

    return [int(offset)+int(base), "{} ( {} , {} )".format(offset, index_reg, base)]


def determineBase(symcontent):
    diff = 10000000
    base = 0
    offset = 0
    for i in BT:
        if BT[i][0] == "Y":
            if abs(BT[i][1]-symcontent) < abs(diff):
                base = i
                diff = (BT[i][1]-symcontent)
                offset = diff
    return [base, offset*-1]


index_reg = 0
base_reg = 0
base_content = 0

machine_code = []
file = open(str(sys.argv[1]), 'r')
count = 0
LC = 0


while True:
    count += 1
    line = file.readline().strip()
    if not line:
        break
    line = line.split(' ')

    for item in line:
        if item in POT:
            label = ""
            if line.index(item) == 1:
                label = line[0]

            if item == "DS" or item == "DC":
                op = line[-1]
                length = pass2AlignLC(op)
                if item == "DS":
                    machine_code.append(
                        (str(LC)+"\t"+str(length)+" bytes storage space alloted using DS"))
                    LC += length
            if item == "EQU":
                break
            if item == "USING":
                op1 = line[-3]
                op2 = line[-1]
                # if numeric value, means directly register number is specified...
                if(op2.isnumeric()):
                    base_reg = int(op2)
                # else it is a label...
                else:
                    base_reg = int(ST[adjustBytes(op2)][0], 0)
                BT[base_reg] = ["Y", "-"]
                # if '*' means use current value of LC
                if op1 == "*":
                    base_content = LC
                # else it is a label...
                else:
                    base_content = int(ST[adjustBytes(op1)][0], 0)
                BT[base_reg][1] = base_content
                break

            if item == "LTORG":
                LC += 4

                for lit in LT:
                    alignLC(LT[lit][1])
                    val = ""
                    try:
                        val = re.search("'(.*)'", lit).group(1)
                    except Exception as e:
                        val = re.search("\((.*)\)", lit).group(1)
                        val = ST[adjustBytes(val)][0]
                    machine_code.append((str(LC)+"\t"+hex(int(val, 0))))
                    LC += LT[lit][1]

            # DROP, then make the base register unavailable..
            if item == "DROP":
                BT[line[-1]][0] = "N"
                break

        elif item in MOT:
            label = ""
            if line.index(item) == 1:
                label = line[0]

            if item == "BNE":
                mystr = str(LC)+'\t' + MOT[item][0]+" 7 , " + \
                    solveIndex(adjustBytes(line[-1]))[1]
                machine_code.append(mystr)
                LC += MOT[item][1]
                break
            if item == "BR":
                mystr = MOT[item][0] + " " + \
                    str(determineBase(LC)[0])+" , "+line[-1]
                machine_code.append((str(LC)+'\t'+mystr))
                LC += MOT[item][1]
                break
            else:
                op1, op2 = line[-3], line[-1]
                try:
                    if adjustBytes(op1) in ST:
                        op1 = adjustBytes(op1)
                except Exception as e:
                    pass
                try:
                    if adjustBytes(op2) in ST:
                        op2 = adjustBytes(op2)
                except Exception as e:
                    pass
                instype = MOT[item][2]
                if instype == "RR" or instype == "SI":
                    mystr = MOT[item][0] + " "
                    ls1 = solveRegister(op2)
                    ls2 = solveRegister(op1)
                    mystr += ls2[1]+" , "+ls1[1]
                    machine_code.append((str(LC) + '\t' + mystr))
                    LC += MOT[item][1]
                    break
                if instype == "RX":
                    mystr = MOT[item][0] + " "
                    ls1 = solveRegister(op1)
                    ls2 = solveIndex(op2)
                    mystr += ls1[1] + " , " + ls2[1]
                    machine_code.append((str(LC) + '\t' + mystr))
                    LC += MOT[item][1]
                    break

print("\n\t\t ------ Pass 2 Output ------\n")

print("\n\t\t Machine Code \n")
for i in machine_code:
    print(i)

print("\n\t\t Base Table \n")
print("Reg. No.\tAvailability\tContents\n")
for i in BT:
    print(i, '\t\t', BT[i][0], '\t\t', BT[i][1])

file.close()
