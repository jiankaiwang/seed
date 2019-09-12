# TF1_FrozenModel.py



## Dependencies

*   Not built-in packages:
    *    `tensorflow` (recommended >= 1.13.2)



## APIs



### OperateFrozenModel

```python
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
    
  @staticmethod
  def load_frozen_model(pb_path, graph_name=""):
    """Load the frozen model. (Serial)

    Returns:
      state: True or False
      Message: None (for True) or Message (for False)
    """
 
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
```



### GraphOperations

```python
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
```





### GraphTensors

```python
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
```

