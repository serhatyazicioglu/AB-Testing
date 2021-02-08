import pandas as pd
from scipy.stats import shapiro
import scipy.stats as stats

df_test = pd.read_excel("datasets/ab_testing_data.xlsx", sheet_name="Test Group")
df_control = pd.read_excel("datasets/ab_testing_data.xlsx", sheet_name="Control Group")

df_test.head()
df_control.head()

df_control.info()
df_test.info()

df_test.shape
df_control.shape


# Setting threshold value for outliers
def outlier_thresholds(dataframe, variable, low_quantile=0.05, up_quantile=0.95):
    quantile_one = dataframe[variable].quantile(low_quantile)
    quantile_three = dataframe[variable].quantile(up_quantile)
    interquantile_range = quantile_three - quantile_one
    up_limit = quantile_three + 1.5 * interquantile_range
    low_limit = quantile_one - 1.5 * interquantile_range
    return low_limit, up_limit


# Checks for any outliers in the variable.
def has_outliers(dataframe, numeric_columns):
    for col in numeric_columns:
        low_limit, up_limit = outlier_thresholds(dataframe, col)
        if dataframe[(dataframe[col] > up_limit) | (dataframe[col] < low_limit)].any(axis=None):
            number_of_outliers = dataframe[(dataframe[col] > up_limit) | (dataframe[col] < low_limit)].shape[0]
            print(col, " : ", number_of_outliers, "outliers")


for var in df_control:
    print(var, "has ", has_outliers(df_control, [var]), "Outliers")

for var in df_test:
    print(var, "has ", has_outliers(df_test, [var]), "Outliers")

# How would you describe the hypothesis of the A / B test?

# H0 : There is no statistical difference between the control and test groups in terms of average number of purchases.
# H1 : There is a statistical difference between the control and test groups in terms of the average number of purchases.


df_control["Purchase"].mean()
df_test["Purchase"].mean()

group_a = df_control["Purchase"]
group_b = df_test["Purchase"]

# 1- Assumption Check

# 1.1 - Normality Assumption

test_statistics, pvalue = shapiro(group_a)
print('Test Statistics = %.4f, p-value = %.4f' % (test_statistics, pvalue))

pvalue < 0.05

# If p-value <0.05 HO rejected.
# If p-value is not <0.05 H0 CAN NOT be rejected.
# group_a is distributed normally.

test_statistics, pvalue = shapiro(group_b)
print('Test Statistics = %.4f, p-value = %.4f' % (test_statistics, pvalue))

pvalue < 0.05

# If p-value <0.05 HO rejected.
# If p-value is not <0.05 H0 CAN NOT be rejected.
# group_b is distributed normally.

# 1.2 - Variance Homogeneity Assumption

# H0: Variances Are Homogeneous
# H1: Variances Are Not Homogeneous

test_statistics, pvalue = stats.levene(group_a, group_b)
print('Test Statistics = %.4f, p-value = %.4f' % (test_statistics, pvalue))

pvalue < 0.05

# If p-value <0.05 HO rejected.
# If p-value is not <0.05 H0 CAN NOT be rejected.
# Variance homogeneity provided.

# HO: there is no statistical difference between the control and test groups in terms of average number of purchases.
# H1: there is a statistical difference between the control and test groups in terms of average number of purchases

# 1.1 Independent two-sample t-test if assumptions are provided (parametric test)
test_statistics, pvalue = stats.ttest_ind(group_a, group_b, equal_var=True)
print('Test Statistics = %.4f, p-value = %.4f' % (test_statistics, pvalue))

# Can we make statistically significant results?

# There is no statistically significant difference between the control group and test groups.
# The two groups are alike.

# Which test did you use? Why is that?

# We used the two-sample t-test (parametric test) since both assumptions are satisfied

# What is your advice to the customer?
# There is no statistical difference between average bidding and maximum bidding
# It can be preferred with a low cost per click.
# We can evaluate the differences in interaction gain and conversion rates and determine which method is more profitable.
# The test can be extended for 1 month.
# The number of observations can be increased.
