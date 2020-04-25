from abc import ABCMeta, abstractmethod
from six import add_metaclass
from collections import namedtuple

Repr = namedtuple('repr',['symb' , 'unic', 'other' ])

@add_metaclass(ABCMeta)
class Punct(object):
    
    N_LINEAR_PUNCT   = ['apostrophe', 'shesht','bacakanchakan', 'harcakan']
    N_LINEAR_SYMBOLS = ['՚','՛','՜','՞']
    N_LINEAR_UNICODE = ['\u055A','\u055B','\u055C','\u055E']
    N_LINEAR_OTHER   = ['', '' ,'~','']
    Repr = namedtuple('repr',['symb' , 'unic', 'other' ])
    NON_LINEAR_PDICT = {n : Repr(s,u,o) for n,s,u,o in zip(N_LINEAR_PUNCT,N_LINEAR_SYMBOLS,N_LINEAR_UNICODE,N_LINEAR_OTHER)}
    
    LINEAR_PUNCT  = ['verjaket','4bazmaket' ,'3bazmaket','mijaket','storaket','but', 
                     'hyphen', 'b_chakert','p_chakert','gtcik' ,'aliq', 'quote1',
                     'quote2','dram', 'b_pakagitc','p_pakagitc', 'b_dzevavor','p_dzevavor',
                     'b_qarakusi','p_qarakusi', 'slesh'
                    ]
    LINEAR_SYMBOLS = ['։'  , '\.\.\.\.' , '\.\.\.' , '\.' , ',' ,  '՝'  ,
                      '֊'  , '«'        ,  '»'     , '—'  , '~' ,  '’' ,
                      '”'  , '֏'        , '\('     ,'\)'  , '\{', '\}' ,  
                      '\[' , '\]'       , '\/'
                     ]
    LINEAR_UNICODE = ['\u0589' , ''       , ''      , '\u002E', '\u002C' , '\u055D' ,
                      '\u058A' , '\u00AB' , '\u00BB', '\u2014', '\u007E' , '\u2019' ,
                      '\u201D' , '\u058F' , '\u0028', '\u0029', '\u007B' , '\u007D',
                      '\u005B' , '\u005D' , '\u002F'

                    ]
    LINEAR_OTHER = [ ':' , '' , '' , '\.', ',' , '`',
                     ''  , '' , '' , '_' , ''  , '' ,
                     ''  , '' , '' , ''  , ''  , ''  ,
                     ''  , '' , '' ,
                   ]
    
    LINEAR_PDICT = {n : Repr(s,u,o) for n,s,u,o in zip(LINEAR_PUNCT,LINEAR_SYMBOLS,LINEAR_UNICODE,LINEAR_OTHER)}
    INTERNATIONAL = [ '+', '-', '?','!','%', '°С', '$', '€', '₩', '¥', '₦', '₽', '£' ]
    METRIC = [ 'կմ', 'մ','սմ' , 'մմ', 'ժ', 'վ', 'ր', 'մվ', 'կգ', 'գ',  'մգ', 'տ' , 'ց','ք']
                      
    def __init__(self, punct):
        if punct:
            if not isinstance(punct, list):
                self.punct = [punct]
            else:
                self.punct = punct
        else:
            raise KeyError('Please write punctuation symbol.')
    
    def regex(self):
        reg_arr = []
        if self.punct:
            for p in self.punct:
                if p in self.NON_LINEAR_PDICT:
                    reg_arr += [i for i in self.NON_LINEAR_PDICT[p] if i]
                elif p in self.LINEAR_PDICT:
                    reg_arr += [i for i in self.LINEAR_PDICT[p] if i]
        else:
            return ''
        return u'|'.join(reg_arr)
    
    @classmethod
    def all(cls, linear=True):
        reg_arr = []
        for i in (cls.LINEAR_PDICT.values() if linear == True else cls.NON_LINEAR_PDICT.values()):
            for j in i:
                if j:
                    reg_arr.append(j)
        return u'|'.join( reg_arr )
    
    @classmethod
    def inter(cls):
        return u'|'.join( cls.INTERNATIONAL )
    
    @classmethod
    def metric(cls, double):
        if double:
            return u'|'.join(['{}/{}'.format(i,j) for i in cls.METRIC for j in cls.METRIC if i!=j])
        else:
            return u'|'.join(cls.METRIC)

