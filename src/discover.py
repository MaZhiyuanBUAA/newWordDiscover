#coding:utf-8
import cPickle
import math
import re

LEAST_COUNT_THRESHOLD = 2
SOLIDE_RATE_THRESHOLD = 0.018
ENTROPY_THRESHOLD = 1.92
structuralLetters = ['我', '你', '您', '他', '她', '谁','哪', '那', '这', '的', '了', '着', '也', '是', '有', '不', '在', '与', '呢','啊', '呀', '吧', '嗯', '哦', '哈', '呐' ]
STRUCTURALLETTERSDIC = dict([(ele.decode('utf-8'),1) for ele in structuralLetters])
MAX_SIZE_WORD_EVALUATED = 1000000
class newWordDiscover():
    def __init__(self,docPath):
        f = file(docPath)
        tmp = f.read().decode('utf-8')
        self.doc = re.sub(u'[^\u4e00-\u9fa5]','*',tmp)
        self.docLength = len(self.doc)
        f.close()
        self.posVec = {}
        self.newWordList = {}
        self.minlen = 2
        self.maxlen = 5
        self.wordEvaluated = {}
        self.commenDic = {}    

    def readdic(self,dictPath):
        f = file(dictPath)
        words = f.readlines()
        f.close()
        self.commenDic = dict([(ele.strip().decode('utf-8'),1) for ele in words])

    def _buildPosVec(self):
        for ind, ele in enumerate(self.doc):
            try:
                self.posVec[ele].append(ind)
            except:
                self.posVec[ele] = [ind]

    def _updateWordEvaluated(self):
        l = len(self.wordEvaluated)
        if l < MAX_SIZE_WORD_EVALUATED:
            return
        else:
            tmp = []
            for ele in self.wordEvaluated.items():
                if ele[1] > 1:
                    tmp.append(ele)
            self.wordEvaluated = dict(tmp)
            print 'WordEvaluated updated,size:%d ----> %d'%(l,len(self.wordEvaluated))
            print 'NewDictSize:%d'%len(self.newWordList)

    def evaluate(self,candidate):
        candidateLen = len(candidate)
        def _getEntropy():
            frontList, backList = [], []
            pos_front = [ele-1 for ele in self.posVec[candidate[0]]]
            for pos in pos_front:
                if self.doc[pos+1:pos+1+candidateLen] == candidate:
                    frontList.append(self.doc[pos])
            pos_back = [ele+1 for ele in self.posVec[candidate[-1]]]
            for pos in pos_back:
                if self.doc[pos-candidateLen:pos] == candidate:
                    backList.append(self.doc[pos])
            frontEntropy, backEntropy = 0, 0
            for ele in list(set(frontList)):
                rate = 1.*frontList.count(ele)/len(frontList)
                frontEntropy -= rate * math.log(rate)
            for ele in list(set(backList)):
                rate = 1.*backList.count(ele)/len(backList)
                backEntropy -= rate * math.log(rate)
            return  frontEntropy if frontEntropy < backEntropy else backEntropy
            
        def _getSolideRate():
            count = self.doc.count(candidate)
            if candidateLen < 2:
                return 1
            if count < LEAST_COUNT_THRESHOLD:
                return 0
            rate = 1.0
            for c in candidate:
                rate *= 1. * count / len(self.posVec[c])
            return math.pow(rate, 1. / candidateLen) * math.sqrt(candidateLen)
        try:
            entropy = _getEntropy()
            soliderate = _getSolideRate()
        except:
            return (False,0.,0.)
        if (soliderate < SOLIDE_RATE_THRESHOLD) or (entropy < ENTROPY_THRESHOLD):
            return (False,soliderate,entropy)
        else:
            return (True,soliderate,entropy)
        
    def selector(self):
        self._buildPosVec()
        for i in range(self.docLength):
            for l in [self.minlen + j for j in range(self.maxlen-self.minlen+1)]:
                candidate = self.doc[i:i+l]
                if candidate.find('*')>-1:
                    continue
                try:
                    self.commenDic[candidate] += 0
                    continue
                except:
                    pass
                try:
                    STRUCTURALLETTERSDIC[candidate[0]] += 0
                    continue
                except:
                    pass
                try:
                    STRUCTURALLETTERSDIC[candidate[-1]] += 0
                    continue
                except:
                    pass
                try:
                    self.newWordList[candidate] += 0
                    continue 
                except:
                    pass
                self._updateWordEvaluated()
                try:
                    self.wordEvaluated[candidate] += 1 
                    continue
                except:
                    self.wordEvaluated[candidate] = 1
                value = self.evaluate(candidate)
                if value[0]:
                    self.newWordList[candidate] = 1
                    print candidate.encode('utf-8'),value[1],value[2]
        f = file('../tmp/newWordList.txt','w')
        f.write('\n'.join(self.newWordList.keys()))
        f.close()
        
    
if __name__ == '__main__':
    docPath = '../data/text.dat'
    dicPath = '../data/commen.dic'
    worker = newWordDiscover(docPath)
    #worker.readdic(dicPath)
    worker.selector()
    
