import time
import random
import sys

wielkosc_tablicy = 2000000 # Ile liczb ma mieć tablica
maksymana_liczba = 1000000 # Zakres liczb od 1 do makszymalnej liczby
################################################################################
# Heapsort
################################################################################

def maxHeapify(A, i, heapsize):

    leftChild = 2*i+1
    rightChild = 2*i+2
    largest = i

    if(leftChild < heapsize and A[leftChild] > A[largest]):
        largest = leftChild
   
    if(rightChild < heapsize and A[rightChild] > A[largest]):
        largest = rightChild
    
    if(largest != i):
        A[largest], A[i] = A[i], A[largest]
        maxHeapify(A, largest ,heapsize)

def heapSort(A, heapsize):
    for i in range(heapsize // 2 - 1, -1, -1):
        maxHeapify(A, i, heapsize)

    for i in range(heapsize-1, 0, -1):
        A[0], A[i] = A[i], A[0]
        maxHeapify(A, 0, i)

# heapSort(tablica, rozmiar tablicy)
# heapSort(A, len(A))

################################################################################
# Quicsort - Lemuto
################################################################################

def partition(A, p, r):

    pivot = A[r]
    smaller =  p 
    
    for j in range(p, r):
        if A[j] <= pivot:
            A[j], A[smaller] = A[smaller], A[j]
            smaller = smaller + 1

    A[smaller], A[r] = A[r], A[smaller]
    return smaller


def quicksort(A, p, r):
    if p < r:
        q = partition(A, p, r)
        quicksort(A, p, q - 1)
        quicksort(A, q + 1, r)

# quicksort(tablica, pierwszy index = 0, ostatni index = rozmiar tablicy - 1)
# quicksort(A, 0, len(A) - 1)

################################################################################
# Mergesort + opis
################################################################################

# Merge sort dzieli tablicę tak długo aż utworzą się tablice jedno elementowe, które następnie po porównaniu elementów składa w całość.

def merge_sort(A):
    # Dopóki tablica nie ma jednego elementu kontynuuj dzielenie na części
    # w przeciwnym razie zwróć jednoelementową tablicę
    if len(A) <= 1:
        return A

    # Dzielenie listy na dwie połowy
    middle = len(A) // 2
    left_half = A[:middle]
    right_half = A[middle:]

    # Rekurencyjne sortowanie obu połówek powtarzane tak długo
    # dopóki warunek zakończenia programu będzie na to pozwalał
    left_half = merge_sort(left_half)
    right_half = merge_sort(right_half)

    # Scalanie posortowanych połówek
    return merge(left_half, right_half)


#funkcja scalania
def merge(left, right):
    merged = []
    i = j = 0

    # Porównywanie i scalanie elementów z obu połówek
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # Dołączanie pozostałych elementów jeśli jedna część (tablica)
    # była dłuższa od drugiej np jedna dwu, a druga trzy elementowa
    while i < len(left):
        merged.append(left[i])
        i += 1

    while j < len(right):
        merged.append(right[j])
        j += 1

    return merged

# A = merge_sort(A)

################################################################################
# Reverse Mergesort
################################################################################

# W celu utworzenia tablicy odwrotnie posortowanej można użyć 
# mergesorta z odwróconym znakiem

def reverse_merge_sort(A):
    if len(A) <= 1:
        return A

    middle = len(A) // 2
    left_half = A[:middle]
    right_half = A[middle:]

    left_half = reverse_merge_sort(left_half)
    right_half = reverse_merge_sort(right_half)

    return reverse_merge(left_half, right_half)

def reverse_merge(left, right):
    merged = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] >= right[j]: # <----------- O tutaj odwrócony
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    while i < len(left):
        merged.append(left[i])
        i += 1

    while j < len(right):
        merged.append(right[j])
        j += 1

    return merged

################################################################################
# Funkcje pomocnicze
################################################################################

def getHeapsortTime(A):
    start_time = time.time()

    heapSort(A, len(A))

    end_time = time.time()

    # print(A)
    execution_time = end_time - start_time
    return execution_time

def getQuicksortTime(A):
    start_time = time.time()

    quicksort(A, 0, len(A)-1)

    end_time = time.time()

    # print(A)
    execution_time = end_time - start_time
    return execution_time

def getMergesortTime(A):
    start_time = time.time()

    A = merge_sort(A)

    end_time = time.time()

    # print(A)
    execution_time = end_time - start_time
    return execution_time

# Wylosuj tablicę
def create_array(size):
    A = [random.randint(1, maksymana_liczba) for _ in range(size)]
    return A


# Losowa tablica
A1 = create_array(wielkosc_tablicy)
A_losowa1 = A1.copy()
A_losowa2 = A1.copy()
A_losowa3 = A1.copy()

# Posortowana tablica
A_posortowana1 = merge_sort(A1)
A_posortowana2 = A_posortowana1.copy()
A_posortowana3 = A_posortowana1.copy()

# Odwrotnie posortowana tablica
A_odwrotnie_posortowana1 = reverse_merge_sort(A1)
A_odwrotnie_posortowana2 = A_odwrotnie_posortowana1.copy()
A_odwrotnie_posortowana3 = A_odwrotnie_posortowana1.copy()


#Obejście limitu rekurencji w pythonie
print(sys.setrecursionlimit(100000))

# print(A_losowa1)
# print(A_losowa2)
# print(A_losowa3)
# print("")

# print(A_posortowana1)
# print(A_posortowana2)
# print(A_posortowana3)
# print("")

# print(A_odwrotnie_posortowana1)
# print(A_odwrotnie_posortowana2)
# print(A_odwrotnie_posortowana3)
# print("")

################################################################################
# To co nas interesuje
################################################################################

print("Losowe")
print("Heapsort  ", getHeapsortTime(A_losowa1))
print("Quicksort ", getQuicksortTime(A_losowa2))
print("Mergesort ", getMergesortTime(A_losowa3))
print("")

print("Posortowane")
print("Heapsort  ", getHeapsortTime(A_posortowana1))
# print("Quicksort ", getQuicksortTime(A_posortowana2))
print("Mergesort ", getMergesortTime(A_posortowana3))

print("")
print("Odwrotnie posortowane")
print("Heapsort  ", getHeapsortTime(A_odwrotnie_posortowana1))
# print("Quicksort ", getQuicksortTime(A_odwrotnie_posortowana2))
print("Mergesort ", getMergesortTime(A_odwrotnie_posortowana3))
