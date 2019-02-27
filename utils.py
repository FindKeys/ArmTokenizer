import re
from punct import Punct

#Help Functions
def overrides(interface_class):
	'''Protocol'''
	def overrider(method):
		if method.__name__  not in dir(interface_class):
			raise NotImplementedError("Override error: Protacol {}".format(interface_class.__name__))
		return method
	return overrider

def inter_measures(): 
	measures = Punct.inter()
	measures = '\\'+ measures[:4] + '\\' + measures[4:13] + '\\' + measures[13:]
	return r'{}'.format(measures)

def single_measures(): 
	pattern = r'|'.join(sorted(Punct.metric(double=False).split('|'),key=lambda x: len(x),reverse=True))
	return r'(?:\s|^|(?:[\s^]?[\+\-]?\d+?\.?\d*))(' + pattern + '){1}(?:\s|$|'+Punct('verjaket').regex()+')(?!\w|ա-ֆԱ-Ֆև)' 

def single_measures_with_postfix():
	pattern = r'|'.join(sorted(Punct.metric(double=False).split('|'),key=lambda x: len(x),reverse=True))
	return r'(?:\s|^|(?:[\s^]?[\+\-]?\d+?\.?\d*))(' + pattern + '){1}'+'([' + Punct('gtcik').regex() +  '|-]{1}' +'[ա-ֆև]+)'

def date(): 
	# dd mm yyyy
	return r'(?:^|\s|\-|'+Punct('gtcik').regex()+')(\d{1,2}(?:\.|/|,){1}\d{1,2}(?:\.|/|,){1}\d{4})'

def postfix_1(): 
	dash = Punct('gtcik').regex() + '|-'
	return r'{}'.format('(\d+(?:' + dash + ')\d+(?:' + dash + ')?(?:[ա-ֆԱ-Ֆևև]+)?)')

def postfix_2(): 
	dash = Punct('gtcik').regex() + '|-'
	return r'{}'.format('([ա-ֆԱ-Ֆևa-zA-Zа-яА-ЯЁё]+(?:' + dash + ')\d+)')

def numbers():
	return r'\d+'

def postfix_3(): 
	dash = Punct('gtcik').regex() + '|-'
	return r'(?:\s|^)(\d+(?:'+ dash + ')'+'[ա-ֆԱ-Ֆևև]+)'



def urls(): 
	return r'{}'.format('((?:https?:\/\/(?:www\.)?[\w@\.\?%&\-_\/\+:=!]+(?:\.[a-zA-Z]+)?)|(?:(?:www\.)[\w@\.\?%&\-_\/\+:=!]+\.(?:[a-zA-Z]+){2,})|(?:[\w@\.\?%&\-_\/\+:=!]+\.(?:[a-zA-Z]+){2,}))')

def english_word():
	#dash = (Punct('gtcik').regex() + '-').replace('|','')
	appo = (Punct('apostrophe').regex()+"'").replace('|','')
	#return r'{}'.format('([a-zA-Z' +dash+']+)')
	return r'{}'.format('([a-zA-Z' +appo+']+)')


def arm_postfix_word(): 
	dash = (Punct('gtcik').regex() + '|-')#.replace('|','')
	return r'([Ա-Ֆևа-яА-ЯЁёA-Za-z]+'+ '(?:' + dash + ')' +'[ա-ֆԱ-Ֆև]+)'

def russian_word(): 
	dash = (Punct('gtcik').regex() + '-').replace('|','')
	return r'{}'.format('[а-яА-ЯЁё' + dash + ']+')               

def all_linear_puncts(): 
	return r'{}'.format('([' + Punct.all() + ']{1})')

def double_measures():
   	pattern = r'|'.join(sorted(Punct.metric(double=True).split('|'),key=lambda x: len(x),reverse=True))
    	return r'(?:\s|^||\s(?:\d+?\.?\d*))(' + pattern + ')(?!\w|ա-ֆԱ-Ֆև)'

def time():
	return r'([0-2]?\d:[0-5]?\d)(?!\w|ա-ֆԱ-Ֆև)'

def float_numbers(without_first=False):
	if without_first == False:
		return r'(\d+[\.,/]{1}\d+)'
	return r'([\.,]\d+)'

def email():
   	return r'([a-zA-Z0-9][a-zA-Z0-9_.'+ Punct('gtcik').regex() +']+@[a-zA-Z0-9-]+\.[a-zA-Z0]{2,3}(?!\w|ա-ֆԱ-Ֆև))'

def hashtags():
	return r'(?:^| )([@#][ա-ֆԱ-Ֆևa-zA-Z0-9а-яА-ЯЁё'+Punct('gtcik').regex()+']+)'

def armenian_word():
	return r'([ա-ֆԱ-Ֆև]+)'

def arm_non_linear_word():
	return r'([ա-ֆԱ-Ֆև]+[' + Punct.all(linear=False) + ']{1,3})(?!\w|ա-ֆԱ-Ֆև)'

def dots():
	return r'(\.{3,4})'

def all_non_linear_puncts():
	return r'([' + Punct.all(linear=False) + ']{1})'

def special_names(vocab_path):
	with open(vocab_path,'r') as txt:
		vocab = txt.read().split('\n')
	gtcikner = set((Punct('gtcik').regex()+'|-').replace('|',''))
	new_vocab = []
	for i,word in enumerate(vocab):
		inter = gtcikner & set(word)
		if inter:
			for ch in inter:
				new_ = word.replace(ch,"(?:"+Punct('gtcik').regex()+'|-'+")")
				new_vocab.append(new_)
		else:
			new_vocab.append(word)

	r = r'|'.join([r'(?:{})'.format(special_word) for special_word in set(new_vocab)])
	return '('+r+')'

def abbrivations(abbr_path):
	with open(abbr_path,'r') as txt:
		vocab = txt.read().split('\n')

	r = r'|'.join([r'({})'.format(abbr) for abbr in vocab])
	return r
