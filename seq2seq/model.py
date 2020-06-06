from seq2seq.data import DataProcess
from keras.models import load_model
from keras.models import Model, Input
# from seq2seq.data import DataProcess
# from keras.models import load_model
# from keras.models import Model, Input
import numpy as np

class Seq2seq:
    def __init__(self, process=DataProcess()):
        self.model = load_model('./seq2seq/seq2seq_keras.h5')
        self.process = process
        self.PAD_INDEX = 0
        self.STA_INDEX = 1
        self.END_INDEX = 2
        self.UNK_INDEX = 3
        self.max_sequences = 60
        self.ENCODER_INPUT = 0

    def convert_text_to_index(self, sentence, vocabulary):
        """

        :param sentence: DataProcess의 prepocess_sentence를 통해 전처리된 텍스트 문장
        :param vocabulary: DataProcess의 word2idx
        :return:[[num,num,num,...]] 형태의 ndarray
        """
        PAD = "<PADDING>"  # 패딩
        UNK = "<UNK>"  # 없는 단어

        sentence_index = []
        for word in sentence.split(' '):
            if vocabulary.get(word) is not None:
                sentence_index.append(vocabulary[word])
            else:
                sentence_index.append(vocabulary[UNK])
        # max_sequences 길이로 자름
        if len(sentence_index) > self.max_sequences:
            sentence_index = sentence_index[:self.max_sequences]
        # max_sequences 보다 길이가 작으면 나머지 부분을 max_sequences 만큼 padding
        sentence_index += (self.max_sequences - len(sentence_index)) * [vocabulary[PAD]]
        sentence_index = [sentence_index]
        return np.asarray(sentence_index, dtype='uint16')

    def convert_index_to_text(self, indices, vocabulary):
        """

        :param indices: 예측 모델을 통해 생성된 index가 들어있는 리스트
        :param vocabulary: index를 단어로 바꿔주는 단어사전
        :return: 단어를 공백없이 이은 문장
        """
        sentence = ''
        for index in indices:
            if index == self.END_INDEX:
                break
            if vocabulary.get(index) is not None:
                sentence += vocabulary[index]
            else:
                sentence += vocabulary[self.UNK_INDEX]
            # sentence += ' '
        return sentence

    def predict_model(self):
        """
        훈련된 모델의 labeling된 layer들을 가져와
        1. 훈련된 모델의 데이터 사용
        2. 예측 모델의 layer와 형식을 맞춰줌
        :return: 예측에 사용할 encoder_model과 decoder_model
        """
        encoder_input_model = self.model.get_layer('encoder_input').input
        decoder_input_model = self.model.get_layer('decoder_input').input
        encoder_embedding_layer = self.model.get_layer('encoder_embedding')
        decoder_embedding_layer = self.model.get_layer('decoder_embedding')
        encoder_LSTM_layer = self.model.get_layer('encoder_LSTM')
        decoder_LSTM_layer = self.model.get_layer('decoder_LSTM')
        decoder_wrapper_layer = self.model.get_layer('decoder_wrapper')

        lstm_hidden_dim = 128

        encoder_inputs = encoder_input_model
        encoder_outputs = encoder_embedding_layer(encoder_inputs)
        encoder_outputs, state_h, state_c = encoder_LSTM_layer(encoder_outputs)
        encoder_states = [state_h, state_c]
        encoder_model = Model(encoder_inputs, encoder_states)

        decoder_inputs = decoder_input_model

        decoder_state_input_h = Input(shape=(lstm_hidden_dim,))
        decoder_state_input_c = Input(shape=(lstm_hidden_dim,))
        decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]

        decoder_outputs = decoder_embedding_layer(decoder_inputs)

        decoder_outputs, state_h, state_c = decoder_LSTM_layer(decoder_outputs,
                                                               initial_state=decoder_states_inputs)
        decoder_states = [state_h, state_c]
        decoder_dense = decoder_wrapper_layer
        decoder_outputs = decoder_dense(decoder_outputs)

        decoder_model = Model([decoder_inputs] + decoder_states_inputs,
                              [decoder_outputs] + decoder_states)
        predicted_model=(encoder_model, decoder_model)
        return predicted_model

    def idx_to_sentence(self, input_seq, pred):
        """

        :param input_seq: convert_text_to_index()의 return값
        :param pred:
            예측에 사용할 encoder_model과 decoder_model을 튜플로 묶은 것
            default : predict_model()의 리턴값
        :return:
        """
        encoder_model, decoder_model = pred
        states = encoder_model.predict(input_seq)  # [(1, 128), (1, 128)]
        target_seq = np.zeros((1, 1))
        target_seq[0, 0] = self.STA_INDEX
        indices = []
        while 1:
            decoder_outputs, state_h, state_c = decoder_model.predict(
                [target_seq] + states # ndarray가 3개 들어있는 list
            )
            # decoder_outputs의 shape : (1, 1, 26208)
            index = np.argmax(decoder_outputs[0, 0, :])
            # 이전 예측값이 다시 model로 들어가 다음값을 예측하면서
            # indices의 원소 개수가 점점 늘어남
            indices.append(index)
            if index == self.END_INDEX or len(indices) >= self.max_sequences:
                break
            # target_seq을 이전 index로 초기화
            target_seq = np.zeros((1, 1))
            target_seq[0, 0] = index
            states = [state_h, state_c]
        sentence = self.convert_index_to_text(indices, self.process.idx2word)
        return sentence

