import gurobipy as gp
from gurobipy import GRB


#computers = ['CP1', 'CP1', 'GP3', 'WS1', 'WS2']
computers = [0, 1, 2, 3, 4]
price = [60000, 40000, 30000, 30000, 15000]
drives = [0.3, 1.7, 0, 1.4, 0]
boards = [4, 2, 2, 2, 1]
cpu = [2, 1, 1, 1, 1]
orderquantity = [0, 500, 0, 500, 400]
partsavailable = [7000, 8000, 3000]     #cpu, boards, disc drives

# Model
m = gp.Model("DEC")

# Create decision variables for the computers to produce
produce = {}
for c in computers:
   produce[c] = m.addVar(vtype=GRB.INTEGER,lb=0, ub = 100000, name='{} {}'.format('produced',c+1))

# The objective is to maximize the profit
m.setObjective(sum(produce[c]*price[c] for c in computers), GRB.MAXIMIZE)

# Order quantities constraints
for c in computers:
   m.addConstr(orderquantity[c] <= produce[c])   

#We can add all the order quantity constraints at the same time with the following
#m.addConstrs((produce[c] >= orderquantity[c] for c in computers) , 'Order quantities')

# Parts availability constraints
m.addConstr(gp.quicksum(cpu[c] * produce[c] for c in computers)       <= partsavailable[0], 'cpu')
m.addConstr(gp.quicksum(boards[c] * produce[c] for c in computers)    <= partsavailable[1], 'boards')
m.addConstr(gp.quicksum(drives[c] * produce[c] for c in computers)    <= partsavailable[2], 'drives')

m.write('test.lp')

m.optimize()

m.printAttr('X')

#for v in m.getVars():
#    print('{} = {}'.format(v.varName,v.x))
