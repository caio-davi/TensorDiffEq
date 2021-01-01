from tensordiffeq.domains import *
import numpy as np
import tensorflow as tf
from .utils import meshgrid2

class BC(DomainND):
    def __init__(self):
        self.doms = self.domain.create_domains()
        self.grid = self.domain.create_mesh()


class dirichlectBC(BC):
    def __init__(self, domain, val, var, time_var, target):
        self.domain = domain
        self.val = val
        self.var = var
        self.time_var = time_var
        self.target = target

    def create_target_input_repeat(self):
        linspace_list = []

        iter_ids = np.setdiff1d(self.domain.domain_ids, self.var).tolist()
        for id in (iter_ids):
            self.dict_ = next(item for item in self.domain.domaindict if item["identifier"] == id)
            #print(self.domain.domaindict)
            linspace_list.append(self.dict_[(id+"linspace")])
        print(linspace_list)
        out, out1 = np.meshgrid(linspace_list[0], linspace_list[1])

        print(np.shape(np.hstack((out.flatten()[:,None], out1.flatten()[:,None]))))
        search_key = self.var
        self.dict_ = next(item for item in self.domain.domaindict if item["identifier"] == search_key)
        self.dict_t = next(item for item in self.domain.domaindict if item["identifier"] == self.time_var)
        repeated_value = np.repeat(self.dict_[(self.var+self.target)], self.dict_t[(self.time_var+"fidelity")])
        return repeated_value


    def loss(self):
        repeated_value = self.create_target_input_repeat()
        repeated_value = np.reshape(repeated_value, (-1,1))
        mesh = np.reshape(np.meshgrid(self.dict_t[(self.time_var+"linspace")]), (-1,1))
        #linsp = np.meshgrid(self.dict_t[(self.time_var+"linspace")])

        input = tf.concat([repeated_value, mesh], 1)
        print(input)
        #pred = u_model(input)
        #return MSE(pred, val)




class IC(BC):
    def __init__(self, domain, fun, vars):
        self.domain = domain
        self.fun = fun
        self.vars = vars




class periodicBC(BC):
    def __init__(self, domain):
        self.domain = domain

    def u_x_model(self, u_model, nn_input):
        u = u_model(nn_input)
        u_x = tf.gradients(u, nn_input[:,0:1])
        return u, u_x

    def create_edges(self):
        edges = []
        for i, val in enumerate(self.domain.bounds[:-1]):
            for value in val:
                edges.append(tf.concat([np.repeat(value, self.domain.fidel[i]), self.doms[-1]], 0))

    def loss(self, u_model):
        loss = 0.0
        for i, val in enumerate(self.val):
            tf.assign_add()
        u_lb_pred, u_x_lb_pred = self.u_x_model(self.u_model, self.x_lb, self.t_lb)
        u_ub_pred, u_x_ub_pred = self.u_x_model(self.u_model, self.x_ub, self.t_ub)
        return
