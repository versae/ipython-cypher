import codecs
from collections import defaultdict
import copy
import csv
from functools import reduce
import json
import prettytable
import operator
import os.path
try:
    import matplotlib.pylab as plt
    import matplotlib.patches as mpatches
    import matplotlib.lines as Line2D
except:
    plt = None
    mpatches = None
    Line2D = None
try:
    import networkx as nx
except ImportError:
    nx = None
try:
    import pandas as pd
except ImportError:
    pd = None

from cypher.column_guesser import ColumnGuesserMixin
from cypher.connection import Connection
from cypher.utils import (
    DefaultConfigurable, DEFAULT_CONFIGURABLE, PY2, StringIO,
    string_types
)


def unduplicate_field_names(field_names):
    """Append a number to duplicate field names to make them unique. """
    res = []
    for k in field_names:
        if k in res:
            i = 1
            while k + '_' + str(i) in res:
                i += 1
            k += '_' + str(i)
        res.append(k)
    return res


class UnicodeWriter(object):
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        _row = [s.encode("utf-8")
                if PY2
                else s
                for s in row]
        self.writer.writerow(_row)
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        if PY2:
            data = data.decode("utf-8")
            # ... and reencode it into the target encoding
            data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


class CsvResultDescriptor(object):
    """Provides IPython Notebook-friendly output for the feedback after
    a ``.csv`` called."""

    def __init__(self, file_path):
        self.file_path = file_path

    def __repr__(self):
        return 'CSV results at %s' % os.path.join(os.path.abspath('.'),
                                                  self.file_path)

    def _repr_html_(self):
        return '<a href="%s">CSV results</a>' % os.path.join('.', 'files',
                                                             self.file_path)


