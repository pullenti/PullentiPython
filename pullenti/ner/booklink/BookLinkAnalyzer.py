# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing
import math
from enum import IntEnum
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.person.internal.FioTemplateType import FioTemplateType
from pullenti.ner.booklink.internal.BookLinkTyp import BookLinkTyp
from pullenti.ner.booklink.BookLinkRefType import BookLinkRefType
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.uri.UriReferent import UriReferent
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.titlepage.internal.TitleItemToken import TitleItemToken
from pullenti.ner.person.internal.PersonItemToken import PersonItemToken
from pullenti.ner.booklink.internal.MetaBookLinkRef import MetaBookLinkRef
from pullenti.ner.booklink.internal.MetaBookLink import MetaBookLink
from pullenti.ner.Referent import Referent
from pullenti.ner.core.internal.PullentiNerCoreInternalResourceHelper import PullentiNerCoreInternalResourceHelper
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.date.DateReferent import DateReferent
from pullenti.ner.org.OrganizationReferent import OrganizationReferent
from pullenti.ner.person.PersonReferent import PersonReferent
from pullenti.ner.booklink.BookLinkReferent import BookLinkReferent
from pullenti.ner.Token import Token
from pullenti.ner.booklink.internal.BookLinkToken import BookLinkToken
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.booklink.BookLinkRefReferent import BookLinkRefReferent
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.Analyzer import Analyzer

