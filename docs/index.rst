.. IPython Cypher documentation master file, created by
   sphinx-quickstart on Sun Jan 25 18:22:49 2015.

========================
IPython Cypher Extension
========================

``ipython-cypher`` is an IPython extension that provides
``%cypher`` and ``%%cypher`` magic for cells and lines, respectively. When
executed through ``ipython-cypher``, Cypher queries can be returned as a Pandas_
``DataFrame``, a NetworkX_ ``MultiDiGraph``, or plotted using matplotlib_.

This work is inspired by Catherine Devlin's `ipython-sql`_.


Releases
========
The latest release of ``ipython-cypher`` is **0.2.5**.


Requirements
============

- Python 2.7, 3.3, 3.4, 3.5
- Neo4j 1.9, 2.0, 2.1, 2.2


Dependencies
============
- neo4jrestclient 2.0

Depending on your needs, you might want to Pandas, NetworkX and/or matplotlib in order for
``ipython-cypher`` to produce adapted ouputs from Cypher queries. The
minimum versions supported are detailed below.

- Pandas 0.15
- NetworkX 2.0
- matplotlib 1.4


Installation
============
To install, run the following::

    $ pip install ipython-cypher


Getting Started
===============
Inside IPython, load the extension::

    %load_ext cypher

And then you are reay to go by using the ``%cypher`` line magic::

    %cypher MATCH (a)-[]-(b) RETURN a, b

Some Cypher queries can be very long, in those cases the the cell magic,
``%%cypher`` comes in handy::

    %%cypher
    create
        // Nodes
        (Neo:Crew {name:'Neo'}),
        (Morpheus:Crew {name: 'Morpheus'}),
        (Trinity:Crew {name: 'Trinity'}),
        // Relationships
        (Neo)-[:KNOWS]->(Morpheus),
        (Neo)-[:LOVES]->(Trinity),


Queries results can be stored in a variable and then converted to a Pandas
``DataFrame``::

    results = %cypher MATCH (a)-[]-(b) RETURN a, b
    results.get_dataframe()


Or to a NetworkX ``MultiDiGraph``::

    results.get_graph()


See real examples in an `IPython Notebook`_.

Configuration
=============

To change the behaviour of the cypher magic function, you can configure it::

    %config CypherMagic

    ... list of options

    %config CypherMagic.some_option = new_value



Contents
========

.. toctree::
   :maxdepth: 2

   introduction
   cypher


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _Pandas: http://pandas.pydata.org/pandas-docs/dev/
.. _NetworkX: https://networkx.github.io/
.. _matplotlib: http://matplotlib.org/
.. _IPython Notebook: http://nbviewer.ipython.org/github/versae/ipython-cypher/blob/master/docs/examples.ipynb
.. _`ipython-sql`: https://github.com/catherinedevlin/ipython-sql
