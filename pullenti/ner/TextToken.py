# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.MorphBaseInfo import MorphBaseInfo
from pullenti.morph.MorphWordForm import MorphWordForm
from pullenti.morph.MorphologyService import MorphologyService
from pullenti.ner.MorphCollection import MorphCollection
from pullenti.ner.Token import Token

class TextToken(Token):
    """ Входной токен (после морфанализа)
    Текстовой токен
    """
    
    def __init__(self, source : 'MorphToken', kit_ : 'AnalysisKit', bchar : int=-1, echar : int=-1) -> None:
        super().__init__(kit_, (bchar if bchar >= 0 else (0 if source is None else source.begin_char)), (echar if echar >= 0 else (0 if source is None else source.end_char)))
        self.term = None;
        self.lemma = None;
        self.term0 = None;
        self.invariant_prefix_length_of_morph_vars = 0
        self.max_length_of_morph_vars = 0
        if (source is None): 
            return
        self.chars = source.char_info
        self.term = source.term
        self.lemma = (Utils.ifNotNull(source.get_lemma(), self.term))
        self.max_length_of_morph_vars = (len(self.term))
        self.morph = MorphCollection()
        if (source.word_forms is not None): 
            for wf in source.word_forms: 
                self.morph.add_item(wf)
                if (wf.normal_case is not None and (self.max_length_of_morph_vars < len(wf.normal_case))): 
                    self.max_length_of_morph_vars = (len(wf.normal_case))
                if (wf.normal_full is not None and (self.max_length_of_morph_vars < len(wf.normal_full))): 
                    self.max_length_of_morph_vars = (len(wf.normal_full))
        i = 0
        while i < len(self.term): 
            ch = self.term[i]
            j = 0
            while j < self.morph.items_count: 
                wf = Utils.asObjectOrNull(self.morph.get_indexer_item(j), MorphWordForm)
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
            self.invariant_prefix_length_of_morph_vars = ((i + 1))
            i += 1
        if (self.morph.language.is_undefined and not source.language.is_undefined): 
            self.morph.language = source.language
    
    def __str__(self) -> str:
        res = Utils.newStringIO(self.term)
        for l_ in self.morph.items: 
            print(", {0}".format(str(l_)), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    def check_value(self, dict0_ : typing.List[tuple]) -> object:
        """ Попробовать привязать словарь
        
        Args:
            dict0_(typing.List[tuple]): 
        
        """
        if (dict0_ is None): 
            return None
        wrapres2864 = RefOutArgWrapper(None)
        inoutres2865 = Utils.tryGetValue(dict0_, self.term, wrapres2864)
        res = wrapres2864.value
        if (inoutres2865): 
            return res
        if (self.morph is not None): 
            for it in self.morph.items: 
                mf = Utils.asObjectOrNull(it, MorphWordForm)
                if (mf is not None): 
                    if (mf.normal_case is not None): 
                        wrapres2860 = RefOutArgWrapper(None)
                        inoutres2861 = Utils.tryGetValue(dict0_, mf.normal_case, wrapres2860)
                        res = wrapres2860.value
                        if (inoutres2861): 
                            return res
                    if (mf.normal_full is not None and mf.normal_case != mf.normal_full): 
                        wrapres2862 = RefOutArgWrapper(None)
                        inoutres2863 = Utils.tryGetValue(dict0_, mf.normal_full, wrapres2862)
                        res = wrapres2862.value
                        if (inoutres2863): 
                            return res
        return None
    
    def get_source_text(self) -> str:
        return super().get_source_text()
    
    def is_value(self, term_ : str, termua : str=None) -> bool:
        if (termua is not None and self.morph.language.is_ua): 
            if (self.is_value(termua, None)): 
                return True
        if (term_ is None): 
            return False
        if (self.invariant_prefix_length_of_morph_vars > len(term_)): 
            return False
        if (self.max_length_of_morph_vars >= len(self.term) and (self.max_length_of_morph_vars < len(term_))): 
            return False
        if (term_ == self.term): 
            return True
        for wf in self.morph.items: 
            if ((isinstance(wf, MorphWordForm)) and ((wf.normal_case == term_ or wf.normal_full == term_))): 
                return True
        return False
    
    @property
    def is_and(self) -> bool:
        """ Это соединительный союз И (на всех языках) """
        if (not self.morph.class0_.is_conjunction): 
            if (self.length_char == 1 and self.is_char('&')): 
                return True
            return False
        val = self.term
        if (val == "И" or val == "AND" or val == "UND"): 
            return True
        if (self.morph.language.is_ua): 
            if (val == "І" or val == "ТА"): 
                return True
        return False
    
    @property
    def is_or(self) -> bool:
        """ Это соединительный союз ИЛИ (на всех языках) """
        if (not self.morph.class0_.is_conjunction): 
            return False
        val = self.term
        if (val == "ИЛИ" or val == "ЛИБО" or val == "OR"): 
            return True
        if (self.morph.language.is_ua): 
            if (val == "АБО"): 
                return True
        return False
    
    @property
    def is_letters(self) -> bool:
        return str.isalpha(self.term[0])
    
    def get_morph_class_in_dictionary(self) -> 'MorphClass':
        res = MorphClass()
        for wf in self.morph.items: 
            if ((isinstance(wf, MorphWordForm)) and wf.is_in_dictionary): 
                res |= wf.class0_
        return res
    
    def get_normal_case_text(self, mc : 'MorphClass'=None, num : 'MorphNumber'=MorphNumber.UNDEFINED, gender : 'MorphGender'=MorphGender.UNDEFINED, keep_chars : bool=False) -> str:
        from pullenti.ner.core.MiscHelper import MiscHelper
        empty = True
        if (mc is not None and mc.is_preposition): 
            return LanguageHelper.normalize_preposition(self.term)
        for it in self.morph.items: 
            if (mc is not None and not mc.is_undefined): 
                cc = (it.class0_) & mc
                if (cc.is_undefined): 
                    continue
                if (cc.is_misc and not cc.is_proper and mc != it.class0_): 
                    continue
            wf = Utils.asObjectOrNull(it, MorphWordForm)
            normal_full = False
            if (gender != MorphGender.UNDEFINED): 
                if (((it.gender) & (gender)) == (MorphGender.UNDEFINED)): 
                    if ((gender == MorphGender.MASCULINE and ((it.gender != MorphGender.UNDEFINED or it.number == MorphNumber.PLURAL)) and wf is not None) and wf.normal_full is not None): 
                        normal_full = True
                    elif (gender == MorphGender.MASCULINE and it.class0_.is_personal_pronoun): 
                        pass
                    else: 
                        continue
            if (not it.case_.is_undefined): 
                empty = False
            if (wf is not None): 
                if (num == MorphNumber.SINGULAR and it.number == MorphNumber.PLURAL and wf.normal_full is not None): 
                    le = len(wf.normal_case)
                    if ((le == (len(wf.normal_full) + 2) and le > 4 and wf.normal_case[le - 2] == 'С') and wf.normal_case[le - 1] == 'Я'): 
                        res = wf.normal_case
                    else: 
                        res = (wf.normal_full if normal_full else wf.normal_full)
                else: 
                    res = (wf.normal_full if normal_full else (Utils.ifNotNull(wf.normal_case, self.term)))
                if (num == MorphNumber.SINGULAR and mc is not None and mc == MorphClass.NOUN): 
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
        if (num == MorphNumber.SINGULAR and mc is not None): 
            bi = MorphBaseInfo._new492(MorphClass._new53(mc.value), gender, MorphNumber.SINGULAR, self.morph.language)
            vars0_ = MorphologyService.get_wordform(self.term, bi)
            if (vars0_ is not None): 
                te = vars0_
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
                res.append(Utils.asObjectOrNull(t, TextToken))
            elif (isinstance(t, MetaToken)): 
                res.extend(TextToken.get_source_text_tokens(t.begin_token, t.end_token))
            t = t.next0_
        return res
    
    @property
    def is_pure_verb(self) -> bool:
        """ Признак того, что это чистый глагол """
        ret = False
        if ((self.is_value("МОЖНО", None) or self.is_value("МОЖЕТ", None) or self.is_value("ДОЛЖНЫЙ", None)) or self.is_value("НУЖНО", None)): 
            return True
        for it in self.morph.items: 
            if ((isinstance(it, MorphWordForm)) and it.is_in_dictionary): 
                if (it.class0_.is_verb and it.case_.is_undefined): 
                    ret = True
                elif (not it.class0_.is_verb): 
                    if (it.class0_.is_adjective and it.contains_attr("к.ф.", None)): 
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
        from pullenti.ner.core.internal.SerializerHelper import SerializerHelper
        super()._serialize(stream)
        SerializerHelper.serialize_string(stream, self.term)
        SerializerHelper.serialize_string(stream, self.lemma)
        SerializerHelper.serialize_short(stream, self.invariant_prefix_length_of_morph_vars)
        SerializerHelper.serialize_short(stream, self.max_length_of_morph_vars)
    
    def _deserialize(self, stream : io.IOBase, kit_ : 'AnalysisKit', vers : int) -> None:
        from pullenti.ner.core.internal.SerializerHelper import SerializerHelper
        super()._deserialize(stream, kit_, vers)
        self.term = SerializerHelper.deserialize_string(stream)
        self.lemma = SerializerHelper.deserialize_string(stream)
        self.invariant_prefix_length_of_morph_vars = SerializerHelper.deserialize_short(stream)
        self.max_length_of_morph_vars = SerializerHelper.deserialize_short(stream)
    
    @staticmethod
    def _new470(_arg1 : 'MorphToken', _arg2 : 'AnalysisKit', _arg3 : int, _arg4 : int, _arg5 : str) -> 'TextToken':
        res = TextToken(_arg1, _arg2, _arg3, _arg4)
        res.term0 = _arg5
        return res
    
    @staticmethod
    def _new473(_arg1 : 'MorphToken', _arg2 : 'AnalysisKit', _arg3 : int, _arg4 : int, _arg5 : 'CharsInfo', _arg6 : str) -> 'TextToken':
        res = TextToken(_arg1, _arg2, _arg3, _arg4)
        res.chars = _arg5
        res.term0 = _arg6
        return res