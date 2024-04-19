# EvaluateRF_0J.py

import joblib
import numpy as np

#rf = joblib.load('/afs/cern.ch/work/s/sblancof/private/Run2Analysis/mkShapesRDF/examples/MyFull2017_v9/RandomForestCategorical/random_forest_Categorical.pkl')

def load_random_forest_model(inputs):
    try:
        return [-999.9]
        #result = rf.predict_proba(np.array(inputs).reshape(1, -1))
        #return [result[0][1]]
    except Exception as e:
        return [-99.9]

if __name__ == "__main__":
    # You can include some test code here for local testing
    test_input = [1.0, 2.0, 3.0, 4., 5., 6., 7., 8., 9., 10., 11., 12., 13., 14., 15.]
    result = load_random_forest_model(test_input)
    print("Result:", result)