class BookLinkAnalyzer(Analyzer):
    """ Анализатор ссылок на внешнюю литературу (библиография) """
    
    class RegionTyp(IntEnum):
        UNDEFINED = 0
        AUTHORS = 1
        NAME = 2
        FIRST = 3
        SECOND = 4
        
        @classmethod
        def has_value(cls, value):
            return any(value == item.value for item in cls)
    
    @property
    def name(self) -> str:
        return BookLinkAnalyzer.ANALYZER_NAME
    
    ANALYZER_NAME = "BOOKLINK"
    """ Имя анализатора ("BOOKLINK") """
    
    @property
    def caption(self) -> str:
        return "Ссылки на литературу"
    
    @property
    def description(self) -> str:
        return "Ссылки из списка литературы"
    
    @property
    def is_specific(self) -> bool:
        return False
    
    @property
    def progress_weight(self) -> int:
        return 1
    
    def clone(self) -> 'Analyzer':
        return BookLinkAnalyzer()
    
    @property
    def used_extern_object_types(self) -> typing.List[str]:
        return [DateReferent.OBJ_TYPENAME, GeoReferent.OBJ_TYPENAME, OrganizationReferent.OBJ_TYPENAME, PersonReferent.OBJ_TYPENAME]
    
    @property
    def type_system(self) -> typing.List['ReferentClass']:
        return [MetaBookLink._global_meta, MetaBookLinkRef._global_meta]
    
    @property
    def images(self) -> typing.List[tuple]:
        res = dict()
        res[MetaBookLink.IMAGE_ID] = PullentiNerCoreInternalResourceHelper.get_bytes("booklink.png")
        res[MetaBookLinkRef.IMAGE_ID] = PullentiNerCoreInternalResourceHelper.get_bytes("booklinkref.png")
        res[MetaBookLinkRef.IMAGE_ID_INLINE] = PullentiNerCoreInternalResourceHelper.get_bytes("booklinkrefinline.png")
        res[MetaBookLinkRef.IMAGE_ID_LAST] = PullentiNerCoreInternalResourceHelper.get_bytes("booklinkreflast.png")
        return res
    
    def create_referent(self, type0_ : str) -> 'Referent':
        if (type0_ == BookLinkReferent.OBJ_TYPENAME): 
            return BookLinkReferent()
        if (type0_ == BookLinkRefReferent.OBJ_TYPENAME): 
            return BookLinkRefReferent()
        return None
    
    def process(self, kit : 'AnalysisKit') -> None:
        ad = kit.get_analyzer_data(self)
        is_lit_block = 0
        refs_by_num = dict()
        rts = [ ]
        t = kit.first_token
        first_pass3515 = True
        while True:
            if first_pass3515: first_pass3515 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_char('(')): 
                br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                if (br is not None and br.length_char > 70 and (br.length_char < 400)): 
                    if (br.is_newline_after or ((br.end_token.next0_ is not None and br.end_token.next0_.is_char_of(".;")))): 
                        rts = BookLinkAnalyzer.__try_parse(t.next0_, False, br.end_char)
                        if (rts is not None and len(rts) >= 1): 
                            if (len(rts) > 1): 
                                rts[1].referent = ad.register_referent(rts[1].referent)
                                kit.embed_token(rts[1])
                                rts[0].referent.book = Utils.asObjectOrNull(rts[1].referent, BookLinkReferent)
                                if (rts[0].begin_char == rts[1].begin_char): 
                                    rts[0].begin_token = rts[1]
                                if (rts[0].end_char == rts[1].end_char): 
                                    rts[0].end_token = rts[1]
                            rts[0].begin_token = t
                            rts[0].end_token = br.end_token
                            rts[0].referent.typ = BookLinkRefType.INLINE
                            rts[0].referent = ad.register_referent(rts[0].referent)
                            kit.embed_token(rts[0])
                            t = (rts[0])
                            continue
            if (not t.is_newline_before): 
                continue
            if (is_lit_block <= 0): 
                tt = BookLinkToken.parse_start_of_lit_block(t)
                if (tt is not None): 
                    is_lit_block = 5
                    t = tt
                    continue
            rts = BookLinkAnalyzer.__try_parse(t, is_lit_block > 0, 0)
            if (rts is None or (len(rts) < 1)): 
                is_lit_block -= 1
                if (is_lit_block < 0): 
                    is_lit_block = 0
                continue
            is_lit_block += 1
            if (is_lit_block > 5): 
                is_lit_block = 5
            if (len(rts) > 1): 
                rts[1].referent = ad.register_referent(rts[1].referent)
                kit.embed_token(rts[1])
                rts[0].referent.book = Utils.asObjectOrNull(rts[1].referent, BookLinkReferent)
                if (rts[0].begin_char == rts[1].begin_char): 
                    rts[0].begin_token = rts[1]
                if (rts[0].end_char == rts[1].end_char): 
                    rts[0].end_token = rts[1]
            re = Utils.asObjectOrNull(rts[0].referent, BookLinkRefReferent)
            re = (Utils.asObjectOrNull(ad.register_referent(re), BookLinkRefReferent))
            rts[0].referent = (re)
            kit.embed_token(rts[0])
            t = (rts[0])
            if (re.number is not None): 
                li = [ ]
                wrapli368 = RefOutArgWrapper(None)
                inoutres369 = Utils.tryGetValue(refs_by_num, re.number, wrapli368)
                li = wrapli368.value
                if (not inoutres369): 
                    li = list()
                    refs_by_num[re.number] = li
                li.append(re)
        t = kit.first_token
        first_pass3516 = True
        while True:
            if first_pass3516: first_pass3516 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (not (isinstance(t, TextToken))): 
                continue
            rt = BookLinkAnalyzer.__try_parse_short_inline(t)
            if (rt is None): 
                continue
            re = Utils.asObjectOrNull(rt.referent, BookLinkRefReferent)
            li = [ ]
            wrapli370 = RefOutArgWrapper(None)
            inoutres371 = Utils.tryGetValue(refs_by_num, Utils.ifNotNull(re.number, ""), wrapli370)
            li = wrapli370.value
            if (not inoutres371): 
                continue
            i = 0
            while i < len(li): 
                if (t.begin_char < li[i].occurrence[0].begin_char): 
                    break
                i += 1
            if (i >= len(li)): 
                continue
            re.book = li[i].book
            if (re.pages is None): 
                re.pages = li[i].pages
            re.typ = BookLinkRefType.INLINE
            re = (Utils.asObjectOrNull(ad.register_referent(re), BookLinkRefReferent))
            rt.referent = (re)
            kit.embed_token(rt)
            t = (rt)
    
    @staticmethod
    def __try_parse_short_inline(t : 'Token') -> 'ReferentToken':
        if (t is None): 
            return None
        if (t.is_char('[') and not t.is_newline_before): 
            bb = BookLinkToken.try_parse(t, 0)
            if (bb is not None and bb.typ == BookLinkTyp.NUMBER): 
                re = BookLinkRefReferent()
                re.number = bb.value
                return ReferentToken(re, t, bb.end_token)
        if (t.is_char('(')): 
            bbb = BookLinkToken.try_parse(t.next0_, 0)
            if (bbb is None): 
                return None
            if (bbb.typ == BookLinkTyp.SEE): 
                tt = bbb.end_token.next0_
                first_pass3517 = True
                while True:
                    if first_pass3517: first_pass3517 = False
                    else: tt = tt.next0_
                    if (not (tt is not None)): break
                    if (tt.is_char_of(",:.")): 
                        continue
                    if (tt.is_char('[')): 
                        if (((isinstance(tt.next0_, NumberToken)) and tt.next0_.next0_ is not None and tt.next0_.next0_.is_char(']')) and tt.next0_.next0_ is not None and tt.next0_.next0_.next0_.is_char(')')): 
                            re = BookLinkRefReferent()
                            re.number = str(tt.next0_.value)
                            return ReferentToken(re, t, tt.next0_.next0_.next0_)
                    if ((isinstance(tt, NumberToken)) and tt.next0_ is not None and tt.next0_.is_char(')')): 
                        re = BookLinkRefReferent()
                        re.number = str(tt.value)
                        return ReferentToken(re, t, tt.next0_)
                    break
                return None
            if (bbb.typ == BookLinkTyp.NUMBER): 
                tt1 = bbb.end_token.next0_
                if (tt1 is not None and tt1.is_comma): 
                    tt1 = tt1.next0_
                bbb2 = BookLinkToken.try_parse(tt1, 0)
                if ((bbb2 is not None and bbb2.typ == BookLinkTyp.PAGERANGE and bbb2.end_token.next0_ is not None) and bbb2.end_token.next0_.is_char(')')): 
                    re = BookLinkRefReferent()
                    re.number = bbb.value
                    re.pages = bbb2.value
                    return ReferentToken(re, t, bbb2.end_token.next0_)
        return None
    
    @staticmethod
    def __try_parse(t : 'Token', is_in_lit : bool, max_char : int=0) -> typing.List['ReferentToken']:
        if (t is None): 
            return None
        is_bracket_regime = False
        if (t.previous is not None and t.previous.is_char('(')): 
            is_bracket_regime = True
        blt = BookLinkToken.try_parse(t, 0)
        if (blt is None): 
            blt = BookLinkToken.try_parse_author(t, FioTemplateType.UNDEFINED)
        if (blt is None and not is_bracket_regime): 
            return None
        t0 = t
        coef = 0
        is_electr_res = False
        decree = None
        regtyp = BookLinkAnalyzer.RegionTyp.UNDEFINED
        num = None
        spec_see = None
        book_prev = None
        if (is_bracket_regime): 
            regtyp = BookLinkAnalyzer.RegionTyp.AUTHORS
        elif (blt.typ == BookLinkTyp.PERSON): 
            if (not is_in_lit): 
                return None
            regtyp = BookLinkAnalyzer.RegionTyp.AUTHORS
        elif (blt.typ == BookLinkTyp.NUMBER): 
            num = blt.value
            t = blt.end_token.next0_
            if (t is None or t.is_newline_before): 
                return None
            if (not t.is_whitespace_before): 
                if (isinstance(t, NumberToken)): 
                    n = t.value
                    if ((((n == "3" or n == "0")) and not t.is_whitespace_after and (isinstance(t.next0_, TextToken))) and t.next0_.chars.is_all_lower): 
                        pass
                    else: 
                        return None
                elif (not (isinstance(t, TextToken)) or t.chars.is_all_lower): 
                    r = t.get_referent()
                    if (isinstance(r, PersonReferent)): 
                        pass
                    elif (is_in_lit and r is not None and r.type_name == "DECREE"): 
                        pass
                    else: 
                        return None
            first_pass3518 = True
            while True:
                if first_pass3518: first_pass3518 = False
                else: t = t.next0_
                if (not (t is not None)): break
                if (isinstance(t, NumberToken)): 
                    break
                if (not (isinstance(t, TextToken))): 
                    break
                if (BracketHelper.can_be_start_of_sequence(t, True, False)): 
                    break
                if (not t.chars.is_letter): 
                    continue
                bbb = BookLinkToken.try_parse(t, 0)
                if (bbb is not None): 
                    if (bbb.typ == BookLinkTyp.TAMZE): 
                        spec_see = bbb
                        t = bbb.end_token.next0_
                        break
                    if (bbb.typ == BookLinkTyp.SEE): 
                        t = bbb.end_token
                        continue
                break
            if (spec_see is not None and spec_see.typ == BookLinkTyp.TAMZE): 
                coef += 1
                max0_ = 1000
                tt = t0
                while tt is not None and max0_ > 0: 
                    if (isinstance(tt.get_referent(), BookLinkRefReferent)): 
                        book_prev = tt.get_referent().book
                        break
                    tt = tt.previous; max0_ -= 1
            blt1 = BookLinkToken.try_parse_author(t, FioTemplateType.UNDEFINED)
            if (blt1 is not None and blt1.typ == BookLinkTyp.PERSON): 
                regtyp = BookLinkAnalyzer.RegionTyp.AUTHORS
            else: 
                ok = False
                tt = t
                first_pass3519 = True
                while True:
                    if first_pass3519: first_pass3519 = False
                    else: tt = (None if tt is None else tt.next0_)
                    if (not (tt is not None)): break
                    if (tt.is_newline_before): 
                        break
                    if (is_in_lit and tt.get_referent() is not None and tt.get_referent().type_name == "DECREE"): 
                        ok = True
                        decree = tt
                        break
                    bbb = BookLinkToken.try_parse(tt, 0)
                    if (bbb is None): 
                        continue
                    if (bbb.typ == BookLinkTyp.ELECTRONRES): 
                        is_electr_res = True
                        ok = True
                        break
                    if (bbb.typ == BookLinkTyp.DELIMETER): 
                        tt = bbb.end_token.next0_
                        if (BookLinkToken.try_parse_author(tt, FioTemplateType.UNDEFINED) is not None): 
                            ok = True
                            break
                        bbb = BookLinkToken.try_parse(tt, 0)
                        if (bbb is not None): 
                            if (bbb.typ == BookLinkTyp.EDITORS or bbb.typ == BookLinkTyp.TRANSLATE or bbb.typ == BookLinkTyp.SOSTAVITEL): 
                                ok = True
                                break
                if (not ok and not is_in_lit): 
                    if (BookLinkToken.check_link_before(t0, num)): 
                        pass
                    else: 
                        return None
                regtyp = BookLinkAnalyzer.RegionTyp.NAME
        else: 
            return None
        res = BookLinkReferent()
        corr_authors = list()
        t00 = t
        blt00 = None
        start_of_name = None
        prev_pers_templ = FioTemplateType.UNDEFINED
        if (regtyp == BookLinkAnalyzer.RegionTyp.AUTHORS): 
            first_pass3520 = True
            while True:
                if first_pass3520: first_pass3520 = False
                else: t = t.next0_
                if (not (t is not None)): break
                if (max_char > 0 and t.begin_char >= max_char): 
                    break
                if (t.is_char_of(".;") or t.is_comma_and): 
                    continue
                if (t.is_char('/')): 
                    break
                if ((t.is_char('(') and t.next0_ is not None and t.next0_.is_value("EDS", None)) and t.next0_.next0_ is not None and t.next0_.next0_.is_char(')')): 
                    t = t.next0_.next0_.next0_
                    break
                blt = BookLinkToken.try_parse_author(t, prev_pers_templ)
                if (blt is None and t.previous is not None and t.previous.is_and): 
                    blt = BookLinkToken.try_parse_author(t.previous, FioTemplateType.UNDEFINED)
                if (blt is None): 
                    if ((isinstance(t.get_referent(), OrganizationReferent)) and blt00 is not None): 
                        bbb2 = BookLinkToken.try_parse(t.next0_, 0)
                        if (bbb2 is not None): 
                            if (bbb2.typ == BookLinkTyp.YEAR): 
                                res.add_slot(BookLinkReferent.ATTR_AUTHOR, t.get_referent(), False, 0)
                                res.year = int(bbb2.value)
                                coef += 0.5
                                t = bbb2.end_token.next0_
                    break
                if (blt.typ == BookLinkTyp.PERSON): 
                    tt2 = blt.end_token.next0_
                    bbb2 = BookLinkToken.try_parse(tt2, 0)
                    if (bbb2 is not None): 
                        if (bbb2.typ == BookLinkTyp.YEAR): 
                            res.year = int(bbb2.value)
                            coef += 0.5
                            blt.end_token = bbb2.end_token
                            blt00 = (None)
                    if (blt00 is not None and ((blt00.end_token.next0_ == blt.begin_token or blt.begin_token.previous.is_char('.')))): 
                        tt11 = blt.end_token.next0_
                        nex = BookLinkToken.try_parse(tt11, 0)
                        if (nex is not None and nex.typ == BookLinkTyp.ANDOTHERS): 
                            pass
                        else: 
                            if (tt11 is None): 
                                break
                            if (tt11.is_char('/') and tt11.next0_ is not None and tt11.next0_.is_char('/')): 
                                break
                            if (tt11.is_char(':')): 
                                break
                            if ((str(blt).find('.') < 0) and str(blt00).find('.') > 0): 
                                break
                            if ((isinstance(tt11, TextToken)) and tt11.chars.is_all_lower): 
                                break
                            if (tt11.is_char_of(",.;") and tt11.next0_ is not None): 
                                tt11 = tt11.next0_
                            nex = BookLinkToken.try_parse(tt11, 0)
                            if (nex is not None and nex.typ != BookLinkTyp.PERSON and nex.typ != BookLinkTyp.ANDOTHERS): 
                                break
                    elif ((blt00 is not None and blt00.person_template != FioTemplateType.UNDEFINED and blt.person_template != blt00.person_template) and blt.person_template == FioTemplateType.NAMESURNAME): 
                        if (blt.end_token.next0_ is None or not blt.end_token.next0_.is_comma_and): 
                            break
                        if (BookLinkToken.try_parse_author(blt.end_token.next0_.next0_, FioTemplateType.UNDEFINED) is not None): 
                            pass
                        else: 
                            break
                    if (blt00 is None and blt.person_template == FioTemplateType.NAMESURNAME): 
                        tt = blt.end_token.next0_
                        if (tt is not None and tt.is_hiphen): 
                            tt = tt.next0_
                        if (isinstance(tt, NumberToken)): 
                            break
                    BookLinkAnalyzer.__add_author(res, blt)
                    coef += 1
                    t = blt.end_token
                    if (isinstance(t.get_referent(), PersonReferent)): 
                        corr_authors.append(Utils.asObjectOrNull(t, ReferentToken))
                    blt00 = blt
                    prev_pers_templ = blt.person_template
                    start_of_name = blt.start_of_name
                    if ((start_of_name) is not None): 
                        t = t.next0_
                        break
                    continue
                if (blt.typ == BookLinkTyp.ANDOTHERS): 
                    coef += 0.5
                    t = blt.end_token.next0_
                    res.authors_and_other = True
                    break
                break
        if (t is None): 
            return None
        if ((t.is_newline_before and t != t0 and num is None) and res.find_slot(BookLinkReferent.ATTR_AUTHOR, None, True) is None): 
            return None
        if (start_of_name is None): 
            if (t.chars.is_all_lower): 
                coef -= (1)
            if (t.chars.is_latin_letter and not is_electr_res and num is None): 
                if (res.get_slot_value(BookLinkReferent.ATTR_AUTHOR) is None): 
                    return None
        tn0 = t
        tn1 = None
        uri = None
        next_num = None
        wrapnn376 = RefOutArgWrapper(0)
        inoutres377 = Utils.tryParseInt(Utils.ifNotNull(num, ""), wrapnn376)
        nn = wrapnn376.value
        if (inoutres377): 
            next_num = str((nn + 1))
        br = (BracketHelper.try_parse(t, Utils.valToEnum((BracketParseAttr.CANCONTAINSVERBS) | (BracketParseAttr.CANBEMANYLINES), BracketParseAttr), 100) if BracketHelper.can_be_start_of_sequence(t, True, False) else None)
        if (br is not None): 
            t = t.next0_
        pages = None
        first_pass3521 = True
        while True:
            if first_pass3521: first_pass3521 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (max_char > 0 and t.begin_char >= max_char): 
                break
            if (br is not None and br.end_token == t): 
                tn1 = t
                break
            tit = TitleItemToken.try_attach(t)
            if (tit is not None): 
                if ((tit.typ == TitleItemToken.Types.TYP and tn0 == t and br is None) and BracketHelper.can_be_start_of_sequence(tit.end_token.next0_, True, False)): 
                    br = BracketHelper.try_parse(tit.end_token.next0_, BracketParseAttr.NO, 100)
                    if (br is not None): 
                        coef += (1)
                        if (num is not None): 
                            coef += 1
                        tn0 = br.begin_token
                        tn1 = br.end_token
                        res.typ = tit.value.lower()
                        t = br.end_token.next0_
                        break
            if (t.is_newline_before and t != tn0): 
                if (br is not None and (t.end_char < br.end_char)): 
                    pass
                elif (not MiscHelper.can_be_start_of_sentence(t)): 
                    pass
                else: 
                    if (t.newlines_before_count > 1): 
                        break
                    if ((isinstance(t, NumberToken)) and num is not None and t.int_value is not None): 
                        if (num == str((t.int_value - 1))): 
                            break
                    elif (num is not None): 
                        pass
                    else: 
                        nnn = NounPhraseHelper.try_parse(t.previous, Utils.valToEnum(((NounPhraseParseAttr.PARSEPREPOSITION) | (NounPhraseParseAttr.PARSEADVERBS) | (NounPhraseParseAttr.PARSENUMERICASADJECTIVE)) | (NounPhraseParseAttr.MULTILINES), NounPhraseParseAttr), 0, None)
                        if (nnn is not None and nnn.end_char >= t.end_char): 
                            pass
                        else: 
                            break
            if (t.is_char_of(".;") and t.whitespaces_after_count > 0): 
                tit = TitleItemToken.try_attach(t.next0_)
                if ((tit) is not None): 
                    if (tit.typ == TitleItemToken.Types.TYP): 
                        break
                stop = True
                words = 0
                notwords = 0
                tt = t.next0_
                first_pass3522 = True
                while True:
                    if first_pass3522: first_pass3522 = False
                    else: tt = tt.next0_
                    if (not (tt is not None)): break
                    blt0 = BookLinkToken.try_parse(tt, 0)
                    if (blt0 is None): 
                        if (tt.is_newline_before): 
                            break
                        if ((isinstance(tt, TextToken)) and not tt.get_morph_class_in_dictionary().is_undefined): 
                            words += 1
                        else: 
                            notwords += 1
                        if (words > 6 and words > (notwords * 4)): 
                            stop = False
                            break
                        continue
                    if ((blt0.typ == BookLinkTyp.DELIMETER or blt0.typ == BookLinkTyp.TRANSLATE or blt0.typ == BookLinkTyp.TYPE) or blt0.typ == BookLinkTyp.GEO or blt0.typ == BookLinkTyp.PRESS): 
                        stop = False
                    break
                if (br is not None and br.end_token.previous.end_char > t.end_char): 
                    stop = False
                if (stop): 
                    break
            if (t == decree): 
                t = t.next0_
                break
            blt = BookLinkToken.try_parse(t, 0)
            if (blt is None): 
                tn1 = t
                continue
            if (blt.typ == BookLinkTyp.DELIMETER): 
                break
            if (((blt.typ == BookLinkTyp.MISC or blt.typ == BookLinkTyp.TRANSLATE or blt.typ == BookLinkTyp.NAMETAIL) or blt.typ == BookLinkTyp.TYPE or blt.typ == BookLinkTyp.VOLUME) or blt.typ == BookLinkTyp.PAGERANGE or blt.typ == BookLinkTyp.PAGES): 
                coef += 1
                break
            if (blt.typ == BookLinkTyp.GEO or blt.typ == BookLinkTyp.PRESS): 
                if (t.previous.is_hiphen or t.previous.is_char_of(".;") or blt.add_coef > 0): 
                    break
            if (blt.typ == BookLinkTyp.YEAR): 
                if (t.previous is not None and t.previous.is_comma): 
                    break
            if (blt.typ == BookLinkTyp.ELECTRONRES): 
                is_electr_res = True
                break
            if (blt.typ == BookLinkTyp.URL): 
                if (t == tn0 or t.previous.is_char_of(":.")): 
                    is_electr_res = True
                    break
            tn1 = t
        if (tn1 is None and start_of_name is None): 
            if (is_electr_res): 
                uri_re = BookLinkReferent()
                rt0 = ReferentToken(uri_re, t00, t)
                rts0 = list()
                bref0 = BookLinkRefReferent._new372(uri_re)
                if (num is not None): 
                    bref0.number = num
                rt01 = ReferentToken(bref0, t0, rt0.end_token)
                ok = False
                while t is not None: 
                    if (t.is_newline_before): 
                        break
                    blt0 = BookLinkToken.try_parse(t, 0)
                    if (blt0 is not None): 
                        if (isinstance(blt0.ref, UriReferent)): 
                            uri_re.add_slot(BookLinkReferent.ATTR_URL, Utils.asObjectOrNull(blt0.ref, UriReferent), False, 0)
                            ok = True
                        t = blt0.end_token
                    rt0.end_token = rt01.end_token = t
                    t = t.next0_
                if (ok): 
                    rts0.append(rt01)
                    rts0.append(rt0)
                    return rts0
            if (decree is not None and num is not None): 
                rts0 = list()
                bref0 = BookLinkRefReferent._new372(decree.get_referent())
                if (num is not None): 
                    bref0.number = num
                rt01 = ReferentToken(bref0, t0, decree)
                t = decree.next0_
                while t is not None: 
                    if (t.is_newline_before): 
                        break
                    if (isinstance(t, TextToken)): 
                        if (t.is_pure_verb): 
                            return None
                    rt01.end_token = t
                    t = t.next0_
                rts0.append(rt01)
                return rts0
            if (book_prev is not None): 
                tt = t
                while tt is not None and ((tt.is_char_of(",.") or tt.is_hiphen)):
                    tt = tt.next0_
                blt0 = BookLinkToken.try_parse(tt, 0)
                if (blt0 is not None and blt0.typ == BookLinkTyp.PAGERANGE): 
                    rts0 = list()
                    bref0 = BookLinkRefReferent._new372(book_prev)
                    if (num is not None): 
                        bref0.number = num
                    bref0.pages = blt0.value
                    rt00 = ReferentToken(bref0, t0, blt0.end_token)
                    rts0.append(rt00)
                    return rts0
            return None
        if (br is not None and ((tn1 == br.end_token or tn1 == br.end_token.previous))): 
            tn0 = tn0.next0_
            tn1 = tn1.previous
        if (start_of_name is None): 
            while tn0 is not None:
                if (tn0.is_char_of(":,~")): 
                    tn0 = tn0.next0_
                else: 
                    break
        while tn1 is not None and tn1.begin_char > tn0.begin_char: 
            if (tn1.is_char_of(".;,:(~") or tn1.is_hiphen or tn1.is_value("РЕД", None)): 
                pass
            else: 
                break
            tn1 = tn1.previous
        nam = MiscHelper.get_text_value(tn0, tn1, Utils.valToEnum((GetTextAttr.KEEPQUOTES) | (GetTextAttr.KEEPREGISTER), GetTextAttr))
        if (start_of_name is not None): 
            if (nam is None or (len(nam) < 3)): 
                nam = start_of_name
            else: 
                nam = "{0}{1}{2}".format(start_of_name, (" " if tn0.is_whitespace_before else ""), nam)
        if (nam is None): 
            return None
        res.name = nam
        if (num is None and not is_in_lit): 
            if (len(nam) < 20): 
                return None
            coef -= (2)
        if (len(nam) > 500): 
            coef -= (math.floor(len(nam) / 500))
        if (is_bracket_regime): 
            coef -= 1
        if (len(nam) > 200): 
            if (num is None): 
                return None
            if (res.find_slot(BookLinkReferent.ATTR_AUTHOR, None, True) is None and not BookLinkToken.check_link_before(t0, num)): 
                return None
        en = 0
        ru = 0
        ua = 0
        cha = 0
        nocha = 0
        chalen = 0
        lt0 = tn0
        lt1 = tn1
        if (tn1 is None): 
            if (t is None): 
                return None
            lt0 = t0
            lt1 = t
            tn1 = t.previous
        tt = lt0
        while tt is not None and tt.end_char <= lt1.end_char: 
            if ((isinstance(tt, TextToken)) and tt.chars.is_letter): 
                if (tt.chars.is_latin_letter): 
                    en += 1
                elif (tt.morph.language.is_ua): 
                    ua += 1
                elif (tt.morph.language.is_ru): 
                    ru += 1
                if (tt.length_char > 2): 
                    cha += 1
                    chalen += tt.length_char
            elif (not (isinstance(tt, ReferentToken))): 
                nocha += 1
            tt = tt.next0_
        if (ru > (ua + en)): 
            res.lang = "RU"
        elif (ua > (ru + en)): 
            res.lang = "UA"
        elif (en > (ru + ua)): 
            res.lang = "EN"
        if (nocha > 3 and nocha > cha and start_of_name is None): 
            if (nocha > (math.floor(chalen / 3))): 
                coef -= (2)
        if (res.lang == "EN"): 
            tt = tn0.next0_
            first_pass3523 = True
            while True:
                if first_pass3523: first_pass3523 = False
                else: tt = tt.next0_
                if (not (tt is not None and (tt.end_char < tn1.end_char))): break
                if (tt.is_comma and tt.next0_ is not None and ((not tt.next0_.chars.is_all_lower or (isinstance(tt.next0_, ReferentToken))))): 
                    if (tt.next0_.next0_ is not None and tt.next0_.next0_.is_comma_and): 
                        if (isinstance(tt.next0_, ReferentToken)): 
                            pass
                        else: 
                            continue
                    nam = MiscHelper.get_text_value(tn0, tt.previous, Utils.valToEnum((GetTextAttr.KEEPQUOTES) | (GetTextAttr.KEEPREGISTER), GetTextAttr))
                    if (nam is not None and len(nam) > 15): 
                        res.name = nam
                        break
        rt = ReferentToken(res, t00, tn1)
        authors = True
        edits = False
        br = (None)
        first_pass3524 = True
        while True:
            if first_pass3524: first_pass3524 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (max_char > 0 and t.begin_char >= max_char): 
                break
            if (BracketHelper.can_be_start_of_sequence(t, False, False)): 
                br = BracketHelper.try_parse(t, BracketParseAttr.CANBEMANYLINES, 100)
                if (br is not None and br.length_char > 300): 
                    br = (None)
            blt = BookLinkToken.try_parse(t, 0)
            if (t.is_newline_before and not t.is_char('/') and not t.previous.is_char('/')): 
                if (blt is not None and blt.typ == BookLinkTyp.NUMBER): 
                    break
                if (t.previous.is_char_of(":")): 
                    pass
                elif (blt is not None and ((((blt.typ == BookLinkTyp.DELIMETER or blt.typ == BookLinkTyp.PAGERANGE or blt.typ == BookLinkTyp.PAGES) or blt.typ == BookLinkTyp.GEO or blt.typ == BookLinkTyp.PRESS) or blt.typ == BookLinkTyp.N))): 
                    pass
                elif (num is not None and BookLinkToken.try_parse_author(t, FioTemplateType.UNDEFINED) is not None): 
                    pass
                elif (num is not None and blt is not None and blt.typ != BookLinkTyp.NUMBER): 
                    pass
                elif (br is not None and (t.end_char < br.end_char) and t.begin_char > br.begin_char): 
                    pass
                else: 
                    ok = False
                    mmm = 50
                    tt = t.next0_
                    while tt is not None and mmm > 0: 
                        if (tt.is_newline_before): 
                            blt2 = BookLinkToken.try_parse(tt, 0)
                            if (blt2 is not None and blt2.typ == BookLinkTyp.NUMBER and blt2.value == next_num): 
                                ok = True
                                break
                            if (blt2 is not None): 
                                if (blt2.typ == BookLinkTyp.PAGES or blt2.typ == BookLinkTyp.GEO or blt2.typ == BookLinkTyp.PRESS): 
                                    ok = True
                                    break
                        tt = tt.next0_; mmm -= 1
                    if (not ok): 
                        npt = NounPhraseHelper.try_parse(t.previous, Utils.valToEnum(((NounPhraseParseAttr.MULTILINES) | (NounPhraseParseAttr.PARSEADVERBS) | (NounPhraseParseAttr.PARSEPREPOSITION)) | (NounPhraseParseAttr.PARSEVERBS) | (NounPhraseParseAttr.PARSEPRONOUNS), NounPhraseParseAttr), 0, None)
                        if (npt is not None and npt.end_char >= t.end_char): 
                            ok = True
                    if (not ok): 
                        break
            rt.end_token = t
            if (blt is not None): 
                rt.end_token = blt.end_token
            if (t.is_char_of(".,") or t.is_hiphen): 
                continue
            if (t.is_value("С", None)): 
                pass
            if (regtyp == BookLinkAnalyzer.RegionTyp.FIRST and blt is not None and blt.typ == BookLinkTyp.EDITORS): 
                edits = True
                t = blt.end_token
                coef += 1
                continue
            if (regtyp == BookLinkAnalyzer.RegionTyp.FIRST and blt is not None and blt.typ == BookLinkTyp.SOSTAVITEL): 
                edits = False
                t = blt.end_token
                coef += 1
                continue
            if (regtyp == BookLinkAnalyzer.RegionTyp.FIRST and authors): 
                blt2 = BookLinkToken.try_parse_author(t, prev_pers_templ)
                if (blt2 is not None and blt2.typ == BookLinkTyp.PERSON): 
                    prev_pers_templ = blt2.person_template
                    if (not edits): 
                        BookLinkAnalyzer.__add_author(res, blt2)
                    coef += 1
                    t = blt2.end_token
                    continue
                if (blt2 is not None and blt2.typ == BookLinkTyp.ANDOTHERS): 
                    if (not edits): 
                        res.authors_and_other = True
                    coef += 1
                    t = blt2.end_token
                    continue
                authors = False
            if (blt is None): 
                continue
            if (blt.typ == BookLinkTyp.ELECTRONRES or blt.typ == BookLinkTyp.URL): 
                is_electr_res = True
                if (blt.typ == BookLinkTyp.ELECTRONRES): 
                    coef += 1.5
                else: 
                    coef += 0.5
                if (isinstance(blt.ref, UriReferent)): 
                    res.add_slot(BookLinkReferent.ATTR_URL, Utils.asObjectOrNull(blt.ref, UriReferent), False, 0)
            elif (blt.typ == BookLinkTyp.YEAR): 
                if (res.year == 0): 
                    res.year = int(blt.value)
                    coef += 0.5
            elif (blt.typ == BookLinkTyp.DELIMETER): 
                coef += 1
                if (blt.length_char == 2): 
                    regtyp = BookLinkAnalyzer.RegionTyp.SECOND
                else: 
                    regtyp = BookLinkAnalyzer.RegionTyp.FIRST
            elif ((((blt.typ == BookLinkTyp.MISC or blt.typ == BookLinkTyp.TYPE or blt.typ == BookLinkTyp.PAGES) or blt.typ == BookLinkTyp.NAMETAIL or blt.typ == BookLinkTyp.TRANSLATE) or blt.typ == BookLinkTyp.PRESS or blt.typ == BookLinkTyp.VOLUME) or blt.typ == BookLinkTyp.N): 
                coef += 1
            elif (blt.typ == BookLinkTyp.PAGERANGE): 
                pages = blt
                coef += 1
                if (is_bracket_regime and blt.end_token.next0_ is not None and blt.end_token.next0_.is_char(')')): 
                    coef += (2)
                    if (res.name is not None and res.find_slot(BookLinkReferent.ATTR_AUTHOR, None, True) is not None): 
                        coef = (10)
            elif (blt.typ == BookLinkTyp.GEO and ((regtyp == BookLinkAnalyzer.RegionTyp.SECOND or regtyp == BookLinkAnalyzer.RegionTyp.FIRST))): 
                coef += 1
            elif (blt.typ == BookLinkTyp.GEO and t.previous is not None and t.previous.is_char('.')): 
                coef += 1
            elif (blt.typ == BookLinkTyp.ANDOTHERS): 
                coef += 1
                if (authors): 
                    res.authors_and_other = True
            coef += blt.add_coef
            t = blt.end_token
        if ((coef < 2.5) and num is not None): 
            if (BookLinkToken.check_link_before(t0, num)): 
                coef += (2)
            elif (BookLinkToken.check_link_after(rt.end_token, num)): 
                coef += (1)
        if (rt.length_char > 500): 
            return None
        if (is_in_lit): 
            coef += 1
        if (coef < 2.5): 
            if (is_electr_res and uri is not None): 
                pass
            elif (coef >= 2 and is_in_lit): 
                pass
            else: 
                return None
        for rr in corr_authors: 
            pits0 = PersonItemToken.try_attach_list(rr.begin_token, None, PersonItemToken.ParseAttr.CANINITIALBEDIGIT, 10)
            if (pits0 is None or (len(pits0) < 2)): 
                continue
            if (pits0[0].typ == PersonItemToken.ItemType.VALUE): 
                exi = False
                for i in range(len(rr.referent.slots) - 1, -1, -1):
                    s = rr.referent.slots[i]
                    if (s.type_name == PersonReferent.ATTR_LASTNAME): 
                        ln = Utils.asObjectOrNull(s.value, str)
                        if (ln is None): 
                            continue
                        if (ln == pits0[0].value): 
                            exi = True
                            continue
                        if (ln.find('-') > 0): 
                            ln = ln[0:0+ln.find('-')]
                        if (pits0[0].begin_token.is_value(ln, None)): 
                            del rr.referent.slots[i]
                if (not exi): 
                    rr.referent.add_slot(PersonReferent.ATTR_LASTNAME, pits0[0].value, False, 0)
        rts = list()
        bref = BookLinkRefReferent._new372(res)
        if (num is not None): 
            bref.number = num
        rt1 = ReferentToken(bref, t0, rt.end_token)
        if (pages is not None): 
            if (pages.value is not None): 
                bref.pages = pages.value
            rt.end_token = pages.begin_token.previous
        rts.append(rt1)
        rts.append(rt)
        return rts
    
    @staticmethod
    def __add_author(blr : 'BookLinkReferent', tok : 'BookLinkToken') -> None:
        if (tok.ref is not None): 
            blr.add_slot(BookLinkReferent.ATTR_AUTHOR, tok.ref, False, 0)
        elif (tok.tok is not None): 
            blr.add_slot(BookLinkReferent.ATTR_AUTHOR, tok.tok.referent, False, 0)
            blr.add_ext_referent(tok.tok)
        elif (tok.value is not None): 
            blr.add_slot(BookLinkReferent.ATTR_AUTHOR, tok.value, False, 0)
    
    @staticmethod
    def initialize() -> None:
        MetaBookLink.initialize2()
        MetaBookLinkRef.initialize()
        try: 
            Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = True
            BookLinkToken.initialize()
            Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = False
        except Exception as ex: 
            raise Utils.newException(ex.__str__(), ex)
        ProcessorService.register_analyzer(BookLinkAnalyzer())