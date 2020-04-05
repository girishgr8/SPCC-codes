file = open('first_follow_input.txt', 'r')
grammar = dict()
first = dict()
follow = dict()

# Read the grammar rules from the input file #
def inputGrammar():
	while True:
		line = file.readline()
		if not line:
			break
		line = line.strip().split('->')
		NT = line[0].strip()
		rules = list()
		for r in line[1].split('|'):
			rules.append(r.strip())
		grammar[NT] = rules
		first[NT] = list()
		follow[NT] = list()

# Print the inputted grammar rules #
def printGrammar():
	print("\n\t--- Grammar rules ---")
	for NT in grammar:
		rules = grammar[NT]
		print("{}->".format(NT),end=" ")
		for i in range(len(rules)):
			if i==len(rules)-1:
				print(rules[i],end="\n")
			else:
				print(rules[i],end=" | ")

# Recursive function to find first(X) #
def firstRec(NT):
	symbol = first[NT][0]
	if symbol not in grammar.keys():
		return first[NT]
	
	return firstRec(symbol)

def findFirst():
	for NT in grammar:
		for rule in grammar[NT]:
			if rule[0] == 'e': first[NT].append('e')
			else: first[NT].append(rule[0])

	for NT in first:
		s = set()
		first[NT] = set(firstRec(NT))

def findFollow():
	for NT in follow:
		follow[NT].append('$')
	for prod in grammar[NT]:
		


def printFirstFollow():
	print("\n\t\t--- First Table ---")
	for NT in first:
		print("First of {} is: ".format(NT),first[NT])

	print("\n\t\t--- Follow Table ---")
	for NT in follow:
		print("Follow of {} is: ".format(NT),follow[NT])

		
inputGrammar()
printGrammar()
findFirst()
findFollow()
printFirstFollow()

