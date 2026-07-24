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
        MATCH (a)-[:TRANSFERRED]->()
        RETURN count(DISTINCT a) AS total
        """).single()["total"]

    return accounts, transactions, high_risk


def search_account(account_id):

    with driver.session() as session:

        result = session.run("""
        MATCH (a:Account {id:$id})

        OPTIONAL MATCH (a)-[o:TRANSFERRED]->()
        OPTIONAL MATCH ()-[i:TRANSFERRED]->(a)

        RETURN
            a.id AS account,
            count(DISTINCT o) AS outgoing,
            count(DISTINCT i) AS incoming,
            coalesce(sum(o.amount),0) AS sent,
            coalesce(sum(i.amount),0) AS received
        """, id=account_id)

        return result.single()