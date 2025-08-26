#!/bin/bash
deleted_count=$(
python manage.py shell <<EOF

from crm.models import Customer, Order
from datetime import datetime,date
from django.db.models import Q
current_datetime = datetime.now()
current_year = current_datetime.year
start_year = date(current_year, 1, 1)
end_year = date(current_year, 12, 31)

unactive_customers= Customer.objects.exclude(order__order_date__range=(start_year, end_year))
num = unactive_customers.count()

print(num)

# unactive_customers.delete()

EOF
)
echo "$(date): $deleted_count" unactive customers have deleted  >> /tmp/customer_cleanup_log.txt