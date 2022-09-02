import sys

import tensorflow as tf # not set up for gpu yet (I don't think)
import numpy as np
import pandas as pd

import sklearn_tools as sktools

from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import plot_model

from sklearn.neural_network import MLPClassifier
from sklearn.metrics import roc_curve
from sklearn.metrics import auc
from sklearn.ensemble import RandomForestClassifier

from matplotlib import pyplot

import selection_criteria as selcri

# Need this to to save sklearn's models
import joblib

#tag = 'pmu_1005'

# **********************************************
# Output: dataset without specified 
#           rows/columns, additional "Class" 
#           column
# **********************************************
def format(df, columnsToDrop, rowsToDrop, className=None):
  # The errors='ignore' means that if the column is not there, no error is thrown
  df = df.drop(columns=columnsToDrop, errors='ignore') # remove specified columns
  #print(rowsToDrop)
  #df = df.drop(rowsToDrop) # remove specified rows

  if className != None:
    # add column with class name
    labels = [className] * len(df) #list of labels is the length of the df
    df['Class'] = labels # creates new class column

  return df # returns data frame with new class and reformatted


# **********************************************
# Input: list of datsets to be merged
# Output: one merged dataframe
# **********************************************
def mergeDataframes(dfs):
  mergedDfs = pd.DataFrame()

  for df in dfs:
    mergedDfs = pd.concat([mergedDfs, df])
    
  return mergedDfs
################################################################################

infilenames = sys.argv[1:]

df0,df1 = sktools.read_in_files_and_return_dataframe(infilenames)

dRcut = 0.1 

mask = selcri.selection_dRcut(df0, dRcut=0.1)
df0 = df0[mask]
mask = selcri.selection_dRcut(df1, dRcut=0.1)
df1 = df1[mask]


print(df0.columns)
print()
print(df1.columns)
cols = df1.columns

print("Size of files!")
print(len(df0),infilenames[0])
print(len(df1),infilenames[1])

print(df0.columns)
print()
print(df1.columns)
print()

#exit()

toberemoved = []
toberemoved.append('bnv_dR12_lab')
toberemoved.append('bnv_dR13_lab')
toberemoved.append('bnv_dR1_23_lab')
toberemoved.append('bnv_dR23_lab')
toberemoved.append('bnv_dR3_12_lab')
toberemoved.append('bnv_dTheta12_CMtop')
toberemoved.append('bnv_dTheta13_CMtop')
toberemoved.append('bnv_dTheta1_23_CMtop')
toberemoved.append('bnv_dTheta23_CMtop')
toberemoved.append('bnv_dTheta3_12_CMtop')
toberemoved.append('bnv_j12_m')
toberemoved.append('bnv_j13_m')
toberemoved.append('bnv_j1_btag')
toberemoved.append('bnv_j1_mag_CMtop')
toberemoved.append('bnv_j1_mag_lab')
toberemoved.append('bnv_j1_pt_CMtop')
toberemoved.append('bnv_j1_pt_lab')
toberemoved.append('bnv_j23_m')
toberemoved.append('bnv_j2_btag')
toberemoved.append('bnv_j2_mag_CMtop')
toberemoved.append('bnv_j2_mag_lab')
toberemoved.append('bnv_j2_pt_CMtop')
toberemoved.append('bnv_j2_pt_lab')
toberemoved.append('bnv_j3_mag_CMtop')
toberemoved.append('bnv_j3_mag_lab')
toberemoved.append('bnv_j3_pt_CMtop')
toberemoved.append('bnv_j3_pt_lab')
toberemoved.append('bnv_lep_q')
#toberemoved.append('bnv_top_m')
#toberemoved.append('bnv_top_mag')
#toberemoved.append('bnv_top_pt')

toberemoved.append('event_idx')


for tbr in toberemoved:
    if tbr in cols:
        print("Yes! ",tbr)
    else:
        print("No! ",tbr)



#df0 = format(df0, ['cos(theta)', 'p3'], 0, 'signal')
#df1 = format(df1, ['cos(theta)', 'p3'], 0, 'background')
df0 = format(df0, toberemoved, 0, 'signal')
df1 = format(df1, toberemoved, 0, 'background')

#df = mergeDataframes([df0[0:100000], df1[0:100000]])
#df = mergeDataframes([df0[0:50000], df1[0:50000]])
#df = mergeDataframes([df0[100000:200000], df1[100000:200000]])
#df = mergeDataframes([df0[0:10000], df1[0:10000]])
df = mergeDataframes([df0, df1])

# Get rid of nans
df.dropna(0,inplace=True)

print("Merged and dropped columns!")
print(df.columns)
print()
#exit()


# split into input and output columns
y = df.pop('Class') # all class values become 'y'
X = df

print("Lenth of X and y!")
print(len(X))
print(len(y))

# ensure all data are floating point values
X = X.astype('float32')
# encode strings to integer
y = LabelEncoder().fit_transform(y)
# split into train and test datasets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)

#.shape returns the dimensions of the dataset. So (48778, 18) means 48778 rows and 18 columns
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape) 

