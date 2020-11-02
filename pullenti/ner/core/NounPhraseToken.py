# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing
import io
from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.morph.MorphLang import MorphLang
from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.core.NounPhraseMultivarToken import NounPhraseMultivarToken
from pullenti.morph.MorphBaseInfo import MorphBaseInfo
from pullenti.morph.MorphologyService import MorphologyService
from pullenti.ner.core.internal.NounPhraseItemTextVar import NounPhraseItemTextVar
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.TextToken import TextToken
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.core.MiscHelper import MiscHelper

class NounPhraseToken(MetaToken):
    """ Метатокен - именная группа (это существительное с возможными прилагательными, морфологичски согласованными).
    Выделяется методом TryParse() класса NounPhraseHelper.
    
    Именная группа
    """
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
        self.noun = None;
        self.adjectives = list()
        self.adverbs = None
        self.internal_noun = None;
        self.anafor = None;
        self.anafora_ref = None;
        self.preposition = None;
        self.multi_nouns = False
    
    def get_multivars(self) -> typing.List['NounPhraseMultivarToken']:
        """ Это если MultiNouns = true, то можно как бы расщепить на варианты
        (грузовой и легковой автомобили -> грузовой автомобиль и легковой автомобиль)
        
        Returns:
            typing.List[NounPhraseMultivarToken]: список NounPhraseMultivarToken
        """
        res = list()
        i = 0
        while i < len(self.adjectives): 
            v = NounPhraseMultivarToken._new498(self.adjectives[i].begin_token, self.adjectives[i].end_token, self, i, i)
            while i < (len(self.adjectives) - 1): 
                if (self.adjectives[i + 1].begin_token == self.adjectives[i].end_token.next0_): 
                    v.end_token = self.adjectives[i + 1].end_token
                    v.adj_index2 = (i + 1)
                else: 
                    break
                i += 1
            if (i == (len(self.adjectives) - 1)): 
                v.end_token = self.end_token
            res.append(v)
            i += 1
        return res
    
    def get_normal_case_text(self, mc : 'MorphClass'=None, num : 'MorphNumber'=MorphNumber.UNDEFINED, gender : 'MorphGender'=MorphGender.UNDEFINED, keep_chars : bool=False) -> str:
        res = io.StringIO()
        if (gender == MorphGender.UNDEFINED): 
            gender = self.morph.gender
        if (self.adverbs is not None and len(self.adverbs) > 0): 
            i = 0
            if (len(self.adjectives) > 0): 
                j = 0
                while j < len(self.adjectives): 
                    while i < len(self.adverbs): 
                        if (self.adverbs[i].begin_char < self.adjectives[j].begin_char): 
                            print("{0} ".format(self.adverbs[i].get_normal_case_text(MorphClass.ADVERB, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)), end="", file=res, flush=True)
                        else: 
                            break
                        i += 1
                    s = self.adjectives[j].get_normal_case_text((MorphClass.ADJECTIVE) | MorphClass.PRONOUN, num, gender, keep_chars)
                    print("{0} ".format(Utils.ifNotNull(s, "?")), end="", file=res, flush=True)
                    j += 1
            while i < len(self.adverbs): 
                print("{0} ".format(self.adverbs[i].get_normal_case_text(MorphClass.ADVERB, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)), end="", file=res, flush=True)
                i += 1
        else: 
            for t in self.adjectives: 
                s = t.get_normal_case_text((MorphClass.ADJECTIVE) | MorphClass.PRONOUN, num, gender, keep_chars)
                print("{0} ".format(Utils.ifNotNull(s, "?")), end="", file=res, flush=True)
        r = None
        if ((isinstance(self.noun.begin_token, ReferentToken)) and self.noun.begin_token == self.noun.end_token): 
            r = self.noun.begin_token.get_normal_case_text(None, num, gender, keep_chars)
        else: 
            cas = (MorphClass.NOUN) | MorphClass.PRONOUN
            if (mc is not None and not mc.is_undefined): 
                cas = mc
            r = self.noun.get_normal_case_text(cas, num, gender, keep_chars)
        if (r is None or r == "?"): 
            r = self.noun.get_normal_case_text(None, num, MorphGender.UNDEFINED, False)
        print(Utils.ifNotNull(r, str(self.noun)), end="", file=res)
        return Utils.toStringStringIO(res)
    
    def get_normal_case_text_without_adjective(self, adj_index : int) -> str:
        res = io.StringIO()
        i = 0
        while i < len(self.adjectives): 
            if (i != adj_index): 
                s = self.adjectives[i].get_normal_case_text((MorphClass.ADJECTIVE) | MorphClass.PRONOUN, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)
                print("{0} ".format(Utils.ifNotNull(s, "?")), end="", file=res, flush=True)
            i += 1
        r = self.noun.get_normal_case_text((MorphClass.NOUN) | MorphClass.PRONOUN, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)
        if (r is None): 
            r = self.noun.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)
        print(Utils.ifNotNull(r, str(self.noun)), end="", file=res)
        return Utils.toStringStringIO(res)
    
    def get_morph_variant(self, cas : 'MorphCase', plural : bool) -> str:
        """ Сгенерировать текст именной группы в нужном падеже и числе
        
        Args:
            cas(MorphCase): нужный падеж
            plural(bool): нужное число
        
        Returns:
            str: результирующая строка
        """
        mi = MorphBaseInfo._new499(cas, MorphLang.RU)
        if (plural): 
            mi.number = MorphNumber.PLURAL
        else: 
            mi.number = MorphNumber.SINGULAR
        res = None
        for a in self.adjectives: 
            tt = MiscHelper.get_text_value_of_meta_token(a, GetTextAttr.NO)
            if (a.begin_token != a.end_token or not (isinstance(a.begin_token, TextToken))): 
                pass
            else: 
                tt2 = MorphologyService.get_wordform(tt, mi)
                if (tt2 is not None): 
                    tt = tt2
            if (res is None): 
                res = tt
            else: 
                res = "{0} {1}".format(res, tt)
        if (self.noun is not None): 
            tt = MiscHelper.get_text_value_of_meta_token(self.noun, GetTextAttr.NO)
            if (self.noun.begin_token != self.noun.end_token or not (isinstance(self.noun.begin_token, TextToken))): 
                pass
            else: 
                tt2 = MorphologyService.get_wordform(tt, mi)
                if (tt2 is not None): 
                    tt = tt2
            if (res is None): 
                res = tt
            else: 
                res = "{0} {1}".format(res, tt)
        return res
    
    def __str__(self) -> str:
        if (self.internal_noun is None): 
            return "{0} {1}".format(Utils.ifNotNull(self.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False), "?"), str(self.morph))
        else: 
            return "{0} {1} / {2}".format(Utils.ifNotNull(self.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False), "?"), str(self.morph), str(self.internal_noun))
    
    def remove_last_noun_word(self) -> None:
        if (self.noun is not None): 
            for it in self.noun.morph.items: 
                ii = Utils.asObjectOrNull(it, NounPhraseItemTextVar)
                if (ii is None or ii.normal_value is None): 
                    continue
                j = ii.normal_value.find('-')
                if (j > 0): 
                    ii.normal_value = ii.normal_value[0:0+j]
                if (ii.single_number_value is not None): 
                    j = ii.single_number_value.find('-')
                    if (((j)) > 0): 
                        ii.single_number_value = ii.single_number_value[0:0+j]
    
    @staticmethod
    def _new466(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'PrepositionToken') -> 'NounPhraseToken':
        res = NounPhraseToken(_arg1, _arg2)
        res.preposition = _arg3
        return res
    
    @staticmethod
    def _new2949(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'MorphCollection') -> 'NounPhraseToken':
        res = NounPhraseToken(_arg1, _arg2)
        res.morph = _arg3
        return res