# INFSCI 2591: Algorithm Design: Spring 2019
## Shortest Path Among Airports in U.S.(Final Report)

### Group members
Cai-Cian Song - cas386
Linlu Liu - lil131
Sahar Omidi - sao66
Xuechun Dong - xud8
Yifei Lin - yil199

### Introduction
Our team's report will concentrate on an Web Application that people can find the shortest flight path between all of the airports in U.S. on it. 

Our team initially finds datasets from Kaggle which contains the information of airports and calculates distances between them. After preparing the data, we use Neo4j as the database to maintain the relationships(distances) between every airport. Afterwards, we choose to implement Yen’s algorithm to find the k-shortest paths and validate our result with the Neo4j build-in function. Finally, we build our web application to show our results to users.

### Description of Data
The data set of our report is from 2015 Flight Delays and Cancellations provided by The U.S. Department of Transportation's (DOT) Bureau of Transportation Statistics(https://www.kaggle.com/levaniz/machine-learning-analysis-of-flights-data/data). 

We only extract the airports information and airline route information from it.
- For airport data
Here is the definitions of each feature in airports_45.csv:


    | Property | Description |
    | -------- | -------- |
    | IATA_CODE| Location Identifier|
    | AIRPORT  | Airport's Name     |
    | CITY     | City's Name        |
    | COUNTRY  | Country Name of the airport |
    | LATITUDE | Latitude of the airport     |
    | LONGITUDE| Longitude of the airport    |

- For flight data
We use Euclidean Distance to calculate the distances between each airport with airports' latitude and longitude.

  Here is the difinitions of each feature in flights_83.csv:
  

    | Property | Description |
    | ------------------- | -------------------- |
    | ORGIN_AIRPORT       | Starting Airport     |
    | DESTINATION_AIRPORT | Destination Airport     |
    | DISTANCE            | Distance between airports    |
    | FLIGHT_NUMBER       | Fight identifier     |


### Data import into Neo4j
- For airport data:
Use the command below to import data.(Hint: remember to put the file(data/airports_45.csv) under Neo4j project directory(project/import/*))
    ```
    LOAD CSV WITH HEADERS FROM 'file:///airports_45.csv' AS line
    CREATE (:Airports { IATA_CODE:line.IATA_CODE,AIRPORT:line.AIRPORT,
    CITY:line.CITY,STATE:line.STATE,COUNRY:line.COUNRY,
    LATITUDE:line.LATITUDE,LONGITUDE:line.LONGITUDE})
    ```

- For relationship data:
We use the distance between the starting airport and destination airport as the relationship of two nodes.
After import all of the nodes, in order to import relation data, please execute the python script: import.py

- Result:
The result shown below:

![](https://i.imgur.com/VXjkO9T.png)

### How to run the project
- In order to make this project work, execute those two steps:
    1. Start Neo4j graph database
    2. Run the Flask script
    ```
    python3 calculate.py
    ```
- Then, try this link with browser
    ```
    http://127.0.0.1:5000/?start=OGG&destination=DEN
    ```

### Algorithm
We choose to implement Yen's algorithm assisted by Dijkstra's algorithm. 
Instead of find the shortest path, Yen's algorithm aims to find the k-shortest paths.

It uses two lists, i.e. list A (permanent shortest paths from source to destination - chronologically ordered) and list B (tentative/candidate shortest paths). At first it find the 1st shortest path using Dijkstra. Then Yen exploits the idea that the k-th shortest paths may share edges and sub-paths (path from source to any intermediary nodes within the route) from (k-1)-th shortest path. Then it take (k-1)th shortest path and make each node in the route unreachable in turn. Once the node is unreachable, find the shortest path from the preceding node to the destination(using Dijkstra). Then it has a new route which is created by appending the common sub-path (from source to the preceding node of the unreachable node) and adds the new shortest path from preceding node to destination. This route is then added to the list B, provided that it has not appeared in list A or list B before. After repeating this for all nodes in the route, it find the shortest route in list B and move that to list A. Then repeat this process for number of Ks.

This algorithm has a computational complexity of $O(kn^{3}$)

### Validation
To guarantee the correctness of our shortest path result, we would like to have a comparison to validate our result. Since we store all nodes and relationships in Neo4j, we can compare our result with the Neo4j build-in function, [The Yen’s K-shortest paths algorithm](https://neo4j.com/docs/graph-algorithms/current/algorithms/yen-s-k-shortest-path/).

Using two airports as start and end airport. In our application, the result queried from these two airports is
```
# ["OGG", "OAK", "HNL", "LAX", "DAL", "DEN"]
```
On the other hand, the command below shows the command to query the shortest path between OGG to DEN and return 1 result
```
# Query
Match (start:Airports{IATA_CODE:'OGG'}), (end:Airports{IATA_CODE:'DEN'}) 
CALL algo.kShortestPaths.stream(start, end, 1, 'distance' ,{}) 
YIELD index, nodeIds
RETURN [node in algo.getNodesById(nodeIds) | node.IATA_CODE] AS places

# Result
# ["OGG", "OAK", "HNL", "LAX", "DAL", "DEN"]
```
## User Interface
Our website is built for users who want to find the shortest path from one starting airport to their destination airport to make a better flight plan.
### Search Interface
In the search interface, users can type in their departure and arrival airports. We also provide the autocomplete function to give users hints of the code of airports. When they click "SEARCH" botton, the results will appear.

![](https://i.imgur.com/ckIbHzx.jpg)

### Results and Map Interface
This interface will display the shortest path from departure to arrival in the first place and show another two short paths  in order. And the map will directly show the shortest path on the map. 
![](https://i.imgur.com/8SteG3N.jpg)![](https://i.imgur.com/LnI1OWT.png)


Also, when user click another path, for example, the second one, it will be displayed on the map as well.




## References
#### Installation for Neo4j
The official guide for Neo4j(https://neo4j.com/docs/operations-manual/current/installation/). 

#### Installation for Flask
The official document(http://flask.pocoo.org/) for Flask.

#### Neo4j shortest path document
https://neo4j.com/docs/graph-algorithms/current/algorithms/yen-s-k-shortest-path/

#### The concept of Yen's algorithm 
http://www.linchenguang.com/2018/01/30/Yen-s-algorithm/
