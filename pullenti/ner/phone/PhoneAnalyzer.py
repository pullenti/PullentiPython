# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing
import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.Token import Token
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.uri.UriAnalyzer import UriAnalyzer
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.Termin import Termin
from pullenti.ner.phone.internal.PhoneHelper import PhoneHelper
from pullenti.ner.core.ReferentsEqualType import ReferentsEqualType
from pullenti.ner.bank.internal.PullentiNerBankInternalResourceHelper import PullentiNerBankInternalResourceHelper
from pullenti.ner.Referent import Referent
from pullenti.ner.phone.internal.MetaPhone import MetaPhone
from pullenti.ner.phone.PhoneReferent import PhoneReferent
from pullenti.ner.phone.PhoneKind import PhoneKind
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.phone.internal.PhoneItemToken import PhoneItemToken
from pullenti.ner.core.AnalyzerData import AnalyzerData
from pullenti.ner.Analyzer import Analyzer

class PhoneAnalyzer(Analyzer):
    """ Анализатор для выделения телефонных номеров """
    
    class PhoneAnalizerData(AnalyzerData):
        
        def __init__(self) -> None:
            super().__init__()
            self.__m_phones_hash = dict()
        
        def register_referent(self, referent : 'Referent') -> 'Referent':
            from pullenti.ner.core.ReferentsEqualType import ReferentsEqualType
            from pullenti.ner.Referent import Referent
            from pullenti.ner.phone.PhoneReferent import PhoneReferent
            phone_ = Utils.asObjectOrNull(referent, PhoneReferent)
            if (phone_ is None): 
                return None
            key = phone_.number
            if (len(key) >= 10): 
                key = key[3:]
            ph_li = [ ]
            wrapph_li2648 = RefOutArgWrapper(None)
            inoutres2649 = Utils.tryGetValue(self.__m_phones_hash, key, wrapph_li2648)
            ph_li = wrapph_li2648.value
            if (not inoutres2649): 
                ph_li = list()
                self.__m_phones_hash[key] = ph_li
            for p in ph_li: 
                if (p.can_be_equals(phone_, ReferentsEqualType.WITHINONETEXT)): 
                    p.merge_slots(phone_, True)
                    return p
            ph_li.append(phone_)
            self._m_referents.append(phone_)
            return phone_
    
    ANALYZER_NAME = "PHONE"
    """ Имя анализатора ("PHONE") """
    
    @property
    def name(self) -> str:
        return PhoneAnalyzer.ANALYZER_NAME
    
    @property
    def caption(self) -> str:
        return "Телефоны"
    
    @property
    def description(self) -> str:
        return "Телефонные номера"
    
    def clone(self) -> 'Analyzer':
        return PhoneAnalyzer()
    
    @property
    def type_system(self) -> typing.List['ReferentClass']:
        return [MetaPhone._global_meta]
    
    @property
    def images(self) -> typing.List[tuple]:
        res = dict()
        res[MetaPhone.PHONE_IMAGE_ID] = PullentiNerBankInternalResourceHelper.get_bytes("phone.png")
        return res
    
    def create_referent(self, type0_ : str) -> 'Referent':
        if (type0_ == PhoneReferent.OBJ_TYPENAME): 
            return PhoneReferent()
        return None
    
    @property
    def progress_weight(self) -> int:
        return 2
    
    def create_analyzer_data(self) -> 'AnalyzerData':
        return PhoneAnalyzer.PhoneAnalizerData()
    
    def process(self, kit : 'AnalysisKit') -> None:
        ad = Utils.asObjectOrNull(kit.get_analyzer_data(self), PhoneAnalyzer.PhoneAnalizerData)
        t = kit.first_token
        first_pass3882 = True
        while True:
            if first_pass3882: first_pass3882 = False
            else: t = t.next0_
            if (not (t is not None)): break
            pli = PhoneItemToken.try_attach_all(t, 15)
            if (pli is None or len(pli) == 0): 
                continue
            prev_phone = None
            kkk = 0
            tt = t.previous
            while tt is not None: 
                if (isinstance(tt.get_referent(), PhoneReferent)): 
                    prev_phone = (Utils.asObjectOrNull(tt.get_referent(), PhoneReferent))
                    break
                elif (isinstance(tt, ReferentToken)): 
                    pass
                elif (tt.is_char(')')): 
                    ttt = tt.previous
                    cou = 0
                    while ttt is not None: 
                        if (ttt.is_char('(')): 
                            break
                        else: 
                            cou += 1
                            if (cou > 100): 
                                break
                        ttt = ttt.previous
                    if (ttt is None or not ttt.is_char('(')): 
                        break
                    tt = ttt
                elif (not tt.is_char_of(",;/\\") and not tt.is_and): 
                    kkk += 1
                    if (kkk > 5): 
                        break
                    if (tt.is_newline_before or tt.is_newline_after): 
                        break
                tt = tt.previous
            j = 0
            is_phone_before = False
            is_pref = False
            ki = PhoneKind.UNDEFINED
            while j < len(pli):
                if (pli[j].item_type == PhoneItemToken.PhoneItemType.PREFIX): 
                    if (ki == PhoneKind.UNDEFINED): 
                        ki = pli[j].kind
                    is_pref = True
                    is_phone_before = True
                    j += 1
                    if ((j < len(pli)) and pli[j].item_type == PhoneItemToken.PhoneItemType.DELIM): 
                        j += 1
                elif (((j + 1) < len(pli)) and pli[j + 1].item_type == PhoneItemToken.PhoneItemType.PREFIX and j == 0): 
                    if (ki == PhoneKind.UNDEFINED): 
                        ki = pli[0].kind
                    is_pref = True
                    del pli[0]
                else: 
                    break
            if (prev_phone is not None): 
                is_phone_before = True
            if (len(pli) == 1 and pli[0].item_type == PhoneItemToken.PhoneItemType.NUMBER): 
                tt = t.previous
                if ((isinstance(tt, TextToken)) and not tt.chars.is_letter): 
                    tt = tt.previous
                if (isinstance(tt, TextToken)): 
                    if (UriAnalyzer._m_schemes.try_parse(tt, TerminParseAttr.NO) is not None): 
                        continue
            rts = self.__try_attach(pli, j, is_phone_before, prev_phone)
            if (rts is None): 
                j = 1
                while j < len(pli): 
                    if (pli[j].item_type == PhoneItemToken.PhoneItemType.PREFIX): 
                        del pli[0:0+j]
                        rts = self.__try_attach(pli, 1, True, prev_phone)
                        break
                    j += 1
            if (rts is None): 
                t = pli[len(pli) - 1].end_token
            else: 
                if ((ki == PhoneKind.UNDEFINED and prev_phone is not None and not is_pref) and prev_phone.kind != PhoneKind.MOBILE and kkk == 0): 
                    ki = prev_phone.kind
                for rt in rts: 
                    ph = Utils.asObjectOrNull(rt.referent, PhoneReferent)
                    if (ki != PhoneKind.UNDEFINED): 
                        ph.kind = ki
                    else: 
                        if (rt == rts[0] and (rt.whitespaces_before_count < 3)): 
                            tt1 = rt.begin_token.previous
                            if (tt1 is not None and tt1.is_table_control_char): 
                                tt1 = tt1.previous
                            if ((isinstance(tt1, TextToken)) and ((tt1.is_newline_before or ((tt1.previous is not None and tt1.previous.is_table_control_char))))): 
                                term = tt1.term
                                if (term == "T" or term == "Т"): 
                                    rt.begin_token = tt1
                                elif (term == "Ф" or term == "F"): 
                                    ki = PhoneKind.FAX
                                    ph.kind = ki
                                    rt.begin_token = tt1
                                elif (term == "M" or term == "М"): 
                                    ki = PhoneKind.MOBILE
                                    ph.kind = ki
                                    rt.begin_token = tt1
                        ph._correct()
                    rt.referent = ad.register_referent(rt.referent)
                    kit.embed_token(rt)
                    t = (rt)
    
    def __try_attach(self, pli : typing.List['PhoneItemToken'], ind : int, is_phone_before : bool, prev_phone : 'PhoneReferent') -> typing.List['ReferentToken']:
        rt = self.__try_attach_(pli, ind, is_phone_before, prev_phone, 0)
        if (rt is None): 
            return None
        res = list()
        res.append(rt)
        for i in range(5):
            ph0 = Utils.asObjectOrNull(rt.referent, PhoneReferent)
            if (ph0.add_number is not None): 
                return res
            alt = PhoneItemToken.try_attach_alternate(rt.end_token.next0_, ph0, pli)
            if (alt is None): 
                break
            ph = PhoneReferent()
            for s in rt.referent.slots: 
                ph.add_slot(s.type_name, s.value, False, 0)
            num = ph.number
            if (num is None or len(num) <= len(alt.value)): 
                break
            ph.number = num[0:0+len(num) - len(alt.value)] + alt.value
            ph._m_template = ph0._m_template
            rt2 = ReferentToken(ph, alt.begin_token, alt.end_token)
            res.append(rt2)
            rt = rt2
        add = PhoneItemToken.try_attach_additional(rt.end_token.next0_)
        if (add is not None): 
            for rr in res: 
                rr.referent.add_number = add.value
            res[len(res) - 1].end_token = add.end_token
        return res
    
    def process_referent(self, begin : 'Token', end : 'Token') -> 'ReferentToken':
        pli = PhoneItemToken.try_attach_all(begin, 15)
        if (pli is None or len(pli) == 0): 
            return None
        i = 0
        while i < len(pli): 
            if (pli[i].item_type != PhoneItemToken.PhoneItemType.PREFIX): 
                break
            i += 1
        rt = self.__try_attach_(pli, i, True, None, 0)
        if (rt is not None): 
            rt.begin_token = begin
            return rt
        return None
    
    def __try_attach_(self, pli : typing.List['PhoneItemToken'], ind : int, is_phone_before : bool, prev_phone : 'PhoneReferent', lev : int=0) -> 'ReferentToken':
        if (ind >= len(pli) or lev > 4): 
            return None
        country_code = None
        city_code = None
        j = ind
        if (prev_phone is not None and prev_phone._m_template is not None and pli[j].item_type == PhoneItemToken.PhoneItemType.NUMBER): 
            tmp = io.StringIO()
            jj = j
            first_pass3883 = True
            while True:
                if first_pass3883: first_pass3883 = False
                else: jj += 1
                if (not (jj < len(pli))): break
                if (pli[jj].item_type == PhoneItemToken.PhoneItemType.NUMBER): 
                    print(len(pli[jj].value), end="", file=tmp)
                elif (pli[jj].item_type == PhoneItemToken.PhoneItemType.DELIM): 
                    if (pli[jj].value == " "): 
                        break
                    print(pli[jj].value, end="", file=tmp)
                    continue
                else: 
                    break
                templ0 = Utils.toStringStringIO(tmp)
                if (templ0 == prev_phone._m_template): 
                    if ((jj + 1) < len(pli)): 
                        if (pli[jj + 1].item_type == PhoneItemToken.PhoneItemType.PREFIX and (jj + 2) == len(pli)): 
                            pass
                        else: 
                            del pli[jj + 1:jj + 1+len(pli) - jj - 1]
                    break
        if ((j < len(pli)) and pli[j].item_type == PhoneItemToken.PhoneItemType.COUNTRYCODE): 
            country_code = pli[j].value
            if (country_code != "8"): 
                cc = PhoneHelper.get_country_prefix(country_code)
                if (cc is not None and (len(cc) < len(country_code))): 
                    city_code = country_code[len(cc):]
                    country_code = cc
            j += 1
        elif ((j < len(pli)) and pli[j].can_be_country_prefix): 
            k = j + 1
            if ((k < len(pli)) and pli[k].item_type == PhoneItemToken.PhoneItemType.DELIM): 
                k += 1
            rrt = self.__try_attach_(pli, k, is_phone_before, None, lev + 1)
            if (rrt is not None): 
                if ((((is_phone_before and pli[j + 1].item_type == PhoneItemToken.PhoneItemType.DELIM and pli[j + 1].begin_token.is_hiphen) and pli[j].item_type == PhoneItemToken.PhoneItemType.NUMBER and len(pli[j].value) == 3) and ((j + 2) < len(pli)) and pli[j + 2].item_type == PhoneItemToken.PhoneItemType.NUMBER) and len(pli[j + 2].value) == 3): 
                    pass
                else: 
                    country_code = pli[j].value
                    j += 1
        if (((j < len(pli)) and pli[j].item_type == PhoneItemToken.PhoneItemType.NUMBER and ((pli[j].value[0] == '8' or pli[j].value[0] == '7'))) and country_code is None): 
            if (len(pli[j].value) == 1): 
                country_code = pli[j].value
                j += 1
            elif (len(pli[j].value) == 4): 
                country_code = pli[j].value[0:0+1]
                if (city_code is None): 
                    city_code = pli[j].value[1:]
                else: 
                    city_code += pli[j].value[1:]
                j += 1
            elif (len(pli[j].value) == 11 and j == (len(pli) - 1) and is_phone_before): 
                ph0 = PhoneReferent()
                if (pli[j].value[0] != '8'): 
                    ph0.country_code = pli[j].value[0:0+1]
                ph0.number = pli[j].value[1:1+3] + pli[j].value[4:]
                return ReferentToken(ph0, pli[0].begin_token, pli[j].end_token)
            elif (city_code is None and len(pli[j].value) > 3 and ((j + 1) < len(pli))): 
                sum0_ = 0
                for it in pli: 
                    if (it.item_type == PhoneItemToken.PhoneItemType.NUMBER): 
                        sum0_ += len(it.value)
                if (sum0_ == 11): 
                    city_code = pli[j].value[1:]
                    j += 1
        if ((j < len(pli)) and pli[j].item_type == PhoneItemToken.PhoneItemType.CITYCODE): 
            if (city_code is None): 
                city_code = pli[j].value
            else: 
                city_code += pli[j].value
            j += 1
        if ((j < len(pli)) and pli[j].item_type == PhoneItemToken.PhoneItemType.DELIM): 
            j += 1
        if ((country_code == "8" and city_code is None and ((j + 3) < len(pli))) and pli[j].item_type == PhoneItemToken.PhoneItemType.NUMBER): 
            if (len(pli[j].value) == 3 or len(pli[j].value) == 4): 
                city_code = pli[j].value
                j += 1
                if ((j < len(pli)) and pli[j].item_type == PhoneItemToken.PhoneItemType.DELIM): 
                    j += 1
        normal_num_len = 0
        if (country_code == "421"): 
            normal_num_len = 9
        num = io.StringIO()
        templ = io.StringIO()
        part_length = list()
        delim = None
        ok = False
        additional = None
        std = False
        if (country_code is not None and ((j + 4) < len(pli)) and j > 0): 
            if (((((pli[j - 1].value == "-" or pli[j - 1].item_type == PhoneItemToken.PhoneItemType.COUNTRYCODE)) and pli[j].item_type == PhoneItemToken.PhoneItemType.NUMBER and pli[j + 1].item_type == PhoneItemToken.PhoneItemType.DELIM) and pli[j + 2].item_type == PhoneItemToken.PhoneItemType.NUMBER and pli[j + 3].item_type == PhoneItemToken.PhoneItemType.DELIM) and pli[j + 4].item_type == PhoneItemToken.PhoneItemType.NUMBER): 
                if ((((len(pli[j].value) + len(pli[j + 2].value)) == 6 or ((len(pli[j].value) == 4 and len(pli[j + 2].value) == 5)))) and ((len(pli[j + 4].value) == 4 or len(pli[j + 4].value) == 1))): 
                    print(pli[j].value, end="", file=num)
                    print(pli[j + 2].value, end="", file=num)
                    print(pli[j + 4].value, end="", file=num)
                    print("{0}{1}{2}{3}{4}".format(len(pli[j].value), pli[j + 1].value, len(pli[j + 2].value), pli[j + 3].value, len(pli[j + 4].value)), end="", file=templ, flush=True)
                    std = True
                    ok = True
                    j += 5
        first_pass3884 = True
        while True:
            if first_pass3884: first_pass3884 = False
            else: j += 1
            if (not (j < len(pli))): break
            if (std): 
                break
            if (pli[j].item_type == PhoneItemToken.PhoneItemType.DELIM): 
                if (pli[j].is_in_brackets): 
                    continue
                if (j > 0 and pli[j - 1].is_in_brackets): 
                    continue
                if (templ.tell() > 0): 
                    print(pli[j].value, end="", file=templ)
                if (delim is None): 
                    delim = pli[j].value
                elif (pli[j].value != delim): 
                    if ((len(part_length) == 2 and ((part_length[0] == 3 or part_length[0] == 4)) and city_code is None) and part_length[1] == 3): 
                        city_code = Utils.toStringStringIO(num)[0:0+part_length[0]]
                        Utils.removeStringIO(num, 0, part_length[0])
                        del part_length[0]
                        delim = pli[j].value
                        continue
                    if (is_phone_before and ((j + 1) < len(pli)) and pli[j + 1].item_type == PhoneItemToken.PhoneItemType.NUMBER): 
                        if (num.tell() < 6): 
                            continue
                        if (normal_num_len > 0 and (num.tell() + len(pli[j + 1].value)) == normal_num_len): 
                            continue
                    break
                else: 
                    continue
                ok = False
            elif (pli[j].item_type == PhoneItemToken.PhoneItemType.NUMBER): 
                if (num.tell() == 0 and pli[j].begin_token.previous is not None and pli[j].begin_token.previous.is_table_control_char): 
                    tt = pli[len(pli) - 1].end_token.next0_
                    if (tt is not None and tt.is_char_of(",.")): 
                        tt = tt.next0_
                    if (isinstance(tt, NumberToken)): 
                        return None
                if ((num.tell() + len(pli[j].value)) > 13): 
                    if (j > 0 and pli[j - 1].item_type == PhoneItemToken.PhoneItemType.DELIM): 
                        j -= 1
                    ok = True
                    break
                print(pli[j].value, end="", file=num)
                part_length.append(len(pli[j].value))
                print(len(pli[j].value), end="", file=templ)
                ok = True
                if (num.tell() > 10): 
                    j += 1
                    if ((j < len(pli)) and pli[j].item_type == PhoneItemToken.PhoneItemType.ADDNUMBER): 
                        additional = pli[j].value
                        j += 1
                    break
            elif (pli[j].item_type == PhoneItemToken.PhoneItemType.ADDNUMBER): 
                additional = pli[j].value
                j += 1
                break
            else: 
                break
        if ((j == (len(pli) - 1) and pli[j].is_in_brackets and ((len(pli[j].value) == 3 or len(pli[j].value) == 4))) and additional is None): 
            additional = pli[j].value
            j += 1
        if ((j < len(pli)) and pli[j].item_type == PhoneItemToken.PhoneItemType.PREFIX and pli[j].is_in_brackets): 
            is_phone_before = True
            j += 1
        if ((country_code is None and city_code is not None and len(city_code) > 3) and (num.tell() < 8) and city_code[0] != '8'): 
            if ((len(city_code) + num.tell()) == 10): 
                pass
            else: 
                cc = PhoneHelper.get_country_prefix(city_code)
                if (cc is not None): 
                    if (len(cc) > 1 and (len(city_code) - len(cc)) > 1): 
                        country_code = cc
                        city_code = city_code[len(cc):]
        if (country_code is None and city_code is not None and city_code.startswith("00")): 
            cc = PhoneHelper.get_country_prefix(city_code[2:])
            if (cc is not None): 
                if (len(city_code) > (len(cc) + 3)): 
                    country_code = cc
                    city_code = city_code[len(cc) + 2:]
        if (num.tell() == 0 and city_code is not None): 
            if (len(city_code) == 10): 
                print(city_code[3:], end="", file=num)
                part_length.append(num.tell())
                city_code = city_code[0:0+3]
                ok = True
            elif (((len(city_code) == 9 or len(city_code) == 11 or len(city_code) == 8)) and ((is_phone_before or country_code is not None))): 
                print(city_code, end="", file=num)
                part_length.append(num.tell())
                city_code = (None)
                ok = True
        if (num.tell() < 4): 
            ok = False
        if (num.tell() < 7): 
            if (city_code is not None and (len(city_code) + num.tell()) > 7): 
                if (not is_phone_before and len(city_code) == 3): 
                    ii = 0
                    while ii < len(part_length): 
                        if (part_length[ii] == 3): 
                            pass
                        elif (part_length[ii] > 3): 
                            break
                        elif ((ii < (len(part_length) - 1)) or (part_length[ii] < 2)): 
                            break
                        ii += 1
                    if (ii >= len(part_length)): 
                        if (country_code == "61"): 
                            pass
                        else: 
                            ok = False
            elif (((num.tell() == 6 or num.tell() == 5)) and ((len(part_length) >= 1 and len(part_length) <= 3)) and is_phone_before): 
                if (pli[0].item_type == PhoneItemToken.PhoneItemType.PREFIX and pli[0].kind == PhoneKind.HOME): 
                    ok = False
            elif (prev_phone is not None and prev_phone.number is not None and ((len(prev_phone.number) == num.tell() or len(prev_phone.number) == (num.tell() + 3) or len(prev_phone.number) == (num.tell() + 4)))): 
                pass
            elif (num.tell() > 4 and prev_phone is not None and Utils.toStringStringIO(templ) == prev_phone._m_template): 
                ok = True
            else: 
                ok = False
        if (delim == "." and country_code is None and city_code is None): 
            ok = False
        if ((is_phone_before and country_code is None and city_code is None) and num.tell() > 10): 
            cc = PhoneHelper.get_country_prefix(Utils.toStringStringIO(num))
            if (cc is not None): 
                if ((num.tell() - len(cc)) == 9): 
                    country_code = cc
                    Utils.removeStringIO(num, 0, len(cc))
                    ok = True
        if (ok): 
            if (std): 
                pass
            elif (prev_phone is not None and prev_phone.number is not None and (((len(prev_phone.number) == num.tell() or len(prev_phone.number) == (num.tell() + 3) or len(prev_phone.number) == (num.tell() + 4)) or prev_phone._m_template == Utils.toStringStringIO(templ)))): 
                pass
            elif ((len(part_length) == 3 and part_length[0] == 3 and part_length[1] == 2) and part_length[2] == 2): 
                pass
            elif (len(part_length) == 3 and is_phone_before): 
                pass
            elif ((len(part_length) == 4 and (((part_length[0] + part_length[1]) == 3)) and part_length[2] == 2) and part_length[3] == 2): 
                pass
            elif ((len(part_length) == 4 and part_length[0] == 3 and part_length[1] == 3) and part_length[2] == 2 and part_length[3] == 2): 
                pass
            elif (len(part_length) == 5 and (part_length[1] + part_length[2]) == 4 and (part_length[3] + part_length[4]) == 4): 
                pass
            elif (len(part_length) > 4): 
                ok = False
            elif (len(part_length) > 3 and city_code is not None): 
                ok = False
            elif ((is_phone_before or city_code is not None or country_code is not None) or additional is not None): 
                ok = True
            else: 
                ok = False
                if (((num.tell() == 6 or num.tell() == 7)) and (len(part_length) < 4) and j > 0): 
                    next_ph = self.__get_next_phone(pli[j - 1].end_token.next0_, lev + 1)
                    if (next_ph is not None): 
                        d = len(next_ph.number) - num.tell()
                        if (d == 0 or d == 3 or d == 4): 
                            ok = True
        end = (pli[j - 1].end_token if j > 0 else None)
        if (end is None): 
            ok = False
        if ((ok and city_code is None and country_code is None) and prev_phone is None and not is_phone_before): 
            if (not end.is_whitespace_after and end.next0_ is not None): 
                tt = end.next0_
                if (tt.is_char_of(".,)") and tt.next0_ is not None): 
                    tt = tt.next0_
                if (not tt.is_whitespace_before): 
                    ok = False
        if (not ok): 
            return None
        if (templ.tell() > 0 and not str.isdigit(Utils.getCharAtStringIO(templ, templ.tell() - 1))): 
            Utils.setLengthStringIO(templ, templ.tell() - 1)
        if ((country_code is None and city_code is not None and len(city_code) > 3) and num.tell() > 6): 
            cc = PhoneHelper.get_country_prefix(city_code)
            if (cc is not None and ((len(cc) + 1) < len(city_code))): 
                country_code = cc
                city_code = city_code[len(cc):]
        if (pli[0].begin_token.previous is not None): 
            if (pli[0].begin_token.previous.is_value("ГОСТ", None) or pli[0].begin_token.previous.is_value("ТУ", None)): 
                return None
        ph = PhoneReferent()
        if (country_code is not None): 
            ph.country_code = country_code
        number = Utils.toStringStringIO(num)
        if ((city_code is None and num.tell() > 7 and len(part_length) > 0) and (part_length[0] < 5)): 
            city_code = number[0:0+part_length[0]]
            number = number[part_length[0]:]
        if (city_code is None and num.tell() == 11 and Utils.getCharAtStringIO(num, 0) == '8'): 
            city_code = number[1:1+3]
            number = number[4:]
        if (city_code is None and num.tell() == 10): 
            city_code = number[0:0+3]
            number = number[3:]
        if (city_code is not None): 
            number = (city_code + number)
        elif (country_code is None and prev_phone is not None): 
            ok1 = False
            if (len(prev_phone.number) >= (len(number) + 2)): 
                ok1 = True
            elif (templ.tell() > 0 and prev_phone._m_template is not None and LanguageHelper.ends_with(prev_phone._m_template, Utils.toStringStringIO(templ))): 
                ok1 = True
            if (ok1 and len(prev_phone.number) > len(number)): 
                number = (prev_phone.number[0:0+len(prev_phone.number) - len(number)] + number)
        if (ph.country_code is None and prev_phone is not None and prev_phone.country_code is not None): 
            if (len(prev_phone.number) == len(number)): 
                ph.country_code = prev_phone.country_code
        ok = False
        for d in number: 
            if (d != '0'): 
                ok = True
                break
        if (not ok): 
            return None
        if (country_code is not None): 
            if (len(number) < 7): 
                return None
        else: 
            s = PhoneHelper.get_country_prefix(number)
            if (s is not None): 
                num2 = number[len(s):]
                if (len(num2) >= 10 and len(num2) <= 11): 
                    number = num2
                    if (s != "7"): 
                        ph.country_code = s
            if (len(number) == 8 and prev_phone is None): 
                return None
        if (len(number) > 11): 
            if ((len(number) < 14) and ((country_code == "1" or country_code == "43"))): 
                pass
            else: 
                return None
        ph.number = number
        if (additional is not None): 
            ph.add_slot(PhoneReferent.ATTR_ADDNUMBER, additional, True, 0)
        if (not is_phone_before and end.next0_ is not None and not end.is_newline_after): 
            if (end.next0_.is_char_of("+=") or end.next0_.is_hiphen): 
                return None
        if (country_code is not None and country_code == "7"): 
            if (len(number) != 10): 
                return None
        ph._m_template = Utils.toStringStringIO(templ)
        if (j == (len(pli) - 1) and pli[j].item_type == PhoneItemToken.PhoneItemType.PREFIX and not pli[j].is_newline_before): 
            end = pli[j].end_token
            if (pli[j].kind != PhoneKind.UNDEFINED): 
                ph.kind = pli[j].kind
        res = ReferentToken(ph, pli[0].begin_token, end)
        if (pli[0].item_type == PhoneItemToken.PhoneItemType.PREFIX and pli[0].end_token.next0_.is_table_control_char): 
            res.begin_token = pli[1].begin_token
        return res
    
    def __get_next_phone(self, t : 'Token', lev : int) -> 'PhoneReferent':
        if (t is not None and t.is_char(',')): 
            t = t.next0_
        if (t is None or lev > 3): 
            return None
        its = PhoneItemToken.try_attach_all(t, 15)
        if (its is None): 
            return None
        rt = self.__try_attach_(its, 0, False, None, lev + 1)
        if (rt is None): 
            return None
        return Utils.asObjectOrNull(rt.referent, PhoneReferent)
    
    M_INITED = None
    
    @staticmethod
    def initialize() -> None:
        if (PhoneAnalyzer.M_INITED): 
            return
        PhoneAnalyzer.M_INITED = True
        MetaPhone.initialize()
        try: 
            Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = True
            PhoneHelper.initialize()
            PhoneItemToken.initialize()
            Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = False
        except Exception as ex: 
            raise Utils.newException(ex.__str__(), ex)
        ProcessorService.register_analyzer(PhoneAnalyzer())