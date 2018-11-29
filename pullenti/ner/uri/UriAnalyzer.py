# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import typing
import io
from pullenti.unisharp.Utils import Utils
from pullenti.ner.Analyzer import Analyzer
from pullenti.ner.bank.internal.EpNerBankInternalResourceHelper import EpNerBankInternalResourceHelper
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.core.GetTextAttr import GetTextAttr


class UriAnalyzer(Analyzer):
    """ Картридж для выделения интернетных объектов (URL, E-mail) """
    
    ANALYZER_NAME = "URI"
    
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
        from pullenti.ner.uri.internal.MetaUri import MetaUri
        return [MetaUri._global_meta]
    
    @property
    def images(self) -> typing.List[tuple]:
        from pullenti.ner.uri.internal.MetaUri import MetaUri
        res = dict()
        res[MetaUri.MAIL_IMAGE_ID] = EpNerBankInternalResourceHelper.getBytes("email.png")
        res[MetaUri.URI_IMAGE_ID] = EpNerBankInternalResourceHelper.getBytes("uri.png")
        return res
    
    @property
    def used_extern_object_types(self) -> typing.List[str]:
        return ["PHONE"]
    
    def createReferent(self, type0_ : str) -> 'Referent':
        from pullenti.ner.uri.UriReferent import UriReferent
        if (type0_ == UriReferent.OBJ_TYPENAME): 
            return UriReferent()
        return None
    
    def process(self, kit : 'AnalysisKit') -> None:
        """ Основная функция выделения объектов
        
        Args:
            container: 
            lastStage: 
        
        """
        from pullenti.ner.uri.internal.UriItemToken import UriItemToken
        from pullenti.ner.uri.UriReferent import UriReferent
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        ad = kit.getAnalyzerData(self)
        t = kit.first_token
        first_pass3161 = True
        while True:
            if first_pass3161: first_pass3161 = False
            else: t = t.next0_
            if (not (t is not None)): break
            tt = t
            tok = UriAnalyzer.__m_schemes.tryParse(t, TerminParseAttr.NO)
            if (tok is not None): 
                i = (tok.termin.tag)
                tt = tok.end_token
                if (tt.next0_ is not None and tt.next0_.isChar('(')): 
                    tok1 = UriAnalyzer.__m_schemes.tryParse(tt.next0_.next0_, TerminParseAttr.NO)
                    if ((tok1 is not None and tok1.termin.canonic_text == tok.termin.canonic_text and tok1.end_token.next0_ is not None) and tok1.end_token.next0_.isChar(')')): 
                        tt = tok1.end_token.next0_
                if (i == 0): 
                    if ((tt.next0_ is None or ((not tt.next0_.isCharOf(":|") and not tt.is_table_control_char)) or tt.next0_.is_whitespace_before) or tt.next0_.whitespaces_after_count > 2): 
                        continue
                    t1 = tt.next0_.next0_
                    while t1 is not None and t1.isCharOf("/\\"):
                        t1 = t1.next0_
                    if (t1 is None or t1.whitespaces_before_count > 2): 
                        continue
                    ut = UriItemToken.attachUriContent(t1, False)
                    if (ut is None): 
                        continue
                    ur = Utils.asObjectOrNull(ad.registerReferent(UriReferent._new2569(tok.termin.canonic_text.lower(), ut.value)), UriReferent)
                    rt = ReferentToken(ad.registerReferent(ur), t, ut.end_token)
                    rt.begin_token = Utils.ifNotNull(UriAnalyzer.__siteBefore(t.previous), t)
                    if (rt.end_token.next0_ is not None and rt.end_token.next0_.isCharOf("/\\")): 
                        rt.end_token = rt.end_token.next0_
                    kit.embedToken(rt)
                    t = (rt)
                    continue
                if (i == 10): 
                    tt = tt.next0_
                    if (tt is None or not tt.isChar(':')): 
                        continue
                    tt = tt.next0_
                    while tt is not None: 
                        if (tt.isCharOf("/\\")): 
                            pass
                        else: 
                            break
                        tt = tt.next0_
                    if (tt is None): 
                        continue
                    if (tt.isValue("WWW", None) and tt.next0_ is not None and tt.next0_.isChar('.')): 
                        tt = tt.next0_.next0_
                    if (tt is None or tt.is_newline_before): 
                        continue
                    ut = UriItemToken.attachUriContent(tt, True)
                    if (ut is None): 
                        continue
                    if (len(ut.value) < 4): 
                        continue
                    ur = Utils.asObjectOrNull(ad.registerReferent(UriReferent._new2569(tok.termin.canonic_text.lower(), ut.value)), UriReferent)
                    rt = ReferentToken(ad.registerReferent(ur), t, ut.end_token)
                    rt.begin_token = Utils.ifNotNull(UriAnalyzer.__siteBefore(t.previous), t)
                    if (rt.end_token.next0_ is not None and rt.end_token.next0_.isCharOf("/\\")): 
                        rt.end_token = rt.end_token.next0_
                    kit.embedToken(rt)
                    t = (rt)
                    continue
                if (i == 2): 
                    if (tt.next0_ is None or not tt.next0_.isChar('.') or tt.next0_.is_whitespace_before): 
                        continue
                    if (tt.next0_.is_whitespace_after and tok.termin.canonic_text != "WWW"): 
                        continue
                    ut = UriItemToken.attachUriContent(tt.next0_.next0_, True)
                    if (ut is None): 
                        continue
                    ur = Utils.asObjectOrNull(ad.registerReferent(UriReferent._new2569("http", ut.value)), UriReferent)
                    rt = ReferentToken(ur, t, ut.end_token)
                    rt.begin_token = Utils.ifNotNull(UriAnalyzer.__siteBefore(t.previous), t)
                    if (rt.end_token.next0_ is not None and rt.end_token.next0_.isCharOf("/\\")): 
                        rt.end_token = rt.end_token.next0_
                    kit.embedToken(rt)
                    t = (rt)
                    continue
                if (i == 1): 
                    sch = tok.termin.canonic_text
                    ut = None
                    if (sch == "ISBN"): 
                        ut = UriItemToken.attachISBN(tt.next0_)
                        if ((ut is None and t.previous is not None and t.previous.isChar('(')) and t.next0_ is not None and t.next0_.isChar(')')): 
                            tt0 = t.previous.previous
                            while tt0 is not None: 
                                if (tt0.whitespaces_after_count > 2): 
                                    break
                                if (tt0.is_whitespace_before): 
                                    ut = UriItemToken.attachISBN(tt0)
                                    if (ut is not None and ut.end_token.next0_ != t.previous): 
                                        ut = (None)
                                    break
                                tt0 = tt0.previous
                    elif ((sch == "RFC" or sch == "ISO" or sch == "ОКФС") or sch == "ОКОПФ"): 
                        ut = UriItemToken.attachISOContent(tt.next0_, ":")
                    elif (sch == "ГОСТ"): 
                        ut = UriItemToken.attachISOContent(tt.next0_, "-.")
                    elif (sch == "ТУ"): 
                        if (tok.chars.is_all_upper): 
                            ut = UriItemToken.attachISOContent(tt.next0_, "-.")
                            if (ut is not None and (ut.length_char < 10)): 
                                ut = (None)
                    else: 
                        ut = UriItemToken.attachBBK(tt.next0_)
                    if (ut is None): 
                        continue
                    ur = Utils.asObjectOrNull(ad.registerReferent(UriReferent._new2572(ut.value, sch)), UriReferent)
                    if (ut.begin_char < t.begin_char): 
                        rt = ReferentToken(ur, ut.begin_token, t)
                        if (t.next0_ is not None and t.next0_.isChar(')')): 
                            rt.end_token = t.next0_
                    else: 
                        rt = ReferentToken(ur, t, ut.end_token)
                    if (t.previous is not None and t.previous.isValue("КОД", None)): 
                        rt.begin_token = t.previous
                    if (ur.scheme.startswith("ОК")): 
                        UriAnalyzer.__checkDetail(rt)
                    kit.embedToken(rt)
                    t = (rt)
                    if (ur.scheme.startswith("ОК")): 
                        while t.next0_ is not None:
                            if (t.next0_.is_comma_and and (isinstance(t.next0_.next0_, NumberToken))): 
                                pass
                            else: 
                                break
                            ut = UriItemToken.attachBBK(t.next0_.next0_)
                            if (ut is None): 
                                break
                            ur = (Utils.asObjectOrNull(ad.registerReferent(UriReferent._new2572(ut.value, sch)), UriReferent))
                            rt = ReferentToken(ur, t.next0_.next0_, ut.end_token)
                            UriAnalyzer.__checkDetail(rt)
                            kit.embedToken(rt)
                            t = (rt)
                    continue
                if (i == 3): 
                    t0 = tt.next0_
                    while t0 is not None:
                        if (t0.isCharOf(":|") or t0.is_table_control_char or t0.is_hiphen): 
                            t0 = t0.next0_
                        else: 
                            break
                    if (t0 is None): 
                        continue
                    ut = UriItemToken.attachSkype(t0)
                    if (ut is None): 
                        continue
                    ur = Utils.asObjectOrNull(ad.registerReferent(UriReferent._new2572(ut.value.lower(), ("skype" if tok.termin.canonic_text == "SKYPE" else tok.termin.canonic_text))), UriReferent)
                    rt = ReferentToken(ur, t, ut.end_token)
                    kit.embedToken(rt)
                    t = (rt)
                    continue
                if (i == 4): 
                    t0 = tt.next0_
                    if (t0 is not None and ((t0.isChar(':') or t0.is_hiphen))): 
                        t0 = t0.next0_
                    if (t0 is None): 
                        continue
                    ut = UriItemToken.attachIcqContent(t0)
                    if (ut is None): 
                        continue
                    ur = Utils.asObjectOrNull(ad.registerReferent(UriReferent._new2572(ut.value, "ICQ")), UriReferent)
                    rt = ReferentToken(ur, t, t0)
                    kit.embedToken(rt)
                    t = (rt)
                    continue
                if (i == 5 or i == 6): 
                    t0 = tt.next0_
                    has_tab_cel = False
                    is_iban = False
                    first_pass3162 = True
                    while True:
                        if first_pass3162: first_pass3162 = False
                        else: t0 = t0.next0_
                        if (not (t0 is not None)): break
                        if ((((t0.isValue("БАНК", None) or t0.morph.class0_.is_preposition or t0.is_hiphen) or t0.isCharOf(".:") or t0.isValue("РУБЛЬ", None)) or t0.isValue("РУБ", None) or t0.isValue("ДОЛЛАР", None)) or t0.isValue("№", None) or t0.isValue("N", None)): 
                            pass
                        elif (t0.is_table_control_char): 
                            has_tab_cel = True
                        elif (t0.isCharOf("\\/") and t0.next0_ is not None and t0.next0_.isValue("IBAN", None)): 
                            is_iban = True
                            t0 = t0.next0_
                        elif (t0.isValue("IBAN", None)): 
                            is_iban = True
                        elif (isinstance(t0, TextToken)): 
                            npt = NounPhraseHelper.tryParse(t0, NounPhraseParseAttr.NO, 0)
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
                    val = t0.getSourceText()
                    if (str.isdigit(val[0]) and ((((i == 6 or tok.termin.canonic_text == "ИНН" or tok.termin.canonic_text == "БИК") or tok.termin.canonic_text == "ОГРН" or tok.termin.canonic_text == "СНИЛС") or tok.termin.canonic_text == "ОКПО"))): 
                        if (t0.chars.is_letter): 
                            continue
                        if (Utils.isNullOrEmpty(val) or not str.isdigit(val[0])): 
                            continue
                        if (t0.length_char < 9): 
                            tmp = io.StringIO()
                            print(val, end="", file=tmp)
                            ttt = t0.next0_
                            first_pass3163 = True
                            while True:
                                if first_pass3163: first_pass3163 = False
                                else: ttt = ttt.next0_
                                if (not (ttt is not None)): break
                                if (ttt.whitespaces_before_count > 1): 
                                    break
                                if (isinstance(ttt, NumberToken)): 
                                    print(ttt.getSourceText(), end="", file=tmp)
                                    t0 = ttt
                                    continue
                                if (ttt.is_hiphen or ttt.isChar('.')): 
                                    if (ttt.next0_ is None or not ((isinstance(ttt.next0_, NumberToken)))): 
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
                    elif (not ((isinstance(t0, NumberToken)))): 
                        if ((isinstance(t0, TextToken)) and is_iban): 
                            tmp1 = io.StringIO()
                            t1 = None
                            ttt = t0
                            first_pass3164 = True
                            while True:
                                if first_pass3164: first_pass3164 = False
                                else: ttt = ttt.next0_
                                if (not (ttt is not None)): break
                                if (ttt.is_newline_before and ttt != t0): 
                                    break
                                if (ttt.is_hiphen): 
                                    continue
                                if (not ((isinstance(ttt, NumberToken)))): 
                                    if (not ((isinstance(ttt, TextToken))) or not ttt.chars.is_latin_letter): 
                                        break
                                print(ttt.getSourceText(), end="", file=tmp1)
                                t1 = ttt
                                if (tmp1.tell() >= 34): 
                                    break
                            if (tmp1.tell() < 10): 
                                continue
                            ur1 = UriReferent._new2572(Utils.toStringStringIO(tmp1), tok.termin.canonic_text)
                            ur1.addSlot(UriReferent.ATTR_DETAIL, "IBAN", False, 0)
                            rt1 = ReferentToken(ad.registerReferent(ur1), t, t1)
                            kit.embedToken(rt1)
                            t = (rt1)
                            continue
                        if (not t0.isCharOf("/\\") or t0.next0_ is None): 
                            continue
                        tok2 = UriAnalyzer.__m_schemes.tryParse(t0.next0_, TerminParseAttr.NO)
                        if (tok2 is None or not ((isinstance(tok2.termin.tag, int))) or (tok2.termin.tag) != i): 
                            continue
                        t0 = tok2.end_token.next0_
                        while t0 is not None:
                            if (t0.isCharOf(":N№")): 
                                t0 = t0.next0_
                            elif (t0.is_table_control_char): 
                                t0 = t0.next0_
                                t00 = t0
                                has_tab_cel = True
                            else: 
                                break
                        if (not ((isinstance(t0, NumberToken)))): 
                            continue
                        tmp = io.StringIO()
                        while t0 is not None: 
                            if (not ((isinstance(t0, NumberToken)))): 
                                break
                            print(t0.getSourceText(), end="", file=tmp)
                            t0 = t0.next0_
                        if (t0 is None or not t0.isCharOf("/\\,") or not ((isinstance(t0.next0_, NumberToken)))): 
                            continue
                        val = Utils.toStringStringIO(tmp)
                        Utils.setLengthStringIO(tmp, 0)
                        ur2begin = t0.next0_
                        t0 = t0.next0_
                        while t0 is not None: 
                            if (not ((isinstance(t0, NumberToken)))): 
                                break
                            if (t0.whitespaces_before_count > 4 and tmp.tell() > 0): 
                                break
                            print(t0.getSourceText(), end="", file=tmp)
                            ur2end = t0
                            t0 = t0.next0_
                        ur2 = (Utils.asObjectOrNull(ad.registerReferent(UriReferent._new2569(tok2.termin.canonic_text, Utils.toStringStringIO(tmp))), UriReferent))
                    if (len(val) < 5): 
                        continue
                    ur = Utils.asObjectOrNull(ad.registerReferent(UriReferent._new2572(val, tok.termin.canonic_text)), UriReferent)
                    rt = ReferentToken(ur, t, (t0 if ur2begin is None else ur2begin.previous))
                    if (has_tab_cel): 
                        rt.begin_token = t00
                    if (ur.scheme.startswith("ОК")): 
                        UriAnalyzer.__checkDetail(rt)
                    ttt = t.previous
                    first_pass3165 = True
                    while True:
                        if first_pass3165: first_pass3165 = False
                        else: ttt = ttt.previous
                        if (not (ttt is not None)): break
                        if (ttt.is_table_control_char): 
                            break
                        if (ttt.morph.class0_.is_preposition): 
                            continue
                        if (ttt.isValue("ОРГАНИЗАЦИЯ", None)): 
                            continue
                        if (ttt.isValue("НОМЕР", None) or ttt.isValue("КОД", None)): 
                            rt.begin_token = ttt
                            t = rt.begin_token
                        break
                    kit.embedToken(rt)
                    t = (rt)
                    if (ur2 is not None): 
                        rt2 = ReferentToken(ur2, ur2begin, ur2end)
                        kit.embedToken(rt2)
                        t = (rt2)
                    continue
                continue
            if (t.isChar('@')): 
                u1s = UriItemToken.attachMailUsers(t.previous)
                if (u1s is None): 
                    continue
                u2 = UriItemToken.attachDomainName(t.next0_, False, True)
                if (u2 is None): 
                    continue
                for ii in range(len(u1s) - 1, -1, -1):
                    ur = Utils.asObjectOrNull(ad.registerReferent(UriReferent._new2572("{0}@{1}".format(u1s[ii].value, u2.value).lower(), "mailto")), UriReferent)
                    b = u1s[ii].begin_token
                    t0 = b.previous
                    if (t0 is not None and t0.isChar(':')): 
                        t0 = t0.previous
                    if (t0 is not None and ii == 0): 
                        br = False
                        ttt = t0
                        first_pass3166 = True
                        while True:
                            if first_pass3166: first_pass3166 = False
                            else: ttt = ttt.previous
                            if (not (ttt is not None)): break
                            if (not ((isinstance(ttt, TextToken)))): 
                                break
                            if (ttt != t0 and ttt.whitespaces_after_count > 1): 
                                break
                            if (ttt.isChar(')')): 
                                br = True
                                continue
                            if (ttt.isChar('(')): 
                                if (not br): 
                                    break
                                br = False
                                continue
                            if (ttt.isValue("EMAIL", None) or ttt.isValue("MAILTO", None)): 
                                b = ttt
                                break
                            if (ttt.isValue("MAIL", None)): 
                                b = ttt
                                if ((ttt.previous is not None and ttt.previous.is_hiphen and ttt.previous.previous is not None) and ((ttt.previous.previous.isValue("E", None) or ttt.previous.previous.isValue("Е", None)))): 
                                    b = ttt.previous.previous
                                break
                            if (ttt.isValue("ПОЧТА", None) or ttt.isValue("АДРЕС", None)): 
                                b = t0
                                ttt = ttt.previous
                                if (ttt is not None and ttt.isChar('.')): 
                                    ttt = ttt.previous
                                if (ttt is not None and ((t0.isValue("ЭЛ", None) or ttt.isValue("ЭЛЕКТРОННЫЙ", None)))): 
                                    b = ttt
                                if (b.previous is not None and b.previous.isValue("АДРЕС", None)): 
                                    b = b.previous
                                break
                            if (ttt.morph.class0_.is_preposition): 
                                continue
                    rt = ReferentToken(ur, b, (u2.end_token if ii == (len(u1s) - 1) else u1s[ii].end_token))
                    kit.embedToken(rt)
                    t = (rt)
                continue
            if (not t.morph.language.is_cyrillic): 
                if (t.is_whitespace_before or ((t.previous is not None and t.previous.isCharOf(",(")))): 
                    u1 = UriItemToken.attachUrl(t)
                    if (u1 is not None): 
                        if (u1.is_whitespace_after or u1.end_token.next0_ is None or not u1.end_token.next0_.isChar('@')): 
                            ur = Utils.asObjectOrNull(ad.registerReferent(UriReferent._new2569("http", u1.value)), UriReferent)
                            rt = ReferentToken(ur, u1.begin_token, u1.end_token)
                            rt.begin_token = Utils.ifNotNull(UriAnalyzer.__siteBefore(u1.begin_token.previous), u1.begin_token)
                            kit.embedToken(rt)
                            t = (rt)
                            continue
            if ((isinstance(t, TextToken)) and not t.is_whitespace_after and t.length_char > 2): 
                if (UriAnalyzer.__siteBefore(t.previous) is not None): 
                    ut = UriItemToken.attachUriContent(t, True)
                    if (ut is None or ut.value.find('.') <= 0 or ut.value.find('@') > 0): 
                        continue
                    ur = Utils.asObjectOrNull(ad.registerReferent(UriReferent._new2569("http", ut.value)), UriReferent)
                    rt = ReferentToken(ur, t, ut.end_token)
                    rt.begin_token = UriAnalyzer.__siteBefore(t.previous)
                    if (rt.end_token.next0_ is not None and rt.end_token.next0_.isCharOf("/\\")): 
                        rt.end_token = rt.end_token.next0_
                    kit.embedToken(rt)
                    t = (rt)
                    continue
            if ((t.chars.is_latin_letter and not t.chars.is_all_lower and t.next0_ is not None) and not t.is_whitespace_after): 
                if (t.next0_.isChar('/')): 
                    rt = UriAnalyzer.__TryAttachLotus(Utils.asObjectOrNull(t, TextToken))
                    if (rt is not None): 
                        rt.referent = ad.registerReferent(rt.referent)
                        kit.embedToken(rt)
                        t = (rt)
                        continue
    
    @staticmethod
    def __checkDetail(rt : 'ReferentToken') -> None:
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.uri.UriReferent import UriReferent
        from pullenti.ner.core.MiscHelper import MiscHelper
        if (rt.end_token.whitespaces_after_count > 2 or rt.end_token.next0_ is None): 
            return
        if (rt.end_token.next0_.isChar('(')): 
            br = BracketHelper.tryParse(rt.end_token.next0_, BracketParseAttr.NO, 100)
            if (br is not None): 
                (Utils.asObjectOrNull(rt.referent, UriReferent)).detail = MiscHelper.getTextValue(br.begin_token.next0_, br.end_token.previous, GetTextAttr.NO)
                rt.end_token = br.end_token
    
    @staticmethod
    def __siteBefore(t : 'Token') -> 'Token':
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        if (t is not None and t.isChar(':')): 
            t = t.previous
        if (t is None): 
            return None
        if ((t.isValue("ВЕБСАЙТ", None) or t.isValue("WEBSITE", None) or t.isValue("WEB", None)) or t.isValue("WWW", None)): 
            return t
        t0 = None
        if (t.isValue("САЙТ", None) or t.isValue("SITE", None)): 
            t0 = t
            t = t.previous
        elif (t.isValue("АДРЕС", None)): 
            t0 = t.previous
            if (t0 is not None and t0.isChar('.')): 
                t0 = t0.previous
            if (t0 is not None): 
                if (t0.isValue("ЭЛ", None) or t0.isValue("ЭЛЕКТРОННЫЙ", None)): 
                    return t0
            return None
        else: 
            return None
        if (t is not None and t.is_hiphen): 
            t = t.previous
        if (t is None): 
            return t0
        if (t.isValue("WEB", None) or t.isValue("ВЕБ", None)): 
            t0 = t
        if (t0.previous is not None and t0.previous.morph.class0_.is_adjective and (t0.whitespaces_before_count < 3)): 
            npt = NounPhraseHelper.tryParse(t0.previous, NounPhraseParseAttr.NO, 0)
            if (npt is not None): 
                t0 = npt.begin_token
        return t0
    
    @staticmethod
    def __TryAttachLotus(t : 'TextToken') -> 'ReferentToken':
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.uri.UriReferent import UriReferent
        from pullenti.ner.ReferentToken import ReferentToken
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
            if (not ((isinstance(tt, TextToken)))): 
                return None
            if (tails is None): 
                tails = list()
            tails.append((Utils.asObjectOrNull(tt, TextToken)).term)
            t1 = tt
            if (tt.is_whitespace_after or tt.next0_ is None): 
                break
            tt = tt.next0_
            if (not tt.isChar('/')): 
                break
            tt = tt.next0_
        if (tails is None or (len(tails) < 3)): 
            return None
        heads = list()
        heads.append(t.term)
        t0 = t
        ok = True
        for k in range(2):
            if (not ((isinstance(t0.previous, TextToken)))): 
                break
            if (t0.whitespaces_before_count != 1): 
                if (not t0.is_newline_before or k > 0): 
                    break
            if (not t0.is_whitespace_before and t0.previous.isChar('/')): 
                break
            if (t0.previous.chars == t.chars): 
                t0 = t0.previous
                heads.insert(0, (Utils.asObjectOrNull(t0, TextToken)).term)
                ok = True
                continue
            if ((t0.previous.chars.is_latin_letter and t0.previous.chars.is_all_upper and t0.previous.length_char == 1) and k == 0): 
                t0 = t0.previous
                heads.insert(0, (Utils.asObjectOrNull(t0, TextToken)).term)
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
            print(MiscHelper.convertFirstCharUpperAndOtherLower(heads[i]), end="", file=tmp)
            i += 1
        for tail in tails: 
            print("/{0}".format(tail), end="", file=tmp, flush=True)
        if (((t1.next0_ is not None and t1.next0_.isChar('@') and t1.next0_.next0_ is not None) and t1.next0_.next0_.chars.is_latin_letter and not t1.next0_.is_whitespace_after) and not t1.is_whitespace_after): 
            t1 = t1.next0_.next0_
        uri_ = UriReferent._new2569("lotus", Utils.toStringStringIO(tmp))
        return ReferentToken(uri_, t0, t1)
    
    __m_schemes = None
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.core.Termin import Termin
        from pullenti.ner.core.TerminCollection import TerminCollection
        from pullenti.morph.MorphLang import MorphLang
        from pullenti.ner.uri.internal.UriItemToken import UriItemToken
        from pullenti.ner.ProcessorService import ProcessorService
        if (UriAnalyzer.__m_schemes is not None): 
            return
        Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = True
        try: 
            UriAnalyzer.__m_schemes = TerminCollection()
            obj = EpNerBankInternalResourceHelper.getString("UriSchemes.csv")
            if (obj is None): 
                raise Utils.newException("Can't file resource file {0} in Organization analyzer".format("UriSchemes.csv"), None)
            for line0 in Utils.splitString(obj, '\n', False): 
                line = line0.strip()
                if (Utils.isNullOrEmpty(line)): 
                    continue
                UriAnalyzer.__m_schemes.add(Termin._new705(line, MorphLang.UNKNOWN, True, 0))
            for s in ["ISBN", "УДК", "ББК", "ТНВЭД", "ОКВЭД"]: 
                UriAnalyzer.__m_schemes.add(Termin._new705(s, MorphLang.UNKNOWN, True, 1))
            UriAnalyzer.__m_schemes.add(Termin._new2585("Общероссийский классификатор форм собственности", "ОКФС", 1, "ОКФС"))
            UriAnalyzer.__m_schemes.add(Termin._new2585("Общероссийский классификатор организационно правовых форм", "ОКОПФ", 1, "ОКОПФ"))
            UriAnalyzer.__m_schemes.add(Termin._new705("WWW", MorphLang.UNKNOWN, True, 2))
            UriAnalyzer.__m_schemes.add(Termin._new705("HTTP", MorphLang.UNKNOWN, True, 10))
            UriAnalyzer.__m_schemes.add(Termin._new705("HTTPS", MorphLang.UNKNOWN, True, 10))
            UriAnalyzer.__m_schemes.add(Termin._new705("SHTTP", MorphLang.UNKNOWN, True, 10))
            UriAnalyzer.__m_schemes.add(Termin._new705("FTP", MorphLang.UNKNOWN, True, 10))
            t = Termin._new705("SKYPE", MorphLang.UNKNOWN, True, 3)
            t.addVariant("СКАЙП", True)
            t.addVariant("SKYPEID", True)
            t.addVariant("SKYPE ID", True)
            UriAnalyzer.__m_schemes.add(t)
            t = Termin._new705("SWIFT", MorphLang.UNKNOWN, True, 3)
            t.addVariant("СВИФТ", True)
            UriAnalyzer.__m_schemes.add(t)
            UriAnalyzer.__m_schemes.add(Termin._new705("ICQ", MorphLang.UNKNOWN, True, 4))
            t = Termin._new2595("основной государственный регистрационный номер", "ОГРН", 5, "ОГРН", True)
            t.addVariant("ОГРН ИП", True)
            UriAnalyzer.__m_schemes.add(t)
            UriAnalyzer.__m_schemes.add(Termin._new2595("Индивидуальный идентификационный номер", "ИИН", 5, "ИИН", True))
            UriAnalyzer.__m_schemes.add(Termin._new2595("Индивидуальный номер налогоплательщика", "ИНН", 5, "ИНН", True))
            UriAnalyzer.__m_schemes.add(Termin._new2595("Код причины постановки на учет", "КПП", 5, "КПП", True))
            UriAnalyzer.__m_schemes.add(Termin._new2595("Банковский идентификационный код", "БИК", 5, "БИК", True))
            UriAnalyzer.__m_schemes.add(Termin._new2595("основной государственный регистрационный номер индивидуального предпринимателя", "ОГРНИП", 5, "ОГРНИП", True))
            t = Termin._new2595("Страховой номер индивидуального лицевого счёта", "СНИЛС", 5, "СНИЛС", True)
            t.addVariant("Свидетельство пенсионного страхования", False)
            t.addVariant("Страховое свидетельство обязательного пенсионного страхования", False)
            t.addVariant("Страховое свидетельство", False)
            UriAnalyzer.__m_schemes.add(t)
            UriAnalyzer.__m_schemes.add(Termin._new2595("Общероссийский классификатор предприятий и организаций", "ОКПО", 5, "ОКПО", True))
            UriAnalyzer.__m_schemes.add(Termin._new2595("Общероссийский классификатор объектов административно-территориального деления", "ОКАТО", 5, "ОКАТО", True))
            UriAnalyzer.__m_schemes.add(Termin._new2595("Общероссийский классификатор территорий муниципальных образований", "ОКТМО", 5, "ОКТМО", True))
            UriAnalyzer.__m_schemes.add(Termin._new2595("Общероссийский классификатор органов государственной власти и управления", "ОКОГУ", 5, "ОКОГУ", True))
            UriAnalyzer.__m_schemes.add(Termin._new2595("Общероссийский классификатор Отрасли народного хозяйства", "ОКОНХ", 5, "ОКОНХ", True))
            t = Termin._new2607("РАСЧЕТНЫЙ СЧЕТ", MorphLang.UNKNOWN, True, "Р/С", 6, 20)
            t.addAbridge("Р.С.")
            t.addAbridge("Р.СЧ.")
            t.addAbridge("P.C.")
            t.addAbridge("РАСЧ.СЧЕТ")
            t.addAbridge("РАС.СЧЕТ")
            t.addAbridge("РАСЧ.СЧ.")
            t.addAbridge("РАС.СЧ.")
            t.addAbridge("Р.СЧЕТ")
            t.addVariant("СЧЕТ ПОЛУЧАТЕЛЯ", False)
            t.addVariant("СЧЕТ ОТПРАВИТЕЛЯ", False)
            t.addVariant("СЧЕТ", False)
            UriAnalyzer.__m_schemes.add(t)
            t = Termin._new2608("ЛИЦЕВОЙ СЧЕТ", "Л/С", 6, 20)
            t.addAbridge("Л.С.")
            t.addAbridge("Л.СЧ.")
            t.addAbridge("Л/С")
            t.addAbridge("ЛИЦ.СЧЕТ")
            t.addAbridge("ЛИЦ.СЧ.")
            t.addAbridge("Л.СЧЕТ")
            UriAnalyzer.__m_schemes.add(t)
            t = Termin._new2607("СПЕЦИАЛЬНЫЙ ЛИЦЕВОЙ СЧЕТ", MorphLang.UNKNOWN, True, "СПЕЦ/С", 6, 20)
            t.addAbridge("СПЕЦ.С.")
            t.addAbridge("СПЕЦ.СЧЕТ")
            t.addAbridge("СПЕЦ.СЧ.")
            t.addVariant("СПЕЦСЧЕТ", True)
            t.addVariant("СПЕЦИАЛЬНЫЙ СЧЕТ", True)
            UriAnalyzer.__m_schemes.add(t)
            t = Termin._new2607("КОРРЕСПОНДЕНТСКИЙ СЧЕТ", MorphLang.UNKNOWN, True, "К/С", 6, 20)
            t.addAbridge("КОРР.СЧЕТ")
            t.addAbridge("КОР.СЧЕТ")
            t.addAbridge("КОРР.СЧ.")
            t.addAbridge("КОР.СЧ.")
            t.addAbridge("К.СЧЕТ")
            t.addAbridge("КОР.С.")
            t.addAbridge("К.С.")
            t.addAbridge("K.C.")
            t.addAbridge("К-С")
            t.addAbridge("К/С")
            t.addAbridge("К.СЧ.")
            t.addAbridge("К/СЧ")
            UriAnalyzer.__m_schemes.add(t)
            t = Termin._new2611("КОД БЮДЖЕТНОЙ КЛАССИФИКАЦИИ", "КБК", "КБК", 6, 20, True)
            UriAnalyzer.__m_schemes.add(t)
            UriItemToken.initialize()
        except Exception as ex: 
            raise Utils.newException(ex.__str__(), ex)
        Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = False
        ProcessorService.registerAnalyzer(UriAnalyzer())