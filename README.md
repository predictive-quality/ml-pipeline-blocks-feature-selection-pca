# Principal component analysis (PCA).

Linear dimensionality reduction using Singular Value Decomposition of the data to project it to a lower dimensional space. The input data is centered but not scaled for each feature before applying the SVD.

It uses the LAPACK implementation of the full SVD or a randomized truncated SVD by the method of Halko et al. 2009, depending on the shape of the input data and the number of components to extract.

It can also use the scipy.sparse.linalg ARPACK implementation of the truncated SVD.

Notice that this class does not support sparse input. See TruncatedSVD for an alternative with sparse data.

Read more in the [User Guide](https://scikit-learn.org/stable/modules/decomposition.html#pca).


## Installation

Clone the repository and install all requirements using `pip install -r requirements.txt` .


## Usage

You can run the code in two ways.
1. Use command line flags as arguments `python main.py --input_path= --output_path=...`
2. Use a flagfile.txt which includes the arguments `python main.py --flagfile=example/flagfile.txt`

### Input Flags/Arguments

#### --input_path
Specify the a local or s3 object storage path where the needed files are stored.
For a s3 object storage path a valid s3 configuration yaml file is required.

#### --output_path
Specify the path where the output files will be stored.
For a s3 object storage path a valid s3 configuration yaml file is required.

#### --stage
 - fit: pca.fit_transform to fit a new pca class
 - transform: pca.transform to use fitted pca class
 - inverse: pca.inverse_pca to reconstruct the original data


#### --inverse_scaling
Wether to fit_transform/transform and generate principal components or 

#### --pca_object
Name of the saveobject of the pca class. \
When `stage==fit` the class will be saved with this name. Otherwise the class with this name will be loaded. \
Defaults to 'pca.pckl'

#### --total_variance
Sum of variances of the individual principal components. Must be between `0.0 < total_variance <= 1.0` \
Principal components with the highest variances will be kept. \
`total_variance == 1.0` saves all principal components in the dateframe.

#### --filename_x
Feature(_x) filenames for feature selection.

#### --filename_y
Target(_y) filenames if the target dataframe should be copied and stored to the output_path with the feature file.



## Example

First move to the repository directory. \
We run e.g. select features for a new train dataset with `python main.py --flagfile=fit_transform.txt` \
Afterwards we run feature selection for a test dataset with the fitted configuration from the train step `python main.py --flagfile=transform.txt` \
At the End we can run a inverse transformation for one or both of the above examples. `python main.py --flagfile=inverse_transform.txt`

## Data Set

The data set was recorded with the help of the Festo Polymer GmbH. The features (`x.csv`) are either parameters explicitly set on the injection molding machine or recorded sensor values. The target value (`y.csv`) is a crucial length measured on the parts. We measured with a high precision coordinate-measuring machine at the Laboratory for Machine Tools (WZL) at RWTH Aachen University.