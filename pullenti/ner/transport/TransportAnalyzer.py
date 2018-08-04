# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import typing
from pullenti.ntopy.Utils import Utils
from pullenti.ntopy.Misc import RefOutArgWrapper
from pullenti.ner.Analyzer import Analyzer
from pullenti.ner.transport.TransportKind import TransportKind
from pullenti.ner.business.internal.ResourceHelper import ResourceHelper
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
        res[Utils.enumToString(TransportKind.FLY)] = ResourceHelper.get_bytes("fly.png")
        res[Utils.enumToString(TransportKind.SHIP)] = ResourceHelper.get_bytes("ship.png")
        res[Utils.enumToString(TransportKind.SPACE)] = ResourceHelper.get_bytes("space.png")
        res[Utils.enumToString(TransportKind.TRAIN)] = ResourceHelper.get_bytes("train.png")
        res[Utils.enumToString(TransportKind.AUTO)] = ResourceHelper.get_bytes("auto.png")
        res[MetaTransport.IMAGE_ID] = ResourceHelper.get_bytes("transport.png")
        return res
    
    def create_referent(self, type0_ : str) -> 'Referent':
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
        ad = kit.get_analyzer_data(self)
        models = TerminCollection()
        objs_by_model = dict()
        obj_by_names = TerminCollection()
        t = kit.first_token
        first_pass3063 = True
        while True:
            if first_pass3063: first_pass3063 = False
            else: t = t.next0_
            if (not (t is not None)): break
            its = TransItemToken.try_parse_list(t, 10)
            if (its is None): 
                continue
            rts = self.__try_attach(its, False)
            if (rts is not None): 
                for rt in rts: 
                    cou = 0
                    tt = t.previous
                    first_pass3064 = True
                    while True:
                        if first_pass3064: first_pass3064 = False
                        else: tt = tt.previous; cou += 1
                        if (not (tt is not None and (cou < 1000))): break
                        tr = (tt.get_referent() if isinstance(tt.get_referent(), TransportReferent) else None)
                        if (tr is None): 
                            continue
                        ok = True
                        for s in rt.referent.slots: 
                            if (tr.find_slot(s.type_name, s.value, True) is None): 
                                ok = False
                                break
                        if (ok): 
                            rt.referent = tr
                            break
                    rt.referent = ad.register_referent(rt.referent)
                    kit.embed_token(rt)
                    t = rt
                    for s in rt.referent.slots: 
                        if (s.type_name == TransportReferent.ATTR_MODEL): 
                            mod = str(s.value)
                            for k in range(2):
                                if (not mod[0].isdigit()): 
                                    li = [ ]
                                    inoutarg2515 = RefOutArgWrapper(None)
                                    inoutres2516 = Utils.tryGetValue(objs_by_model, mod, inoutarg2515)
                                    li = inoutarg2515.value
                                    if (not inoutres2516): 
                                        li = list()
                                        objs_by_model[mod] = li
                                    if (not rt.referent in li): 
                                        li.append(rt.referent)
                                    models.add_str(mod, li, MorphLang(), False)
                                if (k > 0): 
                                    break
                                brand = rt.referent.get_string_value(TransportReferent.ATTR_BRAND)
                                if (brand is None): 
                                    break
                                mod = "{0} {1}".format(brand, mod)
                        elif (s.type_name == TransportReferent.ATTR_NAME): 
                            obj_by_names.add(Termin._new118(str(s.value), rt.referent))
        if (len(objs_by_model) == 0 and len(obj_by_names.termins) == 0): 
            return
        t = kit.first_token
        first_pass3065 = True
        while True:
            if first_pass3065: first_pass3065 = False
            else: t = t.next0_
            if (not (t is not None)): break
            br = BracketHelper.try_parse(t, BracketParseAttr.NO, 10)
            if (br is not None): 
                toks = obj_by_names.try_parse(t.next0_, TerminParseAttr.NO)
                if (toks is not None and toks.end_token.next0_ == br.end_token): 
                    rt0 = ReferentToken(toks.termin.tag if isinstance(toks.termin.tag, Referent) else None, br.begin_token, br.end_token)
                    kit.embed_token(rt0)
                    t = rt0
                    continue
            if (not ((isinstance(t, TextToken)))): 
                continue
            if (not t.chars.is_letter): 
                continue
            tok = models.try_parse(t, TerminParseAttr.NO)
            if (tok is None): 
                if (not t.chars.is_all_lower): 
                    tok = obj_by_names.try_parse(t, TerminParseAttr.NO)
                if (tok is None): 
                    continue
            if (not tok.is_whitespace_after): 
                if (tok.end_token.next0_ is None or not tok.end_token.next0_.is_char_of(",.)")): 
                    if (not BracketHelper.is_bracket(tok.end_token.next0_, False)): 
                        continue
            tr = None
            li = (tok.termin.tag if isinstance(tok.termin.tag, list) else None)
            if (li is not None and len(li) == 1): 
                tr = li[0]
            else: 
                tr = (tok.termin.tag if isinstance(tok.termin.tag, Referent) else None)
            if (tr is not None): 
                tit = TransItemToken.try_parse(tok.begin_token.previous, None, False, True)
                if (tit is not None and tit.typ == TransItemToken.Typs.BRAND): 
                    tr.add_slot(TransportReferent.ATTR_BRAND, tit.value, False, 0)
                    tok.begin_token = tit.begin_token
                rt0 = ReferentToken(tr, tok.begin_token, tok.end_token)
                kit.embed_token(rt0)
                t = rt0
                continue
    
    def _process_referent(self, begin : 'Token', end : 'Token') -> 'ReferentToken':
        from pullenti.ner.transport.internal.TransItemToken import TransItemToken
        its = TransItemToken.try_parse_list(begin, 10)
        if (its is None): 
            return None
        rr = self.__try_attach(its, True)
        if (rr is not None and len(rr) > 0): 
            return rr[0]
        return None
    
    def __try_attach(self, its : typing.List['TransItemToken'], attach : bool) -> typing.List['ReferentToken']:
        from pullenti.ner.transport.TransportReferent import TransportReferent
        from pullenti.ner.transport.internal.TransItemToken import TransItemToken
        from pullenti.ner.ReferentToken import ReferentToken
        tr = TransportReferent()
        t1 = None
        for i in range(len(its)):
            if (its[i].typ == TransItemToken.Typs.NOUN): 
                if (tr.find_slot(TransportReferent.ATTR_TYPE, None, True) is not None): 
                    break
                if (its[i].kind != TransportKind.UNDEFINED): 
                    if (tr.kind != TransportKind.UNDEFINED and its[i].kind != tr.kind): 
                        break
                    else: 
                        tr.kind = its[i].kind
                tr.add_slot(TransportReferent.ATTR_TYPE, its[i].value, False, 0)
                if (its[i].alt_value is not None): 
                    tr.add_slot(TransportReferent.ATTR_TYPE, its[i].alt_value, False, 0)
                if (its[i].state is not None): 
                    tr._add_geo(its[i].state)
                t1 = its[i].end_token
                continue
            if (its[i].typ == TransItemToken.Typs.BRAND): 
                if (tr.find_slot(TransportReferent.ATTR_BRAND, None, True) is not None): 
                    if (tr.find_slot(TransportReferent.ATTR_BRAND, its[i].value, True) is None): 
                        break
                if (its[i].kind != TransportKind.UNDEFINED): 
                    if (tr.kind != TransportKind.UNDEFINED and its[i].kind != tr.kind): 
                        break
                    else: 
                        tr.kind = its[i].kind
                tr.add_slot(TransportReferent.ATTR_BRAND, its[i].value, False, 0)
                t1 = its[i].end_token
                continue
            if (its[i].typ == TransItemToken.Typs.MODEL): 
                if (tr.find_slot(TransportReferent.ATTR_MODEL, None, True) is not None): 
                    break
                tr.add_slot(TransportReferent.ATTR_MODEL, its[i].value, False, 0)
                if (its[i].alt_value is not None): 
                    tr.add_slot(TransportReferent.ATTR_MODEL, its[i].alt_value, False, 0)
                t1 = its[i].end_token
                continue
            if (its[i].typ == TransItemToken.Typs.CLASS): 
                if (tr.find_slot(TransportReferent.ATTR_CLASS, None, True) is not None): 
                    break
                tr.add_slot(TransportReferent.ATTR_CLASS, its[i].value, False, 0)
                t1 = its[i].end_token
                continue
            if (its[i].typ == TransItemToken.Typs.NAME): 
                if (tr.find_slot(TransportReferent.ATTR_NAME, None, True) is not None): 
                    break
                tr.add_slot(TransportReferent.ATTR_NAME, its[i].value, False, 0)
                if (its[i].alt_value is not None): 
                    tr.add_slot(TransportReferent.ATTR_NAME, its[i].alt_value, False, 0)
                t1 = its[i].end_token
                continue
            if (its[i].typ == TransItemToken.Typs.NUMBER): 
                if (tr.find_slot(TransportReferent.ATTR_NUMBER, None, True) is not None): 
                    break
                if (its[i].kind != TransportKind.UNDEFINED): 
                    if (tr.kind != TransportKind.UNDEFINED and its[i].kind != tr.kind): 
                        break
                    else: 
                        tr.kind = its[i].kind
                tr.add_slot(TransportReferent.ATTR_NUMBER, its[i].value, False, 0)
                if (its[i].alt_value is not None): 
                    tr.add_slot(TransportReferent.ATTR_NUMBER_REGION, its[i].alt_value, False, 0)
                t1 = its[i].end_token
                continue
            if (its[i].typ == TransItemToken.Typs.ORG): 
                if (tr.find_slot(TransportReferent.ATTR_ORG, None, True) is not None): 
                    break
                if (not its[i].morph.case.is_undefined and not its[i].morph.case.is_genitive): 
                    break
                tr.add_slot(TransportReferent.ATTR_ORG, its[i].ref, True, 0)
                t1 = its[i].end_token
                continue
            if (its[i].typ == TransItemToken.Typs.DATE): 
                if (tr.find_slot(TransportReferent.ATTR_DATE, None, True) is not None): 
                    break
                tr.add_slot(TransportReferent.ATTR_DATE, its[i].ref, True, 0)
                t1 = its[i].end_token
                continue
            if (its[i].typ == TransItemToken.Typs.ROUTE): 
                if (tr.find_slot(TransportReferent.ATTR_ROUTEPOINT, None, True) is not None): 
                    break
                for o in its[i].route_items: 
                    tr.add_slot(TransportReferent.ATTR_ROUTEPOINT, o, False, 0)
                t1 = its[i].end_token
                continue
        else: i = len(its)
        if (not tr._check(attach)): 
            return None
        res = list()
        res.append(ReferentToken(tr, its[0].begin_token, t1))
        if ((i < len(its)) and tr.kind == TransportKind.SHIP and its[i - 1].typ == TransItemToken.Typs.NAME): 
            while i < len(its): 
                if (its[i].typ != TransItemToken.Typs.NAME or not its[i].is_after_conjunction): 
                    break
                tr1 = TransportReferent()
                tr1.merge_slots(tr, True)
                tr1.add_slot(TransportReferent.ATTR_NAME, its[i].value, True, 0)
                res.append(ReferentToken(tr1, its[i].begin_token, its[i].end_token))
                i += 1
        return res
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.transport.internal.TransItemToken import TransItemToken
        from pullenti.ner.ProcessorService import ProcessorService
        try: 
            TransItemToken.initialize()
        except Exception as ex: 
            raise Utils.newException(ex.__str__(), ex)
        ProcessorService.register_analyzer(TransportAnalyzer())