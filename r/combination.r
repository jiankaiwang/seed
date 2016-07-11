##########################################################################
# github : https://github.com/jiankaiwang/DetailScience
# classification : math
# description : functions related to the combination of elements
# 
# function description :
# - getAllCombinationNumber
#   count all combinations without the permutation
#
# - getCombination :
#   return the combination set based on the order of the set
#   for example: the 3rd combination order from vector c(1,2,3,4,5) 
#                as three elements in the set
#   1st order : 1,2,3
#   2nd order : 1,2,4
#   3rd order : 1,2,5
#   the function would return c(1,2,5)
#   when the input collection is c('a','b','c','d','e'), 
#   return would be c('a','b','e')
#
# - getRandomSet : 
#   return a matrix conserving all combination set
#
# function usage :
# - numeric getAllCombinationNumber(numeric cntEles, numeric eleInSet)
#   (1) cntEles (as integer) : count of total elements
#   (2) eleInSet (as integer) : count of elements selected in the set
#
# - vector getCombination(vector eleColl, numeric eleInSet, numeric setOrd)
#   (1) eleColl (as vector) : a collection with all elements
#   (2) eleInSet (as integer) : count of elements selected in the set
#   (3) setOrd (as integer) : the combination order
#
# - matrix getRandomSet(vector eleColl, numeric eleCountInSet, numeric getTtlSetNum, logical retByIndex)
#   (1) eleColl (as vector) : a collection with all elements
#   (2) eleCountInSet (as integer) : count of elements selected in the set
#   (3) getTtlSetNum (as integer) : total set count
#   (4) retByIndex (as bool) : return by index or name in the set
#
# function example :
# - allCombNumber <- getAllCombinationNumber(80,4)
#   return 1581580
#
# - getEleSet <- getCombination(c('a','b','c','d','e'),3,7)
#   return c("b" "c" "d")
#
# - getRandomSet(c('a','b','c','d','e'),3,2,FALSE)
#        [,1] [,2] [,3]
#   [1,] "b"  "c"  "e" 
#   [2,] "b"  "c"  "d" 
##########################################################################

getAllCombinationNumber <- function(setNum, selectedNum) {
  leftNum <- min(setNum - selectedNum, selectedNum)
  res <- 1
  divNum <- 1
  for(i in setNum:(max(setNum - selectedNum, selectedNum)+1)) {
    res <- res * i
    if(res %% divNum == 0) {
      res <- res / divNum
      divNum <- divNum + 1
    }
  }
  divLeftNum <- 1
  if(divNum < leftNum) {
    for(i in divNum : leftNum) {
      divLeftNum <- divLeftNum * i
    }
  }
  return(res/divLeftNum)
}

getCombination <- function(getSet, getNum, getWhichCombination) {
  # initial
  # as stack
  retList <- 1:getNum
  count <- 1
  countLast <- 0
  
  # others
  while(count < getWhichCombination) {
    # pop the last one
    popValue <- retList[length(retList)]
    retList <- retList[1:length(retList)-1]
    
    # get new value
    if(popValue + 1 <= length(getSet)) {
      if(countLast == 0) {
        retList <- c(retList,popValue + 1)
      } else {
        if(popValue + 1 == length(getSet)) {
          countLast <- countLast + 1
          next
        }
        retList <- c(retList, (popValue + 1) : (popValue + 1 + countLast))
      } 
      
      # initial for next multiple pops
      countLast <- 0
    } else {
      countLast <- countLast + 1
      next
    }
    
    # count add 1
    count <- count + 1
  }
  
  return(getSet[retList])
}

getRandomSet <- function(getSet, eleCountInSet, getTtlSetNum, retByIndex) {
  # check parameters
  if(getTtlSetNum > getAllCombinationNumber(length(getSet),eleCountInSet)) {
    return("getTtlSetNum is larger than all combination set count")
  } else if (length(getSet) < eleCountInSet) {
    return("total elements in data set is smaller than the getTtlSetNum value")
  }
  
  # as return matrix
  retSet <- matrix(c(1:eleCountInSet),nrow=1,ncol=eleCountInSet)
  
  tmpList <- c()
  tmpCheckFlag <- 0
  setIndex <- 1
  
  while(setIndex <= getTtlSetNum) {
    # initialization
    tmpList <- sort(sample(c(1:length(getSet)),eleCountInSet))
    tmpCheckFlag <- 0
    
    # check whether the same combination exists
    for(checkIndex in 1:nrow(retSet)) {
      if(length(which((retSet[checkIndex,] == tmpList) == TRUE)) == eleCountInSet) {
        tmpCheckFlag <- 1
        break
      }
    }
    
    if(tmpCheckFlag == 1) {
      # there is one combination same with new set
      next
    }
    
    if(retByIndex == TRUE) {
      retSet <- rbind(retSet, tmpList)
    } else {
      retSet <- rbind(retSet, getSet[tmpList])
    }
    
    setIndex <- setIndex + 1
  }
  
  # the first row is self-assigned for rbinding usage
  retSet <- retSet[-1,]
  
  if(is.numeric(retSet)) {
    return(matrix(retSet,nrow=nrow(retSet),ncol=eleCountInSet))
  } else {
    return(retSet)
  }
}




