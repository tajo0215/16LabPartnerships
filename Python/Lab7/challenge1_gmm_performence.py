# Import for searching a directory
import glob

# The usual suspects
import numpy as np
import ECE16Lib.DSP as filt
import matplotlib.pyplot as plt

# The GMM Import
from sklearn.mixture import GaussianMixture as GMM
from sklearn.metrics import mean_squared_error as MSE
from sklearn.metrics import mean_absolute_error as MAE

# Import for Gaussian PDF
from scipy.stats import norm
from scipy.stats import pearsonr

# Retrieve a list of the names of the subjects


def get_subjects(directory):
    filepaths = glob.glob(directory + "\\*")
    return [filepath.split("\\")[-1] for filepath in filepaths]

# Retrieve a data file, verifying its FS is reasonable


def get_data(directory, subject, trial, fs):
    search_key = "%s\\%s\\%s_%02d_*.csv" % (directory, subject, subject, trial)
    filepath = glob.glob(search_key)[0]
    t, ppg = np.loadtxt(filepath, delimiter=',', unpack=True)
    t = (t-t[0])/1e3
    hr = get_hr(filepath, len(ppg), fs)

    fs_est = estimate_fs(t)
    #if(fs_est < fs-1 or fs_est > fs):
        #print("Bad data! FS=%.2f. Consider discarding: %s" % (fs_est, filepath))

    return t, ppg, hr, fs_est

# Estimate the heart rate from the user-reported peak count


def get_hr(filepath, num_samples, fs):
    count = int(filepath.split("_")[-1].split(".")[0])
    seconds = num_samples / fs
    return count / seconds * 60  # 60s in a minute

# Estimate the sampling rate from the time vector


def estimate_fs(times):
    return 1 / np.mean(np.diff(times))

# Filter the signal (as in the prior lab)


def process(x):
    x = filt.detrend(x, 25)
    x = filt.moving_average(x, 5)
    x = filt.gradient(x)
    return filt.normalize(x)

# Plot each component of the GMM as a separate Gaussian


def plot_gaussian(weight, mu, var):
    weight = float(weight)
    mu = float(mu)
    var = float(var)

    x = np.linspace(0, 1)
    y = weight * norm.pdf(x, mu, np.sqrt(var))
    plt.plot(x, y)

# Estimate the heart rate given GMM output labels


def estimate_hr(labels, num_samples, fs):
    peaks = np.diff(labels, prepend=0) == 1
    count = sum(peaks)
    seconds = num_samples / fs
    hr = count / seconds * 60  # 60s in a minute
    return hr, peaks


def RMSE(y_pred, y_true):
    mse_vals = MSE(y_true, y_pred)
    rmse = np.sqrt(mse_vals)
    return rmse

def correlation_coefficient(y_pred, y_true):
    r = pearsonr(y_true, y_pred)
    return r[0]

def mae(y_pred, y_true):
    loss = MAE(y_true, y_pred)
    return loss


# Run the GMM with Leave-One-Subject-Out-Validation
if __name__ == "__main__":
    fs = 50
    directory = ".\\data"
    subjects = get_subjects(directory)

    # Leave-One-Subject-Out-Validation
    # 1) Exclude subject
    # 2) Load all other data, process, concatenate
    # 3) Train the GMM
    # 4) Compute the histogram and compare with GMM
    # 5) Test the GMM on excluded subject

    rmse_vals = []
    r_vals = []
    loss_vals = []
    
    data_true = []
    data_pred = []

    for exclude in subjects:
        print("Training - excluding subject: %s" % exclude)
        train_data = np.array([])
        for subject in subjects:
            for trial in range(1, 11):
                t, ppg, hr, fs_est = get_data(directory, subject, trial, fs)

                if subject != exclude:
                    train_data = np.append(train_data, process(ppg))

        # Train the GMM
        # convert from (N,1) to (N,) vector
        train_data = train_data.reshape(-1, 1)
        gmm = GMM(n_components=2).fit(train_data)

        # Compare the histogram with the GMM to make sure it is a good fit
        """
        plt.hist(train_data, 100, density=True)
        plot_gaussian(gmm.weights_[0], gmm.means_[0], gmm.covariances_[0])
        plot_gaussian(gmm.weights_[1], gmm.means_[1], gmm.covariances_[1])
        plt.show()
        """

        # Test the GMM on excluded subject
        print("Testing - all trials of subject: %s" % exclude)

        y_true = []
        y_pred = []
        for trial in range(1, 11):
        
            t, ppg, hr, fs_est = get_data(directory, exclude, trial, fs) # gives the data from the csv file
            
            y_true.append(hr)
            data_true.append(hr)

            test_data = process(ppg) # processes the signal to make it more readable 
  
            labels = gmm.predict(test_data.reshape(-1, 1)) # predicts the estimated hr

            hr_est, peaks = estimate_hr(labels, len(ppg), fs) # getting the predicted heart rate 

            y_pred.append(hr_est)
            data_pred.append(hr_est)
        
            print("File: %s_%s: HR: %3.2f, HR_EST: %3.2f" % (exclude, trial, hr, hr_est))

        rmse = RMSE(y_pred, y_true)
        rmse_vals.append(rmse)

        r = correlation_coefficient(y_pred, y_true)
        r_vals.append(r)

        loss = mae(y_pred, y_true)
        loss_vals.append(loss)

    total_rmse = RMSE(data_pred, data_true)
    total_r = correlation_coefficient(data_pred, data_true)
    total_loss = mae(data_pred, data_true)

    x = list(range(len(subjects)))


    plt.subplot(3, 1, 1)
    plt.scatter(x, rmse_vals)
    plt.xlabel("Subjects")
    plt.ylabel("RMSE Value")
    plt.title("RMSE vs Subjects")
    plt.xticks(np.arange(0, len(x), step = 1))

    plt.subplot(3, 1, 2)
    plt.scatter(x, r_vals)
    plt.xlabel("Subjects")
    plt.ylabel("R (Correlation Coefficient) Value")
    plt.title("Correlation Coefficient (R) vs Subjects")
    plt.xticks(np.arange(0, len(x), step = 1))

    plt.subplot(3, 1, 3)
    plt.scatter(x, loss_vals)
    plt.xlabel("Subjects")
    plt.ylabel("Mean Absolute Error Value")
    plt.title("Mean Absolute Error vs Subjects")
    plt.xticks(np.arange(0, len(x), step = 1))


    plt.show()

    print("\n" + '-'*40)
    print("-" * 11 + "Statistics Summary" + "-" * 11)
    print('-'*40 + "\n")

    print(f'Total Data Stats:\n\tRMSE: {total_rmse:.2f}\n\tr value: {total_r:.2f}\n\tMAE: {total_loss:.2f}\n')

    i = 0
    for exclude in subjects:
        print(f'Subject: {exclude}\n\tRMSE: {rmse_vals[i]:.2f}\n\tr value: {r_vals[i]:.2f}')
        i += 1
