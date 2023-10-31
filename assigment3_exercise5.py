import gurobipy as gp
from gurobipy import GRB

""" a_11 = 4
a_22 = -1
a_33 = 3
b_1  = 30
b_2  = 20
c_2  = -8
c_3  = 4 """

a_11 = 4.4
a_22 = -0.6
a_33 = 3.5
b_1  = 27
b_2  = 19
c_2  = -9
c_3  = 3

processes           = [0, 1, 2]
price               = [5, c_2, c_3]
resource_cost_1     = [a_11, -3, 2]
resource_cost_2     = [3, a_22, 1]
resource_cost_3     = [2, -4, a_33]
available_resources = [b_1, b_2, 20]  

# Model
m = gp.Model("DEC")

# Create decision variables for the computers to produce
decision_vars = {}
for c in processes:
   decision_vars[c] = m.addVar(vtype=GRB.CONTINUOUS,lb=0, name='{}_{}'.format('x',c+1))
print(decision_vars)
# The objective is to maximize the profit
m.setObjective(sum(decision_vars[c]*price[c] for c in processes), GRB.MAXIMIZE)

# availability constraints
m.addConstr(gp.quicksum(resource_cost_1[c] * decision_vars[c] for c in processes)    <= available_resources [0], 'resource_cost_1')
m.addConstr(gp.quicksum(resource_cost_2[c] * decision_vars[c] for c in processes)    <= available_resources [1], 'resource_cost_2')
m.addConstr(gp.quicksum(resource_cost_3[c] * decision_vars[c] for c in processes)    <= available_resources [2], 'resource_cost_3')

m.write('test.lp')

m.optimize()

m.printAttr('X')

for v in m.getVars():
    print('{} = {}'.format(v.varName,v.x))
