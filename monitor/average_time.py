import subprocess
import time

#use moving average to get average ping time over certain
#amount of time

MAX_SIZE = int(raw_input('Size of moving average: '))
PING_PRINT_INTERVAL = int(raw_input('After how many pings should the average be printed: ' ))
SLEEP_TIME = int(raw_input('Time between pings: '))

moving_queue = []
count = 0

while True :
  output = subprocess.Popen(["ping -c 1 server"], shell=True, stdout=subprocess.PIPE).communicate()[0].split('\n')

  for line in output :
    if '64 bytes from' in line :
      for element in  line.split(' ') :
        if 'time=' in element :
          time_ = float(element.split('=')[1])
      
          if len(moving_queue) < MAX_SIZE :
            moving_queue.append(time_)
          else :
            moving_queue.pop(0)
            moving_queue.append(time_)
          print time_

  if count is PING_PRINT_INTERVAL - 1:
    temp = 0
    for i in moving_queue :
      temp = temp + i
    temp = temp / len(moving_queue)
    print 'AVERAGE: ' + str(temp)
    count = 0
  else :
    count = count + 1
  time.sleep(SLEEP_TIME)
