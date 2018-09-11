# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import io
import xml.etree
import typing
import math
from pullenti.unisharp.Utils import Utils
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner._org.internal.ResourceHelper import ResourceHelper
from pullenti.ner._org.OrgProfile import OrgProfile
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.internal.MorphSerializeHelper import MorphSerializeHelper
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner._org.OrganizationReferent import OrganizationReferent
from pullenti.ner._org.OrganizationKind import OrganizationKind
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.core.TerminParseAttr import TerminParseAttr


class OrgItemTypeToken(MetaToken):
    
    __m_global = None
    
    __m_bank = None
    
    __m_mo = None
    
    __m_ispr_kolon = None
    
    __m_sber_bank = None
    
    __m_akcion_comp = None
    
    __m_sovm_pred = None
    
    _m_pref_words = None
    
    _m_key_words_for_refs = None
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.core.IntOntologyCollection import IntOntologyCollection
        from pullenti.ner.core.Termin import Termin
        from pullenti.ner._org.internal.OrgItemTermin import OrgItemTermin
        from pullenti.morph.MorphLang import MorphLang
        from pullenti.morph.Morphology import Morphology
        from pullenti.morph.MorphBaseInfo import MorphBaseInfo
        from pullenti.morph.MorphClass import MorphClass
        from pullenti.ner.core.TerminCollection import TerminCollection
        if (OrgItemTypeToken.__m_global is not None): 
            return
        OrgItemTypeToken.__m_global = IntOntologyCollection()
        Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = True
        tdat = ResourceHelper.get_bytes("OrgTypes.dat")
        if (tdat is None): 
            raise Utils.newException("Can't file resource file OrgTypes.dat in Organization analyzer", None)
        tdat = OrgItemTypeToken._deflate(tdat)
        with io.BytesIO(tdat) as tmp: 
            tmp.seek(0, io.SEEK_SET)
            xml0_ = None # new XmlDocument
            xml0_ = xml.etree.ElementTree.parse(tmp)
            set0_ = None
            for x in xml0_.getroot(): 
                its = OrgItemTermin.deserialize_src(x, set0_)
                if (x.tag == "set"): 
                    set0_ = (None)
                    if (its is not None and len(its) > 0): 
                        set0_ = its[0]
                elif (its is not None): 
                    for ii in its: 
                        OrgItemTypeToken.__m_global.add(ii)
        sovs = ["СОВЕТ БЕЗОПАСНОСТИ", "НАЦИОНАЛЬНЫЙ СОВЕТ", "ГОСУДАРСТВЕННЫЙ СОВЕТ", "ОБЛАСТНОЙ СОВЕТ", "РАЙОННЫЙ СОВЕТ", "ГОРОДСКОЙ СОВЕТ", "СЕЛЬСКИЙ СОВЕТ", "КРАЕВОЙ СОВЕТ", "СЛЕДСТВЕННЫЙ КОМИТЕТ", "СЛЕДСТВЕННОЕ УПРАВЛЕНИЕ", "ГОСУДАРСТВЕННОЕ СОБРАНИЕ", "МУНИЦИПАЛЬНОЕ СОБРАНИЕ", "ГОРОДСКОЕ СОБРАНИЕ", "ЗАКОНОДАТЕЛЬНОЕ СОБРАНИЕ", "НАРОДНОЕ СОБРАНИЕ", "ОБЛАСТНАЯ ДУМА", "ГОРОДСКАЯ ДУМА", "КРАЕВАЯ ДУМА", "КАБИНЕТ МИНИСТРОВ"]
        sov2 = ["СОВБЕЗ", "НАЦСОВЕТ", "ГОССОВЕТ", "ОБЛСОВЕТ", "РАЙСОВЕТ", "ГОРСОВЕТ", "СЕЛЬСОВЕТ", "КРАЙСОВЕТ", None, None, "ГОССОБРАНИЕ", "МУНСОБРАНИЕ", "ГОРСОБРАНИЕ", "ЗАКСОБРАНИЕ", "НАРСОБРАНИЕ", "ОБЛДУМА", "ГОРДУМА", "КРАЙДУМА", "КАБМИН"]
        i = 0
        while i < len(sovs): 
            t = OrgItemTermin._new1702(sovs[i], MorphLang.RU, OrgProfile.STATE, 4, OrgItemTermin.Types.ORG, True, True)
            if (sov2[i] is not None): 
                t.add_variant(sov2[i], False)
                if (sov2[i] == "ГОССОВЕТ" or sov2[i] == "НАЦСОВЕТ" or sov2[i] == "ЗАКСОБРАНИЕ"): 
                    t.coeff = (5)
            OrgItemTypeToken.__m_global.add(t)
            i += 1
        sovs = ["РАДА БЕЗПЕКИ", "НАЦІОНАЛЬНА РАДА", "ДЕРЖАВНА РАДА", "ОБЛАСНА РАДА", "РАЙОННА РАДА", "МІСЬКА РАДА", "СІЛЬСЬКА РАДА", "КРАЙОВИЙ РАДА", "СЛІДЧИЙ КОМІТЕТ", "СЛІДЧЕ УПРАВЛІННЯ", "ДЕРЖАВНІ ЗБОРИ", "МУНІЦИПАЛЬНЕ ЗБОРИ", "МІСЬКЕ ЗБОРИ", "ЗАКОНОДАВЧІ ЗБОРИ", "НАРОДНІ ЗБОРИ", "ОБЛАСНА ДУМА", "МІСЬКА ДУМА", "КРАЙОВА ДУМА", "КАБІНЕТ МІНІСТРІВ"]
        sov2 = ["РАДБЕЗ", None, None, "ОБЛРАДА", "РАЙРАДА", "МІСЬКРАДА", "СІЛЬРАДА", "КРАЙРАДА", None, None, "ДЕРЖЗБОРИ", "МУНЗБОРИ", "ГОРСОБРАНИЕ", "ЗАКЗБОРИ", "НАРСОБРАНИЕ", "ОБЛДУМА", "МІСЬКДУМА", "КРАЙДУМА", "КАБМІН"]
        i = 0
        while i < len(sovs): 
            t = OrgItemTermin._new1702(sovs[i], MorphLang.UA, OrgProfile.STATE, 4, OrgItemTermin.Types.ORG, True, True)
            if (sov2[i] is not None): 
                t.add_variant(sov2[i], False)
            if (sov2[i] == "ГОССОВЕТ" or sov2[i] == "ЗАКЗБОРИ"): 
                t.coeff = (5)
            OrgItemTypeToken.__m_global.add(t)
            i += 1
        sovs = ["SECURITY COUNCIL", "NATIONAL COUNCIL", "STATE COUNCIL", "REGIONAL COUNCIL", "DISTRICT COUNCIL", "CITY COUNCIL", "RURAL COUNCIL", "INVESTIGATIVE COMMITTEE", "INVESTIGATION DEPARTMENT", "NATIONAL ASSEMBLY", "MUNICIPAL ASSEMBLY", "URBAN ASSEMBLY", "LEGISLATURE"]
        i = 0
        while i < len(sovs): 
            t = OrgItemTermin._new1702(sovs[i], MorphLang.EN, OrgProfile.STATE, 4, OrgItemTermin.Types.ORG, True, True)
            OrgItemTypeToken.__m_global.add(t)
            i += 1
        t = OrgItemTermin._new1705("ГОСУДАРСТВЕННЫЙ КОМИТЕТ", OrgItemTermin.Types.ORG, OrgProfile.STATE, 2)
        t.add_variant("ГОСКОМИТЕТ", False)
        t.add_variant("ГОСКОМ", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1706("ДЕРЖАВНИЙ КОМІТЕТ", MorphLang.UA, OrgItemTermin.Types.ORG, OrgProfile.STATE, 2)
        t.add_variant("ДЕРЖКОМІТЕТ", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1707("КРАЕВОЙ КОМИТЕТ ГОСУДАРСТВЕННОЙ СТАТИСТИКИ", OrgItemTermin.Types.DEP, OrgProfile.STATE, 3, True)
        t.add_variant("КРАЙКОМСТАТ", False)
        t._profile = OrgProfile.UNIT
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1707("ОБЛАСТНОЙ КОМИТЕТ ГОСУДАРСТВЕННОЙ СТАТИСТИКИ", OrgItemTermin.Types.DEP, OrgProfile.STATE, 3, True)
        t.add_variant("ОБЛКОМСТАТ", False)
        t._profile = OrgProfile.UNIT
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1707("РАЙОННЫЙ КОМИТЕТ ГОСУДАРСТВЕННОЙ СТАТИСТИКИ", OrgItemTermin.Types.DEP, OrgProfile.STATE, 3, True)
        t.add_variant("РАЙКОМСТАТ", False)
        t._profile = OrgProfile.UNIT
        OrgItemTypeToken.__m_global.add(t)
        sovs = ["ЦЕНТРАЛЬНЫЙ КОМИТЕТ", "РАЙОННЫЙ КОМИТЕТ", "ГОРОДСКОЙ КОМИТЕТ", "КРАЕВОЙ КОМИТЕТ", "ОБЛАСТНОЙ КОМИТЕТ", "ПОЛИТИЧЕСКОЕ БЮРО"]
        sov2 = ["ЦК", "РАЙКОМ", "ГОРКОМ", "КРАЙКОМ", "ОБКОМ", "ПОЛИТБЮРО"]
        i = 0
        while i < len(sovs): 
            t = OrgItemTermin._new1710(sovs[i], 2, OrgItemTermin.Types.DEP, OrgProfile.UNIT)
            if (i == 0): 
                t.acronym = "ЦК"
                t.can_be_normal_dep = True
            elif (sov2[i] is not None): 
                t.add_variant(sov2[i], False)
            OrgItemTypeToken.__m_global.add(t)
            i += 1
        for s in ["Standing Committee", "Political Bureau", "Central Committee"]: 
            OrgItemTypeToken.__m_global.add(OrgItemTermin._new1711(s.upper(), 3, OrgItemTermin.Types.DEP, OrgProfile.UNIT, True))
        sovs = ["ЦЕНТРАЛЬНИЙ КОМІТЕТ", "РАЙОННИЙ КОМІТЕТ", "МІСЬКИЙ КОМІТЕТ", "КРАЙОВИЙ КОМІТЕТ", "ОБЛАСНИЙ КОМІТЕТ"]
        i = 0
        while i < len(sovs): 
            t = OrgItemTermin._new1712(sovs[i], MorphLang.UA, 2, OrgItemTermin.Types.DEP, OrgProfile.UNIT)
            if (i == 0): 
                t.acronym = "ЦК"
                t.can_be_normal_dep = True
            elif (sov2[i] is not None): 
                t.add_variant(sov2[i], False)
            OrgItemTypeToken.__m_global.add(t)
            i += 1
        t = OrgItemTermin._new1713("КАЗНАЧЕЙСТВО", 3, OrgItemTermin.Types.ORG, True)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1714("КАЗНАЧЕЙСТВО", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1713("TREASURY", 3, OrgItemTermin.Types.ORG, True)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1716("ГОСУДАРСТВЕННЫЙ ДЕПАРТАМЕНТ", 5, OrgItemTermin.Types.ORG, True, True)
        t.add_variant("ГОСДЕПАРТАМЕНТ", False)
        t.add_variant("ГОСДЕП", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1716("DEPARTMENT OF STATE", 5, OrgItemTermin.Types.ORG, True, True)
        t.add_variant("STATE DEPARTMENT", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1718("ДЕРЖАВНИЙ ДЕПАРТАМЕНТ", MorphLang.UA, 5, OrgItemTermin.Types.ORG, True, True)
        t.add_variant("ДЕРЖДЕПАРТАМЕНТ", False)
        t.add_variant("ДЕРЖДЕП", False)
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1719("ДЕПАРТАМЕНТ", 2, OrgItemTermin.Types.ORG))
        t = OrgItemTermin._new1719("DEPARTMENT", 2, OrgItemTermin.Types.ORG)
        t.add_abridge("DEPT.")
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1721("АГЕНТСТВО", 1, OrgItemTermin.Types.ORG, True)
        t.add_variant("АГЕНСТВО", False)
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1721("ADGENCY", 1, OrgItemTermin.Types.ORG, True))
        t = OrgItemTermin._new1710("АКАДЕМИЯ", 3, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION)
        t.profiles.append(OrgProfile.SCIENCE)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1724("АКАДЕМІЯ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION)
        t.profiles.append(OrgProfile.SCIENCE)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1710("ACADEMY", 3, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION)
        t.profiles.append(OrgProfile.SCIENCE)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1726("ГЕНЕРАЛЬНЫЙ ШТАБ", 3, OrgItemTermin.Types.DEP, True, True, OrgProfile.ARMY)
        t.add_variant("ГЕНЕРАЛЬНИЙ ШТАБ", False)
        t.add_variant("ГЕНШТАБ", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1726("GENERAL STAFF", 3, OrgItemTermin.Types.DEP, True, True, OrgProfile.ARMY)
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1728("ФРОНТ", 3, OrgItemTermin.Types.ORG, True, True, OrgProfile.ARMY))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1729("ВОЕННЫЙ ОКРУГ", 3, OrgItemTermin.Types.ORG, True, OrgProfile.ARMY))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1730("ВІЙСЬКОВИЙ ОКРУГ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, OrgProfile.ARMY))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1728("ГРУППА АРМИЙ", 3, OrgItemTermin.Types.ORG, True, True, OrgProfile.ARMY))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1732("ГРУПА АРМІЙ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, True, OrgProfile.ARMY))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1728("АРМИЯ", 3, OrgItemTermin.Types.ORG, True, True, OrgProfile.ARMY))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1732("АРМІЯ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, True, OrgProfile.ARMY))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1728("ARMY", 3, OrgItemTermin.Types.ORG, True, True, OrgProfile.ARMY))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1729("ГВАРДИЯ", 3, OrgItemTermin.Types.ORG, True, OrgProfile.ARMY))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1730("ГВАРДІЯ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, OrgProfile.ARMY))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1729("GUARD", 3, OrgItemTermin.Types.ORG, True, OrgProfile.ARMY))
        t = OrgItemTermin._new1739("ВОЙСКОВАЯ ЧАСТЬ", 3, "ВЧ", OrgItemTermin.Types.ORG, True, OrgProfile.ARMY)
        OrgItemTypeToken.__m_military_unit = t
        t.add_abridge("В.Ч.")
        t.add_variant("ВОИНСКАЯ ЧАСТЬ", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1740("ВІЙСЬКОВА ЧАСТИНА", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True)
        t.add_abridge("В.Ч.")
        OrgItemTypeToken.__m_global.add(t)
        for s in ["ДИВИЗИЯ", "ДИВИЗИОН", "ПОЛК", "БАТАЛЬОН", "РОТА", "ВЗВОД", "АВИАДИВИЗИЯ", "АВИАПОЛК", "ПОГРАНПОЛК", "АРТБРИГАДА", "МОТОМЕХБРИГАДА", "ТАНКОВЫЙ КОРПУС", "ГАРНИЗОН"]: 
            t = OrgItemTermin._new1741(s, 3, OrgItemTermin.Types.ORG, True, OrgProfile.ARMY)
            if (s == "ГАРНИЗОН"): 
                t.can_be_single_geo = True
            OrgItemTypeToken.__m_global.add(t)
        for s in ["ДИВІЗІЯ", "ДИВІЗІОН", "ПОЛК", "БАТАЛЬЙОН", "РОТА", "ВЗВОД", "АВІАДИВІЗІЯ", "АВІАПОЛК", "ПОГРАНПОЛК", "АРТБРИГАДА", "МОТОМЕХБРИГАДА", "ТАНКОВИЙ КОРПУС", "ГАРНІЗОН"]: 
            t = OrgItemTermin._new1742(s, 3, MorphLang.UA, OrgItemTermin.Types.ORG, True, OrgProfile.ARMY)
            if (s == "ГАРНІЗОН"): 
                t.can_be_single_geo = True
            OrgItemTypeToken.__m_global.add(t)
        for s in ["КОРПУС", "БРИГАДА"]: 
            t = OrgItemTermin._new1741(s, 1, OrgItemTermin.Types.ORG, True, OrgProfile.ARMY)
            OrgItemTypeToken.__m_global.add(t)
        for s in ["КОРПУС", "БРИГАДА"]: 
            t = OrgItemTermin._new1742(s, 1, MorphLang.UA, OrgItemTermin.Types.ORG, True, OrgProfile.ARMY)
            OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1710("ГОСУДАРСТВЕННЫЙ УНИВЕРСИТЕТ", 3, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1724("ДЕРЖАВНИЙ УНІВЕРСИТЕТ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1710("STATE UNIVERSITY", 3, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1710("УНИВЕРСИТЕТ", 3, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1724("УНІВЕРСИТЕТ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1750("UNIVERSITY", 3, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1751("УЧРЕЖДЕНИЕ", 1, OrgItemTermin.Types.ORG, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1752("УСТАНОВА", MorphLang.UA, 1, OrgItemTermin.Types.ORG, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1751("INSTITUTION", 1, OrgItemTermin.Types.ORG, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1719("ГОСУДАРСТВЕННОЕ УЧРЕЖДЕНИЕ", 3, OrgItemTermin.Types.ORG))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1755("ДЕРЖАВНА УСТАНОВА", MorphLang.UA, 3, OrgItemTermin.Types.ORG))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1713("STATE INSTITUTION", 3, OrgItemTermin.Types.ORG, True))
        t = OrgItemTermin._new1710("ИНСТИТУТ", 2, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION)
        t.profiles.append(OrgProfile.SCIENCE)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1724("ІНСТИТУТ", MorphLang.UA, 2, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION)
        t.profiles.append(OrgProfile.SCIENCE)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1710("INSTITUTE", 2, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION)
        t.profiles.append(OrgProfile.SCIENCE)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1760("ОТДЕЛ СУДЕБНЫХ ПРИСТАВОВ", OrgItemTermin.Types.PREFIX, "ОСП", OrgProfile.UNIT, True, True)
        t.profiles.append(OrgProfile.JUSTICE)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1760("МЕЖРАЙОННЫЙ ОТДЕЛ СУДЕБНЫХ ПРИСТАВОВ", OrgItemTermin.Types.PREFIX, "МОСП", OrgProfile.UNIT, True, True)
        t.add_variant("МЕЖРАЙОННЫЙ ОСП", False)
        t.profiles.append(OrgProfile.JUSTICE)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1760("ОТДЕЛ ВНЕВЕДОМСТВЕННОЙ ОХРАНЫ", OrgItemTermin.Types.PREFIX, "ОВО", OrgProfile.UNIT, True, True)
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1763("ЛИЦЕЙ", 2, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1764("ЛІЦЕЙ", MorphLang.UA, 2, OrgProfile.EDUCATION, OrgItemTermin.Types.ORG, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1763("ИНТЕРНАТ", 3, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1764("ІНТЕРНАТ", MorphLang.UA, 3, OrgProfile.EDUCATION, OrgItemTermin.Types.ORG, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1767("HIGH SCHOOL", 3, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1767("SECONDARY SCHOOL", 3, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1767("MIDDLE SCHOOL", 3, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1767("PUBLIC SCHOOL", 3, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1767("JUNIOR SCHOOL", 3, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1767("GRAMMAR SCHOOL", 3, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION, True, True))
        t = OrgItemTermin._new1773("СРЕДНЯЯ ШКОЛА", 3, "СОШ", OrgItemTermin.Types.ORG, OrgProfile.EDUCATION, True)
        t.add_variant("СРЕДНЯЯ ОБРАЗОВАТЕЛЬНАЯ ШКОЛА", False)
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1774("БИЗНЕС ШКОЛА", 3, OrgItemTermin.Types.ORG, True, True, True, True, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1774("БІЗНЕС ШКОЛА", 3, OrgItemTermin.Types.ORG, True, True, True, True, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1764("СЕРЕДНЯ ШКОЛА", MorphLang.UA, 3, OrgProfile.EDUCATION, OrgItemTermin.Types.ORG, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1710("ВЫСШАЯ ШКОЛА", 3, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1724("ВИЩА ШКОЛА", MorphLang.UA, 3, OrgItemTermin.Types.ORG, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1741("НАЧАЛЬНАЯ ШКОЛА", 3, OrgItemTermin.Types.ORG, True, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1780("ПОЧАТКОВА ШКОЛА", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1741("СЕМИНАРИЯ", 3, OrgItemTermin.Types.ORG, True, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1780("СЕМІНАРІЯ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1741("ГИМНАЗИЯ", 3, OrgItemTermin.Types.ORG, True, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1780("ГІМНАЗІЯ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, OrgProfile.EDUCATION))
        t = OrgItemTermin._new1741("ДЕТСКИЙ САД", 3, OrgItemTermin.Types.ORG, True, OrgProfile.EDUCATION)
        t.add_variant("ДЕТСАД", False)
        t.add_abridge("Д.С.")
        t.add_abridge("Д/С")
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1780("ДИТЯЧИЙ САДОК", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, OrgProfile.EDUCATION)
        t.add_variant("ДИТСАДОК", False)
        t.add_abridge("Д.С.")
        t.add_abridge("Д/З")
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1741("ШКОЛА", 1, OrgItemTermin.Types.ORG, True, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1788("SCHOOL", 3, OrgItemTermin.Types.ORG, True, OrgProfile.EDUCATION, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1741("УЧИЛИЩЕ", 2, OrgItemTermin.Types.ORG, True, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1741("КОЛЛЕДЖ", 2, OrgItemTermin.Types.ORG, True, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1788("COLLEGE", 3, OrgItemTermin.Types.ORG, True, OrgProfile.EDUCATION, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1792("ЦЕНТР", OrgItemTermin.Types.ORG, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1710("НАУЧНЫЙ ЦЕНТР", 3, OrgItemTermin.Types.ORG, OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1724("НАУКОВИЙ ЦЕНТР", MorphLang.UA, 3, OrgItemTermin.Types.ORG, OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1741("БОЛЬНИЦА", 2, OrgItemTermin.Types.ORG, True, OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1780("ЛІКАРНЯ", MorphLang.UA, 2, OrgItemTermin.Types.ORG, True, OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1741("МОРГ", 3, OrgItemTermin.Types.ORG, True, OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1780("МОРГ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1741("ХОСПИС", 3, OrgItemTermin.Types.ORG, True, OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1780("ХОСПІС", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, OrgProfile.MEDICINE))
        t = OrgItemTermin._new1741("ГОРОДСКАЯ БОЛЬНИЦА", 3, OrgItemTermin.Types.ORG, True, OrgProfile.MEDICINE)
        t.add_abridge("ГОР.БОЛЬНИЦА")
        t.add_variant("ГОРБОЛЬНИЦА", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1780("МІСЬКА ЛІКАРНЯ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, OrgProfile.MEDICINE)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1803("ГОРОДСКАЯ КЛИНИЧЕСКАЯ БОЛЬНИЦА", 3, OrgItemTermin.Types.ORG, True, "ГКБ", OrgProfile.MEDICINE)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1804("МІСЬКА КЛІНІЧНА ЛІКАРНЯ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, "МКЛ", OrgProfile.MEDICINE)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1805("КЛАДБИЩЕ", 3, OrgItemTermin.Types.ORG, True)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1740("КЛАДОВИЩЕ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True)
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1741("ПОЛИКЛИНИКА", 2, OrgItemTermin.Types.ORG, True, OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1780("ПОЛІКЛІНІКА", MorphLang.UA, 2, OrgItemTermin.Types.ORG, True, OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1741("ГОСПИТАЛЬ", 2, OrgItemTermin.Types.ORG, True, OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1780("ГОСПІТАЛЬ", MorphLang.UA, 2, OrgItemTermin.Types.ORG, True, OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1741("КЛИНИКА", 1, OrgItemTermin.Types.ORG, True, OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1780("КЛІНІКА", MorphLang.UA, 1, OrgItemTermin.Types.ORG, True, OrgProfile.MEDICINE))
        t = OrgItemTermin._new1741("МЕДИКО САНИТАРНАЯ ЧАСТЬ", 2, OrgItemTermin.Types.ORG, True, OrgProfile.MEDICINE)
        t.add_variant("МЕДСАНЧАСТЬ", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1780("МЕДИКО САНІТАРНА ЧАСТИНА", MorphLang.UA, 2, OrgItemTermin.Types.ORG, True, OrgProfile.MEDICINE)
        t.add_variant("МЕДСАНЧАСТИНА", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1815("МЕДИЦИНСКИЙ ЦЕНТР", 2, OrgItemTermin.Types.ORG, True, True, True, OrgProfile.MEDICINE)
        t.add_variant("МЕДЦЕНТР", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1816("МЕДИЧНИЙ ЦЕНТР", MorphLang.UA, 2, OrgItemTermin.Types.ORG, True, True, True, OrgProfile.MEDICINE)
        t.add_variant("МЕДЦЕНТР", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1741("РОДИЛЬНЫЙ ДОМ", 1, OrgItemTermin.Types.ORG, True, OrgProfile.MEDICINE)
        t.add_variant("РОДДОМ", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1780("ПОЛОГОВИЙ БУДИНОК", MorphLang.UA, 1, OrgItemTermin.Types.ORG, True, OrgProfile.MEDICINE)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1819("АЭРОПОРТ", 3, OrgItemTermin.Types.ORG, True, True, True, True)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1820("АЕРОПОРТ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, True, True, True)
        OrgItemTypeToken.__m_global.add(t)
        for s in ["ТЕАТР", "ТЕАТР-СТУДИЯ", "КИНОТЕАТР", "МУЗЕЙ", "ГАЛЕРЕЯ", "КОНЦЕРТНЫЙ ЗАЛ", "ФИЛАРМОНИЯ", "КОНСЕРВАТОРИЯ", "ДОМ КУЛЬТУРЫ", "ДВОРЕЦ КУЛЬТУРЫ", "ДВОРЕЦ ПИОНЕРОВ"]: 
            OrgItemTypeToken.__m_global.add(OrgItemTermin._new1721(s, 3, OrgItemTermin.Types.ORG, True))
        for s in ["ТЕАТР", "ТЕАТР-СТУДІЯ", "КІНОТЕАТР", "МУЗЕЙ", "ГАЛЕРЕЯ", "КОНЦЕРТНИЙ ЗАЛ", "ФІЛАРМОНІЯ", "КОНСЕРВАТОРІЯ", "БУДИНОК КУЛЬТУРИ", "ПАЛАЦ КУЛЬТУРИ", "ПАЛАЦ ПІОНЕРІВ"]: 
            OrgItemTypeToken.__m_global.add(OrgItemTermin._new1822(s, MorphLang.UA, 3, OrgItemTermin.Types.ORG, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1823("БИБЛИОТЕКА", 3, OrgItemTermin.Types.ORG, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1824("БІБЛІОТЕКА", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, True))
        for s in ["ЦЕРКОВЬ", "ХРАМ", "СОБОР", "МЕЧЕТЬ", "СИНАГОГА", "МОНАСТЫРЬ", "ЛАВРА"]: 
            OrgItemTypeToken.__m_global.add(OrgItemTermin._new1825(s, 3, OrgItemTermin.Types.ORG, True, True))
        for s in ["ЦЕРКВА", "ХРАМ", "СОБОР", "МЕЧЕТЬ", "СИНАГОГА", "МОНАСТИР", "ЛАВРА"]: 
            OrgItemTypeToken.__m_global.add(OrgItemTermin._new1826(s, MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, True))
        for s in ["ФЕДЕРАЛЬНАЯ СЛУЖБА", "ГОСУДАРСТВЕННАЯ СЛУЖБА", "ФЕДЕРАЛЬНОЕ УПРАВЛЕНИЕ", "ГОСУДАРСТВЕННЫЙ КОМИТЕТ", "ГОСУДАРСТВЕННАЯ ИНСПЕКЦИЯ"]: 
            t = OrgItemTermin._new1827(s, 3, OrgItemTermin.Types.ORG, True)
            OrgItemTypeToken.__m_global.add(t)
            t = OrgItemTermin._new1828(s, 3, OrgItemTermin.Types.ORG, s)
            t.terms.insert(1, Termin.Term._new1829(None, True))
            OrgItemTypeToken.__m_global.add(t)
        for s in ["ФЕДЕРАЛЬНА СЛУЖБА", "ДЕРЖАВНА СЛУЖБА", "ФЕДЕРАЛЬНЕ УПРАВЛІННЯ", "ДЕРЖАВНИЙ КОМІТЕТ УКРАЇНИ", "ДЕРЖАВНА ІНСПЕКЦІЯ"]: 
            t = OrgItemTermin._new1830(s, MorphLang.UA, 3, OrgItemTermin.Types.ORG, True)
            OrgItemTypeToken.__m_global.add(t)
            t = OrgItemTermin._new1831(s, MorphLang.UA, 3, OrgItemTermin.Types.ORG, s)
            t.terms.insert(1, Termin.Term._new1829(None, True))
            OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1805("СЛЕДСТВЕННЫЙ ИЗОЛЯТОР", 5, OrgItemTermin.Types.ORG, True)
        t.add_variant("СИЗО", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1740("СЛІДЧИЙ ІЗОЛЯТОР", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True)
        t.add_variant("СІЗО", False)
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1805("КОЛОНИЯ-ПОСЕЛЕНИЕ", 3, OrgItemTermin.Types.ORG, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1740("КОЛОНІЯ-ПОСЕЛЕННЯ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1837("ТЮРЬМА", 3, OrgItemTermin.Types.ORG, True, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1838("ВЯЗНИЦЯ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1805("КОЛОНИЯ", 2, OrgItemTermin.Types.ORG, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1740("КОЛОНІЯ", MorphLang.UA, 2, OrgItemTermin.Types.ORG, True))
        OrgItemTypeToken.__m_ispr_kolon = OrgItemTermin._new1841("ИСПРАВИТЕЛЬНАЯ КОЛОНИЯ", 3, OrgItemTermin.Types.ORG, "ИК", True)
        OrgItemTypeToken.__m_global.add(OrgItemTypeToken.__m_ispr_kolon)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1740("ВИПРАВНА КОЛОНІЯ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True))
        for s in ["ПОЛИЦИЯ", "МИЛИЦИЯ"]: 
            t = OrgItemTermin._new1843(s, OrgItemTermin.Types.ORG, 3, True, False)
            OrgItemTypeToken.__m_global.add(t)
        for s in ["ПОЛІЦІЯ", "МІЛІЦІЯ"]: 
            t = OrgItemTermin._new1844(s, MorphLang.UA, OrgItemTermin.Types.ORG, 3, True, False)
            OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1845("ПАЕВЫЙ ИНВЕСТИЦИОННЫЙ ФОНД", 2, OrgItemTermin.Types.ORG, "ПИФ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1846("РОССИЙСКОЕ ИНФОРМАЦИОННОЕ АГЕНТСТВО", 3, OrgItemTermin.Types.ORG, "РИА", OrgProfile.MEDIA))
        t = OrgItemTermin._new1846("ИНФОРМАЦИОННОЕ АГЕНТСТВО", 3, OrgItemTermin.Types.ORG, "ИА", OrgProfile.MEDIA)
        t.add_variant("ИНФОРМАГЕНТСТВО", False)
        t.add_variant("ИНФОРМАГЕНСТВО", False)
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1751("ОТДЕЛ", 1, OrgItemTermin.Types.DEP, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1849("ВІДДІЛ", MorphLang.UA, 1, OrgItemTermin.Types.DEP, True))
        t = OrgItemTermin._new1719("ФАКУЛЬТЕТ", 3, OrgItemTermin.Types.DEP)
        t.add_abridge("ФАК.")
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1719("КАФЕДРА", 3, OrgItemTermin.Types.DEP)
        t.add_abridge("КАФ.")
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1719("ЛАБОРАТОРИЯ", 1, OrgItemTermin.Types.DEP)
        t.add_abridge("ЛАБ.")
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1853("ЛАБОРАТОРІЯ", MorphLang.UA, 1, OrgItemTermin.Types.DEP)
        t.add_abridge("ЛАБ.")
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1729("ПАТРИАРХИЯ", 3, OrgItemTermin.Types.DEP, True, OrgProfile.RELIGION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1729("ПАТРІАРХІЯ", 3, OrgItemTermin.Types.DEP, True, OrgProfile.RELIGION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1729("ЕПАРХИЯ", 3, OrgItemTermin.Types.DEP, True, OrgProfile.RELIGION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1729("ЄПАРХІЯ", 3, OrgItemTermin.Types.DEP, True, OrgProfile.RELIGION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1858("ПРЕДСТАВИТЕЛЬСТВО", OrgItemTermin.Types.DEPADD))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1859("ПРЕДСТАВНИЦТВО", MorphLang.UA, OrgItemTermin.Types.DEPADD))
        t = OrgItemTermin._new1792("ОТДЕЛЕНИЕ", OrgItemTermin.Types.DEPADD, True)
        t.add_abridge("ОТД.")
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1861("ВІДДІЛЕННЯ", MorphLang.UA, OrgItemTermin.Types.DEPADD, True)
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1792("ИНСПЕКЦИЯ", OrgItemTermin.Types.DEPADD, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1861("ІНСПЕКЦІЯ", MorphLang.UA, OrgItemTermin.Types.DEPADD, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1858("ФИЛИАЛ", OrgItemTermin.Types.DEPADD))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1859("ФІЛІЯ", MorphLang.UA, OrgItemTermin.Types.DEPADD))
        for s in ["ОТДЕЛ ПОЛИЦИИ", "ОТДЕЛ МИЛИЦИИ", "ОТДЕЛЕНИЕ ПОЛИЦИИ", "ОТДЕЛЕНИЕ МИЛИЦИИ"]: 
            OrgItemTypeToken.__m_global.add(OrgItemTermin._new1866(s, OrgItemTermin.Types.DEP, 1.5, True, True))
            if (s.startswith("ОТДЕЛ ")): 
                t = OrgItemTermin._new1866("ГОРОДСКОЙ " + s, OrgItemTermin.Types.DEP, 3, True, True)
                t.add_variant("ГОР" + s, False)
                OrgItemTypeToken.__m_global.add(t)
                t = OrgItemTermin._new1866("РАЙОННЫЙ " + s, OrgItemTermin.Types.DEP, 3, True, True)
                t.add_variant("РАЙ" + s, False)
                OrgItemTypeToken.__m_global.add(t)
        for s in ["ВІДДІЛ ПОЛІЦІЇ", "ВІДДІЛ МІЛІЦІЇ", "ВІДДІЛЕННЯ ПОЛІЦІЇ", "ВІДДІЛЕННЯ МІЛІЦІЇ"]: 
            OrgItemTypeToken.__m_global.add(OrgItemTermin._new1869(s, MorphLang.UA, OrgItemTermin.Types.DEP, 1.5, True, True))
        t = OrgItemTermin._new1870("ГЛАВНОЕ УПРАВЛЕНИЕ", "ГУ", OrgItemTermin.Types.DEPADD, True)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1871("ГОЛОВНЕ УПРАВЛІННЯ", MorphLang.UA, "ГУ", OrgItemTermin.Types.DEPADD, True)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1870("ГЛАВНОЕ ТЕРРИТОРИАЛЬНОЕ УПРАВЛЕНИЕ", "ГТУ", OrgItemTermin.Types.DEPADD, True)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1871("ГОЛОВНЕ ТЕРИТОРІАЛЬНЕ УПРАВЛІННЯ", MorphLang.UA, "ГТУ", OrgItemTermin.Types.DEPADD, True)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1870("ОПЕРАЦИОННОЕ УПРАВЛЕНИЕ", "ОПЕРУ", OrgItemTermin.Types.DEPADD, True)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1871("ОПЕРАЦІЙНЕ УПРАВЛІННЯ", MorphLang.UA, "ОПЕРУ", OrgItemTermin.Types.DEPADD, True)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1876("ТЕРРИТОРИАЛЬНОЕ УПРАВЛЕНИЕ", OrgItemTermin.Types.DEPADD, True)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1877("ТЕРИТОРІАЛЬНЕ УПРАВЛІННЯ", MorphLang.UA, OrgItemTermin.Types.DEPADD, True)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1792("УПРАВЛЕНИЕ", OrgItemTermin.Types.DEPADD, True)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1861("УПРАВЛІННЯ", MorphLang.UA, OrgItemTermin.Types.DEPADD, True)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1870("ПОГРАНИЧНОЕ УПРАВЛЕНИЕ", "ПУ", OrgItemTermin.Types.DEPADD, True)
        OrgItemTypeToken.__m_global.add(t)
        for s in ["ПРЕСС-СЛУЖБА", "ПРЕСС-ЦЕНТР", "КОЛЛ-ЦЕНТР", "БУХГАЛТЕРИЯ", "МАГИСТРАТУРА", "АСПИРАНТУРА", "ДОКТОРАНТУРА", "ОРДИНАТУРА", "СОВЕТ ДИРЕКТОРОВ", "УЧЕНЫЙ СОВЕТ", "КОЛЛЕГИЯ", "ПЛЕНУМ", "АППАРАТ", "НАБЛЮДАТЕЛЬНЫЙ СОВЕТ", "ОБЩЕСТВЕННЫЙ СОВЕТ", "РУКОВОДСТВО", "ДИРЕКЦИЯ", "ПРАВЛЕНИЕ", "ЖЮРИ", "ПРЕЗИДИУМ", "СЕКРЕТАРИАТ", "PRESS", "PRESS CENTER", "CLIENT CENTER", "CALL CENTER", "ACCOUNTING", "MASTER DEGREE", "POSTGRADUATE", "DOCTORATE", "RESIDENCY", "BOARD OF DIRECTORS", "DIRECTOR BOARD", "ACADEMIC COUNCIL", "BOARD", "PLENARY", "UNIT", "SUPERVISORY BOARD", "PUBLIC COUNCIL", "LEADERSHIP", "MANAGEMENT", "JURY", "BUREAU", "SECRETARIAT"]: 
            OrgItemTypeToken.__m_global.add(OrgItemTermin._new1881(s, OrgItemTermin.Types.DEPADD, True, OrgProfile.UNIT))
        for s in ["ПРЕС-СЛУЖБА", "ПРЕС-ЦЕНТР", "БУХГАЛТЕРІЯ", "МАГІСТРАТУРА", "АСПІРАНТУРА", "ДОКТОРАНТУРА", "ОРДИНАТУРА", "РАДА ДИРЕКТОРІВ", "ВЧЕНА РАДА", "КОЛЕГІЯ", "ПЛЕНУМ", "АПАРАТ", "НАГЛЯДОВА РАДА", "ГРОМАДСЬКА РАДА", "КЕРІВНИЦТВО", "ДИРЕКЦІЯ", "ПРАВЛІННЯ", "ЖУРІ", "ПРЕЗИДІЯ", "СЕКРЕТАРІАТ"]: 
            OrgItemTypeToken.__m_global.add(OrgItemTermin._new1882(s, MorphLang.UA, OrgItemTermin.Types.DEPADD, True, OrgProfile.UNIT))
        t = OrgItemTermin._new1881("ОТДЕЛ ИНФОРМАЦИОННОЙ БЕЗОПАСНОСТИ", OrgItemTermin.Types.DEPADD, True, OrgProfile.UNIT)
        t.add_variant("ОТДЕЛ ИБ", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1881("ОТДЕЛ ИНФОРМАЦИОННЫХ ТЕХНОЛОГИЙ", OrgItemTermin.Types.DEPADD, True, OrgProfile.UNIT)
        t.add_variant("ОТДЕЛ ИТ", False)
        t.add_variant("ОТДЕЛ IT", False)
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1792("СЕКТОР", OrgItemTermin.Types.DEP, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1886("КУРС", OrgItemTermin.Types.DEP, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1887("ГРУППА", OrgItemTermin.Types.DEP, True, True, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1888("ГРУПА", MorphLang.UA, OrgItemTermin.Types.DEP, True, True, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1881("ДНЕВНОЕ ОТДЕЛЕНИЕ", OrgItemTermin.Types.DEP, True, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1882("ДЕННЕ ВІДДІЛЕННЯ", MorphLang.UA, OrgItemTermin.Types.DEP, True, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1881("ВЕЧЕРНЕЕ ОТДЕЛЕНИЕ", OrgItemTermin.Types.DEP, True, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1882("ВЕЧІРНЄ ВІДДІЛЕННЯ", MorphLang.UA, OrgItemTermin.Types.DEP, True, OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1876("ДЕЖУРНАЯ ЧАСТЬ", OrgItemTermin.Types.DEP, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1877("ЧЕРГОВА ЧАСТИНА", MorphLang.UA, OrgItemTermin.Types.DEP, True))
        t = OrgItemTermin._new1895("ПАСПОРТНЫЙ СТОЛ", OrgItemTermin.Types.DEP, True)
        t.add_abridge("П/С")
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1896("ПАСПОРТНИЙ СТІЛ", MorphLang.UA, OrgItemTermin.Types.DEP, True)
        t.add_abridge("П/С")
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1897("ВЫСШЕЕ УЧЕБНОЕ ЗАВЕДЕНИЕ", OrgItemTermin.Types.PREFIX, OrgProfile.EDUCATION, "ВУЗ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1898("ВИЩИЙ НАВЧАЛЬНИЙ ЗАКЛАД", MorphLang.UA, OrgItemTermin.Types.PREFIX, OrgProfile.EDUCATION, "ВНЗ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1897("ВЫСШЕЕ ПРОФЕССИОНАЛЬНОЕ УЧИЛИЩЕ", OrgItemTermin.Types.PREFIX, OrgProfile.EDUCATION, "ВПУ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1898("ВИЩЕ ПРОФЕСІЙНЕ УЧИЛИЩЕ", MorphLang.UA, OrgItemTermin.Types.PREFIX, OrgProfile.EDUCATION, "ВПУ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1897("НАУЧНО ИССЛЕДОВАТЕЛЬСКИЙ ИНСТИТУТ", OrgItemTermin.Types.PREFIX, OrgProfile.SCIENCE, "НИИ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1898("НАУКОВО ДОСЛІДНИЙ ІНСТИТУТ", MorphLang.UA, OrgItemTermin.Types.PREFIX, OrgProfile.SCIENCE, "НДІ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1903("НАУЧНО ИССЛЕДОВАТЕЛЬСКИЙ ЦЕНТР", OrgItemTermin.Types.PREFIX, "НИЦ", OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1904("НАУКОВО ДОСЛІДНИЙ ЦЕНТР", MorphLang.UA, OrgItemTermin.Types.PREFIX, "НДЦ", OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1903("ЦЕНТРАЛЬНЫЙ НАУЧНО ИССЛЕДОВАТЕЛЬСКИЙ ИНСТИТУТ", OrgItemTermin.Types.PREFIX, "ЦНИИ", OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1903("ВСЕРОССИЙСКИЙ НАУЧНО ИССЛЕДОВАТЕЛЬСКИЙ ИНСТИТУТ", OrgItemTermin.Types.PREFIX, "ВНИИ", OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1903("РОССИЙСКИЙ НАУЧНО ИССЛЕДОВАТЕЛЬСКИЙ ИНСТИТУТ", OrgItemTermin.Types.PREFIX, "РНИИ", OrgProfile.SCIENCE))
        t = OrgItemTermin._new1908("ИННОВАЦИОННЫЙ ЦЕНТР", OrgItemTermin.Types.PREFIX, OrgProfile.SCIENCE)
        t.add_variant("ИННОЦЕНТР", False)
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1903("НАУЧНО ТЕХНИЧЕСКИЙ ЦЕНТР", OrgItemTermin.Types.PREFIX, "НТЦ", OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1904("НАУКОВО ТЕХНІЧНИЙ ЦЕНТР", MorphLang.UA, OrgItemTermin.Types.PREFIX, "НТЦ", OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1903("НАУЧНО ТЕХНИЧЕСКАЯ ФИРМА", OrgItemTermin.Types.PREFIX, "НТФ", OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1904("НАУКОВО ВИРОБНИЧА ФІРМА", MorphLang.UA, OrgItemTermin.Types.PREFIX, "НВФ", OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1903("НАУЧНО ПРОИЗВОДСТВЕННОЕ ОБЪЕДИНЕНИЕ", OrgItemTermin.Types.PREFIX, "НПО", OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1904("НАУКОВО ВИРОБНИЧЕ ОБЄДНАННЯ", MorphLang.UA, OrgItemTermin.Types.PREFIX, "НВО", OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1908("НАУЧНО ПРОИЗВОДСТВЕННЫЙ КООПЕРАТИВ", OrgItemTermin.Types.PREFIX, OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1904("НАУКОВО-ВИРОБНИЧИЙ КООПЕРАТИВ", MorphLang.UA, OrgItemTermin.Types.PREFIX, "НВК", OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1903("НАУЧНО ПРОИЗВОДСТВЕННАЯ КОРПОРАЦИЯ", OrgItemTermin.Types.PREFIX, "НПК", OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1903("НАУЧНО ТЕХНИЧЕСКИЙ КОМПЛЕКС", OrgItemTermin.Types.PREFIX, "НТК", OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1903("МЕЖОТРАСЛЕВОЙ НАУЧНО ТЕХНИЧЕСКИЙ КОМПЛЕКС", OrgItemTermin.Types.PREFIX, "МНТК", OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1903("НАУЧНО ПРОИЗВОДСТВЕННОЕ ПРЕДПРИЯТИЕ", OrgItemTermin.Types.PREFIX, "НПП", OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1904("НАУКОВО ВИРОБНИЧЕ ПІДПРИЄМСТВО", MorphLang.UA, OrgItemTermin.Types.PREFIX, "НВП", OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1903("НАУЧНО ПРОИЗВОДСТВЕННЫЙ ЦЕНТР", OrgItemTermin.Types.PREFIX, "НПЦ", OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1904("НАУКОВО ВИРОБНИЧЕ ЦЕНТР", MorphLang.UA, OrgItemTermin.Types.PREFIX, "НВЦ", OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1903("НАУЧНО ПРОИЗВОДСТВЕННОЕ УНИТАРНОЕ ПРЕДПРИЯТИЕ", OrgItemTermin.Types.PREFIX, "НПУП", OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1925("ЧАСТНОЕ ПРЕДПРИЯТИЕ", OrgItemTermin.Types.PREFIX, "ЧП"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1926("ПРИВАТНЕ ПІДПРИЄМСТВО", MorphLang.UA, OrgItemTermin.Types.PREFIX, "ПП"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1925("ЧАСТНОЕ УНИТАРНОЕ ПРЕДПРИЯТИЕ", OrgItemTermin.Types.PREFIX, "ЧУП"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1925("ЧАСТНОЕ ПРОИЗВОДСТВЕННОЕ УНИТАРНОЕ ПРЕДПРИЯТИЕ", OrgItemTermin.Types.PREFIX, "ЧПУП"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1925("ЧАСТНОЕ ИНДИВИДУАЛЬНОЕ ПРЕДПРИЯТИЕ", OrgItemTermin.Types.PREFIX, "ЧИП"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1925("ЧАСТНОЕ ОХРАННОЕ ПРЕДПРИЯТИЕ", OrgItemTermin.Types.PREFIX, "ЧОП"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1925("ЧАСТНАЯ ОХРАННАЯ ОРГАНИЗАЦИЯ", OrgItemTermin.Types.PREFIX, "ЧОО"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1925("ЧАСТНОЕ ТРАНСПОРТНОЕ УНИТАРНОЕ ПРЕДПРИЯТИЕ", OrgItemTermin.Types.PREFIX, "ЧТУП"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1925("ЧАСТНОЕ ТРАНСПОРТНО ЭКСПЛУАТАЦИОННОЕ УНИТАРНОЕ ПРЕДПРИЯТИЕ", OrgItemTermin.Types.PREFIX, "ЧТЭУП"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1925("НАУЧНО ПРОИЗВОДСТВЕННОЕ КОРПОРАЦИЯ", OrgItemTermin.Types.PREFIX, "НПК"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1925("ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ УНИТАРНОЕ ПРЕДПРИЯТИЕ", OrgItemTermin.Types.PREFIX, "ФГУП"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1925("ГОСУДАРСТВЕННОЕ УНИТАРНОЕ ПРЕДПРИЯТИЕ", OrgItemTermin.Types.PREFIX, "ГУП"))
        t = OrgItemTermin._new1925("ГОСУДАРСТВЕННОЕ ПРЕДПРИЯТИЕ", OrgItemTermin.Types.PREFIX, "ГП")
        t.add_variant("ГОСПРЕДПРИЯТИЕ", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1926("ДЕРЖАВНЕ ПІДПРИЄМСТВО", MorphLang.UA, OrgItemTermin.Types.PREFIX, "ДП")
        t.add_variant("ДЕРЖПІДПРИЄМСТВО", False)
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1903("ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ НАУЧНОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "ФГНУ", OrgProfile.SCIENCE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1925("ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "ФГУ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1925("ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ УЧРЕЖДЕНИЕ КУЛЬТУРЫ", OrgItemTermin.Types.PREFIX, "ФГУК"))
        t = OrgItemTermin._new1925("ЧАСТНОЕ УЧРЕЖДЕНИЕ КУЛЬТУРЫ", OrgItemTermin.Types.PREFIX, "ЧУК")
        t.add_variant("ЧАСТНОЕ УЧРЕЖДЕНИЕ КУЛЬТУРЫ ЛФП", False)
        t.add_variant("ЧУК ЛФП", False)
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1925("ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ КАЗЕННОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "ФГКУ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1925("ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ КАЗЕННОЕ ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "ФГКОУ"))
        t = OrgItemTermin._new1925("ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "ФГБУ")
        t.add_variant("ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ УЧРЕЖДЕНИЕ НАУКИ", False)
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1925("ВОЕННО ПРОМЫШЛЕННАЯ КОРПОРАЦИЯ", OrgItemTermin.Types.PREFIX, "ВПК"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1925("ФЕДЕРАЛЬНОЕ БЮДЖЕТНОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "ФБУ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1925("ФЕДЕРАЛЬНОЕ УНИТАРНОЕ ПРЕДПРИЯТИЕ", OrgItemTermin.Types.PREFIX, "ФУП"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1925("ФЕДЕРАЛЬНОЕ КАЗЕННОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "ФКУ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1925("МУНИЦИПАЛЬНОЕ НЕКОММЕРЧЕСКОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "МНУ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1925("МУНИЦИПАЛЬНОЕ БЮДЖЕТНОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "МБУ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1925("МУНИЦИПАЛЬНОЕ АВТОНОМНОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "МАУ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1925("МУНИЦИПАЛЬНОЕ КАЗЕННОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "МКУ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1925("МУНИЦИПАЛЬНОЕ УНИТАРНОЕ ПРЕДПРИЯТИЕ", OrgItemTermin.Types.PREFIX, "МУП"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1925("МУНИЦИПАЛЬНОЕ УНИТАРНОЕ ПРОИЗВОДСТВЕННОЕ ПРЕДПРИЯТИЕ", OrgItemTermin.Types.PREFIX, "МУПП"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1925("МУНИЦИПАЛЬНОЕ КАЗЕННОЕ ПРЕДПРИЯТИЕ", OrgItemTermin.Types.PREFIX, "МКП"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1925("МУНИЦИПАЛЬНОЕ ПРЕДПРИЯТИЕ", OrgItemTermin.Types.PREFIX, "МП"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1925("НЕБАНКОВСКАЯ КРЕДИТНАЯ ОРГАНИЗАЦИЯ", OrgItemTermin.Types.PREFIX, "НКО"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1925("РАСЧЕТНАЯ НЕБАНКОВСКАЯ КРЕДИТНАЯ ОРГАНИЗАЦИЯ", OrgItemTermin.Types.PREFIX, "РНКО"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1925("ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "ГБУ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1925("ГОСУДАРСТВЕННОЕ КАЗЕННОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "ГКУ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1925("ГОСУДАРСТВЕННОЕ АВТОНОМНОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "ГАУ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1858("МАЛОЕ ИННОВАЦИОННОЕ ПРЕДПРИЯТИЕ", OrgItemTermin.Types.PREFIX))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1925("НЕГОСУДАРСТВЕННЫЙ ПЕНСИОННЫЙ ФОНД", OrgItemTermin.Types.PREFIX, "НПФ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1926("ДЕРЖАВНА АКЦІОНЕРНА КОМПАНІЯ", MorphLang.UA, OrgItemTermin.Types.PREFIX, "ДАК"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1926("ДЕРЖАВНА КОМПАНІЯ", MorphLang.UA, OrgItemTermin.Types.PREFIX, "ДК"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1926("КОЛЕКТИВНЕ ПІДПРИЄМСТВО", MorphLang.UA, OrgItemTermin.Types.PREFIX, "КП"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1926("КОЛЕКТИВНЕ МАЛЕ ПІДПРИЄМСТВО", MorphLang.UA, OrgItemTermin.Types.PREFIX, "КМП"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1926("ВИРОБНИЧА ФІРМА", MorphLang.UA, OrgItemTermin.Types.PREFIX, "ВФ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1926("ВИРОБНИЧЕ ОБЄДНАННЯ", MorphLang.UA, OrgItemTermin.Types.PREFIX, "ВО"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1926("ВИРОБНИЧЕ ПІДПРИЄМСТВО", MorphLang.UA, OrgItemTermin.Types.PREFIX, "ВП"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1926("ВИРОБНИЧИЙ КООПЕРАТИВ", MorphLang.UA, OrgItemTermin.Types.PREFIX, "ВК"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1926("СТРАХОВА КОМПАНІЯ", MorphLang.UA, OrgItemTermin.Types.PREFIX, "СК"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1926("ТВОРЧЕ ОБЄДНАННЯ", MorphLang.UA, OrgItemTermin.Types.PREFIX, "ТО"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1903("ГОСУДАРСТВЕННОЕ УЧРЕЖДЕНИЕ ЗДРАВООХРАНЕНИЯ", OrgItemTermin.Types.PREFIX, "ГУЗ", OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1903("ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ УЧРЕЖДЕНИЕ ЗДРАВООХРАНЕНИЯ", OrgItemTermin.Types.PREFIX, "ФГУЗ", OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1903("ФЕДЕРАЛЬНОЕ КАЗЕННОЕ УЧРЕЖДЕНИЕ ЗДРАВООХРАНЕНИЯ", OrgItemTermin.Types.PREFIX, "ФКУЗ", OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1903("ГОСУДАРСТВЕННОЕ АВТОНОМНОЕ УЧРЕЖДЕНИЕ ЗДРАВООХРАНЕНИЯ", OrgItemTermin.Types.PREFIX, "ГАУЗ", OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1903("ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ УЧРЕЖДЕНИЕ ЗДРАВООХРАНЕНИЯ", OrgItemTermin.Types.PREFIX, "ГБУЗ", OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1903("ГОСУДАРСТВЕННОЕ ОБЛАСТНОЕ БЮДЖЕТНОЕ УЧРЕЖДЕНИЕ ЗДРАВООХРАНЕНИЯ", OrgItemTermin.Types.PREFIX, "ГОБУЗ", OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1903("ГОСУДАРСТВЕННОЕ КАЗЕННОЕ УЧРЕЖДЕНИЕ ЗДРАВООХРАНЕНИЯ", OrgItemTermin.Types.PREFIX, "ГКУЗ", OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1903("ГОСУДАРСТВЕННОЕ ОБЛАСТНОЕ КАЗЕННОЕ УЧРЕЖДЕНИЕ ЗДРАВООХРАНЕНИЯ", OrgItemTermin.Types.PREFIX, "ГОКУЗ", OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1903("МУНИЦИПАЛЬНОЕ УЧРЕЖДЕНИЕ ЗДРАВООХРАНЕНИЯ", OrgItemTermin.Types.PREFIX, "МУЗ", OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1903("НЕГОСУДАРСТВЕННОЕ УЧРЕЖДЕНИЕ ЗДРАВООХРАНЕНИЯ", OrgItemTermin.Types.PREFIX, "НУЗ", OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1903("МУНИЦИПАЛЬНОЕ БЮДЖЕТНОЕ УЧРЕЖДЕНИЕ ЗДРАВООХРАНЕНИЯ", OrgItemTermin.Types.PREFIX, "МБУЗ", OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1903("МУНИЦИПАЛЬНОЕ ОБЛАСТНОЕ БЮДЖЕТНОЕ УЧРЕЖДЕНИЕ ЗДРАВООХРАНЕНИЯ", OrgItemTermin.Types.PREFIX, "МОБУЗ", OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1903("МУНИЦИПАЛЬНОЕ АВТОНОМНОЕ УЧРЕЖДЕНИЕ ЗДРАВООХРАНЕНИЯ", OrgItemTermin.Types.PREFIX, "МАУЗ", OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1903("ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ УЧРЕЖДЕНИЕ ОБРАЗОВАНИЯ", OrgItemTermin.Types.PREFIX, "ГБУО", OrgProfile.EDUCATION))
        t = OrgItemTermin._new1903("ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ ПРФЕСИОНАЛЬНОЕ ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "ГБПОУ", OrgProfile.EDUCATION)
        t.add_variant("ГБ ПОУ", True)
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1903("ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ ОБЩЕОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "ГБОУ", OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1903("ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ УЧРЕЖДЕНИЕ ДОПОЛНИТЕЛЬНОГО ОБРАЗОВАНИЯ", OrgItemTermin.Types.PREFIX, "ГБУДО", OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1903("МУНИЦИПАЛЬНОЕ ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "МОУ", OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1903("МУНИЦИПАЛЬНОЕ КАЗЕННОЕ ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "МКОУ", OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1903("МУНИЦИПАЛЬНОЕ ЛЕЧЕБНО ПРОФИЛАКТИЧЕСКОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "МЛПУ", OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1903("ФЕДЕРАЛЬНОЕ КАЗЕННОЕ ЛЕЧЕБНО ПРОФИЛАКТИЧЕСКОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "ФКЛПУ", OrgProfile.MEDICINE))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1903("ГОСУДАРСТВЕННОЕ ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "ГОУ", OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1903("ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "ГБОУ", OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1903("ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ", OrgItemTermin.Types.PREFIX, "ФГБОУ", OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1903("ВЫСШЕЕ ПРОФЕССИОНАЛЬНОЕ ОБРАЗОВАНИЕ", OrgItemTermin.Types.PREFIX, "ВПО", OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1903("ДОПОЛНИТЕЛЬНОЕ ПРОФЕССИОНАЛЬНОЕ ОБРАЗОВАНИЕ", OrgItemTermin.Types.PREFIX, "ДПО", OrgProfile.EDUCATION))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2001("ДЕПАРТАМЕНТ ЕДИНОГО ЗАКАЗЧИКА", OrgItemTermin.Types.PREFIX, "ДЕЗ", True, True))
        t = OrgItemTermin._new2002("СОЮЗ АРБИТРАЖНЫХ УПРАВЛЯЮЩИХ", OrgItemTermin.Types.PREFIX, "САУ", True)
        t.add_variant("САМОРЕГУЛИРУЕМАЯ ОРГАНИЗАЦИЯ АРБИТРАЖНЫХ УПРАВЛЯЮЩИХ", False)
        t.add_variant("СОАУ", False)
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2003("АКЦИОНЕРНОЕ ОБЩЕСТВО", OrgItemTermin.Types.PREFIX, True, "АО"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2004("АКЦІОНЕРНЕ ТОВАРИСТВО", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, "АТ"))
        OrgItemTypeToken.__m_sovm_pred = OrgItemTermin._new2003("СОВМЕСТНОЕ ПРЕДПРИЯТИЕ", OrgItemTermin.Types.PREFIX, True, "СП")
        OrgItemTypeToken.__m_global.add(OrgItemTypeToken.__m_sovm_pred)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2004("СПІЛЬНЕ ПІДПРИЄМСТВО", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, "СП"))
        OrgItemTypeToken.__m_akcion_comp = OrgItemTermin._new2007("АКЦИОНЕРНАЯ КОМПАНИЯ", OrgItemTermin.Types.PREFIX, True)
        OrgItemTypeToken.__m_global.add(OrgItemTypeToken.__m_akcion_comp)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2003("ЗАКРЫТОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО", OrgItemTermin.Types.PREFIX, True, "ЗАО"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2009("РОССИЙСКОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО", OrgItemTermin.Types.PREFIX, True, "РАО", "PAO"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2003("РОССИЙСКОЕ ОТКРЫТОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО", OrgItemTermin.Types.PREFIX, True, "РОАО"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2003("АКЦИОНЕРНОЕ ОБЩЕСТВО ЗАКРЫТОГО ТИПА", OrgItemTermin.Types.PREFIX, True, "АОЗТ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2004("АКЦІОНЕРНЕ ТОВАРИСТВО ЗАКРИТОГО ТИПУ", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, "АТЗТ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2003("АКЦИОНЕРНОЕ ОБЩЕСТВО ОТКРЫТОГО ТИПА", OrgItemTermin.Types.PREFIX, True, "АООТ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2004("АКЦІОНЕРНЕ ТОВАРИСТВО ВІДКРИТОГО ТИПУ", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, "АТВТ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2003("ОБЩЕСТВЕННАЯ ОРГАНИЗАЦИЯ", OrgItemTermin.Types.PREFIX, True, "ОО"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2004("ГРОМАДСЬКА ОРГАНІЗАЦІЯ", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, "ГО"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2003("АВТОНОМНАЯ НЕКОММЕРЧЕСКАЯ ОРГАНИЗАЦИЯ", OrgItemTermin.Types.PREFIX, True, "АНО"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2004("АВТОНОМНА НЕКОМЕРЦІЙНА ОРГАНІЗАЦІЯ", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, "АНО"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2009("ОТКРЫТОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО", OrgItemTermin.Types.PREFIX, True, "ОАО", "OAO"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2020("ВІДКРИТЕ АКЦІОНЕРНЕ ТОВАРИСТВО", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, "ВАТ", "ВАТ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2003("ОТКРЫТОЕ СТРАХОВОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО", OrgItemTermin.Types.PREFIX, True, "ОСАО"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2009("ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ", OrgItemTermin.Types.PREFIX, True, "ООО", "OOO"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2020("ТОВАРИСТВО З ОБМЕЖЕНОЮ ВІДПОВІДАЛЬНІСТЮ", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, "ТОВ", "ТОВ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2020("ТОВАРИСТВО З ПОВНОЮ ВІДПОВІДАЛЬНІСТЮ", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, "ТПВ", "ТПВ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2020("ТОВАРИСТВО З ОБМЕЖЕНОЮ ВІДПОВІДАЛЬНІСТЮ", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, "ТЗОВ", "ТЗОВ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2020("ТОВАРИСТВО З ДОДАТКОВОЮ ВІДПОВІДАЛЬНІСТЮ", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, "ТДВ", "ТДВ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2007("ЧАСТНОЕ АКЦИОНЕРНОЕ ТОВАРИЩЕСТВО", OrgItemTermin.Types.PREFIX, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2020("ПРИВАТНЕ АКЦІОНЕРНЕ ТОВАРИСТВО", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, "ПРАТ", "ПРАТ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2007("ПУБЛИЧНОЕ АКЦИОНЕРНОЕ ТОВАРИЩЕСТВО", OrgItemTermin.Types.PREFIX, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2020("ПУБЛІЧНЕ АКЦІОНЕРНЕ ТОВАРИСТВО", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, "ПАТ", "ПАТ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2007("ЗАКРЫТОЕ АКЦИОНЕРНОЕ ТОВАРИЩЕСТВО", OrgItemTermin.Types.PREFIX, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2020("ЗАКРИТЕ АКЦІОНЕРНЕ ТОВАРИСТВО", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, "ЗАТ", "ЗАТ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2007("ОТКРЫТОЕ АКЦИОНЕРНОЕ ТОВАРИЩЕСТВО", OrgItemTermin.Types.PREFIX, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2020("ВІДКРИТЕ АКЦІОНЕРНЕ ТОВАРИСТВО", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, "ВАТ", "ВАТ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2003("ПУБЛИЧНОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО", OrgItemTermin.Types.PREFIX, True, "ПАО"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2003("СТРАХОВОЕ ПУБЛИЧНОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО", OrgItemTermin.Types.PREFIX, True, "СПАО"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2037("ТОВАРИЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ", OrgItemTermin.Types.PREFIX, "ТОО", "TOO"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1925("ПРЕДПРИНИМАТЕЛЬ БЕЗ ОБРАЗОВАНИЯ ЮРИДИЧЕСКОГО ЛИЦА", OrgItemTermin.Types.PREFIX, "ПБОЮЛ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2003("АКЦИОНЕРНЫЙ КОММЕРЧЕСКИЙ БАНК", OrgItemTermin.Types.PREFIX, True, "АКБ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2004("АКЦІОНЕРНИЙ КОМЕРЦІЙНИЙ БАНК", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, "АКБ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2003("АКЦИОНЕРНЫЙ БАНК", OrgItemTermin.Types.PREFIX, True, "АБ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2004("АКЦІОНЕРНИЙ БАНК", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, "АБ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2007("КОММЕРЧЕСКИЙ БАНК", OrgItemTermin.Types.PREFIX, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2044("КОМЕРЦІЙНИЙ БАНК", MorphLang.UA, OrgItemTermin.Types.PREFIX, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2007("КОНСТРУКТОРСКОЕ БЮРО", OrgItemTermin.Types.PREFIX, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2044("КОНСТРУКТОРСЬКЕ БЮРО", MorphLang.UA, OrgItemTermin.Types.PREFIX, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2003("ОПЫТНО КОНСТРУКТОРСКОЕ БЮРО", OrgItemTermin.Types.PREFIX, True, "ОКБ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2004("ДОСЛІДНО КОНСТРУКТОРСЬКЕ БЮРО", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, "ДКБ"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2002("СПЕЦИАЛЬНОЕ КОНСТРУКТОРСКОЕ БЮРО", OrgItemTermin.Types.PREFIX, "СКБ", True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2050("СПЕЦІАЛЬНЕ КОНСТРУКТОРСЬКЕ БЮРО", MorphLang.UA, OrgItemTermin.Types.PREFIX, "СКБ", True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2003("АКЦИОНЕРНАЯ СТРАХОВАЯ КОМПАНИЯ", OrgItemTermin.Types.PREFIX, True, "АСК"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2004("АКЦІОНЕРНА СТРАХОВА КОМПАНІЯ", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, "АСК"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2053("АВТОТРАНСПОРТНОЕ ПРЕДПРИЯТИЕ", OrgItemTermin.Types.PREFIX, True, True, "АТП"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2054("АВТОТРАНСПОРТНЕ ПІДПРИЄМСТВО", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, True, "АТП"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2003("ТЕЛЕРАДИОКОМПАНИЯ", OrgItemTermin.Types.PREFIX, True, "ТРК"))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2004("ТЕЛЕРАДІОКОМПАНІЯ", MorphLang.UA, OrgItemTermin.Types.PREFIX, True, "ТРК"))
        t = OrgItemTermin._new2002("ОРГАНИЗОВАННАЯ ПРЕСТУПНАЯ ГРУППИРОВКА", OrgItemTermin.Types.PREFIX, "ОПГ", True)
        t.add_variant("ОРГАНИЗОВАННАЯ ПРЕСТУПНАЯ ГРУППА", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2002("ОРГАНИЗОВАННОЕ ПРЕСТУПНОЕ СООБЩЕСТВО", OrgItemTermin.Types.PREFIX, "ОПС", True)
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2059("ПОДРОСТКОВО МОЛОДЕЖНЫЙ КЛУБ", OrgItemTermin.Types.PREFIX, "ПМК", True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2059("СКЛАД ВРЕМЕННОГО ХРАНЕНИЯ", OrgItemTermin.Types.PREFIX, "СВХ", True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2059("ЖИЛИЩНО СТРОИТЕЛЬНЫЙ КООПЕРАТИВ", OrgItemTermin.Types.PREFIX, "ЖСК", True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2059("ГАРАЖНО СТРОИТЕЛЬНЫЙ КООПЕРАТИВ", OrgItemTermin.Types.PREFIX, "ГСК", True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2059("ГАРАЖНО ЭКСПЛУАТАЦИОННЫЙ КООПЕРАТИВ", OrgItemTermin.Types.PREFIX, "ГЭК", True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2059("ГАРАЖНО ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ", OrgItemTermin.Types.PREFIX, "ГПК", True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2059("ПОТРЕБИТЕЛЬСКИЙ ГАРАЖНО СТРОИТЕЛЬНЫЙ КООПЕРАТИВ", OrgItemTermin.Types.PREFIX, "ПГСК", True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2059("ГАРАЖНЫЙ СТРОИТЕЛЬНО ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ", OrgItemTermin.Types.PREFIX, "ГСПК", True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2059("ДАЧНО СТРОИТЕЛЬНЫЙ КООПЕРАТИВ", OrgItemTermin.Types.PREFIX, "ДСК", True, True))
        t = OrgItemTermin._new2059("САДОВОЕ НЕКОММЕРЧЕСКОЕ ТОВАРИЩЕСТВО", OrgItemTermin.Types.PREFIX, "СНТ", True, True)
        t.add_abridge("САДОВОЕ НЕКОМ-Е ТОВАРИЩЕСТВО")
        t.add_variant("СНТ ПМК", False)
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2059("ПРЕДПРИЯТИЕ ПОТРЕБИТЕЛЬСКОЙ КООПЕРАЦИИ", OrgItemTermin.Types.PREFIX, "ППК", True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2070("ПІДПРИЄМСТВО СПОЖИВЧОЇ КООПЕРАЦІЇ", MorphLang.UA, OrgItemTermin.Types.PREFIX, "ПСК", True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2071("ФІЗИЧНА ОСОБА ПІДПРИЄМЕЦЬ", MorphLang.UA, OrgItemTermin.Types.PREFIX, "ФОП", True, True))
        t = OrgItemTermin._new2072("ЖЕЛЕЗНАЯ ДОРОГА", OrgItemTermin.Types.ORG, OrgProfile.TRANSPORT, True, 3)
        t.add_variant("ЖЕЛЕЗНОДОРОЖНАЯ МАГИСТРАЛЬ", False)
        t.add_abridge("Ж.Д.")
        t.add_abridge("Ж/Д")
        t.add_abridge("ЖЕЛ.ДОР.")
        OrgItemTypeToken.__m_global.add(t)
        for s in ["ЗАВОД", "ФАБРИКА", "БАНК", "КОМБИНАТ", "БАНКОВСКАЯ ГРУППА", "БИРЖА", "ФОНДОВАЯ БИРЖА", "FACTORY", "MANUFACTORY", "BANK"]: 
            t = OrgItemTermin._new2073(s, 3.5, OrgItemTermin.Types.ORG, True, True)
            OrgItemTypeToken.__m_global.add(t)
            if (s == "БАНК" or s == "BANK" or s.endswith("БИРЖА")): 
                t._profile = OrgProfile.FINANCE
                t.coeff = (2)
                t.can_has_latin_name = True
                if (OrgItemTypeToken.__m_bank is None): 
                    OrgItemTypeToken.__m_bank = t
        for s in ["ЗАВОД", "ФАБРИКА", "БАНК", "КОМБІНАТ", "БАНКІВСЬКА ГРУПА", "БІРЖА", "ФОНДОВА БІРЖА"]: 
            t = OrgItemTermin._new2074(s, MorphLang.UA, 3.5, OrgItemTermin.Types.ORG, True, True)
            OrgItemTypeToken.__m_global.add(t)
            if (s == "БАНК" or s.endswith("БІРЖА")): 
                t.coeff = (2)
                t.can_has_latin_name = True
                if (OrgItemTypeToken.__m_bank is None): 
                    OrgItemTypeToken.__m_bank = t
        for s in ["ТУРФИРМА", "ТУРАГЕНТСТВО", "ТУРКОМПАНИЯ", "АВИАКОМПАНИЯ", "КИНОСТУДИЯ", "БИЗНЕС-ЦЕНТР", "КООПЕРАТИВ", "РИТЕЙЛЕР", "ОНЛАЙН РИТЕЙЛЕР", "МЕДИАГИГАНТ", "МЕДИАКОМПАНИЯ", "МЕДИАХОЛДИНГ"]: 
            t = OrgItemTermin._new2075(s, 3.5, OrgItemTermin.Types.ORG, True, True, True)
            if (s.startswith("МЕДИА")): 
                t.profiles.append(OrgProfile.MEDIA)
            if ("РИТЕЙЛЕР" in s): 
                t.add_variant(s.replace("РИТЕЙЛЕР", "РЕТЕЙЛЕР"), False)
            OrgItemTypeToken.__m_global.add(t)
        for s in ["ТУРФІРМА", "ТУРАГЕНТСТВО", "ТУРКОМПАНІЯ", "АВІАКОМПАНІЯ", "КІНОСТУДІЯ", "БІЗНЕС-ЦЕНТР", "КООПЕРАТИВ", "РІТЕЙЛЕР", "ОНЛАЙН-РІТЕЙЛЕР", "МЕДІАГІГАНТ", "МЕДІАКОМПАНІЯ", "МЕДІАХОЛДИНГ"]: 
            t = OrgItemTermin._new2076(s, MorphLang.UA, 3.5, OrgItemTermin.Types.ORG, True, True, True)
            OrgItemTypeToken.__m_global.add(t)
        for s in ["ТУРОПЕРАТОР"]: 
            t = OrgItemTermin._new2075(s, .5, OrgItemTermin.Types.ORG, True, True, True)
            OrgItemTypeToken.__m_global.add(t)
        for s in ["ТУРОПЕРАТОР"]: 
            t = OrgItemTermin._new2076(s, MorphLang.UA, .5, OrgItemTermin.Types.ORG, True, True, True)
            OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2079("СБЕРЕГАТЕЛЬНЫЙ БАНК", 4, OrgItemTermin.Types.ORG, True)
        OrgItemTypeToken.__m_sber_bank = t
        t.add_variant("СБЕРБАНК", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2080("ОЩАДНИЙ БАНК", MorphLang.UA, 4, OrgItemTermin.Types.ORG, True)
        t.add_variant("ОЩАДБАНК", False)
        OrgItemTypeToken.__m_global.add(t)
        for s in ["ОРГАНИЗАЦИЯ", "ПРЕДПРИЯТИЕ", "КОМИТЕТ", "КОМИССИЯ", "ПРОИЗВОДИТЕЛЬ", "ГИГАНТ", "ORGANIZATION", "ENTERPRISE", "COMMITTEE", "COMMISSION", "MANUFACTURER"]: 
            t = OrgItemTermin._new2081(s, OrgItemTermin.Types.ORG, True, True, True)
            OrgItemTypeToken.__m_global.add(t)
        for s in ["ОБЩЕСТВО", "АССАМБЛЕЯ", "СЛУЖБА", "ОБЪЕДИНЕНИЕ", "ФЕДЕРАЦИЯ", "COMPANY", "ASSEMBLY", "SERVICE", "UNION", "FEDERATION"]: 
            t = OrgItemTermin._new2081(s, OrgItemTermin.Types.ORG, True, True, True)
            OrgItemTypeToken.__m_global.add(t)
        for s in ["СООБЩЕСТВО", "ФОНД", "АССОЦИАЦИЯ", "АЛЬЯНС", "ГИЛЬДИЯ", "ОБЩИНА", "СОЮЗ", "КЛУБ", "ГРУППИРОВКА", "ЛИГА", "COMMUNITY", "FOUNDATION", "ASSOCIATION", "ALLIANCE", "GUILD", "UNION", "CLUB", "GROUP", "LEAGUE"]: 
            t = OrgItemTermin._new2083(s, 3, OrgItemTermin.Types.ORG, True, True, True, OrgProfile.UNION)
            OrgItemTypeToken.__m_global.add(t)
        for s in ["ПАРТИЯ", "ДВИЖЕНИЕ", "PARTY", "MOVEMENT"]: 
            t = OrgItemTermin._new2084(s, OrgItemTermin.Types.ORG, True, True, True, OrgProfile.UNION)
            OrgItemTypeToken.__m_global.add(t)
        for s in ["НОЧНОЙ КЛУБ", "NIGHTCLUB"]: 
            t = OrgItemTermin._new2085(s, OrgItemTermin.Types.ORG, True, True, OrgProfile.MUSIC)
            OrgItemTypeToken.__m_global.add(t)
        for s in ["ОРГАНІЗАЦІЯ", "ПІДПРИЄМСТВО", "КОМІТЕТ", "КОМІСІЯ", "ВИРОБНИК", "ГІГАНТ", "СУСПІЛЬСТВО", "СПІЛЬНОТА", "ФОНД", "СЛУЖБА", "АСОЦІАЦІЯ", "АЛЬЯНС", "АСАМБЛЕЯ", "ГІЛЬДІЯ", "ОБЄДНАННЯ", "СОЮЗ", "ПАРТІЯ", "РУХ", "ФЕДЕРАЦІЯ", "КЛУБ", "ГРУПУВАННЯ"]: 
            t = OrgItemTermin._new2086(s, MorphLang.UA, OrgItemTermin.Types.ORG, True, True, True)
            OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2087("ДЕПУТАТСКАЯ ГРУППА", OrgItemTermin.Types.ORG, 3, True)
        t.add_variant("ГРУППА ДЕПУТАТОВ", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2088("ДЕПУТАТСЬКА ГРУПА", MorphLang.UA, OrgItemTermin.Types.ORG, 3, True)
        t.add_variant("ГРУПА ДЕПУТАТІВ", False)
        OrgItemTypeToken.__m_global.add(t)
        for s in ["ФОНД", "СОЮЗ", "ОБЪЕДИНЕНИЕ", "ОРГАНИЗАЦИЯ", "ФЕДЕРАЦИЯ", "ДВИЖЕНИЕ"]: 
            for ss in ["ВСЕМИРНЫЙ", "МЕЖДУНАРОДНЫЙ", "ВСЕРОССИЙСКИЙ", "ОБЩЕСТВЕННЫЙ", "НЕКОММЕРЧЕСКИЙ", "ЕВРОПЕЙСКИЙ", "ВСЕУКРАИНСКИЙ"]: 
                t = OrgItemTermin._new2073("{0} {1}".format(ss, s), 3.5, OrgItemTermin.Types.ORG, True, True)
                if (s == "ОБЪЕДИНЕНИЕ" or s == "ДВИЖЕНИЕ"): 
                    t.canonic_text = "{0}ОЕ {1}".format(ss[0:0+len(ss) - 2], s)
                elif (s == "ОРГАНИЗАЦИЯ" or s == "ФЕДЕРАЦИЯ"): 
                    t.canonic_text = "{0}АЯ {1}".format(ss[0:0+len(ss) - 2], s)
                    t.coeff = (3)
                OrgItemTypeToken.__m_global.add(t)
        for s in ["ФОНД", "СОЮЗ", "ОБЄДНАННЯ", "ОРГАНІЗАЦІЯ", "ФЕДЕРАЦІЯ", "РУХ"]: 
            for ss in ["СВІТОВИЙ", "МІЖНАРОДНИЙ", "ВСЕРОСІЙСЬКИЙ", "ГРОМАДСЬКИЙ", "НЕКОМЕРЦІЙНИЙ", "ЄВРОПЕЙСЬКИЙ", "ВСЕУКРАЇНСЬКИЙ"]: 
                t = OrgItemTermin._new2074("{0} {1}".format(ss, s), MorphLang.UA, 3.5, OrgItemTermin.Types.ORG, True, True)
                bi = Morphology.get_word_base_info(s, MorphLang.UA, False, False)
                if (bi is not None and bi.gender != MorphGender.MASCULINE): 
                    adj = Morphology.get_wordform(ss, MorphBaseInfo._new504(MorphClass.ADJECTIVE, bi.gender, MorphNumber.SINGULAR, MorphLang.UA))
                    if (adj is not None): 
                        t.canonic_text = "{0} {1}".format(adj, s)
                if (s == "ОРГАНІЗАЦІЯ" or s == "ФЕДЕРАЦІЯ"): 
                    t.coeff = (3)
                OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2073("ИНВЕСТИЦИОННЫЙ ФОНД", 3, OrgItemTermin.Types.ORG, True, True)
        t.add_variant("ИНВЕСТФОНД", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2074("ІНВЕСТИЦІЙНИЙ ФОНД", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, True)
        t.add_variant("ІНВЕСТФОНД", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2073("СОЦИАЛЬНАЯ СЕТЬ", 3, OrgItemTermin.Types.ORG, True, True)
        t.add_variant("СОЦСЕТЬ", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2074("СОЦІАЛЬНА МЕРЕЖА", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, True)
        t.add_variant("СОЦМЕРЕЖА", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2073("ОФФШОРНАЯ КОМПАНИЯ", 3, OrgItemTermin.Types.ORG, True, True)
        t.add_variant("ОФФШОР", False)
        t.add_variant("ОФШОР", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2074("ОФШОРНА КОМПАНІЯ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, True)
        t.add_variant("ОФШОР", False)
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new1825("ТЕРРОРИСТИЧЕСКАЯ ОРГАНИЗАЦИЯ", 3, OrgItemTermin.Types.ORG, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2099("ТЕРОРИСТИЧНА ОРГАНІЗАЦІЯ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2100("АТОМНАЯ ЭЛЕКТРОСТАНЦИЯ", 3, OrgItemTermin.Types.ORG, "АЭС", True, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2101("АТОМНА ЕЛЕКТРОСТАНЦІЯ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, "АЕС", True, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2100("ГИДРОЭЛЕКТРОСТАНЦИЯ", 3, OrgItemTermin.Types.ORG, "ГЭС", True, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2101("ГІДРОЕЛЕКТРОСТАНЦІЯ", MorphLang.UA, 3, OrgItemTermin.Types.ORG, "ГЕС", True, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2100("ГИДРОРЕЦИРКУЛЯЦИОННАЯ ЭЛЕКТРОСТАНЦИЯ", 3, OrgItemTermin.Types.ORG, "ГРЭС", True, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2100("ТЕПЛОВАЯ ЭЛЕКТРОСТАНЦИЯ", 3, OrgItemTermin.Types.ORG, "ТЭС", True, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2100("НЕФТЕПЕРЕРАБАТЫВАЮЩИЙ ЗАВОД", 3, OrgItemTermin.Types.ORG, "НПЗ", True, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2101("НАФТОПЕРЕРОБНИЙ ЗАВОД", MorphLang.UA, 3, OrgItemTermin.Types.ORG, "НПЗ", True, True, True))
        for s in ["ФИРМА", "КОМПАНИЯ", "КОРПОРАЦИЯ", "ГОСКОРПОРАЦИЯ", "КОНЦЕРН", "КОНСОРЦИУМ", "ХОЛДИНГ", "МЕДИАХОЛДИНГ", "ТОРГОВЫЙ ДОМ", "ТОРГОВЫЙ ЦЕНТР", "УЧЕБНЫЙ ЦЕНТР", "ИССЛЕДОВАТЕЛЬСКИЙ ЦЕНТР", "КОСМИЧЕСКИЙ ЦЕНТР", "АУКЦИОННЫЙ ДОМ", "ИЗДАТЕЛЬСТВО", "ИЗДАТЕЛЬСКИЙ ДОМ", "ТОРГОВЫЙ КОМПЛЕКС", "ТОРГОВО РАЗВЛЕКАТЕЛЬНЫЙ КОМПЛЕКС", "АГЕНТСТВО НЕДВИЖИМОСТИ", "ГРУППА КОМПАНИЙ", "МЕДИАГРУППА", "МАГАЗИН", "ТОРГОВЫЙ КОМПЛЕКС", "ГИПЕРМАРКЕТ", "СУПЕРМАРКЕТ", "КАФЕ", "РЕСТОРАН", "БАР", "АУКЦИОН", "АНАЛИТИЧЕСКИЙ ЦЕНТР", "COMPANY", "CORPORATION"]: 
            t = OrgItemTermin._new2108(s, 3, OrgItemTermin.Types.ORG, True, True, True)
            if (s == "ИЗДАТЕЛЬСТВО"): 
                t.add_abridge("ИЗД-ВО")
                t.add_abridge("ИЗ-ВО")
                t.profiles.append(OrgProfile.MEDIA)
                t.profiles.append(OrgProfile.PRESS)
                t.add_variant("ИЗДАТЕЛЬСКИЙ ДОМ", False)
            elif (s.startswith("ИЗДАТ")): 
                t.profiles.append(OrgProfile.PRESS)
                t.profiles.append(OrgProfile.MEDIA)
            elif (s == "ТОРГОВЫЙ ДОМ"): 
                t.acronym = "ТД"
            elif (s == "ТОРГОВЫЙ ЦЕНТР"): 
                t.acronym = "ТЦ"
            elif (s == "ТОРГОВЫЙ КОМПЛКС"): 
                t.acronym = "ТК"
            elif (s == "ГРУППА КОМПАНИЙ"): 
                t.acronym = "ГК"
            if (s.startswith("МЕДИА")): 
                t.profiles.append(OrgProfile.MEDIA)
            if (s.endswith(" ЦЕНТР")): 
                t.coeff = 3.5
            if (s == "КОМПАНИЯ" or s == "ФИРМА"): 
                t.coeff = (1)
            OrgItemTypeToken.__m_global.add(t)
        for s in ["ФІРМА", "КОМПАНІЯ", "КОРПОРАЦІЯ", "ДЕРЖКОРПОРАЦІЯ", "КОНЦЕРН", "КОНСОРЦІУМ", "ХОЛДИНГ", "МЕДІАХОЛДИНГ", "ТОРГОВИЙ ДІМ", "ТОРГОВИЙ ЦЕНТР", "НАВЧАЛЬНИЙ ЦЕНТР", "ВИДАВНИЦТВО", "ВИДАВНИЧИЙ ДІМ", "ТОРГОВИЙ КОМПЛЕКС", "ТОРГОВО-РОЗВАЖАЛЬНИЙ КОМПЛЕКС", "АГЕНТСТВО НЕРУХОМОСТІ", "ГРУПА КОМПАНІЙ", "МЕДІАГРУПА", "МАГАЗИН", "ТОРГОВИЙ КОМПЛЕКС", "ГІПЕРМАРКЕТ", "СУПЕРМАРКЕТ", "КАФЕ", "БАР", "АУКЦІОН", "АНАЛІТИЧНИЙ ЦЕНТР"]: 
            t = OrgItemTermin._new2109(s, MorphLang.UA, OrgItemTermin.Types.ORG, True, True, True)
            if (s == "ВИДАВНИЦТВО"): 
                t.add_abridge("ВИД-ВО")
                t.add_variant("ВИДАВНИЧИЙ ДІМ", False)
            elif (s == "ТОРГОВИЙ ДІМ"): 
                t.acronym = "ТД"
            elif (s == "ТОРГОВИЙ ЦЕНТР"): 
                t.acronym = "ТЦ"
            elif (s == "ТОРГОВИЙ КОМПЛЕКС"): 
                t.acronym = "ТК"
            elif (s == "ГРУПА КОМПАНІЙ"): 
                t.acronym = "ГК"
            elif (s == "КОМПАНІЯ" or s == "ФІРМА"): 
                t.coeff = (1)
            if (s.startswith("МЕДІА")): 
                t.profiles.append(OrgProfile.MEDIA)
            OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2110("РОК ГРУППА", MorphLang.RU, OrgProfile.MUSIC, OrgItemTermin.Types.ORG, 3, True)
        t.add_variant("РОКГРУППА", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2110("ПАНК ГРУППА", MorphLang.RU, OrgProfile.MUSIC, OrgItemTermin.Types.ORG, 3, True)
        t.add_variant("ПАНКГРУППА", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2110("ОРКЕСТР", MorphLang.RU, OrgProfile.MUSIC, OrgItemTermin.Types.ORG, 3, True)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2110("ХОР", MorphLang.RU, OrgProfile.MUSIC, OrgItemTermin.Types.ORG, 3, True)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2110("МУЗЫКАЛЬНЫЙ КОЛЛЕКТИВ", MorphLang.RU, OrgProfile.MUSIC, OrgItemTermin.Types.ORG, 3, True)
        t.add_variant("РОКГРУППА", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2115("ВОКАЛЬНО ИНСТРУМЕНТАЛЬНЫЙ АНСАМБЛЬ", MorphLang.RU, OrgProfile.MUSIC, OrgItemTermin.Types.ORG, 3, True, "ВИА")
        t.add_variant("ИНСТРУМЕНТАЛЬНЫЙ АНСАМБЛЬ", False)
        OrgItemTypeToken.__m_global.add(t)
        for s in ["НОТАРИАЛЬНАЯ КОНТОРА", "АДВОКАТСКОЕ БЮРО", "СТРАХОВОЕ ОБЩЕСТВО", "ЮРИДИЧЕСКИЙ ДОМ"]: 
            t = OrgItemTermin._new2116(s, OrgItemTermin.Types.ORG, True, True, True, True)
            OrgItemTypeToken.__m_global.add(t)
        for s in ["НОТАРІАЛЬНА КОНТОРА", "АДВОКАТСЬКЕ БЮРО", "СТРАХОВЕ ТОВАРИСТВО"]: 
            t = OrgItemTermin._new2117(s, MorphLang.UA, OrgItemTermin.Types.ORG, True, True, True, True)
            OrgItemTypeToken.__m_global.add(t)
        for s in ["ГАЗЕТА", "ЕЖЕНЕДЕЛЬНИК", "ТАБЛОИД", "ЕЖЕНЕДЕЛЬНЫЙ ЖУРНАЛ", "NEWSPAPER", "WEEKLY", "TABLOID", "MAGAZINE"]: 
            t = OrgItemTermin._new2118(s, 3, OrgItemTermin.Types.ORG, True, True, True, OrgProfile.MEDIA)
            t.profiles.append(OrgProfile.PRESS)
            OrgItemTypeToken.__m_global.add(t)
        for s in ["ГАЗЕТА", "ТИЖНЕВИК", "ТАБЛОЇД"]: 
            t = OrgItemTermin._new2119(s, MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, True, True, OrgProfile.MEDIA)
            t.profiles.append(OrgProfile.PRESS)
            OrgItemTypeToken.__m_global.add(t)
        for s in ["РАДИОСТАНЦИЯ", "РАДИО", "ТЕЛЕКАНАЛ", "ТЕЛЕКОМПАНИЯ", "НОВОСТНОЙ ПОРТАЛ", "ИНТЕРНЕТ ПОРТАЛ", "ИНТЕРНЕТ ИЗДАНИЕ", "ИНТЕРНЕТ РЕСУРС"]: 
            t = OrgItemTermin._new2118(s, 3, OrgItemTermin.Types.ORG, True, True, True, OrgProfile.MEDIA)
            if (s == "РАДИО"): 
                t.canonic_text = "РАДИОСТАНЦИЯ"
                t.is_doubt_word = True
            OrgItemTypeToken.__m_global.add(t)
        for s in ["РАДІО", "РАДІО", "ТЕЛЕКАНАЛ", "ТЕЛЕКОМПАНІЯ", "НОВИННИЙ ПОРТАЛ", "ІНТЕРНЕТ ПОРТАЛ", "ІНТЕРНЕТ ВИДАННЯ", "ІНТЕРНЕТ РЕСУРС"]: 
            t = OrgItemTermin._new2119(s, MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, True, True, OrgProfile.MEDIA)
            if (s == "РАДІО"): 
                t.canonic_text = "РАДІОСТАНЦІЯ"
                t.is_doubt_word = True
            OrgItemTypeToken.__m_global.add(t)
        for s in ["ПАНСИОНАТ", "САНАТОРИЙ", "ДОМ ОТДЫХА", "ОТЕЛЬ", "ГОСТИНИЦА", "SPA-ОТЕЛЬ", "ОЗДОРОВИТЕЛЬНЫЙ ЛАГЕРЬ", "ДЕТСКИЙ ЛАГЕРЬ", "ПИОНЕРСКИЙ ЛАГЕРЬ", "БАЗА ОТДЫХА", "СПОРТ-КЛУБ"]: 
            t = OrgItemTermin._new2108(s, 3, OrgItemTermin.Types.ORG, True, True, True)
            if (s == "САНАТОРИЙ"): 
                t.add_abridge("САН.")
            elif (s == "ДОМ ОТДЫХА"): 
                t.add_abridge("Д.О.")
                t.add_abridge("ДОМ ОТД.")
                t.add_abridge("Д.ОТД.")
            elif (s == "ПАНСИОНАТ"): 
                t.add_abridge("ПАНС.")
            OrgItemTypeToken.__m_global.add(t)
        for s in ["ПАНСІОНАТ", "САНАТОРІЙ", "БУДИНОК ВІДПОЧИНКУ", "ГОТЕЛЬ", "SPA-ГОТЕЛЬ", "ОЗДОРОВЧИЙ ТАБІР", "БАЗА ВІДПОЧИНКУ", "СПОРТ-КЛУБ"]: 
            t = OrgItemTermin._new2123(s, MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, True, True)
            if (s == "САНАТОРІЙ"): 
                t.add_abridge("САН.")
            OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2124("ДЕТСКИЙ ОЗДОРОВИТЕЛЬНЫЙ ЛАГЕРЬ", 3, OrgItemTermin.Types.ORG, "ДОЛ", True, True, True))
        OrgItemTypeToken.__m_global.add(OrgItemTermin._new2124("ДЕТСКИЙ СПОРТИВНЫЙ ОЗДОРОВИТЕЛЬНЫЙ ЛАГЕРЬ", 3, OrgItemTermin.Types.ORG, "ДСОЛ", True, True, True))
        for s in ["КОЛХОЗ", "САДОВО ОГОРОДНОЕ ТОВАРИЩЕСТВО", "КООПЕРАТИВ", "ФЕРМЕРСКОЕ ХОЗЯЙСТВО", "КРЕСТЬЯНСКО ФЕРМЕРСКОЕ ХОЗЯЙСТВО", "АГРОФИРМА", "КОНЕЗАВОД", "ПТИЦЕФЕРМА", "СВИНОФЕРМА", "ФЕРМА", "ЛЕСПРОМХОЗ"]: 
            t = OrgItemTermin._new2126(s, 3, OrgItemTermin.Types.ORG, True, True, True, True)
            OrgItemTypeToken.__m_global.add(t)
        for s in ["КОЛГОСП", "САДОВО ГОРОДНЄ ТОВАРИСТВО", "КООПЕРАТИВ", "ФЕРМЕРСЬКЕ ГОСПОДАРСТВО", "СЕЛЯНСЬКО ФЕРМЕРСЬКЕ ГОСПОДАРСТВО", "АГРОФІРМА", "КОНЕЗАВОД", "ПТАХОФЕРМА", "СВИНОФЕРМА", "ФЕРМА"]: 
            t = OrgItemTermin._new2127(s, MorphLang.UA, 3, OrgItemTermin.Types.ORG, True, True, True, True)
            OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2126("АВТОМОБИЛЬНЫЙ ЗАВОД", 3, OrgItemTermin.Types.ORG, True, True, True, True)
        t.add_variant("АВТОЗАВОД", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2126("АВТОМОБИЛЬНЫЙ ЦЕНТР", 3, OrgItemTermin.Types.ORG, True, True, True, True)
        t.add_variant("АВТОЦЕНТР", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2126("СОВХОЗ", 3, OrgItemTermin.Types.ORG, True, True, True, True)
        t.add_abridge("С/Х")
        t.add_abridge("С-З")
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2126("ПЛЕМЕННОЕ ХОЗЯЙСТВО", 3, OrgItemTermin.Types.ORG, True, True, True, True)
        t.add_variant("ПЛЕМХОЗ", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2126("ЛЕСНОЕ ХОЗЯЙСТВО", 3, OrgItemTermin.Types.ORG, True, True, True, True)
        t.add_variant("ЛЕСХОЗ", False)
        OrgItemTypeToken.__m_global.add(t)
        sads = ["Садоводческое некоммерческое товарищество", "СНТ", "Дачное некоммерческое товарищество", "ДНТ", "Огородническое некоммерческое товарищество", "ОНТ", "Садоводческое некоммерческое партнерство", "СНП", "Дачное некоммерческое партнерство", "ДНП", "Огородническое некоммерческое партнерство", "ОНП", "Садоводческий потребительский кооператив", "СПК", "Дачный потребительский кооператив", "ДПК", "Огороднический потребительский кооператив", "ОПК"]
        i = 0
        while i < len(sads): 
            t = OrgItemTermin._new2133(sads[i].upper(), 3, sads[i + 1], OrgItemTermin.Types.ORG, True, True, True)
            t.add_abridge(sads[i + 1])
            if (t.acronym == "СНТ"): 
                t.add_abridge("САДОВ.НЕКОМ.ТОВ.")
            OrgItemTypeToken.__m_global.add(t)
            i += 2
        t = OrgItemTermin._new2126("САДОВОДЧЕСКОЕ ТОВАРИЩЕСТВО", 3, OrgItemTermin.Types.ORG, True, True, True, True)
        t.add_abridge("САДОВОДЧ.ТОВ.")
        t.add_abridge("САДОВ.ТОВ.")
        t.add_abridge("САД.ТОВ.")
        t.add_abridge("С.Т.")
        t.add_variant("САДОВОЕ ТОВАРИЩЕСТВО", False)
        t.add_variant("САДОВ. ТОВАРИЩЕСТВО", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2126("САДОВОДЧЕСКИЙ КООПЕРАТИВ", 3, OrgItemTermin.Types.ORG, True, True, True, True)
        t.add_abridge("САДОВОДЧ.КООП.")
        t.add_abridge("САДОВ.КООП.")
        t.add_variant("САДОВЫЙ КООПЕРАТИВ", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new2126("ДАЧНОЕ ТОВАРИЩЕСТВО", 3, OrgItemTermin.Types.ORG, True, True, True, True)
        t.add_abridge("ДАЧН.ТОВ.")
        t.add_abridge("ДАЧ.ТОВ.")
        OrgItemTypeToken.__m_global.add(t)
        for s in ["ФЕСТИВАЛЬ", "ЧЕМПИОНАТ", "ОЛИМПИАДА", "КОНКУРС"]: 
            t = OrgItemTermin._new1721(s, 3, OrgItemTermin.Types.ORG, True)
            OrgItemTypeToken.__m_global.add(t)
        for s in ["ФЕСТИВАЛЬ", "ЧЕМПІОНАТ", "ОЛІМПІАДА"]: 
            t = OrgItemTermin._new2138(s, MorphLang.UA, 3, OrgItemTermin.Types.ORG, True)
            OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1823("ПОГРАНИЧНЫЙ ПОСТ", 3, OrgItemTermin.Types.ORG, True, True)
        t.add_variant("ПОГП", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1823("ПОГРАНИЧНАЯ ЗАСТАВА", 3, OrgItemTermin.Types.ORG, True, True)
        t.add_variant("ПОГЗ", False)
        t.add_variant("ПОГРАНЗАСТАВА", False)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1805("ТЕРРИТОРИАЛЬНЫЙ ПУНКТ", 3, OrgItemTermin.Types.DEP, True)
        OrgItemTypeToken.__m_global.add(t)
        t = OrgItemTermin._new1805("МИГРАЦИОННЫЙ ПУНКТ", 3, OrgItemTermin.Types.DEP, True)
        OrgItemTypeToken.__m_global.add(t)
        OrgItemTypeToken._m_pref_words = TerminCollection()
        for s in ["КАПИТАЛ", "РУКОВОДСТВО", "СЪЕЗД", "СОБРАНИЕ", "СОВЕТ", "УПРАВЛЕНИЕ", "ДЕПАРТАМЕНТ"]: 
            OrgItemTypeToken._m_pref_words.add(Termin(s))
        for s in ["КАПІТАЛ", "КЕРІВНИЦТВО", "ЗЇЗД", "ЗБОРИ", "РАДА", "УПРАВЛІННЯ"]: 
            OrgItemTypeToken._m_pref_words.add(Termin._new886(s, MorphLang.UA))
        for s in ["АКЦИЯ", "ВЛАДЕЛЕЦ", "ВЛАДЕЛИЦА", "СОВЛАДЕЛЕЦ", "СОВЛАДЕЛИЦА", "КОНКУРЕНТ"]: 
            OrgItemTypeToken._m_pref_words.add(Termin._new118(s, s))
        for s in ["АКЦІЯ", "ВЛАСНИК", "ВЛАСНИЦЯ", "СПІВВЛАСНИК", "СПІВВЛАСНИЦЯ", "КОНКУРЕНТ"]: 
            OrgItemTypeToken._m_pref_words.add(Termin._new119(s, s, MorphLang.UA))
        for k in range(3):
            name_ = ("pattrs_ru.dat" if k == 0 else ("pattrs_ua.dat" if k == 1 else "pattrs_en.dat"))
            dat = ResourceHelper.get_bytes(name_)
            if (dat is None): 
                raise Utils.newException("Can't file resource file {0} in Organization analyzer".format(name_), None)
            with io.BytesIO(OrgItemTypeToken._deflate(dat)) as tmp: 
                tmp.seek(0, io.SEEK_SET)
                xml0_ = None # new XmlDocument
                xml0_ = xml.etree.ElementTree.parse(tmp)
                for x in xml0_.getroot(): 
                    if (k == 0): 
                        OrgItemTypeToken._m_pref_words.add(Termin._new118(Utils.getXmlInnerText(x), 1))
                    elif (k == 1): 
                        OrgItemTypeToken._m_pref_words.add(Termin._new119(Utils.getXmlInnerText(x), 1, MorphLang.UA))
                    elif (k == 2): 
                        OrgItemTypeToken._m_pref_words.add(Termin._new119(Utils.getXmlInnerText(x), 1, MorphLang.EN))
        OrgItemTypeToken._m_key_words_for_refs = TerminCollection()
        for s in ["КОМПАНИЯ", "ФИРМА", "ПРЕДПРИЯТИЕ", "КОРПОРАЦИЯ", "ВЕДОМСТВО", "УЧРЕЖДЕНИЕ", "КОМПАНІЯ", "ФІРМА", "ПІДПРИЄМСТВО", "КОРПОРАЦІЯ", "ВІДОМСТВО", "УСТАНОВА"]: 
            OrgItemTypeToken._m_key_words_for_refs.add(Termin(s))
        for s in ["ЧАСТЬ", "БАНК", "ЗАВОД", "ФАБРИКА", "АЭРОПОРТ", "БИРЖА", "СЛУЖБА", "МИНИСТЕРСТВО", "КОМИССИЯ", "КОМИТЕТ", "ГРУППА", "ЧАСТИНА", "БАНК", "ЗАВОД", "ФАБРИКА", "АЕРОПОРТ", "БІРЖА", "СЛУЖБА", "МІНІСТЕРСТВО", "КОМІСІЯ", "КОМІТЕТ", "ГРУПА"]: 
            OrgItemTypeToken._m_key_words_for_refs.add(Termin._new118(s, s))
        Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = False
    
    @staticmethod
    def _deflate(zip0_ : bytearray) -> bytearray:
        with io.BytesIO() as unzip: 
            data = io.BytesIO(zip0_)
            data.seek(0, io.SEEK_SET)
            MorphSerializeHelper.deflate_gzip(data, unzip)
            data.close()
            return unzip.getvalue()
    
    M_EMPTY_TYP_WORDS = None
    
    __m_decree_key_words = None
    
    @staticmethod
    def is_decree_keyword(t : 'Token', cou : int=1) -> bool:
        if (t is None): 
            return False
        i = 0
        while (i < cou) and t is not None: 
            if (t.is_newline_after): 
                break
            if (not t.chars.is_cyrillic_letter): 
                break
            for d in OrgItemTypeToken.__m_decree_key_words: 
                if (t.is_value(d, None)): 
                    return True
            i += 1; t = t.previous
        return False
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        from pullenti.morph.CharsInfo import CharsInfo
        self.typ = None
        self.name = None
        self.alt_name = None
        self.name_is_name = False
        self.alt_typ = None
        self.number = None
        self.__m_profile = None
        self.root = None
        self.__m_is_dep = -1
        self.is_not_typ = False
        self.__m_coef = -1
        self.geo = None
        self.geo2 = None
        self.chars_root = CharsInfo()
        self.can_be_dep_before_organization = False
        self.is_douter_org = False
        self.__m_is_doubt_root_word = -1
        self.can_be_organization = False
        super().__init__(begin, end, None)
    
    @property
    def profiles(self) -> typing.List['OrgProfile']:
        """ Список профилей """
        if (self.__m_profile is None): 
            self.__m_profile = list()
            if (self.root is not None): 
                self.__m_profile.extend(self.root.profiles)
        return self.__m_profile
    
    @profiles.setter
    def profiles(self, value) -> typing.List['OrgProfile']:
        self.__m_profile = value
        return value
    
    @property
    def is_dep(self) -> bool:
        if (self.__m_is_dep >= 0): 
            return self.__m_is_dep > 0
        if (self.root is None): 
            return False
        if (OrgProfile.UNIT in self.root.profiles): 
            return True
        return False
    
    @is_dep.setter
    def is_dep(self, value) -> bool:
        self.__m_is_dep = (1 if value else 0)
        return value
    
    @property
    def coef(self) -> float:
        if (self.__m_coef >= 0): 
            return self.__m_coef
        if (self.root is not None): 
            return self.root.coeff
        return 0
    
    @coef.setter
    def coef(self, value) -> float:
        self.__m_coef = value
        return value
    
    @property
    def name_words_count(self) -> int:
        """ Количество слов в имени """
        cou = 1
        if (self.name is None): 
            return 1
        i = 0
        while i < len(self.name): 
            if (self.name[i] == ' '): 
                cou += 1
            i += 1
        return cou
    
    @property
    def is_doubt_root_word(self) -> bool:
        """ Корень - сомнительное слово (типа: организация или движение) """
        if (self.__m_is_doubt_root_word >= 0): 
            return self.__m_is_doubt_root_word == 1
        if (self.root is None): 
            return False
        return self.root.is_doubt_word
    
    @is_doubt_root_word.setter
    def is_doubt_root_word(self, value) -> bool:
        self.__m_is_doubt_root_word = (1 if value else 0)
        return value
    
    def __str__(self) -> str:
        if (self.name is not None): 
            return self.name
        else: 
            return self.typ
    
    @staticmethod
    def try_attach(t : 'Token', can_be_first_letter_lower : bool=False, ad : 'AnalyzerDataWithOntology'=None) -> 'OrgItemTypeToken':
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.Referent import Referent
        from pullenti.ner.geo.GeoReferent import GeoReferent
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.morph.MorphClass import MorphClass
        from pullenti.ner._org.internal.OrgItemTermin import OrgItemTermin
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner._org.internal.OrgItemNumberToken import OrgItemNumberToken
        from pullenti.morph.MorphLang import MorphLang
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.morph.Morphology import Morphology
        if (t is None or (((isinstance(t, ReferentToken)) and not t.chars.is_latin_letter))): 
            return None
        res = OrgItemTypeToken.__try_attach(t, can_be_first_letter_lower)
        if (res is None and t.chars.is_latin_letter): 
            if (t.is_value("THE", None)): 
                res1 = OrgItemTypeToken.try_attach(t.next0_, can_be_first_letter_lower, None)
                if (res1 is not None): 
                    res1.begin_token = t
                    return res1
                return None
            if ((isinstance(t.get_referent(), GeoReferent)) and (isinstance(t.next0_, TextToken)) and t.next0_.chars.is_latin_letter): 
                res1 = OrgItemTypeToken.try_attach(t.next0_, can_be_first_letter_lower, None)
                if (res1 is not None): 
                    res1.begin_token = t
                    res1.geo = (t if isinstance(t, ReferentToken) else None)
                    res1.name = MiscHelper.get_text_value_of_meta_token(res1, GetTextAttr.NO)
                    return res1
            if (t.chars.is_capital_upper): 
                mc = t.get_morph_class_in_dictionary()
                if ((mc.is_conjunction or mc.is_preposition or mc.is_misc) or mc.is_pronoun or mc.is_personal_pronoun): 
                    pass
                else: 
                    ttt = t.next0_
                    while ttt is not None: 
                        if (not ttt.chars.is_latin_letter): 
                            break
                        if (ttt.whitespaces_before_count > 3): 
                            break
                        if (MiscHelper.is_eng_adj_suffix(ttt.next0_)): 
                            ttt = ttt.next0_.next0_.next0_
                            if (ttt is None): 
                                break
                        res1 = OrgItemTypeToken.__try_attach(ttt, True)
                        if (res1 is not None): 
                            res1.name = MiscHelper.get_text_value(t, res1.end_token, GetTextAttr.IGNOREARTICLES)
                            if (res1.coef < 5): 
                                res1.coef = 5
                            res1.begin_token = t
                            return res1
                        if (ttt.chars.is_all_lower and not ttt.is_and): 
                            break
                        if (ttt.whitespaces_before_count > 1): 
                            break
                        ttt = ttt.next0_
        if ((res is not None and res.name is not None and res.name.startswith("СОВМЕСТ")) and LanguageHelper.ends_with_ex(res.name, "ПРЕДПРИЯТИЕ", "КОМПАНИЯ", None, None)): 
            res.root = OrgItemTypeToken.__m_sovm_pred
            res.typ = "совместное предприятие"
            tt1 = t.next0_
            while tt1 is not None and tt1.end_char <= res.end_token.begin_char: 
                rt = tt1.kit.process_referent("GEO", tt1)
                if (rt is not None): 
                    res.coef += .5
                    if (res.geo is None): 
                        res.geo = rt
                    elif (res.geo.referent.can_be_equals(rt.referent, Referent.EqualType.WITHINONETEXT)): 
                        pass
                    elif (res.geo2 is None): 
                        res.geo2 = rt
                    tt1 = rt.end_token
                tt1 = tt1.next0_
        if (((((res is not None and res.begin_token.length_char <= 2 and not res.begin_token.chars.is_all_lower) and res.begin_token.next0_ is not None and res.begin_token.next0_.is_char('.')) and res.begin_token.next0_.next0_ is not None and res.begin_token.next0_.next0_.length_char <= 2) and not res.begin_token.next0_.next0_.chars.is_all_lower and res.begin_token.next0_.next0_.next0_ is not None) and res.begin_token.next0_.next0_.next0_.is_char('.') and res.end_token == res.begin_token.next0_.next0_.next0_): 
            return None
        if (res is not None and res.typ == "управление"): 
            if (res.name is not None and "ГОСУДАРСТВЕННОЕ" in res.name): 
                return None
            if (res.begin_token.previous is not None and res.begin_token.previous.is_value("ГОСУДАРСТВЕННЫЙ", None)): 
                return None
        if (res is not None and res.geo is None and (isinstance(res.begin_token.previous, TextToken))): 
            rt = res.kit.process_referent("GEO", res.begin_token.previous)
            if (rt is not None and rt.morph.class0_.is_adjective): 
                if (res.begin_token.previous.previous is not None and res.begin_token.previous.previous.is_value("ОРДЕН", None)): 
                    pass
                else: 
                    res.geo = rt
                    res.begin_token = rt.begin_token
        if ((res is not None and res.typ == "комитет" and res.geo is None) and res.end_token.next0_ is not None and (isinstance(res.end_token.next0_.get_referent(), GeoReferent))): 
            res.geo = (res.end_token.next0_ if isinstance(res.end_token.next0_, ReferentToken) else None)
            res.end_token = res.end_token.next0_
            res.coef = 2
            if (res.end_token.next0_ is not None and res.end_token.next0_.is_value("ПО", None)): 
                res.coef += 1
        if ((res is not None and res.typ == "агентство" and res.chars.is_capital_upper) and res.end_token.next0_ is not None and res.end_token.next0_.is_value("ПО", None)): 
            res.coef += 3
        if (res is not None and res.geo is not None): 
            has_adj = False
            tt1 = res.begin_token
            first_pass3951 = True
            while True:
                if first_pass3951: first_pass3951 = False
                else: tt1 = tt1.next0_
                if (not (tt1 is not None and tt1.end_char <= res.end_token.begin_char)): break
                rt = tt1.kit.process_referent("GEO", tt1)
                if (rt is not None): 
                    if (res.geo is not None and res.geo.referent.can_be_equals(rt.referent, Referent.EqualType.WITHINONETEXT)): 
                        continue
                    if (res.geo2 is not None and res.geo2.referent.can_be_equals(rt.referent, Referent.EqualType.WITHINONETEXT)): 
                        continue
                    res.coef += .5
                    if (res.geo is None): 
                        res.geo = rt
                    elif (res.geo2 is None): 
                        res.geo2 = rt
                    tt1 = rt.end_token
                elif (tt1.get_morph_class_in_dictionary().is_adjective): 
                    has_adj = True
            if ((res.typ == "институт" or res.typ == "академия" or res.typ == "інститут") or res.typ == "академія"): 
                if (has_adj): 
                    res.coef += 2
                    res.can_be_organization = True
        if (res is not None and res.geo is None): 
            tt2 = res.end_token.next0_
            if (tt2 is not None and not tt2.is_newline_before and tt2.morph.class0_.is_preposition): 
                if (((isinstance(tt2.next0_, TextToken)) and (tt2.next0_ if isinstance(tt2.next0_, TextToken) else None).term == "ВАШ" and res.root is not None) and OrgProfile.JUSTICE in res.root.profiles): 
                    res.coef = 5
                    res.end_token = tt2.next0_
                    tt2 = tt2.next0_.next0_
                    res.name = (((Utils.ifNotNull(res.name, (res.root.canonic_text if res is not None and res.root is not None else None)))) + " ПО ВЗЫСКАНИЮ АДМИНИСТРАТИВНЫХ ШТРАФОВ")
                    res.typ = "отдел"
            if (tt2 is not None and not tt2.is_newline_before and tt2.morph.class0_.is_preposition): 
                tt2 = tt2.next0_
                if (tt2 is not None and not tt2.is_newline_before and (isinstance(tt2.get_referent(), GeoReferent))): 
                    res.end_token = tt2
                    res.geo = (tt2 if isinstance(tt2, ReferentToken) else None)
                    if ((tt2.next0_ is not None and tt2.next0_.is_and and (isinstance(tt2.next0_.next0_, ReferentToken))) and (isinstance(tt2.next0_.next0_.get_referent(), GeoReferent))): 
                        tt2 = tt2.next0_.next0_
                        res.end_token = tt2
                        res.geo2 = (tt2 if isinstance(tt2, ReferentToken) else None)
            elif (((tt2 is not None and not tt2.is_newline_before and tt2.is_hiphen) and (isinstance(tt2.next0_, TextToken)) and tt2.next0_.get_morph_class_in_dictionary().is_noun) and not tt2.next0_.is_value("БАНК", None)): 
                npt1 = NounPhraseHelper.try_parse(res.end_token, NounPhraseParseAttr.NO, 0)
                if (npt1 is not None and npt1.end_token == tt2.next0_): 
                    res.alt_typ = npt1.get_normal_case_text(MorphClass(), True, MorphGender.UNDEFINED, False).lower()
                    res.end_token = npt1.end_token
            elif (tt2 is not None and (tt2.whitespaces_before_count < 3)): 
                npt = NounPhraseHelper.try_parse(tt2, NounPhraseParseAttr.NO, 0)
                if (npt is not None and npt.morph.case.is_genitive): 
                    rr = tt2.kit.process_referent("NAMEDENTITY", tt2)
                    if (rr is not None and ((rr.morph.case.is_genitive or rr.morph.case.is_undefined)) and rr.referent.find_slot("KIND", "location", True) is not None): 
                        res.end_token = rr.end_token
                    elif (res.root is not None and res.root.typ == OrgItemTermin.Types.PREFIX and npt.end_token.is_value("ОБРАЗОВАНИЕ", None)): 
                        res.end_token = npt.end_token
                        res.profiles.append(OrgProfile.EDUCATION)
        if (res is not None and res.typ is not None and str.isdigit(res.typ[0])): 
            ii = res.typ.find(' ')
            if (ii < (len(res.typ) - 1)): 
                res.number = res.typ[0:0+ii]
                res.typ = res.typ[ii + 1:].strip()
        if (res is not None and res.name is not None and str.isdigit(res.name[0])): 
            ii = res.name.find(' ')
            if (ii < (len(res.name) - 1)): 
                res.number = res.name[0:0+ii]
                res.name = res.name[ii + 1:].strip()
        if (res is not None and res.typ == "фонд"): 
            if (t.previous is not None and ((t.previous.is_value("ПРИЗОВОЙ", None) or t.previous.is_value("ЖИЛИЩНЫЙ", None)))): 
                return None
            if (res.begin_token.is_value("ПРИЗОВОЙ", None) or res.begin_token.is_value("ЖИЛИЩНЫЙ", None)): 
                return None
        if (res is not None and res.length_char == 2 and res.typ == "АО"): 
            res.is_doubt_root_word = True
        if (res is not None and res.typ == "администрация" and t.next0_ is not None): 
            if ((t.next0_.is_char('(') and t.next0_.next0_ is not None and ((t.next0_.next0_.is_value("ПРАВИТЕЛЬСТВО", None) or t.next0_.next0_.is_value("ГУБЕРНАТОР", None)))) and t.next0_.next0_.next0_ is not None and t.next0_.next0_.next0_.is_char(')')): 
                res.end_token = t.next0_.next0_.next0_
                res.alt_typ = "правительство"
                return res
            if (isinstance(t.next0_.get_referent(), GeoReferent)): 
                res.alt_typ = "правительство"
        if ((res is not None and res.typ == "ассоциация" and res.end_token.next0_ is not None) and (res.whitespaces_after_count < 2)): 
            npt = NounPhraseHelper.try_parse(res.end_token.next0_, NounPhraseParseAttr.NO, 0)
            if (npt is not None): 
                str0_ = MiscHelper.get_text_value_of_meta_token(npt, GetTextAttr.NO)
                res.name = "{0} {1}".format(Utils.ifNotNull(res.name, (res.typ.upper() if res is not None and res.typ is not None else None)), str0_)
                res.end_token = npt.end_token
                res.coef += 1
        if ((res is not None and res.typ == "представительство" and res.end_token.next0_ is not None) and (res.whitespaces_after_count < 2)): 
            npt = NounPhraseHelper.try_parse(res.end_token.next0_, NounPhraseParseAttr.NO, 0)
            if (npt is not None): 
                if (npt.end_token.is_value("ИНТЕРЕС", None)): 
                    return None
        if (res is not None and ((res.typ == "производитель" or res.typ == "завод"))): 
            tt1 = res.end_token.next0_
            if (res.typ == "завод"): 
                if ((tt1 is not None and tt1.is_value("ПО", None) and tt1.next0_ is not None) and tt1.next0_.is_value("ПРОИЗВОДСТВО", None)): 
                    tt1 = tt1.next0_.next0_
            npt = NounPhraseHelper.try_parse(tt1, NounPhraseParseAttr.NO, 0)
            if ((npt is not None and (res.whitespaces_after_count < 2) and tt1.chars.is_all_lower) and npt.morph.case.is_genitive): 
                str0_ = MiscHelper.get_text_value_of_meta_token(npt, GetTextAttr.NO)
                res.name = "{0} {1}".format(Utils.ifNotNull(res.name, (res.typ.upper() if res is not None and res.typ is not None else None)), str0_)
                if (res.geo is not None): 
                    res.coef += 1
                res.end_token = npt.end_token
            elif (res.typ != "завод"): 
                return None
        if (res is not None and (isinstance(res.begin_token.previous, TextToken)) and ((res.typ == "милиция" or res.typ == "полиция"))): 
            tok = OrgItemTypeToken.__m_global.try_attach(res.begin_token.previous, None, False)
            if (tok is not None): 
                return None
        if (res is not None and res.typ == "предприятие"): 
            if (res.alt_typ == "головное предприятие" or res.alt_typ == "дочернее предприятие"): 
                res.is_not_typ = True
            elif (t.previous is not None and ((t.previous.is_value("ГОЛОВНОЙ", None) or t.previous.is_value("ДОЧЕРНИЙ", None)))): 
                return None
        if (res is not None and res.is_douter_org): 
            res.is_not_typ = True
            if (res.begin_token != res.end_token): 
                res1 = OrgItemTypeToken.__try_attach(res.begin_token.next0_, True)
                if (res1 is not None and not res1.is_doubt_root_word): 
                    res.is_not_typ = False
        if (res is not None and res.typ == "суд"): 
            tt1 = (res.end_token if isinstance(res.end_token, TextToken) else None)
            if (tt1 is not None and ((tt1.term == "СУДА" or tt1.term == "СУДОВ"))): 
                if ((((res.morph.number) & (MorphNumber.PLURAL))) != (MorphNumber.UNDEFINED)): 
                    return None
        if (res is not None and res.typ == "кафедра" and (isinstance(t, TextToken))): 
            if (t.is_value("КАФЕ", None) and ((t.next0_ is None or not t.next0_.is_char('.')))): 
                return None
        if (res is not None and res.typ == "компания"): 
            if ((t.previous is not None and t.previous.is_hiphen and t.previous.previous is not None) and t.previous.previous.is_value("КАЮТ", None)): 
                return None
        if (res is not None and t.previous is not None): 
            if (res.morph.case.is_genitive): 
                if (t.previous.is_value("СТАНДАРТ", None)): 
                    return None
        if (res is not None and res.typ == "радиостанция" and res.name_words_count > 1): 
            return None
        if ((res is not None and res.typ == "предприятие" and res.alt_typ is not None) and res.begin_token.morph.class0_.is_adjective and not res.root.is_pure_prefix): 
            res.typ = res.alt_typ
            res.alt_typ = (None)
            res.coef = 3
        if (res is not None): 
            npt = NounPhraseHelper.try_parse(res.end_token.next0_, NounPhraseParseAttr.NO, 0)
            if (npt is not None and ((npt.noun.is_value("ТИП", None) or npt.noun.is_value("РЕЖИМ", None))) and npt.morph.case.is_genitive): 
                res.end_token = npt.end_token
                s = "{0} {1}".format(res.typ, MiscHelper.get_text_value_of_meta_token(npt, GetTextAttr.NO)).lower()
                if ("колония" in res.typ or "тюрьма" in res.typ): 
                    res.coef = 3
                    res.alt_typ = s
                elif (res.name is None or len(res.name) == len(res.typ)): 
                    res.name = s
                else: 
                    res.alt_typ = s
        if (res is not None and OrgProfile.EDUCATION in res.profiles and (isinstance(res.end_token.next0_, TextToken))): 
            tt1 = res.end_token.next0_
            if ((tt1 if isinstance(tt1, TextToken) else None).term == "ВПО" or (tt1 if isinstance(tt1, TextToken) else None).term == "СПО"): 
                res.end_token = res.end_token.next0_
            else: 
                nnt = NounPhraseHelper.try_parse(tt1, NounPhraseParseAttr.NO, 0)
                if (nnt is not None and nnt.end_token.is_value("ОБРАЗОВАНИЕ", "ОСВІТА")): 
                    res.end_token = nnt.end_token
        if (res is not None and res.root is not None and res.root.is_pure_prefix): 
            tt1 = res.end_token.next0_
            if (tt1 is not None and ((tt1.is_value("С", None) or tt1.is_value("C", None)))): 
                npt = NounPhraseHelper.try_parse(tt1.next0_, NounPhraseParseAttr.NO, 0)
                if (npt is not None and ((npt.noun.is_value("ИНВЕСТИЦИЯ", None) or npt.noun.is_value("ОТВЕТСТВЕННОСТЬ", None)))): 
                    res.end_token = npt.end_token
        if (res is not None and res.root == OrgItemTypeToken.__m_military_unit and res.end_token.next0_ is not None): 
            if (res.end_token.next0_.is_value("ПП", None)): 
                res.end_token = res.end_token.next0_
            elif (res.end_token.next0_.is_value("ПОЛЕВОЙ", None) and res.end_token.next0_.next0_ is not None and res.end_token.next0_.next0_.is_value("ПОЧТА", None)): 
                res.end_token = res.end_token.next0_.next0_
        if (res is not None): 
            if (res.name_words_count > 1 and res.typ == "центр"): 
                res.can_be_dep_before_organization = True
            elif (LanguageHelper.ends_with(res.typ, " центр")): 
                res.can_be_dep_before_organization = True
        if (res is not None or not ((isinstance(t, TextToken)))): 
            return res
        tt = (t if isinstance(t, TextToken) else None)
        term = tt.term
        if (tt.chars.is_all_upper and (((term == "CRM" or term == "IT" or term == "ECM") or term == "BPM" or term == "HR"))): 
            tt2 = t.next0_
            if (tt2 is not None and tt2.is_hiphen): 
                tt2 = tt2.next0_
            res = OrgItemTypeToken.__try_attach(tt2, True)
            if (res is not None and res.root is not None and OrgProfile.UNIT in res.root.profiles): 
                res.name = "{0} {1}".format(Utils.ifNotNull(res.name, (res.root.canonic_text if res is not None and res.root is not None else None)), term)
                res.begin_token = t
                res.coef = 5
                return res
        if (term == "ВЧ"): 
            tt1 = t.next0_
            if (tt1 is not None and tt1.is_value("ПП", None)): 
                res = OrgItemTypeToken._new2150(t, tt1, 3)
            elif ((isinstance(tt1, NumberToken)) and (tt1.whitespaces_before_count < 3)): 
                res = OrgItemTypeToken(t, t)
            elif (MiscHelper.check_number_prefix(tt1) is not None): 
                res = OrgItemTypeToken(t, t)
            elif (((isinstance(tt1, TextToken)) and not tt1.is_whitespace_after and tt1.chars.is_letter) and tt1.length_char == 1): 
                res = OrgItemTypeToken(t, t)
            if (res is not None): 
                res.root = OrgItemTypeToken.__m_military_unit
                res.typ = OrgItemTypeToken.__m_military_unit.canonic_text.lower()
                res.profiles.append(OrgProfile.ARMY)
                return res
        if (term == "КБ"): 
            cou = 0
            ok = False
            ttt = t.next0_
            while ttt is not None and (cou < 30): 
                if (ttt.is_value("БАНК", None)): 
                    ok = True
                    break
                r = ttt.get_referent()
                if (r is not None and r.type_name == "URI"): 
                    vv = r.get_string_value("SCHEME")
                    if ((vv == "БИК" or vv == "Р/С" or vv == "К/С") or vv == "ОКАТО"): 
                        ok = True
                        break
                ttt = ttt.next0_; cou += 1
            if (ok): 
                res = OrgItemTypeToken(t, t)
                res.typ = "коммерческий банк"
                res.profiles.append(OrgProfile.FINANCE)
                res.coef = 3
                return res
        if (term == "ТП" or term == "МП"): 
            num = OrgItemNumberToken.try_attach(t.next0_, True, None)
            if (num is not None and num.end_token.next0_ is not None): 
                tt1 = num.end_token.next0_
                if (tt1.is_comma and tt1.next0_ is not None): 
                    tt1 = tt1.next0_
                oo = (tt1.get_referent() if isinstance(tt1.get_referent(), OrganizationReferent) else None)
                if (oo is not None): 
                    if ("МИГРАЦ" in str(oo).upper()): 
                        res = OrgItemTypeToken._new2151(t, t, ("территориальный пункт" if term == "ТП" else "миграционный пункт"), 4, True)
                        return res
        if (tt.chars.is_all_upper and term == "МГТУ"): 
            if (tt.next0_.is_value("БАНК", None) or (((isinstance(tt.next0_.get_referent(), OrganizationReferent)) and (tt.next0_.get_referent() if isinstance(tt.next0_.get_referent(), OrganizationReferent) else None).kind == OrganizationKind.BANK)) or ((tt.previous is not None and tt.previous.is_value("ОПЕРУ", None)))): 
                res = OrgItemTypeToken._new2152(tt, tt, "главное территориальное управление")
                res.alt_typ = "ГТУ"
                res.name = "МОСКОВСКОЕ"
                res.name_is_name = True
                res.alt_name = "МГТУ"
                res.coef = 3
                res.root = OrgItemTermin(res.name)
                res.profiles.append(OrgProfile.UNIT)
                tt.term = "МОСКОВСКИЙ"
                res.geo = tt.kit.process_referent("GEO", tt)
                tt.term = "МГТУ"
                return res
        if (tt.is_value("СОВЕТ", "РАДА")): 
            if (tt.next0_ is not None and tt.next0_.is_value("ПРИ", None)): 
                rt = tt.kit.process_referent("PERSONPROPERTY", tt.next0_.next0_)
                if (rt is not None): 
                    res = OrgItemTypeToken(tt, tt)
                    res.typ = "совет"
                    res.is_dep = True
                    res.coef = 2
                    return res
        say = False
        if ((((term == "СООБЩАЕТ" or term == "СООБЩЕНИЮ" or term == "ПИШЕТ") or term == "ПЕРЕДАЕТ" or term == "ПОВІДОМЛЯЄ") or term == "ПОВІДОМЛЕННЯМ" or term == "ПИШЕ") or term == "ПЕРЕДАЄ"): 
            say = True
        if (((say or tt.is_value("ОБЛОЖКА", "ОБКЛАДИНКА") or tt.is_value("РЕДАКТОР", None)) or tt.is_value("КОРРЕСПОНДЕНТ", "КОРЕСПОНДЕНТ") or tt.is_value("ЖУРНАЛИСТ", "ЖУРНАЛІСТ")) or term == "ИНТЕРВЬЮ" or term == "ІНТЕРВЮ"): 
            if (OrgItemTypeToken.__m_pressru is None): 
                OrgItemTypeToken.__m_pressru = OrgItemTermin._new2153("ИЗДАНИЕ", MorphLang.RU, OrgProfile.MEDIA, True, 4)
            if (OrgItemTypeToken.__m_pressua is None): 
                OrgItemTypeToken.__m_pressua = OrgItemTermin._new2153("ВИДАННЯ", MorphLang.UA, OrgProfile.MEDIA, True, 4)
            pres = (OrgItemTypeToken.__m_pressua if tt.kit.base_language.is_ua else OrgItemTypeToken.__m_pressru)
            t1 = t.next0_
            if (t1 is None): 
                return None
            if (t1.chars.is_latin_letter and not t1.chars.is_all_lower): 
                if (tt.is_value("РЕДАКТОР", None)): 
                    return None
                return OrgItemTypeToken._new2155(t, t, pres.canonic_text.lower(), pres, True)
            if (not say): 
                br = BracketHelper.try_parse(t1, BracketParseAttr.NO, 100)
                if ((br is not None and br.is_quote_type and not t1.next0_.chars.is_all_lower) and ((br.end_char - br.begin_char) < 40)): 
                    return OrgItemTypeToken._new2155(t, t, pres.canonic_text.lower(), pres, True)
            npt = NounPhraseHelper.try_parse(t1, NounPhraseParseAttr.NO, 0)
            if (npt is not None and npt.end_token.next0_ is not None): 
                t1 = npt.end_token.next0_
                root_ = npt.noun.get_normal_case_text(MorphClass(), False, MorphGender.UNDEFINED, False)
                ok = t1.chars.is_latin_letter and not t1.chars.is_all_lower
                if (not ok and BracketHelper.can_be_start_of_sequence(t1, True, False)): 
                    ok = True
                if (ok): 
                    if ((root_ == "ИЗДАНИЕ" or root_ == "ИЗДАТЕЛЬСТВО" or root_ == "ЖУРНАЛ") or root_ == "ВИДАННЯ" or root_ == "ВИДАВНИЦТВО"): 
                        res = OrgItemTypeToken._new2152(npt.begin_token, npt.end_token, root_.lower())
                        res.profiles.append(OrgProfile.MEDIA)
                        res.profiles.append(OrgProfile.PRESS)
                        if (len(npt.adjectives) > 0): 
                            for a in npt.adjectives: 
                                rt1 = res.kit.process_referent("GEO", a.begin_token)
                                if (rt1 is not None and rt1.morph.class0_.is_adjective): 
                                    if (res.geo is None): 
                                        res.geo = rt1
                                    else: 
                                        res.geo2 = rt1
                            res.alt_typ = npt.get_normal_case_text(MorphClass(), False, MorphGender.UNDEFINED, False).lower()
                        res.root = OrgItemTermin._new2158(root_, True, 4)
                        return res
            rt = t1.kit.process_referent("GEO", t1)
            if (rt is not None and rt.morph.class0_.is_adjective): 
                if (rt.end_token.next0_ is not None and rt.end_token.next0_.chars.is_latin_letter): 
                    res = OrgItemTypeToken._new2159(t1, rt.end_token, pres.canonic_text.lower(), pres)
                    res.geo = rt
                    return res
            tt1 = t1
            if (BracketHelper.can_be_start_of_sequence(tt1, True, False)): 
                tt1 = t1.next0_
            if ((((tt1.chars.is_latin_letter and tt1.next0_ is not None and tt1.next0_.is_char('.')) and tt1.next0_.next0_ is not None and tt1.next0_.next0_.chars.is_latin_letter) and (tt1.next0_.next0_.length_char < 4) and tt1.next0_.next0_.length_char > 1) and not tt1.next0_.is_whitespace_after): 
                if (tt1 != t1 and not BracketHelper.can_be_end_of_sequence(tt1.next0_.next0_.next0_, True, t1, False)): 
                    pass
                else: 
                    res = OrgItemTypeToken._new2159(t1, tt1.next0_.next0_, pres.canonic_text.lower(), pres)
                    res.name = MiscHelper.get_text_value(t1, tt1.next0_.next0_, GetTextAttr.NO).replace(" ", "")
                    if (tt1 != t1): 
                        res.end_token = res.end_token.next0_
                    res.coef = 4
                return res
        elif ((t.is_value("ЖУРНАЛ", None) or t.is_value("ИЗДАНИЕ", None) or t.is_value("ИЗДАТЕЛЬСТВО", None)) or t.is_value("ВИДАННЯ", None) or t.is_value("ВИДАВНИЦТВО", None)): 
            ok = False
            if (ad is not None): 
                ot_ex_li = ad.local_ontology.try_attach(t.next0_, None, False)
                if (ot_ex_li is None and t.kit.ontology is not None): 
                    ot_ex_li = t.kit.ontology.attach_token(OrganizationReferent.OBJ_TYPENAME, t.next0_)
                if ((ot_ex_li is not None and len(ot_ex_li) > 0 and ot_ex_li[0].item is not None) and (isinstance(ot_ex_li[0].item.referent, OrganizationReferent))): 
                    if ((ot_ex_li[0].item.referent if isinstance(ot_ex_li[0].item.referent, OrganizationReferent) else None).kind == OrganizationKind.PRESS): 
                        ok = True
            if (t.next0_ is not None and t.next0_.chars.is_latin_letter and not t.next0_.chars.is_all_lower): 
                ok = True
            if (ok): 
                res = OrgItemTypeToken._new2152(t, t, t.get_normal_case_text(MorphClass(), False, MorphGender.UNDEFINED, False).lower())
                res.profiles.append(OrgProfile.MEDIA)
                res.profiles.append(OrgProfile.PRESS)
                res.root = OrgItemTermin._new2162(t.get_normal_case_text(MorphClass(), False, MorphGender.UNDEFINED, False), OrgItemTermin.Types.ORG, 3, True)
                res.morph = t.morph
                res.chars = t.chars
                if (t.previous is not None and t.previous.morph.class0_.is_adjective): 
                    rt = t.kit.process_referent("GEO", t.previous)
                    if (rt is not None and rt.end_token == t.previous): 
                        res.begin_token = t.previous
                        res.geo = rt
                return res
        elif ((term == "МО" and t.chars.is_all_upper and (isinstance(t.next0_, ReferentToken))) and (isinstance(t.next0_.get_referent(), GeoReferent))): 
            geo_ = (t.next0_.get_referent() if isinstance(t.next0_.get_referent(), GeoReferent) else None)
            if (geo_ is not None and geo_.is_state): 
                res = OrgItemTypeToken._new2163(t, t, "министерство", "МИНИСТЕРСТВО ОБОРОНЫ", 4, OrgItemTypeToken.__m_mo)
                res.profiles.append(OrgProfile.STATE)
                res.can_be_organization = True
                return res
        elif (term == "ИК" and t.chars.is_all_upper): 
            et = None
            if (OrgItemNumberToken.try_attach(t.next0_, False, None) is not None): 
                et = t
            elif (t.next0_ is not None and (isinstance(t.next0_, NumberToken))): 
                et = t
            elif ((t.next0_ is not None and t.next0_.is_hiphen and t.next0_.next0_ is not None) and (isinstance(t.next0_.next0_, NumberToken))): 
                et = t.next0_
            if (et is not None): 
                return OrgItemTypeToken._new2164(t, et, "исправительная колония", "колония", OrgItemTypeToken.__m_ispr_kolon, True)
        elif (t.is_value("ПАКЕТ", None) and t.next0_ is not None and t.next0_.is_value("АКЦИЯ", "АКЦІЯ")): 
            return OrgItemTypeToken._new2165(t, t.next0_, 4, True, "")
        else: 
            tok = OrgItemTypeToken._m_pref_words.try_parse(t, TerminParseAttr.NO)
            if (tok is not None and tok.tag is not None): 
                if ((tok.whitespaces_after_count < 2) and BracketHelper.can_be_start_of_sequence(tok.end_token.next0_, True, False)): 
                    return OrgItemTypeToken._new2165(t, tok.end_token, 4, True, "")
        if (res is None and term == "АК" and t.chars.is_all_upper): 
            if (OrgItemTypeToken.try_attach(t.next0_, can_be_first_letter_lower, ad) is not None): 
                return OrgItemTypeToken._new2167(t, t, OrgItemTypeToken.__m_akcion_comp, OrgItemTypeToken.__m_akcion_comp.canonic_text.lower())
        if (term == "В"): 
            if ((t.next0_ is not None and t.next0_.is_char_of("\\/") and t.next0_.next0_ is not None) and t.next0_.next0_.is_value("Ч", None)): 
                if (OrgItemNumberToken.try_attach(t.next0_.next0_.next0_, True, None) is not None): 
                    return OrgItemTypeToken._new2167(t, t.next0_.next0_, OrgItemTypeToken.__m_military_unit, OrgItemTypeToken.__m_military_unit.canonic_text.lower())
        if (t.morph.class0_.is_adjective and t.next0_ is not None and ((t.next0_.chars.is_all_upper or t.next0_.chars.is_last_lower))): 
            if (t.chars.is_capital_upper or (((t.previous is not None and t.previous.is_hiphen and t.previous.previous is not None) and t.previous.previous.chars.is_capital_upper))): 
                res1 = OrgItemTypeToken.__try_attach(t.next0_, True)
                if ((res1 is not None and res1.end_token == t.next0_ and res1.name is None) and res1.root is not None): 
                    res1.begin_token = t
                    res1.coef = 5
                    gen = MorphGender.UNDEFINED
                    for ii in range(len(res1.root.canonic_text) - 1, -1, -1):
                        if (ii == 0 or res1.root.canonic_text[ii - 1] == ' '): 
                            mm = Morphology.get_word_base_info(res1.root.canonic_text[ii:], MorphLang(), False, False)
                            gen = mm.gender
                            break
                    nam = t.get_normal_case_text(MorphClass.ADJECTIVE, True, gen, False)
                    if (((t.previous is not None and t.previous.is_hiphen and (isinstance(t.previous.previous, TextToken))) and t.previous.previous.chars.is_capital_upper and not t.is_whitespace_before) and not t.previous.is_whitespace_before): 
                        res1.begin_token = t.previous.previous
                        nam = "{0}-{1}".format((res1.begin_token if isinstance(res1.begin_token, TextToken) else None).term, nam)
                    res1.name = nam
                    return res1
        if (t.morph.class0_.is_adjective and not t.chars.is_all_lower and (t.whitespaces_after_count < 2)): 
            res1 = OrgItemTypeToken.__try_attach(t.next0_, True)
            if ((res1 is not None and OrgProfile.TRANSPORT in res1.profiles and res1.name is None) and res1.root is not None): 
                nam = t.get_normal_case_text(MorphClass.ADJECTIVE, True, (MorphGender.FEMINIE if res1.root.canonic_text.endswith("ДОРОГА") else MorphGender.MASCULINE), False)
                if (nam is not None): 
                    if (((t.previous is not None and t.previous.is_hiphen and (isinstance(t.previous.previous, TextToken))) and t.previous.previous.chars.is_capital_upper and not t.is_whitespace_before) and not t.previous.is_whitespace_before): 
                        t = t.previous.previous
                        nam = "{0}-{1}".format((t if isinstance(t, TextToken) else None).term, nam)
                    res1.begin_token = t
                    res1.coef = 5
                    res1.name = "{0} {1}".format(nam, res1.root.canonic_text)
                    res1.can_be_organization = True
                    return res1
        return res
    
    __m_pressru = None
    
    __m_pressua = None
    
    __m_pressia = None
    
    __m_military_unit = None
    
    @staticmethod
    def __try_attach(t : 'Token', can_be_first_letter_lower : bool) -> 'OrgItemTypeToken':
        from pullenti.ner._org.internal.OrgItemTermin import OrgItemTermin
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.morph.MorphClass import MorphClass
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.geo.GeoReferent import GeoReferent
        from pullenti.ner.core.MiscHelper import MiscHelper
        if (t is None): 
            return None
        li = OrgItemTypeToken.__m_global.try_attach(t, None, False)
        if (li is not None): 
            if (t.previous is not None and t.previous.is_hiphen and not t.is_whitespace_before): 
                li1 = OrgItemTypeToken.__m_global.try_attach(t.previous.previous, None, False)
                if (li1 is not None and li1[0].end_token == li[0].end_token): 
                    return None
            res = OrgItemTypeToken(li[0].begin_token, li[0].end_token)
            res.root = (li[0].termin if isinstance(li[0].termin, OrgItemTermin) else None)
            nn = NounPhraseHelper.try_parse(li[0].begin_token, NounPhraseParseAttr.NO, 0)
            if (nn is not None and ((nn.end_token.next0_ is None or not nn.end_token.next0_.is_char('.')))): 
                res.morph = nn.morph
            else: 
                res.morph = li[0].morph
            res.chars_root = res.chars
            if (res.root.is_pure_prefix): 
                res.typ = res.root.acronym
                if (res.typ is None): 
                    res.typ = res.root.canonic_text.lower()
            else: 
                res.typ = res.root.canonic_text.lower()
            if (res.begin_token != res.end_token and not res.root.is_pure_prefix): 
                npt0 = NounPhraseHelper.try_parse(res.begin_token, NounPhraseParseAttr.NO, 0)
                if (npt0 is not None and npt0.end_token == res.end_token and len(npt0.adjectives) >= res.name_words_count): 
                    s = npt0.get_normal_case_text(MorphClass(), True, MorphGender.UNDEFINED, False)
                    if (Utils.compareStrings(s, res.typ, True) != 0): 
                        res.name = s
                        res.can_be_organization = True
            if (res.typ == "сберегательный банк" and res.name is None): 
                res.name = res.typ.upper()
                res.typ = "банк"
            if (res.is_dep and res.typ.startswith("отдел ") and res.name is None): 
                res.name = res.typ.upper()
                res.typ = "отдел"
            if (res.begin_token == res.end_token): 
                if (res.chars.is_capital_upper): 
                    if ((res.length_char < 4) and not res.begin_token.is_value(res.root.canonic_text, None)): 
                        if (not can_be_first_letter_lower): 
                            return None
                if (res.chars.is_all_upper): 
                    if (res.begin_token.is_value("САН", None)): 
                        return None
            if (res.end_token.next0_ is not None and res.end_token.next0_.is_char('(')): 
                li22 = OrgItemTypeToken.__m_global.try_attach(res.end_token.next0_.next0_, None, False)
                if ((li22 is not None and len(li22) > 0 and li22[0].termin == li[0].termin) and li22[0].end_token.next0_ is not None and li22[0].end_token.next0_.is_char(')')): 
                    res.end_token = li22[0].end_token.next0_
            return res
        if ((isinstance(t, NumberToken)) and t.morph.class0_.is_adjective): 
            pass
        elif (isinstance(t, TextToken)): 
            pass
        else: 
            return None
        if (t.is_value("СБ", None)): 
            if (t.next0_ is not None and (isinstance(t.next0_.get_referent(), GeoReferent))): 
                return OrgItemTypeToken._new2169(t, t, "банк", OrgItemTypeToken.__m_sber_bank, OrgItemTypeToken.__m_sber_bank.canonic_text)
        npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.IGNOREADJBEST, 0)
        if (npt is None or npt.internal_noun is not None): 
            if (((not t.chars.is_all_lower and t.next0_ is not None and t.next0_.is_hiphen) and not t.is_whitespace_after and not t.next0_.is_whitespace_after) and t.next0_.next0_ is not None and t.next0_.next0_.is_value("БАНК", None)): 
                s = t.get_normal_case_text(MorphClass(), False, MorphGender.UNDEFINED, False)
                res = OrgItemTypeToken._new2170(t, t.next0_.next0_, s, t.next0_.next0_.morph, t.chars, t.next0_.next0_.chars)
                res.root = OrgItemTypeToken.__m_bank
                res.typ = "банк"
                return res
            if ((isinstance(t, NumberToken)) and (t.whitespaces_after_count < 3) and (isinstance(t.next0_, TextToken))): 
                res11 = OrgItemTypeToken.__try_attach(t.next0_, False)
                if (res11 is not None and res11.root is not None and res11.root.can_has_number): 
                    res11.begin_token = t
                    res11.number = str((t if isinstance(t, NumberToken) else None).value)
                    res11.coef += 1
                    return res11
            return None
        if (npt.morph.gender == MorphGender.FEMINIE and npt.noun.get_normal_case_text(MorphClass(), False, MorphGender.UNDEFINED, False) == "БАНКА"): 
            return None
        if (npt.begin_token == npt.end_token): 
            s = npt.get_normal_case_text(MorphClass(), False, MorphGender.UNDEFINED, False)
            if (LanguageHelper.ends_with_ex(s, "БАНК", "БАНКА", "БАНОК", None)): 
                if (LanguageHelper.ends_with(s, "БАНКА")): 
                    s = s[0:0+len(s) - 1]
                elif (LanguageHelper.ends_with(s, "БАНОК")): 
                    s = (s[0:0+len(s) - 2] + "К")
                res = OrgItemTypeToken._new2170(npt.begin_token, npt.end_token, s, npt.morph, npt.chars, npt.chars)
                res.root = OrgItemTypeToken.__m_bank
                res.typ = "банк"
                return res
            return None
        tt = npt.end_token
        first_pass3952 = True
        while True:
            if first_pass3952: first_pass3952 = False
            else: tt = tt.previous
            if (not (tt is not None)): break
            if (tt == npt.begin_token): 
                break
            lii = OrgItemTypeToken.__m_global.try_attach(tt, None, False)
            if (lii is not None): 
                if (tt == npt.end_token and tt.previous is not None and tt.previous.is_hiphen): 
                    continue
                li = lii
                if (li[0].end_char < npt.end_char): 
                    npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.IGNOREADJBEST, li[0].end_char)
                break
        if (li is None or npt is None): 
            return None
        res = OrgItemTypeToken(npt.begin_token, li[0].end_token)
        for a in npt.adjectives: 
            if (a.is_value("ДОЧЕРНИЙ", None) or a.is_value("ДОЧІРНІЙ", None)): 
                res.is_douter_org = True
                break
        for em in OrgItemTypeToken.M_EMPTY_TYP_WORDS: 
            for a in npt.adjectives: 
                if (a.is_value(em, None)): 
                    npt.adjectives.remove(a)
                    break
        while len(npt.adjectives) > 0:
            if (npt.adjectives[0].begin_token.get_morph_class_in_dictionary().is_verb): 
                del npt.adjectives[0]
            elif (isinstance(npt.adjectives[0].begin_token, NumberToken)): 
                res.number = str((npt.adjectives[0].begin_token if isinstance(npt.adjectives[0].begin_token, NumberToken) else None).value)
                del npt.adjectives[0]
            else: 
                break
        if (len(npt.adjectives) > 0): 
            res.alt_typ = npt.get_normal_case_text(MorphClass(), True, MorphGender.UNDEFINED, False)
            if (li[0].end_char > npt.end_char): 
                res.alt_typ = "{0} {1}".format(res.alt_typ, MiscHelper.get_text_value(npt.end_token.next0_, li[0].end_token, GetTextAttr.NO))
        if (res.number is None): 
            while len(npt.adjectives) > 0:
                if (not npt.adjectives[0].chars.is_all_lower or can_be_first_letter_lower): 
                    break
                if (npt.kit.process_referent("GEO", npt.adjectives[0].begin_token) is not None): 
                    break
                if (OrgItemTypeToken.is_std_adjective(npt.adjectives[0], False)): 
                    break
                bad = False
                if (not npt.noun.chars.is_all_lower or not OrgItemTypeToken.is_std_adjective(npt.adjectives[0], False)): 
                    bad = True
                else: 
                    i = 1
                    first_pass3953 = True
                    while True:
                        if first_pass3953: first_pass3953 = False
                        else: i += 1
                        if (not (i < len(npt.adjectives))): break
                        if (npt.kit.process_referent("GEO", npt.adjectives[i].begin_token) is not None): 
                            continue
                        if (not npt.adjectives[i].chars.is_all_lower): 
                            bad = True
                            break
                if (not bad): 
                    break
                del npt.adjectives[0]
        for a in npt.adjectives: 
            r = npt.kit.process_referent("GEO", a.begin_token)
            if (r is not None): 
                if (a == npt.adjectives[0]): 
                    res2 = OrgItemTypeToken.__try_attach(a.end_token.next0_, True)
                    if (res2 is not None and res2.end_char > npt.end_char and res2.geo is None): 
                        res2.begin_token = a.begin_token
                        res2.geo = r
                        return res2
                if (res.geo is None): 
                    res.geo = r
                elif (res.geo2 is None): 
                    res.geo2 = r
        if (res.end_token == npt.end_token): 
            res.name = npt.get_normal_case_text(MorphClass(), True, MorphGender.UNDEFINED, False)
        if (res.name == res.alt_typ): 
            res.alt_typ = (None)
        if (res.alt_typ is not None): 
            res.alt_typ = res.alt_typ.lower().replace('-', ' ')
        res.root = (li[0].termin if isinstance(li[0].termin, OrgItemTermin) else None)
        if (res.root.is_pure_prefix and (li[0].length_char < 7)): 
            return None
        res.typ = res.root.canonic_text.lower()
        if (len(npt.adjectives) > 0): 
            i = 0
            while i < len(npt.adjectives): 
                s = npt.get_normal_case_text_without_adjective(i)
                ctli = OrgItemTypeToken.__m_global.find_termin_by_canonic_text(s)
                if (ctli is not None and len(ctli) > 0 and (isinstance(ctli[0], OrgItemTermin))): 
                    res.root = (ctli[0] if isinstance(ctli[0], OrgItemTermin) else None)
                    if (res.alt_typ is None): 
                        res.alt_typ = res.root.canonic_text.lower()
                        if (res.alt_typ == res.typ): 
                            res.alt_typ = (None)
                    break
                i += 1
            res.coef = res.root.coeff
            if (res.coef == 0): 
                i = 0
                while i < len(npt.adjectives): 
                    if (OrgItemTypeToken.is_std_adjective(npt.adjectives[i], True)): 
                        res.coef += 1
                        if (((i + 1) < len(npt.adjectives)) and not OrgItemTypeToken.is_std_adjective(npt.adjectives[i + 1], False)): 
                            res.coef += 1
                        if (npt.adjectives[i].is_value("ФЕДЕРАЛЬНЫЙ", "ФЕДЕРАЛЬНИЙ") or npt.adjectives[i].is_value("ГОСУДАРСТВЕННЫЙ", "ДЕРЖАВНИЙ")): 
                            res.is_doubt_root_word = False
                            if (res.is_dep): 
                                res.is_dep = False
                    elif (OrgItemTypeToken.is_std_adjective(npt.adjectives[i], False)): 
                        res.coef += .5
                    i += 1
            else: 
                i = 0
                while i < (len(npt.adjectives) - 1): 
                    if (OrgItemTypeToken.is_std_adjective(npt.adjectives[i], True)): 
                        if (((i + 1) < len(npt.adjectives)) and not OrgItemTypeToken.is_std_adjective(npt.adjectives[i + 1], True)): 
                            res.coef += 1
                            res.is_doubt_root_word = False
                            res.can_be_organization = True
                            if (res.is_dep): 
                                res.is_dep = False
                    i += 1
        res.morph = npt.morph
        res.chars = npt.chars
        if (not res.chars.is_all_upper and not res.chars.is_capital_upper and not res.chars.is_all_lower): 
            res.chars = npt.noun.chars
            if (res.chars.is_all_lower): 
                res.chars = res.begin_token.chars
        if (npt.noun is not None): 
            res.chars_root = npt.noun.chars
        return res
    
    @staticmethod
    def is_std_adjective(t : 'Token', only_federal : bool=False) -> bool:
        if (t is None): 
            return False
        if (t.morph.language.is_ua): 
            for a in OrgItemTypeToken.__m_org_adjactivesua: 
                if (t.is_value(a, None)): 
                    return True
            if (not only_federal): 
                for a in OrgItemTypeToken.__m_org_adjactives2ua: 
                    if (t.is_value(a, None)): 
                        return True
        else: 
            for a in OrgItemTypeToken.__m_org_adjactives: 
                if (t.is_value(a, None)): 
                    return True
            if (not only_federal): 
                for a in OrgItemTypeToken.__m_org_adjactives2: 
                    if (t.is_value(a, None)): 
                        return True
        return False
    
    __m_org_adjactives = None
    
    __m_org_adjactivesua = None
    
    __m_org_adjactives2 = None
    
    __m_org_adjactives2ua = None
    
    @staticmethod
    def check_org_special_word_before(t : 'Token') -> bool:
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.NumberToken import NumberToken
        if (t is None): 
            return False
        if (t.is_comma_and and t.previous is not None): 
            t = t.previous
        k = 0
        tt = t
        first_pass3954 = True
        while True:
            if first_pass3954: first_pass3954 = False
            else: tt = tt.previous
            if (not (tt is not None)): break
            r = tt.get_referent()
            if (r is not None): 
                if (tt == t and (isinstance(r, OrganizationReferent))): 
                    return True
                return False
            if (not ((isinstance(tt, TextToken)))): 
                if (not ((isinstance(tt, NumberToken)))): 
                    break
                k += 1
                continue
            if (tt.is_newline_after): 
                if (not tt.is_char(',')): 
                    return False
                continue
            if (tt.is_value("УПРАВЛЕНИЕ", None) or tt.is_value("УПРАВЛІННЯ", None)): 
                ty = OrgItemTypeToken.try_attach(tt.next0_, True, None)
                if (ty is not None and ty.is_doubt_root_word): 
                    return False
            if (tt == t and OrgItemTypeToken._m_pref_words.try_parse(tt, TerminParseAttr.NO) is not None): 
                return True
            if (tt == t and tt.is_char('.')): 
                continue
            ty = OrgItemTypeToken.try_attach(tt, True, None)
            if (ty is not None and ty.end_token.end_char <= t.end_char and ty.end_token == t): 
                if (not ty.is_doubt_root_word): 
                    return True
            if (tt.kit.recurse_level == 0): 
                rt = tt.kit.process_referent("PERSONPROPERTY", tt)
                if (rt is not None and rt.referent is not None and rt.referent.type_name == "PERSONPROPERTY"): 
                    if (rt.end_char >= t.end_char): 
                        return True
            k += 1
            if (k > 4): 
                break
        return False
    
    @staticmethod
    def check_person_property(t : 'Token') -> bool:
        if (t is None or not t.chars.is_cyrillic_letter): 
            return False
        tok = OrgItemTypeToken._m_pref_words.try_parse(t, TerminParseAttr.NO)
        if (tok is None): 
            return False
        if (tok.termin.tag is None): 
            return False
        return True
    
    @staticmethod
    def try_attach_reference_to_exist_org(t : 'Token') -> 'ReferentToken':
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.ReferentToken import ReferentToken
        if (not ((isinstance(t, TextToken)))): 
            return None
        tok = OrgItemTypeToken._m_key_words_for_refs.try_parse(t, TerminParseAttr.NO)
        if (tok is None and t.morph.class0_.is_pronoun): 
            tok = OrgItemTypeToken._m_key_words_for_refs.try_parse(t.next0_, TerminParseAttr.NO)
        abbr = None
        if (tok is None): 
            if (t.length_char > 1 and ((t.chars.is_capital_upper or t.chars.is_last_lower))): 
                abbr = (t if isinstance(t, TextToken) else None).get_lemma()
            else: 
                ty1 = OrgItemTypeToken.__try_attach(t, True)
                if (ty1 is not None): 
                    abbr = ty1.typ
                else: 
                    return None
        cou = 0
        tt = t.previous
        first_pass3955 = True
        while True:
            if first_pass3955: first_pass3955 = False
            else: tt = tt.previous
            if (not (tt is not None)): break
            if (tt.is_newline_after): 
                cou += 10
            cou += 1
            if (cou > 500): 
                break
            if (not ((isinstance(tt, ReferentToken)))): 
                continue
            refs = tt.get_referents()
            if (refs is None): 
                continue
            for r in refs: 
                if (isinstance(r, OrganizationReferent)): 
                    if (abbr is not None): 
                        if (r.find_slot(OrganizationReferent.ATTR_TYPE, abbr, True) is None): 
                            continue
                        rt = ReferentToken(r, t, t)
                        hi = (r.get_value(OrganizationReferent.ATTR_HIGHER) if isinstance(r.get_value(OrganizationReferent.ATTR_HIGHER), OrganizationReferent) else None)
                        if (hi is not None and t.next0_ is not None): 
                            for ty in hi.types: 
                                if (t.next0_.is_value(ty.upper(), None)): 
                                    rt.end_token = t.next0_
                                    break
                        return rt
                    if (tok.termin.tag is not None): 
                        ok = False
                        for ty in (r if isinstance(r, OrganizationReferent) else None).types: 
                            if (Utils.endsWithString(ty, tok.termin.canonic_text, True)): 
                                ok = True
                                break
                        if (not ok): 
                            continue
                    return ReferentToken(r, t, tok.end_token)
        return None
    
    @staticmethod
    def is_types_antagonisticoo(r1 : 'OrganizationReferent', r2 : 'OrganizationReferent') -> bool:
        k1 = r1.kind
        k2 = r2.kind
        if (k1 != OrganizationKind.UNDEFINED and k2 != OrganizationKind.UNDEFINED): 
            if (OrgItemTypeToken.is_types_antagonistickk(k1, k2)): 
                return True
        types1 = r1.types
        types2 = r2.types
        for t1 in types1: 
            if (t1 in types2): 
                return False
        for t1 in types1: 
            for t2 in types2: 
                if (OrgItemTypeToken.is_types_antagonisticss(t1, t2)): 
                    return True
        return False
    
    @staticmethod
    def is_type_accords(r1 : 'OrganizationReferent', t2 : 'OrgItemTypeToken') -> bool:
        if (t2 is None or t2.typ is None): 
            return False
        if (t2.typ == "министерство" or t2.typ == "міністерство" or t2.typ.endswith("штаб")): 
            return r1.find_slot(OrganizationReferent.ATTR_TYPE, t2.typ, True) is not None
        prs = r1.profiles
        for pr in prs: 
            if (pr in t2.profiles): 
                return True
        if (r1.find_slot(OrganizationReferent.ATTR_TYPE, None, True) is None): 
            if (len(prs) == 0): 
                return True
        if (len(t2.profiles) == 0): 
            if (OrgProfile.POLICY in prs): 
                if (t2.typ == "группа" or t2.typ == "организация"): 
                    return True
            if (OrgProfile.MUSIC in prs): 
                if (t2.typ == "группа"): 
                    return True
        for t in r1.types: 
            if (t == t2.typ): 
                return True
            if (t.endswith(t2.typ)): 
                return True
            if (t2.typ == "издание"): 
                if (t.endswith("агентство")): 
                    return True
        if ((t2.typ == "компания" or t2.typ == "корпорация" or t2.typ == "company") or t2.typ == "corporation"): 
            if (len(prs) == 0): 
                return True
            if (OrgProfile.BUSINESS in prs or OrgProfile.FINANCE in prs or OrgProfile.INDUSTRY in prs): 
                return True
        return False
    
    @staticmethod
    def is_types_antagonistictt(t1 : 'OrgItemTypeToken', t2 : 'OrgItemTypeToken') -> bool:
        k1 = OrgItemTypeToken._get_kind(t1.typ, Utils.ifNotNull(t1.name, ""), None)
        k2 = OrgItemTypeToken._get_kind(t2.typ, Utils.ifNotNull(t2.name, ""), None)
        if (k1 == OrganizationKind.JUSTICE and t2.typ.startswith("Ф")): 
            return False
        if (k2 == OrganizationKind.JUSTICE and t1.typ.startswith("Ф")): 
            return False
        if (OrgItemTypeToken.is_types_antagonistickk(k1, k2)): 
            return True
        if (OrgItemTypeToken.is_types_antagonisticss(t1.typ, t2.typ)): 
            return True
        if (k1 == OrganizationKind.BANK and k2 == OrganizationKind.BANK): 
            if (t1.name is not None and t2.name is not None and t1 != t2): 
                return True
        return False
    
    @staticmethod
    def is_types_antagonisticss(typ1 : str, typ2 : str) -> bool:
        if (typ1 == typ2): 
            return False
        uni = "{0} {1} ".format(typ1, typ2)
        if (("служба" in uni or "департамент" in uni or "инспекция" in uni) or "інспекція" in uni): 
            return True
        if ("министерство" in uni or "міністерство" in uni): 
            return True
        if ("правительство" in uni and not "администрация" in uni): 
            return True
        if ("уряд" in uni and not "адміністрація" in uni): 
            return True
        if (typ1 == "управление" and ((typ2 == "главное управление" or typ2 == "пограничное управление"))): 
            return True
        if (typ2 == "управление" and ((typ1 == "главное управление" or typ2 == "пограничное управление"))): 
            return True
        if (typ1 == "керування" and typ2 == "головне управління"): 
            return True
        if (typ2 == "керування" and typ1 == "головне управління"): 
            return True
        if (typ1 == "university"): 
            if (typ2 == "school" or typ2 == "college"): 
                return True
        if (typ2 == "university"): 
            if (typ1 == "school" or typ1 == "college"): 
                return True
        return False
    
    @staticmethod
    def is_types_antagonistickk(k1 : 'OrganizationKind', k2 : 'OrganizationKind') -> bool:
        if (k1 == k2): 
            return False
        if (k1 == OrganizationKind.DEPARTMENT or k2 == OrganizationKind.DEPARTMENT): 
            return False
        if (k1 == OrganizationKind.GOVENMENT or k2 == OrganizationKind.GOVENMENT): 
            return True
        if (k1 == OrganizationKind.JUSTICE or k2 == OrganizationKind.JUSTICE): 
            return True
        if (k1 == OrganizationKind.PARTY or k2 == OrganizationKind.PARTY): 
            return True
        if (k1 == OrganizationKind.STUDY): 
            k1 = OrganizationKind.SCIENCE
        if (k2 == OrganizationKind.STUDY): 
            k2 = OrganizationKind.SCIENCE
        if (k1 == OrganizationKind.PRESS): 
            k1 = OrganizationKind.MEDIA
        if (k2 == OrganizationKind.PRESS): 
            k2 = OrganizationKind.MEDIA
        if (k1 == k2): 
            return False
        if (k1 == OrganizationKind.UNDEFINED or k2 == OrganizationKind.UNDEFINED): 
            return False
        return True
    
    @staticmethod
    def check_kind(obj : 'OrganizationReferent') -> 'OrganizationKind':
        t = io.StringIO()
        n = io.StringIO()
        for s in obj.slots: 
            if (s.type_name == OrganizationReferent.ATTR_NAME): 
                print("{0};".format(s.value), end="", file=n, flush=True)
            elif (s.type_name == OrganizationReferent.ATTR_TYPE): 
                print("{0};".format(s.value), end="", file=t, flush=True)
        return OrgItemTypeToken._get_kind(Utils.toStringStringIO(t), Utils.toStringStringIO(n), obj)
    
    @staticmethod
    def _get_kind(t : str, n : str, r : 'OrganizationReferent'=None) -> 'OrganizationKind':
        if (not LanguageHelper.ends_with(t, ";")): 
            t += ";"
        if ((((((((((((("министерство" in t or "правительство" in t or "администрация" in t) or "префектура" in t or "мэрия;" in t) or "муниципалитет" in t or LanguageHelper.ends_with(t, "совет;")) or "дума;" in t or "собрание;" in t) or "кабинет" in t or "сенат;" in t) or "палата" in t or "рада;" in t) or "парламент;" in t or "конгресс" in t) or "комиссия" in t or "полиция;" in t) or "милиция;" in t or "хурал" in t) or "суглан" in t or "меджлис;" in t) or "хасе;" in t or "ил тумэн" in t) or "курултай" in t or "бундестаг" in t) or "бундесрат" in t): 
            return OrganizationKind.GOVENMENT
        if (((((((((((("міністерство" in t or "уряд" in t or "адміністрація" in t) or "префектура" in t or "мерія;" in t) or "муніципалітет" in t or LanguageHelper.ends_with(t, "рада;")) or "дума;" in t or "збори" in t) or "кабінет;" in t or "сенат;" in t) or "палата" in t or "рада;" in t) or "парламент;" in t or "конгрес" in t) or "комісія" in t or "поліція;" in t) or "міліція;" in t or "хурал" in t) or "суглан" in t or "хасе;" in t) or "іл тумен" in t or "курултай" in t) or "меджліс;" in t): 
            return OrganizationKind.GOVENMENT
        if ("комитет" in t or "комітет" in t): 
            if (r is not None and r.higher is not None and r.higher.kind == OrganizationKind.PARTY): 
                return OrganizationKind.DEPARTMENT
            return OrganizationKind.GOVENMENT
        if ("штаб;" in t): 
            if (r is not None and r.higher is not None and r.higher.kind == OrganizationKind.MILITARY): 
                return OrganizationKind.MILITARY
            return OrganizationKind.GOVENMENT
        tn = t
        if (not Utils.isNullOrEmpty(n)): 
            tn += n
        tn = tn.lower()
        if ((((("служба;" in t or "инспекция;" in t or "управление;" in t) or "департамент" in t or "комитет;" in t) or "комиссия;" in t or "інспекція;" in t) or "керування;" in t or "комітет;" in t) or "комісія;" in t): 
            if ("федеральн" in tn or "государствен" in tn or "державн" in tn): 
                return OrganizationKind.GOVENMENT
            if (r is not None and r.find_slot(OrganizationReferent.ATTR_GEO, None, True) is not None): 
                if (r.higher is None and r._m_temp_parent_org is None): 
                    if (not "управление;" in t and not "департамент" in t and not "керування;" in t): 
                        return OrganizationKind.GOVENMENT
        if ((((((((((((((((((((((((((((((((("подразделение" in t or "отдел;" in t or "отдел " in t) or "направление" in t or "отделение" in t) or "кафедра" in t or "инспекция" in t) or "факультет" in t or "лаборатория" in t) or "пресс центр" in t or "пресс служба" in t) or "сектор " in t or t == "группа;") or (("курс;" in t and not "конкурс" in t)) or "филиал" in t) or "главное управление" in t or "пограничное управление" in t) or "главное территориальное управление" in t or "бухгалтерия" in t) or "магистратура" in t or "аспирантура" in t) or "докторантура" in t or "дирекция" in t) or "руководство" in t or "правление" in t) or "пленум;" in t or "президиум" in t) or "стол;" in t or "совет директоров" in t) or "ученый совет" in t or "коллегия" in t) or "аппарат" in t or "представительство" in t) or "жюри;" in t or "підрозділ" in t) or "відділ;" in t or "відділ " in t) or "напрямок" in t or "відділення" in t) or "інспекція" in t or t == "група;") or "лабораторія" in t or "прес центр" in t) or "прес служба" in t or "філія" in t) or "головне управління" in t or "головне територіальне управління" in t) or "бухгалтерія" in t or "магістратура" in t) or "аспірантура" in t or "докторантура" in t) or "дирекція" in t or "керівництво" in t) or "правління" in t or "президія" in t) or "стіл" in t or "рада директорів" in t) or "вчена рада" in t or "колегія" in t) or "апарат" in t or "представництво" in t) or "журі;" in t or "фракция" in t) or "депутатская группа" in t or "фракція" in t) or "депутатська група" in t): 
            return OrganizationKind.DEPARTMENT
        if (("научн" in t or "исследовательск" in t or "науков" in t) or "дослідн" in t): 
            return OrganizationKind.SCIENCE
        if ("агенство" in t or "агентство" in t): 
            if ("федеральн" in tn or "державн" in tn): 
                return OrganizationKind.GOVENMENT
            if ("информацион" in tn or "інформаційн" in tn): 
                return OrganizationKind.PRESS
        if ("холдинг" in t or "группа компаний" in t or "група компаній" in t): 
            return OrganizationKind.HOLDING
        if ("академия" in t or "академія" in t): 
            if ("наук" in tn): 
                return OrganizationKind.SCIENCE
            return OrganizationKind.STUDY
        if (((((((((("школа;" in t or "университет" in t or "учебный " in tn) or "лицей" in t or "колледж" in t) or "детский сад" in t or "училище" in t) or "гимназия" in t or "семинария" in t) or "образовательн" in t or "интернат" in t) or "університет" in t or "навчальний " in tn) or "ліцей" in t or "коледж" in t) or "дитячий садок" in t or "училище" in t) or "гімназія" in t or "семінарія" in t) or "освітн" in t or "інтернат" in t): 
            return OrganizationKind.STUDY
        if ((("больница" in t or "поликлиника" in t or "клиника" in t) or "госпиталь" in t or "санитарн" in tn) or "медико" in tn or "медицин" in tn): 
            return OrganizationKind.MEDICAL
        if (((((("церковь" in t or "храм;" in t or "собор" in t) or "синагога" in t or "мечеть" in t) or "лавра" in t or "монастырь" in t) or "церква" in t or "монастир" in t) or "патриархия" in t or "епархия" in t) or "патріархія" in t or "єпархія" in t): 
            return OrganizationKind.CHURCH
        if ("департамент" in t or "управление" in t or "керування" in t): 
            if (r is not None): 
                if (r.find_slot(OrganizationReferent.ATTR_HIGHER, None, True) is not None): 
                    return OrganizationKind.DEPARTMENT
        if (("академия" in t or "институт" in t or "академія" in t) or "інститут" in t): 
            if (n is not None and ((("НАУК" in n or "НАУЧН" in n or "НАУКОВ" in n) or "ИССЛЕДОВАТ" in n or "ДОСЛІДН" in n))): 
                return OrganizationKind.SCIENCE
        if ("аэропорт" in t or "аеропорт" in t): 
            return OrganizationKind.AIRPORT
        if ((("фестиваль" in t or "чемпионат" in t or "олимпиада" in t) or "конкурс" in t or "чемпіонат" in t) or "олімпіада" in t): 
            return OrganizationKind.FESTIVAL
        if ((((((((("армия" in t or "генеральный штаб" in t or "войсковая часть" in t) or "армія" in t or "генеральний штаб" in t) or "військова частина" in t or "дивизия" in t) or "полк" in t or "батальон" in t) or "рота" in t or "взвод" in t) or "дивізія" in t or "батальйон" in t) or "гарнизон" in t or "гарнізон" in t) or "бригада" in t or "корпус" in t) or "дивизион" in t or "дивізіон" in t): 
            return OrganizationKind.MILITARY
        if ((("партия" in t or "движение" in t or "группировка" in t) or "партія" in t or "рух;" in t) or "групування" in t): 
            return OrganizationKind.PARTY
        if ((((((("газета" in t or "издательство" in t or "информационное агентство" in t) or "риа;" in tn or "журнал" in t) or "издание" in t or "еженедельник" in t) or "таблоид" in t or "видавництво" in t) or "інформаційне агентство" in t or "журнал" in t) or "видання" in t or "тижневик" in t) or "таблоїд" in t or "портал" in t): 
            return OrganizationKind.PRESS
        if ((("телеканал" in t or "телекомпания" in t or "радиостанция" in t) or "киностудия" in t or "телекомпанія" in t) or "радіостанція" in t or "кіностудія" in t): 
            return OrganizationKind.MEDIA
        if ((("завод;" in t or "фабрика" in t or "комбинат" in t) or "производитель" in t or "комбінат" in t) or "виробник" in t): 
            return OrganizationKind.FACTORY
        if (((((("театр;" in t or "концертный зал" in t or "музей" in t) or "консерватория" in t or "филармония" in t) or "галерея" in t or "театр студия" in t) or "дом культуры" in t or "концертний зал" in t) or "консерваторія" in t or "філармонія" in t) or "театр студія" in t or "будинок культури" in t): 
            return OrganizationKind.CULTURE
        if ((((((("федерация" in t or "союз" in t or "объединение" in t) or "фонд;" in t or "ассоциация" in t) or "клуб" in t or "альянс" in t) or "ассамблея" in t or "федерація" in t) or "обєднання" in t or "фонд;" in t) or "асоціація" in t or "асамблея" in t) or "гильдия" in t or "гільдія" in t): 
            return OrganizationKind.FEDERATION
        if (((((("пансионат" in t or "санаторий" in t or "дом отдыха" in t) or "база отдыха" in t or "гостиница" in t) or "отель" in t or "лагерь" in t) or "пансіонат" in t or "санаторій" in t) or "будинок відпочинку" in t or "база відпочинку" in t) or "готель" in t or "табір" in t): 
            return OrganizationKind.HOTEL
        if (((((("суд;" in t or "колония" in t or "изолятор" in t) or "тюрьма" in t or "прокуратура" in t) or "судебный" in t or "трибунал" in t) or "колонія" in t or "ізолятор" in t) or "вязниця" in t or "судовий" in t) or "трибунал" in t): 
            return OrganizationKind.JUSTICE
        if ("банк" in tn or "казначейство" in tn): 
            return OrganizationKind.BANK
        if ("торгов" in tn or "магазин" in tn or "маркет;" in tn): 
            return OrganizationKind.TRADE
        if ("УЗ;" in t): 
            return OrganizationKind.MEDICAL
        if ("центр;" in t): 
            if (("диагностический" in tn or "медицинский" in tn or "діагностичний" in tn) or "медичний" in tn): 
                return OrganizationKind.MEDICAL
            if ((isinstance(r, OrganizationReferent)) and (r if isinstance(r, OrganizationReferent) else None).higher is not None): 
                if ((r if isinstance(r, OrganizationReferent) else None).higher.kind == OrganizationKind.DEPARTMENT): 
                    return OrganizationKind.DEPARTMENT
        if ("часть;" in t or "частина;" in t): 
            return OrganizationKind.DEPARTMENT
        if (r is not None): 
            if (r.contains_profile(OrgProfile.POLICY)): 
                return OrganizationKind.PARTY
            if (r.contains_profile(OrgProfile.MEDIA)): 
                return OrganizationKind.MEDIA
        return OrganizationKind.UNDEFINED
    
    @staticmethod
    def _new2150(_arg1 : 'Token', _arg2 : 'Token', _arg3 : float) -> 'OrgItemTypeToken':
        res = OrgItemTypeToken(_arg1, _arg2)
        res.__m_coef = _arg3
        return res
    
    @staticmethod
    def _new2151(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : float, _arg5 : bool) -> 'OrgItemTypeToken':
        res = OrgItemTypeToken(_arg1, _arg2)
        res.typ = _arg3
        res.coef = _arg4
        res.is_dep = _arg5
        return res
    
    @staticmethod
    def _new2152(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str) -> 'OrgItemTypeToken':
        res = OrgItemTypeToken(_arg1, _arg2)
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new2155(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : 'OrgItemTermin', _arg5 : bool) -> 'OrgItemTypeToken':
        res = OrgItemTypeToken(_arg1, _arg2)
        res.typ = _arg3
        res.root = _arg4
        res.is_not_typ = _arg5
        return res
    
    @staticmethod
    def _new2159(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : 'OrgItemTermin') -> 'OrgItemTypeToken':
        res = OrgItemTypeToken(_arg1, _arg2)
        res.typ = _arg3
        res.root = _arg4
        return res
    
    @staticmethod
    def _new2163(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : str, _arg5 : float, _arg6 : 'OrgItemTermin') -> 'OrgItemTypeToken':
        res = OrgItemTypeToken(_arg1, _arg2)
        res.typ = _arg3
        res.name = _arg4
        res.coef = _arg5
        res.root = _arg6
        return res
    
    @staticmethod
    def _new2164(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : str, _arg5 : 'OrgItemTermin', _arg6 : bool) -> 'OrgItemTypeToken':
        res = OrgItemTypeToken(_arg1, _arg2)
        res.typ = _arg3
        res.alt_typ = _arg4
        res.root = _arg5
        res.can_be_organization = _arg6
        return res
    
    @staticmethod
    def _new2165(_arg1 : 'Token', _arg2 : 'Token', _arg3 : float, _arg4 : bool, _arg5 : str) -> 'OrgItemTypeToken':
        res = OrgItemTypeToken(_arg1, _arg2)
        res.coef = _arg3
        res.is_not_typ = _arg4
        res.typ = _arg5
        return res
    
    @staticmethod
    def _new2167(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'OrgItemTermin', _arg4 : str) -> 'OrgItemTypeToken':
        res = OrgItemTypeToken(_arg1, _arg2)
        res.root = _arg3
        res.typ = _arg4
        return res
    
    @staticmethod
    def _new2169(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : 'OrgItemTermin', _arg5 : str) -> 'OrgItemTypeToken':
        res = OrgItemTypeToken(_arg1, _arg2)
        res.typ = _arg3
        res.root = _arg4
        res.name = _arg5
        return res
    
    @staticmethod
    def _new2170(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : 'MorphCollection', _arg5 : 'CharsInfo', _arg6 : 'CharsInfo') -> 'OrgItemTypeToken':
        res = OrgItemTypeToken(_arg1, _arg2)
        res.name = _arg3
        res.morph = _arg4
        res.chars = _arg5
        res.chars_root = _arg6
        return res
    
    # static constructor for class OrgItemTypeToken
    @staticmethod
    def _static_ctor():
        OrgItemTypeToken.M_EMPTY_TYP_WORDS = ["КРУПНЫЙ", "КРУПНЕЙШИЙ", "ИЗВЕСТНЫЙ", "ИЗВЕСТНЕЙШИЙ", "МАЛОИЗВЕСТНЫЙ", "ЗАРУБЕЖНЫЙ", "ВЛИЯТЕЛЬНЫЙ", "ВЛИЯТЕЛЬНЕЙШИЙ", "ЗНАМЕНИТЫЙ", "НАЙБІЛЬШИЙ", "ВІДОМИЙ", "ВІДОМИЙ", "МАЛОВІДОМИЙ", "ЗАКОРДОННИЙ"]
        OrgItemTypeToken.__m_decree_key_words = ["УКАЗ", "УКАЗАНИЕ", "ПОСТАНОВЛЕНИЕ", "РАСПОРЯЖЕНИЕ", "ПРИКАЗ", "ДИРЕКТИВА", "ПИСЬМО", "ЗАКОН", "КОДЕКС", "КОНСТИТУЦИЯ", "РЕШЕНИЕ", "ПОЛОЖЕНИЕ", "РАСПОРЯЖЕНИЕ", "ПОРУЧЕНИЕ", "ДОГОВОР", "СУБДОГОВОР", "АГЕНТСКИЙ ДОГОВОР", "ОПРЕДЕЛЕНИЕ", "СОГЛАШЕНИЕ", "ПРОТОКОЛ", "УСТАВ", "ХАРТИЯ", "РЕГЛАМЕНТ", "КОНВЕНЦИЯ", "ПАКТ", "БИЛЛЬ", "ДЕКЛАРАЦИЯ", "ТЕЛЕФОНОГРАММА", "ТЕЛЕФАКСОГРАММА", "ФАКСОГРАММА", "ПРАВИЛО", "ПРОГРАММА", "ПЕРЕЧЕНЬ", "ПОСОБИЕ", "РЕКОМЕНДАЦИЯ", "НАСТАВЛЕНИЕ", "СТАНДАРТ", "СОГЛАШЕНИЕ", "МЕТОДИКА", "ТРЕБОВАНИЕ", "УКАЗ", "ВКАЗІВКА", "ПОСТАНОВА", "РОЗПОРЯДЖЕННЯ", "НАКАЗ", "ДИРЕКТИВА", "ЛИСТ", "ЗАКОН", "КОДЕКС", "КОНСТИТУЦІЯ", "РІШЕННЯ", "ПОЛОЖЕННЯ", "РОЗПОРЯДЖЕННЯ", "ДОРУЧЕННЯ", "ДОГОВІР", "СУБКОНТРАКТ", "АГЕНТСЬКИЙ ДОГОВІР", "ВИЗНАЧЕННЯ", "УГОДА", "ПРОТОКОЛ", "СТАТУТ", "ХАРТІЯ", "РЕГЛАМЕНТ", "КОНВЕНЦІЯ", "ПАКТ", "БІЛЛЬ", "ДЕКЛАРАЦІЯ", "ТЕЛЕФОНОГРАМА", "ТЕЛЕФАКСОГРАММА", "ФАКСОГРАМА", "ПРАВИЛО", "ПРОГРАМА", "ПЕРЕЛІК", "ДОПОМОГА", "РЕКОМЕНДАЦІЯ", "ПОВЧАННЯ", "СТАНДАРТ", "УГОДА", "МЕТОДИКА", "ВИМОГА"]
        OrgItemTypeToken.__m_org_adjactives = ["РОССИЙСКИЙ", "ВСЕРОССИЙСКИЙ", "МЕЖДУНАРОДНЫЙ", "ВСЕМИРНЫЙ", "ЕВРОПЕЙСКИЙ", "ГОСУДАРСТВЕННЫЙ", "НЕГОСУДАРСТВЕННЫЙ", "ФЕДЕРАЛЬНЫЙ", "РЕГИОНАЛЬНЫЙ", "ОБЛАСТНОЙ", "ГОРОДСКОЙ", "МУНИЦИПАЛЬНЫЙ", "АВТОНОМНЫЙ", "НАЦИОНАЛЬНЫЙ", "МЕЖРАЙОННЫЙ", "РАЙОННЫЙ", "ОТРАСЛЕВОЙ", "МЕЖОТРАСЛЕВОЙ", "НАРОДНЫЙ", "ВЕРХОВНЫЙ", "УКРАИНСКИЙ", "ВСЕУКРАИНСКИЙ", "РУССКИЙ"]
        OrgItemTypeToken.__m_org_adjactivesua = ["РОСІЙСЬКИЙ", "ВСЕРОСІЙСЬКИЙ", "МІЖНАРОДНИЙ", "СВІТОВИЙ", "ЄВРОПЕЙСЬКИЙ", "ДЕРЖАВНИЙ", "НЕДЕРЖАВНИЙ", "ФЕДЕРАЛЬНИЙ", "РЕГІОНАЛЬНИЙ", "ОБЛАСНИЙ", "МІСЬКИЙ", "МУНІЦИПАЛЬНИЙ", "АВТОНОМНИЙ", "НАЦІОНАЛЬНИЙ", "МІЖРАЙОННИЙ", "РАЙОННИЙ", "ГАЛУЗЕВИЙ", "МІЖГАЛУЗЕВИЙ", "НАРОДНИЙ", "ВЕРХОВНИЙ", "УКРАЇНСЬКИЙ", "ВСЕУКРАЇНСЬКИЙ", "РОСІЙСЬКА"]
        OrgItemTypeToken.__m_org_adjactives2 = ["КОММЕРЧЕСКИЙ", "НЕКОММЕРЧЕСКИЙ", "БЮДЖЕТНЫЙ", "КАЗЕННЫЙ", "БЛАГОТВОРИТЕЛЬНЫЙ", "СОВМЕСТНЫЙ", "ИНОСТРАННЫЙ", "ИССЛЕДОВАТЕЛЬСКИЙ", "ОБРАЗОВАТЕЛЬНЫЙ", "ОБЩЕОБРАЗОВАТЕЛЬНЫЙ", "ВЫСШИЙ", "УЧЕБНЫЙ", "СПЕЦИАЛИЗИРОВАННЫЙ", "ГЛАВНЫЙ", "ЦЕНТРАЛЬНЫЙ", "ТЕХНИЧЕСКИЙ", "ТЕХНОЛОГИЧЕСКИЙ", "ВОЕННЫЙ", "ПРОМЫШЛЕННЫЙ", "ТОРГОВЫЙ", "СИНОДАЛЬНЫЙ", "МЕДИЦИНСКИЙ", "ДИАГНОСТИЧЕСКИЙ", "ДЕТСКИЙ", "АКАДЕМИЧЕСКИЙ", "ПОЛИТЕХНИЧЕСКИЙ", "ИНВЕСТИЦИОННЫЙ", "ТЕРРОРИСТИЧЕСКИЙ", "РАДИКАЛЬНЫЙ", "ИСЛАМИСТСКИЙ", "ЛЕВОРАДИКАЛЬНЫЙ", "ПРАВОРАДИКАЛЬНЫЙ", "ОППОЗИЦИОННЫЙ", "НЕФТЯНОЙ", "ГАЗОВЫЙ", "ВЕЛИКИЙ"]
        OrgItemTypeToken.__m_org_adjactives2ua = ["КОМЕРЦІЙНИЙ", "НЕКОМЕРЦІЙНИЙ", "БЮДЖЕТНИЙ", "КАЗЕННИМ", "БЛАГОДІЙНИЙ", "СПІЛЬНИЙ", "ІНОЗЕМНИЙ", "ДОСЛІДНИЦЬКИЙ", "ОСВІТНІЙ", "ЗАГАЛЬНООСВІТНІЙ", "ВИЩИЙ", "НАВЧАЛЬНИЙ", "СПЕЦІАЛІЗОВАНИЙ", "ГОЛОВНИЙ", "ЦЕНТРАЛЬНИЙ", "ТЕХНІЧНИЙ", "ТЕХНОЛОГІЧНИЙ", "ВІЙСЬКОВИЙ", "ПРОМИСЛОВИЙ", "ТОРГОВИЙ", "СИНОДАЛЬНИЙ", "МЕДИЧНИЙ", "ДІАГНОСТИЧНИЙ", "ДИТЯЧИЙ", "АКАДЕМІЧНИЙ", "ПОЛІТЕХНІЧНИЙ", "ІНВЕСТИЦІЙНИЙ", "ТЕРОРИСТИЧНИЙ", "РАДИКАЛЬНИЙ", "ІСЛАМІЗМ", "ЛІВОРАДИКАЛЬНИЙ", "ПРАВОРАДИКАЛЬНИЙ", "ОПОЗИЦІЙНИЙ", "НАФТОВИЙ", "ГАЗОВИЙ", "ВЕЛИКИЙ"]

OrgItemTypeToken._static_ctor()