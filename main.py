# Ref: add relationship between exsited nodes https://segmentfault.com/a/1190000014488430

from py2neo import Graph
import csv

graph = Graph("bolt://localhost:7687", auth=("neo4j", "algorithm"))
# tx = graph.begin()
print(graph.run("MATCH (a:Airports) WHERE a.STATE = 'TX' RETURN a").to_table())
print(graph.evaluate("MATCH (a:Airports) WHERE a.STATE = 'TX' RETURN count(a)"))

with open('data/flights_100.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
        line_count += 1
        print(row['ORIGIN_AIRPORT'], row['DESTINATION_AIRPORT'], row['DISTANCE'])
        print(graph.run("match (a:Airports), (b:Airports) where a.IATA_CODE = '"+row['ORIGIN_AIRPORT']+"' and b.IATA_CODE = '"+row['DESTINATION_AIRPORT']+"' create (a)-[r:airline{distance: "+row['DISTANCE']+"}]->(b)"))
    print(line_count) 