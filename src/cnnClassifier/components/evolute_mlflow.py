import tensorflow as tf
from pathlib import Path
import mlflow
import mlflow.keras
from urllib.parse import urlparse
from cnnClassifier.entity.config_entity import EvaluationConfig
from cnnClassifier.utils.common import save_json
import dagshub




class Evaluation:
    def __init__(self, config: EvaluationConfig):
        self.config = config

    def _valid_generator(self):

        datagenerator_kwargs = dict(
            rescale = 1./255,
            validation_split=0.30
        )

        dataflow_kwargs = dict(
            target_size=self.config.params_image_size[:-1],
            batch_size=self.config.params_batch_size,
            interpolation="bilinear"
        )

        valid_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
            **datagenerator_kwargs
        )

        self.valid_generator = valid_datagenerator.flow_from_directory(
            directory=self.config.training_data,
            subset="validation",
            shuffle=False,
            **dataflow_kwargs
        )

    @staticmethod
    def load_model(path: Path) -> tf.keras.Model:
        return tf.keras.models.load_model(path)
    
    def evaluation(self):
        self.model = self.load_model(self.config.path_of_model)
        self._valid_generator()
        self.score = self.model.evaluate(self.valid_generator)
        self.save_score()

    def save_score(self):
        scores = {"loss": self.score[0], "accuracy": self.score[1]}
        save_json(path=Path("scores.json"), data=scores)

    
    def log_into_mlflow(self):

        dagshub.init(
        repo_owner='datanerdppts', 
        repo_name='Dog_Cat_Classification_With_MLOPS', 
        mlflow=True
    )
        mlflow.set_registry_uri(self.config.mlflow_uri)
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        with mlflow.start_run():
            mlflow.log_params(self.config.all_params)
            mlflow.log_metrics(
                {"loss": self.score[0], "accuracy": self.score[1]}
            )
            # Model registry does not work with file store
            if tracking_url_type_store != "file":

                # Register the model
                # There are other ways to use the Model Registry, which depends on the use case,
                # please refer to the doc for more information:
                # https://mlflow.org/docs/latest/model-registry.html#api-workflow
                mlflow.keras.log_model(self.model, "model", registered_model_name="VGG16Model")
            else:
                mlflow.keras.log_model(self.model, "model")






# import dagshub
# dagshub.init(repo_owner='datanerdppts', repo_name='Dog_Cat_Classification_With_MLOPS', mlflow=True)

# import mlflow
# with mlflow.start_run():
#   mlflow.log_param('parameter name', 'value')
#   mlflow.log_metric('metric name', 1)



#   8813d33483814238d0b2f24b7f9ee7b591c16a11
#   https://dagshub.com/datanerdppts/Dog_Cat_Classification_With_MLOPS.mlflow




# export MLFLOW_TRACKING_URI=https://dagshub.com/datanerdppts/Dog_Cat_Classification_With_MLOPS.mlflow

# export MLFLOW_TRACKING_USERNAME=datanerdppts 

# export MLFLOW_TRACKING_PASSWORD=8813d33483814238d0b2f24b7f9ee7b591c16a11




# set MLFLOW_TRACKING_URI=https://dagshub.com/datanerdppts/Dog_Cat_Classification_With_MLOPS.mlflow
# set MLFLOW_TRACKING_USERNAME=datanerdppts
# set MLFLOW_TRACKING_PASSWORD=8813d33483814238d0b2f24b7f9ee7b591c16a11

