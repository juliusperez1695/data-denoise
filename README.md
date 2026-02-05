# Data Denoise 
## About
This application was built to address the concern of measurement datasets containing outliers which affect the application and characterization of associated models.  As an example,
imagine an experiment which involves sensing the current flowing through a device as a sweep of DC voltage is applied to its terminals.  If contact with either of the terminals is
lost for a short duration of time and subsequently regained during the experiment, this would appear as a short segment of zero-values for current - however, the overall linear
structure of the rest of the data remains to be analyzed.  To properly characterize this linear structure, say for the device's resistance, we would want to discount the data associated
with the loss of contact before applying a linear fit to analyze for dV/dI.  This describes the purpose of the Data Denoise application, and the goal is to be able to apply such a
process to a variety of datasets and their associated models.
