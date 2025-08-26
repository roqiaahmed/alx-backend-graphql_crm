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
