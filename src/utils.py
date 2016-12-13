#coding:utf-8
import re
import conf

def readData():
	f = file(conf.DICPATH)
	dic = f.readlines()
	f.close()
	f = file(conf.DOCPATH)
	text = f.read().decode('utf-8')
	f.close()
	dic = [ele.strip().decode('utf-8') for ele in dic]
	text = re.sub(u'[^\u4e00-\u9fa5]','*',text)
	return text, dic

