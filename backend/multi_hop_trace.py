from neo4j import GraphDatabase

URI = "bolt://127.0.0.1:7687"
USER = "neo4j"
PASSWORD = "welcometocit"

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

account = input("Enter Account ID: ")

with driver.session() as session:

    result = session.run("""
    MATCH path = (a:Account {id:$account})-[:TRANSFERRED*1..3]->(b)
    RETURN path
    LIMIT 10
    """, account=account)

    print("\nTransaction Paths\n")

    for record in result:
        path = record["path"]

        accounts = []

        for node in path.nodes:
            accounts.append(node["id"])

        print(" -> ".join(accounts))

driver.close()