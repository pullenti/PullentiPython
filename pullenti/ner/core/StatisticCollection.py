# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.ntopy.Utils import Utils
from pullenti.ntopy.Misc import RefOutArgWrapper


from pullenti.morph.MorphGender import MorphGender


class StatisticCollection:
    """ Поддержка анализа биграммной зависимости токенов в тексте """
    
    class BigrammInfo:
        
        def __init__(self) -> None:
            self.first_count = 0
            self.second_count = 0
            self.pair_count = 0
            self.first_has_other_second = False
            self.second_has_other_first = False
    
        
        @staticmethod
        def _new586(_arg1 : int, _arg2 : int) -> 'BigrammInfo':
            res = StatisticCollection.BigrammInfo()
            res.first_count = _arg1
            res.second_count = _arg2
            return res
    
    class WordInfo:
        
        def __init__(self) -> None:
            self.normal = None
            self.total_count = 0
            self.lower_count = 0
            self.upper_count = 0
            self.capital_count = 0
            self.male_verbs_after_count = 0
            self.female_verbs_after_count = 0
            self.has_before_person_attr = False
            self.not_capital_before_count = 0
            self.like_chars_before_words = None
            self.like_chars_after_words = None
        
        def __str__(self) -> str:
            return self.normal
        
        def add_before(self, w : 'WordInfo') -> None:
            if (self.like_chars_before_words is None): 
                self.like_chars_before_words = dict()
            if (not w in self.like_chars_before_words): 
                self.like_chars_before_words[w] = 1
            else: 
                self.like_chars_before_words[w] += 1
        
        def add_after(self, w : 'WordInfo') -> None:
            if (self.like_chars_after_words is None): 
                self.like_chars_after_words = dict()
            if (not w in self.like_chars_after_words): 
                self.like_chars_after_words[w] = 1
            else: 
                self.like_chars_after_words[w] += 1
    
        
        @staticmethod
        def _new573(_arg1 : str) -> 'WordInfo':
            res = StatisticCollection.WordInfo()
            res.normal = _arg1
            return res
    
    def __init__(self) -> None:
        self.__m_items = dict()
        self.__m_bigramms = dict()
        self.__m_bigramms_rev = dict()
        self.__m_initials = dict()
        self.__m_initials_rev = dict()
    
    def prepare(self, first : 'Token') -> None:
        from pullenti.ner.TextToken import TextToken
        prev = None
        prevt = None
        t = first
        first_pass2608 = True
        while True:
            if first_pass2608: first_pass2608 = False
            else: t = t.next0
            if (not (t is not None)): break
            if (t.is_hiphen): 
                continue
            it = None
            if ((isinstance(t, TextToken) and t.chars.is_letter and t.length_char > 1) and not t.chars.is_all_lower): 
                it = self.__add_token(t if isinstance(t, TextToken) else None)
            elif (((isinstance(t, TextToken) and (t if isinstance(t, TextToken) else None).length_char == 1 and t.chars.is_all_upper) and t.next0 is not None and t.next0.is_char('.')) and not t.is_whitespace_after): 
                it = self.__add_token(t if isinstance(t, TextToken) else None)
                t = t.next0
            if (prev is not None and it is not None): 
                self.__add_bigramm(prev, it)
                if (prevt.chars == t.chars): 
                    prev.add_after(it)
                    it.add_before(prev)
            prev = it
            prevt = t
        t = first
        while t is not None: 
            if (t.chars.is_letter and isinstance(t, TextToken)): 
                it = self.__find_item(t if isinstance(t, TextToken) else None, False)
                if (it is not None): 
                    if (t.chars.is_all_lower): 
                        it.lower_count += 1
                    elif (t.chars.is_all_upper): 
                        it.upper_count += 1
                    elif (t.chars.is_capital_upper): 
                        it.capital_count += 1
            t = t.next0
    
    def __add_token(self, tt : 'TextToken') -> 'WordInfo':
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.morph.MorphWordForm import MorphWordForm
        from pullenti.ner.TextToken import TextToken
        vars0 = list()
        vars0.append(tt.term)
        s = MiscHelper.get_absolute_normal_value(tt.term, False)
        if (s is not None and not s in vars0): 
            vars0.append(s)
        for wff in tt.morph.items: 
            wf = (wff if isinstance(wff, MorphWordForm) else None)
            if (wf is None): 
                continue
            if (wf.normal_case is not None and not wf.normal_case in vars0): 
                vars0.append(wf.normal_case)
            if (wf.normal_full is not None and not wf.normal_full in vars0): 
                vars0.append(wf.normal_full)
        res = None
        for v in vars0: 
            inoutarg571 = RefOutArgWrapper(None)
            inoutres572 = Utils.tryGetValue(self.__m_items, v, inoutarg571)
            res = inoutarg571.value
            if (inoutres572): 
                break
        if (res is None): 
            res = StatisticCollection.WordInfo._new573(tt.lemma)
        for v in vars0: 
            if (not v in self.__m_items): 
                self.__m_items[v] = res
        res.total_count += 1
        if (isinstance(tt.next0, TextToken) and tt.next0.chars.is_all_lower): 
            if (tt.next0.chars.is_cyrillic_letter and tt.next0.get_morph_class_in_dictionary().is_verb): 
                g = tt.next0.morph.gender
                if (g == MorphGender.FEMINIE): 
                    res.female_verbs_after_count += 1
                elif (((g & MorphGender.MASCULINE)) != MorphGender.UNDEFINED): 
                    res.male_verbs_after_count += 1
        if (tt.previous is not None): 
            if (isinstance(tt.previous, TextToken) and tt.previous.chars.is_letter and not tt.previous.chars.is_all_lower): 
                pass
            else: 
                res.not_capital_before_count += 1
        return res
    
    def __find_item(self, tt : 'TextToken', do_absolute : bool=True) -> 'WordInfo':
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.morph.MorphWordForm import MorphWordForm
        if (tt is None): 
            return None
        inoutarg580 = RefOutArgWrapper(None)
        inoutres581 = Utils.tryGetValue(self.__m_items, tt.term, inoutarg580)
        res = inoutarg580.value
        if (inoutres581): 
            return res
        if (do_absolute): 
            s = MiscHelper.get_absolute_normal_value(tt.term, False)
            if (s is not None): 
                inoutarg574 = RefOutArgWrapper(None)
                inoutres575 = Utils.tryGetValue(self.__m_items, s, inoutarg574)
                res = inoutarg574.value
                if (inoutres575): 
                    return res
        for wff in tt.morph.items: 
            wf = (wff if isinstance(wff, MorphWordForm) else None)
            if (wf is None): 
                continue
            inoutarg578 = RefOutArgWrapper(None)
            inoutres579 = Utils.tryGetValue(self.__m_items, Utils.ifNotNull(wf.normal_case, ""), inoutarg578)
            res = inoutarg578.value
            if (inoutres579): 
                return res
            inoutarg576 = RefOutArgWrapper(None)
            inoutres577 = Utils.tryGetValue(self.__m_items, wf.normal_full, inoutarg576)
            res = inoutarg576.value
            if (wf.normal_full is not None and inoutres577): 
                return res
        return None
    
    def __add_bigramm(self, b1 : 'WordInfo', b2 : 'WordInfo') -> None:
        di = [ ]
        inoutarg584 = RefOutArgWrapper(None)
        inoutres585 = Utils.tryGetValue(self.__m_bigramms, b1.normal, inoutarg584)
        di = inoutarg584.value
        if (not inoutres585): 
            di = dict()
            self.__m_bigramms[b1.normal] = di
        if (b2.normal in di): 
            di[b2.normal] += 1
        else: 
            di[b2.normal] = 1
        inoutarg582 = RefOutArgWrapper(None)
        inoutres583 = Utils.tryGetValue(self.__m_bigramms_rev, b2.normal, inoutarg582)
        di = inoutarg582.value
        if (not inoutres583): 
            di = dict()
            self.__m_bigramms_rev[b2.normal] = di
        if (b1.normal in di): 
            di[b1.normal] += 1
        else: 
            di[b1.normal] = 1
    
    def get_bigramm_info(self, t1 : 'Token', t2 : 'Token') -> 'BigrammInfo':
        from pullenti.ner.TextToken import TextToken
        si1 = self.__find_item(t1 if isinstance(t1, TextToken) else None, True)
        si2 = self.__find_item(t2 if isinstance(t2, TextToken) else None, True)
        if (si1 is None or si2 is None): 
            return None
        return self.__get_bigrams_info(si1, si2)
    
    def __get_bigrams_info(self, si1 : 'WordInfo', si2 : 'WordInfo') -> 'BigrammInfo':
        res = StatisticCollection.BigrammInfo._new586(si1.total_count, si2.total_count)
        di12 = None
        inoutarg588 = RefOutArgWrapper(None)
        Utils.tryGetValue(self.__m_bigramms, si1.normal, inoutarg588)
        di12 = inoutarg588.value
        di21 = None
        inoutarg587 = RefOutArgWrapper(None)
        Utils.tryGetValue(self.__m_bigramms_rev, si2.normal, inoutarg587)
        di21 = inoutarg587.value
        if (di12 is not None): 
            if (not si2.normal in di12): 
                res.first_has_other_second = True
            else: 
                res.pair_count = di12[si2.normal]
                if (len(di12) > 1): 
                    res.first_has_other_second = True
        if (di21 is not None): 
            if (not si1.normal in di21): 
                res.second_has_other_first = True
            elif (not si1.normal in di21): 
                res.second_has_other_first = True
            elif (len(di21) > 1): 
                res.second_has_other_first = True
        return res
    
    def get_initial_info(self, ini : str, sur : 'Token') -> 'BigrammInfo':
        from pullenti.ner.TextToken import TextToken
        if (Utils.isNullOrEmpty(ini)): 
            return None
        si2 = self.__find_item(sur if isinstance(sur, TextToken) else None, True)
        if (si2 is None): 
            return None
        si1 = None
        inoutarg589 = RefOutArgWrapper(None)
        inoutres590 = Utils.tryGetValue(self.__m_items, ini[0 : 1], inoutarg589)
        si1 = inoutarg589.value
        if (not inoutres590): 
            return None
        if (si1 is None): 
            return None
        return self.__get_bigrams_info(si1, si2)
    
    def get_word_info(self, t : 'Token') -> 'WordInfo':
        from pullenti.ner.TextToken import TextToken
        tt = (t if isinstance(t, TextToken) else None)
        if (tt is None): 
            return None
        return self.__find_item(tt, True)