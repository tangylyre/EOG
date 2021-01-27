import calibrationv1raspi
import collectRaws


def main():
    # call calibration, retrieve the minima, maxima and center values.
    hz = 100
    t = 20
    # switch these hz and timing values as appropriate.
    critical = calibrationv1raspi.calibrate(hz, t)
    print("Your minima is %0.2f v," % critical[0])
    print("Your center is %0.2f v," % critical[1])
    print("Your max is %0.2f v," % critical[2])


if __name__ == "__main__":
    main()
