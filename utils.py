import re
import punct as pu 

#Help Functions
def overrides(interface_class):
	'''Protocol'''
	def overrider(method):
		if method.__name__  not in dir(interface_class):
			raise NotImplementedError("Override error: Protacol {}".format(interface_class.__name__))
		return method
	return overrider


#TODO
def double_measures():
	pattern = r'|'.join(sorted(Punct.metric(double=True).split('|'),key=lambda x: len(x),reverse=True))
	return r'(?:\s|^|\s(?:\d+?\.?\d*))('+ pattern+ ')(?:\s|$)'

def time():
	return r'(?:^|\s)([0-2]?\d:[0-5]?\d)(?:\s|$)'

def float_numbers(without_first=False):
	if without_first == False:
		return r'(?:^|\s|\s[+-]{1})(\d+[\.,/]{1}\d+)(?:\s|$)'
	return r'(?:^|\s)([\.,]\d+)(?:\s|$)'

def email():
	return r'(?:\s|^)([a-zA-Z0-9][a-zA-Z0-9_.'+ Punct('gtcik').regex() +']+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)(?:\s|$)'

def hashtags():
	return r'(?:\s|^)([@,#][ա-ֆԱ-Ֆևa-zA-Z0-9а-яА-ЯЁё'+Punct('gtcik').regex()+'\.]+)(?:\s|$)'

def armenian_word():
	return r'(?:\s|^)([ա-ֆԱ-Ֆև]+)(?:\s|$)'

def arm_non_linear_word():
	return r'(?:\s|^)([ա-ֆԱ-Ֆև]+[' + Punct.all(linear=False) + ']{1,3})(?:\s|$)'

def  dots():
	return r'(?:\s|^)(\.{3,4})(?:\s|$)'

def all_non_linear_puncts():
	return r'([' + Punct.all(linear=False) + ']{1})'

def special_names(vocab_path):
	with open(vocab_path,'r') as txt:
		vocab = txt.read().split('\n')
	for special_word in vocab:
		if '-' in special_word:
			special_word = '(?:'+Punct('gtcik').regex()+r'|-)'.join(special_word.split('-'))
		yield r'(?:\s|^)({})(?:\s|$)'.format(special_word)

def abbrivations(abbr_path):
	with open(abbr_path,'r') as txt:
		vocab = txt.read().split('\n')
	for abbr in vocab:
		if '.' in abbr:
			abbr = '(?:'+Punct('mijaket').regex()+')'.join(abbr.split('.'))
		yield r'(?:\s|^)({})(?:\s|$)'.format(abbr)
