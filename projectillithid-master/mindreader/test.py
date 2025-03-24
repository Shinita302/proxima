import mindwave, time

headset = mindwave.Headset('COM7')
time.sleep(2)

while True:
    time.sleep(.1)
    print ("Raw value: %s, Attention: %s, Meditation: %s" % (headset.raw_value, headset.attention, headset.meditation))
    print ("Waves: {}".format(headset.waves))