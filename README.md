# IEEE-CIS-Fraud-Detection

In this classification project,online transactions must be monitored to detect fraudulent transactions based on historic data which is in form of a time series data set.

In order to block a transaction detected as fruad, we need to find anomalies in the transactions and show it to the model so that it can learn and when it observe such anomalies in a transaction it can classify it as fraud.

I've done extensive EDA to figure out relation between current features, their evolution through time and the relation between their exception conditions and fruad in a transaction.

Several features are engineered based in EDA and some online research to get more domain knowledge and lgbm was chosen as the single model for this problem.

AUC score for this model was 0.910340.
