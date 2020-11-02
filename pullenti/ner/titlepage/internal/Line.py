# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing

from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.internal.BlkTyps import BlkTyps
from pullenti.ner.person.PersonReferent import PersonReferent
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.titlepage.internal.TitleItemToken import TitleItemToken
from pullenti.ner.core.internal.BlockTitleToken import BlockTitleToken

class Line(MetaToken):
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
    
    @property
    def chars_count(self) -> int:
        cou = 0
        t = self.begin_token
        while t is not None: 
            cou += t.length_char
            if (t == self.end_token): 
                break
            t = t.next0_
        return cou
    
    @property
    def is_pure_en(self) -> bool:
        en = 0
        ru = 0
        t = self.begin_token
        while t is not None and t.end_char <= self.end_char: 
            if ((isinstance(t, TextToken)) and t.chars.is_letter): 
                if (t.chars.is_cyrillic_letter): 
                    ru += 1
                elif (t.chars.is_latin_letter): 
                    en += 1
            t = t.next0_
        if (en > 0 and ru == 0): 
            return True
        return False
    
    @property
    def is_pure_ru(self) -> bool:
        en = 0
        ru = 0
        t = self.begin_token
        while t is not None and t.end_char <= self.end_char: 
            if ((isinstance(t, TextToken)) and t.chars.is_letter): 
                if (t.chars.is_cyrillic_letter): 
                    ru += 1
                elif (t.chars.is_latin_letter): 
                    en += 1
            t = t.next0_
        if (ru > 0 and en == 0): 
            return True
        return False
    
    @staticmethod
    def parse(t0 : 'Token', max_lines : int, max_chars : int, max_end_char : int) -> typing.List['Line']:
        res = list()
        total_chars = 0
        t = t0
        while t is not None: 
            if (max_end_char > 0): 
                if (t.begin_char > max_end_char): 
                    break
            t1 = t
            first_pass3885 = True
            while True:
                if first_pass3885: first_pass3885 = False
                else: t1 = t1.next0_
                if (not (t1 is not None and t1.next0_ is not None)): break
                if (t1.is_newline_after): 
                    if (t1.next0_ is None or MiscHelper.can_be_start_of_sentence(t1.next0_)): 
                        break
                if (t1 == t and t.is_newline_before and (isinstance(t.get_referent(), PersonReferent))): 
                    if (t1.next0_ is None): 
                        continue
                    if ((isinstance(t1.next0_, TextToken)) and t1.next0_.chars.is_letter and not t1.next0_.chars.is_all_lower): 
                        break
            if (t1 is None): 
                t1 = t
            tit = TitleItemToken.try_attach(t)
            if (tit is not None): 
                if (tit.typ == TitleItemToken.Types.KEYWORDS): 
                    break
            bl = BlockTitleToken.try_attach(t, False, None)
            if (bl is not None): 
                if (bl.typ != BlkTyps.UNDEFINED): 
                    break
            l_ = Line(t, t1)
            res.append(l_)
            total_chars += l_.chars_count
            if (len(res) >= max_lines or total_chars >= max_chars): 
                break
            t = t1
            t = t.next0_
        return res