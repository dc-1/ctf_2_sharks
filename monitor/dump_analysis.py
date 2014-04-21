import sys
import os
from multiprocessing import Process, Manager

class state_ :
  Syncing, Synced, Fin, Fin_Ack, No_Syn, Reset = range(6)

def map_(s) :
  if s == state_.Syncing :
    return 'Syncing'
  elif s == state_.Synced :
    return 'Synced' 
  elif s == state_.Fin :
    return 'Fin' 
  elif s == state_.Fin_Ack :
    return 'Fin_Ack' 
  elif s == state_.No_Syn :
    return 'No_Syn'
  elif s == state_.Reset :
    return 'Reset'
  else :
    return 'Error'
    

class connection :
  def __init__(self, total_bytes, data_bytes, instance_, port_) :
    self.packets = 1
    self.total_bytes = total_bytes
    self.data_bytes = 0
    self.state = state_.Syncing
    self.instance = instance_
    self.port = port_

#constants
NUM_CLIENTS = 3

clients = []

for i in range(0, NUM_CLIENTS) :
  clients.append({})

try:
  num_newlines = 0
  buff = ''
  while True:
    buff += sys.stdin.read(1)
    if buff.endswith('\n') and num_newlines is 1 :
      #do processing here
      print buff
      lines = buff.split('\n')

      name = lines[1].lstrip().split(' ')[0]
      if 'client' in name :
        bucket = int(name[6])
        port = int(name.split('.')[1])

        temp_1 = lines[0].split(' ')
        temp_2 = lines[1].split(' ')

        total_bytes = int(temp_1[len(temp_1) - 1].split(')')[0])
        data_bytes = int(temp_2[len(temp_2)-1])

        if clients[bucket - 1].get(port, False) == False :
          clients[bucket - 1][port] = []
          clients[bucket - 1][port].append(connection(total_bytes, data_bytes, 1, port))
          if '[S]' not in lines[1] :
            clients[bucket - 1][port][0].state = state_.No_Syn

        else :
          l = clients[bucket - 1].get(port)
          c = l[len(l) - 1]

          if c.state != state_.Fin_Ack :
            if 'ack' in lines[1] and c.state == state_.Syncing :
              c.total_bytes = c.total_bytes + total_bytes
              c.data_bytes = c.data_bytes + data_bytes
              c.state = state_.Synced
            elif '[F.]' in lines[1] and c.state == state_.Synced :
              c.total_bytes = c.total_bytes + total_bytes
              c.data_bytes = c.data_bytes + data_bytes
              c.state = state_.Fin
            elif 'ack' in lines[1] and c.state == state_.Fin :
              c.total_bytes = c.total_bytes + total_bytes
              c.data_bytes = c.data_bytes + data_bytes
              c.state = state_.Fin_Ack
            elif '[P.]' in lines[1] and c.state == state_.Synced :
              c.total_bytes = c.total_bytes + total_bytes
              c.data_bytes = c.data_bytes + data_bytes
            elif '[U]' or '[U.]' in lines[1] and c.state == state_.Synced :
              c.total_bytes = c.total_bytes + total_bytes
              c.data_bytes = c.data_bytes + data_bytes
            elif '[R]' in lines[1] :
              c.total_bytes = c.total_bytes + total_bytes
              c.data_bytes = c.data_bytes + data_bytes
              c.state = state_.Reset
            elif c.state == state_.No_Syn :
              c.total_bytes = c.total_bytes + total_bytes
              c.data_bytes = c.data_bytes + data_bytes
  
          elif '[S]' in lines[1] :
            instance = c.instance + 1
            clients[bucket - 1][port].append(connection(total_bytes, data_bytes, instance, port))

      buff = ''
      num_newlines = 0
    elif buff.endswith('\n') and num_newlines is 0 :
      num_newlines = 1
except KeyboardInterrupt:
  sys.stdout.flush()
  pass

i = 1
for dic in clients :
  for key,l in dic.items() :
    for connection_ in l :
      print "Client: " + str(i) + " Port: " + str(key) + " State: " + map_(connection_.state) + " Total Bytes: " + str(connection_.total_bytes) + " Data Bytes: " + str(connection_.data_bytes) 
  i = i + 1
