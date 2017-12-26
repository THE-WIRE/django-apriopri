import pandas as pd
import numpy as np
from numpy import nan

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
    for i in x:
        if(len(i) > 1) and (len(i) < 3):
            a.append(i)
    
    return a

class Apriopri:
    def __init__(self, infile, supp=700, conf=0.5):
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
        self.support = np.sum(self.d, axis=0)
        print(self.support)
        indices = []
        for i in range(len(self.support)):
            if(self.support[i] < self.supp):
                indices.append(i)
        self.d = np.array(self.d)
        self.item_data = np.array(self.item_data)
        print(self.d.shape, indices, self.support.shape)
        self.d = np.delete(self.d, indices, 1)
        print(self.d.shape, indices, self.support.shape)
        print("----------------------------")
        print(self.item_data.shape, indices)
        self.item_data = np.delete(self.item_data, indices)
        print(self.item_data.shape, indices)
        print("----------------------------")
        print("Data cleaned by columns.")
        self.support = np.sum(self.d, axis=1)
        indices = []
        for i in range(len(self.support)):
            if(self.support[i] < 3):
                indices.append(i)
        self.d = np.delete(self.d, indices, 0)
        print(self.d.shape, indices, self.support.shape)
        self.basket_data = np.delete(self.basket_data, indices, 0)
        print("Data cleaned by rows.")
        self.s = np.sum(self.d, axis=0)/self.d.shape[1]
        print("Support values calculated.")
        x = get_sets(self.item_data.size)
        self.confidence = np.zeros([self.item_data.size, self.item_data.size])
        print("Calculating confidence...")
        for i in x:
            count = 0
            for y in self.d:
                if( y[i[0]] and y[i[1]] ):
                    count += 1
            self.confidence[i[0], i[1]] = count/np.sum(self.d[:, i[0]])
        print("Confidence calculated (1/2)")
        for i in x:
            count = 0
            for y in self.d:
                if( y[i[0]] and y[i[1]] ):
                    count += 1
            self.confidence[i[1], i[0]] = count/np.sum(self.d[:, i[1]])
        print("Confidence calculated (2/2)")
        
    def get_max_pairs(self):
        i, j = np.unravel_index(np.argmax(self.confidence), self.confidence.shape)
        return self.item_data[i], self.item_data[j]

a = Apriopri('/Users/suyog/Projects/apriopri/file/GroceriesInitial.csv')
