##########################################################################
# github : https://github.com/jiankaiwang/DetailScience
# classification : math
# description : calculate the network in matrix
#
# class description :
# - networkAfterRemoveNodesRetData
#		(1) net : perserve the network after removing nodes recursively
#		(2) sel : perserve the origin nodes for absolutely deletion
#		(3) rmv : perserve nodes for deletion finally
# 
# function description :
# - networkAfterRemoveNodes
#   (1) directed : row is the source and column is the target (or destination)
#		(2) return : returned object is "networkAfterRemoveNodesRetData" data type
#
# function usage :
# - networkAfterRemoveNodesRetData networkAfterRemoveNodes(matrix originNetwork, vector selectedNodes, logical isDirected)
#   (1) originNetwork (as matrix) : a matrix conserving edge information
#   (2) selectedNodes (as vector) : a vector listing all nodes are removed
#   (3) isDirected (as boolean) : whether the matrix is directed or not
#
# function example :
# - leftNetwork <- networkAfterRemoveNodes(net,selected,TRUE)
#
# > net
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
#
# > leftNetwork
# An object of class "classNetAfterNodeRevData"
#	Slot "net":
#		A B C D E F G H I
#	A 0 0 0 1 0 0 0 1 0
#	B 0 0 0 0 0 0 0 0 0
#	C 0 0 0 0 0 0 0 0 0
#	D 0 0 0 0 0 0 0 0 0
#	E 0 0 0 0 0 0 0 0 0
#	F 0 0 0 0 0 0 0 0 0
#	G 0 0 0 0 0 0 0 0 0
#	H 0 0 0 0 0 0 0 0 0
#	I 0 0 0 0 0 0 0 0 0

#	Slot "sel":
#	[1] "B" "C" "E"

#	Slot "rmv":
#	[1] "B" "C" "E" "F" "G"
##########################################################################

networkAfterRemoveNodesRetData <- setClass(
  # Set the name for the class
  "classNetAfterNodeRevData",
  
  # Define the slots
  slots = c(
    net = "matrix",
    sel = "vector",
    rmv = "vector"
  ),
  
  # Set the default values for the slots. (optional)
  prototype=list(
    net = matrix(c(1:4),nrow=2,ncol=2,dimnames = list(c("A","B"),c("A","B"))),
    sel = c("A"),
    rmv = c("A")
  ),
  
  # Make a function that can test to see if the data is consistent.
  # This is not called if you have an initialize function defined!
  validity=function(object)
  {
    if((length(object@net) < 1) || (length(object@sel) < 1) || (length(object@rmv) < 1)) {
      return("Either one of net, selected or removed is not empty.")
    }
    return(TRUE)
  }
)

networkAfterRemoveNodes <- function(originNetwork, selectedNodes, isDirected) {
  
  # continuously reconstruct the network
  net <- originNetwork
  
  # construct mask network
  maskOperated <- originNetwork
  
  # selected items
  selected <- selectedNodes
  
  # initial flag
  continueFlag = 1
  
  while(continueFlag == 1) {
    
    # initial mask matrix
    maskOperated[,] <- 0
    
    # drug would cause edge missing
    maskOperated[selected,] <- 1
    if(! isDirected) {
      maskOperated[,selected] <- 1
    }
    
    left <- matrix(
      bitwAnd(net,maskOperated),
      nrow=nrow(net),
      ncol=ncol(net),
      dimnames = list(
        rownames(net),
        colnames(net)
      )
    )
    
    fetNew <- which(left[,] == 1)
    sourceName <- rownames(net)
    itemName <- colnames(net)
    newSelect <- selected
    
    # check whether new node is found
    for(item in fetNew) {
      # r default is column-based, not row-based
      sourceNode <- sourceName[item %% nrow(net)]
      checkNode <- itemName[ceiling(item / nrow(net))]
      
      if(length(which(net[,checkNode] == 1)) > 1) {
        # there are others existing source
        # origin Network must be modified to remove the edge singlely
        # but the node does not be removed
        net[sourceNode,checkNode] <- 0
        next
      }
      
      # no matter whether node is removed, edge must be removed
      net[sourceNode,checkNode] <- 0

      # there are no other source, this node should be added for removing
      if(checkNode %in% newSelect) {
        next
      } else {
        # add new selected nodes
        newSelect <- c(newSelect,checkNode)
      }

    }
    
    if(length(newSelect) != length(selected)) {
      # new nodes are added
      selected <- newSelect
    } else {
      # not found new nodes
      continueFlag <- 0
    } 
    
    #print(newSelect)   
  }
  
  # restore the network
  mask <- originNetwork
  mask[,] <- 1
  mask[selected,] <- 0
  # if the destination node is removed
  # the edge between the source and the destination is also removed
  mask[,selected] <- 0
  leftNet <- matrix(
    bitwAnd(originNetwork,mask),
    nrow=nrow(originNetwork),
    ncol=ncol(originNetwork),
    dimnames = list(
      rownames(originNetwork),
      colnames(originNetwork)
    )
  )

  return(networkAfterRemoveNodesRetData(net=leftNet,sel=selectedNodes,rmv=selected))
}
