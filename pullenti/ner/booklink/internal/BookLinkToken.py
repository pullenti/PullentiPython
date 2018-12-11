# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import datetime
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.TextToken import TextToken
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.date.DateReferent import DateReferent
from pullenti.ner.org.OrganizationKind import OrganizationKind
from pullenti.ner.uri.UriReferent import UriReferent
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.internal.BlkTyps import BlkTyps
from pullenti.ner.core.internal.BlockLine import BlockLine
from pullenti.ner.booklink.BookLinkRefReferent import BookLinkRefReferent
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.person.internal.FioTemplateType import FioTemplateType
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent
from pullenti.ner.booklink.internal.BookLinkTyp import BookLinkTyp
from pullenti.ner.person.internal.PersonItemToken import PersonItemToken
from pullenti.ner.org.OrganizationReferent import OrganizationReferent
from pullenti.ner.person.PersonReferent import PersonReferent
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.core.BracketHelper import BracketHelper

class BookLinkToken(MetaToken):
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        super().__init__(b, e0_, None)
        self.typ = BookLinkTyp.UNDEFINED
        self.value = None;
        self.tok = None;
        self.ref = None;
        self.add_coef = 0
        self.person_template = FioTemplateType.UNDEFINED
        self.start_of_name = None;
    
    @staticmethod
    def tryParseAuthor(t : 'Token', prev_pers_template : 'FioTemplateType'=FioTemplateType.UNDEFINED) -> 'BookLinkToken':
        if (t is None): 
            return None
        rtp = PersonItemToken.tryParsePerson(t, prev_pers_template)
        if (rtp is not None): 
            if (rtp.data is None): 
                re = BookLinkToken._new344(t, (t if rtp == t else rtp.end_token), BookLinkTyp.PERSON, rtp.referent)
            else: 
                re = BookLinkToken._new345(t, rtp.end_token, BookLinkTyp.PERSON, rtp)
            re.person_template = (Utils.valToEnum(rtp.misc_attrs, FioTemplateType))
            tt = rtp.begin_token
            first_pass2759 = True
            while True:
                if first_pass2759: first_pass2759 = False
                else: tt = tt.next0_
                if (not (tt is not None and tt.end_char <= rtp.end_char)): break
                if (not ((isinstance(tt.getReferent(), PersonPropertyReferent)))): 
                    continue
                rt = Utils.asObjectOrNull(tt, ReferentToken)
                if (rt.begin_token.chars.is_capital_upper and tt != rtp.begin_token): 
                    re.start_of_name = MiscHelper.getTextValueOfMetaToken(rt, GetTextAttr.KEEPREGISTER)
                    break
                return None
            return re
        if (t.isChar('[')): 
            re = BookLinkToken.tryParseAuthor(t.next0_, FioTemplateType.UNDEFINED)
            if (re is not None and re.end_token.next0_ is not None and re.end_token.next0_.isChar(']')): 
                re.begin_token = t
                re.end_token = re.end_token.next0_
                return re
        if (((t.isValue("И", None) or t.isValue("ET", None))) and t.next0_ is not None): 
            if (t.next0_.isValue("ДРУГИЕ", None) or t.next0_.isValue("ДР", None) or t.next0_.isValue("AL", None)): 
                res = BookLinkToken._new346(t, t.next0_, BookLinkTyp.ANDOTHERS)
                if (t.next0_.next0_ is not None and t.next0_.next0_.isChar('.')): 
                    res.end_token = res.end_token.next0_
                return res
        return None
    
    @staticmethod
    def tryParse(t : 'Token', lev : int=0) -> 'BookLinkToken':
        if (t is None or lev > 3): 
            return None
        res = BookLinkToken.__tryParse(t, lev + 1)
        if (res is None): 
            if (t.is_hiphen): 
                res = BookLinkToken.__tryParse(t.next0_, lev + 1)
            if (res is None): 
                return None
        if (res.end_token.next0_ is not None and res.end_token.next0_.isChar('.')): 
            res.end_token = res.end_token.next0_
        t = res.end_token.next0_
        if (t is not None and t.is_comma): 
            t = t.next0_
        if (res.typ == BookLinkTyp.GEO or res.typ == BookLinkTyp.PRESS): 
            re2 = BookLinkToken.__tryParse(t, lev + 1)
            if (re2 is not None and ((re2.typ == BookLinkTyp.PRESS or re2.typ == BookLinkTyp.YEAR))): 
                res.add_coef += (1)
        return res
    
    @staticmethod
    def __tryParse(t : 'Token', lev : int) -> 'BookLinkToken':
        if (t is None or lev > 3): 
            return None
        if (t.isChar('[')): 
            re = BookLinkToken.__tryParse(t.next0_, lev + 1)
            if (re is not None and re.end_token.next0_ is not None and re.end_token.next0_.isChar(']')): 
                re.begin_token = t
                re.end_token = re.end_token.next0_
                return re
            if (re is not None and re.end_token.isChar(']')): 
                re.begin_token = t
                return re
            if (re is not None): 
                if (re.typ == BookLinkTyp.SOSTAVITEL or re.typ == BookLinkTyp.EDITORS): 
                    return re
            br = BracketHelper.tryParse(t, BracketParseAttr.NO, 100)
            if (br is not None): 
                if ((isinstance(br.end_token.previous, NumberToken)) and (br.length_char < 30)): 
                    return BookLinkToken._new347(t, br.end_token, BookLinkTyp.NUMBER, MiscHelper.getTextValue(br.begin_token.next0_, br.end_token.previous, GetTextAttr.NO))
        t0 = t
        if (isinstance(t, ReferentToken)): 
            if (isinstance(t.getReferent(), PersonReferent)): 
                return BookLinkToken.tryParseAuthor(t, FioTemplateType.UNDEFINED)
            if (isinstance(t.getReferent(), GeoReferent)): 
                return BookLinkToken._new344(t, t, BookLinkTyp.GEO, t.getReferent())
            if (isinstance(t.getReferent(), DateReferent)): 
                dr = Utils.asObjectOrNull(t.getReferent(), DateReferent)
                if (len(dr.slots) == 1 and dr.year > 0): 
                    return BookLinkToken._new347(t, t, BookLinkTyp.YEAR, str(dr.year))
                if (dr.year > 0 and t.previous is not None and t.previous.is_comma): 
                    return BookLinkToken._new347(t, t, BookLinkTyp.YEAR, str(dr.year))
            if (isinstance(t.getReferent(), OrganizationReferent)): 
                org0_ = Utils.asObjectOrNull(t.getReferent(), OrganizationReferent)
                if (org0_.kind == OrganizationKind.PRESS): 
                    return BookLinkToken._new344(t, t, BookLinkTyp.PRESS, org0_)
            if (isinstance(t.getReferent(), UriReferent)): 
                uri = Utils.asObjectOrNull(t.getReferent(), UriReferent)
                if ((uri.scheme == "http" or uri.scheme == "https" or uri.scheme == "ftp") or uri.scheme is None): 
                    return BookLinkToken._new344(t, t, BookLinkTyp.URL, uri)
        tok_ = BookLinkToken.__m_termins.tryParse(t, TerminParseAttr.NO)
        if (tok_ is not None): 
            typ_ = Utils.valToEnum(tok_.termin.tag, BookLinkTyp)
            ok = True
            if (typ_ == BookLinkTyp.TYPE or typ_ == BookLinkTyp.NAMETAIL or typ_ == BookLinkTyp.ELECTRONRES): 
                if (t.previous is not None and ((t.previous.isCharOf(".:[") or t.previous.is_hiphen))): 
                    pass
                else: 
                    ok = False
            if (ok): 
                return BookLinkToken._new347(t, tok_.end_token, typ_, tok_.termin.canonic_text)
            if (typ_ == BookLinkTyp.ELECTRONRES): 
                tt = tok_.end_token.next0_
                first_pass2760 = True
                while True:
                    if first_pass2760: first_pass2760 = False
                    else: tt = tt.next0_
                    if (not (tt is not None)): break
                    if ((isinstance(tt, TextToken)) and not tt.chars.is_letter): 
                        continue
                    if (isinstance(tt.getReferent(), UriReferent)): 
                        return BookLinkToken._new344(t, tt, BookLinkTyp.ELECTRONRES, tt.getReferent())
                    break
        if (t.isChar('/')): 
            res = BookLinkToken._new347(t, t, BookLinkTyp.DELIMETER, "/")
            if (t.next0_ is not None and t.next0_.isChar('/')): 
                res.end_token = t.next0_
                res.value = "//"
            if (not t.is_whitespace_before and not t.is_whitespace_after): 
                coo = 3
                no = True
                tt = t.next0_
                while tt is not None and coo > 0: 
                    vvv = BookLinkToken.tryParse(tt, lev + 1)
                    if (vvv is not None and vvv.typ != BookLinkTyp.NUMBER): 
                        no = False
                        break
                    tt = tt.next0_; coo -= 1
                if (no): 
                    return None
            return res
        if ((isinstance(t, NumberToken)) and (t).typ == NumberSpellingType.DIGIT): 
            res = BookLinkToken._new347(t, t, BookLinkTyp.NUMBER, str((t).value))
            val = (t).value
            if (val >= 1930 and (val < 2030)): 
                res.typ = BookLinkTyp.YEAR
            if (t.next0_ is not None and t.next0_.isChar('.')): 
                res.end_token = t.next0_
            elif ((t.next0_ is not None and t.next0_.length_char == 1 and not t.next0_.chars.is_letter) and t.next0_.is_whitespace_after): 
                res.end_token = t.next0_
            elif (isinstance(t.next0_, TextToken)): 
                term = (t.next0_).term
                if (((term == "СТР" or term == "C" or term == "С") or term == "P" or term == "S") or term == "PAGES"): 
                    res.end_token = t.next0_
                    res.typ = BookLinkTyp.PAGES
                    res.value = str((t).value)
            return res
        if (isinstance(t, TextToken)): 
            term = (t).term
            if (((((((term == "СТР" or term == "C" or term == "С") or term == "ТОМ" or term == "T") or term == "Т" or term == "P") or term == "PP" or term == "V") or term == "VOL" or term == "S") or term == "СТОР" or t.isValue("PAGE", None)) or t.isValue("СТРАНИЦА", "СТОРІНКА")): 
                tt = t.next0_
                while tt is not None:
                    if (tt.isCharOf(".:~")): 
                        tt = tt.next0_
                    else: 
                        break
                if (isinstance(tt, NumberToken)): 
                    res = BookLinkToken._new346(t, tt, BookLinkTyp.PAGERANGE)
                    tt0 = tt
                    tt1 = tt
                    tt = tt.next0_
                    first_pass2761 = True
                    while True:
                        if first_pass2761: first_pass2761 = False
                        else: tt = tt.next0_
                        if (not (tt is not None)): break
                        if (tt.isCharOf(",") or tt.is_hiphen): 
                            if (isinstance(tt.next0_, NumberToken)): 
                                tt = tt.next0_
                                res.end_token = tt
                                tt1 = tt
                                continue
                        break
                    res.value = MiscHelper.getTextValue(tt0, tt1, GetTextAttr.NO)
                    return res
            if ((term == "M" or term == "М" or term == "СПБ") or term == "K" or term == "К"): 
                if (t.next0_ is not None and t.next0_.isCharOf(":;")): 
                    re = BookLinkToken._new346(t, t.next0_, BookLinkTyp.GEO)
                    return re
                if (t.next0_ is not None and t.next0_.isCharOf(".")): 
                    res = BookLinkToken._new346(t, t.next0_, BookLinkTyp.GEO)
                    if (t.next0_.next0_ is not None and t.next0_.next0_.isCharOf(":;")): 
                        res.end_token = t.next0_.next0_
                    elif (t.next0_.next0_ is not None and (isinstance(t.next0_.next0_, NumberToken))): 
                        pass
                    elif (t.next0_.next0_ is not None and t.next0_.next0_.is_comma and (isinstance(t.next0_.next0_.next0_, NumberToken))): 
                        pass
                    else: 
                        return None
                    return res
            if (term == "ПЕР" or term == "ПЕРЕВ" or term == "ПЕРЕВОД"): 
                tt = t
                if (tt.next0_ is not None and tt.next0_.isChar('.')): 
                    tt = tt.next0_
                if (tt.next0_ is not None and ((tt.next0_.isValue("C", None) or tt.next0_.isValue("С", None)))): 
                    tt = tt.next0_
                    if (tt.next0_ is None or tt.whitespaces_after_count > 2): 
                        return None
                    re = BookLinkToken._new346(t, tt.next0_, BookLinkTyp.TRANSLATE)
                    return re
            if (term == "ТАМ" or term == "ТАМЖЕ"): 
                res = BookLinkToken._new346(t, t, BookLinkTyp.TAMZE)
                if (t.next0_ is not None and t.next0_.isValue("ЖЕ", None)): 
                    res.end_token = t.next0_
                return res
            if (((term == "СМ" or term == "CM" or term == "НАПР") or term == "НАПРИМЕР" or term == "SEE") or term == "ПОДРОБНЕЕ" or term == "ПОДРОБНО"): 
                res = BookLinkToken._new346(t, t, BookLinkTyp.SEE)
                t = t.next0_
                first_pass2762 = True
                while True:
                    if first_pass2762: first_pass2762 = False
                    else: t = t.next0_
                    if (not (t is not None)): break
                    if (t.isCharOf(".:") or t.isValue("ALSO", None)): 
                        res.end_token = t
                        continue
                    if (t.isValue("В", None) or t.isValue("IN", None)): 
                        res.end_token = t
                        continue
                    vvv = BookLinkToken.__tryParse(t, lev + 1)
                    if (vvv is not None and vvv.typ == BookLinkTyp.SEE): 
                        res.end_token = vvv.end_token
                        break
                    break
                return res
            if (term == "БОЛЕЕ"): 
                vvv = BookLinkToken.__tryParse(t.next0_, lev + 1)
                if (vvv is not None and vvv.typ == BookLinkTyp.SEE): 
                    vvv.begin_token = t
                    return vvv
            no = MiscHelper.checkNumberPrefix(t)
            if (isinstance(no, NumberToken)): 
                return BookLinkToken._new346(t, no, BookLinkTyp.N)
            if (((term == "B" or term == "В")) and (isinstance(t.next0_, NumberToken)) and (isinstance(t.next0_.next0_, TextToken))): 
                term2 = (t.next0_.next0_).term
                if (((term2 == "Т" or term2 == "T" or term2.startswith("ТОМ")) or term2 == "TT" or term2 == "ТТ") or term2 == "КН" or term2.startswith("КНИГ")): 
                    return BookLinkToken._new346(t, t.next0_.next0_, BookLinkTyp.VOLUME)
        if (t.isChar('(')): 
            if ((isinstance(t.next0_, NumberToken)) and t.next0_.next0_ is not None and t.next0_.next0_.isChar(')')): 
                num = (t.next0_).value
                if (num > (1900) and num <= (2040)): 
                    if (num <= datetime.datetime.now().year): 
                        return BookLinkToken._new347(t, t.next0_.next0_, BookLinkTyp.YEAR, str(num))
            if (((isinstance(t.next0_, ReferentToken)) and (isinstance(t.next0_.getReferent(), DateReferent)) and t.next0_.next0_ is not None) and t.next0_.next0_.isChar(')')): 
                num = (t.next0_.getReferent()).year
                if (num > 0): 
                    return BookLinkToken._new347(t, t.next0_.next0_, BookLinkTyp.YEAR, str(num))
        return None
    
    @staticmethod
    def checkLinkBefore(t0 : 'Token', num : str) -> bool:
        if (num is None or t0 is None): 
            return False
        if (t0.previous is not None and (isinstance(t0.previous.getReferent(), BookLinkRefReferent))): 
            wrapnn367 = RefOutArgWrapper(0)
            inoutres368 = Utils.tryParseInt(Utils.ifNotNull((t0.previous.getReferent()).number, ""), wrapnn367)
            nn = wrapnn367.value
            if (inoutres368): 
                if (str((nn + 1)) == num): 
                    return True
        return False
    
    @staticmethod
    def checkLinkAfter(t1 : 'Token', num : str) -> bool:
        if (num is None or t1 is None): 
            return False
        if (t1.is_newline_after): 
            bbb = BookLinkToken.tryParse(t1.next0_, 0)
            if (bbb is not None and bbb.typ == BookLinkTyp.NUMBER): 
                wrapnn369 = RefOutArgWrapper(0)
                inoutres370 = Utils.tryParseInt(Utils.ifNotNull(bbb.value, ""), wrapnn369)
                nn = wrapnn369.value
                if (inoutres370): 
                    if (str((nn - 1)) == num): 
                        return True
        return False
    
    @staticmethod
    def initialize() -> None:
        if (BookLinkToken.__m_termins is not None): 
            return
        BookLinkToken.__m_termins = TerminCollection()
        tt = Termin._new118("ТЕКСТ", BookLinkTyp.NAMETAIL)
        BookLinkToken.__m_termins.add(tt)
        tt = Termin._new118("ЭЛЕКТРОННЫЙ РЕСУРС", BookLinkTyp.ELECTRONRES)
        tt.addVariant("ЕЛЕКТРОННИЙ РЕСУРС", False)
        tt.addVariant("MODE OF ACCESS", False)
        tt.addVariant("URL", False)
        tt.addVariant("URLS", False)
        tt.addVariant("ELECTRONIC RESOURCE", False)
        tt.addVariant("ON LINE", False)
        tt.addVariant("ONLINE", False)
        BookLinkToken.__m_termins.add(tt)
        tt = Termin._new118("РЕЖИМ ДОСТУПА", BookLinkTyp.MISC)
        tt.addVariant("РЕЖИМ ДОСТУПУ", False)
        tt.addVariant("AVAILABLE", False)
        BookLinkToken.__m_termins.add(tt)
        tt = Termin._new118("МОНОГРАФИЯ", BookLinkTyp.TYPE)
        tt.addVariant("МОНОГРАФІЯ", False)
        BookLinkToken.__m_termins.add(tt)
        tt = Termin._new118("УЧЕБНОЕ ПОСОБИЕ", BookLinkTyp.TYPE)
        tt.addAbridge("УЧ.ПОСОБИЕ")
        tt.addAbridge("УЧЕБ.")
        tt.addAbridge("УЧЕБН.")
        tt.addVariant("УЧЕБНИК", False)
        tt.addVariant("ПОСОБИЕ", False)
        BookLinkToken.__m_termins.add(tt)
        tt = Termin._new119("НАВЧАЛЬНИЙ ПОСІБНИК", BookLinkTyp.TYPE, MorphLang.UA)
        tt.addAbridge("НАВЧ.ПОСІБНИК")
        tt.addAbridge("НАВЧ.ПОСІБ")
        tt.addVariant("ПІДРУЧНИК", False)
        tt.addVariant("ПІДРУЧ", False)
        BookLinkToken.__m_termins.add(tt)
        tt = Termin._new118("АВТОРЕФЕРАТ", BookLinkTyp.TYPE)
        tt.addAbridge("АВТОРЕФ.")
        BookLinkToken.__m_termins.add(tt)
        tt = Termin._new118("ДИССЕРТАЦИЯ", BookLinkTyp.TYPE)
        tt.addVariant("ДИСС", False)
        tt.addAbridge("ДИС.")
        tt.addVariant("ДИСЕРТАЦІЯ", False)
        tt.addVariant("DISSERTATION", False)
        BookLinkToken.__m_termins.add(tt)
        tt = Termin._new118("ДОКЛАД", BookLinkTyp.TYPE)
        tt.addVariant("ДОКЛ", False)
        tt.addAbridge("ДОКЛ.")
        tt.addVariant("ДОПОВІДЬ", False)
        BookLinkToken.__m_termins.add(tt)
        tt = Termin._new118("ПОД РЕДАКЦИЕЙ", BookLinkTyp.EDITORS)
        tt.addAbridge("ПОД РЕД")
        tt.addAbridge("ОТВ.РЕД")
        tt.addAbridge("ОТВ.РЕДАКТОР")
        tt.addVariant("ПОД ОБЩЕЙ РЕДАКЦИЕЙ", False)
        tt.addAbridge("ОТВ.РЕД")
        tt.addAbridge("ОТВ.РЕДАКТОР")
        tt.addAbridge("ПОД ОБЩ. РЕД")
        tt.addAbridge("ПОД ОБЩЕЙ РЕД")
        BookLinkToken.__m_termins.add(tt)
        tt = Termin._new119("ПІД РЕДАКЦІЄЮ", BookLinkTyp.EDITORS, MorphLang.UA)
        tt.addAbridge("ПІД РЕД")
        tt.addAbridge("ОТВ.РЕД")
        tt.addAbridge("ВІД. РЕДАКТОР")
        tt.addVariant("ЗА ЗАГ.РЕД", False)
        tt.addAbridge("ВІДПОВІДАЛЬНИЙ РЕДАКТОР")
        BookLinkToken.__m_termins.add(tt)
        tt = Termin._new118("СОСТАВИТЕЛЬ", BookLinkTyp.SOSTAVITEL)
        tt.addAbridge("СОСТ.")
        BookLinkToken.__m_termins.add(tt)
        tt = Termin._new119("УКЛАДАЧ", BookLinkTyp.SOSTAVITEL, MorphLang.UA)
        tt.addAbridge("УКЛ.")
        BookLinkToken.__m_termins.add(tt)
        for s in ["Политиздат", "Прогресс", "Мысль", "Просвещение", "Наука", "Физматлит", "Физматкнига", "Инфра-М", "Питер", "Интеллект", "Аспект пресс", "Аспект-пресс", "АСВ", "Радиотехника", "Радио и связь", "Лань", "Академия", "Академкнига", "URSS", "Академический проект", "БИНОМ", "БВХ", "Вильямс", "Владос", "Волтерс Клувер", "Wolters Kluwer", "Восток-Запад", "Высшая школа", "ГЕО", "Дашков и К", "Кнорус", "Когито-Центр", "КолосС", "Проспект", "РХД", "Статистика", "Финансы и статистика", "Флинта", "Юнити-дана"]: 
            BookLinkToken.__m_termins.add(Termin._new118(s.upper(), BookLinkTyp.PRESS))
        tt = Termin._new118("ИЗДАТЕЛЬСТВО", BookLinkTyp.PRESS)
        tt.addAbridge("ИЗ-ВО")
        tt.addAbridge("ИЗД-ВО")
        tt.addAbridge("ИЗДАТ-ВО")
        tt.addVariant("ISSN", False)
        tt.addVariant("PRESS", False)
        tt.addVariant("VERLAG", False)
        tt.addVariant("JOURNAL", False)
        BookLinkToken.__m_termins.add(tt)
    
    __m_termins = None
    
    @staticmethod
    def parseStartOfLitBlock(t : 'Token') -> 'Token':
        if (t is None): 
            return None
        bl = BlockLine.create(t, None)
        if (bl is not None and bl.typ == BlkTyps.LITERATURE): 
            return bl.end_token
        return None
    
    @staticmethod
    def _new344(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'BookLinkTyp', _arg4 : 'Referent') -> 'BookLinkToken':
        res = BookLinkToken(_arg1, _arg2)
        res.typ = _arg3
        res.ref = _arg4
        return res
    
    @staticmethod
    def _new345(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'BookLinkTyp', _arg4 : 'ReferentToken') -> 'BookLinkToken':
        res = BookLinkToken(_arg1, _arg2)
        res.typ = _arg3
        res.tok = _arg4
        return res
    
    @staticmethod
    def _new346(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'BookLinkTyp') -> 'BookLinkToken':
        res = BookLinkToken(_arg1, _arg2)
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new347(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'BookLinkTyp', _arg4 : str) -> 'BookLinkToken':
        res = BookLinkToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        return res