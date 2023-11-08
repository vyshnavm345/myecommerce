from django.db import models
from products.models import Custom_User

class Wallet(models.Model):
    user = models.OneToOneField(Custom_User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return f"Wallet for {self.user.username}"
    
    

class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="user_transcation")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transaction_type = models.CharField(max_length=10, choices=[('deposit', 'Deposit'), ('withdrawal', 'Withdrawal')])
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction_balance =  models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} on {self.timestamp} balance : {self.transaction_balance}"
            
    def save(self, *args, **kwargs):
        if not self.transaction_balance:
            # Calculate the current balance based on the transaction type
            if self.transaction_type == 'deposit':
                self.transaction_balance = self.wallet.balance + self.amount
            elif self.transaction_type == 'withdrawal':
                self.transaction_balance = self.wallet.balance - self.amount

        # Call the original save method to save the object
        super(Transaction, self).save(*args, **kwargs)