Getting Started
===============
Inside IPython, load the extension::

    %load_ext cypher

And then you are reay to go by using the ``%cypher`` cell magic::

    %cypher MATCH (a)-[]-(b) RETURN a, b

Some Cypher queries can be very long, in those cases the the line magic,
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

Note that by default ``ipython-cypher`` will connect to <http://localhost:7474/db/data>.

Queries results can be stored in a variable and then converted to other formats::

    results = %cypher MATCH (a)-[]-(b) RETURN a, b
    results.get_dataframe()

    results.get_networkx()

Options
=======

Usage out of IPython
====================

``ipython-cypher`` can also be easily used outside IPython.
The main function that makes this possible is ``cypher.run()``, that takes a
Cypher query string, and optional parameters for the query in a dictionary.
By default, ``http://localhost:7474/db/data`` will be used,
but a URL connection string to a Neo4j instance, or a
``cypher.run.Connection`` object can be passed as the last parameter::

    import cypher

    cypher.run("MATCH (a)-[]-(b) RETURN a, b")
