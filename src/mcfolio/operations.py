import copy

import numpy as np


class Identity:
    def __init__(self):
        pass
    def apply(self, lastaccounttuple, variables):
        t, accounts = copy.deepcopy(lastaccounttuple)
        return (t, accounts)    

class SellAsset:
    def __init__(self, asset, toaccount):
        self.asset = asset
        self.toaccount = toaccount
    def apply(self, lastaccounttuple, variables):
        t, accounts = copy.deepcopy(lastaccounttuple)
        value = accounts[self.asset].sell(variables)
        accounts[self.toaccount].deposit(value)
        return (t, accounts)
    
class BuyAsset:
    def __init__(self, assetname, paymentaccounts, assetcost, newasset):
        self.assetname = assetname
        self.paymentaccounts = paymentaccounts
        self.assetcost = assetcost
        self.newasset = newasset
    def apply(self, lastaccounttuple, variables):
        t, accounts = copy.deepcopy(lastaccounttuple)
        assetcost = self.assetcost
        for paymentaccount in self.paymentaccounts:
            assetcost -= accounts[paymentaccount].withdraw(assetcost)
            if assetcost <= 0:
                break
        if assetcost != 0:
            raise ValueError(assetcost)
        accounts[self.assetname] = self.newasset(variables)
        return (t, accounts)

class Transfer:
    def __init__(self, fromaccount, toaccount, value):
        self.fromaccount = fromaccount
        self.toaccount = toaccount
        self.value = value
    def apply(self, lastaccounttuple, variables):
        t, accounts = copy.deepcopy(lastaccounttuple)
        value = accounts[self.fromaccount].withdraw(self.value)
        if value != self.value:
            raise ValueError(value)
        if self.toaccount is not None:
            accounts[self.toaccount].deposit(value)
        return (t, accounts)
    
class TransferFullBalance:
    def __init__(self, fromaccount, toaccount):
        self.fromaccount = fromaccount
        self.toaccount = toaccount
    def apply(self, lastaccounttuple, variables):
        t, accounts = copy.deepcopy(lastaccounttuple)
        value = accounts[self.fromaccount].withdrawfullbalance()
        if self.toaccount is not None:
            accounts[self.toaccount].deposit(value)
        return (t, accounts)
    
class MonthlyMortgagePayment:
    def __init__(self, mortgageaccount, paymentaccount):
        self.mortgageaccount = mortgageaccount
        self.paymentaccount = paymentaccount
    def apply(self, lastaccounttuple, variables):
        t, accounts = copy.deepcopy(lastaccounttuple)
        payment = accounts[self.mortgageaccount].makemonthlypayment()
        withdrawamount = accounts[self.paymentaccount].withdraw(np.abs(payment))
        if withdrawamount != payment:
            raise ValueError(payment, withdrawamount)
        return (t, accounts)

class PayoffMortgage:
    def __init__(self,mortgageaccount, paymentaccounts):
        self.mortgageaccount = mortgageaccount
        self.paymentaccounts = paymentaccounts
    def apply(self, lastaccounttuple, variables):
        t, accounts = copy.deepcopy(lastaccounttuple)
        payment = accounts[self.mortgageaccount].makefullpayment(variables)
        for paymentaccount in self.paymentaccounts:
            payment -= accounts[paymentaccount].withdraw(payment)
            if payment <= 0:
                break
        if payment != 0:
            raise ValueError(payment)
        return (t, accounts)

class CloseMortgage:
    def __init__(self, newaccountname):
        self.newaccountname = newaccountname

class Time:
    def __init__(self, dt):
        self.dt = dt
    def apply(self, lastaccounttuple, variables):
        t, accounts = lastaccounttuple
        return (t+self.dt, {k:v.time(t,self.dt,variables) for k,v in accounts.items()})
