from ECE16Lib.HRMonitor import HRMonitor
from scipy import stats 
import numpy as np
import matplotlib.pyplot as plt
import os

estimates = []
ground_truth = []

def eval_hr_monitor():

    for file in os.listdir("./data/a16651346"):

        ground_truth.append(int(file[13:15]) * 6)

        data = np.genfromtxt("./data/a16651346/" + file, delimiter=",")
        t = data[:,0]
        t = (t - t[0])/1e3
        ppg = data[:,1]

        hr_monitor = HRMonitor(500, 50)
        hr_monitor.add(t, ppg)
        hr, peaks, filtered = hr_monitor.process()

        estimates.append(hr)
    plotResults()
    
def plotResults():
    [R,p] = stats.pearsonr(ground_truth, estimates) # correlation coefficient

    plt.figure(1)
    plt.clf()

    # Correlation Plot
    plt.subplot(211)
    plt.plot(estimates, estimates)
    plt.scatter(ground_truth, estimates)

    plt.ylabel("Estimated HR (BPM)")
    plt.xlabel("Reference HR (BPM)")
    plt.title("Correlation Plot: Coefficient (R) = {:.2f}".format(R))

    # Bland-Altman Plot
    avg = [(i+j)/2 for i, j in zip(ground_truth, estimates)]# take the average between each element of the ground_truth and
          # estimates arrays and you should end up with another array
    dif = [i-j for i, j in zip(ground_truth, estimates)] # take the difference between ground_truth and estimates
    std = np.std(dif) # get the standard deviation of the difference (using np.std)
    bias = np.mean(dif) # get the mean value of the difference
    upper_std = bias + 1.96*std # the bias plus 1.96 times the std
    lower_std = bias - 1.96*std # the bias minus 1.96 times the std

    plt.subplot(212)
    plt.scatter(avg, dif)

    plt.plot(avg, len(avg)*[bias])
    plt.plot(avg, len(avg)*[upper_std])
    plt.plot(avg, len(avg)*[lower_std])

    plt.legend(["Mean Value: {:.2f}".format(bias),
      "Upper bound (+1.96*STD): {:.2f}".format(upper_std),
      "Lower bound (-1.96*STD): {:.2f}".format(lower_std)
    ])

    plt.ylabel("Difference between estimates and ground_truth (BPM)")
    plt.xlabel("Average of estimates and ground_truth (BPM)")
    plt.title("Bland-Altman Plot")
    plt.show()


if __name__ == "__main__":
    eval_hr_monitor()