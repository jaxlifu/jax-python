#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tensorflow
import numpy

# 使用Numpy生成假数据(phony data) 总共100个点
x_data = numpy.float32(numpy.random.rand(2, 100))  # 随机输入
y_data = numpy.dot([0.100, 0.200], x_data) + 0.300

# 构建一个线性模型
b = tensorflow.Variable(tensorflow.zeros([1]))
w = tensorflow.Variable(tensorflow.random_uniform([1, 2], -1.0, 1.0))
y = tensorflow.matmul(w, x_data) + b

# 最小方差
loss = tensorflow.reduce_mean(tensorflow.square(y - y_data))
optimizer = tensorflow.train.GradientDescentOptimizer(0.5)
train = optimizer.minimize(loss)

# 初始化变量
init = tensorflow.initialize_all_variables()

# 启动器(graph)
sess = tensorflow.Session()
sess.run(init)

# 拟合平台
for step in range(0, 200):
    sess.run(train)
    if step % 20 == 0:
        print(step, sess.run(w), sess.run(b))

# 得到最佳拟合结果
# W: [[0.100  0.200]], b: [0.300]
