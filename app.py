"""
the entry & exit point to our application
"""
# Packages for training the model and working with the dataset.
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import json
# Utility/helper packages.
import platform
import time
import pathlib
import os

checkpoint_dir = 'checkpoints'

tf.train.latest_checkpoint(checkpoint_dir)

VOCABULARY_SIZE = 93
MAX_QUOTE_LENGTH = 300
BATCH_SIZE = 64

def build_model(vocab_size, embedding_dim, rnn_units, batch_size):
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Embedding(
        input_dim=vocab_size,
        output_dim=embedding_dim,
        batch_input_shape=[batch_size, None]
    ))
    model.add(tf.keras.layers.LSTM(
        units=rnn_units,
        return_sequences=True,
        stateful=True,
        recurrent_initializer=tf.keras.initializers.GlorotNormal()
    ))
    model.add(tf.keras.layers.Dense(vocab_size))

    return model


model = build_model(
    vocab_size=VOCABULARY_SIZE,
    embedding_dim=256,
    rnn_units=1024,
    batch_size=BATCH_SIZE
)

simplified_batch_size = 1
model_simplified = build_model(
    vocab_size=VOCABULARY_SIZE,
    embedding_dim=256,
    rnn_units=1024,
    batch_size=simplified_batch_size
)
model_simplified.load_weights(tf.train.latest_checkpoint(checkpoint_dir))
model_simplified.build(tf.TensorShape([simplified_batch_size, None]))
model_simplified.summary()

STOP_WORD_QUOTE = '💭 '
STOP_WORD_AUTHOR = '\n👨\n\n'

import pickle
# loading
with open('tokenizer/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

def generate_text(model, start_string, num_generate=1000, temperature=1.0):
    # Evaluation step (generating text using the learned model)

    padded_start_string = STOP_WORD_QUOTE + start_string
    # Converting our start string to numbers (vectorizing).
    input_indices = np.array(
        tokenizer.texts_to_sequences([padded_start_string]))
    # Empty string to store our results.
    text_generated = []
    # Here batch size == 1.
    model.reset_states()
    for char_index in range(num_generate):
        predictions = model(input_indices)
        # remove the batch dimension
        predictions = tf.squeeze(predictions, 0)
        # Using a categorical distribution to predict the character returned by the model.
        predictions = predictions / temperature
        predicted_id = tf.random.categorical(
            predictions,
            num_samples=1
        )[-1, 0].numpy()
        # We pass the predicted character as the next input to the model
        # along with the previous hidden state.
        input_indices = tf.expand_dims([predicted_id], 0)

        next_character = tokenizer.sequences_to_texts(input_indices.numpy())[0]
        text_generated.append(next_character)
    return (padded_start_string + ''.join(text_generated))


from flask import Flask, request

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/", methods=["GET", "POST"])
def adder_page():
    errors = ""
    if request.method == "POST":
        seed = None
        temperature = None
        words = None
        seed = request.form["seed"]
        try:
            temperature = float(request.form["temperature"])
            if temperature > 1.5 or temperature < 0:
                errors += "<p>Please enter a float between 0 and 1.5 for temperature.</p>\n".format(
                request.form["temperature"])
                temperature = None
        except:
            errors += "<p>{!r} is not a number.</p>\n".format(
                request.form["temperature"])
        try:
            words = float(request.form["words"])
            if words > 100000 or words < 0:
                errors += "<p>Please enter a float between 0 and 100000 for quote length.</p>\n".format(
                request.form["words"])
                words = None
        except:
            errors += "<p>{!r} is not a number.</p>\n".format(
                request.form["words"])

        if seed is not None and temperature is not None and words is not None:
            #result = seed
            result = generate_text(model=model_simplified, start_string=seed,
                                   num_generate=int(words)+len(seed), temperature=temperature)
            result = result.replace("␣", "")
            return '''
                <html>
                    <body style="background-color:skyblue;">
                    <center>
                        <p><font size="5">The result is {result}</font></p>
                        <p><font size="5"><a href="/">Click here to generate again</font></a>
                    </center>
                    </body>
                </html>
            '''.format(result=result)

    return '''
        <html>
            <body style="background-color:skyblue;">
            <center>
                {errors}
                <h1><font size="24">Quote Generator</font></h1>
                <p><font size="5">Enter your starting string:</font></p>
                <form method="post" action=".">
                    <p><input name="seed" /></p>
                <p><font size="5">Enter your temperature:</font></p>
                    <p><input name="temperature" /></p>
                <p><font size="5">Enter your quote length:</font></p>
                    <p><input name="words" /></p>
                    <p><input type="submit" value="Generate quote" /></p>
                </form>
            </center>
            </body>
        </html>
    '''.format(errors=errors)
