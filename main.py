from py2neo import Graph
graph = Graph("bolt://localhost:7687", auth=("neo4j", "algorithm"))
tx = graph.begin()
print(graph.run("MATCH (a:Person) RETURN a.name, a.born LIMIT 3").to_table())
print(graph.evaluate("MATCH (a:Person) RETURN count(a)"))