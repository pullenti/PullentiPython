# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing
import math
from pullenti.unisharp.Utils import Utils

from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.internal.BlkTyps import BlkTyps
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.core.internal.BlockLine import BlockLine

class BlockTitleToken(MetaToken):
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
        self.typ = BlkTyps.UNDEFINED
        self.value = None;
    
    def __str__(self) -> str:
        return "{0} {1} {2}".format(Utils.enumToString(self.typ), Utils.ifNotNull(self.value, ""), self.get_source_text())
    
    @staticmethod
    def try_attach_list(t : 'Token') -> typing.List['BlockTitleToken']:
        content = None
        intro = None
        lits = None
        tt = t
        first_pass3528 = True
        while True:
            if first_pass3528: first_pass3528 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            if (tt.is_newline_before): 
                btt = BlockTitleToken.try_attach(tt, False, None)
                if (btt is None): 
                    continue
                if (btt.typ == BlkTyps.INDEX): 
                    content = btt
                    break
                if (btt.typ == BlkTyps.INTRO): 
                    tt2 = btt.end_token.next0_
                    for k in range(5):
                        li = BlockLine.create(tt2, None)
                        if (li is None): 
                            break
                        if (li.has_content_item_tail or li.typ == BlkTyps.INDEXITEM): 
                            content = btt
                            break
                        if (li.has_verb): 
                            break
                        if (li.typ != BlkTyps.UNDEFINED): 
                            if ((li.begin_char - btt.end_char) < 400): 
                                content = btt
                                break
                        tt2 = li.end_token.next0_
                    if (content is None): 
                        intro = btt
                    break
                if (btt.typ == BlkTyps.LITERATURE): 
                    if (lits is None): 
                        lits = list()
                    lits.append(btt)
        if (content is None and intro is None and ((lits is None or len(lits) != 1))): 
            return None
        res = list()
        chapter_names = TerminCollection()
        t0 = None
        if (content is not None): 
            res.append(content)
            cou = 0
            err = 0
            tt = content.end_token.next0_
            first_pass3529 = True
            while True:
                if first_pass3529: first_pass3529 = False
                else: tt = tt.next0_
                if (not (tt is not None)): break
                if (not tt.is_newline_before): 
                    continue
                li = BlockLine.create(tt, None)
                if (li is None): 
                    break
                if (li.has_verb): 
                    if (li.end_token.is_char('.')): 
                        break
                    if (li.length_char > 100): 
                        break
                btt = BlockTitleToken.try_attach(tt, True, None)
                if (btt is None): 
                    continue
                err = 0
                if (btt.typ == BlkTyps.INTRO): 
                    if (content.typ == BlkTyps.INTRO or cou > 2): 
                        break
                cou += 1
                content.end_token = btt.end_token
                tt = content.end_token
                if (btt.value is not None): 
                    chapter_names.add_string(btt.value, None, None, False)
            content.typ = BlkTyps.INDEX
            t0 = content.end_token.next0_
        elif (intro is not None): 
            t0 = intro.begin_token
        elif (lits is not None): 
            t0 = t
        else: 
            return None
        first = True
        tt = t0
        first_pass3530 = True
        while True:
            if first_pass3530: first_pass3530 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            if (not tt.is_newline_before): 
                continue
            if (tt.is_value("СЛАБОЕ", None)): 
                pass
            btt = BlockTitleToken.try_attach(tt, False, chapter_names)
            if (btt is None): 
                continue
            if (len(res) == 104): 
                pass
            tt = btt.end_token
            if (content is not None and btt.typ == BlkTyps.INDEX): 
                continue
            if (len(res) > 0 and res[len(res) - 1].typ == BlkTyps.LITERATURE): 
                if (btt.typ != BlkTyps.APPENDIX and btt.typ != BlkTyps.MISC and btt.typ != BlkTyps.LITERATURE): 
                    if (btt.typ == BlkTyps.CHAPTER and (res[len(res) - 1].end_char < (math.floor((len(tt.kit.sofa.text) * 3) / 4)))): 
                        pass
                    else: 
                        continue
            if (first): 
                if ((tt.begin_char - t0.begin_char) > 300): 
                    btt0 = BlockTitleToken(t0, (t0 if t0.previous is None else t0.previous))
                    btt0.typ = BlkTyps.CHAPTER
                    btt0.value = "Похоже на начало"
                    res.append(btt0)
            res.append(btt)
            tt = btt.end_token
            first = False
        i = 0
        while i < (len(res) - 1): 
            if (res[i].typ == BlkTyps.LITERATURE and res[i + 1].typ == res[i].typ): 
                del res[i + 1]
                i -= 1
            i += 1
        return res
    
    @staticmethod
    def try_attach(t : 'Token', is_content_item : bool=False, names : 'TerminCollection'=None) -> 'BlockTitleToken':
        if (t is None): 
            return None
        if (not t.is_newline_before): 
            return None
        if (t.chars.is_all_lower): 
            return None
        li = BlockLine.create(t, names)
        if (li is None): 
            return None
        if (li.words == 0 and li.typ == BlkTyps.UNDEFINED): 
            return None
        if (li.typ == BlkTyps.INDEX): 
            pass
        if (li.is_exist_name): 
            return BlockTitleToken._new392(t, li.end_token, li.typ)
        if (li.end_token == li.number_end or ((li.end_token.is_char_of(".:") and li.end_token.previous == li.number_end))): 
            res2 = BlockTitleToken._new392(t, li.end_token, li.typ)
            if (li.typ == BlkTyps.CHAPTER or li.typ == BlkTyps.APPENDIX): 
                li2 = BlockLine.create(li.end_token.next0_, names)
                if ((li2 is not None and li2.typ == BlkTyps.UNDEFINED and li2.is_all_upper) and li2.words > 0): 
                    res2.end_token = li2.end_token
                    tt = res2.end_token.next0_
                    while tt is not None: 
                        li2 = BlockLine.create(tt, names)
                        if (li2 is None): 
                            break
                        if (li2.typ != BlkTyps.UNDEFINED or not li2.is_all_upper or li2.words == 0): 
                            break
                        res2.end_token = li2.end_token
                        tt = res2.end_token
                        tt = tt.next0_
            return res2
        if (li.number_end is None): 
            return None
        res = BlockTitleToken._new392(t, li.end_token, li.typ)
        if (res.typ == BlkTyps.UNDEFINED): 
            if (li.words < 1): 
                return None
            if (li.has_verb): 
                return None
            if (not is_content_item): 
                if (not li.is_all_upper or li.not_words > (math.floor(li.words / 2))): 
                    return None
            res.typ = BlkTyps.CHAPTER
            if ((li.number_end.end_char - t.begin_char) == 7 and li.number_end.next0_ is not None and li.number_end.next0_.is_hiphen): 
                res.typ = BlkTyps.UNDEFINED
        if (li.has_content_item_tail and is_content_item): 
            res.typ = BlkTyps.INDEXITEM
        if (res.typ == BlkTyps.CHAPTER or res.typ == BlkTyps.APPENDIX): 
            if (li.has_verb): 
                return None
            if (li.not_words > li.words and not is_content_item): 
                return None
            t = li.end_token.next0_
            while t is not None: 
                li2 = BlockLine.create(t, names)
                if (li2 is None): 
                    break
                if (li2.has_verb or (li2.words < 1)): 
                    break
                if (not li2.is_all_upper and not is_content_item): 
                    break
                if (li2.typ != BlkTyps.UNDEFINED or li2.number_end is not None): 
                    break
                res.end_token = li2.end_token
                t = res.end_token
                if (is_content_item and li2.has_content_item_tail): 
                    res.typ = BlkTyps.INDEXITEM
                    break
                t = t.next0_
        tt = res.end_token
        while tt is not None and tt.begin_char > li.number_end.end_char: 
            if ((isinstance(tt, TextToken)) and tt.chars.is_letter): 
                res.value = MiscHelper.get_text_value(li.number_end.next0_, tt, GetTextAttr.NO)
                break
            tt = tt.previous
        if ((res.typ == BlkTyps.INDEX or res.typ == BlkTyps.INTRO or res.typ == BlkTyps.CONSLUSION) or res.typ == BlkTyps.LITERATURE): 
            if (res.value is not None and len(res.value) > 100): 
                return None
            if (li.words < li.not_words): 
                return None
        return res
    
    @staticmethod
    def _new392(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'BlkTyps') -> 'BlockTitleToken':
        res = BlockTitleToken(_arg1, _arg2)
        res.typ = _arg3
        return res