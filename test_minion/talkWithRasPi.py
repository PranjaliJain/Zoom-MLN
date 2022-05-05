
import salt.client

def connect():
    print("Id: ", minion_id)
    local = salt.client.LocalClient()
    status = local.cmd(minion_id, 'test.ping')
    print("Ping status : ", status)

def runCommand():
    local = salt.client.LocalClient()
    output = local.cmd(minion_id, 'cmd.run', ["uname -a"])
    print("Command results: ", output)

def main():
    #init()
    connect()
    runCommand()

if __name__ == '__main__':
    minion_id = "raspi-e4:5f:01:56:d8:cd"
    local = None
    main()
