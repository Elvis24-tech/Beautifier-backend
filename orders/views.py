from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .models import Order, OrderItem
from .serializers import OrderSerializer
from products.models import Product


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all().order_by("-created_at")
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        data = request.data

        order = Order.objects.create(
            total_price=data.get("total", 0),
            phone=data.get("phone", ""),
            user=request.user if request.user.is_authenticated else None
        )

        items = data.get("items", [])

        for item in items:
            try:
                product = Product.objects.get(id=item["id"])
                quantity = item.get("quantity", 1)

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price * quantity
                )

            except Product.DoesNotExist:
                continue

        order.save()

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=["post"])
    def add_item(self, request, pk=None):
        order = self.get_object()

        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

        item = OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price * quantity
        )

        order.total_price += item.price
        order.save()

        return Response({"message": "Item added"})

    @action(detail=True, methods=["post"])
    def remove_item(self, request, pk=None):
        order = self.get_object()
        item_id = request.data.get("item_id")

        try:
            item = OrderItem.objects.get(id=item_id, order=order)
        except OrderItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=404)

        order.total_price -= item.price
        order.save()
        item.delete()

        return Response({"message": "Item removed"})