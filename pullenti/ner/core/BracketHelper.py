# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.core.BracketSequenceToken import BracketSequenceToken
from pullenti.ner.Token import Token
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.morph.MorphClass import MorphClass
from pullenti.ner.TextToken import TextToken
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper

class BracketHelper:
    """ Поддержка анализа скобок и кавычек
    
    Хелпер скобок и кавычек
    """
    
    class Bracket:
        
        def __init__(self, t : 'Token') -> None:
            from pullenti.ner.TextToken import TextToken
            self.source = None;
            self.char0_ = None;
            self.can_be_open = False
            self.can_be_close = False
            self.source = t
            if (isinstance(t, TextToken)): 
                self.char0_ = t.term[0]
            self.can_be_open = BracketHelper.can_be_start_of_sequence(t, False, False)
            self.can_be_close = BracketHelper.can_be_end_of_sequence(t, False, None, False)
        
        def __str__(self) -> str:
            res = io.StringIO()
            print("!{0} ".format(self.char0_), end="", file=res, flush=True)
            if (self.can_be_open): 
                print(" Open", end="", file=res)
            if (self.can_be_close): 
                print(" Close", end="", file=res)
            return Utils.toStringStringIO(res)
    
    @staticmethod
    def can_be_start_of_sequence(t : 'Token', quotes_only : bool=False, ignore_whitespaces : bool=False) -> bool:
        """ Проверка, что с этого токена может начинаться последовательность, а сам токен является открывающей скобкой или кавычкой
        
        Args:
            t(Token): проверяемый токен
            quotes_only(bool): должны быть именно кавычка, а не скобка
        
        Returns:
            bool: да-нет
        
        """
        tt = Utils.asObjectOrNull(t, TextToken)
        if (tt is None or tt.next0_ is None): 
            return False
        ch = tt.term[0]
        if (str.isalnum(ch)): 
            return False
        if (quotes_only and (BracketHelper.M_QUOTES.find(ch) < 0)): 
            return False
        if (t.next0_ is None): 
            return False
        if (BracketHelper.M_OPEN_CHARS.find(ch) < 0): 
            return False
        if (not ignore_whitespaces): 
            if (t.is_whitespace_after): 
                if (not t.is_whitespace_before): 
                    if (t.previous is not None and t.previous.is_table_control_char): 
                        pass
                    else: 
                        return False
                if (t.is_newline_after): 
                    return False
            elif (not t.is_whitespace_before): 
                if (str.isalnum(t.kit.get_text_character(t.begin_char - 1))): 
                    if (t.next0_ is not None and ((t.next0_.chars.is_all_lower or not t.next0_.chars.is_letter))): 
                        if (ch != '('): 
                            return False
        return True
    
    @staticmethod
    def can_be_end_of_sequence(t : 'Token', quotes_only : bool=False, open_token : 'Token'=None, ignore_whitespaces : bool=False) -> bool:
        """ Проверка, что на этом токене может заканчиваться последовательность, а сам токен является закрывающей скобкой или кавычкой
        
        Args:
            t(Token): проверяемый токен
            quotes_only(bool): должны быть именно кавычка, а не скобка
            open_token(Token): это ссылка на токен, который был открывающим
        
        Returns:
            bool: да-нет
        
        """
        tt = Utils.asObjectOrNull(t, TextToken)
        if (tt is None): 
            return False
        ch = tt.term[0]
        if (str.isalnum(ch)): 
            return False
        if (t.previous is None): 
            return False
        if (BracketHelper.M_CLOSE_CHARS.find(ch) < 0): 
            return False
        if (quotes_only): 
            if (BracketHelper.M_QUOTES.find(ch) < 0): 
                return False
        if (not ignore_whitespaces): 
            if (not t.is_whitespace_after): 
                if (t.is_whitespace_before): 
                    if (t.next0_ is not None and t.next0_.is_table_control_char): 
                        pass
                    else: 
                        return False
                if (t.is_newline_before): 
                    return False
            elif (t.is_whitespace_before): 
                if (str.isalnum(t.kit.get_text_character(t.end_char + 1))): 
                    return False
                if (not t.is_whitespace_after): 
                    return False
        if (isinstance(open_token, TextToken)): 
            ch0 = open_token.term[0]
            i = BracketHelper.M_OPEN_CHARS.find(ch0)
            if (i < 0): 
                return BracketHelper.M_CLOSE_CHARS.find(ch) < 0
            ii = BracketHelper.M_CLOSE_CHARS.find(ch)
            return ii == i
        return True
    
    @staticmethod
    def is_bracket_char(ch : 'char', quotes_only : bool=False) -> bool:
        """ Проверка символа, что он может быть скобкой или кавычкой
        
        Args:
            ch('char'): проверяемый символ
            quotes_only(bool): должны быть именно кавычка, а не скобка
        
        Returns:
            bool: да-нет
        """
        if (BracketHelper.M_OPEN_CHARS.find(ch) >= 0 or BracketHelper.M_CLOSE_CHARS.find(ch) >= 0): 
            if (not quotes_only): 
                return True
            return BracketHelper.M_QUOTES.find(ch) >= 0
        return False
    
    @staticmethod
    def is_bracket(t : 'Token', quotes_only : bool=False) -> bool:
        """ Проверка токена, что он является скобкой или кавычкой
        
        Args:
            t(Token): проверяемый токен
            quotes_only(bool): должны быть именно кавычка, а не скобка
        
        Returns:
            bool: да-нет
        """
        if (t is None): 
            return False
        if (t.is_char_of(BracketHelper.M_OPEN_CHARS)): 
            if (quotes_only): 
                if (isinstance(t, TextToken)): 
                    if (BracketHelper.M_QUOTES.find(t.term[0]) < 0): 
                        return False
            return True
        if (t.is_char_of(BracketHelper.M_CLOSE_CHARS)): 
            if (quotes_only): 
                if (isinstance(t, TextToken)): 
                    if (BracketHelper.M_QUOTES.find(t.term[0]) < 0): 
                        return False
            return True
        return False
    
    @staticmethod
    def try_parse(t : 'Token', attrs : 'BracketParseAttr'=BracketParseAttr.NO, max_tokens : int=100) -> 'BracketSequenceToken':
        """ Попробовать восстановить последовательность, обрамляемую кавычками или скобками. Поддерживается
        вложенность, возможность отсутствия закрывающего элемента и др.
        
        Args:
            t(Token): начальный токен
            attrs(BracketParseAttr): параметры выделения
            max_tokens(int): максимально токенов (вдруг забыли закрывающую кавычку)
        
        Returns:
            BracketSequenceToken: метатокен BracketSequenceToken
        
        """
        t0 = t
        cou = 0
        if (not BracketHelper.can_be_start_of_sequence(t0, False, False)): 
            return None
        br_list = list()
        br_list.append(BracketHelper.Bracket(t0))
        cou = 0
        crlf = 0
        last = None
        lev = 1
        is_assim = br_list[0].char0_ != '«' and BracketHelper.M_ASSYMOPEN_CHARS.find(br_list[0].char0_) >= 0
        gen_case = False
        t = t0.next0_
        first_pass3550 = True
        while True:
            if first_pass3550: first_pass3550 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_table_control_char): 
                break
            last = t
            if (t.is_char_of(BracketHelper.M_OPEN_CHARS) or t.is_char_of(BracketHelper.M_CLOSE_CHARS)): 
                if (t.is_newline_before and (((attrs) & (BracketParseAttr.CANBEMANYLINES))) == (BracketParseAttr.NO)): 
                    if (t.whitespaces_before_count > 10 or BracketHelper.can_be_start_of_sequence(t, False, False)): 
                        if (t.is_char('(') and not t0.is_char('(')): 
                            pass
                        else: 
                            last = t.previous
                            break
                bb = BracketHelper.Bracket(t)
                br_list.append(bb)
                if (len(br_list) > 20): 
                    break
                if ((len(br_list) == 3 and br_list[1].can_be_open and bb.can_be_close) and BracketHelper.__must_be_close_char(bb.char0_, br_list[1].char0_) and BracketHelper.__must_be_close_char(bb.char0_, br_list[0].char0_)): 
                    ok = False
                    tt = t.next0_
                    while tt is not None: 
                        if (tt.is_newline_before): 
                            break
                        if (tt.is_char(',')): 
                            break
                        if (tt.is_char('.')): 
                            tt = tt.next0_
                            while tt is not None: 
                                if (tt.is_newline_before): 
                                    break
                                elif (tt.is_char_of(BracketHelper.M_OPEN_CHARS) or tt.is_char_of(BracketHelper.M_CLOSE_CHARS)): 
                                    bb2 = BracketHelper.Bracket(tt)
                                    if (BracketHelper.can_be_end_of_sequence(tt, False, None, False) and BracketHelper.__can_be_close_char(bb2.char0_, br_list[0].char0_)): 
                                        ok = True
                                    break
                                tt = tt.next0_
                            break
                        if (t.is_char_of(BracketHelper.M_OPEN_CHARS) or t.is_char_of(BracketHelper.M_CLOSE_CHARS)): 
                            ok = True
                            break
                        tt = tt.next0_
                    if (not ok): 
                        break
                if (is_assim): 
                    if (bb.can_be_open and not bb.can_be_close and bb.char0_ == br_list[0].char0_): 
                        lev += 1
                    elif (bb.can_be_close and not bb.can_be_open and BracketHelper.M_OPEN_CHARS.find(br_list[0].char0_) == BracketHelper.M_CLOSE_CHARS.find(bb.char0_)): 
                        lev -= 1
                        if (lev == 0): 
                            break
            else: 
                cou += 1
                if (cou > max_tokens): 
                    break
                if ((((attrs) & (BracketParseAttr.CANCONTAINSVERBS))) == (BracketParseAttr.NO)): 
                    if (t.morph.language.is_cyrillic): 
                        if (t.get_morph_class_in_dictionary() == MorphClass.VERB): 
                            if (not t.morph.class0_.is_adjective and not t.morph.contains_attr("страд.з.", None)): 
                                if (t.chars.is_all_lower): 
                                    norm = t.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)
                                    if (not LanguageHelper.ends_with(norm, "СЯ")): 
                                        if (len(br_list) > 1): 
                                            break
                                        if (br_list[0].char0_ != '('): 
                                            break
                    elif (t.morph.language.is_en): 
                        if (t.morph.class0_ == MorphClass.VERB and t.chars.is_all_lower): 
                            break
                    r = t.get_referent()
                    if (r is not None and r.type_name == "ADDRESS"): 
                        if (not t0.is_char('(')): 
                            break
            if ((((attrs) & (BracketParseAttr.CANBEMANYLINES))) != (BracketParseAttr.NO)): 
                if (t.is_newline_before): 
                    if (t.newlines_before_count > 1): 
                        break
                    crlf += 1
                continue
            if (t.is_newline_before): 
                if (t.whitespaces_before_count > 15): 
                    last = t.previous
                    break
                crlf += 1
                if (not t.chars.is_all_lower): 
                    if (MiscHelper.can_be_start_of_sentence(t)): 
                        has = False
                        tt = t.next0_
                        while tt is not None: 
                            if (tt.is_newline_before): 
                                break
                            elif (tt.length_char == 1 and tt.is_char_of(BracketHelper.M_OPEN_CHARS) and tt.is_whitespace_before): 
                                break
                            elif (tt.length_char == 1 and tt.is_char_of(BracketHelper.M_CLOSE_CHARS) and not tt.is_whitespace_before): 
                                has = True
                                break
                            tt = tt.next0_
                        if (not has): 
                            last = t.previous
                            break
                if ((isinstance(t.previous, MetaToken)) and BracketHelper.can_be_end_of_sequence(t.previous.end_token, False, None, False)): 
                    last = t.previous
                    break
            if (crlf > 1): 
                if (len(br_list) > 1): 
                    break
                if (crlf > 10): 
                    break
            if (t.is_char(';') and t.is_newline_after): 
                break
            npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0, None)
            if (npt is not None): 
                if (t.is_newline_before): 
                    gen_case = npt.morph.case_.is_genitive
                t = npt.end_token
                last = t
        if ((len(br_list) == 1 and br_list[0].can_be_open and (isinstance(last, MetaToken))) and last.is_newline_after): 
            if (BracketHelper.can_be_end_of_sequence(last.end_token, False, None, False)): 
                return BracketSequenceToken(t0, last)
        if ((len(br_list) == 1 and br_list[0].can_be_open and gen_case) and last.is_newline_after and crlf <= 2): 
            return BracketSequenceToken(t0, last)
        if (len(br_list) < 1): 
            return None
        i = 1
        while i < (len(br_list) - 1): 
            if (br_list[i].char0_ == '<' and br_list[i + 1].char0_ == '>'): 
                br_list[i].can_be_open = True
                br_list[i + 1].can_be_close = True
            i += 1
        internals = None
        while len(br_list) > 3:
            i = len(br_list) - 1
            if ((br_list[i].can_be_close and br_list[i - 1].can_be_open and not BracketHelper.__can_be_close_char(br_list[i].char0_, br_list[0].char0_)) and BracketHelper.__can_be_close_char(br_list[i].char0_, br_list[i - 1].char0_)): 
                del br_list[len(br_list) - 2:len(br_list) - 2+2]
                continue
            break
        while len(br_list) >= 4:
            changed = False
            i = 1
            while i < (len(br_list) - 2): 
                if ((br_list[i].can_be_open and not br_list[i].can_be_close and br_list[i + 1].can_be_close) and not br_list[i + 1].can_be_open): 
                    ok = False
                    if (BracketHelper.__must_be_close_char(br_list[i + 1].char0_, br_list[i].char0_) or br_list[i].char0_ != br_list[0].char0_): 
                        ok = True
                        if ((i == 1 and ((i + 2) < len(br_list)) and br_list[i + 2].char0_ == ')') and br_list[i + 1].char0_ != ')' and BracketHelper.__can_be_close_char(br_list[i + 1].char0_, br_list[i - 1].char0_)): 
                            br_list[i + 2] = br_list[i + 1]
                    elif (i > 1 and ((i + 2) < len(br_list)) and BracketHelper.__must_be_close_char(br_list[i + 2].char0_, br_list[i - 1].char0_)): 
                        ok = True
                    if (ok): 
                        if (internals is None): 
                            internals = list()
                        internals.append(BracketSequenceToken(br_list[i].source, br_list[i + 1].source))
                        del br_list[i:i+2]
                        changed = True
                        break
                i += 1
            if (not changed): 
                break
        res = None
        if ((len(br_list) >= 4 and br_list[1].can_be_open and br_list[2].can_be_close) and br_list[3].can_be_close and not br_list[3].can_be_open): 
            if (BracketHelper.__can_be_close_char(br_list[3].char0_, br_list[0].char0_)): 
                res = BracketSequenceToken(br_list[0].source, br_list[3].source)
                if (br_list[0].source.next0_ != br_list[1].source or br_list[2].source.next0_ != br_list[3].source): 
                    res.internal.append(BracketSequenceToken(br_list[1].source, br_list[2].source))
                if (internals is not None): 
                    res.internal.extend(internals)
        if ((res is None and len(br_list) >= 3 and br_list[2].can_be_close) and not br_list[2].can_be_open): 
            if ((((attrs) & (BracketParseAttr.NEARCLOSEBRACKET))) != (BracketParseAttr.NO)): 
                if (BracketHelper.__can_be_close_char(br_list[1].char0_, br_list[0].char0_)): 
                    return BracketSequenceToken(br_list[0].source, br_list[1].source)
            ok = True
            if (BracketHelper.__can_be_close_char(br_list[2].char0_, br_list[0].char0_) and BracketHelper.__can_be_close_char(br_list[1].char0_, br_list[0].char0_) and br_list[1].can_be_close): 
                t = br_list[1].source
                while t != br_list[2].source and t is not None: 
                    if (t.is_newline_before): 
                        ok = False
                        break
                    if (t.chars.is_letter and t.chars.is_all_lower): 
                        ok = False
                        break
                    npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0, None)
                    if (npt is not None): 
                        t = npt.end_token
                    t = t.next0_
                if (ok): 
                    t = br_list[0].source.next0_
                    while t != br_list[1].source and t is not None: 
                        if (t.is_newline_before): 
                            return BracketSequenceToken(br_list[0].source, t.previous)
                        t = t.next0_
                lev1 = 0
                tt = br_list[0].source.previous
                first_pass3551 = True
                while True:
                    if first_pass3551: first_pass3551 = False
                    else: tt = tt.previous
                    if (not (tt is not None)): break
                    if (tt.is_newline_after or tt.is_table_control_char): 
                        break
                    if (not (isinstance(tt, TextToken))): 
                        continue
                    if (tt.chars.is_letter or tt.length_char > 1): 
                        continue
                    ch = tt.term[0]
                    if (BracketHelper.__can_be_close_char(ch, br_list[0].char0_)): 
                        lev1 += 1
                    elif (BracketHelper.__can_be_close_char(br_list[1].char0_, ch)): 
                        lev1 -= 1
                        if (lev1 < 0): 
                            return BracketSequenceToken(br_list[0].source, br_list[1].source)
            if (ok and BracketHelper.__can_be_close_char(br_list[2].char0_, br_list[0].char0_)): 
                intern = BracketSequenceToken(br_list[1].source, br_list[2].source)
                res = BracketSequenceToken(br_list[0].source, br_list[2].source)
                res.internal.append(intern)
            elif (ok and BracketHelper.__can_be_close_char(br_list[2].char0_, br_list[1].char0_) and br_list[0].can_be_open): 
                if (BracketHelper.__can_be_close_char(br_list[2].char0_, br_list[0].char0_)): 
                    intern = BracketSequenceToken(br_list[1].source, br_list[2].source)
                    res = BracketSequenceToken(br_list[0].source, br_list[2].source)
                    res.internal.append(intern)
                elif (len(br_list) == 3): 
                    return None
        if (res is None and len(br_list) > 1 and br_list[1].can_be_close): 
            res = BracketSequenceToken(br_list[0].source, br_list[1].source)
        if (res is None and len(br_list) > 1 and BracketHelper.__can_be_close_char(br_list[1].char0_, br_list[0].char0_)): 
            res = BracketSequenceToken(br_list[0].source, br_list[1].source)
        if (res is None and len(br_list) == 2 and br_list[0].char0_ == br_list[1].char0_): 
            res = BracketSequenceToken(br_list[0].source, br_list[1].source)
        if (res is not None and internals is not None): 
            for i in internals: 
                if (i.begin_char < res.end_char): 
                    res.internal.append(i)
        if (res is None): 
            cou = 0
            tt = t0.next0_
            first_pass3552 = True
            while True:
                if first_pass3552: first_pass3552 = False
                else: tt = tt.next0_; cou += 1
                if (not (tt is not None)): break
                if (tt.is_table_control_char): 
                    break
                if (MiscHelper.can_be_start_of_sentence(tt)): 
                    break
                if (max_tokens > 0 and cou > max_tokens): 
                    break
                mt = Utils.asObjectOrNull(tt, MetaToken)
                if (mt is None): 
                    continue
                if (isinstance(mt.end_token, TextToken)): 
                    if (mt.end_token.is_char_of(BracketHelper.M_CLOSE_CHARS)): 
                        bb = BracketHelper.Bracket(Utils.asObjectOrNull(mt.end_token, TextToken))
                        if (bb.can_be_close and BracketHelper.__can_be_close_char(bb.char0_, br_list[0].char0_)): 
                            return BracketSequenceToken(t0, tt)
        return res
    
    M_OPEN_CHARS = "\"'`’<{([«“„”"
    
    M_CLOSE_CHARS = "\"'`’>})]»”“"
    
    M_QUOTES = "\"'`’«“<”„»>"
    
    M_ASSYMOPEN_CHARS = "<{([«"
    
    @staticmethod
    def __can_be_close_char(close0_ : 'char', open0_ : 'char') -> bool:
        i = BracketHelper.M_OPEN_CHARS.find(open0_)
        if (i < 0): 
            return False
        j = BracketHelper.M_CLOSE_CHARS.find(close0_)
        return i == j
    
    @staticmethod
    def __must_be_close_char(close0_ : 'char', open0_ : 'char') -> bool:
        if (BracketHelper.M_ASSYMOPEN_CHARS.find(open0_) < 0): 
            return False
        i = BracketHelper.M_OPEN_CHARS.find(open0_)
        j = BracketHelper.M_CLOSE_CHARS.find(close0_)
        return i == j