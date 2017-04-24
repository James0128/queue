# -*- coding: utf-8 -*- 2

import tensorflow as tf
import numpy  as np
import  threading
import  time

def MyLoop(coord,worked_id):
    while not coord.should_stop():
        #随机停止所有线程
        if np.random.rand() <0.1:
            print "Stoping from id:%d\n" %worked_id,
            coord.request_stop()
        else:
            #打印当前线程id
            print "Working on id:%d\n" %worked_id,
        time.sleep(1)
#协同多个线程
coord = tf.train.Coordinator()
threads=[threading.Thread(target=MyLoop,args=(coord,i,)) for i in range(5)]
#启动所有线程
for t in threads:t.start()
#等待所有线程退出
coord.join(threads)