# grid_search.py

from sklearn import model_selection


class GridSearch():
    """
    The GridSearch class implements GridSearchCV from sklearn and
    acts as a wrapper around SocialMeter's architecture for that
    class.
    """
    def __init__(self, parameters):
        """
        `parameters` should be an array of dictionaries of parameters
        and their various configurations.

        Example (none of the variable names are real):
        [{'param': ['value1'], other_param: ['v1', 'v2']},
        {'param': ['value2'], another_param: ['1', '2', '3']}]

        In this example, a search will be done on the first dictionary
        and all the possible combinations of the parameters. Afterwards,
        the second dictionary will also be tested. The results will then
        be compared against each other.
        """
        self.parameters = parameters
        self.cv = 5

    def search_meter(self, meter, data):
        """
        Tests the classifier module. Note that the module must implement
        `score` and the instantiated GridSearch's `parameters` field
        must be a valid object.

        This runs on 5 threads by default.
        """
        threads = 5

        classif = meter.class_mod.classifier
        grid = model_selection.GridSearchCV(
            classif, self.parameters, cv=self.cv,
            n_jobs=threads)

        texts = data[0]
        classifications = data[1]
        features = meter.extract_features(texts)

        print(features[0], features[1])

        grid.fit(features, classifications)

        results = grid.cv_results_
        length = len(results["mean_test_score"])

        # Rotate to be dicts of results instead of a "DataFrame" format
        fixed_results = [dict() for _ in range(length)]
        # Go through each key...
        for k in results.keys():
            # Get the list of values for that key...
            value = results[k]
            # Go through each value in the list of values...
            for i in range(len(value)):
                # Get the value
                r_value = value[i]
                # Set the location of the value to the new value
                fixed_results[i][k] = r_value
                if k == 'mean_test_score':
                    print(r_value)
                    print(value)
                    print()

        return sorted(fixed_results,
                      key=lambda r: r['mean_test_score'],
                      reverse=True)
