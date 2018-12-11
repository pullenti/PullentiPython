# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.Token import Token
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.weapon.internal.WeaponItemToken import WeaponItemToken
from pullenti.ner.Referent import Referent
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.internal.EpNerCoreInternalResourceHelper import EpNerCoreInternalResourceHelper
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.weapon.internal.MetaWeapon import MetaWeapon
from pullenti.ner.weapon.WeaponReferent import WeaponReferent
from pullenti.ner.Analyzer import Analyzer
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.geo.GeoReferent import GeoReferent

class WeaponAnalyzer(Analyzer):
    
    ANALYZER_NAME = "WEAPON"
    
    @property
    def name(self) -> str:
        return WeaponAnalyzer.ANALYZER_NAME
    
    @property
    def caption(self) -> str:
        return "Оружие"
    
    @property
    def description(self) -> str:
        return "Оружие (пистолеты, пулемёты)"
    
    def clone(self) -> 'Analyzer':
        return WeaponAnalyzer()
    
    @property
    def type_system(self) -> typing.List['ReferentClass']:
        return [MetaWeapon._global_meta]
    
    @property
    def images(self) -> typing.List[tuple]:
        res = dict()
        res[MetaWeapon.IMAGE_ID] = EpNerCoreInternalResourceHelper.getBytes("weapon.jpg")
        return res
    
    def createReferent(self, type0_ : str) -> 'Referent':
        if (type0_ == WeaponReferent.OBJ_TYPENAME): 
            return WeaponReferent()
        return None
    
    @property
    def used_extern_object_types(self) -> typing.List[str]:
        return [GeoReferent.OBJ_TYPENAME, "ORGANIZATION"]
    
    @property
    def progress_weight(self) -> int:
        return 5
    
    def process(self, kit : 'AnalysisKit') -> None:
        ad = kit.getAnalyzerData(self)
        models = TerminCollection()
        objs_by_model = dict()
        obj_by_names = TerminCollection()
        t = kit.first_token
        first_pass3170 = True
        while True:
            if first_pass3170: first_pass3170 = False
            else: t = t.next0_
            if (not (t is not None)): break
            its = WeaponItemToken.tryParseList(t, 10)
            if (its is None): 
                continue
            rts = self.__tryAttach(its, False)
            if (rts is not None): 
                for rt in rts: 
                    rt.referent = ad.registerReferent(rt.referent)
                    kit.embedToken(rt)
                    t = (rt)
                    for s in rt.referent.slots: 
                        if (s.type_name == WeaponReferent.ATTR_MODEL): 
                            mod = str(s.value)
                            for k in range(2):
                                if (not str.isdigit(mod[0])): 
                                    li = [ ]
                                    wrapli2650 = RefOutArgWrapper(None)
                                    inoutres2651 = Utils.tryGetValue(objs_by_model, mod, wrapli2650)
                                    li = wrapli2650.value
                                    if (not inoutres2651): 
                                        li = list()
                                        objs_by_model[mod] = li
                                    if (not rt.referent in li): 
                                        li.append(rt.referent)
                                    models.addStr(mod, li, None, False)
                                if (k > 0): 
                                    break
                                brand = rt.referent.getStringValue(WeaponReferent.ATTR_BRAND)
                                if (brand is None): 
                                    break
                                mod = "{0} {1}".format(brand, mod)
                        elif (s.type_name == WeaponReferent.ATTR_NAME): 
                            obj_by_names.add(Termin._new118(str(s.value), rt.referent))
        if (len(objs_by_model) == 0 and len(obj_by_names.termins) == 0): 
            return
        t = kit.first_token
        first_pass3171 = True
        while True:
            if first_pass3171: first_pass3171 = False
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
                tit = WeaponItemToken.tryParse(tok.begin_token.previous, None, False, True)
                if (tit is not None and tit.typ == WeaponItemToken.Typs.BRAND): 
                    tr.addSlot(WeaponReferent.ATTR_BRAND, tit.value, False, 0)
                    tok.begin_token = tit.begin_token
                rt0 = ReferentToken(tr, tok.begin_token, tok.end_token)
                kit.embedToken(rt0)
                t = (rt0)
                continue
    
    def _processReferent(self, begin : 'Token', end : 'Token') -> 'ReferentToken':
        its = WeaponItemToken.tryParseList(begin, 10)
        if (its is None): 
            return None
        rr = self.__tryAttach(its, True)
        if (rr is not None and len(rr) > 0): 
            return rr[0]
        return None
    
    def __tryAttach(self, its : typing.List['WeaponItemToken'], attach : bool) -> typing.List['ReferentToken']:
        tr = WeaponReferent()
        t1 = None
        noun = None
        brand = None
        model = None
        i = 0
        first_pass3172 = True
        while True:
            if first_pass3172: first_pass3172 = False
            else: i += 1
            if (not (i < len(its))): break
            if (its[i].typ == WeaponItemToken.Typs.NOUN): 
                if (len(its) == 1): 
                    return None
                if (tr.findSlot(WeaponReferent.ATTR_TYPE, None, True) is not None): 
                    if (tr.findSlot(WeaponReferent.ATTR_TYPE, its[i].value, True) is None): 
                        break
                if (not its[i].is_internal): 
                    noun = its[i]
                tr.addSlot(WeaponReferent.ATTR_TYPE, its[i].value, False, 0)
                if (its[i].alt_value is not None): 
                    tr.addSlot(WeaponReferent.ATTR_TYPE, its[i].alt_value, False, 0)
                t1 = its[i].end_token
                continue
            if (its[i].typ == WeaponItemToken.Typs.BRAND): 
                if (tr.findSlot(WeaponReferent.ATTR_BRAND, None, True) is not None): 
                    if (tr.findSlot(WeaponReferent.ATTR_BRAND, its[i].value, True) is None): 
                        break
                if (not its[i].is_internal): 
                    if (noun is not None and noun.is_doubt): 
                        noun.is_doubt = False
                brand = its[i]
                tr.addSlot(WeaponReferent.ATTR_BRAND, its[i].value, False, 0)
                t1 = its[i].end_token
                continue
            if (its[i].typ == WeaponItemToken.Typs.MODEL): 
                if (tr.findSlot(WeaponReferent.ATTR_MODEL, None, True) is not None): 
                    if (tr.findSlot(WeaponReferent.ATTR_MODEL, its[i].value, True) is None): 
                        break
                model = its[i]
                tr.addSlot(WeaponReferent.ATTR_MODEL, its[i].value, False, 0)
                if (its[i].alt_value is not None): 
                    tr.addSlot(WeaponReferent.ATTR_MODEL, its[i].alt_value, False, 0)
                t1 = its[i].end_token
                continue
            if (its[i].typ == WeaponItemToken.Typs.NAME): 
                if (tr.findSlot(WeaponReferent.ATTR_NAME, None, True) is not None): 
                    break
                tr.addSlot(WeaponReferent.ATTR_NAME, its[i].value, False, 0)
                if (its[i].alt_value is not None): 
                    tr.addSlot(WeaponReferent.ATTR_NAME, its[i].alt_value, False, 0)
                t1 = its[i].end_token
                continue
            if (its[i].typ == WeaponItemToken.Typs.NUMBER): 
                if (tr.findSlot(WeaponReferent.ATTR_NUMBER, None, True) is not None): 
                    break
                tr.addSlot(WeaponReferent.ATTR_NUMBER, its[i].value, False, 0)
                if (its[i].alt_value is not None): 
                    tr.addSlot(WeaponReferent.ATTR_NUMBER, its[i].alt_value, False, 0)
                t1 = its[i].end_token
                continue
            if (its[i].typ == WeaponItemToken.Typs.DATE): 
                if (tr.findSlot(WeaponReferent.ATTR_DATE, None, True) is not None): 
                    break
                tr.addSlot(WeaponReferent.ATTR_DATE, its[i].ref, True, 0)
                t1 = its[i].end_token
                continue
        has_good_noun = (False if noun is None else not noun.is_doubt)
        prev = None
        if (noun is None): 
            tt = its[0].begin_token.previous
            while tt is not None: 
                prev = Utils.asObjectOrNull(tt.getReferent(), WeaponReferent)
                if ((prev) is not None): 
                    add_slots = list()
                    for s in prev.slots: 
                        if (s.type_name == WeaponReferent.ATTR_TYPE): 
                            tr.addSlot(s.type_name, s.value, False, 0)
                        elif (s.type_name == WeaponReferent.ATTR_BRAND or s.type_name == WeaponReferent.ATTR_BRAND or s.type_name == WeaponReferent.ATTR_MODEL): 
                            if (tr.findSlot(s.type_name, None, True) is None): 
                                add_slots.append(s)
                    for s in add_slots: 
                        tr.addSlot(s.type_name, s.value, False, 0)
                    has_good_noun = True
                    break
                elif ((isinstance(tt, TextToken)) and ((not tt.chars.is_letter or tt.morph.class0_.is_conjunction))): 
                    pass
                else: 
                    break
                tt = tt.previous
        if (noun is None and model is not None): 
            cou = 0
            tt = its[0].begin_token.previous
            first_pass3173 = True
            while True:
                if first_pass3173: first_pass3173 = False
                else: tt = tt.previous; cou += 1
                if (not (tt is not None and (cou < 100))): break
                prev = Utils.asObjectOrNull(tt.getReferent(), WeaponReferent)
                if ((prev) is not None): 
                    if (prev.findSlot(WeaponReferent.ATTR_MODEL, model.value, True) is None): 
                        continue
                    add_slots = list()
                    for s in prev.slots: 
                        if (s.type_name == WeaponReferent.ATTR_TYPE): 
                            tr.addSlot(s.type_name, s.value, False, 0)
                        elif (s.type_name == WeaponReferent.ATTR_BRAND or s.type_name == WeaponReferent.ATTR_BRAND): 
                            if (tr.findSlot(s.type_name, None, True) is None): 
                                add_slots.append(s)
                    for s in add_slots: 
                        tr.addSlot(s.type_name, s.value, False, 0)
                    has_good_noun = True
                    break
        if (has_good_noun): 
            pass
        elif (noun is not None): 
            if (model is not None or ((brand is not None and not brand.is_doubt))): 
                pass
            else: 
                return None
        else: 
            if (model is None): 
                return None
            cou = 0
            ok = False
            tt = t1.previous
            while tt is not None and (cou < 20): 
                if ((tt.isValue("ОРУЖИЕ", None) or tt.isValue("ВООРУЖЕНИЕ", None) or tt.isValue("ВЫСТРЕЛ", None)) or tt.isValue("ВЫСТРЕЛИТЬ", None)): 
                    ok = True
                    break
                tt = tt.previous; cou += 1
            if (not ok): 
                return None
        res = list()
        res.append(ReferentToken(tr, its[0].begin_token, t1))
        return res
    
    __m_inited = None
    
    @staticmethod
    def initialize() -> None:
        if (WeaponAnalyzer.__m_inited): 
            return
        WeaponAnalyzer.__m_inited = True
        MetaWeapon.initialize()
        try: 
            Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = True
            WeaponItemToken.initialize()
            Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = False
        except Exception as ex: 
            raise Utils.newException(ex.__str__(), ex)
        ProcessorService.registerAnalyzer(WeaponAnalyzer())