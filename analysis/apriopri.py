import pandas as pd
import numpy as np
from numpy import nan

class Apriopri:
    def __init__(self, infile, supp=0.15, conf=0.5):
        self.file = infile
        self.supp = supp
        self.conf = conf
        self.read_file()

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
        #TODO Iterate through z and check for the corresponding
        # availability of items and mark it in new array q
        
        self.raw_data = z
        self.process()
        
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
            

a = Apriopri('/Users/suyog/Projects/apriopri/file/GroceriesInitial.csv')
