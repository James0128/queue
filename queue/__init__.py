# -*- coding: utf-8 -*- 2
#import  tensorflow as tf
#创建一个队列
#q = tf.FIFOQueue(2, "int32")
#init = q.enqueue_many(([0,10],))

#将第一个元素出队列
#x= q.dequeue()
#y=x+1
#重新加入队列
#q_inc= q.enqueue([y])

#with tf.Session() as sess:
    #运行初始化队列操作
 #   init.run()
  #  for _ in range(5):
   #     v, _ = sess.run([x,q_inc])
    #    print v
import  tensorflow as tf
import numpy as np
import threading
import time
#线程中运行的程序，这个程序每隔一秒判断是否需要停止打印自己的ID
def MyLoop(coord,worked_id):
    #判断当前线程是否需要停止
    while not coord.should_stop():
        #随即停止所有的线程
        if np.random.rand() < 0.1:
            print "Stopping from id: %d\n" %worked_id,
            coord.requst_stop()
        else:
            print  "Working on id: %d\n" %worked_id,
        time.sleep(1)

coord = tf.train.Coordinator()

threads=[threading.Thread(target=MyLoop,args=(coord,i,)) for i in xrange(5)]

for t in threads:t.start()

coord.join(threads)

