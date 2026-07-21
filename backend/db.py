from neo4j import GraphDatabase

URI = "bolt://127.0.0.1:7687"
USER = "neo4j"
PASSWORD = "welcometocit"

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

def get_stats():

    with driver.session() as session:

        accounts = session.run("""
        MATCH (a:Account)
        RETURN count(a) AS total
        """).single()["total"]

        transactions = session.run("""
        MATCH ()-[t:TRANSFERRED]->()
        RETURN count(t) AS total
        """).single()["total"]

        high_risk = session.run("""
        MATCH (a)-[t:TRANSFERRED]->()
        RETURN count(a) AS total
        ORDER BY total DESC
        LIMIT 20
        """).single()["total"]

    return accounts, transactions, high_risk