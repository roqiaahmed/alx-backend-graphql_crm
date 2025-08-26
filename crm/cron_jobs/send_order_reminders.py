#!/usr/bin/env python3

import requests
from datetime import timedelta, date
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

today = date.today()
week_ago = today - timedelta(days=7)

transport = RequestsHTTPTransport(url="http://localhost:8000/graphql")
client = Client(transport=transport)

query = gql(
    f"""
    query {{
        allOrders(orderDate_Gte: "{week_ago}") {{
            edges {{
                node {{
                    id
                    customer {{ email }}
                }}
            }}
        }}
    }}
    """
)

try:
    result = client.execute(query)
    orders = result["allOrders"]["edges"]
    path_dir = "/tmp/order_reminders_log.txt"
    with open(path_dir, "a") as file:
        for edge in orders:
            order = edge["node"]
            file.write(
                f"{today} — Order {order['id']} — {order['customer']['email']}\n"
            )

    print("Order reminders processed!")
except Exception as e:
    print(f"Error sending GraphQL query: {e}")
