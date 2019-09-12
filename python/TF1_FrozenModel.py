#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jiankaiwang (https://jiankaiwang.no-ip.biz/)
@version:
  Tensorflow: 1.x (developed >= 1.13.2)
@description:
  We provided several useful tools for using TF frozen model, including
  listing operations, listing nodes, transforming the model into tflite one, etc.
  We hope this script can bring you easier way access to the portable model.
@changelog (main):
  2019-04: initial commit
"""

import os
import tensorflow as tf
from collections import OrderedDict

# In[]

class OperateFrozenModel:
  @staticmethod
  def save_sess_into_frozen_model(sess, outputs, pb_path):
    """Access the sess and save it as the frozen model.

    Args:
      sess: an active session
      outputs: a list contains the name of tensor, e.g. ["result"]
      pb_path: the path for output frozen model

    Returns:
      state: True or False
      Message: None (for True) or Message (for False)
    """
    try:
      output_graph_def = tf.graph_util.convert_variables_to_constants(
          sess, sess.graph.as_graph_def(), outputs)
      with tf.gfile.FastGFile(pb_path, "wb") as fout:
        fout.write(output_graph_def.SerializeToString())
      return True, None
    except Exception as e:
      return False, str(e)

  @staticmethod
  def load_frozen_model(pb_path, graph_name=""):
    """Load the frozen model. (Serial)

    Returns:
      state: True or False
      Message: None (for True) or Message (for False)
    """
    try:
      tf.reset_default_graph()
      graph = tf.Graph()
      with graph.as_default():
        graph_def = tf.GraphDef()
        with tf.gfile.GFile(pb_path, "rb") as fin:
          graph_def.ParseFromString(fin.read())
          tf.import_graph_def(graph_def, name=graph_name)
      return True, graph
    except Exception as e:
      return False, str(e)

  @staticmethod
  def transform_into_tflite(pb_path, inputs, outputs, tflite_path):
    """Transform a frozen model into a tflite one.

    Args:
      pb_path: the path to a frozen model
      inputs: a list contains the name of tensor, e.g. ["input"]
      outputs: a list contains the name of tensor, e.g. ["result"]
      tflite_path: the path for tflite model

    Returns:
      state: True or False
      Message: None (for True) or Message (for False)
    """
    try:
      converter = tf.lite.TFLiteConverter.from_frozen_graph(pb_path, inputs, outputs)
      tflite_model = converter.convert()
      open(tflite_path, "wb").write(tflite_model)
      return True, None
    except Exception as e:
      return False, str(e)

  @staticmethod
  def transform_into_savedmodel(pb_path, inputs, outputs, model_dir):
    """Export the frozen model as the savedModel format.

    Args:
      pb_path: the path to a frozen model
      inputs: a list contains available name of tensor node, e.g. ['image']
      outputs: a list contains the name of tensor, e.g. ["result"]
      model_dir: the directory to the saved model

    Returns:
      state: True or False
      Message: Output Directory (for True) or Message (for False)
    """
    try:
      state, graph = OperateFrozenModel.load_frozen_model(pb_path)
      if not state: raise Exception(graph)
      tensor_inputs, tensor_outputs = {}, {}
      for node in inputs:
        tensor_inputs[node] = graph.get_tensor_by_name("{}:0".format(node))
      for node in outputs:
        tensor_outputs[node] = graph.get_tensor_by_name("{}:0".format(node))
      print(tensor_inputs, tensor_outputs)
      tf.reset_default_graph()
      with tf.Session(graph=graph) as sess:
        tf.saved_model.simple_save(sess, model_dir, tensor_inputs, tensor_outputs)
      return True, model_dir
    except Exception as e:
      return False, str(e)

  @staticmethod
  def write_graph_for_tfboard(pb_path, logdir_path):
    """Write out the frozen graph into the logdir for visualization on TFBoard.

    Args:
      pb_path: the path to a frozen model
      logdir_path: the folder path further monitored by Tensorboard

    Returns:
      state: True or False
      Message: Output directory (for True) or Message (for False)
    """
    try:
      state, graph = OperateFrozenModel.load_frozen_model(pb_path)
      if not state: raise Exception(graph)
      if not tf.gfile.Exists(logdir_path):
        os.makedirs(logdir_path)
      writer = tf.summary.FileWriter(logdir=logdir_path)
      writer.add_graph(graph)
      return True, logdir_path
    except Exception as e:
      return False, str(e)

# In[]

class GraphOperations:
  @staticmethod
  def list_operations(graph, count=5):
    """List operations in the frozen model.

    Args:
      graph: a tf.Graph() object, you can first load the graph via
             OperateFrozenModel.load_frozen_model(pb_path)

    Standard Outputs:
      List operations or error messages.
    """
    try:
      operations = graph.get_operations()
      print("Total Operations: {}".format(len(operations)))

      if count < 1:
        for ops in operations:
          print(ops.name)
      else:
        for ops in operations[:count]:
          print(ops.name)
        print("...")
        for ops in operations[-count:]:
          print(ops.name)
    except Exception as e:
      print("Error in listing operations: {}.".format(str(e)))

  @staticmethod
  def find_operations(graph, name=None):
    """Test whether the operation is available in graph or not.

    Args:
      graph: a tf.Graph() object, you can first load the graph via
             OperateFrozenModel.load_frozen_model(pb_path)

    Returns:
      state: True or False
      Message: True / False (for state `True`) or Message (for False)
    """
    try:
      operations = graph.get_operations()
      operation_names = [ ops.name for ops in operations ]
      return True, name in operation_names
    except Exception as e:
      return False, str(e)

# In[]

class GraphTensors:
  @staticmethod
  def list_tensors(graph):
    """List tensors in the graph.

    Args:
      graph: a tf.Graph() object, you can first load the graph via
             OperateFrozenModel.load_frozen_model(pb_path)

    Standard Outputs:
      List tensors or error messages.
    """
    try:
      for n in graph.as_graph_def().node:
        if n.op in ["Placeholder", "PlaceholderWithDefault", "Const", "Identity"]:
          if n.op == "Identity":
            if len(n.attr['_class'].list.s) < 1:
              # check there is source or not
              tensor_name = graph.get_tensor_by_name(n.name + ":0")
            else: continue
          else:
            tensor_name = graph.get_tensor_by_name(n.name + ":0")
          print("{:<50} {}".format(n.name + ":0", tensor_name.shape))
    except Exception as e:
      print("Can't list tensors because error {}.".format(str(e)))

  @staticmethod
  def get_nodes_with_type(graph):
    """List the type of each node in the graph.

    Args:
      graph: a tf.Graph() object, you can first load the graph via
             OperateFrozenModel.load_frozen_model(pb_path)

    Returns:
      state: True or False
      object: a OrderedDict object whose key is node type and value is a list
              containing all nodes belonging to the same node type
              or Message in string (for False)
    """
    try:
      node_type = OrderedDict()
      for n in graph.as_graph_def().node:
        if n.op not in list(node_type.keys()):
          node_type[n.op] = [n]
        else:
          node_type[n.op].append(n)
      return True, node_type
    except Exception as e:
      return False, str(e)

# In[]

if __name__ == "__main__":
  pb_path = "/Users/jiankaiwang/Desktop/output_graph.pb"

  if not os.path.exists(pb_path):

    # a simple MLP network was implemented to generated a frozen model
    from tensorflow.examples.tutorials.mnist import input_data
    mnist = input_data.read_data_sets("/Users/jiankaiwang/devops/tmp/MNIST_data/", one_hot=True)

    tf.reset_default_graph()

    def mlp(inputs):
      def perception(inputs, input_shape, bias_shape):
        weight_std = (2.0 / input_shape[0]) ** 0.5
        w_init = tf.random_normal_initializer(stddev=weight_std)
        b_init = tf.constant_initializer(value=0.)
        W = tf.get_variable("W", shape=input_shape, initializer=w_init)
        b = tf.get_variable("b", shape=bias_shape, initializer=b_init)
        output = tf.add(tf.matmul(inputs, W), b)
        return tf.nn.relu(output)

      with tf.variable_scope("mlp"):
        with tf.variable_scope("hidden_1"):
          hidden_1 = perception(img, [784, 256], [256])
        with tf.variable_scope("hidden_2"):
          hidden_2 = perception(hidden_1, [256, 128], [128])
        with tf.variable_scope("hidden_3"):
          output = perception(hidden_2, [128, 10], [10])

      output = tf.identity(output, name="result")
      return output

    def validation(label, logits):
      compare = tf.equal(tf.argmax(label, axis=1), tf.argmax(logits, axis=1))
      accuracy = tf.reduce_mean(tf.cast(compare, tf.float32))
      return accuracy

    with tf.Graph().as_default() as graph:
      img = tf.placeholder(tf.float32, shape=[None, 784], name="input")
      img -= 0.5  # shift data to -0.5 ~ 0.5
      label = tf.placeholder(tf.float32, shape=[None, 10])
      global_step = tf.Variable(0, name="global_step", trainable=False)

      output = mlp(img)

      cross_entropy = tf.nn.softmax_cross_entropy_with_logits_v2(
          labels=label, logits=output)
      loss = tf.reduce_mean(cross_entropy)

      optimizer = tf.train.GradientDescentOptimizer(learning_rate=1e-2)
      train_opt = optimizer.minimize(loss, global_step=global_step)
      validator = validation(label, output)

      batch_size = 32
      batches = mnist.train.num_examples // batch_size

      with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for epoch in range(0, 51):
          for bs in range(0, batches):
            train_x, train_y = mnist.train.next_batch(batch_size)
            sess.run([train_opt], feed_dict={img: train_x, label: train_y})
          if epoch != 0 and epoch % 10 == 0:
            val_x, val_y = mnist.test.images, mnist.test.labels
            acc, cost = sess.run([validator, loss], feed_dict={img: val_x, label: val_y})
            print("Epoch {}: Accuracy {}, Cost {}".format(epoch, acc, cost))
        state, error = OperateFrozenModel.save_sess_into_frozen_model(
            sess, ["result"], pb_path)

  assert os.path.exists(pb_path), "PB was not found."

  print("\n----------")
  state, graph = OperateFrozenModel.load_frozen_model(pb_path)
  assert state, "Can't load the frozen model. {}".format(graph)
  print("Load the frozen model completely.")
  print("----------\n")

  print("\n----------")
  print("Transfrom a frozen model into tflite one.")
  tflite_model_path = "/Users/jiankaiwang/Desktop/output.tflite"
  state, error = OperateFrozenModel.transform_into_tflite(
      pb_path, ["input"], ["result"], tflite_model_path)
  assert state, "Error in transforming tflite model: {}.".format(error)
  print("----------\n")

  print("\n----------")
  print("Transfrom a frozen model into savedmodel format.")
  model_dir = "/Users/jiankaiwang/Desktop/savedModel"
  state, error = OperateFrozenModel.transform_into_savedmodel(
      pb_path, ["input"], ["result"], model_dir)
  assert state, "Error in transforming savedmodel format: {}.".format(error)
  print("----------\n")

  print("\n----------")
  print("List operations in graph.")
  GraphOperations.list_operations(graph)
  print("----------\n")

  print("\n----------")
  print("Check if the nodel is in graph or not.")
  for ops_name in ["a", "b"]:
    state, existing = GraphOperations.find_operations(graph, ops_name)
    assert state, "Can't find operations because of error {}.".format(existing)
    print("Operation {} exists? {}.".format(ops_name, existing))
  print("----------\n")

  print("\n----------")
  print("List tensors in graph.")
  GraphTensors.list_tensors(graph)
  print("----------\n")

  print("\n----------")
  print("Aggregate tensors with their types.")
  state, dicts = GraphTensors.get_nodes_with_type(graph)
  assert state, "Can't form dictionary: {}".format(dicts)
  type_1 = list(dicts.keys())[0]
  operators = dicts[type_1]
  print(operators)
  print("----------\n")

  print("\n----------")
  print("Write graph for visualization via TFBoard.")
  logdir_path = "/Users/jiankaiwang/Desktop/logs"
  state, error = OperateFrozenModel.write_graph_for_tfboard(pb_path, logdir_path)
  assert state, "Error in writing out frozen graph: {}.".format(error)
  print("----------\n")








