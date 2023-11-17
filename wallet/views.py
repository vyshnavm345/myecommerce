from django.shortcuts import render, redirect
from .models import Wallet, Transaction
from decimal import Decimal
from products.decorators import custom_login_required_with_message

@custom_login_required_with_message
def wallet_view(request):
    try:
        wallet = Wallet.objects.get(user = request.user)
        transactions = wallet.user_transcation.all().order_by("-timestamp")
        print("rendered transactions : ", transactions)
    except:
        wallet = None
        transactions = None
    context = {
        "wallet" : wallet,
        "transactions" : transactions
    }
    return render(request, "wallet/walletview.html", context)


def new_wallet(request):
    wallet = Wallet.objects.create(user=request.user, balance=0)
    try:
        if request.session['for_refunding'] == True:
            pk = request.session['order_id']
            return redirect("cancel_order", pk)
        return redirect("wallet_view")
    except:
        pass
    return redirect("wallet_view")


def deposit_wallet(request):
    if request.method == "POST":
        print("depositing money")
        wallet = Wallet.objects.get(user = request.user)
        total = float(request.POST.get('total', 0))
        total = Decimal(total)
        wallet.balance+=total
        wallet.save()
        
        transaction = Transaction.objects.create(wallet=wallet, amount=total, transaction_type="deposit", transaction_balance= wallet.balance )
        transaction.save()
        print("current transaction : ",transaction)

    return redirect("wallet_view")











