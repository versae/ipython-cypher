==============
ipython-cypher
==============

:Author: Javier de la Rosa, http://versae.es

Introduces a %cypher (or %%cypher) magic for Neo4j in IPython.
Inspired by Catherine Devlin's ipython-sql_.

Connect to a graph database, using neo4jrestclient_ driver, then issue Cypher
commands within IPython or IPython Notebook. See examples_.

Install
-------

    pip install ipython-cypher

Then open an IPython or IPython Notebook and load the module

    %load_ext cypher

By default, it will connect to `http://localhost:7474/db/data`

    %%cypher
    match (n) return id(n) as id, n.name as name skip 1 limit 3


    %cypher match (n) return id(n) as id, n.name as name skip 1 limit 3

    results = %cypher match (n) return id(n) as id, n.name as name skip 1 limit 3
    results.dataframe()

    results.pie()

More soon...


Credits
-------
- Distribute_
- Buildout_
- modern-package-template_

.. _Distribute: http://pypi.python.org/pypi/distribute
.. _Buildout: http://www.buildout.org/
.. _modern-package-template: http://pypi.python.org/pypi/modern-package-template
.. _ipython-sql: https://github.com/catherinedevlin/ipython-sql
.. _examples: http://nbviewer.ipython.org/github/versae/ipython-cypher/blob/master/src/examples.ipynb
.. _neo4jrestclient: https://pypi.python.org/pypi/neo4jrestclient