class ResultSet(list, ColumnGuesserMixin):
    """
    Results of a Cypher query.

    Can access rows listwise, or by string value of leftmost column.
    """
    def __init__(self, results, query, config):
        self._results = results
        self._labels = defaultdict(int)
        self._types = defaultdict(int)
        self._graph = None
        self._dataframe = None
        self.keys = results.columns
        self.query = query
        self.config = config
        self.limit = config.auto_limit
        style_name = config.style
        self.style = prettytable.__dict__[style_name.upper()]
        if results is not None:
            if not config.rest:
                _results = results.rows
            else:
                _results = results
            _results = _results or []
            if self.limit:
                list.__init__(self, _results[:self.limit])
            else:
                list.__init__(self, _results)
            if self.keys is not None:
                self.field_names = unduplicate_field_names(self.keys)
            else:
                self.field_names = []
            self.pretty = prettytable.PrettyTable(self.field_names)
            if not config.auto_pandas:
                for row in self[:config.display_limit or None]:
                    self.pretty.add_row(row)
            self.pretty.set_style(self.style)
        else:
            list.__init__(self, [])
            self.pretty = None

    def _repr_html_(self):
        if self.config.auto_html:
            return self._results._repr_html_()
        elif self.pretty:
            result = self.pretty.get_html_string()
            if (self.config.display_limit
                    and len(self) > self.config.display_limit):
                result = """
                %s\n<span style="font-style:italic;text-align:center;">%d rows,
                truncated to displaylimit of %d</span>""" % (
                    result, len(self), self.config.display_limit
                )
            return result
        else:
            return None

    def __str__(self, *arg, **kwarg):
        """String representation of a ``ResultSet``."""
        return str(self.pretty or '')

    def __getitem__(self, key):
        """
        Access by integer (row position within result set)
        or by string (value of leftmost column)
        """
        try:
            return list.__getitem__(self, key)
        except TypeError:
            result = [row for row in self if row[0] == key]
            if not result:
                raise KeyError(key)
            if len(result) > 1:
                raise KeyError('%d results for "%s"' % (len(result), key))
            return result[0]

    def get_dataframe(self):
        """Returns a Pandas DataFrame instance built from the result set."""
        if pd is None:
            raise ImportError("Try installing Pandas first.")
        frame = pd.DataFrame(self[:], columns=(self and self.keys) or [])
        return frame

    def _get_dataframe(self):
        if self._dataframe is None:
            self._dataframe = self.get_dataframe()
        return self._dataframe
    dataframe = property(_get_dataframe)

    def get_graph(self, directed=True):
        """Returns a NetworkX multi-graph instance built from the result set

        :param directed: boolean, optional (default=`True`).
            Whether to create a direted or an undirected graph.
        """
        if nx is None:
            raise ImportError("Try installing NetworkX first.")
        if directed:
            graph = nx.MultiDiGraph()
        else:
            graph = nx.MultiGraph()
        for item in self._results.graph:
            for node in item['nodes']:
                properties = copy.deepcopy(node['properties'])
                properties['labels'] = node['labels']
                graph.add_node(node['id'], **properties)
            for rel in item['relationships']:
                properties = copy.deepcopy(rel['properties'])
                properties.update(
                    id=rel['id'],
                    type=rel['type']
                )
                graph.add_edge(rel['startNode'], rel['endNode'],
                               key=rel.get('type'), **properties)
        return graph

    def _get_graph(self):
        if self._graph is None:
            self._graph = self.get_graph()
        return self._graph
    graph = property(_get_graph)

    def draw(self, directed=True, layout="spring",
             node_label_attr=None, show_node_labels=True,
             edge_label_attr=None, show_edge_labels=True,
             node_size=1600, node_color='blue', node_alpha=0.3,
             node_text_size=12,
             edge_color='blue', edge_alpha=0.3, edge_tickness=1,
             edge_text_pos=0.3,
             text_font='sans-serif', ax=None):
        """Plot of a NetworkX multi-graph instance

        :param directed: boolean, optional (default=`True`).
            Whether to return a directed graph or not.
        :param layout: string, optional (default=`"spring"`).
            Layout to apply. Any of the possible NetworkX layouts will work:
            ``'circular_layout'``, ``'random_layout'``, ``'shell_layout'``,
            ``'spring_layout'``, ``'spectral_layout'``,
            or ``'fruchterman_reingold_layout'``.
        :param node_label_attr: string, optional (default=`None`).
            Attribute of the nodes that has to be used as the label.
        :param show_node_labels: boolean, optional (default=`True`).
            Whether to show or not the labels of the nodes.
        :param edge_label_attr: boolean, optional (default=`None`).
            Attribute of the edges that has to be used as the label.
        :param show_edge_labels: . optional (default=`True`).
            Whether to show or not the labels of the edges.
        :param node_size: integer, optional (default=`1600`).
            Desired size for nodes.
        :param node_color: color string, or array of floats, (default=`'blue'`)
            Node color. Can be a single color format string, or a sequence of
            colors with the same length as nodelist. If numeric values are
            specified they will be mapped to colors using the ``cmap`` and
            ``vmin``, ``vmax`` parameters. See ``matplotlib.scatter`` for more
            details.
        :param node_alpha: float, optional (default=`0.3`).
            Between 0 and 1 for transparency of nodes.
        :param node_text_size: integer, optional (default=`12`).
            Size of the node text.
        :param edge_color: color string, or array of floats (default=`'blue'`)
            Edge color. Can be a single color format string, or a sequence of
            colors with the same length as edgelist. If numeric values are
            specified they will be mapped to colors using the ``edge_cmap`` and
            ``edge_vmin``, ``edge_vmax`` parameters.
        :param edge_alpha: float, optional (default=`0.3`)
            Transparency for thee edges.
        :param edge_tickness: float or integer, optional (default=`1`).
            Thickness of the lines drawn for the edges.
        :param edge_text_pos: . Default to optional (d0)=
        :param text_font: . Default to optional (default=`'sans-serif'`).
        :param ax: ``matplotlib.Figure``, optional (default=`None`).
            A ``matplotlib.Figure`` to use when rendering the graph. If `None`,
            a new object is created and returned.----

        :return: a ``matplotlib.Figure`` with the graph rendered.
        """
        graph = self.get_graph(directed=directed)
        pos = getattr(nx, "{}_layout".format(layout))(graph)
        node_labels = {}
        edge_labels = {}
        node_colors = set()
        if show_node_labels:
            for node, props in graph.nodes(data=True):
                labels = props.pop('labels', [])
                for label in labels:
                    node_colors.add(label)
                if node_label_attr is None:
                    node_labels[node] = "$:{}$\n{}".format(
                        ":".join(labels),
                        next(iter(props.values())) if props else "",
                    )
                else:
                    props_list = ["{}: {}".format(k, v)
                                  for k, v in props.items()]
                    node_labels[node] = "$:{}$\n{}".format(
                        ":".join(labels), "\n".join(props_list)
                    )
        node_color = []
        node_colors = list(node_colors)
        legend_colors = []
        colors = list(plt.matplotlib.colors.ColorConverter().cache.items())[2:]
        for _, color_rgb in colors[:len(node_colors)]:
            node_color.append(color_rgb)
            legend_colors.append(color_rgb)
        if show_edge_labels:
            for start, end, props in graph.edges(data=True):
                if edge_label_attr is None:
                    edge_label = props.get("type", '')
                else:
                    edge_label = props.get(edge_label_attr, '')
                edge_labels[(start, end)] = edge_label
        if not ax:
            fig = plt.figure()
            ax = fig.add_subplot(111)
        nodes = nx.draw_networkx_nodes(
            graph, pos=pos, node_color=node_color,
            node_size=node_size, alpha=node_alpha,
            ax=ax
        )
        nx.draw_networkx_labels(
            graph, pos=pos, labels=node_labels,
            font_size=node_text_size,
            font_family=text_font,
            ax=ax
        )
        nx.draw_networkx_edges(
            graph, pos=pos, width=edge_tickness,
            alpha=edge_alpha, edge_color=edge_color,
            ax=ax
        )
        nx.draw_networkx_edge_labels(
            graph, pos=pos, edge_labels=edge_labels,
            ax=ax
        )
        ax.legend([plt.Line2D([0], [0], linestyle="none", marker="o",
                              alpha=node_alpha,
                              markersize=10, markerfacecolor=color)
                  for color in legend_colors],
                  node_colors, loc=(-0.25, 1), numpoints=1, frameon=False)
        ax.set_axis_off()
        return graph, ax, nodes

    def pie(self, key_word_sep=" ", title=None, **kwargs):
        """Generates a pylab pie chart from the result set.

        ``matplotlib`` must be installed, and in an
        IPython Notebook, inlining must be on::

            %%matplotlib inline

        Values (pie slice sizes) are taken from the
        rightmost column (numerical values required).
        All other columns are used to label the pie slices.

        :param key_word_sep: string used to separate column values
                             from each other in pie labels
        :param title: plot title, defaults to name of value column
        :kwargs: any additional keyword arguments will be passsed
            through to ``matplotlib.pylab.pie``.
        """
        if not plt:
            raise ImportError("Try installing matplotlib first.")
        self.guess_pie_columns(xlabel_sep=key_word_sep)
        pie = plt.pie(self.ys[0], labels=self.xlabels, **kwargs)
        plt.title(title or self.ys[0].name)
        return pie

    def plot(self, title=None, **kwargs):
        """Generates a pylab plot from the result set.

        ``matplotlib`` must be installed, and in an
        IPython Notebook, inlining must be on::

            %%matplotlib inline

        The first and last columns are taken as the X and Y
        values.  Any columns between are ignored.

        :param title: plot title, defaults to names of Y value columns

        Any additional keyword arguments will be passsed
        through to ``matplotlib.pylab.plot``.
        """
        if not plt:
            raise ImportError("Try installing matplotlib first.")
        self.guess_plot_columns()
        self.x = self.x or range(len(self.ys[0]))
        coords = reduce(operator.add, [(self.x, y) for y in self.ys])
        plot = plt.plot(*coords, **kwargs)
        if hasattr(self.x, 'name'):
            plt.xlabel(self.x.name)
        ylabel = ", ".join(y.name for y in self.ys)
        plt.title(title or ylabel)
        plt.ylabel(ylabel)
        return plot

    def bar(self, key_word_sep=" ", title=None, **kwargs):
        """Generates a pylab bar plot from the result set.

        ``matplotlib`` must be installed, and in an
        IPython Notebook, inlining must be on::

            %%matplotlib inline

        The last quantitative column is taken as the Y values;
        all other columns are combined to label the X axis.

        :param title: plot title, defaults to names of Y value columns
        :param key_word_sep: string used to separate column values
                             from each other in labels

        Any additional keyword arguments will be passsed
        through to ``matplotlib.pylab.bar``.
        """
        if not plt:
            raise ImportError("Try installing matplotlib first.")
        self.guess_pie_columns(xlabel_sep=key_word_sep)
        plot = plt.bar(range(len(self.ys[0])), self.ys[0], **kwargs)
        if self.xlabels:
            plt.xticks(range(len(self.xlabels)), self.xlabels,
                       rotation=45)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ys[0].name)
        return plot

    def csv(self, filename=None, **format_params):
        """Generates results in comma-separated form.  Write to ``filename``
        if given. Any other parameter will be passed on to ``csv.writer``.

        :param filename: if given, the CSV will be written to filename.

        Any additional keyword arguments will be passsed
        through to ``csv.writer``.
        """
        if not self.pretty:
            return None  # no results
        if filename:
            outfile = open(filename, 'w')
        else:
            outfile = StringIO()
        writer = UnicodeWriter(outfile, **format_params)
        writer.writerow(self.field_names)
        for row in self:
            writer.writerow(row)
        if filename:
            outfile.close()
            return CsvResultDescriptor(filename)
        else:
            return outfile.getvalue()


