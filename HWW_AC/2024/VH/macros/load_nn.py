import numpy as np
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# 2. Silence the CPU feature guard warnings (AVX2, AVX512, etc.)
# '2' filters out INFO and WARNING messages, leaving only ERRORS.
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
from tensorflow.keras.models import load_model

N_FEATURES = 23
means = np.array([ 3.0511398315430, -0.0003265215200, 1.7531279325485, 527.9433593750000, 390.8070373535156, 94.1194839477539, 94.8735504150391, 78.4361343383789, 0.0024167520460, 0.0025929037947, 118.7911987304688, 60.1717529296875, 1.6956757307053, 86.1391296386719, 0.4473632574081, 278.0943298339844, 239.1411590576172, 187.8593444824219, 174.2985992431641, -0.0008020567475, -0.0030226092786, 77.8747558593750, 41.0843353271484]
, dtype=np.float32)

sigmas = np.array([ 1.8011655807495, 1.6184015274048, 0.9314146041870, 587.1565551757812, 192.6058502197266, 18.0009632110596, 86.8571166992188, 55.6762313842773, 2.0143384933472, 2.3785352706909, 82.9669265747070, 32.4114913940430, 0.7333313822746, 50.5885505676270, 1.2077165842056, 202.0291900634766, 205.8050842285156, 147.5556030273438, 152.8744659423828, 1.1719994544983, 1.1872959136963, 49.2313461303711, 25.5916996002197]
, dtype=np.float32)

# --- Load the Model (Using compile=False to ignore training/custom loss logic) ---
model_path = "/eos/user/s/squinto/SWAN_projects/ML/VBF classifier/saved_models/dbnn_consistent.h5"

try:
    # Adding compile=False strips away the custom loss/KDE tracking dependencies
    model = load_model(model_path, compile=False)
    print("Model loaded successfully using compile=False!")
except Exception as e:
    print(f"Error loading model directly: {e}")
    print("Attempting backup checkpoint restoration method...")
    # If the .h5 metadata still fails due to keras.api, use the bare layout fallback:
    def build_bare_model():
        m = tf.keras.models.Sequential([
            tf.keras.layers.Input(shape=(N_FEATURES,)),
            *[tf.keras.layers.Dense(50, activation='relu') for _ in range(5)],
            tf.keras.layers.Dense(4, activation='softmax')
        ])
        return m
    model = build_bare_model()
    tf.train.Checkpoint(model=model).read(model_path).expect_partial()


def load_dbnn_model(inputs):
    try:
        # Convert input to array and reshape for inference (1, 23)
        input_array = np.array(inputs, dtype=np.float32).reshape(1, -1)

        # Scale features using your manual mean/sigma constants
        inputs_scaled = (input_array - means) / (sigmas + 1e-12)

        # Predict probabilities (using standard __call__ instead of .predict for speed in loops)
        probabilities_tensor = model(inputs_scaled, training=False)
        
        # Mirror original clipping constraints
        clipped_probabilities = tf.clip_by_value(probabilities_tensor, 1e-7, 1. - 1e-7)
        probabilities = clipped_probabilities.numpy()[0]

        # Extract argmax selection
        predicted_class = int(np.argmax(probabilities))

        return [
            float(probabilities[0]),
            float(probabilities[1]),
            float(probabilities[2]),
            float(probabilities[3]),
            predicted_class,
        ]
    except Exception:
        return [-99.9, -99.9, -99.9, -99.9, -1]


if __name__ == "__main__":
    # Test vector matching your 23 features
    test_input_nominal = [ 7.01123047e+00, -8.47190857e-01,  9.69886780e-01,  3.83019458e+03,
        3.69179749e+02,  1.17840134e+02,  4.75591087e+01,  3.80897636e+01,
       -3.44482422e+00,  3.56640625e+00,  1.24569130e+02,  1.06041901e+02,
        2.98987722e+00,  9.16684036e+01, -2.00477441e+00,  4.34046814e+02,
        4.93643585e+02,  4.90124146e+02,  3.67717896e+02, -1.71148300e-01,
        3.01025391e-01,  5.45982666e+01,  4.58807106e+01]
    test_input_relsampleup = [ 7.01123047e+00, -8.47190857e-01,  9.69886780e-01,  3.72618311e+03,
        3.64975586e+02,  1.20873604e+02,  4.76349525e+01,  4.00171661e+01,
       -3.44482422e+00,  3.56640625e+00,  1.20769775e+02,  1.03518105e+02,
        2.98347187e+00,  9.18489151e+01, -2.00477441e+00,  4.34046814e+02,
        4.93643585e+02,  4.90124146e+02,  3.67717896e+02, -1.71148300e-01,
        3.01025391e-01,  5.45982666e+01,  4.58807106e+01]
    test_input_relsampledo = [ 7.01123047e+00, -8.47190857e-01,  9.69886780e-01,  3.93416333e+03,
        3.73329529e+02,  1.14351364e+02,  4.76061325e+01,  3.57291107e+01,
       -3.44482422e+00,  3.56640625e+00,  1.28368484e+02,  1.08565697e+02,
        3.01634789e+00,  9.18554001e+01, -2.00477441e+00,  4.34046814e+02,
        4.93643585e+02,  4.90124146e+02,  3.67717896e+02, -1.71148300e-01,
        3.01025391e-01,  5.45982666e+01,  4.58807106e+01]

    result_nominal = load_dbnn_model(test_input_nominal)
    result_relsampleup = load_dbnn_model(test_input_relsampleup)
    result_relsampledo = load_dbnn_model(test_input_relsampledo)
    print("Result nominal:", result_nominal)
    print("Result relsampleup:", result_relsampleup)
    print("Result relsampledo:", result_relsampledo)
