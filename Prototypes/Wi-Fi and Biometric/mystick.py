from lib import time_ex
timEx = time_ex.TimerEx()

from speaker import Speaker
spkr = Speaker()
spkr.setVolume(100)

for n in [(2349, 250),(2959, 250),(3520, 250),(4698, 500)]:
	spkr.tone(n[0],n[1],100)
