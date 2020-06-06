import re
from konlpy.tag import Mecab

"""
[한국어 단어의 품사는 9개]
    -> 명사, 대명사, 수사, 동사, 형용사, 관형사, 부사, 감탄사, 조사

[띄어쓰기의 원칙]
1. 조사를 제외한 나머지 8개 품사는 모두 띄어쓴다
2. 한 글자짜리 관형사/부사를 붙여쓰지 않는다.
3. 조사는 몇 개가 되든 붙여쓴다.

[함수에 적용한 것들]
1. 조사는 모두 붙여쓸거임('^J')
2. 테스트 결과 어미('^E')도 모두 붙여써야함
3. 의존명사('NNB', 'NNBC')는 띄어써야함
4. 긍정지정사('VCP'), 부정지정사('VNP')는 붙여써야함
5. 접미사는('^XS) 붙여쓴다
6. 접두사는 앞에 붙여쓴다.
7. 숫자와 단위는 띄어쓴다.
8. 부호('^S')는 붙여쓴다.

"""

def sentence_spacing(pre_sentence : str)->str:
    """

    :param pre_sentence: 띄어쓰기 없이 이어붙인 문장
    :return: 띄어쓰기가 된 문장
    """
    m = Mecab()
    pattern = re.compile('^J|E|SE|SF|SSO|SSC|SC|SY|VC|VN|XS')
    word_morph = m.pos(pre_sentence)
    sentence = word_morph[0][0]

    for word, morph in word_morph[1:]:
        if re.match(pattern, morph):
            sentence += word
        else:
            sentence += ' ' + word
    return sentence