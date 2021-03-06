configutator
------------

Maps yaml nodes and command line arguments to python function parameters.

To install: ``pip install configutator``
Or::

  git clone git@github.com:innovate-invent/configutator.git
  cd configutator
  python3 setup.py install

To use:
-------

#. Create a main function with all the parameters you need, annotated with any defaults.
#. Use the ``@ConfigMap`` and ``@ArgMap`` decorators to modify the default mappings if needed.
#. In the ``if __name__ == "__main__":`` block at the bottom of the file call the loadConfig() function.

Here is an example of the most basic use::

  from configutator import loadConfig
  from sys import argv
  
  def foo(param1, param2, param3=None):
    pass
  
  if __name__ == "__main__":
    for argmap in loadConfig(argv, (foo,)):
      foo(**argmap[foo])

One thing you need to keep in mind when working with configutator is that the config, command line arguments, and function parameters are all independant. The parameters given to @ConfigMap and @ArgMap are what connects them all. You should never have to change a function signature to modify the command line functionality.
