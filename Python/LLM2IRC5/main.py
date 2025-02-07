import socket
from lastStep import fixCommands #Es necesario validar al pose en casos de move 1
from llm2values import getArrayCommands, NL2Array

lengths = [4,4,4,12,12,12,12,1,4]
# X, Y, Z, qw, q1, q2, q3, action, value

def socketMsg(command):
  stringCommand = ''
  for value, length in zip(command, lengths):
    aux = ''
    if value < 0:
        value = -value
        length = length - 1
        aux = '-'
    if value == 0:
       value = 0
    value = aux + str(value).rjust(length, '0')
    stringCommand = stringCommand + value
  return stringCommand

def main ():
  mySocket = socket.socket()
  # 192.168.125.1 Real Robot
  mySocket.connect(("127.0.0.1", 8000))
  ans = mySocket.recv(1024)
  print(ans)

  while True:
    rawCommands = getArrayCommands()
    # test = 'draw, none, 35, move, none, [-30,-30,40]'
    # rawCommands = NL2Array(test)
    commands = fixCommands(rawCommands)
    print(commands)
    for command in commands:
        msg = socketMsg(command)
        mySocket.send(msg.encode())
        print(command)        
        print(msg)
        allGood = int(mySocket.recv(1024).strip())
        if allGood == 1: print('Command successful finished!!!!')
        elif allGood == 2: print("¡¡¡ERROR!!!, That action would break end effector")
        else: print("¡¡¡ERROR!!!, The arm can't reach that point")

if __name__ == '__main__':
    main()
