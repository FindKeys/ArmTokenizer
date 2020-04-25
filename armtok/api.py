from abc import ABCMeta, abstractmethod
from six import add_metaclass

@add_metaclass(ABCMeta)
class ArmTokenizerBase(object):
    """
    A processing interface for tokenizing a string.
    Subclasses must define ``tokenize()``.
    """
        
    @abstractmethod
    def tokenize(self, s):
        """
        Return a tokenized copy of *s*.
        :rtype: list of str
        """
        pass
    
    @abstractmethod
    def segmentize(self,s):
        """
        Return segmentized form of *s*
        :rtype: list of str
        """
        pass
    
    def tokenize_sents(self, strings):
        """
        Apply ``self.tokenize()`` to each element of ``strings``
        :rtype: gen
        """
        return [self.tokenize(s) for s in strings]