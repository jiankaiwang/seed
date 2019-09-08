# seedalgorithm.h



### Required libraries
---

* none

### API Description
---

* quicksort

```cpp
/*
  desc : quicksort algorithm
  parm :
  |- array_data : all data in array for sorting
  |- left : left boundary
  |- right : right boundary
  oupt : data array already sorted
  e.g. :
  int data[] = {1, -1, 2, 5, -3, 5, 7, 9, -10, 10};
  quicksort(data, 0, 10);
*/

void quicksort(int array_data[], int left, int right);
```

* binarysearch

```cpp
/*
  desc : binary search algorithm
  parm :
  |- array_data : searched data in array (notice : data must be sorted)
  |- search_number : checked number
  |- left_b : left boundary
  |- right_b : right boundary
  oupt : order in the data sequence or -1 stands for not in it
  e.g. :
  int data[] = {-10 -3 -2 -1 1 2 5 5 7 9};
  binarysearch(data, 7, 0, 10);   // return : 8
*/
    
int binarysearch(int array_data[], int search_number, int left_b, int right_b);
```