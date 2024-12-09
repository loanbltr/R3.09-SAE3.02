import os

def fileToMsg(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    else:
        return f"Le fichier '{file_path}' n'existe pas."

file_path = 'C:\\Users\\loanb\\Documents\\BUT_RT\\R3\\R3.09\\GitHub\\R3.09-SAE3.02\\SAE3.02\\Codes\\CodeTest\\python.py'

contenu_fichier = fileToMsg(file_path)

print(contenu_fichier)
exec(contenu_fichier)