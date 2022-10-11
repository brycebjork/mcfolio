import numpy as np
import numpy_financial as npf
from dataclasses import dataclass
from typing import Union
import copy
from .expr import Expr

from . import constants

@dataclass
class Mortgage:
    date0: float
    balance0: float
    annualrate: Union[float, Expr]
    Nmonths: int
    paymentsmade: int = 0
    def __call__(self, variables):
        return MortgageAccount(
            date0 = Expr.eval(self.date0, variables),
            balance0 = Expr.eval(self.balance0, variables),
            annualrate = Expr.eval(self.annualrate, variables),
            Nmonths = Expr.eval(self.Nmonths, variables),
            paymentsmade = Expr.eval(self.paymentsmade, variables),
            )

@dataclass
class MortgageAccount:
    date0: float
    balance0: float
    annualrate: Union[float, Expr]
    Nmonths: int
    paymentsmade: int

    def time(self, t0, dt, variables):
        return copy.deepcopy(self)
    def value(self, variables):
        return npf.fv(rate=self.annualrate/12, nper=self.paymentsmade, pmt=-self.getmonthlypayment(), pv=self.balance0)
    def getmonthlypayment(self):
        return -npf.pmt(self.annualrate/12, self.Nmonths, self.balance0, fv=0, when='end')
    def makemonthlypayment(self):
        self.paymentsmade += 1
        return self.getmonthlypayment()
    def makefullpayment(self, variables):
        paymentamount = self.value(variables)
        self.paymentsmade = self.Nmonths
        return -paymentamount

@dataclass
class Checking:
    balance: float
    annualrate: Union[float, Expr]
    negativebalanceallowed: bool = False

    def __call__(self, variables):
        return CheckingAccount(
            balance = Expr.eval(self.balance, variables),
            annualrate = Expr.eval(self.annualrate, variables),
            negativebalanceallowed = Expr.eval(self.negativebalanceallowed, variables),
            )

@dataclass
class CheckingAccount:
    balance: float
    annualrate: Union[float, Expr]
    negativebalanceallowed: bool = False

    def time(self, t0, dt, variables):
        return CheckingAccount(balance=self.balance*np.exp(dt*self.annualrate/constants.year), annualrate=self.annualrate, negativebalanceallowed=self.negativebalanceallowed)
    def value(self, variables):
        return self.balance
    def deposit(self, value):
        self.balance += value
    def withdraw(self, value):
        if value < 0:
            raise ValueError()
        positivebalance = self.balance
        if positivebalance < 0:
            positivebalance = 0
        if value > self.balance:
            if self.negativebalanceallowed:
                withdrawamount = value
            else:
                withdrawamount = positivebalance
        else:
            withdrawamount = value
        self.balance -= withdrawamount
        return withdrawamount
    def withdrawfullbalance(self):
        withdrawamount = self.balance
        if withdrawamount < 0:
            withdrawamount = 0
        self.balance -= withdrawamount
        return withdrawamount

@dataclass
class Stocks:
    balance: float
    annualrate: Union[float, Expr]
    negativebalanceallowed: bool = False

    def __call__(self, variables):
        return StockAccount(
            balance = Expr.eval(self.balance, variables),
            annualrate = Expr.eval(self.annualrate, variables),
            negativebalanceallowed = Expr.eval(self.negativebalanceallowed, variables),
            )

@dataclass
class StockAccount:
    balance: float
    annualrate: float
    negativebalanceallowed: bool = False

    def time(self, t0, dt, variables):
        return StockAccount(balance=self.balance*np.exp(dt*self.annualrate/constants.year), annualrate=self.annualrate)
    def value(self, variables):
        return self.balance
    def deposit(self, value):
        self.balance += value
    def withdraw(self, value):
        withdrawamount = value
        if value > self.balance and not self.negativebalanceallowed:
            withdrawamount = self.balance
        if withdrawamount < 0:
            withdrawamount = 0
        self.balance -= withdrawamount
        return withdrawamount
    def withdrawfullbalance(self):
        withdrawamount = self.balance
        if withdrawamount < 0:
            withdrawamount = 0
        self.balance -= withdrawamount
        return withdrawamount 

@dataclass
class Escrow:
    balance: float
    annualrate: Union[float, Expr]
    negativebalanceallowed: bool = False

    def __call__(self, variables):
        return StockAccount(
            balance = Expr.eval(self.balance, variables),
            annualrate = Expr.eval(self.annualrate, variables),
            negativebalanceallowed = Expr.eval(self.negativebalanceallowed, variables),
            )

@dataclass
class EscrowAccount:
    balance: float
    annualrate: float
    negativebalanceallowed: bool = False

    def time(self, t0, dt, variables):
        return Escrow(balance=self.balance*np.exp(dt*self.annualrate/constants.year), annualrate=self.annualrate)
    def value(self, variables):
        return self.balance
    def deposit(self, value):
        self.balance += value
    def withdraw(self, value):
        withdrawamount = value
        if value > self.balance and not self.negativebalanceallowed:
            withdrawamount = self.balance
        if withdrawamount < 0:
            withdrawamount = 0
        self.balance -= withdrawamount
        return withdrawamount
    def withdrawfullbalance(self):
        withdrawamount = self.balance
        if withdrawamount < 0:
            withdrawamount = 0
        self.balance -= withdrawamount
        return withdrawamount
