import Pyro4
import Pyro4.naming
import threading


class Calculator(object):
    @Pyro4.expose
    def sum(self, num1, num2):
        return float(num1)+float(num2)

    @Pyro4.expose
    def sub(self, num1, num2):
        return float(num1)-float(num2)

    @Pyro4.expose
    def mul(self, num1, num2):
        return float(num1)*float(num2)

    @Pyro4.expose
    def div(self, num1, num2):
        return float(num1)/float(num2)

if __name__ == '__main__':
    # Starting name server:
    threading.Thread(target=Pyro4.naming.startNSloop, args=()).start()

    with Pyro4.Daemon() as daemon:
        calculator = Calculator()
        # Registering object calculator inside the daemon
        calculator_uri = daemon.register(calculator)

        # Registering calculator to name server
        with Pyro4.locateNS() as ns:
            ns.register("calculator", calculator_uri)
        # So we can have multiple requests
        daemon.requestLoop()
