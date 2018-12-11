# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import typing
from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.address.internal.StreetItemType import StreetItemType
from pullenti.ner.address.AddressAnalyzer import AddressAnalyzer
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.address.internal.MetaStreet import MetaStreet
from pullenti.ner.TextToken import TextToken
from pullenti.ner.geo.internal.GeoOwnerHelper import GeoOwnerHelper
from pullenti.ner.address.internal.MetaAddress import MetaAddress
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.core.IntOntologyItem import IntOntologyItem
from pullenti.ner.core.AnalyzerData import AnalyzerData
from pullenti.ner.Token import Token
from pullenti.ner.core.internal.EpNerCoreInternalResourceHelper import EpNerCoreInternalResourceHelper
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.AnalyzerDataWithOntology import AnalyzerDataWithOntology
from pullenti.ner.geo.internal.MetaGeo import MetaGeo
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.Referent import Referent
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.Analyzer import Analyzer
from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken
from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.address.internal.AddressItemToken import AddressItemToken
from pullenti.ner.address.internal.StreetItemToken import StreetItemToken
from pullenti.ner.geo.internal.CityItemToken import CityItemToken
from pullenti.ner.geo.internal.CityAttachHelper import CityAttachHelper
from pullenti.ner.geo.internal.TerrAttachHelper import TerrAttachHelper

