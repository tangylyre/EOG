f = open('tyler.cali', 'r')
for line in f:
    try:
        thresh = int(line)
        break
    except ValueError:
        pass

print(thresh)
