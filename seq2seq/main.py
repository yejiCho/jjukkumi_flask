# from seq2seq.model import Seq2seq
# # from seq2seq.model import Seq2seq
# from seq2seq.data import DataProcess
# from seq2seq.spacing import sentence_spacing
from seq2seq.model import Seq2seq
from seq2seq.data import DataProcess
from seq2seq.spacing import sentence_spacing


def run(user_question, seq2seq = Seq2seq(), proc = DataProcess()):
    pro_sent = proc.prepocess_sentence(user_question)
    txt_to_idx = seq2seq.convert_text_to_index(pro_sent, proc.word2idx)
    pred = seq2seq.predict_model()
    sentence = seq2seq.idx_to_sentence(txt_to_idx, pred)
    return sentence_spacing(sentence)