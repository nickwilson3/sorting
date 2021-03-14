#!/bin/python3
'''
Python provides built-in sort/sorted functions that use timsort internally.
You cannot use these built-in functions anywhere in this file.

Every function in this file takes a comparator `cmp` as input
which controls how the elements of the list should be compared againsti
each other:
If cmp(a, b) returns -1, then a < b;
if cmp(a, b) returns  1, then a > b;
if cmp(a, b) returns  0, then a == b.
'''

import random
import copy


def cmp_standard(a, b):
    '''
    used for sorting from lowest to highest

    >>> cmp_standard(125, 322)
    -1
    >>> cmp_standard(523, 322)
    1
    '''
    if a < b:
        return -1
    if b < a:
        return 1
    return 0


def cmp_reverse(a, b):
    '''
    used for sorting from highest to lowest

    >>> cmp_reverse(125, 322)
    1
    >>> cmp_reverse(523, 322)
    -1
    '''
    if a < b:
        return 1
    if b < a:
        return -1
    return 0


def cmp_last_digit(a, b):
    '''
    used for sorting based on the last digit only

    >>> cmp_last_digit(125, 322)
    1
    >>> cmp_last_digit(523, 322)
    1
    '''
    return cmp_standard(a % 10, b % 10)


def _merged(xs, ys, cmp=cmp_standard):
    '''
    Assumes that both xs and ys are sorted,
    and returns a new list containing the elements of both xs and ys.
    Runs in linear time.

    NOTE:
    In python, helper functions are frequently prepended with the _.
    This is a signal to users of a library that these functions are
    for "internal use only",
    and not part of the "public interface".

    This _merged function could be implemented as a local function within the
    merge_sorted scope rather than a global function.
    The downside of this is that the function can then not be tested on its
    own.
    Typically, you should only implement a function as a local function if it
    cannot function on its own
    (like the go functions from binary search).
    If it's possible to make a function stand-alone,
    then you probably should do that and write test cases for the stand-alone
    function.

    >>> _merged([1, 3, 5], [2, 4, 6])
    [1, 2, 3, 4, 5, 6]
    '''
    xs2 = 0
    ys2 = 0
    sorted_list = []
    while xs2 < len(xs) and ys2 < len(ys):
        compare = cmp(xs[xs2], ys[ys2])
        if compare == -1:
            sorted_list.append(xs[xs2])
            xs2 += 1
        elif compare == 1:
            sorted_list.append(ys[ys2])
            ys2 += 1
        elif compare == 0:
            sorted_list.append(xs[xs2])
            sorted_list.append(ys[ys2])
            xs2 += 1
            ys2 += 1
    sorted_list = sorted_list + xs[xs2:] + ys[ys2:]
    return sorted_list


def merge_sorted(xs, cmp=cmp_standard):
    '''
    Merge sort is the standard O(n log n) sorting algorithm.
    Recall that the merge sort pseudo code is:

        if xs has 1 element
            it is sorted, so return xs
        else
            divide the list into two halves left,right
            sort the left
            sort the right
            merge the two sorted halves

    You should return a sorted version of the input list xs.
    You should not modify the input list xs in any way.
    '''
    copy_xs = copy.deepcopy(xs)

    if len(xs) <= 1:
        return xs
    else:
        mid = len(copy_xs) // 2
        left_merge = merge_sorted(copy_xs[:mid], cmp)
        right_merge = merge_sorted(copy_xs[mid:], cmp)
        return _merged(left_merge, right_merge, cmp)


def quick_sorted(xs, cmp=cmp_standard):
    '''
    Quicksort is like mergesort,
    but it uses a different strategy to split the list.
    Instead of splitting the list down the middle,
    a "pivot" value is randomly selected,
    and the list is split into a "less than" sublist and a "greater than"
    sublist.

    The pseudocode is:

        if xs has 1 element
            it is sorted, so return xs
        else
            select a pivot value p
            put all the values less than p in a list
            put all the values greater than p in a list
            put all the values equal to p in a list
            sort the greater/less than lists recursively
            return the concatenation of (less than, equal, greater than)

    You should return a sorted version of the input list xs.
    You should not modify the input list xs in any way.
    '''
    less_list = []
    greater_list = []
    equal_list = []

    if len(xs) <= 1:
        return xs
    else:
        p_index = random.randint(0, len(xs) - 1)
        p_value = xs[p_index]
        for num in list(xs):
            compare = cmp(num, p_value)
            if compare == -1:
                less_list.append(num)
            if compare == 1:
                greater_list.append(num)
            if compare == 0:
                equal_list.append(num)
        less = quick_sorted(less_list, cmp)
        greater = quick_sorted(greater_list, cmp)
        return less + equal_list + greater


def quick_sort(xs, cmp=cmp_standard):
    '''
    EXTRA CREDIT:
    The main advantage of quick_sort is that it can be implemented "in-place".
    This means that no extra lists are allocated,
    or that the algorithm uses Theta(1) additional memory.
    Merge sort, on the other hand, must allocate intermediate lists for the
    merge step,
    and has a Theta(n) memory requirement.
    Even though quick sort and merge sort both have the same Theta(n log n)
    runtime,
    this more efficient memory usage typically makes quick sort faster ini
    practice.
    (We say quick sort has a lower "constant factor" in its runtime.)
    The downside of implementing quick sort in this way is that it will no
    longer be ai
    [stable sort](https://en.wikipedia.org/wiki/Sorting_algorithm#Stability),
    but this is typically inconsequential.

    Follow the pseudocode of the Lomuto partition scheme given on wikipedia
    (https://en.wikipedia.org/wiki/Quicksort#Algorithm)
    to implement quick_sort as an in-place algorithm.
    You should directly modify the input xs variable instead of returning a
    copy of the list.
    '''
