# -*- coding: utf-8 -*-

from konlpy.tag import Mecab
import re
import os


class DataProcess:
    '''데이터 처리를 담당하는 클래스'''
    
    def __init__(self,
                 vocab_path="./transformer/vocbulary.voc",
                 tagger=Mecab()):
        # tagger: 형태소 분석기 -> Mecab() (default)
        self.tagger = tagger
        
        # 단어 사전 형태별 저장
        self.vocab, self.word2idx, \
        self.idx2word, self.vocab_len \
        = self._load_vocab_file(vocab_path)
        
        # start, end, unk 토큰 지정
        self.STD = "<START>"
        self.END = "<END>"
        self.UNK = "<UNK>"
        
        # start, end, unk 토큰 인덱스 번호
        self.STD_IDX = self.word2idx[self.STD]
        self.END_IDX = self.word2idx[self.END]
        self.UNK_IDX = self.word2idx[self.UNK]
    
    def _load_vocab_file(self, vocab_path):
        '''
        단어 사전 파일을 불러와서 네가지 형태의 단어 사전을 리턴
        DataProcess 오브젝트 생성시 즉시 실행
        
        param>>
            vocab_path -> 단어 사전 파일 경로
        
        return>>
            vocab_list -> 단어 리스트
            word2idx -> 단어: 인덱스
            idx2word -> 인덱스: 단어
            vocab_len -> 단어 사전 길이
        '''

        # 단어 사전이 없을 경우 에러 발생
        assert os.path.exists(vocab_path), "단어 사전이 존재하지 않습니다."

        with open(vocab_path, 'r', encoding='utf-8') as vocab_file:
            vocab_list = [line.strip() for line in vocab_file]

        word2idx = {word: idx for idx, word in enumerate(vocab_list)}
        idx2word = {idx: word for idx, word in enumerate(vocab_list)}

        return vocab_list, word2idx, idx2word, len(vocab_list)
    
    def prepocess_sentence(self, sentence):
        '''
        입력받은 문장을 전처리하고 형태소 분석을 하여 리턴
        최종적으로 공백으로 분리 후 문자열로 리턴
        '''
        sentence = re.sub("[^a-zA-Z가-힣0-9]", " ", sentence)    
        sentence = ','.join(self.tagger.morphs(sentence))
        sentence = re.sub("\s+", "", sentence)

        words = []
        for word in sentence.split(','):
            word = word if word in self.vocab else self.UNK
            words.append(word)

        sentence = ' '.join(words)

        return sentence
    
    def encoder(self, word_sentence):
        '''
        전처리된 텍스트 문자열을 단어 사전을 참조하여
        단어 인덱스 리스트로 리턴
        '''
        word_idxes = [
            self.word2idx[word]
            for word in word_sentence.split()
        ]
        
        return word_idxes        
    
    def decoder(self, idx_sentence):
        '''
        단어 인덱스 리스트를 문장으로 바꿔서 리
        '''
        idx_words = [
            self.idx2word[idx]
            for idx in idx_sentence
        ]
        
        sentence = ' '.join(idx_words)
        
        return sentence