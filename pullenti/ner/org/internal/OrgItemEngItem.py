# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.org.OrganizationReferent import OrganizationReferent
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.Referent import Referent
from pullenti.ner.org.OrgProfile import OrgProfile
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.TextToken import TextToken
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.org.internal.OrgItemTypeToken import OrgItemTypeToken

class OrgItemEngItem(MetaToken):
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
        self.full_value = None;
        self.short_value = None;
    
    @property
    def is_bank(self) -> bool:
        return self.full_value == "bank"
    
    @staticmethod
    def try_attach(t : 'Token', can_be_cyr : bool=False) -> 'OrgItemEngItem':
        if (t is None or not (isinstance(t, TextToken))): 
            return None
        tok = (OrgItemEngItem.__m_ontology.try_parse(t, TerminParseAttr.NO) if can_be_cyr else None)
        if (not t.chars.is_latin_letter and tok is None): 
            if (not t.is_and or t.next0_ is None): 
                return None
            if (t.next0_.is_value("COMPANY", None) or t.next0_.is_value("CO", None)): 
                res = OrgItemEngItem(t, t.next0_)
                res.full_value = "company"
                if (res.end_token.next0_ is not None and res.end_token.next0_.is_char('.')): 
                    res.end_token = res.end_token.next0_
                return res
            return None
        if (t.chars.is_latin_letter): 
            tok = OrgItemEngItem.__m_ontology.try_parse(t, TerminParseAttr.NO)
        if (tok is not None): 
            if (not OrgItemEngItem.__check_tok(tok)): 
                return None
            res = OrgItemEngItem(tok.begin_token, tok.end_token)
            res.full_value = tok.termin.canonic_text.lower()
            res.short_value = tok.termin.acronym
            return res
        return None
    
    @staticmethod
    def __check_tok(tok : 'TerminToken') -> bool:
        if (tok.termin.acronym == "SA"): 
            tt0 = tok.begin_token.previous
            if (tt0 is not None and tt0.is_char('.')): 
                tt0 = tt0.previous
            if (isinstance(tt0, TextToken)): 
                if (tt0.term == "U"): 
                    return False
        elif (tok.begin_token.is_value("CO", None) and tok.begin_token == tok.end_token): 
            if (tok.end_token.next0_ is not None and tok.end_token.next0_.is_hiphen): 
                return False
        if (not tok.is_whitespace_after): 
            if (isinstance(tok.end_token.next0_, NumberToken)): 
                return False
        return True
    
    @staticmethod
    def try_attach_org(t : 'Token', can_be_cyr : bool=False) -> 'ReferentToken':
        from pullenti.ner.org.internal.OrgItemNameToken import OrgItemNameToken
        if (t is None): 
            return None
        br = False
        if (t.is_char('(') and t.next0_ is not None): 
            t = t.next0_
            br = True
        if (isinstance(t, NumberToken)): 
            if (t.typ == NumberSpellingType.WORDS and t.morph.class0_.is_adjective and t.chars.is_capital_upper): 
                pass
            else: 
                return None
        else: 
            if (t.chars.is_all_lower): 
                return None
            if ((t.length_char < 3) and not t.chars.is_letter): 
                return None
            if (not t.chars.is_latin_letter): 
                if (not can_be_cyr or not t.chars.is_cyrillic_letter): 
                    return None
        t0 = t
        t1 = t0
        nam_wo = 0
        tok = None
        geo_ = None
        add_typ = None
        first_pass3804 = True
        while True:
            if first_pass3804: first_pass3804 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t != t0 and t.whitespaces_before_count > 1): 
                break
            if (t.is_char(')')): 
                break
            if (t.is_char('(') and t.next0_ is not None): 
                if ((isinstance(t.next0_.get_referent(), GeoReferent)) and t.next0_.next0_ is not None and t.next0_.next0_.is_char(')')): 
                    geo_ = (Utils.asObjectOrNull(t.next0_.get_referent(), GeoReferent))
                    t = t.next0_.next0_
                    continue
                typ = OrgItemTypeToken.try_attach(t.next0_, True, None)
                if ((typ is not None and typ.end_token.next0_ is not None and typ.end_token.next0_.is_char(')')) and typ.chars.is_latin_letter): 
                    add_typ = typ
                    t = typ.end_token.next0_
                    continue
                if (((isinstance(t.next0_, TextToken)) and t.next0_.next0_ is not None and t.next0_.next0_.is_char(')')) and t.next0_.chars.is_capital_upper): 
                    t = t.next0_.next0_
                    t1 = t
                    continue
                break
            tok = OrgItemEngItem.try_attach(t, can_be_cyr)
            if (tok is None and t.is_char_of(".,") and t.next0_ is not None): 
                tok = OrgItemEngItem.try_attach(t.next0_, can_be_cyr)
                if (tok is None and t.next0_.is_char_of(",.")): 
                    tok = OrgItemEngItem.try_attach(t.next0_.next0_, can_be_cyr)
            if (tok is not None): 
                if (tok.length_char == 1 and t0.chars.is_cyrillic_letter): 
                    return None
                break
            if (t.is_hiphen and not t.is_whitespace_after and not t.is_whitespace_before): 
                continue
            if (t.is_char_of("&+") or t.is_and): 
                continue
            if (t.is_char('.')): 
                if (t.previous is not None and t.previous.length_char == 1): 
                    continue
                elif (MiscHelper.can_be_start_of_sentence(t.next0_)): 
                    break
            if (not t.chars.is_latin_letter): 
                if (not can_be_cyr or not t.chars.is_cyrillic_letter): 
                    break
            if (t.chars.is_all_lower): 
                if (t.morph.class0_.is_preposition or t.morph.class0_.is_conjunction): 
                    continue
                if (br): 
                    continue
                break
            mc = t.get_morph_class_in_dictionary()
            if (mc.is_verb): 
                if (t.next0_ is not None and t.next0_.morph.class0_.is_preposition): 
                    break
            if (t.next0_ is not None and t.next0_.is_value("OF", None)): 
                break
            if (isinstance(t, TextToken)): 
                nam_wo += 1
            t1 = t
        if (tok is None): 
            return None
        if (t0 == tok.begin_token): 
            br2 = BracketHelper.try_parse(tok.end_token.next0_, BracketParseAttr.NO, 100)
            if (br2 is not None): 
                org1 = OrganizationReferent()
                if (tok.short_value is not None): 
                    org1.add_type_str(tok.short_value)
                org1.add_type_str(tok.full_value)
                nam1 = MiscHelper.get_text_value(br2.begin_token, br2.end_token, GetTextAttr.NO)
                if (nam1 is not None): 
                    org1.add_name(nam1, True, None)
                    return ReferentToken(org1, t0, br2.end_token)
            return None
        org0_ = OrganizationReferent()
        te = tok.end_token
        if (tok.is_bank): 
            t1 = tok.end_token
        if (tok.full_value == "company" and (tok.whitespaces_after_count < 3)): 
            tok1 = OrgItemEngItem.try_attach(tok.end_token.next0_, can_be_cyr)
            if (tok1 is not None): 
                t1 = tok.end_token
                tok = tok1
                te = tok.end_token
        if (tok.full_value == "company"): 
            if (nam_wo == 0): 
                return None
        nam = MiscHelper.get_text_value(t0, t1, GetTextAttr.IGNOREARTICLES)
        if (nam == "STOCK" and tok.full_value == "company"): 
            return None
        alt_nam = None
        if (Utils.isNullOrEmpty(nam)): 
            return None
        if (nam.find('(') > 0): 
            i1 = nam.find('(')
            i2 = nam.find(')')
            if (i1 < i2): 
                alt_nam = nam
                tai = None
                if ((i2 + 1) < len(nam)): 
                    tai = nam[i2:].strip()
                nam = nam[0:0+i1].strip()
                if (tai is not None): 
                    nam = "{0} {1}".format(nam, tai)
        if (tok.is_bank): 
            org0_.add_type_str(("bank" if tok.kit.base_language.is_en else "банк"))
            org0_.add_profile(OrgProfile.FINANCE)
            if ((t1.next0_ is not None and t1.next0_.is_value("OF", None) and t1.next0_.next0_ is not None) and t1.next0_.next0_.chars.is_latin_letter): 
                nam0 = OrgItemNameToken.try_attach(t1.next0_, None, False, False)
                if (nam0 is not None): 
                    te = nam0.end_token
                else: 
                    te = t1.next0_.next0_
                nam = MiscHelper.get_text_value(t0, te, GetTextAttr.NO)
                if (isinstance(te.get_referent(), GeoReferent)): 
                    org0_._add_geo_object(Utils.asObjectOrNull(te.get_referent(), GeoReferent))
            elif (t0 == t1): 
                return None
        else: 
            if (tok.short_value is not None): 
                org0_.add_type_str(tok.short_value)
            org0_.add_type_str(tok.full_value)
        if (Utils.isNullOrEmpty(nam)): 
            return None
        org0_.add_name(nam, True, None)
        if (alt_nam is not None): 
            org0_.add_name(alt_nam, True, None)
        res = ReferentToken(org0_, t0, te)
        t = te
        while t.next0_ is not None:
            if (t.next0_.is_char_of(",.")): 
                t = t.next0_
            else: 
                break
        if (t.whitespaces_after_count < 2): 
            tok = OrgItemEngItem.try_attach(t.next0_, can_be_cyr)
            if (tok is not None): 
                if (tok.short_value is not None): 
                    org0_.add_type_str(tok.short_value)
                org0_.add_type_str(tok.full_value)
                res.end_token = tok.end_token
        if (geo_ is not None): 
            org0_._add_geo_object(geo_)
        if (add_typ is not None): 
            org0_.add_type(add_typ, False)
        if (not br): 
            return res
        t = res.end_token
        if (t.next0_ is None or t.next0_.is_char(')')): 
            res.end_token = t.next0_
        else: 
            return None
        return res
    
    @staticmethod
    def initialize() -> None:
        if (OrgItemEngItem.__m_ontology is not None): 
            return
        OrgItemEngItem.__m_ontology = TerminCollection()
        t = Termin("BANK")
        OrgItemEngItem.__m_ontology.add(t)
        t = Termin._new95("Public Limited Company".upper(), "PLC")
        t.add_abridge("P.L.C.")
        OrgItemEngItem.__m_ontology.add(t)
        t = Termin._new95("Limited Liability Company".upper(), "LLC")
        t.add_abridge("L.L.C.")
        OrgItemEngItem.__m_ontology.add(t)
        t = Termin._new95("Limited Liability Partnership".upper(), "LLP")
        t.add_abridge("L.L.P.")
        OrgItemEngItem.__m_ontology.add(t)
        t = Termin._new95("Limited Liability Limited Partnership".upper(), "LLLP")
        t.add_abridge("L.L.L.P.")
        OrgItemEngItem.__m_ontology.add(t)
        t = Termin._new95("Limited Duration Company".upper(), "LDC")
        t.add_abridge("L.D.C.")
        OrgItemEngItem.__m_ontology.add(t)
        t = Termin._new95("International Business Company".upper(), "IBC")
        t.add_abridge("I.B.S.")
        OrgItemEngItem.__m_ontology.add(t)
        t = Termin._new95("Joint stock company".upper(), "JSC")
        t.add_abridge("J.S.C.")
        OrgItemEngItem.__m_ontology.add(t)
        t = Termin._new95("Open Joint stock company".upper(), "OJSC")
        t.add_abridge("O.J.S.C.")
        OrgItemEngItem.__m_ontology.add(t)
        t = Termin._new95("Sosiedad Anonima".upper(), "SA")
        t.add_variant("Sociedad Anonima".upper(), False)
        t.add_abridge("S.A.")
        t.add_variant("SPA", False)
        OrgItemEngItem.__m_ontology.add(t)
        t = Termin._new95("Société en commandite".upper(), "SC")
        t.add_abridge("S.C.")
        t.add_variant("SCS", False)
        OrgItemEngItem.__m_ontology.add(t)
        t = Termin._new95("Societas Europaea".upper(), "SE")
        t.add_abridge("S.E.")
        OrgItemEngItem.__m_ontology.add(t)
        t = Termin._new95("Società in accomandita".upper(), "SAS")
        OrgItemEngItem.__m_ontology.add(t)
        t = Termin._new95("Société en commandite par actions".upper(), "SCA")
        t.add_abridge("S.C.A.")
        OrgItemEngItem.__m_ontology.add(t)
        t = Termin._new95("Société en nom collectif".upper(), "SNC")
        t.add_variant("Società in nome collettivo".upper(), False)
        t.add_abridge("S.N.C.")
        OrgItemEngItem.__m_ontology.add(t)
        t = Termin._new95("General Partnership".upper(), "GP")
        t.add_variant("General Partners", False)
        t.add_abridge("G.P.")
        OrgItemEngItem.__m_ontology.add(t)
        t = Termin._new95("Limited Partnership".upper(), "LP")
        t.add_abridge("L.P.")
        OrgItemEngItem.__m_ontology.add(t)
        t = Termin._new95("Kommanditaktiengesellschaft".upper(), "KGAA")
        t.add_variant("KOMMAG", False)
        OrgItemEngItem.__m_ontology.add(t)
        t = Termin._new95("Societe a Responsidilite Limitee".upper(), "SRL")
        t.add_abridge("S.A.R.L.")
        t.add_abridge("S.R.L.")
        t.add_variant("SARL", False)
        OrgItemEngItem.__m_ontology.add(t)
        t = Termin._new95("Società a garanzia limitata".upper(), "SAGL")
        t.add_abridge("S.A.G.L.")
        OrgItemEngItem.__m_ontology.add(t)
        t = Termin._new95("Società limitata".upper(), "SL")
        t.add_abridge("S.L.")
        OrgItemEngItem.__m_ontology.add(t)
        t = Termin._new95("Vennootschap Met Beperkte Aansparkelij kheid".upper(), "BV")
        OrgItemEngItem.__m_ontology.add(t)
        t = Termin._new95("Vennootschap Met Beperkte Aansparkelij".upper(), "AVV")
        OrgItemEngItem.__m_ontology.add(t)
        t = Termin._new95("Naamlose Vennootschap".upper(), "NV")
        t.add_abridge("N.V.")
        OrgItemEngItem.__m_ontology.add(t)
        t = Termin._new95("Gesellschaft mit beschrakter Haftung".upper(), "GMBH")
        t.add_variant("ГМБХ", False)
        OrgItemEngItem.__m_ontology.add(t)
        t = Termin._new95("Aktiengesellschaft".upper(), "AG")
        OrgItemEngItem.__m_ontology.add(t)
        t = Termin._new95("International Company".upper(), "IC")
        t.add_abridge("I.C.")
        OrgItemEngItem.__m_ontology.add(t)
        t = Termin("And Company".upper())
        t.add_variant("& Company", False)
        t.add_variant("& Co", False)
        t.add_variant("& Company", False)
        OrgItemEngItem.__m_ontology.add(t)
        t = Termin._new95("Kollektivgesellschaft".upper(), "KG")
        t.add_abridge("K.G.")
        t.add_variant("OHG", False)
        OrgItemEngItem.__m_ontology.add(t)
        t = Termin._new95("Kommanditgesellschaft".upper(), "KG")
        t.add_variant("KOMMG", False)
        OrgItemEngItem.__m_ontology.add(t)
        t = Termin("LIMITED")
        t.add_abridge("LTD")
        t.add_variant("LTD", False)
        t.add_variant("ЛИМИТЕД", False)
        t.add_variant("ЛТД", False)
        OrgItemEngItem.__m_ontology.add(t)
        t = Termin("PRIVATE LIMITED")
        t.add_variant("PTE LTD", False)
        OrgItemEngItem.__m_ontology.add(t)
        t = Termin("INCORPORATED")
        t.add_abridge("INC")
        t.add_variant("INC", False)
        t.add_variant("ИНКОРПОРЕЙТЕД", False)
        t.add_variant("ИНК", False)
        OrgItemEngItem.__m_ontology.add(t)
        t = Termin("CORPORATION")
        t.add_variant("CO", False)
        t.add_variant("СО", False)
        t.add_variant("КОРПОРЕЙШН", False)
        t.add_variant("КОРПОРЕЙШЕН", False)
        OrgItemEngItem.__m_ontology.add(t)
        t = Termin("COMPANY")
        OrgItemEngItem.__m_ontology.add(t)
    
    __m_ontology = None