# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing
from pullenti.unisharp.Utils import Utils

from pullenti.ner.uri.UriReferent import UriReferent
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.Token import Token
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.Referent import Referent
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.bank.internal.MetaBank import MetaBank
from pullenti.ner.bank.internal.PullentiNerBankInternalResourceHelper import PullentiNerBankInternalResourceHelper
from pullenti.ner.bank.BankDataReferent import BankDataReferent
from pullenti.ner.core.Termin import Termin
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.Analyzer import Analyzer

class BankAnalyzer(Analyzer):
    """ Анализатор банковских данных (счетов, платёжных реквизитов...) """
    
    ANALYZER_NAME = "BANKDATA"
    """ Имя анализатора ("BANKDATA") """
    
    @property
    def name(self) -> str:
        return BankAnalyzer.ANALYZER_NAME
    
    @property
    def caption(self) -> str:
        return "Банковские данные"
    
    @property
    def description(self) -> str:
        return "Банковские реквизиты, счета и пр."
    
    def clone(self) -> 'Analyzer':
        return BankAnalyzer()
    
    @property
    def progress_weight(self) -> int:
        return 1
    
    @property
    def type_system(self) -> typing.List['ReferentClass']:
        return [MetaBank._global_meta]
    
    @property
    def images(self) -> typing.List[tuple]:
        res = dict()
        res[MetaBank.IMAGE_ID] = PullentiNerBankInternalResourceHelper.get_bytes("dollar.png")
        return res
    
    def create_referent(self, type0_ : str) -> 'Referent':
        if (type0_ == BankDataReferent.OBJ_TYPENAME): 
            return BankDataReferent()
        return None
    
    @property
    def used_extern_object_types(self) -> typing.List[str]:
        return ["URI", "ORGANIZATION"]
    
    def process(self, kit : 'AnalysisKit') -> None:
        ad = kit.get_analyzer_data(self)
        t = kit.first_token
        while t is not None: 
            rt = None
            if (t.chars.is_letter): 
                tok = BankAnalyzer.__m_ontology.try_parse(t, TerminParseAttr.NO)
                if (tok is not None): 
                    tt = tok.end_token.next0_
                    if (tt is not None and tt.is_char(':')): 
                        tt = tt.next0_
                    rt = self.__try_attach(tt, True)
                    if (rt is not None): 
                        rt.begin_token = t
            if (rt is None and (((isinstance(t, ReferentToken)) or t.is_newline_before))): 
                rt = self.__try_attach(t, False)
            if (rt is not None): 
                rt.referent = ad.register_referent(rt.referent)
                kit.embed_token(rt)
                t = (rt)
            t = t.next0_
    
    @staticmethod
    def __is_bank_req(txt : str) -> bool:
        if (((((((txt == "Р/С" or txt == "К/С" or txt == "Л/С") or txt == "ОКФС" or txt == "ОКАТО") or txt == "ОГРН" or txt == "БИК") or txt == "SWIFT" or txt == "ОКПО") or txt == "ОКВЭД" or txt == "ОКОНХ") or txt == "КБК" or txt == "ИНН") or txt == "КПП"): 
            return True
        else: 
            return False
    
    def __try_attach(self, t : 'Token', key_word : bool) -> 'ReferentToken':
        if (t is None): 
            return None
        t0 = t
        t1 = t
        uris_keys = None
        uris = None
        org0_ = None
        cor_org = None
        org_is_bank = False
        empty = 0
        last_uri = None
        first_pass3510 = True
        while True:
            if first_pass3510: first_pass3510 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_table_control_char and t != t0): 
                break
            if (t.is_comma or t.morph.class0_.is_preposition or t.is_char_of("/\\")): 
                continue
            bank_keyword = False
            if (t.is_value("ПОЛНЫЙ", None) and t.next0_ is not None and ((t.next0_.is_value("НАИМЕНОВАНИЕ", None) or t.next0_.is_value("НАЗВАНИЕ", None)))): 
                t = t.next0_.next0_
                if (t is None): 
                    break
            if (t.is_value("БАНК", None)): 
                if ((isinstance(t, ReferentToken)) and t.get_referent().type_name == "ORGANIZATION"): 
                    bank_keyword = True
                tt = t.next0_
                npt = NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.NO, 0, None)
                if (npt is not None): 
                    tt = npt.end_token.next0_
                if (tt is not None and tt.is_char(':')): 
                    tt = tt.next0_
                if (tt is not None): 
                    if (not bank_keyword): 
                        t = tt
                        bank_keyword = True
                    elif (tt.get_referent() is not None and tt.get_referent().type_name == "ORGANIZATION"): 
                        t = tt
            r = t.get_referent()
            if (r is not None and r.type_name == "ORGANIZATION"): 
                is_bank = False
                kk = 0
                rr = r
                while rr is not None and (kk < 4): 
                    is_bank = Utils.compareStrings(Utils.ifNotNull(rr.get_string_value("KIND"), ""), "Bank", True) == 0
                    if (is_bank): 
                        break
                    rr = rr.parent_referent; kk += 1
                if (not is_bank and bank_keyword): 
                    is_bank = True
                if (not is_bank and uris is not None and "ИНН" in uris_keys): 
                    return None
                if ((last_uri is not None and last_uri.scheme == "К/С" and t.previous is not None) and t.previous.is_value("В", None)): 
                    cor_org = r
                    t1 = t
                elif (org0_ is None or ((not org_is_bank and is_bank))): 
                    org0_ = r
                    t1 = t
                    org_is_bank = is_bank
                    if (is_bank): 
                        continue
                if (uris is None and not key_word): 
                    return None
                continue
            if (isinstance(r, UriReferent)): 
                u = Utils.asObjectOrNull(r, UriReferent)
                if (uris is None): 
                    if (not BankAnalyzer.__is_bank_req(u.scheme)): 
                        return None
                    if (u.scheme == "ИНН" and t.is_newline_after): 
                        return None
                    uris = list()
                    uris_keys = list()
                else: 
                    if (not BankAnalyzer.__is_bank_req(u.scheme)): 
                        break
                    if (u.scheme in uris_keys): 
                        break
                    if (u.scheme == "ИНН"): 
                        if (empty > 0): 
                            break
                uris_keys.append(u.scheme)
                uris.append(u)
                last_uri = u
                t1 = t
                empty = 0
                continue
            elif (uris is None and not key_word and not org_is_bank): 
                return None
            if (r is not None and ((r.type_name == "GEO" or r.type_name == "ADDRESS"))): 
                empty += 1
                continue
            if (isinstance(t, TextToken)): 
                if (t.is_value("ПОЛНЫЙ", None) or t.is_value("НАИМЕНОВАНИЕ", None) or t.is_value("НАЗВАНИЕ", None)): 
                    pass
                elif (t.chars.is_letter): 
                    tok = BankAnalyzer.__m_ontology.try_parse(t, TerminParseAttr.NO)
                    if (tok is not None): 
                        t = tok.end_token
                        empty = 0
                    else: 
                        empty += 1
                        if (t.is_newline_before): 
                            nnn = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0, None)
                            if (nnn is not None and nnn.end_token.next0_ is not None and nnn.end_token.next0_.is_char(':')): 
                                break
                    if (uris is None): 
                        break
            if (empty > 2): 
                break
            if (empty > 0 and t.is_char(':') and t.is_newline_after): 
                break
            if (((isinstance(t, NumberToken)) and t.is_newline_before and t.next0_ is not None) and not t.next0_.chars.is_letter): 
                break
        if (uris is None): 
            return None
        if (not "Р/С" in uris_keys and not "Л/С" in uris_keys): 
            return None
        ok = False
        if ((len(uris) < 2) and org0_ is None): 
            return None
        bdr = BankDataReferent()
        for u in uris: 
            bdr.add_slot(BankDataReferent.ATTR_ITEM, u, False, 0)
        if (org0_ is not None): 
            bdr.add_slot(BankDataReferent.ATTR_BANK, org0_, False, 0)
        if (cor_org is not None): 
            bdr.add_slot(BankDataReferent.ATTR_CORBANK, cor_org, False, 0)
        org0 = (None if t0.previous is None else t0.previous.get_referent())
        if (org0 is not None and org0.type_name == "ORGANIZATION"): 
            for s in org0.slots: 
                if (isinstance(s.value, UriReferent)): 
                    u = Utils.asObjectOrNull(s.value, UriReferent)
                    if (BankAnalyzer.__is_bank_req(u.scheme)): 
                        if (not u.scheme in uris_keys): 
                            bdr.add_slot(BankDataReferent.ATTR_ITEM, u, False, 0)
        return ReferentToken(bdr, t0, t1)
    
    __m_ontology = None
    
    @staticmethod
    def initialize() -> None:
        if (BankAnalyzer.__m_ontology is not None): 
            return
        MetaBank.initialize()
        BankAnalyzer.__m_ontology = TerminCollection()
        t = Termin("БАНКОВСКИЕ РЕКВИЗИТЫ", None, True)
        t.add_variant("ПЛАТЕЖНЫЕ РЕКВИЗИТЫ", False)
        t.add_variant("РЕКВИЗИТЫ", False)
        BankAnalyzer.__m_ontology.add(t)
        ProcessorService.register_analyzer(BankAnalyzer())