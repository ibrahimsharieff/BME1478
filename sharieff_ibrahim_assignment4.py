# # Assignment 4 - Classes and analyzing data from multiple files 
# 
# ## Completing and Submitting the Assignment
# - Follow the instructions to fill in the code in this jupyter notebook template to complete the assignment. 
# - Places where you need to change or add something are denoted with **# TODO**
# 
# - Rename your completed version of this notebook so that your last and first name are filled in the file name
#     - e.g "Garton_Michael_assignment4.ipynb"
# - Export as a Python script .py file with the same filename:
#     - e.g. "Garton_Michael_assignment4.py
# - Upload both .ipynb and .py files to Quercus Assignment 4.
# 
# ## Setup (1 mark)
# 1. Download the .zip of data files from Quercus or here (http://swcarpentry.github.io/python-novice-inflammation/data/python-novice-inflammation-data.zip) and extract the /data/ folder and all of it's contents **into to the same folder as you downloaded this notebook**. **(0.5 marks)**
# 
# This is required and will make sure all relative paths are the same across student submissions when marking. 
# It should have this structure
# ```
# main_directory
# │   last_first_assignment4.ipynb
# │   last_first_assignment4.py # a copy of the .ipynb exported as a script
# │
# │   # you can have other things in this folder, the key thing is data/ is in the same directory as your .ipynb and .py
# │
# └───data/
# │   │   inflammation-01.csv
# │   │   inflammation-01.csv
# │   │   ...
# │   │   inflammation-12.csv
# │   │   small-01.csv
# │   │   small-02.csv
# │   │   small-03.csv
# │
# ```

# ## 1. Reading in our files and analyzing the data (2.5 marks)
# 
# We want to read in data from an arthritis study that followed 60 patients in a longitudinal study. This happened 12 times over the course of the study, resulting in 12 different data files. 
# 
# a. Make a list of **only** the .csv file paths that start with `inflammation` using `glob.glob()` and store in a variable named `fnames`. **(0.5 marks)**

# import libraries we will use 
import glob
import numpy as np

# TODO: fix this line to solve (a) 
fnames = glob.glob("./data/inflammation*.csv")

# # right now it includes all .csv files including small-xx.csv which we don't want
# fnames.sort() # this just sorts them alphabetically
# print(fnames) # confirm only inflammation files listed

# 
# b. Read in the first file in that list using `np.loadtxt()`, providing a filename and specifiying the `delimiter=','` and store in the variable `dt`. **(0.5 marks)**

# TODO: (b)
dt = np.loadtxt(fnames[0], delimiter=',')

# c. Define a function `patient_summary()` that summarizes the data using either "mean", "max" or "min" across patients **(0.5 marks)**
#   - `patient_summary(data, operation)` should take a numpy array of data from our files, as well as a string ("mean", "max" or "min") describing what operation to use summarize the data over the course of the 40 days across **each patient**.
#   - note: the shape of the output should be the same size as the number of patients (i.e. 60)

def patient_summary(data, operation):
    # TODO: specify the axis, 0 or 1
    ax = 1
    
    # TODO: fill in the rest of the if(and or elif/else) statements
    if operation == 'mean':
        summary_values = data.mean(axis=ax)
    elif operation == 'max':
        summary_values = data.max(axis=ax)
    else:
        summary_values = data.min(axis=ax)
    
    
    
    
    return summary_values


# test it out on the data file we read in and make sure the size is what we expect
dt_min = patient_summary(dt, 'min')
print(len(dt_min))

# Sometimes, data entry results in some errors. We can programmatically screen for certain errors. 
# 
# For example, if a patient has a mean inflammation of 0, this may indicate a healthy individual was misgrouped into this dataset, or some other issue requiring further attention. 
# 
# d. Define a function, `detect_problems()` that can check for issues that may have come from data input errors **(1 mark)**
#    - `detect_problems(data)` should take a numpy array of the data from one of our experiment files
#    - we created a helper function `check_zeros(x)` that returns True or False if there are values of zero in an array
#    - combine the results of `patient_summary()` with our helper function `check_zeros()` to create your new `detect_problems()` function
#    - return True or False depending whether a problem was found. 

