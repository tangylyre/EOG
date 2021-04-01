def calibrationRead(filename):
    try:
        f = open(filename, 'r')
        lines = f.readlines()
        print(lines[0])
        lines.pop(0)
        print(lines[0])
    except FileNotFoundError:
        print("no file found under this filename.")
        return False

calibrationRead('testdatamore')