# -*- coding: utf-8 -*-

import tensorflow as tf
import numpy as np

from transformer.model import transformer
from transformer.data import DataProcess


MAX_LENGTH = 50

NUM_LAYERS = 2
UNITS = 512
D_MODEL = 256
NUM_HEADS = 8
DROPOUT= 0.1

dp = DataProcess()

model = transformer(
      vocab_size=dp.vocab_len
    , num_layers=NUM_LAYERS
    , units=UNITS
    , d_model=D_MODEL
    , num_heads=NUM_HEADS
    , dropout=DROPOUT
)

model.load_weights('./transformer/transformer_weights_10.h5')


def evaluate(sentence):
    sentence = dp.prepocess_sentence(sentence)
    sentence = [dp.STD_IDX] + dp.encoder(sentence) + [dp.END_IDX]
    sentence = tf.expand_dims(sentence, axis=0)
    
    output = tf.expand_dims([dp.STD_IDX], axis=0)
    for i in range(MAX_LENGTH):
        predictions = model(
              inputs=[sentence, output]
            , training=False
        )
        
        predictions = predictions[:, -1:, :]
        predicted_id = tf.cast(
              tf.argmax(predictions, axis=-1)
            , tf.int32
        )

        if tf.equal(predicted_id, dp.END_IDX):
            break

        output = tf.concat([output, predicted_id], axis=-1)
    
    return tf.squeeze(output, axis=0)


def predict(sentence):
    prediction = evaluate(sentence)
    
    predicted_sentence = ' '.join([
        dp.idx2word[word_idx]
        for word_idx in np.array(prediction)[1:]
    ])
    
    return predicted_sentence