def interpret_stats(results):
    """Generates the string to be shown as updates after the execution of a
    Cypher query

    :param results: ``ResultSet`` with the raw results of the execution of
                    the Cypher query
    """
    stats = results.stats
    contains_updates = stats.pop("contains_updates", False) if stats else False
    if not contains_updates:
        result = '{} rows affected.'.format(len(results))
    else:
        result = ''
        for stat, value in stats.items():
            if value:
                result = "{}\n{} {}.".format(result, value,
                                             stat.replace("_", " "))
    return result.strip()


def extract_params_from_query(query, user_ns):
    """Generates a dictionary with safe keys and values to pass onto Neo4j

    :param query: string with the Cypher query to execute
    :param user_ns: dictionary with the IPython user space
    """
    # TODO: Optmize this function
    params = {}
    for k, v in user_ns.items():
        try:
            json.dumps(v)
            params[k] = v
        except:
            pass
    return params


def run(query, params=None, config=None, conn=None, **kwargs):
    """Executes a query and depending on the options of the extensions will
    return raw data, a ``ResultSet``, a Pandas ``DataFrame`` or a
    NetworkX graph.

    :param query: string with the Cypher query
    :param params: dictionary with parameters for the query (default=``None``)
    :param config: Configurable or NamedTuple with extra IPython configuration
                   details. If ``None``, a new object will be created
                   (defaults=``None``)
    :param conn: connection dictionary or string for the Neo4j backend.
                 If ``None``, a new connection will be created
                 (default=``None``)
    :param **kwargs: Any of the cell configuration options.
    """
    if params is None:
        params = {}
    if conn is None:
        conn = Connection.get(DEFAULT_CONFIGURABLE["uri"])
    elif isinstance(conn, string_types):
        conn = Connection.get(conn)
    if config is None:
        default_config = DEFAULT_CONFIGURABLE.copy()
        kwargs.update(default_config)
        config = DefaultConfigurable(**kwargs)
    if query.strip():
        # TODO: Handle multiple queries
        params = extract_params_from_query(query, params)
        result = conn.session.query(query, params,
                                    data_contents=config.data_contents)
        if config.feedback:
            print(interpret_stats(result))
        resultset = ResultSet(result, query, config)
        if config.auto_pandas:
            return resultset.get_dataframe()
        elif config.auto_networkx:
            graph = resultset.get_graph()
            resultset.draw()
            return graph
        else:
            return resultset  # returning only last result, intentionally
    else:
        return 'Connected: %s' % conn.name
