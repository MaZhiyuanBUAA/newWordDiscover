#coding:utf-8

DOCPATH = '../data/text.dat'
DICPATH = '../data/common.dic'
LEAST_COUNT_THRESHOLD = 2
SOLIDE_RATE_THRESHOLD = 0.018
ENTROPY_THRESHOLD = 1.92
structuralLetters = ['我', '你', '您', '他', '她', '谁','哪', '那', '这', '的', '了', '着', '也', '是', '有', '不', '在', '与', '呢','啊', '呀', '吧', '嗯', '哦', '哈', '呐' ]
STRUCTURALLETTERSDIC = dict([(ele.decode('utf-8'),1) for ele in structuralLetters])
MAX_SIZE_WORD_EVALUATED = 500000
MIN_LENGTH = 2
MAX_LENGTH = 5
