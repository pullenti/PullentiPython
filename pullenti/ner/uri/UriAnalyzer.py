# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing
import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.Token import Token
from pullenti.ner.TextToken import TextToken
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.bank.internal.PullentiNerBankInternalResourceHelper import PullentiNerBankInternalResourceHelper
from pullenti.ner.core.Termin import Termin
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.Referent import Referent
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.uri.internal.MetaUri import MetaUri
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.uri.internal.UriItemToken import UriItemToken
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.Analyzer import Analyzer
from pullenti.ner.uri.UriReferent import UriReferent

class UriAnalyzer(Analyzer):
    """ Анализатор для выделения URI-объектов (схема:значение) """
    
    ANALYZER_NAME = "URI"
    """ Имя анализатора ("URI") """
    
    @property
    def name(self) -> str:
        return UriAnalyzer.ANALYZER_NAME
    
    @property
    def caption(self) -> str:
        return "URI"
    
    @property
    def description(self) -> str:
        return "URI (URL, EMail), ISBN, УДК, ББК ..."
    
    def clone(self) -> 'Analyzer':
        return UriAnalyzer()
    
    @property
    def progress_weight(self) -> int:
        return 2
    
    @property
    def type_system(self) -> typing.List['ReferentClass']:
        return [MetaUri._global_meta]
    
    @property
    def images(self) -> typing.List[tuple]:
        res = dict()
        res[MetaUri.MAIL_IMAGE_ID] = PullentiNerBankInternalResourceHelper.get_bytes("email.png")
        res[MetaUri.URI_IMAGE_ID] = PullentiNerBankInternalResourceHelper.get_bytes("uri.png")
        return res
    
    @property
    def used_extern_object_types(self) -> typing.List[str]:
        return ["PHONE"]
    
    def create_referent(self, type0_ : str) -> 'Referent':
        if (type0_ == UriReferent.OBJ_TYPENAME): 
            return UriReferent()
        return None
    
    def process(self, kit : 'AnalysisKit') -> None:
        ad = kit.get_analyzer_data(self)
        t = kit.first_token
        first_pass3911 = True
        while True:
            if first_pass3911: first_pass3911 = False
            else: t = t.next0_
            if (not (t is not None)): break
            tt = t
            tok = UriAnalyzer._m_schemes.try_parse(t, TerminParseAttr.NO)
            if (tok is not None): 
                i = (tok.termin.tag)
                tt = tok.end_token
                if (tt.next0_ is not None and tt.next0_.is_char('(')): 
                    tok1 = UriAnalyzer._m_schemes.try_parse(tt.next0_.next0_, TerminParseAttr.NO)
                    if ((tok1 is not None and tok1.termin.canonic_text == tok.termin.canonic_text and tok1.end_token.next0_ is not None) and tok1.end_token.next0_.is_char(')')): 
                        tt = tok1.end_token.next0_
                if (i == 0): 
                    if ((tt.next0_ is None or ((not tt.next0_.is_char_of(":|") and not tt.is_table_control_char)) or tt.next0_.is_whitespace_before) or tt.next0_.whitespaces_after_count > 2): 
                        continue
                    t1 = tt.next0_.next0_
                    while t1 is not None and t1.is_char_of("/\\"):
                        t1 = t1.next0_
                    if (t1 is None or t1.whitespaces_before_count > 2): 
                        continue
                    ut = UriItemToken.attach_uri_content(t1, False)
                    if (ut is None): 
                        continue
                    ur = Utils.asObjectOrNull(ad.register_referent(UriReferent._new2710(tok.termin.canonic_text.lower(), ut.value)), UriReferent)
                    rt = ReferentToken(ad.register_referent(ur), t, ut.end_token)
                    rt.begin_token = Utils.ifNotNull(UriAnalyzer.__site_before(t.previous), t)
                    if (rt.end_token.next0_ is not None and rt.end_token.next0_.is_char_of("/\\")): 
                        rt.end_token = rt.end_token.next0_
                    kit.embed_token(rt)
                    t = (rt)
                    continue
                if (i == 10): 
                    tt = tt.next0_
                    if (tt is None or not tt.is_char(':')): 
                        continue
                    tt = tt.next0_
                    while tt is not None: 
                        if (tt.is_char_of("/\\")): 
                            pass
                        else: 
                            break
                        tt = tt.next0_
                    if (tt is None): 
                        continue
                    if (tt.is_value("WWW", None) and tt.next0_ is not None and tt.next0_.is_char('.')): 
                        tt = tt.next0_.next0_
                    if (tt is None or tt.is_newline_before): 
                        continue
                    ut = UriItemToken.attach_uri_content(tt, True)
                    if (ut is None): 
                        continue
                    if (len(ut.value) < 4): 
                        continue
                    ur = Utils.asObjectOrNull(ad.register_referent(UriReferent._new2710(tok.termin.canonic_text.lower(), ut.value)), UriReferent)
                    rt = ReferentToken(ad.register_referent(ur), t, ut.end_token)
                    rt.begin_token = Utils.ifNotNull(UriAnalyzer.__site_before(t.previous), t)
                    if (rt.end_token.next0_ is not None and rt.end_token.next0_.is_char_of("/\\")): 
                        rt.end_token = rt.end_token.next0_
                    kit.embed_token(rt)
                    t = (rt)
                    continue
                if (i == 2): 
                    if (tt.next0_ is None or not tt.next0_.is_char('.') or tt.next0_.is_whitespace_before): 
                        continue
                    if (tt.next0_.is_whitespace_after and tok.termin.canonic_text != "WWW"): 
                        continue
                    ut = UriItemToken.attach_uri_content(tt.next0_.next0_, True)
                    if (ut is None): 
                        continue
                    ur = Utils.asObjectOrNull(ad.register_referent(UriReferent._new2710("http", ut.value)), UriReferent)
                    rt = ReferentToken(ur, t, ut.end_token)
                    rt.begin_token = Utils.ifNotNull(UriAnalyzer.__site_before(t.previous), t)
                    if (rt.end_token.next0_ is not None and rt.end_token.next0_.is_char_of("/\\")): 
                        rt.end_token = rt.end_token.next0_
                    kit.embed_token(rt)
                    t = (rt)
                    continue
                if (i == 1): 
                    sch = tok.termin.canonic_text
                    ut = None
                    if (sch == "ISBN"): 
                        ut = UriItemToken.attachisbn(tt.next0_)
                        if ((ut is None and t.previous is not None and t.previous.is_char('(')) and t.next0_ is not None and t.next0_.is_char(')')): 
                            tt0 = t.previous.previous
                            while tt0 is not None: 
                                if (tt0.whitespaces_after_count > 2): 
                                    break
                                if (tt0.is_whitespace_before): 
                                    ut = UriItemToken.attachisbn(tt0)
                                    if (ut is not None and ut.end_token.next0_ != t.previous): 
                                        ut = (None)
                                    break
                                tt0 = tt0.previous
                    elif ((sch == "RFC" or sch == "ISO" or sch == "ОКФС") or sch == "ОКОПФ"): 
                        ut = UriItemToken.attachisocontent(tt.next0_, ":")
                    elif (sch == "ГОСТ"): 
                        ut = UriItemToken.attachisocontent(tt.next0_, "-.")
                    elif (sch == "ТУ"): 
                        if (tok.chars.is_all_upper): 
                            ut = UriItemToken.attachisocontent(tt.next0_, "-.")
                            if (ut is not None and (ut.length_char < 10)): 
                                ut = (None)
                    else: 
                        ut = UriItemToken.attachbbk(tt.next0_)
                    if (ut is None): 
                        continue
                    ur = Utils.asObjectOrNull(ad.register_referent(UriReferent._new2713(ut.value, sch)), UriReferent)
                    if (ut.begin_char < t.begin_char): 
                        rt = ReferentToken(ur, ut.begin_token, t)
                        if (t.next0_ is not None and t.next0_.is_char(')')): 
                            rt.end_token = t.next0_
                    else: 
                        rt = ReferentToken(ur, t, ut.end_token)
                    if (t.previous is not None and t.previous.is_value("КОД", None)): 
                        rt.begin_token = t.previous
                    if (ur.scheme.startswith("ОК")): 
                        UriAnalyzer.__check_detail(rt)
                    kit.embed_token(rt)
                    t = (rt)
                    if (ur.scheme.startswith("ОК")): 
                        while t.next0_ is not None:
                            if (t.next0_.is_comma_and and (isinstance(t.next0_.next0_, NumberToken))): 
                                pass
                            else: 
                                break
                            ut = UriItemToken.attachbbk(t.next0_.next0_)
                            if (ut is None): 
                                break
                            ur = (Utils.asObjectOrNull(ad.register_referent(UriReferent._new2713(ut.value, sch)), UriReferent))
                            rt = ReferentToken(ur, t.next0_.next0_, ut.end_token)
                            UriAnalyzer.__check_detail(rt)
                            kit.embed_token(rt)
                            t = (rt)
                    continue
                if (i == 3): 
                    t0 = tt.next0_
                    while t0 is not None:
                        if (t0.is_char_of(":|") or t0.is_table_control_char or t0.is_hiphen): 
                            t0 = t0.next0_
                        else: 
                            break
                    if (t0 is None): 
                        continue
                    ut = UriItemToken.attach_skype(t0)
                    if (ut is None): 
                        continue
                    ur = Utils.asObjectOrNull(ad.register_referent(UriReferent._new2713(ut.value.lower(), ("skype" if tok.termin.canonic_text == "SKYPE" else tok.termin.canonic_text))), UriReferent)
                    rt = ReferentToken(ur, t, ut.end_token)
                    kit.embed_token(rt)
                    t = (rt)
                    continue
                if (i == 4): 
                    t0 = tt.next0_
                    if (t0 is not None and ((t0.is_char(':') or t0.is_hiphen))): 
                        t0 = t0.next0_
                    if (t0 is None): 
                        continue
                    ut = UriItemToken.attach_icq_content(t0)
                    if (ut is None): 
                        continue
                    ur = Utils.asObjectOrNull(ad.register_referent(UriReferent._new2713(ut.value, "ICQ")), UriReferent)
                    rt = ReferentToken(ur, t, t0)
                    kit.embed_token(rt)
                    t = (rt)
                    continue
                if (i == 5 or i == 6): 
                    t0 = tt.next0_
                    has_tab_cel = False
                    is_iban = False
                    first_pass3912 = True
                    while True:
                        if first_pass3912: first_pass3912 = False
                        else: t0 = t0.next0_
                        if (not (t0 is not None)): break
                        if ((((t0.is_value("БАНК", None) or t0.morph.class0_.is_preposition or t0.is_hiphen) or t0.is_char_of(".:") or t0.is_value("РУБЛЬ", None)) or t0.is_value("РУБ", None) or t0.is_value("ДОЛЛАР", None)) or t0.is_value("№", None) or t0.is_value("N", None)): 
                            pass
                        elif (t0.is_table_control_char): 
                            has_tab_cel = True
                        elif (t0.is_char_of("\\/") and t0.next0_ is not None and t0.next0_.is_value("IBAN", None)): 
                            is_iban = True
                            t0 = t0.next0_
                        elif (t0.is_value("IBAN", None)): 
                            is_iban = True
                        elif (isinstance(t0, TextToken)): 
                            npt = NounPhraseHelper.try_parse(t0, NounPhraseParseAttr.NO, 0, None)
                            if (npt is not None and npt.morph.case_.is_genitive): 
                                t0 = npt.end_token
                                continue
                            break
                        else: 
                            break
                    if (t0 is None): 
                        continue
                    ur2 = None
                    ur2begin = None
                    ur2end = None
                    t00 = t0
                    val = t0.get_source_text()
                    if (str.isdigit(val[0]) and ((((i == 6 or tok.termin.canonic_text == "ИНН" or tok.termin.canonic_text == "БИК") or tok.termin.canonic_text == "ОГРН" or tok.termin.canonic_text == "СНИЛС") or tok.termin.canonic_text == "ОКПО"))): 
                        if (t0.chars.is_letter): 
                            continue
                        if (Utils.isNullOrEmpty(val) or not str.isdigit(val[0])): 
                            continue
                        if (t0.length_char < 9): 
                            tmp = io.StringIO()
                            print(val, end="", file=tmp)
                            ttt = t0.next0_
                            first_pass3913 = True
                            while True:
                                if first_pass3913: first_pass3913 = False
                                else: ttt = ttt.next0_
                                if (not (ttt is not None)): break
                                if (ttt.whitespaces_before_count > 1): 
                                    break
                                if (isinstance(ttt, NumberToken)): 
                                    print(ttt.get_source_text(), end="", file=tmp)
                                    t0 = ttt
                                    continue
                                if (ttt.is_hiphen or ttt.is_char('.')): 
                                    if (ttt.next0_ is None or not (isinstance(ttt.next0_, NumberToken))): 
                                        break
                                    if (ttt.is_whitespace_after or ttt.is_whitespace_before): 
                                        break
                                    continue
                                break
                            val = (None)
                            if (tmp.tell() == 20): 
                                val = Utils.toStringStringIO(tmp)
                            elif (tmp.tell() == 9 and tok.termin.canonic_text == "БИК"): 
                                val = Utils.toStringStringIO(tmp)
                            elif (((tmp.tell() == 10 or tmp.tell() == 12)) and tok.termin.canonic_text == "ИНН"): 
                                val = Utils.toStringStringIO(tmp)
                            elif (tmp.tell() >= 15 and tok.termin.canonic_text == "Л/С"): 
                                val = Utils.toStringStringIO(tmp)
                            elif (tmp.tell() >= 11 and ((tok.termin.canonic_text == "ОГРН" or tok.termin.canonic_text == "СНИЛС"))): 
                                val = Utils.toStringStringIO(tmp)
                            elif (tok.termin.canonic_text == "ОКПО"): 
                                val = Utils.toStringStringIO(tmp)
                        if (val is None): 
                            continue
                    elif (not (isinstance(t0, NumberToken))): 
                        if ((isinstance(t0, TextToken)) and is_iban): 
                            tmp1 = io.StringIO()
                            t1 = None
                            ttt = t0
                            first_pass3914 = True
                            while True:
                                if first_pass3914: first_pass3914 = False
                                else: ttt = ttt.next0_
                                if (not (ttt is not None)): break
                                if (ttt.is_newline_before and ttt != t0): 
                                    break
                                if (ttt.is_hiphen): 
                                    continue
                                if (not (isinstance(ttt, NumberToken))): 
                                    if (not (isinstance(ttt, TextToken)) or not ttt.chars.is_latin_letter): 
                                        break
                                print(ttt.get_source_text(), end="", file=tmp1)
                                t1 = ttt
                                if (tmp1.tell() >= 34): 
                                    break
                            if (tmp1.tell() < 10): 
                                continue
                            ur1 = UriReferent._new2713(Utils.toStringStringIO(tmp1), tok.termin.canonic_text)
                            ur1.add_slot(UriReferent.ATTR_DETAIL, "IBAN", False, 0)
                            rt1 = ReferentToken(ad.register_referent(ur1), t, t1)
                            kit.embed_token(rt1)
                            t = (rt1)
                            continue
                        if (not t0.is_char_of("/\\") or t0.next0_ is None): 
                            continue
                        tok2 = UriAnalyzer._m_schemes.try_parse(t0.next0_, TerminParseAttr.NO)
                        if (tok2 is None or not (isinstance(tok2.termin.tag, int)) or (tok2.termin.tag) != i): 
                            continue
                        t0 = tok2.end_token.next0_
                        while t0 is not None:
                            if (t0.is_char_of(":N№")): 
                                t0 = t0.next0_
                            elif (t0.is_table_control_char): 
                                t0 = t0.next0_
                                t00 = t0
                                has_tab_cel = True
                            else: 
                                break
                        if (not (isinstance(t0, NumberToken))): 
                            continue
                        tmp = io.StringIO()
                        while t0 is not None: 
                            if (not (isinstance(t0, NumberToken))): 
                                break
                            print(t0.get_source_text(), end="", file=tmp)
                            t0 = t0.next0_
                        if (t0 is None or not t0.is_char_of("/\\,") or not (isinstance(t0.next0_, NumberToken))): 
                            continue
                        val = Utils.toStringStringIO(tmp)
                        Utils.setLengthStringIO(tmp, 0)
                        ur2begin = t0.next0_
                        t0 = t0.next0_
                        while t0 is not None: 
                            if (not (isinstance(t0, NumberToken))): 
                                break
                            if (t0.whitespaces_before_count > 4 and tmp.tell() > 0): 
                                break
                            print(t0.get_source_text(), end="", file=tmp)
                            ur2end = t0
                            t0 = t0.next0_
                        ur2 = (Utils.asObjectOrNull(ad.register_referent(UriReferent._new2710(tok2.termin.canonic_text, Utils.toStringStringIO(tmp))), UriReferent))
                    if (len(val) < 5): 
                        continue
                    ur = Utils.asObjectOrNull(ad.register_referent(UriReferent._new2713(val, tok.termin.canonic_text)), UriReferent)
                    rt = ReferentToken(ur, t, (t0 if ur2begin is None else ur2begin.previous))
                    if (has_tab_cel): 
                        rt.begin_token = t00
                    if (ur.scheme.startswith("ОК")): 
                        UriAnalyzer.__check_detail(rt)
                    ttt = t.previous
                    first_pass3915 = True
                    while True:
                        if first_pass3915: first_pass3915 = False
                        else: ttt = ttt.previous
                        if (not (ttt is not None)): break
                        if (ttt.is_table_control_char): 
                            break
                        if (ttt.morph.class0_.is_preposition): 
                            continue
                        if (ttt.is_value("ОРГАНИЗАЦИЯ", None)): 
                            continue
                        if (ttt.is_value("НОМЕР", None) or ttt.is_value("КОД", None)): 
                            rt.begin_token = ttt
                            t = rt.begin_token
                        break
                    kit.embed_token(rt)
                    t = (rt)
                    if (ur2 is not None): 
                        rt2 = ReferentToken(ur2, ur2begin, ur2end)
                        kit.embed_token(rt2)
                        t = (rt2)
                    while (t.next0_ is not None and t.next0_.is_comma_and and (isinstance(t.next0_.next0_, NumberToken))) and t.next0_.next0_.length_char == len(val) and t.next0_.next0_.typ == NumberSpellingType.DIGIT:
                        val2 = t.next0_.next0_.get_source_text()
                        ur2 = UriReferent()
                        ur2.scheme = ur.scheme
                        ur2.value = val2
                        ur2 = (Utils.asObjectOrNull(ad.register_referent(ur2), UriReferent))
                        rt2 = ReferentToken(ur2, t.next0_, t.next0_.next0_)
                        kit.embed_token(rt2)
                        t = (rt2)
                    continue
                continue
            if (t.is_char('@')): 
                u1s = UriItemToken.attach_mail_users(t.previous)
                if (u1s is None): 
                    continue
                u2 = UriItemToken.attach_domain_name(t.next0_, False, True)
                if (u2 is None): 
                    continue
                for ii in range(len(u1s) - 1, -1, -1):
                    ur = Utils.asObjectOrNull(ad.register_referent(UriReferent._new2713("{0}@{1}".format(u1s[ii].value, u2.value).lower(), "mailto")), UriReferent)
                    b = u1s[ii].begin_token
                    t0 = b.previous
                    if (t0 is not None and t0.is_char(':')): 
                        t0 = t0.previous
                    if (t0 is not None and ii == 0): 
                        br = False
                        ttt = t0
                        first_pass3916 = True
                        while True:
                            if first_pass3916: first_pass3916 = False
                            else: ttt = ttt.previous
                            if (not (ttt is not None)): break
                            if (not (isinstance(ttt, TextToken))): 
                                break
                            if (ttt != t0 and ttt.whitespaces_after_count > 1): 
                                break
                            if (ttt.is_char(')')): 
                                br = True
                                continue
                            if (ttt.is_char('(')): 
                                if (not br): 
                                    break
                                br = False
                                continue
                            if (ttt.is_value("EMAIL", None) or ttt.is_value("MAILTO", None)): 
                                b = ttt
                                break
                            if (ttt.is_value("MAIL", None)): 
                                b = ttt
                                if ((ttt.previous is not None and ttt.previous.is_hiphen and ttt.previous.previous is not None) and ((ttt.previous.previous.is_value("E", None) or ttt.previous.previous.is_value("Е", None)))): 
                                    b = ttt.previous.previous
                                break
                            if (ttt.is_value("ПОЧТА", None) or ttt.is_value("АДРЕС", None)): 
                                b = t0
                                ttt = ttt.previous
                                if (ttt is not None and ttt.is_char('.')): 
                                    ttt = ttt.previous
                                if (ttt is not None and ((t0.is_value("ЭЛ", None) or ttt.is_value("ЭЛЕКТРОННЫЙ", None)))): 
                                    b = ttt
                                if (b.previous is not None and b.previous.is_value("АДРЕС", None)): 
                                    b = b.previous
                                break
                            if (ttt.morph.class0_.is_preposition): 
                                continue
                    rt = ReferentToken(ur, b, (u2.end_token if ii == (len(u1s) - 1) else u1s[ii].end_token))
                    kit.embed_token(rt)
                    t = (rt)
                continue
            if (not t.chars.is_cyrillic_letter): 
                if (t.is_whitespace_before or ((t.previous is not None and t.previous.is_char_of(",(")))): 
                    u1 = UriItemToken.attach_url(t)
                    if (u1 is not None): 
                        if (u1.is_whitespace_after or u1.end_token.next0_ is None or not u1.end_token.next0_.is_char('@')): 
                            if (u1.end_token.next0_ is not None and u1.end_token.next0_.is_char_of("\\/")): 
                                u2 = UriItemToken.attach_uri_content(t, False)
                                if (u2 is not None): 
                                    u1 = u2
                            ur = Utils.asObjectOrNull(ad.register_referent(UriReferent._new2710("http", u1.value)), UriReferent)
                            rt = ReferentToken(ur, u1.begin_token, u1.end_token)
                            rt.begin_token = Utils.ifNotNull(UriAnalyzer.__site_before(u1.begin_token.previous), u1.begin_token)
                            kit.embed_token(rt)
                            t = (rt)
                            continue
            if ((isinstance(t, TextToken)) and not t.is_whitespace_after and t.length_char > 2): 
                if (UriAnalyzer.__site_before(t.previous) is not None): 
                    ut = UriItemToken.attach_uri_content(t, True)
                    if (ut is None or ut.value.find('.') <= 0 or ut.value.find('@') > 0): 
                        continue
                    ur = Utils.asObjectOrNull(ad.register_referent(UriReferent._new2710("http", ut.value)), UriReferent)
                    rt = ReferentToken(ur, t, ut.end_token)
                    rt.begin_token = UriAnalyzer.__site_before(t.previous)
                    if (rt.end_token.next0_ is not None and rt.end_token.next0_.is_char_of("/\\")): 
                        rt.end_token = rt.end_token.next0_
                    kit.embed_token(rt)
                    t = (rt)
                    continue
            if ((t.chars.is_latin_letter and not t.chars.is_all_lower and t.next0_ is not None) and not t.is_whitespace_after): 
                if (t.next0_.is_char('/')): 
                    rt = UriAnalyzer.__try_attach_lotus(Utils.asObjectOrNull(t, TextToken))
                    if (rt is not None): 
                        rt.referent = ad.register_referent(rt.referent)
                        kit.embed_token(rt)
                        t = (rt)
                        continue
    
    @staticmethod
    def __check_detail(rt : 'ReferentToken') -> None:
        if (rt.end_token.whitespaces_after_count > 2 or rt.end_token.next0_ is None): 
            return
        if (rt.end_token.next0_.is_char('(')): 
            br = BracketHelper.try_parse(rt.end_token.next0_, BracketParseAttr.NO, 100)
            if (br is not None): 
                rt.referent.detail = MiscHelper.get_text_value(br.begin_token.next0_, br.end_token.previous, GetTextAttr.NO)
                rt.end_token = br.end_token
    
    @staticmethod
    def __site_before(t : 'Token') -> 'Token':
        if (t is not None and t.is_char(':')): 
            t = t.previous
        if (t is None): 
            return None
        if ((t.is_value("ВЕБСАЙТ", None) or t.is_value("WEBSITE", None) or t.is_value("WEB", None)) or t.is_value("WWW", None)): 
            return t
        t0 = None
        if (t.is_value("САЙТ", None) or t.is_value("SITE", None)): 
            t0 = t
            t = t.previous
        elif (t.is_value("АДРЕС", None)): 
            t0 = t.previous
            if (t0 is not None and t0.is_char('.')): 
                t0 = t0.previous
            if (t0 is not None): 
                if (t0.is_value("ЭЛ", None) or t0.is_value("ЭЛЕКТРОННЫЙ", None)): 
                    return t0
            return None
        else: 
            return None
        if (t is not None and t.is_hiphen): 
            t = t.previous
        if (t is None): 
            return t0
        if (t.is_value("WEB", None) or t.is_value("ВЕБ", None)): 
            t0 = t
        if (t0.previous is not None and t0.previous.morph.class0_.is_adjective and (t0.whitespaces_before_count < 3)): 
            npt = NounPhraseHelper.try_parse(t0.previous, NounPhraseParseAttr.NO, 0, None)
            if (npt is not None): 
                t0 = npt.begin_token
        return t0
    
    @staticmethod
    def __try_attach_lotus(t : 'TextToken') -> 'ReferentToken':
        if (t is None or t.next0_ is None): 
            return None
        t1 = t.next0_.next0_
        tails = None
        tt = t1
        while tt is not None: 
            if (tt.is_whitespace_before): 
                if (not tt.is_newline_before): 
                    break
                if (tails is None or (len(tails) < 2)): 
                    break
            if (not tt.is_letters or tt.chars.is_all_lower): 
                return None
            if (not (isinstance(tt, TextToken))): 
                return None
            if (tails is None): 
                tails = list()
            tails.append(tt.term)
            t1 = tt
            if (tt.is_whitespace_after or tt.next0_ is None): 
                break
            tt = tt.next0_
            if (not tt.is_char('/')): 
                break
            tt = tt.next0_
        if (tails is None or (len(tails) < 3)): 
            return None
        heads = list()
        heads.append(t.term)
        t0 = t
        ok = True
        for k in range(2):
            if (not (isinstance(t0.previous, TextToken))): 
                break
            if (t0.whitespaces_before_count != 1): 
                if (not t0.is_newline_before or k > 0): 
                    break
            if (not t0.is_whitespace_before and t0.previous.is_char('/')): 
                break
            if (t0.previous.chars == t.chars): 
                t0 = t0.previous
                heads.insert(0, t0.term)
                ok = True
                continue
            if ((t0.previous.chars.is_latin_letter and t0.previous.chars.is_all_upper and t0.previous.length_char == 1) and k == 0): 
                t0 = t0.previous
                heads.insert(0, t0.term)
                ok = False
                continue
            break
        if (not ok): 
            del heads[0]
        tmp = io.StringIO()
        i = 0
        while i < len(heads): 
            if (i > 0): 
                print(' ', end="", file=tmp)
            print(MiscHelper.convert_first_char_upper_and_other_lower(heads[i]), end="", file=tmp)
            i += 1
        for tail in tails: 
            print("/{0}".format(tail), end="", file=tmp, flush=True)
        if (((t1.next0_ is not None and t1.next0_.is_char('@') and t1.next0_.next0_ is not None) and t1.next0_.next0_.chars.is_latin_letter and not t1.next0_.is_whitespace_after) and not t1.is_whitespace_after): 
            t1 = t1.next0_.next0_
        uri_ = UriReferent._new2710("lotus", Utils.toStringStringIO(tmp))
        return ReferentToken(uri_, t0, t1)
    
    _m_schemes = None
    
    @staticmethod
    def initialize() -> None:
        if (UriAnalyzer._m_schemes is not None): 
            return
        Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = True
        MetaUri.initialize()
        try: 
            UriAnalyzer._m_schemes = TerminCollection()
            obj = PullentiNerBankInternalResourceHelper.get_string("UriSchemes.csv")
            if (obj is None): 
                raise Utils.newException("Can't file resource file {0} in Organization analyzer".format("UriSchemes.csv"), None)
            for line0 in Utils.splitString(obj, '\n', False): 
                line = line0.strip()
                if (Utils.isNullOrEmpty(line)): 
                    continue
                UriAnalyzer._m_schemes.add(Termin._new530(line, MorphLang.UNKNOWN, True, 0))
            for s in ["ISBN", "УДК", "ББК", "ТНВЭД", "ОКВЭД"]: 
                UriAnalyzer._m_schemes.add(Termin._new530(s, MorphLang.UNKNOWN, True, 1))
            UriAnalyzer._m_schemes.add(Termin._new2726("Общероссийский классификатор форм собственности", "ОКФС", 1, "ОКФС"))
            UriAnalyzer._m_schemes.add(Termin._new2726("Общероссийский классификатор организационно правовых форм", "ОКОПФ", 1, "ОКОПФ"))
            UriAnalyzer._m_schemes.add(Termin._new530("WWW", MorphLang.UNKNOWN, True, 2))
            UriAnalyzer._m_schemes.add(Termin._new530("HTTP", MorphLang.UNKNOWN, True, 10))
            UriAnalyzer._m_schemes.add(Termin._new530("HTTPS", MorphLang.UNKNOWN, True, 10))
            UriAnalyzer._m_schemes.add(Termin._new530("SHTTP", MorphLang.UNKNOWN, True, 10))
            UriAnalyzer._m_schemes.add(Termin._new530("FTP", MorphLang.UNKNOWN, True, 10))
            t = Termin._new530("SKYPE", MorphLang.UNKNOWN, True, 3)
            t.add_variant("СКАЙП", True)
            t.add_variant("SKYPEID", True)
            t.add_variant("SKYPE ID", True)
            UriAnalyzer._m_schemes.add(t)
            t = Termin._new530("SWIFT", MorphLang.UNKNOWN, True, 3)
            t.add_variant("СВИФТ", True)
            UriAnalyzer._m_schemes.add(t)
            UriAnalyzer._m_schemes.add(Termin._new530("ICQ", MorphLang.UNKNOWN, True, 4))
            UriAnalyzer._m_schemes.add(Termin._new2736("International Mobile Equipment Identity", "IMEI", 5, "IMEI", True))
            t = Termin._new2736("основной государственный регистрационный номер", "ОГРН", 5, "ОГРН", True)
            t.add_variant("ОГРН ИП", True)
            UriAnalyzer._m_schemes.add(t)
            UriAnalyzer._m_schemes.add(Termin._new2736("Индивидуальный идентификационный номер", "ИИН", 5, "ИИН", True))
            UriAnalyzer._m_schemes.add(Termin._new2736("Индивидуальный номер налогоплательщика", "ИНН", 5, "ИНН", True))
            UriAnalyzer._m_schemes.add(Termin._new2736("Код причины постановки на учет", "КПП", 5, "КПП", True))
            UriAnalyzer._m_schemes.add(Termin._new2736("Банковский идентификационный код", "БИК", 5, "БИК", True))
            UriAnalyzer._m_schemes.add(Termin._new2736("основной государственный регистрационный номер индивидуального предпринимателя", "ОГРНИП", 5, "ОГРНИП", True))
            t = Termin._new2736("Страховой номер индивидуального лицевого счёта", "СНИЛС", 5, "СНИЛС", True)
            t.add_variant("Свидетельство пенсионного страхования", False)
            t.add_variant("Страховое свидетельство обязательного пенсионного страхования", False)
            t.add_variant("Страховое свидетельство", False)
            UriAnalyzer._m_schemes.add(t)
            UriAnalyzer._m_schemes.add(Termin._new2736("Общероссийский классификатор предприятий и организаций", "ОКПО", 5, "ОКПО", True))
            UriAnalyzer._m_schemes.add(Termin._new2736("Общероссийский классификатор объектов административно-территориального деления", "ОКАТО", 5, "ОКАТО", True))
            UriAnalyzer._m_schemes.add(Termin._new2736("Общероссийский классификатор территорий муниципальных образований", "ОКТМО", 5, "ОКТМО", True))
            UriAnalyzer._m_schemes.add(Termin._new2736("Общероссийский классификатор органов государственной власти и управления", "ОКОГУ", 5, "ОКОГУ", True))
            UriAnalyzer._m_schemes.add(Termin._new2736("Общероссийский классификатор Отрасли народного хозяйства", "ОКОНХ", 5, "ОКОНХ", True))
            t = Termin._new2749("РАСЧЕТНЫЙ СЧЕТ", MorphLang.UNKNOWN, True, "Р/С", 6, 20)
            t.add_abridge("Р.С.")
            t.add_abridge("Р.СЧ.")
            t.add_abridge("P.C.")
            t.add_abridge("РАСЧ.СЧЕТ")
            t.add_abridge("РАС.СЧЕТ")
            t.add_abridge("РАСЧ.СЧ.")
            t.add_abridge("РАС.СЧ.")
            t.add_abridge("Р.СЧЕТ")
            t.add_variant("СЧЕТ ПОЛУЧАТЕЛЯ", False)
            t.add_variant("СЧЕТ ОТПРАВИТЕЛЯ", False)
            t.add_variant("СЧЕТ", False)
            UriAnalyzer._m_schemes.add(t)
            t = Termin._new2750("ЛИЦЕВОЙ СЧЕТ", "Л/С", 6, 20)
            t.add_abridge("Л.С.")
            t.add_abridge("Л.СЧ.")
            t.add_abridge("Л/С")
            t.add_abridge("ЛИЦ.СЧЕТ")
            t.add_abridge("ЛИЦ.СЧ.")
            t.add_abridge("Л.СЧЕТ")
            UriAnalyzer._m_schemes.add(t)
            t = Termin._new2749("СПЕЦИАЛЬНЫЙ ЛИЦЕВОЙ СЧЕТ", MorphLang.UNKNOWN, True, "СПЕЦ/С", 6, 20)
            t.add_abridge("СПЕЦ.С.")
            t.add_abridge("СПЕЦ.СЧЕТ")
            t.add_abridge("СПЕЦ.СЧ.")
            t.add_variant("СПЕЦСЧЕТ", True)
            t.add_variant("СПЕЦИАЛЬНЫЙ СЧЕТ", True)
            UriAnalyzer._m_schemes.add(t)
            t = Termin._new2749("КОРРЕСПОНДЕНТСКИЙ СЧЕТ", MorphLang.UNKNOWN, True, "К/С", 6, 20)
            t.add_abridge("КОРР.СЧЕТ")
            t.add_abridge("КОР.СЧЕТ")
            t.add_abridge("КОРР.СЧ.")
            t.add_abridge("КОР.СЧ.")
            t.add_abridge("К.СЧЕТ")
            t.add_abridge("КОР.С.")
            t.add_abridge("К.С.")
            t.add_abridge("K.C.")
            t.add_abridge("К-С")
            t.add_abridge("К/С")
            t.add_abridge("К.СЧ.")
            t.add_abridge("К/СЧ")
            UriAnalyzer._m_schemes.add(t)
            t = Termin._new2753("КОД БЮДЖЕТНОЙ КЛАССИФИКАЦИИ", "КБК", "КБК", 6, 20, True)
            UriAnalyzer._m_schemes.add(t)
            UriItemToken.initialize()
        except Exception as ex: 
            raise Utils.newException(ex.__str__(), ex)
        Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = False
        ProcessorService.register_analyzer(UriAnalyzer())