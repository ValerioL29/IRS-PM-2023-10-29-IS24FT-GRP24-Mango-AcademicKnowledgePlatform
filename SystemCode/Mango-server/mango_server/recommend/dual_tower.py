import numpy as np
import tensorflow as tf

from mango_server.db.core import get_paper_details_with_titles


# Load TFLite model and allocate tensors.
model_path = "models/naive_dual_tower.tflite"
interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


async def get_top_candidates_for_user(user_id: str, num_candidate: int = 10):
    """
    Get top candidates for user from the dual tower model.
    """
    # Test the model.
    interpreter.set_tensor(input_details[0]["index"], np.array([user_id]))
    # Search within index
    interpreter.invoke()
    # Get the results
    scores = interpreter.get_tensor(output_details[0]['index'])[0].tolist()
    raw_titles = interpreter.get_tensor(output_details[1]['index'])
    titles = [title.decode("utf-8") for title in raw_titles[0]]
    # Get paper details
    paper_details = await get_paper_details_with_titles(
        titles=titles[:num_candidate]
    )
    # Return the results
    ret = {
        "scores": scores,
        "papers": paper_details
    }

    return ret
