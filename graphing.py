from config import tprint


class Vertex:
    def __init__(self, node):
        self.node = node
        self.edges = None
        self.index = None
        self.low_link = None
        self.status = 0                 # 0 for unvisited, 1 for in stack, 2 for completed


class SCC:
    def __init__(self):
        self.nodes = []
        self.low_link = None


class Graph:
    def __init__(self, no_variables):
        self.graph = {str(variable): Vertex(str(variable))
                      for variable in range(-int(no_variables), int(no_variables)+1) if variable != 0}

    def add_edge(self, v1, v2):
        if self.graph[v1].edges:
            self.graph[v1].edges.append(v2)
        else:
            self.graph[v1].edges = [v2]

    def add_clause(self, clause):
        if len(clause.split(" ")) > 1:
            [var1, var2] = clause.split(" ")
            self.add_edge(str(-int(var1)), var2)
            self.add_edge(str(-int(var2)), var1)
        else:
            self.add_edge(str(-int(clause)), clause)

    def create_dag(self, clauses):
        for clause in clauses:
            self.add_clause(clause)
        for variable in self.graph.keys():
            if self.graph[variable].edges:
                self.graph[variable].edges = list([variable, None] for variable in set(self.graph[variable].edges))

    def visualise(self):
        print({variable: vertex.__dict__ for variable, vertex in self.graph.items()})


class Tarjan:
    def __init__(self, graph_obj):
        self.dag = graph_obj.graph
        self.index = 0
        self.stack = []
        self.SCC = SCC()

    def run(self):
        for variable, vertex in self.dag.items():
            if vertex.status == 0:
                self.visit(variable)

        for variable, vertex in self.dag.items():
            if not vertex.low_link:
                self.dag[variable].status = 2
                lowlink_node = min([self.stack.index(node) for node in self.stack])
                self.dag[variable].low_link = lowlink_node

    def pop_scc(self, node_idx):
        self.SCC.nodes = self.stack[node_idx:]
        self.stack = self.stack[:node_idx]
        self.SCC.low_link = min([self.dag[node].index for node in self.SCC.nodes])
        tprint("Lowlink of SCC is {}".format(self.SCC.low_link))
        while self.SCC.nodes:
            node = self.SCC.nodes[0]
            self.dag[node].status, self.dag[node].low_link = 2, self.SCC.low_link
            self.SCC.nodes.pop(0)

    def visit(self, node):
        tprint("We are at node {} now".format(node))
        self.dag[node].index, self.dag[node].status = self.index, 1
        self.index += 1
        self.stack.append(node)

        if self.dag[node].edges:
            for edge in self.dag[node].edges:
                if edge[1]:                                         # Edge visited before
                    pass
                else:
                    edge_no = self.dag[node].edges.index(edge)
                    self.dag[node].edges[edge_no][1] = 1
                    if self.dag[edge[0]].status == 2:               # Node completed
                        tprint("Went to {}, it was cleared?".format(self.dag[edge[0]].node))
                        pass
                    elif self.dag[edge[0]].status == 0:             # Completely unvisited
                        self.visit(edge[0])
                    else:                                           # Visited, in stack. Form SCC
                        start_index = self.stack.index(edge[0])
                        tprint("Current stack = {}, split to SCC stack = {}".format(str(self.stack),
                                                                                    str(self.stack[start_index:])))
                        self.pop_scc(start_index)
                        break

    def visualise(self):
        print({variable: vertex.__dict__ for variable, vertex in self.dag.items()})

    def split_scc(self):
        low_link = dict()
        for variable, vertex in self.dag.items():
            if vertex.low_link not in low_link:
                low_link[vertex.low_link] = [variable]
            else:
                low_link[vertex.low_link].append(variable)
        return low_link
