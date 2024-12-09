file = "test.txt"
file2 = "test1.txt"

def main():
    try:
        with open(file2, 'r') as f:
            for l in f:
                l = l.rstrip("\n\r")
                print(l)
    except FileNotFoundError:
        print("Le fichier n'a pas été trouvé.")
    except IOError as e:
        print("Le disque dur n'est pas joignable.")
    except FileExistsError:
        print("Le fichier est déjà existant..")
    except PermissionError:
        print("Tu n'as pas la permission pour ouvrir le fichier.")
    finally:
        print("END")

main()