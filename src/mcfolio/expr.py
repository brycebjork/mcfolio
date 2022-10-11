class Expr:
    def __init__(self, expression: str):
        self.expression = expression
    
    @staticmethod
    def eval(expression, variables):
        if isinstance(expression, Expr):
            return eval(expression.expression, variables)
        else:
            return expression