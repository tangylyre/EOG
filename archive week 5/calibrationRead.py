def calibrationRead(filename):
    try:
        f = open(filename, 'r')
        lines = f.readlines()
        header = lines[0]
        threshScore = header.split('\t')[1]
        neutral = []
        weighted = []
        lines.pop(0)
        lines.pop(0)
        for i in range(len(lines)):
            line = lines[i].split('\t')
            neutral.append(float(line[4].replace('\n', '')))
            weighted.append(float(line[6].replace('\n', '')))
        return threshScore, neutral, weighted
    except FileNotFoundError:
        print("no file found under this filename.")
        return False


threshScore, neutral, weighted = calibrationRead('calibration_profile_500Hz_10seconds.tsv')
print(threshScore)
print(len(neutral))
print(len(weighted))
