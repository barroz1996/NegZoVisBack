# temporali

### User Guide

Notice that this project is in beta. Therefore, it is possible to encounter bugs and/or false results.

### Installation
In order to run the system, you will need to have a python environment of any kind containing the necessary packages. For you convenience, a file named 'environment.yml' is attached from which you can install a conda environment easily.

In order to install the environment from the file, run <br/>
`conda env create -f environment.yml` <br/>

Don't forget to activate the installed environment by running <br/>
`conda activate hugobot`


### Introduction
The main goal of this system is to integrate with KarmaLego.

The system takes as input a dataset file in a csv format. <br/>
The dataset structure is comprised of 4 columns: <br/>
EntityID, TemporalPropertyID, TimeStamp, TemporalPropertyValue<br/>

The system allows to perform **Pre-Processing**, **Discretization**, and creates results file which can be given to KarmaLego in order to perform **Time Intervals Mining**.

### Pre-Processing

The system allows for pre-processing of the given dataset.

Currently there are 2 pre-processing algorithms available: **Piecewise Aggregate Approximation(PAA)**, and **Outliers Remover**.

#### PAA

The purpose of PAA is to lower to resolution of the data, or in other words, to **decrease** the amount of samples in the dataset.

To that end, PAA takes a 'PAA Window Size', then go over each (EntityID, TemporalPropertyID) and calculates the mean of each time-window, according to the parameter given.

All the samples within the window are dropped, and a new sample containing the start-time of that window and the average of that window is inserted.

