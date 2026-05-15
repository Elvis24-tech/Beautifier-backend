from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiExample
from .models import Order, OrderItem
from .serializers import OrderSerializer
from products.models import Product
class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all().order_by("-created_at")
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]
    @extend_schema(
        summary="Create Order",
        description="Creates a new order with items and calculates total price",
        examples=[
            OpenApiExample(
                "Create Order Example",
                value={
                    "phone": "0712345678",
                    "total": 500,
                    "items": [
                        {"id": 1, "quantity": 2},
                        {"id": 3, "quantity": 1}
                    ]
                },
                request_only=True,
            )
        ],
    )
    def create(self, request, *args, **kwargs):
        data = request.data

        order = Order.objects.create(
            total_price=0,
            phone=data.get("phone", ""),
            user=request.user if request.user.is_authenticated else None
        )

        items = data.get("items", [])
        total = 0

        for item in items:
            try:
                product = Product.objects.get(id=item["id"])
                quantity = int(item.get("quantity", 1))

                item_total = product.price * quantity

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=item_total
                )

                total += item_total

            except Product.DoesNotExist:
                continue

        order.total_price = total
        order.save()

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED
        )
    @extend_schema(
        summary="Add Item to Order",
        request={
            "type": "object",
            "properties": {
                "product_id": {"type": "integer"},
                "quantity": {"type": "integer"}
            }
        }
    )
    @action(detail=True, methods=["post"])
    def add_item(self, request, pk=None):
        order = self.get_object()

        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        if not product_id:
            return Response({"error": "product_id is required"}, status=400)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

        item_total = product.price * quantity

        item = OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=item_total
        )

        order.total_price += item_total
        order.save()

        return Response(
            {
                "message": "Item added",
                "item_id": item.id,
                "order_total": order.total_price
            },
            status=200
        )
    @extend_schema(
        summary="Remove Item from Order",
        request={
            "type": "object",
            "properties": {
                "item_id": {"type": "integer"}
            }
        }
    )
    @action(detail=True, methods=["post"])
    def remove_item(self, request, pk=None):
        order = self.get_object()

        item_id = request.data.get("item_id")

        if not item_id:
            return Response({"error": "item_id is required"}, status=400)

        try:
            item = OrderItem.objects.get(id=item_id, order=order)
        except OrderItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=404)

        order.total_price = max(0, order.total_price - item.price)
        order.save()

        item.delete()

        return Response(
            {
                "message": "Item removed",
                "order_total": order.total_price
            },
            status=200
        )