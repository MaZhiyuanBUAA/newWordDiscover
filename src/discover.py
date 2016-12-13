#coding:utf-8
import cPickle
import math
import re, time
from conf import LEAST_COUNT_THRESHOLD,SOLIDE_RATE_THRESHOLD,ENTROPY_THRESHOLD,STRUCTURALLETTERSDIC,MAX_SIZE_WORD_EVALUATED,MIN_LENGTH,MAX_LENGTH
from utils import readData

class newWordDiscover():
	def __init__(self):
		self.doc = ''
		self.docLength = 0
		self.posVec = {}
		self.newWordList = {}
		self.minlen = MIN_LENGTH
		self.maxlen = MAX_LENGTH
		self.wordEvaluated = {}
		self.commonDic = {}
		self.name = 'Ant0'
		self.valuesOfCommonDic = []

	def dataSet(self,doc,dic):
		self.doc = doc
		self.commonDic = dic
		self.docLength = len(self.doc)
		for ind, ele in enumerate(self.doc):
			try:
				self.posVec[ele].append(ind)
			except:
				self.posVec[ele] = [ind]

	def giveName(self, name):
		self.name = name

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
			if candidateLen < 2:
				return 1
			least = 1e9
			for ind, ele in enumerate(candidate):
				l_tmp = len(self.posVec[ele])
				if least > l_tmp:
					least = l_tmp
					c_least = ele
					check_pos = ind
					check_list = self.posVec[ele]
			count = 0   
			for ind in check_list:
				start = ind-check_pos
				if self.doc[start:start+candidateLen] == candidate:
					count += 1
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
			return (0.,0.)
		return (soliderate,entropy)

	def threshold_ready(self):
		gap = len(self.commonDic)/100
		for ind, ele in enumerate(self.commonDic):
			self.valuesOfCommonDic.append(self.evaluate(ele))
			if ind%gap == 0:
				print ind*1./gap
	def threshold_analysis(self,solide,entropy):
		num = 0
		for value in self.valuesOfCommonDic:
			if value[0] >= solide and value[1] >= entropy:
				num += 1
		print 'RECALL is %f'%(num*1./len(self.commonDic))
		
	def parser(self):
		start_time = time.time()
		with open('../tmp/newWordList.txt','w') as f:
			for i in range(self.docLength):
				for l in [self.minlen + j for j in range(self.maxlen-self.minlen+1)]:
					candidate = self.doc[i:i+l]
					if candidate.find('*')>-1:
						continue
					try:
						self.commonDic[candidate] += 0
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
					if value[0] >= SOLIDE_RATE_THRESHOLD and value[1] >= ENTROPY_THRESHOLD:
						self.newWordList[candidate] = 1
						f.write(candidate.encode('utf-8')+'\n')
				#print '%s: %s'%(self.name,candidate.encode('utf-8'))
				if i%10000 == 0:
					print '%d,%f'%(i,time.time()-start_time)


if __name__ == '__main__':
	doc, dic = readData()
	worker = newWordDiscover()
	worker.dataSet(doc,dic)
	print worker.docLength
	worker.threshold_ready()
	worker.threshold_analysis(SOLIDE_RATE_THRESHOLD,ENTROPY_THRESHOLD)
	#worker.parser()

