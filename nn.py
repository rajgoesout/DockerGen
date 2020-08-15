import math
from keras.models import Sequential
from keras.layers import Dense
import tensorflow as tf
import numpy as np

x_train = np.array([
    [],
    [],
    [],
    [],
    [],
    []
])
y_train = np.array(['django','flask','go','nodejs','rust','scala'])

nn = Sequential()
nn.add(Dense(10, activation="relu", input_shape=(10,)))
nn.add(Dense(6))#6 labels (possible langs)

nn.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

nn.fit()

def sigmoid(z):
    return [1 / (1 + math.exp(-n)) for n in z]


def softmax(z):
    z_exp = [math.exp(i) for i in z]
    sum_z_exp = sum(z_exp)
    return [i / sum_z_exp for i in z_exp]

# model = tf.keras.Sequential([
#     # Add an Embedding layer expecting input vocab of size 5000, and output embedding dimension of size 64 we set at the top
#     tf.keras.layers.Embedding(vocab_size, embedding_dim),
#     tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(embedding_dim)),
# #    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(32)),
#     # use ReLU in place of tanh function since they are very good alternatives of each other.
#     tf.keras.layers.Dense(embedding_dim, activation='relu'),
#     # Add a Dense layer with 6 units and softmax activation.
#     # When we have multiple outputs, softmax convert outputs layers into a probability distribution.
#     tf.keras.layers.Dense(6, activation='softmax')
# ])
# model.summary()

z = [-1.0, 5.0, -0.5, 5.0, -0.5]
print(softmax(z))
