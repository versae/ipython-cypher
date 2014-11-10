ipython-cypher
==============

IPython cell magic for Neo4j Cypher.

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
    
    results.plot()
    
More soon...
