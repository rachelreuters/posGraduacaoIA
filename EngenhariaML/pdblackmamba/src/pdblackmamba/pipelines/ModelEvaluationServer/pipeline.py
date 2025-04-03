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
                outputs=["y_prod_pred", "y_prod_pred_prob" ],
                tags=["prod_run" ]
            ),
            node(
                func=nodes.generate_main_metrics,
                inputs=["X_prod", "Y_prod", "y_prod_pred", "y_prod_pred_prob"],
                outputs="predict_prod_server",
                tags=["prod_analysis"]
            ),
            node(
                func=nodes.generate_roc_plot,
                inputs=["Y_prod","y_prod_pred_prob"],
                outputs=None,
                tags=["prod_analysis"]
            ),
            node(
                func=nodes.lat_lon_plot_model_success,
                inputs=["Y_prod","y_prod_pred","X_prod" ],
                outputs=None,
                tags=["prod_analysis"]
            )
        ]
    )
