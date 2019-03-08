# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.Token import Token
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.internal.EpNerCoreInternalResourceHelper import EpNerCoreInternalResourceHelper
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.transport.TransportKind import TransportKind
from pullenti.ner.transport.internal.MetaTransport import MetaTransport
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.Referent import Referent
from pullenti.ner.transport.internal.TransItemToken import TransItemToken
from pullenti.ner.transport.TransportReferent import TransportReferent
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.Analyzer import Analyzer

class TransportAnalyzer(Analyzer):
    """ Анализатор транспортных стредств """
    
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
        return [MetaTransport._global_meta]
    
    @property
    def images(self) -> typing.List[tuple]:
        res = dict()
        res[Utils.enumToString(TransportKind.FLY)] = EpNerCoreInternalResourceHelper.get_bytes("fly.png")
        res[Utils.enumToString(TransportKind.SHIP)] = EpNerCoreInternalResourceHelper.get_bytes("ship.png")
        res[Utils.enumToString(TransportKind.SPACE)] = EpNerCoreInternalResourceHelper.get_bytes("space.png")
        res[Utils.enumToString(TransportKind.TRAIN)] = EpNerCoreInternalResourceHelper.get_bytes("train.png")
        res[Utils.enumToString(TransportKind.AUTO)] = EpNerCoreInternalResourceHelper.get_bytes("auto.png")
        res[MetaTransport.IMAGE_ID] = EpNerCoreInternalResourceHelper.get_bytes("transport.png")
        return res
    
    def create_referent(self, type0_ : str) -> 'Referent':
        if (type0_ == TransportReferent.OBJ_TYPENAME): 
            return TransportReferent()
        return None
    
    @property
    def used_extern_object_types(self) -> typing.List[str]:
        return [GeoReferent.OBJ_TYPENAME, "ORGANIZATION"]
    
    @property
    def progress_weight(self) -> int:
        return 5
    
    def process(self, kit : 'AnalysisKit') -> None:
        ad = kit.get_analyzer_data(self)
        models = TerminCollection()
        objs_by_model = dict()
        obj_by_names = TerminCollection()
        t = kit.first_token
        first_pass3250 = True
        while True:
            if first_pass3250: first_pass3250 = False
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
                    first_pass3251 = True
                    while True:
                        if first_pass3251: first_pass3251 = False
                        else: tt = tt.previous; cou += 1
                        if (not (tt is not None and (cou < 1000))): break
                        tr = Utils.asObjectOrNull(tt.get_referent(), TransportReferent)
                        if (tr is None): 
                            continue
                        ok = True
                        for s in rt.referent.slots: 
                            if (tr.find_slot(s.type_name, s.value, True) is None): 
                                ok = False
                                break
                        if (ok): 
                            rt.referent = (tr)
                            break
                    rt.referent = ad.register_referent(rt.referent)
                    kit.embed_token(rt)
                    t = (rt)
                    for s in rt.referent.slots: 
                        if (s.type_name == TransportReferent.ATTR_MODEL): 
                            mod = str(s.value)
                            for k in range(2):
                                if (not str.isdigit(mod[0])): 
                                    li = [ ]
                                    wrapli2643 = RefOutArgWrapper(None)
                                    inoutres2644 = Utils.tryGetValue(objs_by_model, mod, wrapli2643)
                                    li = wrapli2643.value
                                    if (not inoutres2644): 
                                        li = list()
                                        objs_by_model[mod] = li
                                    if (not rt.referent in li): 
                                        li.append(rt.referent)
                                    models.add_str(mod, li, None, False)
                                if (k > 0): 
                                    break
                                brand = rt.referent.get_string_value(TransportReferent.ATTR_BRAND)
                                if (brand is None): 
                                    break
                                mod = "{0} {1}".format(brand, mod)
                        elif (s.type_name == TransportReferent.ATTR_NAME): 
                            obj_by_names.add(Termin._new119(str(s.value), rt.referent))
        if (len(objs_by_model) == 0 and len(obj_by_names.termins) == 0): 
            return
        t = kit.first_token
        first_pass3252 = True
        while True:
            if first_pass3252: first_pass3252 = False
            else: t = t.next0_
            if (not (t is not None)): break
            br = BracketHelper.try_parse(t, BracketParseAttr.NO, 10)
            if (br is not None): 
                toks = obj_by_names.try_parse(t.next0_, TerminParseAttr.NO)
                if (toks is not None and toks.end_token.next0_ == br.end_token): 
                    rt0 = ReferentToken(Utils.asObjectOrNull(toks.termin.tag, Referent), br.begin_token, br.end_token)
                    kit.embed_token(rt0)
                    t = (rt0)
                    continue
            if (not ((isinstance(t, TextToken)))): 
                continue
            if (not t.chars.is_letter0): 
                continue
            tok = models.try_parse(t, TerminParseAttr.NO)
            if (tok is None): 
                if (not t.chars.is_all_lower0): 
                    tok = obj_by_names.try_parse(t, TerminParseAttr.NO)
                if (tok is None): 
                    continue
            if (not tok.is_whitespace_after): 
                if (tok.end_token.next0_ is None or not tok.end_token.next0_.is_char_of(",.)")): 
                    if (not BracketHelper.is_bracket(tok.end_token.next0_, False)): 
                        continue
            tr = None
            li = Utils.asObjectOrNull(tok.termin.tag, list)
            if (li is not None and len(li) == 1): 
                tr = li[0]
            else: 
                tr = (Utils.asObjectOrNull(tok.termin.tag, Referent))
            if (tr is not None): 
                tit = TransItemToken.try_parse(tok.begin_token.previous, None, False, True)
                if (tit is not None and tit.typ == TransItemToken.Typs.BRAND): 
                    tr.add_slot(TransportReferent.ATTR_BRAND, tit.value, False, 0)
                    tok.begin_token = tit.begin_token
                rt0 = ReferentToken(tr, tok.begin_token, tok.end_token)
                kit.embed_token(rt0)
                t = (rt0)
                continue
    
    def _process_referent(self, begin : 'Token', end : 'Token') -> 'ReferentToken':
        its = TransItemToken.try_parse_list(begin, 10)
        if (its is None): 
            return None
        rr = self.__try_attach(its, True)
        if (rr is not None and len(rr) > 0): 
            return rr[0]
        return None
    
    def __try_attach(self, its : typing.List['TransItemToken'], attach : bool) -> typing.List['ReferentToken']:
        tr = TransportReferent()
        t1 = None
        brand_is_doubt = False
        i = 0
        first_pass3253 = True
        while True:
            if first_pass3253: first_pass3253 = False
            else: i += 1
            if (not (i < len(its))): break
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
            if (its[i].typ == TransItemToken.Typs.GEO): 
                if (its[i].state is not None): 
                    tr._add_geo(its[i].state)
                elif (its[i].ref is not None): 
                    tr._add_geo(its[i].ref)
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
                brand_is_doubt = its[i].is_doubt
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
                if (not its[i].morph.case_.is_undefined0 and not its[i].morph.case_.is_genitive0): 
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
        if (not tr._check(attach, brand_is_doubt)): 
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
        elif (i == len(its) and its[len(its) - 1].typ == TransItemToken.Typs.NUMBER): 
            tt = t1.next0_
            while tt is not None: 
                if (not tt.is_comma_and0): 
                    break
                nn = TransItemToken._attach_rus_auto_number(tt.next0_)
                if (nn is None): 
                    nn = TransItemToken._attach_number(tt.next0_, False)
                if (nn is None or nn.typ != TransItemToken.Typs.NUMBER): 
                    break
                tr1 = TransportReferent()
                for s in tr.slots: 
                    if (s.type_name != TransportReferent.ATTR_NUMBER): 
                        tr1.add_slot(s.type_name, s.value, False, 0)
                tr1.add_slot(TransportReferent.ATTR_NUMBER, nn.value, True, 0)
                res.append(ReferentToken(tr1, nn.begin_token, nn.end_token))
                tt = nn.end_token
                tt = tt.next0_
        return res
    
    __m_inited = None
    
    @staticmethod
    def initialize() -> None:
        if (TransportAnalyzer.__m_inited): 
            return
        TransportAnalyzer.__m_inited = True
        MetaTransport.initialize()
        try: 
            Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = True
            TransItemToken.initialize()
            Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = False
        except Exception as ex: 
            raise Utils.newException(ex.__str__(), ex)
        ProcessorService.register_analyzer(TransportAnalyzer())