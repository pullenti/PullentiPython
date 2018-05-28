# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import io
from pullenti.ntopy.Utils import Utils
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.NumberSpellingType import NumberSpellingType


class ProperNameHelper:
    """ Поддержка работы с собственными именами """
    
    @staticmethod
    def __corr_chars(str0 : str, ci : 'CharsInfo', keep_chars : bool) -> str:
        from pullenti.ner.core.MiscHelper import MiscHelper
        if (not keep_chars): 
            return str0
        if (ci.is_all_lower): 
            return str0.lower()
        if (ci.is_capital_upper): 
            return MiscHelper.convert_first_char_upper_and_other_lower(str0)
        return str0
    
    @staticmethod
    def __get_name_without_brackets(begin : 'Token', end : 'Token', normalize_first_noun_group : bool=False, normal_first_group_single : bool=False, ignore_geo_referent : bool=False) -> str:
        """ Получить строковое значение между токенами, при этом исключая кавычки и скобки
        
        Args:
            begin(Token): начальный токен
            end(Token): конечный токен
            normalize_first_noun_group(bool): нормализовывать ли первую именную группу (именит. падеж)
            normal_first_group_single(bool): приводить ли к единственному числу первую именную группу
            ignore_geo_referent(bool): игнорировать внутри географические сущности
        
        """
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.morph.MorphClass import MorphClass
        from pullenti.ner.TextToken import TextToken
        from pullenti.morph.MorphBaseInfo import MorphBaseInfo
        from pullenti.morph.MorphWordForm import MorphWordForm
        from pullenti.morph.Morphology import Morphology
        from pullenti.morph.MorphCase import MorphCase
        res = None
        if (BracketHelper.can_be_start_of_sequence(begin, False, False) and BracketHelper.can_be_end_of_sequence(end, False, begin, False)): 
            begin = begin.next0
            end = end.previous
        if (normalize_first_noun_group and not begin.morph.class0.is_preposition): 
            npt = NounPhraseHelper.try_parse(begin, NounPhraseParseAttr.REFERENTCANBENOUN, 0)
            if (npt is not None): 
                if (npt.noun.get_morph_class_in_dictionary().is_undefined and len(npt.adjectives) == 0): 
                    npt = None
            if (npt is not None and npt.end_token.end_char > end.end_char): 
                npt = None
            if (npt is not None): 
                res = npt.get_normal_case_text(MorphClass(), normal_first_group_single, MorphGender.UNDEFINED, False)
                te = npt.end_token.next0
                if (((te is not None and te.next0 is not None and te.is_comma) and isinstance(te.next0, TextToken) and te.next0.end_char <= end.end_char) and te.next0.morph.class0.is_verb and te.next0.morph.class0.is_adjective): 
                    for it in te.next0.morph.items: 
                        if (it.gender == npt.morph.gender or ((it.gender & npt.morph.gender)) != MorphGender.UNDEFINED): 
                            if (not (it.case & npt.morph.case).is_undefined): 
                                if (it.number == npt.morph.number or ((it.number & npt.morph.number)) != MorphNumber.UNDEFINED): 
                                    var = (te.next0 if isinstance(te.next0, TextToken) else None).term
                                    if (isinstance(it, MorphWordForm)): 
                                        var = (it if isinstance(it, MorphWordForm) else None).normal_case
                                    bi = MorphBaseInfo._new486(MorphClass.ADJECTIVE, npt.morph.gender, npt.morph.number, npt.morph.language)
                                    var = Morphology.get_wordform(var, bi)
                                    if (var is not None): 
                                        res = "{0}, {1}".format(res, var)
                                        te = te.next0.next0
                                    break
                if (te is not None and te.end_char <= end.end_char): 
                    s = ProperNameHelper.get_name(te, end, MorphClass.UNDEFINED, MorphCase.UNDEFINED, MorphGender.UNDEFINED, True, ignore_geo_referent)
                    if (not Utils.isNullOrEmpty(s)): 
                        if (not s[0].isalnum()): 
                            res = "{0}{1}".format(res, s)
                        else: 
                            res = "{0} {1}".format(res, s)
            elif (isinstance(begin, TextToken) and begin.chars.is_cyrillic_letter): 
                mm = begin.get_morph_class_in_dictionary()
                if (not mm.is_undefined): 
                    res = begin.get_normal_case_text(mm, False, MorphGender.UNDEFINED, False)
                    if (begin.end_char < end.end_char): 
                        res = "{0} {1}".format(res, ProperNameHelper.get_name(begin.next0, end, MorphClass.UNDEFINED, MorphCase.UNDEFINED, MorphGender.UNDEFINED, True, False))
        if (res is None): 
            res = ProperNameHelper.get_name(begin, end, MorphClass.UNDEFINED, MorphCase.UNDEFINED, MorphGender.UNDEFINED, True, ignore_geo_referent)
        if (not Utils.isNullOrEmpty(res)): 
            k = 0
            i = len(res) - 1
            while i >= 0: 
                if (res[i] == '*' or Utils.isWhitespace(res[i])): 
                    pass
                else: 
                    break
                i -= 1; k += 1
            if (k > 0): 
                if (k == len(res)): 
                    return None
                res = res[0 : (len(res) - k)]
        return res
    
    @staticmethod
    def __get_name(begin : 'Token', end : 'Token') -> str:
        """ Получить строковое значение между токенами без нормализации первой группы, всё в верхнем регистре.
        
        Args:
            begin(Token): 
            end(Token): 
        
        """
        from pullenti.morph.MorphClass import MorphClass
        from pullenti.morph.MorphCase import MorphCase
        res = ProperNameHelper.get_name(begin, end, MorphClass.UNDEFINED, MorphCase.UNDEFINED, MorphGender.UNDEFINED, False, False)
        return res
    
    @staticmethod
    def get_name(begin : 'Token', end : 'Token', cla : 'MorphClass', mc : 'MorphCase', gender : 'MorphGender'=MorphGender.UNDEFINED, ignore_brackets_and_hiphens : bool=False, ignore_geo_referent : bool=False) -> str:
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.morph.MorphClass import MorphClass
        from pullenti.morph.MorphCase import MorphCase
        from pullenti.ner.MetaToken import MetaToken
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.TextToken import TextToken
        from pullenti.morph.MorphWordForm import MorphWordForm
        from pullenti.ner.NumberToken import NumberToken
        if (end is None or begin is None): 
            return None
        if (begin.end_char > end.begin_char and begin != end): 
            return None
        res = Utils.newStringIO(None)
        prefix = None
        t = begin
        first_pass2607 = True
        while True:
            if first_pass2607: first_pass2607 = False
            else: t = t.next0
            if (not (t is not None and t.end_char <= end.end_char)): break
            if (res.tell() > 1000): 
                break
            if (t.is_table_control_char): 
                continue
            if (ignore_brackets_and_hiphens): 
                if (BracketHelper.is_bracket(t, False)): 
                    if (t == end): 
                        break
                    if (t.is_char_of("(<[")): 
                        br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                        if (br is not None and br.end_char <= end.end_char): 
                            tmp = ProperNameHelper.get_name(br.begin_token.next0, br.end_token.previous, MorphClass.UNDEFINED, MorphCase.UNDEFINED, MorphGender.UNDEFINED, ignore_brackets_and_hiphens, False)
                            if (tmp is not None): 
                                if ((br.end_char == end.end_char and br.begin_token.next0 == br.end_token.previous and not br.begin_token.next0.chars.is_letter) and not ((isinstance(br.begin_token.next0, ReferentToken)))): 
                                    pass
                                else: 
                                    print(" {0}{1}{2}".format(t.get_source_text(), tmp, br.end_token.get_source_text()), end="", file=res, flush=True)
                            t = br.end_token
                    continue
                if (t.is_hiphen): 
                    if (t == end): 
                        break
                    elif (t.is_whitespace_before or t.is_whitespace_after): 
                        continue
            tt = (t if isinstance(t, TextToken) else None)
            if (tt is not None): 
                if (not ignore_brackets_and_hiphens): 
                    if ((tt.next0 is not None and tt.next0.is_hiphen and isinstance(tt.next0.next0, TextToken)) and tt != end and tt.next0 != end): 
                        if (prefix is None): 
                            prefix = tt.term
                        else: 
                            prefix = "{0}-{1}".format(prefix, tt.term)
                        t = tt.next0
                        if (t == end): 
                            break
                        else: 
                            continue
                s = None
                if (cla.value != 0 or not mc.is_undefined or gender != MorphGender.UNDEFINED): 
                    for wff in tt.morph.items: 
                        wf = (wff if isinstance(wff, MorphWordForm) else None)
                        if (wf is None): 
                            continue
                        if (cla.value != 0): 
                            if (((wf.class0.value & cla.value)) == 0): 
                                continue
                        if (not mc.is_undefined): 
                            if ((wf.case & mc).is_undefined): 
                                continue
                        if (gender != MorphGender.UNDEFINED): 
                            if (((wf.gender & gender)) == MorphGender.UNDEFINED): 
                                continue
                        if (s is None or wf.normal_case == tt.term): 
                            s = wf.normal_case
                    if (s is None and gender != MorphGender.UNDEFINED): 
                        for wff in tt.morph.items: 
                            wf = (wff if isinstance(wff, MorphWordForm) else None)
                            if (wf is None): 
                                continue
                            if (cla.value != 0): 
                                if (((wf.class0.value & cla.value)) == 0): 
                                    continue
                            if (not mc.is_undefined): 
                                if ((wf.case & mc).is_undefined): 
                                    continue
                            if (s is None or wf.normal_case == tt.term): 
                                s = wf.normal_case
                if (s is None): 
                    s = tt.term
                    if (tt.chars.is_last_lower and tt.length_char > 2): 
                        s = tt.get_source_text()
                        for i in range(len(s) - 1, -1, -1):
                            if (s[i].isupper()): 
                                s = s[0 : (i + 1)]
                                break
                if (prefix is not None): 
                    delim = "-"
                    if (ignore_brackets_and_hiphens): 
                        delim = " "
                    s = "{0}{1}{2}".format(prefix, delim, s)
                prefix = None
                if (res.tell() > 0 and len(s) > 0): 
                    if (s[0].isalnum()): 
                        ch0 = Utils.getCharAtStringIO(res, res.tell() - 1)
                        if (ch0 == '-'): 
                            pass
                        else: 
                            print(' ', end="", file=res)
                    elif (not ignore_brackets_and_hiphens and BracketHelper.can_be_start_of_sequence(tt, False, False)): 
                        print(' ', end="", file=res)
                print(s, end="", file=res)
            elif (isinstance(t, NumberToken)): 
                if (res.tell() > 0): 
                    if (not t.is_whitespace_before and Utils.getCharAtStringIO(res, res.tell() - 1) == '-'): 
                        pass
                    else: 
                        print(' ', end="", file=res)
                nt = (t if isinstance(t, NumberToken) else None)
                if ((t.morph.class0.is_adjective and nt.typ == NumberSpellingType.WORDS and nt.begin_token == nt.end_token) and isinstance(nt.begin_token, TextToken)): 
                    print((nt.begin_token if isinstance(nt.begin_token, TextToken) else None).term, end="", file=res)
                else: 
                    print(nt.value, end="", file=res)
            elif (isinstance(t, MetaToken)): 
                if ((ignore_geo_referent and t != begin and t.get_referent() is not None) and t.get_referent().type_name == "GEO"): 
                    continue
                s = ProperNameHelper.get_name((t if isinstance(t, MetaToken) else None).begin_token, (t if isinstance(t, MetaToken) else None).end_token, cla, mc, gender, ignore_brackets_and_hiphens, ignore_geo_referent)
                if (not Utils.isNullOrEmpty(s)): 
                    if (res.tell() > 0): 
                        if (not t.is_whitespace_before and Utils.getCharAtStringIO(res, res.tell() - 1) == '-'): 
                            pass
                        else: 
                            print(' ', end="", file=res)
                    print(s, end="", file=res)
            if (t == end): 
                break
        if (res.tell() == 0): 
            return None
        return Utils.toStringStringIO(res)