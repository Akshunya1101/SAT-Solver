from msilib.schema import Directory
import sys
from copy import deepcopy
import os



def trim(cnf, x):  # To simplify the clauses in cnf by doing following operation
    cnf = [i for i in cnf if x not in i]  # If literal is present  in the clause, remove the clause
    cnf = [list(set(i).difference({-x})) for i in cnf]  # If negation of literal is present in clause then remove that clause
    return cnf

def add(cnf, x):  
    if [x] not in cnf: cnf.append([x])
    return cnf

def simplify(cnf):
    soln = set()
    units = [x for x in cnf if len(x)==1]
    while len(units)!=0:
        for unit in units:
            soln.add(unit[0])
            cnf = trim(cnf, unit[0])
        
        units = [x for x in cnf if len(x)==1]
    return soln, cnf


def dpll(cnf):
    lits, cnf = simplify(cnf)
    if [] in cnf: return 0
    if cnf==[]: return lits
    X = cnf[0][0]

    lits2 = dpll(add(cnf, X))
    if lits2 != 0: return lits.union(lits2)
    cnf.remove([X])
    lits3 = dpll(add(cnf, -X))
    if lits3 != 0: return lits.union(lits3)

    return 0


def main():   # This is the main function to take input, call the solving function and then print output in output file
    f = open("uuf50-02.cnf")
    cnf = []
    for line in f:
        if(line[0]=='c'):
            continue
        elif(line[0]=='p'):
            x=line.split()
            literals=int(x[2])
            continue
        else:
            x=line.split()
            clause=[]
            for i in x:
                    if(int(i)!=0):
                        clause.append(int(i))
            cnf.append(clause)
    f.close()
    print(cnf)
    solution=(dpll(cnf))
    with open("output.txt", 'w') as file:
        if(solution==0):
            file.write("Formula is UNSATISFIABLE")
        else:
            solution = list(solution)
            solution.sort(key = lambda x: abs(x))
            file.write(str(list(solution)))


main()