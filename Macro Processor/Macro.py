import re
import sys
# 80 bytes per entry for MDT
# MDT entry => | Index | Card |
MDT = []
# 12 bytes per entry for MNT
# MNT entry => | Index | Name | MDT index |
MNT = {}
MDTC = 1
MNTC = 1
# ALA entry => | Index | Argument |
ALA = {}
count = 1
ala = 1
copy = []


def makestr(length, word):
    repeat = "b" * (8-length)
    return ("\""+word+"{}\"").format(repeat)


def printMDT(MDT):
    print("\n\t***** MDT table *****\n")
    print("------------------------------------------------")
    print("Index\t\t\t Card\t\t\t")
    print("------------------------------------------------")
    for i in range(len(MDT)):
        print(i+1, "\t\t", MDT[i])
    print("------------------------------------------------")


def printMNT(MNT):
    print("\n\t***** MNT table ******\n")
    print("-----------------------------------")
    print("Index\t  Name\t\t MDT index")
    print("-----------------------------------")
    count = 1
    for word in MNT:
        print(count, "\t", makestr(len(word), word), "\t  ", MNT[word])
        count += 1
    print("-----------------------------------")


def printALA(ALA):
    print("\n\t***** ALA table *****")
    c = 1
    for i in ALA:
        print("\nALA for {} macro is: ".format(i))
        print("Index\t Argument")
        for j in range(len(ALA[i])):
            word = ALA[i][j]
            print(j+1, '\t', makestr(len(word), word))
        c += 1


file = open(str(sys.argv[1]), 'r')
while True:
    line = file.readline().strip()
    if not line:
        break
    print(count, line)
    count += 1
    line = line.strip().split(' ')
    punch = ""
    for i in range(len(line)):
        # If MACRO pseudo-op found....
        if line[i] == "MACRO":
            # Read next source card....
            line = file.readline().strip()
            spline = line.strip().split(' ')
            print(count, line)
            count += 1
            spline = [item for item in spline if item not in (',')]
            
            # Enter Macro Name & current value of MDTC in MNT entry number MNTC
            looplabel = False
            # If there is label before the macro name....
            if(spline[0].startswith('&')):
                MNT[spline[1]] = MDTC
                macro = spline[1]
                looplabel = True
            else:
                MNT[spline[0]] = MDTC
                macro = spline[0]
            # MNTC <-- MNTC + 1
            MNTC += 1
            # Prepare an argument list array
            ALA[macro] = []
            if looplabel:
                ALA[macro].append(spline[0][1:])
            else:
                ALA[macro].append("b"*8)

            for arg in range(1, len(spline)):
                if(spline[arg].startswith("&")):
                    argument = spline[arg][1:]
                    if "=" in list(argument):
                        argument = argument[:argument.index("=")]
                    ALA[macro].append(argument)
                    ala += 1
            # Enter macro name card into MDT
            MDT.append(line)
            # MDTC <-- MDTC + 1
            MDTC += 1
            line = file.readline().strip()
            print(count, line)
            count += 1
            spline = line.strip().split(' ')
            while("MEND" not in spline):
                # Read next source card....
                newline = ""
                for w in spline:
                    if w[1:] in ALA[macro]:
                        newline += "#"+str(ALA[macro].index(w[1:]))
                    else:
                        newline += w
                    newline += " "
                # Enter line into MDT
                MDT.append(newline)
                # MDTC <-- MDTC + 1
                MDTC += 1
                line = file.readline().strip()
                print(count, line)
                spline = line.strip().split(' ')
                count += 1
            # MEND is encountered...
            MDT.append("MEND")
            MDTC += 1
            break
        # Write a copy of source card...
        else:
            punch += line[i]+" "

    # Avoid copying blank lines
    if not(punch.strip() == ""):
        copy.append(punch)


print("\n\t############## PASS 1 ##############")

printMDT(MDT)
printMNT(MNT)
printALA(ALA)

output = []
print("\n\t############## PASS 2 ##############\n")
print("\rProgram copied from PASS 1 is:\n")
for i in range(len(copy)):
    print(i+1, copy[i])

for line in copy:
    # Read the source card copied from PASS 1 .....
    line = line.strip().split(' ')
    append = True
    # Search in MNT for match with operation code.....
    for macro in MNT:
        # If Macro name found .....
        if macro in line:
            # print("{} is in {}".format(macro, str(line)))
            MDTP = MNT[macro]-1
            definition = MDT[MDTP].split(' ')
            append = False
            # Setup argument list array...
            argALA = ALA[macro]
            # MDTP <-- MDTP + 1
            MDTP += 1
            start = 1
            # If the macro definition has some label....
            if definition.index(macro) == 1:
                # Replace the dummy label name with actual label name...
                argALA[argALA.index(definition[0][1:])] = line[0]
                start = 2

            for i in range(start, len(definition)):
                try:
                    if definition[i] == "," and line[i] == ",":
                        continue
                    if "=" in line[i]:
                        keyword = re.search("(.*)=", line[i]).group(1)[1:]
                        value = re.search("=(.*)", line[i]).group(1)
                        argALA[argALA.index(keyword)] = value
                    else:
                        if "=" not in definition[i]:
                            argALA[argALA.index(definition[i][1:])] = line[i]
                        else:
                            argALA[argALA.index(
                                definition[i][1:definition[i].index("=")])] = line[i]
                    ALA[macro] = argALA
                except Exception as e:
                    if(definition[i] == ","):
                        continue
                    keyword = re.search("(.*)=", definition[i]).group(1)[1:]
                    value = re.search("=(.*)", definition[i]).group(1)
                    argALA[argALA.index(keyword)] = value
                    pass
            argALA = ALA[macro]
            # Get line from MDT
            definition = MDT[MDTP].split(' ')
            # MDTP <-- MDTP + 1
            MDTP += 1
            while("MEND" not in definition):
                mystr = ""
                for spline in definition:
                    if "#" in spline:
                        mystr += argALA[int(spline[1:])] + " "
                    else:
                        mystr += spline + " "
                output.append(mystr)
                # Get line from MDT
                definition = MDT[MDTP].split(' ')
                # MDTP <-- MDTP + 1
                MDTP += 1
    if(append):
        output.append((' '.join(line)))


printALA(ALA)

print("\nExpanded macro code:\n")
for i in range(len(output)):
    print(i+1, output[i])

file.close()
