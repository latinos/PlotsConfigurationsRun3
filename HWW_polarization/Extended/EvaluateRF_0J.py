# EvaluateRF_1J.py

import joblib
import numpy as np

rf_0 = joblib.load('/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/examples/extended/Training/random_forest_Categorical_0j_df.pkl')

def load_random_forest_model_0jet(inputs_0):
    try:
        result_0_1 = rf_0.predict_proba(np.array(inputs_0).reshape(1, -1))
        result_0_2 = rf_0.predict(np.array(inputs_0).reshape(1, -1))
        return [result_0_1[0][0], result_0_1[0][1], result_0_1[0][2], result_0_2[0][0], result_0_2[0][1], result_0_2[0][2]]
    except Exception as e:
        return [-99.9, -99.9, -99.9]

if __name__ == "__main__":
    # You can include some test code here for local testing
    test_input = [1.0, 2.0, 3.0, 4., 5., 6., 7., 8., 9., 10., 11., 12., 13., 14., 15.]
    result = load_random_forest_model_1jet(test_input)
    print("Result:", result)
