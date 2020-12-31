from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

import braintree
# Create your views here.


gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id="4p7xvtdbrjgd4fbh",
        public_key="dx858d7df2skjr8z",
        private_key="364af55aa869b47f732e87041ea84b20"
    )
)


# to check user is signed up or not
def validate_user_session(id, token):
    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(pk=id)
        if user.session_token == token:
            return True
        else:
            return False
    except UserModel.DoesNotExist:
        return False

# generating token


@csrf_exempt
def generate_token(request, id, token):
    if not validate_user_session(id, token):
        return JsonResponse({'error': 'invalid session, please login again!'})

    return JsonResponse({'clientToken': gateway.client_token.generate(), 'success': True})

# 8.3 process payment from backend


@csrf_exempt
def process_payment(request, id, token):
    if not validate_user_session(id, token):
        return JsonResponse({'error': 'invalid session, please login again!'})

    nonce_from_the_client = request.POST['paymentMethodNonce']
    amount_from_the_client = request.POST['amount']

    result = gateway.transaction.sale({
        "amount": amount_from_the_client,
        "payment_method_nonce": nonce_from_the_client,
        "options": {
            "submit_for_settlement": True
        }
    })

    if result.is_success:
        return JsonResponse
        (
            {
                'success': result.is_success,
                'transaction': {'id': result.transaction.id,
                                'amount': result.transaction.amount}
            }
        )
    else:
        return JsonResponse({"error": True, 'success': False})
