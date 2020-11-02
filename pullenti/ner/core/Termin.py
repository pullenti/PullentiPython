# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing
import io
from pullenti.unisharp.Utils import Utils

from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.morph.MorphWordForm import MorphWordForm
from pullenti.ner.MorphCollection import MorphCollection
from pullenti.ner.core.TerminToken import TerminToken
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.Token import Token
from pullenti.ner.TextToken import TextToken
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.NumberToken import NumberToken
from pullenti.morph.MorphologyService import MorphologyService

class Termin:
    """ Термин, понятие, система обозначений чего-либо и варианты его написания. Элемент словаря TerminCollection.
    
    Термин словаря
    """
    
    class Term:
        # Элемент термина (слово или число)
        
        def __init__(self, src : 'TextToken', add_lemma_variant : bool=False, number : str=None) -> None:
            from pullenti.morph.MorphGender import MorphGender
            from pullenti.morph.MorphWordForm import MorphWordForm
            from pullenti.ner.Token import Token
            from pullenti.ner.NumberSpellingType import NumberSpellingType
            from pullenti.ner.NumberToken import NumberToken
            self.__m_source = None;
            self.is_pattern_any = False
            self.__m_number = None;
            self.__m_variants = list()
            self.__m_gender = MorphGender.UNDEFINED
            self.__m_source = src
            if (src is not None): 
                self.variants.append(src.term)
                if (len(src.term) > 0 and str.isdigit(src.term[0])): 
                    nt = NumberToken(src, src, src.term, NumberSpellingType.DIGIT)
                    self.__m_number = nt.value
                    self.__m_source = (None)
                    return
                if (add_lemma_variant): 
                    lemma = src.lemma
                    if (lemma is not None and lemma != src.term): 
                        self.variants.append(lemma)
                    for wff in src.morph.items: 
                        wf = Utils.asObjectOrNull(wff, MorphWordForm)
                        if (wf is not None and wf.is_in_dictionary): 
                            s = Utils.ifNotNull(wf.normal_full, wf.normal_case)
                            if (s != lemma and s != src.term): 
                                self.variants.append(s)
            if (number is not None): 
                self.__m_number = number
                self.variants.append(number)
        
        @property
        def variants(self) -> typing.List[str]:
            """ Варианты морфологического написания """
            return self.__m_variants
        
        @property
        def canonical_text(self) -> str:
            """ Каноническое изображение (первый вариант) """
            return (self.__m_variants[0] if len(self.__m_variants) > 0 else "?")
        
        def __str__(self) -> str:
            if (self.is_pattern_any): 
                return "IsPatternAny"
            res = io.StringIO()
            for v in self.variants: 
                if (res.tell() > 0): 
                    print(", ", end="", file=res)
                print(v, end="", file=res)
            return Utils.toStringStringIO(res)
        
        @property
        def is_number(self) -> bool:
            """ Признак того, что это число """
            return self.__m_source is None or self.__m_number is not None
        
        @property
        def is_hiphen(self) -> bool:
            """ Это перенос """
            return self.__m_source is not None and self.__m_source.term == "-"
        
        @property
        def is_point(self) -> bool:
            """ Это точка """
            return self.__m_source is not None and self.__m_source.term == "."
        
        @property
        def gender(self) -> 'MorphGender':
            """ Род """
            from pullenti.morph.MorphGender import MorphGender
            from pullenti.morph.MorphWordForm import MorphWordForm
            if (self.__m_gender != MorphGender.UNDEFINED): 
                return self.__m_gender
            res = MorphGender.UNDEFINED
            if (self.__m_source is not None): 
                for wf in self.__m_source.morph.items: 
                    if ((isinstance(wf, MorphWordForm)) and wf.is_in_dictionary): 
                        res = (Utils.valToEnum((res) | (wf.gender), MorphGender))
            return res
        @gender.setter
        def gender(self, value) -> 'MorphGender':
            from pullenti.morph.MorphGender import MorphGender
            self.__m_gender = value
            if (self.__m_source is not None): 
                for i in range(self.__m_source.morph.items_count - 1, -1, -1):
                    if (((self.__m_source.morph.get_indexer_item(i).gender) & (value)) == (MorphGender.UNDEFINED)): 
                        self.__m_source.morph.remove_item(i)
            return value
        
        @property
        def _is_noun(self) -> bool:
            if (self.__m_source is not None): 
                for wf in self.__m_source.morph.items: 
                    if (wf.class0_.is_noun): 
                        return True
            return False
        
        @property
        def _is_adjective(self) -> bool:
            if (self.__m_source is not None): 
                for wf in self.__m_source.morph.items: 
                    if (wf.class0_.is_adjective): 
                        return True
            return False
        
        @property
        def morph_word_forms(self) -> typing.List['MorphWordForm']:
            from pullenti.morph.MorphWordForm import MorphWordForm
            res = list()
            if (self.__m_source is not None): 
                for wf in self.__m_source.morph.items: 
                    if (isinstance(wf, MorphWordForm)): 
                        res.append(Utils.asObjectOrNull(wf, MorphWordForm))
            return res
        
        def check_by_term(self, t : 'Term') -> bool:
            if (self.is_number): 
                return self.__m_number == t.__m_number
            if (self.__m_variants is not None and t.__m_variants is not None): 
                for v in self.__m_variants: 
                    if (v in t.__m_variants): 
                        return True
            return False
        
        def check_by_token(self, t : 'Token') -> bool:
            """ Сравнение с токеном
            
            Args:
                t(Token): 
            
            """
            return self.__check(t, 0)
        
        def __check(self, t : 'Token', lev : int) -> bool:
            from pullenti.ner.MetaToken import MetaToken
            from pullenti.ner.NumberToken import NumberToken
            from pullenti.ner.TextToken import TextToken
            if (lev > 10): 
                return False
            if (self.is_pattern_any): 
                return True
            if (isinstance(t, TextToken)): 
                if (self.is_number): 
                    return False
                for v in self.variants: 
                    if (t.is_value(v, None)): 
                        return True
                return False
            if (isinstance(t, NumberToken)): 
                if (self.is_number): 
                    return self.__m_number == t.value
                num = Utils.asObjectOrNull(t, NumberToken)
                if (num.begin_token == num.end_token): 
                    return self.__check(num.begin_token, lev)
                return False
            if (isinstance(t, MetaToken)): 
                mt = Utils.asObjectOrNull(t, MetaToken)
                if (mt.begin_token == mt.end_token): 
                    if (self.__check(mt.begin_token, lev + 1)): 
                        return True
            return False
        
        def check_by_pref_token(self, prefix : 'Term', t : 'TextToken') -> bool:
            if (prefix is None or prefix.__m_source is None or t is None): 
                return False
            pref = prefix.canonical_text
            tterm = t.term
            if (pref[0] != tterm[0]): 
                return False
            if (not tterm.startswith(pref)): 
                return False
            for v in self.variants: 
                if (t.is_value(pref + v, None)): 
                    return True
            return False
        
        def check_by_str_pref_token(self, pref : str, t : 'TextToken') -> bool:
            if (pref is None or t is None): 
                return False
            for v in self.variants: 
                if (v.startswith(pref) and len(v) > len(pref)): 
                    if (t.is_value(v[len(pref):], None)): 
                        return True
            return False
        
        @staticmethod
        def _new1962(_arg1 : 'TextToken', _arg2 : bool) -> 'Term':
            res = Termin.Term(_arg1)
            res.is_pattern_any = _arg2
            return res
    
    class Abridge:
        
        def __init__(self) -> None:
            self.parts = list()
            self.tail = None;
        
        def add_part(self, val : str, has_delim : bool=False) -> None:
            self.parts.append(Termin.AbridgePart._new562(val, has_delim))
        
        def __str__(self) -> str:
            if (self.tail is not None): 
                return "{0}-{1}".format(self.parts[0], self.tail)
            res = io.StringIO()
            for p in self.parts: 
                print(p, end="", file=res)
            return Utils.toStringStringIO(res)
        
        def try_attach(self, t0 : 'Token') -> 'TerminToken':
            from pullenti.ner.Token import Token
            from pullenti.ner.TextToken import TextToken
            from pullenti.ner.MetaToken import MetaToken
            from pullenti.ner.MorphCollection import MorphCollection
            from pullenti.ner.core.TerminToken import TerminToken
            t1 = Utils.asObjectOrNull(t0, TextToken)
            if (t1 is None): 
                return None
            if (t1.term != self.parts[0].value): 
                if (len(self.parts) != 1 or not t1.is_value(self.parts[0].value, None)): 
                    return None
            if (self.tail is None): 
                te = t1
                point = False
                if (te.next0_ is not None): 
                    if (te.next0_.is_char('.')): 
                        te = te.next0_
                        point = True
                    elif (len(self.parts) > 1): 
                        while te.next0_ is not None:
                            if (te.next0_.is_char_of("\\/.") or te.next0_.is_hiphen): 
                                te = te.next0_
                                point = True
                            else: 
                                break
                if (te is None): 
                    return None
                tt = te.next0_
                i = 1
                while i < len(self.parts): 
                    if (tt is not None and tt.whitespaces_before_count > 2): 
                        return None
                    if (tt is not None and ((tt.is_hiphen or tt.is_char_of("\\/.")))): 
                        tt = tt.next0_
                    elif (not point and self.parts[i - 1].has_delim): 
                        return None
                    if (tt is None): 
                        return None
                    if (isinstance(tt, TextToken)): 
                        tet = Utils.asObjectOrNull(tt, TextToken)
                        if (tet.term != self.parts[i].value): 
                            if (not tet.is_value(self.parts[i].value, None)): 
                                return None
                    elif (isinstance(tt, MetaToken)): 
                        mt = Utils.asObjectOrNull(tt, MetaToken)
                        if (mt.begin_token != mt.end_token): 
                            return None
                        if (not mt.begin_token.is_value(self.parts[i].value, None)): 
                            return None
                    te = tt
                    if (tt.next0_ is not None and ((tt.next0_.is_char_of(".\\/") or tt.next0_.is_hiphen))): 
                        tt = tt.next0_
                        point = True
                        if (tt is not None): 
                            te = tt
                    else: 
                        point = False
                    tt = tt.next0_
                    i += 1
                res = TerminToken._new563(t0, te, t0 == te)
                if (point): 
                    res.morph = MorphCollection()
                return res
            t1 = (Utils.asObjectOrNull(t1.next0_, TextToken))
            if (t1 is None or not t1.is_char_of("-\\/")): 
                return None
            t1 = (Utils.asObjectOrNull(t1.next0_, TextToken))
            if (t1 is None): 
                return None
            if (t1.term[0] != self.tail[0]): 
                return None
            return TerminToken(t0, t1)
    
    class AbridgePart:
        
        def __init__(self) -> None:
            self.value = None;
            self.has_delim = False
        
        def __str__(self) -> str:
            if (self.has_delim): 
                return self.value + "."
            else: 
                return self.value
        
        @staticmethod
        def _new562(_arg1 : str, _arg2 : bool) -> 'AbridgePart':
            res = Termin.AbridgePart()
            res.value = _arg1
            res.has_delim = _arg2
            return res
        
        @staticmethod
        def _new564(_arg1 : str) -> 'AbridgePart':
            res = Termin.AbridgePart()
            res.value = _arg1
            return res
    
    def __init__(self, source : str=None, lang_ : 'MorphLang'=None, source_is_normal : bool=False) -> None:
        """ Создать термин из строки с добавлением всех морфологических вариантов написания
        
        Args:
            source(str): строка
            lang_(MorphLang): возможный язык (null, если совпадает с текущим языком анализируемого текста)
            source_is_normal(bool): при true морфварианты не добавляются
        (эквивалентно вызову InitByNormalText)
        """
        self.terms = list()
        self.additional_vars = None
        self.__m_canonic_text = None;
        self.ignore_terms_order = False
        self.acronym = None;
        self.acronym_smart = None;
        self.acronym_can_be_lower = False
        self.abridges = None;
        self.lang = MorphLang()
        self.tag = None;
        self.tag2 = None;
        self.tag3 = None;
        if (source is None): 
            return
        if (source_is_normal or Termin.ASSIGN_ALL_TEXTS_AS_NORMAL): 
            self.init_by_normal_text(source, lang_)
            return
        toks = MorphologyService.process(source, lang_, None)
        if (toks is not None): 
            i = 0
            while i < len(toks): 
                tt = TextToken(toks[i], None)
                self.terms.append(Termin.Term(tt, not source_is_normal))
                i += 1
        self.lang = MorphLang()
        if (lang_ is not None): 
            self.lang.value = lang_.value
    
    ASSIGN_ALL_TEXTS_AS_NORMAL = False
    # Используется внутренним образом (для ускорения Питона)
    
    def init_by_normal_text(self, text : str, lang_ : 'MorphLang'=None) -> None:
        """ Быстрая инициализация без морф.вариантов, производится только
        токенизация текста. Используется для ускорения работы со словарём в случае,
        когда изначально известно, что на входе уже нормализованные строки.
        
        Args:
            text(str): исходно нормализованный текст
            lang_(MorphLang): возможный язык (можно null)
        """
        if (Utils.isNullOrEmpty(text)): 
            return
        text = text.upper()
        if (text.find('\'') >= 0): 
            text = text.replace("'", "")
        tok = False
        sp = False
        for ch in text: 
            if (not str.isalpha(ch)): 
                if (ch == ' '): 
                    sp = True
                else: 
                    tok = True
                    break
        if (not tok and not sp): 
            tt = TextToken(None, None)
            tt.term = text
            self.terms.append(Termin.Term(tt, False))
        elif (not tok and sp): 
            wrds = Utils.splitString(text, ' ', False)
            i = 0
            first_pass3560 = True
            while True:
                if first_pass3560: first_pass3560 = False
                else: i += 1
                if (not (i < len(wrds))): break
                if (Utils.isNullOrEmpty(wrds[i])): 
                    continue
                tt = TextToken(None, None)
                tt.term = wrds[i]
                self.terms.append(Termin.Term(tt, False))
        else: 
            toks = MorphologyService.tokenize(text)
            if (toks is not None): 
                i = 0
                while i < len(toks): 
                    tt = TextToken(toks[i], None)
                    self.terms.append(Termin.Term(tt, False))
                    i += 1
        self.lang = MorphLang()
        if (lang_ is not None): 
            self.lang.value = lang_.value
    
    def init_by(self, begin : 'Token', end : 'Token', tag_ : object=None, add_lemma_variant : bool=False) -> None:
        if (tag_ is not None): 
            self.tag = tag_
        t = begin
        while t is not None: 
            if (self.lang.is_undefined and not t.morph.language.is_undefined): 
                self.lang = t.morph.language
            tt = Utils.asObjectOrNull(t, TextToken)
            if (tt is not None): 
                self.terms.append(Termin.Term(tt, add_lemma_variant))
            elif (isinstance(t, NumberToken)): 
                self.terms.append(Termin.Term(None, False, t.value))
            if (t == end): 
                break
            t = t.next0_
    
    def add_variant(self, var : str, source_is_normal : bool=False) -> None:
        """ Добавить дополнительный вариант полного написания
        
        Args:
            var(str): строка варианта
            source_is_normal(bool): при true морфварианты не добавляются, иначе добавляются
        """
        if (self.additional_vars is None): 
            self.additional_vars = list()
        self.additional_vars.append(Termin(var, MorphLang.UNKNOWN, source_is_normal))
    
    def add_variant_term(self, t : 'Termin') -> None:
        """ Добавить дополнительный вариант написания
        
        Args:
            t(Termin): термин
        """
        if (self.additional_vars is None): 
            self.additional_vars = list()
        self.additional_vars.append(t)
    
    @property
    def canonic_text(self) -> str:
        """ Канонический текст термина. Если явно не задан, то создаётся автоматически. """
        if (self.__m_canonic_text is not None): 
            return self.__m_canonic_text
        if (len(self.terms) > 0): 
            tmp = io.StringIO()
            for v in self.terms: 
                if (tmp.tell() > 0): 
                    print(' ', end="", file=tmp)
                print(v.canonical_text, end="", file=tmp)
            self.__m_canonic_text = Utils.toStringStringIO(tmp)
        elif (self.acronym is not None): 
            self.__m_canonic_text = self.acronym
        return Utils.ifNotNull(self.__m_canonic_text, "?")
    @canonic_text.setter
    def canonic_text(self, value) -> str:
        self.__m_canonic_text = value
        return value
    
    def set_std_acronim(self, smart : bool) -> None:
        """ Установить стандартную аббревиатуру """
        acr = io.StringIO()
        for t in self.terms: 
            s = t.canonical_text
            if (Utils.isNullOrEmpty(s)): 
                continue
            if (len(s) > 2): 
                print(s[0], end="", file=acr)
        if (acr.tell() > 1): 
            if (smart): 
                self.acronym_smart = Utils.toStringStringIO(acr)
            else: 
                self.acronym = Utils.toStringStringIO(acr)
    
    def add_abridge(self, abr : str) -> 'Abridge':
        """ Добавить сокращение в термин
        
        Args:
            abr(str): сокращение, например, "нас.п." или "д-р наук"
        
        Returns:
            Abridge: разобранное сокращение, добавленное в термин
        """
        if (abr == "В/ГОР"): 
            pass
        a = Termin.Abridge()
        if (self.abridges is None): 
            self.abridges = list()
        i = 0
        while i < len(abr): 
            if (not str.isalpha(abr[i])): 
                break
            i += 1
        if (i == 0): 
            return None
        a.parts.append(Termin.AbridgePart._new564(abr[0:0+i].upper()))
        self.abridges.append(a)
        if (((i + 1) < len(abr)) and abr[i] == '-'): 
            a.tail = abr[i + 1:].upper()
        elif (i < len(abr)): 
            if (not Utils.isWhitespace(abr[i])): 
                a.parts[0].has_delim = True
            while i < len(abr): 
                if (str.isalpha(abr[i])): 
                    j = (i + 1)
                    while j < len(abr): 
                        if (not str.isalpha(abr[j])): 
                            break
                        j += 1
                    p = Termin.AbridgePart._new564(abr[i:i+j - i].upper())
                    if (j < len(abr)): 
                        if (not Utils.isWhitespace(abr[j])): 
                            p.has_delim = True
                    a.parts.append(p)
                    i = j
                i += 1
        return a
    
    @property
    def gender(self) -> 'MorphGender':
        """ Род (вычисляется по первому слову термина) """
        if (len(self.terms) > 0): 
            if (len(self.terms) > 0 and self.terms[0]._is_adjective and self.terms[len(self.terms) - 1]._is_noun): 
                return self.terms[len(self.terms) - 1].gender
            return self.terms[0].gender
        else: 
            return MorphGender.UNDEFINED
    @gender.setter
    def gender(self, value) -> 'MorphGender':
        if (len(self.terms) > 0): 
            self.terms[0].gender = value
        return value
    
    def copy_to(self, dst : 'Termin') -> None:
        dst.terms = self.terms
        dst.ignore_terms_order = self.ignore_terms_order
        dst.acronym = self.acronym
        dst.abridges = self.abridges
        dst.lang = self.lang
        dst.__m_canonic_text = self.__m_canonic_text
    
    def __str__(self) -> str:
        res = io.StringIO()
        if (len(self.terms) > 0): 
            i = 0
            while i < len(self.terms): 
                if (i > 0): 
                    print(' ', end="", file=res)
                print(self.terms[i].canonical_text, end="", file=res)
                i += 1
        if (self.acronym is not None): 
            if (res.tell() > 0): 
                print(", ", end="", file=res)
            print(self.acronym, end="", file=res)
        if (self.acronym_smart is not None): 
            if (res.tell() > 0): 
                print(", ", end="", file=res)
            print(self.acronym_smart, end="", file=res)
        if (self.abridges is not None): 
            for a in self.abridges: 
                if (res.tell() > 0): 
                    print(", ", end="", file=res)
                print(a, end="", file=res)
        return Utils.toStringStringIO(res)
    
    M_STD_ABRIDE_PREFIXES = None
    
    def add_std_abridges(self) -> None:
        if (len(self.terms) != 2): 
            return
        first = self.terms[0].canonical_text
        i = 0
        while i < len(Termin.M_STD_ABRIDE_PREFIXES): 
            if (first.startswith(Termin.M_STD_ABRIDE_PREFIXES[i])): 
                break
            i += 1
        if (i >= len(Termin.M_STD_ABRIDE_PREFIXES)): 
            return
        head = Termin.M_STD_ABRIDE_PREFIXES[i]
        second = self.terms[1].canonical_text
        i = 0
        while i < len(head): 
            if (not LanguageHelper.is_cyrillic_vowel(head[i])): 
                a = Termin.Abridge()
                a.add_part(head[0:0+i + 1], False)
                a.add_part(second, False)
                if (self.abridges is None): 
                    self.abridges = list()
                self.abridges.append(a)
            i += 1
    
    def add_all_abridges(self, tail_len : int=0, max_first_len : int=0, min_first_len : int=0) -> None:
        """ Добавить все сокращения (с первой буквы до любого согласного) """
        if (len(self.terms) < 1): 
            return
        txt = self.terms[0].canonical_text
        if (tail_len == 0): 
            for i in range(len(txt) - 2, -1, -1):
                if (not LanguageHelper.is_cyrillic_vowel(txt[i])): 
                    if (min_first_len > 0 and (i < (min_first_len - 1))): 
                        break
                    a = Termin.Abridge()
                    a.add_part(txt[0:0+i + 1], False)
                    j = 1
                    while j < len(self.terms): 
                        a.add_part(self.terms[j].canonical_text, False)
                        j += 1
                    if (self.abridges is None): 
                        self.abridges = list()
                    self.abridges.append(a)
        else: 
            tail = txt[len(txt) - tail_len:]
            txt = txt[0:0+len(txt) - tail_len - 1]
            for i in range(len(txt) - 2, -1, -1):
                if (max_first_len > 0 and i >= max_first_len): 
                    pass
                elif (not LanguageHelper.is_cyrillic_vowel(txt[i])): 
                    self.add_abridge("{0}-{1}".format(txt[0:0+i + 1], tail))
    
    def _get_hash_variants(self) -> typing.List[str]:
        res = list()
        j = 0
        while j < len(self.terms): 
            for v in self.terms[j].variants: 
                if (not v in res): 
                    res.append(v)
            if (((j + 2) < len(self.terms)) and self.terms[j + 1].is_hiphen): 
                pref = self.terms[j].canonical_text
                for v in self.terms[j + 2].variants: 
                    if (not pref + v in res): 
                        res.append(pref + v)
            if (not self.ignore_terms_order): 
                break
            j += 1
        if (self.acronym is not None): 
            if (not self.acronym in res): 
                res.append(self.acronym)
        if (self.acronym_smart is not None): 
            if (not self.acronym_smart in res): 
                res.append(self.acronym_smart)
        if (self.abridges is not None): 
            for a in self.abridges: 
                if (len(a.parts[0].value) > 1): 
                    if (not a.parts[0].value in res): 
                        res.append(a.parts[0].value)
        return res
    
    def is_equal(self, t : 'Termin') -> bool:
        if (t.acronym is not None): 
            if (self.acronym == t.acronym or self.acronym_smart == t.acronym): 
                return True
        if (t.acronym_smart is not None): 
            if (self.acronym == t.acronym_smart or self.acronym_smart == t.acronym_smart): 
                return True
        if (len(t.terms) != len(self.terms)): 
            return False
        i = 0
        while i < len(self.terms): 
            if (not self.terms[i].check_by_term(t.terms[i])): 
                return False
            i += 1
        return True
    
    def try_parse(self, t0 : 'Token', pars : 'TerminParseAttr'=TerminParseAttr.NO) -> 'TerminToken':
        """ Попробовать привязать термин
        
        Args:
            t0(Token): начальный токен
            pars(TerminParseAttr): дополнительные параметры привязки
        
        Returns:
            TerminToken: метатокен привязки или null
        """
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.ner.core.BracketHelper import BracketHelper
        if (t0 is None): 
            return None
        term = None
        if (isinstance(t0, TextToken)): 
            term = t0.term
        if (self.acronym_smart is not None and (((pars) & (TerminParseAttr.FULLWORDSONLY))) == (TerminParseAttr.NO) and term is not None): 
            if (self.acronym_smart == term): 
                if (t0.next0_ is not None and t0.next0_.is_char('.') and not t0.is_whitespace_after): 
                    return TerminToken._new409(t0, t0.next0_, self)
                else: 
                    return TerminToken._new409(t0, t0, self)
            t1 = Utils.asObjectOrNull(t0, TextToken)
            tt = Utils.asObjectOrNull(t0, TextToken)
            i = 0
            while i < len(self.acronym): 
                if (tt is None): 
                    break
                term1 = tt.term
                if (len(term1) != 1 or tt.is_whitespace_after): 
                    break
                if (i > 0 and tt.is_whitespace_before): 
                    break
                if (term1[0] != self.acronym[i]): 
                    break
                if (tt.next0_ is None or not tt.next0_.is_char('.')): 
                    break
                t1 = (Utils.asObjectOrNull(tt.next0_, TextToken))
                tt = (Utils.asObjectOrNull(tt.next0_.next0_, TextToken))
                i += 1
            if (i >= len(self.acronym)): 
                return TerminToken._new409(t0, t1, self)
        if (self.acronym is not None and term is not None and self.acronym == term): 
            if (t0.chars.is_all_upper or self.acronym_can_be_lower or ((not t0.chars.is_all_lower and len(term) >= 3))): 
                return TerminToken._new409(t0, t0, self)
        if (self.acronym is not None and t0.chars.is_last_lower and t0.length_char > 3): 
            if (t0.is_value(self.acronym, None)): 
                return TerminToken._new409(t0, t0, self)
        cou = 0
        i = 0
        while i < len(self.terms): 
            if (self.terms[i].is_hiphen): 
                cou -= 1
            else: 
                cou += 1
            i += 1
        if (len(self.terms) > 0 and ((not self.ignore_terms_order or cou == 1))): 
            t1 = t0
            tt = t0
            e0_ = None
            eup = None
            ok = True
            mc = None
            dont_change_mc = False
            i = 0
            first_pass3561 = True
            while True:
                if first_pass3561: first_pass3561 = False
                else: i += 1
                if (not (i < len(self.terms))): break
                if (self.terms[i].is_hiphen): 
                    continue
                if (tt is not None and tt.is_hiphen and i > 0): 
                    tt = tt.next0_
                if (i > 0 and tt is not None): 
                    if ((((pars) & (TerminParseAttr.IGNOREBRACKETS))) != (TerminParseAttr.NO) and not tt.chars.is_letter and BracketHelper.is_bracket(tt, False)): 
                        tt = tt.next0_
                if (((((pars) & (TerminParseAttr.CANBEGEOOBJECT))) != (TerminParseAttr.NO) and i > 0 and (isinstance(tt, ReferentToken))) and tt.get_referent().type_name == "GEO"): 
                    tt = tt.next0_
                if ((isinstance(tt, ReferentToken)) and e0_ is None): 
                    eup = tt
                    e0_ = tt.end_token
                    tt = tt.begin_token
                if (tt is None): 
                    ok = False
                    break
                if (not self.terms[i].check_by_token(tt)): 
                    if (tt.next0_ is not None and tt.is_char_of(".,") and self.terms[i].check_by_token(tt.next0_)): 
                        tt = tt.next0_
                    elif (((i > 0 and tt.next0_ is not None and (isinstance(tt, TextToken))) and ((tt.morph.class0_.is_preposition or MiscHelper.is_eng_article(tt))) and self.terms[i].check_by_token(tt.next0_)) and not self.terms[i - 1].is_pattern_any): 
                        tt = tt.next0_
                    else: 
                        ok = False
                        if (((i + 2) < len(self.terms)) and self.terms[i + 1].is_hiphen and self.terms[i + 2].check_by_pref_token(self.terms[i], Utils.asObjectOrNull(tt, TextToken))): 
                            i += 2
                            ok = True
                        elif (((not tt.is_whitespace_after and tt.next0_ is not None and (isinstance(tt, TextToken))) and tt.length_char == 1 and tt.next0_.is_char_of("\"'`’“”")) and not tt.next0_.is_whitespace_after and (isinstance(tt.next0_.next0_, TextToken))): 
                            if (self.terms[i].check_by_str_pref_token(tt.term, Utils.asObjectOrNull(tt.next0_.next0_, TextToken))): 
                                ok = True
                                tt = tt.next0_.next0_
                        if (not ok): 
                            if (i > 0 and (((pars) & (TerminParseAttr.IGNORESTOPWORDS))) != (TerminParseAttr.NO)): 
                                if (isinstance(tt, TextToken)): 
                                    if (not tt.chars.is_letter): 
                                        tt = tt.next0_
                                        i -= 1
                                        continue
                                    mc1 = tt.get_morph_class_in_dictionary()
                                    if (mc1.is_conjunction or mc1.is_preposition): 
                                        tt = tt.next0_
                                        i -= 1
                                        continue
                                if (isinstance(tt, NumberToken)): 
                                    tt = tt.next0_
                                    i -= 1
                                    continue
                            break
                if (tt.morph.items_count > 0 and not dont_change_mc): 
                    mc = MorphCollection(tt.morph)
                    if (((mc.class0_.is_noun or mc.class0_.is_verb)) and not mc.class0_.is_adjective): 
                        if (((i + 1) < len(self.terms)) and self.terms[i + 1].is_hiphen): 
                            pass
                        else: 
                            dont_change_mc = True
                if (tt.morph.class0_.is_preposition or tt.morph.class0_.is_conjunction): 
                    dont_change_mc = True
                if (tt == e0_): 
                    tt = eup
                    eup = (None)
                    e0_ = (None)
                if (e0_ is None): 
                    t1 = tt
                tt = tt.next0_
            if (ok and i >= len(self.terms)): 
                if (t1.next0_ is not None and t1.next0_.is_char('.') and self.abridges is not None): 
                    for a in self.abridges: 
                        if (a.try_attach(t0) is not None): 
                            t1 = t1.next0_
                            break
                if (t0 != t1 and t0.morph.class0_.is_adjective): 
                    npt = NounPhraseHelper.try_parse(t0, NounPhraseParseAttr.NO, 0, None)
                    if (npt is not None and npt.end_char <= t1.end_char): 
                        mc = npt.morph
                return TerminToken._new571(t0, t1, mc)
        if (len(self.terms) > 1 and self.ignore_terms_order): 
            terms_ = list(self.terms)
            t1 = t0
            tt = t0
            while len(terms_) > 0:
                if (tt != t0 and tt is not None and tt.is_hiphen): 
                    tt = tt.next0_
                if (tt is None): 
                    break
                j = 0
                while j < len(terms_): 
                    if (terms_[j].check_by_token(tt)): 
                        break
                    j += 1
                if (j >= len(terms_)): 
                    if (tt != t0 and (((pars) & (TerminParseAttr.IGNORESTOPWORDS))) != (TerminParseAttr.NO)): 
                        if (isinstance(tt, TextToken)): 
                            if (not tt.chars.is_letter): 
                                tt = tt.next0_
                                continue
                            mc1 = tt.get_morph_class_in_dictionary()
                            if (mc1.is_conjunction or mc1.is_preposition): 
                                tt = tt.next0_
                                continue
                        if (isinstance(tt, NumberToken)): 
                            tt = tt.next0_
                            continue
                    break
                del terms_[j]
                t1 = tt
                tt = tt.next0_
            for i in range(len(terms_) - 1, -1, -1):
                if (terms_[i].is_hiphen): 
                    del terms_[i]
            if (len(terms_) == 0): 
                return TerminToken(t0, t1)
        if (self.abridges is not None and (((pars) & (TerminParseAttr.FULLWORDSONLY))) == (TerminParseAttr.NO)): 
            res = None
            for a in self.abridges: 
                r = a.try_attach(t0)
                if (r is None): 
                    continue
                if (r.abridge_without_point and len(self.terms) > 0): 
                    if (not (isinstance(t0, TextToken))): 
                        continue
                    if (a.parts[0].value != t0.term): 
                        continue
                if (res is None or (res.length_char < r.length_char)): 
                    res = r
            if (res is not None): 
                return res
        return None
    
    def try_parse_sim(self, t0 : 'Token', simd : float, pars : 'TerminParseAttr'=TerminParseAttr.NO) -> 'TerminToken':
        # Попробовать привязать термин с использованием "похожести"
        if (t0 is None): 
            return None
        if (simd >= 1 or (simd < 0.05)): 
            return self.try_parse(t0, pars)
        term = None
        if (isinstance(t0, TextToken)): 
            term = t0.term
        if (self.acronym_smart is not None and (((pars) & (TerminParseAttr.FULLWORDSONLY))) == (TerminParseAttr.NO) and term is not None): 
            if (self.acronym_smart == term): 
                if (t0.next0_ is not None and t0.next0_.is_char('.') and not t0.is_whitespace_after): 
                    return TerminToken._new409(t0, t0.next0_, self)
                else: 
                    return TerminToken._new409(t0, t0, self)
            t1 = Utils.asObjectOrNull(t0, TextToken)
            tt = Utils.asObjectOrNull(t0, TextToken)
            i = 0
            while i < len(self.acronym): 
                if (tt is None): 
                    break
                term1 = tt.term
                if (len(term1) != 1 or tt.is_whitespace_after): 
                    break
                if (i > 0 and tt.is_whitespace_before): 
                    break
                if (term1[0] != self.acronym[i]): 
                    break
                if (tt.next0_ is None or not tt.next0_.is_char('.')): 
                    break
                t1 = (Utils.asObjectOrNull(tt.next0_, TextToken))
                tt = (Utils.asObjectOrNull(tt.next0_.next0_, TextToken))
                i += 1
            if (i >= len(self.acronym)): 
                return TerminToken._new409(t0, t1, self)
        if (self.acronym is not None and term is not None and self.acronym == term): 
            if (t0.chars.is_all_upper or self.acronym_can_be_lower or ((not t0.chars.is_all_lower and len(term) >= 3))): 
                return TerminToken._new409(t0, t0, self)
        if (self.acronym is not None and t0.chars.is_last_lower and t0.length_char > 3): 
            if (t0.is_value(self.acronym, None)): 
                return TerminToken._new409(t0, t0, self)
        if (len(self.terms) > 0): 
            t1 = None
            tt = t0
            mc = None
            term_ind = -1
            terms_len = 0
            tk_cnt = 0
            terms_found_cnt = 0
            wr_oder = False
            for it in self.terms: 
                if ((len(it.canonical_text) < 2) or it.is_hiphen or it.is_point): 
                    terms_len += 0.3
                elif (it.is_number or it.is_pattern_any): 
                    terms_len += 0.7
                else: 
                    terms_len += (1)
            max_tks_len = terms_len / simd
            curjm = simd
            terms_found = list()
            while tt is not None and (tk_cnt < max_tks_len) and (terms_found_cnt < terms_len):
                mcls = None
                ttt = Utils.asObjectOrNull(tt, TextToken)
                mm = False
                if (tt.length_char < 2): 
                    tk_cnt += 0.3
                elif (isinstance(tt, NumberToken)): 
                    tk_cnt += 0.7
                elif (ttt is None): 
                    tk_cnt += 1
                else: 
                    mcls = ttt.morph.class0_
                    mm = (((mcls.is_conjunction or mcls.is_preposition or mcls.is_pronoun) or mcls.is_misc or mcls.is_undefined))
                    if (mm): 
                        tk_cnt += 0.3
                    else: 
                        tk_cnt += (1)
                i = 0
                while i < len(self.terms): 
                    if (not i in terms_found): 
                        trm = self.terms[i]
                        if (trm.is_pattern_any): 
                            terms_found_cnt += 0.7
                            terms_found.append(i)
                            break
                        elif (len(trm.canonical_text) < 2): 
                            terms_found_cnt += 0.3
                            terms_found.append(i)
                            break
                        elif (trm.check_by_token(tt)): 
                            terms_found.append(i)
                            if (mm): 
                                terms_len -= 0.7
                                terms_found_cnt += 0.3
                            else: 
                                terms_found_cnt += (0.7 if trm.is_number else 1)
                            if (not wr_oder): 
                                if (i < term_ind): 
                                    wr_oder = True
                                else: 
                                    term_ind = i
                            break
                    i += 1
                if (terms_found_cnt < 0.2): 
                    return None
                newjm = (terms_found_cnt / (((tk_cnt + terms_len) - terms_found_cnt))) * (((0.7 if wr_oder else 1)))
                if (curjm < newjm): 
                    t1 = tt
                    curjm = newjm
                tt = tt.next0_
            if (t1 is None): 
                return None
            if (t0.morph.items_count > 0): 
                mc = MorphCollection(t0.morph)
            return TerminToken._new577(t0, t1, mc, self)
        if (self.abridges is not None and (((pars) & (TerminParseAttr.FULLWORDSONLY))) == (TerminParseAttr.NO)): 
            res = None
            for a in self.abridges: 
                r = a.try_attach(t0)
                if (r is None): 
                    continue
                if (r.abridge_without_point and len(self.terms) > 0): 
                    if (not (isinstance(t0, TextToken))): 
                        continue
                    if (a.parts[0].value != t0.term): 
                        continue
                if (res is None or (res.length_char < r.length_char)): 
                    res = r
            if (res is not None): 
                return res
        return None
    
    @staticmethod
    def _new95(_arg1 : str, _arg2 : str) -> 'Termin':
        res = Termin(_arg1)
        res.acronym = _arg2
        return res
    
    @staticmethod
    def _new100(_arg1 : str, _arg2 : object) -> 'Termin':
        res = Termin(_arg1)
        res.tag = _arg2
        return res
    
    @staticmethod
    def _new101(_arg1 : str, _arg2 : object, _arg3 : 'MorphLang') -> 'Termin':
        res = Termin(_arg1)
        res.tag = _arg2
        res.lang = _arg3
        return res
    
    @staticmethod
    def _new102(_arg1 : str, _arg2 : object, _arg3 : object) -> 'Termin':
        res = Termin(_arg1)
        res.tag = _arg2
        res.tag2 = _arg3
        return res
    
    @staticmethod
    def _new124(_arg1 : str, _arg2 : str, _arg3 : object) -> 'Termin':
        res = Termin(_arg1)
        res.canonic_text = _arg2
        res.tag = _arg3
        return res
    
    @staticmethod
    def _new126(_arg1 : str, _arg2 : object, _arg3 : str) -> 'Termin':
        res = Termin(_arg1)
        res.tag = _arg2
        res.acronym = _arg3
        return res
    
    @staticmethod
    def _new163(_arg1 : str, _arg2 : str, _arg3 : bool) -> 'Termin':
        res = Termin(_arg1)
        res.acronym = _arg2
        res.acronym_can_be_lower = _arg3
        return res
    
    @staticmethod
    def _new241(_arg1 : str, _arg2 : object, _arg3 : 'MorphGender') -> 'Termin':
        res = Termin(_arg1)
        res.tag = _arg2
        res.gender = _arg3
        return res
    
    @staticmethod
    def _new242(_arg1 : str, _arg2 : object, _arg3 : 'MorphLang', _arg4 : 'MorphGender') -> 'Termin':
        res = Termin(_arg1)
        res.tag = _arg2
        res.lang = _arg3
        res.gender = _arg4
        return res
    
    @staticmethod
    def _new244(_arg1 : str, _arg2 : object, _arg3 : object, _arg4 : 'MorphGender') -> 'Termin':
        res = Termin(_arg1)
        res.tag = _arg2
        res.tag2 = _arg3
        res.gender = _arg4
        return res
    
    @staticmethod
    def _new245(_arg1 : str, _arg2 : object, _arg3 : 'MorphLang', _arg4 : object, _arg5 : 'MorphGender') -> 'Termin':
        res = Termin(_arg1)
        res.tag = _arg2
        res.lang = _arg3
        res.tag2 = _arg4
        res.gender = _arg5
        return res
    
    @staticmethod
    def _new272(_arg1 : str, _arg2 : object, _arg3 : str, _arg4 : object, _arg5 : 'MorphGender') -> 'Termin':
        res = Termin(_arg1)
        res.tag = _arg2
        res.acronym = _arg3
        res.tag2 = _arg4
        res.gender = _arg5
        return res
    
    @staticmethod
    def _new285(_arg1 : str, _arg2 : str, _arg3 : object, _arg4 : object, _arg5 : 'MorphGender') -> 'Termin':
        res = Termin(_arg1)
        res.canonic_text = _arg2
        res.tag = _arg3
        res.tag2 = _arg4
        res.gender = _arg5
        return res
    
    @staticmethod
    def _new289(_arg1 : str, _arg2 : str, _arg3 : object, _arg4 : 'MorphLang', _arg5 : object, _arg6 : 'MorphGender') -> 'Termin':
        res = Termin(_arg1)
        res.canonic_text = _arg2
        res.tag = _arg3
        res.lang = _arg4
        res.tag2 = _arg5
        res.gender = _arg6
        return res
    
    @staticmethod
    def _new290(_arg1 : str, _arg2 : str, _arg3 : object, _arg4 : 'MorphGender') -> 'Termin':
        res = Termin(_arg1)
        res.acronym = _arg2
        res.tag = _arg3
        res.gender = _arg4
        return res
    
    @staticmethod
    def _new294(_arg1 : str, _arg2 : object, _arg3 : str, _arg4 : 'MorphGender') -> 'Termin':
        res = Termin(_arg1)
        res.tag = _arg2
        res.acronym = _arg3
        res.gender = _arg4
        return res
    
    @staticmethod
    def _new313(_arg1 : object, _arg2 : bool) -> 'Termin':
        res = Termin()
        res.tag = _arg1
        res.ignore_terms_order = _arg2
        return res
    
    @staticmethod
    def _new388(_arg1 : str, _arg2 : 'MorphLang', _arg3 : object) -> 'Termin':
        res = Termin(_arg1, _arg2)
        res.tag = _arg3
        return res
    
    @staticmethod
    def _new418(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : str, _arg5 : object) -> 'Termin':
        res = Termin(_arg1, _arg2, _arg3)
        res.canonic_text = _arg4
        res.tag = _arg5
        return res
    
    @staticmethod
    def _new530(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : object) -> 'Termin':
        res = Termin(_arg1, _arg2, _arg3)
        res.tag = _arg4
        return res
    
    @staticmethod
    def _new654(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : str) -> 'Termin':
        res = Termin(_arg1, _arg2, _arg3)
        res.canonic_text = _arg4
        return res
    
    @staticmethod
    def _new901(_arg1 : str, _arg2 : 'MorphLang') -> 'Termin':
        res = Termin(_arg1)
        res.lang = _arg2
        return res
    
    @staticmethod
    def _new913(_arg1 : str, _arg2 : 'MorphLang', _arg3 : object, _arg4 : object) -> 'Termin':
        res = Termin(_arg1, _arg2)
        res.tag = _arg3
        res.tag2 = _arg4
        return res
    
    @staticmethod
    def _new917(_arg1 : str, _arg2 : 'MorphLang', _arg3 : object, _arg4 : str) -> 'Termin':
        res = Termin(_arg1, _arg2)
        res.tag = _arg3
        res.acronym = _arg4
        return res
    
    @staticmethod
    def _new923(_arg1 : str, _arg2 : str, _arg3 : 'MorphLang', _arg4 : object) -> 'Termin':
        res = Termin(_arg1)
        res.canonic_text = _arg2
        res.lang = _arg3
        res.tag = _arg4
        return res
    
    @staticmethod
    def _new926(_arg1 : str, _arg2 : object, _arg3 : str, _arg4 : object) -> 'Termin':
        res = Termin(_arg1)
        res.tag = _arg2
        res.acronym = _arg3
        res.tag2 = _arg4
        return res
    
    @staticmethod
    def _new928(_arg1 : str, _arg2 : 'MorphLang', _arg3 : object, _arg4 : str, _arg5 : object) -> 'Termin':
        res = Termin(_arg1, _arg2)
        res.tag = _arg3
        res.acronym = _arg4
        res.tag2 = _arg5
        return res
    
    @staticmethod
    def _new948(_arg1 : str, _arg2 : str, _arg3 : object, _arg4 : object) -> 'Termin':
        res = Termin(_arg1)
        res.acronym = _arg2
        res.tag = _arg3
        res.tag2 = _arg4
        return res
    
    @staticmethod
    def _new997(_arg1 : str, _arg2 : 'MorphLang', _arg3 : str, _arg4 : object) -> 'Termin':
        res = Termin(_arg1, _arg2)
        res.canonic_text = _arg3
        res.tag = _arg4
        return res
    
    @staticmethod
    def _new1116(_arg1 : str, _arg2 : str) -> 'Termin':
        res = Termin(_arg1)
        res.canonic_text = _arg2
        return res
    
    @staticmethod
    def _new1152(_arg1 : str, _arg2 : 'MorphLang', _arg3 : str) -> 'Termin':
        res = Termin(_arg1, _arg2)
        res.canonic_text = _arg3
        return res
    
    @staticmethod
    def _new1254(_arg1 : str, _arg2 : 'MorphLang') -> 'Termin':
        res = Termin()
        res.acronym = _arg1
        res.lang = _arg2
        return res
    
    @staticmethod
    def _new1506(_arg1 : str, _arg2 : 'MorphLang', _arg3 : str) -> 'Termin':
        res = Termin(_arg1, _arg2)
        res.acronym = _arg3
        return res
    
    @staticmethod
    def _new2352(_arg1 : str, _arg2 : object) -> 'Termin':
        res = Termin(_arg1)
        res.tag2 = _arg2
        return res
    
    @staticmethod
    def _new2616(_arg1 : str, _arg2 : bool) -> 'Termin':
        res = Termin(_arg1)
        res.ignore_terms_order = _arg2
        return res
    
    @staticmethod
    def _new2638(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : object) -> 'Termin':
        res = Termin(_arg1, _arg2, _arg3)
        res.tag2 = _arg4
        return res
    
    @staticmethod
    def _new2726(_arg1 : str, _arg2 : str, _arg3 : object, _arg4 : str) -> 'Termin':
        res = Termin(_arg1)
        res.canonic_text = _arg2
        res.tag = _arg3
        res.acronym = _arg4
        return res
    
    @staticmethod
    def _new2736(_arg1 : str, _arg2 : str, _arg3 : object, _arg4 : str, _arg5 : bool) -> 'Termin':
        res = Termin(_arg1)
        res.canonic_text = _arg2
        res.tag = _arg3
        res.acronym = _arg4
        res.acronym_can_be_lower = _arg5
        return res
    
    @staticmethod
    def _new2749(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : str, _arg5 : object, _arg6 : object) -> 'Termin':
        res = Termin(_arg1, _arg2, _arg3)
        res.canonic_text = _arg4
        res.tag = _arg5
        res.tag2 = _arg6
        return res
    
    @staticmethod
    def _new2750(_arg1 : str, _arg2 : str, _arg3 : object, _arg4 : object) -> 'Termin':
        res = Termin(_arg1)
        res.canonic_text = _arg2
        res.tag = _arg3
        res.tag2 = _arg4
        return res
    
    @staticmethod
    def _new2753(_arg1 : str, _arg2 : str, _arg3 : str, _arg4 : object, _arg5 : object, _arg6 : bool) -> 'Termin':
        res = Termin(_arg1)
        res.canonic_text = _arg2
        res.acronym = _arg3
        res.tag = _arg4
        res.tag2 = _arg5
        res.acronym_can_be_lower = _arg6
        return res
    
    @staticmethod
    def _new2777(_arg1 : str, _arg2 : str, _arg3 : object) -> 'Termin':
        res = Termin(_arg1)
        res.acronym = _arg2
        res.tag = _arg3
        return res
    
    @staticmethod
    def _new2788(_arg1 : str, _arg2 : str, _arg3 : str, _arg4 : object) -> 'Termin':
        res = Termin(_arg1)
        res.canonic_text = _arg2
        res.acronym = _arg3
        res.tag = _arg4
        return res
    
    # static constructor for class Termin
    @staticmethod
    def _static_ctor():
        Termin.M_STD_ABRIDE_PREFIXES = ["НИЖ", "ВЕРХ", "МАЛ", "БОЛЬШ", "НОВ", "СТАР"]

Termin._static_ctor()