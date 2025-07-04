# cnn classifier for dog cat classification



import dagshub
dagshub.init(repo_owner='datanerdppts', repo_name='Dog_Cat_Classification_With_MLOPS', mlflow=True)

import mlflow
with mlflow.start_run():
  mlflow.log_param('parameter name', 'value')
  mlflow.log_metric('metric name', 1)