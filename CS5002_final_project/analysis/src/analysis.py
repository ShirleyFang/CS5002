import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt

import os

class Analysis:
    def __init__(self):
        self.invalid_rows = 0
        self.df = pd.read_csv("../data/SleepStudyData.csv")

    def data_clean(self):
        self.df = self.df.dropna()
        enough_sleep_time = [7, 8, 9]
        df = self.df[((self.df["Enough"] == "No") & (self.df["Hours"] <= 6)) |
                     ((self.df["Enough"] == "Yes") & (self.df["Hours"].isin(enough_sleep_time)))]
        self.df = pd.DataFrame(df)
        # print(self.df.head())
        # self.df.to_csv("clean_data.csv")
        
    @staticmethod
    def get_A_probability(df, total):
        count_enough = df["Enough"].value_counts()["No"]
        P_A = round(count_enough / total, 2)
        return P_A

    @staticmethod
    def get_A_complement(P_A):
        return round(1 - P_A, 2)
    
    @staticmethod
    def get_B_probability(df, total):
        count_phone_reach = df["PhoneReach"].value_counts()["Yes"]
        P_B = round(count_phone_reach / total, 2)
        return P_B

    @staticmethod
    def get_B_complement(P_B):
        return round(1 - P_B, 2)

    @staticmethod
    def get_C_probability(df, total):
        count_phone_time = df["PhoneTime"].value_counts()["Yes"]
        P_C = round(count_phone_time / total, 2)
        return P_C

    @staticmethod
    def get_C_complement(P_C):
        return round(1 - P_C, 2)

    @staticmethod
    def get_D_probability(df, total):
        count_tired = (df["Tired"].value_counts()[4]
                       + df["Tired"].value_counts()[5]
                       + df["Tired"].value_counts()[3])
        P_D = round(count_tired / total, 2)
        return P_D

    @staticmethod
    def get_D_complement(P_D):
        return round(1 - P_D, 2)
    
    @staticmethod
    def get_P_A_intersection_B(df, total):
        count_enough_and_phone_reach = df[((df["Enough"] == "No") & (df["PhoneReach"] == "Yes"))]
        P_A_intersection_B = round(len(count_enough_and_phone_reach) / total, 2)
        return P_A_intersection_B

    @staticmethod
    def get_P_A_intersection_C(df, total):
        count_not_enough = df["Enough"].value_counts()["No"]
        count_enough_and_phone_time = df[((df["Enough"] == "No") & (df["PhoneTime"] == "Yes"))]
        P_A_intersection_C = round(len(count_enough_and_phone_time) / total, 2)
        print("----------------------------------------------------------------------------")
        print(round(len(count_enough_and_phone_time) / count_not_enough, 2))
        print("----------------------------------------------------------------------------")
        return P_A_intersection_C

    @staticmethod
    def get_P_A_intersection_D(df, total):
        count_not_enough = df["Enough"].value_counts()["No"]
        count_enough = df["Enough"].value_counts()["Yes"]
        count_not_enough_and_tired = df[((df["Enough"] == "No") & ((df["Tired"] == 3) | (df["Tired"] == 4) | (df["Tired"] == 5)))]
        P_A_intersection_D = round(len(count_not_enough_and_tired) / total, 2)
        P_A_intersection_D_not_enough = round(len(count_not_enough_and_tired) / count_not_enough, 2)
        count_enough_and_tired = df[((df["Enough"] == "Yes") & ((df["Tired"] == 3) | (df["Tired"] == 4) | (df["Tired"] == 5)))]
        print("----------------------------------------------------------------------------")
        print(round(len(count_enough_and_tired) / count_enough, 2))
        print(P_A_intersection_D_not_enough)
        print("----------------------------------------------------------------------------")
        return P_A_intersection_D

    @staticmethod
    def get_P_B_intersection_C(df):
        count_phone_reach = df["PhoneReach"].value_counts()["Yes"]
        count_phone_reach_and_phone_time = df[((df["PhoneReach"] == "Yes") & (df["PhoneTime"] == "Yes"))]
        P_B_intersection_C = round(len(count_phone_reach_and_phone_time) / count_phone_reach, 2)
        return P_B_intersection_C
    
    @staticmethod
    def get_P_A_and_B_intersection_C(df):
        # X: B and C happen at the same time
        count_enough = df["Enough"].value_counts()["No"]
        A_B_and_C_intersection = df[((df["Enough"] == "No") & (df["PhoneReach"] == "Yes") & (df["PhoneTime"] == "Yes"))]
        P_X_A = round(len(A_B_and_C_intersection) / count_enough, 2)
        return P_X_A
    
    @staticmethod
    def data_analysis():
        df = pd.read_csv("clean_data.csv")
        df = pd.DataFrame(df)
        count_enough = df["Enough"].value_counts()["No"]
        total = len(df)

        # A: Not enough
        P_A = Analysis.get_A_probability(df, total)
        P_A_complement = Analysis.get_A_complement(P_A)
        # print(P_A)
        # print(P_A_complement)
        count_phone_reach = df["PhoneReach"].value_counts()["Yes"]
        #: PhoneReach is YES
        P_B = Analysis.get_B_probability(df, total)
        P_B_complement = Analysis.get_B_complement(P_B)
        # print(P_B)
        # print(P_B_complement)
        #: PhoneTime is YES
        P_C = Analysis.get_C_probability(df, total)
        P_C_complement = Analysis.get_C_complement(P_C)
        # print(P_C)
        # print(P_C_complement)
        # D: tired
        P_D = Analysis.get_D_probability(df, total)
        P_D_complement = Analysis.get_D_complement(P_D)
        # print(P_D)
        # print(P_D_complement)
        P_A_intersection_B = Analysis.get_P_A_intersection_B(df, total)
        print("The probability of not enough sleep and phone reach:", P_A_intersection_B)
        P_A_intersection_C = Analysis.get_P_A_intersection_C(df, total)
        print("The probability of not enough sleep and phone reach:", P_A_intersection_C)
        P_B_intersection_C = Analysis.get_P_B_intersection_C(df)
        print("The probability of phone time and phone reach:", P_B_intersection_C)
        P_A_intersection_D = Analysis.get_P_A_intersection_D(df, total)
        print("The probability of not enough and tired:", P_A_intersection_D)
        P_B_A = round(P_A_intersection_B / P_A, 2)
        P_C_A = round(P_A_intersection_C / P_A, 2)
        P_D_A = round(P_A_intersection_D / P_A, 2)
        
        P_A_B = round(P_B_A * P_A / P_B, 2)
        P_A_C = round(P_C_A * P_A / P_C, 2)
        P_A_D = round(P_D_A * P_A / P_D, 2)
        
        print("-------------------")
        print("The probability of A, given B:", P_A_B)
        print("The probability of B, given A:", P_B_A)
        print("The probability of A, given C:", P_A_C)
        print("The probability of C, given A:", P_C_A)
        print("The probability of A, given D:", P_D_A)
        print("The probability of D, given A:", P_A_D)
        # 
        # X: B and C happen at the same time
        # A_B_and_C_intersection = df[((df["Enough"] == "No") & (df["PhoneReach"] == "Yes") & (df["PhoneTime"] == "Yes"))]
        # P_X_A = round(len(A_B_and_C_intersection) / count_enough, 5)  # round(len(A_B_and_C_intersection) / (total * P_A), 5)
        P_X_A = Analysis.get_P_A_and_B_intersection_C(df)
        print('This value represents the likelihood of both "PhoneReach" and "PhoneTime" being "Yes" given that "Enough" is "No".', P_X_A)
       

a = Analysis()
a.data_clean()
a.data_analysis()