default PAA=1 (doesn't perform PAA)

#### Outliers Remover

The outliers remover is quite simple - it calculates the mean and standard deviation of each TemporalPropertyID, and then removes each sample which is not in the range of `[mean - 2 * std, mean + 2 * std]`.

In order to allow flexibility for the user, the system takes a parameter named 'Std Coefficient' which allows to replace the coefficient of the std (2 in the case above).

Note: This outlier remover assumes the properties of the dataset distribute normally.

default std_coefficient=-1 (not perform)

### Temporal Abstraction

Temporal abstraction allows to discretize the values in the dataset. It gets as input a time-point series and returns a symbolic time series

Temporal abstraction can be done by performing Gradient, by performing knowledge-based discretization, or by performing one of the discretization methods implemented in the system.

-Max Gap Example-
setting maxgap=1: timestamp=7 and timestamp=9 will create an interval since there is a gap of 1 between them

#### Gradient

Gradient is a knowledge-based temporal abstraction which discretizes the dataset by the values of the gradient of each sample.

The size of that time window is determined according to the 'Gradient Window Size' parameter.

In order to to normalize the data, the value in each dot will be the angle with respect to the positive side of X (or t - for time in our case), meaning it will be `tan(dot.slope)`.

There are two options to run the gradient:
1. Write the range values as a part of the command (the same bins will apply for all PropertyIDs)
2. Path to state files

-Gradient Command Format-

1.
temporal-abstraction
'Path to dataset file'
'Path to output dir'
per-dataset
'MaxGap value'
gradient
-sl
'-inf -90 -10 10 90 inf'
'Gradient window size value'

In this case the states will be:
StateID, TemporalPropertyID, BinID, BinLow, BinHigh
1,1,0,-inf,-90
2,1,1,-90,-10
3,1,2,-10,10
4,1,3,10,90
5,1,4,90,inf
6,2,0,-inf,-90
7,2,1,-90,-10
8,2,2,-10,10
9,2,3,10,90
10,2,4,90,inf
...

2.
temporal-abstraction
'Path to dataset file'
'Path to output dir'
per-dataset
'MaxGap value'
gradient
-sp
'Path to states file'
'Gradient window size value'


-Gradient States File Format-

StateID(mandatory), TemporalPropertyID(mandatory), Method(mandatory), BinID(mandatory), BinLow(mandatory), BinHigh(mandatory)
1,111,gradient,0,-90,-10
2,111,gradient,1,-10,10
3,111,gradient,2,10,90

#### Knowledge-Based

Knowledge based temporal abstraction uses a pre-determined set of states which is given by the user as input to the system. It then assigns each value to the matching state.


-KB Command Format-

temporal-abstraction
'Path to dataset file'
'Path to output dir'
per-dataset
'MaxGap value'
knowledge-based
'Path to states file'


-KB File Format-

StateID(mandatory), TemporalPropertyID(mandatory), Method(mandatory), BinID(mandatory), BinLow(mandatory), BinHigh(mandatory)
1,111,knowledge-based,0,-inf,-20
2,111,knowledge-based,1,-20,20
3,111,knowledge-based,2,20,inf

#### Discretization methods


Discretization algorithms currently supported by the system include:

##### Unsupervised

1. Equal Width - splits the data to equally-sized bins
2. Equal Frequency - splits the data so that in each bin there will be the same amount of samples
3. SAX - splits the data so that the probability to "fall" in each bin will be equal
4. KMeans - uses K-Means in order to cluster the data and sets the cutoffs at the center of each pair of centroids

##### Supervised


5. Persist - Creates a bag of cutoffs using Equal Frequency, and then chooses the cutoffs which gives the minimal amount of states transitions
6. TD4C - Creates a bag of cutoffs using Equal Frequency, and then chooses the cutoffs which gives best separation of classes between bins (maximal distance between classes distributions between the bins)<br>
6.1. TD4C cosine - uses cosine as the distance measure function <br>
6.2. TD4C entropy - uses entropy as the distance measure function <br>
6.3. TD4C entropy-ig - uses information gain as the distance measure function <br>
6.4. TD4C kullback-leibler - uses symmetric-kullback-leibler as the distance measure function <br>

*Entity class relations format in the dataset file (-1 in the TemporalPropertyID field):

EntityID,TemporalPropertyID,TimeStamp,TemporalPropertyValue
5,-1,0,0
6,-1,0,1
7,-1,0,0
8,-1,0,0


-Command Format-
gradient, knowledge-based
kmeans, equal-width, equal-frequency,
sax, persist, td4c-skl, td4c-entropy, td4c-entropy-ig, td4c-cosine, td4c-diffsum, td4c-diffmax


### K-Fold

The system allows to perform a k-fold experiment easily, in which the dataset is divided to `nb_folds` folds, and then for each train and test sets, states are generated for the train set, and are used to discretize the test set.

The dataset is divided so that the distribution of classes between test and train sets is equal.

Example:
```
temporal-abstraction
-kf
5
'Path to dataset file csv'
'Path to output dir'
per-dataset
5
discretization
equal-width
3
```

### Time Intervals Mining

After the system performs discretization and discover the bins for each property, it creates time-intervals from the data and from the states in order to integrate with KarmaLego which takes a time-intervals file as input.

The general idea is to connect each 2 samples of the same StateID (or symbol) only if the distance between them is lower than a parameter named 'Max Gap'. So notice that running the system with 2 configurations which differ only in the max gap parameter will give the same states, but possibly different time-intervals.

### Usage

In order to use the system you have 2 ways: <br>

(1) Open 'Edit Configurations' (small arrow next to the CLI and on the left of the 'Run' button)
Then, click on 'Parameters' and a dialog box will appear where you will enter your commands.
After filling in the commands (example below), click 'OK' and then click 'Run'

```
temporal-abstraction
'Path to dataset file csv'
'Path to output dir'
per-dataset
'MaxGap value'
discretization
'Method name'
'Number of bins value'
```

(2) Running in terminal commands:
type: `python cli.py`<br>

and then provide the relevant parameters.

You can use the help menu in order to get more info about the parameters for each command:
```
python cli.py --help
python cli.py temporal-abstraction --help
python cli.py results-union --help
...
```

The system contains two main commands: temporal-abstraction, and results-union.

The temporal abstraction command takes as parameters an input path, which is the local path to a dataset file, and an output path, which is a path to a folder into which the results will be written.

It is possible to give as a parameter a **name**, which will be concatenated to the start of each result file, for easier file-managment.

For examples on how to use the system, see the file 'exp.py', as well as the dataset given as an example 'FAGender' in the Datasets folder.

### Abstraction Per Property

It is possible to perform abstraction per property. In order to do so, you have to create 2 files.

1. A Pre-processing params file.
2. A Temporal abstraction params file.


-Per Property Command Format-

temporal-abstraction
'Path to dataset file csv'
'Path to output dir'
per-property
-s (when using Gradient or KnowledgeBased)
'Path to states file' (when using Gradient or KnowledgeBased)
'Path to Preprocessing file'
'Path to Temporal Abstraction file'


-Preprocessing File Format- (mandatory)

TemporalPropertyID(mandatory), PAAWindowSize(optional) ,StdCoefficient(optional), MaxGap(mandatory)
1,,2,5
1,7,2,5

-Temporal Abstraction File Format- (mandatory)

TemporalPropertyID(mandatory), Method(mandatory), NbBins(mandatory), GradientWindowSize(optional)
17,td4c-entropy,4,

-Gradient and/or KB File Format- (optional)

StateID(mandatory), TemporalPropertyID(mandatory), Method(mandatory), BinID(mandatory), BinLow(mandatory), BinHigh(mandatory)
1,111,gradient,0,-90,-10
2,111,gradient,1,-10,10
3,111,gradient,2,10,90
4,222,gradient,0,-90,-10
5,222,gradient,1,-10,10
6,222,gradient,2,10,90

1,111,knowledge-based,0,-inf,0
2,111,knowledge-based,1,0,inf


### Abstraction Per Dataset
Applies the same method to all temporal property id's


-Per Dataset Command Format-

temporal-abstraction
'Path to dataset file csv'
'Path to output dir'
per-dataset
'MaxGap value'
discretization
'Method name'
'Number of bins value'


##### Pre-processing params
In the preprocessing params file you have to specify for each property the parameters that you want, so that each property will show up **once** in the file.

The structure of the file is:

TemporalPropertyID, PAAWindowSize, StdCoefficient, MaxGap
1,,5
14,,5

Notice that the max gap parameter is relevant to the time intervals mining, and not to the pre-processing step.

For each pre-processing step that you do not wish to perform, leave an empty field.

An example is shown in the FAGender dataset folder in the file named 'preprocessing.csv'.

##### Temporal abstraction params

The temporal abstraction params contains all the temporal abstraction you wish to perform in the dataset.

In this file, you can have duplicates, which means that for a single property id, you can perform several methods of temporal abstraction.

The structure of the file is:

TemporalPropertyID, Method, NbBins, GradientWindowSize(optional)
1,equal-width,2,
14,td4c-cosine,3,

The method can be any discretization method, or knowledge-based, or gradient.

In case you did not choose the gradient method, leave the GradientWindowSize field for this row empty.

An example is shown in the FAGender dataset folder in the file named 'temporal_abstraction.csv'.


### Commands Summary

**temporal-abstraction**


optional:
```
-n <name>
-npd (flag to not create prop-data.csv file)
-hdf (flag to change csv file format to hf5 - should be faster)
-kf <k-value> (K-Fold)
-ncr (flag to allow non-continous range in states definition)
```

mandatory:
```
<input-path>
<output-path>
choose one: per-property / per-dataset
```


---------------------------
**per-property**

optional (mandatory when using gradient or knowledge-based):
```
-s <states-file-path>
```
mandatory:
```
<preprocessing-params-file-path>
<temporal-abstraction-params-file-path>
```
----------------------------
**per-dataset**

optional:
```
-paa <paa-window-size> (PAA pre-processing)
-std <std_coefficient_value> (Outliers Remover pre-processing)
```
mandatory:
```
<max-gap>
choose one: gradient / knowledge-based / discretization
```
----------------------------
**gradient** 

mandatory:
```
choose one: -sp <states-file-path> / -sl <states-string-list>
<window-size>
```
----------------------------
**knowledge-based**

mandatory:
```
<states-file-path>
```
----------------------------
**discretization**

mandatory:
```
choose one: kmeans / equal-width / equal-frequency / sax / persist / td4c-skl / td4c-entropy / td4c-entropy-ig / td4c-cosine / td4c-diffsum / td4c-diffmax 
<nb-bins>
```

### Results

The results contain several files:

Prop-data - a file which contains the dataset without any class records (-1 in the TemporalPropertyID field).

Entity class relations - a file which contains a mapping between each entity to its corresponding class.

States - a file which contains the states for each property, and the boundaries of them. It also contains scores in case TD4C or Persist have been run.

Symbolic time series - A file which contains the original dataset as is, with the values replaced by the states ids.

KL - A file which contains the symbolic time intervals in the KarmaLego input format:
EntityID;
StartTime,EndTime,SymbolID,PropertyID;

### FAQ

TBA

### Contact
You can contact via mail if you have any questions, or improvement suggestions:
 
[zvikf@post.bgu.ac.il](zvikf@post.bgu.ac.il)

October 2020 relevant contacts:

Irad: [irad@post.bgu.ac.il](irad@post.bgu.ac.il)

Maor: [maos@post.bgu.ac.il](maos@post.bgu.ac.il)

Good luck :)


### Acknowledgements

© The system was built by Kfir Zvi and Guy Danieli.