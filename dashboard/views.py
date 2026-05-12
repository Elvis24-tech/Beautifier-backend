from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.db.models import Sum
from django.db.models.functions import TruncDate

from products.models import Product
from orders.models import Order
from django.contrib.auth import get_user_model

User = get_user_model()


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard(request):
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_users = User.objects.count()

    pending_orders = Order.objects.filter(status="pending").count()
    completed_orders = Order.objects.filter(status="completed").count()
    revenue = 0
    completed_qs = Order.objects.filter(status="completed")

    for order in completed_qs:
        if getattr(order, "total_price", None):
            revenue += float(order.total_price)
    sales_data = (
        Order.objects.filter(status="completed")
        .annotate(date=TruncDate("created_at"))
        .values("date")
        .annotate(sales=Sum("total_price"))
        .order_by("date")
    )

    sales_chart = [
        {
            "date": item["date"],
            "sales": float(item["sales"])
        }
        for item in sales_data
    ]

    recent_orders = Order.objects.all().order_by("-id")[:5]

    recent_orders_data = [
        {
            "id": order.id,
            "status": order.status,
            "created_at": getattr(order, "created_at", None),
            "total_price": getattr(order, "total_price", None),
        }
        for order in recent_orders
    ]
    recent_products = Product.objects.all().order_by("-id")[:5]

    recent_products_data = [
        {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "stock": product.stock,
        }
        for product in recent_products
    ]
    return Response({
        "stats": {
            "products": total_products,
            "orders": total_orders,
            "users": total_users,
            "pending_orders": pending_orders,
            "completed_orders": completed_orders,
            "revenue": revenue,
        },

        "sales_chart": sales_chart,  

        "recent": {
            "orders": recent_orders_data,
            "products": recent_products_data,
        }
    })