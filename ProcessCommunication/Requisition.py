class Requisition:
    """Class to be used to send a requisition from a client to a server"""
    valid_options = ['soma', 'sub', 'div', 'multi']

    def __init__(self, num_1, num_2, op):

        if op not in Requisition.valid_options:
            raise TypeError("'op' must be one of the following: " + ", ".join(Requisition.valid_options))

        self.num_1 = num_1
        self.num_2 = num_2
        self.op = op

    def get_op_symbol(self, op=None):
        """
        This method returns a symbol representation of a operation.
        If argument 'op' is not passed, this function returns self.op symbol
        """
        if not op:
            op = self.op

        symbol = None

        if op == "soma":
            symbol = "+"
        elif op == "multi":
            symbol = "*"

        elif op == "div":
            symbol = "/"

        elif op == "sub":
            symbol = "-"

        return symbol
