# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import math
import io
import typing
from pullenti.ntopy.Utils import Utils
from pullenti.ner.MetaToken import MetaToken

from pullenti.ner.instrument.InstrumentKind import InstrumentKind
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.decree.DecreeKind import DecreeKind


from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.instrument.internal.ILTypes import ILTypes
from pullenti.ner.core.internal.TableHelper import TableHelper
from pullenti.ner.decree.DecreeChangeKind import DecreeChangeKind
from pullenti.ner.core.internal.BlkTyps import BlkTyps
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner._org.OrganizationKind import OrganizationKind

from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.instrument.internal.NumberTypes import NumberTypes
from pullenti.ner.instrument.internal.ContentAnalyzeWhapper import ContentAnalyzeWhapper
from pullenti.ner.instrument.internal.NumberingHelper import NumberingHelper
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.decree.DecreeChangeValueKind import DecreeChangeValueKind


class FragToken(MetaToken):
    
    @staticmethod
    def __createtztitle(t0 : 'Token', doc : 'InstrumentReferent') -> 'FragToken':
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.decree.internal.DecreeToken import DecreeToken
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        tz = None
        cou = 0
        t = t0
        first_pass2877 = True
        while True:
            if first_pass2877: first_pass2877 = False
            else: t = t.next0_
            if (not (t is not None and (cou < 300))): break
            if (isinstance(t, TextToken) and t.length_char > 1): 
                cou += 1
            if (not t.is_newline_before): 
                if (t.previous is not None and t.previous.is_table_control_char): 
                    pass
                else: 
                    continue
            dt = DecreeToken.try_attach(t, None, False)
            if (dt is not None and dt.typ == DecreeToken.ItemType.TYP): 
                if (dt.value == "ТЕХНИЧЕСКОЕ ЗАДАНИЕ"): 
                    tz = dt
                break
        if (tz is None): 
            return None
        title = FragToken._new1236(t0, tz.end_token, InstrumentKind.HEAD)
        t = t0
        first_pass2878 = True
        while True:
            if first_pass2878: first_pass2878 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (not t.is_newline_before): 
                title.end_token = t
                continue
            if (FragToken.__is_start_of_body(t)): 
                break
            if (t.is_value("СОДЕРЖИМОЕ", None) or t.is_value("СОДЕРЖАНИЕ", None) or t.is_value("ОГЛАВЛЕНИЕ", None)): 
                break
            dt = DecreeToken.try_attach(t, None, False)
            if (dt is not None): 
                FragToken.__add_title_attr(doc, title, dt)
                t = dt.end_token
                title.end_token = t
                if (dt.typ != DecreeToken.ItemType.TYP): 
                    continue
                br = BracketHelper.try_parse(t.next0_, BracketParseAttr.CANBEMANYLINES, 100)
                if (br is not None and BracketHelper.is_bracket(t.next0_, True)): 
                    nam = FragToken._new1257(br.begin_token, br.end_token, InstrumentKind.NAME, True)
                    title.children.append(nam)
                    t = br.end_token
                    title.end_token = t
                    continue
                if (t.next0_ is not None and t.next0_.is_value("НА", None)): 
                    t1 = t.next0_
                    tt = t1.next0_
                    first_pass2879 = True
                    while True:
                        if first_pass2879: first_pass2879 = False
                        else: tt = tt.next0_
                        if (not (tt is not None)): break
                        if (tt.is_newline_before): 
                            if (MiscHelper.can_be_start_of_sentence(tt)): 
                                break
                        br1 = BracketHelper.try_parse(tt, BracketParseAttr.NO, 100)
                        if (br1 is not None): 
                            tt = br1.end_token
                            t1 = tt
                            continue
                        npt = NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.PARSEPREPOSITION, 0)
                        if (npt is not None): 
                            tt = npt.end_token
                        t1 = tt
                    nam = FragToken._new1257(t.next0_, t1, InstrumentKind.NAME, True)
                    title.children.append(nam)
                    t = t1
                    title.end_token = t
                    continue
            appr1 = FragToken.__create_approved(t)
            if (appr1 is not None): 
                t = appr1.end_token
                title.children.append(appr1)
                title.end_token = appr1.end_token
                continue
            appr1 = FragToken._create_misc(t)
            if (appr1 is not None): 
                t = appr1.end_token
                title.children.append(appr1)
                title.end_token = appr1.end_token
                continue
            eds = FragToken._create_editions(t)
            if (eds is not None): 
                title.children.append(eds)
                t = eds.end_token
                title.end_token = t
                continue
        return title
    
    @staticmethod
    def __create_doc_title(t0 : 'Token', doc : 'InstrumentReferent') -> 'FragToken':
        if (t0 is None): 
            return None
        title = FragToken.__create_contract_title(t0, doc)
        if (title is not None): 
            return title
        title = FragToken.__create_gost_title(t0, doc)
        if (title is not None): 
            return title
        title = FragToken.__create_zapiska_title(t0, doc)
        if (title is not None): 
            return title
        title = FragToken.__createtztitle(t0, doc)
        if (title is not None): 
            return title
        doc.slots.clear()
        title = FragToken.__create_project_title(t0, doc)
        if (title is not None): 
            return title
        doc.slots.clear()
        title = FragToken.__create_doc_title_(t0, doc)
        if (title is not None and len(title.children) == 1 and title.children[0].kind == InstrumentKind.NAME): 
            title2 = FragToken.__create_doc_title_(title.end_token.next0_, doc)
            if (title2 is not None and doc.typ is not None): 
                title.children.extend(title2.children)
                title.end_token = title2.end_token
        return title
    
    @staticmethod
    def __create_doc_title_(t0 : 'Token', doc : 'InstrumentReferent') -> 'FragToken':
        from pullenti.ner.decree.internal.DecreeToken import DecreeToken
        from pullenti.ner.decree.DecreeReferent import DecreeReferent
        from pullenti.ner.instrument.internal.InstrToken1 import InstrToken1
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.money.MoneyReferent import MoneyReferent
        from pullenti.ner._org.OrganizationReferent import OrganizationReferent
        from pullenti.ner.instrument.internal.InstrToken import InstrToken
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.decree.DecreePartReferent import DecreePartReferent
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.decree.internal.PartToken import PartToken
        from pullenti.ner.instrument.InstrumentReferent import InstrumentReferent
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.date.DateReferent import DateReferent
        from pullenti.ner.address.AddressReferent import AddressReferent
        from pullenti.ner.uri.UriReferent import UriReferent
        from pullenti.ner.phone.PhoneReferent import PhoneReferent
        from pullenti.ner.person.PersonIdentityReferent import PersonIdentityReferent
        from pullenti.ner.bank.BankDataReferent import BankDataReferent
        from pullenti.ner.person.PersonReferent import PersonReferent
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.morph.MorphClass import MorphClass
        from pullenti.ner.geo.GeoReferent import GeoReferent
        while t0 is not None: 
            if (not t0.is_table_control_char): 
                break
            t0 = t0.next0_
        if (t0 is None): 
            return None
        title = FragToken._new1236(t0, t0, InstrumentKind.HEAD)
        dt0 = None
        t1 = None
        name_ = None
        nt0 = None
        empty_lines = 0
        end_empty_lines = None
        ignore_empty_lines = False
        attrs = 0
        can_be_orgs = True
        unknown_orgs = list()
        is_contract = False
        start_of_name = False
        t = t0
        if (t0.get_referent() is not None): 
            if (t0.get_referent().type_name == "PERSON"): 
                return None
        appr0 = None
        if (t0.is_value("УТВЕРДИТЬ", "ЗАТВЕРДИТИ") or t0.is_value("ПРИНЯТЬ", "ПРИЙНЯТИ") or t0.is_value("УТВЕРЖДАТЬ", None)): 
            appr0 = FragToken.__create_approved(t)
            if (appr0 is not None and appr0.referents is None): 
                appr0 = None
        if (appr0 is not None): 
            title.end_token = appr0.end_token
            t1 = title.end_token
            title.children.append(appr0)
            t = t1.next0_
        if (t is not None and t.is_value("ДЕЛО", "СПРАВА")): 
            dt = DecreeToken.try_attach(t.next0_, None, False)
            if (dt is not None and dt.typ == DecreeToken.ItemType.NUMBER): 
                dt.begin_token = t
                title.children.append(FragToken._new1284(t, t, InstrumentKind.KEYWORD, "ДЕЛО"))
                FragToken.__add_title_attr(doc, title, dt)
                t = dt.end_token.next0_
                if (t is not None and t.is_value("КОПИЯ", "КОПІЯ")): 
                    t = t.next0_
                elif ((t.is_char('(') and t.next0_ is not None and t.next0_.is_value("КОПИЯ", "КОПІЯ")) and t.next0_.next0_ is not None and t.next0_.next0_.is_char(')')): 
                    t = t.next0_.next0_
        first_pass2880 = True
        while True:
            if first_pass2880: first_pass2880 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_table_control_char): 
                continue
            if (t.is_newline_before or ((t.previous is not None and t.previous.is_table_control_char))): 
                if (isinstance(t.get_referent(), DecreeReferent) and (t.get_referent() if isinstance(t.get_referent(), DecreeReferent) else None).kind != DecreeKind.PUBLISHER): 
                    t = t.kit.debed_token(t)
                if (t.is_value("О", "ПРО") or t.is_value("ОБ", None) or t.is_value("ПО", None)): 
                    break
                if (FragToken.__is_start_of_body(t)): 
                    break
                if (t.is_char_of("[") and name_ is None): 
                    break
                iii = InstrToken1.parse(t, True, None, 0, None, False, 0, False)
                if (iii is not None and iii.typ == InstrToken1.Types.COMMENT): 
                    cmt = FragToken._new1236(iii.begin_token, iii.end_token, InstrumentKind.COMMENT)
                    title.children.append(cmt)
                    title.end_token = iii.end_token
                    t1 = title.end_token
                    t = t1
                    continue
                if (iii is not None and iii.end_token.is_char('?')): 
                    cmt = FragToken._new1236(iii.begin_token, iii.end_token, InstrumentKind.NAME)
                    cmt.value = FragToken._get_restored_namemt(iii, False)
                    title.children.append(cmt)
                    title.end_token = iii.end_token
                    t1 = title.end_token
                    t = t1
                    break
                if ((((t.is_value("ЗАЯВИТЕЛЬ", "ЗАЯВНИК") or t.is_value("ИСТЕЦ", "ПОЗИВАЧ") or t.is_value("ОТВЕТЧИК", "ВІДПОВІДАЧ")) or t.is_value("ДОЛЖНИК", "БОРЖНИК") or t.is_value("КОПИЯ", "КОПІЯ"))) and t.next0_ is not None and ((t.next0_.is_char(':') or t.next0_.is_table_control_char))): 
                    ptt = FragToken.__create_just_participant(t.next0_.next0_, None)
                    if (ptt is not None): 
                        if (t.is_value("КОПИЯ", None)): 
                            pass
                        t1 = ptt.end_token
                        while t1.next0_ is not None and t1.next0_.is_table_control_char:
                            t1 = t1.next0_
                        if (t1.next0_ is not None and t1.next0_.is_char('(')): 
                            br = BracketHelper.try_parse(t1.next0_, BracketParseAttr.NO, 100)
                            if (br is not None): 
                                t1 = br.end_token
                        ft = FragToken._new1236(t, t1, InstrumentKind.INITIATOR)
                        title.children.append(ft)
                        title.end_token = t1
                        t = title.end_token
                        continue
                if (t.is_value("ЦЕНА", "ЦІНА") and t.next0_ is not None and t.next0_.is_value("ИСК", "ПОЗОВ")): 
                    has_money = False
                    tt = t.next0_
                    while tt is not None: 
                        if (isinstance(tt.get_referent(), MoneyReferent)): 
                            has_money = True
                        if (tt.is_newline_after): 
                            break
                        tt = tt.next0_
                    if (tt is not None and has_money): 
                        while tt.next0_ is not None and tt.next0_.is_table_control_char:
                            tt = tt.next0_
                        if (tt.next0_ is not None and tt.next0_.is_char('(')): 
                            br = BracketHelper.try_parse(tt.next0_, BracketParseAttr.NO, 100)
                            if (br is not None): 
                                tt = br.end_token
                        title.children.append(FragToken._new1236(t, tt, InstrumentKind.CASEINFO))
                        t1 = tt
                        title.end_token = t1
                        t = title.end_token
                        continue
                if (t.is_value("В", "У")): 
                    tt = t.next0_
                    if (tt is not None and tt.is_table_control_char): 
                        tt = tt.next0_
                    if (tt is not None and isinstance(tt.get_referent(), OrganizationReferent)): 
                        r = tt.get_referent()
                        while tt.next0_ is not None and tt.next0_.is_table_control_char:
                            tt = tt.next0_
                        t1 = tt
                        if (t1.next0_ is not None and t1.next0_.is_char('(')): 
                            br = BracketHelper.try_parse(t1.next0_, BracketParseAttr.NO, 100)
                            if (br is not None): 
                                t1 = br.end_token
                        ooo = FragToken._new1236(t, t1, InstrumentKind.ORGANIZATION)
                        ooo.referents = list()
                        ooo.referents.append(r)
                        title.children.append(ooo)
                        title.end_token = t1
                        t = title.end_token
                        continue
                if (t.length_char == 1 and t.chars.is_letter and t.is_whitespace_after): 
                    for ii in range(len(InstrToken._m_directives_norm)):
                        ee = MiscHelper.try_attach_word_by_letters(InstrToken._m_directives_norm[ii], t, False)
                        if (ee is not None and ee.is_newline_after): 
                            ooo = FragToken._new1284(t, ee, InstrumentKind.KEYWORD, InstrToken._m_directives_norm[ii])
                            title.children.append(ooo)
                            doc.typ = InstrToken._m_directives_norm[ii]
                            title.end_token = ee
                            t = title.end_token
                            break
                    else: ii = len(InstrToken._m_directives_norm)
                    if (ii < len(InstrToken._m_directives_norm)): 
                        continue
            if (t.is_hiphen or t.is_char('_')): 
                ch = t.get_source_text()[0]
                while t is not None: 
                    if (not t.is_char(ch)): 
                        break
                    t = t.next0_
            if (t is None): 
                break
            casinf = FragToken.__create_case_info(t)
            if (casinf is not None): 
                break
            dr0 = (t.get_referent() if isinstance(t.get_referent(), DecreeReferent) else None)
            if (dr0 is not None): 
                if (dr0.kind == DecreeKind.PUBLISHER): 
                    continue
            elif (isinstance(t.get_referent(), DecreePartReferent)): 
                dpr = (t.get_referent() if isinstance(t.get_referent(), DecreePartReferent) else None)
                if (dpr is not None): 
                    if (((dpr.part is None and dpr.doc_part is None)) or len(dpr.slots) != 2): 
                        break
                    if (isinstance(t.next0_, TextToken) and (t.next0_ if isinstance(t.next0_, TextToken) else None).is_pure_verb): 
                        break
                    dr0 = dpr.owner
            if (dr0 is not None): 
                if (doc.typ is None or doc.typ == dr0.typ): 
                    tt1 = (t if isinstance(t, ReferentToken) else None).begin_token
                    li = DecreeToken.try_attach_list(tt1, None, 10, False)
                    if (li is not None and len(li) > 0 and li[len(li) - 1].is_newline_after): 
                        for dd in li: 
                            FragToken.__add_title_attr(doc, title, dd)
                        ttt = li[len(li) - 1].end_token
                        if (ttt.end_char < t.end_char): 
                            nt0 = ttt.next0_
                            name_ = FragToken._get_restored_name(ttt.next0_, (t if isinstance(t, ReferentToken) else None).end_token, False)
                        t1 = t
                        if (name_ is not None and t1.is_newline_after): 
                            t = t.next0_
                            break
                        if (doc.typ == "КОДЕКС"): 
                            pt = PartToken.try_attach(t.next0_, None, False, False)
                            if (pt is not None): 
                                if (((pt.typ != PartToken.ItemType.PART and pt.typ != PartToken.ItemType.DOCPART)) or len(pt.values) != 1): 
                                    pt = None
                            if (pt is not None and len(pt.values) > 0): 
                                doc.add_slot(InstrumentReferent.ATTR_PART, pt.values[0].value, False, 0)
                                title.children.append(FragToken._new1284(pt.begin_token, pt.end_token, InstrumentKind.DOCPART, pt.values[0].value))
                                t = pt.end_token
                                continue
                        if (doc.name is not None): 
                            t = t.next0_
                            break
                elif (dr0.typ == "КОДЕКС"): 
                    pt = PartToken.try_attach(t.next0_, None, False, False)
                    nam = dr0.name
                    if (pt is not None): 
                        if (((pt.typ != PartToken.ItemType.PART and pt.typ != PartToken.ItemType.DOCPART)) or len(pt.values) != 1): 
                            pt = None
                    if (pt is not None and len(pt.values) > 0): 
                        doc.add_slot(InstrumentReferent.ATTR_PART, pt.values[0].value, False, 0)
                    doc.add_slot(InstrumentReferent.ATTR_NAME, nam, False, 0)
                    doc.typ = dr0.typ
                    geo_ = dr0.get_value(DecreeReferent.ATTR_GEO)
                    if (geo_ is not None): 
                        doc.add_slot(InstrumentReferent.ATTR_GEO, geo_, False, 0)
                    t1 = t
                    title.children.append(FragToken._new1284(t, t, InstrumentKind.NAME, nam))
                    if (pt is not None and len(pt.values) > 0): 
                        title.children.append(FragToken._new1284(pt.begin_token, pt.end_token, InstrumentKind.DOCPART, pt.values[0].value))
                        t1 = pt.end_token
                    t = t1
                    continue
                t1 = t
                ignore_empty_lines = True
                can_be_orgs = False
                continue
            if (FragToken.__is_start_of_body(t)): 
                break
            if (t.is_value("ПРОЕКТ", None) and t.is_newline_after): 
                continue
            if (doc.typ is None): 
                ttt1 = DecreeToken.is_keyword(t, False)
                if (ttt1 is not None and ttt1.is_newline_after): 
                    typ = MiscHelper.get_text_value(t, ttt1, GetTextAttr.KEEPQUOTES)
                    if (doc.typ is None): 
                        doc.typ = typ
                    title.children.append(FragToken._new1284(t, ttt1, InstrumentKind.TYP, typ))
                    dt0 = DecreeToken._new833(t, ttt1, DecreeToken.ItemType.TYP, typ)
                    can_be_orgs = False
                    t = ttt1
                    t1 = t
                    continue
                if (t.is_newline_before and ttt1 is not None and DecreeToken.try_attach(t, None, False) is None): 
                    start_of_name = True
                    break
            appr = FragToken.__create_approved(t)
            if (appr is not None): 
                t1 = appr.end_token
                t = t1
                title.children.append(appr)
                continue
            misc = FragToken._create_misc(t)
            if (misc is not None): 
                t1 = misc.end_token
                t = t1
                title.children.append(misc)
                continue
            edss = FragToken._create_editions(t)
            if (edss is not None): 
                break
            dt = DecreeToken.try_attach(t, dt0, False)
            if (dt is None and dt0 is not None and ((dt0.typ == DecreeToken.ItemType.OWNER or dt0.typ == DecreeToken.ItemType.ORG))): 
                if (isinstance(t, NumberToken) and t.is_newline_after and t.is_newline_before): 
                    dt = DecreeToken._new833(t, t, DecreeToken.ItemType.NUMBER, str((t if isinstance(t, NumberToken) else None).value))
            if (dt is not None and dt.typ == DecreeToken.ItemType.UNKNOWN): 
                dt = None
            if ((dt is None and isinstance(t, NumberToken) and t.is_newline_before) and t.is_newline_after): 
                if (dt0 is not None and dt0.typ == DecreeToken.ItemType.ORG and (((t if isinstance(t, NumberToken) else None).typ == NumberSpellingType.DIGIT))): 
                    dt = DecreeToken._new833(t, t, DecreeToken.ItemType.NUMBER, str((t if isinstance(t, NumberToken) else None).value))
            if (dt is not None and ((dt.typ == DecreeToken.ItemType.TYP or dt.typ == DecreeToken.ItemType.OWNER or dt.typ == DecreeToken.ItemType.ORG))): 
                if (not t.is_newline_before): 
                    dt = None
                else: 
                    ttt = dt.end_token.next0_
                    while ttt is not None: 
                        if (ttt.is_newline_before): 
                            break
                        elif (isinstance(ttt, TextToken) and (ttt if isinstance(ttt, TextToken) else None).is_pure_verb): 
                            dt = None
                            break
                        ttt = ttt.next0_
            if (dt is not None and dt.typ == DecreeToken.ItemType.DATE and dt0 is not None): 
                if (dt.is_newline_before or dt.is_newline_after): 
                    pass
                else: 
                    dt = None
            if (dt is None): 
                if (isinstance(t.get_referent(), DateReferent)): 
                    continue
                if (t.is_value("ДАТА", None)): 
                    ok = False
                    tt = t.next0_
                    first_pass2881 = True
                    while True:
                        if first_pass2881: first_pass2881 = False
                        else: tt = tt.next0_
                        if (not (tt is not None)): break
                        if ((tt.is_value("ПОДПИСАНИЕ", "ПІДПИСАННЯ") or tt.is_value("ВВЕДЕНИЕ", "ВВЕДЕННЯ") or tt.is_value("ПРИНЯТИЕ", "ПРИЙНЯТТЯ")) or tt.is_value("ДЕЙСТВИЕ", "ДІЮ") or tt.morph.class0_.is_preposition): 
                            continue
                        if (isinstance(tt, TextToken) and not tt.chars.is_letter): 
                            continue
                        da = (tt.get_referent() if isinstance(tt.get_referent(), DateReferent) else None)
                        if (da is not None): 
                            frdt = FragToken._new1236(t, tt, InstrumentKind.DATE)
                            title.children.append(frdt)
                            t = tt
                            ok = True
                            if (doc.date is None): 
                                doc._add_date(da)
                        break
                    if (ok): 
                        continue
                r = t.get_referent()
                if ((isinstance(r, AddressReferent) or isinstance(r, UriReferent) or isinstance(r, PhoneReferent)) or isinstance(r, PersonIdentityReferent) or isinstance(r, BankDataReferent)): 
                    cnt = FragToken._new1236(t, t, InstrumentKind.CONTACT)
                    cnt.referents = list()
                    cnt.referents.append(r)
                    title.children.append(cnt)
                    while t is not None: 
                        if (t.next0_ is not None and t.next0_.is_char_of(",;.")): 
                            t = t.next0_
                        if (t.next0_ is None): 
                            break
                        r = t.next0_.get_referent()
                        if ((isinstance(r, AddressReferent) or isinstance(r, UriReferent) or isinstance(r, PhoneReferent)) or isinstance(r, PersonIdentityReferent) or isinstance(r, BankDataReferent)): 
                            cnt.referents.append(r)
                            cnt.end_token = t.next0_
                        elif (t.is_newline_after): 
                            break
                        t = t.next0_
                    continue
                pt = (PartToken.try_attach(t, None, False, False) if t.is_newline_before else None)
                if ((pt is not None and ((pt.typ == PartToken.ItemType.PART or pt.typ == PartToken.ItemType.DOCPART)) and len(pt.values) == 1) and pt.is_newline_after): 
                    ok = False
                    if (dt0 is not None and dt0.typ == DecreeToken.ItemType.TYP): 
                        ok = True
                    else: 
                        ddd = DecreeToken.try_attach(pt.end_token.next0_, None, False)
                        if (ddd is not None and ddd.typ == DecreeToken.ItemType.TYP): 
                            ok = True
                        elif (FragToken.__create_approved(pt.end_token.next0_) is not None): 
                            ok = True
                    if (ok): 
                        title.children.append(FragToken._new1284(pt.begin_token, pt.end_token, InstrumentKind.DOCPART, pt.values[0].value))
                        doc.add_slot(InstrumentReferent.ATTR_PART, pt.values[0].value, False, 0)
                        t = pt.end_token
                        continue
                if (appr0 is not None): 
                    break
                if (can_be_orgs): 
                    if (isinstance(t.get_referent(), PersonReferent)): 
                        pass
                    else: 
                        org0_ = FragToken.__create_owner(t)
                        if (org0_ is not None): 
                            unknown_orgs.append(org0_)
                            t = org0_.end_token
                            t1 = t
                            continue
                stok = InstrToken.parse(t, 0, None)
                if (stok is not None and stok.no_words): 
                    if (t0 == t): 
                        t0 = stok.end_token.next0_
                    t = stok.end_token
                    continue
                if ((t.is_newline_before and doc.typ is not None and isinstance(t, TextToken)) and NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0) is not None): 
                    break
                if (t.is_newline_before and t.is_value("К", "ДО")): 
                    break
                if (((not ignore_empty_lines and stok is not None and stok.typ == ILTypes.UNDEFINED) and not stok.has_verb and ((dt0 is None or dt0.typ == DecreeToken.ItemType.NUMBER))) and (empty_lines < 3)): 
                    if (stok.is_newline_after): 
                        empty_lines += 1
                    elif (dt0 is not None): 
                        break
                    end_empty_lines = stok.end_token
                    t = end_empty_lines
                    continue
                break
            if ((not ignore_empty_lines and dt.typ == DecreeToken.ItemType.TERR and end_empty_lines is not None) and dt0 is None): 
                if (dt.is_newline_after): 
                    empty_lines += 1
                end_empty_lines = dt.end_token
                t = end_empty_lines
                continue
            if (dt.typ == DecreeToken.ItemType.ORG or dt.typ == DecreeToken.ItemType.OWNER): 
                if (is_contract): 
                    break
                ttt = dt.end_token.next0_
                while ttt is not None: 
                    if (ttt.whitespaces_before_count > 15): 
                        break
                    if (ttt.get_morph_class_in_dictionary() == MorphClass.VERB): 
                        dt = None
                        break
                    dt1 = DecreeToken.try_attach(ttt, dt0, False)
                    if (dt1 is not None): 
                        if ((dt1.typ == DecreeToken.ItemType.NUMBER or dt1.typ == DecreeToken.ItemType.TYP or dt1.typ == DecreeToken.ItemType.NAME) or dt1.typ == DecreeToken.ItemType.DATE or dt1.typ == DecreeToken.ItemType.ORG): 
                            break
                        dt.end_token = dt1.end_token
                    elif (ttt.chars != dt.begin_token.chars and ttt.is_newline_before): 
                        break
                    else: 
                        dt.end_token = ttt
                    ttt = ttt.next0_
                if (dt is None): 
                    break
            if (dt.typ == DecreeToken.ItemType.TYP): 
                typ = DecreeToken.get_kind(dt.value)
                if (typ == DecreeKind.PUBLISHER): 
                    while t is not None: 
                        if (t.is_newline_after): 
                            break
                        t = t.next0_
                    if (t is None): 
                        break
                    continue
                if (typ == DecreeKind.CONTRACT or dt.value == "ДОВЕРЕННОСТЬ" or dt.value == "ДОВІРЕНІСТЬ"): 
                    is_contract = True
                elif (dt.value == "ПРОТОКОЛ" and not dt.is_newline_after): 
                    npt1 = NounPhraseHelper.try_parse(dt.end_token.next0_, NounPhraseParseAttr.NO, 0)
                    if (npt1 is not None): 
                        t = dt.end_token.next0_
                        while t is not None: 
                            dt.end_token = t
                            if (t.is_newline_after): 
                                break
                            t = t.next0_
                can_be_orgs = False
            dt0 = dt
            if (dt.typ == DecreeToken.ItemType.NUMBER and len(unknown_orgs) > 0): 
                for org0_ in unknown_orgs: 
                    title.children.append(org0_)
                    doc.add_slot(InstrumentReferent.ATTR_SOURCE, org0_.value, False, 0)
                unknown_orgs.clear()
            if (not FragToken.__add_title_attr(doc, title, dt)): 
                break
            else: 
                attrs += 1
            t = dt.end_token
            t1 = t
        title.sort_children()
        if (t is None or (((doc.typ is None and doc.reg_number is None and appr0 is None) and not start_of_name))): 
            if (t == t0): 
                nam = DecreeToken.try_attach_name(t0, None, True, False)
                if (nam is not None): 
                    name_ = FragToken._get_restored_name(t0, nam.end_token, False)
                    if (not Utils.isNullOrEmpty(name_)): 
                        t1 = nam.end_token
                        doc.add_slot(InstrumentReferent.ATTR_NAME, name_.strip(), True, 0)
                        title.children.append(FragToken._new1284(t0, t1, InstrumentKind.NAME, name_.strip()))
                        while t1.next0_ is not None: 
                            if (t1.is_table_control_char and not t1.is_char(chr(0x1F))): 
                                pass
                            else: 
                                break
                            t1 = t1.next0_
                        title.end_token = t1
                        t = t1.next0_
                        first_pass2882 = True
                        while True:
                            if first_pass2882: first_pass2882 = False
                            else: t = t.next0_
                            if (not (t is not None)): break
                            if (FragToken.__is_start_of_body(t)): 
                                break
                            if (t.is_table_control_char): 
                                continue
                            appr1 = FragToken.__create_approved(t)
                            if (appr1 is not None): 
                                title.children.append(appr1)
                                title.end_token = appr1.end_token
                                t = title.end_token
                                continue
                            appr1 = FragToken._create_misc(t)
                            if (appr1 is not None): 
                                title.children.append(appr1)
                                title.end_token = appr1.end_token
                                t = title.end_token
                                continue
                            eds = FragToken._create_editions(t)
                            if (eds is not None): 
                                title.children.append(eds)
                                title.end_token = eds.end_token
                                t = title.end_token
                                break
                            dt00 = DecreeToken.try_attach(t, None, False)
                            if (dt00 is not None): 
                                if (dt00.typ == DecreeToken.ItemType.DATE or dt00.typ == DecreeToken.ItemType.TERR): 
                                    FragToken.__add_title_attr(doc, title, dt00)
                                    title.end_token = dt00.end_token
                                    t = title.end_token
                                    continue
                            break
                        return title
            if (attrs > 0): 
                title.end_token = t1
                return title
            return None
        for j in range(len(unknown_orgs)):
            title.children.insert(j, unknown_orgs[j])
            doc.add_slot(InstrumentReferent.ATTR_SOURCE, unknown_orgs[j].value, False, 0)
        if (end_empty_lines is not None and doc.find_slot(InstrumentReferent.ATTR_SOURCE, None, True) is None): 
            val = MiscHelper.get_text_value(t0, end_empty_lines, GetTextAttr.NO)
            doc.add_slot(InstrumentReferent.ATTR_SOURCE, val, False, 0)
            title.children.insert(0, FragToken._new1284(t0, end_empty_lines, InstrumentKind.ORGANIZATION, val))
        is_case = False
        for ch in title.children: 
            if (ch.value is None and ch.kind != InstrumentKind.APPROVED and ch.kind != InstrumentKind.EDITIONS): 
                ch.value = MiscHelper.get_text_value(ch.begin_token, ch.end_token, GetTextAttr.NO)
            if (ch.kind == InstrumentKind.CASENUMBER): 
                is_case = True
        if ((((name_ is not None or t.is_newline_before or ((t.previous is not None and t.previous.is_table_control_char))) or ((not t.is_newline_before and len(title.children) > 0 and title.children[len(title.children) - 1].kind == InstrumentKind.TYP)))) and not is_case): 
            tt0 = t
            first_line = None
            po_delu = False
            if (t.is_value("ПО", None) and t.next0_ is not None and t.next0_.is_value("ДЕЛО", "СПРАВА")): 
                po_delu = True
            while t is not None: 
                if (FragToken.__is_start_of_body(t)): 
                    break
                if ((name_ is not None and t == tt0 and t.is_newline_before) and t.whitespaces_before_count > 15): 
                    break
                if (t.is_newline_before): 
                    pt = PartToken.try_attach(t, None, False, False)
                    if (pt is not None and pt.typ != PartToken.ItemType.PREFIX): 
                        break
                    ltt = InstrToken1.parse(t, False, None, 0, None, False, 0, False)
                    if (ltt is None): 
                        break
                    if (t != tt0 and t.whitespaces_before_count > 15): 
                        if (t.newlines_before_count > 2): 
                            break
                        if (t.newlines_before_count > 1 and not t.chars.is_all_upper): 
                            break
                        if (t.is_value("О", "ПРО") or t.is_value("ОБ", None)): 
                            pass
                        elif (ltt.all_upper): 
                            pass
                        else: 
                            break
                    if (len(ltt.numbers) > 0): 
                        break
                    appr = FragToken.__create_approved(t)
                    if (appr is not None): 
                        if (t.previous is not None and t.previous.is_char(',')): 
                            pass
                        else: 
                            break
                    if (FragToken._create_editions(t) is not None or FragToken.__create_case_info(t) is not None): 
                        break
                    if (isinstance(t.get_referent(), GeoReferent)): 
                        if (t.is_newline_after): 
                            break
                        if (t.next0_ is not None and isinstance(t.next0_.get_referent(), DateReferent)): 
                            break
                    if (isinstance(t.get_referent(), DateReferent)): 
                        if (t.is_newline_after): 
                            break
                        if (t.next0_ is not None and isinstance(t.next0_.get_referent(), GeoReferent)): 
                            break
                    if (isinstance(t.get_referent(), DecreePartReferent)): 
                        break
                    if (isinstance(t.get_referent(), DecreeReferent)): 
                        dr = (t.get_referent() if isinstance(t.get_referent(), DecreeReferent) else None)
                        if (dr.kind == DecreeKind.PUBLISHER): 
                            break
                    if (t.is_char('(')): 
                        if (FragToken._create_editions(t) is not None): 
                            break
                        br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                        if (br is not None and not br.is_newline_after): 
                            pass
                        else: 
                            break
                    if (ltt.has_verb and not ltt.all_upper): 
                        if (t.is_value("О", "ПРО") and tt0 == t): 
                            pass
                        elif (not po_delu): 
                            break
                    if (ltt.typ == InstrToken1.Types.DIRECTIVE): 
                        break
                    str0_ = str(ltt)
                    if ("В СОСТАВЕ" in str0_ or "В СКЛАДІ" in str0_ or "У СКЛАДІ" in str0_): 
                        break
                    if (t.is_value("В", None) and t.next0_ is not None and t.next0_.is_value("ЦЕЛЬ", "МЕТА")): 
                        break
                    if (first_line is None): 
                        first_line = ltt
                    elif (first_line.all_upper and not ltt.all_upper and not BracketHelper.can_be_start_of_sequence(t, False, False)): 
                        break
                    t = ltt.end_token
                    t1 = t
                else: 
                    t1 = t
                t = t.next0_
            tt1 = DecreeToken._try_attach_std_change_name(tt0)
            if (tt1 is not None): 
                if (t1 is None or (t1.end_char < tt1.end_char)): 
                    t1 = tt1
            val = (FragToken._get_restored_name(tt0, t1, False) if t1 is not None and t1 != tt0 else None)
            if (not Utils.isNullOrEmpty(val) and val[0].isalpha() and val[0].islower()): 
                val = (val[0].upper() + val[1 : ])
            if (name_ is None and len(title.children) > 0 and title.children[len(title.children) - 1].kind == InstrumentKind.TYP): 
                npt = NounPhraseHelper.try_parse(tt0, NounPhraseParseAttr.NO, 0)
                if (npt is not None): 
                    if (npt.morph.case.is_genitive): 
                        name_ = (title.children[len(title.children) - 1].value if isinstance(title.children[len(title.children) - 1].value, str) else None)
                        if (DecreeToken.try_attach(title.children[len(title.children) - 1].begin_token, None, False) is None): 
                            tt0 = title.children[len(title.children) - 1].begin_token
                            del title.children[len(title.children) - 1]
            if (val is None): 
                val = name_
            elif (name_ is not None): 
                val = "{0} {1}".format(name_, val)
            if (val is not None): 
                if (nt0 is not None): 
                    tt0 = nt0
                val = val.strip()
                if (val.startswith("[") and val.endswith("]")): 
                    val = val[1 : 1 + (len(val) - 2)].strip()
                doc.add_slot(InstrumentReferent.ATTR_NAME, val.strip(), True, 0)
                title.children.append(FragToken._new1284(tt0, t1, InstrumentKind.NAME, val.strip()))
                if ("КОДЕКС" in val): 
                    npt = NounPhraseHelper.try_parse(tt0, NounPhraseParseAttr.NO, 0)
                    if (npt is not None and npt.noun.is_value("КОДЕКС", None)): 
                        doc.typ = "КОДЕКС"
        if (t1 is None): 
            return None
        title.end_token = t1
        t1 = t1.next0_
        first_pass2883 = True
        while True:
            if first_pass2883: first_pass2883 = False
            else: t1 = t1.next0_
            if (not (t1 is not None)): break
            if (t1.is_newline_before and t1.is_value("ЧАСТЬ", "ЧАСТИНА")): 
                pt = PartToken.try_attach(t1, None, False, False)
                if (pt is not None and pt.is_newline_after): 
                    pt2 = PartToken.try_attach(pt.end_token.next0_, None, False, False)
                    if (pt2 is not None and (((pt2.typ == PartToken.ItemType.SECTION or pt2.typ == PartToken.ItemType.SUBSECTION or pt2.typ == PartToken.ItemType.CHAPTER) or pt2.typ == PartToken.ItemType.CLAUSE))): 
                        pass
                    else: 
                        doc.add_slot(InstrumentReferent.ATTR_PART, pt.values[0].value, False, 0)
                        title.children.append(FragToken._new1284(t1, pt.end_token, InstrumentKind.DOCPART, pt.values[0].value))
                        title.end_token = pt.end_token
                        t1 = title.end_token
                        continue
            appr1 = FragToken.__create_approved(t1)
            if (appr1 is not None): 
                t1 = appr1.end_token
                title.children.append(appr1)
                title.end_token = appr1.end_token
                continue
            appr1 = FragToken._create_misc(t1)
            if (appr1 is not None): 
                t1 = appr1.end_token
                title.children.append(appr1)
                title.end_token = appr1.end_token
                continue
            cinf = FragToken.__create_case_info(t1)
            if (cinf is not None): 
                t1 = cinf.end_token
                title.children.append(cinf)
                title.end_token = cinf.end_token
                continue
            eds = FragToken._create_editions(t1)
            if (eds is not None): 
                title.children.append(eds)
                t1 = eds.end_token
                title.end_token = t1
                continue
            if (isinstance(t1.get_referent(), DecreeReferent) and (t1.get_referent() if isinstance(t1.get_referent(), DecreeReferent) else None).kind == DecreeKind.PUBLISHER and t1.is_newline_after): 
                pub = FragToken._new1236(t1, t1, InstrumentKind.APPROVED)
                pub.referents = list()
                pub.referents.append(t1.get_referent())
                title.children.append(pub)
                title.end_token = t1
                continue
            tt = t1
            if (tt.next0_ is not None and tt.is_char(',')): 
                tt = tt.next0_
            dt = DecreeToken.try_attach(tt, None, False)
            if (dt is not None and ((dt.typ == DecreeToken.ItemType.DATE or dt.typ == DecreeToken.ItemType.TERR or ((dt.typ == DecreeToken.ItemType.NUMBER and ((dt.is_delo or MiscHelper.check_number_prefix(tt) is not None))))))): 
                if (dt.typ == DecreeToken.ItemType.DATE): 
                    if (doc.date is not None): 
                        break
                    if (not dt.is_newline_after and not MiscHelper.can_be_start_of_sentence(dt.end_token.next0_)): 
                        break
                if (not dt.is_newline_after): 
                    lll = InstrToken1.parse(tt, True, None, 0, None, False, 0, False)
                    if (lll is not None and lll.has_verb): 
                        break
                FragToken.__add_title_attr(doc, title, dt)
                title.end_token = dt.end_token
                t1 = title.end_token
                continue
            if (tt.is_char_of("([") and tt.is_newline_before): 
                br = BracketHelper.try_parse(tt, Utils.valToEnum(BracketParseAttr.CANBEMANYLINES | BracketParseAttr.CANCONTAINSVERBS, BracketParseAttr), 100)
                if (br is not None): 
                    title.end_token = br.end_token
                    t1 = title.end_token
                    title.children.append(FragToken._new1236(br.begin_token, br.end_token, (InstrumentKind.NAME if tt.is_char('[') else InstrumentKind.COMMENT)))
                    continue
            break
        t1 = title.end_token.next0_
        if (t1 is not None and t1.is_newline_before and doc.typ == "КОДЕКС"): 
            pt = PartToken.try_attach(t1, None, False, False)
            if (pt is not None and ((pt.typ == PartToken.ItemType.PART or pt.typ == PartToken.ItemType.DOCPART)) and len(pt.values) > 0): 
                cou = 0
                t = pt.end_token
                while t is not None: 
                    if (t.is_newline_before): 
                        cou += 1
                        if ((cou) > 4): 
                            break
                        eds = FragToken._create_editions(t)
                        if (eds is not None): 
                            title.children.append(eds)
                            t1 = eds.end_token
                            title.end_token = t1
                            title.children.append(FragToken._new1284(pt.begin_token, pt.end_token, InstrumentKind.DOCPART, pt.values[0].value))
                            if (doc.name is not None and "КОДЕКС" in doc.name): 
                                doc.add_slot(InstrumentReferent.ATTR_PART, pt.values[0].value, False, 0)
                            break
                    t = t.next0_
            elif (isinstance(t1.get_referent(), DecreePartReferent)): 
                dr0 = (t1.get_referent() if isinstance(t1.get_referent(), DecreePartReferent) else None)
                if (dr0.part is not None or dr0.doc_part is not None): 
                    cou = 0
                    t = t1.next0_
                    while t is not None: 
                        if (t.is_newline_before): 
                            cou += 1
                            if ((cou) > 4): 
                                break
                            eds = FragToken._create_editions(t)
                            if (eds is not None): 
                                title.children.append(eds)
                                t1 = eds.end_token
                                title.end_token = t1
                                break
                        t = t.next0_
        return title
    
    @staticmethod
    def __create_appendix_title(t0 : 'Token', app : 'FragToken', doc : 'InstrumentReferent', is_app : bool) -> 'FragToken':
        from pullenti.ner.decree.DecreePartReferent import DecreePartReferent
        from pullenti.ner.instrument.internal.InstrToken1 import InstrToken1
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.decree.internal.PartToken import PartToken
        from pullenti.ner.instrument.InstrumentReferent import InstrumentReferent
        from pullenti.ner.decree.DecreeReferent import DecreeReferent
        from pullenti.ner.decree.internal.DecreeToken import DecreeToken
        from pullenti.ner.instrument.internal.InstrToken import InstrToken
        from pullenti.ner.date.DateReferent import DateReferent
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.instrument.InstrumentParticipant import InstrumentParticipant
        from pullenti.ner._org.OrganizationReferent import OrganizationReferent
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.ner.decree.DecreeChangeReferent import DecreeChangeReferent
        from pullenti.ner.geo.GeoReferent import GeoReferent
        if (t0 is None): 
            return None
        if (t0 != t0.kit.first_token): 
            if (isinstance(t0.get_referent(), DecreePartReferent)): 
                if ((t0.get_referent() if isinstance(t0.get_referent(), DecreePartReferent) else None).appendix is not None): 
                    t0 = t0.kit.debed_token(t0)
        t = t0
        t1 = None
        rr = t.get_referent()
        if (rr is not None): 
            if (rr.type_name == "PERSON"): 
                return None
        title = FragToken._new1236(t0, t, InstrumentKind.HEAD)
        first_pass2884 = True
        while True:
            if first_pass2884: first_pass2884 = False
            else: t = t.next0_
            if (not (t is not None)): break
            fr = InstrToken1.parse(t, True, None, 0, None, False, 0, False)
            if (fr is None): 
                break
            if (fr.typ != InstrToken1.Types.APPENDIX and fr.typ != InstrToken1.Types.APPROVED): 
                break
            t2 = t
            if (t.is_value("ОСОБЫЙ", "ОСОБЛИВИЙ") and t.next0_ is not None): 
                t2 = t.next0_
            if (isinstance(t, TextToken)): 
                title.children.append(FragToken._new1254(t, t2, InstrumentKind.KEYWORD, True))
            t = fr.end_token
            title.end_token = t
            if (fr.typ == InstrToken1.Types.APPENDIX and fr.num_begin_token is None): 
                fr1 = InstrToken1.parse(t.next0_, True, None, 0, None, False, 0, False)
                if (fr1 is not None and fr1.typ == InstrToken1.Types.APPROVED): 
                    t = fr1.begin_token
                    title.children.append(FragToken._new1284(t, t, InstrumentKind.KEYWORD, t.get_source_text().upper()))
                    t = fr1.end_token
                    title.end_token = t
                    fr = fr1
            if (fr.num_begin_token is not None and fr.num_end_token is not None): 
                num = FragToken._new1284(fr.num_begin_token, fr.num_end_token, InstrumentKind.NUMBER, MiscHelper.get_text_value(fr.num_begin_token, fr.num_end_token, GetTextAttr.KEEPREGISTER))
                title.children.append(num)
                if (len(fr.numbers) > 0): 
                    app.number = PartToken.get_number(fr.numbers[0])
                if (len(fr.numbers) > 1): 
                    app.sub_number = PartToken.get_number(fr.numbers[1])
                    if (len(fr.numbers) > 2): 
                        app.sub_number2 = PartToken.get_number(fr.numbers[2])
                if (is_app): 
                    doc.add_slot(InstrumentReferent.ATTR_APPENDIX, Utils.ifNotNull(num.value, "1"), False, 0)
            elif (isinstance(t.get_referent(), DecreeReferent)): 
                if ((t.get_referent() if isinstance(t.get_referent(), DecreeReferent) else None).kind == DecreeKind.PUBLISHER): 
                    ff = FragToken._new1236(t, t, InstrumentKind.APPROVED)
                    ff.referents = list()
                    ff.referents.append(t.get_referent())
                    title.children.append(ff)
                elif (fr.typ == InstrToken1.Types.APPROVED and len(title.children) > 0 and title.children[len(title.children) - 1].kind == InstrumentKind.KEYWORD): 
                    kw = title.children[len(title.children) - 1]
                    appr = FragToken._new1236(kw.begin_token, t, InstrumentKind.APPROVED)
                    del title.children[len(title.children) - 1]
                    appr.children.append(kw)
                    appr.children.append(FragToken._new1236(t, t, InstrumentKind.DOCREFERENCE))
                    title.children.append(appr)
                else: 
                    title.children.append(FragToken._new1236(t, t, InstrumentKind.DOCREFERENCE))
            elif (fr.typ == InstrToken1.Types.APPROVED and fr.length_char > 15 and fr.begin_token != fr.end_token): 
                title.children.append(FragToken._new1236(fr.begin_token.next0_, t, InstrumentKind.DOCREFERENCE))
            else: 
                dts = DecreeToken.try_attach_list(t.next0_, None, 10, False)
                if (dts is not None and len(dts) > 0 and dts[0].typ == DecreeToken.ItemType.TYP): 
                    dref = FragToken._new1236(dts[0].begin_token, dts[0].end_token, InstrumentKind.DOCREFERENCE)
                    for i in range(1, len(dts), 1):
                        if (dts[i].typ == DecreeToken.ItemType.TYP): 
                            break
                        elif (dts[i].typ != DecreeToken.ItemType.UNKNOWN): 
                            dref.end_token = dts[i].end_token
                    title.children.append(dref)
                    t = dref.end_token
                    title.end_token = t
            if (fr.typ == InstrToken1.Types.APPENDIX): 
                t = t.next0_
                if (t is not None): 
                    dpr = (t.get_referent() if isinstance(t.get_referent(), DecreePartReferent) else None)
                    if (dpr is not None and dpr.appendix is not None): 
                        t = t.kit.debed_token(t)
                        t = t.previous
                        continue
                    if (t.is_value("ПРИЛОЖЕНИЕ", "ДОДАТОК")): 
                        t = t.previous
                        continue
                break
        if (t is None): 
            return None
        if (t.is_value("К", "ДО")): 
            toks = list()
            tt = t.next0_
            while tt is not None: 
                if (tt != t.next0_ and tt.is_table_control_char): 
                    break
                if (tt.is_newline_before): 
                    if (tt.newlines_before_count > 1): 
                        break
                    it1 = InstrToken1.parse(tt, False, None, 0, None, False, 0, False)
                    if (it1 is not None and len(it1.numbers) > 0): 
                        break
                tok = InstrToken.parse(tt, 0, None)
                if (tok is None): 
                    break
                toks.append(tok)
                if (len(toks) > 20): 
                    break
                if (tt == t.next0_ and tok.typ == ILTypes.UNDEFINED): 
                    ttt = DecreeToken.is_keyword(tt, False)
                    if (ttt is not None): 
                        tok.end_token = ttt
                        tok.typ = ILTypes.TYP
                tt = tok.end_token
                if (tok.typ == ILTypes.TYP and not tt.is_newline_after): 
                    nn = DecreeToken.try_attach_name(tt.next0_, None, False, True)
                    if (nn is not None): 
                        tok.end_token = nn.end_token
                        tt = tok.end_token
                        break
                tt = tt.next0_
            max_ind = -1
            for ii in range(len(toks)):
                tok = toks[ii]
                if (tok.typ == ILTypes.TYP and ((tok.value == doc.typ or ii == 0))): 
                    max_ind = ii
                elif (tok.typ == ILTypes.REGNUMBER and (((tok.value == doc.reg_number or tok.is_newline_before or tok.is_newline_after) or tok.has_table_chars))): 
                    max_ind = ii
                elif (tok.typ == ILTypes.DATE and doc.date is not None): 
                    if (isinstance(tok.ref, DateReferent) and (tok.ref if isinstance(tok.ref, DateReferent) else None).dt == doc.date): 
                        max_ind = ii
                    elif (isinstance(tok.ref, ReferentToken)): 
                        dre = ((tok.ref if isinstance(tok.ref, ReferentToken) else None).referent if isinstance((tok.ref if isinstance(tok.ref, ReferentToken) else None).referent, DateReferent) else None)
                        if (dre is not None and dre.dt is not None and doc.date is not None): 
                            if (dre.dt == doc.date): 
                                max_ind = ii
                elif (tok.typ == ILTypes.DATE and tok.begin_token.previous is not None and tok.begin_token.previous.is_value("ОТ", None)): 
                    max_ind = ii
                elif (tok.typ == ILTypes.UNDEFINED and isinstance(tok.begin_token.get_referent(), DecreeReferent)): 
                    max_ind = ii
                    break
                elif (ii == 0 and tok.typ == ILTypes.UNDEFINED and isinstance(tok.begin_token.get_referent(), DecreePartReferent)): 
                    part = (tok.begin_token.get_referent() if isinstance(tok.begin_token.get_referent(), DecreePartReferent) else None)
                    if (part.appendix is not None): 
                        max_ind = ii
                        break
                elif (tok.typ == ILTypes.ORGANIZATION and ii == 1): 
                    max_ind = ii
                elif (tok.typ == ILTypes.UNDEFINED and ((tok.begin_token.is_value("ОТ", None) or not tok.is_newline_before))): 
                    max_ind = ii
                elif (tok.typ == ILTypes.GEO): 
                    max_ind = ii
            if (len(toks) > 0 and DecreeToken.is_keyword(toks[len(toks) - 1].end_token.next0_, False) is not None): 
                max_ind = (len(toks) - 1)
            te = None
            if (max_ind >= 0): 
                te = toks[max_ind].end_token
                if (not te.is_newline_after): 
                    nn = DecreeToken.try_attach_name(te.next0_, None, False, True)
                    if (nn is not None): 
                        te = nn.end_token
            elif (t.next0_ is not None and isinstance(t.next0_.get_referent(), DecreeReferent)): 
                te = t.next0_
            if (te is not None): 
                dr = FragToken._new1236(t, te, InstrumentKind.DOCREFERENCE)
                title.children.append(dr)
                title.end_token = te
                t = te.next0_
                if ((t) is None): 
                    return title
        for kk in range(10):
            ta = FragToken.__create_approved(t)
            if (ta is not None): 
                title.children.append(ta)
                t = ta.end_token
                title.end_token = t
                t = t.next0_
                if (t is None): 
                    return title
                continue
            ta = FragToken._create_misc(t)
            if (ta is not None): 
                title.children.append(ta)
                t = ta.end_token
                title.end_token = t
                t = t.next0_
                if (t is None): 
                    return title
                continue
            ee = FragToken._create_editions(t)
            if (ee is not None): 
                title.children.append(ee)
                title.end_token = ee.end_token
                t = ee.end_token.next0_
                if (t is None): 
                    return title
                continue
            break
        nt0 = None
        tt0 = t
        first_pass2885 = True
        while True:
            if first_pass2885: first_pass2885 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_table_control_char): 
                if (t == tt0): 
                    if (t.is_char(chr(0x1E))): 
                        rows = TableHelper.try_parse_rows(t, 0, True)
                        if (rows is not None and len(rows) > 2): 
                            break
                        break
                    tt0 = t.next0_
                    continue
                break
            if (t.is_newline_before): 
                if (FragToken.__is_start_of_body(t)): 
                    break
                if (t != tt0 and t.whitespaces_before_count > 15): 
                    if (DecreeToken.is_keyword(t.previous, False) is None): 
                        if (not t.previous.is_value("ОБРАЗЕЦ", "ЗРАЗОК")): 
                            break
                    if (t.whitespaces_before_count > 25): 
                        break
                if (isinstance(t.get_referent(), InstrumentParticipant)): 
                    break
                if (isinstance(t.get_referent(), OrganizationReferent)): 
                    if (t.whitespaces_before_count > 15): 
                        break
                dd = DecreeToken.try_attach(t, None, False)
                if (dd is not None and ((dd.typ == DecreeToken.ItemType.DATE or dd.typ == DecreeToken.ItemType.TERR)) and dd.is_newline_after): 
                    npt0 = None
                    if (dd.typ == DecreeToken.ItemType.TERR and isinstance(t, ReferentToken)): 
                        npt0 = NounPhraseHelper.try_parse((t if isinstance(t, ReferentToken) else None).begin_token, NounPhraseParseAttr.NO, 0)
                    if (npt0 is not None and not npt0.morph.case.is_undefined and not npt0.morph.case.is_nominative): 
                        pass
                    else: 
                        FragToken.__add_title_attr(None, title, dd)
                        title.end_token = dd.end_token
                        t = title.end_token
                        continue
                ltt = InstrToken1.parse(t, True, None, 0, None, False, 0, False)
                if (ltt is None): 
                    break
                if (len(ltt.numbers) > 0): 
                    break
                if (ltt.typ == InstrToken1.Types.APPROVED): 
                    title.children.append(FragToken._new1236(ltt.begin_token, ltt.begin_token, InstrumentKind.APPROVED))
                    if (ltt.begin_token != ltt.end_token): 
                        title.children.append(FragToken._new1236(ltt.begin_token.next0_, ltt.end_token, InstrumentKind.DOCREFERENCE))
                    t = ltt.end_token
                    if (ltt.begin_token == tt0): 
                        tt0 = t.next0_
                        continue
                    break
                if (ltt.has_verb and not ltt.all_upper): 
                    if (t.chars.is_letter and t.chars.is_all_lower): 
                        pass
                    elif (isinstance(t.get_referent(), DecreeChangeReferent)): 
                        dch = (t.get_referent() if isinstance(t.get_referent(), DecreeChangeReferent) else None)
                        if (dch.kind == DecreeChangeKind.CONTAINER and t.is_value("ИЗМЕНЕНИЕ", None)): 
                            pass
                        else: 
                            break
                    else: 
                        break
                if (ltt.typ == InstrToken1.Types.DIRECTIVE): 
                    break
                if (t.chars.is_letter and t != tt0): 
                    if (not t.chars.is_all_lower and not t.chars.is_all_upper): 
                        if (not ((isinstance(t.get_referent(), OrganizationReferent))) and not ((isinstance(t.get_referent(), GeoReferent)))): 
                            if (DecreeToken.is_keyword(t.previous, False) is None): 
                                npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0)
                                if (npt is not None and npt.morph.case.is_genitive): 
                                    pass
                                else: 
                                    break
                has_words = False
                ttt = ltt.begin_token
                while ttt is not None: 
                    if (ttt.begin_char > ltt.end_char): 
                        break
                    if (ttt.chars.is_cyrillic_letter): 
                        has_words = True
                        break
                    r = ttt.get_referent()
                    if (isinstance(r, OrganizationReferent) or isinstance(r, GeoReferent) or isinstance(r, DecreeChangeReferent)): 
                        has_words = True
                        break
                    ttt = ttt.next0_
                if (not has_words): 
                    break
                eds = FragToken._create_editions(t)
                if (eds is not None): 
                    if (t != tt0): 
                        break
                    title.children.append(eds)
                    title.end_token = eds.end_token
                    t = title.end_token
                    t1 = t
                    tt0 = t.next0_
                    continue
                t = ltt.end_token
                t1 = t
            else: 
                t1 = t
        val = (FragToken._get_restored_name(tt0, t1, False) if t1 is not None and tt0 is not None else None)
        if (val is not None): 
            if (nt0 is not None): 
                tt0 = nt0
            title.children.append(FragToken._new1284(tt0, t1, InstrumentKind.NAME, val.strip()))
            title.end_token = t1
            title.name = val
        if (title.end_token.next0_ is not None): 
            eds = FragToken._create_editions(title.end_token.next0_)
            if (eds is not None): 
                title.children.append(eds)
                title.end_token = eds.end_token
        if (is_app): 
            if (doc.find_slot(InstrumentReferent.ATTR_APPENDIX, None, True) is None): 
                doc.add_slot(InstrumentReferent.ATTR_APPENDIX, "", False, 0)
            for ch in title.children: 
                if (ch.kind == InstrumentKind.DOCREFERENCE): 
                    tt = ch.begin_token
                    while tt is not None and tt.end_char <= ch.end_char: 
                        if (isinstance(tt.get_referent(), DecreeReferent)): 
                            for s in tt.get_referent().slots: 
                                if (s.type_name == DecreeReferent.ATTR_TYPE): 
                                    doc.add_slot(InstrumentReferent.ATTR_TYPE, s.value, False, 0)
                                elif (s.type_name == DecreeReferent.ATTR_NUMBER): 
                                    doc.add_slot(InstrumentReferent.ATTR_REGNUMBER, s.value, False, 0)
                                elif (s.type_name == DecreeReferent.ATTR_DATE): 
                                    doc.add_slot(InstrumentReferent.ATTR_DATE, s.value, False, 0)
                                elif (s.type_name == DecreeReferent.ATTR_SOURCE): 
                                    doc.add_slot(InstrumentReferent.ATTR_SOURCE, s.value, False, 0)
                                elif (s.type_name == DecreeReferent.ATTR_GEO): 
                                    doc.add_slot(InstrumentReferent.ATTR_GEO, s.value, False, 0)
                            break
                        dt = DecreeToken.try_attach(tt, None, False)
                        if (dt is not None): 
                            if (FragToken.__add_title_attr(doc, None, dt)): 
                                tt = dt.end_token
                        tt = tt.next0_
                    break
        if (len(title.children) == 0 and title.end_token == title.begin_token): 
            return None
        t1 = title.end_token.next0_
        first_pass2886 = True
        while True:
            if first_pass2886: first_pass2886 = False
            else: t1 = t1.next0_
            if (not (t1 is not None)): break
            dt = DecreeToken.try_attach(t1, None, False)
            if (dt is not None): 
                if (dt.typ == DecreeToken.ItemType.DATE or dt.typ == DecreeToken.ItemType.TERR): 
                    FragToken.__add_title_attr(None, title, dt)
                    title.end_token = dt.end_token
                    t1 = title.end_token
                    continue
            break
        return title
    
    @staticmethod
    def __is_start_of_body(t : 'Token') -> bool:
        from pullenti.ner.core.internal.BlockTitleToken import BlockTitleToken
        from pullenti.ner.instrument.internal.InstrToken1 import InstrToken1
        from pullenti.ner._org.OrganizationReferent import OrganizationReferent
        if (t is None or not t.is_newline_before): 
            return False
        bl = BlockTitleToken.try_attach(t, False, None)
        if (bl is not None): 
            if (bl.typ != BlkTyps.UNDEFINED and bl.typ != BlkTyps.LITERATURE): 
                return True
        ok = False
        if (t.is_value("ВВЕДЕНИЕ", "ВВЕДЕННЯ") or t.is_value("АННОТАЦИЯ", "АНОТАЦІЯ") or t.is_value("ПРЕДИСЛОВИЕ", "ПЕРЕДМОВА")): 
            ok = True
        elif (t.is_value("ОБЩИЙ", "ЗАГАЛЬНИЙ") and t.next0_ is not None and t.next0_.is_value("ПОЛОЖЕНИЕ", "ПОЛОЖЕННЯ")): 
            t = t.next0_
            ok = True
        elif ((t.next0_ is not None and t.next0_.chars.is_all_lower and t.morph.class0_.is_preposition) and ((t.next0_.is_value("СВЯЗЬ", "ЗВЯЗОК") or t.next0_.is_value("ЦЕЛЬ", "МЕТА") or t.next0_.is_value("СООТВЕТСТВИЕ", "ВІДПОВІДНІСТЬ")))): 
            return True
        if (ok): 
            t1 = t.next0_
            if (t1 is not None and t1.is_char(':')): 
                t1 = t1.next0_
            if (t1 is None or t1.is_newline_before): 
                return True
            return False
        it = InstrToken1.parse(t, False, None, 0, None, False, 0, False)
        if (it is not None): 
            if (it.typ_container_rank > 0 or it.typ == InstrToken1.Types.DIRECTIVE): 
                if (t.is_value("ЧАСТЬ", "ЧАСТИНА") and len(it.numbers) == 1): 
                    if (FragToken.__create_approved(it.end_token.next0_) is not None): 
                        return False
                return True
            if (len(it.numbers) > 0): 
                if (len(it.numbers) > 1 or it.num_suffix is not None): 
                    return True
        if (isinstance(t.get_referent(), OrganizationReferent) and t.next0_ is not None): 
            if (t.next0_.is_value("СОСТАВ", "СКЛАД")): 
                return True
            if (t.next0_.is_value("В", "У") and t.next0_.next0_ is not None and t.next0_.next0_.is_value("СОСТАВ", "СКЛАД")): 
                return True
        return False
    
    @staticmethod
    def __add_title_attr(doc : 'InstrumentReferent', title : 'FragToken', dt : 'DecreeToken') -> bool:
        from pullenti.ner.decree.internal.DecreeToken import DecreeToken
        from pullenti.ner.instrument.InstrumentBlockReferent import InstrumentBlockReferent
        from pullenti.ner.instrument.InstrumentReferent import InstrumentReferent
        from pullenti.ner.decree.DecreeReferent import DecreeReferent
        from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent
        from pullenti.ner.core.MiscHelper import MiscHelper
        if (dt.typ == DecreeToken.ItemType.TYP): 
            if (doc is not None): 
                if (doc.typ is not None and dt.value != doc.typ): 
                    if (doc.typ != "ПРОЕКТ"): 
                        return False
                    if ("ЗАКОН" in dt.value): 
                        doc.typ = "ПРОЕКТ ЗАКОНА"
                    else: 
                        return False
                else: 
                    doc.typ = dt.value
                if (dt.full_value is not None and dt.full_value != dt.value and doc.name is None): 
                    doc.name = dt.full_value
            if (title is not None): 
                title.children.append(FragToken._new1284(dt.begin_token, dt.end_token, InstrumentKind.TYP, Utils.ifNotNull(dt.full_value, dt.value)))
        elif (dt.typ == DecreeToken.ItemType.NUMBER): 
            if (dt.is_delo): 
                if (doc is not None): 
                    doc.add_slot(InstrumentReferent.ATTR_CASENUMBER, dt.value, False, 0)
                    if (doc.reg_number == dt.value): 
                        doc.reg_number = None
                if (title is not None): 
                    title.children.append(FragToken._new1284(dt.begin_token, dt.end_token, InstrumentKind.CASENUMBER, dt.value))
            else: 
                if (dt.value != "?" and doc is not None): 
                    if (doc.get_string_value(InstrumentReferent.ATTR_CASENUMBER) == dt.value): 
                        pass
                    else: 
                        doc.add_slot(InstrumentBlockReferent.ATTR_NUMBER, dt.value, False, 0)
                if (title is not None): 
                    title.children.append(FragToken._new1284(dt.begin_token, dt.end_token, InstrumentKind.NUMBER, dt.value))
                if (doc is not None and doc.typ is None and dt.value is not None): 
                    if (LanguageHelper.ends_with(dt.value, "ФКЗ")): 
                        doc.typ = "ФЕДЕРАЛЬНЫЙ КОНСТИТУЦИОННЫЙ ЗАКОН"
                    elif (LanguageHelper.ends_with(dt.value, "ФЗ")): 
                        doc.typ = "ФЕДЕРАЛЬНЫЙ ЗАКОН"
        elif (dt.typ == DecreeToken.ItemType.NAME): 
            if (doc is not None): 
                doc.add_slot(InstrumentBlockReferent.ATTR_NAME, dt.value, False, 0)
            if (title is not None): 
                title.children.append(FragToken._new1284(dt.begin_token, dt.end_token, InstrumentKind.NAME, dt.value))
        elif (dt.typ == DecreeToken.ItemType.DATE): 
            if (doc is None or doc._add_date(dt)): 
                if (title is not None): 
                    title.children.append(FragToken._new1284(dt.begin_token, dt.end_token, InstrumentKind.DATE, dt))
        elif (dt.typ == DecreeToken.ItemType.TERR): 
            if (title is not None): 
                title.children.append(FragToken._new1284(dt.begin_token, dt.end_token, InstrumentKind.PLACE, dt))
            if (doc is not None and dt.ref is not None): 
                geo_ = doc.get_string_value(InstrumentReferent.ATTR_GEO)
                if (geo_ == "Россия"): 
                    doc.add_slot(InstrumentReferent.ATTR_GEO, None, True, 0)
                    geo_ = None
                if (geo_ is None): 
                    doc.add_slot(InstrumentReferent.ATTR_GEO, str(dt.ref.referent), False, 0)
        elif (dt.typ == DecreeToken.ItemType.OWNER or dt.typ == DecreeToken.ItemType.ORG): 
            if (title is not None): 
                title.children.append(FragToken._new1284(dt.begin_token, dt.end_token, (InstrumentKind.ORGANIZATION if dt.typ == DecreeToken.ItemType.ORG else InstrumentKind.INITIATOR), dt))
            if (doc is not None): 
                if (dt.ref is not None): 
                    doc.add_slot(DecreeReferent.ATTR_SOURCE, dt.ref.referent, False, 0).tag = dt.get_source_text()
                    if (isinstance(dt.ref.referent, PersonPropertyReferent)): 
                        doc.add_ext_referent(dt.ref)
                else: 
                    doc.add_slot(DecreeReferent.ATTR_SOURCE, MiscHelper.convert_first_char_upper_and_other_lower(dt.value), False, 0).tag = dt.get_source_text()
        else: 
            return False
        return True
    
    def _analize_tables(self) -> bool:
        if (len(self.children) > 0): 
            abz_count = 0
            cou = 0
            for ch in self.children: 
                if (ch.kind == InstrumentKind.INDENTION): 
                    abz_count += 1
                if (ch.kind != InstrumentKind.KEYWORD and ch.kind != InstrumentKind.NUMBER and ch.kind != InstrumentKind.NUMBER): 
                    cou += 1
            if (abz_count == cou and cou > 0): 
                chs = self.children
                self.children = list()
                bb = self._analize_tables()
                self.children = chs
                if (bb): 
                    i = 0
                    while i < len(self.children): 
                        if (self.children[i].kind == InstrumentKind.INDENTION): 
                            ch0 = (self.children[i - 1] if i > 0 else None)
                            if (ch0 is not None and ch0.kind == InstrumentKind.CONTENT): 
                                ch0.end_token = self.children[i].end_token
                                del self.children[i]
                                i -= 1
                            else: 
                                self.children[i].kind = InstrumentKind.CONTENT
                        i += 1
            changed = list()
            for ch in self.children: 
                if (ch._analize_tables()): 
                    changed.append(ch)
            for i in range(len(changed) - 1, -1, -1):
                if (changed[i].kind == InstrumentKind.CONTENT): 
                    j = Utils.indexOfList(self.children, changed[i], 0)
                    if (j < 0): 
                        continue
                    del self.children[j]
                    self.children[j:j] = changed[i].children
            return False
        if (((self.kind == InstrumentKind.CHAPTER or self.kind == InstrumentKind.CLAUSE or self.kind == InstrumentKind.CONTENT) or self.kind == InstrumentKind.ITEM or self.kind == InstrumentKind.SUBITEM) or self.kind == InstrumentKind.INDENTION): 
            pass
        else: 
            return False
        if (self._itok is not None and self._itok.has_changes): 
            return False
        end_char_ = self.end_char
        if (self.end_token.next0_ is None): 
            end_char_ = (len(self.kit.sofa.text) - 1)
        t0 = self.begin_token
        tabs = False
        tt = self.begin_token
        first_pass2887 = True
        while True:
            if first_pass2887: first_pass2887 = False
            else: tt = tt.next0_
            if (not (tt is not None and tt.end_char <= end_char_)): break
            if (not tt.is_newline_before): 
                continue
            if (tt.is_char(chr(0x1E))): 
                pass
            rows = TableHelper.try_parse_rows(tt, end_char_, False)
            if (rows is None or (len(rows) < 2)): 
                continue
            ok = True
            for r in rows: 
                if (len(r.cells) > 15): 
                    ok = False
            if (not ok): 
                tt = rows[len(rows) - 1].end_token
                continue
            if (t0.end_char < rows[0].begin_char): 
                self.children.append(FragToken._new1236(t0, rows[0].begin_token.previous, InstrumentKind.CONTENT))
            tab = FragToken._new1236(rows[0].begin_token, rows[len(rows) - 1].end_token, InstrumentKind.TABLE)
            self.children.append(tab)
            for i in range(len(rows)):
                rr = FragToken._new1252(rows[i].begin_token, rows[i].end_token, InstrumentKind.TABLEROW, i + 1)
                tab.children.append(rr)
                tabs = True
                no = 0
                cols = 0
                for ce in rows[i].cells: 
                    cell = FragToken._new1252(ce.begin_token, ce.end_token, InstrumentKind.TABLECELL, ++ no)
                    if (ce.col_span > 1): 
                        cell.sub_number = ce.col_span
                        cols += (cell.sub_number)
                    else: 
                        cols += 1
                    if (ce.row_span > 1): 
                        cell.sub_number2 = ce.row_span
                    rr.children.append(cell)
                if (tab.number < cols): 
                    tab.number = cols
                tt = rows[i].end_token
            if (tab.number > 1): 
                rnums = Utils.newArray(tab.number, 0)
                rnums_cols = Utils.newArray(tab.number, 0)
                for r in tab.children: 
                    no = 0
                    ii = 0
                    first_pass2888 = True
                    while True:
                        if first_pass2888: first_pass2888 = False
                        else: ii += 1
                        if (not (ii < len(r.children))): break
                        if ((no < len(rnums)) and rnums[no] > 0): 
                            rnums[no] -= 1
                            no += rnums_cols[no]
                            ii -= 1
                            continue
                        r.children[ii].number = (no + 1)
                        if (r.children[ii].sub_number2 > 1 and (no < len(rnums))): 
                            rnums[no] = (r.children[ii].sub_number2 - 1)
                            rnums_cols[no] = (1 if r.children[ii].sub_number == 0 else r.children[ii].sub_number)
                        no += (1 if r.children[ii].sub_number == 0 else r.children[ii].sub_number)
            t0 = tt.next0_
        if ((t0 is not None and (t0.end_char < self.end_char) and tabs) and t0 != self.end_token): 
            self.children.append(FragToken._new1236(t0, self.end_token, InstrumentKind.CONTENT))
        return tabs
    
    @staticmethod
    def __create_zapiska_title(t0 : 'Token', doc : 'InstrumentReferent') -> 'FragToken':
        from pullenti.ner.instrument.internal.InstrToken1 import InstrToken1
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        cou = 0
        t = t0
        while t is not None and (cou < 30): 
            li = InstrToken1.parse(t, True, None, 0, None, False, 0, False)
            if (li is None): 
                break
            if (len(li.numbers) > 0): 
                break
            ok = False
            npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0)
            if (npt is not None and npt.end_token == li.end_token): 
                for kv in FragToken.__m_zapiska_keywords: 
                    if (npt.end_token.is_value(kv, None)): 
                        ok = True
                        break
            if (t.is_value("ОТВЕТ", None)): 
                if (t.is_newline_after): 
                    ok = True
                elif (t.next0_ is not None and t.next0_.is_value("НА", None)): 
                    ok = True
            if (ok): 
                res = FragToken._new1236(t0, li.end_token, InstrumentKind.HEAD)
                if (li.begin_token != t0): 
                    hh = FragToken._new1236(t0, li.begin_token.previous, InstrumentKind.APPROVED)
                    res.children.append(hh)
                res.children.append(FragToken._new1257(li.begin_token, li.end_token, InstrumentKind.KEYWORD, True))
                return res
            t = li.end_token
            t = t.next0_; cou += 1
        return None
    
    __m_zapiska_keywords = None
    
    @staticmethod
    def __create_contract_title(t0 : 'Token', doc : 'InstrumentReferent') -> 'FragToken':
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.decree.internal.DecreeToken import DecreeToken
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent
        from pullenti.ner.person.PersonReferent import PersonReferent
        from pullenti.ner._org.OrganizationReferent import OrganizationReferent
        from pullenti.ner.instrument.internal.ParticipantToken import ParticipantToken
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.instrument.InstrumentParticipant import InstrumentParticipant
        from pullenti.ner.instrument.InstrumentReferent import InstrumentReferent
        from pullenti.ner.decree.DecreeReferent import DecreeReferent
        from pullenti.ner.instrument.internal.InstrToken1 import InstrToken1
        from pullenti.ner.geo.GeoReferent import GeoReferent
        from pullenti.ner.date.DateReferent import DateReferent
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.morph.Morphology import Morphology
        from pullenti.morph.MorphLang import MorphLang
        from pullenti.ner.instrument.InstrumentAnalyzer import InstrumentAnalyzer
        from pullenti.ner.NumberToken import NumberToken
        if (t0 is None): 
            return None
        is_contract = False
        while isinstance(t0, TextToken) and t0.next0_ is not None:
            if (t0.is_table_control_char or not t0.chars.is_letter): 
                t0 = t0.next0_
            else: 
                break
        dt0 = DecreeToken.try_attach(t0, None, False)
        if (dt0 is not None and dt0.typ == DecreeToken.ItemType.TYP): 
            is_contract = (("ДОГОВОР" in dt0.value or "ДОГОВІР" in dt0.value or "КОНТРАКТ" in dt0.value) or "СОГЛАШЕНИЕ" in dt0.value or "УГОДА" in dt0.value)
        cou = 0
        par1 = None
        t = t0
        while t is not None: 
            if (isinstance(t, ReferentToken)): 
                rtt = (t if isinstance(t, ReferentToken) else None)
                if (rtt.begin_token == rtt.end_token): 
                    r = t.get_referent()
                    if (isinstance(r, PersonPropertyReferent)): 
                        str0_ = str(r)
                        if ("директор" in str0_ or "начальник" in str0_): 
                            pass
                        else: 
                            t = t.kit.debed_token(t)
                    elif (isinstance(r, PersonReferent) and isinstance(rtt.begin_token.get_referent(), PersonPropertyReferent)): 
                        str0_ = str(rtt.begin_token.get_referent())
                        if ("директор" in str0_ or "начальник" in str0_): 
                            pass
                        else: 
                            t = t.kit.debed_token(t)
                            t = t.kit.debed_token(t)
            t = t.next0_
        t = t0
        first_pass2889 = True
        while True:
            if first_pass2889: first_pass2889 = False
            else: t = t.next0_; cou += 1
            if (not (t is not None and (cou < 300))): break
            if (t.is_char('_')): 
                cou -= 1
                continue
            if (t.is_newline_before): 
                while t.is_table_control_char and t.next0_ is not None:
                    t = t.next0_
                dt = DecreeToken.try_attach(t, None, False)
                if (dt is not None and dt.typ == DecreeToken.ItemType.TYP): 
                    if (((((dt.value == "ОПРЕДЕЛЕНИЕ" or dt.value == "ПОСТАНОВЛЕНИЕ" or dt.value == "РЕШЕНИЕ") or dt.value == "ПРИГОВОР" or dt.value == "ВИЗНАЧЕННЯ") or dt.value == "ПОСТАНОВА" or dt.value == "РІШЕННЯ") or dt.value == "ВИРОК" or dt.value.endswith("ЗАЯВЛЕНИЕ")) or dt.value.endswith("ЗАЯВА")): 
                        return None
                if (isinstance(t.get_referent(), OrganizationReferent)): 
                    ki = (t.get_referent() if isinstance(t.get_referent(), OrganizationReferent) else None).kind
                    if (ki == OrganizationKind.JUSTICE): 
                        return None
            if (t.is_value("ДАЛЕЕ", None)): 
                pass
            if (t.is_newline_after): 
                continue
            par1 = ParticipantToken.try_attach(t, None, None, is_contract)
            if (par1 is not None and ((par1.kind == ParticipantToken.Kinds.NAMEDAS or par1.kind == ParticipantToken.Kinds.NAMEDASPARTS))): 
                t = par1.end_token.next0_
                break
            par1 = None
        if (par1 is None): 
            return None
        par2 = None
        cou = 0
        first_pass2890 = True
        while True:
            if first_pass2890: first_pass2890 = False
            else: t = t.next0_; cou += 1
            if (not (t is not None and (cou < 100))): break
            if (par1.kind == ParticipantToken.Kinds.NAMEDASPARTS): 
                break
            if (t.is_char('_')): 
                cou -= 1
                continue
            if (t.is_char('(')): 
                br2 = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                if (br2 is not None): 
                    t = br2.end_token
                    continue
            par2 = ParticipantToken.try_attach(t, None, None, True)
            if (par2 is not None): 
                if (par2.kind == ParticipantToken.Kinds.NAMEDAS and par2.typ != par1.typ): 
                    break
                if (par2.kind == ParticipantToken.Kinds.PURE and par2.typ != par1.typ): 
                    if (t.previous.is_and): 
                        break
                t = par2.end_token
            par2 = None
        if (par1 is not None and par2 is not None and ((par1.typ is None or par2.typ is None))): 
            stat = dict()
            tt = t
            first_pass2891 = True
            while True:
                if first_pass2891: first_pass2891 = False
                else: tt = tt.next0_
                if (not (tt is not None)): break
                ttt = tt
                if (isinstance(tt, MetaToken)): 
                    ttt = (tt if isinstance(tt, MetaToken) else None).begin_token
                tok = ParticipantToken._m_ontology.try_parse(ttt, TerminParseAttr.NO)
                if (tok is None or tok.termin.tag is None): 
                    continue
                key = tok.termin.canonic_text
                if (key == par1.typ or key == par2.typ or key == "СТОРОНА"): 
                    continue
                if (not key in stat): 
                    stat[key] = 1
                else: 
                    stat[key] += 1
            max0_ = 0
            best_typ = None
            for kp in stat.items(): 
                if (kp[1] > max0_): 
                    max0_ = kp[1]
                    best_typ = kp[0]
            if (best_typ is not None): 
                if (par1.typ is None): 
                    par1.typ = best_typ
                elif (par2.typ is None): 
                    par2.typ = best_typ
        contr_typs = ParticipantToken.get_doc_types(par1.typ, (None if par2 is None else par2.typ))
        t1 = par1.begin_token.previous
        lastt1 = None
        first_pass2892 = True
        while True:
            if first_pass2892: first_pass2892 = False
            else: t1 = t1.previous
            if (not (t1 is not None and t1.begin_char >= t0.begin_char)): break
            if (t1.is_newline_after): 
                lastt1 = t1
                if (t1.is_char(',')): 
                    continue
                if (t1.next0_ is None): 
                    break
                if (t1.next0_.chars.is_letter and t1.next0_.chars.is_all_lower): 
                    continue
                break
        if (t1 is None): 
            t1 = lastt1
        if (t1 is None): 
            return None
        p1 = InstrumentParticipant._new1337(par1.typ)
        if (par1.parts is not None): 
            for p in par1.parts: 
                p1.add_slot(InstrumentParticipant.ATTR_REF, p, False, 0)
        p2 = None
        all_parts = list()
        all_parts.append(p1)
        if (par1.kind == ParticipantToken.Kinds.NAMEDASPARTS): 
            p1.typ = "СТОРОНА 1"
            p1.add_slot(InstrumentParticipant.ATTR_REF, par1.parts[0], False, 0)
            for ii in range(1, len(par1.parts), 1):
                pp = InstrumentParticipant._new1337("СТОРОНА {0}".format(ii + 1))
                pp.add_slot(InstrumentParticipant.ATTR_REF, par1.parts[ii], False, 0)
                if (ii == 1): 
                    p2 = pp
                all_parts.append(pp)
            for pp in par1.parts: 
                doc.add_slot(InstrumentReferent.ATTR_SOURCE, pp, False, 0)
        title = FragToken._new1236(t0, t0, InstrumentKind.HEAD)
        add = False
        nam_beg = None
        nam_end = None
        dttyp = None
        dt00 = None
        t = t0
        first_pass2893 = True
        while True:
            if first_pass2893: first_pass2893 = False
            else: t = t.next0_
            if (not (t is not None and t.end_char <= t1.end_char)): break
            if (isinstance(t.get_referent(), DecreeReferent)): 
                if (t.is_newline_before or ((t.previous is not None and t.previous.is_table_control_char))): 
                    t = t.kit.debed_token(t)
            new_line_bef = t.is_newline_before
            if (t.previous is not None and t.previous.is_table_control_char): 
                new_line_bef = True
            dt = DecreeToken.try_attach(t, dt00, False)
            if (dt is not None): 
                dt00 = dt
                if ((dt.typ == DecreeToken.ItemType.DATE or dt.typ == DecreeToken.ItemType.NUMBER or ((dt.typ == DecreeToken.ItemType.TYP and new_line_bef))) or ((dt.typ == DecreeToken.ItemType.TERR and new_line_bef))): 
                    if (nam_beg is not None and nam_end is None): 
                        nam_end = t.previous
                    if (((dt.typ == DecreeToken.ItemType.TYP and doc.typ is not None and not "ДОГОВОР" in doc.typ) and not "ДОГОВІР" in doc.typ and not is_contract) and dt.value is not None and (("ДОГОВОР" in dt.value or "ДОГОВІР" in dt.value))): 
                        doc.typ = None
                        doc.number = 0
                        doc.reg_number = None
                        is_contract = True
                        nam_end = None
                        nam_beg = nam_end
                        title.children.clear()
                    FragToken.__add_title_attr(doc, title, dt)
                    t = dt.end_token
                    title.end_token = t
                    if (dt.typ == DecreeToken.ItemType.TYP): 
                        dttyp = dt.value
                    add = True
                    continue
            dt00 = None
            if (new_line_bef and t != t0): 
                edss = FragToken._create_editions(t)
                if (edss is not None): 
                    if (nam_beg is not None and nam_end is None): 
                        nam_end = t.previous
                    title.children.append(edss)
                    title.end_token = edss.end_token
                    break
                it1 = InstrToken1.parse(t, True, None, 0, None, False, 0, False)
                if (it1 is not None and len(it1.numbers) > 0 and it1.num_typ == NumberTypes.DIGIT): 
                    title.end_token = t.previous
                    if (nam_beg is not None and nam_end is None): 
                        nam_end = t.previous
                    break
                if (nam_beg is None and ((t.is_value("О", "ПРО") or t.is_value("ОБ", None) or t.is_value("НА", None)))): 
                    nam_beg = t
                    continue
                if (add): 
                    title.end_token = t.previous
                add = False
                r = t.get_referent()
                if (isinstance(r, GeoReferent) or isinstance(r, DateReferent) or isinstance(r, DecreeReferent)): 
                    if (nam_beg is not None and nam_end is None): 
                        nam_end = t.previous
            if ((dttyp is not None and nam_beg is None and t.chars.is_cyrillic_letter) and isinstance(t, TextToken)): 
                if (t.is_value("МЕЖДУ", "МІЖ")): 
                    pp = ParticipantToken.try_attach_to_exist(t.next0_, p1, p2)
                    if (pp is not None and pp.end_token.next0_ is not None and pp.end_token.next0_.is_and): 
                        pp2 = ParticipantToken.try_attach_to_exist(pp.end_token.next0_.next0_, p1, p2)
                        if (pp2 is not None): 
                            fr = FragToken._new1236(t, pp2.end_token, InstrumentKind.PLACE)
                            if (fr.referents is None): 
                                fr.referents = list()
                            fr.referents.append(pp.referent)
                            fr.referents.append(pp2.referent)
                            title.children.append(fr)
                            title.end_token = fr.end_token
                            t = title.end_token
                            if (t.next0_ is not None): 
                                if (t.next0_.is_value("О", "ПРО") or t.next0_.is_value("ОБ", None)): 
                                    nam_beg = t.next0_
                                    nam_end = None
                            continue
                nam_beg = t
            elif (((t.is_value("МЕЖДУ", "МІЖ") or t.is_value("ЗАКЛЮЧИТЬ", "УКЛАСТИ"))) and nam_beg is not None and nam_end is None): 
                nam_end = t.previous
            if ((new_line_bef and t.whitespaces_before_count > 15 and nam_beg is not None) and nam_end is None): 
                nam_end = t.previous
        if (nam_beg is not None and nam_end is None and t1 is not None): 
            nam_end = t1
        if (nam_end is not None and nam_beg is not None): 
            val = MiscHelper.get_text_value(nam_beg, nam_end, GetTextAttr.KEEPQUOTES)
            if (val is not None and len(val) > 3): 
                nam = FragToken._new1284(nam_beg, nam_end, InstrumentKind.NAME, val)
                title.children.append(nam)
                title.sort_children()
                if (nam_end.end_char > title.end_char): 
                    title.end_token = nam_end
                val = nam.get_source_text().upper().replace('\r', ' ').replace('\n', ' ')
                while "  " in val:
                    val = val.replace("  ", " ")
                if (dttyp is not None and not dttyp in val): 
                    val = "{0} {1}".format(dttyp, val)
                doc.name = val
        if (len(title.children) > 0 and title.children[0].begin_char > title.begin_char): 
            title.children.insert(0, FragToken._new1236(title.begin_token, title.children[0].begin_token.previous, InstrumentKind.UNDEFINED))
        if (((doc.typ == "ДОГОВОР" or doc.typ == "ДОГОВІР")) and par1.kind != ParticipantToken.Kinds.NAMEDASPARTS): 
            if (len(title.children) > 0 and title.children[0].kind == InstrumentKind.TYP): 
                addi = None
                for ch in title.children: 
                    if (ch.kind == InstrumentKind.NAME): 
                        if (ch.begin_token.morph.class0_.is_preposition): 
                            npt = NounPhraseHelper.try_parse(ch.begin_token.next0_, NounPhraseParseAttr.NO, 0)
                            if (npt is not None): 
                                addi = npt.noun.get_source_text().upper()
                                vvv = Morphology.get_all_wordforms(addi, MorphLang())
                                for fi in vvv: 
                                    if (fi.case.is_genitive): 
                                        addi = fi.normal_case
                                        if (addi.endswith("НЬЯ")): 
                                            addi = (addi[0 : (len(addi) - 2)] + "ИЯ")
                                        break
                        else: 
                            npt = NounPhraseHelper.try_parse(ch.begin_token, NounPhraseParseAttr.NO, 0)
                            if (npt is not None and npt.end_char <= ch.end_char): 
                                addi = npt.noun.get_source_text().upper()
                        break
                if (addi is not None): 
                    if (addi.startswith("ОКАЗАН")): 
                        addi = "УСЛУГ"
                    elif (addi.startswith("НАДАН")): 
                        addi = "ПОСЛУГ"
                    doc.typ = "{0} {1}".format(doc.typ, addi)
                    if (doc.typ == doc.name): 
                        doc.name = None
                elif (len(contr_typs) == 1): 
                    if (doc.typ is None or (len(doc.typ) < len(contr_typs[0]))): 
                        doc.typ = contr_typs[0]
                elif (len(contr_typs) > 0 and doc.typ is None): 
                    doc.typ = contr_typs[0]
        if (doc.typ == "ДОГОВОР УСЛУГ"): 
            doc.typ = "ДОГОВОР ОКАЗАНИЯ УСЛУГ"
        if (doc.typ == "ДОГОВІР ПОСЛУГ"): 
            doc.typ = "ДОГОВІР НАДАННЯ ПОСЛУГ"
        if (doc.typ is None and len(contr_typs) > 0): 
            doc.typ = contr_typs[0]
        ad = t0.kit.get_analyzer_data_by_analyzer_name(InstrumentAnalyzer.ANALYZER_NAME)
        if (ad is None): 
            return None
        doc.add_slot(InstrumentReferent.ATTR_PARTICIPANT, p1, False, 0)
        rt = par1.attach_first(p1, title.end_char + 1, (0 if par2 is None else par2.begin_char - 1))
        if (rt is None): 
            return None
        if (par2 is None): 
            if (len(p1.slots) < 2): 
                return None
            if (not is_contract): 
                return None
            tt2 = None
            ttt = rt.end_token.next0_
            first_pass2894 = True
            while True:
                if first_pass2894: first_pass2894 = False
                else: ttt = ttt.next0_
                if (not (ttt is not None)): break
                if (ttt.is_comma or ttt.is_and): 
                    continue
                if (ttt.morph.class0_.is_preposition): 
                    continue
                npt = NounPhraseHelper.try_parse(ttt, NounPhraseParseAttr.PARSENUMERICASADJECTIVE, 0)
                if (npt is not None): 
                    if (npt.end_token.is_value("СТОРОНА", None)): 
                        ttt = npt.end_token
                        continue
                tt2 = ttt
                break
            if (tt2 is not None and par1 is not None): 
                stat = dict()
                cou1 = 0
                ttt = tt2
                first_pass2895 = True
                while True:
                    if first_pass2895: first_pass2895 = False
                    else: ttt = ttt.next0_
                    if (not (ttt is not None)): break
                    if (ttt.is_value(par1.typ, None)): 
                        cou1 += 1
                        continue
                    tok = ParticipantToken._m_ontology.try_parse(ttt, TerminParseAttr.NO)
                    if (tok is not None and tok.termin.tag is not None and tok.termin.canonic_text != "СТОРОНА"): 
                        if (not tok.termin.canonic_text in stat): 
                            stat[tok.termin.canonic_text] = 1
                        else: 
                            stat[tok.termin.canonic_text] += 1
                typ2 = None
                if (cou1 > 10): 
                    min_cou = math.floor((cou1 * 0.6))
                    max_cou = math.floor((cou1 * 1.4))
                    for kp in stat.items(): 
                        if (kp[1] >= min_cou and kp[1] <= max_cou): 
                            typ2 = kp[0]
                            break
                if (typ2 is not None): 
                    par2 = ParticipantToken._new1343(tt2, tt2, typ2)
        p1 = (ad.register_referent(p1) if isinstance(ad.register_referent(p1), InstrumentParticipant) else None)
        rt.referent = p1
        t0.kit.embed_token(rt)
        if (par2 is not None): 
            p2 = InstrumentParticipant._new1337(par2.typ)
            if (par2.parts is not None): 
                for p in par2.parts: 
                    p2.add_slot(InstrumentParticipant.ATTR_REF, p, False, 0)
            p2 = (ad.register_referent(p2) if isinstance(ad.register_referent(p2), InstrumentParticipant) else None)
            doc.add_slot(InstrumentReferent.ATTR_PARTICIPANT, p2, False, 0)
            rt = par2.attach_first(p2, rt.end_char + 1, 0)
            if (rt is None): 
                return title
            t0.kit.embed_token(rt)
        elif (len(all_parts) > 1): 
            for pp in all_parts: 
                ppp = (ad.register_referent(pp) if isinstance(ad.register_referent(pp), InstrumentParticipant) else None)
                doc.add_slot(InstrumentReferent.ATTR_PARTICIPANT, ppp, False, 0)
                if (pp == all_parts[1]): 
                    p2 = ppp
        req_regim = 0
        t = rt.next0_
        first_pass2896 = True
        while True:
            if first_pass2896: first_pass2896 = False
            else: t = (((None if t is None else t.next0_)))
            if (not (t is not None)): break
            if (t.begin_char >= 712 and (t.begin_char < 740)): 
                pass
            if (t.is_newline_before): 
                if (isinstance(t, NumberToken) and (t if isinstance(t, NumberToken) else None).value == 6): 
                    pass
                ii = InstrToken1.parse(t, True, None, 0, None, False, 0, True)
                if (ii is not None and ii.is_standard_title): 
                    req_regim = 5
                    t = ii.end_token
                    continue
            if (t.is_value("ПРИЛОЖЕНИЕ", None) and t.is_newline_before): 
                pass
            if (req_regim == 5 and t.is_char(chr(0x1E))): 
                rows = TableHelper.try_parse_rows(t, 0, True)
                if (rows is not None and len(rows) > 0 and ((len(rows[0].cells) == 2 or len(rows[0].cells) == 3))): 
                    i0 = len(rows[0].cells) - 2
                    rt0 = ParticipantToken.try_attach_to_exist(rows[0].cells[i0].begin_token, p1, p2)
                    rt1 = ParticipantToken.try_attach_to_exist(rows[0].cells[i0 + 1].begin_token, p1, p2)
                    if (rt0 is not None and rt1 is not None and rt1.referent != rt0.referent): 
                        for ii in range(len(rows)):
                            if (len(rows[ii].cells) == len(rows[0].cells)): 
                                rt = ParticipantToken.try_attach_requisites(rows[ii].cells[i0].begin_token, (rt0.referent if isinstance(rt0.referent, InstrumentParticipant) else None), (rt1.referent if isinstance(rt1.referent, InstrumentParticipant) else None), False)
                                if (rt is not None and rt.end_char <= rows[ii].cells[i0].end_char): 
                                    t0.kit.embed_token(rt)
                                rt = ParticipantToken.try_attach_requisites(rows[ii].cells[i0 + 1].begin_token, (rt1.referent if isinstance(rt1.referent, InstrumentParticipant) else None), (rt0.referent if isinstance(rt0.referent, InstrumentParticipant) else None), False)
                                if (rt is not None and rt.end_char <= rows[ii].cells[i0 + 1].end_char): 
                                    t0.kit.embed_token(rt)
                        t = rows[len(rows) - 1].end_token
                        req_regim = 0
                        continue
            rt = ParticipantToken.try_attach_to_exist(t, p1, p2)
            if (rt is None and req_regim > 0): 
                tt = t
                while tt is not None: 
                    if (tt.is_table_control_char): 
                        pass
                    elif (tt.is_char_of(".)") or isinstance(tt, NumberToken)): 
                        pass
                    else: 
                        rt = ParticipantToken.try_attach_to_exist(tt, p1, p2)
                        if (rt is not None and not t.is_table_control_char): 
                            rt.begin_token = t
                        break
                    tt = tt.next0_
            if (rt is None): 
                req_regim -= 1
                continue
            ps = list()
            ps.append(rt.referent if isinstance(rt.referent, InstrumentParticipant) else None)
            if (req_regim > 0): 
                rt1 = ParticipantToken.try_attach_requisites(rt.end_token.next0_, ps[0], (p2 if ps[0] == p1 else p1), False)
                if (rt1 is not None): 
                    rt.end_token = rt1.end_token
            t0.kit.embed_token(rt)
            t = rt
            if (req_regim <= 0): 
                if (t.is_newline_before): 
                    pass
                elif (t.previous is not None and t.previous.is_table_control_char): 
                    pass
                else: 
                    continue
            else: 
                pass
            if (rt.end_token.next0_ is not None and rt.end_token.next0_.is_table_control_char and not rt.end_token.next0_.is_char(chr(0x1E))): 
                tt = rt.end_token.next0_
                while tt is not None: 
                    if (tt.is_table_control_char): 
                        pass
                    elif (tt.is_char_of(".)") or isinstance(tt, NumberToken)): 
                        pass
                    else: 
                        rt1 = ParticipantToken.try_attach_requisites(tt, (p2 if ps[0] == p1 else p1), ps[0], True)
                        if (rt1 is not None): 
                            ps.append(rt1.referent if isinstance(rt1.referent, InstrumentParticipant) else None)
                            t0.kit.embed_token(rt1)
                            t = rt1
                        break
                    tt = tt.next0_
            t = t.next0_
            if (t is None): 
                break
            while t.is_table_control_char and t.next0_ is not None:
                t = t.next0_
            cur = 0
            first_pass2897 = True
            while True:
                if first_pass2897: first_pass2897 = False
                else: t = t.next0_
                if (not (t is not None)): break
                if (t.is_table_control_char and t.is_char(chr(0x1F))): 
                    req_regim = 0
                    break
                rt = ParticipantToken.try_attach_requisites(t, ps[cur], (p2 if p1 == ps[cur] else p1), req_regim <= 0)
                if (rt is not None): 
                    req_regim = 5
                    t0.kit.embed_token(rt)
                    t = rt
                else: 
                    t = t.previous
                    break
                if (len(ps) == 2 and t.next0_.is_table_control_char): 
                    tt = t.next0_
                    first_pass2898 = True
                    while True:
                        if first_pass2898: first_pass2898 = False
                        else: tt = tt.next0_
                        if (not (tt is not None)): break
                        if (tt.is_table_control_char and tt.is_char(chr(0x1F))): 
                            break
                        if (tt.is_table_control_char): 
                            cur = (1 - cur)
                            if (TableHelper.is_cell_end(tt) and TableHelper.is_row_end(tt.next0_)): 
                                tt = tt.next0_
                            t = tt
                            continue
                        break
                    continue
                if (t.is_table_control_char and len(ps) == 2): 
                    if (TableHelper.is_cell_end(t) and TableHelper.is_row_end(t.next0_)): 
                        t = t.next0_
                    cur = (1 - cur)
                    continue
                if (not t.is_newline_after): 
                    continue
                it1 = InstrToken1.parse(t.next0_, True, None, 0, None, False, 0, False)
                if (it1 is not None): 
                    if (it1.all_upper or it1.is_standard_title or len(it1.numbers) > 0): 
                        break
        return title
    
    @staticmethod
    def __create_project_title(t0 : 'Token', doc : 'InstrumentReferent') -> 'FragToken':
        from pullenti.ner.decree.DecreeReferent import DecreeReferent
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner._org.OrganizationReferent import OrganizationReferent
        from pullenti.ner.instrument.InstrumentReferent import InstrumentReferent
        from pullenti.ner.decree.internal.DecreeToken import DecreeToken
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.morph.MorphClass import MorphClass
        from pullenti.ner.instrument.internal.InstrToken1 import InstrToken1
        if (t0 is None): 
            return None
        is_project = False
        is_entered = False
        is_typ = False
        if (t0.is_table_control_char and t0.next0_ is not None): 
            t0 = t0.next0_
        title = FragToken._new1236(t0, t0, InstrumentKind.HEAD)
        t = t0
        first_pass2899 = True
        while True:
            if first_pass2899: first_pass2899 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_table_control_char): 
                continue
            if (isinstance(t.get_referent(), DecreeReferent)): 
                t = t.kit.debed_token(t)
            if (isinstance(t, TextToken) and (((t if isinstance(t, TextToken) else None).term == "ПРОЕКТ" or (t if isinstance(t, TextToken) else None).term == "ЗАКОНОПРОЕКТ"))): 
                if ((t.is_value("ПРОЕКТ", None) and t == t0 and isinstance(t.next0_, ReferentToken)) and isinstance(t.next0_.get_referent(), OrganizationReferent)): 
                    return None
                is_project = True
                title.children.append(FragToken._new1254(t, t, InstrumentKind.KEYWORD, True))
                doc.add_slot(InstrumentReferent.ATTR_TYPE, "ПРОЕКТ", False, 0)
                continue
            tt = FragToken.__attach_project_enter(t)
            if (tt is not None): 
                is_entered = True
                title.children.append(FragToken._new1236(t, tt, InstrumentKind.APPROVED))
                t = tt
                continue
            tt = FragToken.__attach_project_misc(t)
            if (tt is not None): 
                title.children.append(FragToken._new1236(t, tt, (InstrumentKind.EDITIONS if tt.is_value("ЧТЕНИЕ", "ЧИТАННЯ") else InstrumentKind.UNDEFINED)))
                t = tt
                continue
            if (t.is_newline_before and isinstance(t.get_referent(), DecreeReferent) and ((is_project or is_entered))): 
                t = t.kit.debed_token(t)
            dt = DecreeToken.try_attach(t, None, False)
            if (dt is not None): 
                if ((dt.typ == DecreeToken.ItemType.DATE or dt.typ == DecreeToken.ItemType.TYP or dt.typ == DecreeToken.ItemType.TERR) or dt.typ == DecreeToken.ItemType.NUMBER): 
                    if (FragToken.__add_title_attr(doc, title, dt)): 
                        if (dt.typ == DecreeToken.ItemType.TYP): 
                            is_typ = True
                        t = dt.end_token
                        continue
            break
        if (is_project): 
            pass
        elif (is_entered and is_typ): 
            pass
        else: 
            return None
        title.end_token = t.previous
        t00 = t
        t11 = None
        is_br = BracketHelper.can_be_start_of_sequence(t00, False, False)
        t = t00
        first_pass2900 = True
        while True:
            if first_pass2900: first_pass2900 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_newline_after): 
                if (t.next0_ is not None and t.next0_.chars.is_all_lower): 
                    continue
            if (t.whitespaces_after_count > 15): 
                t11 = t
                break
            elif (t.is_newline_after and t.next0_ is not None): 
                if (t.next0_.get_morph_class_in_dictionary() == MorphClass.VERB): 
                    t11 = t
                    break
                if (t.next0_.chars.is_capital_upper and t.next0_.morph.class0_.is_verb): 
                    t11 = t
                    break
            if (t.is_whitespace_after and is_br and BracketHelper.can_be_end_of_sequence(t, False, None, False)): 
                t11 = t
                break
            if (not t.is_newline_before): 
                continue
            it = InstrToken1.parse(t, True, None, 0, None, False, 0, False)
            if (it is not None and len(it.numbers) > 0 and it.last_number == 1): 
                t11 = t.previous
                break
        if (t11 is None): 
            return None
        nam = FragToken._new1254(t00, t11, InstrumentKind.NAME, True)
        doc.add_slot(InstrumentReferent.ATTR_NAME, nam.value, False, 0)
        title.children.append(nam)
        title.end_token = t11
        appr1 = FragToken.__create_approved(t11.next0_)
        if (appr1 is not None): 
            title.children.append(appr1)
            title.end_token = appr1.end_token
        return title
    
    @staticmethod
    def __attach_project_misc(t : 'Token') -> 'Token':
        from pullenti.ner.NumberToken import NumberToken
        if (t is None): 
            return None
        br = False
        if (t.is_char('(') and t.next0_ is not None): 
            br = True
            t = t.next0_
        if (t.morph.class0_.is_preposition): 
            t = t.next0_
        if (isinstance(t, NumberToken) and t.next0_ is not None and t.next0_.is_value("ЧТЕНИЕ", "ЧИТАННЯ")): 
            t = t.next0_
            if (br and t.next0_ is not None and t.next0_.is_char(')')): 
                t = t.next0_
            return t
        return None
    
    @staticmethod
    def __attach_project_enter(t : 'Token') -> 'Token':
        from pullenti.ner._org.OrganizationReferent import OrganizationReferent
        from pullenti.ner.person.PersonReferent import PersonReferent
        from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent
        if (t is None): 
            return None
        if (t.is_value("ВНОСИТЬ", "ВНОСИТИ") or t.is_value("ВНЕСТИ", None)): 
            pass
        else: 
            return None
        cou = 0
        t = t.next0_
        first_pass2901 = True
        while True:
            if first_pass2901: first_pass2901 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.morph.class0_.is_preposition or t.morph.class0_.is_conjunction): 
                continue
            if (((t.is_value("ПЕРИОД", "ПЕРІОД") or t.is_value("РАССМОТРЕНИЕ", "РОЗГЛЯД") or t.is_value("ДЕПУТАТ", None)) or t.is_value("ПОЛНОМОЧИЕ", "ПОВНОВАЖЕННЯ") or t.is_value("ПЕРЕДАЧА", None)) or t.is_value("ИСПОЛНЕНИЕ", "ВИКОНАННЯ")): 
                continue
            r = t.get_referent()
            if (isinstance(r, OrganizationReferent)): 
                if (cou > 0 and t.is_newline_before): 
                    return t.previous
                cou += 1
                continue
            if (isinstance(r, PersonReferent) or isinstance(r, PersonPropertyReferent)): 
                cou += 1
                continue
            if (t.is_newline_before): 
                return t.previous
        return None
    
    @staticmethod
    def __create_justice_participants(title : 'FragToken', doc : 'InstrumentReferent') -> None:
        from pullenti.ner.instrument.InstrumentReferent import InstrumentReferent
        from pullenti.ner._org.OrganizationReferent import OrganizationReferent
        from pullenti.ner.instrument.InstrumentParticipant import InstrumentParticipant
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.instrument.InstrumentAnalyzer import InstrumentAnalyzer
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.money.MoneyReferent import MoneyReferent
        from pullenti.ner.decree.DecreePartReferent import DecreePartReferent
        from pullenti.ner.decree.DecreeReferent import DecreeReferent
        from pullenti.ner.person.PersonReferent import PersonReferent
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.instrument.InstrumentArtefact import InstrumentArtefact
        from pullenti.ner.ReferentToken import ReferentToken
        typ = doc.typ
        ok = ((((typ == "ПОСТАНОВЛЕНИЕ" or typ == "РЕШЕНИЕ" or typ == "ОПРЕДЕЛЕНИЕ") or typ == "ПРИГОВОР" or (Utils.ifNotNull(typ, "")).endswith("ЗАЯВЛЕНИЕ")) or typ == "ПОСТАНОВА" or typ == "РІШЕННЯ") or typ == "ВИЗНАЧЕННЯ" or typ == "ВИРОК") or (Utils.ifNotNull(typ, "")).endswith("ЗАЯВА")
        for s in doc.slots: 
            if (s.type_name == InstrumentReferent.ATTR_SOURCE and isinstance(s.value, OrganizationReferent)): 
                ki = (s.value if isinstance(s.value, OrganizationReferent) else None).kind
                if (ki == OrganizationKind.JUSTICE): 
                    ok = True
            elif (s.type_name == InstrumentReferent.ATTR_CASENUMBER): 
                ok = True
        pist = None
        potv = None
        pzayav = None
        cou = 0
        tmp = Utils.newStringIO(None)
        t = title.begin_token
        first_pass2902 = True
        while True:
            if first_pass2902: first_pass2902 = False
            else: t = t.next0_
            if (not (t is not None and t.end_char <= title.end_char)): break
            if (t.is_newline_before): 
                pass
            elif (t.previous is not None and t.previous.is_table_control_char): 
                pass
            else: 
                continue
            if (t.next0_ is not None and ((t.next0_.is_char(':') or t.next0_.is_table_control_char))): 
                if (t.is_value("ЗАЯВИТЕЛЬ", "ЗАЯВНИК")): 
                    pzayav = FragToken.__create_just_participant(t.next0_, None)
                    if (pzayav is not None): 
                        pzayav.begin_token = t
                        (pzayav.referent if isinstance(pzayav.referent, InstrumentParticipant) else None).typ = "ЗАЯВИТЕЛЬ"
                elif (t.is_value("ИСТЕЦ", "ПОЗИВАЧ")): 
                    pist = FragToken.__create_just_participant(t.next0_, None)
                    if (pist is not None): 
                        pist.begin_token = t
                        (pist.referent if isinstance(pist.referent, InstrumentParticipant) else None).typ = "ИСТЕЦ"
                elif (t.is_value("ОТВЕТЧИК", "ВІДПОВІДАЧ") or t.is_value("ДОЛЖНИК", "БОРЖНИК")): 
                    potv = FragToken.__create_just_participant(t.next0_, None)
                    if (potv is not None): 
                        potv.begin_token = t
                        (potv.referent if isinstance(potv.referent, InstrumentParticipant) else None).typ = "ОТВЕТЧИК"
        t = title.end_token.next0_
        first_pass2903 = True
        while True:
            if first_pass2903: first_pass2903 = False
            else: t = t.next0_
            if (not (t is not None)): break
            cou += 1
            if ((cou) > 1000): 
                break
            if (t.is_value("ЗАЯВЛЕНИЕ", "ЗАЯВА")): 
                pass
            elif (t.is_value("ИСК", "ПОЗОВ") and t.previous is not None and t.previous.morph.class0_.is_preposition): 
                pass
            else: 
                continue
            if (t.next0_ is not None and t.next0_.is_char('(')): 
                br = BracketHelper.try_parse(t.next0_, BracketParseAttr.NO, 100)
                if (br is not None): 
                    t = br.end_token
            if (pist is not None): 
                break
            pist = FragToken.__create_just_participant(t.next0_, ("ПОЗИВАЧ" if t.next0_.morph.language.is_ua else "ИСТЕЦ"))
            if (pist is None): 
                break
            t = pist.end_token.next0_
            if (t is not None and t.is_char(',')): 
                t = t.next0_
            if (t is None): 
                break
            if (potv is not None): 
                break
            if (t.is_value("О", "ПРО") and t.next0_ is not None and t.next0_.is_value("ПРИВЛЕЧЕНИЕ", "ЗАЛУЧЕННЯ")): 
                if (t.next0_.morph.language.is_ua): 
                    print("ПРО ПРИТЯГНЕННЯ", end="", file=tmp)
                else: 
                    print("О ПРИВЛЕЧЕНИИ", end="", file=tmp)
                t = t.next0_.next0_
                potv = FragToken.__create_just_participant(t, ("ВІДПОВІДАЧ" if t.next0_.morph.language.is_ua else "ОТВЕТЧИК"))
            elif (t.is_value("О", "ПРО") and t.next0_ is not None and t.next0_.is_value("ПРИЗНАНИЕ", "ВИЗНАННЯ")): 
                if (t.next0_.morph.language.is_ua): 
                    print("ПРО ВИЗНАННЯ", end="", file=tmp)
                else: 
                    print("О ПРИЗНАНИИ", end="", file=tmp)
                t = t.next0_.next0_
                potv = FragToken.__create_just_participant(t, ("ВІДПОВІДАЧ" if t.next0_.morph.language.is_ua else "ОТВЕТЧИК"))
            elif (t.is_value("О", "ПРО") and t.next0_ is not None and t.next0_.is_value("ВЗЫСКАНИЕ", "СТЯГНЕННЯ")): 
                if (t.next0_.morph.language.is_ua): 
                    print("ПРО СТЯГНЕННЯ", end="", file=tmp)
                else: 
                    print("О ВЗЫСКАНИИ", end="", file=tmp)
                t = t.next0_.next0_
                if (t is not None and t.morph.class0_.is_preposition): 
                    t = t.next0_
                potv = FragToken.__create_just_participant(t, ("ВІДПОВІДАЧ" if t.next0_.morph.language.is_ua else "ОТВЕТЧИК"))
            else: 
                if (t is None or not t.is_value("К", "ПРО")): 
                    break
                potv = FragToken.__create_just_participant(t.next0_, ("ВІДПОВІДАЧ" if t.next0_.morph.language.is_ua else "ОТВЕТЧИК"))
            if (potv is not None): 
                t = potv.end_token.next0_
            break
        if (((pist is None and pzayav is None)) or ((potv is None and tmp.tell() == 0))): 
            return
        ad = title.kit.get_analyzer_data_by_analyzer_name(InstrumentAnalyzer.ANALYZER_NAME)
        if (pzayav is not None): 
            pzayav.referent = ad.register_referent(pzayav.referent)
            pzayav.kit.embed_token(pzayav)
            doc.add_slot(InstrumentReferent.ATTR_PARTICIPANT, pzayav.referent, False, 0)
        if (pist is not None): 
            pist.referent = ad.register_referent(pist.referent)
            pist.kit.embed_token(pist)
            doc.add_slot(InstrumentReferent.ATTR_PARTICIPANT, pist.referent, False, 0)
        if (potv is not None): 
            potv.referent = ad.register_referent(potv.referent)
            potv.kit.embed_token(potv)
            doc.add_slot(InstrumentReferent.ATTR_PARTICIPANT, potv.referent, False, 0)
        if (t is not None and t.is_char(',')): 
            t = t.next0_
        if (t is None): 
            return
        npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0)
        if (npt is not None and npt.end_token.is_value("ЛИЦО", "ОСОБА")): 
            t = npt.end_token.next0_
            if (t is not None and t.is_char(':')): 
                t = t.next0_
            first_pass2904 = True
            while True:
                if first_pass2904: first_pass2904 = False
                else: t = t.next0_
                if (not (t is not None)): break
                if (t.is_char(',')): 
                    continue
                tret = FragToken.__create_just_participant(t, ("ТРЕТЯ ОСОБА" if t.morph.language.is_ua else "ТРЕТЬЕ ЛИЦО"))
                if (tret is None): 
                    break
                tret.referent = ad.register_referent(tret.referent)
                tret.kit.embed_token(tret)
                doc.add_slot(InstrumentReferent.ATTR_PARTICIPANT, tret.referent, False, 0)
                t = tret
        tt00 = t
        while t is not None:
            t0 = t
            if (not t.is_value("О", "ПРО") and not t.is_value("ОБ", None)): 
                if (tmp.tell() == 0): 
                    if (t != tt00): 
                        break
                    cou2 = 0
                    has_isk = True
                    tt = t.next0_
                    while tt is not None and (cou2 < 140): 
                        if (tt.is_value("ЗАЯВЛЕНИЕ", "ЗАЯВА") or tt.is_value("ИСК", "ПОЗОВ")): 
                            cou2 = 0
                            has_isk = True
                        if ((has_isk and ((tt.is_value("О", "ПРО") or tt.is_value("ОБ", None))) and tt.next0_.get_morph_class_in_dictionary().is_noun) and tt.next0_.morph.case.is_prepositional): 
                            print(MiscHelper.get_text_value(tt, tt.next0_, GetTextAttr.NO), end="", file=tmp)
                            t0 = tt
                            t = tt.next0_.next0_
                            break
                        tt = tt.next0_; cou2 += 1
                    if (tmp.tell() == 0 or t is None): 
                        break
            arefs = list()
            t1 = None
            first_pass2905 = True
            while True:
                if first_pass2905: first_pass2905 = False
                else: t = t.next0_
                if (not (t is not None)): break
                if (t.is_newline_before and t != t0): 
                    if (t.whitespaces_before_count > 15): 
                        break
                if (t.is_value("ПРИ", "ЗА") and t.next0_ is not None and t.next0_.is_value("УЧАСТИЕ", "УЧАСТЬ")): 
                    break
                if (t.is_value("БЕЗ", None) and t.next0_ is not None and t.next0_.is_value("ВЫЗОВ", None)): 
                    break
                r = t.get_referent()
                if (r is not None): 
                    if (isinstance(r, MoneyReferent)): 
                        arefs.append(r)
                        if (t.previous is not None and t.previous.is_value("СУММА", "СУМА")): 
                            pass
                        else: 
                            print(" СУММЫ".format(), end="", file=tmp, flush=True)
                        t1 = t
                        continue
                    if (isinstance(r, DecreePartReferent) or isinstance(r, DecreeReferent)): 
                        arefs.append(r)
                        if (t.previous is not None and t.previous.is_value("ПО", None)): 
                            Utils.setLengthStringIO(tmp, tmp.tell() - 3)
                        t1 = t
                        tt = t.next0_
                        first_pass2906 = True
                        while True:
                            if first_pass2906: first_pass2906 = False
                            else: tt = tt.next0_
                            if (not (tt is not None)): break
                            if (tt.is_comma_and): 
                                continue
                            r = tt.get_referent()
                            if (isinstance(r, DecreePartReferent) or isinstance(r, DecreeReferent)): 
                                arefs.append(r)
                                t = tt
                                t1 = t
                                continue
                            break
                        break
                    if (isinstance(r, PersonReferent)): 
                        continue
                    break
                if (t.is_char_of(",.") or t.is_hiphen): 
                    break
                if (isinstance(t, TextToken)): 
                    term = (t if isinstance(t, TextToken) else None).term
                    if (term == "ИП"): 
                        continue
                if (t.is_and): 
                    if (t.next0_ is None): 
                        break
                    if (t.next0_.is_value("О", "ПРО") or t.next0_.is_value("ОБ", None)): 
                        t = t.next0_
                        break
                if (t.is_newline_after): 
                    if (t.next0_ is None): 
                        pass
                    elif (t.next0_.chars.is_all_lower): 
                        pass
                    else: 
                        break
                if (t.is_whitespace_before and tmp.tell() > 0): 
                    print(' ', end="", file=tmp)
                print(MiscHelper.get_text_value(t, t, GetTextAttr.NO), end="", file=tmp)
                t1 = t
            if (tmp.tell() > 10 and t1 is not None): 
                art = InstrumentArtefact._new1350("предмет")
                str0_ = Utils.toStringStringIO(tmp)
                str0_ = str0_.replace("В РАЗМЕРЕ СУММЫ", "СУММЫ").strip()
                if (str0_.endswith("В РАЗМЕРЕ")): 
                    str0_ = (str0_[0 : (len(str0_) - 9)] + "СУММЫ")
                if (str0_.endswith("В СУММЕ")): 
                    str0_ = (str0_[0 : (len(str0_) - 7)] + "СУММЫ")
                art.value = str0_
                for a in arefs: 
                    art.add_slot(InstrumentArtefact.ATTR_REF, a, False, 0)
                rta = ReferentToken(art, t0, t1)
                rta.referent = ad.register_referent(rta.referent)
                doc.add_slot(InstrumentReferent.ATTR_ARTEFACT, rta.referent, False, 0)
                rta.kit.embed_token(rta)
                Utils.setLengthStringIO(tmp, 0)
            else: 
                break
        t = (t if potv is None else potv.next0_)
        first_pass2907 = True
        while True:
            if first_pass2907: first_pass2907 = False
            else: t = t.next0_
            if (not (t is not None)): break
            rt = None
            check_del = False
            if (t.is_value("ИСТЕЦ", "ПОЗИВАЧ") and pist is not None): 
                rt = ReferentToken(pist.referent, t, t)
                check_del = True
            elif (t.is_value("ЗАЯВИТЕЛЬ", "ЗАЯВНИК") and pzayav is not None): 
                rt = ReferentToken(pzayav.referent, t, t)
                check_del = True
            elif (((t.is_value("ОТВЕТЧИК", "ВІДПОВІДАЧ") or t.is_value("ДОЛЖНИК", "БОРЖНИК"))) and potv is not None): 
                rt = ReferentToken(potv.referent, t, t)
                check_del = True
            else: 
                r = t.get_referent()
                if (not ((isinstance(r, OrganizationReferent))) and not ((isinstance(r, PersonReferent)))): 
                    continue
                if (pist is not None and pist.referent.find_slot(InstrumentParticipant.ATTR_REF, r, True) is not None): 
                    rt = ReferentToken(pist.referent, t, t)
                elif (pzayav is not None and pzayav.referent.find_slot(InstrumentParticipant.ATTR_REF, r, True) is not None): 
                    rt = ReferentToken(pzayav.referent, t, t)
                elif (potv is not None and potv.referent.find_slot(InstrumentParticipant.ATTR_REF, r, True) is not None): 
                    rt = ReferentToken(potv.referent, t, t)
            if (rt is None): 
                continue
            if (check_del and t.previous is not None and t.previous.is_value("ОТ", None)): 
                tt = t.previous
                if (tt.previous is not None and tt.previous.is_hiphen): 
                    tt = tt.previous
                if (tt.is_whitespace_before): 
                    tt1 = t.next0_
                    if (tt1 is not None and ((tt1.is_hiphen or tt1.is_char(':')))): 
                        tt1 = tt1.next0_
                    if (isinstance(tt1.get_referent(), PersonReferent)): 
                        rt.begin_token = tt
                        rt.end_token = tt1
                        rt.referent.add_slot(InstrumentParticipant.ATTR_DELEGATE, (tt1.get_referent() if isinstance(tt1.get_referent(), PersonReferent) else None), False, 0)
            if (rt is not None and rt.end_token.next0_ is not None and rt.end_token.next0_.is_char('(')): 
                tt = rt.end_token.next0_.next0_
                if (tt is not None and tt.next0_ is not None and tt.next0_.is_char(')')): 
                    if (tt.is_value("ИСТЕЦ", "ПОЗИВАЧ") and pist is not None and rt.referent == pist.referent): 
                        rt.end_token = tt.next0_
                    elif (tt.is_value("ЗАЯВИТЕЛЬ", "ЗАЯВНИК") and pzayav is not None and rt.referent == pzayav.referent): 
                        rt.end_token = tt.next0_
                    elif (((tt.is_value("ОТВЕТЧИК", "ВІДПОВІДАЧ") or tt.is_value("ДОЛЖНИК", "БОРЖНИК"))) and potv is not None and rt.referent == potv.referent): 
                        rt.end_token = tt.next0_
                    elif (isinstance(tt.get_referent(), PersonReferent) or isinstance(tt.get_referent(), OrganizationReferent)): 
                        if (pist is not None and rt.referent == pist.referent): 
                            if (pist.referent.find_slot(None, tt.get_referent(), True) is not None): 
                                rt.end_token = tt.next0_
                            elif (potv is not None and potv.referent.find_slot(None, tt.get_referent(), True) is None): 
                                rt.end_token = tt.next0_
                                pist.referent.add_slot(InstrumentParticipant.ATTR_REF, tt.get_referent(), False, 0)
                        elif (potv is not None and rt.referent == potv.referent): 
                            if (potv.referent.find_slot(None, tt.get_referent(), True) is not None): 
                                rt.end_token = tt.next0_
                            elif (pist is not None and pist.referent.find_slot(None, tt.get_referent(), True) is None): 
                                rt.end_token = tt.next0_
                                potv.referent.add_slot(InstrumentParticipant.ATTR_REF, tt.get_referent(), False, 0)
            t.kit.embed_token(rt)
            t = rt
    
    @staticmethod
    def __create_just_participant(t : 'Token', typ : str) -> 'ReferentToken':
        from pullenti.ner.person.PersonReferent import PersonReferent
        from pullenti.ner._org.OrganizationReferent import OrganizationReferent
        from pullenti.ner.uri.UriReferent import UriReferent
        from pullenti.ner.decree.DecreeReferent import DecreeReferent
        from pullenti.ner.decree.DecreePartReferent import DecreePartReferent
        from pullenti.ner.phone.PhoneReferent import PhoneReferent
        from pullenti.ner.address.AddressReferent import AddressReferent
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.ner._org.internal.OrgItemTypeToken import OrgItemTypeToken
        from pullenti.ner.TextToken import TextToken
        from pullenti.morph.MorphClass import MorphClass
        from pullenti.ner.instrument.InstrumentParticipant import InstrumentParticipant
        from pullenti.ner.ReferentToken import ReferentToken
        if (t is None): 
            return None
        r0 = None
        t0 = t
        t1 = t
        ok = False
        br = False
        refs = list()
        first_pass2908 = True
        while True:
            if first_pass2908: first_pass2908 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_newline_before and t != t0): 
                if (t.whitespaces_before_count > 15): 
                    break
            if (t.is_hiphen or t.is_char_of(":,") or t.is_table_control_char): 
                continue
            if (not br): 
                if (t.is_value("К", None) or t.is_value("О", "ПРО")): 
                    break
            if (t.is_char('(')): 
                if (br): 
                    break
                br = True
                continue
            if (t.is_char(')') and br): 
                br = False
                t1 = t
                break
            r = t.get_referent()
            if (isinstance(r, PersonReferent) or isinstance(r, OrganizationReferent)): 
                if (r0 is None): 
                    refs.append(r)
                    r0 = r
                    t1 = t
                    ok = True
                    continue
                break
            if (isinstance(r, UriReferent)): 
                ur = (r if isinstance(r, UriReferent) else None)
                if (ur.scheme == "ИНН" or ur.scheme == "ИИН" or ur.scheme == "ОГРН"): 
                    ok = True
                refs.append(r)
                t1 = t
                continue
            if (not br): 
                if (isinstance(r, DecreeReferent) or isinstance(r, DecreePartReferent)): 
                    break
            if (r is not None or br): 
                if (isinstance(r, PhoneReferent) or isinstance(r, AddressReferent)): 
                    refs.append(r)
                t1 = t
                continue
            if (BracketHelper.can_be_start_of_sequence(t, True, False)): 
                brr = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                if (brr is not None): 
                    ok = True
                    t = brr.end_token
                    t1 = t
                    continue
            if (t.previous.is_comma and not br): 
                break
            if (t.previous.morph.class0_.is_preposition and t.is_value("УЧАСТИЕ", "УЧАСТЬ")): 
                break
            if (isinstance(t.previous, NumberToken) and t.is_value("ЛИЦО", "ОСОБА")): 
                break
            npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0)
            if (npt is not None): 
                if ((npt.noun.is_value("УЧРЕЖДЕНИЕ", "УСТАНОВА") or npt.noun.is_value("ПРЕДПРИЯТИЕ", "ПІДПРИЄМСТВО") or npt.noun.is_value("ОРГАНИЗАЦИЯ", "ОРГАНІЗАЦІЯ")) or npt.noun.is_value("КОМПЛЕКС", None)): 
                    t = npt.end_token
                    t1 = t
                    ok = True
                    continue
            ty = OrgItemTypeToken.try_attach(t, True, None)
            if (ty is not None): 
                t = ty.end_token
                t1 = t
                ok = True
                continue
            if (isinstance(t, TextToken) and t.chars.is_cyrillic_letter and t.chars.is_all_lower): 
                if (t.morph.class0_ == MorphClass.VERB or t.morph.class0_ == MorphClass.ADVERB): 
                    break
            if (t.is_newline_before and typ is None): 
                break
            elif (not t.morph.class0_.is_preposition and not t.morph.class0_.is_conjunction): 
                t1 = t
            elif (t.is_newline_before): 
                break
        if (not ok): 
            return None
        pat = InstrumentParticipant._new1337(typ)
        for r in refs: 
            pat.add_slot(InstrumentParticipant.ATTR_REF, r, False, 0)
        return ReferentToken(pat, t0, t1)
    
    def __create_justice_resolution(self) -> None:
        from pullenti.ner.instrument.InstrumentAnalyzer import InstrumentAnalyzer
        from pullenti.ner.money.MoneyReferent import MoneyReferent
        from pullenti.ner.instrument.InstrumentArtefact import InstrumentArtefact
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.instrument.InstrumentReferent import InstrumentReferent
        ad = self.kit.get_analyzer_data_by_analyzer_name(InstrumentAnalyzer.ANALYZER_NAME)
        if (ad is None): 
            return
        res = self.__find_resolution()
        if (res is None): 
            return
        t = res.begin_token
        first_pass2909 = True
        while True:
            if first_pass2909: first_pass2909 = False
            else: t = t.next0_
            if (not (t is not None and t.end_char <= res.end_char)): break
            if (t == res.begin_token): 
                pass
            elif (t.previous is not None and t.previous.is_char('.') and t.is_whitespace_before): 
                pass
            elif (not t.is_value("ПРИЗНАТЬ", "ВИЗНАТИ")): 
                continue
            if (t.morph.class0_.is_preposition and t.next0_ is not None): 
                t = t.next0_
            arts = list()
            tt = None
            te = None
            if (t.is_value("ВЗЫСКАТЬ", "СТЯГНУТИ")): 
                gosposh = False
                sum0_ = None
                te = None
                tt = t.next0_
                first_pass2910 = True
                while True:
                    if first_pass2910: first_pass2910 = False
                    else: tt = tt.next0_
                    if (not (tt is not None and tt.end_char <= res.end_char)): break
                    if (tt.morph.class0_.is_preposition): 
                        continue
                    if (tt.is_char('.')): 
                        break
                    if (tt.is_value("ТОМ", "ТОМУ") and tt.next0_ is not None and tt.next0_.is_value("ЧИСЛО", None)): 
                        break
                    if (tt.is_value("ГОСПОШЛИНА", "ДЕРЖМИТО")): 
                        gosposh = True
                    elif (tt.is_value("ФЕДЕРАЛЬНЫЙ", "ФЕДЕРАЛЬНИЙ") and tt.next0_ is not None and tt.next0_.is_value("БЮДЖЕТ", None)): 
                        gosposh = True
                    if (isinstance(tt.get_referent(), MoneyReferent)): 
                        te = tt
                        sum0_ = (tt.get_referent() if isinstance(tt.get_referent(), MoneyReferent) else None)
                if (sum0_ is not None): 
                    art = InstrumentArtefact._new1350("РЕЗОЛЮЦИЯ")
                    if (gosposh): 
                        art.value = "ВЗЫСКАТЬ ГОСПОШЛИНУ"
                    else: 
                        art.value = "ВЗЫСКАТЬ СУММУ"
                    art.add_slot(InstrumentArtefact.ATTR_REF, sum0_, False, 0)
                    arts.append(ReferentToken(art, t, te))
            if ((t.is_value("ЗАЯВЛЕНИЕ", "ЗАЯВА") or t.is_value("ИСК", "ПОЗОВ") or t.is_value("ТРЕБОВАНИЕ", "ВИМОГА")) or t.is_value("ЗАЯВЛЕННЫЙ", "ЗАЯВЛЕНИЙ") or t.is_value("УДОВЛЕТВОРЕНИЕ", "ЗАДОВОЛЕННЯ")): 
                tt = t.next0_
                first_pass2911 = True
                while True:
                    if first_pass2911: first_pass2911 = False
                    else: tt = tt.next0_
                    if (not (tt is not None and tt.end_char <= res.end_char)): break
                    if (tt.morph.class0_.is_preposition): 
                        continue
                    if (tt.is_char('.')): 
                        if (tt.is_whitespace_after): 
                            break
                    if (tt.is_value("УДОВЛЕТВОРИТЬ", "ЗАДОВОЛЬНИТИ")): 
                        val = "УДОВЛЕТВОРИТЬ"
                        te = tt
                        if (tt.next0_ is not None and tt.next0_.is_value("ПОЛНОСТЬЮ", "ПОВНІСТЮ")): 
                            val += " ПОЛНОСТЬЮ"
                            te = tt.next0_
                        elif (tt.previous is not None and tt.previous.is_value("ПОЛНОСТЬЮ", "ПОВНІСТЮ")): 
                            val += " ПОЛНОСТЬЮ"
                        art = InstrumentArtefact._new1350("РЕЗОЛЮЦИЯ")
                        art.value = val
                        arts.append(ReferentToken(art, t, te))
                        break
                    if (tt.is_value("ОТКАЗАТЬ", "ВІДМОВИТИ")): 
                        art = InstrumentArtefact._new1350("РЕЗОЛЮЦИЯ")
                        art.value = "ОТКАЗАТЬ"
                        te = tt
                        arts.append(ReferentToken(art, t, te))
                        break
            if (t.is_value("ПРИЗНАТЬ", "ВИЗНАТИ")): 
                zak = -1
                otm = -1
                tt = t.next0_
                first_pass2912 = True
                while True:
                    if first_pass2912: first_pass2912 = False
                    else: tt = tt.next0_
                    if (not (tt is not None and tt.end_char <= res.end_char)): break
                    if (tt.morph.class0_.is_preposition): 
                        continue
                    if (tt.is_char('.')): 
                        break
                    if (tt.is_value("НЕЗАКОННЫЙ", "НЕЗАКОННИЙ")): 
                        zak = 0
                        te = tt
                    elif (tt.is_value("ЗАКОННЫЙ", "ЗАКОННИЙ")): 
                        zak = 1
                        te = tt
                    elif (tt.is_value("ОТМЕНИТЬ", "СКАСУВАТИ")): 
                        otm = 1
                        te = tt
                if (zak >= 0): 
                    val = "ПРИЗНАТЬ {0}".format(("ЗАКОННЫМ" if zak > 0 else "НЕЗАКОННЫМ"))
                    if (otm > 0): 
                        val += " И ОТМЕНИТЬ"
                    art = InstrumentArtefact._new1350("РЕЗОЛЮЦИЯ")
                    art.value = val
                    arts.append(ReferentToken(art, t, te))
                else: 
                    continue
            for rt in arts: 
                rt.referent = ad.register_referent(rt.referent)
                self._m_doc.add_slot(InstrumentReferent.ATTR_ARTEFACT, rt.referent, False, 0)
                if (res.begin_token == rt.begin_token): 
                    res.begin_token = rt
                if (res.end_token == rt.end_token): 
                    res.end_token = rt
                self.kit.embed_token(rt)
                t = rt
    
    def __find_resolution(self) -> 'FragToken':
        if (self.kind == InstrumentKind.APPENDIX): 
            return None
        dir0_ = False
        for i in range(len(self.children)):
            if (self.children[i].kind == InstrumentKind.DIRECTIVE and ((i + 1) < len(self.children))): 
                v = self.children[i].value
                if (v is None): 
                    continue
                s = str(v)
                if ((((s == "РЕШЕНИЕ" or s == "ОПРЕДЕЛЕНИЕ" or s == "ПОСТАНОВЛЕНИЕ") or s == "ПРИГОВОР" or s == "РІШЕННЯ") or s == "ВИЗНАЧЕННЯ" or s == "ПОСТАНОВА") or s == "ВИРОК"): 
                    ii = i + 1
                    for j in range(ii + 1, len(self.children), 1):
                        if (self.children[j].kind != self.children[ii].kind): 
                            break
                        else: 
                            ii = j
                    if (ii == (i + 1)): 
                        return self.children[i + 1]
                    else: 
                        return FragToken._new1236(self.children[i + 1].begin_token, self.children[ii].end_token, InstrumentKind.CONTENT)
                dir0_ = True
        if (dir0_): 
            return None
        for ch in self.children: 
            re = ch.__find_resolution()
            if (re is not None): 
                return re
        return None
    
    @staticmethod
    def __create_action_question(t : 'Token', max_char : int) -> 'FragToken':
        from pullenti.ner.instrument.internal.InstrToken import InstrToken
        from pullenti.ner.instrument.internal.InstrToken1 import InstrToken1
        from pullenti.ner.decree.internal.DecreeToken import DecreeToken
        li = list()
        ok = False
        tt = t
        while tt is not None: 
            it = InstrToken.parse(tt, max_char, None)
            if (it is None): 
                break
            li.append(it)
            if (len(li) > 5): 
                return None
            if (it.typ == ILTypes.QUESTION): 
                ok = True
                break
            tt = it.end_token
            tt = tt.next0_
        if (not ok): 
            return None
        t1 = li[len(li) - 1].end_token
        li2 = list()
        ok = False
        tt = t1.next0_
        first_pass2913 = True
        while True:
            if first_pass2913: first_pass2913 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            if (not tt.is_newline_before): 
                continue
            it = InstrToken.parse(tt, max_char, None)
            if (it is None): 
                break
            li2.append(it)
            tt = it.end_token
            if (it.typ != ILTypes.TYP): 
                continue
            it1 = InstrToken1.parse(tt, True, None, 0, None, False, max_char, False)
            if (it1 is not None and it1.has_verb): 
                tt = it1.end_token
                continue
            tt2 = DecreeToken.is_keyword(it.begin_token, False)
            if (tt2 is not None and tt2 == it.end_token): 
                ok = True
                break
        if (not ok): 
            return None
        t2 = li2[len(li2) - 1].begin_token
        while len(li2) > 1 and li2[len(li2) - 2].typ == ILTypes.ORGANIZATION:
            t2 = li2[len(li2) - 2].begin_token
            del li2[len(li2) - 1]
        res = FragToken.create_document(t2, max_char, InstrumentKind.UNDEFINED)
        if (res is None): 
            return None
        ques = FragToken._new1236(t, t2.previous, InstrumentKind.QUESTION)
        res.children.insert(0, ques)
        ques.children.append(FragToken._new1236(li[len(li) - 1].begin_token, li[len(li) - 1].end_token, InstrumentKind.KEYWORD))
        content = FragToken._new1236(li[len(li) - 1].end_token.next0_, t2.previous, InstrumentKind.CONTENT)
        ques.children.append(content)
        content._analize_content(res, max_char > 0, InstrumentKind.UNDEFINED)
        if (len(li) > 1): 
            fr = FragToken._new1257(t, li[len(li) - 2].end_token, InstrumentKind.NAME, True)
            ques.children.insert(0, fr)
        res.begin_token = t
        return res
    
    @staticmethod
    def __create_gost_title(t0 : 'Token', doc : 'InstrumentReferent') -> 'FragToken':
        from pullenti.ner.decree.DecreeReferent import DecreeReferent
        from pullenti.ner.decree.internal.DecreeToken import DecreeToken
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.instrument.InstrumentReferent import InstrumentReferent
        if (t0 is None): 
            return None
        ok = False
        if (t0.is_table_control_char and t0.next0_ is not None): 
            t0 = t0.next0_
        cou = 0
        t = t0
        first_pass2914 = True
        while True:
            if first_pass2914: first_pass2914 = False
            else: t = t.next0_; cou += 1
            if (not (t is not None and (cou < 300))): break
            dr = (t.get_referent() if isinstance(t.get_referent(), DecreeReferent) else None)
            if (dr is not None): 
                if (dr.kind == DecreeKind.STANDARD): 
                    t = t.kit.debed_token(t)
                    if (t.begin_char == t0.begin_char): 
                        t0 = t
                    ok = True
                break
            if (t.is_table_control_char): 
                continue
            if (t.is_newline_before or ((t.previous is not None and t.previous.is_table_control_char))): 
                if (FragToken.__is_start_of_body(t)): 
                    break
                dt = DecreeToken.try_attach(t, None, False)
                if (dt is not None): 
                    if (dt.typ == DecreeToken.ItemType.TYP): 
                        if (dt.typ_kind == DecreeKind.STANDARD): 
                            ok = True
                        break
        if (not ok): 
            return None
        title = FragToken._new1236(t0, t0, InstrumentKind.HEAD)
        cou = 0
        has_num = False
        t = t0
        first_pass2915 = True
        while True:
            if first_pass2915: first_pass2915 = False
            else: t = t.next0_
            if (not (t is not None and (cou < 100))): break
            if (t.is_newline_before and t != t0): 
                title.end_token = t.previous
                if (t.is_value("ЧАСТЬ", None)): 
                    t = t.next0_
                    tt1 = MiscHelper.check_number_prefix(t)
                    if (tt1 is not None): 
                        t = tt1
                    if (isinstance(t, NumberToken)): 
                        tmp = Utils.newStringIO(None)
                        while t is not None: 
                            if (isinstance(t, NumberToken)): 
                                print((t if isinstance(t, NumberToken) else None).value, end="", file=tmp)
                            elif (((t.is_hiphen or t.is_char('.'))) and not t.is_whitespace_after and isinstance(t.next0_, NumberToken)): 
                                print((t if isinstance(t, TextToken) else None).term, end="", file=tmp)
                            else: 
                                break
                            if (t.is_whitespace_after): 
                                break
                            t = t.next0_
                        doc.add_slot(InstrumentReferent.ATTR_PART, Utils.toStringStringIO(tmp), True, 0)
                    continue
                if (FragToken.__is_start_of_body(t)): 
                    break
                cou += 1
            if (not has_num): 
                dr = (t.get_referent() if isinstance(t.get_referent(), DecreeReferent) else None)
                if (dr is not None and dr.kind == DecreeKind.STANDARD): 
                    t = t.kit.debed_token(t)
            title.end_token = t
            dt = DecreeToken.try_attach(t, None, False)
            if (dt is None): 
                continue
            if (dt.typ == DecreeToken.ItemType.TYP): 
                if (dt.typ_kind != DecreeKind.STANDARD): 
                    continue
                FragToken.__add_title_attr(doc, title, dt)
                t = dt.end_token
                if (not has_num): 
                    num = DecreeToken.try_attach(t.next0_, dt, False)
                    if (num is not None and num.typ == DecreeToken.ItemType.NUMBER): 
                        FragToken.__add_title_attr(doc, title, num)
                        if (num.num_year > 0): 
                            doc.add_slot(InstrumentReferent.ATTR_DATE, num.num_year, False, 0)
                        t = dt.end_token
                        has_num = True
                continue
        title.tag = DecreeKind.STANDARD
        return title
    
    def _analize_content(self, top_doc : 'FragToken', is_citat : bool, root_kind : 'InstrumentKind'=InstrumentKind.UNDEFINED) -> None:
        self.kind = InstrumentKind.CONTENT
        if (self.begin_token.previous is not None and self.begin_token.previous.is_char(chr(0x1E))): 
            self.begin_token = self.begin_token.previous
        wr = ContentAnalyzeWhapper()
        wr.analyze(self, top_doc, is_citat, root_kind)
        for ch in top_doc.children: 
            if (ch.kind == InstrumentKind.HEAD): 
                for chh in ch.children: 
                    if (chh.kind == InstrumentKind.EDITIONS and chh.referents is not None): 
                        if (top_doc.referents is None): 
                            top_doc.referents = list()
                        for r in chh.referents: 
                            if (not r in top_doc.referents): 
                                top_doc.referents.append(r)
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        self.kind = InstrumentKind.UNDEFINED
        self.kind2 = InstrumentKind.UNDEFINED
        self.value = None
        self.name = None
        self.number = 0
        self.min_number = 0
        self.sub_number = 0
        self.sub_number2 = 0
        self.sub_number3 = 0
        self.referents = None
        self.is_expired = False
        self.children = list()
        self._m_doc = None
        self._itok = None
        super().__init__(b, e0_, None)
        t = self.end_token.next0_
        while t is not None: 
            if (t.is_char(chr(7)) or t.is_char(chr(0x1F))): 
                self.end_token = t
            else: 
                break
            t = t.next0_
    
    @property
    def number_string(self) -> str:
        if (self.sub_number == 0): 
            return str(self.number)
        tmp = Utils.newStringIO(None)
        print("{0}.{1}".format(self.number, self.sub_number), end="", file=tmp, flush=True)
        if (self.sub_number2 > 0): 
            print(".{0}".format(self.sub_number2), end="", file=tmp, flush=True)
        if (self.sub_number3 > 0): 
            print(".{0}".format(self.sub_number3), end="", file=tmp, flush=True)
        return Utils.toStringStringIO(tmp)
    
    def sort_children(self) -> None:
        for k in range(len(self.children)):
            ch = False
            i = 0
            while i < (len(self.children) - 1): 
                if (self.children[i].compare_to(self.children[i + 1]) > 0): 
                    ch = True
                    v = self.children[i]
                    self.children[i] = self.children[i + 1]
                    self.children[i + 1] = v
                i += 1
            if (not ch): 
                break
    
    def find_child(self, kind_ : 'InstrumentKind') -> 'FragToken':
        for ch in self.children: 
            if (ch.kind == kind_): 
                return ch
        return None
    
    def compare_to(self, other : 'FragToken') -> int:
        if (self.begin_char < other.begin_char): 
            return -1
        if (self.begin_char > other.begin_char): 
            return 1
        if (self.end_char < other.end_char): 
            return -1
        if (self.end_char > other.end_char): 
            return 1
        return 0
    
    @property
    def min_child_number(self) -> int:
        for ch in self.children: 
            if (ch.number > 0): 
                if (ch.number != 1): 
                    if (ch._itok is not None and ch._itok.num_typ == NumberTypes.LETTER): 
                        return 0
                return ch.number
        return 0
    
    @property
    def max_child_number(self) -> int:
        max0_ = 0
        for ch in self.children: 
            if (ch.number > max0_): 
                max0_ = ch.number
        return max0_
    
    @property
    def _def_val(self) -> bool:
        return False
    
    @_def_val.setter
    def _def_val(self, value_) -> bool:
        str0_ = self.get_source_text()
        while len(str0_) > 0:
            last = str0_[len(str0_) - 1]
            if (ord(last) == 0x1E or ord(last) == 0x1F or ord(last) == 7): 
                str0_ = str0_[0 : (len(str0_) - 1)]
            else: 
                break
        self.value = str0_
        return value_
    
    @property
    def _def_val2(self) -> bool:
        return False
    
    @_def_val2.setter
    def _def_val2(self, value_) -> bool:
        self.value = FragToken._get_restored_namemt(self, False)
        return value_
    
    @staticmethod
    def _get_restored_namemt(mt : 'MetaToken', index_item : bool=False) -> str:
        return FragToken._get_restored_name(mt.begin_token, mt.end_token, index_item)
    
    @staticmethod
    def _get_restored_name(b : 'Token', e0_ : 'Token', index_item : bool=False) -> str:
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.core.MiscHelper import MiscHelper
        e0 = e0_
        while e0_ is not None and e0_.begin_char > b.end_char: 
            if (e0_.is_char_of("*<") or e0_.is_table_control_char): 
                pass
            elif ((e0_.is_char_of(">") and isinstance(e0_.previous, NumberToken) and e0_.previous.previous is not None) and e0_.previous.previous.is_char('<')): 
                e0_ = e0_.previous
            elif (e0_.is_char_of(">") and e0_.previous.is_char('*')): 
                pass
            elif (isinstance(e0_, NumberToken) and e0_ == e0 and index_item): 
                pass
            elif (((e0_.is_char('.') or e0_.is_hiphen)) and index_item): 
                pass
            else: 
                break
            e0_ = e0_.previous
        str0_ = MiscHelper.get_text_value(b, e0_, Utils.valToEnum(GetTextAttr.RESTOREREGISTER | GetTextAttr.KEEPREGISTER | GetTextAttr.KEEPQUOTES, GetTextAttr))
        if (not Utils.isNullOrEmpty(str0_)): 
            if (str0_[0].islower()): 
                str0_ = "{0}{1}".format(str0_[0].upper(), str0_[1 : ])
        return str0_
    
    def __str__(self) -> str:
        tmp = Utils.newStringIO(None)
        if (self.kind != InstrumentKind.UNDEFINED): 
            print("{0}:".format(Utils.enumToString(self.kind)), end="", file=tmp, flush=True)
            if (self.kind2 != InstrumentKind.UNDEFINED): 
                print(" ({0}):".format(Utils.enumToString(self.kind2)), end="", file=tmp, flush=True)
        elif (self._itok is not None): 
            print("{0} ".format(self._itok), end="", file=tmp, flush=True)
        if (self.number > 0): 
            if (self.min_number > 0): 
                print(" Num=[{0}..{1}]".format(self.min_number, self.number), end="", file=tmp, flush=True)
            else: 
                print(" Num={0}".format(self.number), end="", file=tmp, flush=True)
            if (self.sub_number > 0): 
                print(".{0}".format(self.sub_number), end="", file=tmp, flush=True)
            if (self.sub_number2 > 0): 
                print(".{0}".format(self.sub_number2), end="", file=tmp, flush=True)
            if (self.sub_number3 > 0): 
                print(".{0}".format(self.sub_number3), end="", file=tmp, flush=True)
        if (self.is_expired): 
            print(" Expired", end="", file=tmp)
        if (len(self.children) > 0): 
            print(" ChCount={0}".format(len(self.children)), end="", file=tmp, flush=True)
        if (self.name is not None): 
            print(" Nam='{0}'".format(self.name), end="", file=tmp, flush=True)
        if (self.value is not None): 
            print(" Val='{0}'".format(str(self.value)), end="", file=tmp, flush=True)
        if (tmp.tell() == 0): 
            print(self.get_source_text(), end="", file=tmp)
        return Utils.toStringStringIO(tmp)
    
    def create_referent(self, ad : 'AnalyzerData') -> 'InstrumentBlockReferent':
        return self._create_referent(ad, self)
    
    def _create_referent(self, ad : 'AnalyzerData', bas : 'FragToken') -> 'InstrumentBlockReferent':
        from pullenti.ner.Referent import Referent
        from pullenti.ner.instrument.InstrumentBlockReferent import InstrumentBlockReferent
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.decree.internal.DecreeToken import DecreeToken
        from pullenti.ner.decree.DecreeChangeReferent import DecreeChangeReferent
        res = None
        if (self._m_doc is not None): 
            res = self._m_doc
        else: 
            res = InstrumentBlockReferent()
            res.kind = self.kind
            res.kind2 = self.kind2
            if (self.number > 0): 
                res.number = self.number
            if (self.min_number > 0): 
                res.min_number = self.min_number
            if (self.sub_number > 0): 
                res.sub_number = self.sub_number
            if (self.sub_number2 > 0): 
                res.sub_number2 = self.sub_number2
            if (self.sub_number3 > 0): 
                res.sub_number3 = self.sub_number3
            if (self.is_expired): 
                res.is_expired = True
            if (self.name is not None and self.kind != InstrumentKind.HEAD): 
                s = res.add_slot(InstrumentBlockReferent.ATTR_NAME, self.name.upper(), False, 0)
                s.tag = self.name
            if (self.value is not None and self.kind != InstrumentKind.CONTACT): 
                if (isinstance(self.value, str)): 
                    res.add_slot(InstrumentBlockReferent.ATTR_VALUE, self.value, False, 0)
                elif (isinstance(self.value, Referent)): 
                    res.add_slot(InstrumentBlockReferent.ATTR_REF, self.value, False, 0)
                elif (isinstance(self.value, ReferentToken)): 
                    r = (self.value if isinstance(self.value, ReferentToken) else None).referent
                    (self.value if isinstance(self.value, ReferentToken) else None).save_to_local_ontology()
                    res.add_slot(InstrumentBlockReferent.ATTR_REF, (self.value if isinstance(self.value, ReferentToken) else None).referent, False, 0)
                    res.add_ext_referent(self.value if isinstance(self.value, ReferentToken) else None)
                    s = bas._m_doc.find_slot(None, r, True)
                    if (s is not None): 
                        s.value = (self.value if isinstance(self.value, ReferentToken) else None).referent
                elif (isinstance(self.value, DecreeToken)): 
                    dt = (self.value if isinstance(self.value, DecreeToken) else None)
                    if (isinstance(dt.ref, ReferentToken)): 
                        r = (dt.ref if isinstance(dt.ref, ReferentToken) else None).referent
                        (dt.ref if isinstance(dt.ref, ReferentToken) else None).save_to_local_ontology()
                        res.add_slot(InstrumentBlockReferent.ATTR_REF, (dt.ref if isinstance(dt.ref, ReferentToken) else None).referent, False, 0)
                        res.add_ext_referent(dt.ref if isinstance(dt.ref, ReferentToken) else None)
                        s = bas._m_doc.find_slot(None, r, True)
                        if (s is not None): 
                            s.value = (dt.ref if isinstance(dt.ref, ReferentToken) else None).referent
                    elif (dt.value is not None): 
                        res.add_slot(InstrumentBlockReferent.ATTR_VALUE, dt.value, False, 0)
            if (self.referents is not None): 
                for r in self.referents: 
                    res.add_slot(InstrumentBlockReferent.ATTR_REF, r, False, 0)
            if (len(self.children) == 0): 
                t = self.begin_token
                while t is not None and (t.begin_char < self.end_char): 
                    if (isinstance(t.get_referent(), DecreeChangeReferent)): 
                        res.add_slot(InstrumentBlockReferent.ATTR_REF, t.get_referent(), False, 0)
                    if (t.end_char > self.end_char): 
                        break
                    t = t.next0_
        if (ad is not None): 
            if (len(ad.referents) > 200000): 
                return None
            ad.referents.append(res)
            res.add_occurence_of_ref_tok(ReferentToken(res, self.begin_token, self.end_token))
        for ch in self.children: 
            ich = ch._create_referent(ad, bas)
            if (ich is not None): 
                res.add_slot(InstrumentBlockReferent.ATTR_CHILD, ich, False, 0)
        return res
    
    def fill_by_content_children(self) -> None:
        self.sort_children()
        if (len(self.children) == 0): 
            self.children.append(FragToken._new1236(self.begin_token, self.end_token, InstrumentKind.CONTENT))
            return
        if (self.begin_char < self.children[0].begin_char): 
            self.children.insert(0, FragToken._new1236(self.begin_token, self.children[0].begin_token.previous, InstrumentKind.CONTENT))
        i = 0
        while i < (len(self.children) - 1): 
            if (self.children[i].end_token.next0_ != self.children[i + 1].begin_token and (self.children[i].end_token.next0_.end_char < self.children[i + 1].begin_char)): 
                self.children.insert(i + 1, FragToken._new1236(self.children[i].end_token.next0_, self.children[i + 1].begin_token.previous, InstrumentKind.CONTENT))
            i += 1
        if (self.children[len(self.children) - 1].end_char < self.end_char): 
            self.children.append(FragToken._new1236(self.children[len(self.children) - 1].end_token.next0_, self.end_token, InstrumentKind.CONTENT))
    
    @staticmethod
    def create_document(t : 'Token', max_char : int, root_kind : 'InstrumentKind'=InstrumentKind.UNDEFINED) -> 'FragToken':
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.decree.DecreeReferent import DecreeReferent
        from pullenti.ner.decree.DecreePartReferent import DecreePartReferent
        from pullenti.ner.instrument.InstrumentReferent import InstrumentReferent
        from pullenti.ner.instrument.internal.InstrToken import InstrToken
        from pullenti.ner.instrument.internal.InstrToken1 import InstrToken1
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.decree.internal.DecreeToken import DecreeToken
        if (t is None): 
            return None
        while isinstance(t, TextToken) and t.next0_ is not None:
            if (t.is_table_control_char or not t.chars.is_letter): 
                t = t.next0_
            else: 
                break
        if (isinstance(t.get_referent(), DecreeReferent)): 
            dec0 = (t.get_referent() if isinstance(t.get_referent(), DecreeReferent) else None)
            if (dec0.kind == DecreeKind.PUBLISHER): 
                t = t.next0_
            else: 
                t = t.kit.debed_token(t)
        elif (isinstance(t.get_referent(), DecreePartReferent)): 
            dp = (t.get_referent() if isinstance(t.get_referent(), DecreePartReferent) else None)
            if ((dp.clause is not None or dp.item is not None or dp.sub_item is not None) or dp.indention is not None): 
                pass
            else: 
                t = t.kit.debed_token(t)
        if (t is None): 
            return None
        res = FragToken.__create_action_question(t, max_char)
        if (res is not None): 
            return res
        res = FragToken._new1236(t, t, InstrumentKind.DOCUMENT)
        res._m_doc = InstrumentReferent()
        is_app = False
        if (t.is_value("ПРИЛОЖЕНИЕ", "ДОДАТОК")): 
            is_app = True
        head = (None if is_app or max_char > 0 else FragToken.__create_doc_title(t, res._m_doc))
        head_kind = DecreeKind.UNDEFINED
        if (head is not None and isinstance(head.tag, DecreeKind)): 
            head_kind = Utils.valToEnum(head.tag, DecreeKind)
        head1 = None
        if (max_char > 0 and not is_app): 
            pass
        else: 
            head1 = FragToken.__create_appendix_title(t, res, res._m_doc, is_app)
        if (head is None): 
            head = head1
        elif (head1 is not None and head1.end_char > head.end_char and ((res._m_doc.typ == "ПРИЛОЖЕНИЕ" or res._m_doc.typ == "ДОДАТОК"))): 
            head = head1
        if (head is not None): 
            if (max_char == 0): 
                FragToken.__create_justice_participants(head, res._m_doc)
            head.sort_children()
            res.children.append(head)
            res.end_token = head.end_token
            t = res.end_token.next0_
        if (t is None): 
            return None
        is_contract = False
        if (res._m_doc.typ is not None): 
            if ("ДОГОВОР" in res._m_doc.typ or "ДОГОВІР" in res._m_doc.typ or "КОНТРАКТ" in res._m_doc.typ): 
                is_contract = True
        t0 = t
        li = InstrToken.parse_list(t, max_char)
        if (li is None or len(li) == 0): 
            return None
        if (is_app): 
            for i in range(len(li)):
                if (li[i].typ == ILTypes.APPROVED): 
                    li[i].typ = ILTypes.UNDEFINED
                elif (li[i].typ == ILTypes.APPENDIX and li[i].value != "ПРИЛОЖЕНИЕ" and li[i].value != "ДОДАТОК"): 
                    li[i].typ = ILTypes.UNDEFINED
            else: i = len(li)
        i = 0
        while i < (len(li) - 1): 
            if (li[i].typ == ILTypes.APPENDIX): 
                if (i > 0 and li[i - 1].typ == ILTypes.PERSON): 
                    break
                num1 = InstrToken1.parse(li[i].begin_token, True, None, 0, None, False, 0, False)
                for j in range(i + 1, len(li), 1):
                    if (li[j].typ == ILTypes.APPENDIX): 
                        if (li[j].value != li[i].value): 
                            if (li[i].value == "ПРИЛОЖЕНИЕ" or li[i].value == "ДОДАТОК"): 
                                li[j].typ = ILTypes.UNDEFINED
                            elif (li[j].value == "ПРИЛОЖЕНИЕ" or li[j].value == "ДОДАТОК"): 
                                li[i].typ = ILTypes.UNDEFINED
                                break
                        else: 
                            le = li[j].begin_char - li[i].begin_char
                            if (le > 400): 
                                break
                            li[i].typ = ILTypes.UNDEFINED
                            i = j
                            num2 = InstrToken1.parse(li[j].begin_token, True, None, 0, None, False, 0, False)
                            d = NumberingHelper.calc_delta(num1, num2, True)
                            if (d == 1): 
                                li[j].typ = ILTypes.UNDEFINED
                            num1 = num2
                    elif (li[j].typ == ILTypes.APPROVED): 
                        li[j].typ = ILTypes.UNDEFINED
            i += 1
        has_app = False
        for i in range(len(li)):
            if (li[i].typ == ILTypes.APPENDIX or li[i].typ == ILTypes.APPROVED): 
                if (li[i].typ == ILTypes.APPROVED): 
                    has_app = True
                    if (i == 0 or not li[i].is_newline_after): 
                        continue
                if (isinstance(li[i].ref, DecreeReferent)): 
                    dr_app = (li[i].ref if isinstance(li[i].ref, DecreeReferent) else None)
                    if (dr_app.typ != res._m_doc.typ): 
                        continue
                    if (dr_app.number is not None and res._m_doc.reg_number is not None): 
                        if (dr_app.number != res._m_doc.reg_number): 
                            continue
                break
        else: i = len(li)
        i1 = i
        if (max_char == 0 and i1 == len(li)): 
            i = 0
            while i < len(li): 
                if (li[i].typ == ILTypes.PERSON and li[i].is_newline_before and not li[i].has_table_chars): 
                    dat = False
                    num = False
                    geo_ = False
                    pers = 0
                    for j in range(i + 1, len(li), 1):
                        if (li[j].typ == ILTypes.GEO): 
                            geo_ = True
                        elif (li[j].typ == ILTypes.REGNUMBER): 
                            num = True
                        elif (li[j].typ == ILTypes.DATE): 
                            dat = True
                        elif (li[j].typ == ILTypes.PERSON and li[j].is_pure_person): 
                            if (((li[j].is_newline_before or li[j - 1].typ == ILTypes.PERSON)) and ((li[j].is_newline_after or ((((j + 1) < len(li)) and li[j + 1].typ == ILTypes.PERSON))))): 
                                pers += 1
                            else: 
                                break
                        else: 
                            break
                    else: j = len(li)
                    k = pers
                    if (dat): 
                        k += 1
                    if (num): 
                        k += 1
                    if (geo_): 
                        k += 1
                    if ((j < len(li)) and ((li[j].typ == ILTypes.APPENDIX or li[j].typ == ILTypes.APPROVED))): 
                        k += 2
                    elif ((li[i].is_pure_person and li[i].begin_token.previous is not None and li[i].begin_token.previous.is_char('.')) and li[i].is_newline_after): 
                        k += 2
                    if (k >= 2): 
                        i = j
                        if ((i < len(li)) and ((li[i].typ == ILTypes.UNDEFINED or li[i].typ == ILTypes.TYP))): 
                            li[i].typ = ILTypes.APPROVED
                        if ((i > (i1 + 10) and (i1 < len(li)) and li[i1].typ == ILTypes.APPENDIX) and li[i1].whitespaces_before_count > 15): 
                            pass
                        else: 
                            i1 = i
                        break
                i += 1
        if ((max_char == 0 and (i1 < len(li)) and (i1 + 10) > len(li)) and not has_app and ((li[len(li) - 1].end_char - li[i1].end_char) < 200)): 
            for ii in range(len(li) - 1, i, -1):
                if (li[ii].typ == ILTypes.PERSON or li[ii].typ == ILTypes.DATE or li[ii].typ == ILTypes.REGNUMBER): 
                    i1 = (ii + 1)
                    break
        cmax = i1 - 1
        tail = None
        pers_list = list()
        for i in range(i1 - 1, 0, -1):
            if (max_char > 0): 
                break
            lii = li[i]
            if (lii.has_table_chars): 
                if ((i < (i1 - 1)) and lii.typ != ILTypes.PERSON): 
                    break
                if (is_contract): 
                    break
            if ((lii.typ == ILTypes.PERSON or lii.typ == ILTypes.REGNUMBER or lii.typ == ILTypes.DATE) or lii.typ == ILTypes.GEO): 
                if (len(pers_list) > 0 and ((((lii.typ != ILTypes.PERSON and lii.typ != ILTypes.DATE)) or ((not lii.is_newline_before and not lii.has_table_chars))))): 
                    break
                if (lii.typ == ILTypes.PERSON and isinstance(lii.ref, ReferentToken)): 
                    if ((lii.ref if isinstance(lii.ref, ReferentToken) else None).referent in pers_list): 
                        break
                if (not lii.is_newline_before and not lii.begin_token.is_table_control_char and ((lii.typ == ILTypes.GEO or li[i].typ == ILTypes.PERSON))): 
                    if (i > 0 and ((li[i - 1].typ == ILTypes.UNDEFINED and not li[i - 1].end_token.is_table_control_char))): 
                        break
                    if (lii.end_token.is_char_of(";.")): 
                        break
                    if (not lii.is_newline_after): 
                        if (lii.end_token.next0_ is not None and not lii.end_token.next0_.is_table_control_char): 
                            break
                if (tail is None): 
                    tail = FragToken._new1236(li[i].begin_token, li[i1 - 1].end_token, InstrumentKind.TAIL)
                    if ((i1 - 1) > i): 
                        pass
                tail.begin_token = lii.begin_token
                cmax = (i - 1)
                fr = FragToken(li[i].begin_token, li[i].end_token)
                tail.children.insert(0, fr)
                if (li[i].typ == ILTypes.PERSON): 
                    fr.kind = InstrumentKind.SIGNER
                    if (isinstance(li[i].ref, ReferentToken)): 
                        res._m_doc.add_slot(InstrumentReferent.ATTR_SIGNER, (li[i].ref if isinstance(li[i].ref, ReferentToken) else None).referent, False, 0)
                        res._m_doc.add_ext_referent(li[i].ref if isinstance(li[i].ref, ReferentToken) else None)
                        fr.value = li[i].ref
                        pers_list.append((li[i].ref if isinstance(li[i].ref, ReferentToken) else None).referent)
                elif (li[i].typ == ILTypes.REGNUMBER): 
                    if (li[i].is_newline_before): 
                        if (res._m_doc.reg_number is None or res._m_doc.reg_number == li[i].value): 
                            fr.kind = InstrumentKind.NUMBER
                            fr.value = li[i].value
                            res._m_doc.add_slot(InstrumentReferent.ATTR_NUMBER, li[i].value, False, 0)
                elif (li[i].typ == ILTypes.DATE): 
                    fr.kind = InstrumentKind.DATE
                    fr.value = li[i].value
                    if (li[i].ref is not None): 
                        res._m_doc._add_date(li[i].ref)
                        fr.value = li[i].ref
                    elif (li[i].value is not None): 
                        res._m_doc._add_date(li[i].value)
                elif (li[i].typ == ILTypes.GEO): 
                    fr.kind = InstrumentKind.PLACE
                    fr.value = li[i].ref
                if (fr.value is None): 
                    fr.value = MiscHelper.get_text_value_of_meta_token(fr, GetTextAttr.NO)
            else: 
                ss = MiscHelper.get_text_value(li[i].begin_token, li[i].end_token, GetTextAttr.KEEPQUOTES)
                if (ss is None or len(ss) == 0): 
                    continue
                if (ss[len(ss) - 1] == ':'): 
                    ss = ss[0 : (len(ss) - 1)]
                if (li[i].is_podpis_storon and tail is not None): 
                    tail.begin_token = li[i].begin_token
                    tail.children.insert(0, FragToken._new1284(li[i].begin_token, li[i].end_token, InstrumentKind.NAME, ss))
                    cmax = (i - 1)
                    break
                for jj in range(len(ss)):
                    if (ss[jj].isalnum()): 
                        break
                else: jj = len(ss)
                if (jj >= len(ss)): 
                    continue
                if ((len(ss) < 100) and (((i1 - i) < 3))): 
                    continue
                break
        else: i = 0
        if (cmax < 0): 
            if (i1 > 0): 
                return None
        else: 
            content = FragToken._new1236(li[0].begin_token, li[cmax].end_token, InstrumentKind.CONTENT)
            res.children.append(content)
            content._analize_content(res, max_char > 0, root_kind)
            if (max_char > 0 and cmax == (len(li) - 1) and head is None): 
                res = content
        if (tail is not None): 
            res.children.append(tail)
            while i1 < len(li): 
                if (li[i1].begin_token == li[i1].end_token and isinstance(li[i1].begin_token.get_referent(), DecreeReferent) and (li[i1].begin_token.get_referent() if isinstance(li[i1].begin_token.get_referent(), DecreeReferent) else None).kind == DecreeKind.PUBLISHER): 
                    ap = FragToken._new1236(li[i1].begin_token, li[i1].end_token, InstrumentKind.APPROVED)
                    ap.referents = list()
                    ap.referents.append(li[i1].begin_token.get_referent() if isinstance(li[i1].begin_token.get_referent(), DecreeReferent) else None)
                    tail.children.append(ap)
                    tail.end_token = li[i1].end_token
                else: 
                    break
                i1 += 1
            if (len(tail.children) > 0 and (tail.children[len(tail.children) - 1].end_char < tail.end_char)): 
                unkw = FragToken._new1236(tail.children[len(tail.children) - 1].end_token.next0_, tail.end_token, InstrumentKind.UNDEFINED)
                tail.end_token = unkw.begin_token.previous
                res.children.append(unkw)
        is_all_apps = is_app
        i = i1
        while i < len(li): 
            for j in range(i + 1, len(li), 1):
                if (li[j].typ == ILTypes.APPENDIX): 
                    if (li[j].value == li[i1].value): 
                        break
                    continue
                elif (li[j].typ == ILTypes.APPROVED): 
                    if ((li[j].begin_char - li[i].end_char) > 200): 
                        break
            else: j = len(li)
            app = FragToken(li[i].begin_token, li[j - 1].end_token)
            tail = None
            if (li[j - 1].typ == ILTypes.PERSON and li[j - 1].is_newline_before and li[j - 1].is_newline_after): 
                tail = FragToken._new1236(li[j - 1].begin_token, li[j - 1].end_token, InstrumentKind.TAIL)
                for jj in range(j - 1, i, -1):
                    if (li[jj].typ != ILTypes.PERSON or not li[jj].is_newline_before or not li[jj].is_newline_after): 
                        break
                    else: 
                        fr = FragToken._new1236(li[jj].begin_token, li[jj].end_token, InstrumentKind.SIGNER)
                        if (isinstance(li[jj].ref, ReferentToken)): 
                            fr.value = li[jj].ref
                        tail.children.insert(0, fr)
                        tail.begin_token = fr.begin_token
                        app.end_token = tail.begin_token.previous
            if (li[i].typ == ILTypes.APPENDIX or ((((i + 1) < len(li)) and li[i + 1].typ == ILTypes.APPENDIX))): 
                app.kind = InstrumentKind.APPENDIX
            else: 
                app.kind = InstrumentKind.INTERNALDOCUMENT
            title = FragToken.__create_appendix_title(app.begin_token, app, res._m_doc, is_all_apps)
            if (title is None): 
                ok = True
                if (app.length_char < 500): 
                    ok = False
                else: 
                    app._analize_content(app, False, InstrumentKind.UNDEFINED)
                    if (len(app.children) < 2): 
                        ok = False
                if (ok): 
                    res.children.append(app)
                else: 
                    app.kind = InstrumentKind.UNDEFINED
                    res.children[len(res.children) - 1].children.append(app)
                    res.children[len(res.children) - 1].end_token = app.end_token
            else: 
                if (is_app and app.kind == InstrumentKind.APPENDIX): 
                    if (len(res.children) > 0): 
                        res.end_token = res.children[len(res.children) - 1].end_token
                    res0 = FragToken._new1374(res.begin_token, res.end_token, res._m_doc, InstrumentKind.DOCUMENT)
                    res._m_doc = None
                    res.kind = InstrumentKind.APPENDIX
                    res0.children.insert(0, res)
                    res = res0
                    is_app = False
                res.children.append(app)
                if (title.name is not None): 
                    app.name = title.name
                    title.name = None
                app.children.append(title)
                if (title.end_token.next0_ is not None): 
                    if (title.end_token.end_char < app.end_token.begin_char): 
                        acontent = FragToken._new1236(title.end_token.next0_, app.end_token, InstrumentKind.CONTENT)
                        app.children.append(acontent)
                        acontent._analize_content(app, False, InstrumentKind.UNDEFINED)
                    else: 
                        pass
                if (len(app.children) == 1 and app.kind != InstrumentKind.APPENDIX): 
                    app.children.clear()
                    app.kind = InstrumentKind.UNDEFINED
                    app.name = None
            if (tail is not None): 
                app.children.append(tail)
                app.end_token = tail.end_token
            i = (j - 1)
            i += 1
        if (len(res.children) > 0): 
            res.end_token = res.children[len(res.children) - 1].end_token
        appendixes = list()
        for ch in res.children: 
            if (ch.kind == InstrumentKind.APPENDIX): 
                appendixes.append(ch)
        for i in range(1, len(appendixes), 1):
            max_coef = 0
            ii = -1
            for j in range(i - 1, -1, -1):
                coef = appendixes[i].__calc_owner_coef(appendixes[j])
                if (coef > max_coef): 
                    max_coef = coef
                    ii = j
            if (ii < 0): 
                continue
            appendixes[ii].children.append(appendixes[i])
            res.children.remove(appendixes[i])
        else: i = len(appendixes)
        if (max_char > 0): 
            return res
        if (not is_contract and head_kind != DecreeKind.STANDARD): 
            for ch in res.children: 
                if (ch.kind == InstrumentKind.APPENDIX or ch.kind == InstrumentKind.INTERNALDOCUMENT or ch.kind == InstrumentKind.HEAD): 
                    if (ch.kind == InstrumentKind.APPENDIX and res._m_doc.name is not None): 
                        continue
                    hi = (ch if ch.kind == InstrumentKind.HEAD else ch.find_child(InstrumentKind.HEAD))
                    if (hi is not None): 
                        hi = hi.find_child(InstrumentKind.NAME)
                        if (hi is not None and hi.value is not None and len(str(hi.value)) > 20): 
                            res._m_doc.add_slot(InstrumentReferent.ATTR_NAME, hi.value, False, 0)
        if (res._m_doc.typ is None): 
            for ch in res.children: 
                if (ch.kind == InstrumentKind.APPENDIX): 
                    hi = ch.find_child(InstrumentKind.HEAD)
                    if (hi is not None): 
                        hi = hi.find_child(InstrumentKind.DOCREFERENCE)
                    if (hi is not None): 
                        t1 = hi.begin_token
                        if (t1.is_value("К", "ДО") and t1.next0_ is not None): 
                            t1 = t1.next0_
                        dr = (t1.get_referent() if isinstance(t1.get_referent(), DecreeReferent) else None)
                        if (dr is not None and dr.number == res._m_doc.reg_number): 
                            res._m_doc.typ = dr.typ
                        else: 
                            dt = DecreeToken.try_attach(t1, None, False)
                            if (dt is not None and dt.typ == DecreeToken.ItemType.TYP): 
                                res._m_doc.typ = dt.value
                    break
        res.__create_justice_resolution()
        if (res._m_doc.typ is None and ((res._m_doc.reg_number is not None or res._m_doc.case_number is not None))): 
            if ((len(res.children) > 1 and res.children[1].kind == InstrumentKind.CONTENT and len(res.children[1].children) > 0) and res.children[1].children[len(res.children[1].children) - 1].kind == InstrumentKind.DOCPART): 
                part = res.children[1].children[len(res.children[1].children) - 1]
                for ch in part.children: 
                    if (ch.kind == InstrumentKind.DIRECTIVE and ch.value is not None): 
                        res._m_doc.typ = (ch.value if isinstance(ch.value, str) else None)
                        break
        return res
    
    @staticmethod
    def __create_case_info(t : 'Token') -> 'FragToken':
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.decree.DecreePartReferent import DecreePartReferent
        from pullenti.ner.decree.internal.DecreeToken import DecreeToken
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.date.DateReferent import DateReferent
        if (t is None): 
            return None
        if (not t.is_newline_before): 
            return None
        rez = False
        t1 = None
        if (isinstance(t, ReferentToken) and isinstance(t.get_referent(), DecreePartReferent)): 
            dpr = (t.get_referent() if isinstance(t.get_referent(), DecreePartReferent) else None)
            if (dpr.part == "резолютивная"): 
                t1 = t
        elif (t.is_value("РЕЗОЛЮТИВНЫЙ", "РЕЗОЛЮТИВНЫЙ") and t.next0_ is not None and t.next0_.is_value("ЧАСТЬ", "ЧАСТИНА")): 
            t1 = t.next0_
        elif (t.is_value("ПОЛНЫЙ", "ПОВНИЙ") and t.next0_ is not None and t.next0_.is_value("ТЕКСТ", None)): 
            t1 = t.next0_
        if (t1 is not None): 
            rez = True
            dt = DecreeToken.try_attach(t1.next0_, None, False)
            if (dt is not None and dt.typ == DecreeToken.ItemType.TYP): 
                t1 = dt.end_token
        if (not rez): 
            if ((t.is_value("ПОСТАНОВЛЕНИЕ", "ПОСТАНОВА") or t.is_value("РЕШЕНИЕ", "РІШЕННЯ") or t.is_value("ОПРЕДЕЛЕНИЕ", "ВИЗНАЧЕННЯ")) or t.is_value("ПРИГОВОР", "ВИРОК")): 
                if (t.is_newline_after and t.chars.is_all_upper): 
                    return None
                t1 = t
        if (t1 is None): 
            return None
        if (t1.next0_ is not None and t1.next0_.morph.class0_.is_preposition): 
            npt = NounPhraseHelper.try_parse(t1.next0_.next0_, NounPhraseParseAttr.NO, 0)
            if (npt is not None): 
                t1 = npt.end_token
        if (t1.next0_ is not None and t1.next0_.morph.class0_.is_verb): 
            pass
        else: 
            return None
        has_date = False
        tt = t1.next0_
        while tt is not None: 
            if (MiscHelper.can_be_start_of_sentence(tt)): 
                break
            else: 
                t1 = tt
                if (isinstance(t1.get_referent(), DateReferent)): 
                    has_date = True
            tt = tt.next0_
        if ((not has_date and t1.next0_ is not None and isinstance(t1.next0_.get_referent(), DateReferent)) and t1.next0_.is_newline_after): 
            t1 = t1.next0_
        return FragToken._new1236(t, t1, InstrumentKind.CASEINFO)
    
    @staticmethod
    def __create_approved(t : 'Token') -> 'FragToken':
        from pullenti.ner.instrument.internal.InstrToken import InstrToken
        from pullenti.morph.MorphClass import MorphClass
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.decree.internal.DecreeToken import DecreeToken
        from pullenti.ner.decree.DecreeReferent import DecreeReferent
        from pullenti.ner.person.PersonReferent import PersonReferent
        from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent
        from pullenti.ner.date.DateReferent import DateReferent
        if (t is None): 
            return None
        res = None
        tt = InstrToken._check_approved(t)
        if (tt is not None): 
            res = FragToken._new1236(t, tt, InstrumentKind.APPROVED)
        elif (t.is_value("ОДОБРИТЬ", "СХВАЛИТИ") or t.is_value("ПРИНЯТЬ", "ПРИЙНЯТИ") or t.is_value("УТВЕРДИТЬ", "ЗАТВЕРДИТИ")): 
            if (t.morph.contains_attr("инф.", MorphClass()) and t.morph.contains_attr("сов.в.", MorphClass())): 
                pass
            else: 
                res = FragToken._new1236(t, t, InstrumentKind.APPROVED)
        elif (isinstance(t, TextToken) and (((t if isinstance(t, TextToken) else None).term == "ИМЕНЕМ" or (t if isinstance(t, TextToken) else None).term == "ІМЕНЕМ"))): 
            res = FragToken._new1236(t, t, InstrumentKind.APPROVED)
        if (res is None): 
            return None
        t = res.end_token
        if (t.next0_ is None): 
            return res
        if (not t.is_newline_after and t.next0_.get_normal_case_text(MorphClass(), False, MorphGender.UNDEFINED, False) == res.begin_token.get_normal_case_text(MorphClass(), False, MorphGender.UNDEFINED, False)): 
            t = t.next0_
            while t is not None: 
                if (t.is_newline_before or t.get_normal_case_text(MorphClass(), False, MorphGender.UNDEFINED, False) != res.begin_token.get_normal_case_text(MorphClass(), False, MorphGender.UNDEFINED, False)): 
                    break
                else: 
                    res.end_token = t
                t = t.next0_
            if (t.next0_ is None): 
                return res
            tt0 = t.next0_
            t = t.next0_
            first_pass2916 = True
            while True:
                if first_pass2916: first_pass2916 = False
                else: t = t.next0_
                if (not (t is not None)): break
                dtt = DecreeToken.try_attach(t, None, False)
                if (dtt is not None): 
                    if (dtt.typ == DecreeToken.ItemType.TYP and t != tt0 and t.is_newline_before): 
                        break
                    t = dtt.end_token
                    res.end_token = t
                    continue
                if (t.newlines_before_count > 1): 
                    break
                res.end_token = t
            return res
        t = t.next0_
        first_pass2917 = True
        while True:
            if first_pass2917: first_pass2917 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_and or t.morph.class0_.is_preposition): 
                continue
            if (t.is_value("ВВЕСТИ", None) or t.is_value("ДЕЙСТВИЕ", "ДІЯ")): 
                res.end_token = t
                continue
            break
        if (t is None): 
            return res
        dts = DecreeToken.try_attach_list(t, None, 10, False)
        if (dts is not None and len(dts) > 0): 
            i = 0
            while i < len(dts): 
                dt = dts[i]
                if (dt.typ == DecreeToken.ItemType.ORG): 
                    res.children.append(FragToken._new1284(dt.begin_token, dt.end_token, InstrumentKind.ORGANIZATION, dt))
                elif (dt.typ == DecreeToken.ItemType.OWNER): 
                    res.children.append(FragToken._new1284(dt.begin_token, dt.end_token, InstrumentKind.INITIATOR, dt))
                elif (dt.typ == DecreeToken.ItemType.DATE): 
                    res.children.append(FragToken._new1284(dt.begin_token, dt.end_token, InstrumentKind.DATE, dt))
                elif (dt.typ == DecreeToken.ItemType.NUMBER and i > 0 and dts[i - 1].typ == DecreeToken.ItemType.DATE): 
                    res.children.append(FragToken._new1284(dt.begin_token, dt.end_token, InstrumentKind.NUMBER, dt))
                elif (dt.typ == DecreeToken.ItemType.TYP and i == 0): 
                    if (((i + 1) < len(dts)) and dts[i + 1].typ == DecreeToken.ItemType.TERR): 
                        i += 1
                        dt = dts[i]
                elif (dt.typ == DecreeToken.ItemType.TERR and res.begin_token.is_value("ИМЕНЕМ", "ІМЕНЕМ")): 
                    res.children.append(FragToken._new1284(dt.begin_token, dt.end_token, InstrumentKind.PLACE, dt))
                else: 
                    break
                res.end_token = dt.end_token
                i += 1
        elif (isinstance(t.get_referent(), DecreeReferent)): 
            res.referents = list()
            first_pass2918 = True
            while True:
                if first_pass2918: first_pass2918 = False
                else: t = t.next0_
                if (not (t is not None)): break
                if (t.is_comma_and): 
                    continue
                dr = (t.get_referent() if isinstance(t.get_referent(), DecreeReferent) else None)
                if (dr is None): 
                    break
                res.referents.append(dr)
                res.end_token = t
        elif (isinstance(t.get_referent(), PersonReferent) or isinstance(t.get_referent(), PersonPropertyReferent)): 
            res.referents = list()
            first_pass2919 = True
            while True:
                if first_pass2919: first_pass2919 = False
                else: t = t.next0_
                if (not (t is not None)): break
                if (t.is_comma_and): 
                    continue
                if (isinstance(t.get_referent(), PersonReferent) or isinstance(t.get_referent(), PersonPropertyReferent)): 
                    res.referents.append(t.get_referent())
                    res.end_token = t
                else: 
                    break
        if (len(res.children) == 0): 
            if (not res.begin_token.is_newline_before or not res.end_token.is_newline_after): 
                return None
        if (res.end_token.next0_ is not None and isinstance(res.end_token.next0_.get_referent(), DateReferent)): 
            dt = DecreeToken.try_attach(res.end_token.next0_, None, False)
            if (dt is not None): 
                res.children.append(FragToken._new1284(dt.begin_token, dt.end_token, InstrumentKind.DATE, dt))
                res.end_token = dt.end_token
                dt = DecreeToken.try_attach(res.end_token.next0_, None, False)
                if (dt is not None and dt.typ == DecreeToken.ItemType.NUMBER): 
                    res.children.append(FragToken._new1284(dt.begin_token, dt.end_token, InstrumentKind.NUMBER, dt))
                    res.end_token = dt.end_token
        t = res.end_token.next0_
        if (t is not None and t.is_comma): 
            t = t.next0_
        if (t is not None and t.is_value("ПРОТОКОЛ", None)): 
            dts = DecreeToken.try_attach_list(t, None, 10, False)
            if (dts is not None and len(dts) > 0): 
                res.end_token = dts[len(dts) - 1].end_token
        return res
    
    @staticmethod
    def _create_misc(t : 'Token') -> 'FragToken':
        from pullenti.ner.decree.internal.DecreeToken import DecreeToken
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.date.DateReferent import DateReferent
        if (t is None or t.next0_ is None): 
            return None
        if (t.is_value("ФОРМА", None) and t.next0_.is_value("ДОКУМЕНТА", None)): 
            num = DecreeToken.try_attach(t.next0_.next0_, None, False)
            if (num is not None and num.typ == DecreeToken.ItemType.NUMBER): 
                return FragToken._new1236(t, num.end_token, InstrumentKind.UNDEFINED)
            if (isinstance(t.next0_.next0_, NumberToken) and t.next0_.next0_.is_newline_after): 
                return FragToken._new1236(t, t.next0_.next0_, InstrumentKind.UNDEFINED)
        if (t.is_value("С", None) and t.next0_.is_value("ИЗМЕНЕНИЕ", None) and t.next0_.next0_ is not None): 
            tt = t.next0_.next0_
            if (tt.morph.class0_.is_preposition and tt.next0_ is not None): 
                tt = tt.next0_
            if (isinstance(tt.get_referent(), DateReferent)): 
                if (tt.next0_ is not None and tt.next0_.is_char('.')): 
                    tt = tt.next0_
                return FragToken._new1236(t, tt, InstrumentKind.UNDEFINED)
        return None
    
    @staticmethod
    def _create_editions(t : 'Token') -> 'FragToken':
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.ner.decree.internal.DecreeToken import DecreeToken
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.decree.internal.PartToken import PartToken
        from pullenti.ner.decree.DecreePartReferent import DecreePartReferent
        from pullenti.ner.decree.DecreeReferent import DecreeReferent
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.TextToken import TextToken
        if (t is None or t.next0_ is None): 
            return None
        t0 = t
        is_in_bracks = False
        if (t.is_value("СПИСОК", None)): 
            npt = NounPhraseHelper.try_parse(t.next0_, NounPhraseParseAttr.NO, 0)
            if (npt is not None and npt.noun.is_value("ДОКУМЕНТ", None)): 
                t = npt.end_token.next0_
                if (t is not None and t.is_char_of(":.")): 
                    t = t.next0_
                if (t is None): 
                    return None
        if (not t.is_char('(') and not t.is_value("ПРИЛОЖЕНИЕ", "ДОДАТОК")): 
            if (t.is_value("В", "У") and t.next0_ is not None and ((t.next0_.is_value("РЕДАКЦИЯ", "РЕДАКЦІЯ") or t.next0_.is_value("РЕД", None)))): 
                pass
            else: 
                return None
        else: 
            is_in_bracks = t.is_char('(')
            t = t.next0_
        ok = False
        dt = DecreeToken.try_attach(t, None, False)
        if (dt is not None and dt.typ == DecreeToken.ItemType.NUMBER): 
            t = dt.end_token.next0_
        elif (isinstance(t, NumberToken)): 
            t = t.next0_
        pt = PartToken.try_attach(t, None, False, True)
        if (pt is not None): 
            t = pt.end_token.next0_
        elif (is_in_bracks and isinstance(t.get_referent(), DecreePartReferent)): 
            t = t.next0_
        if (t is None): 
            return None
        is_doubt = False
        while ((t.morph.class0_.is_preposition or t.morph.class0_.is_adverb)) and t.next0_ is not None:
            t = t.next0_
        if (t.is_value("РЕДАКЦИЯ", "РЕДАКЦІЯ")): 
            ok = True
        elif (t.is_value("РЕД", None)): 
            ok = True
            if (t.next0_ is not None and t.next0_.is_char('.')): 
                t = t.next0_
        elif ((t.is_value("ИЗМ", None) or t.is_value("ИЗМЕНЕНИЕ", "ЗМІНА") or t.is_value("УЧЕТ", "ОБЛІК")) or t.is_value("ВКЛЮЧИТЬ", "ВКЛЮЧИТИ") or t.is_value("ДОПОЛНИТЬ", "ДОПОВНИТИ")): 
            if (t.is_value("УЧЕТ", "ОБЛІК")): 
                is_doubt = True
            ok = True
            t = t.next0_
            first_pass2920 = True
            while True:
                if first_pass2920: first_pass2920 = False
                else: t = t.next0_
                if (not (t is not None)): break
                if (t.next0_ is None): 
                    break
                if (t.is_char_of(",.")): 
                    continue
                if (t.is_value("ВНЕСЕННЫЙ", "ВНЕСЕНИЙ") or t.is_value("ПОПРАВКА", None)): 
                    continue
                t = t.previous
                break
        elif (isinstance(t.get_referent(), DecreeReferent)): 
            tt = (t if isinstance(t, MetaToken) else None).begin_token
            if (tt.is_value("В", "У") and tt.next0_ is not None): 
                tt = tt.next0_
            if (tt.is_value("РЕДАКЦИЯ", "РЕДАКЦІЯ")): 
                ok = True
            elif (tt.is_value("РЕД", None)): 
                ok = True
            t = t.previous
        if (not ok or t is None): 
            return None
        decrs = list()
        t = t.next0_
        first_pass2921 = True
        while True:
            if first_pass2921: first_pass2921 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (is_in_bracks): 
                if (t.is_char('(')): 
                    br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                    if (br is not None and (br.length_char < 200)): 
                        t = br.end_token
                        continue
                if (t.is_char(')')): 
                    break
            elif (t.is_char('.') or t.is_newline_after): 
                break
            dr = (t.get_referent() if isinstance(t.get_referent(), DecreeReferent) else None)
            if (dr is not None): 
                decrs.append(dr)
        if (t is None): 
            return None
        ok = False
        if (is_in_bracks): 
            ok = t.is_char(')')
            if (not t.is_newline_after): 
                if (isinstance(t.next0_, TextToken) and t.next0_.is_newline_after and not t.next0_.chars.is_letter): 
                    pass
                else: 
                    is_doubt = True
        elif (t.is_char('.') or t.is_newline_after): 
            ok = True
        if (len(decrs) > 0): 
            is_doubt = False
        if (ok and not is_doubt): 
            eds = FragToken._new1236(t0, t, InstrumentKind.EDITIONS)
            eds.referents = list()
            for d in decrs: 
                eds.referents.append(d)
            return eds
        return None
    
    @staticmethod
    def __create_owner(t : 'Token') -> 'FragToken':
        from pullenti.ner.decree.internal.DecreeToken import DecreeToken
        from pullenti.ner.date.DateReferent import DateReferent
        from pullenti.ner.address.AddressReferent import AddressReferent
        from pullenti.ner.address.StreetReferent import StreetReferent
        from pullenti.ner.phone.PhoneReferent import PhoneReferent
        from pullenti.ner.uri.UriReferent import UriReferent
        from pullenti.ner.person.PersonIdentityReferent import PersonIdentityReferent
        from pullenti.ner.bank.BankDataReferent import BankDataReferent
        from pullenti.ner.decree.DecreeReferent import DecreeReferent
        from pullenti.ner.decree.DecreePartReferent import DecreePartReferent
        from pullenti.morph.MorphClass import MorphClass
        from pullenti.ner.geo.GeoReferent import GeoReferent
        if (t is None or not t.is_newline_before): 
            return None
        if (not t.chars.is_cyrillic_letter or t.chars.is_all_lower): 
            return None
        t1 = None
        t11 = None
        ignore_cur_line = False
        tt = t
        first_pass2922 = True
        while True:
            if first_pass2922: first_pass2922 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            dt = DecreeToken.try_attach(tt, None, False)
            if (dt is not None): 
                if ((dt.typ != DecreeToken.ItemType.OWNER and dt.typ != DecreeToken.ItemType.ORG and dt.typ != DecreeToken.ItemType.UNKNOWN) and dt.typ != DecreeToken.ItemType.TERR and dt.typ != DecreeToken.ItemType.MISC): 
                    break
                tt = dt.end_token
                t1 = tt
                continue
            if (tt != t and tt.whitespaces_before_count > 15): 
                break
            r = tt.get_referent()
            if ((((isinstance(r, DateReferent) or isinstance(r, AddressReferent) or isinstance(r, StreetReferent)) or isinstance(r, PhoneReferent) or isinstance(r, UriReferent)) or isinstance(r, PersonIdentityReferent) or isinstance(r, BankDataReferent)) or isinstance(r, DecreeReferent) or isinstance(r, DecreePartReferent)): 
                ignore_cur_line = True
                t1 = t11
                break
            if (tt.morph.class0_ == MorphClass.VERB): 
                ignore_cur_line = True
                t1 = t11
                break
            if (isinstance(r, GeoReferent) and tt.is_newline_before): 
                break
            if (tt.is_newline_before): 
                t11 = t1
            t1 = tt
        if (t1 is None): 
            return None
        fr = FragToken._new1254(t, t1, InstrumentKind.ORGANIZATION, True)
        return fr
    
    def __calc_owner_coef(self, owner : 'FragToken') -> int:
        from pullenti.ner.decree.internal.DecreeToken import DecreeToken
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.decree.internal.PartToken import PartToken
        from pullenti.ner.core.MiscHelper import MiscHelper
        own_typs = list()
        own_name = None
        for ch in owner.children: 
            if (ch.kind == InstrumentKind.HEAD): 
                for chh in ch.children: 
                    if (chh.kind == InstrumentKind.TYP or chh.kind == InstrumentKind.NAME or chh.kind == InstrumentKind.KEYWORD): 
                        t = DecreeToken.is_keyword(chh.begin_token, False)
                        if (isinstance(t, TextToken)): 
                            own_typs.append((t if isinstance(t, TextToken) else None).get_lemma())
                        if (chh.kind == InstrumentKind.NAME and own_name is None): 
                            own_name = chh
        for ch in self.children: 
            if (ch.kind == InstrumentKind.HEAD): 
                for chh in ch.children: 
                    if (chh.kind == InstrumentKind.DOCREFERENCE): 
                        t = chh.begin_token
                        if (t.morph.class0_.is_preposition): 
                            t = t.next0_
                        tt = DecreeToken.is_keyword(t, False)
                        if (isinstance(tt, TextToken)): 
                            ty = (tt if isinstance(tt, TextToken) else None).get_lemma()
                            if (ty in own_typs): 
                                return 1
                            continue
                        pt = PartToken.try_attach(t, None, False, False)
                        if (pt is not None): 
                            if (pt.typ == PartToken.ItemType.APPENDIX): 
                                if (owner.number > 0): 
                                    for nn in pt.values: 
                                        if (nn.value == str(owner.number)): 
                                            return 3
                        if (own_name is not None and isinstance(own_name.value, str)): 
                            val0 = (own_name.value if isinstance(own_name.value, str) else None)
                            val1 = MiscHelper.get_text_value(t, chh.end_token, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)
                            if (val1 == val0): 
                                return 3
                            if (MiscHelper.can_be_equals(val0, val1, True, True, False)): 
                                return 3
                            if (val1 is not None and ((val1.startswith(val0) or val0.startswith(val1)))): 
                                return 1
        return 0
    
    @property
    def has_changes(self) -> bool:
        from pullenti.ner.decree.DecreeChangeReferent import DecreeChangeReferent
        if (isinstance(self.begin_token.get_referent(), DecreeChangeReferent)): 
            return True
        t = self.begin_token
        while t is not None and t.end_char <= self.end_char: 
            if (isinstance(t.get_referent(), DecreeChangeReferent)): 
                return True
            t = t.next0_
        return False
    
    @property
    def multiline_changes_value(self) -> 'MetaToken':
        from pullenti.ner.decree.DecreeChangeReferent import DecreeChangeReferent
        from pullenti.ner.decree.DecreeChangeValueReferent import DecreeChangeValueReferent
        from pullenti.ner.core.BracketHelper import BracketHelper
        t = self.begin_token
        while t is not None and (t.begin_char < self.end_char): 
            if (isinstance(t.get_referent(), DecreeChangeReferent)): 
                dcr = (t.get_referent() if isinstance(t.get_referent(), DecreeChangeReferent) else None)
                tt = (t if isinstance(t, MetaToken) else None).begin_token
                first_pass2923 = True
                while True:
                    if first_pass2923: first_pass2923 = False
                    else: tt = tt.next0_
                    if (not (tt is not None and tt.end_char <= t.end_char)): break
                    dval = (tt.get_referent() if isinstance(tt.get_referent(), DecreeChangeValueReferent) else None)
                    if (dval is None or dval.kind != DecreeChangeValueKind.TEXT): 
                        continue
                    val = dval.value
                    if (val is None or (len(val) < 100)): 
                        continue
                    if ((('\r') not in val) and (('\n') not in val) and not tt.is_newline_before): 
                        continue
                    t0 = None
                    t = (tt if isinstance(tt, MetaToken) else None).begin_token
                    while t is not None and t.end_char <= tt.end_char: 
                        if (BracketHelper.is_bracket(t, True) and ((t.is_whitespace_before or t.previous.is_char(':')))): 
                            t0 = t.next0_
                            break
                        elif (t.previous is not None and t.previous.is_char(':') and t.is_newline_before): 
                            t0 = t
                            break
                        t = t.next0_
                    t1 = (tt if isinstance(tt, MetaToken) else None).end_token
                    if (BracketHelper.is_bracket(t1, True)): 
                        t1 = t1.previous
                    if (t0 is not None and ((t0.end_char + 50) < t1.end_char)): 
                        return MetaToken._new825(t0, t1, dcr)
                    return None
            if (t.end_char > self.end_char): 
                break
            t = t.next0_
        return None

    
    @staticmethod
    def _new1236(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'InstrumentKind') -> 'FragToken':
        res = FragToken(_arg1, _arg2)
        res.kind = _arg3
        return res
    
    @staticmethod
    def _new1237(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'InstrToken1', _arg4 : bool) -> 'FragToken':
        res = FragToken(_arg1, _arg2)
        res._itok = _arg3
        res.is_expired = _arg4
        return res
    
    @staticmethod
    def _new1238(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'InstrumentKind', _arg4 : bool, _arg5 : 'InstrToken1') -> 'FragToken':
        res = FragToken(_arg1, _arg2)
        res.kind = _arg3
        res._def_val2 = _arg4
        res._itok = _arg5
        return res
    
    @staticmethod
    def _new1244(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'InstrToken1') -> 'FragToken':
        res = FragToken(_arg1, _arg2)
        res._itok = _arg3
        return res
    
    @staticmethod
    def _new1245(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'InstrumentKind', _arg4 : 'InstrToken1') -> 'FragToken':
        res = FragToken(_arg1, _arg2)
        res.kind = _arg3
        res._itok = _arg4
        return res
    
    @staticmethod
    def _new1252(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'InstrumentKind', _arg4 : int) -> 'FragToken':
        res = FragToken(_arg1, _arg2)
        res.kind = _arg3
        res.number = _arg4
        return res
    
    @staticmethod
    def _new1254(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'InstrumentKind', _arg4 : bool) -> 'FragToken':
        res = FragToken(_arg1, _arg2)
        res.kind = _arg3
        res._def_val2 = _arg4
        return res
    
    @staticmethod
    def _new1257(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'InstrumentKind', _arg4 : bool) -> 'FragToken':
        res = FragToken(_arg1, _arg2)
        res.kind = _arg3
        res._def_val = _arg4
        return res
    
    @staticmethod
    def _new1269(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'InstrumentKind', _arg4 : object, _arg5 : 'InstrToken1') -> 'FragToken':
        res = FragToken(_arg1, _arg2)
        res.kind = _arg3
        res.value = _arg4
        res._itok = _arg5
        return res
    
    @staticmethod
    def _new1274(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'InstrumentKind', _arg4 : int, _arg5 : bool, _arg6 : typing.List['Referent']) -> 'FragToken':
        res = FragToken(_arg1, _arg2)
        res.kind = _arg3
        res.number = _arg4
        res.is_expired = _arg5
        res.referents = _arg6
        return res
    
    @staticmethod
    def _new1284(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'InstrumentKind', _arg4 : object) -> 'FragToken':
        res = FragToken(_arg1, _arg2)
        res.kind = _arg3
        res.value = _arg4
        return res
    
    @staticmethod
    def _new1374(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'InstrumentReferent', _arg4 : 'InstrumentKind') -> 'FragToken':
        res = FragToken(_arg1, _arg2)
        res._m_doc = _arg3
        res.kind = _arg4
        return res
    
    @staticmethod
    def _new1444(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'InstrumentKind', _arg4 : bool, _arg5 : 'InstrToken1') -> 'FragToken':
        res = FragToken(_arg1, _arg2)
        res.kind = _arg3
        res._def_val = _arg4
        res._itok = _arg5
        return res
    
    # static constructor for class FragToken
    @staticmethod
    def _static_ctor():
        FragToken.__m_zapiska_keywords = ["ЗАЯВЛЕНИЕ", "ЗАПИСКА", "РАПОРТ", "ДОКЛАД", "ОТЧЕТ"]

FragToken._static_ctor()