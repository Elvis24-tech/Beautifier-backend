from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiExample
from .mpesa import stk_push
@extend_schema(
    summary="M-Pesa STK Push",
    description="Initiates STK push payment to user's phone",
    examples=[
        OpenApiExample(
            "STK Example",
            value={
                "phone": "0712345678",
                "amount": 100
            },
            request_only=True,
        )
    ]
)
@api_view(["POST"])
@permission_classes([AllowAny])
def stk_push_view(request):
    phone = request.data.get("phone")
    amount = request.data.get("amount")

    if not phone or not amount:
        return Response(
            {"error": "Phone and amount required"},
            status=status.HTTP_400_BAD_REQUEST
        )
    if phone.startswith("0"):
        phone = "254" + phone[1:]
    elif phone.startswith("+254"):
        phone = phone.replace("+", "")

    try:
        response = stk_push(
            phone=phone,
            amount=int(amount),
            account_reference="BeautyShop",
            transaction_desc="Payment"
        )

        return Response(response, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@extend_schema(
    summary="M-Pesa Callback",
    description="Receives payment confirmation from Safaricom"
)
@api_view(["POST"])
@permission_classes([AllowAny])
def mpesa_callback(request):
    print("M-PESA CALLBACK:", request.data)

    return Response(
        {
            "ResultCode": 0,
            "ResultDesc": "Accepted"
        },
        status=status.HTTP_200_OK
    )