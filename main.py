from reader import CNFReader
from graphing import Graph, Tarjan
from check import Satisfiability


def run(filename):
    test_file = CNFReader(filename=filename)
    test_file.parse()
    test_file.visualise(parsed=test_file.parsed)  # Showing the problem in plaintext
    parsed = test_file.parsed

    graph = Graph(no_variables=parsed['parameters']['variables'])
    graph.create_dag(clauses=parsed['clauses'])

    print("Inital DAG:")            # Showing the initial DAG
    graph.visualise()

    tarjan = Tarjan(graph)
    tarjan.run()

    print("Final DAG:")             # Showing the final DAG
    tarjan.visualise()              # DAG with low-link values

    scc = tarjan.split_scc()

    sat = Satisfiability(scc, parsed['clauses'], parsed['parameters']['variables'])
    sat.run()


if __name__ == "__main__":
    run('test1.cnf')
