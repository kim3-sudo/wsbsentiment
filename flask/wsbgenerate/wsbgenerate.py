import pandas as pd
import gpt_2_simple as gpt2
import tensorflow as tf

class wsbgenerate:
  def textgen():
    tf.compat.v1.reset_default_graph()
    sess = gpt2.start_tf_sess()
    gpt2.load_gpt2(sess)
    return gpt2.generate(sess, temperature = 0.7, nsamples = 1, batch_size = 1, length = 50, return_as_list = True)[0]
