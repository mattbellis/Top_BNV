import pandas as pd


# Expects a dataframe
def selection_dRcut(df, dRcut=0.0):
    mask = (df['had_dTheta12_CMtop'] > dRcut) & \
           (df['had_dTheta23_CMtop'] > dRcut) & \
           (df['had_dTheta13_CMtop'] > dRcut) & \
           (df['had_dTheta1_23_CMtop'] > dRcut) & \
           (df['had_dTheta3_12_CMtop'] > dRcut) & \
           (df['bnv_dTheta12_CMtop'] > dRcut) & \
           (df['bnv_dTheta23_CMtop'] > dRcut) & \
           (df['bnv_dTheta13_CMtop'] > dRcut) & \
           (df['bnv_dTheta1_23_CMtop'] > dRcut) & \
           (df['bnv_dTheta3_12_CMtop'] > dRcut)

    return mask

