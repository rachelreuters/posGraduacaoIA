"""
This is a boilerplate pipeline 'classifier'
generated using Kedro 0.19.11
"""
import pandas as pd


def prepare_data(raw_data):

    return (
        raw_data
        [
            ['Survived', 'Pclass', 'Age', 'SibSp', 'Parch', 'Fare']
        ]
        .join(pd.get_dummies(raw_data['Sex'], prefix="Sex"))
        .join(pd.get_dummies(raw_data['Embarked'], prefix='Embarked'))
        .dropna()
        .assign(Survived=lambda x: x['Survived'].astype(bool))
    )
