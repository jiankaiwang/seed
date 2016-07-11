# seed
Provide libraries or packages for the software development in multiple programming languages.

### R
---

* Combination.r

| api | desc |
| -- | -- |
| getAllCombinationNumber(numeric SetNum, numeric selectedNum) | count all combinations without the permutation (計算不考慮排列下所有組合的數目) |
| getCombination(vector getSet, numeric getNum, numeric getWhichCombination) | return the combination set based on the order of the set (計算不考慮排列下所有組合的數目) |

* Network.r

| api | desc |
| -- | -- |
| networkAfterRemoveNodes(matrix originNetwork, vector selectedNodes, bool isDirected) | calculate a new network while removing several nodes and their linking nodes recursively (當移除數個啟始節點與遞迴移除其相連的其他節點所形成的網路) |