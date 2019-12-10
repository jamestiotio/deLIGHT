import machine
import time
class Speaker:
  def __init__(self, pin=26, volume=2):
    self.pwm_init = False
    self.pin = pin
    self._timer = None
    self._volume = volume
    self._beat_time = 500
    self._timer = machine.Timer(2)

  def checkInit(self):
    if self.pwm_init == False:
      self.pwm_init = True
      self.pwm = machine.PWM(machine.Pin(26), freq = 0)

  def _timeout_cb(self, timer):
    self.checkInit()
    self.pwm.duty(0)
    time.sleep_ms(1)
    self.pwm.freq(1)

  def tone(self, freq=1800, duration=200, volume=None, timer=True):
    duration = min(max(30, duration), 2000)
    freq = min(max(20, freq), 20000)
    self.checkInit()
    if volume == None:
      self.pwm.init(freq=freq, duty=self._volume)
    else:
      self.pwm.init(freq=freq, duty=volume)
    if timer:
      # if self._timer.isrunning():
      #   self._timer.period(duration)
      # else:
      self._timer.init(period=duration, mode=self._timer.ONE_SHOT, callback=self._timeout_cb)   
      time.sleep_ms(duration-15)
    else:
      time.sleep_ms(duration)
      self.pwm.duty(0)
      time.sleep_ms(1)
      self.pwm.freq(1)

  def sing(self, freq=1800, beat=1, end=True, volume=None):
    self.tone(freq, int(beat*self._beat_time), volume, end)

  def setBeat(self, value=120):
    self._beat_time = int(60000 / value)

  def setVolume(self, val):
    self._volume = val
