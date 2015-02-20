==============
ipython-cypher
==============

:Author: Javier de la Rosa, http://versae.es

Introduces a ``%cypher`` (and ``%%cypher``) magic for Neo4j in IPython.
Inspired by Catherine Devlin's ipython-sql_.

Connect to a graph database, using ``neo4jrestclient_`` driver, then issue Cypher
commands within IPython or IPython Notebook. See examples_.

Install
-------
As easy as usual::

    pip install ipython-cypher

Usage
-----

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

Note that by default ``ipython-cypher`` will connect to ``http://localhost:7474/db/data``.

Queries results can be stored in a variable and then converted to a Pandas
``DataFrame``::

    results = %cypher MATCH (a)-[]-(b) RETURN a, b
    results.get_dataframe()

Or to a NetworkX ``MultiDiGraph``::

    results.get_graph()

For more detailed descriptions, please visit the official documentation_.


.. _examples: http://nbviewer.ipython.org/github/versae/ipython-cypher/blob/master/docs/examples.ipynb
.. _neo4jrestclient: https://pypi.python.org/pypi/neo4jrestclient
.. _documentation: http://ipython-cypher.readthedocs.org/en/latest/
.. _ipython-sql: https://github.com/catherinedevlin/ipython-sql
