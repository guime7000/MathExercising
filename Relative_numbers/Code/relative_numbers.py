#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 21:13:21 2020

@author: tom

working on addition and substraction of relative numbers


user specifies:
    - the number of terms of the operation (nb_terms)
    - the number of operations to be generated (nb_ope)

"""

from random import randint, choice
from itertools import repeat
import string
import os

from pylatex import Document, MiniPage, LineBreak, VerticalSpace, NoEscape
from pylatex import Section, Subsection, Tabular, Math, Command
from pylatex.utils import italic

def generate_operation(nb_terms,nb_ope):
    """
    randomly generates nb_ope operations composed of nb_terms terms
    returns:
        - couple list of terms, list of signs
    """
    termsList=[j for j in range(-50,0)] +[k for k in range(1,51)]
    operation_terms=[]
    operation_signs=[]
    for t in range(nb_ope):
        random_terms=[]
        random_signs=[]
        for i in range(nb_terms):
            random_terms.append(choice(termsList))
            random_signs.append(choice(["+","-"]))
        operation_terms += [random_terms]
        operation_signs += [random_signs]
        
    return operation_terms, operation_signs

def parenthesis(inlist):
    """
    puts parenthesis on each term of operation (except the first one)
    """
    parenthesised=[]
    for i in range(len(inlist)):
        tmp_list=inlist[i]
        tmp_parenthesised=[str(tmp_list[0])]
        for term in tmp_list[1:]:
            if term > 0:
                tmp_parenthesised.append("(+" + str(term) + ")")
            else:
                tmp_parenthesised.append("(" + str(term) + ")")
        parenthesised += [tmp_parenthesised]
    return parenthesised

def latex_operation(in_terms,in_signs):
    """
    concatenates terms list of operation with signs list of operation and pops
    out the last sign of signs list
    """
    ltx_operation =[]
    for i in range(len(in_terms)):
#        tmp_operation ='$'
        tmp_operation =''        
        for j in range(len(in_terms[i][:])):   
            tmp_operation += in_terms[i][j]+in_signs[i][j]
        ltx_operation += [tmp_operation[:-1]]
#    for k in range(len(in_terms)):
#        ltx_operation[k] += "$"
    return ltx_operation

def latexifies(inlist):
    """
    Adds a $ at the begining and the end of each term of inlist for 
    latex mathematical mode.
    """
    outlist=['$' + str(i) + '$' for i in inlist]
    
    return outlist
        
    

def converts_signs(in_signs):
    """
    creates a list that containing conversion of sign list : '+' becomes +1 and
    '-' becomes '-1'
     """
    converted_signs=[]     
    for i in range(len(in_signs)):
        tmp_list=in_signs[i]
        tmp_converted_signs=[]
        for j in tmp_list:
            if j == '+':
                tmp_converted_signs.append(1)
            else :
                tmp_converted_signs.append(-1)
        converted_signs += [tmp_converted_signs]
    return converted_signs

def simplifies(in_terms,in_signs):
    """
    simplifies the operation, i.e. converts:
        * -(-a) to +a
        * -(+a) to -a
        * +(-a) to -a
        * +(+a) to +a
    
    returns:
        - a list of strings corresponding to the simplified operation
    for latex output
        - a list of simplified calculated coefficients
    """
    simplified=[]
    simplified_str=[]
    for t in range(len(in_terms)):
#        tmp_simplified_str = "$" +str(in_terms[t][0])
        tmp_simplified_str = str(in_terms[t][0])        
        tmp_simplified = [in_terms[t][0]]
        for i,j in zip(in_terms[t][1:],in_signs[t][:len(in_signs[t])]):
            tmp_simplified.append(i*j)
            if i*j > 0 :
                tmp_simplified_str += '+' + str(i*j)
            else :
                tmp_simplified_str += str(i*j)
        simplified += [tmp_simplified]
        simplified_str += [tmp_simplified_str]
#    for k in range(len(simplified_str)):
#        simplified_str[k] += "$"
    return simplified_str,simplified

def final_result(inlist):
    """
    outputs a list of strings containing each result
    """
    sums = []
    for k in simply:
        sums.append(sum(k))
    return sums
 
def generate_labels(tata,titi,toto):
    geometry_options = {"margin": "0.5in"}
    doc = Document(geometry_options=geometry_options)

    doc.change_document_style("empty")

    doc.preamble.append(Command('title', 'Opérations sur les nombres relatifs'))
    doc.preamble.append(Command('author', 'Niveau de difficulté : 7 termes'))
    doc.preamble.append(Command('date', NoEscape(r"{}")))
    doc.append(NoEscape(r'\maketitle'))

    with doc.create(Section("Enoncé")):
        doc.append(NoEscape("Simplifier les expressions puis calculer :"))
        doc.append("\n")
        doc.append("\n")        
        
        for i in range(len(tata)):
#            with doc.create(MiniPage(width=r"0.5\textwidth"))
            doc.append(NoEscape(f"{string.ascii_uppercase[i]}={tata[i]}"+"\\\\"))
            doc.append(NoEscape("\\vspace{0.35cm}"))
#            if (i % 2) == 1:
#                doc.append(NoEscape("\\\\"))
                
    doc.append(NoEscape("\\newpage"))
    
    with doc.create(Section("Corrigé")):
        for i in range(len(tata)):
            with doc.create(MiniPage(width=r"0.5\textwidth")):
                doc.append(NoEscape(f"{string.ascii_uppercase[i]}={tata[i]}"+"\\\\"))
                doc.append(NoEscape(f"{string.ascii_uppercase[i]}={titi[i]}"+"\\\\"))
                doc.append(NoEscape(f"{string.ascii_uppercase[i]}={toto[i]}"+"\\\\"))

            if (i % 2) == 1:
                doc.append(NoEscape("\\\\"))
#
#            else :
#                with doc.create(MiniPage(width=r"0.5\textwidth")):
#                    doc.append(NoEscape(f"{string.ascii_uppercase[i]}={tata[i]}"+"\\\\"))
#                    doc.append(NoEscape(f"{string.ascii_uppercase[i]}={titi[i]}"+"\\\\"))
#                    doc.append(NoEscape(f"{string.ascii_uppercase[i]}={toto[i]}"+"\\\\"))
#                    if toutou[i] != toto[i]:
#                        doc.append(NoEscape(f"{string.ascii_uppercase[i]}={toutou[i]}"+"\\\\"))                    
#                    doc.append(NoEscape(f"{string.ascii_uppercase[i]}={tutu[i]}"+"\\\\"))
#
#            if (i % 2) == 1:
#                doc.append(NoEscape("\\\\"))

    doc.generate_pdf("operation_relatifs_7termes", clean_tex=False)    

toto,tata = generate_operation(7,25)

str_toto=parenthesis(toto)
str_tata=converts_signs(tata)

latex=latexifies(latex_operation(str_toto,tata))
simply_str,simply=simplifies(toto,str_tata)
simply_str=latexifies(simply_str)
results = latexifies(final_result(simply))

generate_labels(latex,simply_str,results)

for e in range(len(results)):
    print("*************")
    print(latex[e])
    print(simply_str[e])
    print(results[e])
    print("*************\n")
