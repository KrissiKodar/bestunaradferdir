import gurobipy as gp
from gurobipy import GRB

processes = [0, 1, 2]
price = [200, 60, 205]
crude_A = [3, 1, 5]
crude_B = [5, 1, 3]
barrelsavailable= [8E6, 5E6]     #cpu, boards, disc drives

# Model
m = gp.Model("DEC")

# Create decision variables for the computers to produce
produce = {}
for c in processes:
   produce[c] = m.addVar(vtype=GRB.INTEGER,lb=0, name='{} {}'.format('Process',c+1))
# The objective is to maximize the profit
m.setObjective(sum(produce[c]*price[c] for c in processes), GRB.MAXIMIZE)

# availability constraints
m.addConstr(gp.quicksum(crude_A[c] * produce[c] for c in processes)    <= barrelsavailable[0], 'crude_A')
m.addConstr(gp.quicksum(crude_B[c] * produce[c] for c in processes)    <= barrelsavailable[1], 'crude_B')

m.write('test.lp')

m.optimize()

m.printAttr('X')

#for v in m.getVars():
#    print('{} = {}'.format(v.varName,v.x))
