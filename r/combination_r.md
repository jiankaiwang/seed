# Combination.r



### API
---

* count all combinations without the permutation (計算不考慮排列下所有組合的數目)

```R
numeric getAllCombinationNumber(
  numeric SetNum, 
  numeric selectedNum
) 
```

* return the combination set based on the order of the set (計算不考慮排列下所有組合的數目)

```R
vector getCombination(
  vector getSet, 
  numeric getNum, 
  numeric getWhichCombination
)
```

* return the random combination set as a matrix

```R
matrix getRandomSet(
  vector eleColl, 
  numeric eleCountInSet, 
  numeric getTtlSetNum, 
  logical retByIndex
)
```

### Example
---

```R
# return 1581580
allCombNumber <- getAllCombinationNumber(80,4)

# return c("b" "c" "d")
getEleSet <- getCombination(c('a','b','c','d','e'),3,7)

#        [,1] [,2] [,3]
#   [1,] "b"  "c"  "e" 
#   [2,] "b"  "c"  "d" 
getRandomSet(c('a','b','c','d','e'),3,2,FALSE)
```






