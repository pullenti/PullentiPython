# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import typing
import math
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.ner.Analyzer import Analyzer
from pullenti.ner.core.AnalyzerData import AnalyzerData
from pullenti.ner.address.internal.ResourceHelper import ResourceHelper
from pullenti.ner.address.AddressDetailType import AddressDetailType
from pullenti.ner.address.AddressHouseType import AddressHouseType
from pullenti.ner.address.AddressBuildingType import AddressBuildingType
from pullenti.ner.geo.internal.GeoOwnerHelper import GeoOwnerHelper
from pullenti.ner.address.internal.StreetDefineHelper import StreetDefineHelper
from pullenti.ner.core.GetTextAttr import GetTextAttr


class AddressAnalyzer(Analyzer):
    """ Семантический анализатор адресов """
    
    class AddressAnalyzerData(AnalyzerData):
        
        def __init__(self) -> None:
            from pullenti.ner.core.AnalyzerDataWithOntology import AnalyzerDataWithOntology
            super().__init__()
            self.__m_addresses = AnalyzerData()
            self.streets = AnalyzerDataWithOntology()
        
        def register_referent(self, referent : 'Referent') -> 'Referent':
            from pullenti.ner.address.StreetReferent import StreetReferent
            if (isinstance(referent, StreetReferent)): 
                (referent if isinstance(referent, StreetReferent) else None)._correct()
                return self.streets.register_referent(referent)
            else: 
                return self.__m_addresses.register_referent(referent)
        
        @property
        def referents(self) -> typing.List['Referent']:
            if (len(self.streets.referents) == 0): 
                return self.__m_addresses.referents
            elif (len(self.__m_addresses.referents) == 0): 
                return self.streets.referents
            res = list(self.streets.referents)
            res.extend(self.__m_addresses.referents)
            return res
    
    ANALYZER_NAME = "ADDRESS"
    
    @property
    def name(self) -> str:
        return AddressAnalyzer.ANALYZER_NAME
    
    @property
    def caption(self) -> str:
        return "Адреса"
    
    @property
    def description(self) -> str:
        return "Адреса (улицы, дома ...)"
    
    def clone(self) -> 'Analyzer':
        return AddressAnalyzer()
    
    @property
    def type_system(self) -> typing.List['ReferentClass']:
        from pullenti.ner.address.internal.MetaAddress import MetaAddress
        from pullenti.ner.address.internal.MetaStreet import MetaStreet
        return [MetaAddress._global_meta, MetaStreet._global_meta]
    
    @property
    def images(self) -> typing.List[tuple]:
        from pullenti.ner.address.internal.MetaAddress import MetaAddress
        from pullenti.ner.address.internal.MetaStreet import MetaStreet
        res = dict()
        res[MetaAddress.ADDRESS_IMAGE_ID] = ResourceHelper.get_bytes("address.png")
        res[MetaStreet.IMAGE_ID] = ResourceHelper.get_bytes("street.png")
        return res
    
    @property
    def progress_weight(self) -> int:
        return 10
    
    def create_referent(self, type0_ : str) -> 'Referent':
        from pullenti.ner.address.AddressReferent import AddressReferent
        from pullenti.ner.address.StreetReferent import StreetReferent
        if (type0_ == AddressReferent.OBJ_TYPENAME): 
            return AddressReferent()
        if (type0_ == StreetReferent.OBJ_TYPENAME): 
            return StreetReferent()
        return None
    
    @property
    def used_extern_object_types(self) -> typing.List[str]:
        from pullenti.ner.geo.GeoReferent import GeoReferent
        return [GeoReferent.OBJ_TYPENAME, "PHONE", "URI"]
    
    def create_analyzer_data(self) -> 'AnalyzerData':
        
        return AddressAnalyzer.AddressAnalyzerData()
    
    def process(self, kit : 'AnalysisKit') -> None:
        
        from pullenti.ner.address.internal.AddressItemToken import AddressItemToken
        from pullenti.ner.Referent import Referent
        from pullenti.ner.address.AddressReferent import AddressReferent
        from pullenti.ner.geo.GeoReferent import GeoReferent
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.address.StreetReferent import StreetReferent
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.NumberToken import NumberToken
        ad = (kit.get_analyzer_data(self) if isinstance(kit.get_analyzer_data(self), AddressAnalyzer.AddressAnalyzerData) else None)
        steps = 1
        max0_ = steps
        delta = 100000
        parts = math.floor((((len(kit.sofa.text) + delta) - 1)) / delta)
        if (parts == 0): 
            parts = 1
        max0_ *= parts
        cur = 0
        next_pos = delta
        t = kit.first_token
        first_pass3641 = True
        while True:
            if first_pass3641: first_pass3641 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.begin_char > next_pos): 
                next_pos += delta
                cur += 1
                if (not self._on_progress(cur, max0_, kit)): 
                    return
            li = AddressItemToken.try_parse_list(t, ad.streets.local_ontology, 20)
            if (li is None): 
                continue
            addr = AddressReferent()
            streets = list()
            metro = None
            det_typ = AddressDetailType.UNDEFINED
            det_param = 0
            geos = None
            err = False
            near_city = None
            i = 0
            while i < len(li): 
                if ((li[i].typ == AddressItemToken.ItemType.DETAIL and li[i].detail_type == AddressDetailType.CROSS and ((i + 2) < len(li))) and li[i + 1].typ == AddressItemToken.ItemType.STREET and li[i + 2].typ == AddressItemToken.ItemType.STREET): 
                    det_typ = AddressDetailType.CROSS
                    streets.append(li[i + 1])
                    streets.append(li[i + 2])
                    li[i + 1].end_token = li[i + 2].end_token
                    li[i].tag = (self)
                    li[i + 1].tag = (self)
                    del li[i + 2]
                    break
                elif (li[i].typ == AddressItemToken.ItemType.STREET): 
                    if (((li[i].ref_token is not None and not li[i].ref_token_is_gsk)) and len(streets) == 0): 
                        if (i > 0 and li[i].is_newline_before): 
                            err = True
                        elif ((i + 1) == len(li)): 
                            err = (det_typ == AddressDetailType.UNDEFINED and det_param == 0 and near_city is None)
                        elif (((i + 1) < len(li)) and li[i + 1].typ == AddressItemToken.ItemType.NUMBER): 
                            err = True
                        if (err and geos is not None): 
                            for ii in range(i - 1, -1, -1):
                                if (li[ii].typ == AddressItemToken.ItemType.ZIP or li[ii].typ == AddressItemToken.ItemType.PREFIX): 
                                    err = False
                        if (err): 
                            break
                    li[i].tag = (self)
                    streets.append(li[i])
                    if (((i + 1) < len(li)) and li[i + 1].typ == AddressItemToken.ItemType.STREET): 
                        pass
                    else: 
                        break
                elif (li[i].typ == AddressItemToken.ItemType.CITY or li[i].typ == AddressItemToken.ItemType.REGION): 
                    if (geos is None): 
                        geos = list()
                    geos.insert(0, (li[i].referent if isinstance(li[i].referent, GeoReferent) else None))
                    if (li[i].detail_type != AddressDetailType.UNDEFINED and det_typ == AddressDetailType.UNDEFINED): 
                        if (li[i].typ == AddressItemToken.ItemType.CITY and li[i].detail_type == AddressDetailType.NEAR and li[i].detail_meters == 0): 
                            near_city = li[i]
                        else: 
                            det_typ = li[i].detail_type
                    if (li[i].detail_meters > 0 and det_param == 0): 
                        det_param = li[i].detail_meters
                elif (li[i].typ == AddressItemToken.ItemType.DETAIL): 
                    if (li[i].detail_type != AddressDetailType.UNDEFINED and det_typ == AddressDetailType.UNDEFINED): 
                        if (li[i].detail_type == AddressDetailType.NEAR and ((i + 1) < len(li)) and li[i + 1].typ == AddressItemToken.ItemType.CITY): 
                            near_city = li[i + 1]
                            li[i].tag = (self)
                            i += 1
                        else: 
                            det_typ = li[i].detail_type
                            if (li[i].detail_meters > 0): 
                                det_param = li[i].detail_meters
                    li[i].tag = (self)
                i += 1
            if (i >= len(li) and metro is None and det_typ == AddressDetailType.UNDEFINED): 
                i = 0
                first_pass3642 = True
                while True:
                    if first_pass3642: first_pass3642 = False
                    else: i += 1
                    if (not (i < len(li))): break
                    cit = False
                    if (li[i].typ == AddressItemToken.ItemType.CITY): 
                        cit = True
                    elif (li[i].typ == AddressItemToken.ItemType.REGION): 
                        for s in li[i].referent.slots: 
                            if (s.type_name == GeoReferent.ATTR_TYPE): 
                                ss = (s.value if isinstance(s.value, str) else None)
                                if ("посел" in ss or "сельск" in ss): 
                                    cit = True
                    if (cit): 
                        if (((i + 1) < len(li)) and ((((li[i + 1].typ == AddressItemToken.ItemType.HOUSE or li[i + 1].typ == AddressItemToken.ItemType.BLOCK or li[i + 1].typ == AddressItemToken.ItemType.PLOT) or li[i + 1].typ == AddressItemToken.ItemType.BUILDING or li[i + 1].typ == AddressItemToken.ItemType.CORPUS) or li[i + 1].typ == AddressItemToken.ItemType.POSTOFFICEBOX or li[i + 1].typ == AddressItemToken.ItemType.CSP))): 
                            break
                        if (((i + 1) < len(li)) and li[i + 1].typ == AddressItemToken.ItemType.NUMBER): 
                            if (li[i].end_token.next0_.is_comma): 
                                if ((isinstance(li[i].referent, GeoReferent)) and not (li[i].referent if isinstance(li[i].referent, GeoReferent) else None).is_big_city and (li[i].referent if isinstance(li[i].referent, GeoReferent) else None).is_city): 
                                    li[i + 1].typ = AddressItemToken.ItemType.HOUSE
                                    break
                        if (li[0].typ == AddressItemToken.ItemType.ZIP or li[0].typ == AddressItemToken.ItemType.PREFIX): 
                            break
                        continue
                    if (li[i].typ == AddressItemToken.ItemType.REGION): 
                        if ((isinstance(li[i].referent, GeoReferent)) and (li[i].referent if isinstance(li[i].referent, GeoReferent) else None).higher is not None and (li[i].referent if isinstance(li[i].referent, GeoReferent) else None).higher.is_city): 
                            if (((i + 1) < len(li)) and li[i + 1].typ == AddressItemToken.ItemType.HOUSE): 
                                break
                if (i >= len(li)): 
                    continue
            if (err): 
                continue
            i0 = i
            if (i > 0 and li[i - 1].typ == AddressItemToken.ItemType.HOUSE and li[i - 1].is_digit): 
                addr.house = li[i - 1].value
                li[i - 1].tag = (self)
            elif ((i > 0 and li[i - 1].typ == AddressItemToken.ItemType.KILOMETER and li[i - 1].is_digit) and (i < len(li)) and li[i].is_street_road): 
                addr.kilometer = li[i - 1].value
                li[i - 1].tag = (self)
            else: 
                if (i >= len(li)): 
                    i = -1
                i = 0
                first_pass3643 = True
                while True:
                    if first_pass3643: first_pass3643 = False
                    else: i += 1
                    if (not (i < len(li))): break
                    if (li[i].tag is not None): 
                        continue
                    if (li[i].typ == AddressItemToken.ItemType.HOUSE): 
                        if (addr.house is not None): 
                            break
                        if (li[i].value is not None): 
                            addr.house = (Utils.ifNotNull(li[i].value, ""))
                            if (li[i].house_type != AddressHouseType.UNDEFINED): 
                                addr.house_type = li[i].house_type
                        li[i].tag = (self)
                    elif (li[i].typ == AddressItemToken.ItemType.KILOMETER and li[i].is_digit and (((i0 < len(li)) and li[i0].is_street_road))): 
                        if (addr.kilometer is not None): 
                            break
                        addr.kilometer = li[i].value
                        li[i].tag = (self)
                    elif (li[i].typ == AddressItemToken.ItemType.PLOT): 
                        if (addr.plot is not None): 
                            break
                        addr.plot = li[i].value
                        li[i].tag = (self)
                    elif (li[i].typ == AddressItemToken.ItemType.BOX and li[i].is_digit): 
                        if (addr.box is not None): 
                            break
                        addr.box = li[i].value
                        li[i].tag = (self)
                    elif (li[i].typ == AddressItemToken.ItemType.BLOCK and li[i].is_digit): 
                        if (addr.block is not None): 
                            break
                        addr.block = li[i].value
                        li[i].tag = (self)
                    elif (li[i].typ == AddressItemToken.ItemType.CORPUS): 
                        if (addr.corpus is not None): 
                            break
                        if (li[i].value is not None): 
                            addr.corpus = li[i].value
                        li[i].tag = (self)
                    elif (li[i].typ == AddressItemToken.ItemType.BUILDING): 
                        if (addr.building is not None): 
                            break
                        if (li[i].value is not None): 
                            addr.building = li[i].value
                            if (li[i].building_type != AddressBuildingType.UNDEFINED): 
                                addr.building_type = li[i].building_type
                        li[i].tag = (self)
                    elif (li[i].typ == AddressItemToken.ItemType.FLOOR and li[i].is_digit): 
                        if (addr.floor0_ is not None): 
                            break
                        addr.floor0_ = li[i].value
                        li[i].tag = (self)
                    elif (li[i].typ == AddressItemToken.ItemType.POTCH and li[i].is_digit): 
                        if (addr.potch is not None): 
                            break
                        addr.potch = li[i].value
                        li[i].tag = (self)
                    elif (li[i].typ == AddressItemToken.ItemType.FLAT): 
                        if (addr.flat is not None): 
                            break
                        if (li[i].value is not None): 
                            addr.flat = li[i].value
                        li[i].tag = (self)
                    elif (li[i].typ == AddressItemToken.ItemType.OFFICE and li[i].is_digit): 
                        if (addr.office is not None): 
                            break
                        addr.office = li[i].value
                        li[i].tag = (self)
                    elif (li[i].typ == AddressItemToken.ItemType.CORPUSORFLAT and ((li[i].is_digit or li[i].value is None))): 
                        j = (i + 1)
                        while j < len(li): 
                            if (li[j].is_digit): 
                                if (((li[j].typ == AddressItemToken.ItemType.FLAT or li[j].typ == AddressItemToken.ItemType.CORPUSORFLAT or li[j].typ == AddressItemToken.ItemType.OFFICE) or li[j].typ == AddressItemToken.ItemType.FLOOR or li[j].typ == AddressItemToken.ItemType.POTCH) or li[j].typ == AddressItemToken.ItemType.POSTOFFICEBOX or li[j].typ == AddressItemToken.ItemType.BUILDING): 
                                    break
                            j += 1
                        if (li[i].value is not None): 
                            if ((j < len(li)) and addr.corpus is None): 
                                addr.corpus = li[i].value
                            elif (addr.corpus is not None): 
                                addr.flat = li[i].value
                            else: 
                                addr.corpus_or_flat = li[i].value
                        li[i].tag = (self)
                    elif ((not li[i].is_newline_before and li[i].typ == AddressItemToken.ItemType.NUMBER and li[i].is_digit) and li[i - 1].typ == AddressItemToken.ItemType.STREET): 
                        v = 0
                        inoutarg339 = RefOutArgWrapper(0)
                        inoutres340 = Utils.tryParseInt(li[i].value, inoutarg339)
                        v = inoutarg339.value
                        if (not inoutres340): 
                            inoutarg333 = RefOutArgWrapper(0)
                            inoutres334 = Utils.tryParseInt(li[i].value[0:0+len(li[i].value) - 1], inoutarg333)
                            v = inoutarg333.value
                            if (not inoutres334): 
                                if (not "/" in li[i].value): 
                                    break
                        if (v > 400): 
                            break
                        addr.house = li[i].value
                        li[i].tag = (self)
                        if (((i + 1) < len(li)) and ((li[i + 1].typ == AddressItemToken.ItemType.NUMBER or li[i + 1].typ == AddressItemToken.ItemType.FLAT)) and not li[i + 1].is_newline_before): 
                            inoutarg337 = RefOutArgWrapper(0)
                            inoutres338 = Utils.tryParseInt(li[i + 1].value, inoutarg337)
                            v = inoutarg337.value
                            if (not inoutres338): 
                                break
                            if (v > 500): 
                                break
                            i += 1
                            if ((((i + 1) < len(li)) and li[i + 1].typ == AddressItemToken.ItemType.NUMBER and not li[i + 1].is_newline_before) and (v < 5)): 
                                inoutarg335 = RefOutArgWrapper(0)
                                inoutres336 = Utils.tryParseInt(li[i + 1].value, inoutarg335)
                                v = inoutarg335.value
                                if (inoutres336): 
                                    if (v < 500): 
                                        addr.corpus = li[i].value
                                        li[i].tag = (self)
                                        i += 1
                            addr.flat = li[i].value
                            li[i].tag = (self)
                    elif (li[i].typ == AddressItemToken.ItemType.CITY): 
                        if (geos is None): 
                            geos = list()
                        if (li[i].is_newline_before): 
                            if (len(geos) > 0): 
                                if ((i > 0 and li[i - 1].typ != AddressItemToken.ItemType.CITY and li[i - 1].typ != AddressItemToken.ItemType.REGION) and li[i - 1].typ != AddressItemToken.ItemType.ZIP and li[i - 1].typ != AddressItemToken.ItemType.PREFIX): 
                                    break
                            if (((i + 1) < len(li)) and li[i + 1].typ == AddressItemToken.ItemType.STREET and i > i0): 
                                break
                        if (li[i].detail_type == AddressDetailType.NEAR and li[i].detail_meters == 0): 
                            near_city = li[i]
                            li[i].tag = (self)
                            continue
                        ii = 0
                        while ii < len(geos): 
                            if (geos[ii].is_city): 
                                break
                            ii += 1
                        if (ii >= len(geos)): 
                            geos.append(li[i].referent if isinstance(li[i].referent, GeoReferent) else None)
                        elif (i > 0 and li[i].is_newline_before and i > i0): 
                            jj = 0
                            while jj < i: 
                                if ((li[jj].typ != AddressItemToken.ItemType.PREFIX and li[jj].typ != AddressItemToken.ItemType.ZIP and li[jj].typ != AddressItemToken.ItemType.REGION) and li[jj].typ != AddressItemToken.ItemType.COUNTRY and li[jj].typ != AddressItemToken.ItemType.CITY): 
                                    break
                                jj += 1
                            if (jj < i): 
                                break
                        if (li[i].detail_type != AddressDetailType.UNDEFINED and det_typ == AddressDetailType.UNDEFINED): 
                            det_typ = li[i].detail_type
                            if (li[i].detail_meters > 0): 
                                det_param = li[i].detail_meters
                        li[i].tag = (self)
                    elif (li[i].typ == AddressItemToken.ItemType.POSTOFFICEBOX): 
                        if (addr.post_office_box is not None): 
                            break
                        addr.post_office_box = li[i].value
                        li[i].tag = (self)
                    elif (li[i].typ == AddressItemToken.ItemType.CSP): 
                        if (addr.csp is not None): 
                            break
                        addr.csp = li[i].value
                        li[i].tag = (self)
                    elif (li[i].typ == AddressItemToken.ItemType.STREET): 
                        if (len(streets) > 1): 
                            break
                        if (len(streets) > 0): 
                            if (li[i].is_newline_before): 
                                break
                            if (MiscHelper.can_be_start_of_sentence(li[i].begin_token)): 
                                break
                        if (li[i].ref_token is None and i > 0 and li[i - 1].typ != AddressItemToken.ItemType.STREET): 
                            break
                        streets.append(li[i])
                        li[i].tag = (self)
                    elif (li[i].typ == AddressItemToken.ItemType.DETAIL): 
                        if ((i + 1) == len(li) and li[i].detail_type == AddressDetailType.NEAR): 
                            break
                        if (li[i].detail_type == AddressDetailType.NEAR and ((i + 1) < len(li)) and li[i + 1].typ == AddressItemToken.ItemType.CITY): 
                            near_city = li[i + 1]
                            li[i].tag = (self)
                            i += 1
                        elif (li[i].detail_type != AddressDetailType.UNDEFINED and det_typ == AddressDetailType.UNDEFINED): 
                            det_typ = li[i].detail_type
                            if (li[i].detail_meters > 0): 
                                det_param = li[i].detail_meters
                        li[i].tag = (self)
                    elif (li[i].typ == AddressItemToken.ItemType.BUSINESSCENTER and li[i].ref_token is not None): 
                        addr.add_ext_referent(li[i].ref_token)
                        addr.add_slot(AddressReferent.ATTR_MISC, li[i].ref_token.referent, False, 0)
                        li[i].tag = (self)
                    elif (i > i0): 
                        break
            typs = list()
            for s in addr.slots: 
                if (not s.type_name in typs): 
                    typs.append(s.type_name)
            if (len(streets) == 1 and not streets[0].is_doubt and streets[0].ref_token is None): 
                pass
            elif (len(li) > 2 and li[0].typ == AddressItemToken.ItemType.ZIP and ((li[1].typ == AddressItemToken.ItemType.COUNTRY or li[1].typ == AddressItemToken.ItemType.REGION))): 
                pass
            elif ((len(typs) + len(streets)) < 2): 
                if (len(typs) > 0): 
                    if ((((typs[0] != AddressReferent.ATTR_STREET and typs[0] != AddressReferent.ATTR_POSTOFFICEBOX and metro is None) and typs[0] != AddressReferent.ATTR_HOUSE and typs[0] != AddressReferent.ATTR_CORPUS) and typs[0] != AddressReferent.ATTR_BUILDING and typs[0] != AddressReferent.ATTR_PLOT) and typs[0] != AddressReferent.ATTR_DETAIL and det_typ == AddressDetailType.UNDEFINED): 
                        continue
                elif (len(streets) == 0 and det_typ == AddressDetailType.UNDEFINED): 
                    if (li[i - 1].typ == AddressItemToken.ItemType.CITY and i > 2 and li[i - 2].typ == AddressItemToken.ItemType.ZIP): 
                        pass
                    else: 
                        continue
                elif ((i == len(li) and len(streets) == 1 and (isinstance(streets[0].referent, StreetReferent))) and streets[0].referent.find_slot(StreetReferent.ATTR_TYP, "квартал", True) is not None): 
                    continue
                if (geos is None): 
                    has_geo = False
                    tt = li[0].begin_token.previous
                    first_pass3644 = True
                    while True:
                        if first_pass3644: first_pass3644 = False
                        else: tt = tt.previous
                        if (not (tt is not None)): break
                        if (tt.morph.class0_.is_preposition or tt.is_comma): 
                            continue
                        r = tt.get_referent()
                        if (r is None): 
                            break
                        if (r.type_name == "DATE" or r.type_name == "DATERANGE"): 
                            continue
                        if (isinstance(r, GeoReferent)): 
                            if (not (r if isinstance(r, GeoReferent) else None).is_state): 
                                if (geos is None): 
                                    geos = list()
                                geos.append(r if isinstance(r, GeoReferent) else None)
                                has_geo = True
                        break
                    if (not has_geo): 
                        continue
            i = 0
            while i < len(li): 
                if (li[i].typ == AddressItemToken.ItemType.PREFIX): 
                    li[i].tag = (self)
                elif (li[i].tag is None): 
                    if (li[i].is_newline_before and i > i0): 
                        stop = False
                        j = (i + 1)
                        while j < len(li): 
                            if (li[j].typ == AddressItemToken.ItemType.STREET): 
                                stop = True
                                break
                            j += 1
                        if (stop): 
                            break
                    if (li[i].typ == AddressItemToken.ItemType.COUNTRY or li[i].typ == AddressItemToken.ItemType.REGION or li[i].typ == AddressItemToken.ItemType.CITY): 
                        if (geos is None): 
                            geos = list()
                        if (not (li[i].referent if isinstance(li[i].referent, GeoReferent) else None) in geos): 
                            geos.append(li[i].referent if isinstance(li[i].referent, GeoReferent) else None)
                        if (li[i].typ != AddressItemToken.ItemType.COUNTRY): 
                            if (li[i].detail_type != AddressDetailType.UNDEFINED and addr.detail == AddressDetailType.UNDEFINED): 
                                addr.detail = li[i].detail_type
                                if (li[i].detail_meters > 0): 
                                    addr.add_slot(AddressReferent.ATTR_DETAILPARAM, "{0}м".format(li[i].detail_meters), False, 0)
                        li[i].tag = (self)
                    elif (li[i].typ == AddressItemToken.ItemType.ZIP): 
                        if (addr.zip0_ is not None): 
                            break
                        addr.zip0_ = li[i].value
                        li[i].tag = (self)
                    elif (li[i].typ == AddressItemToken.ItemType.POSTOFFICEBOX): 
                        if (addr.post_office_box is not None): 
                            break
                        addr.post_office_box = li[i].value
                        li[i].tag = (self)
                    elif (li[i].typ == AddressItemToken.ItemType.CSP): 
                        if (addr.csp is not None): 
                            break
                        addr.csp = li[i].value
                        li[i].tag = (self)
                    elif (li[i].typ == AddressItemToken.ItemType.NUMBER and li[i].is_digit and len(li[i].value) == 6): 
                        if (((i + 1) < len(li)) and li[i + 1].typ == AddressItemToken.ItemType.CITY): 
                            if (addr.zip0_ is not None): 
                                break
                            addr.zip0_ = li[i].value
                            li[i].tag = (self)
                    else: 
                        break
                i += 1
            t0 = None
            t1 = None
            i = 0
            while i < len(li): 
                if (li[i].tag is not None): 
                    t0 = li[i].begin_token
                    break
                i += 1
            for i in range(len(li) - 1, -1, -1):
                if (li[i].tag is not None): 
                    t1 = li[i].end_token
                    break
            else: i = -1
            if (t0 is None or t1 is None): 
                continue
            if (len(addr.slots) == 0): 
                pure_streets = 0
                gsks = 0
                for s in streets: 
                    if (s.ref_token is not None and s.ref_token_is_gsk): 
                        gsks += 1
                    elif (s.ref_token is None): 
                        pure_streets += 1
                if ((pure_streets + gsks) == 0 and len(streets) > 0): 
                    if (((det_typ != AddressDetailType.UNDEFINED or near_city is not None)) and geos is not None): 
                        pass
                    else: 
                        addr = (None)
                elif (len(streets) < 2): 
                    if ((len(streets) == 1 and geos is not None and len(geos) > 0) and ((streets[0].ref_token is None or streets[0].ref_token_is_gsk))): 
                        pass
                    elif (det_typ != AddressDetailType.UNDEFINED and geos is not None and len(streets) == 0): 
                        pass
                    else: 
                        addr = (None)
            if (addr is not None and det_typ != AddressDetailType.UNDEFINED): 
                addr.detail = det_typ
                if (det_param > 0): 
                    addr.add_slot(AddressReferent.ATTR_DETAILPARAM, "{0}м".format(det_param), False, 0)
            if (geos is None and len(streets) > 0 and not streets[0].is_street_road): 
                cou = 0
                tt = t0.previous
                while tt is not None and (cou < 200): 
                    if (tt.is_newline_after): 
                        cou += 10
                    r = tt.get_referent()
                    if ((isinstance(r, GeoReferent)) and not (r if isinstance(r, GeoReferent) else None).is_state): 
                        geos = list()
                        geos.append(r if isinstance(r, GeoReferent) else None)
                        break
                    if (isinstance(r, StreetReferent)): 
                        ggg = (r if isinstance(r, StreetReferent) else None).geos
                        if (len(ggg) > 0): 
                            geos = list(ggg)
                            break
                    if (isinstance(r, AddressReferent)): 
                        ggg = (r if isinstance(r, AddressReferent) else None).geos
                        if (len(ggg) > 0): 
                            geos = list(ggg)
                            break
                    tt = tt.previous; cou += 1
            terr_ref = None
            ter_ref0 = None
            sr0 = None
            ii = 0
            first_pass3645 = True
            while True:
                if first_pass3645: first_pass3645 = False
                else: ii += 1
                if (not (ii < len(streets))): break
                s = streets[ii]
                sr = (s.referent if isinstance(s.referent, StreetReferent) else None)
                if ((sr is None and s.referent is not None and s.referent.type_name == "ORGANIZATION") and s.ref_token is not None): 
                    if (s.ref_token_is_gsk and addr is None): 
                        addr = AddressReferent()
                    if (addr is not None): 
                        addr.add_referent(s.referent)
                        addr.add_ext_referent(s.ref_token)
                        ter_ref0 = s.ref_token
                        if (geos is None or len(geos) == 0): 
                            continue
                        jj = Utils.indexOfList(li, s, 0)
                        geo0 = None
                        if (jj > 0 and (isinstance(li[jj - 1].referent, GeoReferent)) and ((li[jj - 1] != near_city or (li[jj - 1].referent if isinstance(li[jj - 1].referent, GeoReferent) else None).higher is not None))): 
                            geo0 = (li[jj - 1].referent if isinstance(li[jj - 1].referent, GeoReferent) else None)
                        elif (jj > 1 and (isinstance(li[jj - 2].referent, GeoReferent))): 
                            geo0 = (li[jj - 2].referent if isinstance(li[jj - 2].referent, GeoReferent) else None)
                        elif (near_city is not None): 
                            geo0 = (near_city.referent if isinstance(near_city.referent, GeoReferent) else None)
                        if (geo0 is not None and ((geo0.is_region or geo0.is_city))): 
                            geo = GeoReferent()
                            geo._add_typ_ter(kit.base_language)
                            if (geo0.is_region): 
                                geo._add_typ(("населений пункт" if kit.base_language.is_ua else "населенный пункт"))
                            geo._add_org_referent(s.referent)
                            if (near_city is not None and geo0 == near_city.referent): 
                                geo.higher = geo0.higher
                            else: 
                                geo.higher = geo0
                            sl = addr.find_slot(AddressReferent.ATTR_GEO, geo0, True)
                            if (sl is not None): 
                                addr.slots.remove(sl)
                            sl = addr.find_slot(AddressReferent.ATTR_STREET, s.referent, True)
                            if ((sl) is not None): 
                                addr.slots.remove(sl)
                            geos.remove(geo0)
                            if (near_city is not None and (near_city.referent if isinstance(near_city.referent, GeoReferent) else None) in geos): 
                                geos.remove(near_city.referent if isinstance(near_city.referent, GeoReferent) else None)
                            geos.append(geo)
                            del streets[ii]
                            rtt = ReferentToken(geo, s.ref_token.begin_token, s.ref_token.end_token)
                            rtt.data = kit.get_analyzer_data_by_analyzer_name("GEO")
                            if (near_city is not None and (isinstance(near_city.referent, GeoReferent))): 
                                geo.add_slot(GeoReferent.ATTR_REF, near_city.referent, False, 0)
                                if (near_city.end_char > rtt.end_char): 
                                    rtt.end_token = near_city.end_token
                                if (near_city.begin_char < rtt.begin_char): 
                                    rtt.begin_token = near_city.begin_token
                                if ((near_city.referent if isinstance(near_city.referent, GeoReferent) else None).higher is None and geo0 != near_city.referent): 
                                    (near_city.referent if isinstance(near_city.referent, GeoReferent) else None).higher = geo0
                            addr.add_ext_referent(rtt)
                            terr_ref = rtt
                            ii -= 1
                            continue
                        if ((geo0 is not None and geo0.is_territory and jj > 0) and li[jj - 1].referent == geo0): 
                            geo0.add_slot(GeoReferent.ATTR_REF, s.referent, False, 0)
                            geo0.add_ext_referent(s.ref_token)
                            rtt = ReferentToken(geo0, li[jj - 1].begin_token, s.ref_token.end_token)
                            rtt.data = kit.get_analyzer_data_by_analyzer_name("GEO")
                            addr.add_ext_referent(rtt)
                            terr_ref = rtt
                            del streets[ii]
                            ii -= 1
                            continue
                        for gr in geos: 
                            if (s.referent.find_slot("GEO", gr, True) is not None): 
                                geos.remove(gr)
                                sl = addr.find_slot(AddressReferent.ATTR_GEO, gr, True)
                                if (sl is not None): 
                                    addr.slots.remove(sl)
                                break
                    continue
                if (sr is not None and terr_ref is not None): 
                    sr.add_slot(StreetReferent.ATTR_GEO, terr_ref.referent, False, 0)
                    sr.add_ext_referent(terr_ref)
                    if (geos is not None and (terr_ref.referent if isinstance(terr_ref.referent, GeoReferent) else None) in geos): 
                        geos.remove(terr_ref.referent if isinstance(terr_ref.referent, GeoReferent) else None)
                if (geos is not None and sr is not None and len(sr.geos) == 0): 
                    for gr in geos: 
                        if (gr.is_city or ((gr.higher is not None and gr.higher.is_city))): 
                            sr.add_slot(StreetReferent.ATTR_GEO, gr, False, 0)
                            if (li[0].referent == gr): 
                                streets[0].begin_token = li[0].begin_token
                            jj = ii + 1
                            while jj < len(streets): 
                                if (isinstance(streets[jj].referent, StreetReferent)): 
                                    streets[jj].referent.add_slot(StreetReferent.ATTR_GEO, gr, False, 0)
                                jj += 1
                            geos.remove(gr)
                            break
                if (sr is not None and len(sr.geos) == 0): 
                    if (sr0 is not None): 
                        for g in sr0.geos: 
                            sr.add_slot(StreetReferent.ATTR_GEO, g, False, 0)
                    sr0 = sr
                if (s.referent is not None and s.referent.find_slot(StreetReferent.ATTR_NAME, "НЕТ", True) is not None): 
                    for ss in s.referent.slots: 
                        if (ss.type_name == StreetReferent.ATTR_GEO): 
                            addr.add_referent(ss.value if isinstance(ss.value, Referent) else None)
                else: 
                    s.referent = ad.register_referent(s.referent)
                    if (addr is not None): 
                        addr.add_referent(s.referent)
                    rt = ReferentToken(s.referent, s.begin_token, s.end_token)
                    t = rt
                    kit.embed_token(rt)
                    if (s.begin_token == t0): 
                        t0 = (rt)
                    if (s.end_token == t1): 
                        t1 = (rt)
            if (addr is not None): 
                ok = False
                for s in addr.slots: 
                    if (s.type_name != AddressReferent.ATTR_DETAIL): 
                        ok = True
                if (not ok): 
                    addr = (None)
            if (addr is None): 
                if (terr_ref is not None): 
                    terr_ref.referent.add_ext_referent(ter_ref0)
                    terr_ref.referent = ad.register_referent(terr_ref.referent)
                    kit.embed_token(terr_ref)
                    t = (terr_ref)
                    continue
                continue
            if (geos is not None): 
                if ((len(geos) == 1 and geos[0].is_region and len(streets) == 1) and streets[0].ref_token is not None): 
                    pass
                if (len(streets) == 1 and streets[0].referent is not None): 
                    for s in streets[0].referent.slots: 
                        if (s.type_name == StreetReferent.ATTR_GEO and (isinstance(s.value, GeoReferent))): 
                            k = 0
                            gg = (s.value if isinstance(s.value, GeoReferent) else None)
                            while gg is not None and (k < 5): 
                                for ii in range(len(geos) - 1, -1, -1):
                                    if (geos[ii] == gg): 
                                        del geos[ii]
                                        break
                                gg = (gg.parent_referent if isinstance(gg.parent_referent, GeoReferent) else None); k += 1
                while len(geos) >= 2:
                    if (geos[1].higher is None and GeoOwnerHelper.can_be_higher(geos[0], geos[1])): 
                        geos[1].higher = geos[0]
                        del geos[0]
                    elif (geos[0].higher is None and GeoOwnerHelper.can_be_higher(geos[1], geos[0])): 
                        geos[0].higher = geos[1]
                        del geos[1]
                    elif (geos[1].higher is not None and geos[1].higher.higher is None and GeoOwnerHelper.can_be_higher(geos[0], geos[1].higher)): 
                        geos[1].higher.higher = geos[0]
                        del geos[0]
                    elif (geos[0].higher is not None and geos[0].higher.higher is None and GeoOwnerHelper.can_be_higher(geos[1], geos[0].higher)): 
                        geos[0].higher.higher = geos[1]
                        del geos[1]
                    else: 
                        break
                for g in geos: 
                    addr.add_referent(g)
            ok1 = False
            for s in addr.slots: 
                if (s.type_name != AddressReferent.ATTR_STREET): 
                    ok1 = True
                    break
            if (not ok1): 
                continue
            if (addr.house is not None and addr.corpus is None and addr.find_slot(AddressReferent.ATTR_STREET, None, True) is None): 
                if (geos is not None and len(geos) > 0 and geos[0].find_slot(GeoReferent.ATTR_NAME, "ЗЕЛЕНОГРАД", True) is not None): 
                    addr.corpus = addr.house
                    addr.house = None
            rt = ReferentToken(ad.register_referent(addr), t0, t1)
            kit.embed_token(rt)
            t = (rt)
            if ((t.next0_ is not None and ((t.next0_.is_comma or t.next0_.is_char(';'))) and (t.next0_.whitespaces_after_count < 2)) and (isinstance(t.next0_.next0_, NumberToken))): 
                last = None
                for ll in li: 
                    if (ll.tag is not None): 
                        last = ll
                attr_name = None
                if (last is None): 
                    continue
                if (last.typ == AddressItemToken.ItemType.HOUSE): 
                    attr_name = AddressReferent.ATTR_HOUSE
                elif (last.typ == AddressItemToken.ItemType.CORPUS): 
                    attr_name = AddressReferent.ATTR_CORPUS
                elif (last.typ == AddressItemToken.ItemType.BUILDING): 
                    attr_name = AddressReferent.ATTR_BUILDING
                elif (last.typ == AddressItemToken.ItemType.FLAT): 
                    attr_name = AddressReferent.ATTR_FLAT
                elif (last.typ == AddressItemToken.ItemType.PLOT): 
                    attr_name = AddressReferent.ATTR_PLOT
                elif (last.typ == AddressItemToken.ItemType.BOX): 
                    attr_name = AddressReferent.ATTR_BOX
                elif (last.typ == AddressItemToken.ItemType.POTCH): 
                    attr_name = AddressReferent.ATTR_PORCH
                elif (last.typ == AddressItemToken.ItemType.BLOCK): 
                    attr_name = AddressReferent.ATTR_BLOCK
                elif (last.typ == AddressItemToken.ItemType.OFFICE): 
                    attr_name = AddressReferent.ATTR_OFFICE
                if (attr_name is not None): 
                    t = t.next0_.next0_
                    while t is not None: 
                        if (not ((isinstance(t, NumberToken)))): 
                            break
                        addr1 = (addr.clone() if isinstance(addr.clone(), AddressReferent) else None)
                        addr1.occurrence.clear()
                        addr1.add_slot(attr_name, str((t if isinstance(t, NumberToken) else None).value), True, 0)
                        rt = ReferentToken(ad.register_referent(addr1), t, t)
                        kit.embed_token(rt)
                        t = (rt)
                        if ((t.next0_ is not None and ((t.next0_.is_comma or t.next0_.is_char(';'))) and (t.next0_.whitespaces_after_count < 2)) and (isinstance(t.next0_.next0_, NumberToken))): 
                            pass
                        else: 
                            break
                        t = t.next0_
        sli = list()
        t = kit.first_token
        first_pass3646 = True
        while True:
            if first_pass3646: first_pass3646 = False
            else: t = (None if t is None else t.next0_)
            if (not (t is not None)): break
            sr = (t.get_referent() if isinstance(t.get_referent(), StreetReferent) else None)
            if (sr is None): 
                continue
            if (t.next0_ is None or not t.next0_.is_comma_and): 
                continue
            sli.clear()
            sli.append(sr)
            t = t.next0_
            first_pass3647 = True
            while True:
                if first_pass3647: first_pass3647 = False
                else: t = t.next0_
                if (not (t is not None)): break
                if (t.is_comma_and): 
                    continue
                sr = (t.get_referent() if isinstance(t.get_referent(), StreetReferent) else None)
                if ((sr) is not None): 
                    sli.append(sr)
                    continue
                adr = (t.get_referent() if isinstance(t.get_referent(), AddressReferent) else None)
                if (adr is None): 
                    break
                if (len(adr.streets) == 0): 
                    break
                for ss in adr.streets: 
                    if (isinstance(ss, StreetReferent)): 
                        sli.append(ss if isinstance(ss, StreetReferent) else None)
            if (len(sli) < 2): 
                continue
            ok = True
            hi = None
            for s in sli: 
                if (len(s.geos) == 0): 
                    continue
                elif (len(s.geos) == 1): 
                    if (hi is None or hi == s.geos[0]): 
                        hi = s.geos[0]
                    else: 
                        ok = False
                        break
                else: 
                    ok = False
                    break
            if (ok and hi is not None): 
                for s in sli: 
                    if (len(s.geos) == 0): 
                        s.add_slot(StreetReferent.ATTR_GEO, hi, False, 0)
        for a in ad.referents: 
            if (isinstance(a, AddressReferent)): 
                (a if isinstance(a, AddressReferent) else None)._correct()
    
    def process_ontology_item(self, begin : 'Token') -> 'ReferentToken':
        from pullenti.ner.address.internal.StreetItemToken import StreetItemToken
        from pullenti.ner.address.StreetReferent import StreetReferent
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.ReferentToken import ReferentToken
        li = StreetItemToken.try_parse_list(begin, None, 10)
        if (li is None or (len(li) < 2)): 
            return None
        rt = StreetDefineHelper._try_parse_street(li, True, False)
        if (rt is None): 
            return None
        street = (rt.referent if isinstance(rt.referent, StreetReferent) else None)
        t = rt.end_token.next0_
        first_pass3648 = True
        while True:
            if first_pass3648: first_pass3648 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (not t.is_char(';')): 
                continue
            t = t.next0_
            if (t is None): 
                break
            li = StreetItemToken.try_parse_list(begin, None, 10)
            rt1 = StreetDefineHelper._try_parse_street(li, True, False)
            if (rt1 is not None): 
                rt.end_token = rt1.end_token
                t = rt.end_token
                street.merge_slots(rt1.referent, True)
            else: 
                tt = None
                ttt = t
                while ttt is not None: 
                    if (ttt.is_char(';')): 
                        break
                    else: 
                        tt = ttt
                    ttt = ttt.next0_
                if (tt is not None): 
                    str0_ = MiscHelper.get_text_value(t, tt, GetTextAttr.NO)
                    if (str0_ is not None): 
                        street.add_slot(StreetReferent.ATTR_NAME, MiscHelper.convert_first_char_upper_and_other_lower(str0_), False, 0)
                    rt.end_token = tt
                    t = rt.end_token
        return ReferentToken(street, rt.begin_token, rt.end_token)
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.address.internal.AddressItemToken import AddressItemToken
        from pullenti.ner.ProcessorService import ProcessorService
        try: 
            AddressItemToken.initialize()
        except Exception as ex: 
            raise Utils.newException(ex.__str__(), ex)
        ProcessorService.register_analyzer(AddressAnalyzer())