# Run this cell so you can use this premade helper function to do the check 
# for values in an array that equal 0, DO NOT MODIFY THIS CODE
def check_zeros(x):
    '''
    Given an array, x, check whether any values in x equal 0.
    Return True if any values found, else returns False.
    '''
    # np.where() checks every value in x against the condition (x == 0) 
    # and returns a tuple of indices where it was True (i.e. x was 0)
    flag = np.where(x == 0)[0] 
    
    # We can check if there are any objects in flag (i.e. not empty)
    # If not empty, it found at least one zero, so flag is True. And vice-versa.
    flag = len(flag) > 0
    
    return flag

# It is not necessary to understand all the code inside the helper function, but when using code others have written, you should have a good idea of:
# 1. what goes IN the function (x, an array of numbers) 
# 2. what comes OUT of the function (True or False) 
# 3. what the output means (True if 0 found in array, False if no 0 found).

# example usage of check_zeros
values_0 = np.array([12,0,8,9,1])
values_1 = np.array([1,1,1,1,1])

print(check_zeros(values_0))
print(check_zeros(values_1))

# Write your function here

# TODO: Define your function `detect_problems` here 
# using patient_summary() to get the means and check_zeros() to check for zeros in the means

def detect_problems(data):
    # Get the mean inflammation across the 40 days for each patient
    mean_values = patient_summary(data, 'mean')
    
    # Use the helper function to check if there are any zeros in the mean values
    problem_found = check_zeros(mean_values)
    
    return problem_found


# ## 2. Creating an experiment class (4.5 marks)

# Let's store our experiments in a class. Each instance will be ONE experiment consisting of measurements from 60 patients over 40 days in the arthritis and inflammation study:
# - Each instance object comes from one of the 12 sessions i.e. one `Experiment()` = one data file/data collection period.
# - We can also bundle all the functions we've made above that operate on these data files into one class.
# 
# Modify the cell below to accomplish the following:
# 
# a. Create two **class attributes** named **study** to store the string "arthritis", and another named **experimenter** to store the string "Dr. Aria" **(1 mark)**  
# b. Define a new method `add_data()` that reads in a .csv and stores the result in the pre-existing .data attribute that was made during `__init__()`. Don't forget the delimiter. **(1 mark)**  
# c. Define a new method `patient_summary(self, operation)`. It is the same as the one we have already written, BUT it does not take `data` as an argument anymore (but still takes `operation`). The method reads from an instance's state to access what is in `.data`. It should still return summary values per patient for the given operation. **(1 mark)**

# TODO: modify this basic class as per the instructions above
class Experiment:
    # Class attributes
    study = "arthritis"
    experimenter = "Dr. Aria"
    
    def __init__(self, session_no):
        self.session_no = session_no  # Store session number
        self.data = None  # Data will be added using add_data()
    
    # Method to read in data from a .csv file
    def add_data(self, file_path):
        # Use np.loadtxt to read in the data, assuming the delimiter is a comma
        self.data = np.loadtxt(file_path, delimiter=',')
    
    # Method to perform the patient summary
    def patient_summary(self, operation):
        ax = 1  # Axis 1 summarizes across 40 days for each patient
        
        if operation == 'mean':
            summary_values = self.data.mean(axis=ax)
        elif operation == 'max':
            summary_values = self.data.max(axis=ax)
        else:
            summary_values = self.data.min(axis=ax)
        
        return summary_values


# **Putting it all together.** 
# 
# d. Loop over `fnames` created earlier with all the `inflammation-xx.csv` files and create one instance of the Experiment() class per file. These do not need to be stored beyond inside the loop (e.g. we don't need to save all the Experiments in a list). Only print the filenames where the data was flagged in that experiment. **(1.5 marks)** 
# 
# We have written the code for you, but you need to move them around to make the code functional (including adding indents where necessary).
# 
# Note: We can assume that the filenames are ordered such that they reflect the order of data collection (e.g. inflammation-01.csv is session # 1).
# 

# TODO: move these lines around and indent as necessary to make it work again, it *should* find three files.
session_counter = 1 # initialize counter

for f in fnames: # iterate over data files
    exp = Experiment(session_counter) # create an instance of our experiment and give it a session_no
    
    exp.add_data(f) # read in our data to our experiment
    
    values = exp.patient_summary("mean") # get our patient means
    
    if check_zeros(values): # check whether any 0s in our means
        print(f) # print filename

    session_counter += 1 # increment our counter to the next session number

# ## Finishing Up
# 1. Rename this file if you haven't already replacing the words in the filename with your actual last and first name
# 2. Export as a .py and submit BOTH .ipynb and .py files
# 3. Make sure you haven't changed any variable names we specifically asked you to define as such. 

# 

