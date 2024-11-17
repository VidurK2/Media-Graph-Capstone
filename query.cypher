// Query to calculate the number of nodes
MATCH (n:Entity)
RETURN count(n) AS NumberOfNodes;

// Query to calculate the number of edges
MATCH ()-[r:CO_OCCURS_WITH]->()
RETURN count(r) AS NumberOfEdges;

// Combined query to calculate graph density
MATCH (n:Entity)
WITH count(n) AS NumberOfNodes
MATCH ()-[r:CO_OCCURS_WITH]->()
WITH NumberOfNodes, count(r) AS NumberOfEdges
RETURN (2 * NumberOfEdges) / (NumberOfNodes * (NumberOfNodes - 1)) AS Density;
