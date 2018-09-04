from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf

NUM_SPACES = 9

HIDDEN_SIZES = [256, 256]

OPTIMIZER_CLASS = tf.train.AdamOptimizer
ACTIVATION_FUNCTION = tf.nn.relu
WEIGHT_INIT_SCALE = 0.01

INIT_LEARNING_RATE = 1e-4
LR_DECAY_PER_100K = 0.98

class FeedModel(object):
    """Class to construct the tensorflow model with relevant tensors"""

    def __init__(self):
        self.state_batch_placeholder = 