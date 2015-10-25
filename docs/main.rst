Usage
=====

``metaframe`` allows placing hooks into the creation/initializaion of objects,
enabling use cases like:

  - Modification of args/kwargs on the fly

  - Instance scanning/modification


Direct Inheritance
------------------

The package offers an already **metaclassed** base class supporting the
infrastructure.

  - ``MetaFrameBase``


Intercepting Object Creation
++++++++++++++++++++++++++++

An example from one of the tests included in the sources.

.. literalinclude:: ../tests/test_init_post.py
   :language: python
   :lines: 24-42

Doing something with it::

  ft = FrameTest()
  print('ft.check_val:', ft.check_val())

Yields the following output::

  ft.check_val: True

From the example:

  - No kwargs were passed to ``FrameTest`` for instantiation

  - During init ``self._KEY`` ('ft') was extracted from kwargs and assigned to
    ``self._val``

  - The ``kwargs`` were actually modified in the :func:`classmethod` where
    ``self._VAL`` was added with key ``self._KEY''

    And the modified ``kwargs`` were returned to be fed to object
    creation/initialization

  - Hence :func:`check_val` returning ``True``


Before initialization
+++++++++++++++++++++

The previous example can be extended to undo the effect achieved during object
creation.

Let's add a hook before init

.. literalinclude:: ../tests/test_init_post.py
   :language: python
   :lines: 43-48

Doing something with it::

  ft = FrameTest()
  print('ft.check_val:', ft.check_val())

Yields the following output::

  ft.check_val: False

The new code in :func:`_init_pre` removes the key ``self._KEY`` from the passed
``kwargs`` and returns them for object initialization.

After initialization
+++++++++++++++++++++

Redoing the effect by directly operating on the instance can be done after
initialization.

The hook after __init__

.. literalinclude:: ../tests/test_init_post.py
   :language: python
   :lines: 49-54

Repeating execution::

  ft = FrameTest()
  print('ft.check_val:', ft.check_val())

Yields the following output::

  ft.check_val: True

In this case the post initialization hook has directly changed the value of
attribute ``_val`` after object init.


Applying the metaclass
----------------------

Instead of inheriting from ``MetaFrameBase`` a derived metaclass for your class
can be created::

  import metaframe as mf

  class MyMetaClass(mf.MetaFrame):
      def _new_pre(cls, *args, **kwargs):
          # Insert a kwarg
          kwargs[cls._KEY] = cls._VAL
          return cls, args, kwargs

      def _init_pre(cls, obj, *args, **kwargs):
          # Remove the kwarg
          kwargs.pop(cls._KEY)
          return obj, args, kwargs

      def _init_post(cls, obj, *args, **kwargs):
          # change self._val ... to the expected value
          obj._val = obj._VAL
          return obj, args, kwargs

Now there is no need to declare the 3 hoods as ``classmethods`` because they are
already being declared in the MetaClass.

The ``FrameTest`` class would now look like this::

  class FrameTest(MyMetaClass.as_metaclass(object)):
      _KEY = 'ft'
      _VAL = True

      def __init__(self, *args, **kwargs):
          self._val = kwargs.get(self._KEY, False)

      def check_val(self):
          return self._val == self._VAL

The execution examples remain unchanged.

Alternatively, you can directly MetaFrame-enable a class applying ``MetaFrame``
as metaclass and defining the methods in the class as ``@classmethods``::

  class FrameTest(mf.MetaFrame.as_metaclass(object)):
      _KEY = 'ft'
      _VAL = True

    @classmethod
    def _new_pre(cls, *args, **kwargs):
        # Insert a kwarg
        kwargs[cls._KEY] = cls._VAL
        return cls, args, kwargs

    @classmethod
    def _init_pre(cls, obj, *args, **kwargs):
        # Remove the kwarg
        kwargs.pop(cls._KEY)
        return obj, args, kwargs

    @classmethod
    def _init_post(cls, obj, *args, **kwargs):
        # change self._val ... to the expected value
        obj._val = obj._VAL
        return obj, args, kwargs

      def __init__(self, *args, **kwargs):
          self._val = kwargs.get(self._KEY, False)

      def check_val(self):
          return self._val == self._VAL
