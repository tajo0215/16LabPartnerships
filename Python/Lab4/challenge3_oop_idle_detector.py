from ECE16Lib.IdleDetector import IdleDetector

if __name__ == "__main__":

    try:
        # Instantiaing Idle Detector (num_samples, refresh_rate, N, Com port, baud rate)
        idleDetector1 = IdleDetector(250, .25, .02, "COM5", 115200) 
        idleDetector1.run(False) # true for graphing, false for no graphing
    except KeyboardInterrupt():
        print("Program Ended")
    finally:
        print("Closed Program!")
