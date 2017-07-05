#!/usr/bin/env python3
import os
import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import random
import math
import csv
import ast
import numpy as np
import sys
import inspectcheckpoint

def init_weights(shape):
    return tf.Variable(tf.random_normal(shape, stddev=0.01))

#3 layer neural network with dropout
def model1(X, w_h, w_h2, w_o):
    
    h = tf.nn.tanh(tf.matmul(X, w_h))
       
    h2 = tf.nn.tanh(tf.matmul(h, w_h2))
    
    return tf.matmul(h2, w_o)

X = tf.placeholder("float", [None, 4])
Y = tf.placeholder("float", [None, 3])

w_h = init_weights([4, 60])
w_h2 = init_weights([60, 60])
w_o = init_weights([60, 3])

p_keep_input = tf.placeholder("float")
p_keep_hidden = tf.placeholder("float")
py_x = model1(X, w_h, w_h2, w_o)

predict_op1 = tf.argmax(py_x, 1)


secondplayersess1 = tf.Session()
init = tf.global_variables_initializer()
saver = tf.train.Saver()



secondplayersess2 = tf.Session()

savefile2 = "models/turnmodel1.ckpt"
saver.restore(secondplayersess2, savefile2)

savefile = "models/rivermodel1.ckpt"
saver.restore(secondplayersess1, savefile)


player1sess1 = tf.Session()
player1sess2 = tf.Session()
player1sess3 = tf.Session()
savefile3 = "models/flopmodel2.ckpt"
savefile4 = "models/turnmodel2.ckpt"
savefile5 = "models/rivermodel2.ckpt"

#inspectcheckpoint.print_tensors_in_checkpoint_file(savefile3, "Variable_6", True)
saver.restore(player1sess1, savefile3)
saver.restore(player1sess2, savefile4)
saver.restore(player1sess3, savefile5)

nn3sess1 = tf.Session()
nn3sess2 = tf.Session()
nn3sess3 = tf.Session()

nn3savefile1 = "models/flopmodel3.ckpt"
nn3savefile2 = "models/turnmodel3.ckpt"
nn3savefile3 = "models/rivermodel3.ckpt"

saver.restore(nn3sess1, nn3savefile1)
saver.restore(nn3sess2, nn3savefile2)
saver.restore(nn3sess3, nn3savefile3)

nn3sess1.run(init)

tf.reset_default_graph()

nn4sess1 = tf.Session()
nn4sess2 = tf.Session()
nn4sess3 = tf.Session()
init = tf.global_variables_initializer()


def model2(X, w_h, w_h2, w_h3, w_o):
    
    h = tf.nn.tanh(tf.matmul(X, w_h))
    
    
    h2 = tf.nn.tanh(tf.matmul(h, w_h2))
    
    h3 = tf.nn.tanh(tf.matmul(h2, w_h3))

    return tf.matmul(h3, w_o)

w_h2 = init_weights([4, 60])
w_h22 = init_weights([60, 60])
w_h32 = init_weights([60, 60])
w_o2 = init_weights([60, 3])

'''
p_keep_input = tf.placeholder("float")
p_keep_hidden = tf.placeholder("float")
'''
X2 = tf.placeholder("float", [None, 4])
Y2 = tf.placeholder("float", [None, 3])

py_x2 = model2(X2, w_h2, w_h22, w_h32, w_o2)
predict_op2 = tf.argmax(py_x2, 1)
saver2 = tf.train.Saver()
nn4savefile1 = "models/flopmodel4.ckpt"
nn4savefile2 = "models/turnmodel4.ckpt"
nn4savefile3 = "models/rivermodel4.ckpt"
saver2.restore(nn4sess1, nn4savefile1)
saver2.restore(nn4sess2, nn4savefile2)
saver2.restore(nn4sess3, nn4savefile3)

nn6sess1 = tf.Session()
nn6sess2 = tf.Session()
nn6sess3 = tf.Session()

nn6savefile1 = "models/flopmodel6.ckpt"
nn6savefile2 = "models/turnmodel6.ckpt"
nn6savefile3 = "models/rivermodel6.ckpt"
saver2.restore(nn6sess1, nn6savefile1)
saver2.restore(nn6sess2, nn6savefile2)
saver2.restore(nn6sess3, nn6savefile3)

nn7sess1 = tf.Session()
nn7sess2 = tf.Session()
nn7sess3 = tf.Session()

nn7savefile1 = "models/flopmodel7.ckpt"
nn7savefile2 = "models/turnmodel7.ckpt"
nn7savefile3 = "models/rivermodel7.ckpt"
saver2.restore(nn7sess1, nn7savefile1)
saver2.restore(nn7sess2, nn7savefile2)
saver2.restore(nn7sess3, nn7savefile3)

nn4sess2.run(init)

tf.reset_default_graph()


def model3(X, w_h, w_h2, w_h3, w_o):
    
    h = tf.nn.tanh(tf.matmul(X, w_h))
    
    
    h2 = tf.nn.tanh(tf.matmul(h, w_h2))
    
    h3 = tf.nn.tanh(tf.matmul(h2, w_h3))

    return tf.matmul(h3, w_o)
X3 = tf.placeholder("float", [None, 5])
Y3 = tf.placeholder("float", [None, 3])

w_h3 = init_weights([5, 60])
w_h23 = init_weights([60, 60])
w_h33 = init_weights([60, 60])
w_o3 = init_weights([60, 3])

p_keep_input = tf.placeholder("float")
p_keep_hidden = tf.placeholder("float")
py_x = model3(X3, w_h3, w_h23, w_h33, w_o3)
predict_op3 = tf.argmax(py_x, 1) 

nn5sess1 = tf.Session()
nn5sess2 = tf.Session()
nn5sess3 = tf.Session()
saver3 = tf.train.Saver()
nn5savefile1 = "models/flopmodel5.ckpt"
nn5savefile2 = "models/turnmodel5.ckpt"
nn5savefile3 = "models/rivermodel5.ckpt"
saver3.restore(nn5sess1, nn5savefile1)
saver3.restore(nn5sess2, nn5savefile2)
saver3.restore(nn5sess3, nn5savefile3)
    
