from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Order, OrderItem
from .serializers import OrderSerializer
from products.models import Product


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("-created_at")

    # CREATE ORDER (checkout)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # ADD ITEM TO ORDER
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

        # update total
        order.total_price += item.price
        order.save()

        return Response({"message": "Item added to order"})

    # REMOVE ITEM
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