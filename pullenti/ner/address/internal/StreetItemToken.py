# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.address.internal.StreetItemType import StreetItemType
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.core.NumberExType import NumberExType
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
from pullenti.ner.address.AddressDetailType import AddressDetailType
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.address.internal.EpNerAddressInternalResourceHelper import EpNerAddressInternalResourceHelper


class StreetItemToken(MetaToken):
    """ Токен для поддержки выделения улиц """
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
        self.typ = StreetItemType.NOUN
        self.termin = None;
        self.alt_termin = None;
        self.exist_street = None;
        self.number = None;
        self.number_has_prefix = False
        self.is_number_km = False
        self.value = None;
        self.alt_value = None;
        self.alt_value2 = None;
        self.is_abridge = False
        self.is_in_dictionary = False
        self.is_in_brackets = False
        self.has_std_suffix = False
        self.noun_is_doubt_coef = 0
    
    @property
    def is_road(self) -> bool:
        if (self.termin is None): 
            return False
        if ((self.termin.canonic_text == "АВТОДОРОГА" or self.termin.canonic_text == "ШОССЕ" or self.termin.canonic_text == "АВТОШЛЯХ") or self.termin.canonic_text == "ШОСЕ"): 
            return True
        return False
    
    def __str__(self) -> str:
        res = io.StringIO()
        print("{0}".format(Utils.enumToString(self.typ)), end="", file=res, flush=True)
        if (self.value is not None): 
            print(" {0}".format(self.value), end="", file=res, flush=True)
            if (self.alt_value is not None): 
                print("/{0}".format(self.alt_value), end="", file=res, flush=True)
        if (self.exist_street is not None): 
            print(" {0}".format(str(self.exist_street)), end="", file=res, flush=True)
        if (self.termin is not None): 
            print(" {0}".format(str(self.termin)), end="", file=res, flush=True)
            if (self.alt_termin is not None): 
                print("/{0}".format(str(self.alt_termin)), end="", file=res, flush=True)
        elif (self.number is not None): 
            print(" {0}".format(str(self.number)), end="", file=res, flush=True)
        else: 
            print(" {0}".format(super().__str__()), end="", file=res, flush=True)
        if (self.is_abridge): 
            print(" (?)", end="", file=res)
        return Utils.toStringStringIO(res)
    
    def __isSurname(self) -> bool:
        from pullenti.ner.TextToken import TextToken
        if (self.typ != StreetItemType.NAME): 
            return False
        if (not ((isinstance(self.end_token, TextToken)))): 
            return False
        nam = (Utils.asObjectOrNull(self.end_token, TextToken)).term
        if (len(nam) > 4): 
            if (LanguageHelper.endsWithEx(nam, "А", "Я", "КО", "ЧУКА")): 
                if (not LanguageHelper.endsWithEx(nam, "АЯ", "ЯЯ", None, None)): 
                    return True
        return False
    
    @staticmethod
    def tryParse(t : 'Token', loc_streets : 'IntOntologyCollection', recurse : bool=False, prev : 'StreetItemToken'=None, ignore_onto : bool=False) -> 'StreetItemToken':
        if (t is None): 
            return None
        if (t.kit.is_recurce_overflow): 
            return None
        t.kit.recurse_level += 1
        res = StreetItemToken._tryParse(t, loc_streets, recurse, prev, ignore_onto)
        t.kit.recurse_level -= 1
        return res
    
    @staticmethod
    def _tryParse(t : 'Token', loc_streets : 'IntOntologyCollection', recurse : bool, prev : 'StreetItemToken', ignore_onto : bool) -> 'StreetItemToken':
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.address.internal.AddressItemToken import AddressItemToken
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.TextToken import TextToken
        from pullenti.morph.MorphClass import MorphClass
        from pullenti.ner.address.AddressReferent import AddressReferent
        from pullenti.ner.address.StreetReferent import StreetReferent
        from pullenti.morph.MorphBaseInfo import MorphBaseInfo
        from pullenti.morph.MorphWordForm import MorphWordForm
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.geo.GeoReferent import GeoReferent
        from pullenti.morph.Morphology import Morphology
        from pullenti.morph.MorphCase import MorphCase
        if (t is None): 
            return None
        tn = None
        if (t.isValue("ИМЕНИ", None) or t.isValue("ІМЕНІ", None)): 
            tn = t
        elif (t.isValue("ИМ", None) or t.isValue("ІМ", None)): 
            tn = t
            if (tn.next0_ is not None and tn.next0_.isChar('.')): 
                tn = tn.next0_
        if (tn is not None): 
            if (tn.next0_ is None or tn.whitespaces_after_count > 2): 
                return None
            t = tn.next0_
        nt = NumberHelper.tryParseAge(t)
        if (nt is not None): 
            return StreetItemToken._new218(nt.begin_token, nt.end_token, StreetItemType.AGE, nt)
        nt = Utils.asObjectOrNull(t, NumberToken)
        if ((nt) is not None): 
            if ((Utils.asObjectOrNull(nt, NumberToken)).value == (0)): 
                return None
            res = StreetItemToken._new219(nt, nt, StreetItemType.NUMBER, nt, nt.morph)
            if ((t.next0_ is not None and t.next0_.is_hiphen and t.next0_.next0_ is not None) and t.next0_.next0_.isValue("Я", None)): 
                res.end_token = t.next0_.next0_
            nex = NumberHelper.tryParseNumberWithPostfix(t)
            if (nex is not None): 
                if (nex.ex_typ == NumberExType.KILOMETER): 
                    res.is_number_km = True
                    res.end_token = nex.end_token
                else: 
                    return None
            aaa = AddressItemToken.tryParse(t, None, False, True, None)
            if (aaa is not None and aaa.typ == AddressItemToken.ItemType.NUMBER and aaa.end_char > t.end_char): 
                if (prev is not None and prev.typ == StreetItemType.NOUN and prev.termin.canonic_text == "КВАРТАЛ"): 
                    res.end_token = aaa.end_token
                    res.value = aaa.value
                    res.number = (None)
                else: 
                    return None
            if (nt.typ == NumberSpellingType.WORDS and nt.morph.class0_.is_adjective): 
                npt2 = NounPhraseHelper.tryParse(t, NounPhraseParseAttr.NO, 0)
                if (npt2 is not None and npt2.end_char > t.end_char and npt2.morph.number != MorphNumber.SINGULAR): 
                    if (t.next0_ is not None and not t.next0_.chars.is_all_lower): 
                        pass
                    else: 
                        return None
            return res
        ntt = MiscHelper.checkNumberPrefix(t)
        if (ntt is not None and (isinstance(ntt, NumberToken)) and prev is not None): 
            return StreetItemToken._new220(t, ntt, StreetItemType.NUMBER, Utils.asObjectOrNull(ntt, NumberToken), True)
        tt = Utils.asObjectOrNull(t, TextToken)
        if (tt is not None and tt.morph.class0_.is_adjective): 
            if (tt.chars.is_capital_upper or ((prev is not None and prev.typ == StreetItemType.NUMBER and tt.isValue("ТРАНСПОРТНЫЙ", None)))): 
                npt = NounPhraseHelper.tryParse(tt, NounPhraseParseAttr.NO, 0)
                if (npt is not None and "-" in MiscHelper.getTextValueOfMetaToken(npt.noun, GetTextAttr.NO)): 
                    npt = (None)
                tte = tt.next0_
                if (npt is not None and len(npt.adjectives) == 1): 
                    tte = npt.end_token
                if (tte is not None): 
                    if ((((((((((tte.isValue("ВАЛ", None) or tte.isValue("ТРАКТ", None) or tte.isValue("ПОЛЕ", None)) or tte.isValue("МАГИСТРАЛЬ", None) or tte.isValue("СПУСК", None)) or tte.isValue("ВЗВОЗ", None) or tte.isValue("РЯД", None)) or tte.isValue("СЛОБОДА", None) or tte.isValue("РОЩА", None)) or tte.isValue("ПРУД", None) or tte.isValue("СЪЕЗД", None)) or tte.isValue("КОЛЬЦО", None) or tte.isValue("МАГІСТРАЛЬ", None)) or tte.isValue("УЗВІЗ", None) or tte.isValue("ЛІНІЯ", None)) or tte.isValue("УЗВІЗ", None) or tte.isValue("ГАЙ", None)) or tte.isValue("СТАВОК", None) or tte.isValue("ЗЇЗД", None)) or tte.isValue("КІЛЬЦЕ", None)): 
                        sit = StreetItemToken._new221(tt, tte, True)
                        sit.typ = StreetItemType.NAME
                        if (npt is None or len(npt.adjectives) == 0): 
                            sit.value = MiscHelper.getTextValue(tt, tte, GetTextAttr.NO)
                        else: 
                            sit.value = npt.getNormalCaseText(MorphClass(), False, MorphGender.UNDEFINED, False)
                        tok2 = StreetItemToken.__m_ontology.tryParse(tt, TerminParseAttr.NO)
                        if (tok2 is not None and tok2.termin is not None and tok2.end_token == tte): 
                            sit.termin = tok2.termin
                        return sit
                if (npt is not None and npt.begin_token != npt.end_token and len(npt.adjectives) <= 1): 
                    tt1 = npt.end_token.next0_
                    if (tt1 is not None and tt1.is_comma): 
                        tt1 = tt1.next0_
                    ok = False
                    sti1 = (None if recurse else StreetItemToken.tryParse(tt1, loc_streets, True, None, False))
                    if (sti1 is not None and sti1.typ == StreetItemType.NOUN): 
                        ok = True
                    else: 
                        ait = AddressItemToken.tryParse(tt1, loc_streets, False, True, None)
                        if (ait is not None): 
                            if (ait.typ == AddressItemToken.ItemType.HOUSE): 
                                ok = True
                            elif (ait.typ == AddressItemToken.ItemType.NUMBER): 
                                ait2 = AddressItemToken.tryParse(npt.end_token, loc_streets, False, True, None)
                                if (ait2 is None): 
                                    ok = True
                    if (ok): 
                        sti1 = StreetItemToken.tryParse(npt.end_token, loc_streets, False, None, False)
                        if (sti1 is not None and sti1.typ == StreetItemType.NOUN): 
                            ok = False
                    if (ok): 
                        sit = StreetItemToken(tt, npt.end_token)
                        sit.typ = StreetItemType.NAME
                        sit.value = MiscHelper.getTextValue(tt, npt.end_token, GetTextAttr.NO)
                        sit.alt_value = npt.getNormalCaseText(MorphClass(), False, MorphGender.UNDEFINED, False)
                        return sit
        if ((tt is not None and (isinstance(tt.next0_, TextToken)) and tt.next0_.chars.is_capital_upper) and not recurse): 
            if ((tt.isValue("ВАЛ", None) or tt.isValue("ТРАКТ", None) or tt.isValue("ПОЛЕ", None)) or tt.isValue("КОЛЬЦО", None) or tt.isValue("КІЛЬЦЕ", None)): 
                sit = StreetItemToken.tryParse(tt.next0_, loc_streets, True, None, False)
                if (sit is not None and sit.typ == StreetItemType.NAME): 
                    if (sit.value is not None): 
                        sit.value = "{0} {1}".format(sit.value, tt.getNormalCaseText(MorphClass(), False, MorphGender.UNDEFINED, False))
                    else: 
                        sit.value = "{0} {1}".format(sit.getSourceText().upper(), tt.getNormalCaseText(MorphClass(), False, MorphGender.UNDEFINED, False))
                    if (sit.alt_value is not None): 
                        sit.alt_value = "{0} {1}".format(sit.alt_value, tt.getNormalCaseText(MorphClass(), False, MorphGender.UNDEFINED, False))
                    sit.begin_token = tt
                    return sit
        if (((tt is not None and tt.length_char == 1 and tt.chars.is_all_lower) and tt.next0_ is not None and tt.next0_.isChar('.')) and tt.kit.base_language.is_ru): 
            if (tt.isValue("М", None) or tt.isValue("M", None)): 
                if (prev is not None and prev.typ == StreetItemType.NOUN): 
                    pass
                else: 
                    return StreetItemToken._new222(tt, tt.next0_, StreetItemToken.__m_metro, StreetItemType.NOUN, True)
        ot = None
        if (loc_streets is not None): 
            ots = loc_streets.tryAttach(t, None, False)
            if (ots is not None): 
                ot = ots[0]
        if (t.kit.ontology is not None and ot is None): 
            ots = t.kit.ontology.attachToken(AddressReferent.OBJ_TYPENAME, t)
            if (ots is not None): 
                ot = ots[0]
        if (ot is not None and ot.begin_token == ot.end_token and ot.morph.class0_.is_adjective): 
            tok0 = StreetItemToken.__m_ontology.tryParse(t, TerminParseAttr.NO)
            if (tok0 is not None): 
                if ((Utils.valToEnum(tok0.termin.tag, StreetItemType)) == StreetItemType.STDADJECTIVE): 
                    ot = (None)
        if (ot is not None): 
            res0 = StreetItemToken._new223(ot.begin_token, ot.end_token, StreetItemType.NAME, Utils.asObjectOrNull(ot.item.referent, StreetReferent), ot.morph, True)
            return res0
        tok = StreetItemToken.__m_ontology.tryParse(t, TerminParseAttr.NO)
        if (tok is not None and tok.termin.canonic_text == "НАБЕРЕЖНАЯ" and not tok.chars.is_all_lower): 
            nex = StreetItemToken.tryParse(tok.end_token.next0_, None, False, None, False)
            if (nex is not None and ((nex.typ == StreetItemType.NOUN or nex.typ == StreetItemType.STDADJECTIVE))): 
                tok = (None)
            elif ((((t.morph.gender) & (MorphGender.FEMINIE))) == (MorphGender.UNDEFINED) and t.length_char > 7): 
                tok = (None)
        if (((tok is not None and t.length_char == 1 and t.isValue("Б", None)) and prev is not None and prev.number is not None) and prev.number.value == (26)): 
            tok = (None)
        if (tok is not None and not ignore_onto): 
            if ((Utils.valToEnum(tok.termin.tag, StreetItemType)) == StreetItemType.NUMBER): 
                if (isinstance(tok.end_token.next0_, NumberToken)): 
                    return StreetItemToken._new224(t, tok.end_token.next0_, StreetItemType.NUMBER, Utils.asObjectOrNull(tok.end_token.next0_, NumberToken), True, tok.morph)
                return None
            if (tt is None): 
                return None
            abr = True
            swichVal = Utils.valToEnum(tok.termin.tag, StreetItemType)
            if (swichVal == StreetItemType.STDADJECTIVE): 
                while True:
                    if (tt.chars.is_all_lower and prev is None): 
                        return None
                    elif (tt.isValue(tok.termin.canonic_text, None)): 
                        abr = False
                    elif (tt.length_char == 1): 
                        if (not tt.is_whitespace_before and not tt.previous.isCharOf(":,.")): 
                            break
                        if (not tok.end_token.isChar('.')): 
                            if (not tt.chars.is_all_upper): 
                                break
                            oo2 = False
                            if (tok.end_token.is_newline_after and prev is not None): 
                                oo2 = True
                            else: 
                                next0__ = StreetItemToken.tryParse(tok.end_token.next0_, None, False, None, False)
                                if (next0__ is not None and ((next0__.typ == StreetItemType.NAME or next0__.typ == StreetItemType.NOUN))): 
                                    oo2 = True
                                elif (AddressItemToken.checkHouseAfter(tok.end_token.next0_, False, True) and prev is not None): 
                                    oo2 = True
                            if (oo2): 
                                return StreetItemToken._new225(tok.begin_token, tok.end_token, StreetItemType.STDADJECTIVE, tok.termin, abr, tok.morph)
                            break
                        tt2 = tok.end_token.next0_
                        if (tt2 is not None and tt2.is_hiphen): 
                            tt2 = tt2.next0_
                        if (isinstance(tt2, TextToken)): 
                            if (tt2.length_char == 1 and tt2.chars.is_all_upper): 
                                break
                            if (tt2.chars.is_capital_upper): 
                                is_sur = False
                                txt = (Utils.asObjectOrNull(tt2, TextToken)).term
                                if (txt.endswith("ОГО")): 
                                    is_sur = True
                                else: 
                                    for wf in tt2.morph.items: 
                                        if (wf.class0_.is_proper_surname and (Utils.asObjectOrNull(wf, MorphWordForm)).is_in_dictionary): 
                                            if (wf.case_.is_genitive): 
                                                is_sur = True
                                                break
                                if (is_sur): 
                                    break
                    return StreetItemToken._new225(tok.begin_token, tok.end_token, StreetItemType.STDADJECTIVE, tok.termin, abr, tok.morph)
            elif (swichVal == StreetItemType.NOUN): 
                while True:
                    if (tt.isValue(tok.termin.canonic_text, None) or tok.end_token.isValue(tok.termin.canonic_text, None) or tt.isValue("УЛ", None)): 
                        abr = False
                    elif (tok.begin_token != tok.end_token and ((tok.begin_token.next0_.is_hiphen or tok.begin_token.next0_.isCharOf("/\\")))): 
                        pass
                    elif (not tt.chars.is_all_lower and tt.length_char == 1): 
                        break
                    elif (tt.length_char == 1): 
                        if (not tt.is_whitespace_before): 
                            if (tt.previous is not None and tt.previous.isCharOf(",")): 
                                pass
                            else: 
                                return None
                        if (tok.end_token.isChar('.')): 
                            pass
                        elif (tok.begin_token != tok.end_token and tok.begin_token.next0_ is not None and ((tok.begin_token.next0_.is_hiphen or tok.begin_token.next0_.isCharOf("/\\")))): 
                            pass
                        elif (tok.length_char > 5): 
                            pass
                        elif (tok.begin_token == tok.end_token and tt.isValue("Ш", None) and tt.chars.is_all_lower): 
                            if (prev is not None and ((prev.typ == StreetItemType.NAME or prev.typ == StreetItemType.STDNAME or prev.typ == StreetItemType.STDPARTOFNAME))): 
                                pass
                            else: 
                                sii = StreetItemToken.tryParse(tt.next0_, None, False, None, False)
                                if (sii is not None and (((sii.typ == StreetItemType.NAME or sii.typ == StreetItemType.STDNAME or sii.typ == StreetItemType.STDPARTOFNAME) or sii.typ == StreetItemType.AGE))): 
                                    pass
                                else: 
                                    return None
                        else: 
                            return None
                    elif (((tt.term == "КВ" or tt.term == "КВАРТ")) and not tok.end_token.isValue("Л", None)): 
                        pass
                    if (not t.chars.is_all_lower and t.morph.class0_.is_proper_surname and t.chars.is_cyrillic_letter): 
                        if ((((t.morph.number) & (MorphNumber.PLURAL))) != (MorphNumber.UNDEFINED)): 
                            return None
                    if (tt.term == "ДОРОГОЙ"): 
                        return None
                    alt = None
                    if (tok.begin_token.isValue("ПР", None) and ((tok.begin_token == tok.end_token or tok.begin_token.next0_.isChar('.')))): 
                        alt = StreetItemToken.__m_prospect
                    return StreetItemToken._new227(tok.begin_token, tok.end_token, StreetItemType.NOUN, tok.termin, alt, abr, tok.morph, (tok.termin.tag2 if isinstance(tok.termin.tag2, int) else 0))
            elif (swichVal == StreetItemType.STDNAME): 
                is_post_off = tok.termin.canonic_text == "ПОЧТОВОЕ ОТДЕЛЕНИЕ"
                if (tok.begin_token.chars.is_all_lower and not is_post_off and tok.end_token.chars.is_all_lower): 
                    return None
                sits = StreetItemToken._new228(tok.begin_token, tok.end_token, StreetItemType.STDNAME, tok.morph, tok.termin.canonic_text)
                if (tok.begin_token != tok.end_token and not is_post_off): 
                    vv = MiscHelper.getTextValue(tok.begin_token, tok.end_token, GetTextAttr.NO)
                    if (vv != sits.value): 
                        if (len(vv) < len(sits.value)): 
                            sits.alt_value = vv
                        else: 
                            sits.alt_value = sits.value
                            sits.value = vv
                    if (((StreetItemToken.__m_std_ont_misc.tryParse(tok.begin_token, TerminParseAttr.NO) is not None or tok.begin_token.getMorphClassInDictionary().is_proper_name or (tok.begin_token.length_char < 4))) and ((tok.end_token.morph.class0_.is_proper_surname or not tok.end_token.getMorphClassInDictionary().is_proper_name))): 
                        sits.alt_value2 = MiscHelper.getTextValue(tok.end_token, tok.end_token, GetTextAttr.NO)
                    elif (((tok.end_token.getMorphClassInDictionary().is_proper_name or StreetItemToken.__m_std_ont_misc.tryParse(tok.end_token, TerminParseAttr.NO) is not None)) and ((tok.begin_token.morph.class0_.is_proper_surname or not tok.begin_token.getMorphClassInDictionary().is_proper_name))): 
                        sits.alt_value2 = MiscHelper.getTextValue(tok.begin_token, tok.begin_token, GetTextAttr.NO)
                return sits
            elif (swichVal == StreetItemType.STDPARTOFNAME): 
                if (prev is not None and prev.typ == StreetItemType.NAME): 
                    nam = Utils.ifNotNull(prev.value, MiscHelper.getTextValueOfMetaToken(prev, GetTextAttr.NO))
                    if (prev.alt_value is None): 
                        prev.alt_value = "{0} {1}".format(tok.termin.canonic_text, nam)
                    else: 
                        prev.alt_value = "{0} {1}".format(tok.termin.canonic_text, prev.alt_value)
                    prev.end_token = tok.end_token
                    prev.value = nam
                    return StreetItemToken.tryParse(tok.end_token.next0_, loc_streets, recurse, prev, False)
                sit = StreetItemToken.tryParse(tok.end_token.next0_, loc_streets, False, None, False)
                if (sit is None): 
                    if (tok.morph.number == MorphNumber.PLURAL): 
                        return StreetItemToken._new228(tok.begin_token, tok.end_token, StreetItemType.NAME, tok.morph, MiscHelper.getTextValueOfMetaToken(tok, GetTextAttr.NO))
                    return None
                if (sit.typ != StreetItemType.NAME and sit.typ != StreetItemType.NOUN): 
                    return None
                if (sit.typ == StreetItemType.NOUN): 
                    if (tok.morph.number == MorphNumber.PLURAL): 
                        return StreetItemToken._new228(tok.begin_token, tok.end_token, StreetItemType.NAME, tok.morph, MiscHelper.getTextValueOfMetaToken(tok, GetTextAttr.NO))
                    else: 
                        return StreetItemToken._new231(tok.begin_token, tok.end_token, StreetItemType.NAME, tok.morph, tok.termin)
                if (sit.value is not None): 
                    if (sit.alt_value is None): 
                        sit.alt_value = "{0} {1}".format(tok.termin.canonic_text, sit.value)
                    else: 
                        sit.value = "{0} {1}".format(tok.termin.canonic_text, sit.value)
                elif (sit.exist_street is None): 
                    sit.alt_value = (Utils.asObjectOrNull(sit.begin_token, TextToken)).term
                    sit.value = "{0} {1}".format(tok.termin.canonic_text, (Utils.asObjectOrNull(sit.begin_token, TextToken)).term)
                sit.begin_token = tok.begin_token
                return sit
            elif (swichVal == StreetItemType.NAME): 
                if (tok.begin_token.chars.is_all_lower): 
                    if (prev is not None and prev.typ == StreetItemType.STDADJECTIVE): 
                        pass
                    elif (prev is not None and prev.typ == StreetItemType.NOUN and AddressItemToken.checkHouseAfter(tok.end_token.next0_, True, False)): 
                        pass
                    elif (t.isValue("ПРОЕКТИРУЕМЫЙ", None) or t.isValue("МИРА", None)): 
                        pass
                    else: 
                        nex = StreetItemToken.tryParse(tok.end_token.next0_, None, True, None, False)
                        if (nex is not None and nex.typ == StreetItemType.NOUN): 
                            tt2 = nex.end_token.next0_
                            while tt2 is not None and tt2.isCharOf(",."):
                                tt2 = tt2.next0_
                            if (tt2 is None or tt2.whitespaces_before_count > 1): 
                                return None
                            if (AddressItemToken.checkHouseAfter(tt2, False, True)): 
                                pass
                            else: 
                                return None
                        else: 
                            return None
                sit0 = StreetItemToken.tryParse(tok.begin_token, None, False, prev, True)
                if (sit0 is not None and sit0.typ == StreetItemType.NAME and sit0.end_char > tok.end_char): 
                    sit0.is_in_dictionary = True
                    return sit0
                sit1 = StreetItemToken._new232(tok.begin_token, tok.end_token, StreetItemType.NAME, tok.morph, True)
                if ((not tok.is_whitespace_after and tok.end_token.next0_ is not None and tok.end_token.next0_.is_hiphen) and not tok.end_token.next0_.is_whitespace_after): 
                    sit2 = StreetItemToken.tryParse(tok.end_token.next0_.next0_, loc_streets, False, None, False)
                    if (sit2 is not None and ((sit2.typ == StreetItemType.NAME or sit2.typ == StreetItemType.STDPARTOFNAME or sit2.typ == StreetItemType.STDNAME))): 
                        sit1.end_token = sit2.end_token
                return sit1
            elif (swichVal == StreetItemType.FIX): 
                return StreetItemToken._new233(tok.begin_token, tok.end_token, StreetItemType.FIX, tok.morph, True, tok.termin)
        if (tt is not None): 
            if ((prev is not None and prev.typ == StreetItemType.NUMBER and prev.number is not None) and prev.number.value == (26)): 
                if (tt.isValue("БАКИНСКИЙ", None) or "БАКИНСК".startswith((Utils.asObjectOrNull(tt, TextToken)).term)): 
                    tt2 = tt
                    if (tt2.next0_ is not None and tt2.next0_.isChar('.')): 
                        tt2 = tt2.next0_
                    if (isinstance(tt2.next0_, TextToken)): 
                        tt2 = tt2.next0_
                        if (tt2.isValue("КОМИССАР", None) or tt2.isValue("КОММИССАР", None) or "КОМИС".startswith((Utils.asObjectOrNull(tt2, TextToken)).term)): 
                            if (tt2.next0_ is not None and tt2.next0_.isChar('.')): 
                                tt2 = tt2.next0_
                            sit = StreetItemToken._new234(tt, tt2, StreetItemType.STDNAME, True, "БАКИНСКИХ КОМИССАРОВ", tt2.morph)
                            return sit
            if ((tt.next0_ is not None and tt.next0_.isChar('.') and not tt.chars.is_all_lower) and (tt.next0_.whitespaces_after_count < 3) and (isinstance(tt.next0_.next0_, TextToken))): 
                tt1 = tt.next0_.next0_
                if (tt1 is not None and tt1.is_hiphen): 
                    tt1 = tt1.next0_
                if (tt.length_char == 1 and tt1.length_char == 1 and (isinstance(tt1.next0_, TextToken))): 
                    if (tt1.is_and and tt1.next0_.chars.is_all_upper and tt1.next0_.length_char == 1): 
                        tt1 = tt1.next0_
                    if ((tt1.chars.is_all_upper and tt1.next0_.isChar('.') and (tt1.next0_.whitespaces_after_count < 3)) and (isinstance(tt1.next0_.next0_, TextToken))): 
                        tt1 = tt1.next0_.next0_
                sit = StreetItemToken.tryParse(tt1, loc_streets, False, None, False)
                if (sit is not None and (isinstance(tt1, TextToken))): 
                    str0_ = (Utils.asObjectOrNull(tt1, TextToken)).term
                    ok = False
                    cla = tt.next0_.next0_.getMorphClassInDictionary()
                    if (sit.is_in_dictionary): 
                        ok = True
                    elif (sit.__isSurname() or cla.is_proper_surname): 
                        ok = True
                    elif (LanguageHelper.endsWith(str0_, "ОЙ") and ((cla.is_proper_surname or ((sit.typ == StreetItemType.NAME and sit.is_in_dictionary))))): 
                        ok = True
                    elif (LanguageHelper.endsWithEx(str0_, "ГО", "ИХ", None, None)): 
                        ok = True
                    elif (tt1.is_whitespace_before and not tt1.getMorphClassInDictionary().is_undefined): 
                        pass
                    elif (prev is not None and prev.typ == StreetItemType.NOUN and ((not prev.is_abridge or prev.length_char > 2))): 
                        ok = True
                    elif ((prev is not None and prev.typ == StreetItemType.NAME and sit.typ == StreetItemType.NOUN) and AddressItemToken.checkHouseAfter(sit.end_token.next0_, False, True)): 
                        ok = True
                    elif (sit.typ == StreetItemType.NAME and AddressItemToken.checkHouseAfter(sit.end_token.next0_, False, True)): 
                        if (MiscLocationHelper.checkGeoObjectBefore(tt)): 
                            ok = True
                    if (ok): 
                        sit.begin_token = tt
                        sit.value = str0_
                        sit.alt_value = MiscHelper.getTextValue(tt, sit.end_token, GetTextAttr.NO)
                        if (sit.alt_value is not None): 
                            sit.alt_value = sit.alt_value.replace("-", "")
                        return sit
            if (tt.chars.is_cyrillic_letter and tt.length_char > 1 and not tt.morph.class0_.is_preposition): 
                if (tt.isValue("ГЕРОЙ", None) or tt.isValue("ЗАЩИТНИК", "ЗАХИСНИК")): 
                    if ((isinstance(tt.next0_, ReferentToken)) and (isinstance(tt.next0_.getReferent(), GeoReferent))): 
                        re = StreetItemToken._new235(tt, tt.next0_, StreetItemType.STDPARTOFNAME, MiscHelper.getTextValue(tt, tt.next0_, GetTextAttr.NO))
                        sit = StreetItemToken.tryParse(tt.next0_.next0_, loc_streets, False, None, False)
                        if (sit is None or sit.typ != StreetItemType.NAME): 
                            ok2 = False
                            if (sit is not None and ((sit.typ == StreetItemType.STDADJECTIVE or sit.typ == StreetItemType.NOUN))): 
                                ok2 = True
                            elif (AddressItemToken.checkHouseAfter(tt.next0_.next0_, False, True)): 
                                ok2 = True
                            elif (tt.next0_.is_newline_after): 
                                ok2 = True
                            if (ok2): 
                                sit = StreetItemToken._new236(tt, tt.next0_, StreetItemType.NAME)
                                sit.value = MiscHelper.getTextValue(tt, tt.next0_, GetTextAttr.NO)
                                return sit
                            return re
                        if (sit.value is None): 
                            sit.value = MiscHelper.getTextValueOfMetaToken(sit, GetTextAttr.NO)
                        if (sit.alt_value is None): 
                            sit.alt_value = sit.value
                            sit.value = "{0} {1}".format(re.value, sit.value)
                        else: 
                            sit.value = "{0} {1}".format(re.value, sit.value)
                        sit.begin_token = tt
                        return sit
                ani = NumberHelper.tryParseAnniversary(t)
                if (ani is not None): 
                    return StreetItemToken._new237(t, ani.end_token, StreetItemType.AGE, ani, str(ani.value))
                ok1 = False
                if (not tt.chars.is_all_lower): 
                    ait = AddressItemToken.tryParse(tt, None, False, True, None)
                    if (ait is not None): 
                        pass
                    else: 
                        ok1 = True
                elif (prev is not None and prev.typ == StreetItemType.NOUN): 
                    tt1 = prev.begin_token.previous
                    if (tt1 is not None and tt1.is_comma): 
                        tt1 = tt1.previous
                    if (tt1 is not None and (isinstance(tt1.getReferent(), GeoReferent))): 
                        ok1 = True
                    elif (AddressItemToken.checkHouseAfter(tt.next0_, False, False)): 
                        if (not AddressItemToken.checkHouseAfter(tt, False, False)): 
                            ok1 = True
                elif (tt.whitespaces_after_count < 2): 
                    nex = StreetItemToken.tryParse(tt.next0_, None, True, None, False)
                    if (nex is not None and nex.typ == StreetItemType.NOUN): 
                        if (nex.termin.canonic_text == "ПЛОЩАДЬ"): 
                            if (tt.isValue("ОБЩИЙ", None)): 
                                return None
                        tt1 = tt.previous
                        if (tt1 is not None and tt1.is_comma): 
                            tt1 = tt1.previous
                        if (tt1 is not None and (isinstance(tt1.getReferent(), GeoReferent))): 
                            ok1 = True
                        elif (AddressItemToken.checkHouseAfter(nex.end_token.next0_, False, False)): 
                            ok1 = True
                if (ok1): 
                    dc = tt.getMorphClassInDictionary()
                    if (dc.is_adverb): 
                        if (not ((dc.is_proper))): 
                            return None
                    res = StreetItemToken._new238(tt, tt, StreetItemType.NAME, tt.morph)
                    if ((tt.next0_ is not None and ((tt.next0_.is_hiphen or tt.next0_.isCharOf("\\/"))) and (isinstance(tt.next0_.next0_, TextToken))) and not tt.is_whitespace_after and not tt.next0_.is_whitespace_after): 
                        ok2 = AddressItemToken.checkHouseAfter(tt.next0_.next0_.next0_, False, False) or tt.next0_.next0_.is_newline_after
                        if (not ok2): 
                            te2 = StreetItemToken.tryParse(tt.next0_.next0_.next0_, None, False, None, False)
                            if (te2 is not None and te2.typ == StreetItemType.NOUN): 
                                ok2 = True
                        if (ok2): 
                            res.end_token = tt.next0_.next0_
                            res.value = "{0} {1}".format(MiscHelper.getTextValue(res.begin_token, res.begin_token, GetTextAttr.NO), MiscHelper.getTextValue(res.end_token, res.end_token, GetTextAttr.NO))
                    elif ((tt.whitespaces_after_count < 2) and (isinstance(tt.next0_, TextToken)) and tt.next0_.chars.is_letter): 
                        if (not AddressItemToken.checkHouseAfter(tt.next0_, False, False) or tt.next0_.is_newline_after): 
                            tt1 = tt.next0_
                            is_pref = False
                            if ((isinstance(tt1, TextToken)) and tt1.chars.is_all_lower): 
                                if (tt1.isValue("ДЕ", None) or tt1.isValue("ЛА", None)): 
                                    tt1 = tt1.next0_
                                    is_pref = True
                            nn = StreetItemToken.tryParse(tt1, loc_streets, False, None, False)
                            if (nn is None or nn.typ == StreetItemType.NAME): 
                                npt = NounPhraseHelper.tryParse(tt, NounPhraseParseAttr.NO, 0)
                                if (npt is not None): 
                                    if (npt.begin_token == npt.end_token): 
                                        npt = (None)
                                if (npt is not None and ((npt.is_newline_after or AddressItemToken.checkHouseAfter(npt.end_token.next0_, False, False)))): 
                                    res.end_token = npt.end_token
                                    if (npt.morph.case_.is_genitive): 
                                        res.value = MiscHelper.getTextValueOfMetaToken(npt, GetTextAttr.NO)
                                        res.alt_value = npt.getNormalCaseText(MorphClass(), False, MorphGender.UNDEFINED, False)
                                    else: 
                                        res.value = npt.getNormalCaseText(MorphClass(), False, MorphGender.UNDEFINED, False)
                                        res.alt_value = MiscHelper.getTextValueOfMetaToken(npt, GetTextAttr.NO)
                                elif (AddressItemToken.checkHouseAfter(tt1.next0_, False, False) and tt1.chars.is_cyrillic_letter == tt.chars.is_cyrillic_letter and (t.whitespaces_after_count < 2)): 
                                    if (tt1.morph.class0_.is_verb and not tt1.isValue("ДАЛИ", None)): 
                                        pass
                                    elif (npt is None and not tt1.chars.is_all_lower and not is_pref): 
                                        pass
                                    else: 
                                        res.end_token = tt1
                                        res.value = "{0} {1}".format(MiscHelper.getTextValue(res.begin_token, res.begin_token, GetTextAttr.NO), MiscHelper.getTextValue(res.end_token, res.end_token, GetTextAttr.NO))
                            elif (nn.typ == StreetItemType.NOUN): 
                                npt = NounPhraseHelper.tryParse(tt, NounPhraseParseAttr.NO, 0)
                                if (npt is not None and npt.end_token == nn.end_token): 
                                    res.value = MiscHelper.getTextValue(res.begin_token, res.end_token, GetTextAttr.NO)
                                    var = Morphology.getWordform(res.value, MorphBaseInfo._new239(MorphCase.NOMINATIVE, MorphClass.ADJECTIVE, MorphNumber.SINGULAR, npt.morph.gender))
                                    if (var is not None and var != res.value): 
                                        res.alt_value = res.value
                                        res.value = var
                    return res
            if (((tt.isValue("РЕКА", None) or tt.isValue("РІЧКА", None))) and tt.next0_ is not None and tt.next0_.chars.is_capital_upper): 
                return StreetItemToken._new240(tt, tt.next0_, StreetItemType.NAME, tt.morph, tt.next0_.getSourceText().upper())
            if (tt.isValue("№", None) or tt.isValue("НОМЕР", None) or tt.isValue("НОМ", None)): 
                tt1 = tt.next0_
                if (tt1 is not None and tt1.isChar('.')): 
                    tt1 = tt1.next0_
                if (isinstance(tt1, NumberToken)): 
                    return StreetItemToken._new220(tt, tt1, StreetItemType.NUMBER, Utils.asObjectOrNull(tt1, NumberToken), True)
            if (tt.is_hiphen and (isinstance(tt.next0_, NumberToken))): 
                if (prev is not None and prev.typ == StreetItemType.NOUN): 
                    if (prev.termin.canonic_text == "МИКРОРАЙОН" or LanguageHelper.endsWith(prev.termin.canonic_text, "ГОРОДОК")): 
                        return StreetItemToken._new220(tt, tt.next0_, StreetItemType.NUMBER, Utils.asObjectOrNull(tt.next0_, NumberToken), True)
        r = (None if t is None else t.getReferent())
        if (isinstance(r, GeoReferent)): 
            geo = Utils.asObjectOrNull(r, GeoReferent)
            if (prev is not None and prev.typ == StreetItemType.NOUN): 
                if (AddressItemToken.checkHouseAfter(t.next0_, False, False)): 
                    return StreetItemToken._new235(t, t, StreetItemType.NAME, MiscHelper.getTextValue(t, t, GetTextAttr.NO))
        if (((isinstance(tt, TextToken)) and tt.chars.is_capital_upper and tt.chars.is_latin_letter) and (tt.whitespaces_after_count < 2)): 
            if (MiscHelper.isEngArticle(tt)): 
                return None
            tt2 = tt.next0_
            if (MiscHelper.isEngAdjSuffix(tt2)): 
                tt2 = tt2.next0_.next0_
            tok1 = StreetItemToken.__m_ontology.tryParse(tt2, TerminParseAttr.NO)
            if (tok1 is not None): 
                return StreetItemToken._new228(tt, tt2.previous, StreetItemType.NAME, tt.morph, (Utils.asObjectOrNull(tt, TextToken)).term)
        return None
    
    @staticmethod
    def _tryParseSpec(t : 'Token', prev : 'StreetItemToken') -> typing.List['StreetItemToken']:
        from pullenti.ner.date.DateReferent import DateReferent
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.geo.GeoReferent import GeoReferent
        from pullenti.ner.TextToken import TextToken
        if (t is None): 
            return None
        res = None
        if (isinstance(t.getReferent(), DateReferent)): 
            dr = Utils.asObjectOrNull(t.getReferent(), DateReferent)
            if (not ((isinstance((Utils.asObjectOrNull(t, ReferentToken)).begin_token, NumberToken)))): 
                return None
            if (dr.year == 0 and dr.day > 0 and dr.month > 0): 
                res = list()
                res.append(StreetItemToken._new218(t, t, StreetItemType.NUMBER, NumberToken(t, t, dr.day, NumberSpellingType.DIGIT)))
                tmp = dr.toString(False, t.morph.language, 0)
                i = tmp.find(' ')
                sit = StreetItemToken._new235(t, t, StreetItemType.STDNAME, tmp[i + 1:].upper())
                res.append(sit)
                sit.chars.is_capital_upper = True
                return res
            if (dr.year > 0 and dr.month == 0): 
                res = list()
                res.append(StreetItemToken._new218(t, t, StreetItemType.NUMBER, NumberToken(t, t, dr.year, NumberSpellingType.DIGIT)))
                sit = StreetItemToken._new235(t, t, StreetItemType.STDNAME, ("РОКУ" if t.morph.language.is_ua else "ГОДА"))
                res.append(sit)
                sit.chars.is_capital_upper = True
                return res
            return None
        if (prev is not None and prev.typ == StreetItemType.AGE): 
            res = list()
            if (isinstance(t.getReferent(), GeoReferent)): 
                sit = StreetItemToken._new249(t, t, StreetItemType.NAME, t.getSourceText().upper(), t.getReferent().toString(True, t.kit.base_language, 0).upper())
                res.append(sit)
            elif (t.isValue("ГОРОД", None) or t.isValue("МІСТО", None)): 
                sit = StreetItemToken._new235(t, t, StreetItemType.NAME, "ГОРОДА")
                res.append(sit)
            else: 
                return None
            return res
        if (prev is not None and prev.typ == StreetItemType.NOUN): 
            num = NumberHelper.tryParseRoman(t)
            if (num is not None): 
                res = list()
                sit = StreetItemToken._new218(num.begin_token, num.end_token, StreetItemType.NUMBER, num)
                res.append(sit)
                t = num.end_token.next0_
                if ((num.typ == NumberSpellingType.DIGIT and (isinstance(t, TextToken)) and not t.is_whitespace_before) and t.length_char == 1): 
                    sit.end_token = t
                    sit.value = "{0}{1}".format(num.value, (Utils.asObjectOrNull(t, TextToken)).term)
                    sit.number = (None)
                return res
        return None
    
    @staticmethod
    def tryParseList(t : 'Token', loc_streets : 'IntOntologyCollection', max_count : int=10) -> typing.List['StreetItemToken']:
        from pullenti.ner.address.internal.AddressItemToken import AddressItemToken
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.geo.GeoReferent import GeoReferent
        from pullenti.ner.geo.internal.CityItemToken import CityItemToken
        res = None
        sit = StreetItemToken.tryParse(t, loc_streets, False, None, False)
        if (sit is not None): 
            res = list()
            res.append(sit)
            t = sit.end_token.next0_
        else: 
            res = StreetItemToken._tryParseSpec(t, None)
            if (res is None): 
                return None
            sit = res[len(res) - 1]
            t = sit.end_token.next0_
            sit2 = StreetItemToken.tryParse(t, loc_streets, False, None, False)
            if (sit2 is not None and sit2.typ == StreetItemType.NOUN): 
                pass
            elif (AddressItemToken.checkHouseAfter(t, False, True)): 
                pass
            else: 
                return None
        first_pass2745 = True
        while True:
            if first_pass2745: first_pass2745 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (max_count > 0 and len(res) >= max_count): 
                break
            if (t.is_newline_before): 
                if (t.newlines_before_count > 1): 
                    break
                if (((t.whitespaces_after_count < 15) and sit is not None and sit.typ == StreetItemType.NOUN) and t.chars.is_capital_upper): 
                    pass
                else: 
                    break
            if (t.is_hiphen and sit is not None and ((sit.typ == StreetItemType.NAME or ((sit.typ == StreetItemType.STDADJECTIVE and not sit.is_abridge))))): 
                sit1 = StreetItemToken.tryParse(t.next0_, loc_streets, False, sit, False)
                if (sit1 is None): 
                    break
                if (sit1.typ == StreetItemType.NUMBER): 
                    tt = sit1.end_token.next0_
                    if (tt is not None and tt.is_comma): 
                        tt = tt.next0_
                    ok = False
                    ait = AddressItemToken.tryParse(tt, loc_streets, False, True, None)
                    if (ait is not None): 
                        if (ait.typ == AddressItemToken.ItemType.HOUSE): 
                            ok = True
                    if (not ok): 
                        if (len(res) == 2 and res[0].typ == StreetItemType.NOUN): 
                            if (res[0].termin.canonic_text == "МИКРОРАЙОН"): 
                                ok = True
                    if (ok): 
                        sit = sit1
                        res.append(sit)
                        t = sit.end_token
                        sit.number_has_prefix = True
                        continue
                if (sit1.typ != StreetItemType.NAME and sit1.typ != StreetItemType.NAME): 
                    break
                if (t.is_whitespace_before and t.is_whitespace_after): 
                    break
                if (res[0].begin_token.previous is not None): 
                    aaa = AddressItemToken.tryParse(res[0].begin_token.previous, None, False, True, None)
                    if (aaa is not None and aaa.typ == AddressItemToken.ItemType.DETAIL and aaa.detail_type == AddressDetailType.CROSS): 
                        break
                sit = sit1
                res.append(sit)
                t = sit.end_token
                continue
            elif (t.is_hiphen and sit is not None and sit.typ == StreetItemType.NUMBER): 
                sit1 = StreetItemToken.tryParse(t.next0_, loc_streets, False, None, False)
                if (sit1 is not None and ((sit1.typ == StreetItemType.STDADJECTIVE or sit1.typ == StreetItemType.STDNAME or sit1.typ == StreetItemType.NAME))): 
                    sit.number_has_prefix = True
                    sit = sit1
                    res.append(sit)
                    t = sit.end_token
                    continue
            if (t.isChar('.') and sit is not None and sit.typ == StreetItemType.NOUN): 
                if (t.whitespaces_after_count > 1): 
                    break
                sit = StreetItemToken.tryParse(t.next0_, loc_streets, False, None, False)
                if (sit is None): 
                    break
                if (sit.typ == StreetItemType.NUMBER or sit.typ == StreetItemType.STDADJECTIVE): 
                    sit1 = StreetItemToken.tryParse(sit.end_token.next0_, None, False, None, False)
                    if (sit1 is not None and ((sit1.typ == StreetItemType.STDADJECTIVE or sit1.typ == StreetItemType.STDNAME or sit1.typ == StreetItemType.NAME))): 
                        pass
                    else: 
                        break
                elif (sit.typ != StreetItemType.NAME and sit.typ != StreetItemType.STDNAME and sit.typ != StreetItemType.AGE): 
                    break
                if (t.previous.getMorphClassInDictionary().is_noun): 
                    if (not sit.is_in_dictionary): 
                        tt = sit.end_token.next0_
                        has_house = False
                        first_pass2746 = True
                        while True:
                            if first_pass2746: first_pass2746 = False
                            else: tt = tt.next0_
                            if (not (tt is not None)): break
                            if (tt.is_newline_before): 
                                break
                            if (tt.is_comma): 
                                continue
                            ai = AddressItemToken.tryParse(tt, None, False, True, None)
                            if (ai is not None and ((ai.typ == AddressItemToken.ItemType.HOUSE or ai.typ == AddressItemToken.ItemType.BUILDING or ai.typ == AddressItemToken.ItemType.CORPUS))): 
                                has_house = True
                                break
                            vv = StreetItemToken.tryParse(tt, None, False, None, False)
                            if (vv is None or vv.typ == StreetItemType.NOUN): 
                                break
                            tt = vv.end_token
                        if (not has_house): 
                            break
                    if (t.previous.previous is not None): 
                        npt11 = NounPhraseHelper.tryParse(t.previous.previous, NounPhraseParseAttr.NO, 0)
                        if (npt11 is not None and npt11.end_token == t.previous): 
                            break
                res.append(sit)
            else: 
                sit = StreetItemToken.tryParse(t, loc_streets, False, res[len(res) - 1], False)
                if (sit is None): 
                    spli = StreetItemToken._tryParseSpec(t, res[len(res) - 1])
                    if (spli is not None and len(spli) > 0): 
                        res.extend(spli)
                        t = spli[len(spli) - 1].end_token
                        continue
                    if (((isinstance(t, TextToken)) and ((len(res) == 2 or len(res) == 3)) and res[0].typ == StreetItemType.NOUN) and res[1].typ == StreetItemType.NUMBER and ((((Utils.asObjectOrNull(t, TextToken)).term == "ГОДА" or (Utils.asObjectOrNull(t, TextToken)).term == "МАЯ" or (Utils.asObjectOrNull(t, TextToken)).term == "МАРТА") or (Utils.asObjectOrNull(t, TextToken)).term == "СЪЕЗДА"))): 
                        sit = StreetItemToken._new235(t, t, StreetItemType.STDNAME, (Utils.asObjectOrNull(t, TextToken)).term)
                        res.append(sit)
                        continue
                    sit = res[len(res) - 1]
                    if (t is None): 
                        break
                    if (sit.typ == StreetItemType.NOUN and ((sit.termin.canonic_text == "МИКРОРАЙОН" or sit.termin.canonic_text == "МІКРОРАЙОН")) and (t.whitespaces_before_count < 2)): 
                        tt1 = t
                        if (tt1.is_hiphen and tt1.next0_ is not None): 
                            tt1 = tt1.next0_
                        if (BracketHelper.isBracket(tt1, True) and tt1.next0_ is not None): 
                            tt1 = tt1.next0_
                        tt2 = tt1.next0_
                        br = False
                        if (BracketHelper.isBracket(tt2, True)): 
                            tt2 = tt2.next0_
                            br = True
                        if (((isinstance(tt1, TextToken)) and tt1.length_char == 1 and tt1.chars.is_letter) and ((AddressItemToken.checkHouseAfter(tt2, False, True) or tt2 is None))): 
                            sit = StreetItemToken._new235(t, (tt1.next0_ if br else tt1), StreetItemType.NAME, (Utils.asObjectOrNull(tt1, TextToken)).term)
                            ch1 = AddressItemToken.correctChar(sit.value[0])
                            if ((ord(ch1)) != 0 and ch1 != sit.value[0]): 
                                sit.alt_value = "{0}".format(ch1)
                            res.append(sit)
                            break
                    if (t.is_comma and (((sit.typ == StreetItemType.NAME or sit.typ == StreetItemType.STDNAME or sit.typ == StreetItemType.STDPARTOFNAME) or sit.typ == StreetItemType.STDADJECTIVE or ((sit.typ == StreetItemType.NUMBER and len(res) > 1 and (((res[len(res) - 2].typ == StreetItemType.NAME or res[len(res) - 2].typ == StreetItemType.STDNAME or res[len(res) - 2].typ == StreetItemType.STDADJECTIVE) or res[len(res) - 2].typ == StreetItemType.STDPARTOFNAME))))))): 
                        sit = StreetItemToken.tryParse(t.next0_, None, False, None, False)
                        if (sit is not None and sit.typ == StreetItemType.NOUN): 
                            ttt = sit.end_token.next0_
                            if (ttt is not None and ttt.is_comma): 
                                ttt = ttt.next0_
                            add = AddressItemToken.tryParse(ttt, None, False, True, None)
                            if (add is not None and ((add.typ == AddressItemToken.ItemType.HOUSE or add.typ == AddressItemToken.ItemType.CORPUS or add.typ == AddressItemToken.ItemType.BUILDING))): 
                                res.append(sit)
                                t = sit.end_token
                                continue
                    if (BracketHelper.canBeStartOfSequence(t, True, False)): 
                        sit1 = res[len(res) - 1]
                        if (sit1.typ == StreetItemType.NOUN and ((sit1.noun_is_doubt_coef == 0 or (((isinstance(t.next0_, TextToken)) and not t.next0_.chars.is_all_lower))))): 
                            br = BracketHelper.tryParse(t, BracketParseAttr.NO, 100)
                            if (br is not None and (br.length_char < 50)): 
                                sit2 = StreetItemToken.tryParse(t.next0_, loc_streets, False, None, False)
                                if (sit2 is not None and sit2.end_token.next0_ == br.end_token): 
                                    if (sit2.value is None and sit2.typ == StreetItemType.NAME): 
                                        sit2.value = MiscHelper.getTextValue(sit2.begin_token, sit2.end_token, GetTextAttr.NO)
                                    sit2.begin_token = t
                                    sit2.is_in_brackets = True
                                    sit2.end_token = br.end_token
                                    t = sit2.end_token
                                    res.append(sit2)
                                    continue
                                res.append(StreetItemToken._new254(t, br.end_token, StreetItemType.NAME, MiscHelper.getTextValue(t, br.end_token, GetTextAttr.NO), True))
                                t = br.end_token
                                continue
                    if (t.is_hiphen and (isinstance(t.next0_, NumberToken))): 
                        sit = res[len(res) - 1]
                        if (sit.typ == StreetItemType.NOUN and (((sit.termin.canonic_text == "КВАРТАЛ" or sit.termin.canonic_text == "МИКРОРАЙОН" or sit.termin.canonic_text == "ГОРОДОК") or sit.termin.canonic_text == "МІКРОРАЙОН"))): 
                            sit = StreetItemToken._new220(t, t.next0_, StreetItemType.NUMBER, Utils.asObjectOrNull(t.next0_, NumberToken), True)
                            res.append(sit)
                            t = t.next0_
                            continue
                    break
                res.append(sit)
                if (sit.typ == StreetItemType.NAME): 
                    cou = 0
                    for jj in range(len(res) - 1, -1, -1):
                        if (sit.typ == StreetItemType.NAME): 
                            cou += 1
                        else: 
                            break
                    else: jj = -1
                    if (cou > 4): 
                        if (jj < 0): 
                            return None
                        del res[jj:jj+len(res) - jj]
                        break
            t = sit.end_token
        i = 0
        first_pass2747 = True
        while True:
            if first_pass2747: first_pass2747 = False
            else: i += 1
            if (not (i < (len(res) - 1))): break
            if (res[i].typ == StreetItemType.NAME and res[i + 1].typ == StreetItemType.NAME and (res[i].whitespaces_after_count < 3)): 
                is_prop = False
                is_pers = False
                if (res[i].begin_token.morph.class0_.is_noun): 
                    rt = res[i].kit.processReferent("PERSON", res[i].begin_token)
                    if (rt is not None): 
                        if (rt.referent.type_name == "PERSONPROPERTY"): 
                            is_prop = True
                        elif (rt.end_token == res[i + 1].end_token): 
                            is_pers = True
                if ((i == 0 and ((not is_prop and not is_pers)) and ((i + 2) < len(res))) and res[i + 2].typ == StreetItemType.NOUN and not res[i].begin_token.morph.class0_.is_adjective): 
                    if (MiscLocationHelper.checkGeoObjectBefore(res[0].begin_token) and res[0].end_token.next0_ == res[1].begin_token and (res[0].whitespaces_after_count < 2)): 
                        pass
                    else: 
                        del res[i]
                        i -= 1
                        continue
                if (res[i].morph.class0_.is_adjective and res[i + 1].morph.class0_.is_adjective): 
                    if (res[i].end_token.next0_.is_hiphen): 
                        pass
                    elif (i == 1 and res[0].typ == StreetItemType.NOUN and len(res) == 3): 
                        pass
                    elif (i == 0 and len(res) == 3 and res[2].typ == StreetItemType.NOUN): 
                        pass
                    else: 
                        continue
                res[i].value = MiscHelper.getTextValue(res[i].begin_token, res[i + 1].end_token, GetTextAttr.NO)
                if ("-" in res[i].value): 
                    res[i].value = res[i].value.replace('-', ' ')
                if (not res[i + 1].begin_token.previous.is_hiphen and ((not res[i].begin_token.morph.class0_.is_adjective or is_prop or is_pers))): 
                    if (is_pers and res[i + 1].end_token.getMorphClassInDictionary().is_proper_name): 
                        res[i].alt_value = MiscHelper.getTextValue(res[i].begin_token, res[i].end_token, GetTextAttr.NO)
                    else: 
                        res[i].alt_value = MiscHelper.getTextValue(res[i + 1].begin_token, res[i + 1].end_token, GetTextAttr.NO)
                    if ("-" in res[i].alt_value): 
                        res[i].alt_value = res[i].alt_value.replace('-', ' ')
                res[i].end_token = res[i + 1].end_token
                res[i].exist_street = (None)
                res[i].is_in_dictionary = (res[i + 1].is_in_dictionary or res[i].is_in_dictionary)
                del res[i + 1]
                i -= 1
        i = 0
        while i < (len(res) - 1): 
            if (res[i].typ == StreetItemType.STDADJECTIVE and res[i].end_token.isChar('.') and res[i + 1].__isSurname()): 
                res[i + 1].value = (Utils.asObjectOrNull(res[i + 1].begin_token, TextToken)).term
                res[i + 1].alt_value = MiscHelper.getTextValue(res[i].begin_token, res[i + 1].end_token, GetTextAttr.NO)
                res[i + 1].begin_token = res[i].begin_token
                del res[i]
                break
            i += 1
        i = 0
        while i < (len(res) - 1): 
            if ((res[i + 1].typ == StreetItemType.STDADJECTIVE and res[i + 1].end_token.isChar('.') and res[i + 1].begin_token.length_char == 1) and not res[i].begin_token.chars.is_all_lower): 
                if (res[i].__isSurname()): 
                    if (i == (len(res) - 2) or res[i + 2].typ != StreetItemType.NOUN): 
                        res[i].end_token = res[i + 1].end_token
                        del res[i + 1]
                        break
            i += 1
        i = 0
        first_pass2748 = True
        while True:
            if first_pass2748: first_pass2748 = False
            else: i += 1
            if (not (i < (len(res) - 1))): break
            if (res[i].typ == StreetItemType.NAME or res[i].typ == StreetItemType.STDNAME or res[i].typ == StreetItemType.STDADJECTIVE): 
                if (res[i + 1].typ == StreetItemType.NOUN and not res[i + 1].is_abridge): 
                    i0 = -1
                    if (i == 1 and res[0].typ == StreetItemType.NOUN and len(res) == 3): 
                        i0 = 0
                    elif (i == 0 and len(res) == 3 and res[2].typ == StreetItemType.NOUN): 
                        i0 = 2
                    if (i0 < 0): 
                        continue
                    if (res[i0].termin == res[i + 1].termin): 
                        continue
                    res[i].alt_value = (Utils.ifNotNull(res[i].value, MiscHelper.getTextValue(res[i].begin_token, res[i].end_token, GetTextAttr.NO)))
                    if (res[i].typ == StreetItemType.STDADJECTIVE): 
                        adjs = MiscLocationHelper.getStdAdjFull(res[i].begin_token, res[i + 1].morph.gender, res[i + 1].morph.number, True)
                        if (len(adjs) > 0): 
                            res[i].alt_value = adjs[0]
                    res[i].value = "{0} {1}".format(res[i].alt_value, res[i + 1].termin.canonic_text)
                    res[i].typ = StreetItemType.STDNAME
                    res[i0].alt_termin = res[i + 1].termin
                    res[i].end_token = res[i + 1].end_token
                    del res[i + 1]
                    i -= 1
        if ((len(res) >= 3 and res[0].typ == StreetItemType.NOUN and res[0].termin.canonic_text == "КВАРТАЛ") and ((res[1].typ == StreetItemType.NAME or res[1].typ == StreetItemType.STDNAME)) and res[2].typ == StreetItemType.NOUN): 
            if (len(res) == 3 or res[3].typ == StreetItemType.NUMBER): 
                res[1].value = "{0} {1}".format(MiscHelper.getTextValueOfMetaToken(res[1], GetTextAttr.NO), res[2].termin.canonic_text)
                res[1].end_token = res[2].end_token
                del res[2]
        if ((len(res) >= 3 and res[0].typ == StreetItemType.NOUN and res[0].termin.canonic_text == "КВАРТАЛ") and ((res[2].typ == StreetItemType.NAME or res[2].typ == StreetItemType.STDNAME)) and res[1].typ == StreetItemType.NOUN): 
            if (len(res) == 3 or res[3].typ == StreetItemType.NUMBER): 
                res[1].value = "{0} {1}".format(MiscHelper.getTextValueOfMetaToken(res[2], GetTextAttr.NO), res[1].termin.canonic_text)
                res[1].end_token = res[2].end_token
                res[1].typ = StreetItemType.NAME
                del res[2]
        if (len(res) >= 3 and res[0].typ == StreetItemType.NUMBER and res[1].typ == StreetItemType.NOUN): 
            nt = Utils.asObjectOrNull(res[0].begin_token, NumberToken)
            if (nt is not None and nt.typ == NumberSpellingType.DIGIT and nt.morph.class0_.is_undefined): 
                return None
        ii0 = -1
        ii1 = -1
        if (res[0].typ == StreetItemType.NOUN and res[0].is_road): 
            ii1 = 0
            ii0 = ii1
            if (((ii0 + 1) < len(res)) and res[ii0 + 1].typ == StreetItemType.NUMBER and res[ii0 + 1].is_number_km): 
                ii0 += 1
        elif ((len(res) > 1 and res[0].typ == StreetItemType.NUMBER and res[0].is_number_km) and res[1].typ == StreetItemType.NOUN and res[1].is_road): 
            ii1 = 1
            ii0 = ii1
        if (ii0 >= 0): 
            if (len(res) == (ii0 + 1)): 
                tt = res[ii0].end_token.next0_
                num = StreetItemToken.__tryAttachRoadNum(tt)
                if (num is not None): 
                    res.append(num)
                    tt = num.end_token.next0_
                    res[0].is_abridge = False
                if (tt is not None and (isinstance(tt.getReferent(), GeoReferent))): 
                    g1 = Utils.asObjectOrNull(tt.getReferent(), GeoReferent)
                    tt = tt.next0_
                    if (tt is not None and tt.is_hiphen): 
                        tt = tt.next0_
                    g2 = (None if tt is None else Utils.asObjectOrNull(tt.getReferent(), GeoReferent))
                    if (g2 is not None): 
                        if (g1.is_city and g2.is_city): 
                            nam = StreetItemToken._new236(res[0].end_token.next0_, tt, StreetItemType.NAME)
                            nam.value = "{0} - {1}".format(g1.toString(True, tt.kit.base_language, 0), g2.toString(True, tt.kit.base_language, 0)).upper()
                            nam.alt_value = "{0} - {1}".format(g2.toString(True, tt.kit.base_language, 0), g1.toString(True, tt.kit.base_language, 0)).upper()
                            res.append(nam)
                elif (BracketHelper.isBracket(tt, False)): 
                    br = BracketHelper.tryParse(tt, BracketParseAttr.NO, 100)
                    if (br is not None): 
                        nam = StreetItemToken._new257(tt, br.end_token, StreetItemType.NAME, True)
                        nam.value = MiscHelper.getTextValue(tt.next0_, br.end_token, GetTextAttr.NO)
                        res.append(nam)
            elif ((len(res) == (ii0 + 2) and res[ii0 + 1].typ == StreetItemType.NAME and res[ii0 + 1].end_token.next0_ is not None) and res[ii0 + 1].end_token.next0_.is_hiphen): 
                tt = res[ii0 + 1].end_token.next0_.next0_
                g2 = (None if tt is None else Utils.asObjectOrNull(tt.getReferent(), GeoReferent))
                te = None
                name2 = None
                if (g2 is None and tt is not None): 
                    rt = tt.kit.processReferent("GEO", tt)
                    if (rt is not None): 
                        te = rt.end_token
                        name2 = rt.referent.toString(True, te.kit.base_language, 0)
                    else: 
                        cits2 = CityItemToken.tryParseList(tt, None, 2)
                        if (cits2 is not None): 
                            if (len(cits2) == 1 and cits2[0].typ == CityItemToken.ItemType.PROPERNAME): 
                                name2 = cits2[0].value
                                te = cits2[0].end_token
                else: 
                    te = tt
                    name2 = g2.toString(True, te.kit.base_language, 0)
                if (((g2 is not None and g2.is_city)) or ((g2 is None and name2 is not None))): 
                    res[ii0 + 1].alt_value = "{0} - {1}".format(name2, Utils.ifNotNull(res[ii0 + 1].value, res[ii0 + 1].getSourceText())).upper()
                    res[ii0 + 1].value = "{0} - {1}".format(Utils.ifNotNull(res[ii0 + 1].value, res[ii0 + 1].getSourceText()), name2).upper()
                    res[ii0 + 1].end_token = te
            nn = StreetItemToken.__tryAttachRoadNum(res[len(res) - 1].end_token.next0_)
            if (nn is not None): 
                res.append(nn)
                res[ii1].is_abridge = False
            if (len(res) > (ii0 + 1) and res[ii0 + 1].typ == StreetItemType.NAME and res[ii1].termin.canonic_text == "АВТОДОРОГА"): 
                npt = NounPhraseHelper.tryParse(res[ii0 + 1].begin_token, NounPhraseParseAttr.NO, 0)
                if (npt is not None and len(npt.adjectives) > 0): 
                    return None
        if (len(res) > 0): 
            it = res[len(res) - 1]
            it0 = (res[len(res) - 2] if len(res) > 1 else None)
            if (it.typ == StreetItemType.NUMBER and not it.number_has_prefix): 
                if (isinstance(it.begin_token, NumberToken)): 
                    if (not it.begin_token.morph.class0_.is_adjective or it.begin_token.morph.class0_.is_noun): 
                        if (AddressItemToken.checkHouseAfter(it.end_token.next0_, False, True)): 
                            it.number_has_prefix = True
                        elif (it0 is not None and it0.typ == StreetItemType.NOUN and (((it0.termin.canonic_text == "МИКРОРАЙОН" or it0.termin.canonic_text == "МІКРОРАЙОН" or it0.termin.canonic_text == "КВАРТАЛ") or it0.termin.canonic_text == "ГОРОДОК"))): 
                            ait = AddressItemToken.tryParse(it.begin_token, loc_streets, False, True, None)
                            if (ait is not None and ait.typ == AddressItemToken.ItemType.NUMBER and ait.end_char > it.end_char): 
                                it.number = (None)
                                it.value = ait.value
                                it.end_token = ait.end_token
                                it.typ = StreetItemType.NAME
                        elif (it0 is not None and it0.termin is not None and it0.termin.canonic_text == "ПОЧТОВОЕ ОТДЕЛЕНИЕ"): 
                            it.number_has_prefix = True
                        elif (len(res) == 2 and res[0].typ == StreetItemType.NOUN and (res[0].whitespaces_after_count < 2)): 
                            pass
                        else: 
                            del res[len(res) - 1]
                    else: 
                        it.number_has_prefix = True
        if (len(res) == 0): 
            return None
        i = 0
        while i < len(res): 
            if ((res[i].typ == StreetItemType.NOUN and res[i].chars.is_capital_upper and (((res[i].termin.canonic_text == "НАБЕРЕЖНАЯ" or res[i].termin.canonic_text == "МИКРОРАЙОН" or res[i].termin.canonic_text == "НАБЕРЕЖНА") or res[i].termin.canonic_text == "МІКРОРАЙОН" or res[i].termin.canonic_text == "ГОРОДОК"))) and res[i].begin_token.isValue(res[i].termin.canonic_text, None)): 
                ok = False
                if (i > 0 and ((res[i - 1].typ == StreetItemType.NOUN or res[i - 1].typ == StreetItemType.STDADJECTIVE))): 
                    ok = True
                elif (i > 1 and ((res[i - 1].typ == StreetItemType.STDADJECTIVE or res[i - 1].typ == StreetItemType.NUMBER)) and res[i - 2].typ == StreetItemType.NOUN): 
                    ok = True
                if (ok): 
                    res[i].termin = (None)
                    res[i].typ = StreetItemType.NAME
            i += 1
        last = res[len(res) - 1]
        for kk in range(2):
            ttt = last.end_token.next0_
            if (((last.typ == StreetItemType.NAME and ttt is not None and ttt.length_char == 1) and ttt.chars.is_all_upper and (ttt.whitespaces_before_count < 2)) and ttt.next0_ is not None and ttt.next0_.isChar('.')): 
                last.end_token = ttt.next0_
        return res
    
    @staticmethod
    def __tryAttachRoadNum(t : 'Token') -> 'StreetItemToken':
        from pullenti.ner.NumberToken import NumberToken
        if (t is None): 
            return None
        if (not t.chars.is_letter or t.length_char != 1): 
            return None
        tt = t.next0_
        if (tt is not None and tt.is_hiphen): 
            tt = tt.next0_
        if (not ((isinstance(tt, NumberToken)))): 
            return None
        res = StreetItemToken._new236(t, tt, StreetItemType.NAME)
        res.value = "{0}{1}".format(t.getSourceText().upper(), (Utils.asObjectOrNull(tt, NumberToken)).value)
        return res
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.core.TerminCollection import TerminCollection
        from pullenti.ner.core.Termin import Termin
        from pullenti.morph.MorphLang import MorphLang
        if (StreetItemToken.__m_ontology is not None): 
            return
        StreetItemToken.__m_ontology = TerminCollection()
        StreetItemToken.__m_std_ont_misc = TerminCollection()
        t = Termin._new259("УЛИЦА", StreetItemType.NOUN, MorphGender.FEMINIE)
        t.addAbridge("УЛ.")
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new260("ВУЛИЦЯ", StreetItemType.NOUN, MorphLang.UA, MorphGender.FEMINIE)
        t.addAbridge("ВУЛ.")
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new118("STREET", StreetItemType.NOUN)
        t.addAbridge("ST.")
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new262("ПЛОЩАДЬ", StreetItemType.NOUN, 1, MorphGender.FEMINIE)
        t.addAbridge("ПЛ.")
        t.addAbridge("ПЛОЩ.")
        t.addAbridge("ПЛ-ДЬ")
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new263("ПЛОЩА", StreetItemType.NOUN, MorphLang.UA, 1, MorphGender.FEMINIE)
        t.addAbridge("ПЛ.")
        t.addAbridge("ПЛОЩ.")
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new262("МАЙДАН", StreetItemType.NOUN, 0, MorphGender.MASCULINE)
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new118("SQUARE", StreetItemType.NOUN)
        t.addAbridge("SQ.")
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new262("ПРОЕЗД", StreetItemType.NOUN, 1, MorphGender.MASCULINE)
        t.addAbridge("ПР.")
        t.addAbridge("П-Д")
        t.addAbridge("ПР-Д")
        t.addAbridge("ПР-ЗД")
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new262("ЛИНИЯ", StreetItemType.NOUN, 2, MorphGender.FEMINIE)
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new263("ЛІНІЯ", StreetItemType.NOUN, MorphLang.UA, 2, MorphGender.FEMINIE)
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new262("ПРОСПЕКТ", StreetItemType.NOUN, 0, MorphGender.MASCULINE)
        StreetItemToken.__m_prospect = t
        t.addAbridge("ПРОС.")
        t.addAbridge("ПРКТ")
        t.addAbridge("ПРОСП.")
        t.addAbridge("ПР-Т")
        t.addAbridge("ПР-КТ")
        t.addAbridge("П-Т")
        t.addAbridge("П-КТ")
        t.addAbridge("ПР Т")
        t.addAbridge("ПР-ТЕ")
        t.addAbridge("ПР-КТЕ")
        t.addAbridge("П-ТЕ")
        t.addAbridge("П-КТЕ")
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new262("ПЕРЕУЛОК", StreetItemType.NOUN, 0, MorphGender.MASCULINE)
        t.addAbridge("ПЕР.")
        t.addAbridge("ПЕР-К")
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new262("ПРОУЛОК", StreetItemType.NOUN, 0, MorphGender.MASCULINE)
        t.addAbridge("ПРОУЛ.")
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new263("ПРОВУЛОК", StreetItemType.NOUN, MorphLang.UA, 0, MorphGender.MASCULINE)
        t.addAbridge("ПРОВ.")
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new120("LANE", StreetItemType.NOUN, 0)
        t.addAbridge("LN.")
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new262("ТУПИК", StreetItemType.NOUN, 1, MorphGender.MASCULINE)
        t.addAbridge("ТУП.")
        t.addAbridge("Т.")
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new262("БУЛЬВАР", StreetItemType.NOUN, 0, MorphGender.MASCULINE)
        t.addAbridge("БУЛЬВ.")
        t.addAbridge("БУЛ.")
        t.addAbridge("Б-Р")
        t.addAbridge("Б-РЕ")
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new120("BOULEVARD", StreetItemType.NOUN, 0)
        t.addAbridge("BLVD")
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new120("СКВЕР", StreetItemType.NOUN, 1)
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new262("НАБЕРЕЖНАЯ", StreetItemType.NOUN, 0, MorphGender.FEMINIE)
        t.addAbridge("НАБ.")
        t.addAbridge("НАБЕР.")
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new263("НАБЕРЕЖНА", StreetItemType.NOUN, MorphLang.UA, 0, MorphGender.FEMINIE)
        t.addAbridge("НАБ.")
        t.addAbridge("НАБЕР.")
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new262("АЛЛЕЯ", StreetItemType.NOUN, 0, MorphGender.FEMINIE)
        t.addAbridge("АЛ.")
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new263("АЛЕЯ", StreetItemType.NOUN, MorphLang.UA, 0, MorphGender.FEMINIE)
        t.addAbridge("АЛ.")
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new120("ALLEY", StreetItemType.NOUN, 0)
        t.addAbridge("ALY.")
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new262("ПРОСЕКА", StreetItemType.NOUN, 1, MorphGender.FEMINIE)
        t.addVariant("ПРОСЕК", False)
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new263("ПРОСІКА", StreetItemType.NOUN, MorphLang.UA, 1, MorphGender.FEMINIE)
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new262("ШОССЕ", StreetItemType.NOUN, 1, MorphGender.NEUTER)
        t.addAbridge("Ш.")
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new263("ШОСЕ", StreetItemType.NOUN, MorphLang.UA, 1, MorphGender.NEUTER)
        t.addAbridge("Ш.")
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new120("ROAD", StreetItemType.NOUN, 1)
        t.addAbridge("RD.")
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new262("МИКРОРАЙОН", StreetItemType.NOUN, 0, MorphGender.MASCULINE)
        t.addAbridge("МКР.")
        t.addAbridge("МИКР-Н")
        t.addAbridge("МКР-Н")
        t.addAbridge("МКРН.")
        t.addAbridge("М-Н")
        t.addAbridge("М-ОН")
        t.addAbridge("М/Р")
        t.addVariant("МІКРОРАЙОН", False)
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new262("КВАРТАЛ", StreetItemType.NOUN, 2, MorphGender.MASCULINE)
        t.addAbridge("КВАРТ.")
        t.addAbridge("КВ-Л")
        t.addAbridge("КВ.")
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new290("ЖИЛОЙ КОМПЛЕКС", StreetItemType.NOUN, "ЖК", 0, MorphGender.MASCULINE)
        t.addVariant("ЖИЛКОМПЛЕКС", False)
        t.addAbridge("ЖИЛ.К.")
        t.addAbridge("Ж/К")
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new262("ГОРОДОК", StreetItemType.NOUN, 0, MorphGender.MASCULINE)
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new263("МІСТЕЧКО", StreetItemType.NOUN, MorphLang.UA, 0, MorphGender.NEUTER)
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new120("HILL", StreetItemType.NOUN, 0)
        t.addAbridge("HL.")
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new262("ВОЕННЫЙ ГОРОДОК", StreetItemType.NOUN, 0, MorphGender.MASCULINE)
        t.addAbridge("В.ГОРОДОК")
        t.addAbridge("В/Г")
        t.addAbridge("В/ГОРОДОК")
        t.addAbridge("В/ГОР")
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new262("ПРОМЗОНА", StreetItemType.NOUN, 1, MorphGender.FEMINIE)
        t.addVariant("ПРОМЫШЛЕННАЯ ЗОНА", False)
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new262("ЖИЛАЯ ЗОНА", StreetItemType.NOUN, 1, MorphGender.FEMINIE)
        t.addVariant("ЖИЛЗОНА", False)
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new262("КОММУНАЛЬНАЯ ЗОНА", StreetItemType.NOUN, 1, MorphGender.FEMINIE)
        t.addVariant("КОМЗОНА", False)
        t.addAbridge("КОММУН. ЗОНА")
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new262("МАССИВ", StreetItemType.NOUN, 2, MorphGender.MASCULINE)
        t.addVariant("ЖИЛОЙ МАССИВ", False)
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new262("МОСТ", StreetItemType.NOUN, 2, MorphGender.MASCULINE)
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new263("МІСТ", StreetItemType.NOUN, MorphLang.UA, 2, MorphGender.MASCULINE)
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new262("ПАРК", StreetItemType.NOUN, 2, MorphGender.MASCULINE)
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new120("PLAZA", StreetItemType.NOUN, 1)
        t.addAbridge("PLZ")
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new303("СТАНЦИЯ МЕТРО", "МЕТРО", StreetItemType.NOUN, 0, MorphGender.FEMINIE)
        StreetItemToken.__m_metro = t
        t.addVariant("СТАНЦІЯ МЕТРО", False)
        t.addAbridge("СТ.МЕТРО")
        t.addAbridge("СТ.М.")
        t.addAbridge("МЕТРО")
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new262("АВТОДОРОГА", StreetItemType.NOUN, 0, MorphGender.FEMINIE)
        t.addVariant("ФЕДЕРАЛЬНАЯ АВТОДОРОГА", False)
        t.addVariant("АВТОМОБИЛЬНАЯ ДОРОГА", False)
        t.addVariant("АВТОТРАССА", False)
        t.addVariant("ФЕДЕРАЛЬНАЯ ТРАССА", False)
        t.addVariant("АВТОМАГИСТРАЛЬ", False)
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new303("ДОРОГА", "АВТОДОРОГА", StreetItemType.NOUN, 1, MorphGender.FEMINIE)
        t.addVariant("ТРАССА", False)
        t.addVariant("МАГИСТРАЛЬ", False)
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new263("АВТОДОРОГА", StreetItemType.NOUN, MorphLang.UA, 0, MorphGender.FEMINIE)
        t.addVariant("ФЕДЕРАЛЬНА АВТОДОРОГА", False)
        t.addVariant("АВТОМОБІЛЬНА ДОРОГА", False)
        t.addVariant("АВТОТРАСА", False)
        t.addVariant("ФЕДЕРАЛЬНА ТРАСА", False)
        t.addVariant("АВТОМАГІСТРАЛЬ", False)
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new307("ДОРОГА", "АВТОДОРОГА", StreetItemType.NOUN, MorphLang.UA, 1, MorphGender.FEMINIE)
        t.addVariant("ТРАСА", False)
        t.addVariant("МАГІСТРАЛЬ", False)
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new308("МОСКОВСКАЯ КОЛЬЦЕВАЯ АВТОМОБИЛЬНАЯ ДОРОГА", "МКАД", StreetItemType.FIX, MorphGender.FEMINIE)
        t.addVariant("МОСКОВСКАЯ КОЛЬЦЕВАЯ АВТОДОРОГА", False)
        StreetItemToken.__m_ontology.add(t)
        StreetItemToken.__m_ontology.add(Termin._new118("САДОВОЕ КОЛЬЦО", StreetItemType.FIX))
        StreetItemToken.__m_ontology.add(Termin._new118("БУЛЬВАРНОЕ КОЛЬЦО", StreetItemType.FIX))
        StreetItemToken.__m_ontology.add(Termin._new118("ТРАНСПОРТНОЕ КОЛЬЦО", StreetItemType.FIX))
        t = Termin._new259("ПОЧТОВОЕ ОТДЕЛЕНИЕ", StreetItemType.STDNAME, MorphGender.NEUTER)
        t.addAbridge("П.О.")
        t.addAbridge("ПОЧТ.ОТД.")
        t.addAbridge("ПОЧТОВ.ОТД.")
        t.addAbridge("ПОЧТОВОЕ ОТД.")
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new118("БОЛЬШОЙ", StreetItemType.STDADJECTIVE)
        t.addAbridge("БОЛ.")
        t.addAbridge("Б.")
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new119("ВЕЛИКИЙ", StreetItemType.STDADJECTIVE, MorphLang.UA)
        t.addAbridge("ВЕЛ.")
        t.addAbridge("В.")
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new118("МАЛЫЙ", StreetItemType.STDADJECTIVE)
        t.addAbridge("МАЛ.")
        t.addAbridge("М.")
        t.addVariant("МАЛИЙ", False)
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new118("СРЕДНИЙ", StreetItemType.STDADJECTIVE)
        t.addAbridge("СРЕД.")
        t.addAbridge("СР.")
        t.addAbridge("С.")
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new119("СЕРЕДНІЙ", StreetItemType.STDADJECTIVE, MorphLang.UA)
        t.addAbridge("СЕРЕД.")
        t.addAbridge("СЕР.")
        t.addAbridge("С.")
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new118("ВЕРХНИЙ", StreetItemType.STDADJECTIVE)
        t.addAbridge("ВЕРХН.")
        t.addAbridge("ВЕРХ.")
        t.addAbridge("ВЕР.")
        t.addAbridge("В.")
        t.addVariant("ВЕРХНІЙ", False)
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new118("НИЖНИЙ", StreetItemType.STDADJECTIVE)
        t.addAbridge("НИЖН.")
        t.addAbridge("НИЖ.")
        t.addAbridge("Н.")
        t.addVariant("НИЖНІЙ", False)
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new118("СТАРЫЙ", StreetItemType.STDADJECTIVE)
        t.addAbridge("СТАР.")
        t.addAbridge("СТ.")
        t.addVariant("СТАРИЙ", False)
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new118("НОВЫЙ", StreetItemType.STDADJECTIVE)
        t.addAbridge("НОВ.")
        t.addVariant("НОВИЙ", False)
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new118("НОМЕР", StreetItemType.STDADJECTIVE)
        t.addAbridge("N")
        t.addAbridge("№")
        t.addAbridge("НОМ.")
        StreetItemToken.__m_ontology.add(t)
        for s in ["ФРИДРИХА ЭНГЕЛЬСА", "КАРЛА МАРКСА", "РОЗЫ ЛЮКСЕМБУРГ"]: 
            t = Termin._new118(s, StreetItemType.STDNAME)
            t.addAllAbridges(0, 0, 0)
            StreetItemToken.__m_ontology.add(t)
        for s in ["МАРТА", "МАЯ", "ОКТЯБРЯ", "НОЯБРЯ", "БЕРЕЗНЯ", "ТРАВНЯ", "ЖОВТНЯ", "ЛИСТОПАДА"]: 
            StreetItemToken.__m_ontology.add(Termin._new118(s, StreetItemType.STDNAME))
        for s in ["МАРШАЛА", "ГЕНЕРАЛА", "АДМИРАЛА", "КОСМОНАВТА", "ЛЕТЧИКА", "АВИАКОНСТРУКТОРА", "АРХИТЕКТОРА", "СКУЛЬПТОРА", "ХУДОЖНИКА", "КОНСТРУКТОРА", "АКАДЕМИКА", "ПРОФЕССОРА", "ЛЕЙТЕНАНТА", "КАПИТАНА", "МАЙОРА", "ПОДПОЛКОВНИКА", "ПОЛКОВНИКА", "ПОЛИЦИИ", "МИЛИЦИИ"]: 
            StreetItemToken.__m_std_ont_misc.add(Termin(s))
            t = Termin._new118(s, StreetItemType.STDPARTOFNAME)
            t.addAllAbridges(0, 0, 2)
            t.addAllAbridges(2, 5, 0)
            t.addAbridge("ГЛ." + s)
            t.addAbridge("ГЛАВ." + s)
            StreetItemToken.__m_ontology.add(t)
        for s in ["МАРШАЛА", "ГЕНЕРАЛА", "АДМІРАЛА", "КОСМОНАВТА", "ЛЬОТЧИКА", "АВІАКОНСТРУКТОРА", "АРХІТЕКТОРА", "СКУЛЬПТОРА", "ХУДОЖНИКА", "КОНСТРУКТОРА", "АКАДЕМІКА", "ПРОФЕСОРА", "ЛЕЙТЕНАНТА", "КАПІТАН", "МАЙОР", "ПІДПОЛКОВНИК", "ПОЛКОВНИК", "ПОЛІЦІЇ", "МІЛІЦІЇ"]: 
            StreetItemToken.__m_std_ont_misc.add(Termin(s))
            t = Termin._new119(s, StreetItemType.STDPARTOFNAME, MorphLang.UA)
            t.addAllAbridges(0, 0, 2)
            t.addAllAbridges(2, 5, 0)
            t.addAbridge("ГЛ." + s)
            t.addAbridge("ГЛАВ." + s)
            StreetItemToken.__m_ontology.add(t)
        t = Termin._new118("ВАСИЛЬЕВСКОГО ОСТРОВА", StreetItemType.STDNAME)
        t.addAbridge("В.О.")
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new118("ПЕТРОГРАДСКОЙ СТОРОНЫ", StreetItemType.STDNAME)
        t.addAbridge("П.С.")
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new118("ОЛИМПИЙСКАЯ ДЕРЕВНЯ", StreetItemType.FIX)
        t.addAbridge("ОЛИМП. ДЕРЕВНЯ")
        t.addAbridge("ОЛИМП. ДЕР.")
        StreetItemToken.__m_ontology.add(t)
        t = Termin._new118("ЛЕНИНСКИЕ ГОРЫ", StreetItemType.FIX)
        StreetItemToken.__m_ontology.add(t)
        obj = EpNerAddressInternalResourceHelper.getBytes("s.dat")
        if (obj is None): 
            raise Utils.newException("Can't file resource file s.dat in Location analyzer", None)
        streets = MiscLocationHelper._deflate(obj).decode("UTF-8", 'ignore')
        name = io.StringIO()
        names = dict()
        for line0 in Utils.splitString(streets, '\n', False): 
            line = line0.strip()
            if (Utils.isNullOrEmpty(line)): 
                continue
            if (line.find(';') >= 0): 
                parts = Utils.splitString(line, ';', False)
                t = Termin._new331(StreetItemType.NAME, True)
                t.initByNormalText(parts[0], MorphLang())
                j = 1
                while j < len(parts): 
                    t.addVariant(parts[j], True)
                    j += 1
            else: 
                t = Termin._new331(StreetItemType.NAME, True)
                t.initByNormalText(line, MorphLang())
            if (len(t.terms) > 1): 
                t.tag = StreetItemType.STDNAME
            StreetItemToken.__m_ontology.add(t)
    
    __m_ontology = None
    
    __m_std_ont_misc = None
    
    __m_prospect = None
    
    __m_metro = None
    
    @staticmethod
    def _new218(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'NumberToken') -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.number = _arg4
        return res
    
    @staticmethod
    def _new219(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'NumberToken', _arg5 : 'MorphCollection') -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.number = _arg4
        res.morph = _arg5
        return res
    
    @staticmethod
    def _new220(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'NumberToken', _arg5 : bool) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.number = _arg4
        res.number_has_prefix = _arg5
        return res
    
    @staticmethod
    def _new221(_arg1 : 'Token', _arg2 : 'Token', _arg3 : bool) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.has_std_suffix = _arg3
        return res
    
    @staticmethod
    def _new222(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Termin', _arg4 : 'StreetItemType', _arg5 : bool) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.termin = _arg3
        res.typ = _arg4
        res.is_abridge = _arg5
        return res
    
    @staticmethod
    def _new223(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'StreetReferent', _arg5 : 'MorphCollection', _arg6 : bool) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.exist_street = _arg4
        res.morph = _arg5
        res.is_in_dictionary = _arg6
        return res
    
    @staticmethod
    def _new224(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'NumberToken', _arg5 : bool, _arg6 : 'MorphCollection') -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.number = _arg4
        res.number_has_prefix = _arg5
        res.morph = _arg6
        return res
    
    @staticmethod
    def _new225(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'Termin', _arg5 : bool, _arg6 : 'MorphCollection') -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.termin = _arg4
        res.is_abridge = _arg5
        res.morph = _arg6
        return res
    
    @staticmethod
    def _new227(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'Termin', _arg5 : 'Termin', _arg6 : bool, _arg7 : 'MorphCollection', _arg8 : int) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.termin = _arg4
        res.alt_termin = _arg5
        res.is_abridge = _arg6
        res.morph = _arg7
        res.noun_is_doubt_coef = _arg8
        return res
    
    @staticmethod
    def _new228(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'MorphCollection', _arg5 : str) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.morph = _arg4
        res.value = _arg5
        return res
    
    @staticmethod
    def _new231(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'MorphCollection', _arg5 : 'Termin') -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.morph = _arg4
        res.termin = _arg5
        return res
    
    @staticmethod
    def _new232(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'MorphCollection', _arg5 : bool) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.morph = _arg4
        res.is_in_dictionary = _arg5
        return res
    
    @staticmethod
    def _new233(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'MorphCollection', _arg5 : bool, _arg6 : 'Termin') -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.morph = _arg4
        res.is_in_dictionary = _arg5
        res.termin = _arg6
        return res
    
    @staticmethod
    def _new234(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : bool, _arg5 : str, _arg6 : 'MorphCollection') -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.is_in_dictionary = _arg4
        res.value = _arg5
        res.morph = _arg6
        return res
    
    @staticmethod
    def _new235(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : str) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        return res
    
    @staticmethod
    def _new236(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType') -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new237(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'NumberToken', _arg5 : str) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.number = _arg4
        res.value = _arg5
        return res
    
    @staticmethod
    def _new238(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'MorphCollection') -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.morph = _arg4
        return res
    
    @staticmethod
    def _new240(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'MorphCollection', _arg5 : str) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.morph = _arg4
        res.alt_value = _arg5
        return res
    
    @staticmethod
    def _new249(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : str, _arg5 : str) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        res.alt_value = _arg5
        return res
    
    @staticmethod
    def _new254(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : str, _arg5 : bool) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        res.is_in_brackets = _arg5
        return res
    
    @staticmethod
    def _new257(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : bool) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.is_in_brackets = _arg4
        return res