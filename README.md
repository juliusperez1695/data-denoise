# Data Denoise 
## About
This application was built to address the concern of measurement datasets containing outliers which affect the application and characterization of associated models.  As an example, imagine an experiment which involves sensing the current flowing through a device as a sweep of DC voltage is applied to its terminals.  If contact with either of the terminals is lost for a short duration of time and subsequently regained during the experiment, this would appear as a short segment of zero-values for current - however, the overall linear structure of the rest of the data remains to be analyzed.  To properly characterize this linear structure, say for the device's resistance, we would want to discount the data (remove the outliers) associated with the loss of contact before applying a linear fit to analyze for dV/dI.  This describes the purpose of the Data Denoise application, and the goal is to be able to apply such a process to a variety of datasets and their associated models.

## Installation and Intended Use
As it currently stands, the application is run through a command-line interface (CLI).  Users and developers may install it by creating a virtual environment (if they wish), cloning the repository to their local machine, navigating to the cloned repo where the 'src/' directory lives, and running the following command:
```
pip install -e .
```
This will install the python package in editable mode along with all the required dependencies, allowing the user to test the application immediately.  To start the app, run the following command:
```
datadenoise
```
In this repository, there is a directory labeled 'Data_Files' which contains datasets (.csv) for importing and testing the outlier-removal functionality.

## Contributions
If developers wish to contribute and improve the existing python codebase, please create a new branch and descriptively label it with the associated feature/bug/test/etc. that is being addressed.  For example,
```
git checkout -b feature-add-new-models-for-fitting
```
