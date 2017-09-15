import Pyro4

if __name__ == '__main__':
    # Finding server
    with Pyro4.locateNS() as ns:
        # Finding the exact location of the remote object
        uri = ns.lookup("calculator")
        # Creating a proxy to access the object
        calculator = Pyro4.Proxy(uri)

    choice = input("Choose the operation you would like to execute:"
                   "\n1 - Sum\n2 - Subtraction\n3 - Multiplication\n4 - Division\n")

    choice = int(choice)

    if choice not in range(1, 5):
        raise Exception("Invalid choice. Please choose a value between 1 and 4")

    numbers = input("\nWrite num1 and num2 separated by space, for example: 3 5\n")

    numbers = numbers.split(" ")

    if len(numbers) != 2:
        raise Exception("You should choose exactly 2 numbers!\n")

    num1, num2 = numbers
    op = " "
    result = 0

    # +
    if choice == 1:
        result = calculator.sum(num1, num2)
        op = " + "
    # -
    elif choice == 2:
        result = calculator.sub(num1, num2)
        op = " - "

    # *
    elif choice == 3:
        result = calculator.mul(num1, num2)
        op = " * "

    # /
    elif choice == 4:
        result = calculator.div(num1, num2)
        op = " / "

    print(str(num1) + op + str(num2) + " = " + str(result))
