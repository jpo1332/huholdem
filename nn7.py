#!/usr/bin/env

import numpy as np
import csv
import tensorflow as tf
from random import randint
from random import seed
import sys
import inspectcheckpoint

origfile = sys.argv[1]
savefile = sys.argv[2]
origfile = 'nndata/' + origfile
savefile = 'models/' + savefile
#read inputs from csv file
with open(origfile, 'rU') as f:
    data =[list(line) for line in csv.reader(f, dialect='excel')]
for x in range(len(data)):
    for y in range(len(data[x])):
        try:
            data[x][y] = float(data[x][y])
        except:
            print "number is ",x,y


#function for creating batches of data
def batch(x, y):
    newx = []
    newy = []
    seed()
    for i in range(750):
        a = randint(1, len(x))
        newx.append(x[a-1])
        newy.append(y[a-1])
    return (newx, newy)

#Split data into training and testing
def split(x, y):
    newx = []
    newy = []
    length = len(x)
    print int(length / 5)
    newx = x[0:length /5]
    newy = y[0:length / 5]
    y = y[length/5:length]
    x = x[length/5:length]
    
    return newx, newy, x, y

#initialize weights to random values   
def init_weights(shape):
    return tf.Variable(tf.random_normal(shape, stddev=0.01))

#3 layer neural network with dropout
def model(X, w_h, w_h2, w_h3, w_o):
    
    h = tf.nn.tanh(tf.matmul(X, w_h))
    
    
    h2 = tf.nn.tanh(tf.matmul(h, w_h2))
    
    h3 = tf.nn.tanh(tf.matmul(h2, w_h3))

    return tf.matmul(h3, w_o)

trX = []
trY = []
temp = 0
counter = 0

#feed input and output variables into tensors
print data[0]
length = len(data[0])-3

for a in data:
    trX.append(np.array(a[:length]))
    trX[counter] = np.reshape(trX[counter], (1, 4))
    
    trY.append(np.array(a[length:len(a)]))
    trY[counter] = np.reshape(trY[counter], (1, 3))
    counter += 1

print "x1 =:", trX[0]
print "y1 =:", trY[0]


X = tf.placeholder("float", [None, 4])
Y = tf.placeholder("float", [None, 3])

w_h = init_weights([4, 60])
w_h2 = init_weights([60, 60])
w_h3 = init_weights([60, 60])
w_o = init_weights([60, 3])

p_keep_input = tf.placeholder("float")
p_keep_hidden = tf.placeholder("float")
py_x = model(X, w_h, w_h2, w_h3, w_o)

def cost1(py_x, Y):
    if abs(np.argmax(py_x) - np.argmax(Y)) > 1:
        return 2
    elif abs(np.argmax(py_x) - np.argmax(Y)) > 0:
        return 1
    else:
        return 0
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=py_x, labels=Y)) # compute mean cross entropy (softmax is applied internally)
#cost = tf.reduce_mean(cost1(py_x, Y))
train_op = tf.train.GradientDescentOptimizer(0.2).minimize(cost)
predict_op = tf.argmax(py_x, 1)

'''
var4 = init_weights([3, 60])
var5 = init_weights([60, 60])
var6 = init_weights([60, 3])
'''
saver = tf.train.Saver(var_list={"Variable":w_h, "Variable_1":w_h2, "Variable_2":w_h3, "Variable_3":w_o})#, "Variable_4":var4, "Variable_5":var5,"Variable_6":var6})
sess = tf.Session()
init = tf.initialize_all_variables()
sess.run(init)

#testX, testY, trX2, trY2 = split(trX, trY)
testX, testY, trX2, trY2 = split(trX, trY)
#print "trx2:", trX2[0][0:15], len(trX2)
#print "try2:", trY2[0:15], len(trY2)
#savefile = "models/rivermodel2.ckpt"
#saver.restore(sess, savefile)
l2 = 0
test = 0
#batchx, batchy = batch(trX2, trY2)
for i in range(501):
    
    batchx, batchy = batch(trX2, trY2)
    for (x, y) in zip(batchx, batchy):
        sess.run(train_op, feed_dict={X: x, Y: y})
    total = 0
    l = 0
    
    batchtx, batchty = batch(testX, testY)
    for (x, y) in zip(batchtx, batchty):
        pred = sess.run(predict_op, feed_dict={X: x})
        real = np.argmax(y, axis=1)
        
            
        right = False
        if pred == real:
            total += 1
            right = True
        l += 1
        l2 += 1
        if l2 % 751 == 0:
            print "Real:", real, "Guess:", pred,  "Y:", y, "right?:", right
    test += total
    if i % 10 == 0:
        print "\nHands:", l, "Hands correct:", total, "%:", float(total) / l, "Runs:", i
print test / float(l2)

savepath = saver.save(sess, savefile)
#inspectcheckpoint.print_tensors_in_checkpoint_file(savefile, "Variable_6", True)
print "save path", savepath






















    
