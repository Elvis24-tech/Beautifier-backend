from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .mpesa import stk_push


@api_view(["POST"])
@permission_classes([AllowAny])
def stk_push_view(request):
    phone = request.data.get("phone")
    amount = request.data.get("amount")

    if not phone or not amount:
        return Response({"error": "Phone and amount required"}, status=400)

    if phone.startswith("0"):
        phone = "254" + phone[1:]

    response = stk_push(
        phone=phone,
        amount=int(amount),
        account_reference="BeautyShop",
        transaction_desc="Payment"
    )

    return Response(response)


@api_view(["POST"])
@permission_classes([AllowAny])
def mpesa_callback(request):
    print("🔥 M-PESA CALLBACK:", request.data)
    return Response({"ResultCode": 0, "ResultDesc": "Accepted"})