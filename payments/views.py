from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

from .mpesa import stk_push

@api_view(["POST"])
@permission_classes([AllowAny])
def stk_push_view(request):
    phone = request.data.get("phone")
    amount = request.data.get("amount")

    if not phone or not amount:
        return Response({
            "error": "Phone and amount are required"
        }, status=400)

    response = stk_push(
        phone,
        amount,
        "BeautyShop",
        "Payment"
    )

    return Response(response)


@api_view(["POST"])
@permission_classes([AllowAny])
def mpesa_callback(request):
    print("M-PESA CALLBACK:")
    print(request.data)

    return Response({
        "message": "Callback received successfully"
    })