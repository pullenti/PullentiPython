# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.MetaToken import MetaToken
from pullenti.morph.MorphLang import MorphLang
from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphBaseInfo import MorphBaseInfo
from pullenti.morph.Morphology import Morphology
from pullenti.ner.core.internal.NounPhraseItemTextVar import NounPhraseItemTextVar
from pullenti.ner.TextToken import TextToken
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.core.MiscHelper import MiscHelper

class NounPhraseToken(MetaToken):
    """ Токен для представления именной группы """
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
        self.noun = None;
        self.adjectives = list()
        self.adverbs = None
        self.internal_noun = None;
        self.anafor = None;
        self.preposition = None;
        self.multi_nouns = False
    
    def get_normal_case_text(self, mc : 'MorphClass'=None, single_number : bool=False, gender : 'MorphGender'=MorphGender.UNDEFINED, keep_chars : bool=False) -> str:
        res = io.StringIO()
        if (gender == MorphGender.UNDEFINED): 
            gender = self.morph.gender
        if (self.adverbs is not None and len(self.adverbs) > 0): 
            i = 0
            if (len(self.adjectives) > 0): 
                j = 0
                while j < len(self.adjectives): 
                    s = self.adjectives[j].get_normal_case_text((MorphClass.ADJECTIVE) | MorphClass.PRONOUN, single_number, gender, keep_chars)
                    print("{0} ".format(Utils.ifNotNull(s, "?")), end="", file=res, flush=True)
                    while i < len(self.adverbs): 
                        if (self.adverbs[i].begin_char < self.adjectives[j].begin_char): 
                            print("{0} ".format(self.adjectives[i].get_normal_case_text(MorphClass.ADVERB, False, MorphGender.UNDEFINED, False)), end="", file=res, flush=True)
                        else: 
                            break
                        i += 1
                    j += 1
            while i < len(self.adverbs): 
                print("{0} ".format(self.adjectives[i].get_normal_case_text(MorphClass.ADVERB, False, MorphGender.UNDEFINED, False)), end="", file=res, flush=True)
                i += 1
        else: 
            for t in self.adjectives: 
                s = t.get_normal_case_text((MorphClass.ADJECTIVE) | MorphClass.PRONOUN, single_number, gender, keep_chars)
                print("{0} ".format(Utils.ifNotNull(s, "?")), end="", file=res, flush=True)
        r = None
        if ((isinstance(self.noun.begin_token, ReferentToken)) and self.noun.begin_token == self.noun.end_token): 
            r = self.noun.begin_token.get_normal_case_text(None, single_number, gender, keep_chars)
        else: 
            cas = (MorphClass.NOUN) | MorphClass.PRONOUN
            if (mc is not None and not mc.is_undefined): 
                cas = mc
            r = self.noun.get_normal_case_text(cas, single_number, gender, keep_chars)
        if (r is None or r == "?"): 
            r = self.noun.get_normal_case_text(None, single_number, MorphGender.UNDEFINED, False)
        print(Utils.ifNotNull(r, str(self.noun)), end="", file=res)
        return Utils.toStringStringIO(res)
    
    def get_normal_case_text_without_adjective(self, adj_index : int) -> str:
        res = io.StringIO()
        i = 0
        while i < len(self.adjectives): 
            if (i != adj_index): 
                s = self.adjectives[i].get_normal_case_text((MorphClass.ADJECTIVE) | MorphClass.PRONOUN, False, MorphGender.UNDEFINED, False)
                print("{0} ".format(Utils.ifNotNull(s, "?")), end="", file=res, flush=True)
            i += 1
        r = self.noun.get_normal_case_text((MorphClass.NOUN) | MorphClass.PRONOUN, False, MorphGender.UNDEFINED, False)
        if (r is None): 
            r = self.noun.get_normal_case_text(None, False, MorphGender.UNDEFINED, False)
        print(Utils.ifNotNull(r, str(self.noun)), end="", file=res)
        return Utils.toStringStringIO(res)
    
    def get_morph_variant(self, cas : 'MorphCase', plural : bool) -> str:
        """ Сгенерировать текст именной группы в нужном падеже и числе
        
        Args:
            cas(MorphCase): 
            plural(bool): 
        
        """
        mi = MorphBaseInfo._new567(cas, MorphLang.RU)
        if (plural): 
            mi.number = MorphNumber.PLURAL
        else: 
            mi.number = MorphNumber.SINGULAR
        res = None
        for a in self.adjectives: 
            tt = MiscHelper.get_text_value_of_meta_token(a, GetTextAttr.NO)
            if (a.begin_token != a.end_token or not ((isinstance(a.begin_token, TextToken)))): 
                pass
            else: 
                tt2 = Morphology.get_wordform(tt, mi)
                if (tt2 is not None): 
                    tt = tt2
            if (res is None): 
                res = tt
            else: 
                res = "{0} {1}".format(res, tt)
        if (self.noun is not None): 
            tt = MiscHelper.get_text_value_of_meta_token(self.noun, GetTextAttr.NO)
            if (self.noun.begin_token != self.noun.end_token or not ((isinstance(self.noun.begin_token, TextToken)))): 
                pass
            else: 
                tt2 = Morphology.get_wordform(tt, mi)
                if (tt2 is not None): 
                    tt = tt2
            if (res is None): 
                res = tt
            else: 
                res = "{0} {1}".format(res, tt)
        return res
    
    def __str__(self) -> str:
        if (self.internal_noun is None): 
            return "{0} {1}".format(Utils.ifNotNull(self.get_normal_case_text(None, False, MorphGender.UNDEFINED, False), "?"), str(self.morph))
        else: 
            return "{0} {1} / {2}".format(Utils.ifNotNull(self.get_normal_case_text(None, False, MorphGender.UNDEFINED, False), "?"), str(self.morph), str(self.internal_noun))
    
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