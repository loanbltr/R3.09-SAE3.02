#Permet de diviser un nombre par un autre
from logging import raiseExceptions
from webbrowser import Error


def divEntier(x: int, y: int) -> int:
    if x < y:
        return 0
    else:
        x = x - y
        return divEntier(x, y) + 1

def main():
    try:
        x = int(input("Entre un nombre: "))
        y = int(input("Entre un nombre: "))
        if x == 0 or y == 0:
            raise ZeroDivisionError("une valeur ne peut pas être 0.")
        if x < 0 or y < 0:
            raise Error("une valeur ne peut pas être inférieur à 0.")
    except Error as e:
        print(f'{e}')
    except ValueError as e:
        print(f'ERROR: {e}')
    except RecursionError as e:
        print(f'ERROR: {e}')
    except ZeroDivisionError as e:
        print(f'ERROR: {e}')
    else:
        print(divEntier(x, y))
    finally:
        print("END")

main()