# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import io
from pullenti.ntopy.Utils import Utils
from pullenti.ner.core.BracketParseAttr import BracketParseAttr

from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr


class BracketHelper:
    """ Поддержка анализа скобок и кавычек """
    
    class Bracket:
        
        def __init__(self, t : 'Token') -> None:
            from pullenti.ner.TextToken import TextToken
            self.source = None
            self.char0 = None
            self.can_be_open = False
            self.can_be_close = False
            self.source = t
            if (isinstance(t, TextToken)): 
                self.char0 = (t if isinstance(t, TextToken) else None).term[0]
            self.can_be_open = BracketHelper.can_be_start_of_sequence(t, False, False)
            self.can_be_close = BracketHelper.can_be_end_of_sequence(t, False, None, False)
        
        def __str__(self) -> str:
            res = Utils.newStringIO(None)
            print("!{0} ".format(self.char0), end="", file=res, flush=True)
            if (self.can_be_open): 
                print(" Open", end="", file=res)
            if (self.can_be_close): 
                print(" Close", end="", file=res)
            return Utils.toStringStringIO(res)
    
    @staticmethod
    def can_be_start_of_sequence(t : 'Token', quotes_only : bool=False, ignore_whitespaces : bool=False) -> bool:
        """ Проверка, что с этого терма может начинаться последовательность
        
        Args:
            t(Token): проверяемый токен
            quotes_only(bool): должны быть именно кавычка, а не скобка
        
        """
        from pullenti.ner.TextToken import TextToken
        tt = (t if isinstance(t, TextToken) else None)
        if (tt is None or tt.next0 is None): 
            return False
        ch = tt.term[0]
        if (ch.isalnum()): 
            return False
        if (quotes_only and ((ch) not in BracketHelper.__m_quotes)): 
            return False
        if (t.next0 is None): 
            return False
        if ((ch) not in BracketHelper.__m_open_chars): 
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
                if (t.kit.get_text_character(t.begin_char - 1).isalnum()): 
                    if (t.next0 is not None and ((t.next0.chars.is_all_lower or not t.next0.chars.is_letter))): 
                        if (ch != '('): 
                            return False
        return True
    
    @staticmethod
    def can_be_end_of_sequence(t : 'Token', quotes_only : bool=False, opent : 'Token'=None, ignore_whitespaces : bool=False) -> bool:
        """ Проверка, что на этом терме может заканчиваться последовательность
        
        Args:
            t(Token): закрывающая кавычка
            quotes_only(bool): должны быть именно кавычка, а не скобка
            opent(Token): это ссылка на токен, который мог быть открывающим
        
        """
        from pullenti.ner.TextToken import TextToken
        tt = (t if isinstance(t, TextToken) else None)
        if (tt is None): 
            return False
        ch = tt.term[0]
        if (ch.isalnum()): 
            return False
        if (t.previous is None): 
            return False
        if ((ch) not in BracketHelper.__m_close_chars): 
            return False
        if (quotes_only): 
            if ((ch) not in BracketHelper.__m_quotes): 
                return False
        if (not ignore_whitespaces): 
            if (not t.is_whitespace_after): 
                if (t.is_whitespace_before): 
                    if (t.next0 is not None and t.next0.is_table_control_char): 
                        pass
                    else: 
                        return False
                if (t.is_newline_before): 
                    return False
            elif (t.is_whitespace_before): 
                if (t.kit.get_text_character(t.end_char + 1).isalnum()): 
                    return False
                if (not t.is_whitespace_after): 
                    return False
        if (isinstance(opent, TextToken)): 
            ch0 = (opent if isinstance(opent, TextToken) else None).term[0]
            i = BracketHelper.__m_open_chars.find(ch0)
            if (i < 0): 
                return (ch) not in BracketHelper.__m_close_chars
            ii = BracketHelper.__m_close_chars.find(ch)
            return ii == i
        return True
    
    @staticmethod
    def is_bracket_char(ch : 'char', quots_only : bool=False) -> bool:
        """ Проверка символа, что он может быть скобкой или кавычкой
        
        Args:
            ch('char'): 
            quots_only(bool): 
        
        """
        if ((ch) in BracketHelper.__m_open_chars or (ch) in BracketHelper.__m_close_chars): 
            if (not quots_only): 
                return True
            return (ch) in BracketHelper.__m_quotes
        return False
    
    @staticmethod
    def is_bracket(t : 'Token', quots_only : bool=False) -> bool:
        """ Проверка токена, что он является скобкой или кавычкой
        
        Args:
            t(Token): 
            quots_only(bool): 
        
        """
        from pullenti.ner.TextToken import TextToken
        if (t is None): 
            return False
        if (t.is_char_of(BracketHelper.__m_open_chars)): 
            if (quots_only): 
                if (isinstance(t, TextToken)): 
                    if (((t if isinstance(t, TextToken) else None).term[0]) not in BracketHelper.__m_quotes): 
                        return False
            return True
        if (t.is_char_of(BracketHelper.__m_close_chars)): 
            if (quots_only): 
                if (isinstance(t, TextToken)): 
                    if (((t if isinstance(t, TextToken) else None).term[0]) not in BracketHelper.__m_quotes): 
                        return False
            return True
        return False
    
    @staticmethod
    def try_parse(t : 'Token', typ : 'BracketParseAttr'=BracketParseAttr.NO, max_tokens : int=100) -> 'BracketSequenceToken':
        """ Попробовать восстановить последовательность, обрамляемой кавычками
        
        Args:
            t(Token): 
            typ(BracketParseAttr): параметры выделения
            max_tokens(int): максимально токенов (вдруг забыли закрывающую ккавычку)
        
        """
        from pullenti.morph.MorphClass import MorphClass
        from pullenti.ner.MetaToken import MetaToken
        from pullenti.ner.core.BracketSequenceToken import BracketSequenceToken
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.core.MiscHelper import MiscHelper
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
        is_assim = br_list[0].char0 != '«' and (br_list[0].char0) in BracketHelper.__m_assymopen_chars
        t = t0.next0
        first_pass2599 = True
        while True:
            if first_pass2599: first_pass2599 = False
            else: t = t.next0
            if (not (t is not None)): break
            if (t.is_table_control_char): 
                break
            last = t
            if (t.is_char_of(BracketHelper.__m_open_chars) or t.is_char_of(BracketHelper.__m_close_chars)): 
                if (t.is_newline_before and ((typ & BracketParseAttr.CANBEMANYLINES)) == BracketParseAttr.NO): 
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
                if ((len(br_list) == 3 and br_list[1].can_be_open and bb.can_be_close) and BracketHelper.__must_be_close_char(bb.char0, br_list[1].char0) and BracketHelper.__must_be_close_char(bb.char0, br_list[0].char0)): 
                    ok = False
                    tt = t.next0
                    while tt is not None: 
                        if (tt.is_newline_before): 
                            break
                        if (tt.is_char(',')): 
                            break
                        if (tt.is_char('.')): 
                            tt = tt.next0
                            while tt is not None: 
                                if (tt.is_newline_before): 
                                    break
                                elif (tt.is_char_of(BracketHelper.__m_open_chars) or tt.is_char_of(BracketHelper.__m_close_chars)): 
                                    bb2 = BracketHelper.Bracket(tt)
                                    if (BracketHelper.can_be_end_of_sequence(tt, False, None, False) and BracketHelper.__can_be_close_char(bb2.char0, br_list[0].char0)): 
                                        ok = True
                                    break
                                tt = tt.next0
                            break
                        if (t.is_char_of(BracketHelper.__m_open_chars) or t.is_char_of(BracketHelper.__m_close_chars)): 
                            ok = True
                            break
                        tt = tt.next0
                    if (not ok): 
                        break
                if (is_assim): 
                    if (bb.can_be_open and not bb.can_be_close and bb.char0 == br_list[0].char0): 
                        lev += 1
                    elif (bb.can_be_close and not bb.can_be_open and BracketHelper.__m_open_chars.find(br_list[0].char0) == BracketHelper.__m_close_chars.find(bb.char0)): 
                        lev -= 1
                        if (lev == 0): 
                            break
            else: 
                cou += 1
                if ((cou) > max_tokens): 
                    break
                if (((typ & BracketParseAttr.CANCONTAINSVERBS)) == BracketParseAttr.NO): 
                    if (t.morph.language.is_cyrillic): 
                        if (t.get_morph_class_in_dictionary() == MorphClass.VERB): 
                            if (not t.morph.class0.is_adjective and not t.morph.contains_attr("страд.з.", MorphClass())): 
                                if (t.chars.is_all_lower): 
                                    norm = t.get_normal_case_text(MorphClass(), False, MorphGender.UNDEFINED, False)
                                    if (not LanguageHelper.ends_with(norm, "СЯ")): 
                                        if (len(br_list) > 1): 
                                            break
                                        if (br_list[0].char0 != '('): 
                                            break
                    elif (t.morph.language.is_en): 
                        if (t.morph.class0 == MorphClass.VERB and t.chars.is_all_lower): 
                            break
                    r = t.get_referent()
                    if (r is not None and r.type_name == "ADDRESS"): 
                        if (not t0.is_char('(')): 
                            break
            if (((typ & BracketParseAttr.CANBEMANYLINES)) != BracketParseAttr.NO): 
                if (t.is_newline_before): 
                    if (t.newlines_before_count > 1): 
                        break
                    crlf += 1
                continue
            if (t.is_newline_before): 
                if (t.whitespaces_before_count > 15): 
                    break
                crlf += 1
                if (not t.chars.is_all_lower): 
                    if (t.previous is not None and t.previous.is_char('.')): 
                        break
                if (isinstance(t.previous, MetaToken) and BracketHelper.can_be_end_of_sequence((t.previous if isinstance(t.previous, MetaToken) else None).end_token, False, None, False)): 
                    break
            if (crlf > 1): 
                if (len(br_list) > 1): 
                    break
                if (crlf > 10): 
                    break
            if (t.is_char(';') and t.is_newline_after): 
                break
        if ((len(br_list) == 1 and br_list[0].can_be_open and isinstance(last, MetaToken)) and last.is_newline_after): 
            if (BracketHelper.can_be_end_of_sequence((last if isinstance(last, MetaToken) else None).end_token, False, None, False)): 
                return BracketSequenceToken(t0, last)
        if (len(br_list) < 1): 
            return None
        i = 1
        while i < (len(br_list) - 1): 
            if (br_list[i].char0 == '<' and br_list[i + 1].char0 == '>'): 
                br_list[i].can_be_open = True
                br_list[i + 1].can_be_close = True
            i += 1
        internals = None
        while len(br_list) > 3:
            i = len(br_list) - 1
            if ((br_list[i].can_be_close and br_list[i - 1].can_be_open and not BracketHelper.__can_be_close_char(br_list[i].char0, br_list[0].char0)) and BracketHelper.__can_be_close_char(br_list[i].char0, br_list[i - 1].char0)): 
                del br_list[len(br_list) - 2:len(br_list) - 2+2]
                continue
            break
        while len(br_list) >= 4:
            changed = False
            i = 1
            while i < (len(br_list) - 2): 
                if ((br_list[i].can_be_open and not br_list[i].can_be_close and br_list[i + 1].can_be_close) and not br_list[i + 1].can_be_open): 
                    ok = False
                    if (BracketHelper.__must_be_close_char(br_list[i + 1].char0, br_list[i].char0) or br_list[i].char0 != br_list[0].char0): 
                        ok = True
                        if ((i == 1 and ((i + 2) < len(br_list)) and br_list[i + 2].char0 == ')') and br_list[i + 1].char0 != ')' and BracketHelper.__can_be_close_char(br_list[i + 1].char0, br_list[i - 1].char0)): 
                            br_list[i + 2] = br_list[i + 1]
                    elif (i > 1 and ((i + 2) < len(br_list)) and BracketHelper.__must_be_close_char(br_list[i + 2].char0, br_list[i - 1].char0)): 
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
            if (BracketHelper.__can_be_close_char(br_list[3].char0, br_list[0].char0)): 
                res = BracketSequenceToken(br_list[0].source, br_list[3].source)
                if (br_list[0].source.next0 != br_list[1].source or br_list[2].source.next0 != br_list[3].source): 
                    res.internal.append(BracketSequenceToken(br_list[1].source, br_list[2].source))
                if (internals is not None): 
                    res.internal.extend(internals)
        if ((res is None and len(br_list) >= 3 and br_list[2].can_be_close) and not br_list[2].can_be_open): 
            if (((typ & BracketParseAttr.NEARCLOSEBRACKET)) != BracketParseAttr.NO): 
                if (BracketHelper.__can_be_close_char(br_list[1].char0, br_list[0].char0)): 
                    return BracketSequenceToken(br_list[0].source, br_list[1].source)
            ok = True
            if (BracketHelper.__can_be_close_char(br_list[2].char0, br_list[0].char0) and BracketHelper.__can_be_close_char(br_list[1].char0, br_list[0].char0) and br_list[1].can_be_close): 
                t = br_list[1].source
                while t != br_list[2].source and t is not None: 
                    if (t.is_newline_before): 
                        ok = False
                        break
                    if (t.chars.is_letter and t.chars.is_all_lower): 
                        ok = False
                        break
                    npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0)
                    if (npt is not None): 
                        t = npt.end_token
                    t = t.next0
                if (ok): 
                    t = br_list[0].source.next0
                    while t != br_list[1].source and t is not None: 
                        if (t.is_newline_before): 
                            return BracketSequenceToken(br_list[0].source, t.previous)
                        t = t.next0
                lev1 = 0
                tt = br_list[0].source.previous
                first_pass2600 = True
                while True:
                    if first_pass2600: first_pass2600 = False
                    else: tt = tt.previous
                    if (not (tt is not None)): break
                    if (tt.is_newline_after or tt.is_table_control_char): 
                        break
                    if (not ((isinstance(tt, TextToken)))): 
                        continue
                    if (tt.chars.is_letter or tt.length_char > 1): 
                        continue
                    ch = (tt if isinstance(tt, TextToken) else None).term[0]
                    if (BracketHelper.__can_be_close_char(ch, br_list[0].char0)): 
                        lev1 += 1
                    elif (BracketHelper.__can_be_close_char(br_list[1].char0, ch)): 
                        lev1 -= 1
                        if (lev1 < 0): 
                            return BracketSequenceToken(br_list[0].source, br_list[1].source)
            if (ok and BracketHelper.__can_be_close_char(br_list[2].char0, br_list[0].char0)): 
                intern = BracketSequenceToken(br_list[1].source, br_list[2].source)
                res = BracketSequenceToken(br_list[0].source, br_list[2].source)
                res.internal.append(intern)
            elif (ok and BracketHelper.__can_be_close_char(br_list[2].char0, br_list[1].char0) and br_list[0].can_be_open): 
                if (BracketHelper.__can_be_close_char(br_list[2].char0, br_list[0].char0)): 
                    intern = BracketSequenceToken(br_list[1].source, br_list[2].source)
                    res = BracketSequenceToken(br_list[0].source, br_list[2].source)
                    res.internal.append(intern)
                elif (len(br_list) == 3): 
                    return None
        if (res is None and len(br_list) > 1 and br_list[1].can_be_close): 
            res = BracketSequenceToken(br_list[0].source, br_list[1].source)
        if (res is None and len(br_list) > 1 and BracketHelper.__can_be_close_char(br_list[1].char0, br_list[0].char0)): 
            res = BracketSequenceToken(br_list[0].source, br_list[1].source)
        if (res is None and len(br_list) == 2 and br_list[0].char0 == br_list[1].char0): 
            res = BracketSequenceToken(br_list[0].source, br_list[1].source)
        if (res is not None and internals is not None): 
            for i in internals: 
                if (i.begin_char < res.end_char): 
                    res.internal.append(i)
        if (res is None): 
            cou = 0
            tt = t0.next0
            first_pass2601 = True
            while True:
                if first_pass2601: first_pass2601 = False
                else: tt = tt.next0; cou += 1
                if (not (tt is not None)): break
                if (tt.is_table_control_char): 
                    break
                if (MiscHelper.can_be_start_of_sentence(tt)): 
                    break
                if (max_tokens > 0 and cou > max_tokens): 
                    break
                mt = (tt if isinstance(tt, MetaToken) else None)
                if (mt is None): 
                    continue
                if (isinstance(mt.end_token, TextToken)): 
                    if ((mt.end_token if isinstance(mt.end_token, TextToken) else None).is_char_of(BracketHelper.__m_close_chars)): 
                        bb = BracketHelper.Bracket(mt.end_token if isinstance(mt.end_token, TextToken) else None)
                        if (bb.can_be_close and BracketHelper.__can_be_close_char(bb.char0, br_list[0].char0)): 
                            return BracketSequenceToken(t0, tt)
        return res
    
    __m_open_chars = "\"'`’<{([«“„"
    
    __m_close_chars = "\"'`’>})]»”“"
    
    __m_quotes = "\"'`’«“<”„»>"
    
    __m_assymopen_chars = "<{([«"
    
    @staticmethod
    def __can_be_close_char(close0 : 'char', open0 : 'char') -> bool:
        i = BracketHelper.__m_open_chars.find(open0)
        if (i < 0): 
            return False
        j = BracketHelper.__m_close_chars.find(close0)
        return i == j
    
    @staticmethod
    def __must_be_close_char(close0 : 'char', open0 : 'char') -> bool:
        if ((open0) not in BracketHelper.__m_assymopen_chars): 
            return False
        i = BracketHelper.__m_open_chars.find(open0)
        j = BracketHelper.__m_close_chars.find(close0)
        return i == j