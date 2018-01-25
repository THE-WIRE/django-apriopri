import pandas as pd
import numpy as np
from numpy import nan
import itertools

def powerset(seq):
    """
    Returns all the subsets of this set. This is a generator.
    """
    if len(seq) <= 1:
        yield []
        yield seq
    else:
        for item in powerset(seq[1:]):
            yield [seq[0]]+item
            yield item
        

def get_sets(count):
    x = powerset([x for x in range(count)])
    a = []
    b = []
    for i in x:
        if(len(i) > 1):
            y = list(itertools.permutations(i))
            for j in y:
                a.append(j)
    for i in range(2, count+1):
        c = []
        for j in a:
            if(len(j) == i):
                c.append(j)
        b.append(c)
    
    return b
                
                


class Apriopri:
    def __init__(self, infile, supp=0.1, conf=0.5):
        self.file = infile
        self.supp = supp
        self.conf = conf
        print("Reading file data...")
        self.read_file()
        print("File reading completed.")
        print("Processing data...")
        self.process()
        print("Data pocessing completed.")
        print("Calculating support...")
        self.get_support()
        print("Support calculation completed.")

    def read_file(self):
        x = pd.read_csv(self.file)
        y = np.array(x)
        z = y[:, 3:]
        n = list()
        for m in z.tolist():
            for o in m:
                n.append(o)
        p = set(n)
        p.remove(nan)
        self.item_data = list(p)
        
        self.raw_data = z
        self.basket_data = y[:, :3]
        
    def process(self):
        self.data = []
        for d in self.raw_data:
            x = np.zeros(len(self.item_data), dtype=bool)
            count = 0
            for i in self.item_data:
                for k in d:
                    if k == i:
                        x[count] = True
                count += 1
            self.data.append(x)
        self.d = self.data
    
    def get_support(self):
        self.item_data = np.array(self.item_data)
        self.d = np.array(self.d)
        self.support = np.sum(self.d, axis=0)/self.d.shape[0]
        indices = []
        for i in range(len(self.support)):
            if(self.support[i] < self.supp):
                indices.append(i)

        self.d = np.delete(self.d, indices, 1)

        self.item_data = np.delete(self.item_data, indices)
        self.support = np.delete(self.support, indices)
        print("Filtering completed.")
        
#        self.con()
#    
#    def ret_support(self, el):
#        return 1
#        
#    def con(self):
#        self.confidence = dict()
#        perms = get_sets(self.item_data.size)
#        for i, perm in enumerate(perms):
#            for j, _set in enumerate(perm):
#                self.confidence[_set] = self.ret_support(_set[:i+1])/self.ret_support(_set[-1:])
#                
        
        

a = Apriopri('/Users/suyog/Projects/apriopri/file/GroceriesInitial.csv')
