from datetime import datetime
import graphene

from graphene_django import DjangoObjectType
from graphql import GraphQLError
from .models import Customer, Product, Order
import re


def validate_phone_number(phone_number):
    pattern = re.compile(r"^(\+1|1)?\s*\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$")
    # return bool(pattern.match(phone_number))
    return True


def exists_email(email):
    return Customer.objects.filter(email=email).exists()


class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = "__all__"


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = "__all__"


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = "__all__"


class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String(required=False)


class CreateCustomer(graphene.Mutation):
    class Arguments:
        input = CustomerInput(required=True)

    customer = graphene.Field(CustomerType)
    message = graphene.String()

    @classmethod
    def mutate(self, info, name, input):
        if exists_email(input.email):
            raise GraphQLError("User with this email already exists.")
        if input.phone and not validate_phone_number(input.phone):
            raise GraphQLError(
                "Enter a valid phone number in format +1234567890 or 123-456-7890."
            )

        customer = Customer.objects.create(
            name=input.name, email=input.email, phone=input.phone
        )
        return CreateCustomer(
            customer=customer, message="Customer created successfully."
        )


class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        input = graphene.List(CustomerInput, required=True)

    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    @classmethod
    def mutate(cls, root, info, input):
        errors = []
        valid_customers = []
        for cust in input:
            if exists_email(cust.email):
                errors.append(f"Email already exists: {cust.email}")
                continue
            if cust.phone and not validate_phone_number(cust.phone):
                errors.append(f"Invalid phone: {cust.phone}")
                continue
            valid_customers.append(
                Customer(name=cust.name, email=cust.email, phone=cust.phone)
            )

        if valid_customers:
            Customer.objects.bulk_create(valid_customers)
        return BulkCreateCustomers(customers=valid_customers, errors=errors)


class ProductInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    price = graphene.Float(required=True)
    stock = graphene.Int(default_value=0)


class CreateProduct(graphene.Mutation):
    class Arguments:
        input = ProductInput(required=True)

    product = graphene.Field(ProductType)

    @classmethod
    def mutate(cls, root, info, input):
        if input.price <= 0:
            raise GraphQLError("Price must be positive.")
        if input.stock < 0:
            raise GraphQLError("Stock cannot be negative.")

        product = Product.objects.create(
            name=input.name, price=input.price, stock=input.stock
        )
        return CreateProduct(product=product)


class OrderInput(graphene.InputObjectType):
    customer_id = graphene.ID(required=True)
    product_ids = graphene.List(graphene.ID, required=True)
    order_date = graphene.DateTime(required=False)


class CreateOrder(graphene.Mutation):
    class Arguments:
        input = OrderInput(required=True)

    order = graphene.Field(OrderType)

    @classmethod
    def mutate(cls, root, info, input):
        try:
            customer = Customer.objects.get(pk=input.customer_id)
        except Customer.DoesNotExist:
            raise GraphQLError("Invalid customer ID.")

        if not input.product_ids:
            raise GraphQLError("At least one product must be selected.")

        products = []
        total_amount = 0

        for pid in input.product_ids:
            try:
                product = Product.objects.get(pk=pid)
                products.append(product)
                total_amount += product.price
            except Product.DoesNotExist:
                raise GraphQLError(f"Invalid product ID: {pid}")

        order_date = datetime.now()

        order = Order.objects.create(
            customer=customer, order_date=order_date, total_amount=total_amount
        )
        order.products.set(products)

        return CreateOrder(order=order)


class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()


class Query(graphene.ObjectType):

    all_products = graphene.List(ProductType)
    all_customers = graphene.List(CustomerType)
    all_orders = graphene.List(OrderType)

    def resolve_all_products(root, info):
        return Product.objects.all()

    def resolve_all_customers(root, info):
        return Customer.objects.all()

    def resolve_all_orders(root, info):
        return Order.objects.all()
