import copy
from tqdm.auto import trange

from . import constants
from .operations import Time


def run(portfolios, variables={}, trials=1):
    portfolionames = [i[0] for i in portfolios]
    results = [[] for _ in portfolios]
    for trial in trange(trials):
        variabledict = {k:v() if callable(v) else v for k,v in variables.items()}
        for i, portfolio in enumerate(portfolios):
            results[i] += yearlybalance(run_portfolio(portfolio=portfolio, variables=variabledict), variables=variabledict, trial=trial)
    return {k:v for k,v in zip(portfolionames, results)}

def run_portfolio(portfolio, variables):
    name, accounts, ops = copy.deepcopy(portfolio)
    sortedops = sorted(
        ops,
        key= lambda item: item[0]
    )
    r = [(0, {k:v(variables) for k,v in accounts.items()})]
    currtime = sortedops[0][0]
    for op in sortedops:
        dt = op[0] - currtime
        if dt < 0:
            raise ValueError()
        if dt > 0:
            r.append(Time(dt).apply(r[-1], variables=variables))
            currtime += dt
        r.append(op[1].apply(r[-1], variables=variables))
    return r

def yearlybalance(out, variables, trial):
    r = []
    for i in out:
        t = i[0]/constants.year
        values = {k:v.value(variables) for k,v in i[1].items()}
        r.append(dict({"trial": trial, "t":i[0]/constants.year},**values,**{"Total": sum(values.values())}))
    return r
