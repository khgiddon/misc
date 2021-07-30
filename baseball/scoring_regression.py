# Data downloaded from http://www.seanlahman.com/baseball-archive/statistics/

import pandas as pd
import statsmodels.api as sm

# Import dataset
path = '/data/core/'
df = pd.read_csv(path + 'Teams.csv')

# Clean dataset (restrict to 2015 and following; create singles variable)
df = df[df['yearID'] >= 2015]
df['1B'] = df['H'] - df['2B'] - df['3B'] - df['HR']

# Run model
x = df[['BB','1B','2B','3B','HR','BB']]
y = df[['R']]
mod = sm.OLS(y, x)
res = mod.fit()
print(res.summary())

"""
                                 OLS Regression Results                                
=======================================================================================
Dep. Variable:                      R   R-squared (uncentered):                   0.998
Model:                            OLS   Adj. R-squared (uncentered):              0.998
Method:                 Least Squares   F-statistic:                          2.098e+04
Date:                Mon, 28 Jun 2021   Prob (F-statistic):                   4.75e-241
Time:                        20:51:29   Log-Likelihood:                         -854.41
No. Observations:                 180   AIC:                                      1719.
Df Residuals:                     175   BIC:                                      1735.
Df Model:                           5                                                  
Covariance Type:            nonrobust                                                  
==============================================================================
                 coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------
BB             0.1012      0.019      5.203      0.000       0.063       0.140
1B             0.1702      0.025      6.820      0.000       0.121       0.219
2B             0.7697      0.097      7.910      0.000       0.578       0.962
3B             0.5710      0.272      2.097      0.037       0.034       1.109
HR             1.2891      0.075     17.232      0.000       1.141       1.437
BB             0.1012      0.019      5.203      0.000       0.063       0.140
==============================================================================
Omnibus:                        4.283   Durbin-Watson:                   2.205
Prob(Omnibus):                  0.117   Jarque-Bera (JB):                4.216
Skew:                          -0.374   Prob(JB):                        0.121
Kurtosis:                       2.953   Cond. No.                     7.61e+15
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
[2] The smallest eigenvalue is 3.85e-24. This might indicate that there are
strong multicollinearity problems or that the design matrix is singular.
"""
