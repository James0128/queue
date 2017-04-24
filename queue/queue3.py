# -*- coding: utf-8 -*- 2
#管理多线程队列操作
import tensorflow as tf
queue = tf.FIFOQueue(100,"float")
#定义队列入队操作
enqueue_op = queue.enqueue([tf.random_normal([1])])
#创建多个线程运行队列的入队操作
qr= tf.train.QueueRunner(queue,[enqueue_op]*5)
#加入tensorflow计算图上指定的集合
tf.train.add_queue_runner(qr)

out_tensor= queue.dequeue()

with tf.Session() as  sess:
    coord = tf.train.Coordinator()

    threads=tf.train.start_queue_runners(sess=sess,coord=coord)
    #获取队列中的取值
    for _ in  range(3):print sess.run(out_tensor)[0]

    coord.request_stop()
    coord.join(threads)