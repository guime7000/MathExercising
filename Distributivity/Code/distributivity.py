#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 14:17:35 2020

@author: tom

Randomly creates several polynoms (a+b)(c+d) and develops it using double
distributivity to obtain ac + ad + bc + bd

User can choose the number of polynoms of each difficulty he wants by entering
several couples (difficulty,number) (0 <= difficulty <= 4, 1<= number <= 50)

Difficulty choice:
    0 = very simple distributivity: no symbol factorised + positive factors
    1 = very simple distributivity: no symbol factorised + relative nb factors
    2 = simple distributivity (symbol possibly factorised)
    3 = double distributivity with max symbol power equals to 1
    4 = double distributivity with symbol power possibly greater than 1
    
Solution detail:
    0 = only the result
    1 = resolution stages with no ordering before reduction
    2 = resolution stages + ordering by symbol power before reduction    

*************    
-> function distributes(a,b)

simple distributivity k(a+b) = ka + kb

a: [[int, int],...] lists containing coeff and symbol power of first factor
b: [[int, int],...] lists containing coeff and symbol power of second factor
 
returns a list of lists (stage 1 of resolution) containing ka, kb and the relative 
powers of symbol

**************
-> function reduces(a)

concatenates and reduces two lists containing coeffs and power of symbol
outputs an ordered list of decreasing power of symbol

**************

returns a list (stage 2 of resolution) sorted by growing symbol power
 


