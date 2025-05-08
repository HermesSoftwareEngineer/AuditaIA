from graph import app

config = {"configurable": {"thread_id": "abc123"}} 

while True:
    user_input = input("User: ")
    if user_input.lower() in ["exit", "quit", "q", "sair"]:
        break
    response = app.invoke({"messages": user_input}, config)
    print("IA: ", response["messages"][-1].content)