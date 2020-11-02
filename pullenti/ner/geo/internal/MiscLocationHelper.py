# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing
import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.morph.internal.MorphDeserializer import MorphDeserializer
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.TextToken import TextToken
from pullenti.ner.address.StreetReferent import StreetReferent
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.address.AddressReferent import AddressReferent

class MiscLocationHelper:
    
    @staticmethod
    def check_geo_object_before(t : 'Token') -> bool:
        from pullenti.ner.geo.internal.CityItemToken import CityItemToken
        if (t is None): 
            return False
        tt = t.previous
        first_pass3649 = True
        while True:
            if first_pass3649: first_pass3649 = False
            else: tt = tt.previous
            if (not (tt is not None)): break
            if ((tt.is_char_of(",.;:") or tt.is_hiphen or tt.is_and) or tt.morph.class0_.is_conjunction or tt.morph.class0_.is_preposition): 
                continue
            if (tt.is_value("ТЕРРИТОРИЯ", "ТЕРИТОРІЯ")): 
                continue
            if ((tt.is_value("ПРОЖИВАТЬ", "ПРОЖИВАТИ") or tt.is_value("РОДИТЬ", "НАРОДИТИ") or tt.is_value("ЗАРЕГИСТРИРОВАТЬ", "ЗАРЕЄСТРУВАТИ")) or tt.is_value("АДРЕС", None)): 
                return True
            if (tt.is_value("УРОЖЕНЕЦ", "УРОДЖЕНЕЦЬ") or tt.is_value("УРОЖЕНКА", "УРОДЖЕНКА")): 
                return True
            if (tt.length_char == 2 and (isinstance(tt, TextToken)) and tt.chars.is_all_upper): 
                term = tt.term
                if (not Utils.isNullOrEmpty(term) and term[0] == 'Р'): 
                    return True
            rt = Utils.asObjectOrNull(tt, ReferentToken)
            if (rt is None): 
                break
            if ((isinstance(rt.referent, GeoReferent)) or (isinstance(rt.referent, AddressReferent)) or (isinstance(rt.referent, StreetReferent))): 
                return True
            break
        if (t.previous is not None and t.previous.previous is not None): 
            cit2 = CityItemToken.try_parse(t.previous, None, False, None)
            if (cit2 is not None and cit2.typ != CityItemToken.ItemType.NOUN and cit2.end_token.next0_ == t): 
                cit1 = CityItemToken.try_parse(t.previous.previous, None, False, None)
                if (cit1 is not None and cit1.typ == CityItemToken.ItemType.NOUN): 
                    return True
                if (cit1 is None and t.previous.previous.is_char('.') and t.previous.previous.previous is not None): 
                    tt = t.previous.previous.previous
                    cit1 = CityItemToken.try_parse(tt, None, False, None)
                    if (cit1 is not None and cit1.typ == CityItemToken.ItemType.NOUN): 
                        return True
                    if (tt.is_value("С", None) or tt.is_value("Д", None) or tt.is_value("ПОС", None)): 
                        return True
        return False
    
    @staticmethod
    def check_geo_object_after(t : 'Token', dont_check_city : bool=False) -> bool:
        from pullenti.ner.geo.internal.CityItemToken import CityItemToken
        if (t is None): 
            return False
        cou = 0
        tt = t.next0_
        first_pass3650 = True
        while True:
            if first_pass3650: first_pass3650 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            if (tt.is_char_of(",.;") or tt.is_hiphen or tt.morph.class0_.is_conjunction): 
                continue
            if (tt.morph.class0_.is_preposition): 
                if (not dont_check_city and tt.is_value("С", None) and tt.next0_ is not None): 
                    ttt = tt.next0_
                    if (ttt.is_char('.') and (ttt.next0_.whitespaces_after_count < 3)): 
                        ttt = ttt.next0_
                    cits = CityItemToken.try_parse_list(ttt, None, 3)
                    if (cits is not None and len(cits) == 1 and ((cits[0].typ == CityItemToken.ItemType.PROPERNAME or cits[0].typ == CityItemToken.ItemType.CITY))): 
                        if (tt.chars.is_all_upper and not cits[0].chars.is_all_upper): 
                            pass
                        else: 
                            return True
                continue
            if (tt.is_value("ТЕРРИТОРИЯ", "ТЕРИТОРІЯ")): 
                continue
            rt = Utils.asObjectOrNull(tt, ReferentToken)
            if (rt is None): 
                if (not dont_check_city): 
                    cits = CityItemToken.try_parse_list(tt, None, 3)
                    if ((cits is not None and len(cits) == 2 and cits[0].typ == CityItemToken.ItemType.NOUN) and ((cits[1].typ == CityItemToken.ItemType.PROPERNAME or cits[1].typ == CityItemToken.ItemType.CITY))): 
                        if (cits[0].chars.is_all_upper and not cits[1].chars.is_all_upper): 
                            pass
                        else: 
                            return True
                if ((isinstance(tt, TextToken)) and tt.length_char > 2 and cou == 0): 
                    cou += 1
                    continue
                else: 
                    break
            if ((isinstance(rt.referent, GeoReferent)) or (isinstance(rt.referent, AddressReferent)) or (isinstance(rt.referent, StreetReferent))): 
                return True
            break
        return False
    
    @staticmethod
    def check_near_before(t : 'Token') -> 'Token':
        if (t is None or not t.morph.class0_.is_preposition): 
            return None
        if (t.is_value("У", None) or t.is_value("ОКОЛО", None) or t.is_value("ВБЛИЗИ", None)): 
            return t
        if (t.is_value("ОТ", None) and t.previous is not None): 
            if (t.previous.is_value("НЕДАЛЕКО", None) or t.previous.is_value("ВБЛИЗИ", None) or t.previous.is_value("НЕПОДАЛЕКУ", None)): 
                return t.previous
        return None
    
    @staticmethod
    def check_unknown_region(t : 'Token') -> 'Token':
        """ Проверка, что здесь какой-то непонятный регион типа "Европа", "Средняя Азия", "Дикий запад" и т.п.
        
        Args:
            t(Token): 
        
        """
        from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken
        if (not (isinstance(t, TextToken))): 
            return None
        npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0, None)
        if (npt is None): 
            return None
        if (TerrItemToken._m_unknown_regions.try_parse(npt.end_token, TerminParseAttr.FULLWORDSONLY) is not None): 
            return npt.end_token
        return None
    
    @staticmethod
    def get_std_adj_full(t : 'Token', gen : 'MorphGender', num : 'MorphNumber', strict : bool) -> typing.List[str]:
        if (not (isinstance(t, TextToken))): 
            return None
        return MiscLocationHelper.get_std_adj_full_str(t.term, gen, num, strict)
    
    @staticmethod
    def get_std_adj_full_str(v : str, gen : 'MorphGender', num : 'MorphNumber', strict : bool) -> typing.List[str]:
        res = list()
        if (v.startswith("Б")): 
            if (num == MorphNumber.PLURAL): 
                res.append("БОЛЬШИЕ")
                return res
            if (not strict and ((num) & (MorphNumber.PLURAL)) != (MorphNumber.UNDEFINED)): 
                res.append("БОЛЬШИЕ")
            if (((gen) & (MorphGender.FEMINIE)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.FEMINIE): 
                    res.append("БОЛЬШАЯ")
            if (((gen) & (MorphGender.MASCULINE)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.MASCULINE): 
                    res.append("БОЛЬШОЙ")
            if (((gen) & (MorphGender.NEUTER)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.NEUTER): 
                    res.append("БОЛЬШОЕ")
            if (len(res) > 0): 
                return res
            return None
        if (v.startswith("М")): 
            if (num == MorphNumber.PLURAL): 
                res.append("МАЛЫЕ")
                return res
            if (not strict and ((num) & (MorphNumber.PLURAL)) != (MorphNumber.UNDEFINED)): 
                res.append("МАЛЫЕ")
            if (((gen) & (MorphGender.FEMINIE)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.FEMINIE): 
                    res.append("МАЛАЯ")
            if (((gen) & (MorphGender.MASCULINE)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.MASCULINE): 
                    res.append("МАЛЫЙ")
            if (((gen) & (MorphGender.NEUTER)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.NEUTER): 
                    res.append("МАЛОЕ")
            if (len(res) > 0): 
                return res
            return None
        if (v.startswith("В")): 
            if (num == MorphNumber.PLURAL): 
                res.append("ВЕРХНИЕ")
                return res
            if (not strict and ((num) & (MorphNumber.PLURAL)) != (MorphNumber.UNDEFINED)): 
                res.append("ВЕРХНИЕ")
            if (((gen) & (MorphGender.FEMINIE)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.FEMINIE): 
                    res.append("ВЕРХНЯЯ")
            if (((gen) & (MorphGender.MASCULINE)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.MASCULINE): 
                    res.append("ВЕРХНИЙ")
            if (((gen) & (MorphGender.NEUTER)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.NEUTER): 
                    res.append("ВЕРХНЕЕ")
            if (len(res) > 0): 
                return res
            return None
        if (v == "Н"): 
            r1 = MiscLocationHelper.get_std_adj_full_str("НОВ", gen, num, strict)
            r2 = MiscLocationHelper.get_std_adj_full_str("НИЖ", gen, num, strict)
            if (r1 is None and r2 is None): 
                return None
            if (r1 is None): 
                return r2
            if (r2 is None): 
                return r1
            r1.insert(1, r2[0])
            del r2[0]
            r1.extend(r2)
            return r1
        if (v == "С" or v == "C"): 
            r1 = MiscLocationHelper.get_std_adj_full_str("СТ", gen, num, strict)
            r2 = MiscLocationHelper.get_std_adj_full_str("СР", gen, num, strict)
            if (r1 is None and r2 is None): 
                return None
            if (r1 is None): 
                return r2
            if (r2 is None): 
                return r1
            r1.insert(1, r2[0])
            del r2[0]
            r1.extend(r2)
            return r1
        if (v.startswith("НОВ")): 
            if (num == MorphNumber.PLURAL): 
                res.append("НОВЫЕ")
                return res
            if (not strict and ((num) & (MorphNumber.PLURAL)) != (MorphNumber.UNDEFINED)): 
                res.append("НОВЫЕ")
            if (((gen) & (MorphGender.FEMINIE)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.FEMINIE): 
                    res.append("НОВАЯ")
            if (((gen) & (MorphGender.MASCULINE)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.MASCULINE): 
                    res.append("НОВЫЙ")
            if (((gen) & (MorphGender.NEUTER)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.NEUTER): 
                    res.append("НОВОЕ")
            if (len(res) > 0): 
                return res
            return None
        if (v.startswith("НИЖ")): 
            if (num == MorphNumber.PLURAL): 
                res.append("НИЖНИЕ")
                return res
            if (not strict and ((num) & (MorphNumber.PLURAL)) != (MorphNumber.UNDEFINED)): 
                res.append("НИЖНИЕ")
            if (((gen) & (MorphGender.FEMINIE)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.FEMINIE): 
                    res.append("НИЖНЯЯ")
            if (((gen) & (MorphGender.MASCULINE)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.MASCULINE): 
                    res.append("НИЖНИЙ")
            if (((gen) & (MorphGender.NEUTER)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.NEUTER): 
                    res.append("НИЖНЕЕ")
            if (len(res) > 0): 
                return res
            return None
        if (v.startswith("СТ")): 
            if (num == MorphNumber.PLURAL): 
                res.append("СТАРЫЕ")
                return res
            if (not strict and ((num) & (MorphNumber.PLURAL)) != (MorphNumber.UNDEFINED)): 
                res.append("СТАРЫЕ")
            if (((gen) & (MorphGender.FEMINIE)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.FEMINIE): 
                    res.append("СТАРАЯ")
            if (((gen) & (MorphGender.MASCULINE)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.MASCULINE): 
                    res.append("СТАРЫЙ")
            if (((gen) & (MorphGender.NEUTER)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.NEUTER): 
                    res.append("СТАРОЕ")
            if (len(res) > 0): 
                return res
            return None
        if (v.startswith("СР")): 
            if (num == MorphNumber.PLURAL): 
                res.append("СРЕДНИЕ")
                return res
            if (not strict and ((num) & (MorphNumber.PLURAL)) != (MorphNumber.UNDEFINED)): 
                res.append("СРЕДНИЕ")
            if (((gen) & (MorphGender.FEMINIE)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.FEMINIE): 
                    res.append("СРЕДНЯЯ")
            if (((gen) & (MorphGender.MASCULINE)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.MASCULINE): 
                    res.append("СРЕДНИЙ")
            if (((gen) & (MorphGender.NEUTER)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.NEUTER): 
                    res.append("СРЕДНЕЕ")
            if (len(res) > 0): 
                return res
            return None
        return None
    
    @staticmethod
    def get_geo_referent_by_name(name : str) -> 'GeoReferent':
        """ Прлучить глобальный экземпляр существующего объекта по ALPHA2 или краткой текстовой форме (РФ, РОССИЯ, КИТАЙ ...)
        
        Args:
            name(str): 
        
        """
        from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken
        res = None
        wrapres1168 = RefOutArgWrapper(None)
        inoutres1169 = Utils.tryGetValue(MiscLocationHelper.__m_geo_ref_by_name, name, wrapres1168)
        res = wrapres1168.value
        if (inoutres1169): 
            return res
        for r in TerrItemToken._m_all_states: 
            if (r.find_slot(None, name, True) is not None): 
                res = (Utils.asObjectOrNull(r, GeoReferent))
                break
        MiscLocationHelper.__m_geo_ref_by_name[name] = res
        return res
    
    __m_geo_ref_by_name = None
    
    @staticmethod
    def try_attach_nord_west(t : 'Token') -> 'MetaToken':
        """ Выделение существительных и прилагательных типа "северо-западное", "южное"
        
        Args:
            t(Token): 
        
        """
        if (not (isinstance(t, TextToken))): 
            return None
        tok = MiscLocationHelper.__m_nords.try_parse(t, TerminParseAttr.NO)
        if (tok is None): 
            return None
        res = MetaToken._new509(t, t, t.morph)
        t1 = None
        if ((t.next0_ is not None and t.next0_.is_hiphen and not t.is_whitespace_after) and not t.is_whitespace_after): 
            t1 = t.next0_.next0_
        elif (t.morph.class0_.is_adjective and (t.whitespaces_after_count < 2)): 
            t1 = t.next0_
        if (t1 is not None): 
            tok = MiscLocationHelper.__m_nords.try_parse(t1, TerminParseAttr.NO)
            if ((tok) is not None): 
                res.end_token = tok.end_token
                res.morph = tok.morph
        return res
    
    @staticmethod
    def _initialize() -> None:
        if (MiscLocationHelper.__m_nords is not None): 
            return
        MiscLocationHelper.__m_nords = TerminCollection()
        for s in ["СЕВЕРНЫЙ", "ЮЖНЫЙ", "ЗАПАДНЫЙ", "ВОСТОЧНЫЙ", "ЦЕНТРАЛЬНЫЙ", "БЛИЖНИЙ", "ДАЛЬНИЙ", "СРЕДНИЙ", "СЕВЕР", "ЮГ", "ЗАПАД", "ВОСТОК", "СЕВЕРО", "ЮГО", "ЗАПАДНО", "ВОСТОЧНО", "СЕВЕРОЗАПАДНЫЙ", "СЕВЕРОВОСТОЧНЫЙ", "ЮГОЗАПАДНЫЙ", "ЮГОВОСТОЧНЫЙ"]: 
            MiscLocationHelper.__m_nords.add(Termin(s, MorphLang.RU, True))
        table = "\nAF\tAFG\nAX\tALA\nAL\tALB\nDZ\tDZA\nAS\tASM\nAD\tAND\nAO\tAGO\nAI\tAIA\nAQ\tATA\nAG\tATG\nAR\tARG\nAM\tARM\nAW\tABW\nAU\tAUS\nAT\tAUT\nAZ\tAZE\nBS\tBHS\nBH\tBHR\nBD\tBGD\nBB\tBRB\nBY\tBLR\nBE\tBEL\nBZ\tBLZ\nBJ\tBEN\nBM\tBMU\nBT\tBTN\nBO\tBOL\nBA\tBIH\nBW\tBWA\nBV\tBVT\nBR\tBRA\nVG\tVGB\nIO\tIOT\nBN\tBRN\nBG\tBGR\nBF\tBFA\nBI\tBDI\nKH\tKHM\nCM\tCMR\nCA\tCAN\nCV\tCPV\nKY\tCYM\nCF\tCAF\nTD\tTCD\nCL\tCHL\nCN\tCHN\nHK\tHKG\nMO\tMAC\nCX\tCXR\nCC\tCCK\nCO\tCOL\nKM\tCOM\nCG\tCOG\nCD\tCOD\nCK\tCOK\nCR\tCRI\nCI\tCIV\nHR\tHRV\nCU\tCUB\nCY\tCYP\nCZ\tCZE\nDK\tDNK\nDJ\tDJI\nDM\tDMA\nDO\tDOM\nEC\tECU\nEG\tEGY\nSV\tSLV\nGQ\tGNQ\nER\tERI\nEE\tEST\nET\tETH\nFK\tFLK\nFO\tFRO\nFJ\tFJI\nFI\tFIN\nFR\tFRA\nGF\tGUF\nPF\tPYF\nTF\tATF\nGA\tGAB\nGM\tGMB\nGE\tGEO\nDE\tDEU\nGH\tGHA\nGI\tGIB\nGR\tGRC\nGL\tGRL\nGD\tGRD\nGP\tGLP\nGU\tGUM\nGT\tGTM\nGG\tGGY\nGN\tGIN\nGW\tGNB\nGY\tGUY\nHT\tHTI\nHM\tHMD\nVA\tVAT\nHN\tHND\nHU\tHUN\nIS\tISL\nIN\tIND\nID\tIDN\nIR\tIRN\nIQ\tIRQ\nIE\tIRL\nIM\tIMN\nIL\tISR\nIT\tITA\nJM\tJAM\nJP\tJPN\nJE\tJEY\nJO\tJOR\nKZ\tKAZ\nKE\tKEN\nKI\tKIR\nKP\tPRK\nKR\tKOR\nKW\tKWT\nKG\tKGZ\nLA\tLAO\nLV\tLVA\nLB\tLBN\nLS\tLSO\nLR\tLBR\nLY\tLBY\nLI\tLIE\nLT\tLTU\nLU\tLUX\nMK\tMKD\nMG\tMDG\nMW\tMWI\nMY\tMYS\nMV\tMDV\nML\tMLI\nMT\tMLT\nMH\tMHL\nMQ\tMTQ\nMR\tMRT\nMU\tMUS\nYT\tMYT\nMX\tMEX\nFM\tFSM\nMD\tMDA\nMC\tMCO\nMN\tMNG\nME\tMNE\nMS\tMSR\nMA\tMAR\nMZ\tMOZ\nMM\tMMR\nNA\tNAM\nNR\tNRU\nNP\tNPL\nNL\tNLD\nAN\tANT\nNC\tNCL\nNZ\tNZL\nNI\tNIC\nNE\tNER\nNG\tNGA\nNU\tNIU\nNF\tNFK\nMP\tMNP\nNO\tNOR\nOM\tOMN\nPK\tPAK\nPW\tPLW\nPS\tPSE\nPA\tPAN\nPG\tPNG\nPY\tPRY\nPE\tPER\nPH\tPHL\nPN\tPCN\nPL\tPOL\nPT\tPRT\nPR\tPRI\nQA\tQAT\nRE\tREU\nRO\tROU\nRU\tRUS\nRW\tRWA\nBL\tBLM\nSH\tSHN\nKN\tKNA\nLC\tLCA\nMF\tMAF\nPM\tSPM\nVC\tVCT\nWS\tWSM\nSM\tSMR\nST\tSTP\nSA\tSAU\nSN\tSEN\nRS\tSRB\nSC\tSYC\nSL\tSLE\nSG\tSGP\nSK\tSVK\nSI\tSVN\nSB\tSLB\nSO\tSOM\nZA\tZAF\nGS\tSGS\nSS\tSSD\nES\tESP\nLK\tLKA\nSD\tSDN\nSR\tSUR\nSJ\tSJM\nSZ\tSWZ\nSE\tSWE\nCH\tCHE\nSY\tSYR\nTW\tTWN\nTJ\tTJK\nTZ\tTZA\nTH\tTHA\nTL\tTLS\nTG\tTGO\nTK\tTKL\nTO\tTON\nTT\tTTO\nTN\tTUN\nTR\tTUR\nTM\tTKM\nTC\tTCA\nTV\tTUV\nUG\tUGA\nUA\tUKR\nAE\tARE\nGB\tGBR\nUS\tUSA\nUM\tUMI\nUY\tURY\nUZ\tUZB\nVU\tVUT\nVE\tVEN\nVN\tVNM\nVI\tVIR\nWF\tWLF\nEH\tESH\nYE\tYEM\nZM\tZMB\nZW\tZWE "
        for s in Utils.splitString(table, '\n', False): 
            ss = s.strip()
            if ((len(ss) < 6) or not Utils.isWhitespace(ss[2])): 
                continue
            cod2 = ss[0:0+2]
            cod3 = ss[3:].strip()
            if (len(cod3) != 3): 
                continue
            if (not cod2 in MiscLocationHelper._m_alpha2_3): 
                MiscLocationHelper._m_alpha2_3[cod2] = cod3
            if (not cod3 in MiscLocationHelper._m_alpha3_2): 
                MiscLocationHelper._m_alpha3_2[cod3] = cod2
    
    __m_nords = None
    
    _m_alpha2_3 = None
    
    _m_alpha3_2 = None
    
    @staticmethod
    def _deflate(zip0_ : bytearray) -> bytearray:
        with io.BytesIO() as unzip: 
            data = io.BytesIO(zip0_)
            data.seek(0, io.SEEK_SET)
            MorphDeserializer.deflate_gzip(data, unzip)
            data.close()
            return bytearray(unzip.getvalue())
    
    # static constructor for class MiscLocationHelper
    @staticmethod
    def _static_ctor():
        MiscLocationHelper.__m_geo_ref_by_name = dict()
        MiscLocationHelper._m_alpha2_3 = dict()
        MiscLocationHelper._m_alpha3_2 = dict()

MiscLocationHelper._static_ctor()