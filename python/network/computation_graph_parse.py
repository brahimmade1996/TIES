import numpy as np
import torch
from torch.autograd import Variable
from network.ModuleA import ModuleA
from network.ModuleB import ModuleB
from network.ModuleB22 import ModuleB2
from network.ModuleC import ModuleC
from network.ModuleD import ModuleD
from network.ModuleCollect import ModuleCollect
from network.ModuleAssociate2 import ModuleAssociate2


class ComputationGraphTableParse(torch.nn.Module):
    def __init__(self):
        super(ComputationGraphTableParse, self).__init__()
        self.k = 8
        self.D_in = 300 + self.k

        self.A = ModuleA(self.D_in, 100)
        self.B = ModuleB()
        self.B2 = ModuleB2(100, 100, 100)
        self.associate_rows = ModuleAssociate2()
        self.associate_cols = ModuleAssociate2()
        self.associate_cells = ModuleAssociate2()
        self.D = ModuleD(100, 100)
        # self.Cat = ModuleCollect(100, self.N)
        self.iterations = 1

    def set_iterations(self, iterations):
        self.iterations = iterations

    def concat(self, x, indices, indices_not_found, num_words):
        y = Variable(torch.zeros(num_words, 100 * 5)).cuda()
        y[:, 000:100] = x[indices[:, 0]]
        y[:, 100:200] = x[indices[:, 1]]
        y[:, 200:300] = x[indices[:, 2]]
        y[:, 300:400] = x[indices[:, 3]]
        y[:, 400:500] = x[indices[:, 4]]
        y[indices_not_found] = 0

        return y

    def forward(self, indices, indices_not_found, vv, num_words):

        uu = self.A.forward(vv)
        hh = Variable(torch.zeros(num_words,100)).cuda()

        for i in range(self.iterations):
            ww = self.concat(uu, indices, indices_not_found, num_words)
            bb = self.B.forward(ww, hh)
            oo, hh = self.B2.forward(bb)
            uu = self.D.forward(hh)

        return self.associate_rows(oo, num_words), self.associate_cols(oo, num_words), self.associate_cells(oo, num_words)