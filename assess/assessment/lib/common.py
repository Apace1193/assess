###############################################################################
#   common.py
# -----------------------------------------------------------------------------
#   Implements commonly needed library functions
#
###############################################################################

import abc

from copy import deepcopy


#******************************************************************************
#   CommonObjectInterface: Abstract
# -----------------------------------------------------------------------------
#   Implements commonly needed interface methods
#
#******************************************************************************
class CommonObjectInterface(object):

    __metaclass__ = abc.ABCMeta

    #******************************************************************************
    #   CommonObjectInterface::init
    # -----------------------------------------------------------------------------
    def __init__(self):
        pass


#******************************************************************************
#   Sortable: Abstract
# -----------------------------------------------------------------------------
#   Defines the sortable interface
#
#******************************************************************************
class Sortable(object):

    __metaclass__ = abc.ABCMeta

    #******************************************************************************
    #   Sortable::init
    # -----------------------------------------------------------------------------
    def __init__(self):
        pass

    #******************************************************************************
    #   Sortable::sortItems: Abstract
    # -----------------------------------------------------------------------------
    @abc.abstractmethod
    def sortItems(self):
        pass


#******************************************************************************
#   SortableList
# -----------------------------------------------------------------------------
#   A list that is sortable
#
#******************************************************************************
class SortableList(Sortable, CommonObjectInterface):

    #******************************************************************************
    #   SortableList::init
    # -----------------------------------------------------------------------------
    def __init__(self, items):
        self.items = items



#******************************************************************************
#   BubbleSort
# -----------------------------------------------------------------------------
#   An implementation of the popular sorting algorithm Bubble Sort
#
#******************************************************************************
class BubbleSort(CommonObjectInterface):

    #******************************************************************************
    #   BubbleSort::sort
    # -----------------------------------------------------------------------------
    def sort(self, itemsToSort):
        return self.doSort(itemsToSort)

    #******************************************************************************
    #   BubbleSort::doSort
    # -----------------------------------------------------------------------------
    def doSort(self, itemsToSort):
        listToSort = deepcopy(itemsToSort)
        theLengthOfTheItemsToSort = len(listToSort)
        endIndex = theLengthOfTheItemsToSort - 1
        myCurrentIndex = 0
        while endIndex > 1:
            myCurrentIndex = 0
            while myCurrentIndex < endIndex:
                if listToSort[myCurrentIndex] > listToSort[myCurrentIndex + 1]:
                    temp = listToSort[myCurrentIndex + 1]
                    listToSort[myCurrentIndex + 1] = listToSort[myCurrentIndex]
                    listToSort[myCurrentIndex] = temp
                myCurrentIndex += 1
            endIndex -= 1
        return listToSort


#******************************************************************************
#   SortableBubbleSortList
# -----------------------------------------------------------------------------
#   A lsit that is sortable that uses the BubbleSort algorithm
#
#******************************************************************************
class SortableBubbleSortList(SortableList, BubbleSort):

    def sortItems(self):
        self.items = self.sort(self.items)


#******************************************************************************
#   list
# -----------------------------------------------------------------------------
#   A convienence helper that allows the developer to not worry about the
#   nitty-gritty happening inside the complexities of the bubble sort algorithm
#
#******************************************************************************
def list(items=[]):
    return SortableBubbleSortList(items)
