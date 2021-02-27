input("input your dataset.\n")
input("input your calibration dataset.\n")
input("input your reading frame parameter (s)\n")
print("beginning analysis..")
ls = [12.7, 12.95, 16.05, 16.2, 16.35, 16.5, 16.65, 16.85, 16.9, 17, 18.2, 18.5, 18.95, 19.15]

for x in ls:
    print("distress signal detected at t = %0.2fs." % x)
