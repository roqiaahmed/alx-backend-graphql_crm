from datetime import datetime
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

from datetime import datetime
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport


def log_crm_heartbeat():
    now = datetime.now()
    formatted_date = now.strftime("%d/%m/%Y-%H:%M:%S")
    path_dir = "/tmp/crm_heartbeat_log.txt"

    try:
        transport = RequestsHTTPTransport(url="http://localhost:8000/graphql")
        client = Client(transport=transport, fetch_schema_from_transport=False)
        query = gql("query { hello }")
        result = client.execute(query)

        with open(path_dir, "a") as file:
            file.write(f"{formatted_date} CRM is alive\n")
            file.write(f"GraphQL says: {result["data"]["hello"]}\n")

    except Exception as e:
        with open(path_dir, "a") as file:
            file.write(f"{formatted_date} ERROR: {e}\n")


def update_low_stock():
    path_dir = "/tmp/low_stock_updates_log.txt"
    try:
        transport = RequestsHTTPTransport(url="http://localhost:8000/graphql")
        client = Client(transport=transport, fetch_schema_from_transport=False)
        query = gql(
            """
            mutation {
            updateLowStockProducts {
                message
                products {
                    name
                    stock
                    }
                }
            }
"""
        )
        result = client.execute(query)
        updated = result["updateLowStockProducts"]["products"]
        message = result["updateLowStockProducts"]["message"]

        with open(path_dir, "a") as file:
            file.write(f"\n[{datetime.datetime.now()}] {message}\n")
            for p in updated:
                file.write(f"- {p['name']} → stock: {p['stock']}\n")

    except Exception as e:
        with open(path_dir, "a") as file:
            file.write(f"\n[{datetime.datetime.now()}] ERROR: {e}\n")
