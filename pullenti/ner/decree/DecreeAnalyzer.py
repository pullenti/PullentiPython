# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import typing
import datetime
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.ner.Analyzer import Analyzer
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.core.internal.EpNerCoreInternalResourceHelper import EpNerCoreInternalResourceHelper
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.decree.DecreeKind import DecreeKind
from pullenti.ner.decree.internal.DecreeChangeTokenTyp import DecreeChangeTokenTyp
from pullenti.ner.decree.DecreeChangeKind import DecreeChangeKind
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.Slot import Slot


class DecreeAnalyzer(Analyzer):
    
    class ThisDecree(MetaToken):
        
        def __init__(self, b : 'Token', e0_ : 'Token') -> None:
            super().__init__(b, e0_, None)
            self.typ = None;
            self.has_this_ref = False
            self.has_other_ref = False
            self.real = None;
        
        def __str__(self) -> str:
            return "{0} ({1})".format(Utils.ifNotNull(self.typ, "?"), ("This" if self.has_this_ref else (("Other" if self.has_other_ref else "?"))))
        
        @staticmethod
        def tryAttachBack(t : 'Token', base_typ : 'DecreeToken') -> 'ThisDecree':
            from pullenti.ner.decree.internal.DecreeToken import DecreeToken
            from pullenti.ner.TextToken import TextToken
            if (t is None): 
                return None
            ukaz = None
            tt = t
            first_pass2866 = True
            while True:
                if first_pass2866: first_pass2866 = False
                else: tt = tt.previous
                if (not (tt is not None)): break
                if (tt.isCharOf(",") or tt.morph.class0_.is_preposition or tt.morph.class0_.is_conjunction): 
                    continue
                if ((((((tt.isValue("ОПРЕДЕЛЕННЫЙ", "ПЕВНИЙ") or tt.isValue("ЗАДАННЫЙ", "ЗАДАНИЙ") or tt.isValue("ПРЕДУСМОТРЕННЫЙ", "ПЕРЕДБАЧЕНИЙ")) or tt.isValue("УКАЗАННЫЙ", "ЗАЗНАЧЕНИЙ") or tt.isValue("ПЕРЕЧИСЛЕННЫЙ", "ПЕРЕРАХОВАНИЙ")) or tt.isValue("ОПРЕДЕЛИТЬ", "ВИЗНАЧИТИ") or tt.isValue("ОПРЕДЕЛЯТЬ", None)) or tt.isValue("ЗАДАВАТЬ", "ЗАДАВАТИ") or tt.isValue("ПРЕДУСМАТРИВАТЬ", "ПЕРЕДБАЧАТИ")) or tt.isValue("УКАЗЫВАТЬ", "ВКАЗУВАТИ") or tt.isValue("УКАЗАТЬ", "ВКАЗАТИ")) or tt.isValue("СИЛА", "ЧИННІСТЬ")): 
                    ukaz = tt
                    continue
                if (tt == t): 
                    continue
                ttt = DecreeToken.isKeyword(tt, False)
                if (tt != ttt or not ((isinstance(tt, TextToken)))): 
                    break
                if (ttt.isValue("УСЛОВИЕ", None)): 
                    continue
                if (ttt.isValue("ПОРЯДОК", None) and ukaz is not None): 
                    return None
                res = DecreeAnalyzer.ThisDecree(tt, tt)
                res.typ = (Utils.asObjectOrNull(tt, TextToken)).getLemma()
                t = tt.previous
                if (t is not None and ((t.morph.class0_.is_adjective or t.morph.class0_.is_pronoun))): 
                    if (t.isValue("НАСТОЯЩИЙ", "СПРАВЖНІЙ") or t.isValue("ТЕКУЩИЙ", "ПОТОЧНИЙ") or t.isValue("ДАННЫЙ", "ДАНИЙ")): 
                        res.has_this_ref = True
                        res.begin_token = t
                    elif ((t.isValue("ЭТОТ", "ЦЕЙ") or t.isValue("ВЫШЕУКАЗАННЫЙ", "ВИЩЕВКАЗАНИЙ") or t.isValue("УКАЗАННЫЙ", "ЗАЗНАЧЕНИЙ")) or t.isValue("НАЗВАННЫЙ", "НАЗВАНИЙ")): 
                        res.has_other_ref = True
                        res.begin_token = t
                if (not res.has_this_ref and tt.is_newline_after): 
                    return None
                if (base_typ is not None and base_typ.value == res.typ): 
                    res.has_this_ref = True
                return res
            if (ukaz is not None): 
                if (base_typ is not None and base_typ.value is not None and (("ДОГОВОР" in base_typ.value or "ДОГОВІР" in base_typ.value))): 
                    return DecreeAnalyzer.ThisDecree._new1097(ukaz, ukaz, True, base_typ.value)
            return None
        
        @staticmethod
        def tryAttach(dtok : 'PartToken', base_typ : 'DecreeToken') -> 'ThisDecree':
            from pullenti.ner.decree.DecreeReferent import DecreeReferent
            from pullenti.ner.decree.internal.DecreeToken import DecreeToken
            from pullenti.ner.core.BracketHelper import BracketHelper
            from pullenti.ner.TextToken import TextToken
            from pullenti.ner.ReferentToken import ReferentToken
            from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
            from pullenti.morph.MorphClass import MorphClass
            t = dtok.end_token.next0_
            if (t is None): 
                return None
            if (t.is_newline_before): 
                if (t.chars.is_cyrillic_letter and t.chars.is_all_lower): 
                    pass
                else: 
                    return None
            t0 = t
            if (t.isChar('.') and t.next0_ is not None and not t.is_newline_after): 
                if (dtok.is_newline_before): 
                    return None
                t = t.next0_
            if (t.isValue("К", None) and t.next0_ is not None): 
                t = t.next0_
            if (t is not None and (isinstance(t.getReferent(), DecreeReferent))): 
                return None
            tt = DecreeToken.isKeyword(t, False)
            br = False
            if (tt is None and BracketHelper.canBeStartOfSequence(t, True, False)): 
                tt = DecreeToken.isKeyword(t.next0_, False)
                if ((isinstance(tt, TextToken)) and BracketHelper.canBeEndOfSequence(tt.next0_, False, None, False)): 
                    br = True
            if (not ((isinstance(tt, TextToken)))): 
                if ((isinstance(tt, ReferentToken)) and (isinstance(tt.getReferent(), DecreeReferent))): 
                    return DecreeAnalyzer.ThisDecree._new1098(t, tt, Utils.asObjectOrNull(tt.getReferent(), DecreeReferent))
                return None
            if (tt.chars.is_all_lower): 
                if (DecreeToken.isKeyword(tt, True) is not None): 
                    if (tt != t and t.chars.is_capital_upper): 
                        pass
                    else: 
                        return None
            if (not ((isinstance(t, TextToken)))): 
                return None
            res = DecreeAnalyzer.ThisDecree(t0, (tt.next0_ if br else tt))
            res.typ = (Utils.asObjectOrNull(tt, TextToken)).getLemma()
            if (isinstance(tt.previous, TextToken)): 
                tt1 = tt.previous
                mc = tt1.getMorphClassInDictionary()
                if (mc.is_adjective and not mc.is_verb and not tt1.isValue("НАСТОЯЩИЙ", "СПРАВЖНІЙ")): 
                    nnn = NounPhraseHelper.tryParse(tt1, NounPhraseParseAttr.NO, 0)
                    if (nnn is not None): 
                        res.typ = nnn.getNormalCaseText(MorphClass(), False, MorphGender.UNDEFINED, False)
                    if (isinstance(tt1.previous, TextToken)): 
                        tt1 = tt1.previous
                        mc = tt1.getMorphClassInDictionary()
                        if (mc.is_adjective and not mc.is_verb and not tt1.isValue("НАСТОЯЩИЙ", "СПРАВЖНІЙ")): 
                            nnn = NounPhraseHelper.tryParse(tt1, NounPhraseParseAttr.NO, 0)
                            if (nnn is not None): 
                                res.typ = nnn.getNormalCaseText(MorphClass(), False, MorphGender.UNDEFINED, False)
            if (tt.isChar('.') and (isinstance(tt.previous, TextToken))): 
                res.typ = (Utils.asObjectOrNull(tt.previous, TextToken)).getLemma()
            if (t.morph.class0_.is_adjective or t.morph.class0_.is_pronoun): 
                if (t.isValue("НАСТОЯЩИЙ", "СПРАВЖНІЙ") or t.isValue("ТЕКУЩИЙ", "ПОТОЧНИЙ") or t.isValue("ДАННЫЙ", "ДАНИЙ")): 
                    res.has_this_ref = True
                elif ((t.isValue("ЭТОТ", "ЦЕЙ") or t.isValue("ВЫШЕУКАЗАННЫЙ", "ВИЩЕВКАЗАНИЙ") or t.isValue("УКАЗАННЫЙ", "ЗАЗНАЧЕНИЙ")) or t.isValue("НАЗВАННЫЙ", "НАЗВАНИЙ")): 
                    res.has_other_ref = True
            if (not tt.is_newline_after and not res.has_this_ref): 
                dt = DecreeToken.tryAttach(tt.next0_, None, False)
                if (dt is not None and dt.typ != DecreeToken.ItemType.MISC): 
                    return None
                if (DecreeToken.tryAttachName(tt.next0_, res.typ, False, False) is not None): 
                    return None
            if (base_typ is not None and base_typ.value == res.typ): 
                res.has_this_ref = True
            return res
        
        @staticmethod
        def _new1097(_arg1 : 'Token', _arg2 : 'Token', _arg3 : bool, _arg4 : str) -> 'ThisDecree':
            res = DecreeAnalyzer.ThisDecree(_arg1, _arg2)
            res.has_this_ref = _arg3
            res.typ = _arg4
            return res
        
        @staticmethod
        def _new1098(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'DecreeReferent') -> 'ThisDecree':
            res = DecreeAnalyzer.ThisDecree(_arg1, _arg2)
            res.real = _arg3
            return res
    
    ANALYZER_NAME = "DECREE"
    
    @property
    def name(self) -> str:
        return DecreeAnalyzer.ANALYZER_NAME
    
    @property
    def caption(self) -> str:
        return "Законы и указы"
    
    @property
    def description(self) -> str:
        return "Законы, указы, постановления, распоряжения и т.п."
    
    def clone(self) -> 'Analyzer':
        return DecreeAnalyzer()
    
    @property
    def type_system(self) -> typing.List['ReferentClass']:
        from pullenti.ner.decree.internal.MetaDecree import MetaDecree
        from pullenti.ner.decree.internal.MetaDecreePart import MetaDecreePart
        from pullenti.ner.decree.internal.MetaDecreeChange import MetaDecreeChange
        from pullenti.ner.decree.internal.MetaDecreeChangeValue import MetaDecreeChangeValue
        return [MetaDecree.GLOBAL_META, MetaDecreePart.GLOBAL_META, MetaDecreeChange.GLOBAL_META, MetaDecreeChangeValue.GLOBAL_META]
    
    @property
    def images(self) -> typing.List[tuple]:
        from pullenti.ner.decree.internal.MetaDecree import MetaDecree
        from pullenti.ner.decree.internal.MetaDecreePart import MetaDecreePart
        from pullenti.ner.decree.internal.MetaDecreeChange import MetaDecreeChange
        from pullenti.ner.decree.internal.MetaDecreeChangeValue import MetaDecreeChangeValue
        res = dict()
        res[MetaDecree.DECREE_IMAGE_ID] = EpNerCoreInternalResourceHelper.getBytes("decree.png")
        res[MetaDecree.STANDADR_IMAGE_ID] = EpNerCoreInternalResourceHelper.getBytes("decreestd.png")
        res[MetaDecreePart.PART_IMAGE_ID] = EpNerCoreInternalResourceHelper.getBytes("part.png")
        res[MetaDecreePart.PART_LOC_IMAGE_ID] = EpNerCoreInternalResourceHelper.getBytes("document_into.png")
        res[MetaDecree.PUBLISH_IMAGE_ID] = EpNerCoreInternalResourceHelper.getBytes("publish.png")
        res[MetaDecreeChange.IMAGE_ID] = EpNerCoreInternalResourceHelper.getBytes("decreechange.png")
        res[MetaDecreeChangeValue.IMAGE_ID] = EpNerCoreInternalResourceHelper.getBytes("decreechangevalue.png")
        return res
    
    @property
    def used_extern_object_types(self) -> typing.List[str]:
        from pullenti.ner.date.DateReferent import DateReferent
        from pullenti.ner.geo.GeoReferent import GeoReferent
        from pullenti.ner.org.OrganizationReferent import OrganizationReferent
        from pullenti.ner.person.PersonReferent import PersonReferent
        return [DateReferent.OBJ_TYPENAME, GeoReferent.OBJ_TYPENAME, OrganizationReferent.OBJ_TYPENAME, PersonReferent.OBJ_TYPENAME]
    
    def createReferent(self, type0_ : str) -> 'Referent':
        from pullenti.ner.decree.DecreeReferent import DecreeReferent
        from pullenti.ner.decree.DecreePartReferent import DecreePartReferent
        from pullenti.ner.decree.DecreeChangeReferent import DecreeChangeReferent
        from pullenti.ner.decree.DecreeChangeValueReferent import DecreeChangeValueReferent
        if (type0_ == DecreeReferent.OBJ_TYPENAME): 
            return DecreeReferent()
        if (type0_ == DecreePartReferent.OBJ_TYPENAME): 
            return DecreePartReferent()
        if (type0_ == DecreeChangeReferent.OBJ_TYPENAME): 
            return DecreeChangeReferent()
        if (type0_ == DecreeChangeValueReferent.OBJ_TYPENAME): 
            return DecreeChangeValueReferent()
        return None
    
    @property
    def progress_weight(self) -> int:
        return 10
    
    def process(self, kit : 'AnalysisKit') -> None:
        """ Основная функция выделения дат
        
        Args:
            cnt: 
            stage: 
        
        """
        from pullenti.ner.core.TerminCollection import TerminCollection
        from pullenti.ner.decree.internal.DecreeToken import DecreeToken
        from pullenti.ner.decree.internal.PartToken import PartToken
        from pullenti.ner.Referent import Referent
        from pullenti.ner.decree.DecreeReferent import DecreeReferent
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.geo.GeoReferent import GeoReferent
        from pullenti.ner.core.Termin import Termin
        from pullenti.ner.decree.DecreePartReferent import DecreePartReferent
        from pullenti.ner.decree.internal.DecreeChangeToken import DecreeChangeToken
        from pullenti.ner.decree.DecreeChangeReferent import DecreeChangeReferent
        from pullenti.ner.core.BracketHelper import BracketHelper
        ad = kit.getAnalyzerData(self)
        base_typ = None
        ref0 = None
        aliases = TerminCollection()
        last_dec_dist = 0
        t = kit.first_token
        first_pass2867 = True
        while True:
            if first_pass2867: first_pass2867 = False
            else: t = t.next0_; last_dec_dist += 1
            if (not (t is not None)): break
            dts = DecreeToken.tryAttachList(t, None, 10, last_dec_dist > 1000)
            tok = aliases.tryParse(t, TerminParseAttr.NO)
            if (tok is not None and tok.begin_token == tok.end_token and tok.chars.is_all_lower): 
                ok = False
                tt = t.previous
                while tt is not None and ((t.end_char - tt.end_char) < 20): 
                    p = PartToken.tryAttach(tt, None, False, False)
                    if (p is not None and p.typ != PartToken.ItemType.PREFIX and p.end_token.next0_ == t): 
                        ok = True
                        break
                    tt = tt.previous
                if (not ok): 
                    tok = (None)
            if (tok is not None): 
                rt0 = DecreeAnalyzer._tryAttachApproved(t, ad)
                if (rt0 is not None): 
                    tok = (None)
            if (tok is not None): 
                dec0 = Utils.asObjectOrNull(tok.termin.tag, DecreeReferent)
                rt0 = ReferentToken(Utils.asObjectOrNull(tok.termin.tag, Referent), tok.begin_token, tok.end_token)
                if (dec0 is not None and (isinstance(rt0.end_token.next0_, ReferentToken)) and (isinstance(rt0.end_token.next0_.getReferent(), GeoReferent))): 
                    geo0 = Utils.asObjectOrNull(dec0.getSlotValue(DecreeReferent.ATTR_GEO), GeoReferent)
                    geo1 = Utils.asObjectOrNull(rt0.end_token.next0_.getReferent(), GeoReferent)
                    if (geo0 is None): 
                        dec0.addSlot(DecreeReferent.ATTR_GEO, geo1, False, 0)
                        rt0.end_token = rt0.end_token.next0_
                    elif (geo0 == geo1): 
                        rt0.end_token = rt0.end_token.next0_
                    else: 
                        continue
                kit.embedToken(rt0)
                t = (rt0)
                rt0.misc_attrs = 1
                last_dec_dist = 0
                continue
            if (dts is None or len(dts) == 0 or ((len(dts) == 1 and dts[0].typ == DecreeToken.ItemType.TYP))): 
                rt0 = DecreeAnalyzer._tryAttachApproved(t, ad)
                if (rt0 is not None): 
                    rt0.referent = ad.registerReferent(rt0.referent)
                    mt = DecreeAnalyzer._checkAliasAfter(rt0.end_token.next0_)
                    if (mt is not None): 
                        if (aliases is not None): 
                            term = Termin()
                            term.initBy(mt.begin_token, mt.end_token.previous, rt0.referent, False)
                            aliases.add(term)
                        rt0.end_token = mt.end_token
                    else: 
                        mt = Utils.asObjectOrNull(rt0.tag, MetaToken)
                        if ((mt) is not None): 
                            if (aliases is not None): 
                                term = Termin()
                                term.initBy(mt.begin_token, mt.end_token.previous, rt0.referent, False)
                                aliases.add(term)
                    kit.embedToken(rt0)
                    t = (rt0)
                    continue
                if (dts is None or len(dts) == 0): 
                    continue
            if (dts[0].is_newline_after and dts[0].is_newline_before): 
                ignore = False
                if (t == kit.first_token): 
                    ignore = True
                elif ((dts[0].typ == DecreeToken.ItemType.ORG and len(dts) > 1 and dts[1].typ == DecreeToken.ItemType.TYP) and dts[1].is_whitespace_after): 
                    ignore = True
                if (ignore): 
                    t = dts[len(dts) - 1].end_token
                    continue
            if (base_typ is None): 
                for dd in dts: 
                    if (dd.typ == DecreeToken.ItemType.TYP): 
                        base_typ = dd
                        break
            if (dts[0].typ == DecreeToken.ItemType.TYP and DecreeToken.getKind(dts[0].value) == DecreeKind.PUBLISHER): 
                rts = self.__tryAttachPulishers(dts)
                if (rts is not None): 
                    i = 0
                    while i < len(rts): 
                        rtt = rts[i]
                        if (isinstance(rtt.referent, DecreePartReferent)): 
                            (Utils.asObjectOrNull(rtt.referent, DecreePartReferent)).owner = Utils.asObjectOrNull(ad.registerReferent((Utils.asObjectOrNull(rtt.referent, DecreePartReferent)).owner), DecreeReferent)
                        rtt.referent = ad.registerReferent(rtt.referent)
                        kit.embedToken(rtt)
                        t = (rtt)
                        if ((isinstance(rtt.referent, DecreeReferent)) and ((i + 1) < len(rts)) and (isinstance(rts[i + 1].referent, DecreePartReferent))): 
                            rts[i + 1].begin_token = t
                        last_dec_dist = 0
                        i += 1
                    mt = DecreeAnalyzer._checkAliasAfter(t.next0_)
                    if (mt is not None): 
                        tt = dts[0].begin_token.previous
                        first_pass2868 = True
                        while True:
                            if first_pass2868: first_pass2868 = False
                            else: tt = tt.previous
                            if (not (tt is not None)): break
                            if (tt.is_comma): 
                                continue
                            d = Utils.asObjectOrNull(tt.getReferent(), DecreeReferent)
                            if (d is not None): 
                                if (aliases is not None): 
                                    term = Termin()
                                    term.initBy(mt.begin_token, mt.end_token.previous, d, False)
                                    aliases.add(term)
                                t = mt.end_token
                            break
                continue
            rtli = DecreeAnalyzer._tryAttach(dts, base_typ, ad)
            if (rtli is None or ((len(rtli) == 1 and (len(dts) < 3) and dts[0].value == "РЕГЛАМЕНТ"))): 
                rt = DecreeAnalyzer._tryAttachApproved(t, ad)
                if (rt is not None): 
                    rtli = list()
                    rtli.append(rt)
            if (rtli is not None): 
                ii = 0
                while ii < len(rtli): 
                    rt = rtli[ii]
                    last_dec_dist = 0
                    rt.referent = ad.registerReferent(rt.referent)
                    mt = DecreeAnalyzer._checkAliasAfter(rt.end_token.next0_)
                    if (mt is not None): 
                        if (aliases is not None): 
                            term = Termin()
                            term.initBy(mt.begin_token, mt.end_token.previous, rt.referent, False)
                            aliases.add(term)
                        rt.end_token = mt.end_token
                    else: 
                        mt = Utils.asObjectOrNull(rt.tag, MetaToken)
                        if ((mt) is not None): 
                            if (aliases is not None): 
                                term = Termin()
                                term.initBy(mt.begin_token, mt.end_token.previous, rt.referent, False)
                                aliases.add(term)
                    ref0 = rt.referent
                    kit.embedToken(rt)
                    t = (rt)
                    if ((ii + 1) < len(rtli)): 
                        if (rt.end_token.next0_ == rtli[ii + 1].begin_token): 
                            rtli[ii + 1].begin_token = rt
                    ii += 1
            elif (len(dts) == 1 and dts[0].typ == DecreeToken.ItemType.TYP): 
                if (dts[0].chars.is_capital_upper and not dts[0].is_doubtful): 
                    last_dec_dist = 0
                    if (base_typ is not None and dts[0].ref is not None): 
                        drr = Utils.asObjectOrNull(dts[0].ref.getReferent(), DecreeReferent)
                        if (drr is not None): 
                            if (base_typ.value == drr.typ0 or base_typ.value == drr.typ): 
                                continue
                    rt0 = DecreeToken._findBackTyp(dts[0].begin_token.previous, dts[0].value)
                    if (rt0 is not None): 
                        rt = ReferentToken(rt0.referent, dts[0].begin_token, dts[0].end_token)
                        kit.embedToken(rt)
                        t = (rt)
                        rt.tag = (rt0.referent)
        if (len(ad.referents) > 0): 
            t = kit.first_token
            first_pass2869 = True
            while True:
                if first_pass2869: first_pass2869 = False
                else: t = t.next0_
                if (not (t is not None)): break
                dr = Utils.asObjectOrNull(t.getReferent(), DecreeReferent)
                if (dr is None): 
                    continue
                li = None
                tt = t.next0_
                while tt is not None: 
                    if (not tt.is_comma_and): 
                        break
                    if (tt.next0_ is None or not ((isinstance(tt.next0_.getReferent(), DecreeReferent)))): 
                        break
                    if (li is None): 
                        li = list()
                        li.append(dr)
                    dr = (Utils.asObjectOrNull(tt.next0_.getReferent(), DecreeReferent))
                    li.append(dr)
                    tt = tt.next0_
                    tt = tt.next0_
                if (li is None): 
                    continue
                for i in range(len(li) - 1, 0, -1):
                    if (li[i].typ == li[i - 1].typ): 
                        if (li[i].date is not None and li[i - 1].date is None): 
                            li[i - 1].addSlot(DecreeReferent.ATTR_DATE, li[i].getSlotValue(DecreeReferent.ATTR_DATE), False, 0)
                else: i = 0
                i = 0
                while i < (len(li) - 1): 
                    if (li[i].typ == li[i + 1].typ): 
                        sl = li[i].findSlot(DecreeReferent.ATTR_SOURCE, None, True)
                        if (sl is not None and li[i + 1].findSlot(DecreeReferent.ATTR_SOURCE, None, True) is None): 
                            li[i + 1].addSlot(sl.type_name, sl.value, False, 0)
                    i += 1
                i = 0
                while i < len(li): 
                    if (li[i].name is not None): 
                        break
                    i += 1
                if (i == (len(li) - 1)): 
                    for i in range(len(li) - 1, 0, -1):
                        if (li[i - 1].typ == li[i].typ): 
                            li[i - 1]._addName(li[i])
                    else: i = 0
        undefined_decrees = list()
        root_change = None
        last_change = None
        change_stack = list()
        expire_regime = False
        has_start_change = 0
        t = kit.first_token
        first_pass2870 = True
        while True:
            if first_pass2870: first_pass2870 = False
            else: t = t.next0_
            if (not (t is not None)): break
            dts = None
            dcht = None
            if (t.is_newline_before): 
                dcht = DecreeChangeToken.tryAttach(t, root_change, False, change_stack, False)
            if (dcht is not None and dcht.is_start): 
                if (dcht.typ == DecreeChangeTokenTyp.STARTMULTU): 
                    expire_regime = False
                    has_start_change = 3
                    root_change = (None)
                elif (dcht.typ == DecreeChangeTokenTyp.SINGLE): 
                    dcht1 = DecreeChangeToken.tryAttach(dcht.end_token.next0_, root_change, False, change_stack, False)
                    if (dcht1 is not None and dcht1.is_start): 
                        has_start_change = 2
                        if (dcht.decree_tok is not None and dcht.decree is not None): 
                            rt = ReferentToken(dcht.decree, dcht.decree_tok.begin_token, dcht.decree_tok.end_token)
                            kit.embedToken(rt)
                            t = (rt)
                            if (dcht.end_char == t.end_char): 
                                dcht.end_token = t
                elif (dcht.typ == DecreeChangeTokenTyp.STARTSINGLE and dcht.decree is not None and not expire_regime): 
                    expire_regime = False
                    has_start_change = 2
                    if (dcht.decree_tok is not None): 
                        rt = ReferentToken(dcht.decree, dcht.decree_tok.begin_token, dcht.decree_tok.end_token)
                        kit.embedToken(rt)
                        t = (rt)
                        if (dcht.end_char == t.end_char): 
                            dcht.end_token = t
                    else: 
                        root_change = (None)
                if (dcht.typ == DecreeChangeTokenTyp.STARTSINGLE and root_change is not None and dcht.decree is None): 
                    has_start_change = 2
                elif ((dcht.typ == DecreeChangeTokenTyp.SINGLE and dcht.decree is not None and dcht.end_token.isChar(':')) and dcht.is_newline_after): 
                    has_start_change = 2
                if (has_start_change <= 0): 
                    dts = PartToken.tryAttachList(t, False, 40)
                    change_stack.clear()
                else: 
                    if (dcht.decree is not None): 
                        change_stack.clear()
                        change_stack.append(dcht.decree)
                    elif (dcht.act_kind == DecreeChangeKind.EXPIRE and dcht.typ == DecreeChangeTokenTyp.STARTMULTU): 
                        expire_regime = True
                    dts = dcht.parts
            else: 
                dts = PartToken.tryAttachList(t, False, 40)
                if (dcht is None and t.is_newline_before): 
                    expire_regime = False
                    has_start_change -= 1
            if (dts is not None): 
                pass
            rts = DecreeAnalyzer._tryAttachParts(dts, base_typ, (change_stack[0] if has_start_change > 0 and len(change_stack) > 0 else None))
            if (rts is not None): 
                pass
            dprs = None
            diaps = None
            begs = None
            ends = None
            if (rts is not None): 
                for kp in rts: 
                    dpr_list = Utils.asObjectOrNull(kp.tag, list)
                    if (dpr_list is None): 
                        continue
                    i = 0
                    while i < len(dpr_list): 
                        dr = dpr_list[i]
                        if (dr.owner is None and dr.clause is not None and dr.local_typ is None): 
                            if (not dr in undefined_decrees): 
                                undefined_decrees.append(dr)
                        if (dr.owner is not None and dr.clause is not None): 
                            for d in undefined_decrees: 
                                d.owner = dr.owner
                            undefined_decrees.clear()
                        if (dcht is not None and len(change_stack) > 0): 
                            while len(change_stack) > 0:
                                if (dr._isAllItemsLessLevel(change_stack[0], False)): 
                                    if (isinstance(change_stack[0], DecreePartReferent)): 
                                        dr._addHighLevelInfo(Utils.asObjectOrNull(change_stack[0], DecreePartReferent))
                                    break
                                if (isinstance(change_stack[0], DecreePartReferent)): 
                                    del change_stack[0]
                        if (last_change is not None and len(last_change.owners) > 0): 
                            dr0 = Utils.asObjectOrNull(last_change.owners[0], DecreePartReferent)
                            if (dr0 is not None and dr.owner == dr0.owner): 
                                mle = dr._getMinLevel()
                                if (mle == 0 or mle <= PartToken._getRank(PartToken.ItemType.CLAUSE)): 
                                    pass
                                else: 
                                    dr._addHighLevelInfo(dr0)
                        dr = (Utils.asObjectOrNull(ad.registerReferent(dr), DecreePartReferent))
                        if (dprs is None): 
                            dprs = list()
                        dprs.append(dr)
                        if (i == 0): 
                            rt = ReferentToken(dr, kp.begin_token, kp.end_token)
                        else: 
                            rt = ReferentToken(dr, t, t)
                        kit.embedToken(rt)
                        t = (rt)
                        if (len(dprs) == 2 and t.previous is not None and t.previous.is_hiphen): 
                            if (diaps is None): 
                                diaps = dict()
                            if (not dprs[0] in diaps): 
                                diaps[dprs[0]] = dprs[1]
                        if (begs is None): 
                            begs = dict()
                        if (not t.begin_char in begs): 
                            begs[t.begin_char] = t
                        else: 
                            begs[t.begin_char] = t
                        if (ends is None): 
                            ends = dict()
                        if (not t.end_char in ends): 
                            ends[t.end_char] = t
                        else: 
                            ends[t.end_char] = t
                        if (dcht is not None): 
                            if (dcht.begin_char == t.begin_char): 
                                dcht.begin_token = t
                            if (dcht.end_char == t.end_char): 
                                dcht.end_token = t
                            if (t.end_char > dcht.end_char): 
                                dcht.end_token = t
                        i += 1
            if (dts is not None and len(dts) > 0 and dts[len(dts) - 1].end_char > t.end_char): 
                t = dts[len(dts) - 1].end_token
            if (dcht is not None and has_start_change > 0): 
                if (dcht.end_char > t.end_char): 
                    t = dcht.end_token
                chrt = None
                if (dcht.typ == DecreeChangeTokenTyp.STARTMULTU): 
                    root_change = (None)
                    change_stack.clear()
                    if (dcht.decree is not None): 
                        change_stack.append(dcht.decree)
                    if (dprs is not None and len(dprs) > 0): 
                        if (len(change_stack) == 0 and dprs[0].owner is not None): 
                            change_stack.append(dprs[0].owner)
                        change_stack.insert(0, dprs[0])
                    if (len(change_stack) > 0 or dcht.decree is not None): 
                        root_change = (Utils.asObjectOrNull(ad.registerReferent(DecreeChangeReferent._new1085(DecreeChangeKind.CONTAINER)), DecreeChangeReferent))
                        if (len(change_stack) > 0): 
                            root_change.addSlot(DecreeChangeReferent.ATTR_OWNER, change_stack[0], False, 0)
                        else: 
                            root_change.addSlot(DecreeChangeReferent.ATTR_OWNER, dcht.decree, False, 0)
                        rt = ReferentToken(root_change, dcht.begin_token, dcht.end_token)
                        if (rt.end_token.isChar(':')): 
                            rt.end_token = rt.end_token.previous
                        kit.embedToken(rt)
                        t = (rt)
                        if (t.next0_ is not None and t.next0_.isChar(':')): 
                            t = t.next0_
                    continue
                if (dcht.typ == DecreeChangeTokenTyp.SINGLE and dprs is not None and len(dprs) == 1): 
                    while len(change_stack) > 0:
                        if (dprs[0]._isAllItemsLessLevel(change_stack[0], True)): 
                            break
                        else: 
                            del change_stack[0]
                    change_stack.insert(0, dprs[0])
                    if (dprs[0].owner is not None and change_stack[len(change_stack) - 1] != dprs[0].owner): 
                        change_stack.clear()
                        change_stack.insert(0, dprs[0].owner)
                        change_stack.insert(0, dprs[0])
                    continue
                if (dprs is None and dcht.real_part is not None): 
                    dprs = list()
                    dprs.append(dcht.real_part)
                if (dprs is not None and len(dprs) > 0): 
                    chrt = DecreeChangeToken.attachReferents(dprs[0], dcht)
                    if (chrt is None and expire_regime): 
                        chrt = list()
                        dcr = DecreeChangeReferent._new1085(DecreeChangeKind.EXPIRE)
                        chrt.append(ReferentToken(dcr, dcht.begin_token, dcht.end_token))
                elif (dcht.act_kind == DecreeChangeKind.APPEND): 
                    ee = False
                    if (dcht.part_typ != PartToken.ItemType.UNDEFINED): 
                        for ss in change_stack: 
                            if (isinstance(ss, DecreePartReferent)): 
                                if ((Utils.asObjectOrNull(ss, DecreePartReferent))._isAllItemsOverThisLevel(dcht.part_typ)): 
                                    ee = True
                                    chrt = DecreeChangeToken.attachReferents(ss, dcht)
                                    break
                            elif (isinstance(ss, DecreeReferent)): 
                                ee = True
                                chrt = DecreeChangeToken.attachReferents(ss, dcht)
                                break
                    if (last_change is not None and not ee and len(last_change.owners) > 0): 
                        chrt = DecreeChangeToken.attachReferents(last_change.owners[0], dcht)
                if (dprs is None and ((dcht.has_name or dcht.typ == DecreeChangeTokenTyp.VALUE or dcht.change_val is not None)) and len(change_stack) > 0): 
                    chrt = DecreeChangeToken.attachReferents(change_stack[0], dcht)
                if ((chrt is None and ((expire_regime or dcht.act_kind == DecreeChangeKind.EXPIRE)) and dcht.decree is not None) and dprs is None): 
                    chrt = list()
                    dcr = DecreeChangeReferent._new1085(DecreeChangeKind.EXPIRE)
                    dcr.addSlot(DecreeChangeReferent.ATTR_OWNER, dcht.decree, False, 0)
                    chrt.append(ReferentToken(dcr, dcht.begin_token, dcht.end_token))
                    tt = dcht.end_token.next0_
                    first_pass2871 = True
                    while True:
                        if first_pass2871: first_pass2871 = False
                        else: tt = tt.next0_
                        if (not (tt is not None)): break
                        if (tt.next0_ is None): 
                            break
                        if (tt.isChar('(')): 
                            br = BracketHelper.tryParse(tt, BracketParseAttr.NO, 100)
                            if (br is not None): 
                                tt = br.end_token
                                chrt[len(chrt) - 1].end_token = tt
                                continue
                        if (not tt.is_comma_and and not tt.isChar(';')): 
                            break
                        tt = tt.next0_
                        if (isinstance(tt.getReferent(), DecreeReferent)): 
                            dcr = DecreeChangeReferent._new1085(DecreeChangeKind.EXPIRE)
                            dcr.addSlot(DecreeChangeReferent.ATTR_OWNER, tt.getReferent(), False, 0)
                            rt = ReferentToken(dcr, tt, tt)
                            if (tt.next0_ is not None and tt.next0_.isChar('(')): 
                                br = BracketHelper.tryParse(tt.next0_, BracketParseAttr.NO, 100)
                                if (br is not None): 
                                    tt = br.end_token
                                    rt.end_token = tt
                            chrt.append(rt)
                            continue
                        break
                if (chrt is not None): 
                    for rt in chrt: 
                        rt.referent = ad.registerReferent(rt.referent)
                        if (isinstance(rt.referent, DecreeChangeReferent)): 
                            last_change = (Utils.asObjectOrNull(rt.referent, DecreeChangeReferent))
                            if (dprs is not None): 
                                ii = 0
                                while ii < (len(dprs) - 1): 
                                    last_change.addSlot(DecreeChangeReferent.ATTR_OWNER, dprs[ii], False, 0)
                                    ii += 1
                                if (diaps is not None): 
                                    for kp in diaps.items(): 
                                        diap = PartToken.tryCreateBetween(kp[0], kp[1])
                                        if (diap is not None): 
                                            for d in diap: 
                                                dd = ad.registerReferent(d)
                                                last_change.addSlot(DecreeChangeReferent.ATTR_OWNER, dd, False, 0)
                                while ii < len(dprs): 
                                    last_change.addSlot(DecreeChangeReferent.ATTR_OWNER, dprs[ii], False, 0)
                                    ii += 1
                        if (begs is not None and rt.begin_char in begs): 
                            rt.begin_token = begs[rt.begin_char]
                        if (ends is not None and rt.end_char in ends): 
                            rt.end_token = ends[rt.end_char]
                        if (root_change is not None and (isinstance(rt.referent, DecreeChangeReferent))): 
                            root_change.addSlot(DecreeChangeReferent.ATTR_CHILD, rt.referent, False, 0)
                        kit.embedToken(rt)
                        t = (rt)
                        if (begs is None): 
                            begs = dict()
                        if (not t.begin_char in begs): 
                            begs[t.begin_char] = t
                        else: 
                            begs[t.begin_char] = t
                        if (ends is None): 
                            ends = dict()
                        if (not t.end_char in ends): 
                            ends[t.end_char] = t
                        else: 
                            ends[t.end_char] = t
        t = kit.first_token
        while t is not None: 
            if (t.tag is not None and (isinstance(t, ReferentToken)) and (isinstance(t.tag, DecreeReferent))): 
                t = kit.debedToken(t)
                if (t is None): 
                    break
            t = t.next0_
    
    @staticmethod
    def _checkAliasAfter(t : 'Token') -> 'MetaToken':
        if ((t is not None and t.isChar('<') and t.next0_ is not None) and t.next0_.next0_ is not None and t.next0_.next0_.isChar('>')): 
            t = t.next0_.next0_.next0_
        if (t is None or t.next0_ is None or not t.isChar('(')): 
            return None
        t = t.next0_
        if (t.isValue("ДАЛЕЕ", "ДАЛІ")): 
            pass
        else: 
            return None
        t = t.next0_
        if (t is not None and not t.chars.is_letter): 
            t = t.next0_
        if (t is None): 
            return None
        t1 = None
        tt = t
        while tt is not None: 
            if (tt.is_newline_before): 
                break
            elif (tt.isChar(')')): 
                t1 = tt.previous
                break
            tt = tt.next0_
        if (t1 is None): 
            return None
        return MetaToken(t, t1.next0_)
    
    @staticmethod
    def _tryAttachApproved(t : 'Token', ad : 'AnalyzerData') -> 'ReferentToken':
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.decree.DecreeReferent import DecreeReferent
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.decree.internal.DecreeToken import DecreeToken
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.org.OrganizationReferent import OrganizationReferent
        if (t is None): 
            return None
        br = None
        if (BracketHelper.canBeStartOfSequence(t, True, False)): 
            br = BracketHelper.tryParse(t, BracketParseAttr.NO, 100)
        elif ((isinstance(t.previous, TextToken)) and t.previous.length_char == 1 and BracketHelper.canBeStartOfSequence(t.previous, True, False)): 
            br = BracketHelper.tryParse(t.previous, BracketParseAttr.NO, 100)
        if (br is not None and br.length_char > 20): 
            rt0 = DecreeAnalyzer.__tryAttachApproved(br.end_token.next0_, ad, False)
            if (rt0 is not None): 
                dr = Utils.asObjectOrNull(rt0.referent, DecreeReferent)
                rt0.begin_token = br.begin_token
                nam = MiscHelper.getTextValueOfMetaToken(br, GetTextAttr.KEEPREGISTER)
                if (dr.typ is None): 
                    dt = DecreeToken.tryAttach(br.begin_token.next0_, None, False)
                    if (dt is not None and dt.typ == DecreeToken.ItemType.TYP): 
                        dr.typ = dt.value
                        if (dt.end_token.next0_ is not None and dt.end_token.next0_.isValue("О", None)): 
                            nam = MiscHelper.getTextValue(dt.end_token.next0_, br.end_token, GetTextAttr.KEEPREGISTER)
                if (nam is not None): 
                    dr._addNameStr(nam)
                return rt0
        if (not t.chars.is_cyrillic_letter or t.chars.is_all_lower): 
            return None
        tt = DecreeToken.isKeyword(t, False)
        if (tt is None or tt.next0_ is None): 
            return None
        cou = 0
        alias = None
        aliast0 = None
        tt = tt.next0_
        first_pass2872 = True
        while True:
            if first_pass2872: first_pass2872 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            cou += 1
            if ((cou) > 100): 
                break
            if (tt.is_newline_before): 
                if (tt.isValue("ИСТОЧНИК", None)): 
                    break
            if ((((isinstance(tt, NumberToken)) and (Utils.asObjectOrNull(tt, NumberToken)).value == (1))) or tt.isValue("ДРУГОЙ", None)): 
                if (tt.next0_ is not None and tt.next0_.isValue("СТОРОНА", None)): 
                    return None
            if (tt.whitespaces_before_count > 15): 
                break
            if (tt.isChar('(')): 
                mt = DecreeAnalyzer._checkAliasAfter(tt)
                if (mt is not None): 
                    aliast0 = tt
                    alias = mt
                    tt = mt.end_token
                    continue
            if (DecreeToken.isKeyword(tt, False) is not None and tt.chars.is_capital_upper): 
                break
            rt0 = DecreeAnalyzer.__tryAttachApproved(tt, ad, True)
            if (rt0 is not None): 
                t1 = tt.previous
                if (aliast0 is not None): 
                    t1 = aliast0.previous
                nam = MiscHelper.getTextValue(t, t1, Utils.valToEnum((GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE) | (GetTextAttr.KEEPREGISTER), GetTextAttr))
                dt = DecreeToken.tryAttach(t, None, False)
                if (dt is not None and dt.typ == DecreeToken.ItemType.TYP and (Utils.asObjectOrNull(rt0.referent, DecreeReferent)).typ is None): 
                    (Utils.asObjectOrNull(rt0.referent, DecreeReferent)).typ = dt.value
                    if (dt.end_token.next0_ is not None and dt.end_token.next0_.isValue("О", "ПРО")): 
                        nam = MiscHelper.getTextValue(dt.end_token.next0_, t1, GetTextAttr.KEEPREGISTER)
                dec = Utils.asObjectOrNull(rt0.referent, DecreeReferent)
                if (nam is not None): 
                    dec._addNameStr(nam)
                rt0.begin_token = t
                rt0.tag = (alias)
                if (dec.findSlot(DecreeReferent.ATTR_SOURCE, None, True) is None): 
                    if (t.previous is not None and t.previous.isValue("В", None) and (isinstance(t.previous.previous, ReferentToken))): 
                        if (isinstance(t.previous.previous.getReferent(), OrganizationReferent)): 
                            dec.addSlot(DecreeReferent.ATTR_SOURCE, t.previous.previous.getReferent(), False, 0)
                return rt0
            if (tt.isChar('.')): 
                break
            if (tt.is_newline_before and tt.previous is not None and tt.previous.isChar('.')): 
                break
        return None
    
    @staticmethod
    def __tryAttachApproved(t : 'Token', ad : 'AnalyzerData', must_be_comma : bool=True) -> 'ReferentToken':
        from pullenti.ner.geo.GeoReferent import GeoReferent
        from pullenti.ner.decree.internal.DecreeToken import DecreeToken
        from pullenti.ner.date.DateReferent import DateReferent
        from pullenti.ner.decree.DecreeReferent import DecreeReferent
        from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent
        from pullenti.ner.ReferentToken import ReferentToken
        if (t is None or t.next0_ is None): 
            return None
        t0 = t
        if (not t.isCharOf("(,")): 
            if (must_be_comma): 
                return None
        else: 
            t = t.next0_
        ok = False
        first_pass2873 = True
        while True:
            if first_pass2873: first_pass2873 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_comma_and or t.morph.class0_.is_preposition): 
                continue
            if ((isinstance(t.getReferent(), GeoReferent)) and (Utils.asObjectOrNull(t.getReferent(), GeoReferent)).is_city): 
                continue
            if ((((((((t.isValue("УТВ", None) or t.isValue("УТВЕРЖДАТЬ", "СТВЕРДЖУВАТИ") or t.isValue("УТВЕРДИТЬ", "ЗАТВЕРДИТИ")) or t.isValue("УТВЕРЖДЕННЫЙ", "ЗАТВЕРДЖЕНИЙ") or t.isValue("ЗАТВЕРДЖУВАТИ", None)) or t.isValue("СТВЕРДИТИ", None) or t.isValue("ЗАТВЕРДИТИ", None)) or t.isValue("ПРИНЯТЬ", "ПРИЙНЯТИ") or t.isValue("ПРИНЯТЫЙ", "ПРИЙНЯТИЙ")) or t.isValue("ВВОДИТЬ", "ВВОДИТИ") or t.isValue("ВВЕСТИ", None)) or t.isValue("ВВЕДЕННЫЙ", "ВВЕДЕНИЙ") or t.isValue("ПОДПИСАТЬ", "ПІДПИСАТИ")) or t.isValue("ПОДПИСЫВАТЬ", "ПІДПИСУВАТИ") or t.isValue("ЗАКЛЮЧИТЬ", "УКЛАСТИ")) or t.isValue("ЗАКЛЮЧАТЬ", "УКЛАДАТИ")): 
                ok = True
                if (t.next0_ is not None and t.next0_.isChar('.')): 
                    t = t.next0_
            elif (t.isValue("ДЕЙСТВИЕ", None) or t.isValue("ДІЯ", None)): 
                pass
            else: 
                break
        if (not ok): 
            return None
        if (t is None): 
            return None
        kit = t.kit
        olev = None
        lev = 0
        wrapolev1089 = RefOutArgWrapper(None)
        inoutres1090 = Utils.tryGetValue(kit.misc_data, "dovr", wrapolev1089)
        olev = wrapolev1089.value
        if (not inoutres1090): 
            lev = 1
            kit.misc_data["dovr"] = lev
        else: 
            lev = (olev)
            if (lev > 2): 
                return None
            lev += 1
            kit.misc_data["dovr"] = (lev)
        try: 
            dts = DecreeToken.tryAttachList(t, None, 10, False)
            if (dts is None): 
                return None
            rt = DecreeAnalyzer._tryAttach(dts, None, ad)
            if (rt is None): 
                has_date = 0
                has_num = 0
                has_own = 0
                ii = 0
                while ii < len(dts): 
                    if (dts[ii].typ == DecreeToken.ItemType.NUMBER): 
                        has_num += 1
                    elif ((dts[ii].typ == DecreeToken.ItemType.DATE and dts[ii].ref is not None and (isinstance(dts[ii].ref.referent, DateReferent))) and (Utils.asObjectOrNull(dts[ii].ref.referent, DateReferent)).dt is not None): 
                        has_date += 1
                    elif (dts[ii].typ == DecreeToken.ItemType.OWNER or dts[ii].typ == DecreeToken.ItemType.ORG): 
                        has_own += 1
                    else: 
                        break
                    ii += 1
                if (ii >= len(dts) and has_own > 0 and ((has_date == 1 or has_num == 1))): 
                    dr = DecreeReferent()
                    for dt in dts: 
                        if (dt.typ == DecreeToken.ItemType.DATE): 
                            dr._addDate(dt)
                        elif (dt.typ == DecreeToken.ItemType.NUMBER): 
                            dr._addNumber(dt)
                        else: 
                            val = dt.value
                            if (dt.ref is not None and dt.ref.referent is not None): 
                                val = (dt.ref.referent)
                            dr.addSlot(DecreeReferent.ATTR_SOURCE, val, False, 0).tag = dt.getSourceText()
                            if (dt.ref is not None and (isinstance(dt.ref.referent, PersonPropertyReferent))): 
                                dr.addExtReferent(dt.ref)
                    rt = list()
                    rt.append(ReferentToken(dr, dts[0].begin_token, dts[len(dts) - 1].end_token))
            if (((rt is None and len(dts) == 1 and dts[0].typ == DecreeToken.ItemType.DATE) and dts[0].ref is not None and (isinstance(dts[0].ref.referent, DateReferent))) and (Utils.asObjectOrNull(dts[0].ref.referent, DateReferent)).dt is not None): 
                dr = DecreeReferent()
                dr._addDate(dts[0])
                rt = list()
                rt.append(ReferentToken(dr, dts[0].begin_token, dts[len(dts) - 1].end_token))
            if (rt is None): 
                return None
            if (t0.isChar('(') and rt[0].end_token.next0_ is not None and rt[0].end_token.next0_.isChar(')')): 
                rt[0].end_token = rt[0].end_token.next0_
            rt[0].begin_token = t0
            return rt[0]
        finally: 
            lev -= 1
            if (lev < 0): 
                lev = 0
            kit.misc_data["dovr"] = (lev)
    
    @staticmethod
    def _getDecree(t : 'Token') -> 'DecreeReferent':
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.decree.DecreeReferent import DecreeReferent
        from pullenti.ner.decree.DecreePartReferent import DecreePartReferent
        if (not ((isinstance(t, ReferentToken)))): 
            return None
        r = t.getReferent()
        if (isinstance(r, DecreeReferent)): 
            return Utils.asObjectOrNull(r, DecreeReferent)
        if (isinstance(r, DecreePartReferent)): 
            return (Utils.asObjectOrNull(r, DecreePartReferent)).owner
        return None
    
    @staticmethod
    def _checkOtherTyp(t : 'Token', first : bool) -> 'Token':
        from pullenti.ner.decree.internal.DecreeToken import DecreeToken
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        if (t is None): 
            return None
        dit = DecreeToken.tryAttach(t, None, False)
        npt = None
        if (dit is None): 
            npt = NounPhraseHelper.tryParse(t, NounPhraseParseAttr.NO, 0)
            if (npt is not None and npt.begin_token != npt.end_token): 
                dit = DecreeToken.tryAttach(npt.end_token, None, False)
        if (dit is not None and dit.typ == DecreeToken.ItemType.TYP): 
            if (dit.chars.is_capital_upper or first): 
                dit.end_token.tag = (dit.value)
                return dit.end_token
            else: 
                return None
        if (npt is not None): 
            t = npt.end_token
        if (t.chars.is_capital_upper or first): 
            if (t.previous is not None and t.previous.isChar('.') and not first): 
                return None
            tt = DecreeToken.isKeyword(t, False)
            if (tt is not None): 
                return tt
        return None
    
    def __tryAttachPulishers(self, dts : typing.List['DecreeToken']) -> typing.List['ReferentToken']:
        from pullenti.ner.decree.internal.DecreeToken import DecreeToken
        from pullenti.ner.geo.GeoReferent import GeoReferent
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.decree.internal.PartToken import PartToken
        from pullenti.ner.decree.DecreeReferent import DecreeReferent
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.decree.DecreePartReferent import DecreePartReferent
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.TextToken import TextToken
        i = 0
        t1 = None
        typ = None
        geo = None
        org0_ = None
        date_ = None
        i = 0
        while i < len(dts): 
            if (dts[i].typ == DecreeToken.ItemType.TYP and DecreeToken.getKind(dts[i].value) == DecreeKind.PUBLISHER): 
                typ = dts[i].value
                if (dts[i].ref is not None and (isinstance(dts[i].ref.getReferent(), GeoReferent))): 
                    geo = dts[i].ref
            elif (dts[i].typ == DecreeToken.ItemType.TERR): 
                geo = dts[i].ref
                t1 = dts[i].end_token
            elif (dts[i].typ == DecreeToken.ItemType.DATE): 
                date_ = dts[i]
                t1 = dts[i].end_token
            elif (dts[i].typ == DecreeToken.ItemType.ORG): 
                org0_ = dts[i].ref
                t1 = dts[i].end_token
            else: 
                break
            i += 1
        if (typ is None): 
            return None
        t = dts[i - 1].end_token.next0_
        if (t is None): 
            return None
        res = list()
        num = None
        t0 = dts[0].begin_token
        if (BracketHelper.canBeEndOfSequence(t, False, None, False)): 
            t = t.next0_
            if (BracketHelper.canBeStartOfSequence(t0.previous, False, False)): 
                t0 = t0.previous
        pub0 = None
        pub_part0 = None
        first_pass2874 = True
        while True:
            if first_pass2874: first_pass2874 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.isCharOf(",;.") or t.is_and): 
                continue
            dt = DecreeToken.tryAttach(t, dts[0], False)
            if (dt is not None): 
                if (dt.typ == DecreeToken.ItemType.NUMBER): 
                    num = dt
                    pub0 = (None)
                    pub_part0 = (None)
                    if (t0 is None): 
                        t0 = t
                    t = dt.end_token
                    t1 = t
                    continue
                if (dt.typ == DecreeToken.ItemType.DATE): 
                    if (t0 is None): 
                        t0 = t
                    date_ = dt
                    pub0 = (None)
                    pub_part0 = (None)
                    t = dt.end_token
                    t1 = t
                    continue
                if (dt.typ != DecreeToken.ItemType.MISC and t.length_char > 2): 
                    break
            pt = PartToken.tryAttach(t, None, False, False)
            if (pt is None and t.isChar('(')): 
                pt = PartToken.tryAttach(t.next0_, None, False, False)
                if (pt is not None): 
                    if (pt.end_token.next0_ is not None and pt.end_token.next0_.isChar(')')): 
                        pt.end_token = pt.end_token.next0_
                    else: 
                        pt = (None)
            if (pt is not None): 
                if (pt.typ == PartToken.ItemType.PAGE): 
                    t = pt.end_token
                    continue
                if (pt.typ != PartToken.ItemType.CLAUSE and pt.typ != PartToken.ItemType.PART and pt.typ != PartToken.ItemType.PAGE): 
                    break
                if (num is None): 
                    break
                if (pub_part0 is not None): 
                    if (pt.typ == PartToken.ItemType.PART and pub_part0.part is None): 
                        pass
                    elif (pt.typ == PartToken.ItemType.CLAUSE and pub_part0.clause is None): 
                        pass
                    else: 
                        pub_part0 = (None)
                pub = pub0
                pub_part = pub_part0
                if (pub is None): 
                    pub = DecreeReferent()
                    pub.typ = typ
                    if (geo is not None): 
                        pub.addSlot(DecreeReferent.ATTR_GEO, geo.referent, False, 0)
                    if (org0_ is not None): 
                        pub.addSlot(DecreeReferent.ATTR_SOURCE, org0_.referent, False, 0).tag = org0_.getSourceText()
                    if (date_ is not None): 
                        pub._addDate(date_)
                    pub._addNumber(num)
                    res.append(ReferentToken(pub, Utils.ifNotNull(t0, t), pt.begin_token.previous))
                if (pub_part is None): 
                    pub_part = DecreePartReferent._new1091(pub)
                    res.append(ReferentToken(pub_part, pt.begin_token, pt.end_token))
                pub0 = pub
                if (len(pt.values) == 1): 
                    if (pt.typ == PartToken.ItemType.CLAUSE): 
                        pub_part.addSlot(DecreePartReferent.ATTR_CLAUSE, pt.values[0].value, False, 0).tag = pt.values[0].source_value
                    elif (pt.typ == PartToken.ItemType.PART): 
                        pub_part.addSlot(DecreePartReferent.ATTR_PART, pt.values[0].value, False, 0).tag = pt.values[0].source_value
                elif (len(pt.values) > 1): 
                    ii = 0
                    while ii < len(pt.values): 
                        if (ii > 0): 
                            pub_part = DecreePartReferent._new1091(pub)
                            res.append(ReferentToken(pub_part, pt.values[ii].begin_token, pt.values[ii].end_token))
                        else: 
                            res[len(res) - 1].end_token = pt.values[ii].end_token
                        if (pt.typ == PartToken.ItemType.CLAUSE): 
                            pub_part.addSlot(DecreePartReferent.ATTR_CLAUSE, pt.values[ii].value, False, 0).tag = pt.values[ii].source_value
                        elif (pt.typ == PartToken.ItemType.PART): 
                            pub_part.addSlot(DecreePartReferent.ATTR_PART, pt.values[ii].value, False, 0).tag = pt.values[ii].source_value
                        ii += 1
                if (pub_part.clause == "6878"): 
                    pass
                pub_part0 = pub_part
                res[len(res) - 1].end_token = pt.end_token
                t0 = (None)
                t = pt.end_token
                continue
            if (isinstance(t, NumberToken)): 
                rt = t.kit.processReferent("DATE", t)
                if (rt is not None): 
                    date_ = DecreeToken._new842(rt.begin_token, rt.end_token, DecreeToken.ItemType.DATE)
                    date_.ref = rt
                    pub0 = (None)
                    pub_part0 = (None)
                    if (t0 is None): 
                        t0 = t
                    t = rt.end_token
                    t1 = t
                    continue
                if (t.next0_ is not None and t.next0_.isChar(';')): 
                    if (pub_part0 is not None and pub_part0.clause is not None and pub0 is not None): 
                        pub_part = DecreePartReferent()
                        for s in pub_part0.slots: 
                            pub_part.addSlot(s.type_name, s.value, False, 0)
                        pub_part0 = pub_part
                        pub_part0.clause = str((Utils.asObjectOrNull(t, NumberToken)).value)
                        res.append(ReferentToken(pub_part0, t, t))
                        continue
            if (((isinstance(t, TextToken)) and t.chars.is_letter and (t.length_char < 3)) and (isinstance(t.next0_, NumberToken))): 
                t = t.next0_
                continue
            if ((t.isChar('(') and t.next0_ is not None and t.next0_.next0_ is not None) and t.next0_.next0_.isChar(')')): 
                t = t.next0_.next0_
                continue
            break
        if ((len(res) == 0 and date_ is not None and num is not None) and t1 is not None): 
            pub = DecreeReferent()
            pub.typ = typ
            if (geo is not None): 
                pub.addSlot(DecreeReferent.ATTR_GEO, geo.referent, False, 0)
            if (org0_ is not None): 
                pub.addSlot(DecreeReferent.ATTR_SOURCE, org0_.referent, False, 0).tag = org0_.getSourceText()
            if (date_ is not None): 
                pub._addDate(date_)
            pub._addNumber(num)
            res.append(ReferentToken(pub, t0, t1))
        return res
    
    def _processReferent(self, begin : 'Token', end : 'Token') -> 'ReferentToken':
        from pullenti.ner.decree.internal.DecreeToken import DecreeToken
        from pullenti.ner.ReferentToken import ReferentToken
        dp = DecreeToken.tryAttach(begin, None, False)
        if (dp is not None and dp.typ == DecreeToken.ItemType.TYP): 
            return ReferentToken(None, dp.begin_token, dp.end_token)
        return None
    
    M_INITED = None
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.core.Termin import Termin
        from pullenti.ner.decree.internal.DecreeChangeToken import DecreeChangeToken
        from pullenti.ner.decree.internal.DecreeToken import DecreeToken
        from pullenti.ner.ProcessorService import ProcessorService
        if (DecreeAnalyzer.M_INITED): 
            return
        DecreeAnalyzer.M_INITED = True
        try: 
            Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = False
            DecreeChangeToken._initialize()
            Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = True
            DecreeToken.initialize()
            Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = False
        except Exception as ex: 
            raise Utils.newException(ex.__str__(), ex)
        ProcessorService.registerAnalyzer(DecreeAnalyzer())
    
    @staticmethod
    def _tryAttach(dts : typing.List['DecreeToken'], base_typ : 'DecreeToken', ad : 'AnalyzerData') -> typing.List['ReferentToken']:
        res = DecreeAnalyzer.__TryAttach(dts, base_typ, False, ad)
        return res
    
    @staticmethod
    def __TryAttach(dts : typing.List['DecreeToken'], base_typ : 'DecreeToken', after_decree : bool, ad : 'AnalyzerData') -> typing.List['ReferentToken']:
        from pullenti.ner.decree.internal.DecreeToken import DecreeToken
        from pullenti.ner.Referent import Referent
        from pullenti.ner.decree.DecreeReferent import DecreeReferent
        from pullenti.ner.decree.DecreePartReferent import DecreePartReferent
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.decree.internal.PartToken import PartToken
        from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent
        from pullenti.ner.org.OrganizationReferent import OrganizationReferent
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.date.DateRangeReferent import DateRangeReferent
        from pullenti.ner.date.DateReferent import DateReferent
        from pullenti.ner.geo.GeoReferent import GeoReferent
        if (dts is None or (len(dts) < 1)): 
            return None
        if (dts[0].typ == DecreeToken.ItemType.EDITION and len(dts) > 1): 
            del dts[0]
        if (len(dts) == 1): 
            if (dts[0].typ == DecreeToken.ItemType.DECREEREF and dts[0].ref is not None): 
                if (base_typ is not None): 
                    re = dts[0].ref.getReferent()
                    dre = Utils.asObjectOrNull(re, DecreeReferent)
                    if (dre is None and (isinstance(re, DecreePartReferent))): 
                        dre = (Utils.asObjectOrNull(re, DecreePartReferent)).owner
                    if (dre is not None): 
                        if (dre.typ == base_typ.value or dre.typ0 == base_typ.value): 
                            return None
                reli = list()
                reli.append(ReferentToken(dts[0].ref.referent, dts[0].begin_token, dts[0].end_token))
                return reli
        dec0 = None
        kodeks = False
        max_empty = 30
        t = dts[0].begin_token.previous
        first_pass2875 = True
        while True:
            if first_pass2875: first_pass2875 = False
            else: t = t.previous
            if (not (t is not None)): break
            if (t.is_comma_and): 
                continue
            if (t.isChar(')')): 
                cou = 0
                t = t.previous
                while t is not None: 
                    if (t.isChar('(')): 
                        break
                    else: 
                        cou += 1
                        if ((cou) > 200): 
                            break
                    t = t.previous
                if (t is not None and t.isChar('(')): 
                    continue
                break
            max_empty -= 1
            if ((max_empty) < 0): 
                break
            if (not t.chars.is_letter): 
                continue
            dec0 = (Utils.asObjectOrNull(t.getReferent(), DecreeReferent))
            if (dec0 is not None): 
                if (DecreeToken.getKind(dec0.typ) == DecreeKind.KODEX): 
                    kodeks = True
                elif (dec0.kind == DecreeKind.PUBLISHER): 
                    dec0 = (None)
            break
        dec = DecreeReferent()
        i = 0
        morph_ = None
        is_noun_doubt = False
        num_tok = None
        i = 0
        first_pass2876 = True
        while True:
            if first_pass2876: first_pass2876 = False
            else: i += 1
            if (not (i < len(dts))): break
            if (dts[i].typ == DecreeToken.ItemType.TYP): 
                if (dts[i].value is None): 
                    break
                if (dts[i].is_newline_before): 
                    if (dec.date is not None or dec.number is not None): 
                        break
                if (dec.typ is not None): 
                    if (((dec.typ == "РЕШЕНИЕ" or dec.typ == "РІШЕННЯ")) and dts[i].value == "ПРОТОКОЛ"): 
                        pass
                    elif (dec.typ == dts[i].value and dec.typ == "ГОСТ"): 
                        continue
                    else: 
                        break
                ki = DecreeToken.getKind(dts[i].value)
                if (ki == DecreeKind.STANDARD): 
                    if (i > 0): 
                        return None
                if (ki == DecreeKind.KODEX): 
                    if (i > 0): 
                        break
                    if (dts[i].value != "ОСНОВЫ ЗАКОНОДАТЕЛЬСТВА" and dts[i].value != "ОСНОВИ ЗАКОНОДАВСТВА"): 
                        kodeks = True
                    else: 
                        kodeks = False
                else: 
                    kodeks = False
                morph_ = dts[i].morph
                dec.typ = dts[i].value
                if (dts[i].full_value is not None): 
                    dec._addNameStr(dts[i].full_value)
                is_noun_doubt = dts[i].is_doubtful
                if (is_noun_doubt and i == 0): 
                    if (PartToken.isPartBefore(dts[i].begin_token)): 
                        is_noun_doubt = False
                if (dts[i].ref is not None): 
                    if (dec.findSlot(DecreeReferent.ATTR_GEO, None, True) is None): 
                        dec.addSlot(DecreeReferent.ATTR_GEO, dts[i].ref.referent, False, 0)
                        dec.addExtReferent(dts[i].ref)
            elif (dts[i].typ == DecreeToken.ItemType.DATE): 
                if (dec.date is not None): 
                    break
                if (kodeks): 
                    if (i > 0 and dts[i - 1].typ == DecreeToken.ItemType.NUMBER): 
                        pass
                    else: 
                        break
                if (i == (len(dts) - 1)): 
                    if (not dts[i].begin_token.isValue("ОТ", "ВІД")): 
                        ty = DecreeToken.getKind(dec.typ)
                        if ((ty == DecreeKind.KONVENTION or ty == DecreeKind.CONTRACT or dec.typ0 == "ПИСЬМО") or dec.typ0 == "ЛИСТ"): 
                            pass
                        else: 
                            break
                dec._addDate(dts[i])
                dec.addExtReferent(dts[i].ref)
            elif (dts[i].typ == DecreeToken.ItemType.DATERANGE): 
                if (dec.kind != DecreeKind.PROGRAM): 
                    break
                dec._addDate(dts[i])
                dec.addExtReferent(dts[i].ref)
            elif (dts[i].typ == DecreeToken.ItemType.EDITION): 
                if (dts[i].is_newline_before and not dts[i].begin_token.chars.is_all_lower and not dts[i].begin_token.isChar('(')): 
                    break
                if (((i + 2) < len(dts)) and dts[i + 1].typ == DecreeToken.ItemType.TYP): 
                    break
            elif (dts[i].typ == DecreeToken.ItemType.NUMBER): 
                if (kodeks): 
                    if (((i + 1) < len(dts)) and dts[i + 1].typ == DecreeToken.ItemType.DATE): 
                        pass
                    else: 
                        break
                num_tok = dts[i]
                if (dts[i].is_delo): 
                    if (dec.case_number is not None): 
                        break
                    dec.addSlot(DecreeReferent.ATTR_CASENUMBER, dts[i].value, True, 0)
                    continue
                if (dec.number is not None): 
                    if (i > 2 and ((dts[i - 1].typ == DecreeToken.ItemType.OWNER or dts[i - 1].typ == DecreeToken.ItemType.ORG)) and dts[i - 2].typ == DecreeToken.ItemType.NUMBER): 
                        pass
                    else: 
                        break
                if (dts[i].is_newline_before): 
                    if (dec.typ is None and dec0 is None): 
                        break
                if (LanguageHelper.endsWith(dts[i].value, "ФЗ")): 
                    dec.typ = "ФЕДЕРАЛЬНЫЙ ЗАКОН"
                if (LanguageHelper.endsWith(dts[i].value, "ФКЗ")): 
                    dec.typ = "ФЕДЕРАЛЬНЫЙ КОНСТИТУЦИОННЫЙ ЗАКОН"
                if (dts[i].value is not None and Utils.startsWithString(dts[i].value, "ПР", True) and dec.typ is None): 
                    dec.typ = "ПОРУЧЕНИЕ"
                if (dec.typ is None): 
                    if (dec0 is None and not after_decree): 
                        break
                dec._addNumber(dts[i])
                if (dts[i].children is not None): 
                    cou = 0
                    for s in dec.slots: 
                        if (s.type_name == DecreeReferent.ATTR_SOURCE): 
                            cou += 1
                    if (cou == (len(dts[i].children) + 1)): 
                        for dd in dts[i].children: 
                            dec._addNumber(dd)
                        dts[i].children = (None)
                continue
            elif (dts[i].typ == DecreeToken.ItemType.NAME): 
                if (dec.typ is None and dec.number is None and dec0 is None): 
                    break
                if (dec.getStringValue(DecreeReferent.ATTR_NAME) is not None): 
                    if (kodeks): 
                        break
                    if (i > 0 and dts[i - 1].end_token.next0_ == dts[i].begin_token): 
                        pass
                    else: 
                        break
                nam = dts[i].value
                if (kodeks and not "КОДЕКС" in nam.upper()): 
                    nam = ("Кодекс " + nam)
                dec._addNameStr(nam)
            elif (dts[i].typ == DecreeToken.ItemType.BETWEEN): 
                if (dec.kind != DecreeKind.CONTRACT): 
                    break
                for chh in dts[i].children: 
                    dec.addSlot(DecreeReferent.ATTR_SOURCE, chh.ref.referent, False, 0).tag = chh.getSourceText()
                    if (isinstance(chh.ref.referent, PersonPropertyReferent)): 
                        dec.addExtReferent(chh.ref)
            elif (dts[i].typ == DecreeToken.ItemType.OWNER): 
                if (kodeks): 
                    break
                if (dec.name is not None): 
                    break
                if (((i == 0 or i == (len(dts) - 1))) and dts[i].begin_token.chars.is_all_lower): 
                    break
                if (i == 0 and len(dts) > 1 and dts[1].typ == DecreeToken.ItemType.TYP): 
                    break
                if (dec.findSlot(DecreeReferent.ATTR_SOURCE, None, True) is not None): 
                    pass
                if (dts[i].ref is not None): 
                    ty = DecreeToken.getKind(dec.typ)
                    if (ty == DecreeKind.USTAV): 
                        if (not ((isinstance(dts[i].ref.referent, OrganizationReferent)))): 
                            break
                    dec.addSlot(DecreeReferent.ATTR_SOURCE, dts[i].ref.referent, False, 0).tag = dts[i].getSourceText()
                    if (isinstance(dts[i].ref.referent, PersonPropertyReferent)): 
                        dec.addExtReferent(dts[i].ref)
                else: 
                    dec.addSlot(DecreeReferent.ATTR_SOURCE, MiscHelper.convertFirstCharUpperAndOtherLower(dts[i].value), False, 0).tag = dts[i].getSourceText()
            elif (dts[i].typ == DecreeToken.ItemType.ORG): 
                if (kodeks): 
                    break
                if (dec.name is not None): 
                    break
                if (dec.findSlot(DecreeReferent.ATTR_SOURCE, None, True) is not None): 
                    if (i > 2 and dts[i - 1].typ == DecreeToken.ItemType.NUMBER and ((dts[i - 2].typ == DecreeToken.ItemType.ORG or dts[i - 2].typ == DecreeToken.ItemType.OWNER))): 
                        pass
                    elif (dts[i].begin_token.previous is not None and dts[i].begin_token.previous.is_and): 
                        pass
                    elif (i > 0 and ((dts[i - 1].typ == DecreeToken.ItemType.OWNER or dts[i - 1].typ == DecreeToken.ItemType.ORG))): 
                        pass
                    else: 
                        break
                sl = dec.addSlot(DecreeReferent.ATTR_SOURCE, dts[i].ref.referent, False, 0)
                sl.tag = dts[i].getSourceText()
                if (((i + 2) < len(dts)) and dts[i + 1].typ == DecreeToken.ItemType.UNKNOWN and (dts[i + 1].whitespaces_before_count < 2)): 
                    if (dts[i + 2].typ == DecreeToken.ItemType.NUMBER or dts[i + 2].typ == DecreeToken.ItemType.DATE): 
                        sl.tag = (MetaToken(dts[i].begin_token, dts[i + 1].end_token)).getSourceText()
                        i += 1
            elif (dts[i].typ == DecreeToken.ItemType.TERR): 
                if (dec.findSlot(DecreeReferent.ATTR_GEO, None, True) is not None): 
                    break
                if (i > 0 and dts[i - 1].typ == DecreeToken.ItemType.NAME): 
                    break
                if (dts[i].is_newline_before and ((i + 1) < len(dts)) and dts[i + 1].typ == DecreeToken.ItemType.DATE): 
                    break
                dec.addSlot(DecreeReferent.ATTR_GEO, dts[i].ref.referent, False, 0)
            elif (dts[i].typ == DecreeToken.ItemType.UNKNOWN): 
                if (dec.findSlot(DecreeReferent.ATTR_SOURCE, None, True) is not None): 
                    break
                if (kodeks): 
                    break
                if ((dec.kind == DecreeKind.CONTRACT and i == 1 and ((i + 1) < len(dts))) and dts[i + 1].typ == DecreeToken.ItemType.NUMBER): 
                    dec._addNameStr(MiscHelper.getTextValueOfMetaToken(dts[i], GetTextAttr.KEEPREGISTER))
                    continue
                if (i == 0): 
                    if (dec0 is None and not after_decree): 
                        break
                    ok1 = False
                    if (((i + 1) < len(dts)) and dts[i + 1].typ == DecreeToken.ItemType.NUMBER): 
                        ok1 = True
                    elif (((i + 2) < len(dts)) and dts[i + 1].typ == DecreeToken.ItemType.TERR and dts[i + 2].typ == DecreeToken.ItemType.NUMBER): 
                        ok1 = True
                    if (not ok1): 
                        break
                elif (dts[i - 1].typ == DecreeToken.ItemType.OWNER or dts[i - 1].typ == DecreeToken.ItemType.ORG): 
                    continue
                if ((i + 1) >= len(dts)): 
                    break
                if (dts[0].typ == DecreeToken.ItemType.TYP and dts[0].is_doubtful): 
                    break
                if (dts[i + 1].typ == DecreeToken.ItemType.NUMBER or dts[i + 1].typ == DecreeToken.ItemType.DATE or dts[i + 1].typ == DecreeToken.ItemType.NAME): 
                    dec.addSlot(DecreeReferent.ATTR_SOURCE, dts[i].value, False, 0).tag = dts[i].getSourceText()
                    continue
                if (dts[i + 1].typ == DecreeToken.ItemType.TERR): 
                    dec.addSlot(DecreeReferent.ATTR_SOURCE, dts[i].value, False, 0).tag = dts[i].getSourceText()
                    continue
                if (dts[i + 1].typ == DecreeToken.ItemType.OWNER): 
                    s = MiscHelper.getTextValue(dts[i].begin_token, dts[i + 1].end_token, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)
                    dts[i].end_token = dts[i + 1].end_token
                    dec.addSlot(DecreeReferent.ATTR_SOURCE, s, False, 0).tag = dts[i].getSourceText()
                    i += 1
                    continue
                break
            elif (dts[i].typ == DecreeToken.ItemType.MISC): 
                if (i == 0 or kodeks): 
                    break
                if ((i + 1) >= len(dts)): 
                    if (BracketHelper.canBeStartOfSequence(dts[i].end_token.next0_, True, False)): 
                        continue
                    if (i > 0 and dts[i - 1].typ == DecreeToken.ItemType.NUMBER): 
                        if (DecreeToken.tryAttachName(dts[i].end_token.next0_, None, True, False) is not None): 
                            continue
                elif (dts[i + 1].typ == DecreeToken.ItemType.NAME or dts[i + 1].typ == DecreeToken.ItemType.NUMBER or dts[i + 1].typ == DecreeToken.ItemType.DATE): 
                    continue
                break
            else: 
                break
        if (i == 0): 
            return None
        if (dec.typ is None or ((dec0 is not None and dts[0].typ != DecreeToken.ItemType.TYP))): 
            if (dec0 is not None): 
                if (dec.number is None and dec.date is None and dec.findSlot(DecreeReferent.ATTR_NAME, None, True) is None): 
                    return None
                if (dec.typ is None): 
                    dec.typ = dec0.typ
                if (dec.findSlot(DecreeReferent.ATTR_GEO, None, True) is None): 
                    dec.addSlot(DecreeReferent.ATTR_GEO, dec0.getStringValue(DecreeReferent.ATTR_GEO), False, 0)
                if (dec.findSlot(DecreeReferent.ATTR_DATE, None, True) is None and dec0.date is not None): 
                    dec.addSlot(DecreeReferent.ATTR_DATE, dec0.getSlotValue(DecreeReferent.ATTR_DATE), False, 0)
                if (dec.findSlot(DecreeReferent.ATTR_SOURCE, None, True) is None): 
                    sl = dec0.findSlot(DecreeReferent.ATTR_SOURCE, None, True)
                    if ((sl) is not None): 
                        dec.addSlot(DecreeReferent.ATTR_SOURCE, sl.value, False, 0).tag = sl.tag
            elif (base_typ is not None and after_decree): 
                dec.typ = base_typ.value
            else: 
                return None
        et = dts[i - 1].end_token
        if ((((not after_decree and len(dts) == i and i == 3) and dts[0].typ == DecreeToken.ItemType.TYP and dts[i - 1].typ == DecreeToken.ItemType.NUMBER) and dec.findSlot(DecreeReferent.ATTR_SOURCE, None, True) is not None and et.next0_ is not None) and et.next0_.is_comma and dec.number is not None): 
            tt = et.next0_
            while tt is not None: 
                if (not tt.isChar(',')): 
                    break
                ddd = DecreeToken.tryAttachList(tt.next0_, dts[0], 10, False)
                if (ddd is None or (len(ddd) < 2) or ddd[0].typ == DecreeToken.ItemType.TYP): 
                    break
                has_num = False
                for d in ddd: 
                    if (d.typ == DecreeToken.ItemType.NUMBER): 
                        has_num = True
                    elif (d.typ == DecreeToken.ItemType.TYP): 
                        has_num = False
                        break
                if (not has_num): 
                    break
                rtt = DecreeAnalyzer.__TryAttach(ddd, dts[0], True, ad)
                if (rtt is None): 
                    break
                dec.mergeSlots(rtt[0].referent, True)
                tt = rtt[0].end_token
                et = tt
                tt = tt.next0_
        if (((et.next0_ is not None and et.next0_.isChar('<') and (isinstance(et.next0_.next0_, ReferentToken))) and et.next0_.next0_.next0_ is not None and et.next0_.next0_.next0_.isChar('>')) and et.next0_.next0_.getReferent().type_name == "URI"): 
            et = et.next0_.next0_.next0_
        num = dec.number
        if ((dec.findSlot(DecreeReferent.ATTR_NAME, None, True) is None and (i < len(dts)) and dts[i].typ == DecreeToken.ItemType.TYP) and dec.kind == DecreeKind.PROJECT): 
            dts1 = list(dts)
            del dts1[0:0+i]
            rt1 = DecreeAnalyzer.__TryAttach(dts1, None, True, ad)
            if (rt1 is not None): 
                dec._addNameStr(MiscHelper.getTextValueOfMetaToken(rt1[0], GetTextAttr.KEEPREGISTER))
                et = rt1[0].end_token
        if (dec.findSlot(DecreeReferent.ATTR_NAME, None, True) is None and not kodeks and et.next0_ is not None): 
            dn = DecreeToken.tryAttachName((et.next0_.next0_ if et.next0_.isChar(':') else et.next0_), dec.typ, False, False)
            if (dn is not None and et.next0_.chars.is_all_lower and num is not None): 
                if (ad is not None): 
                    for r in ad.referents: 
                        if (r.findSlot(DecreeReferent.ATTR_NUMBER, num, True) is not None): 
                            if (r.canBeEquals(dec, Referent.EqualType.WITHINONETEXT)): 
                                if (r.findSlot(DecreeReferent.ATTR_NAME, dn.value, True) is None): 
                                    dn = (None)
                                break
            if (dn is not None): 
                if (dec.kind == DecreeKind.PROGRAM): 
                    tt1 = dn.end_token.previous
                    while tt1 is not None and tt1.begin_char > dn.begin_char: 
                        if (tt1.isChar(')') and tt1.previous is not None): 
                            tt1 = tt1.previous
                        if (isinstance(tt1.getReferent(), DateRangeReferent)): 
                            dec.addSlot(DecreeReferent.ATTR_DATE, tt1.getReferent(), False, 0)
                        elif ((isinstance(tt1.getReferent(), DateReferent)) and tt1.previous is not None and tt1.previous.isValue("ДО", None)): 
                            rt11 = tt1.kit.processReferent("DATE", tt1.previous)
                            if (rt11 is not None and (isinstance(rt11.referent, DateRangeReferent))): 
                                dec.addSlot(DecreeReferent.ATTR_DATE, rt11.referent, False, 0)
                                dec.addExtReferent(rt11)
                                tt1 = tt1.previous
                            else: 
                                break
                        elif ((isinstance(tt1.getReferent(), DateReferent)) and tt1.previous is not None and ((tt1.previous.isValue("НА", None) or tt1.previous.isValue("В", None)))): 
                            dec.addSlot(DecreeReferent.ATTR_DATE, tt1.getReferent(), False, 0)
                            tt1 = tt1.previous
                        else: 
                            break
                        tt1 = tt1.previous
                        first_pass2877 = True
                        while True:
                            if first_pass2877: first_pass2877 = False
                            else: tt1 = (None if tt1 is None else tt1.previous)
                            if (not (tt1 is not None and tt1.begin_char > dn.begin_char)): break
                            if (tt1.morph.class0_.is_conjunction or tt1.morph.class0_.is_preposition): 
                                continue
                            if (tt1.isValue("ПЕРИОД", "ПЕРІОД") or tt1.isValue("ПЕРСПЕКТИВА", None)): 
                                continue
                            if (tt1.isChar('(')): 
                                continue
                            break
                        if (tt1 is not None and tt1.end_char > dn.begin_char): 
                            if (dn.full_value is None): 
                                dn.full_value = dn.value
                            dn.value = MiscHelper.getTextValue(dn.begin_token, tt1, GetTextAttr.KEEPREGISTER)
                        tt1 = tt1.next0_
                        tt1 = (None if tt1 is None else tt1.previous)
                if (dn.full_value is not None): 
                    dec._addNameStr(dn.full_value)
                dec._addNameStr(dn.value)
                et = dn.end_token
                while True:
                    dn = DecreeToken.tryAttach(et.next0_, None, False)
                    if (dn is None): 
                        break
                    if (dn.typ == DecreeToken.ItemType.DATE and dec.date is None): 
                        if (dec._addDate(dn)): 
                            et = dn.end_token
                            continue
                    if (dn.typ == DecreeToken.ItemType.NUMBER and dec.number is None): 
                        dec._addNumber(dn)
                        et = dn.end_token
                        continue
                    if (dn.typ == DecreeToken.ItemType.DATERANGE and dec.kind == DecreeKind.PROGRAM): 
                        if (dec._addDate(dn)): 
                            et = dn.end_token
                            continue
                    break
        if (dec.findSlot(DecreeReferent.ATTR_SOURCE, None, True) is None): 
            tt0 = dts[0].begin_token.previous
            if ((tt0 is not None and tt0.isValue("В", "У") and tt0.previous is not None) and (isinstance(tt0.previous.getReferent(), OrganizationReferent))): 
                dec.addSlot(DecreeReferent.ATTR_SOURCE, tt0.previous.getReferent(), False, 0)
        if (not dec._checkCorrection(is_noun_doubt)): 
            ty = dec.typ
            sl = None
            if (dec0 is not None and dec.date is not None and dec.findSlot(DecreeReferent.ATTR_SOURCE, None, True) is None): 
                sl = dec0.findSlot(DecreeReferent.ATTR_SOURCE, None, True)
            if (sl is not None and (((((ty == "ПОСТАНОВЛЕНИЕ" or ty == "ПОСТАНОВА" or ty == "ОПРЕДЕЛЕНИЕ") or ty == "ВИЗНАЧЕННЯ" or ty == "РЕШЕНИЕ") or ty == "РІШЕННЯ" or ty == "ПРИГОВОР") or ty == "ВИРОК"))): 
                dec.addSlot(sl.type_name, sl.value, False, 0).tag = sl.tag
            else: 
                eq_decs = 0
                dr0 = None
                if (num is not None): 
                    if (ad is not None): 
                        for r in ad.referents: 
                            if (r.findSlot(DecreeReferent.ATTR_NUMBER, num, True) is not None): 
                                if (r.canBeEquals(dec, Referent.EqualType.WITHINONETEXT)): 
                                    eq_decs += 1
                                    dr0 = (Utils.asObjectOrNull(r, DecreeReferent))
                if (eq_decs == 1): 
                    dec.mergeSlots(dr0, True)
                else: 
                    ok1 = False
                    if (num is not None): 
                        tt = dts[0].begin_token.previous
                        while tt is not None: 
                            if (tt.isCharOf(":,") or tt.is_hiphen or BracketHelper.canBeStartOfSequence(tt, False, False)): 
                                pass
                            else: 
                                if (tt.isValue("ДАЛЕЕ", "ДАЛІ")): 
                                    ok1 = True
                                break
                            tt = tt.previous
                    if (not ok1): 
                        return None
        rt = ReferentToken(dec, dts[0].begin_token, et)
        if (morph_ is not None): 
            rt.morph = morph_
        if (rt.chars.is_all_lower): 
            if (dec.typ0 == "ДЕКЛАРАЦИЯ" or dec.typ0 == "ДЕКЛАРАЦІЯ"): 
                return None
            if (((dec.typ0 == "КОНСТИТУЦИЯ" or dec.typ0 == "КОНСТИТУЦІЯ")) and rt.begin_token == rt.end_token): 
                ok1 = False
                cou = 10
                tt = rt.begin_token.previous
                while tt is not None and cou > 0: 
                    if (tt.is_newline_after): 
                        break
                    pt = PartToken.tryAttach(tt, None, False, False)
                    if (pt is not None and pt.typ != PartToken.ItemType.PREFIX and pt.end_token.next0_ == rt.begin_token): 
                        ok1 = True
                        break
                    tt = tt.previous; cou -= 1
                if (not ok1): 
                    return None
        if (num is not None and ((num.find('/') > 0 or num.find(',') > 0))): 
            cou = 0
            for s in dec.slots: 
                if (s.type_name == DecreeReferent.ATTR_NUMBER): 
                    cou += 1
            if (cou == 1): 
                owns = 0
                for s in dec.slots: 
                    if (s.type_name == DecreeReferent.ATTR_SOURCE): 
                        owns += 1
                if (owns > 1): 
                    nums = Utils.splitString(num, '/', False)
                    nums2 = Utils.splitString(num, ',', False)
                    str_num = None
                    ii = 0
                    while ii < len(dts): 
                        if (dts[ii].typ == DecreeToken.ItemType.NUMBER): 
                            str_num = dts[ii].getSourceText()
                            break
                        ii += 1
                    if (len(nums2) == owns and owns > 1): 
                        dec.addSlot(DecreeReferent.ATTR_NUMBER, None, True, 0)
                        for n in nums2: 
                            dec.addSlot(DecreeReferent.ATTR_NUMBER, n.strip(), False, 0).tag = str_num
                    elif (len(nums) == owns and owns > 1): 
                        dec.addSlot(DecreeReferent.ATTR_NUMBER, None, True, 0)
                        for n in nums: 
                            dec.addSlot(DecreeReferent.ATTR_NUMBER, n.strip(), False, 0).tag = str_num
        if (BracketHelper.canBeStartOfSequence(rt.begin_token.previous, False, False) and BracketHelper.canBeEndOfSequence(rt.end_token.next0_, False, None, False)): 
            rt.begin_token = rt.begin_token.previous
            rt.end_token = rt.end_token.next0_
            dts1 = DecreeToken.tryAttachList(rt.end_token.next0_, None, 10, False)
            if (dts1 is not None and dts1[0].typ == DecreeToken.ItemType.DATE and dec.findSlot(DecreeReferent.ATTR_DATE, None, True) is None): 
                dec._addDate(dts1[0])
                rt.end_token = dts1[0].end_token
        if (dec.kind == DecreeKind.STANDARD and dec.name is None and BracketHelper.canBeStartOfSequence(rt.end_token.next0_, True, False)): 
            br = BracketHelper.tryParse(rt.end_token.next0_, BracketParseAttr.NO, 100)
            if (br is not None): 
                dec._addNameStr(MiscHelper.getTextValueOfMetaToken(br, GetTextAttr.KEEPREGISTER))
                rt.end_token = br.end_token
        if (dec.kind == DecreeKind.PROGRAM and dec.findSlot(DecreeReferent.ATTR_DATE, None, True) is None): 
            if (rt.begin_token.previous is not None and rt.begin_token.previous.isValue("ПАСПОРТ", None)): 
                cou = 0
                tt = rt.end_token.next0_
                first_pass2878 = True
                while True:
                    if first_pass2878: first_pass2878 = False
                    else: tt = (None if tt is None else tt.next0_)
                    if (not (tt is not None and (cou < 1000))): break
                    if (tt.isValue("СРОК", "ТЕРМІН") and tt.next0_ is not None and tt.next0_.isValue("РЕАЛИЗАЦИЯ", "РЕАЛІЗАЦІЯ")): 
                        pass
                    else: 
                        continue
                    tt = tt.next0_.next0_
                    if (tt is None): 
                        break
                    dtok = DecreeToken.tryAttach(tt, None, False)
                    if (dtok is not None and dtok.typ == DecreeToken.ItemType.TYP and ((dtok.value == "ПРОГРАММА" or dtok.value == "ПРОГРАМА"))): 
                        tt = dtok.end_token.next0_
                    while tt is not None: 
                        if (tt.is_hiphen or tt.is_table_control_char or tt.isValue("ПРОГРАММА", "ПРОГРАМА")): 
                            pass
                        elif (isinstance(tt.getReferent(), DateRangeReferent)): 
                            dec.addSlot(DecreeReferent.ATTR_DATE, tt.getReferent(), False, 0)
                            break
                        else: 
                            break
                        tt = tt.next0_
                    break
        if (rt.end_token.next0_ is not None and rt.end_token.next0_.isChar('(')): 
            dt = None
            tt = rt.end_token.next0_.next0_
            first_pass2879 = True
            while True:
                if first_pass2879: first_pass2879 = False
                else: tt = tt.next0_
                if (not (tt is not None)): break
                r = tt.getReferent()
                if (isinstance(r, GeoReferent)): 
                    continue
                if (isinstance(r, DateReferent)): 
                    dt = (Utils.asObjectOrNull(r, DateReferent))
                    continue
                if (tt.morph.class0_.is_preposition): 
                    continue
                if (tt.morph.class0_.is_verb): 
                    continue
                if (tt.isChar(')') and dt is not None): 
                    dec.addSlot(DecreeReferent.ATTR_DATE, dt, False, 0)
                    rt.end_token = tt
                break
        rt_li = list()
        if (((i + 1) < len(dts)) and dts[i].typ == DecreeToken.ItemType.EDITION and not dts[i].is_newline_before): 
            del dts[0:0+i + 1]
            ed = DecreeAnalyzer._tryAttach(dts, base_typ, ad)
            if (ed is not None and len(ed) > 0): 
                rt_li.extend(ed)
                for e0_ in ed: 
                    dec.addSlot(DecreeReferent.ATTR_EDITION, e0_.referent, False, 0)
                rt.end_token = ed[len(ed) - 1].end_token
        rt_li.append(rt)
        if (num_tok is not None and num_tok.children is not None): 
            end = rt.end_token
            rt.end_token = num_tok.children[0].begin_token.previous
            if (rt.end_token.is_comma_and): 
                rt.end_token = rt.end_token.previous
            ii = 0
            while ii < len(num_tok.children): 
                dr1 = DecreeReferent()
                for s in rt.referent.slots: 
                    if (s.type_name == DecreeReferent.ATTR_NUMBER): 
                        dr1.addSlot(s.type_name, num_tok.children[ii].value, False, 0).tag = num_tok.children[ii].getSourceText()
                    else: 
                        ss = dr1.addSlot(s.type_name, s.value, False, 0)
                        if (ss is not None): 
                            ss.tag = s.tag
                rt1 = ReferentToken(dr1, num_tok.children[ii].begin_token, num_tok.children[ii].end_token)
                if (ii == (len(num_tok.children) - 1)): 
                    rt1.end_token = end
                rt_li.append(rt1)
                ii += 1
        if ((len(dts) == 2 and dts[0].typ == DecreeToken.ItemType.TYP and dts[0].typ_kind == DecreeKind.STANDARD) and dts[1].typ == DecreeToken.ItemType.NUMBER): 
            ttt = dts[1].end_token.next0_
            while ttt is not None: 
                if (not ttt.is_comma_and): 
                    break
                nu = DecreeToken.tryAttach(ttt.next0_, dts[0], False)
                if (nu is None or nu.typ != DecreeToken.ItemType.NUMBER): 
                    break
                dr1 = DecreeReferent._new1094(dec.typ)
                dr1._addNumber(nu)
                rt_li.append(ReferentToken(dr1, ttt.next0_, nu.end_token))
                if (not ttt.is_comma): 
                    break
                ttt = nu.end_token
                ttt = ttt.next0_
        return rt_li
    
    @staticmethod
    def _tryAttachParts(parts : typing.List['PartToken'], base_typ : 'DecreeToken', _def_owner : 'Referent') -> typing.List['MetaToken']:
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.decree.DecreeReferent import DecreeReferent
        from pullenti.ner.instrument.internal.InstrToken1 import InstrToken1
        from pullenti.ner.decree.internal.PartToken import PartToken
        from pullenti.ner.decree.DecreePartReferent import DecreePartReferent
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.decree.internal.DecreeToken import DecreeToken
        from pullenti.ner.instrument.internal.InstrToken import InstrToken
        from pullenti.morph.MorphClass import MorphClass
        if (parts is None or len(parts) == 0): 
            return None
        tt = parts[len(parts) - 1].end_token.next0_
        if (_def_owner is not None and tt is not None): 
            if (BracketHelper.isBracket(tt, False)): 
                br = BracketHelper.tryParse(tt, BracketParseAttr.NO, 100)
                if (br is not None and br.end_token.next0_ is not None): 
                    tt = br.end_token.next0_
            if (isinstance(tt.getReferent(), DecreeReferent)): 
                _def_owner = (None)
            elif (tt.isValue("К", None) and tt.next0_ is not None and (isinstance(tt.next0_.getReferent(), DecreeReferent))): 
                _def_owner = (None)
        if ((len(parts) == 1 and parts[0].is_newline_before and parts[0].begin_token.chars.is_letter) and not parts[0].begin_token.chars.is_all_lower): 
            t1 = parts[0].end_token.next0_
            br = BracketHelper.tryParse(t1, BracketParseAttr.NO, 100)
            if (br is not None): 
                t1 = br.end_token.next0_
            if (t1 is not None and (isinstance(t1.getReferent(), DecreeReferent)) and not parts[0].is_newline_after): 
                pass
            else: 
                li = InstrToken1.parse(parts[0].begin_token, True, None, 0, None, False, 0, False)
                if (li is not None and li.has_verb): 
                    if ((len(parts) == 1 and parts[0].typ == PartToken.ItemType.PART and "резолют" in str(parts[0])) and parts[0].is_newline_before): 
                        return None
                else: 
                    return None
        this_dec = None
        is_program = False
        is_add_agree = False
        if (parts[len(parts) - 1].typ != PartToken.ItemType.SUBPROGRAM and parts[len(parts) - 1].typ != PartToken.ItemType.ADDAGREE): 
            this_dec = DecreeAnalyzer.ThisDecree.tryAttach(parts[len(parts) - 1], base_typ)
            if (this_dec is not None): 
                if ((isinstance(_def_owner, DecreeReferent)) and (((Utils.asObjectOrNull(_def_owner, DecreeReferent)).typ0 == this_dec.typ or parts[0].typ == PartToken.ItemType.APPENDIX))): 
                    pass
                else: 
                    _def_owner = (None)
            if (this_dec is None and _def_owner is None): 
                this_dec = DecreeAnalyzer.ThisDecree.tryAttachBack(parts[0].begin_token, base_typ)
            if (this_dec is None): 
                for p in parts: 
                    if (p.typ == PartToken.ItemType.PART): 
                        has_clause = False
                        for pp in parts: 
                            if (pp != p): 
                                if (PartToken._getRank(pp.typ) >= PartToken._getRank(PartToken.ItemType.CLAUSE)): 
                                    has_clause = True
                        if (isinstance(_def_owner, DecreePartReferent)): 
                            if ((Utils.asObjectOrNull(_def_owner, DecreePartReferent)).clause is not None): 
                                has_clause = True
                        if (not has_clause): 
                            p.typ = PartToken.ItemType.DOCPART
                        elif ((((p == parts[len(parts) - 1] and p.end_token.next0_ is not None and len(p.values) == 1) and (isinstance(p.end_token.next0_.getReferent(), DecreeReferent)) and (isinstance(p.begin_token, TextToken))) and (Utils.asObjectOrNull(p.begin_token, TextToken)).term == "ЧАСТИ" and (isinstance(p.end_token, NumberToken))) and p.begin_token.next0_ == p.end_token): 
                            p.typ = PartToken.ItemType.DOCPART
        elif (parts[len(parts) - 1].typ == PartToken.ItemType.ADDAGREE): 
            is_add_agree = True
        else: 
            if (len(parts) > 1): 
                del parts[0:0+len(parts) - 1]
            is_program = True
        def_owner = Utils.asObjectOrNull(_def_owner, DecreeReferent)
        if (isinstance(_def_owner, DecreePartReferent)): 
            def_owner = (Utils.asObjectOrNull(_def_owner, DecreePartReferent)).owner
        res = list()
        has_prefix = False
        if (parts[0].typ == PartToken.ItemType.PREFIX): 
            del parts[0]
            has_prefix = True
            if (len(parts) == 0): 
                return None
        if ((len(parts) == 1 and this_dec is None and parts[0].typ != PartToken.ItemType.SUBPROGRAM) and parts[0].typ != PartToken.ItemType.ADDAGREE): 
            if (parts[0].is_doubt): 
                return None
            if (parts[0].is_newline_before and len(parts[0].values) <= 1): 
                tt1 = parts[0].end_token
                if (tt1.next0_ is None): 
                    return None
                tt1 = tt1.next0_
                if (BracketHelper.canBeStartOfSequence(tt1, False, False)): 
                    br = BracketHelper.tryParse(tt1, BracketParseAttr.NO, 100)
                    if (br is not None and br.end_token.next0_ is not None): 
                        tt1 = br.end_token.next0_
                if (tt1.isChar(',')): 
                    pass
                elif (isinstance(tt1.getReferent(), DecreeReferent)): 
                    pass
                elif (tt1.isValue("К", None) and tt1.next0_ is not None and (isinstance(tt1.next0_.getReferent(), DecreeReferent))): 
                    pass
                elif (DecreeAnalyzer._checkOtherTyp(tt1, True) is not None): 
                    pass
                elif (_def_owner is None): 
                    return None
                elif (MiscHelper.canBeStartOfSentence(tt1)): 
                    return None
                elif (tt1.isChar('.')): 
                    return None
        asc = list()
        desc = list()
        typs = list()
        asc_count = 0
        desc_count = 0
        terminators = 0
        i = 0
        while i < (len(parts) - 1): 
            if (not parts[i].has_terminator): 
                if (parts[i].canBeNextNarrow(parts[i + 1])): 
                    asc_count += 1
                if (parts[i + 1].canBeNextNarrow(parts[i])): 
                    desc_count += 1
            elif ((asc_count > 0 and len(parts[i].values) == 1 and len(parts[i + 1].values) == 1) and parts[i].canBeNextNarrow(parts[i + 1])): 
                asc_count += 1
            elif ((desc_count > 0 and len(parts[i].values) == 1 and len(parts[i + 1].values) == 1) and parts[i + 1].canBeNextNarrow(parts[i])): 
                desc_count += 1
            else: 
                terminators += 1
            i += 1
        if (terminators == 0 and ((((desc_count > 0 and asc_count == 0)) or ((desc_count == 0 and asc_count > 0))))): 
            i = 0
            while i < (len(parts) - 1): 
                parts[i].has_terminator = False
                i += 1
        i = 0
        first_pass2880 = True
        while True:
            if first_pass2880: first_pass2880 = False
            else: i += 1
            if (not (i < len(parts))): break
            if (parts[i].typ == PartToken.ItemType.PREFIX): 
                continue
            asc.clear()
            asc.append(parts[i])
            typs.clear()
            typs.append(parts[i].typ)
            j = (i + 1)
            while j < len(parts): 
                if (len(parts[j].values) == 0 and parts[j].typ != PartToken.ItemType.PREAMBLE): 
                    break
                elif (not parts[j].typ in typs and parts[j - 1].canBeNextNarrow(parts[j])): 
                    if (parts[j - 1].delim_after and terminators == 0): 
                        if (desc_count > asc_count): 
                            break
                        if (((j + 1) < len(parts)) and not parts[j].delim_after and not parts[j].has_terminator): 
                            break
                        if (parts[j - 1].typ == PartToken.ItemType.ITEM and parts[j].typ == PartToken.ItemType.SUBITEM): 
                            if (len(parts[j].values) > 0 and "." in str(parts[j].values[0])): 
                                break
                    asc.append(parts[j])
                    typs.append(parts[j].typ)
                    if (parts[j].has_terminator): 
                        break
                else: 
                    break
                j += 1
            desc.clear()
            desc.append(parts[i])
            typs.clear()
            typs.append(parts[i].typ)
            j = (i + 1)
            while j < len(parts): 
                if (len(parts[j].values) == 0 and parts[j].typ != PartToken.ItemType.PREAMBLE): 
                    break
                elif (((not parts[j].typ in typs or parts[j].typ == PartToken.ItemType.SUBITEM)) and parts[j].canBeNextNarrow(parts[j - 1])): 
                    if (parts[j - 1].delim_after and terminators == 0): 
                        if (desc_count <= asc_count): 
                            break
                    desc.append(parts[j])
                    typs.append(parts[j].typ)
                    if (parts[j].has_terminator): 
                        break
                elif (((not parts[j].typ in typs and parts[j - 1].canBeNextNarrow(parts[j]) and (j + 1) == (len(parts) - 1)) and parts[j + 1].canBeNextNarrow(parts[j]) and parts[j + 1].canBeNextNarrow(parts[j - 1])) and not parts[j].has_terminator): 
                    desc.insert(len(desc) - 1, parts[j])
                    typs.append(parts[j].typ)
                else: 
                    break
                j += 1
            desc.reverse()
            li = (desc if len(asc) < len(desc) else asc)
            j = 0
            while j < len(li): 
                li[j].ind = 0
                j += 1
            while True:
                dr = DecreePartReferent()
                rt = ReferentToken(dr, parts[i].begin_token, parts[(i + len(li)) - 1].end_token)
                if (parts[i].name is not None): 
                    dr.addSlot(DecreePartReferent.ATTR_NAME, parts[i].name, False, 0)
                res.append(rt)
                sl_list = list()
                for p in li: 
                    nam = PartToken._getAttrNameByTyp(p.typ)
                    if (nam is not None): 
                        sl = Slot._new1095(nam, p, 1)
                        sl_list.append(sl)
                        if (p.ind < len(p.values)): 
                            sl.value = p.values[p.ind]
                            if (Utils.isNullOrEmpty(p.values[p.ind].value)): 
                                sl.value = "0"
                        else: 
                            sl.value = "0"
                    if (p.ind > 0): 
                        rt.begin_token = p.values[p.ind].begin_token
                    if ((p.ind + 1) < len(p.values)): 
                        rt.end_token = p.values[p.ind].end_token
                for p in parts: 
                    for s in sl_list: 
                        if (s.tag == p): 
                            dr.addSlot(s.type_name, s.value, False, 0)
                            break
                for j in range(len(li) - 1, -1, -1):
                    li[j].ind += 1
                    if ((li[j].ind) >= len(li[j].values)): 
                        li[j].ind = 0
                    else: 
                        break
                else: j = -1
                if (j < 0): 
                    break
            i += (len(li) - 1)
        if (len(res) == 0): 
            return None
        for j in range(len(res) - 1, 0, -1):
            d0 = Utils.asObjectOrNull(res[j].referent, DecreePartReferent)
            d = Utils.asObjectOrNull(res[j - 1].referent, DecreePartReferent)
            if (d0.clause is not None and d.clause is None): 
                d.clause = d0.clause
        else: j = 0
        tt = parts[i - 1].end_token
        owner = def_owner
        te = tt.next0_
        if ((te is not None and owner is None and te.isChar('(')) and parts[0].typ != PartToken.ItemType.SUBPROGRAM and parts[0].typ != PartToken.ItemType.ADDAGREE): 
            br = BracketHelper.tryParse(te, BracketParseAttr.NO, 100)
            if (br is not None): 
                if (te.next0_.morph.class0_.is_adverb): 
                    pass
                elif (isinstance(te.next0_.getReferent(), DecreeReferent)): 
                    if (owner is None and te.next0_.next0_ == br.end_token): 
                        owner = (Utils.asObjectOrNull(te.next0_.getReferent(), DecreeReferent))
                        te = br.end_token
                else: 
                    s = MiscHelper.getTextValueOfMetaToken(br, GetTextAttr.NO)
                    if (s is not None): 
                        rt = res[len(res) - 1]
                        (Utils.asObjectOrNull(rt.referent, DecreePartReferent))._addName(s)
                        rt.end_token = br.end_token
                        te = rt.end_token.next0_
        if (te is not None and te.isCharOf(",;")): 
            te = te.next0_
        if (owner is None and (isinstance(te, ReferentToken))): 
            owner = Utils.asObjectOrNull(te.getReferent(), DecreeReferent)
            if ((owner) is not None): 
                res[len(res) - 1].end_token = te
        if (owner is None): 
            j = 0
            while j < i: 
                owner = parts[j].decree
                if ((owner) is not None): 
                    break
                j += 1
        if (te is not None and te.isValue("К", None) and te.next0_ is not None): 
            if (isinstance(te.next0_.getReferent(), DecreeReferent)): 
                te = te.next0_
                res[len(res) - 1].end_token = te
                owner = (Utils.asObjectOrNull(te.getReferent(), DecreeReferent))
            elif (owner is not None and this_dec is not None and this_dec.end_char > te.end_char): 
                res[len(res) - 1].end_token = this_dec.end_token
        if (owner is None and this_dec is not None): 
            tt0 = res[0].begin_token
            if (tt0.previous is not None and tt0.previous.isChar('(')): 
                tt0 = tt0.previous
            if (tt0.previous is not None): 
                owner = Utils.asObjectOrNull(tt0.previous.getReferent(), DecreeReferent)
                if ((owner) is not None): 
                    if (this_dec.typ == owner.typ0): 
                        this_dec = (None)
                    else: 
                        owner = (None)
        if (owner is None and this_dec is not None and this_dec.real is not None): 
            owner = this_dec.real
        if (owner is not None and parts[0].typ == PartToken.ItemType.SUBPROGRAM and owner.kind != DecreeKind.PROGRAM): 
            owner = (None)
        if (owner is not None and parts[0].typ == PartToken.ItemType.ADDAGREE and owner.kind != DecreeKind.CONTRACT): 
            owner = (None)
        owner_paer = None
        loc_typ = None
        if ((this_dec is None or not this_dec.has_this_ref)): 
            anafor_ref = None
            for p in parts: 
                anafor_ref = p.anafor_ref
                if ((anafor_ref) is not None): 
                    break
            is_change_word_after = False
            tt2 = res[len(res) - 1].end_token.next0_
            if (tt2 is not None): 
                if (((tt2.isChar(':') or tt2.isValue("ДОПОЛНИТЬ", None) or tt2.isValue("СЛОВО", None)) or tt2.isValue("ИСКЛЮЧИТЬ", None) or tt2.isValue("ИЗЛОЖИТЬ", None)) or tt2.isValue("СЧИТАТЬ", None) or tt2.isValue("ПРИЗНАТЬ", None)): 
                    is_change_word_after = True
            tt2 = parts[0].begin_token.previous
            if (tt2 is not None): 
                if (((tt2.isValue("ДОПОЛНИТЬ", None) or tt2.isValue("ИСКЛЮЧИТЬ", None) or tt2.isValue("ИЗЛОЖИТЬ", None)) or tt2.isValue("СЧИТАТЬ", None) or tt2.isValue("УСТАНОВЛЕННЫЙ", None)) or tt2.isValue("ОПРЕДЕЛЕННЫЙ", None)): 
                    is_change_word_after = True
            cou = 0
            ugol_delo = False
            brack_level = 0
            bt = None
            coef_before = 0
            is_over_brr = False
            if (parts[0].begin_token.previous is not None and parts[0].begin_token.previous.isChar('(')): 
                if (parts[len(parts) - 1].end_token.next0_ is not None and parts[len(parts) - 1].end_token.next0_.isChar(')')): 
                    if (len(parts) == 1 and parts[0].typ == PartToken.ItemType.APPENDIX): 
                        pass
                    else: 
                        is_over_brr = True
                        if (owner is not None and DecreeAnalyzer._getDecree(parts[0].begin_token.previous.previous) is not None): 
                            owner = (None)
            tt = parts[0].begin_token.previous
            first_pass2881 = True
            while True:
                if first_pass2881: first_pass2881 = False
                else: tt = tt.previous; coef_before += 1
                if (not (tt is not None)): break
                if (tt.is_newline_after): 
                    coef_before += 2
                    if (((anafor_ref is None and not is_over_brr and not ugol_delo) and this_dec is None and not is_change_word_after) and not is_program and not is_add_agree): 
                        if (not tt.is_table_control_char): 
                            break
                if (this_dec is not None and this_dec.has_this_ref): 
                    break
                if (tt.is_table_control_char): 
                    break
                if (tt.morph.class0_.is_preposition): 
                    coef_before -= 1
                    continue
                if (isinstance(tt, TextToken)): 
                    if (BracketHelper.canBeEndOfSequence(tt, False, None, False)): 
                        brack_level += 1
                        continue
                    if (BracketHelper.canBeStartOfSequence(tt, False, False)): 
                        if (tt.isChar('(') and tt == parts[0].begin_token.previous): 
                            pass
                        else: 
                            brack_level -= 1
                            coef_before -= 1
                        continue
                if (tt.is_newline_before): 
                    brack_level = 0
                cou += 1
                if ((cou) > 100): 
                    if (((ugol_delo or is_program or is_add_agree) or anafor_ref is not None or this_dec is not None) or is_over_brr): 
                        if (cou > 1000): 
                            break
                    elif (is_change_word_after): 
                        if (cou > 250): 
                            break
                    else: 
                        break
                if (cou < 4): 
                    if (tt.isValue("УГОЛОВНЫЙ", "КРИМІНАЛЬНИЙ") and tt.next0_ is not None and tt.next0_.isValue("ДЕЛО", "СПРАВА")): 
                        ugol_delo = True
                if (tt.isCharOf(".")): 
                    coef_before += 50
                    if (tt.is_newline_after): 
                        coef_before += 100
                    continue
                if (brack_level > 0): 
                    continue
                dr = DecreeAnalyzer._getDecree(tt)
                if (dr is not None and dr.kind != DecreeKind.PUBLISHER): 
                    if (ugol_delo and ((dr.name == "УГОЛОВНЫЙ КОДЕКС" or dr.name == "КРИМІНАЛЬНИЙ КОДЕКС"))): 
                        coef_before = 0
                    if (dr.kind == DecreeKind.PROGRAM): 
                        if (is_program): 
                            bt = tt
                            break
                        else: 
                            continue
                    if (dr.kind == DecreeKind.CONTRACT): 
                        if (is_add_agree): 
                            bt = tt
                            break
                        elif (this_dec is not None and ((dr.typ == this_dec.typ or dr.typ0 == this_dec.typ))): 
                            bt = tt
                            break
                        else: 
                            continue
                    if (this_dec is not None): 
                        dpr = Utils.asObjectOrNull(tt.getReferent(), DecreePartReferent)
                        if (this_dec.typ == dr.typ or this_dec.typ == dr.typ0): 
                            pass
                        elif ((this_dec.has_other_ref and dpr is not None and dpr.clause is not None) and this_dec.typ == "СТАТЬЯ"): 
                            for r in res: 
                                dpr0 = Utils.asObjectOrNull(r.referent, DecreePartReferent)
                                if (dpr0.clause is None): 
                                    dpr0.clause = dpr.clause
                                    dpr0.owner = dpr.owner
                                    owner = dpr0.owner
                        else: 
                            continue
                    elif (is_change_word_after): 
                        if (owner is None): 
                            coef_before = 0
                        elif (owner == DecreeAnalyzer._getDecree(tt)): 
                            coef_before = 0
                    bt = tt
                    break
                if (dr is not None): 
                    continue
                dpr2 = Utils.asObjectOrNull(tt.getReferent(), DecreePartReferent)
                if (dpr2 is not None): 
                    bt = tt
                    break
                dit = DecreeToken.tryAttach(tt, None, False)
                if (dit is not None and dit.typ == DecreeToken.ItemType.TYP): 
                    if (this_dec is not None): 
                        continue
                    if (dit.chars.is_capital_upper or anafor_ref is not None): 
                        bt = tt
                        break
            cou = 0
            at = None
            coef_after = 0
            aloc_typ = None
            tt0 = parts[len(parts) - 1].end_token.next0_
            has_newline = False
            ttt = parts[len(parts) - 1].begin_token
            while ttt.end_char < parts[len(parts) - 1].end_char: 
                if (ttt.is_newline_after): 
                    has_newline = True
                ttt = ttt.next0_
            tt = tt0
            first_pass2882 = True
            while True:
                if first_pass2882: first_pass2882 = False
                else: tt = tt.next0_; coef_after += 1
                if (not (tt is not None)): break
                if (owner is not None and coef_after > 0): 
                    break
                if (tt.is_newline_before): 
                    break
                if (tt.is_table_control_char): 
                    break
                if (tt.isValue("СМ", None)): 
                    break
                if (anafor_ref is not None): 
                    break
                if (this_dec is not None): 
                    if (tt != tt0): 
                        break
                    if (this_dec.real is not None): 
                        break
                if (InstrToken._checkEntered(tt) is not None): 
                    break
                if (tt.morph.class0_.is_preposition or tt.is_comma_and): 
                    coef_after -= 1
                    continue
                if (tt.morph.class0_ == MorphClass.VERB): 
                    break
                if (BracketHelper.canBeEndOfSequence(tt, False, None, False)): 
                    break
                pts = PartToken.tryAttachList(tt, False, 40)
                if (pts is not None): 
                    tt = pts[len(pts) - 1].end_token
                    coef_after -= 1
                    ttnn = tt.next0_
                    if (ttnn is not None and ttnn.isChar('.')): 
                        ttnn = ttnn.next0_
                    dit = DecreeToken.tryAttach(ttnn, None, False)
                    if (dit is not None and dit.typ == DecreeToken.ItemType.TYP): 
                        loc_typ = dit.value
                        break
                    continue
                if (BracketHelper.canBeStartOfSequence(tt, False, False)): 
                    br = BracketHelper.tryParse(tt, BracketParseAttr.NO, 100)
                    if (br is not None): 
                        coef_after -= 1
                        tt = br.end_token
                        continue
                cou += 1
                if ((cou) > 100): 
                    break
                if (cou > 1 and has_newline): 
                    break
                if (tt.isCharOf(".")): 
                    coef_after += 50
                    if (tt.is_newline_after): 
                        coef_after += 100
                    continue
                dr = Utils.asObjectOrNull(tt.getReferent(), DecreeReferent)
                if (dr is not None and dr.kind != DecreeKind.PUBLISHER): 
                    if (dr.kind == DecreeKind.PROGRAM): 
                        if (is_program): 
                            at = tt
                            break
                        else: 
                            continue
                    if (dr.kind == DecreeKind.CONTRACT): 
                        if (is_add_agree): 
                            at = tt
                            break
                        else: 
                            continue
                    at = tt
                    break
                if (is_program or is_add_agree): 
                    break
                if (dr is not None): 
                    continue
                tte2 = DecreeAnalyzer._checkOtherTyp(tt, tt == tt0)
                if (tte2 is not None): 
                    at = tte2
                    if (tt == tt0 and this_dec is not None and this_dec.real is None): 
                        if (this_dec.typ == ((Utils.asObjectOrNull(at.tag, str)))): 
                            at = (None)
                        else: 
                            this_dec = (None)
                    break
            if (bt is not None and at is not None): 
                if (coef_before < coef_after): 
                    at = (None)
                else: 
                    bt = (None)
            if (owner is None): 
                if (at is not None): 
                    owner = DecreeAnalyzer._getDecree(at)
                    if (isinstance(at, TextToken)): 
                        if (isinstance(at.tag, str)): 
                            loc_typ = (Utils.asObjectOrNull(at.tag, str))
                        else: 
                            loc_typ = (Utils.asObjectOrNull(at, TextToken)).lemma
                elif (bt is not None): 
                    owner = DecreeAnalyzer._getDecree(bt)
                    owner_paer = (Utils.asObjectOrNull(bt.getReferent(), DecreePartReferent))
                    if (owner_paer is not None and loc_typ is None): 
                        loc_typ = owner_paer.local_typ
            elif (coef_after == 0 and at is not None): 
                owner = DecreeAnalyzer._getDecree(at)
            elif (coef_before == 0 and bt is not None): 
                owner = DecreeAnalyzer._getDecree(bt)
                owner_paer = (Utils.asObjectOrNull(bt.getReferent(), DecreePartReferent))
                if (owner_paer is not None and loc_typ is None): 
                    loc_typ = owner_paer.local_typ
            if (((bt is not None and len(parts) == 1 and parts[0].typ == PartToken.ItemType.DOCPART) and (isinstance(bt.getReferent(), DecreePartReferent)) and (Utils.asObjectOrNull(bt.getReferent(), DecreePartReferent)).clause is not None) and len(res) == 1 and owner == (Utils.asObjectOrNull(bt.getReferent(), DecreePartReferent)).owner): 
                for s in res[0].referent.slots: 
                    if (s.type_name == DecreePartReferent.ATTR_DOCPART): 
                        s.type_name = DecreePartReferent.ATTR_PART
                (Utils.asObjectOrNull(res[0].referent, DecreePartReferent))._addHighLevelInfo(Utils.asObjectOrNull(bt.getReferent(), DecreePartReferent))
        if (owner is None): 
            if (this_dec is None and loc_typ is None): 
                if ((len(parts) == 1 and len(parts[0].values) == 1 and parts[0].typ == PartToken.ItemType.APPENDIX) and parts[0].begin_token.chars.is_capital_upper): 
                    pass
                elif ((parts[0].begin_token.previous is not None and parts[0].begin_token.previous.isChar('(') and parts[len(parts) - 1].end_token.next0_ is not None) and parts[len(parts) - 1].end_token.next0_.isChar(')')): 
                    if (parts[0].typ == PartToken.ItemType.PAGE): 
                        return None
                else: 
                    return None
            for r in res: 
                dr = Utils.asObjectOrNull(r.referent, DecreePartReferent)
                if (this_dec is not None): 
                    dr.local_typ = this_dec.typ
                    if (this_dec.begin_char > r.end_char and r == res[len(res) - 1]): 
                        r.end_token = this_dec.end_token
                elif (loc_typ is not None): 
                    if (loc_typ == "СТАТЬЯ" and dr.clause is not None): 
                        pass
                    elif (loc_typ == "ГЛАВА" and dr.chapter is not None): 
                        pass
                    elif (loc_typ == "ПАРАГРАФ" and dr.paragraph is not None): 
                        pass
                    elif (loc_typ == "ЧАСТЬ" and dr.part is not None): 
                        pass
                    else: 
                        dr.local_typ = loc_typ
                        if (r == res[len(res) - 1] and not r.is_newline_after): 
                            ttt1 = r.end_token.next0_
                            if (ttt1 is not None and ttt1.is_comma): 
                                ttt1 = ttt1.next0_
                            at = DecreeAnalyzer._checkOtherTyp(ttt1, True)
                            if (at is not None and ((Utils.asObjectOrNull(at.tag, str))) == loc_typ): 
                                r.end_token = at
        else: 
            for r in res: 
                dr = Utils.asObjectOrNull(r.referent, DecreePartReferent)
                dr.owner = owner
                if (this_dec is not None and this_dec.real == owner): 
                    if (this_dec.begin_char > r.end_char and r == res[len(res) - 1]): 
                        r.end_token = this_dec.end_token
        if (len(res) > 0): 
            rt = res[len(res) - 1]
            tt = rt.end_token.next0_
            if (owner is not None and tt is not None and tt.getReferent() == owner): 
                rt.end_token = tt
                tt = tt.next0_
            if (tt is not None and ((tt.is_hiphen or tt.isChar(':')))): 
                tt = tt.next0_
            br = BracketHelper.tryParse(tt, (BracketParseAttr.CANBEMANYLINES if is_program else BracketParseAttr.NO), 100)
            if (br is not None): 
                ok = True
                if (br.open_char == '('): 
                    if (parts[0].typ == PartToken.ItemType.SUBPROGRAM): 
                        ok = False
                    else: 
                        ttt = tt.next0_
                        while ttt is not None and (ttt.end_char < br.end_char): 
                            if (ttt == tt.next0_ and tt.next0_.morph.class0_.is_adverb): 
                                ok = False
                            if ((isinstance(ttt.getReferent(), DecreeReferent)) or (isinstance(ttt.getReferent(), DecreePartReferent))): 
                                ok = False
                            if (ttt.isValue("РЕДАКЦИЯ", None) and ttt == br.end_token.previous): 
                                ok = False
                            ttt = ttt.next0_
                if (ok): 
                    s = MiscHelper.getTextValueOfMetaToken(br, GetTextAttr.NO)
                    if (s is not None): 
                        (Utils.asObjectOrNull(rt.referent, DecreePartReferent))._addName(s)
                        rt.end_token = br.end_token
                        if ((isinstance(rt.end_token.next0_, ReferentToken)) and rt.end_token.next0_.getReferent() == owner): 
                            rt.end_token = rt.end_token.next0_
            elif ((is_program and len(parts[0].values) > 0 and tt is not None) and tt.is_table_control_char and MiscHelper.canBeStartOfSentence(tt.next0_)): 
                tt1 = tt.next0_
                while tt1 is not None: 
                    if (tt1.is_table_control_char): 
                        s = MiscHelper.getTextValue(tt.next0_, tt1.previous, GetTextAttr.NO)
                        if (s is not None): 
                            (Utils.asObjectOrNull(rt.referent, DecreePartReferent))._addName(s)
                            rt.end_token = tt1
                        break
                    elif (tt1.is_newline_before): 
                        break
                    tt1 = tt1.next0_
            if (this_dec is not None): 
                if (this_dec.end_char > res[len(res) - 1].end_char): 
                    res[len(res) - 1].end_token = this_dec.end_token
        if (owner_paer is not None): 
            ii = 0
            while ii < len(res): 
                (Utils.asObjectOrNull(res[ii].referent, DecreePartReferent))._addHighLevelInfo((owner_paer if ii == 0 else Utils.asObjectOrNull(res[ii - 1].referent, DecreePartReferent)))
                ii += 1
        if (len(res) == 1 and (Utils.asObjectOrNull(res[0].referent, DecreePartReferent)).name is None): 
            if ((res[0].begin_token.previous is not None and res[0].begin_token.previous.isChar('(') and res[0].end_token.next0_ is not None) and res[0].end_token.next0_.isChar(')')): 
                if (BracketHelper.canBeEndOfSequence(res[0].begin_token.previous.previous, False, None, False)): 
                    tt = res[0].begin_token.previous.previous.previous
                    while tt is not None: 
                        if (tt.is_newline_after): 
                            break
                        if (BracketHelper.canBeStartOfSequence(tt, False, False)): 
                            if (tt.next0_.chars.is_letter and not tt.next0_.chars.is_all_lower): 
                                (Utils.asObjectOrNull(res[0].referent, DecreePartReferent))._addName(MiscHelper.getTextValue(tt, res[0].begin_token.previous.previous, GetTextAttr.NO))
                                res[0].begin_token = tt
                                res[0].end_token = res[0].end_token.next0_
                            break
                        tt = tt.previous
        if (is_program): 
            for i in range(len(res) - 1, -1, -1):
                pa = Utils.asObjectOrNull(res[i].referent, DecreePartReferent)
                if (pa.subprogram is None): 
                    continue
                if (pa.owner is None or pa.name is None or pa.owner.kind != DecreeKind.PROGRAM): 
                    del res[i]
            else: i = -1
        if (is_add_agree): 
            for i in range(len(res) - 1, -1, -1):
                pa = Utils.asObjectOrNull(res[i].referent, DecreePartReferent)
                if (pa.addagree is None): 
                    continue
                if (pa.owner is None or pa.owner.kind != DecreeKind.CONTRACT): 
                    del res[i]
            else: i = -1
        res1 = list()
        i = 0
        while i < len(res): 
            li = list()
            j = i
            while j < len(res): 
                if (res[j].begin_token != res[i].begin_token): 
                    break
                else: 
                    li.append(Utils.asObjectOrNull(res[j].referent, DecreePartReferent))
                j += 1
            if (j < len(res)): 
                et = res[j].begin_token.previous
            else: 
                et = res[len(res) - 1].end_token
            while et.begin_char > res[i].begin_char:
                if (et.isChar(',') or et.morph.class0_.is_conjunction or et.is_hiphen): 
                    et = et.previous
                elif (MiscHelper.checkNumberPrefix(et) is not None): 
                    et = et.previous
                else: 
                    break
            res1.append(MetaToken._new836(res[i].begin_token, et, li))
            i = (j - 1)
            i += 1
        return res1