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
        self.state_batch_placeholder = tf.placeholder(tf.float32, shape=(None, NUM_SPACES))
        self.targets_placeholder = tf.placeholder(tf.float32, shape=(None,))
        self.placeholders = (self.state_batch_placeholder, self.targets_placeholder)

        self.weights, self.biases, self.activations = build_inference_graph(self.state_batch_placeholder, HIDDEN_SIZES)
        self.q_values = self.activations[-1]
        self.loss = build_loss(self.q_values, self.targets_placeholder)
        self.train_op, self.global_step, self.learning_rate = build_train_op(self.loss)

        tf.summary.scalar ("Average Target", tf.reduce_mean (self.targets_placeholder))
        tf.summary.scalar ("Learning Rate", self.learning_rate)
        tf.summary.scalar ("Loss", self.loss)
        tf.summary.histogram ("States", self.state_batch_placeholder)
        tf.summary.histogram ("Targets", self.targets_placeholder)

        self.init = tf.initialize_all_variables ()
        self.summary_op = tf.summary.merge_all ()

def build_inference_graph(state_batch, hidden_sizes):
    input_batch = state_batch
    input_size = NUM_SPACES

    weights = []
    biases = []
    activations = []

    for i, hidden_size in enumerate(hidden_sizes):
        weights_i, biases_i, hidden_output_i = build_fully_connected_layer("hidden" + str(i),
                                                                           input_batch, input_size, hidden_size, ACTIVATION_FUNCTION)

        weights.append(weights_i)
        biases.append(biases_i)
        activations.append(hidden_output_i)

        input_batch = hidden_output_i
        input_size = hidden_size

    weights_qvalues, biases_qvalues, output = build_fully_connected_layer("q_values", input_batch, input_size, 1)

    weights.append(weights_qvalues)
    biases.append(biases_qvalues)
    activations.append(output)

    return weights, biases, activations

def build_fully_connected_layer(name, input_batch, input_size, layer_size, activation_function = lambda x: x):

    weights = tf.Variable(tf.truncated_normal([input_size, layer_size], stddev=WEIGHT_INIT_SCALE), name='weights')
    biases = tf.Variable(tf.zeros([layer_size]), name='biases')

    output_batch = activation_function(tf.matmul(input_batch, weights) + biases)

    tf.summary.histogram("Weights " + name, weights)
    tf.summary.histogram("Biases " + name, biases)
    tf.summary.histogram("Activations " + name, output_batch)

    return weights, biases, output_batch

def build_loss(q_values, targets):
    batch_size = tf.shape(q_values)[0]
    q_value_indices = tf.range (0, batch_size) * NUM_SPACES
    relevant_q_values = tf.gather (tf.reshape (q_values, [-1]), q_value_indices)

    # Compute L2 loss (tf.nn.l2_loss() doesn't seem to be available on CPU)
    return tf.reduce_mean (tf.pow (relevant_q_values - targets, 2))

def build_train_op(loss):
    global_step = tf.Variable (0, name='global_step', trainable=False)
    learning_rate = tf.train.exponential_decay (INIT_LEARNING_RATE, global_step, 100000, LR_DECAY_PER_100K)

    optimizer = OPTIMIZER_CLASS (learning_rate)
    train_op = optimizer.minimize (loss, global_step=global_step)
    return train_op, global_step, learning_rate