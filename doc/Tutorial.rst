Tutorial
========

Let's start by importing the modules we will use

.. code-block:: python

    import pandas as pd
    import extremals as xt

and let's fix an example dataframe

.. code-block:: python

    data = pd.DataFrame( 
    {'col1' : [3, 100, 1, -3, None, 9, 22, 8, 9, 0],  
     'col2' : [100, 200, -123, None, 7, -34.5, 95, 3, 12, -567], 
     'col3' : [0, 74, -13.4, 44, 21, 3, -4, None, None, 21]},
     index  = list('abcdefghil')
     )

    # data is the dataframe
        col1   col2  col3
    a    3.0  100.0   0.0
    b  100.0  200.0  74.0
    c    1.0 -123.0 -13.4
    d   -3.0    NaN  44.0
    e    NaN    7.0  21.0
    f    9.0  -34.5   3.0
    g   22.0   95.0  -4.0
    h    8.0    3.0   NaN
    i    9.0   12.0   NaN
    l    0.0 -567.0  21.0

The first step is look at the data and see which rows look different. My first guess would be ``l,b,g``.
Let's run see what a :py:class:`TWDTest <extremals.TWDTest>` tells us by running 

.. code-block:: python

    result = xt.AddTWDTest(data)
    
    # result is the dataframe
        col1   col2  col3       TWD
    e    NaN    7.0  21.0  0.102827
    h    8.0    3.0   NaN  0.153905
    i    9.0   12.0   NaN  0.157379
    f    9.0  -34.5   3.0  0.282413
    d   -3.0    NaN  44.0  0.552499
    g   22.0   95.0  -4.0  0.557941
    a    3.0  100.0   0.0  0.602914
    c    1.0 -123.0 -13.4  0.727218
    l    0.0 -567.0  21.0  1.075787
    b  100.0  200.0  74.0  2.024297
    
``result`` is a concatenation of ``data`` (up to sorting) and a :py:class:`TWDTest <extremals.TWDTest>` on ``data``. Moreover it is sorted
according to this last column. In particular the extremal rows are the last one, so my guess was almost correct: got ``b,l``,
even though not in order, but miss ``c``. That is the reason of :py:func:`PurgeTWD <extremals.PurgeTWD>` existence and we will come back to this.
The last column, as a series, can be obtained with the command

.. code-block:: python
    
    xt.TWDExtremals()
    
In case you don't care about column two and you want to concentrate on the other twos run

.. code-block:: python

    keys = ['col1', 'col3']
    new_result = xt.AddTWDTest(data, keys = keys)

    # new_result is the dataframe
        col1   col2  col3       TWD
    e    NaN    7.0  21.0  0.036613
    i    9.0   12.0   NaN  0.083122
    h    8.0    3.0   NaN  0.094124
    l    0.0 -567.0  21.0  0.218748
    f    9.0  -34.5   3.0  0.281877
    g   22.0   95.0  -4.0  0.350183
    a    3.0  100.0   0.0  0.387113
    d   -3.0    NaN  44.0  0.552499
    c    1.0 -123.0 -13.4  0.584334
    b  100.0  200.0  74.0  1.647650

As you see row ``l`` went back because it is not any special with respect to the chosen columns.

There is a process called normalization that can be applied to a dataframe and can shed some light on how the TWD series is build.
You can read more in :py:func:`Normalize <extremals.Normalize>`.


.. code-block:: python

    nor_result = xt.AddTWDTest(data, normalized = True)

    # nor_result is the dataframe
           col1      col2      col3       TWD
    e       NaN  0.066215  0.036613  0.102827
    h -0.094124  0.059781       NaN  0.153905
    i -0.083122  0.074257       NaN  0.157379
    f -0.083122 -0.000536 -0.198754  0.282413
    d -0.215140       NaN  0.337359  0.552499
    g  0.059897  0.207759 -0.290286  0.557941
    a -0.149131  0.215801 -0.237982  0.602914
    c -0.171134 -0.142884 -0.413199  0.727218
    l -0.182136 -0.857039  0.036613  1.075787
    b  0.918013  0.376647  0.729637  2.024297
    
The first three columns are obtained from ``data`` applying :py:func:`Normalize <extremals.Normalize>`. The last column, which coincides with the last of ``result``,
is the sum of the previous columns up to sign. Those numbers represent the individual contribution of each column and measure the *relative* distance from the mean.
Moreover they are opportunely uniformized: for a column in ``data``, if you sum up the squares of their values you get 1.

Using the function :py:func:`OutOfBound <extremals.OutOfBound>` we can restrict our attention to just a portion of the results

.. code-block:: python

    close_look = xt.OutOfBound(nor_result, high = 0.3, key = 'TWD')

    # close_look is the dataframe
           col1      col2      col3       TWD
    c -0.171134 -0.142884 -0.413199  0.727218
    l -0.182136 -0.857039  0.036613  1.075787
    b  0.918013  0.376647  0.729637  2.024297

Here we selected 30% of ``nor_result`` according to the column ``'TWD'``.

.. _Purge steps:

Let's see now the benefits of selecting extremal rows in different steps.

.. code-block:: python

    purged, good = xt.PurgeTWD(data, high = 0.3, steps = 1)
    
    # purged is the dataframe
        col1   col2  col3
    b  100.0  200.0  74.0
    l    0.0 -567.0  21.0
    c    1.0 -123.0 -13.4

In ``purged`` we removed 30% of ``data`` in one cut and ordered it according to the removal order. ``good`` contains the remaining rows of ``data``.
Let's do the same but in two steps.

.. code-block:: python

    purged2, good2 = xt.PurgeTWD(data, high = 0.3, steps = 2)
    
    # purged2 is the dataframe
        col1   col2  col3
    b  100.0  200.0  74.0
    l    0.0 -567.0  21.0
    g   22.0   95.0  -4.0

Here we see ``g`` appearing again among the "bad" rows. This is because in the first step rows ``b,l`` are removed, means are computed again and they
are not unbalanced by the extremal rows ``b,l``. We can concretely see this running

.. code-block:: python
    
    bad_step_1, good_step_1 = xt.PurgeTWD(data, high = 2) # steps = 1 is default
    new_order = xt.AddTWDTest(good_step_1)
    # new_order is the dataframe
       col1   col2  col3       TWD
    h   8.0    3.0   NaN  0.080280
    i   9.0   12.0   NaN  0.120495
    e   NaN    7.0  21.0  0.278729
    f   9.0  -34.5   3.0  0.448556
    a   3.0  100.0   0.0  0.874074
    d  -3.0    NaN  44.0  1.275176
    c   1.0 -123.0 -13.4  1.478224
    g  22.0   95.0  -4.0  1.493418

``high = 2`` instructs the function to remove only 2 of the bad rows, thus ``good_step_1`` is ``data`` with rows ``b,l`` removed. Applying a :py:class:`TWDTest <extremals.TWDTest>` on it we see that is now ``g`` ranking higher than ``c``,
as we were expecting at the beginning.

