# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.Token import Token
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.person.PersonReferent import PersonReferent
from pullenti.ner.org.OrganizationKind import OrganizationKind
from pullenti.ner.uri.UriReferent import UriReferent
from pullenti.ner.org.OrganizationReferent import OrganizationReferent
from pullenti.ner.date.DateReferent import DateReferent
from pullenti.ner.titlepage.internal.PersonRelations import PersonRelations
from pullenti.ner.Referent import Referent
from pullenti.ner.titlepage.TitlePageReferent import TitlePageReferent
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.booklink.internal.EpNerBooklinkInternalResourceHelper import EpNerBooklinkInternalResourceHelper
from pullenti.ner.TextAnnotation import TextAnnotation
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.titlepage.internal.MetaTitleInfo import MetaTitleInfo
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.core.Termin import Termin
from pullenti.ner.titlepage.internal.TitleItemToken import TitleItemToken
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.Analyzer import Analyzer
from pullenti.ner.date.DateAnalyzer import DateAnalyzer
from pullenti.ner.titlepage.internal.Line import Line
from pullenti.ner.titlepage.internal.TitleNameToken import TitleNameToken

class TitlePageAnalyzer(Analyzer):
    """ Семантический анализатор заголовочной информации """
    
    @property
    def name(self) -> str:
        return TitlePageAnalyzer.ANALYZER_NAME
    
    ANALYZER_NAME = "TITLEPAGE"
    
    @property
    def caption(self) -> str:
        return "Титульный лист"
    
    @property
    def description(self) -> str:
        return "Информация из титульных страниц и из заголовков статей, научных работ, дипломов и т.д."
    
    def clone(self) -> 'Analyzer':
        return TitlePageAnalyzer()
    
    @property
    def is_specific(self) -> bool:
        """ Этот анализатор является специфическим """
        return True
    
    @property
    def progress_weight(self) -> int:
        return 1
    
    @property
    def type_system(self) -> typing.List['ReferentClass']:
        return [MetaTitleInfo._global_meta]
    
    @property
    def images(self) -> typing.List[tuple]:
        res = dict()
        res[MetaTitleInfo.TITLE_INFO_IMAGE_ID] = EpNerBooklinkInternalResourceHelper.getBytes("titleinfo.png")
        return res
    
    def createReferent(self, type0_ : str) -> 'Referent':
        if (type0_ == TitlePageReferent.OBJ_TYPENAME): 
            return TitlePageReferent()
        return None
    
    def processReferent1(self, begin : 'Token', end : 'Token') -> 'ReferentToken':
        wrapet2529 = RefOutArgWrapper(None)
        tpr = TitlePageAnalyzer._process(begin, (0 if end is None else end.end_char), begin.kit, wrapet2529)
        et = wrapet2529.value
        if (tpr is None): 
            return None
        return ReferentToken(tpr, begin, et)
    
    def process(self, kit : 'AnalysisKit') -> None:
        ad = kit.getAnalyzerData(self)
        wrapet2530 = RefOutArgWrapper(None)
        tpr = TitlePageAnalyzer._process(kit.first_token, 0, kit, wrapet2530)
        et = wrapet2530.value
        if (tpr is not None): 
            ad.registerReferent(tpr)
    
    @staticmethod
    def _process(begin : 'Token', max_char_pos : int, kit : 'AnalysisKit', end_token : 'Token') -> 'TitlePageReferent':
        end_token.value = begin
        res = TitlePageReferent()
        term = None
        lines = Line.parse(begin, 30, 1500, max_char_pos)
        if (len(lines) < 1): 
            return None
        cou = len(lines)
        min_newlines_count = 10
        lines_count_stat = dict()
        i = 0
        while i < len(lines): 
            if (TitleNameToken.canBeStartOfTextOrContent(lines[i].begin_token, lines[i].end_token)): 
                cou = i
                break
            j = lines[i].newlines_before_count
            if (i > 0 and j > 0): 
                if (not j in lines_count_stat): 
                    lines_count_stat[j] = 1
                else: 
                    lines_count_stat[j] += 1
            i += 1
        max0_ = 0
        for kp in lines_count_stat.items(): 
            if (kp[1] > max0_): 
                max0_ = kp[1]
                min_newlines_count = kp[0]
        end_char = (lines[cou - 1].end_char if cou > 0 else 0)
        if (max_char_pos > 0 and end_char > max_char_pos): 
            end_char = max_char_pos
        names = list()
        i = 0
        while i < cou: 
            if (i == 6): 
                pass
            j = i
            while (j < cou) and (j < (i + 5)): 
                if (i == 6 and j == 8): 
                    pass
                if (j > i): 
                    if (lines[j - 1].is_pure_en and lines[j].is_pure_ru): 
                        break
                    if (lines[j - 1].is_pure_ru and lines[j].is_pure_en): 
                        break
                    if (lines[j].newlines_before_count >= (min_newlines_count * 2)): 
                        break
                ttt = TitleNameToken.tryParse(lines[i].begin_token, lines[j].end_token, min_newlines_count)
                if (ttt is not None): 
                    if (lines[i].is_pure_en): 
                        ttt.morph.language = MorphLang.EN
                    elif (lines[i].is_pure_ru): 
                        ttt.morph.language = MorphLang.RU
                    names.append(ttt)
                j += 1
            i += 1
        TitleNameToken.sort(names)
        name_rt = None
        if (len(names) > 0): 
            i0 = 0
            if (names[i0].morph.language.is_en): 
                ii = 1
                while ii < len(names): 
                    if (names[ii].morph.language.is_ru and names[ii].rank > 0): 
                        i0 = ii
                        break
                    ii += 1
            term = res._addName(names[i0].begin_name_token, names[i0].end_name_token)
            if (names[i0].type_value is not None): 
                res._addType(names[i0].type_value)
            if (names[i0].speciality is not None): 
                res.speciality = names[i0].speciality
            rt = ReferentToken(res, names[i0].begin_token, names[i0].end_token)
            if (kit is not None): 
                kit.embedToken(rt)
            else: 
                res.addOccurence(TextAnnotation(rt.begin_token, rt.end_token))
            end_token.value = rt.end_token
            name_rt = rt
            if (begin.begin_char == rt.begin_char): 
                begin = (rt)
        if (term is not None and kit is not None): 
            t = kit.first_token
            first_pass3140 = True
            while True:
                if first_pass3140: first_pass3140 = False
                else: t = t.next0_
                if (not (t is not None)): break
                tok = term.tryParse(t, TerminParseAttr.NO)
                if (tok is None): 
                    continue
                t0 = t
                t1 = tok.end_token
                if (t1.next0_ is not None and t1.next0_.isChar('.')): 
                    t1 = t1.next0_
                if (BracketHelper.canBeStartOfSequence(t0.previous, False, False) and BracketHelper.canBeEndOfSequence(t1.next0_, False, None, False)): 
                    t0 = t0.previous
                    t1 = t1.next0_
                rt = ReferentToken(res, t0, t1)
                kit.embedToken(rt)
                t = (rt)
        pr = PersonRelations()
        pers_typ = TitleItemToken.Types.UNDEFINED
        pers_types = pr.rel_types
        t = begin
        first_pass3141 = True
        while True:
            if first_pass3141: first_pass3141 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (max_char_pos > 0 and t.begin_char > max_char_pos): 
                break
            if (t == name_rt): 
                continue
            tpt = TitleItemToken.tryAttach(t)
            if (tpt is not None): 
                pers_typ = TitleItemToken.Types.UNDEFINED
                if (tpt.typ == TitleItemToken.Types.TYP): 
                    if (len(res.types) == 0): 
                        res._addType(tpt.value)
                    elif (len(res.types) == 1): 
                        ty = res.types[0].upper()
                        if (ty == "РЕФЕРАТ"): 
                            res._addType(tpt.value)
                        elif (ty == "АВТОРЕФЕРАТ"): 
                            if (tpt.value == "КАНДИДАТСКАЯ ДИССЕРТАЦИЯ"): 
                                res.addSlot(TitlePageReferent.ATTR_TYPE, "автореферат кандидатской диссертации", True, 0)
                            elif (tpt.value == "ДОКТОРСКАЯ ДИССЕРТАЦИЯ"): 
                                res.addSlot(TitlePageReferent.ATTR_TYPE, "автореферат докторской диссертации", True, 0)
                            elif (tpt.value == "МАГИСТЕРСКАЯ ДИССЕРТАЦИЯ"): 
                                res.addSlot(TitlePageReferent.ATTR_TYPE, "автореферат магистерской диссертации", True, 0)
                            elif (tpt.value == "КАНДИДАТСЬКА ДИСЕРТАЦІЯ"): 
                                res.addSlot(TitlePageReferent.ATTR_TYPE, "автореферат кандидатської дисертації", True, 0)
                            elif (tpt.value == "ДОКТОРСЬКА ДИСЕРТАЦІЯ"): 
                                res.addSlot(TitlePageReferent.ATTR_TYPE, "автореферат докторської дисертації", True, 0)
                            elif (tpt.value == "МАГІСТЕРСЬКА ДИСЕРТАЦІЯ"): 
                                res.addSlot(TitlePageReferent.ATTR_TYPE, "автореферат магістерської дисертації", True, 0)
                            else: 
                                res._addType(tpt.value)
                        elif (tpt.value == "РЕФЕРАТ" or tpt.value == "АВТОРЕФЕРАТ"): 
                            if (not tpt.value in ty): 
                                res._addType(tpt.value)
                elif (tpt.typ == TitleItemToken.Types.SPECIALITY): 
                    if (res.speciality is None): 
                        res.speciality = tpt.value
                elif (tpt.typ in pers_types): 
                    pers_typ = tpt.typ
                t = tpt.end_token
                if (t.end_char > end_token.value.end_char): 
                    end_token.value = t
                if (t.next0_ is not None and t.next0_.isCharOf(":-")): 
                    t = t.next0_
                continue
            if (t.end_char > end_char): 
                break
            rli = t.getReferents()
            if (rli is None): 
                continue
            if (not t.is_newline_before and (isinstance(t.previous, TextToken))): 
                s = (t.previous).term
                if (s == "ИМЕНИ" or s == "ИМ"): 
                    continue
                if (s == "." and t.previous.previous is not None and t.previous.previous.isValue("ИМ", None)): 
                    continue
            for r in rli: 
                if (isinstance(r, PersonReferent)): 
                    if (r != rli[0]): 
                        continue
                    p = Utils.asObjectOrNull(r, PersonReferent)
                    if (pers_typ != TitleItemToken.Types.UNDEFINED): 
                        if (t.previous is not None and t.previous.isChar('.')): 
                            pers_typ = TitleItemToken.Types.UNDEFINED
                    typ = pr.calcTypFromAttrs(p)
                    if (typ != TitleItemToken.Types.UNDEFINED): 
                        pr.add(p, typ, 1)
                        pers_typ = typ
                    elif (pers_typ != TitleItemToken.Types.UNDEFINED): 
                        pr.add(p, pers_typ, 1)
                    elif (t.previous is not None and t.previous.isChar('©')): 
                        pers_typ = TitleItemToken.Types.WORKER
                        pr.add(p, pers_typ, 1)
                    else: 
                        tt = t.next0_
                        first_pass3142 = True
                        while True:
                            if first_pass3142: first_pass3142 = False
                            else: tt = tt.next0_
                            if (not (tt is not None)): break
                            rr = tt.getReferent()
                            if (rr == res): 
                                pers_typ = TitleItemToken.Types.WORKER
                                break
                            if (isinstance(rr, PersonReferent)): 
                                if (pr.calcTypFromAttrs(Utils.asObjectOrNull(r, PersonReferent)) != TitleItemToken.Types.UNDEFINED): 
                                    break
                                else: 
                                    continue
                            if (rr is not None): 
                                break
                            tpt = TitleItemToken.tryAttach(tt)
                            if (tpt is not None): 
                                if (tpt.typ != TitleItemToken.Types.TYP and tpt.typ != TitleItemToken.Types.TYPANDTHEME): 
                                    break
                                tt = tpt.end_token
                                if (tt.end_char > end_token.value.end_char): 
                                    end_token.value = tt
                                continue
                        if (pers_typ == TitleItemToken.Types.UNDEFINED): 
                            tt = t.previous
                            while tt is not None: 
                                rr = tt.getReferent()
                                if (rr == res): 
                                    pers_typ = TitleItemToken.Types.WORKER
                                    break
                                if (rr is not None): 
                                    break
                                if ((tt.isValue("СТУДЕНТ", None) or tt.isValue("СТУДЕНТКА", None) or tt.isValue("СЛУШАТЕЛЬ", None)) or tt.isValue("ДИПЛОМНИК", None) or tt.isValue("ИСПОЛНИТЕЛЬ", None)): 
                                    pers_typ = TitleItemToken.Types.WORKER
                                    break
                                tpt = TitleItemToken.tryAttach(tt)
                                if (tpt is not None and tpt.typ != TitleItemToken.Types.TYP): 
                                    break
                                tt = tt.previous
                        if (pers_typ != TitleItemToken.Types.UNDEFINED): 
                            pr.add(p, pers_typ, 1)
                        else: 
                            pr.add(p, pers_typ, .5)
                        if (t.end_char > end_token.value.end_char): 
                            end_token.value = t
                    continue
                if (r == rli[0]): 
                    pers_typ = TitleItemToken.Types.UNDEFINED
                if (isinstance(r, DateReferent)): 
                    if (res.date is None): 
                        res.date = Utils.asObjectOrNull(r, DateReferent)
                        if (t.end_char > end_token.value.end_char): 
                            end_token.value = t
                elif (isinstance(r, GeoReferent)): 
                    if (res.city is None and (r).is_city): 
                        res.city = Utils.asObjectOrNull(r, GeoReferent)
                        if (t.end_char > end_token.value.end_char): 
                            end_token.value = t
                if (isinstance(r, OrganizationReferent)): 
                    org0_ = Utils.asObjectOrNull(r, OrganizationReferent)
                    if ("курс" in org0_.types and org0_.number is not None): 
                        wrapi2531 = RefOutArgWrapper(0)
                        inoutres2532 = Utils.tryParseInt(org0_.number, wrapi2531)
                        i = wrapi2531.value
                        if (inoutres2532): 
                            if (i > 0 and (i < 8)): 
                                res.student_year = i
                    while org0_.higher is not None: 
                        if (org0_.kind != OrganizationKind.DEPARTMENT): 
                            break
                        org0_ = org0_.higher
                    if (org0_.kind != OrganizationKind.DEPARTMENT): 
                        if (res.org0_ is None): 
                            res.org0_ = org0_
                        elif (OrganizationReferent.canBeHigher(res.org0_, org0_)): 
                            res.org0_ = org0_
                    if (t.end_char > end_token.value.end_char): 
                        end_token.value = t
                if ((isinstance(r, UriReferent)) or (isinstance(r, GeoReferent))): 
                    if (t.end_char > end_token.value.end_char): 
                        end_token.value = t
        for ty in pers_types: 
            for p in pr.getPersons(ty): 
                if (pr.getAttrNameForType(ty) is not None): 
                    res.addSlot(pr.getAttrNameForType(ty), p, False, 0)
        if (res.getSlotValue(TitlePageReferent.ATTR_AUTHOR) is None): 
            for p in pr.getPersons(TitleItemToken.Types.UNDEFINED): 
                res.addSlot(TitlePageReferent.ATTR_AUTHOR, p, False, 0)
                break
        if (res.city is None and res.org0_ is not None): 
            s = res.org0_.findSlot(OrganizationReferent.ATTR_GEO, None, True)
            if (s is not None and (isinstance(s.value, GeoReferent))): 
                if ((s.value).is_city): 
                    res.city = Utils.asObjectOrNull(s.value, GeoReferent)
        if (res.date is None): 
            t = begin
            first_pass3143 = True
            while True:
                if first_pass3143: first_pass3143 = False
                else: t = t.next0_
                if (not (t is not None and t.end_char <= end_char)): break
                city = Utils.asObjectOrNull(t.getReferent(), GeoReferent)
                if (city is None): 
                    continue
                if (isinstance(t.next0_, TextToken)): 
                    if (t.next0_.isCharOf(":,") or t.next0_.is_hiphen): 
                        t = t.next0_
                rt = t.kit.processReferent(DateAnalyzer.ANALYZER_NAME, t.next0_)
                if (rt is not None): 
                    rt.saveToLocalOntology()
                    res.date = Utils.asObjectOrNull(rt.referent, DateReferent)
                    if (kit is not None): 
                        kit.embedToken(rt)
                    break
        if (len(res.slots) == 0): 
            return None
        else: 
            return res
    
    @staticmethod
    def initialize() -> None:
        MetaTitleInfo.initialize()
        try: 
            Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = True
            TitleItemToken.initialize()
            Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = False
        except Exception as ex: 
            raise Utils.newException(ex.__str__(), ex)
        ProcessorService.registerAnalyzer(TitlePageAnalyzer())