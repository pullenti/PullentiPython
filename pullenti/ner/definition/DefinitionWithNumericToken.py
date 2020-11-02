# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphCase import MorphCase
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.Token import Token
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper

class DefinitionWithNumericToken(MetaToken):
    # Для поддержки выделений тезисов с числовыми данными
    
    def __str__(self) -> str:
        return "{0} {1} ({2})".format(self.number, Utils.ifNotNull(self.noun, "?"), Utils.ifNotNull(self.nouns_genetive, "?"))
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        super().__init__(b, e0_, None)
        self.number = 0
        self.number_begin_char = 0
        self.number_end_char = 0
        self.noun = None;
        self.nouns_genetive = None;
        self.number_substring = None;
        self.text = None;
    
    @staticmethod
    def try_parse(t : 'Token') -> 'DefinitionWithNumericToken':
        """ Выделить определение с указанного токена
        
        Args:
            t(Token): токен
        
        """
        if (not MiscHelper.can_be_start_of_sentence(t)): 
            return None
        tt = t
        noun_ = None
        num = None
        first_pass3639 = True
        while True:
            if first_pass3639: first_pass3639 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            if (tt != t and MiscHelper.can_be_start_of_sentence(tt)): 
                return None
            if (not (isinstance(tt, NumberToken))): 
                continue
            if (tt.whitespaces_after_count > 2 or tt == t): 
                continue
            if (tt.morph.class0_.is_adjective): 
                continue
            nn = NounPhraseHelper.try_parse(tt.next0_, NounPhraseParseAttr.NO, 0, None)
            if (nn is None): 
                continue
            num = (Utils.asObjectOrNull(tt, NumberToken))
            noun_ = nn
            break
        if (num is None or num.int_value is None): 
            return None
        res = DefinitionWithNumericToken(t, noun_.end_token)
        res.number = num.int_value
        res.number_begin_char = num.begin_char
        res.number_end_char = num.end_char
        res.noun = noun_.get_normal_case_text(None, MorphNumber.SINGULAR, MorphGender.UNDEFINED, False)
        res.nouns_genetive = (Utils.ifNotNull(noun_.get_morph_variant(MorphCase.GENITIVE, True), (res.noun if res is not None else None)))
        res.text = MiscHelper.get_text_value(t, num.previous, Utils.valToEnum((GetTextAttr.KEEPQUOTES) | (GetTextAttr.KEEPREGISTER), GetTextAttr))
        if (num.is_whitespace_before): 
            res.text += " "
        res.number_substring = MiscHelper.get_text_value(num, noun_.end_token, Utils.valToEnum((GetTextAttr.KEEPQUOTES) | (GetTextAttr.KEEPREGISTER), GetTextAttr))
        res.text += res.number_substring
        tt = noun_.end_token
        while tt is not None: 
            if (MiscHelper.can_be_start_of_sentence(tt)): 
                break
            res.end_token = tt
            tt = tt.next0_
        if (res.end_token != noun_.end_token): 
            if (noun_.is_whitespace_after): 
                res.text += " "
            res.text += MiscHelper.get_text_value(noun_.end_token.next0_, res.end_token, Utils.valToEnum((GetTextAttr.KEEPQUOTES) | (GetTextAttr.KEEPREGISTER), GetTextAttr))
        return res