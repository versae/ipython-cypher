
.. code:: python

    %load_ext cypher
.. code:: python

    %config CypherMagic

.. parsed-literal::

    CypherMagic options
    -----------------
    CypherMagic.auto_html=<Bool>
        Current: False
        Return a D3 representation of the graph instead of regular result sets
    CypherMagic.auto_limit=<Int>
        Current: 0
        Automatically limit the size of the returned result sets
    CypherMagic.auto_networkx=<Bool>
        Current: False
        Return Networkx MultiDiGraph instead of regular result sets
    CypherMagic.auto_pandas=<Bool>
        Current: False
        Return Pandas DataFrame instead of regular result sets
    CypherMagic.data_contents=<Bool>
        Current: True
        Bring extra data to render the results as a graph
    CypherMagic.display_limit=<Int>
        Current: 0
        Automatically limit the number of rows displayed (full result set is still
        stored)
    CypherMagic.feedback=<Bool>
        Current: True
        Print number of rows affected
    CypherMagic.uri=<Unicode>
        Current: u'http://localhost:7474/db/data'
        Default database URL if none is defined inline
    CypherMagic.rest=<Bool>
        Current: False
        Return full REST representations of objects inside the result sets
    CypherMagic.short_errors=<Bool>
        Current: True
        Don't display the full traceback on Neo4j errors
    CypherMagic.style=<Unicode>
        Current: u'DEFAULT'
        Set the table printing style to any of prettytable's defined styles
        (currently DEFAULT, MSWORD_FRIENDLY, PLAIN_COLUMNS, RANDOM)


.. code:: python

    %cypher optional match (n)-[r]-() delete n, r

.. parsed-literal::

    6 relationship deleted.
    6 nodes deleted.




.. parsed-literal::

    []



.. code:: python

    %%cypher
    create
        // Nodes
        (Neo:Crew {name:'Neo'}),
        (Morpheus:Crew {name: 'Morpheus'}),
        (Trinity:Crew {name: 'Trinity'}),
        (Cypher:Crew:Matrix {name: 'Cypher'}),
        (Smith:Matrix {name: 'Agent Smith'}),
        (Architect:Matrix {name:'The Architect'}),
        // Relationships
        (Neo)-[:KNOWS]->(Morpheus),
        (Neo)-[:LOVES]->(Trinity),
        (Morpheus)-[:KNOWS]->(Trinity),
        (Morpheus)-[:KNOWS]->(Cypher),
        (Cypher)-[:KNOWS]->(Smith),
        (Smith)-[:CODED_BY]->(Architect);

.. parsed-literal::

    7 labels added.
    6 nodes created.
    6 properties set.
    6 relationships created.




.. parsed-literal::

    []



.. code:: python

    %cypher match (n)-[r]-() return n, count(r) as degree order by degree desc

.. parsed-literal::

    6 rows affected.




.. raw:: html

    <table>
        <tr>
            <th>n</th>
            <th>degree</th>
        </tr>
        <tr>
            <td>{u'name': u'Morpheus'}</td>
            <td>3</td>
        </tr>
        <tr>
            <td>{u'name': u'Cypher'}</td>
            <td>2</td>
        </tr>
        <tr>
            <td>{u'name': u'Neo'}</td>
            <td>2</td>
        </tr>
        <tr>
            <td>{u'name': u'Trinity'}</td>
            <td>2</td>
        </tr>
        <tr>
            <td>{u'name': u'Agent Smith'}</td>
            <td>2</td>
        </tr>
        <tr>
            <td>{u'name': u'The Architect'}</td>
            <td>1</td>
        </tr>
    </table>



.. code:: python

    %matplotlib inline
.. code:: python

    results = %cypher match (n)-[r]-() return n.name as name, count(r) as degree order by degree desc
    results.dataframe()

.. parsed-literal::

    6 rows affected.




.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>name</th>
          <th>degree</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>      Morpheus</td>
          <td> 3</td>
        </tr>
        <tr>
          <th>1</th>
          <td>       Trinity</td>
          <td> 2</td>
        </tr>
        <tr>
          <th>2</th>
          <td>   Agent Smith</td>
          <td> 2</td>
        </tr>
        <tr>
          <th>3</th>
          <td>           Neo</td>
          <td> 2</td>
        </tr>
        <tr>
          <th>4</th>
          <td>        Cypher</td>
          <td> 2</td>
        </tr>
        <tr>
          <th>5</th>
          <td> The Architect</td>
          <td> 1</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    results.plot()



.. parsed-literal::

    [<matplotlib.lines.Line2D at 0x7f23e3e72950>]




.. image:: examples_files/examples_7_1.png


.. code:: python

    results.bar()



.. parsed-literal::

    <Container object of 6 artists>




.. image:: examples_files/examples_8_1.png


.. code:: python

    results.pie()



.. parsed-literal::

    ([<matplotlib.patches.Wedge at 0x7f23e3c98f90>,
      <matplotlib.patches.Wedge at 0x7f23e3ca69d0>,
      <matplotlib.patches.Wedge at 0x7f23e3cb2390>,
      <matplotlib.patches.Wedge at 0x7f23e3cb2d10>,
      <matplotlib.patches.Wedge at 0x7f23e3cbe6d0>,
      <matplotlib.patches.Wedge at 0x7f23e3ccb090>],
     [<matplotlib.text.Text at 0x7f23e3ca6590>,
      <matplotlib.text.Text at 0x7f23e3ca6f90>,
      <matplotlib.text.Text at 0x7f23e3cb2950>,
      <matplotlib.text.Text at 0x7f23e3cbe310>,
      <matplotlib.text.Text at 0x7f23e3cbec90>,
      <matplotlib.text.Text at 0x7f23e3ccb650>])




.. image:: examples_files/examples_9_1.png


.. code:: python

    for i in range(1, 5):
        %cypher match (n) return n, n.name limit {i}

.. parsed-literal::

    1 rows affected.
    2 rows affected.
    3 rows affected.
    4 rows affected.


.. code:: python

    results = %cypher match (n)-[r]-() return n.name as name, n, r, count(r) as degree order by degree desc

.. parsed-literal::

    12 rows affected.


.. code:: python

    results.draw()



.. parsed-literal::

    (<networkx.classes.multidigraph.MultiDiGraph at 0x7f23e3c5a510>,
     <matplotlib.axes._subplots.AxesSubplot at 0x7f23e3ccba90>,
     <matplotlib.collections.PathCollection at 0x7f23e3c06050>)



.. parsed-literal::

    /home/versae/.venvs/ipython-cypher/local/lib/python2.7/site-packages/matplotlib/text.py:52: UnicodeWarning: Unicode equal comparison failed to convert both arguments to Unicode - interpreting them as being unequal
      if rotation in ('horizontal', None):
    /home/versae/.venvs/ipython-cypher/local/lib/python2.7/site-packages/matplotlib/text.py:54: UnicodeWarning: Unicode equal comparison failed to convert both arguments to Unicode - interpreting them as being unequal
      elif rotation == 'vertical':



.. image:: examples_files/examples_12_2.png

