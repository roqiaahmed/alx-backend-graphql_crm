from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import datetime
from celery import shared_task
from datetime import datetime
import requests


@shared_task
def generate_crm_report():
    log_path = "/tmp/crm_report_log.txt"
    try:
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql", use_json=True
        )
        client = Client(transport=transport, fetch_schema_from_transport=False)

        query = gql(
            """
        query {
          allCustomers {
            id
          }
          allOrders {
            id
            totalamount
          }
        }
        """
        )

        result = client.execute(query)

        customers = result["allCustomers"]
        orders = result["allOrders"]

        total_customers = len(customers)
        total_orders = len(orders)
        total_revenue = sum(float(order["totalamount"]) for order in orders)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = (
            f"{timestamp} - Report: {total_customers} customers, "
            f"{total_orders} orders, {total_revenue} revenue\n"
        )

        with open(log_path, "a") as file:
            file.write(log_entry)

    except Exception as e:
        with open(log_path, "a") as file:
            file.write(f"[{datetime.datetime.now()}] ERROR: {e}\n")
