Python module extremals
=======================

Introduction
~~~~~~~~~~~~
    The python module :ref:`extremals <Documentation:extremals Module>`  contains a set of tools to inspect pandas dataframes looking for
    "extremals rows", that is rows "numerically different" from other ones. This may help filtering a dataframe from anomalous numerical data or, on the
    contrary, highlight exceptional rows from common ones.
    
    But what makes some bunch of numbers special? The answer is: it depends on how you measure them. The :ref:`extremals <Documentation:extremals Module>` module
    provides a special class called :py:class:`Test <extremals.Test>`, which implements the idea of such a measure, creating an ordered series of its results.
    Multiple tests can be run on a dataframe using the class :py:class:`Extremals <extremals.Extremals>`, which allows to build a dataframe of all this different measures.
    
    Tests can be user defined, but :ref:`extremals <Documentation:extremals Module>` provides some special tests as subclasses of :py:class:`Test <extremals.Test>`:
    
    - :py:class:`ColTest <extremals.ColTest>` for testing a single column. Such tests can be run together using :py:class:`ExtremalsCol <extremals.ExtremalsCol>`,
      a subclass of :py:class:`Extremals <extremals.Extremals>`.
    
    - :py:class:`DiffTest <extremals.DiffTest>` for testing a difference of columns. Such tests can be run together using :py:class:`ExtremalsDiff <extremals.ExtremalsDiff>`,
      a subclass of :py:class:`Extremals <extremals.Extremals>`.
    
    - :py:class:`TWDTest <extremals.TWDTest>`, the Total Weighted Distance Test. Given a list of columns, this test associates with a row a sum of numbers between 0 and 1,
      one for each column. Those numbers measure how much an element differs by the mean of the column it belongs. Moreover they are opportunely normalized so that each
      contribution is uniform, i.e. does non depends on "hog big" the numbers are in a given column. See :py:func:`Normalize <extremals.Normalize>` for further information.

    Each test can have a meaning of its own, which depends on the nature of the dataframe it is applied to. On the other hand we follow the idea 
    that, in a general situation, :py:class:`TWDTest <extremals.TWDTest>` tests are able to separate common rows by "extremal" ones. Any istance of
    :py:class:`Extremals <extremals.Extremals>` by default runs an additional :py:class:`TWDTest <extremals.TWDTest>` on the results of the :py:class:`Test <extremals.Test>`
    istances it owns. 
    
    The function :py:func:`TWDExtremals <extremals.TWDExtremals>` is the easiest way to apply a :py:class:`TWDTest <extremals.TWDTest>` on
    a dataframe. To get the whole picture one can use :py:func:`AddTWDTest  <extremals.AddTWDTest>`, which appends the result of the test to the input dataframe.
    
    Once one obtain a series of dataframe as result of one or more tests, the function :py:func:`OutOfBound <extremals.OutOfBound>` can be used to extrapolate extremal
    rows: its arguments allow to specify how many or which proportion of rows to highlight.
    
    There is an interesting phenomenon happening here. Extremals rows in some cases can unbalance the means of the columns towards their values. The consequence is that, when extracting several
    extremal rows, the less "extremal" ones among them may be not special at all, while other "non extremal" rows looks peculiar. 
    You can see an example :ref:`here <Purge steps>`.
    The simple solution to avoid this is to split the selection of extremals rows in consecutive steps. The higher is their number, the more accurate is the result.
    The function which performs this action is called :py:class:`PurgeTWD <extremals.PurgeTWD>`. It splits a dataframe into a "purged" dataframe and a "good" dataframe by applying 
    :py:class:`TWDTest <extremals.TWDTest>` consecutively.
    
..
    .. toctree::
       :maxdepth: 2
       :caption: Contents:

Contents
~~~~~~~~

.. toctree::
    :maxdepth: 4
    
    Installation
    Tutorial
    Documentation
    


