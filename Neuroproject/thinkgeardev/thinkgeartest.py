import thinkgear

def main():
    #logging.basicConfig(level=logging.DEBUG)

    for pkt in thinkgear.ThinkGearProtocol('COM5').get_packets():
        for d in pkt:
            if isinstance(d, thinkgear.ThinkGearPoorSignalData) and d.value > 10:
                print("Signal quality is poor.")

            if isinstance(d, thinkgear.ThinkGearEEGPowerData):
                print("Delta value: {}".format(d.value.delta))

if __name__ == '__main__':
    main()
