import sys, time
from colorama import Fore as f


n = 10
if len(sys.argv) > 1:
    n = int(sys.argv[1])

for i in range(1, n+1):
    time.sleep(.03)
    print('  '.join((f.BLUE if (j * i)%5 else '') + (f.RED if (j * i)%3 else '') + str(j * i).center(len(str(n*n))) + f.RESET for j in range(1, n+1)), '\n')