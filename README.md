# 50.004 Introduction to Algorithms
Implementing the Algorithm to solve the 2-SAT Problem.

## How to Use
1. Upload test file to *test_files*
2. Go to main.py to change the filename under run("test1.cnf")
3. Run the function

## test_files
Upload all test files here, in .cnf format. The plain text should look something like this:
```
c This is test number 1
p cnf 3 2
2 -1 0 
3 2 0
```

## reader.CNFReader
Initialises a test file written in CNF format, assuming that the test file is uploaded in the test_files folder. Calling the class should be as follows:
```
input  = CNFReader('<NAME OF FILE>')
input.parse()           # Parsing action
input.visualise()       # Viewing the problem
parsed_obj = input.parsed
```

## graphing.Vertex
Creates a node object, with no edges

## graphing.Graph
Creates the graph, allowing the entire Directed Acrylic Graph to be created, by forming nodes and linking edges.
```
# Initialising the graph
graph = Graph(<NUMBER OF VARIABLES>)

# Creating the DAG
clauses = ["4 5", "1 3", "-3", "2 1"]
graph.create_dag(clauses)

# Visualising the graph
graph.visualise()
```

## graphing.Tarjan
Applies Tarjan's Algorithm on the graph, by having a recursive visit() function that will do Depth First Search (DFS) on the graph, to find Strongly Connected Components (SCC).
```
# Initialise and run Tarjan's Algorithm
tarjan = Tarjan(graph)
tarjan.run()

# Show graph after Tarjan's Algorithm applied
tarjan.visualise()          

# Getting all SCC groups
scc = tarjan.split_scc()
```

## check.Satisfiability
Checking the satisfiability of the graph, as well as the Boolean values given to the variable.
```
sat = Satisfiability(scc=scc, 
                     clauses=parsed['clauses'], 
                     no_variables=parsed['parameters']['variables'])
sat.run()
```
If it is unsatisfiable, it will print `FORMULA UNSATISFIABLE`. Otherwise it will print `FORMULA SATISFIABLE` followed by the Boolean values of the variables.
