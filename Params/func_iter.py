import numpy as np
from numpy import sqrt
import math
import itertools
import csv
import sys

def Dc(a1, d111, d112, d122, a2, d211, d212, d222, n1, n2):
    return (a1-a2) ** 2 + 4*(a2-a1)*(d111-d212)*n1+4*(a1-a2)*(d222-d112)*n2+4*((d111-d212)**2+4*d211*d112)*n1**2 + 8*((d111+d212)*(d112+d222)-2*(d111*d222-d211*d122))*n1*n2+4*((d112-d222)**2+4*d122*d212)*n2**2

def D1(a1, d111, d112, d122, a2, d211, d212, d222, n1, n2, dc):
    k = -(a1 + a2)/2 + (d111 + d212)*n1+(d112+d222)*n2
    if dc >= 0:
        return k - math.sqrt(dc)/2
    else:
        return k

def D2(a1, d111, d112, d122, a2, d211, d212, d222, n1, n2, dc):
    k = -(a1 + a2)/2 + (d111 + d212)*n1+(d112+d222)*n2
    if dc >= 0:
        return k + math.sqrt(dc)/2
    else:
        return k

number_of_threads = 100
number_of_processes = 1
process_num = int(sys.argv[1])
step = 0.1

field = ['a1', 'd111', 'd112', 'd122', 'a2', 'd211', 'd212', 'd222', 'n1', 'n2', 'Dc', 'D1', 'D2']

with open('results/fun_result'+'_step'+ str(step * 100) + '_' + str(process_num) + '.csv', 'w', newline='') as csvfile:
    write = csv.writer(csvfile)
    write.writerow(field)

    v = list(np.arange(0, 1.02, step))
    curr_iter = 0
    for p_set in itertools.product(v, v, v, v, v, v, v, v, v, v):
        if ((len(v) ** 10) // number_of_threads * process_num <= curr_iter) and (curr_iter < (len(v) ** 10) // number_of_threads * (process_num + 1)):
            print("Processing iteration num", curr_iter, flush=True)
            l = list(p_set)
            a1 = l[0]
            d111 = l[1]
            d112 = l[2]
            d122 = l[3]

            a2 = l[4]
            d211 = l[5]
            d212 = l[6]
            d222 = l[7]

            n1 = l[8]
            n2 = l[9]

            dc = Dc(a1, d111, d112, d122, a2, d211, d212, d222, n1, n2)
            d1 = D1(a1, d111, d112, d122, a2, d211, d212, d222, n1, n2, dc)
            d2 = D2(a1, d111, d112, d122, a2, d211, d212, d222, n1, n2, dc)
            l.append(dc)
            l.append(d1)
            l.append(d2)

            write.writerow(l)
        curr_iter += 1