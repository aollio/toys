#!/usr/bin/env python3

import tensorflow as tf

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'

# stddev 为标准差 = 1
w1 = tf.Variable(tf.random_normal([2, 3], stddev=1, seed=1))
w2 = tf.Variable(tf.random_normal([3, 1], stddev=1, seed=1))

# 暂时将输入的特征向量定义为一个常量.
# x为一个1*2的矩阵
x = tf.constant([[0.7, 0.9]])

# 前向传播算法
a = tf.matmul(x, w1)
y = tf.matmul(a, w2)

sess = tf.Session()
# 与3.4.2中的计算不同, 这里不能通过sess.run(y)来获取值,
# 因为w1与w2还没有运行初始化过程.
# 下面的两行分别初始化了w1与w2两个变量
# sess.run(w1.initializer)
# sess.run(w2.initializer)

# 所有定义的变量一起初始化
sess.run(tf.global_variables_initializer())
#
print(sess.run(y))
sess.close()
