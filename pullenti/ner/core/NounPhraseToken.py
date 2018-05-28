# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import io
from pullenti.ntopy.Utils import Utils
from pullenti.ner.MetaToken import MetaToken
from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.core.GetTextAttr import GetTextAttr


class NounPhraseToken(MetaToken):
    """ Токен для представления именной группы """
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        self.noun = None
        self.adjectives = list()
        self.adverbs = None
        self.internal_noun = None
        self.anafor = None
        self.preposition = None
        super().__init__(begin, end, None)
    
    def get_normal_case_text(self, mc : 'MorphClass'=MorphClass(), single_number : bool=False, gender : 'MorphGender'=MorphGender.UNDEFINED, keep_chars : bool=False) -> str:
        from pullenti.ner.ReferentToken import ReferentToken
        res = Utils.newStringIO(None)
        if (gender == MorphGender.UNDEFINED): 
            gender = self.morph.gender
        if (self.adverbs is not None and len(self.adverbs) > 0): 
            i = 0
            if (len(self.adjectives) > 0): 
                for j in range(len(self.adjectives)):
                    s = self.adjectives[j].get_normal_case_text(MorphClass.ADJECTIVE | MorphClass.PRONOUN, single_number, gender, keep_chars)
                    print("{0} ".format(Utils.ifNotNull(s, "?")), end="", file=res, flush=True)
                    while i < len(self.adverbs): 
                        if (self.adverbs[i].begin_char < self.adjectives[j].begin_char): 
                            print("{0} ".format(self.adjectives[i].get_normal_case_text(MorphClass.ADVERB, False, MorphGender.UNDEFINED, False)), end="", file=res, flush=True)
                        else: 
                            break
                        i += 1
            while i < len(self.adverbs): 
                print("{0} ".format(self.adjectives[i].get_normal_case_text(MorphClass.ADVERB, False, MorphGender.UNDEFINED, False)), end="", file=res, flush=True)
                i += 1
        else: 
            for t in self.adjectives: 
                s = t.get_normal_case_text(MorphClass.ADJECTIVE | MorphClass.PRONOUN, single_number, gender, keep_chars)
                print("{0} ".format(Utils.ifNotNull(s, "?")), end="", file=res, flush=True)
        r = None
        if (isinstance(self.noun.begin_token, ReferentToken) and self.noun.begin_token == self.noun.end_token): 
            r = self.noun.begin_token.get_normal_case_text(MorphClass(), single_number, gender, keep_chars)
        else: 
            r = self.noun.get_normal_case_text(MorphClass.NOUN | MorphClass.PRONOUN, single_number, gender, keep_chars)
        if (r is None or r == "?"): 
            r = self.noun.get_normal_case_text(MorphClass(), single_number, MorphGender.UNDEFINED, False)
        print(Utils.ifNotNull(r, (str(self.noun) if self.noun is not None else None)), end="", file=res)
        return Utils.toStringStringIO(res)
    
    def get_normal_case_text_without_adjective(self, adj_index : int) -> str:
        res = Utils.newStringIO(None)
        for i in range(len(self.adjectives)):
            if (i != adj_index): 
                s = self.adjectives[i].get_normal_case_text(MorphClass.ADJECTIVE | MorphClass.PRONOUN, False, MorphGender.UNDEFINED, False)
                print("{0} ".format(Utils.ifNotNull(s, "?")), end="", file=res, flush=True)
        r = self.noun.get_normal_case_text(MorphClass.NOUN | MorphClass.PRONOUN, False, MorphGender.UNDEFINED, False)
        if (r is None): 
            r = self.noun.get_normal_case_text(MorphClass(), False, MorphGender.UNDEFINED, False)
        print(Utils.ifNotNull(r, (str(self.noun) if self.noun is not None else None)), end="", file=res)
        return Utils.toStringStringIO(res)
    
    def get_morph_variant(self, cas : 'MorphCase', plural : bool) -> str:
        """ Сгенерировать текст именной группы в нужном падеже и числе
        
        Args:
            cas(MorphCase): 
            plural(bool): 
        
        """
        from pullenti.morph.MorphBaseInfo import MorphBaseInfo
        from pullenti.morph.MorphLang import MorphLang
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.TextToken import TextToken
        from pullenti.morph.Morphology import Morphology
        mi = MorphBaseInfo._new488(cas, MorphLang.RU)
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
            return "{0} {1}".format(Utils.ifNotNull(self.get_normal_case_text(MorphClass(), False, MorphGender.UNDEFINED, False), "?"), str(self.morph))
        else: 
            return "{0} {1} / {2}".format(Utils.ifNotNull(self.get_normal_case_text(MorphClass(), False, MorphGender.UNDEFINED, False), "?"), str(self.morph), str(self.internal_noun))
    
    def remove_last_noun_word(self) -> None:
        from pullenti.ner.internal.NounPhraseItemTextVar import NounPhraseItemTextVar
        if (self.noun is not None): 
            for it in self.noun.morph.items: 
                ii = (it if isinstance(it, NounPhraseItemTextVar) else None)
                if (ii is None or ii.normal_value is None): 
                    continue
                j = ii.normal_value.find('-')
                if (j > 0): 
                    ii.normal_value = ii.normal_value[0 : (j)]
                if (ii.single_number_value is not None): 
                    j = ii.single_number_value.find('-')
                    if (((j)) > 0): 
                        ii.single_number_value = ii.single_number_value[0 : (j)]