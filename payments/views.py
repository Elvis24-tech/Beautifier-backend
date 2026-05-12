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
        return Response(
            {"error": "Phone and amount are required"},
            status=400
        )

    try:
        # normalize phone (important for Kenya)
        if phone.startswith("0"):
            phone = "254" + phone[1:]

        response = stk_push(
            phone=phone,
            amount=int(amount),
            account_reference="BeautyShop",
            transaction_desc="BeautyShop Payment"
        )

        return Response(response)

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=500
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def mpesa_callback(request):
    data = request.data

    print("\n🔥 M-PESA CALLBACK RECEIVED")
    print(data)

    try:
        result = data.get("Body", {}).get("stkCallback", {})

        print("ResultCode:", result.get("ResultCode"))
        print("CheckoutRequestID:", result.get("CheckoutRequestID"))

    except Exception as e:
        print("Callback parse error:", str(e))

    return Response({"message": "Callback received"})