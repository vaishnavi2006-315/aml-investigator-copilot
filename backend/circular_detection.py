from neo4j import GraphDatabase

URI = "bolt://127.0.0.1:7687"
USER = "neo4j"
PASSWORD = "welcometocit"

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

with driver.session() as session:

    result = session.run("""
MATCH path=(a:Account)-[:TRANSFERRED*3..6]->(a)
WHERE ALL(n IN nodes(path) WHERE single(m IN nodes(path) WHERE m = n))
RETURN path
LIMIT 10
""")

    print("\nCircular Transaction Paths\n")

    found = False

    for record in result:
        found = True
        path = record["path"]
        accounts = [node["id"] for node in path.nodes]
        print(" -> ".join(accounts))

    if not found:
        print("No circular transaction paths found.")

driver.close()