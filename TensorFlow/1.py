#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tensorflow as tf

hello = tf.constant('Hello ,World')
sess = tf.Session()
print(sess.run(hello))

a = tf.constant(10)
b = tf.constant(32)
print(sess.run(a + b))

# 创建一个常量op ,产生一个1*2的矩阵,这个op被作为一个节点加到默认图中
# 构造器的返回值代表该常量op的返回值
matrix1 = tf.constant([[3., 3.]])
# 常见另一个常量op,产生一个2*1的矩阵
matrix2 = tf.constant([[2.], [2.]])

# 创建一个矩阵乘法matmul op,把matrix1和matrix2作为输入
# 返回值product代表矩阵的乘法结果
product = tf.matmul(matrix1, matrix2)
print(sess.run(product))
sess.close()
