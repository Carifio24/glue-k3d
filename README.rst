Experimental K3D-jupyter plugin for glue
----------------------------------------

This package is a plugin for `glue <https://glueviz.org/>`_ that allows linking glue
to `K3D-jupyter <https://k3d-jupyter.org/>`_. This currently involves two main pieces of functionality

- Export HTML views from glue's `3D VisPy-powered viewers <https://github.com/glue-viz/glue-vispy-viewers>`_
- Experimental glue viewers powered by K3D


============
Installation
============

glue-k3d is not yet available on pip, but can be installed directly from this repository::

    pip install git+https://github.com/glue-viz/glue-k3d


==================
K3D HTML Exporters
==================

The HTML exporters are exposed as viewer tools in the Qt versions of the VisPy scatter and volume viewers.


========
Viewers
========

This package contains two experimental K3D-powered viewers which can be used with glue-jupyter, which are
3D scatter and volume viewers.
