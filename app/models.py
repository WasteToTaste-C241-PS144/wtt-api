import tensorflow as tf

model_path = './dist/cnn_model.h5'

model = tf.keras.models.load_model(model_path)