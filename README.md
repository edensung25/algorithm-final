## Shortest Path Among airports in U.S.

### Introduction
In this Web application, we try to find the shortest flight path between all of the airports in U.S. Using Neo4j as the database to maintain the relationships between everything airport.

### Data import
- For airport data:
Use the command below to import data.(Hint: remember to put the file(data/airports_45.csv) under Neo4j project directory(project/import/*))
    ```
    LOAD CSV WITH HEADERS FROM 'file:///airports_45.csv' AS line
    CREATE (:Airports { IATA_CODE:line.IATA_CODE,AIRPORT:line.AIRPORT,CITY:line.CITY,STATE:line.STATE,COUNRY:line.COUNRY,LATITUDE:line.LATITUDE,LONGITUDE:line.LONGITUDE})
    ```

- For relationship data:
After import all of the nodes, in order to import releation data, please execute the python script: import.py

- Result:
The result shown below![](https://i.imgur.com/VXjkO9T.png)

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
    
## References
### Installation for Neo4j
Here is the official guide for [Neo4j](https://neo4j.com/docs/operations-manual/current/installation/)

### Installation for Flask
Here is the official [document](http://flask.pocoo.org/) for Flask.
