\ Model DEC
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  5 x_1 - 9 x_2 + 3 x_3
Subject To
 resource_cost_1: 4.4 x_1 - 3 x_2 + 2 x_3 <= 27
 resource_cost_2: 3 x_1 - 0.6 x_2 + x_3 <= 19
 resource_cost_3: 2 x_1 - 4 x_2 + 3.5 x_3 <= 20
Bounds
End
