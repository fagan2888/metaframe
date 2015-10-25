Introduction
############

``metaframe`` is a MetaClass infrastructure to intercept instance
creation/initialization enabling modification of args/kwargs and instance.


Features:
=========

  - ``MetaFrame`` metaclass to apply to any object
    - With embedded staticmethod with_metaclass to enable inheritance

  - ``MetaFrameBase`` class from which classes can inherit
  - 3 hooks (classmethods)

    - ``_new_pre``: called before object creation
    - ``_new_do``: called for object creation
    - ``_init_pre``: called after object creation / before object initialization
    - ``_init_do``: called fo object initialization
    - ``_init_post``: called after object initialization

Installation
============

``metaframe`` is self-contained with no external dependencies

From pypi::

  pip install metaframe

From source:

  - Place the *metaframe* directory found in the sources inside your project
