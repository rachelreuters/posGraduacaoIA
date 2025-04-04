from kedro.pipeline import Pipeline, node, pipeline

from . import nodes


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=nodes.prepare_Y_X_prod,
                inputs=["raw_prod"],
                outputs=["X_prod", "Y_prod"],
                tags=["prod_run" ]
            ),
            node(
                func=nodes.model_prod,
                inputs=["X_prod"],
                outputs=["y_pred_prod", "y_prob_prod" ],
                tags=["prod_run" ]
            ),
            node(
                func=nodes.generate_main_metrics,
                inputs=["X_prod", "Y_prod", "y_pred_prod", "y_prob_prod"],
                outputs="predict_prod_server",
                tags=["prod_analysis"]
            ),
            node(
                func=nodes.generate_roc_plot,
                inputs=["Y_prod","y_prob_prod"],
                outputs=None,
                tags=["prod_analysis"]
            ),
            node(
                func=nodes.lat_lon_plot_model_success,
                inputs=["Y_prod","y_pred_prod","X_prod" ],
                outputs=None,
                tags=["prod_analysis"]
            ),
            node(
                func=nodes.plot_shot_balance,
                inputs=["Y_prod"],
                outputs=None,
                tags=["prod_analysis"]
            )

        ]
    )
