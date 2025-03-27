from pycaret.classification import *
import pandas as pd
from sklearn.metrics import log_loss, f1_score
import mlflow


def model_prod(data: pd.DataFrame, model) -> pd.DataFrame:

    data_filtered = data.dropna()

    X_test = data_filtered[['lat','lon','minutes_remaining','period','playoffs','shot_distance']]
    Y_test = data_filtered[['shot_made_flag']]

    y_pred_prob = model.predict_proba(X_test)
    y_pred = model.predict(X_test)

    log_loss_value = log_loss(Y_test, y_pred_prob)

    f1_value = f1_score(Y_test, y_pred)

    predictions_df = pd.DataFrame({
        "Actual": Y_test.values.ravel(),
        "Predicted": y_pred
    }, index=X_test.index)

    result_df = pd.concat([X_test, predictions_df], axis=1)

    mlflow.set_tag("mlflow.runName", "metrics_prod")

    mlflow.log_metric(f"log_loss", log_loss_value)
    mlflow.log_metric(f"f1_score", f1_value)

    return result_df



