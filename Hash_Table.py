# CS122 W'18: Markov models and hash tables
# Noa Ohcana
import math as math

TOO_FULL = 0.5
GROWTH_RATIO = 2


class Hash_Table:

    def __init__(self,cells,defval):
        '''
        Construct a new hash table with a fixed number of cells equal to the
        parameter "cells", and which yields the value defval upon a lookup to a
        key that has not previously been inserted
        '''
        self.cells = cells
        self.defval = defval
        self.hash_table = [(None, None)]*cells
        self.full_cells = 0

    def lookup(self,key):
        '''
        Retrieve the value associated with the specified key in the hash table,
        or return the default value if it has not previously been inserted.
        '''
        hash_index = self.calculate_hash(key)
        item, value = self.hash_table[hash_index]
        if item == key:
            return value
        if item is None:
            return self.defval
        for i in list(range(hash_index + 1, 
            self.cells)) + list(range(hash_index)):
        # should be helper but had trouble implementing
            item, value = self.hash_table[i]
            if item == key:
                return value
        return self.defval
        # just in case

    def update(self,key,val):
        '''
        Change the value associated with key "key" to value "val".
        If "key" is not currently present in the hash table,  insert it with
        value "val".  
        '''

        hash_index = self.calculate_hash(key)
        if self.hash_table[hash_index][0] is None:
            self.hash_table[hash_index] = (key, val)
            self.full_cells += 1
        elif self.hash_table[hash_index][0] == key:
            self.hash_table[hash_index] = (key, val)
        else:
            for i in list(range(hash_index + 1, 
                self.cells)) + list(range(hash_index)):
                if self.hash_table[i][0] is None:
                    self.hash_table[i] = (key, val)
                    self.full_cells += 1
                if self.hash_table[i][0] == key:
                    self.hash_table[i] = (key, val)
                    self.full_cells += 1
                    break
        if self.full_cells/self.cells > TOO_FULL:
            self.rehash()

    def calculate_hash(self,key):
        '''
        Calculates the hash values of the key by the formula discussed in class
        '''
        h_value = 0
        for letter in key:
            ascii = ord(letter)
            h_value += ascii
            h_value = h_value*37
            h_value = h_value%self.cells

        return h_value

    def rehash(self):
        '''
        Creates a copy of the current table and then re-initializes an 
        empty hash table with new length specified by GROWTH_RATIO and 
        then recalculates hash indeces and updates the new table
        '''
        old_table = self.hash_table
        self.hash_table = [(None, None)]*self.cells*GROWTH_RATIO
        self.cells = math.ceil(self.cells*GROWTH_RATIO)
        self.full_cells = 0
        for tuple_h_prev in old_table:
            if tuple_h_prev != (None, None):
                prev_key = tuple_h_prev[0]
                prev_val = tuple_h_prev[1]
                self.update(prev_key, prev_val)