**************
-> function latex_code()
Produces a latex file with detailed resolution stages
"""

from random import randint, choice
from itertools import repeat

from pylatex import Document, MiniPage, LineBreak, VerticalSpace, NoEscape
from pylatex import Section, Subsection, Tabular, Math, Command
from pylatex.utils import italic
import os
import string

def generate_poly(poly_diff):
     
    symbol=choice(['x','y','z','t'])
    first_factor, second_factor, coeffs=[],[],[]
        
    if poly_diff == 0:
        first_factor = [[randint(2,50),0]]
        second_factor.append([randint(2,50),choice([0,1])])
        if second_factor[0][1] == 1 :
            second_factor.append([randint(2,50),0])
        else :
            second_factor.append([randint(2,50),1])
                
    elif poly_diff == 1:
        coeffs=[c for c in range(-50,0)]+[d for d in range(1,51)]
        first_factor = [[choice(coeffs),0]]
        second_factor.append([choice(coeffs),choice([0,1])])
        if second_factor[0][1] == 1 :
            second_factor.append([choice(coeffs),0])
        else :
            second_factor.append([choice(coeffs),1])
    
    elif poly_diff == 2:
        coeffs=[c for c in range(-50,0)]+[d for d in range(1,51)]
        first_factor = [[choice(coeffs),choice([0,1])]]
        second_factor.append([choice(coeffs),choice([0,1])])
        if second_factor[0][1] == 1 :
            second_factor.append([choice(coeffs),0])
        else :
            second_factor.append([choice(coeffs),1])
    
    elif poly_diff == 3:
            coeffs=[c for c in range(-50,0)]+[d for d in range(1,51)]
            first_factor = [[choice(coeffs),choice([0,1])]]
            if first_factor[0][1] == 1:
                first_factor.append([choice(coeffs),0])
            else:
                first_factor.append([choice(coeffs),1])
                
            second_factor.append([choice(coeffs),choice([0,1])])
            if second_factor[0][1] == 1 :
                second_factor.append([choice(coeffs),0])
            else :
                second_factor.append([choice(coeffs),1])

    elif poly_diff == 4:
            coeffs=[c for c in range(-50,0)]+[d for d in range(1,51)]
            first_factor = [[choice(coeffs),randint(0,6)],\
                             [choice(coeffs),randint(0,6)]]
            while first_factor[0][1] == first_factor[1][1]:
                first_factor = [[choice(coeffs),randint(0,6)],\
                                 [choice(coeffs),randint(0,6)]]    
                            
            second_factor=[[choice(coeffs),randint(0,6)],\
                            [choice(coeffs),randint(0,1)]]
            while second_factor[0][1] == second_factor[1][1]:
                second_factor = [[choice(coeffs),randint(0,6)],\
                                 [choice(coeffs),randint(0,6)]]
    
    return first_factor, second_factor

def distributes(factor1,factor2):
    
    distr_output=[] # ka and kb list*
    for j in range(len(factor1)):
        for i in range(len(factor2)):
            product=factor1[j][0]*factor2[i][0] # polynomial coeffs product
            power=factor1[j][1]+factor2[i][1] # symbol power
            distr_output.append([product,power])   
    return distr_output

def reduces(poly) :
    poly.sort(key=lambda power : power[1], reverse= True)
    reduced_out=[]
    temp_power = poly[0][1]
   
    while temp_power >=0 :
        temp_sum=[]
        for i in range(len(poly)):
            if poly[i][1] is temp_power :
                temp_sum.append(poly[i][0])
       
#                print(f"toto : {temp_sum}")
#                print(sum(temp_sum))
        reduced_out.append([sum(temp_sum),temp_power])
        temp_power -= 1
        
    return reduced_out

def coeff_convert(coeff,symbol,stage=2):
    """
    Converts the list containing the couples [polynomial coefficient / power]
    to string for Latex mathematical scripting
    
    coeff : list of couples [coeff,power]
    symbol : string for polynomial symbol
    stage : current number of resolution stage. For the first stage, 
    parenthesis must be added for negative coefficients in the second factor
    of the polynom.
    """
    
    output=[]
          
    for factor in coeff :
        
        if factor[0] < 0:
            if stage == 1 :    
                if factor[0] == -1 :
                    if factor[1] == 0:
                        output.append(f"(-1)")
                    elif factor[1] == 1:
                        output.append(f"(-{symbol})")
                else:
                    if factor[1] == 0:
                        output.append(f"({factor[0]})")
                    elif factor[1] == 1:
                        output.append(f"({factor[0]}{symbol})")
                    else:
                        output.append(f"({factor[0]}"+f"{symbol}^{factor[1]})")
            if stage == 2 :
                if factor[0] == -1 :
                    if factor[1] == 0:
                        output.append(f"-1")
                    elif factor[1] == 1:
                        output.append(f"-{symbol}")
                else:
                    if factor[1] == 0:
                        output.append(f"{factor[0]}")
                    elif factor[1] == 1:
                        output.append(f"{factor[0]}{symbol}")
                    else:
                        output.append(f"{factor[0]}"+f"{symbol}^{factor[1]}")
            
        else:   
            if stage == 1:
                if factor[0] == 0:
                    pass
                elif factor[0] == 1:
                    if factor[1] == 0:
                        output.append(f"1")
                    elif factor[1] == 1:
                        output.append(f"{symbol}")
                    else :
                        output.append(f"{symbol}^{factor[1]}")
                elif factor[1] == 0:
                    output.append(f"{factor[0]}")
                elif factor[1] == 1:
                    output.append(f"{factor[0]}"+f"{symbol}")
                else:
                    output.append(f"{factor[0]}"+f"{symbol}^{factor[1]}")
            else:
                if factor[0] == 0:
                    pass
                elif factor[0] == 1:
                    if factor[1] == 0:
                        output.append(f"+1")
                    elif factor[1] == 1:
                        output.append(f"+{symbol}")
                    else :
                        output.append(f"+{symbol}^{factor[1]}")
                elif factor[1] == 0:
                    output.append(f"+{factor[0]}")
                elif factor[1] == 1:
                    output.append(f"+{factor[0]}"+f"{symbol}")
                else:
                    output.append(f"+{factor[0]}"+f"{symbol}^{factor[1]}")
    return output
    
def rid_of_first_plus(coeff):
    
    if '+' in str(coeff[0]):
        coeff[0]=coeff[0].split("+")[1]
    return coeff

def latex_code_stage0(length_factor1,length_factor2,factor,symbol) :
    
    output=''
        
    factor1_tmp = factor[:length_factor1]
    factor1_tmp = coeff_convert(factor1_tmp,symbol)
    factor1_tmp = rid_of_first_plus([x for item in factor1_tmp
                for x in repeat(item, length_factor2)])
    
    factor2_tmp = rid_of_first_plus(factor[length_factor1:])
    factor2_tmp += factor2_tmp
    factor2_tmp = coeff_convert(factor2_tmp,symbol,1)
  
    for item1,item2 in zip(factor1_tmp,factor2_tmp):
        output=output+f"{item1} \\times {item2}"
    
    output="$"+ output +"$"
    
    return output

def latex_code(factor) :

    factor=rid_of_first_plus(factor)
    return "$"+ "".join(factor) +"$"

def latex_code_ini(factor1, factor2, poly_diff) :

    factor1=rid_of_first_plus(factor1)
    factor2=rid_of_first_plus(factor2)
    out = "$(" + "".join(factor1) + ")(" + "".join(factor2) + ")$"
    if poly_diff < 3:
        out = "$" + "".join(factor1) + "(" + "".join(factor2) + ")$"
    return out
 
def generate_labels(tata,titi,toto,toutou,tutu,diff):
    geometry_options = {"margin": "0.5in"}
    doc = Document(geometry_options=geometry_options)

    doc.change_document_style("empty")

    doc.preamble.append(Command('title', 'Distributivité'))
    doc.preamble.append(Command('author', 'Niveau de difficulté : debutant'))
    doc.preamble.append(Command('date', NoEscape(r"{}")))
    doc.append(NoEscape(r'\maketitle'))

    with doc.create(Section("Enoncé")):
        doc.append(NoEscape("Développer et réduire les expressions suivantes :"))
        doc.append("\n")
        doc.append("\n")        
        
        for i in range(len(tata)):
            with doc.create(MiniPage(width=r"0.5\textwidth")):
                doc.append(NoEscape(f"{string.ascii_uppercase[i]}={tata[i]}"+"\\\\"))
            if (i % 2) == 1:
                doc.append(NoEscape("\\\\"))
                
    doc.append(NoEscape("\\newpage"))
    
    with doc.create(Section("Corrigé")):
        for i in range(len(tata)):
            if diff <= 2 :
                with doc.create(MiniPage(width=r"0.5\textwidth")):
                    doc.append(NoEscape(f"{string.ascii_uppercase[i]}={tata[i]}"+"\\\\"))
                    doc.append(NoEscape(f"{string.ascii_uppercase[i]}={titi[i]}"+"\\\\"))
                    doc.append(NoEscape(f"{string.ascii_uppercase[i]}={toto[i]}"+"\\\\"))
                    if toutou[i] != toto[i]:
                        doc.append(NoEscape(f"{string.ascii_uppercase[i]}={toutou[i]}"+"\\\\"))

                if (i % 2) == 1:
                    doc.append(NoEscape("\\\\"))

            else :
                with doc.create(MiniPage(width=r"0.5\textwidth")):
                    doc.append(NoEscape(f"{string.ascii_uppercase[i]}={tata[i]}"+"\\\\"))
                    doc.append(NoEscape(f"{string.ascii_uppercase[i]}={titi[i]}"+"\\\\"))
                    doc.append(NoEscape(f"{string.ascii_uppercase[i]}={toto[i]}"+"\\\\"))
                    if toutou[i] != toto[i]:
                        doc.append(NoEscape(f"{string.ascii_uppercase[i]}={toutou[i]}"+"\\\\"))                    
                    doc.append(NoEscape(f"{string.ascii_uppercase[i]}={tutu[i]}"+"\\\\"))

            if (i % 2) == 1:
                doc.append(NoEscape("\\\\"))

    doc.generate_pdf("distributivite_debutant", clean_tex=False)



      

    
######## PROGRAM ################    
    
    
poly_difficulty = 3 # difficulty of the polynom
poly_numbers = 10   # number of polynoms to produce
solution = 2           # solution details level

poly_ini = []
stage0_latex = []
stage1_latex = []
stage2_srtd_latex = []
stage2_latex = []

for nb_poly in range(poly_numbers):
    
    symbol=choice(['x','y','z','t'])
    factor1, factor2 = generate_poly(poly_difficulty)
    nb_factor1=len(factor1)
    nb_factor2=len(factor2)

#### Latex scripting ####

    stage0 = factor1 + factor2
    poly_ini +=[latex_code_ini(coeff_convert(factor1,symbol),
                            coeff_convert(factor2,symbol),poly_difficulty)]

    stage0_latex += [latex_code_stage0(nb_factor1,nb_factor2,stage0,symbol)]

    stage1 = distributes(factor1,factor2)
    stage1_latex += [latex_code(coeff_convert(stage1,symbol))]

    stage2 = sorted(stage1,key=lambda power : power[1], reverse= True)
    stage2_srtd_latex += [latex_code(coeff_convert(stage2,symbol))]
    stage2 = reduces(stage2)
    stage2_latex += [latex_code(coeff_convert(stage2,symbol))]

generate_labels(poly_ini,stage0_latex,stage1_latex,stage2_srtd_latex,
                stage2_latex,poly_difficulty)

