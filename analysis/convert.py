#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 14:33:59 2018

@author: suyog
"""

column = []

with open('/Users/suyog/test/colums', 'r') as file:
    for line in file:
        column.append(line[:-1])
        
data = []
with open('/Users/suyog/test/data', 'r') as file:
    for line in file:
        line = line[:-1]
        x = line.split(',')
        y = []
        for i in x:
            if(i == '?'):
                i = 0
            elif(i == 't'):
                i = 1
            y.append(i)
        data.append(y)


s = []
for d in data:
    m = []
    for i, x in enumerate(d):
        if(x == 1):
            x = column[i]
        m.append(x)
    s.append(m)
    
with open('/Users/suyog/test/output.csv', 'w+') as file:
    for i in s:
        file.write(','.join([str(j) for j in i])+'\n')