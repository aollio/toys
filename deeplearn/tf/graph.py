#!/usr/bin/env python3


import tensorflow as tf

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'

g1 = tf.Graph()
with g1.as_default():
    # 在计算图g1中定义变量 "v", 并设置初始值为0.
    v = tf.get_variable(
        "v", initializer=tf.zeros_initializer(), shape=[1])
g2 = tf.Graph()
with g2.as_default():
    v = tf.get_variable(
        "v", initializer=tf.ones_initializer(), shape=[1]
    )

# 读取g1中的v
with tf.Session(graph=g1) as sess:
    # deprecated
    # tf.initialize_all_variables().run()
    tf.global_variables_initializer().run()
    with tf.variable_scope('', reuse=True):
        print(sess.run(tf.get_variable('v')))

with tf.Session(graph=g2) as sess:
    # deprecated
    # tf.initialize_all_variables().run()
    tf.global_variables_initializer().run()
    with tf.variable_scope('', reuse=True):
        print(sess.run(tf.get_variable('v')))
