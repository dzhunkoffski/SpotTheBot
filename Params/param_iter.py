# from types import new_class
import numpy as np
from numpy import sqrt
import math
import itertools
import csv
from multiprocessing import Process, Manager
import sys

from sympy import *
from sympy import solve, Poly, Eq, Function, exp
from sympy.abc import x, y, z, a, b
f = Function('f')

def ode2(params, p1, p2):
    p = [p1, p2]
    return [-p[0] + params[0] * p[0] ** 2 + 2 * params[1] * p[0] * p[1] + params[2] * p[1] ** 2,
           -p[1] + params[3] * p[0] ** 2 + 2 * params[4] * p[0] * p[1] + params[5] * p[1] ** 2]

def J2(params, p1, p2):
    p = [p1, p2]
    return [[ -params[0] + 2 * params[1] * p[0] + 2 * params[2] * p[1], 2 * params[2] * p[0] + 2 * params[3] * p[1]],
           [2 * params[5] * p[0] + 2 * params[6] * p[1], -params[4] + 2 * params[6] * p[0] + 2 * params[7] * p[1]]]

def estimate_roots(paramset, ODE, boundary_l, boundary_r, mesh_accuracy):
    mesh = np.array(np.meshgrid(np.arange(boundary_l, boundary_r, mesh_accuracy), np.arange(boundary_l, boundary_r, mesh_accuracy)))
    points = mesh.T.reshape(-1, 2)
    guess_list_x = []
    guess_list_y = []
    for p in points:
        if np.linalg.norm(ODE(paramset, p[0], p[1])) < 3 * mesh_accuracy:
            guess_list_x.append(p[0])
            guess_list_y.append(p[1])

    return guess_list_x, guess_list_y

def NR2(params, v0, accuracy, round_accuracy):
  it = 0
  v_old = v0
  try:
    v_new = v_old - np.dot(np.linalg.inv(J2(params, v_old[0], v_old[1])), ode2(params, v_old[0], v_old[1]))
  except np.linalg.LinAlgError:
    return [np.nan, np.nan]
  while np.linalg.norm(v_old - v_new) > accuracy and it <= 100:
    if it == 1000:
      return [0, 0]
    it += 1
    v_old = v_new
    try:
      v_new = v_old - np.dot(np.linalg.inv(J2(params, v_old[0], v_old[1])), ode2(params, v_old[0], v_old[1]))
    except np.linalg.LinAlgError:
      return [0, 0]
  return [round(v_new[0], round_accuracy), round(v_new[1], round_accuracy)]

x = Symbol('x', real=True)
y = Symbol('y', real=True)

import math

def correct_ode(param):
  # print("Params:", param)
  is_complex = 0
  is_singular = 0
  is_long = 0
  root_list = set()
  try:
    all_p = solve([-param[0] * x + param[1] * x ** 2 + 2 * param[2] * x * y + param[3] * y ** 2,
            -param[4] * y + param[5] * x ** 2 + 2 * param[6] * x * y + param[7] * y ** 2], set=True, real=True, minimal=True, quick=True )
    if len(all_p) == 0:
      is_long = 1
      root_list.add((0, 0))
    elif len(all_p[0]) == 1 and str(all_p[0][0]) == 'x':
      is_long = 1
      for p in all_p[1]:
        try:
          root_list.add((float(N(p[0])),0))
        except TypeError:
          root_list.add((0, 0))
    elif len(all_p[0]) == 1 and str(all_p[0][0] == 'y'):
      is_long = 1
      for p in all_p[1]:
        try:
          root_list.add((0, float(N(p[0]))))
        except TypeError:
          root_list.add((0, 0))
      # root_list = [(0, float(N(p[0]))) for p in all_p[1]]
    else:
      for p in all_p[1]:
        try:
          root_list.add((float(N(p[0])), float(N(p[1]))))
        except (IndexError, TypeError):
          root_list.add((0, 0))
  except KeyError:
      root_list.add((0, 0))
  root_list = list(root_list)
  eigs = []
  for point in root_list:
    try:
      eig = np.linalg.eigvals(J2(param, point[0], point[1]))
      if np.iscomplexobj(eig[0]) and np.iscomplexobj(eig[1]):
        is_complex = 1
      eigs.append(eig)
    except np.linalg.LinAlgError:
      eigs.append([np.nan, np.nan])
  
  result = list(param)
  if is_long == 0:
    result.append(len(root_list))
  else:
    result.append(999)
  for i in range(4):
    if i >= len(root_list):
      result.append(np.nan)
      result.append(np.nan)
    else:
      result.append(root_list[i][0])
      result.append(root_list[i][1])
  result.append(is_singular)
  result.append(is_complex)
  for i in range(4):
    if i >= len(eigs):
      result.append(np.nan)
      result.append(np.nan)
    else:
      result.append(eigs[i][0])
      result.append(eigs[i][1])

  return result
  
number_of_threads = 100
number_of_processes = 1
process_num = int(sys.argv[1])

step = 0.05
###

field = ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'number_of_solutions', 'x1', 'y1',
         'x2', 'y2', 'x3', 'y3', 'x4', 'y4', 'is_singular','is_complex', '1e1', '1e2', '2e1', 
         '2e2', '3e1', '3e2', '4e1', '4e2']

# print("Process", process_num, "will process from", (len(v) ** 8) // number_of_threads * process_num, "to", (len(v) ** 8) // number_of_threads * (process_num + 1), flush=True)

with open('results/prm_result'+'_step'+ str(step * 100) + '_' + str(process_num) + '.csv', 'w', newline='') as csvfile:
  write = csv.writer(csvfile)
  write.writerow(field)

  v = list(np.arange(0, 1.02, step))
  curr_iter = 0
  for p_set in itertools.product(v, v, v, v, v, v, v, v):
    if ((len(v) ** 8) // number_of_threads * process_num <= curr_iter) and (curr_iter < (len(v) ** 8) // number_of_threads * (process_num + 1)):
      print("Processing iteration num", curr_iter, flush=True)
      get_res = correct_ode(list(p_set))
      write.writerow(get_res)
    curr_iter += 1