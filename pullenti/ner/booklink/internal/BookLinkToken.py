# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import datetime
from pullenti.ntopy.Utils import Utils
from pullenti.ntopy.Misc import RefOutArgWrapper
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.booklink.internal.BookLinkTyp import BookLinkTyp
from pullenti.ner.person.internal.FioTemplateType import FioTemplateType
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.org.OrganizationKind import OrganizationKind
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.core.internal.BlkTyps import BlkTyps


class BookLinkToken(MetaToken):
    
    def __init__(self, b : 'Token', e0 : 'Token') -> None:
        self.typ = BookLinkTyp.UNDEFINED
        self.value = None
        self.tok = None
        self.ref = None
        self.add_coef = 0
        self.person_template = FioTemplateType.UNDEFINED
        self.start_of_name = None
        super().__init__(b, e0, None)
    
    @staticmethod
    def try_parse_author(t : 'Token', prev_pers_template : 'FioTemplateType'=FioTemplateType.UNDEFINED) -> 'BookLinkToken':
        from pullenti.ner.person.internal.PersonItemToken import PersonItemToken
        from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.core.MiscHelper import MiscHelper
        if (t is None): 
            return None
        rtp = PersonItemToken.try_parse_person(t, prev_pers_template)
        if (rtp is not None): 
            if (rtp.data is None): 
                re = BookLinkToken._new343(t, (t if rtp == t else rtp.end_token), BookLinkTyp.PERSON, rtp.referent)
            else: 
                re = BookLinkToken._new344(t, rtp.end_token, BookLinkTyp.PERSON, rtp)
            re.person_template = Utils.valToEnum(rtp.misc_attrs, FioTemplateType)
            tt = rtp.begin_token
            first_pass2549 = True
            while True:
                if first_pass2549: first_pass2549 = False
                else: tt = tt.next0
                if (not (tt is not None and tt.end_char <= rtp.end_char)): break
                if (not ((isinstance(tt.get_referent(), PersonPropertyReferent)))): 
                    continue
                rt = (tt if isinstance(tt, ReferentToken) else None)
                if (rt.begin_token.chars.is_capital_upper and tt != rtp.begin_token): 
                    re.start_of_name = MiscHelper.get_text_value_of_meta_token(rt, GetTextAttr.KEEPREGISTER)
                    break
                return None
            return re
        if (t.is_char('[')): 
            re = BookLinkToken.try_parse_author(t.next0, FioTemplateType.UNDEFINED)
            if (re is not None and re.end_token.next0 is not None and re.end_token.next0.is_char(']')): 
                re.begin_token = t
                re.end_token = re.end_token.next0
                return re
        if (((t.is_value("И", None) or t.is_value("ET", None))) and t.next0 is not None): 
            if (t.next0.is_value("ДРУГИЕ", None) or t.next0.is_value("ДР", None) or t.next0.is_value("AL", None)): 
                res = BookLinkToken._new345(t, t.next0, BookLinkTyp.ANDOTHERS)
                if (t.next0.next0 is not None and t.next0.next0.is_char('.')): 
                    res.end_token = res.end_token.next0
                return res
        return None
    
    @staticmethod
    def try_parse(t : 'Token') -> 'BookLinkToken':
        if (t is None): 
            return None
        res = BookLinkToken.__try_parse(t)
        if (res is None): 
            if (t.is_hiphen): 
                res = BookLinkToken.__try_parse(t.next0)
            if (res is None): 
                return None
        if (res.end_token.next0 is not None and res.end_token.next0.is_char('.')): 
            res.end_token = res.end_token.next0
        t = res.end_token.next0
        if (t is not None and t.is_comma): 
            t = t.next0
        if (res.typ == BookLinkTyp.GEO or res.typ == BookLinkTyp.PRESS): 
            re2 = BookLinkToken.__try_parse(t)
            if (re2 is not None and ((re2.typ == BookLinkTyp.PRESS or re2.typ == BookLinkTyp.YEAR))): 
                res.add_coef += 1
        return res
    
    @staticmethod
    def __try_parse(t : 'Token') -> 'BookLinkToken':
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.person.PersonReferent import PersonReferent
        from pullenti.ner.geo.GeoReferent import GeoReferent
        from pullenti.ner.date.DateReferent import DateReferent
        from pullenti.ner.org.OrganizationReferent import OrganizationReferent
        from pullenti.ner.uri.UriReferent import UriReferent
        from pullenti.ner.TextToken import TextToken
        if (t is None): 
            return None
        if (t.is_char('[')): 
            re = BookLinkToken.__try_parse(t.next0)
            if (re is not None and re.end_token.next0 is not None and re.end_token.next0.is_char(']')): 
                re.begin_token = t
                re.end_token = re.end_token.next0
                return re
            if (re is not None and re.end_token.is_char(']')): 
                re.begin_token = t
                return re
            if (re is not None): 
                if (re.typ == BookLinkTyp.SOSTAVITEL or re.typ == BookLinkTyp.EDITORS): 
                    return re
            br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
            if (br is not None): 
                if (isinstance(br.end_token.previous, NumberToken) and (br.length_char < 30)): 
                    return BookLinkToken._new346(t, br.end_token, BookLinkTyp.NUMBER, MiscHelper.get_text_value(br.begin_token.next0, br.end_token.previous, GetTextAttr.NO))
        t0 = t
        if (isinstance(t, ReferentToken)): 
            if (isinstance(t.get_referent(), PersonReferent)): 
                return BookLinkToken.try_parse_author(t, FioTemplateType.UNDEFINED)
            if (isinstance(t.get_referent(), GeoReferent)): 
                return BookLinkToken._new343(t, t, BookLinkTyp.GEO, t.get_referent())
            if (isinstance(t.get_referent(), DateReferent)): 
                dr = (t.get_referent() if isinstance(t.get_referent(), DateReferent) else None)
                if (len(dr.slots) == 1 and dr.year > 0): 
                    return BookLinkToken._new346(t, t, BookLinkTyp.YEAR, str(dr.year))
                if (dr.year > 0 and t.previous is not None and t.previous.is_comma): 
                    return BookLinkToken._new346(t, t, BookLinkTyp.YEAR, str(dr.year))
            if (isinstance(t.get_referent(), OrganizationReferent)): 
                org = (t.get_referent() if isinstance(t.get_referent(), OrganizationReferent) else None)
                if (org.kind == OrganizationKind.PRESS): 
                    return BookLinkToken._new343(t, t, BookLinkTyp.PRESS, org)
            if (isinstance(t.get_referent(), UriReferent)): 
                uri = (t.get_referent() if isinstance(t.get_referent(), UriReferent) else None)
                if ((uri.scheme == "http" or uri.scheme == "https" or uri.scheme == "ftp") or uri.scheme is None): 
                    return BookLinkToken._new343(t, t, BookLinkTyp.URL, uri)
        tok_ = BookLinkToken.__m_termins.try_parse(t, TerminParseAttr.NO)
        if (tok_ is not None): 
            typ_ = Utils.valToEnum(tok_.termin.tag, BookLinkTyp)
            ok = True
            if (typ_ == BookLinkTyp.TYPE or typ_ == BookLinkTyp.NAMETAIL or typ_ == BookLinkTyp.ELECTRONRES): 
                if (t.previous is not None and ((t.previous.is_char_of(".:[") or t.previous.is_hiphen))): 
                    pass
                else: 
                    ok = False
            if (ok): 
                return BookLinkToken._new346(t, tok_.end_token, typ_, tok_.termin.canonic_text)
            if (typ_ == BookLinkTyp.ELECTRONRES): 
                tt = tok_.end_token.next0
                first_pass2550 = True
                while True:
                    if first_pass2550: first_pass2550 = False
                    else: tt = tt.next0
                    if (not (tt is not None)): break
                    if (isinstance(tt, TextToken) and not tt.chars.is_letter): 
                        continue
                    if (isinstance(tt.get_referent(), UriReferent)): 
                        return BookLinkToken._new343(t, tt, BookLinkTyp.ELECTRONRES, tt.get_referent())
                    break
        if (t.is_char('/')): 
            res = BookLinkToken._new346(t, t, BookLinkTyp.DELIMETER, "/")
            if (t.next0 is not None and t.next0.is_char('/')): 
                res.end_token = t.next0
                res.value = "//"
            if (not t.is_whitespace_before and not t.is_whitespace_after): 
                coo = 3
                no = True
                tt = t.next0
                while tt is not None and coo > 0: 
                    vvv = BookLinkToken.try_parse(tt)
                    if (vvv is not None and vvv.typ != BookLinkTyp.NUMBER): 
                        no = False
                        break
                    tt = tt.next0; coo -= 1
                if (no): 
                    return None
            return res
        if (isinstance(t, NumberToken) and (t if isinstance(t, NumberToken) else None).typ == NumberSpellingType.DIGIT): 
            res = BookLinkToken._new346(t, t, BookLinkTyp.NUMBER, str((t if isinstance(t, NumberToken) else None).value))
            val = (t if isinstance(t, NumberToken) else None).value
            if (val >= 1930 and (val < 2030)): 
                res.typ = BookLinkTyp.YEAR
            if (t.next0 is not None and t.next0.is_char('.')): 
                res.end_token = t.next0
            elif ((t.next0 is not None and t.next0.length_char == 1 and not t.next0.chars.is_letter) and t.next0.is_whitespace_after): 
                res.end_token = t.next0
            elif (isinstance(t.next0, TextToken)): 
                term = (t.next0 if isinstance(t.next0, TextToken) else None).term
                if (((term == "СТР" or term == "C" or term == "С") or term == "P" or term == "S") or term == "PAGES"): 
                    res.end_token = t.next0
                    res.typ = BookLinkTyp.PAGES
                    res.value = str((t if isinstance(t, NumberToken) else None).value)
            return res
        if (isinstance(t, TextToken)): 
            term = (t if isinstance(t, TextToken) else None).term
            if (((((((term == "СТР" or term == "C" or term == "С") or term == "ТОМ" or term == "T") or term == "Т" or term == "P") or term == "PP" or term == "V") or term == "VOL" or term == "S") or term == "СТОР" or t.is_value("PAGE", None)) or t.is_value("СТРАНИЦА", "СТОРІНКА")): 
                tt = t.next0
                while tt is not None:
                    if (tt.is_char_of(".:~")): 
                        tt = tt.next0
                    else: 
                        break
                if (isinstance(tt, NumberToken)): 
                    res = BookLinkToken._new345(t, tt, BookLinkTyp.PAGERANGE)
                    tt0 = tt
                    tt1 = tt
                    tt = tt.next0
                    first_pass2551 = True
                    while True:
                        if first_pass2551: first_pass2551 = False
                        else: tt = tt.next0
                        if (not (tt is not None)): break
                        if (tt.is_char_of(",") or tt.is_hiphen): 
                            if (isinstance(tt.next0, NumberToken)): 
                                tt = tt.next0
                                res.end_token = tt
                                tt1 = tt
                                continue
                        break
                    res.value = MiscHelper.get_text_value(tt0, tt1, GetTextAttr.NO)
                    return res
            if ((term == "M" or term == "М" or term == "СПБ") or term == "K" or term == "К"): 
                if (t.next0 is not None and t.next0.is_char_of(":;")): 
                    re = BookLinkToken._new345(t, t.next0, BookLinkTyp.GEO)
                    return re
                if (t.next0 is not None and t.next0.is_char_of(".")): 
                    res = BookLinkToken._new345(t, t.next0, BookLinkTyp.GEO)
                    if (t.next0.next0 is not None and t.next0.next0.is_char_of(":;")): 
                        res.end_token = t.next0.next0
                    elif (t.next0.next0 is not None and isinstance(t.next0.next0, NumberToken)): 
                        pass
                    elif (t.next0.next0 is not None and t.next0.next0.is_comma and isinstance(t.next0.next0.next0, NumberToken)): 
                        pass
                    else: 
                        return None
                    return res
            if (term == "ПЕР" or term == "ПЕРЕВ" or term == "ПЕРЕВОД"): 
                tt = t
                if (tt.next0 is not None and tt.next0.is_char('.')): 
                    tt = tt.next0
                if (tt.next0 is not None and ((tt.next0.is_value("C", None) or tt.next0.is_value("С", None)))): 
                    tt = tt.next0
                    if (tt.next0 is None or tt.whitespaces_after_count > 2): 
                        return None
                    re = BookLinkToken._new345(t, tt.next0, BookLinkTyp.TRANSLATE)
                    return re
            if (term == "ТАМ" or term == "ТАМЖЕ"): 
                res = BookLinkToken._new345(t, t, BookLinkTyp.TAMZE)
                if (t.next0 is not None and t.next0.is_value("ЖЕ", None)): 
                    res.end_token = t.next0
                return res
            if (((term == "СМ" or term == "CM" or term == "НАПР") or term == "НАПРИМЕР" or term == "SEE") or term == "ПОДРОБНЕЕ" or term == "ПОДРОБНО"): 
                res = BookLinkToken._new345(t, t, BookLinkTyp.SEE)
                t = t.next0
                first_pass2552 = True
                while True:
                    if first_pass2552: first_pass2552 = False
                    else: t = t.next0
                    if (not (t is not None)): break
                    if (t.is_char_of(".:") or t.is_value("ALSO", None)): 
                        res.end_token = t
                        continue
                    if (t.is_value("В", None) or t.is_value("IN", None)): 
                        res.end_token = t
                        continue
                    vvv = BookLinkToken.__try_parse(t)
                    if (vvv is not None and vvv.typ == BookLinkTyp.SEE): 
                        res.end_token = vvv.end_token
                        break
                    break
                return res
            if (term == "БОЛЕЕ"): 
                vvv = BookLinkToken.__try_parse(t.next0)
                if (vvv is not None and vvv.typ == BookLinkTyp.SEE): 
                    vvv.begin_token = t
                    return vvv
            no = MiscHelper.check_number_prefix(t)
            if (isinstance(no, NumberToken)): 
                return BookLinkToken._new345(t, no, BookLinkTyp.N)
            if (((term == "B" or term == "В")) and isinstance(t.next0, NumberToken) and isinstance(t.next0.next0, TextToken)): 
                term2 = (t.next0.next0 if isinstance(t.next0.next0, TextToken) else None).term
                if (((term2 == "Т" or term2 == "T" or term2.startswith("ТОМ")) or term2 == "TT" or term2 == "ТТ") or term2 == "КН" or term2.startswith("КНИГ")): 
                    return BookLinkToken._new345(t, t.next0.next0, BookLinkTyp.VOLUME)
        if (t.is_char('(')): 
            if (isinstance(t.next0, NumberToken) and t.next0.next0 is not None and t.next0.next0.is_char(')')): 
                num = (t.next0 if isinstance(t.next0, NumberToken) else None).value
                if (num > 1900 and num <= 2040): 
                    if (num <= datetime.datetime.now().year): 
                        return BookLinkToken._new346(t, t.next0.next0, BookLinkTyp.YEAR, str(num))
            if ((isinstance(t.next0, ReferentToken) and isinstance(t.next0.get_referent(), DateReferent) and t.next0.next0 is not None) and t.next0.next0.is_char(')')): 
                num = (t.next0.get_referent() if isinstance(t.next0.get_referent(), DateReferent) else None).year
                if (num > 0): 
                    return BookLinkToken._new346(t, t.next0.next0, BookLinkTyp.YEAR, str(num))
        return None
    
    @staticmethod
    def check_link_before(t0 : 'Token', num : str) -> bool:
        from pullenti.ner.booklink.BookLinkRefReferent import BookLinkRefReferent
        if (num is None or t0 is None): 
            return False
        if (t0.previous is not None and isinstance(t0.previous.get_referent(), BookLinkRefReferent)): 
            inoutarg366 = RefOutArgWrapper(None)
            inoutres367 = Utils.tryParseInt(Utils.ifNotNull((t0.previous.get_referent() if isinstance(t0.previous.get_referent(), BookLinkRefReferent) else None).number, ""), inoutarg366)
            nn = inoutarg366.value
            if (inoutres367): 
                if (str((nn + 1)) == num): 
                    return True
        return False
    
    @staticmethod
    def check_link_after(t1 : 'Token', num : str) -> bool:
        if (num is None or t1 is None): 
            return False
        if (t1.is_newline_after): 
            bbb = BookLinkToken.try_parse(t1.next0)
            if (bbb is not None and bbb.typ == BookLinkTyp.NUMBER): 
                inoutarg368 = RefOutArgWrapper(None)
                inoutres369 = Utils.tryParseInt(Utils.ifNotNull(bbb.value, ""), inoutarg368)
                nn = inoutarg368.value
                if (inoutres369): 
                    if (str((nn - 1)) == num): 
                        return True
        return False
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.core.TerminCollection import TerminCollection
        from pullenti.ner.core.Termin import Termin
        from pullenti.morph.MorphLang import MorphLang
        if (BookLinkToken.__m_termins is not None): 
            return
        BookLinkToken.__m_termins = TerminCollection()
        tt = Termin._new118("ТЕКСТ", BookLinkTyp.NAMETAIL)
        BookLinkToken.__m_termins.add(tt)
        tt = Termin._new118("ЭЛЕКТРОННЫЙ РЕСУРС", BookLinkTyp.ELECTRONRES)
        tt.add_variant("ЕЛЕКТРОННИЙ РЕСУРС", False)
        tt.add_variant("MODE OF ACCESS", False)
        tt.add_variant("URL", False)
        tt.add_variant("URLS", False)
        tt.add_variant("ELECTRONIC RESOURCE", False)
        tt.add_variant("ON LINE", False)
        tt.add_variant("ONLINE", False)
        BookLinkToken.__m_termins.add(tt)
        tt = Termin._new118("РЕЖИМ ДОСТУПА", BookLinkTyp.MISC)
        tt.add_variant("РЕЖИМ ДОСТУПУ", False)
        tt.add_variant("AVAILABLE", False)
        BookLinkToken.__m_termins.add(tt)
        tt = Termin._new118("МОНОГРАФИЯ", BookLinkTyp.TYPE)
        tt.add_variant("МОНОГРАФІЯ", False)
        BookLinkToken.__m_termins.add(tt)
        tt = Termin._new118("УЧЕБНОЕ ПОСОБИЕ", BookLinkTyp.TYPE)
        tt.add_abridge("УЧ.ПОСОБИЕ")
        tt.add_abridge("УЧЕБ.")
        tt.add_abridge("УЧЕБН.")
        tt.add_variant("УЧЕБНИК", False)
        tt.add_variant("ПОСОБИЕ", False)
        BookLinkToken.__m_termins.add(tt)
        tt = Termin._new119("НАВЧАЛЬНИЙ ПОСІБНИК", BookLinkTyp.TYPE, MorphLang.UA)
        tt.add_abridge("НАВЧ.ПОСІБНИК")
        tt.add_abridge("НАВЧ.ПОСІБ")
        tt.add_variant("ПІДРУЧНИК", False)
        tt.add_variant("ПІДРУЧ", False)
        BookLinkToken.__m_termins.add(tt)
        tt = Termin._new118("АВТОРЕФЕРАТ", BookLinkTyp.TYPE)
        tt.add_abridge("АВТОРЕФ.")
        BookLinkToken.__m_termins.add(tt)
        tt = Termin._new118("ДИССЕРТАЦИЯ", BookLinkTyp.TYPE)
        tt.add_variant("ДИСС", False)
        tt.add_abridge("ДИС.")
        tt.add_variant("ДИСЕРТАЦІЯ", False)
        tt.add_variant("DISSERTATION", False)
        BookLinkToken.__m_termins.add(tt)
        tt = Termin._new118("ДОКЛАД", BookLinkTyp.TYPE)
        tt.add_variant("ДОКЛ", False)
        tt.add_abridge("ДОКЛ.")
        tt.add_variant("ДОПОВІДЬ", False)
        BookLinkToken.__m_termins.add(tt)
        tt = Termin._new118("ПОД РЕДАКЦИЕЙ", BookLinkTyp.EDITORS)
        tt.add_abridge("ПОД РЕД")
        tt.add_abridge("ОТВ.РЕД")
        tt.add_abridge("ОТВ.РЕДАКТОР")
        tt.add_variant("ПОД ОБЩЕЙ РЕДАКЦИЕЙ", False)
        tt.add_abridge("ОТВ.РЕД")
        tt.add_abridge("ОТВ.РЕДАКТОР")
        tt.add_abridge("ПОД ОБЩ. РЕД")
        tt.add_abridge("ПОД ОБЩЕЙ РЕД")
        BookLinkToken.__m_termins.add(tt)
        tt = Termin._new119("ПІД РЕДАКЦІЄЮ", BookLinkTyp.EDITORS, MorphLang.UA)
        tt.add_abridge("ПІД РЕД")
        tt.add_abridge("ОТВ.РЕД")
        tt.add_abridge("ВІД. РЕДАКТОР")
        tt.add_variant("ЗА ЗАГ.РЕД", False)
        tt.add_abridge("ВІДПОВІДАЛЬНИЙ РЕДАКТОР")
        BookLinkToken.__m_termins.add(tt)
        tt = Termin._new118("СОСТАВИТЕЛЬ", BookLinkTyp.SOSTAVITEL)
        tt.add_abridge("СОСТ.")
        BookLinkToken.__m_termins.add(tt)
        tt = Termin._new119("УКЛАДАЧ", BookLinkTyp.SOSTAVITEL, MorphLang.UA)
        tt.add_abridge("УКЛ.")
        BookLinkToken.__m_termins.add(tt)
        for s in ["Политиздат", "Прогресс", "Мысль", "Просвещение", "Наука", "Физматлит", "Физматкнига", "Инфра-М", "Питер", "Интеллект", "Аспект пресс", "Аспект-пресс", "АСВ", "Радиотехника", "Радио и связь", "Лань", "Академия", "Академкнига", "URSS", "Академический проект", "БИНОМ", "БВХ", "Вильямс", "Владос", "Волтерс Клувер", "Wolters Kluwer", "Восток-Запад", "Высшая школа", "ГЕО", "Дашков и К", "Кнорус", "Когито-Центр", "КолосС", "Проспект", "РХД", "Статистика", "Финансы и статистика", "Флинта", "Юнити-дана"]: 
            BookLinkToken.__m_termins.add(Termin._new118(s.upper(), BookLinkTyp.PRESS))
        tt = Termin._new118("ИЗДАТЕЛЬСТВО", BookLinkTyp.PRESS)
        tt.add_abridge("ИЗ-ВО")
        tt.add_abridge("ИЗД-ВО")
        tt.add_abridge("ИЗДАТ-ВО")
        tt.add_variant("ISSN", False)
        tt.add_variant("PRESS", False)
        tt.add_variant("VERLAG", False)
        tt.add_variant("JOURNAL", False)
        BookLinkToken.__m_termins.add(tt)
    
    __m_termins = None
    
    @staticmethod
    def parse_start_of_lit_block(t : 'Token') -> 'Token':
        from pullenti.ner.core.internal.BlockLine import BlockLine
        if (t is None): 
            return None
        bl = BlockLine.create(t, None)
        if (bl is not None and bl.typ == BlkTyps.LITERATURE): 
            return bl.end_token
        return None

    
    @staticmethod
    def _new343(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'BookLinkTyp', _arg4 : 'Referent') -> 'BookLinkToken':
        res = BookLinkToken(_arg1, _arg2)
        res.typ = _arg3
        res.ref = _arg4
        return res
    
    @staticmethod
    def _new344(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'BookLinkTyp', _arg4 : 'ReferentToken') -> 'BookLinkToken':
        res = BookLinkToken(_arg1, _arg2)
        res.typ = _arg3
        res.tok = _arg4
        return res
    
    @staticmethod
    def _new345(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'BookLinkTyp') -> 'BookLinkToken':
        res = BookLinkToken(_arg1, _arg2)
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new346(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'BookLinkTyp', _arg4 : str) -> 'BookLinkToken':
        res = BookLinkToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        return res