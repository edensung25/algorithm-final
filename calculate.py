#!flask/bin/python
from flask import Flask, jsonify, request
from py2neo import Graph
import json
from collections import defaultdict
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
graph = Graph("bolt://localhost:7687", auth=("neo4j", "algorithm"))

class Network():
    def __init__(self):
        self.edges = defaultdict(list)
        self.weights = {}
    
    def add_edge(self, from_node, to_node, weight):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.weights[(from_node, to_node)] = weight
        self.weights[(to_node, from_node)] = weight

    def dijsktra(self, network, initial, end):
        shortest_paths = {initial: (None, 0)}
        current_node = initial
        visited = set()
        
        while current_node != end:
            visited.add(current_node)
            destinations = network.edges[current_node]
            weight_to_current_node = shortest_paths[current_node][1]

            for next_node in destinations:
                weight = network.weights[(current_node, next_node)] + weight_to_current_node
                if next_node not in shortest_paths:
                    shortest_paths[next_node] = (current_node, weight)
                else:
                    current_shortest_weight = shortest_paths[next_node][1]
                    if current_shortest_weight > weight:
                        shortest_paths[next_node] = (current_node, weight)
            
            next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
            if not next_destinations:
                return []
            current_node = min(next_destinations, key=lambda k: next_destinations[k][1])
        
        path = []
        while current_node is not None:
            path.append(current_node)
            next_node = shortest_paths[current_node][0]
            current_node = next_node
        path = path[::-1]
        return path

@app.route('/')
def request1():
    # create network
    rel = graph.run("MATCH (a:Airports)-[r]-(b:Airports) RETURN a.IATA_CODE, b.IATA_CODE, r.distance").to_table()
    network = Network()
    for edge in rel:
        network.add_edge(*edge)
    
    # calculate shortest path
    airports = network.dijsktra(network, str(request.args.get('start')), str(request.args.get('destination')))
    # wrap up the result into search condition and retrieve airport data from neo4j
    data, arr = {}, []
    for airport in airports:
        details = graph.run("MATCH (n:Airports) WHERE n.IATA_CODE = '" +airport+"' RETURN n.STATE, n.AIRPORT, n.CITY, n.LATITUDE, n.LONGITUDE, n.IATA_CODE").to_table()
    # convert table into json
        n = details[0]
        temp = {'state': n[0], 'airport': n[1], 'city': n[2], 'latitude': n[3], 'longitude': n[3], 'code':n[5]}
        arr.append(temp)
    data['data'] = arr

    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run(debug=True)

   