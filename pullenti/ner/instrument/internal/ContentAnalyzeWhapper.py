# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing
import math
from pullenti.unisharp.Utils import Utils

from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.Referent import Referent
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.decree.DecreeReferent import DecreeReferent
from pullenti.ner.instrument.internal.EditionHelper import EditionHelper
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.decree.DecreeKind import DecreeKind
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.instrument.InstrumentKind import InstrumentKind
from pullenti.ner.TextToken import TextToken
from pullenti.ner.instrument.internal.ContractHelper import ContractHelper
from pullenti.ner.decree.DecreePartReferent import DecreePartReferent
from pullenti.ner.instrument.internal.NumberTypes import NumberTypes

class ContentAnalyzeWhapper:
    
    def __init__(self) -> None:
        self.doc_typ = DecreeKind.UNDEFINED
        self.top_doc = None;
        self.lines = None;
        self.cit_kind = InstrumentKind.UNDEFINED
    
    def analyze(self, root : 'FragToken', top_doc_ : 'FragToken', is_citat : bool, root_kind : 'InstrumentKind') -> None:
        from pullenti.ner.instrument.internal.InstrToken1 import InstrToken1
        from pullenti.ner.instrument.internal.ListHelper import ListHelper
        self.top_doc = top_doc_
        self.cit_kind = root_kind
        lines_ = list()
        directives = 0
        parts = 0
        if (top_doc_ is not None and top_doc_._m_doc is not None): 
            ty = top_doc_._m_doc.typ
            if (ty is not None): 
                if (("КОДЕКС" in ty or "ЗАКОН" in ty or "КОНСТИТУЦИЯ" in ty) or "КОНСТИТУЦІЯ" in ty): 
                    self.doc_typ = DecreeKind.KODEX
                elif ("ДОГОВОР" in ty or "ДОГОВІР" in ty or "КОНТРАКТ" in ty): 
                    self.doc_typ = DecreeKind.CONTRACT
        t = root.begin_token
        first_pass3676 = True
        while True:
            if first_pass3676: first_pass3676 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.begin_char > root.end_token.end_char): 
                break
            dpr = Utils.asObjectOrNull(t.get_referent(), DecreePartReferent)
            if (dpr is not None and dpr.local_typ is not None and (((dpr.chapter is not None or dpr.clause is not None or dpr.section is not None) or dpr.sub_section is not None))): 
                t = t.kit.debed_token(t)
            if (len(lines_) == 120): 
                pass
            lt = InstrToken1.parse(t, False, top_doc_, 0, (lines_[len(lines_) - 1] if len(lines_) > 0 else None), is_citat and t == root.begin_token, root.end_token.end_char, False, False)
            if (lt is None): 
                continue
            if (lt.typ == InstrToken1.Types.CLAUSE and len(lt.numbers) == 1 and lt.numbers[0] == "13"): 
                pass
            if (lt.num_typ == NumberTypes.DIGIT and len(lt.numbers) == 1 and lt.numbers[0] == "10"): 
                pass
            if (lt.typ == InstrToken1.Types.EDITIONS): 
                if ((not lt.is_newline_after and lt.end_token.next0_ is not None and lt.end_token.next0_.is_newline_after) and (isinstance(lt.end_token.next0_, TextToken)) and not lt.end_token.next0_.chars.is_letter): 
                    lt.end_token = lt.end_token.next0_
            if (len(lt.numbers) > 0): 
                pass
            if (len(lines_) == 0 and root_kind != InstrumentKind.UNDEFINED): 
                if ((root_kind == InstrumentKind.INDENTION or root_kind == InstrumentKind.ITEM or root_kind == InstrumentKind.SUBITEM) or root_kind == InstrumentKind.CLAUSEPART): 
                    lt.typ = InstrToken1.Types.LINE
                elif (root_kind == InstrumentKind.CHAPTER): 
                    lt.typ = InstrToken1.Types.CHAPTER
                elif (root_kind == InstrumentKind.CLAUSE): 
                    lt.typ = InstrToken1.Types.CLAUSE
                elif (root_kind == InstrumentKind.SECTION): 
                    lt.typ = InstrToken1.Types.SECTION
                elif (root_kind == InstrumentKind.SUBSECTION): 
                    lt.typ = InstrToken1.Types.SUBSECTION
                elif (root_kind == InstrumentKind.DOCPART): 
                    lt.typ = InstrToken1.Types.DOCPART
            if (lt.typ == InstrToken1.Types.CLAUSE and lt.first_number == 103): 
                pass
            if (lt.end_char > root.end_char): 
                lt.end_token = root.end_token
            if (lt.typ == InstrToken1.Types.DIRECTIVE): 
                directives += 1
            if ((lt.num_typ == NumberTypes.LETTER and len(lt.numbers) == 1 and lt.last_number > 1) and root_kind != InstrumentKind.SUBITEM and root_kind != InstrumentKind.ITEM): 
                ok = False
                for i in range(len(lines_) - 1, -1, -1):
                    if (lines_[i].num_typ == lt.num_typ): 
                        j = lt.last_number - lines_[i].last_number
                        ok = (j == 1 or j == 2)
                        break
                if (not ok): 
                    lt.num_typ = NumberTypes.UNDEFINED
                    lt.numbers.clear()
            if (lt.typ_container_rank > 0 and not lt.is_num_doubt): 
                parts += 1
            lines_.append(lt)
            t = lt.end_token
        ListHelper.correct_index(lines_)
        ListHelper.correct_app_list(lines_)
        if (directives > 0 and directives > parts): 
            self.__analize_content_with_directives(root, lines_, top_doc_._m_doc is not None and top_doc_._m_doc.case_number is not None)
        else: 
            self.__analize_content_with_containers(root, lines_, 0, top_doc_)
        self.__analize_preamble(root)
        root._analize_tables()
        if (self.doc_typ == DecreeKind.CONTRACT): 
            pass
        else: 
            self.__correct_kodex_parts(root)
        self.__analize_sections(root)
        self.__correct_names(root, None)
        EditionHelper.analize_editions(root)
        if (self.doc_typ == DecreeKind.CONTRACT): 
            ContractHelper.correct_dummy_newlines(root)
        ListHelper.analyze(root)
        if (root_kind == InstrumentKind.CLAUSEPART or root_kind == InstrumentKind.ITEM or root_kind == InstrumentKind.SUBITEM): 
            for ch in root.children: 
                if (ch.kind == InstrumentKind.ITEM): 
                    if (root_kind == InstrumentKind.CLAUSEPART): 
                        ch.kind = InstrumentKind.CLAUSEPART
                        for chh in ch.children: 
                            if (chh.kind == InstrumentKind.SUBITEM): 
                                chh.kind = InstrumentKind.ITEM
                    elif (root_kind == InstrumentKind.SUBITEM): 
                        ch.kind = InstrumentKind.SUBITEM
        self.__post_correct(root, lines_)
    
    def __post_correct(self, root : 'FragToken', lines_ : typing.List['InstrToken1']) -> None:
        for ch in root.children: 
            self.__post_correct(ch, lines_)
        if (len(root.children) > 0): 
            if (root.end_char < root.children[len(root.children) - 1].end_char): 
                root.end_token = root.children[len(root.children) - 1].end_token
            if (root.begin_char > root.children[0].begin_char): 
                root.begin_token = root.children[0].begin_token
    
    def __analize_content_with_containers(self, root : 'FragToken', lines_ : typing.List['InstrToken1'], top_level : int, top_doc_ : 'FragToken') -> None:
        """ Анализ текстов, явно содержащих главы, разделы, статьи и т.п.
        
        Args:
            lines_(typing.List[InstrToken1]): 
            proc: 
        """
        from pullenti.ner.instrument.internal.FragToken import FragToken
        from pullenti.ner.instrument.internal.InstrToken1 import InstrToken1
        from pullenti.ner.instrument.internal.NumberingHelper import NumberingHelper
        nums = list()
        k = 0
        lev = 100
        li0 = None
        koef = 0
        if (((root.kind == InstrumentKind.PARAGRAPH and len(lines_) > 10 and lines_[0].typ == InstrToken1.Types.LINE) and len(lines_[0].numbers) > 0 and not lines_[0].has_verb) and lines_[1].typ == InstrToken1.Types.CLAUSE): 
            nums.append(lines_[0])
            ii = 2
            first_pass3677 = True
            while True:
                if first_pass3677: first_pass3677 = False
                else: ii += 1
                if (not (ii < (len(lines_) - 1))): break
                ch = lines_[ii]
                if (ch.typ != InstrToken1.Types.LINE or ch.has_verb or len(ch.numbers) != len(nums[0].numbers)): 
                    continue
                la = nums[len(nums) - 1]
                if (NumberingHelper.calc_delta(la, ch, False) != 1): 
                    continue
                if (la.num_typ != ch.num_typ or la.num_suffix != ch.num_suffix): 
                    continue
                if (ch.end_token.is_char('.')): 
                    if (not la.end_token.is_char('.')): 
                        continue
                has_clause = False
                jj = ii + 1
                while jj < len(lines_): 
                    if (lines_[jj].typ == InstrToken1.Types.CLAUSE): 
                        has_clause = True
                        break
                    elif (lines_[jj].typ != InstrToken1.Types.COMMENT and lines_[jj].typ != InstrToken1.Types.EDITIONS): 
                        break
                    jj += 1
                if (has_clause): 
                    nums.append(ch)
            if (len(nums) < 2): 
                nums.clear()
            else: 
                koef = 2
                for nn in nums: 
                    nn.typ = InstrToken1.Types.SUBPARAGRAPH
                    lev = nn.typ_container_rank
        if (len(nums) == 0): 
            for li in lines_: 
                if (li.typ == InstrToken1.Types.COMMENT or li.typ == InstrToken1.Types.EDITIONS): 
                    continue
                if (li0 is None): 
                    li0 = li
                k += 1
                if (li.typ_container_rank > top_level): 
                    if (li.typ_container_rank < lev): 
                        if (len(nums) > 2 and len(li.numbers) == 0): 
                            pass
                        elif (k > 20): 
                            pass
                        else: 
                            lev = li.typ_container_rank
                            nums.clear()
                    if (li.typ_container_rank == lev): 
                        nums.append(li)
            i = 0
            first_pass3678 = True
            while True:
                if first_pass3678: first_pass3678 = False
                else: i += 1
                if (not (i < len(nums))): break
                d0 = (NumberingHelper.calc_delta(nums[i - 1], nums[i], True) if i > 0 else 0)
                d1 = (NumberingHelper.calc_delta(nums[i], nums[i + 1], True) if (i + 1) < len(nums) else 0)
                d01 = (NumberingHelper.calc_delta(nums[i - 1], nums[i + 1], True) if i > 0 and ((i + 1) < len(nums)) else 0)
                if (d0 == 1): 
                    if (d1 == 1): 
                        continue
                    if (d01 == 1 and not nums[i + 1].is_num_doubt and nums[i].is_num_doubt): 
                        del nums[i]
                        i -= 1
                    continue
                if (d01 == 1 and nums[i].is_num_doubt): 
                    del nums[i]
                    i -= 1
                    continue
            i = 1
            while i < len(nums): 
                d = NumberingHelper.calc_delta(nums[i - 1], nums[i], True)
                if (d == 1): 
                    koef += 2
                elif (d == 2): 
                    koef += 1
                elif (d <= 0): 
                    koef -= 1
                i += 1
            if (len(nums) > 0): 
                has_num_before = False
                for li in lines_: 
                    if (li == nums[0]): 
                        break
                    elif (len(li.numbers) > 0): 
                        has_num_before = True
                if (not has_num_before and ((nums[0].last_number == 1 or ((nums[0] == li0 and nums[0].num_suffix is not None))))): 
                    koef += 2
                elif (nums[0].typ == InstrToken1.Types.CLAUSE and nums[0] == li0): 
                    koef += 2
        is_chapters = False
        if (len(nums) == 0): 
            chaps = 0
            nons = 0
            clauses = 0
            i = 0
            while i < len(lines_): 
                li = lines_[i]
                if (li.typ == InstrToken1.Types.CHAPTER): 
                    nums.append(li)
                    chaps += 1
                    lev = li.typ_container_rank
                elif (li.typ == InstrToken1.Types.LINE and li.title_typ != InstrToken1.StdTitleType.UNDEFINED): 
                    nums.append(li)
                    nons += 1
                elif (li.typ == InstrToken1.Types.CLAUSE): 
                    clauses += 1
                i += 1
            if (chaps == 0): 
                nums.clear()
            else: 
                koef += 2
                is_chapters = True
        if (koef < 2): 
            if (top_level < InstrToken1._calc_rank(InstrToken1.Types.CHAPTER)): 
                if (self.__analize_chapter_without_keywords(root, lines_, top_doc_)): 
                    return
            self.__analize_content_without_containers(root, lines_, False, False, False)
            return
        n = 0
        names = 0
        fr = None
        blk = list()
        i = 0
        first_pass3679 = True
        while True:
            if first_pass3679: first_pass3679 = False
            else: i += 1
            if (not (i <= len(lines_))): break
            li = (lines_[i] if i < len(lines_) else None)
            if (li is None or (((n < len(nums)) and li == nums[n]))): 
                if (len(blk) > 0): 
                    if (fr is None): 
                        fr = FragToken._new1340(blk[0].begin_token, blk[len(blk) - 1].end_token, InstrumentKind.CONTENT)
                        if (len(blk) == 1): 
                            fr._itok = blk[0]
                        root.children.append(fr)
                    fr.end_token = blk[len(blk) - 1].end_token
                    self.__analize_content_with_containers(fr, blk, lev, top_doc_)
                    blk.clear()
                    fr = (None)
            if (li is None): 
                break
            if ((n < len(nums)) and li == nums[n]): 
                n += 1
                fr = FragToken._new1341(li.begin_token, li.end_token, li, li.is_expired)
                root.children.append(fr)
                if (li.typ == InstrToken1.Types.DOCPART): 
                    fr.kind = InstrumentKind.DOCPART
                elif (li.typ == InstrToken1.Types.CLAUSEPART): 
                    fr.kind = InstrumentKind.CLAUSEPART
                elif (li.typ == InstrToken1.Types.SECTION): 
                    fr.kind = InstrumentKind.SECTION
                elif (li.typ == InstrToken1.Types.SUBSECTION): 
                    fr.kind = InstrumentKind.SUBSECTION
                elif (li.typ == InstrToken1.Types.PARAGRAPH): 
                    fr.kind = InstrumentKind.PARAGRAPH
                elif (li.typ == InstrToken1.Types.SUBPARAGRAPH): 
                    fr.kind = InstrumentKind.SUBPARAGRAPH
                elif (li.typ == InstrToken1.Types.CHAPTER): 
                    fr.kind = InstrumentKind.CHAPTER
                elif (li.typ == InstrToken1.Types.CLAUSE): 
                    fr.kind = InstrumentKind.CLAUSE
                elif (li.typ == InstrToken1.Types.NOTICE): 
                    fr.kind = InstrumentKind.NOTICE
                elif (is_chapters): 
                    fr.kind = InstrumentKind.CHAPTER
                if (li.begin_token != li.num_begin_token and li.num_begin_token is not None): 
                    fr.children.append(FragToken._new1342(li.begin_token, li.num_begin_token.previous, InstrumentKind.KEYWORD, True, li))
                NumberingHelper.create_number(fr, li)
                if (li.num_end_token != li.end_token and li.num_end_token is not None): 
                    if (not li.all_upper and ((((li.has_verb and names == 0 and li.end_token.is_char_of(".:"))) or li.end_token.is_char(':')))): 
                        fr.children.append(FragToken._new1340(li.num_end_token.next0_, li.end_token, InstrumentKind.CONTENT))
                    else: 
                        fr_name = FragToken._new1342(li.num_end_token.next0_, li.end_token, InstrumentKind.NAME, True, li)
                        fr.children.append(fr_name)
                        fr.name = FragToken._get_restored_namemt(fr_name, False)
                        i = ContentAnalyzeWhapper.__correct_name(fr, fr_name, lines_, i)
                        names += 1
                elif (li.title_typ != InstrToken1.StdTitleType.UNDEFINED): 
                    fr_name = FragToken._new1342(li.begin_token, li.end_token, InstrumentKind.NAME, True, li)
                    fr.children.append(fr_name)
                    fr.name = FragToken._get_restored_namemt(fr_name, False)
                    i = ContentAnalyzeWhapper.__correct_name(fr, fr_name, lines_, i)
                    names += 1
                elif ((((i + 1) < len(lines_)) and len(lines_[i + 1].numbers) == 0 and not lines_[i + 1].has_verb) and not lines_[i + 1].has_many_spec_chars): 
                    if (lines_[i + 1].all_upper or ((lines_[i + 1].begin_token.is_char('['))) or lines_[i].end_token.is_char('.')): 
                        i += 1
                        li = lines_[i]
                        fr.end_token = li.end_token
                        fr_name = FragToken._new1342(li.begin_token, li.end_token, InstrumentKind.NAME, True, li)
                        fr.children.append(fr_name)
                        fr.name = FragToken._get_restored_namemt(fr_name, False)
                        i = ContentAnalyzeWhapper.__correct_name(fr, fr_name, lines_, i)
                        names += 1
                continue
            if (li.typ == InstrToken1.Types.EDITIONS and len(blk) == 0 and fr is not None): 
                fr.children.append(FragToken._new1340(li.begin_token, li.end_token, InstrumentKind.EDITIONS))
            else: 
                blk.append(li)
    
    @staticmethod
    def __correct_name(fr : 'FragToken', fr_name : 'FragToken', lines_ : typing.List['InstrToken1'], i : int) -> int:
        from pullenti.ner.instrument.internal.FragToken import FragToken
        from pullenti.ner.instrument.internal.InstrToken1 import InstrToken1
        if ((i + 1) >= len(lines_)): 
            return i
        li = lines_[i]
        if (li.typ == InstrToken1.Types.SUBSECTION): 
            pass
        if (fr.name is not None and (len(fr.name) < 100)): 
            while (i + 1) < len(lines_): 
                if (len(fr.name) > 500): 
                    break
                lii = lines_[i + 1]
                if (len(lii.numbers) > 0 or lii.typ != InstrToken1.Types.LINE): 
                    break
                if (lii.end_token.is_char(':')): 
                    break
                if (li.end_token.is_char_of(";")): 
                    break
                if (li.end_token.is_char('.')): 
                    if (lii.all_upper and li.all_upper): 
                        pass
                    else: 
                        break
                if (li.all_upper and not lii.all_upper): 
                    break
                if ((li.length_char < (math.floor(lii.length_char / 2))) and lii.has_verb): 
                    break
                if (li.has_many_spec_chars): 
                    break
                if (lii.begin_token.whitespaces_before_count > 15): 
                    break
                if (lii.begin_token.is_value("НЕТ", None) or lii.begin_token.is_value("НЕ", None) or lii.begin_token.is_value("ОТСУТСТВОВАТЬ", None)): 
                    break
                if (not (isinstance(lii.begin_token, TextToken))): 
                    break
                mc = lii.begin_token.get_morph_class_in_dictionary()
                if (mc.is_undefined): 
                    break
                tt = lii.begin_token
                while isinstance(tt, MetaToken):
                    tt = tt.begin_token
                if (tt.chars.is_capital_upper or not tt.chars.is_letter or mc.is_preposition): 
                    if (not li.end_token.is_char(',') and not li.end_token.is_hiphen and not li.end_token.morph.class0_.is_conjunction): 
                        break
                li = lii
                fr.end_token = fr_name.end_token = li.end_token
                fr_name._def_val2 = True
                fr.name = FragToken._get_restored_namemt(fr_name, False)
                i += 1
        return i
    
    def __analize_chapter_without_keywords(self, root : 'FragToken', lines_ : typing.List['InstrToken1'], top_doc_ : 'FragToken') -> bool:
        """ Анализ ситуации, когда главы без ключевых слов, только цифра + наименование
        
        Args:
            lines_(typing.List[InstrToken1]): 
            proc: 
        
        """
        from pullenti.ner.instrument.internal.FragToken import FragToken
        from pullenti.ner.instrument.internal.InstrToken1 import InstrToken1
        from pullenti.ner.instrument.internal.NumberingHelper import NumberingHelper
        nums = NumberingHelper.extract_main_sequence(lines_, True, False)
        is_contract_struct = False
        if (nums is None or len(nums[0].numbers) != 1 or nums[0].numbers[0] != "1"): 
            if (self.doc_typ == DecreeKind.CONTRACT): 
                nums1 = list()
                num0 = "1"
                ok = True
                i = 1
                first_pass3680 = True
                while True:
                    if first_pass3680: first_pass3680 = False
                    else: i += 1
                    if (not (i < len(lines_))): break
                    li = lines_[i]
                    li0 = lines_[i - 1]
                    if ((len(nums1) > 0 and nums1[0].title_typ == InstrToken1.StdTitleType.SUBJECT and len(nums1[0].numbers) == 0) and nums1[0].all_upper): 
                        if (len(li0.numbers) <= 1 and ((li0.all_upper or li0.title_typ != InstrToken1.StdTitleType.UNDEFINED))): 
                            nums1.append(li0)
                        continue
                    if (len(li.numbers) == 2 and li.numbers[0] == num0 and li.numbers[1] == "1"): 
                        if (len(li0.numbers) == 0 and not li0.begin_token.chars.is_all_lower): 
                            pass
                        elif (len(li0.numbers) == 1 and li0.numbers[0] == num0): 
                            pass
                        else: 
                            ok = False
                            break
                        nums1.append(li0)
                        num0 = str((len(nums1) + 1))
                        continue
                    if (li0.title_typ != InstrToken1.StdTitleType.UNDEFINED or ((len(li0.numbers) == 1 and li0.numbers[0] == num0))): 
                        nums1.append(li0)
                        num0 = str((len(nums1) + 1))
                if (ok and len(nums1) > 1): 
                    nums = nums1
                    is_contract_struct = True
        if (nums is None): 
            return False
        if (len(nums) > 500): 
            return False
        n = 0
        err = 0
        fr = None
        blk = list()
        childs = list()
        i = 0
        first_pass3681 = True
        while True:
            if first_pass3681: first_pass3681 = False
            else: i += 1
            if (not (i <= len(lines_))): break
            li = (lines_[i] if i < len(lines_) else None)
            if (li is None or (((n < len(nums)) and li == nums[n])) or ((n >= len(nums) and li.title_typ != InstrToken1.StdTitleType.UNDEFINED))): 
                if (len(blk) > 0): 
                    if (fr is None): 
                        fr = FragToken._new1340(blk[0].begin_token, blk[len(blk) - 1].end_token, InstrumentKind.CONTENT)
                        if (len(blk) == 1): 
                            fr._itok = blk[0]
                        childs.append(fr)
                    fr.end_token = blk[len(blk) - 1].end_token
                    self.__analize_content_without_containers(fr, blk, False, False, False)
                    blk.clear()
                    fr = (None)
            if (li is None): 
                break
            if ((n < len(nums)) and li == nums[n]): 
                n += 1
                if (not li.all_upper and li.has_verb): 
                    if (((li.num_typ == NumberTypes.ROMAN and n >= 2 and len(childs) > 0) and childs[len(childs) - 1].kind == InstrumentKind.CHAPTER and li.num_typ == nums[n - 2].num_typ) and NumberingHelper.calc_delta(nums[n - 2], li, False) == 1): 
                        pass
                    else: 
                        blk.append(li)
                        continue
                fr = FragToken._new1349(li.begin_token, li.end_token, li)
                childs.append(fr)
                fr.kind = InstrumentKind.CHAPTER
                NumberingHelper.create_number(fr, li)
                if (li.num_end_token != li.end_token and li.num_end_token is not None): 
                    if (li.has_many_spec_chars): 
                        fr.children.append(FragToken._new1350(li.num_end_token.next0_, li.end_token, InstrumentKind.CONTENT, li))
                    else: 
                        fr_name = FragToken._new1342(li.num_end_token.next0_, li.end_token, InstrumentKind.NAME, True, li)
                        fr.children.append(fr_name)
                        fr.name = FragToken._get_restored_namemt(fr_name, False)
                        i = ContentAnalyzeWhapper.__correct_name(fr, fr_name, lines_, i)
                elif (is_contract_struct): 
                    fr_name = FragToken._new1342(li.begin_token, li.end_token, InstrumentKind.NAME, True, li)
                    fr.children.append(fr_name)
                    fr.name = FragToken._get_restored_namemt(fr_name, False)
                continue
            elif (n >= len(nums) and li.title_typ != InstrToken1.StdTitleType.UNDEFINED): 
                fr = FragToken._new1349(li.begin_token, li.end_token, li)
                fr.kind = childs[len(childs) - 1].kind
                childs.append(fr)
                fr_name = FragToken._new1342(li.begin_token, li.end_token, InstrumentKind.NAME, True, li)
                fr.children.append(fr_name)
                fr.name = FragToken._get_restored_namemt(fr_name, False)
                i = ContentAnalyzeWhapper.__correct_name(fr, fr_name, lines_, i)
                continue
            if (len(blk) == 0 and li.has_many_spec_chars): 
                err += 1
            blk.append(li)
        coef = - err
        i = 0
        while i < len(childs): 
            chap = childs[i]
            if (i == 0 and chap.number == 0 and chap.length_char > 1000): 
                coef -= 1
            else: 
                nam = chap.name
                if (nam is None): 
                    coef -= 1
                elif (len(nam) > 300): 
                    coef -= (math.floor(len(nam) / 300))
                else: 
                    coef += 1
                    len0_ = chap.length_char - len(nam)
                    if (len0_ > 200): 
                        coef += 1
                    elif (len(chap.children) < 3): 
                        coef -= 1
            for ch in chap.children: 
                if (ch.kind == InstrumentKind.NAME): 
                    if (ch.end_token.is_char_of(":;")): 
                        coef -= 2
                    break
                if (ch.number == 0): 
                    continue
                if (ch._itok is None): 
                    break
                break
            i += 1
        if (coef < 3): 
            if (err > 2): 
                return True
            return False
        root.children.extend(childs)
        if (top_doc_ is not None and top_doc_._m_doc is not None and top_doc_._m_doc.typ is not None): 
            ty = top_doc_._m_doc.typ
            if (self.doc_typ == DecreeKind.CONTRACT): 
                ok = True
                for ch in childs: 
                    if (ch.kind == InstrumentKind.CHAPTER): 
                        for chh in ch.children: 
                            if (chh.kind == InstrumentKind.CLAUSE): 
                                ok = False
                if (ok): 
                    for ch in childs: 
                        if (ch.kind == InstrumentKind.CHAPTER): 
                            ch.kind = InstrumentKind.CLAUSE
        return True
    
    def __add_comment_or_edition(self, fr : 'FragToken', li : 'InstrToken1') -> None:
        from pullenti.ner.instrument.internal.FragToken import FragToken
        from pullenti.ner.instrument.internal.InstrToken1 import InstrToken1
        if (li.typ == InstrToken1.Types.COMMENT): 
            fr.children.append(FragToken._new1350(li.begin_token, li.end_token, InstrumentKind.COMMENT, li))
        elif (li.typ == InstrToken1.Types.EDITIONS): 
            edt = FragToken._new1350(li.begin_token, li.end_token, InstrumentKind.EDITIONS, li)
            fr.children.append(edt)
            edt.referents = list()
            tt = li.begin_token
            while tt is not None: 
                if (tt.end_char > li.end_token.end_char): 
                    break
                dr = Utils.asObjectOrNull(tt.get_referent(), DecreeReferent)
                if (dr is not None): 
                    if (not dr in edt.referents): 
                        edt.referents.append(dr)
                tt = tt.next0_
    
    def __analize_content_without_containers(self, root : 'FragToken', lines_ : typing.List['InstrToken1'], is_subitem : bool, is_preamble : bool=False, is_kodex : bool=False) -> None:
        from pullenti.ner.instrument.internal.FragToken import FragToken
        from pullenti.ner.instrument.internal.InstrToken1 import InstrToken1
        from pullenti.ner.instrument.internal.NumberingHelper import NumberingHelper
        if (root.kind == InstrumentKind.CHAPTER): 
            pass
        if (root.kind == InstrumentKind.CLAUSE or ((root.kind == InstrumentKind.CHAPTER and self.doc_typ == DecreeKind.CONTRACT))): 
            if (root.number == 8): 
                pass
            while len(lines_) > 0:
                if (lines_[0].typ == InstrToken1.Types.COMMENT or lines_[0].typ == InstrToken1.Types.EDITIONS): 
                    self.__add_comment_or_edition(root, lines_[0])
                    del lines_[0]
                else: 
                    break
            if (len(lines_) == 0): 
                return
            if ((len(lines_) > 2 and len(lines_[0].numbers) == 0 and lines_[0].end_token.is_char_of(":")) and len(lines_[1].numbers) > 0): 
                pass
            if (len(lines_[0].numbers) == 0 and self.doc_typ != DecreeKind.CONTRACT): 
                parts = list()
                tmp = list()
                part = None
                ii = 0
                while ii < len(lines_): 
                    li = lines_[ii]
                    if ((ii > 0 and len(li.numbers) == 0 and li.typ != InstrToken1.Types.EDITIONS) and li.typ != InstrToken1.Types.COMMENT and part is not None): 
                        if (MiscHelper.can_be_start_of_sentence(li.begin_token)): 
                            end = True
                            for j in range(ii - 1, -1, -1):
                                if (lines_[j].typ != InstrToken1.Types.COMMENT and lines_[j].typ != InstrToken1.Types.EDITIONS): 
                                    tt = lines_[j].end_token
                                    if (not tt.is_char_of(".")): 
                                        if (tt.newlines_after_count < 2): 
                                            end = False
                                        elif (tt.is_char_of(":,;")): 
                                            end = False
                                    break
                            if (end): 
                                self.__analize_content_without_containers(part, tmp, False, False, is_kodex)
                                tmp.clear()
                                part = (None)
                    if (part is None): 
                        part = FragToken._new1357(li.begin_token, li.end_token, InstrumentKind.CLAUSEPART, len(parts) + 1)
                        parts.append(part)
                    if (li.end_char > part.end_char): 
                        part.end_token = li.end_token
                    tmp.append(li)
                    ii += 1
                if (part is not None and len(tmp) > 0): 
                    self.__analize_content_without_containers(part, tmp, False, False, is_kodex)
                ok = True
                if (root.kind != InstrumentKind.CLAUSE): 
                    num = 0
                    tot = 0
                    for p in parts: 
                        for ch in p.children: 
                            if (ch.number > 0): 
                                num += 1
                            tot += 1
                    if ((math.floor(tot / 2)) > num): 
                        ok = False
                if (ok): 
                    for p in parts: 
                        NumberingHelper.correct_child_numbers(root, p.children)
                    if (len(parts) > 1): 
                        root.children.extend(parts)
                        return
                    elif (len(parts) == 1): 
                        root.children.extend(parts[0].children)
                        return
        if (root.number == 11 and root.sub_number == 2): 
            pass
        notices = list()
        ii = 0
        while ii < len(lines_): 
            if (lines_[ii].typ == InstrToken1.Types.NOTICE): 
                li = lines_[ii]
                if (((len(li.numbers) == 1 and li.numbers[0] == "1")) or ((len(li.numbers) == 0 and ii == (len(lines_) - 1)))): 
                    j = ii
                    while j < len(lines_): 
                        li = lines_[j]
                        not0_ = FragToken._new1350(li.begin_token, li.end_token, InstrumentKind.NOTICE, li)
                        notices.append(not0_)
                        if (li.num_begin_token is not None and li.begin_token != li.num_begin_token): 
                            not0_.children.append(FragToken._new1359(li.begin_token, li.num_begin_token.previous, InstrumentKind.KEYWORD, True))
                        if (len(li.numbers) > 0): 
                            NumberingHelper.create_number(not0_, li)
                        if (len(not0_.children) > 0): 
                            not0_.children.append(FragToken._new1350(Utils.ifNotNull(li.num_end_token, li.begin_token), li.end_token, InstrumentKind.CONTENT, li))
                        j += 1
                    del lines_[ii:ii+len(lines_) - ii]
                break
            ii += 1
        nums = NumberingHelper.extract_main_sequence(lines_, self.doc_typ != DecreeKind.CONTRACT or self.top_doc.kind == InstrumentKind.APPENDIX, self.doc_typ != DecreeKind.CONTRACT)
        if (len(lines_) > 5): 
            pass
        if (is_kodex and nums is not None): 
            err_cou = 0
            for nu in nums: 
                if (nu.num_suffix is not None and nu.num_suffix != ")" and nu.num_suffix != "."): 
                    err_cou += 1
            if (err_cou > 0): 
                if (err_cou > (math.floor(len(nums) / 2))): 
                    nums = (None)
        if (nums is None): 
            last = (root.children[len(root.children) - 1] if len(root.children) > 0 else None)
            for li in lines_: 
                if (li.typ == InstrToken1.Types.COMMENT or li.typ == InstrToken1.Types.EDITIONS): 
                    self.__add_comment_or_edition(root, li)
                    last = (None)
                    continue
                if (li.typ == InstrToken1.Types.INDEX): 
                    ind = FragToken._new1350(li.begin_token, li.end_token, InstrumentKind.INDEX, li)
                    root.children.append(ind)
                    last = (None)
                    tt = li.begin_token
                    if (not li.index_no_keyword): 
                        while tt is not None and tt.end_char <= li.end_char: 
                            if (tt.is_newline_after): 
                                ind.children.append(FragToken._new1362(li.begin_token, tt, InstrumentKind.NAME, True))
                                tt = tt.next0_
                                break
                            tt = tt.next0_
                    is_tab = False
                    first_pass3682 = True
                    while True:
                        if first_pass3682: first_pass3682 = False
                        else: tt = tt.next0_
                        if (not (tt is not None and tt.end_char <= li.end_char)): break
                        it1 = InstrToken1.parse(tt, True, None, 0, None, False, 0, False, True)
                        if (it1 is None): 
                            break
                        if ((not is_tab and it1.end_char == li.end_char and tt.is_table_control_char) and it1.length_char > 100): 
                            it2 = InstrToken1.parse(tt.next0_, True, None, 0, None, False, 0, False, True)
                            if (it2 is None): 
                                break
                            it1 = it2
                            tt = tt.next0_
                        if (it1.value == "СТР"): 
                            tt = it1.end_token
                            continue
                        if (isinstance(tt.get_referent(), DecreePartReferent)): 
                            tt = tt.kit.debed_token(tt)
                            it1 = InstrToken1.parse(tt, True, None, 0, None, False, 0, False, False)
                        if (it1.typ == InstrToken1.Types.APPENDIX and not it1.is_newline_after): 
                            ttt = it1.end_token
                            while ttt is not None: 
                                if (ttt.is_table_control_char or ttt.is_newline_before): 
                                    break
                                it1.end_token = ttt
                                ttt = ttt.next0_
                        ind_item = FragToken._new1340(tt, it1.end_token, InstrumentKind.INDEXITEM)
                        ind.children.append(ind_item)
                        nam = None
                        if (it1.num_end_token is not None and it1.num_end_token != it1.end_token): 
                            if (it1.begin_token != it1.num_begin_token): 
                                ind_item.children.append(FragToken._new1359(it1.begin_token, it1.num_begin_token.previous, InstrumentKind.KEYWORD, True))
                            NumberingHelper.create_number(ind_item, it1)
                            nam = FragToken._new1359(it1.num_end_token.next0_, it1.end_token, InstrumentKind.NAME, True)
                            ind_item.children.append(nam)
                            it2 = InstrToken1.parse(it1.end_token.next0_, True, None, 0, None, False, 0, False, True)
                            if ((it2 is not None and (isinstance(it1.end_token.next0_, TextToken)) and len(it2.numbers) == 0) and it2.title_typ == InstrToken1.StdTitleType.UNDEFINED and not it1.end_token.next0_.is_table_control_char): 
                                it3 = InstrToken1.parse(it2.end_token.next0_, True, None, 0, None, False, 0, False, True)
                                if (it3 is not None and len(it3.numbers) > 0): 
                                    nam.end_token = it2.end_token
                                    nam._def_val2 = True
                                    ind_item.end_token = it1.end_token = it2.end_token
                        else: 
                            nam = FragToken._new1359(it1.begin_token, it1.end_token, InstrumentKind.NAME, True)
                            ind_item.children.append(nam)
                        ind_item.name = FragToken._get_restored_namemt(nam, True)
                        val = Utils.asObjectOrNull(nam.value, str)
                        if (val is not None): 
                            while len(val) > 4:
                                ch = val[len(val) - 1]
                                if ((ch == '.' or ch == '-' or str.isdigit(ch)) or Utils.isWhitespace(ch) or ch == (chr(7))): 
                                    val = val[0:0+len(val) - 1]
                                else: 
                                    break
                            nam.value = (val)
                        tt = it1.end_token
                    continue
                if (last is not None and last.kind == InstrumentKind.CONTENT): 
                    last.end_token = li.end_token
                else: 
                    last = FragToken._new1350(li.begin_token, li.end_token, InstrumentKind.CONTENT, li)
                    root.children.append(last)
            if (not is_preamble): 
                if ((len(root.children) == 1 and root.children[0].kind == InstrumentKind.CONTENT and root.kind == InstrumentKind.CONTENT) and ((root.children[0]._itok is None or not root.children[0]._itok.has_changes))): 
                    if (root._itok is None): 
                        root._itok = root.children[0]._itok
                    root.children.clear()
                elif (len(root.children) == 1 and root.children[0].kind == InstrumentKind.COMMENT and root.kind == InstrumentKind.CONTENT): 
                    root.children.clear()
                    root.kind = InstrumentKind.COMMENT
            root.children.extend(notices)
            return
        if (is_subitem): 
            pass
        n = 0
        fr = None
        blk = list()
        i = 0
        while i < len(lines_): 
            if (lines_[i] == nums[0]): 
                break
            else: 
                blk.append(lines_[i])
            i += 1
        if (len(blk) > 0): 
            self.__analize_content_without_containers(root, blk, False, True, is_kodex)
        while i < len(lines_): 
            li = lines_[i]
            blk.clear()
            n += 1
            j = (i + 1)
            while j < len(lines_): 
                if ((n < len(nums)) and lines_[j] == nums[n]): 
                    break
                elif (n >= len(nums) and lines_[j].title_typ != InstrToken1.StdTitleType.UNDEFINED and lines_[j].all_upper): 
                    break
                else: 
                    blk.append(lines_[j])
                j += 1
            fr = FragToken._new1349(li.begin_token, li.end_token, li)
            root.children.append(fr)
            fr.kind = (InstrumentKind.SUBITEM if is_subitem else InstrumentKind.ITEM)
            NumberingHelper.create_number(fr, li)
            if (li.num_end_token != li.end_token and li.num_end_token is not None): 
                fr.children.append(FragToken._new1350(li.num_end_token.next0_, li.end_token, InstrumentKind.CONTENT, li))
            elif (li.title_typ != InstrToken1.StdTitleType.UNDEFINED and li.all_upper): 
                fr.kind = InstrumentKind.TAIL
                fr.children.append(FragToken._new1362(li.begin_token, li.end_token, InstrumentKind.NAME, True))
            if (len(blk) > 0): 
                fr.end_token = blk[len(blk) - 1].end_token
                self.__analize_content_without_containers(fr, blk, True, False, is_kodex)
            i = (j - 1)
            i += 1
        NumberingHelper.correct_child_numbers(root, root.children)
        root.children.extend(notices)
    
    @staticmethod
    def __extract_directive_sequence(lines_ : typing.List['InstrToken1']) -> typing.List['InstrToken1']:
        from pullenti.ner.instrument.internal.InstrToken1 import InstrToken1
        res = list()
        i = 0
        while i < len(lines_): 
            if (lines_[i].typ == InstrToken1.Types.DIRECTIVE): 
                j = (i - 1)
                first_pass3683 = True
                while True:
                    if first_pass3683: first_pass3683 = False
                    else: j -= 1
                    if (not (j >= 0)): break
                    li = lines_[j]
                    if (li.typ == InstrToken1.Types.FIRSTLINE): 
                        j -= 1
                        break
                    if (li.begin_token.is_value("РУКОВОДСТВУЯСЬ", None) or li.begin_token.is_value("ИССЛЕДОВАВ", None)): 
                        j -= 1
                        break
                    if (li.begin_token.is_value("НА", None) and li.begin_token.next0_ is not None and li.begin_token.next0_.is_value("ОСНОВАНИЕ", None)): 
                        j -= 1
                        break
                    if (len(li.numbers) > 0): 
                        break
                    if (li.typ == InstrToken1.Types.COMMENT): 
                        continue
                    if (li.typ == InstrToken1.Types.LINE): 
                        continue
                    break
                res.append(lines_[j + 1])
            i += 1
        if (len(res) == 0): 
            return None
        if (res[0] != lines_[0]): 
            res.insert(0, lines_[0])
        return res
    
    def __analize_content_with_directives(self, root : 'FragToken', lines_ : typing.List['InstrToken1'], is_jus : bool) -> None:
        """ Анализ текстов, содержащих директивы
        
        Args:
            lines_(typing.List[InstrToken1]): 
            proc: 
        """
        from pullenti.ner.instrument.internal.FragToken import FragToken
        dir_seq = ContentAnalyzeWhapper.__extract_directive_sequence(lines_)
        if (dir_seq is None): 
            self.__analize_content_without_containers(root, lines_, False, False, False)
            return
        if (len(dir_seq) > 1): 
            pass
        parts = list()
        n = 0
        i = 0
        while i < len(lines_): 
            if (lines_[i] == dir_seq[n]): 
                blk = list()
                j = i
                while j < len(lines_): 
                    if (((n + 1) < len(dir_seq)) and dir_seq[n + 1] == lines_[j]): 
                        break
                    else: 
                        blk.append(lines_[j])
                    j += 1
                fr = self.__create_directive_part(blk)
                if (fr is not None): 
                    parts.append(fr)
                i = (j - 1)
                n += 1
            i += 1
        if (len(parts) == 0): 
            return
        if (len(parts) == 1 and len(parts[0].children) > 0): 
            root.children.extend(parts[0].children)
            return
        if (len(parts) > 2 or ((len(parts) > 1 and is_jus))): 
            if (parts[0].name is None and parts[len(parts) - 1].name is not None): 
                if (parts[1].name == "МОТИВИРОВОЧНАЯ" and not parts[0].is_newline_after): 
                    parts[0].children.extend(parts[1].children)
                    parts[0].name = parts[1].name
                    del parts[1]
                    if (len(parts[0].children) > 1 and parts[0].children[0].kind == InstrumentKind.CONTENT and parts[0].children[1].kind == InstrumentKind.PREAMBLE): 
                        parts[0].children[1].begin_token = parts[0].children[0].begin_token
                        del parts[0].children[0]
                else: 
                    parts[0].name = "ВВОДНАЯ"
                    parts[0].kind = InstrumentKind.DOCPART
                    if (len(parts[0].children) == 0): 
                        parts[0].children.append(FragToken._new1350(parts[0].begin_token, parts[0].end_token, InstrumentKind.CONTENT, parts[0]._itok))
            i = 0
            while i < (len(parts) - 1): 
                if (parts[i].name == "МОТИВИРОВОЧНАЯ" and parts[i + 1].name is None): 
                    parts[i].children.extend(parts[i + 1].children)
                    del parts[i + 1]
                    i -= 1
                i += 1
            has_null = False
            for p in parts: 
                if (p.name is None): 
                    has_null = True
            if (not has_null): 
                root.children.extend(parts)
                return
        for p in parts: 
            if (len(p.children) > 0): 
                root.children.extend(p.children)
            else: 
                root.children.append(p)
    
    def __create_directive_part(self, lines_ : typing.List['InstrToken1']) -> 'FragToken':
        from pullenti.ner.instrument.internal.FragToken import FragToken
        from pullenti.ner.instrument.internal.InstrToken1 import InstrToken1
        res = FragToken._new1340(lines_[0].begin_token, lines_[len(lines_) - 1].end_token, InstrumentKind.DOCPART)
        head = list()
        i = 0
        while i < len(lines_): 
            if (lines_[i].typ == InstrToken1.Types.DIRECTIVE): 
                break
            else: 
                head.append(lines_[i])
            i += 1
        if (i >= len(lines_)): 
            self.__analize_content_without_containers(res, lines_, False, False, False)
            return res
        if (len(head) > 0): 
            fr_head = FragToken._new1340(head[0].begin_token, head[len(head) - 1].end_token, InstrumentKind.CONTENT)
            self.__analize_content_without_containers(fr_head, head, False, False, False)
            res.children.append(fr_head)
        if (len(res.children) == 1 and res.children[0].kind == InstrumentKind.CONTENT): 
            res.children[0].kind = InstrumentKind.PREAMBLE
        res.children.append(FragToken._new1374(lines_[i].begin_token, lines_[i].end_token, InstrumentKind.DIRECTIVE, lines_[i].value, lines_[i]))
        vvv = lines_[i].value
        if (vvv == "УСТАНОВЛЕНИЕ" or vvv == "ВСТАНОВЛЕННЯ"): 
            res.name = "МОТИВИРОВОЧНАЯ"
        elif (((((vvv == "ПОСТАНОВЛЕНИЕ" or vvv == "ОПРЕДЕЛЕНИЕ" or vvv == "ПРИГОВОР") or vvv == "ПРИКАЗ" or vvv == "РЕШЕНИЕ") or vvv == "ПОСТАНОВА" or vvv == "ВИЗНАЧЕННЯ") or vvv == "ВИРОК" or vvv == "НАКАЗ") or vvv == "РІШЕННЯ"): 
            res.name = "РЕЗОЛЮТИВНАЯ"
        del lines_[0:0+i + 1]
        if (len(lines_) > 0): 
            self.__analize_content_without_containers(res, lines_, False, False, False)
        return res
    
    def __analize_sections(self, root : 'FragToken') -> None:
        from pullenti.ner.instrument.internal.FragToken import FragToken
        from pullenti.ner.instrument.internal.InstrToken1 import InstrToken1
        for k in range(2):
            secs = list()
            items = list()
            for ch in root.children: 
                if (ch.kind == InstrumentKind.CHAPTER or ch.kind == InstrumentKind.CLAUSE): 
                    if (ch.number == 0 or (len(ch.children) < 2)): 
                        return
                    new_childs = list()
                    i = 0
                    while i < len(ch.children): 
                        if (ch.children[i].kind != InstrumentKind.NUMBER and ch.children[i].kind != InstrumentKind.NAME and ch.children[i].kind != InstrumentKind.KEYWORD): 
                            break
                        else: 
                            new_childs.append(ch.children[i])
                        i += 1
                    if (i >= len(ch.children)): 
                        return
                    sect = None
                    if (ch.children[i].kind != InstrumentKind.CONTENT): 
                        if (ch.children[i].kind != InstrumentKind.ITEM): 
                            return
                    else: 
                        sect = FragToken._new1359(ch.children[i].begin_token, ch.children[i].end_token, InstrumentKind.SECTION, True)
                        sect.name = (Utils.asObjectOrNull(sect.value, str))
                        sect.value = None
                        sect.children.append(FragToken._new1340(sect.begin_token, sect.end_token, InstrumentKind.NAME))
                        new_childs.append(sect)
                        if ((ch.children[i].whitespaces_before_count < 15) or (ch.children[i].whitespaces_after_count < 15)): 
                            return
                        i += 1
                        if (((i + 1) < len(ch.children)) and ch.children[i].kind == InstrumentKind.COMMENT): 
                            i += 1
                    its = 0
                    j = i
                    first_pass3684 = True
                    while True:
                        if first_pass3684: first_pass3684 = False
                        else: j += 1
                        if (not (j < len(ch.children))): break
                        if (ch.children[j].kind != InstrumentKind.ITEM): 
                            return
                        its += 1
                        if (sect is not None): 
                            sect.children.append(ch.children[j])
                            sect.end_token = ch.children[j].end_token
                        else: 
                            new_childs.append(ch.children[j])
                        if ((ch.children[j].whitespaces_after_count < 15) or j == (len(ch.children) - 1)): 
                            continue
                        la = ContentAnalyzeWhapper.__get_last_child(ch.children[j])
                        if (la.whitespaces_after_count < 15): 
                            continue
                        next_sect = None
                        tt = la.end_token
                        first_pass3685 = True
                        while True:
                            if first_pass3685: first_pass3685 = False
                            else: tt = tt.previous
                            if (not (tt is not None and tt.begin_char > la.begin_char)): break
                            if (tt.is_newline_before): 
                                if (tt.chars.is_cyrillic_letter and tt.chars.is_all_lower): 
                                    continue
                                it = InstrToken1.parse(tt, True, None, 0, None, False, 0, False, False)
                                if (it is not None and len(it.numbers) > 0): 
                                    break
                                if (tt.whitespaces_before_count < 15): 
                                    continue
                                if ((tt.previous.end_char - la.begin_char) < 20): 
                                    break
                                next_sect = FragToken._new1359(tt, la.end_token, InstrumentKind.SECTION, True)
                                next_sect.name = (Utils.asObjectOrNull(next_sect.value, str))
                                next_sect.value = None
                                next_sect.children.append(FragToken._new1340(tt, la.end_token, InstrumentKind.NAME))
                                break
                        if (next_sect is None): 
                            continue
                        if (sect is None): 
                            return
                        if (k > 0): 
                            sect.end_token = la.end_token = next_sect.begin_token.previous
                            if (ch.children[j].end_char > la.end_char): 
                                ch.children[j].end_token = la.end_token
                        new_childs.append(next_sect)
                        sect = next_sect
                    if (k > 0): 
                        ch.children = new_childs
                    else: 
                        items.append(its)
                        secs.append(len(new_childs))
            if (k > 0): 
                break
            if (len(secs) < 3): 
                break
            allsecs = 0
            allits = 0
            okchapts = 0
            i = 0
            while i < len(items): 
                allits += items[i]
                allsecs += secs[i]
                if (secs[i] > 1): 
                    okchapts += 1
                i += 1
            rr = (allits) / (allsecs)
            if (rr < 1.5): 
                break
            if (okchapts < (math.floor(len(items) / 2))): 
                break
    
    @staticmethod
    def __get_last_child(fr : 'FragToken') -> 'FragToken':
        if (len(fr.children) == 0): 
            return fr
        return ContentAnalyzeWhapper.__get_last_child(fr.children[len(fr.children) - 1])
    
    def __correct_names(self, root : 'FragToken', parent : 'FragToken') -> None:
        from pullenti.ner.instrument.internal.InstrToken1 import InstrToken1
        fr_nams = None
        i = 0
        first_pass3686 = True
        while True:
            if first_pass3686: first_pass3686 = False
            else: i += 1
            if (not (i < len(root.children))): break
            ch = root.children[i]
            if (ch.kind != InstrumentKind.CLAUSE and ch.kind != InstrumentKind.CHAPTER): 
                continue
            if (ch.name is not None): 
                fr_nams = (None)
                break
            nam_has = False
            j = 0
            first_pass3687 = True
            while True:
                if first_pass3687: first_pass3687 = False
                else: j += 1
                if (not (j < len(ch.children))): break
                chh = ch.children[j]
                if (chh.kind == InstrumentKind.KEYWORD or chh.kind == InstrumentKind.NUMBER or chh.kind == InstrumentKind.EDITIONS): 
                    continue
                if (chh.kind == InstrumentKind.CONTENT or chh.kind == InstrumentKind.INDENTION or ((chh.kind == InstrumentKind.CLAUSEPART and len(chh.children) == 1))): 
                    if (chh._itok is None): 
                        chh._itok = InstrToken1.parse(chh.begin_token, True, None, 0, None, False, 0, False, False)
                    if (chh._itok is not None and not chh._itok.has_verb): 
                        nam_has = True
                break
            if (not nam_has): 
                fr_nams = (None)
                break
            if (fr_nams is None): 
                fr_nams = list()
                fr_nams.append(ch)
            else: 
                if (fr_nams[len(fr_nams) - 1].kind != ch.kind): 
                    fr_nams = (None)
                    break
                fr_nams.append(ch)
        if (fr_nams is not None): 
            for ch in fr_nams: 
                j = 0
                first_pass3688 = True
                while True:
                    if first_pass3688: first_pass3688 = False
                    else: j += 1
                    if (not (j < len(ch.children))): break
                    chh = ch.children[j]
                    if (chh.kind == InstrumentKind.KEYWORD or chh.kind == InstrumentKind.NUMBER or chh.kind == InstrumentKind.EDITIONS): 
                        continue
                    if (chh.kind == InstrumentKind.CONTENT or chh.kind == InstrumentKind.INDENTION or ((chh.kind == InstrumentKind.CLAUSEPART and len(chh.children) == 1))): 
                        break
                if (j >= len(ch.children)): 
                    continue
                nam = ch.children[j]
                if (nam.kind == InstrumentKind.INDENTION or ((nam.kind == InstrumentKind.CLAUSEPART and len(nam.children) == 1))): 
                    nam.number = 0
                    cou = 0
                    jj = j + 1
                    while jj < len(ch.children): 
                        if (ch.children[jj].kind == nam.kind): 
                            ch.children[jj].number -= 1
                            cou += 1
                        else: 
                            break
                        jj += 1
                    if (cou == 1): 
                        jj = j + 1
                        while jj < len(ch.children): 
                            if (ch.children[jj].kind == nam.kind): 
                                empty = True
                                k = jj + 1
                                while k < len(ch.children): 
                                    if (ch.children[k].kind != InstrumentKind.EDITIONS and ch.children[k].kind != InstrumentKind.COMMENT): 
                                        empty = False
                                        break
                                    k += 1
                                if (empty): 
                                    if (ch.children[jj].kind == InstrumentKind.INDENTION or len(ch.children) == 0): 
                                        ch.children[jj].kind = InstrumentKind.CONTENT
                                        ch.children[jj].number = 0
                                    else: 
                                        ch0 = ch.children[jj]
                                        del ch.children[jj]
                                        ch.children[jj:jj] = ch0.children
                                    break
                            jj += 1
                nam.number = 0
                nam.kind = InstrumentKind.NAME
                nam._def_val2 = True
                nam.children.clear()
                ch.name = (Utils.asObjectOrNull(nam.value, str))
        tt = root.begin_token
        if (root._itok is not None and root._itok.num_end_token is not None): 
            tt = root._itok.num_end_token.next0_
        if (tt is not None): 
            if (parent is not None and parent.is_expired): 
                pass
            else: 
                if (not tt.is_value("УТРАТИТЬ", "ВТРАТИТИ")): 
                    npt = NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.NO, 0, None)
                    if (npt is not None): 
                        tt = npt.end_token.next0_
                if ((tt is not None and tt.is_value("УТРАТИТЬ", "ВТРАТИТИ") and tt.next0_ is not None) and tt.next0_.is_value("СИЛА", "ЧИННІСТЬ")): 
                    root.is_expired = True
        for ch in root.children: 
            self.__correct_names(ch, root)
    
    def __correct_kodex_parts(self, root : 'FragToken') -> None:
        from pullenti.ner.instrument.internal.NumberingHelper import NumberingHelper
        if (root.number == 2 and root.kind == InstrumentKind.CLAUSE): 
            pass
        if (root.number == 11 and root.kind == InstrumentKind.ITEM): 
            pass
        i = 0
        while i < len(root.children): 
            ki = root.children[i].kind
            if ((ki != InstrumentKind.KEYWORD and ki != InstrumentKind.NAME and ki != InstrumentKind.NUMBER) and ki != InstrumentKind.COMMENT and ki != InstrumentKind.EDITIONS): 
                break
            i += 1
        if (i >= len(root.children)): 
            return
        i0 = i
        if (root.kind == InstrumentKind.CLAUSE and self.doc_typ != DecreeKind.CONTRACT): 
            while i < len(root.children): 
                ch = root.children[i]
                if (ch.kind == InstrumentKind.ITEM or ch.kind == InstrumentKind.SUBITEM or ((ch.kind == InstrumentKind.CLAUSEPART and ch.number > 0))): 
                    ch.kind = InstrumentKind.CLAUSEPART
                    for chh in ch.children: 
                        if (chh.kind == InstrumentKind.SUBITEM and chh.number > 0): 
                            chh.kind = InstrumentKind.ITEM
                            for chhh in chh.children: 
                                if (chhh.number > 0): 
                                    chhh.kind = InstrumentKind.SUBITEM
                elif (ch.kind == InstrumentKind.CONTENT): 
                    break
                i += 1
        if (i == i0 and root.children[i0].kind == InstrumentKind.CONTENT): 
            i = (i0 + 1)
            while i < len(root.children): 
                if (root.children[i].kind != InstrumentKind.EDITIONS and root.children[i].kind != InstrumentKind.COMMENT): 
                    break
                i += 1
            if ((i < len(root.children)) and ((((self.doc_typ == DecreeKind.KODEX or root.kind == InstrumentKind.CLAUSE or root.kind == InstrumentKind.ITEM) or root.kind == InstrumentKind.SUBITEM or root.kind == InstrumentKind.CHAPTER) or root.kind == InstrumentKind.CLAUSEPART))): 
                if (root.children[i].kind == InstrumentKind.LISTITEM or root.children[i].kind == InstrumentKind.ITEM or root.children[i].kind == InstrumentKind.SUBITEM): 
                    num = 1
                    root.children[i0].kind = InstrumentKind.INDENTION
                    root.children[i0].number = num
                    if (root.children[i].kind == InstrumentKind.LISTITEM): 
                        while i < len(root.children): 
                            if (root.children[i].kind == InstrumentKind.LISTITEM): 
                                root.children[i].kind = InstrumentKind.INDENTION
                                num += 1
                                root.children[i].number = num
                            elif (root.children[i].kind != InstrumentKind.COMMENT and root.children[i].kind != InstrumentKind.EDITIONS): 
                                break
                            i += 1
        inds = 0
        i = i0
        first_pass3689 = True
        while True:
            if first_pass3689: first_pass3689 = False
            else: i += 1
            if (not (i < len(root.children))): break
            if (root.children[i].kind == InstrumentKind.COMMENT): 
                continue
            lii = ContentAnalyzeWhapper.__split_content_by_indents(root.children[i], inds + 1)
            if (lii is None): 
                break
            inds += len(lii)
        if (inds > 1 and ((i >= len(root.children) or root.children[i].kind != InstrumentKind.DIRECTIVE))): 
            if (root.number == 7 and root.kind == InstrumentKind.CLAUSEPART): 
                pass
            num = 1
            i = i0
            first_pass3690 = True
            while True:
                if first_pass3690: first_pass3690 = False
                else: i += 1
                if (not (i < len(root.children))): break
                if (root.children[i].kind == InstrumentKind.COMMENT): 
                    continue
                lii = ContentAnalyzeWhapper.__split_content_by_indents(root.children[i], num)
                if (lii is None): 
                    break
                if (len(lii) == 0): 
                    continue
                num += len(lii)
                del root.children[i]
                root.children[i:i] = lii
                i += (len(lii) - 1)
            num = 1
            i = (i0 + 1)
            first_pass3691 = True
            while True:
                if first_pass3691: first_pass3691 = False
                else: i += 1
                if (not (i < len(root.children))): break
                ch = root.children[i]
                if (ch.kind == InstrumentKind.COMMENT or ch.kind == InstrumentKind.EDITIONS): 
                    continue
                if (ch._itok is None or len(ch._itok.numbers) != 1): 
                    break
                if (ch._itok.first_number != num): 
                    break
                num += 1
            if (num > 1 and i >= len(root.children)): 
                i = (i0 + 1)
                first_pass3692 = True
                while True:
                    if first_pass3692: first_pass3692 = False
                    else: i += 1
                    if (not (i < len(root.children))): break
                    ch = root.children[i]
                    if (ch.kind == InstrumentKind.COMMENT or ch.kind == InstrumentKind.EDITIONS): 
                        continue
                    if (root.kind == InstrumentKind.CLAUSEPART or root.kind == InstrumentKind.CLAUSE): 
                        ch.kind = InstrumentKind.ITEM
                    elif (root.kind == InstrumentKind.ITEM): 
                        ch.kind = InstrumentKind.SUBITEM
                    else: 
                        break
                    NumberingHelper.create_number(ch, ch._itok)
                    if (len(ch.children) == 1 and (ch.children[0].end_char < ch.end_char)): 
                        ch.fill_by_content_children()
        for ch in root.children: 
            self.__correct_kodex_parts(ch)
    
    @staticmethod
    def __split_content_by_indents(fr : 'FragToken', num : int) -> typing.List['FragToken']:
        from pullenti.ner.instrument.internal.FragToken import FragToken
        from pullenti.ner.instrument.internal.InstrToken1 import InstrToken1
        if (fr.kind != InstrumentKind.CONTENT and fr.kind != InstrumentKind.LISTITEM and fr.kind != InstrumentKind.PREAMBLE): 
            if (fr.kind != InstrumentKind.EDITIONS): 
                return None
            if (fr.begin_token.is_value("АБЗАЦ", None)): 
                t = fr.begin_token.next0_
                if (not (isinstance(t, NumberToken)) or t.value != str(num)): 
                    return None
                next0_ = num
                t = t.next0_
                if ((t is not None and t.is_hiphen and (isinstance(t.next0_, NumberToken))) and t.next0_.int_value is not None): 
                    next0_ = t.next0_.int_value
                    t = t.next0_.next0_
                    if (next0_ <= num): 
                        return None
                if ((t is None or not t.is_value("УТРАТИТЬ", "ВТРАТИТИ") or t.next0_ is None) or not t.next0_.is_value("СИЛА", "ЧИННІСТЬ")): 
                    return None
                res0 = list()
                i = num
                while i <= next0_: 
                    res0.append(FragToken._new1379(fr.begin_token, fr.end_token, InstrumentKind.INDENTION, i, True, fr.referents))
                    i += 1
                return res0
            return list()
        if (len(fr.children) > 0): 
            return None
        if (fr._itok is None): 
            fr._itok = InstrToken1.parse(fr.begin_token, True, None, 0, None, False, 0, False, False)
        res = list()
        t0 = fr.begin_token
        tt = t0
        first_pass3693 = True
        while True:
            if first_pass3693: first_pass3693 = False
            else: tt = tt.next0_
            if (not (tt is not None and tt.end_char <= fr.end_char)): break
            if (tt.end_char == fr.end_char): 
                pass
            elif (not tt.is_newline_after): 
                continue
            elif (tt.is_table_control_char): 
                continue
            elif (not MiscHelper.can_be_start_of_sentence(tt.next0_) and not tt.is_char_of(":")): 
                continue
            re = FragToken._new1357(t0, tt, InstrumentKind.INDENTION, num)
            num += 1
            if (t0 == fr.begin_token and tt == fr.end_token): 
                re._itok = fr._itok
            if (re._itok is None): 
                re._itok = InstrToken1.parse(t0, True, None, 0, None, False, 0, False, False)
            if (len(res) > 100): 
                return None
            res.append(re)
            t0 = tt.next0_
        return res
    
    def __analize_preamble(self, root : 'FragToken') -> None:
        from pullenti.ner.instrument.internal.FragToken import FragToken
        from pullenti.ner.instrument.internal.InstrToken1 import InstrToken1
        cnt_cou = 0
        ch = None
        ok = False
        if ((len(root.children) > 1 and root.children[0].kind == InstrumentKind.CONTENT and root.children[1].number > 0) and len(root.children[0].children) > 0): 
            i = 0
            while i < len(root.children[0].children): 
                ch2 = root.children[0].children[i]
                if ((ch2.kind != InstrumentKind.CONTENT and ch2.kind != InstrumentKind.INDENTION and ch2.kind != InstrumentKind.COMMENT) and ch2.kind != InstrumentKind.EDITIONS): 
                    break
                i += 1
            if (i >= len(root.children[0].children)): 
                chh = root.children[0]
                del root.children[0]
                root.children[0:0] = chh.children
        i = 0
        first_pass3694 = True
        while True:
            if first_pass3694: first_pass3694 = False
            else: i += 1
            if (not (i < len(root.children))): break
            ch = root.children[i]
            if (ch.kind == InstrumentKind.EDITIONS or ch.kind == InstrumentKind.COMMENT or ch.kind == InstrumentKind.INDEX): 
                continue
            if (ch.kind == InstrumentKind.DIRECTIVE): 
                ok = True
                break
            if (ch._itok is not None and ch._itok.has_changes): 
                break
            if (ch.kind == InstrumentKind.CONTENT and len(ch.children) == 1 and ch.children[0].kind == InstrumentKind.INDEX): 
                ch.kind = InstrumentKind.INDEX
                ch.children = ch.children[0].children
                continue
            if (ch.kind == InstrumentKind.CONTENT or ch.kind == InstrumentKind.INDENTION): 
                t = ch.begin_token.next0_
                while t is not None and (t.end_char < ch.end_char): 
                    if (t.is_newline_before): 
                        if (t.previous.is_char_of(".:;") and t.previous.previous is not None and ((t.previous.previous.is_value("НИЖЕСЛЕДУЮЩИЙ", None) or t.previous.previous.is_value("ДОГОВОР", None)))): 
                            itt1 = InstrToken1.parse(t, True, None, 0, None, False, 0, False, False)
                            if (itt1 is not None and not itt1.has_verb and (itt1.end_char < ch.end_char)): 
                                clau = FragToken._new1340(t, ch.end_token, InstrumentKind.CHAPTER)
                                if (((i + 1) < len(root.children)) and root.children[i + 1].kind == InstrumentKind.CLAUSE): 
                                    clau.kind = InstrumentKind.CLAUSE
                                nam = FragToken._new1342(t, itt1.end_token, InstrumentKind.NAME, True, itt1)
                                clau.children.append(nam)
                                clau.name = FragToken._get_restored_namemt(nam, False)
                                clau.children.append(FragToken._new1340(itt1.end_token.next0_, ch.end_token, InstrumentKind.CONTENT))
                                ch.end_token = t.previous
                                root.children.insert(i + 1, clau)
                            break
                    t = t.next0_
                pream = False
                if (ch.begin_token.is_value("ПРЕАМБУЛА", None)): 
                    pream = True
                elif (ch.length_char > 1500): 
                    break
                cnt_cou += 1
                if (ch.end_token.is_char(':') or pream or ((ch.end_token.previous is not None and ch.end_token.previous.is_value("НИЖЕСЛЕДУЮЩИЙ", None)))): 
                    ok = True
                    i += 1
                    break
                continue
            break
        if (cnt_cou == 0 or cnt_cou > 3 or i >= len(root.children)): 
            return
        if (ch.number > 0): 
            ok = True
        if (not ok): 
            return
        if (cnt_cou == 1): 
            j = 0
            while j < i: 
                if (root.children[j].kind == InstrumentKind.CONTENT or root.children[j].kind == InstrumentKind.INDENTION): 
                    root.children[j].kind = InstrumentKind.PREAMBLE
                    if (len(root.children[j].children) == 1 and root.children[j].children[0].kind == InstrumentKind.INDEX): 
                        root.children[j].kind = InstrumentKind.INDEX
                        root.children[j].children = root.children[j].children[0].children
                j += 1
        else: 
            prm = FragToken._new1340(root.children[0].begin_token, root.children[i - 1].end_token, InstrumentKind.PREAMBLE)
            j = 0
            while j < i: 
                prm.children.append(root.children[j])
                j += 1
            del root.children[0:0+i]
            root.children.insert(0, prm)