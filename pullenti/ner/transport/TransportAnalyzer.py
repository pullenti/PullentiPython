# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.ner.Analyzer import Analyzer
from pullenti.ner.transport.TransportKind import TransportKind
from pullenti.ner.core.internal.EpNerCoreInternalResourceHelper import EpNerCoreInternalResourceHelper
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.core.TerminParseAttr import TerminParseAttr


class TransportAnalyzer(Analyzer):
    
    ANALYZER_NAME = "TRANSPORT"
    
    @property
    def name(self) -> str:
        return TransportAnalyzer.ANALYZER_NAME
    
    @property
    def caption(self) -> str:
        return "Транспорт"
    
    @property
    def description(self) -> str:
        return "Техника, автомобили, самолёты, корабли..."
    
    def clone(self) -> 'Analyzer':
        return TransportAnalyzer()
    
    @property
    def type_system(self) -> typing.List['ReferentClass']:
        from pullenti.ner.transport.internal.MetaTransport import MetaTransport
        return [MetaTransport._global_meta]
    
    @property
    def images(self) -> typing.List[tuple]:
        from pullenti.ner.transport.internal.MetaTransport import MetaTransport
        res = dict()
        res[Utils.enumToString(TransportKind.FLY)] = EpNerCoreInternalResourceHelper.getBytes("fly.png")
        res[Utils.enumToString(TransportKind.SHIP)] = EpNerCoreInternalResourceHelper.getBytes("ship.png")
        res[Utils.enumToString(TransportKind.SPACE)] = EpNerCoreInternalResourceHelper.getBytes("space.png")
        res[Utils.enumToString(TransportKind.TRAIN)] = EpNerCoreInternalResourceHelper.getBytes("train.png")
        res[Utils.enumToString(TransportKind.AUTO)] = EpNerCoreInternalResourceHelper.getBytes("auto.png")
        res[MetaTransport.IMAGE_ID] = EpNerCoreInternalResourceHelper.getBytes("transport.png")
        return res
    
    def createReferent(self, type0_ : str) -> 'Referent':
        from pullenti.ner.transport.TransportReferent import TransportReferent
        if (type0_ == TransportReferent.OBJ_TYPENAME): 
            return TransportReferent()
        return None
    
    @property
    def used_extern_object_types(self) -> typing.List[str]:
        from pullenti.ner.geo.GeoReferent import GeoReferent
        return [GeoReferent.OBJ_TYPENAME, "ORGANIZATION"]
    
    @property
    def progress_weight(self) -> int:
        return 5
    
    def process(self, kit : 'AnalysisKit') -> None:
        from pullenti.ner.core.TerminCollection import TerminCollection
        from pullenti.ner.transport.internal.TransItemToken import TransItemToken
        from pullenti.ner.Referent import Referent
        from pullenti.ner.transport.TransportReferent import TransportReferent
        from pullenti.morph.MorphLang import MorphLang
        from pullenti.ner.core.Termin import Termin
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.TextToken import TextToken
        ad = kit.getAnalyzerData(self)
        models = TerminCollection()
        objs_by_model = dict()
        obj_by_names = TerminCollection()
        t = kit.first_token
        first_pass3148 = True
        while True:
            if first_pass3148: first_pass3148 = False
            else: t = t.next0_
            if (not (t is not None)): break
            its = TransItemToken.tryParseList(t, 10)
            if (its is None): 
                continue
            rts = self.__tryAttach(its, False)
            if (rts is not None): 
                for rt in rts: 
                    cou = 0
                    tt = t.previous
                    first_pass3149 = True
                    while True:
                        if first_pass3149: first_pass3149 = False
                        else: tt = tt.previous; cou += 1
                        if (not (tt is not None and (cou < 1000))): break
                        tr = Utils.asObjectOrNull(tt.getReferent(), TransportReferent)
                        if (tr is None): 
                            continue
                        ok = True
                        for s in rt.referent.slots: 
                            if (tr.findSlot(s.type_name, s.value, True) is None): 
                                ok = False
                                break
                        if (ok): 
                            rt.referent = (tr)
                            break
                    rt.referent = ad.registerReferent(rt.referent)
                    kit.embedToken(rt)
                    t = (rt)
                    for s in rt.referent.slots: 
                        if (s.type_name == TransportReferent.ATTR_MODEL): 
                            mod = str(s.value)
                            for k in range(2):
                                if (not str.isdigit(mod[0])): 
                                    li = [ ]
                                    wrapli2558 = RefOutArgWrapper(None)
                                    inoutres2559 = Utils.tryGetValue(objs_by_model, mod, wrapli2558)
                                    li = wrapli2558.value
                                    if (not inoutres2559): 
                                        li = list()
                                        objs_by_model[mod] = li
                                    if (not rt.referent in li): 
                                        li.append(rt.referent)
                                    models.addStr(mod, li, MorphLang(), False)
                                if (k > 0): 
                                    break
                                brand = rt.referent.getStringValue(TransportReferent.ATTR_BRAND)
                                if (brand is None): 
                                    break
                                mod = "{0} {1}".format(brand, mod)
                        elif (s.type_name == TransportReferent.ATTR_NAME): 
                            obj_by_names.add(Termin._new118(str(s.value), rt.referent))
        if (len(objs_by_model) == 0 and len(obj_by_names.termins) == 0): 
            return
        t = kit.first_token
        first_pass3150 = True
        while True:
            if first_pass3150: first_pass3150 = False
            else: t = t.next0_
            if (not (t is not None)): break
            br = BracketHelper.tryParse(t, BracketParseAttr.NO, 10)
            if (br is not None): 
                toks = obj_by_names.tryParse(t.next0_, TerminParseAttr.NO)
                if (toks is not None and toks.end_token.next0_ == br.end_token): 
                    rt0 = ReferentToken(Utils.asObjectOrNull(toks.termin.tag, Referent), br.begin_token, br.end_token)
                    kit.embedToken(rt0)
                    t = (rt0)
                    continue
            if (not ((isinstance(t, TextToken)))): 
                continue
            if (not t.chars.is_letter): 
                continue
            tok = models.tryParse(t, TerminParseAttr.NO)
            if (tok is None): 
                if (not t.chars.is_all_lower): 
                    tok = obj_by_names.tryParse(t, TerminParseAttr.NO)
                if (tok is None): 
                    continue
            if (not tok.is_whitespace_after): 
                if (tok.end_token.next0_ is None or not tok.end_token.next0_.isCharOf(",.)")): 
                    if (not BracketHelper.isBracket(tok.end_token.next0_, False)): 
                        continue
            tr = None
            li = Utils.asObjectOrNull(tok.termin.tag, list)
            if (li is not None and len(li) == 1): 
                tr = li[0]
            else: 
                tr = (Utils.asObjectOrNull(tok.termin.tag, Referent))
            if (tr is not None): 
                tit = TransItemToken.tryParse(tok.begin_token.previous, None, False, True)
                if (tit is not None and tit.typ == TransItemToken.Typs.BRAND): 
                    tr.addSlot(TransportReferent.ATTR_BRAND, tit.value, False, 0)
                    tok.begin_token = tit.begin_token
                rt0 = ReferentToken(tr, tok.begin_token, tok.end_token)
                kit.embedToken(rt0)
                t = (rt0)
                continue
    
    def _processReferent(self, begin : 'Token', end : 'Token') -> 'ReferentToken':
        from pullenti.ner.transport.internal.TransItemToken import TransItemToken
        its = TransItemToken.tryParseList(begin, 10)
        if (its is None): 
            return None
        rr = self.__tryAttach(its, True)
        if (rr is not None and len(rr) > 0): 
            return rr[0]
        return None
    
    def __tryAttach(self, its : typing.List['TransItemToken'], attach : bool) -> typing.List['ReferentToken']:
        from pullenti.ner.transport.TransportReferent import TransportReferent
        from pullenti.ner.transport.internal.TransItemToken import TransItemToken
        from pullenti.ner.ReferentToken import ReferentToken
        tr = TransportReferent()
        t1 = None
        i = 0
        first_pass3151 = True
        while True:
            if first_pass3151: first_pass3151 = False
            else: i += 1
            if (not (i < len(its))): break
            if (its[i].typ == TransItemToken.Typs.NOUN): 
                if (tr.findSlot(TransportReferent.ATTR_TYPE, None, True) is not None): 
                    break
                if (its[i].kind != TransportKind.UNDEFINED): 
                    if (tr.kind != TransportKind.UNDEFINED and its[i].kind != tr.kind): 
                        break
                    else: 
                        tr.kind = its[i].kind
                tr.addSlot(TransportReferent.ATTR_TYPE, its[i].value, False, 0)
                if (its[i].alt_value is not None): 
                    tr.addSlot(TransportReferent.ATTR_TYPE, its[i].alt_value, False, 0)
                if (its[i].state is not None): 
                    tr._addGeo(its[i].state)
                t1 = its[i].end_token
                continue
            if (its[i].typ == TransItemToken.Typs.BRAND): 
                if (tr.findSlot(TransportReferent.ATTR_BRAND, None, True) is not None): 
                    if (tr.findSlot(TransportReferent.ATTR_BRAND, its[i].value, True) is None): 
                        break
                if (its[i].kind != TransportKind.UNDEFINED): 
                    if (tr.kind != TransportKind.UNDEFINED and its[i].kind != tr.kind): 
                        break
                    else: 
                        tr.kind = its[i].kind
                tr.addSlot(TransportReferent.ATTR_BRAND, its[i].value, False, 0)
                t1 = its[i].end_token
                continue
            if (its[i].typ == TransItemToken.Typs.MODEL): 
                if (tr.findSlot(TransportReferent.ATTR_MODEL, None, True) is not None): 
                    break
                tr.addSlot(TransportReferent.ATTR_MODEL, its[i].value, False, 0)
                if (its[i].alt_value is not None): 
                    tr.addSlot(TransportReferent.ATTR_MODEL, its[i].alt_value, False, 0)
                t1 = its[i].end_token
                continue
            if (its[i].typ == TransItemToken.Typs.CLASS): 
                if (tr.findSlot(TransportReferent.ATTR_CLASS, None, True) is not None): 
                    break
                tr.addSlot(TransportReferent.ATTR_CLASS, its[i].value, False, 0)
                t1 = its[i].end_token
                continue
            if (its[i].typ == TransItemToken.Typs.NAME): 
                if (tr.findSlot(TransportReferent.ATTR_NAME, None, True) is not None): 
                    break
                tr.addSlot(TransportReferent.ATTR_NAME, its[i].value, False, 0)
                if (its[i].alt_value is not None): 
                    tr.addSlot(TransportReferent.ATTR_NAME, its[i].alt_value, False, 0)
                t1 = its[i].end_token
                continue
            if (its[i].typ == TransItemToken.Typs.NUMBER): 
                if (tr.findSlot(TransportReferent.ATTR_NUMBER, None, True) is not None): 
                    break
                if (its[i].kind != TransportKind.UNDEFINED): 
                    if (tr.kind != TransportKind.UNDEFINED and its[i].kind != tr.kind): 
                        break
                    else: 
                        tr.kind = its[i].kind
                tr.addSlot(TransportReferent.ATTR_NUMBER, its[i].value, False, 0)
                if (its[i].alt_value is not None): 
                    tr.addSlot(TransportReferent.ATTR_NUMBER_REGION, its[i].alt_value, False, 0)
                t1 = its[i].end_token
                continue
            if (its[i].typ == TransItemToken.Typs.ORG): 
                if (tr.findSlot(TransportReferent.ATTR_ORG, None, True) is not None): 
                    break
                if (not its[i].morph.case_.is_undefined and not its[i].morph.case_.is_genitive): 
                    break
                tr.addSlot(TransportReferent.ATTR_ORG, its[i].ref, True, 0)
                t1 = its[i].end_token
                continue
            if (its[i].typ == TransItemToken.Typs.DATE): 
                if (tr.findSlot(TransportReferent.ATTR_DATE, None, True) is not None): 
                    break
                tr.addSlot(TransportReferent.ATTR_DATE, its[i].ref, True, 0)
                t1 = its[i].end_token
                continue
            if (its[i].typ == TransItemToken.Typs.ROUTE): 
                if (tr.findSlot(TransportReferent.ATTR_ROUTEPOINT, None, True) is not None): 
                    break
                for o in its[i].route_items: 
                    tr.addSlot(TransportReferent.ATTR_ROUTEPOINT, o, False, 0)
                t1 = its[i].end_token
                continue
        if (not tr._check(attach)): 
            return None
        res = list()
        res.append(ReferentToken(tr, its[0].begin_token, t1))
        if ((i < len(its)) and tr.kind == TransportKind.SHIP and its[i - 1].typ == TransItemToken.Typs.NAME): 
            while i < len(its): 
                if (its[i].typ != TransItemToken.Typs.NAME or not its[i].is_after_conjunction): 
                    break
                tr1 = TransportReferent()
                tr1.mergeSlots(tr, True)
                tr1.addSlot(TransportReferent.ATTR_NAME, its[i].value, True, 0)
                res.append(ReferentToken(tr1, its[i].begin_token, its[i].end_token))
                i += 1
        return res
    
    __m_inited = None
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.core.Termin import Termin
        from pullenti.ner.transport.internal.TransItemToken import TransItemToken
        from pullenti.ner.ProcessorService import ProcessorService
        if (TransportAnalyzer.__m_inited): 
            return
        TransportAnalyzer.__m_inited = True
        try: 
            Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = True
            TransItemToken.initialize()
            Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = False
        except Exception as ex: 
            raise Utils.newException(ex.__str__(), ex)
        ProcessorService.registerAnalyzer(TransportAnalyzer())