class GeoAnalyzer(Analyzer):
    """ Семантический анализатор стран """
    
    class GeoAnalyzerDataWithOntology(AnalyzerDataWithOntology):
        
        __ends = None
        
        def registerReferent(self, referent : 'Referent') -> 'Referent':
            from pullenti.ner.geo.GeoReferent import GeoReferent
            from pullenti.morph.MorphGender import MorphGender
            from pullenti.ner.Referent import Referent
            from pullenti.morph.LanguageHelper import LanguageHelper
            g = Utils.asObjectOrNull(referent, GeoReferent)
            if (g is not None): 
                if (g.is_state): 
                    pass
                elif (g.is_region or ((g.is_city and not g.is_big_city))): 
                    names = list()
                    gen = MorphGender.UNDEFINED
                    bas_nam = None
                    for s in g.slots: 
                        if (s.type_name == GeoReferent.ATTR_NAME): 
                            names.append(Utils.asObjectOrNull(s.value, str))
                        elif (s.type_name == GeoReferent.ATTR_TYPE): 
                            typ = Utils.asObjectOrNull(s.value, str)
                            if (LanguageHelper.endsWithEx(typ, "район", "край", "округ", "улус")): 
                                gen = (Utils.valToEnum((gen) | (MorphGender.MASCULINE), MorphGender))
                            elif (LanguageHelper.endsWithEx(typ, "область", "территория", None, None)): 
                                gen = (Utils.valToEnum((gen) | (MorphGender.FEMINIE), MorphGender))
                    i = 0
                    first_pass2915 = True
                    while True:
                        if first_pass2915: first_pass2915 = False
                        else: i += 1
                        if (not (i < len(names))): break
                        n = names[i]
                        ii = n.find(' ')
                        if (ii > 0): 
                            if (isinstance(g.getSlotValue(GeoReferent.ATTR_REF), Referent)): 
                                continue
                            nn = "{0} {1}".format(n[ii + 1:], n[0:0+ii])
                            if (not nn in names): 
                                names.append(nn)
                                g.addSlot(GeoReferent.ATTR_NAME, nn, False, 0)
                                continue
                            continue
                        for end in GeoAnalyzer.GeoAnalyzerDataWithOntology.__ends: 
                            if (LanguageHelper.endsWith(n, end)): 
                                nn = n[0:0+len(n) - 3]
                                for end2 in GeoAnalyzer.GeoAnalyzerDataWithOntology.__ends: 
                                    if (end2 != end): 
                                        if (not nn + end2 in names): 
                                            names.append(nn + end2)
                                            g.addSlot(GeoReferent.ATTR_NAME, nn + end2, False, 0)
                                if (gen == MorphGender.MASCULINE): 
                                    for na in names: 
                                        if (LanguageHelper.endsWith(na, "ИЙ")): 
                                            bas_nam = na
                                elif (gen == MorphGender.FEMINIE): 
                                    for na in names: 
                                        if (LanguageHelper.endsWith(na, "АЯ")): 
                                            bas_nam = na
                                elif (gen == MorphGender.NEUTER): 
                                    for na in names: 
                                        if (LanguageHelper.endsWith(na, "ОЕ")): 
                                            bas_nam = na
                                break
                    if (bas_nam is not None and len(names) > 0 and names[0] != bas_nam): 
                        sl = g.findSlot(GeoReferent.ATTR_NAME, bas_nam, True)
                        if (sl is not None): 
                            g.slots.remove(sl)
                            g.slots.insert(0, sl)
            return super().registerReferent(referent)
        
        # static constructor for class GeoAnalyzerDataWithOntology
        @staticmethod
        def _static_ctor():
            GeoAnalyzer.GeoAnalyzerDataWithOntology.__ends = ["КИЙ", "КОЕ", "КАЯ"]
    
    ANALYZER_NAME = "GEO"
    
    @property
    def name(self) -> str:
        return GeoAnalyzer.ANALYZER_NAME
    
    @property
    def caption(self) -> str:
        return "Страны, регионы, города"
    
    def clone(self) -> 'Analyzer':
        return GeoAnalyzer()
    
    @property
    def type_system(self) -> typing.List['ReferentClass']:
        return [MetaGeo._global_meta]
    
    @property
    def used_extern_object_types(self) -> typing.List[str]:
        return ["PHONE"]
    
    @property
    def images(self) -> typing.List[tuple]:
        res = dict()
        res[MetaGeo.COUNTRY_CITY_IMAGE_ID] = EpNerCoreInternalResourceHelper.getBytes("countrycity.png")
        res[MetaGeo.COUNTRY_IMAGE_ID] = EpNerCoreInternalResourceHelper.getBytes("country.png")
        res[MetaGeo.CITY_IMAGE_ID] = EpNerCoreInternalResourceHelper.getBytes("city.png")
        res[MetaGeo.DISTRICT_IMAGE_ID] = EpNerCoreInternalResourceHelper.getBytes("district.png")
        res[MetaGeo.REGION_IMAGE_ID] = EpNerCoreInternalResourceHelper.getBytes("region.png")
        res[MetaGeo.TERR_IMAGE_ID] = EpNerCoreInternalResourceHelper.getBytes("territory.png")
        res[MetaGeo.UNION_IMAGE_ID] = EpNerCoreInternalResourceHelper.getBytes("union.png")
        return res
    
    def createReferent(self, type0_ : str) -> 'Referent':
        if (type0_ == GeoReferent.OBJ_TYPENAME): 
            return GeoReferent()
        return None
    
    @property
    def progress_weight(self) -> int:
        return 15
    
    def createAnalyzerData(self) -> 'AnalyzerData':
        return GeoAnalyzer.GeoAnalyzerDataWithOntology()
    
    def process(self, kit : 'AnalysisKit') -> None:
        ad = Utils.asObjectOrNull(kit.getAnalyzerData(self), AnalyzerDataWithOntology)
        t = kit.first_token
        while t is not None: 
            t.inner_bool = False
            t = t.next0_
        non_registered = list()
        for step in range(2):
            t = kit.first_token
            first_pass2916 = True
            while True:
                if first_pass2916: first_pass2916 = False
                else: t = t.next0_
                if (not (t is not None)): break
                if (len(ad.referents) >= 2000): 
                    break
                if (step > 0 and (isinstance(t, ReferentToken))): 
                    geo_ = Utils.asObjectOrNull(t.getReferent(), GeoReferent)
                    if (((geo_ is not None and t.next0_ is not None and t.next0_.isChar('(')) and t.next0_.next0_ is not None and geo_.canBeEquals(t.next0_.next0_.getReferent(), Referent.EqualType.WITHINONETEXT)) and t.next0_.next0_.next0_ is not None and t.next0_.next0_.next0_.isChar(')')): 
                        rt0 = ReferentToken._new746(geo_, t, t.next0_.next0_.next0_, t.morph)
                        kit.embedToken(rt0)
                        t = (rt0)
                        continue
                    if ((geo_ is not None and t.next0_ is not None and t.next0_.is_hiphen) and t.next0_.next0_ is not None and geo_.canBeEquals(t.next0_.next0_.getReferent(), Referent.EqualType.WITHINONETEXT)): 
                        rt0 = ReferentToken._new746(geo_, t, t.next0_.next0_, t.morph)
                        kit.embedToken(rt0)
                        t = (rt0)
                        continue
                ok = False
                if (step == 0 or t.inner_bool): 
                    ok = True
                elif ((isinstance(t, TextToken)) and t.chars.is_letter and not t.chars.is_all_lower): 
                    ok = True
                cli = None
                if (ok): 
                    cli = TerrItemToken.tryParseList(t, ad.local_ontology, 5)
                if (cli is None): 
                    continue
                t.inner_bool = True
                rt = TerrAttachHelper.tryAttachTerritory(cli, ad, False, None, non_registered)
                if ((rt is None and len(cli) == 1 and cli[0].is_adjective) and cli[0].onto_item is not None): 
                    tt = cli[0].end_token.next0_
                    if (tt is not None): 
                        if (tt.isChar(',')): 
                            tt = tt.next0_
                        elif (tt.morph.class0_.is_conjunction): 
                            tt = tt.next0_
                            if (tt is not None and tt.morph.class0_.is_conjunction): 
                                tt = tt.next0_
                        cli1 = TerrItemToken.tryParseList(tt, ad.local_ontology, 2)
                        if (cli1 is not None and cli1[0].onto_item is not None): 
                            g0 = Utils.asObjectOrNull(cli[0].onto_item.referent, GeoReferent)
                            g1 = Utils.asObjectOrNull(cli1[0].onto_item.referent, GeoReferent)
                            if ((g0 is not None and g1 is not None and g0.is_region) and g1.is_region): 
                                if (g0.is_city == g1.is_city or g0.is_region == g1.is_region or g0.is_state == g1.is_state): 
                                    rt = TerrAttachHelper.tryAttachTerritory(cli, ad, True, None, None)
                        if (rt is None and (cli[0].onto_item.referent).is_state): 
                            if ((rt is None and tt is not None and (isinstance(tt.getReferent(), GeoReferent))) and tt.whitespaces_before_count == 1): 
                                geo2 = Utils.asObjectOrNull(tt.getReferent(), GeoReferent)
                                if (GeoOwnerHelper.canBeHigher(Utils.asObjectOrNull(cli[0].onto_item.referent, GeoReferent), geo2)): 
                                    rt = ReferentToken._new746(cli[0].onto_item.referent.clone(), cli[0].begin_token, cli[0].end_token, cli[0].morph)
                            if (rt is None and step == 0): 
                                npt = NounPhraseHelper.tryParse(cli[0].begin_token, NounPhraseParseAttr.NO, 0)
                                if (npt is not None and npt.end_char >= tt.begin_char): 
                                    cits = CityItemToken.tryParseList(tt, ad.local_ontology, 5)
                                    rt1 = (None if cits is None else CityAttachHelper.tryAttachCity(cits, ad, False))
                                    if (rt1 is not None): 
                                        rt1.referent = ad.registerReferent(rt1.referent)
                                        kit.embedToken(rt1)
                                        rt = ReferentToken._new746(cli[0].onto_item.referent.clone(), cli[0].begin_token, cli[0].end_token, cli[0].morph)
                if (rt is None): 
                    cits = self.__tryParseCityListBack(t.previous)
                    if (cits is not None): 
                        rt = TerrAttachHelper.tryAttachTerritory(cli, ad, False, cits, None)
                if (rt is None and len(cli) > 1): 
                    te = cli[len(cli) - 1].end_token.next0_
                    if (te is not None): 
                        if (te.morph.class0_.is_preposition or te.isChar(',')): 
                            te = te.next0_
                    li = AddressItemToken.tryParseList(te, None, 2)
                    if (li is not None and len(li) > 0): 
                        if (li[0].typ == AddressItemToken.ItemType.STREET or li[0].typ == AddressItemToken.ItemType.KILOMETER or li[0].typ == AddressItemToken.ItemType.HOUSE): 
                            ad0 = StreetItemToken.tryParse(cli[0].begin_token.previous, None, False, None, False)
                            if (ad0 is not None and ad0.typ == StreetItemType.NOUN): 
                                pass
                            elif (not cli[0].is_adjective): 
                                rt = TerrAttachHelper.tryAttachTerritory(cli, ad, True, None, None)
                            else: 
                                aaa = AddressItemToken.tryParse(cli[0].begin_token, None, False, False, None)
                                if (aaa is not None and aaa.typ == AddressItemToken.ItemType.STREET): 
                                    pass
                                else: 
                                    rt = TerrAttachHelper.tryAttachTerritory(cli, ad, True, None, None)
                if ((rt is None and len(cli) > 2 and cli[0].termin_item is None) and cli[1].termin_item is None and cli[2].termin_item is not None): 
                    cit = CityItemToken.tryParseBack(cli[0].begin_token.previous)
                    if (cit is not None and cit.typ == CityItemToken.ItemType.NOUN): 
                        if (((len(cli) > 4 and cli[1].termin_item is None and cli[2].termin_item is not None) and cli[3].termin_item is None and cli[4].termin_item is not None) and cli[2].termin_item.canonic_text.endswith(cli[4].termin_item.canonic_text)): 
                            pass
                        else: 
                            del cli[0]
                            rt = TerrAttachHelper.tryAttachTerritory(cli, ad, True, None, None)
                if (rt is not None): 
                    geo_ = Utils.asObjectOrNull(rt.referent, GeoReferent)
                    if (not geo_.is_city and not geo_.is_state and geo_.findSlot(GeoReferent.ATTR_TYPE, "республика", True) is None): 
                        non_registered.append(geo_)
                    else: 
                        rt.referent = ad.registerReferent(geo_)
                    kit.embedToken(rt)
                    t = (rt)
                    if (step == 0): 
                        tt = t
                        while True:
                            rr = self.__tryAttachTerritoryBeforeCity(tt, ad)
                            if (rr is None): 
                                break
                            geo_ = (Utils.asObjectOrNull(rr.referent, GeoReferent))
                            if (not geo_.is_city and not geo_.is_state): 
                                non_registered.append(geo_)
                            else: 
                                rr.referent = ad.registerReferent(geo_)
                            kit.embedToken(rr)
                            tt = (rr)
                        if (t.next0_ is not None and ((t.next0_.is_comma or t.next0_.isChar('(')))): 
                            rt1 = TerrAttachHelper.tryAttachStateUSATerritory(t.next0_.next0_)
                            if (rt1 is not None): 
                                rt1.referent = ad.registerReferent(rt1.referent)
                                kit.embedToken(rt1)
                                t = (rt1)
                    continue
            if (step == 0): 
                if (not self._onProgress(1, 4, kit)): 
                    return
            else: 
                if (not self._onProgress(2, 4, kit)): 
                    return
                if (len(ad.referents) == 0 and len(non_registered) == 0): 
                    break
        t = kit.first_token
        first_pass2917 = True
        while True:
            if first_pass2917: first_pass2917 = False
            else: t = (None if t is None else t.next0_)
            if (not (t is not None)): break
            g = Utils.asObjectOrNull(t.getReferent(), GeoReferent)
            if (g is None): 
                continue
            if (not ((isinstance(t.previous, TextToken)))): 
                continue
            t0 = None
            if (t.previous.isValue("СОЮЗ", None)): 
                t0 = t.previous
            elif (t.previous.isValue("ГОСУДАРСТВО", None) and t.previous.previous is not None and t.previous.previous.isValue("СОЮЗНЫЙ", None)): 
                t0 = t.previous.previous
            if (t0 is None): 
                continue
            npt = NounPhraseHelper.tryParse(t0.previous, NounPhraseParseAttr.NO, 0)
            if (npt is not None and npt.end_token == t.previous): 
                t0 = t0.previous
            uni = GeoReferent()
            typ = MiscHelper.getTextValue(t0, t.previous, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)
            if (typ is None): 
                continue
            uni._addTypUnion(t0.kit.base_language)
            uni._addTyp(typ.lower())
            uni.addSlot(GeoReferent.ATTR_REF, g, False, 0)
            t1 = t
            i = 1
            t = t.next0_
            first_pass2918 = True
            while True:
                if first_pass2918: first_pass2918 = False
                else: t = t.next0_
                if (not (t is not None)): break
                if (t.is_comma_and): 
                    continue
                g = Utils.asObjectOrNull(t.getReferent(), GeoReferent)
                if ((g) is None): 
                    break
                if (uni.findSlot(GeoReferent.ATTR_REF, g, True) is not None): 
                    break
                if (t.is_newline_before): 
                    break
                t1 = t
                uni.addSlot(GeoReferent.ATTR_REF, g, False, 0)
                i += 1
            if (i < 2): 
                continue
            uni = (Utils.asObjectOrNull(ad.registerReferent(uni), GeoReferent))
            rt = ReferentToken(uni, t0, t1)
            kit.embedToken(rt)
            t = (rt)
        new_cities = False
        is_city_before = False
        t = kit.first_token
        first_pass2919 = True
        while True:
            if first_pass2919: first_pass2919 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.isCharOf(".,")): 
                continue
            li = None
            li = CityItemToken.tryParseList(t, ad.local_ontology, 5)
            if (li is not None): 
                rt = CityAttachHelper.tryAttachCity(li, ad, False)
                if ((rt) is not None): 
                    tt = t.previous
                    if (tt is not None and tt.is_comma): 
                        tt = tt.previous
                    if (tt is not None and (isinstance(tt.getReferent(), GeoReferent))): 
                        if (tt.getReferent().canBeEquals(rt.referent, Referent.EqualType.WITHINONETEXT)): 
                            rt.begin_token = tt
                            rt.referent = ad.registerReferent(rt.referent)
                            kit.embedToken(rt)
                            t = (rt)
                            continue
                    if (len(ad.referents) > 2000): 
                        break
                    rt.referent = (Utils.asObjectOrNull(ad.registerReferent(rt.referent), GeoReferent))
                    kit.embedToken(rt)
                    t = (rt)
                    is_city_before = True
                    new_cities = True
                    tt = t
                    while True:
                        rr = self.__tryAttachTerritoryBeforeCity(tt, ad)
                        if (rr is None): 
                            break
                        geo_ = Utils.asObjectOrNull(rr.referent, GeoReferent)
                        if (not geo_.is_city and not geo_.is_state): 
                            non_registered.append(geo_)
                        else: 
                            rr.referent = ad.registerReferent(geo_)
                        kit.embedToken(rr)
                        tt = (rr)
                    rt = self.__tryAttachTerritoryAfterCity(t, ad)
                    if (rt is not None): 
                        rt.referent = ad.registerReferent(rt.referent)
                        kit.embedToken(rt)
                        t = (rt)
                    continue
            if (not t.inner_bool): 
                is_city_before = False
                continue
            if (not is_city_before): 
                continue
            tts = TerrItemToken.tryParseList(t, ad.local_ontology, 5)
            if (tts is not None and len(tts) > 1 and ((tts[0].termin_item is not None or tts[1].termin_item is not None))): 
                rt = TerrAttachHelper.tryAttachTerritory(tts, ad, True, None, None)
                if ((rt) is not None): 
                    geo_ = Utils.asObjectOrNull(rt.referent, GeoReferent)
                    if (not geo_.is_city and not geo_.is_state): 
                        non_registered.append(geo_)
                    else: 
                        rt.referent = ad.registerReferent(geo_)
                    kit.embedToken(rt)
                    t = (rt)
                    continue
            is_city_before = False
        if (new_cities and len(ad.local_ontology.items) > 0): 
            t = kit.first_token
            first_pass2920 = True
            while True:
                if first_pass2920: first_pass2920 = False
                else: t = t.next0_
                if (not (t is not None)): break
                if (not ((isinstance(t, TextToken)))): 
                    continue
                if (t.chars.is_all_lower): 
                    continue
                li = ad.local_ontology.tryAttach(t, None, False)
                if (li is None): 
                    continue
                mc = t.getMorphClassInDictionary()
                if (mc.is_proper_surname or mc.is_proper_name or mc.is_proper_secname): 
                    continue
                if (t.morph.class0_.is_adjective): 
                    continue
                geo_ = Utils.asObjectOrNull(li[0].item.referent, GeoReferent)
                if (geo_ is not None): 
                    rt = ReferentToken._new746(geo_, li[0].begin_token, li[0].end_token, t.morph)
                    if (rt.begin_token == rt.end_token): 
                        geo_._addName((t).term)
                    if (rt.begin_token.previous is not None and rt.begin_token.previous.isValue("СЕЛО", None) and geo_.is_city): 
                        rt.begin_token = rt.begin_token.previous
                        rt.morph = rt.begin_token.morph
                        geo_.addSlot(GeoReferent.ATTR_TYPE, "село", True, 0)
                    kit.embedToken(rt)
                    t = li[0].end_token
        go_back = False
        t = kit.first_token
        first_pass2921 = True
        while True:
            if first_pass2921: first_pass2921 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (go_back): 
                go_back = False
                if (t.previous is not None): 
                    t = t.previous
            geo_ = Utils.asObjectOrNull(t.getReferent(), GeoReferent)
            if (geo_ is None): 
                continue
            geo1 = None
            tt = t.next0_
            bra = False
            comma1 = False
            comma2 = False
            inp = False
            adj = False
            first_pass2922 = True
            while True:
                if first_pass2922: first_pass2922 = False
                else: tt = tt.next0_
                if (not (tt is not None)): break
                if (tt.isCharOf(",")): 
                    comma1 = True
                    continue
                if (tt.isValue("IN", None) or tt.isValue("В", None)): 
                    inp = True
                    continue
                if (MiscHelper.isEngAdjSuffix(tt)): 
                    adj = True
                    tt = tt.next0_
                    continue
                det = AddressItemToken.tryAttachDetail(tt)
                if (det is not None): 
                    tt = det.end_token
                    comma1 = True
                    continue
                if (tt.morph.class0_.is_preposition): 
                    continue
                if (tt.isChar('(') and tt == t.next0_): 
                    bra = True
                    continue
                if ((isinstance(tt, TextToken)) and BracketHelper.isBracket(tt, True)): 
                    continue
                geo1 = (Utils.asObjectOrNull(tt.getReferent(), GeoReferent))
                break
            if (geo1 is None): 
                continue
            if (tt.whitespaces_before_count > 15): 
                continue
            ttt = tt.next0_
            geo2 = None
            first_pass2923 = True
            while True:
                if first_pass2923: first_pass2923 = False
                else: ttt = ttt.next0_
                if (not (ttt is not None)): break
                if (ttt.is_comma_and): 
                    comma2 = True
                    continue
                det = AddressItemToken.tryAttachDetail(ttt)
                if (det is not None): 
                    ttt = det.end_token
                    comma2 = True
                    continue
                if (ttt.morph.class0_.is_preposition): 
                    continue
                geo2 = (Utils.asObjectOrNull(ttt.getReferent(), GeoReferent))
                break
            if (ttt is not None and ttt.whitespaces_before_count > 15): 
                geo2 = (None)
            if (geo2 is not None): 
                if ((comma1 and comma2 and GeoOwnerHelper._canBeHigherToken(t, tt)) and GeoOwnerHelper._canBeHigherToken(tt, ttt)): 
                    geo2.higher = geo1
                    geo1.higher = geo_
                    rt = ReferentToken._new746(geo2, t, ttt, ttt.morph)
                    kit.embedToken(rt)
                    t = (rt)
                    go_back = True
                    continue
                elif (GeoOwnerHelper._canBeHigherToken(ttt, tt)): 
                    if (GeoOwnerHelper._canBeHigherToken(t, ttt)): 
                        geo2.higher = geo_
                        geo1.higher = geo2
                        rt = ReferentToken._new746(geo1, t, ttt, t.morph)
                        kit.embedToken(rt)
                        t = (rt)
                        go_back = True
                        continue
                    if (GeoOwnerHelper._canBeHigherToken(ttt, t) and GeoOwnerHelper._canBeHigherToken(t, tt)): 
                        geo_.higher = geo2
                        geo1.higher = geo_
                        rt = ReferentToken._new746(geo1, t, ttt, tt.morph)
                        kit.embedToken(rt)
                        t = (rt)
                        go_back = True
                        continue
                    if (GeoOwnerHelper._canBeHigherToken(tt, t)): 
                        geo_.higher = geo1
                        geo1.higher = geo2
                        rt = ReferentToken._new746(geo_, t, ttt, t.morph)
                        kit.embedToken(rt)
                        t = (rt)
                        go_back = True
                        continue
                if (comma2): 
                    continue
            if (GeoOwnerHelper._canBeHigherToken(t, tt) and ((not GeoOwnerHelper._canBeHigherToken(tt, t) or adj))): 
                geo1.higher = geo_
                rt = ReferentToken._new746(geo1, t, tt, tt.morph)
                if ((geo1.is_city and not geo_.is_city and t.previous is not None) and t.previous.isValue("СТОЛИЦА", "СТОЛИЦЯ")): 
                    rt.begin_token = t.previous
                    rt.morph = t.previous.morph
                kit.embedToken(rt)
                t = (rt)
                go_back = True
                continue
            if (GeoOwnerHelper._canBeHigherToken(tt, t) and ((not GeoOwnerHelper._canBeHigherToken(t, tt) or inp))): 
                if (geo_.higher is None): 
                    geo_.higher = geo1
                elif (geo1.higher is None and GeoOwnerHelper.canBeHigher(geo_.higher, geo1) and not GeoOwnerHelper.canBeHigher(geo1, geo_.higher)): 
                    geo1.higher = geo_.higher
                    geo_.higher = geo1
                else: 
                    geo_.higher = geo1
                if (bra and tt.next0_ is not None and tt.next0_.isChar(')')): 
                    tt = tt.next0_
                rt = ReferentToken._new746(geo_, t, tt, t.morph)
                kit.embedToken(rt)
                t = (rt)
                go_back = True
                continue
            if ((not tt.morph.class0_.is_adjective and not t.morph.class0_.is_adjective and tt.chars.is_cyrillic_letter) and t.chars.is_cyrillic_letter and not tt.morph.case_.is_instrumental): 
                geo0 = geo_
                while geo0 is not None: 
                    if (GeoOwnerHelper.canBeHigher(geo1, geo0)): 
                        geo0.higher = geo1
                        rt = ReferentToken._new746(geo_, t, tt, t.morph)
                        kit.embedToken(rt)
                        t = (rt)
                        go_back = True
                        break
                    geo0 = geo0.higher
        if (len(non_registered) == 0): 
            return
        k = 0
        while k < len(non_registered): 
            ch = False
            i = 0
            while i < (len(non_registered) - 1): 
                if (GeoAnalyzer.__geoComp(non_registered[i], non_registered[i + 1]) > 0): 
                    ch = True
                    v = non_registered[i]
                    non_registered[i] = non_registered[i + 1]
                    non_registered[i + 1] = v
                i += 1
            if (not ch): 
                break
            k += 1
        for g in non_registered: 
            g.tag = None
        for ng in non_registered: 
            for s in ng.slots: 
                if (isinstance(s.value, GeoReferent)): 
                    if (isinstance((s.value).tag, GeoReferent)): 
                        ng.uploadSlot(s, Utils.asObjectOrNull((s.value).tag, GeoReferent))
            rg = Utils.asObjectOrNull(ad.registerReferent(ng), GeoReferent)
            if (rg == ng): 
                continue
            ng.tag = rg
            for oc in ng.occurrence: 
                oc.occurence_of = rg
                rg.addOccurence(oc)
        t = kit.first_token
        first_pass2924 = True
        while True:
            if first_pass2924: first_pass2924 = False
            else: t = t.next0_
            if (not (t is not None)): break
            geo_ = Utils.asObjectOrNull(t.getReferent(), GeoReferent)
            if (geo_ is None): 
                continue
            GeoAnalyzer.__replaceTerrs(Utils.asObjectOrNull(t, ReferentToken))
    
    @staticmethod
    def __replaceTerrs(mt : 'ReferentToken') -> None:
        if (mt is None): 
            return
        geo_ = Utils.asObjectOrNull(mt.referent, GeoReferent)
        if (geo_ is not None and (isinstance(geo_.tag, GeoReferent))): 
            mt.referent = (Utils.asObjectOrNull(geo_.tag, GeoReferent))
        if (geo_ is not None): 
            for s in geo_.slots: 
                if (isinstance(s.value, GeoReferent)): 
                    g = Utils.asObjectOrNull(s.value, GeoReferent)
                    if (isinstance(g.tag, GeoReferent)): 
                        geo_.uploadSlot(s, g.tag)
        t = mt.begin_token
        while t is not None: 
            if (t.end_char > mt.end_token.end_char): 
                break
            else: 
                if (isinstance(t, ReferentToken)): 
                    GeoAnalyzer.__replaceTerrs(Utils.asObjectOrNull(t, ReferentToken))
                if (t == mt.end_token): 
                    break
            t = t.next0_
    
    @staticmethod
    def __geoComp(x : 'GeoReferent', y : 'GeoReferent') -> int:
        xcou = 0
        g = x.higher
        while g is not None: 
            xcou += 1
            g = g.higher
        ycou = 0
        g = y.higher
        while g is not None: 
            ycou += 1
            g = g.higher
        if (xcou < ycou): 
            return -1
        if (xcou > ycou): 
            return 1
        return Utils.compareStrings(x.toString(True, MorphLang.UNKNOWN, 0), y.toString(True, MorphLang.UNKNOWN, 0), False)
    
    def __tryParseCityListBack(self, t : 'Token') -> typing.List['CityItemToken']:
        if (t is None): 
            return None
        while t is not None and ((t.morph.class0_.is_preposition or t.isCharOf(",.") or t.morph.class0_.is_conjunction)):
            t = t.previous
        if (t is None): 
            return None
        res = None
        tt = t
        while tt is not None: 
            if (not ((isinstance(tt, TextToken)))): 
                break
            if (tt.previous is not None and tt.previous.is_hiphen and (isinstance(tt.previous.previous, TextToken))): 
                if (not tt.is_whitespace_before and not tt.previous.is_whitespace_before): 
                    tt = tt.previous.previous
            ci = CityItemToken.tryParseList(tt, None, 5)
            if (ci is None and tt.previous is not None): 
                ci = CityItemToken.tryParseList(tt.previous, None, 5)
            if (ci is None): 
                break
            if (ci[len(ci) - 1].end_token == t): 
                res = ci
            tt = tt.previous
        if (res is not None): 
            res.reverse()
        return res
    
    def __tryAttachTerritoryBeforeCity(self, t : 'Token', ad : 'AnalyzerDataWithOntology') -> 'ReferentToken':
        if (isinstance(t, ReferentToken)): 
            t = t.previous
        while t is not None: 
            if (not t.isCharOf(",.") and not t.morph.class0_.is_preposition): 
                break
            t = t.previous
        if (t is None): 
            return None
        i = 0
        res = None
        tt = t
        first_pass2925 = True
        while True:
            if first_pass2925: first_pass2925 = False
            else: tt = tt.previous
            if (not (tt is not None)): break
            i += 1
            if (tt.is_newline_after and not tt.inner_bool): 
                break
            if (i > 10): 
                break
            tits0 = TerrItemToken.tryParseList(tt, ad.local_ontology, 5)
            if (tits0 is None): 
                continue
            if (tits0[len(tits0) - 1].end_token != t): 
                break
            tits1 = TerrItemToken.tryParseList(tt.previous, ad.local_ontology, 5)
            if (tits1 is not None and tits1[len(tits1) - 1].end_token == t and len(tits1) == len(tits0)): 
                tits0 = tits1
            rr = TerrAttachHelper.tryAttachTerritory(tits0, ad, False, None, None)
            if (rr is not None): 
                res = rr
        return res
    
    def __tryAttachTerritoryAfterCity(self, t : 'Token', ad : 'AnalyzerDataWithOntology') -> 'ReferentToken':
        if (t is None): 
            return None
        city = Utils.asObjectOrNull(t.getReferent(), GeoReferent)
        if (city is None): 
            return None
        if (not city.is_city): 
            return None
        if (t.next0_ is None or not t.next0_.is_comma or t.next0_.whitespaces_after_count > 1): 
            return None
        tt = t.next0_.next0_
        if (tt is None or not tt.chars.is_capital_upper or not ((isinstance(tt, TextToken)))): 
            return None
        if (tt.chars.is_latin_letter): 
            re1 = TerrAttachHelper.tryAttachStateUSATerritory(tt)
            if (re1 is not None): 
                return re1
        t0 = tt
        t1 = tt
        for i in range(2):
            tit0 = TerrItemToken.tryParse(tt, ad.local_ontology, False, False)
            if (tit0 is None or tit0.termin_item is not None): 
                if (i == 0): 
                    return None
            cit0 = CityItemToken.tryParse(tt, ad.local_ontology, False, None)
            if (cit0 is None or cit0.typ == CityItemToken.ItemType.NOUN): 
                if (i == 0): 
                    return None
            ait0 = AddressItemToken.tryParse(tt, None, False, False, None)
            if (ait0 is not None): 
                return None
            if (tit0 is None): 
                if (not tt.chars.is_cyrillic_letter): 
                    return None
                cla = tt.getMorphClassInDictionary()
                if (not cla.is_noun and not cla.is_adjective): 
                    return None
                t1 = tt
            else: 
                tt = tit0.end_token
                t1 = tt
            if (tt.next0_ is None): 
                return None
            if (tt.next0_.is_comma): 
                tt = tt.next0_.next0_
                break
            if (i > 0): 
                return None
            tt = tt.next0_
        ait = AddressItemToken.tryParse(tt, None, False, False, None)
        if (ait is None): 
            return None
        if (ait.typ != AddressItemToken.ItemType.STREET or ait.ref_token is not None): 
            return None
        reg = GeoReferent()
        reg._addTyp("муниципальный район")
        reg._addName(MiscHelper.getTextValue(t0, t1, GetTextAttr.NO))
        return ReferentToken(reg, t0, t1)
    
    def _processReferent(self, begin : 'Token', end : 'Token') -> 'ReferentToken':
        """ Это привязка стран к прилагательным (например, "французский лидер")
        
        Args:
            begin(Token): 
            end(Token): 
        
        """
        if (not ((isinstance(begin, TextToken)))): 
            return None
        if (begin.kit.recurse_level > 3): 
            return None
        begin.kit.recurse_level += 1
        toks = CityItemToken.M_CITY_ADJECTIVES.tryParseAll(begin, TerminParseAttr.FULLWORDSONLY)
        begin.kit.recurse_level -= 1
        if (toks is not None): 
            for tok in toks: 
                cit = Utils.asObjectOrNull(tok.termin.tag, IntOntologyItem)
                if (cit is None): 
                    continue
                city = GeoReferent()
                city._addName(cit.canonic_text)
                city._addTypCity(begin.kit.base_language)
                return ReferentToken._new1252(city, tok.begin_token, tok.end_token, tok.morph, begin.kit.getAnalyzerData(self))
            return None
        ad = Utils.asObjectOrNull(begin.kit.getAnalyzerData(self), AnalyzerDataWithOntology)
        if (not begin.morph.class0_.is_adjective): 
            te = Utils.asObjectOrNull(begin, TextToken)
            if ((te.chars.is_all_upper and te.chars.is_cyrillic_letter and te.length_char == 2) and te.getMorphClassInDictionary().is_undefined): 
                abbr = te.term
                geo0 = None
                cou = 0
                for t in ad.local_ontology.items: 
                    geo_ = Utils.asObjectOrNull(t.referent, GeoReferent)
                    if (geo_ is None): 
                        continue
                    if (not geo_.is_region and not geo_.is_state): 
                        continue
                    if (geo_._checkAbbr(abbr)): 
                        cou += 1
                        geo0 = geo_
                if (cou == 1): 
                    return ReferentToken._new115(geo0, begin, begin, ad)
            tt0 = TerrItemToken.tryParse(begin, ad.local_ontology, True, False)
            if (tt0 is not None and tt0.termin_item is not None and tt0.termin_item.canonic_text == "РАЙОН"): 
                tt1 = TerrItemToken.tryParse(tt0.end_token.next0_, ad.local_ontology, True, False)
                if ((tt1 is not None and tt1.chars.is_capital_upper and tt1.termin_item is None) and tt1.onto_item is None): 
                    li = list()
                    li.append(tt0)
                    li.append(tt1)
                    res = TerrAttachHelper.tryAttachTerritory(li, ad, True, None, None)
                    if (res is None): 
                        return None
                    res.morph = begin.morph
                    res.data = (ad)
                    return res
            begin.kit.recurse_level += 1
            ctoks = CityItemToken.tryParseList(begin, None, 3)
            if (ctoks is None and begin.morph.class0_.is_preposition): 
                ctoks = CityItemToken.tryParseList(begin.next0_, None, 3)
            begin.kit.recurse_level -= 1
            if (ctoks is not None): 
                if (((len(ctoks) == 2 and ctoks[0].typ == CityItemToken.ItemType.NOUN and ctoks[1].typ == CityItemToken.ItemType.PROPERNAME)) or ((len(ctoks) == 1 and ctoks[0].typ == CityItemToken.ItemType.CITY))): 
                    if (len(ctoks) == 1 and ctoks[0].begin_token.getMorphClassInDictionary().is_proper_surname): 
                        begin.kit.recurse_level += 1
                        kk = begin.kit.processReferent("PERSON", ctoks[0].begin_token)
                        begin.kit.recurse_level -= 1
                        if (kk is not None): 
                            return None
                    res = CityAttachHelper.tryAttachCity(ctoks, ad, True)
                    if (res is not None): 
                        res.data = (ad)
                        return res
            if ((ctoks is not None and len(ctoks) == 1 and ctoks[0].typ == CityItemToken.ItemType.NOUN) and ctoks[0].value == "ГОРОД"): 
                cou = 0
                t = begin.previous
                first_pass2926 = True
                while True:
                    if first_pass2926: first_pass2926 = False
                    else: t = t.previous
                    if (not (t is not None)): break
                    cou += 1
                    if ((cou) > 500): 
                        break
                    if (not ((isinstance(t, ReferentToken)))): 
                        continue
                    geos = t.getReferents()
                    if (geos is None): 
                        continue
                    for g in geos: 
                        gg = Utils.asObjectOrNull(g, GeoReferent)
                        if (gg is not None): 
                            if (gg.is_city): 
                                return ReferentToken._new1252(gg, begin, ctoks[0].end_token, ctoks[0].morph, ad)
                            if (gg.higher is not None and gg.higher.is_city): 
                                return ReferentToken._new1252(gg.higher, begin, ctoks[0].end_token, ctoks[0].morph, ad)
            if (tt0 is not None and tt0.onto_item is not None): 
                pass
            else: 
                return None
        begin.kit.recurse_level += 1
        tt = TerrItemToken.tryParse(begin, ad.local_ontology, True, False)
        begin.kit.recurse_level -= 1
        if (tt is None or tt.onto_item is None): 
            tok = TerrItemToken._m_terr_ontology.tryAttach(begin, None, False)
            if ((tok is not None and tok[0].item is not None and (isinstance(tok[0].item.referent, GeoReferent))) and (tok[0].item.referent).is_state): 
                tt = TerrItemToken._new1163(tok[0].begin_token, tok[0].end_token, tok[0].item)
        if (tt is None): 
            return None
        if (tt.onto_item is not None): 
            li = list()
            li.append(tt)
            res = TerrAttachHelper.tryAttachTerritory(li, ad, True, None, None)
            if (res is None): 
                tt.onto_item = (None)
            else: 
                if (res.begin_token == res.end_token): 
                    mc = res.begin_token.getMorphClassInDictionary()
                    if (mc.is_adjective): 
                        geo_ = Utils.asObjectOrNull(tt.onto_item.referent, GeoReferent)
                        if (geo_.is_city or geo_.is_state): 
                            pass
                        elif (geo_.findSlot(GeoReferent.ATTR_TYPE, "федеральный округ", True) is not None): 
                            return None
                res.data = (ad)
                return res
        if (not tt.is_adjective): 
            return None
        if (tt.onto_item is None): 
            t1 = tt.end_token.next0_
            if (t1 is None): 
                return None
            begin.kit.recurse_level += 1
            ttyp = TerrItemToken.tryParse(t1, ad.local_ontology, True, True)
            begin.kit.recurse_level -= 1
            if (ttyp is None or ttyp.termin_item is None): 
                cits = CityItemToken.tryParseList(begin, None, 2)
                if (cits is not None and cits[0].typ == CityItemToken.ItemType.CITY): 
                    return CityAttachHelper.tryAttachCity(cits, ad, True)
                return None
            if (t1.getMorphClassInDictionary().is_adjective): 
                return None
            li = list()
            li.append(tt)
            li.append(ttyp)
            res = TerrAttachHelper.tryAttachTerritory(li, ad, True, None, None)
            if (res is None): 
                return None
            res.morph = ttyp.morph
            res.data = (ad)
            return res
        return None
    
    def processCitizen(self, begin : 'Token') -> 'ReferentToken':
        if (not ((isinstance(begin, TextToken)))): 
            return None
        tok = TerrItemToken._m_mans_by_state.tryParse(begin, TerminParseAttr.FULLWORDSONLY)
        if (tok is not None): 
            tok.morph.gender = tok.termin.gender
        if (tok is None): 
            return None
        geo0 = Utils.asObjectOrNull(tok.termin.tag, GeoReferent)
        if (geo0 is None): 
            return None
        geo_ = GeoReferent()
        geo_._mergeSlots2(geo0, begin.kit.base_language)
        res = ReferentToken(geo_, tok.begin_token, tok.end_token)
        res.morph = tok.morph
        ad = Utils.asObjectOrNull(begin.kit.getAnalyzerData(self), AnalyzerDataWithOntology)
        res.data = (ad)
        return res
    
    def processOntologyItem(self, begin : 'Token') -> 'ReferentToken':
        li = CityItemToken.tryParseList(begin, None, 4)
        if (li is not None and len(li) > 1 and li[0].typ == CityItemToken.ItemType.NOUN): 
            rt = CityAttachHelper.tryAttachCity(li, None, True)
            if (rt is None): 
                return None
            city = Utils.asObjectOrNull(rt.referent, GeoReferent)
            t = rt.end_token.next0_
            first_pass2927 = True
            while True:
                if first_pass2927: first_pass2927 = False
                else: t = t.next0_
                if (not (t is not None)): break
                if (not t.isChar(';')): 
                    continue
                t = t.next0_
                if (t is None): 
                    break
                li = CityItemToken.tryParseList(t, None, 4)
                rt1 = CityAttachHelper.tryAttachCity(li, None, False)
                if (rt1 is not None): 
                    rt.end_token = rt1.end_token
                    t = rt.end_token
                    city._mergeSlots2(rt1.referent, begin.kit.base_language)
                else: 
                    tt = None
                    ttt = t
                    while ttt is not None: 
                        if (ttt.isChar(';')): 
                            break
                        else: 
                            tt = ttt
                        ttt = ttt.next0_
                    if (tt is not None): 
                        str0_ = MiscHelper.getTextValue(t, tt, GetTextAttr.NO)
                        if (str0_ is not None): 
                            city._addName(str0_)
                        rt.end_token = tt
                        t = rt.end_token
            return rt
        typ = None
        terr = None
        te = None
        t = begin
        first_pass2928 = True
        while True:
            if first_pass2928: first_pass2928 = False
            else: t = t.next0_
            if (not (t is not None)): break
            t0 = t
            t1 = None
            tn0 = None
            tn1 = None
            tt = t0
            first_pass2929 = True
            while True:
                if first_pass2929: first_pass2929 = False
                else: tt = tt.next0_
                if (not (tt is not None)): break
                if (tt.isCharOf(";")): 
                    break
                tit = TerrItemToken.tryParse(tt, None, False, False)
                if (tit is not None and tit.termin_item is not None): 
                    if (not tit.is_adjective): 
                        if (typ is None): 
                            typ = tit.termin_item.canonic_text
                        tt = tit.end_token
                        t1 = tt
                        continue
                elif (tit is not None and tit.onto_item is not None): 
                    pass
                if (tn0 is None): 
                    tn0 = tt
                if (tit is not None): 
                    tt = tit.end_token
                tn1 = tt
                t1 = tn1
            if (t1 is None): 
                continue
            if (terr is None): 
                terr = GeoReferent()
            if (tn0 is not None): 
                terr._addName(MiscHelper.getTextValue(tn0, tn1, GetTextAttr.NO))
            te = t1
            t = te
        if (terr is None or te is None): 
            return None
        if (typ is not None): 
            terr._addTyp(typ)
        if (not terr.is_city and not terr.is_region and not terr.is_state): 
            terr._addTypReg(begin.kit.base_language)
        return ReferentToken(terr, begin, te)
    
    @staticmethod
    def getAllCountries() -> typing.List['Referent']:
        """ Получить список всех стран из внутреннего словаря
        
        """
        return TerrItemToken._m_all_states
    
    M_INITIALIZED = False
    
    @staticmethod
    def initialize() -> None:
        if (GeoAnalyzer.M_INITIALIZED): 
            return
        GeoAnalyzer.M_INITIALIZED = True
        MetaGeo.initialize()
        MetaAddress.initialize()
        MetaStreet.initialize()
        try: 
            Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = True
            MiscLocationHelper._initialize()
            TerrItemToken.initialize()
            CityItemToken.initialize()
            AddressAnalyzer.initialize()
        except Exception as ex: 
            raise Utils.newException(ex.__str__(), ex)
        Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = False
        ProcessorService.registerAnalyzer(GeoAnalyzer())

GeoAnalyzer.GeoAnalyzerDataWithOntology._static_ctor()