# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import io
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.ner.Token import Token
from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.core.internal.SerializerHelper import SerializerHelper


class TextToken(Token):
    """ Входной токен (после морфанализа) """
    
    def __init__(self, source : 'MorphToken', kit_ : 'AnalysisKit') -> None:
        from pullenti.ner.MorphCollection import MorphCollection
        from pullenti.morph.MorphWordForm import MorphWordForm
        self.term = None
        self.lemma = None
        self.term0 = None
        self.invariant_prefix_length = 0
        self.max_length = 0
        super().__init__(kit_, (0 if source is None else source.begin_char), (0 if source is None else source.end_char))
        if (source is None): 
            return
        self.chars = source.char_info
        self.term = source.term
        self.lemma = (Utils.ifNotNull(source.lemma, self.term))
        self.max_length = (len(self.term))
        self.morph = MorphCollection()
        if (source.word_forms is not None): 
            for wf in source.word_forms: 
                self.morph.add_item(wf)
                if (wf.normal_case is not None and (self.max_length < len(wf.normal_case))): 
                    self.max_length = (len(wf.normal_case))
                if (wf.normal_full is not None and (self.max_length < len(wf.normal_full))): 
                    self.max_length = (len(wf.normal_full))
        i = 0
        while i < len(self.term): 
            ch = self.term[i]
            j = 0
            while j < self.morph.items_count: 
                wf = (self.morph.get_indexer_item(j) if isinstance(self.morph.get_indexer_item(j), MorphWordForm) else None)
                if (wf.normal_case is not None): 
                    if (i >= len(wf.normal_case)): 
                        break
                    if (wf.normal_case[i] != ch): 
                        break
                if (wf.normal_full is not None): 
                    if (i >= len(wf.normal_full)): 
                        break
                    if (wf.normal_full[i] != ch): 
                        break
                j += 1
            if (j < self.morph.items_count): 
                break
            self.invariant_prefix_length = ((i + 1))
            i += 1
        if (self.morph.language.is_undefined and not source.language.is_undefined): 
            self.morph.language = source.language
    
    def get_lemma(self) -> str:
        return self.lemma
    
    def __str__(self) -> str:
        res = Utils.newStringIO(self.term)
        for l_ in self.morph.items: 
            print(", {0}".format(str(l_)), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    def check_value(self, dict0_ : typing.List[tuple]) -> object:
        from pullenti.morph.MorphWordForm import MorphWordForm
        if (dict0_ is None): 
            return None
        inoutarg2671 = RefOutArgWrapper(None)
        inoutres2672 = Utils.tryGetValue(dict0_, self.term, inoutarg2671)
        res = inoutarg2671.value
        if (inoutres2672): 
            return res
        if (self.morph is not None): 
            for it in self.morph.items: 
                mf = (it if isinstance(it, MorphWordForm) else None)
                if (mf is not None): 
                    if (mf.normal_case is not None): 
                        inoutarg2667 = RefOutArgWrapper(None)
                        inoutres2668 = Utils.tryGetValue(dict0_, mf.normal_case, inoutarg2667)
                        res = inoutarg2667.value
                        if (inoutres2668): 
                            return res
                    if (mf.normal_full is not None and mf.normal_case != mf.normal_full): 
                        inoutarg2669 = RefOutArgWrapper(None)
                        inoutres2670 = Utils.tryGetValue(dict0_, mf.normal_full, inoutarg2669)
                        res = inoutarg2669.value
                        if (inoutres2670): 
                            return res
        return None
    
    def get_source_text(self) -> str:
        return super().get_source_text()
    
    def is_value(self, term_ : str, termua : str=None) -> bool:
        from pullenti.morph.MorphWordForm import MorphWordForm
        if (termua is not None and self.morph.language.is_ua): 
            if (self.is_value(termua, None)): 
                return True
        if (term_ is None): 
            return False
        if (self.invariant_prefix_length > len(term_)): 
            return False
        if (self.max_length >= len(self.term) and (self.max_length < len(term_))): 
            return False
        if (term_ == self.term): 
            return True
        for wf in self.morph.items: 
            if ((wf if isinstance(wf, MorphWordForm) else None).normal_case == term_ or (wf if isinstance(wf, MorphWordForm) else None).normal_full == term_): 
                return True
        return False
    
    def get_normal_case_text(self, mc : 'MorphClass'=MorphClass(), single_number : bool=False, gender : 'MorphGender'=MorphGender.UNDEFINED, keep_chars : bool=False) -> str:
        from pullenti.morph.MorphBaseInfo import MorphBaseInfo
        from pullenti.morph.MorphWordForm import MorphWordForm
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.morph.Morphology import Morphology
        empty = True
        for it in self.morph.items: 
            if (mc is not None and not mc.is_undefined): 
                cc = (it.class0_.value) & (mc.value)
                if (cc == 0): 
                    continue
                if (MorphClass.is_misc_int(cc) and not MorphClass.is_proper_int(cc) and mc.value != it.class0_.value): 
                    continue
            wf = (it if isinstance(it, MorphWordForm) else None)
            normal_full = False
            if (gender != MorphGender.UNDEFINED): 
                if ((((it.gender) & (gender))) == (MorphGender.UNDEFINED)): 
                    if ((gender == MorphGender.MASCULINE and ((it.gender != MorphGender.UNDEFINED or it.number == MorphNumber.PLURAL)) and wf is not None) and wf.normal_full is not None): 
                        normal_full = True
                    elif (gender == MorphGender.MASCULINE and it.class0_.is_personal_pronoun): 
                        pass
                    else: 
                        continue
            if (not it.case.is_undefined): 
                empty = False
            if (wf is not None): 
                if (single_number and it.number == MorphNumber.PLURAL and wf.normal_full is not None): 
                    le = len(wf.normal_case)
                    if ((le == (len(wf.normal_full) + 2) and le > 4 and wf.normal_case[le - 2] == 'С') and wf.normal_case[le - 1] == 'Я'): 
                        res = wf.normal_case
                    else: 
                        res = (wf.normal_full if normal_full else wf.normal_full)
                else: 
                    res = (wf.normal_full if normal_full else (Utils.ifNotNull(wf.normal_case, self.term)))
                if (single_number and mc is not None and mc == MorphClass.NOUN): 
                    if (res == "ДЕТИ"): 
                        res = "РЕБЕНОК"
                if (keep_chars): 
                    if (self.chars.is_all_lower): 
                        res = res.lower()
                    elif (self.chars.is_capital_upper): 
                        res = MiscHelper.convert_first_char_upper_and_other_lower(res)
                return res
        if (not empty): 
            return None
        te = None
        if (single_number and mc is not None): 
            bi = MorphBaseInfo._new504(MorphClass(mc), gender, MorphNumber.SINGULAR, self.morph.language)
            vars0_ = Morphology.get_wordform(self.term, bi)
            if (vars0_ is not None): 
                te = vars0_
        if (self.chars.is_cyrillic_letter and te is None and len(self.term) > 3): 
            ch0 = self.term[len(self.term) - 1]
            ch1 = self.term[len(self.term) - 2]
            if (ch0 == 'М' and ((ch1 == 'О' or ch1 == 'А'))): 
                te = self.term[0:0+len(self.term) - 2]
            elif (not LanguageHelper.is_cyrillic_vowel(ch1) and LanguageHelper.is_cyrillic_vowel(ch0)): 
                te = self.term[0:0+len(self.term) - 1]
        if (te is None): 
            te = self.term
        if (keep_chars): 
            if (self.chars.is_all_lower): 
                return te.lower()
            elif (self.chars.is_capital_upper): 
                return MiscHelper.convert_first_char_upper_and_other_lower(te)
        return te
    
    @staticmethod
    def get_source_text_tokens(begin : 'Token', end : 'Token') -> typing.List['TextToken']:
        from pullenti.ner.MetaToken import MetaToken
        res = list()
        t = begin
        while t is not None and t != end.next0_ and t.end_char <= end.end_char: 
            if (isinstance(t, TextToken)): 
                res.append(t if isinstance(t, TextToken) else None)
            elif (isinstance(t, MetaToken)): 
                res.extend(TextToken.get_source_text_tokens((t if isinstance(t, MetaToken) else None).begin_token, (t if isinstance(t, MetaToken) else None).end_token))
            t = t.next0_
        return res
    
    @property
    def is_pure_verb(self) -> bool:
        """ Признак того, что это чистый глагол """
        from pullenti.morph.MorphWordForm import MorphWordForm
        ret = False
        if ((self.is_value("МОЖНО", None) or self.is_value("МОЖЕТ", None) or self.is_value("ДОЛЖНЫЙ", None)) or self.is_value("НУЖНО", None)): 
            return True
        for it in self.morph.items: 
            if ((isinstance(it, MorphWordForm)) and (it if isinstance(it, MorphWordForm) else None).is_in_dictionary): 
                if (it.class0_.is_verb and it.case.is_undefined): 
                    ret = True
                elif (not it.class0_.is_verb): 
                    if (it.class0_.is_adjective and it.contains_attr("к.ф.", MorphClass())): 
                        pass
                    else: 
                        return False
        return ret
    
    @property
    def is_verb_be(self) -> bool:
        """ Проверка, что это глагол типа БЫТЬ, ЯВЛЯТЬСЯ и т.п. """
        if ((self.is_value("БЫТЬ", None) or self.is_value("ЕСТЬ", None) or self.is_value("ЯВЛЯТЬ", None)) or self.is_value("BE", None)): 
            return True
        if (self.term == "IS" or self.term == "WAS" or self.term == "BECAME"): 
            return True
        if (self.term == "Є"): 
            return True
        return False
    
    def _serialize(self, stream : io.IOBase) -> None:
        super()._serialize(stream)
        SerializerHelper.serialize_string(stream, self.term)
        SerializerHelper.serialize_string(stream, self.lemma)
        SerializerHelper.serialize_short(stream, self.invariant_prefix_length)
        SerializerHelper.serialize_short(stream, self.max_length)
    
    def _deserialize(self, stream : io.IOBase, kit_ : 'AnalysisKit') -> None:
        super()._deserialize(stream, kit_)
        self.term = SerializerHelper.deserialize_string(stream)
        self.lemma = SerializerHelper.deserialize_string(stream)
        self.invariant_prefix_length = SerializerHelper.deserialize_short(stream)
        self.max_length = SerializerHelper.deserialize_short(stream)
    
    @staticmethod
    def _new493(_arg1 : 'MorphToken', _arg2 : 'AnalysisKit', _arg3 : str) -> 'TextToken':
        res = TextToken(_arg1, _arg2)
        res.term0 = _arg3
        return res
    
    @staticmethod
    def _new496(_arg1 : 'MorphToken', _arg2 : 'AnalysisKit', _arg3 : 'CharsInfo', _arg4 : int, _arg5 : int, _arg6 : str) -> 'TextToken':
        res = TextToken(_arg1, _arg2)
        res.chars = _arg3
        res.begin_char = _arg4
        res.end_char = _arg5
        res.term0 = _arg6
        return res