import glob

def function():
    grains = {}
    grains["diskdevices"] = []
    for device in glob.iglob("/sys/block/[hsv]d[a-z]/device/type"):
        fh = open(device, "r")
        if fh.readline().rstrip() == "0":
            parts = device.split("/")
            grains["diskdevices"].append(parts[3])
        fh.close()
    return grains
