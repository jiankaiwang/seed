namespace std {

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
    template<class T>
    void quicksort(T array_data[], int left, int right) {
        /*
        pivot : is the compare standard, is also the first number of the sequence
        i : find the larger number than the pivot from left to right, and is not the boundary
        j : find the smaller number than the pivot from right to left, and is not the boundary
        */
        int pivot, i, j;

        if (left < right)
        {

            // right + 1, because do while loop would first - 1
            i = left;
            j = right + 1;

            // set the first number as the pivot (standard)
            pivot = array_data[left];
            do {
                do i = i+1; while (array_data[i] < pivot);
                do j = j-1; while (array_data[j] > pivot);
                if(i<j) {swap(array_data[i], array_data[j]);}
            } while(i < j);

            // when i > j, pivot pointer would swap
            swap(array_data[left], array_data[j]);

            // sort smaller number
            quicksort(array_data, left, j-1);

            // sort larger number
            quicksort(array_data, j+1, right);

        }
    }

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
    template<class T>
    int binarysearch(T array_data[], T search_number, int left_b, int right_b) {
        // middle : the middle number in the searching sequence
        int middle(0);

        // control : the status flag to indicate whether it is searched
        int control(0);

        while(left_b <= right_b)
        {
            middle = (left_b + right_b)/2;

            if(array_data[middle] == search_number)
            {
                // the searching value == the middle value in the sequence
                control = 1;    // indicated flag
                return middle;
            }
            else if (array_data[middle] < search_number)
            {
                // searching number is larger than the middle one
                left_b = middle + 1;
            }
            else if (array_data[middle] > search_number)
            {
                // searching number is smaller than the middle one
                right_b = middle - 1;
            }
        }

        if(control == 0) { return -1; }
    }

}