# determine the number of input features
n_features = X_train.shape[1] # 2nd item returned by ".shape" is the # of columns/features


print(y[0:10])
print(y[40000:40010])

# define model
model = Sequential()
model.add(Dense(10, activation='relu', kernel_initializer='he_normal', input_shape=(n_features,)))
model.add(Dense(8, activation='relu', kernel_initializer='he_normal'))
model.add(Dense(1, activation='sigmoid'))

# compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
# fit the model
history = model.fit(X_train, y_train, epochs=105, batch_size=100, validation_split=0.3, verbose=1)
#history = model.fit(X_train, y_train, epochs=105, batch_size=100, validation_split=0.5, verbose=1)
# evaluate the model
loss, acc = model.evaluate(X_test, y_test, verbose=0)
print('Test Accuracy: %.3f' % acc)

# make a prediction
row = X_test.iloc[[0]] # row/one particle to run prediction on
yhat = model.predict([row]) # makes prediction
print('Predicted: %.3f' % yhat) # 1 = proton, 0 = not proton

model.summary()

tag = '{0}_{1}'.format(infilenames[0].split('/')[-1].split('.h5')[0],infilenames[1].split('/')[-1].split('.h5')[0])
modelfilename = f'models/KERAS_TRAINING_{tag}.h5'
model.save(modelfilename)

sktools.compare_train_test(model, X_train, y_train, X_test, y_test, bins=200,tag=tag)

# summarize the model
# Need pydot and graphviz for this
plot_model(model, f'plots/MODEL_LAYOUT_{tag}.png', show_shapes=True)


# plot learning curves
pyplot.figure()
pyplot.title('Learning Curves')
pyplot.xlabel('Epoch')
pyplot.ylabel('Cross Entropy')
pyplot.plot(history.history['loss'], label='train')
pyplot.plot(history.history['val_loss'], label='val')
pyplot.legend()
pyplot.savefig(f'plots/KERAS_LEARNING_CURVE_{tag}.png')

y_pred_keras = model.predict(X_test).ravel()
fpr_keras, tpr_keras, thresholds_keras = roc_curve(y_test, y_pred_keras)

auc_keras = auc(fpr_keras, tpr_keras)

# Supervised transformation based on random forests
rf = RandomForestClassifier(max_depth=3, n_estimators=10)
rf.fit(X_train, y_train)

modelfilename = f'models/SKLEARN_RANDOM_FOREST_TRAINING_{tag}.joblib'
joblib.dump(rf, modelfilename)

y_pred_rf = rf.predict_proba(X_test)[:, 1]
fpr_rf, tpr_rf, thresholds_rf = roc_curve(y_test, y_pred_rf)
auc_rf = auc(fpr_rf, tpr_rf)


mlp = MLPClassifier(hidden_layer_sizes=5, max_iter=1000, verbose=True)
# fit function: trains algorithm on training data
mlp_model = mlp.fit(X_train, y_train)

modelfilename = f'models/SKLEARN_MLP_TRAINING_{tag}.joblib'
joblib.dump(mlp_model,modelfilename)

y_pred_mlp = mlp.predict_proba(X_test)[:, 1]
fpr_mlp, tpr_mlp, thresholds_mlp = roc_curve(y_test, y_pred_mlp)
auc_mlp = auc(fpr_mlp, tpr_mlp)

data_to_save = {}
data_to_save['fpr_keras'] = fpr_keras
data_to_save['tpr_keras'] = tpr_keras
data_to_save['thresholds_keras'] = thresholds_keras
df_out = pd.DataFrame.from_dict(data_to_save)
df_out.to_hdf(f'models/roc_out_{tag}.h5','df_out')

pyplot.figure()
pyplot.plot([0, 1], [0, 1], 'k--')
pyplot.plot(fpr_keras, tpr_keras, label='Keras (area = {:.3f})'.format(auc_keras))
pyplot.plot(fpr_rf, tpr_rf, label='RF (area = {:.3f})'.format(auc_rf))
pyplot.plot(fpr_mlp, tpr_mlp, label='MLP (area = {:.3f})'.format(auc_mlp))
pyplot.xlabel('False positive rate')
pyplot.ylabel('True positive rate')
pyplot.title('ROC curve')
pyplot.legend(loc='best')
pyplot.savefig(f'plots/KERAS_ROC_CURVE_{tag}.png')

'''
# Zoom in view of the upper left corner.
pyplot.figure()
pyplot.xlim(0, 0.2)
pyplot.ylim(0.8, 1)
pyplot.plot([0, 1], [0, 1], 'k--')
pyplot.plot(fpr_keras, tpr_keras, label='Keras (area = {:.3f})'.format(auc_keras))
pyplot.plot(fpr_rf, tpr_rf, label='RF (area = {:.3f})'.format(auc_rf))
pyplot.xlabel('False positive rate')
pyplot.ylabel('True positive rate')
pyplot.title('ROC curve (zoomed in at top left)')
pyplot.legend(loc='best')
'''


print("Displaying plots")
pyplot.show()

# this curve shows underfitting. How to fix?


