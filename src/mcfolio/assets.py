import numpy as np
from typing import Union
from dataclasses import dataclass
from .expr import Expr

from . import constants

@dataclass
class House:
    salevalue: Union[float, Expr]
    annualrate: Union[float, Expr]
    commission: Union[float, Expr] = 0.06
    sold: bool = False
    def __call__(self, variables):
        return HouseAsset(
            salevalue=Expr.eval(self.salevalue, variables),
            annualrate=Expr.eval(self.annualrate, variables),
            commission=Expr.eval(self.commission, variables)
            )

@dataclass
class Land:
    salevalue: Union[float, Expr]
    annualrate: Union[float, Expr]
    commission: Union[float, Expr] = 0.06
    sold: bool = False
    def __call__(self, variables):
        return LandAsset(
            salevalue=Expr.eval(self.salevalue, variables),
            annualrate=Expr.eval(self.annualrate, variables),
            commission=Expr.eval(self.commission, variables)
            )

@dataclass
class HouseAsset:
    salevalue: Union[float, Expr]
    annualrate: Union[float, Expr]
    commission: Union[float, Expr] = 0.06
    sold: bool = False

    def time(self, t0, dt, variables):
        return HouseAsset(salevalue=self.salevalue*np.exp(dt*self.annualrate/constants.year), annualrate=self.annualrate, sold=self.sold)
    def value(self, variables):
        if self.sold:
            return 0
        else:
            return self.salevalue * (1-self.commission)
    def sell(self, variables):
        r = self.value(variables)
        self.sold = True
        return r

@dataclass
class LandAsset:
    salevalue: Union[float, Expr]
    annualrate: Union[float, Expr]
    commission: Union[float, Expr] = 0.06
    sold: bool = False

    def time(self, t0, dt, variables):
        return LandAsset(salevalue=self.salevalue*np.exp(dt*self.annualrate/constants.year), annualrate=self.annualrate, sold=self.sold)
    def value(self, variables):
        if self.sold:
            return 0
        else:
            return self.salevalue * (1-self.commission)
    def sell(self, variables):
        r = self.value(variables)
        self.sold = True
        return r