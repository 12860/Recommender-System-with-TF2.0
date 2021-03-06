"""
Created on Oct 23, 2020

modules of STAMP: attention mechanism

@author: Ziyao Geng
"""
import tensorflow as tf

from tensorflow.keras.regularizers import l2
from tensorflow.keras.layers import Layer


class Attention_Layer(Layer):
    """
    Attention Layer
    """
    def __init__(self, d, reg=1e-4):
        """

        :param d: A scalar. The dimension of embedding.
        :param reg: A scalar. The regularizer of parameters
        """
        self.d = d
        self.reg = reg
        super(Attention_Layer, self).__init__()

    def build(self, input_shape):
        self.W0 = self.add_weight(name='W0',
                                  shape=(self.d, 1),
                                  initializer=tf.random_normal_initializer,
                                  regularizer=l2(self.reg),
                                  trainable=True)
        self.W1 = self.add_weight(name='W1',
                                  shape=(self.d, self.d),
                                  initializer=tf.random_normal_initializer,
                                  regularizer=l2(self.reg),
                                  trainable=True)
        self.W2 = self.add_weight(name='W2',
                                  shape=(self.d, self.d),
                                  initializer=tf.random_normal_initializer,
                                  regularizer=l2(self.reg),
                                  trainable=True)
        self.W3 = self.add_weight(name='W3',
                                  shape=(self.d, self.d),
                                  initializer=tf.random_normal_initializer,
                                  regularizer=l2(self.reg),
                                  trainable=True)
        self.b = self.add_weight(name='b',
                                  shape=(self.d,),
                                  initializer=tf.random_normal_initializer,
                                  regularizer=l2(self.reg),
                                  trainable=True)

    def call(self, inputs):
        seq_embed, m_s, x_t = inputs
        """
        seq_embed: (None, seq_len, d)
        W1: (d, d)
        x_t: (None, d)
        W2: (d, d)
        m_s: (None, d)
        W3: (d, d)
        W0: (d, 1)
        """
        alpha = tf.matmul(tf.nn.sigmoid(
            tf.tensordot(seq_embed, self.W1, axes=[2, 0]) + tf.matmul(x_t, self.W2) +
            tf.matmul(m_s, self.W3) + self.b), self.W0)
        m_a = tf.reduce_sum(tf.multiply(alpha, seq_embed), axis=1)  # (None, d)
        return m_a

