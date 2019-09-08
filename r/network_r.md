# Network.r



### API
---

* calculate a new network while removing several nodes and their linking nodes recursively (當移除數個啟始節點與遞迴移除其相連的其他節點所形成的網路) 

```R
matrix networkAfterRemoveNodes(
  matrix originNetwork, 
  vector selectedNodes, 
  bool isDirected
)
```

### Example
---

```R
# function example :
leftNetwork <- networkAfterRemoveNodes(net,selected,TRUE)

net
#    A B C D E F G H I
#  A 0 0 1 1 0 0 0 1 0
#  B 0 0 0 0 0 0 0 0 0
#  C 0 0 0 0 0 1 0 0 0
#  D 0 1 0 0 1 0 0 0 0
#  E 0 0 0 0 0 0 0 1 0
#  F 0 0 0 0 0 0 1 0 0
#  G 0 0 0 1 1 0 0 0 0
#  H 0 0 0 0 0 0 0 0 0
#  I 0 0 0 0 0 0 0 0 0

leftNetwork
# An object of class "classNetAfterNodeRevData"
# Slot "net":
#   A B C D E F G H I
# A 0 0 0 1 0 0 0 1 0
# B 0 0 0 0 0 0 0 0 0
# C 0 0 0 0 0 0 0 0 0
# D 0 0 0 0 0 0 0 0 0
# E 0 0 0 0 0 0 0 0 0
# F 0 0 0 0 0 0 0 0 0
# G 0 0 0 0 0 0 0 0 0
# H 0 0 0 0 0 0 0 0 0
# I 0 0 0 0 0 0 0 0 0

# Slot "sel":
# [1] "B" "C" "E"

# Slot "rmv":
# [1] "B" "C" "E" "F" "G"
```