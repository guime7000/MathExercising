#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 10:57:19 2020

@author: tom
"""

class Polynome:
    
    def __init__(self,symbol='x',*args):
        self.symbol=symbol # symbol for polynom
        # sorted list of monomes
        self.monomes = sorted(args, key = lambda power : 
            power[1], reverse = True)
        # polynom's degee        
        self.degree=self.monomes[0][1]
        
    def __add__(self,poly):
        """
        Simply adds 2 polynoms
        For detailed sum, see function dadd()
        
        poly is an object of class Polynom
        """
#        
        
#    def dadd(self,):
#        """
#        Detailed sum (for detailed latex output)
#        """
#    
#    def __mul__(self,):
#        """
#        Simply multiplies 2 polynoms
#        For detailed product, see function dmul()
#        """
#        
#    def dmul(self,):
#        """
#        Detailed product (for detailed latex output)
#        """
#        
#    def opposite(self,):
#        """
#        """
#        
#    def __call__(self,value):
#        
    def __repr__(self):
        out_str=''
        for i in self.monomes :
            out_str += f"{i[0]}*{self.symbol}^{i[1]} | "
            
        return out_str
#    def out_latex(self,):
#        """
#        Returns a string for Latex Math environnement when given a Polynomial
#        enry
#
P=Polynome('y',[1,0],[2,1],[3,2])
Q=Polynome('t',[1,1],[2,2],[3,3])