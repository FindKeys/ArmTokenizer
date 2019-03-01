import unittest
from utils import *
import re

class PatternTest(unittest.TestCase):
	'''
	use this methods for assertion
	self.assertEqual(a, b)			a == b
	self.assertTrue(x)				bool(x) is True
	self.assertFalse(x)				bool(x) is False
	self.assertIs(a, b)				a is b
	self.assertIsNone(x)			x is None
	self.assertIn(a, b)				a in b
	self.assertIsInstance(a, b)		isinstance(a, b)
	'''

	#Todo add pattens for !!! and emojies
	#Todo add special_names like van gog


	def test_inter_measures(self): 
		INTERNATIONAL = [ '+', '-', '?','!','%', '°С', '$', '€', '₩', '¥', '₦', '₽', '£' ]
		test1 = "+5 -5 why? offf! 100% 50°С 500$ "
		test2 = " +5 -5 why? offf! 100% 50°С 500$ "
		test3 = "+5.1 off!!! +4km/j"
		test4 = " 605°С-ից բարձր"
		test5 = " ehhhh1000$"
		compile = re.compile(inter_measures())
		res1 = re.findall(compile,test1)
		res2 = re.findall(compile,test2)
		res3 = re.findall(compile,test3)
		res4 = re.findall(compile,test4)
		res5 = re.findall(compile,test5)
		self.assertEqual(res1, ['+', '-', '?', '!', '%', '°С', '$'])
		self.assertEqual(res2, ['+', '-', '?', '!', '%', '°С', '$'])
		self.assertEqual(res3, ['+', '!', '!', '!', '+'])
		self.assertEqual(res4, ['°С','-'])
		self.assertEqual(res5, ['$'])


	def test_double_measures(self): 
		test1 = '100կմ/ժ,  60մ/վ  4.006գ/տ:'
		test2 = '  Մարդու  միջին  արագությունը  5կմ/ժ  է:'
		test3 = 'Ընդհամենը5կմ/ժ  ?  Ես  կարծում  էի  10մ/ժ :'
		test4 = '  7.9կմ/վէ  առաջին  տիեզերական  արագությունը :'
		compile = re.compile(double_measures())
		res1 = re.findall(compile,test1)
		res2 = re.findall(compile,test2)
		res3 = re.findall(compile,test3)
		res4 = re.findall(compile,test4)
		self.assertEqual(res1, ['կմ/ժ', 'մ/վ', 'գ/տ'])
		self.assertEqual(res2, ['կմ/ժ'])
		self.assertEqual(res3, ['կմ/ժ', 'մ/ժ'])
		self.assertEqual(res4, [])

	def test_single_measures(self): 
		METRIC = [ 'կմ', 'մ','սմ' , 'մմ', 'ժ', 'վ', 'ր', 'մվ', 'կգ', 'գ',  'մգ', 'տ' , 'ց','ք']
		test1 = "4մ բարձր  4սմ   բարձր   60վ   24ժ   60ր   10կգ   100ց։"
		test2 = "100-150կմ   100-150մմ"
		test3 = " +100սմ"
		compile = re.compile(single_measures())
		res1 = re.findall(compile,test1)
		res2 = re.findall(compile,test2)
		res3 = re.findall(compile,test3)
		self.assertEqual(res1, ['մ', 'սմ', 'վ', 'ժ', 'ր', 'կգ', 'ց'])
		self.assertEqual(res2, ['կմ','մմ'])
		self.assertEqual(res3, ['սմ'])

	def test_time(self): 
			test1 = '10:00  6: 24   8:14է'
			test2 = 'Ժամը  1:23  է:'
			test3 = 'Առավոտյան  20:00'
			compile = re.compile(time())
			res1 = re.findall(compile,test1)
			res2 = re.findall(compile,test2)
			res3 = re.findall(compile,test3)
			self.assertEqual(res1, ['10:00'])
			self.assertEqual(res2, ['1:23'])
			self.assertEqual(res3, ['20:00'])

	def test_date(self): 
		# 10.16.2000 10/16/2000 10,16,2000
		test1 = " 10.16.2000  10/16/2000  10,16,2000"
		test2 = " 10.16."
		test3 = " 10/16/2000թ.-ին"
		test4 = " 10.16.2000_10.16.2000թթ-ին"
		test5 = "10.16.2000-10.16.2000թթ-ին"
		compile = re.compile(date())
		res1 = re.findall(compile,test1)
		res2 = re.findall(compile,test2)
		res3 = re.findall(compile,test3)
		res4 = re.findall(compile,test4)
		res5 = re.findall(compile,test5)
		self.assertEqual(res1, ["10.16.2000","10/16/2000","10,16,2000"])
		self.assertEqual(res2, [])
		self.assertEqual(res3, ["10/16/2000"])
		self.assertEqual(res4, ["10.16.2000","10.16.2000"])
		self.assertEqual(res5, ["10.16.2000","10.16.2000"])

	def test_float_numbers(self,without_first=False): 
		test1 = '2.5  10,7  2/3'
		test2 = '5/2  կամ  2.5 :'
		compile = re.compile(float_numbers())
		res1 = re.findall(compile,test1)
		res2 = re.findall(compile,test2)
		self.assertEqual(res1, ['2.5', '10,7', '2/3'])
		self.assertEqual(res2, ['5/2', '2.5'])

	def test_postfix_1(self): 
		test1 = " 10-16-րդ"
		test2 = " 10-16-ից"
		test3 = " 2-3-րորդական պ"
		test4 = "4-5-ական  4-5-ական "
		compile = re.compile(postfix_1())
		res1 = re.findall(compile,test1)
		res2 = re.findall(compile,test2)
		res3 = re.findall(compile,test3)
		res4 = re.findall(compile,test4)
		self.assertEqual(res1, ['10-16-րդ'])
		self.assertEqual(res2, ['10-16-ից'])
		self.assertEqual(res3, ['2-3-րորդական'])
		self.assertEqual(res4, ['4-5-ական','4-5-ական'])

	def test_postfix_2(self): 
		test1 = " Դ-30  Դ-30"
		test2 = " Դավ-30"
		test3 = " Pushkini-24"
		test4 = " -24"
		compile = re.compile(postfix_2())
		res1 = re.findall(compile,test1)
		res2 = re.findall(compile,test2)
		res3 = re.findall(compile,test3)
		res4 = re.findall(compile,test4)
		self.assertEqual(res1, ['Դ-30','Դ-30'])
		self.assertEqual(res2, ['Դավ-30'])
		self.assertEqual(res3, ['Pushkini-24'])
		self.assertEqual(res4, [])

	def test_postfix_3(self): 
		test1 = "1-ին , 5-ական"
		test2 = "1-ին ,5-5"
		test3 = "6_ին 6անց կէս"
		test4 = "5-5-ական"
		compile = re.compile(postfix_3())
		res1 = re.findall(compile,test1)
		res2 = re.findall(compile,test2)
		res3 = re.findall(compile,test3)
		res4 = re.findall(compile,test4)
		self.assertEqual(res1, ["1-ին","5-ական"])
		self.assertEqual(res2, ["1-ին"])
		self.assertEqual(res3, ["6_ին"])
		self.assertEqual(res4, [])

	def test_email(self): 
		test1 = 'davitkar98@gmail.com   FindKeys@armmai.com'
		test2 = 'InvalidEmail.comasdasd'
		compile = re.compile(email())
		res1 = re.findall(compile,test1)
		res2 = re.findall(compile,test2)
		self.assertEqual(res1, ['davitkar98@gmail.com', 'FindKeys@armmai.com'])
		self.assertEqual(res2, [])

	def test_urls(self): 
		test1 = " [news.am]"
		test2 = " news.am   {news.am}"
		test3 = " news.am.com  (www.aca.am) "
		test4 = " (https://www.youtube.com/watch?v=iuJDhFRDx9M&list=RDMMiuJDhFRDx9M&start_radio=1)"
		test5 = "(news.am.com)  (www.aca.am)"
		test6 = " [{https://github.com/FindKeys/ArmTokenizer}]"
		compile = re.compile(urls())
		res1 = re.findall(compile,test1)
		res2 = re.findall(compile,test2)
		res3 = re.findall(compile,test3)
		res4 = re.findall(compile,test4)
		res5 = re.findall(compile,test5)
		res6 = re.findall(compile,test6)
		self.assertEqual(res1, ['news.am'])
		self.assertEqual(res2, ['news.am','news.am'])
		self.assertEqual(res3, ['news.am.com','www.aca.am'])
		self.assertEqual(res4, ['https://www.youtube.com/watch?v=iuJDhFRDx9M&list=RDMMiuJDhFRDx9M&start_radio=1'])
		self.assertEqual(res5, ['news.am.com','www.aca.am'])
		self.assertEqual(res6, ['https://github.com/FindKeys/ArmTokenizer'])

	def test_hashtags(self): 
		test1 = '@DavidS  ,  #FindKeys'
		test2 = ' asdasd#InvalidHashtag  @Valid'
		compile = re.compile(hashtags())
		res1 = re.findall(compile,test1)
		res2 = re.findall(compile,test2)
		self.assertEqual(res1, ['@DavidS', '#FindKeys'])
		self.assertEqual(res2, ['@Valid'])
	
	def test_armenian_word(self): 
		test1 = 'Անուն  ազգանուն  հայրանուն:'
		test2 = 'Մեր  նպատակն  է  կիրառել  մեր  ողջ  մտավոր  ուժը:'
		compile = re.compile(armenian_word())
		res1 = re.findall(compile,test1)
		res2 = re.findall(compile,test2)
		self.assertEqual(res1, ['Անուն', 'ազգանուն', 'հայրանուն'])
		self.assertEqual(res2, ['Մեր', 'նպատակն', 'է', 'կիրառել', 'մեր', 'ողջ', 'մտավոր', 'ուժը'])
	
	def test_english_word(self):
		test1 = "Anyone who reads Old and Middle English literary texts will be familiar with the"
		test2 = '[{( one-two)]}'
		test3 = " Heellooo it's me"
		test4 = " one---two"
		compile = re.compile(english_word())
		res1  = re.findall(compile,test1)
		res2 = re.findall(compile,test2)
		res3 = re.findall(compile,test3)
		res4 = re.findall(compile,test4)
		self.assertEqual(res1, test1.split(' '))
		self.assertEqual(res2, ["one","two"])
		self.assertEqual(res3, ["Heellooo","it's","me"])
		self.assertEqual(res4, ["one","two"])

	def test_arm_postfix_word(self):
		test1 = 'ՀՀԿ-ական'
		test2 = ' ՊԱՏՄԱ_քաղաքական:'
		test3 = ":ՀՀԿ-ական ՀՀԿ-ական ՀՀԿ-ական:"
		test4 = "  Ֆ_կլասի"
		compile = re.compile(arm_postfix_word())
		res1  = re.findall(compile,test1)
		res2 = re.findall(compile,test2)
		res3 = re.findall(compile,test3)
		res4 = re.findall(compile,test4) 
		self.assertEqual(res1,['ՀՀԿ-ական'])
		self.assertEqual(res2,['ՊԱՏՄԱ_քաղաքական'])
		self.assertEqual(res3,['ՀՀԿ-ական','ՀՀԿ-ական','ՀՀԿ-ական'])
		self.assertEqual(res4,['Ֆ_կլասի'])

	def test_arm_non_linear_word(self):
		test1 = 'հեյ~  հե~յ'
		test2 = 'Քո  հետ  կատարվածում  մեղավոր  ես  միայն  դու,  հասկացար՞:'
		test3 = 'Եղիր՛  առաջինը:'
		compile = re.compile(arm_non_linear_word())
		res1 = re.findall(compile,test1)
		res2 = re.findall(compile,test2)
		res3 = re.findall(compile,test3)
		self.assertEqual(res1, ['հեյ~'])
		self.assertEqual(res2, ['հասկացար՞'])
		self.assertEqual(res3, ['Եղիր՛'])
		
	def test_russian_word(self):
		test1 = "Доброе утро."
		test2 = "Как дела? "
		test3 = "В прошлом году мой друг	rheme    построил дом"
		compile = re.compile(russian_word())
		res1 = re.findall(compile,test1)
		res2 = re.findall(compile,test2)
		res3 = re.findall(compile,test3)
		self.assertEqual(res1,["Доброе", "утро"])
		self.assertEqual(res2,['Как', "дела"])
		self.assertEqual(res3,['В', "прошлом", "году", "мой" ,"друг" ,"построил", "дом"])

	def test_dots(self):
			test1 = '....  ...'
			test2 = 'Hmm....'
			compile = re.compile(dots())
			res1 = re.findall(compile,test1)
			res2 = re.findall(compile,test2)
			self.assertEqual(res1, ['....', '...'])
			self.assertEqual(res2, ['....'])

	def test_all_linear_puncts(self):
		test1 = ". ? : « » ! ՜ ՝ , յ,-."
		compile = re.compile(all_linear_puncts())
		res1 = re.findall(compile,test1)
		self.assertEqual(res1,['.', ':', '«', '»', '՝', ',', ',', '.'])

	def test_all_non_linear_puncts(self):
		test1 = '՚  ՚  ՛  ՛  ՜  ՜'
		test2 = 'Մի՛  արա  այդպես,  հե՜յ  լսու՞մ  ես  ինձ:'
		compile = re.compile(all_non_linear_puncts())
		res1 = re.findall(compile,test1)
		res2 = re.findall(compile,test2)
		self.assertEqual(res1, ['՚', '՚', '՛', '՛', '՜', '՜'])
		self.assertEqual(res2, ['՛', '՜', '՞'])
		
	def test_abbrivations(self): 
		pass
	
	def test_special_names(self): 
		pass

if __name__ == '__main__':
	unittest.main()
