#importing library
from abc import ABCMeta, abstractmethod
from six import add_metaclass
from collections import namedtuple
from utils import *
from api import ArmTokenizerBase
from punct import Punct
import re
import math
#Class Defination
class Tokenizer(ArmTokenizerBase):
	
	PURIFICATION_RULES = [
		('–', '—'),
		('-', '—'),
		('<<', '«'),
		('>>', '»'),
		('(?P<w_beg>[ա-ֆԱ-Ֆևև]+)(?P<symbol>[' + Punct.all(linear=False) + ']){1}(?P<w_end>[ա-ֆԱ-Ֆևև]*)', '\g<w_beg>\g<w_end>\g<symbol>'), #LINEAR_PUNCTUATION
		('(?P<day>[0-9]{1,4})(?P<symbol1>[' + Punct(['storaket', 'hyphen', 'slesh']).regex() + '])(?P<month>[0-9]{1,4})(?P<symbol2>[' + Punct(['storaket', 'hyphen', 'slesh']).regex() + '])(?P<year>[0-9]{1,4})',
		  '\g<day> \g<symbol1> \g<month> \g<symbol2> \g<year>'), #Ամսաթվեր 20.12.2015
		]
	SEGMENTATION_RULES = [
	(1, u'[^(http(s)?)(\d+)](' + Punct('verjaket').regex() + '|[\?!]'+')\s*.*?', 1), # ([:?!] Ա) but it's not segment times(2:30) and URL(http//:) 
	(2, u'(' + Punct('4bazmaket').regex() + ')\s*.*?', 4), #.... Ա   
	(3, u'(' + Punct('3bazmaket').regex() + ')\s*.*?', 3), #... Ա    
	(4, u'(' + Punct('4bazmaket').regex() + ')\s*$', 4), #....
	(5, u'(' + Punct('3bazmaket').regex() + ')\s*$', 3), #...
	(6, u'(' + Punct('verjaket').regex() + ')\s*$', 1), #:
	(7, u'[' + Punct.all() + ']\s*[' + Punct('b_chakert').regex() + ']{1}\s*.*?', 1), #. <<
	(8, u'\.{1}\n', 1),
		]
	
	TOKENIZATION_RULES = [
	#TODO
	(1, inter_measures()),
	(2, double_measures()),
	(3, time()),
	(4, date()),
	(5.1, float_numbers(without_first=False)),
	(5.2, float_numbers(without_first=True)),
	(6.1, postfix_1()),
	(6.2, postfix_2()),
	(6.3, postfix_3()),
	(21., numbers()),
	(7,   email()),
	(8,   hashtags()),
	(9,   special_names('./special_names.txt')),
	(10,  abbrivations('./abbrivations.txt')),
	(11,  urls()),
	(12,  english_word()),
	(13,  arm_postfix_word()),
	(14,  arm_non_linear_word()),
	(8.1, single_measures_with_postfix()),
	(15,  single_measures()), 

	(16,  armenian_word()),
	(17,  russian_word()),
	(18,  dots()),
	(19,  all_linear_puncts()),
	(20,  all_non_linear_puncts())]

	# (1,  u'[' + Punct.inter() + ']'), # 5°С, $5, -5, +5
	# (2,  Punct.metric(double=True)), # 5կմ/ժ, 5մ/վ
	# (3,  u'[0-2]?[0-9]:[0-5]?[0-9]'), #times, e.g. 5:23'
	# (3.1,u'\d+[\.|,|/]{1}\d+[\.|,|/]{1}\d+'), #date, e.g.10.16.2000 
	# (4,  u'[0-9]+[\.,/]{1}[0-9]+'), #numbers 2.5 2,5 2/3
	# (4.1,u'[\.,][0-9]+'), #numbers .5 , .08
	# (4.2,u'[0-9]+' + '(' + Punct('gtcik').regex() + ')' + '[0-9]+'+ '(' + Punct('gtcik').regex() + ')?' +'([ա-ֆԱ-Ֆևև]+)?' ), # 2-3-րդ
	# (5.1, u'[ա-ֆԱ-Ֆևa-z]'+ '(' + Punct('gtcik').regex() + ')' + '[0-9]+' ), #Դ-30
	# (5.2, u'[0-9]+'+'((' + Punct('gtcik').regex() + ')'+'[ա-ֆԱ-Ֆևև]+)?'), #1-ին , 5-ական
	# (6, u'([a-zA-Z0-9_.+'+ Punct('gtcik').regex() +']+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)'), #E-mail
	# (7, u'[@,#][ա-ֆԱ-Ֆևa-z0-9_-]{3,}'), # @nickname , #hashtag 
	# (16.0, u'մեկ' + '(' + Punct('gtcik').regex() + ')' + 'երկու'), #special-names
	# (16.1, u'Սայաթ' + '(' + Punct('gtcik').regex() + ')' + 'Նովա'),
	# #.
	# #.
	# #.
	# (17, u'[a-zA-Z0-9-_]+\.[\.a-zA-Z]*'), # news.am
	# (17.1, u'(http(s)?:)//([a-zA-Z0-9\.\/$@-_&+:%\?=])*'),#(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%,[0-9a-fA-F][0-9a-fA-F]))+'), #URL
	# (18, u'[a-zA-Z]+'), #english word
	# (19, u'[Ա-Ֆևа-яА-ЯЁёA-Za-z]+'+ '(' + Punct('gtcik').regex() + ')' +'[ա-ֆև]+'), #ՀՀԿ-ական 
	# (20, u'[ա-ֆԱ-Ֆևև]+[' + Punct.all(linear=False) + ']{1,3}'), #հեյ~(հե~յ)
	# (2.1, u'(' + Punct.metric(double=False)+ ')'+'([' + Punct('gtcik').regex() + ']){1}' +'[ա-ֆև]+') ,# 5կմ, 5մ
	# (21, u'[ա-ֆԱ-Ֆևև]+'), #simple word
	# (22, u'[а-яА-ЯЁё]+'), #russian word
	# (23, u'\.{3,4}'), #.... , ...
	
	# (24, u'([' + Punct.all() + ']{1})'), #all punctuations
	# (25, u'([' + Punct.all(linear=False) + ']{1})'), #all non linear punctuations

  
	SPECIAL_RULES = {
	'segment': [
	  ( '__all__', False, u'[' + Punct('b_chakert').regex() + ']\s*[ա-ֆԱ-ՖևA-Za-zА-Яа-яёЁ]{1}[ա-ֆԱ-ՖևA-Za-zА-Яа-яёЁ\s։]+[^' + Punct('p_chakert').regex() + ']$' ), #<<bla bla: bla>> is not a segment
	],
	'token': []
  }
	MULTIWORD_TOKENS = [
	{
	  'regex': u'^[ա-ֆԱ-Ֆևև]+[' + Punct.all(linear=False) + ']{1,3}$',
	  'seperator': [ u'[ա-ֆԱ-Ֆևև]+', u'[' + Punct.all(linear=False) + ']{1}' ],
	}, # հեյ~ => 1-2.հեյ~ 1.հեյ 2.~
	]
	
	def __init__(self, sent=None):
		self.text = sent
		self.length = len(sent) if sent is not None else 0
		self.segments = []
		
	def cleaning(self):
		for r in self.PURIFICATION_RULES:
			self.text = re.sub(r[0], r[1], self.text)
		self.text =  re.sub('[\s\t\n]+', ' ',self.text).rstrip()#double spaces

		self.length = len(self.text)
		return self
	
	def __str__(self):
		return self.print_()
	
	def print_(self):
		output = ''
		for s in self.segments:
			output += '{num}. {string}\n{line}\n'.format(num=s['id'], string=s['segment'], line='-' * 50)
			for t in s['tokens']:
				output += '{token}\n'.format(token=t)
		  
			output += '\n'
		return output
	
	@classmethod
	def is_segment(cls, text, pointer):
		for index, r, len in cls.SEGMENTATION_RULES:
			if re.match(r, text[pointer:]):
				for s_r in cls.SPECIAL_RULES['segment']:
					if (isinstance(s_r[0], list) and index in s_r[0] ) or s_r[0] == '__all__':
						if not (( re.findall(s_r[2], text[:pointer]) and s_r[1] ) or ( not re.findall(s_r[2], text[:pointer]) and not s_r[1] )):
							return False
					return [r, len]
			return False
		
	@classmethod
	def find_token(cls, text, pointer,verbose = False):
		for index, r in cls.TOKENIZATION_RULES:
			token = re.match(r, text[pointer:])
			if token:
				for t_r in cls.SPECIAL_RULES['token']:
					if (isinstance(t_r[0], list) and index in t_r[0] ) or t_r[0] == '__all__':
						if not (( re.findall(t_r[2], text[:pointer]) and t_r[1] ) or ( not re.findall(t_r[2], text[:pointer]) and not t_r[1] )):
							return False
				if verbose:
					print(token,index)
				return token
				
		return False
	
	@classmethod
	def multitoken(cls, initial_token):
		word = initial_token
		for r in cls.MULTIWORD_TOKENS:
			token = re.match(r['regex'], word)
			if token:
				multitoken = []
				for s in r['seperator']:
					split_part = re.match(s, word)
					if split_part:
						multitoken.append(split_part.group(0))
						word = word[split_part.end():]
				return multitoken
		return False
	
	@overrides(ArmTokenizerBase)
	def segmentize(self,s = None):

		self.cleaning()
		checkpoint ,l = 0,0
		while(l < self.length):
			seg = self.is_segment(self.text[checkpoint:], l-checkpoint)
			if seg:
				punct_len = seg[-1]
				new_segment = self.text[checkpoint:(l + punct_len+1)]
				clean_segment = new_segment.rstrip().lstrip()
				self.segments.append({
					  'segment': clean_segment,
						  'id': len(self.segments)+1,
						  'tokens': []
						})
		
				checkpoint = l + punct_len+1
				l += punct_len+1
			else:
				l+=1
		
		new_segment = self.text[checkpoint:]
		clean_segment = new_segment.rstrip().lstrip()
		if clean_segment:
			self.segments.append({
						  'segment': clean_segment,
						  'id': len(self.segments)+1,
						  'tokens': []
						})

		return self
	
	def tokens(self):
		return [token[1] for seg in self.segments for token in seg['tokens'] if isinstance(token[0],int)]
		
	
	@overrides(ArmTokenizerBase)
	def tokenize(self, s,verbose=False):
		self.__init__(s)
		self.segmentize()
		for s in self.segments:
			l = 0
			index = 1
	  
			while l < len(s['segment']):
				token = self.find_token(s['segment'], l, verbose)
				if token:
					l += token.end()
					new_token = token.group(0)
					clean_token = new_token.rstrip().lstrip()
					multi = self.multitoken(clean_token)
					if multi:
						start_p = index
						end_p = start_p + len(multi) - 1
						s['tokens'].append( ('{s}-{e}'.format(s=start_p, e=end_p), clean_token) )
						for t in multi:
							s['tokens'].append( (index, t) )
							index += 1
					else:
						s['tokens'].append(( index, clean_token ))
						index += 1
				else:
					l += 1
		return self
