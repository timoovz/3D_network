import sql

import plotly.graph_objs as go
import igraph as ig


def create_table(database_name, sql_table, column_names):
    query = "CREATE TABLE IF NOT EXISTS %s (id INT PRIMARY KEY, %s VARCHAR(200) DEFAULT null, %s VARCHAR(200) ,%s VARCHAR(200), %s VARCHAR(200),%s INT,%s INT,%s INT) " % (
        sql_table, column_names["nodenames"], column_names["group_names"], column_names["edges_sources_names"], column_names["edges_targets_names"], column_names["groups_numerics"], column_names["edges_sources_numerics"], column_names["edges_targets_numerics"])
    sql.execute_query(database_name, query)

# empty table
def truncate_table(database_name, sql_table):
    sql.execute_query(database_name, "DELETE FROM %s" % sql_table)

# * This is nescecary to use a color code given by plotly for the groups
def create_numeric_node_group(database_name, sql_table, node_group, sql_groups_source):
    # empty target column in sql database
    sql.execute_query(
        database_name, "UPDATE %s SET %s = null" % (sql_table, node_group))
    # read the source column
    nodes_groups = sql.read_query(database_name, "SELECT %s FROM %s where %s is not null" % (
        sql_groups_source, sql_table, sql_groups_source))
    # creates dictionary with numerical values for every different category in the source column
    dictionary = {}
    k = 0
    for i in range(len(nodes_groups)):
        if ''.join(nodes_groups[i]) not in dictionary:
            dictionary[''.join(nodes_groups[i])] = 1 + k
            k += 1
    # insert dictionary values into source target column
    for k in range(len(nodes_groups)):
        value = dictionary[nodes_groups[k][0]]
        query = "UPDATE %s SET %s = '%s' WHERE id = %s" % (
            sql_table, node_group, value, k + 1)
        sql.execute_query(database_name, query)
    print(f'Created {len(dictionary)} categories')


# *create edges_sources and edges_targets columns for plotly to use by reading the source and target columns in the table

def create_edges(database_name, sql_table, sql_source_column, sql_target_column, sql_nodes_column, edges_sources, edges_targets):
    # empty edges_sources and edges_targets columns in sql database
    sql.execute_query(
        database_name, "UPDATE %s SET %s = null" % (sql_table, edges_sources))
    sql.execute_query(
        database_name, "UPDATE %s SET %s = null" % (sql_table, edges_targets))
    # read sources from table
    sources = sql.read_query(database_name, "SELECT %s from %s where %s is not null" % (
        sql_source_column, sql_table, sql_source_column))
    # read targets from table
    targets = sql.read_query(database_name, "SELECT %s from %s where %s is not null" % (
        sql_target_column, sql_table, sql_target_column))

    # read nodes from table
    query = "SELECT id, %s from %s where %s is not null" % (
        sql_nodes_column, sql_table, sql_nodes_column)
    nodes = sql.read_query(database_name, query)
    # create edges_sources column in sql table
    for k in range(len(sources)):
        for i in range(len(nodes)):
            if sources[k][0] == nodes[i][1]:
                query = "UPDATE %s SET %s = '%s' WHERE id = %s" % (
                    sql_table, edges_sources, nodes[i][0] - 1, k + 1)
                sql.execute_query(database_name, query)
    # create esges_targets columnn in sql table
    for k in range(len(targets)):
        for i in range(len(nodes)):
            if targets[k][0] == nodes[i][1]:
                query = "UPDATE %s SET %s = '%s' WHERE id = %s" % (
                    sql_table, edges_targets, nodes[i][0] - 1, k + 1)
                sql.execute_query(database_name, query)

    print(f'Created {len(sources)} edges sources and targets')

# * Use plotly to show a 3D network graph from the information in the sql database


def create_3d_network_graph(database_name, sql_table, node_names, node_groups, edges_sources, edges_targets, textcolor, linecolor, backgroundcolor):
    # read nodenames
    nodenames = sql.read_query(database_name, "SELECT %s from %s where %s is not null" % (
        node_names, sql_table, node_names))
    # read nodegroups
    nodegroups = sql.read_query(database_name, "SELECT %s from %s where %s is not null" % (
        node_groups, sql_table, node_groups))
    # read edges sources
    edgessources = sql.read_query(database_name, "SELECT %s from %s where %s is not null" % (
        edges_sources, sql_table, edges_sources))
    # read edges targets
    edgestargets = sql.read_query(database_name, "SELECT %s from %s where %s is not null" % (
        edges_targets, sql_table, edges_targets))

    # create edges
    Edges = [(edgessources[k][0], edgestargets[k][0])
             for k in range(len(edgessources))]
    # use Kamada-Kawai(kk) to create edges of more or less equal length and as few crossing edges as possible
    # layt is a list with the coordiantes of all nodes
    G = ig.Graph(Edges, directed=False)
    layt = G.layout('kk', dim=3)
    # creates arrays with coordinates of nodes
    N = len(nodenames)
    Xn = [layt[k][0] for k in range(N)]
    Yn = [layt[k][1] for k in range(N)]
    Zn = [layt[k][2] for k in range(N)]
    # create arrays with coordinates of edges
    Xe = []
    Ye = []
    Ze = []
    for e in Edges:
        # x-coordinates of edge ends
        Xe += [layt[e[0]][0], layt[e[1]][0], None]
        Ye += [layt[e[0]][1], layt[e[1]][1], None]
        Ze += [layt[e[0]][2], layt[e[1]][2], None]

    # * visuals *
    labels = []
    for i in nodenames:
        labels.append(i[0])  # set labels
    group = []
    for i in nodegroups:
        group.append(i[0])  # set groups for color
    # create visuals for nodes
    trace2 = go.Scatter3d(x=Xn,
                          y=Yn,
                          z=Zn,
                          mode='markers + text',
                          name='actors',
                          marker=dict(symbol='circle',
                                      size=4,
                                      color=group,
                                      colorscale='Plasma'
                                      ),
                          text=labels,
                          hoverinfo='text',
                          textfont=dict(family="sans serif",
                                        size=18,
                                        color=textcolor
                                        )
                          )
    # create visuals for edges
    trace1 = go.Scatter3d(x=Xe,
                          y=Ye,
                          z=Ze,
                          mode='lines',
                          line=dict(color=linecolor, width=1),
                          hoverinfo='none'
                          )
    # hides axis system
    axis = dict(showbackground=False,
                showline=False,
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                title=''
                )

    # visualisation of network
    layout = go.Layout(
        width=1920,
        height=1080,
        paper_bgcolor=backgroundcolor,
        showlegend=False,
        scene=dict(
            xaxis=dict(axis),
            yaxis=dict(axis),
            zaxis=dict(axis),
        ),
        margin=dict(l=0, r=0, b=0, t=0)
    )

    # * showing figure
    data = [trace1, trace2]
    fig = go.Figure(data=data, layout=layout)
    fig.show()
    print(f'Showing {N} nodes and {len(edgessources)} links')
