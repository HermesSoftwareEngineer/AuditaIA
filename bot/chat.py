from graph import app

# config = 

while True:
    inpt = input("User: ")
    if inpt.upper() == 'SAIR':
        break
    response = app.invoke({"messages": inpt})
    print("IA: ", response)