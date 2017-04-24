# -*- coding: utf-8 -*- 2
#输入文件队列
import tensorflow as tf

#创建TFRecord文件的帮助函数
def _int64_feature(value):
    return tf.train.Feature(int64_list= tf.train.Int64List(value=[value]))

#模拟海量情况下将数据写入不同的文件
num_shards=2
instances_per_shard =2
for i in range(num_shards):
    filename=('/Users/yifanyang/Desktop/a/data.tfrecords-%.5d-of-%.5d'%(i,num_shards))
    write = tf.python_io.TFRecordWriter(filename)
    #将数据封装成Example结构并写入文件
    for j in range(instances_per_shard):
        example = tf.train.Example(features= tf.train.Features(feature={'i': _int64_feature(i),'j': _int64_feature(j)}))
        write.write(example.SerializeToString())
    write.close()

#读取文件
files= tf.train.match_filenames_once("/Users/yifanyang/Desktop/a/data.tfrecords-*")
filename_queue=tf.train.string_input_producer(files,shuffle=False)
#解析
reader=tf.TFRecordReader()
_,serialized_example = reader.read(filename_queue)
features= tf.parse_single_example(
      serialized_example,features={
      'i':tf.FixedLenFeature([],tf.int64),
      'j':tf.FixedLenFeature([],tf.int64)
    })
with tf.Session() as sess:
    tf.initialize_all_variables().run()
    print(sess.run(files))
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess=sess, coord=coord)
    for i in range(6):
        print(sess.run([features['i'], features['j']]))
    coord.request_stop()
    coord.join(threads)

#组合训练batch
example, label = features['i'], features['j']
batch_size = 3
capacity = 1000 + 3 * batch_size

example_batch, label_batch = tf.train.batch([example, label], batch_size=batch_size, capacity=capacity)

with tf.Session() as sess:
    tf.initialize_all_variables().run()
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess=sess, coord=coord)
    for i in range(3):
        cur_example_batch, cur_label_batch = sess.run([example_batch, label_batch])
        print cur_example_batch, cur_label_batch
    coord.request_stop()
    coord.join(threads)