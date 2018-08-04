# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import typing
from pullenti.ntopy.Utils import Utils
from pullenti.ner.Analyzer import Analyzer
from pullenti.ner.person.internal.ResourceHelper import ResourceHelper

from pullenti.ner.mail.MailKind import MailKind
from pullenti.ner.core.GetTextAttr import GetTextAttr


class MailAnalyzer(Analyzer):
    """ Семантический анализатор анализа писем (блоков писем) """
    
    ANALYZER_NAME = "MAIL"
    
    @property
    def name(self) -> str:
        return MailAnalyzer.ANALYZER_NAME
    
    @property
    def caption(self) -> str:
        return "Блок письма"
    
    @property
    def description(self) -> str:
        return "Блоки писем (e-mail) и их атрибуты"
    
    def clone(self) -> 'Analyzer':
        return MailAnalyzer()
    
    @property
    def type_system(self) -> typing.List['ReferentClass']:
        from pullenti.ner.mail.internal.MetaLetter import MetaLetter
        return [MetaLetter._global_meta]
    
    @property
    def images(self) -> typing.List[tuple]:
        from pullenti.ner.mail.internal.MetaLetter import MetaLetter
        res = dict()
        res[MetaLetter.IMAGE_ID] = ResourceHelper.get_bytes("mail.png")
        return res
    
    def create_referent(self, type0_ : str) -> 'Referent':
        from pullenti.ner.mail.MailReferent import MailReferent
        if (type0_ == MailReferent.OBJ_TYPENAME): 
            return MailReferent()
        return None
    
    @property
    def used_extern_object_types(self) -> typing.List[str]:
        return ["ORGANIZATION", "GEO", "ADDRESS", "PERSON"]
    
    @property
    def is_specific(self) -> bool:
        """ Этот анализатор является специфическим """
        return True
    
    @property
    def progress_weight(self) -> int:
        return 1
    
    def process(self, kit : 'AnalysisKit') -> None:
        from pullenti.ner.mail.internal.MailLine import MailLine
        from pullenti.ner.mail.MailReferent import MailReferent
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.person.PersonReferent import PersonReferent
        lines = list()
        t = kit.first_token
        first_pass2964 = True
        while True:
            if first_pass2964: first_pass2964 = False
            else: t = t.next0_
            if (not (t is not None)): break
            ml = MailLine.parse(t, 0)
            if (ml is None): 
                continue
            if (len(lines) == 91): 
                pass
            lines.append(ml)
            t = ml.end_token
        if (len(lines) == 0): 
            return
        blocks = list()
        blk = None
        i = 0
        first_pass2965 = True
        while True:
            if first_pass2965: first_pass2965 = False
            else: i += 1
            if (not (i < len(lines))): break
            ml = lines[i]
            if (ml.typ == MailLine.Types.FROM): 
                is_new = ml.must_be_first_line or i == 0
                if (((i + 2) < len(lines)) and (((lines[i + 1].typ == MailLine.Types.FROM or lines[i + 2].typ == MailLine.Types.FROM or lines[i + 1].typ == MailLine.Types.HELLO) or lines[i + 2].typ == MailLine.Types.HELLO))): 
                    is_new = True
                if (not is_new): 
                    for j in range(i - 1, -1, -1):
                        if (lines[j].typ != MailLine.Types.UNDEFINED): 
                            if (lines[j].typ == MailLine.Types.BESTREGARDS): 
                                is_new = True
                            break
                if (not is_new): 
                    tt = ml.begin_token
                    while tt is not None and tt.end_char <= ml.end_char: 
                        if (tt.get_referent() is not None): 
                            if (tt.get_referent().type_name == "DATE" or tt.get_referent().type_name == "URI"): 
                                is_new = True
                        tt = tt.next0_
                if (is_new): 
                    blk = list()
                    blocks.append(blk)
                    first_pass2966 = True
                    while True:
                        if first_pass2966: first_pass2966 = False
                        else: i += 1
                        if (not (i < len(lines))): break
                        if (lines[i].typ == MailLine.Types.FROM): 
                            if (len(blk) > 0 and lines[i].must_be_first_line): 
                                break
                            blk.append(lines[i])
                        elif (((i + 1) < len(lines)) and lines[i + 1].typ == MailLine.Types.FROM): 
                            for j in range(len(blk)):
                                if (blk[j].typ == MailLine.Types.FROM): 
                                    if (blk[j].is_real_from or blk[j].must_be_first_line or blk[j].mail_addr is not None): 
                                        break
                            else: j = len(blk)
                            if (j >= len(blk)): 
                                blk.append(lines[i])
                                continue
                            ok = False
                            for j in range(i + 1, len(lines), 1):
                                if (lines[j].typ != MailLine.Types.FROM): 
                                    break
                                if (lines[j].is_real_from or lines[j].must_be_first_line): 
                                    ok = True
                                    break
                                if (lines[j].mail_addr is not None): 
                                    ok = True
                                    break
                            else: j = len(lines)
                            if (ok): 
                                break
                            blk.append(lines[i])
                        else: 
                            break
                    i -= 1
                    continue
            if (blk is None): 
                blk = list()
                blocks.append(blk)
            blk.append(lines[i])
        if (len(blocks) == 0): 
            return
        ad = kit.get_analyzer_data(self)
        for j in range(len(blocks)):
            lines = blocks[j]
            if (len(lines) == 0): 
                continue
            i = 0
            if (lines[0].typ == MailLine.Types.FROM): 
                t1 = lines[0].end_token
                while i < len(lines): 
                    if (lines[i].typ == MailLine.Types.FROM): 
                        t1 = lines[i].end_token
                    elif (((i + 1) < len(lines)) and lines[i + 1].typ == MailLine.Types.FROM): 
                        pass
                    else: 
                        break
                    i += 1
                mail_ = MailReferent._new1497(MailKind.HEAD)
                mt = ReferentToken(mail_, lines[0].begin_token, t1)
                mail_.text = MiscHelper.get_text_value_of_meta_token(mt, GetTextAttr.KEEPREGISTER)
                ad.register_referent(mail_)
                mail_.add_occurence_of_ref_tok(mt)
            i0 = i
            t2 = None
            err = 0
            i = (len(lines) - 1)
            first_pass2967 = True
            while True:
                if first_pass2967: first_pass2967 = False
                else: i -= 1
                if (not (i >= i0)): break
                li = lines[i]
                if (li.typ == MailLine.Types.BESTREGARDS): 
                    t2 = lines[i].begin_token
                    -- i
                    while i >= i0: 
                        if (lines[i].typ == MailLine.Types.BESTREGARDS and (lines[i].words < 2)): 
                            t2 = lines[i].begin_token
                        elif ((i > i0 and (lines[i].words < 3) and lines[i - 1].typ == MailLine.Types.BESTREGARDS) and (lines[i - 1].words < 2)): 
                            i -= 1
                            t2 = lines[i].begin_token
                        else: 
                            break
                        i -= 1
                    break
                if (len(li.refs) > 0 and (li.words < 3) and i > i0): 
                    err = 0
                    t2 = li.begin_token
                    continue
                if (li.words > 10): 
                    t2 = None
                    continue
                if (li.words > 2): 
                    err += 1
                    if ((err) > 2): 
                        t2 = None
            if (t2 is None): 
                for i in range(len(lines) - 1, i0 - 1, -1):
                    li = lines[i]
                    if (li.typ == MailLine.Types.UNDEFINED): 
                        if (len(li.refs) > 0 and isinstance(li.refs[0], PersonReferent)): 
                            if (li.words == 0 and i > i0): 
                                t2 = li.begin_token
                                break
                else: i = i0 - 1
            for ii in range(i0, len(lines), 1):
                if (lines[ii].typ == MailLine.Types.HELLO): 
                    mail_ = MailReferent._new1497(MailKind.HELLO)
                    mt = ReferentToken(mail_, lines[i0].begin_token, lines[ii].end_token)
                    if (mt.length_char > 0): 
                        mail_.text = MiscHelper.get_text_value_of_meta_token(mt, GetTextAttr.KEEPREGISTER)
                        ad.register_referent(mail_)
                        mail_.add_occurence_of_ref_tok(mt)
                        i0 = (ii + 1)
                    break
                elif (lines[ii].typ != MailLine.Types.UNDEFINED or lines[ii].words > 0 or len(lines[ii].refs) > 0): 
                    break
            if (i0 < len(lines)): 
                if (t2 is not None and t2.previous is None): 
                    pass
                else: 
                    mail_ = MailReferent._new1497(MailKind.BODY)
                    mt = ReferentToken(mail_, lines[i0].begin_token, (t2.previous if t2 is not None and t2.previous is not None else lines[len(lines) - 1].end_token))
                    if (mt.length_char > 0): 
                        mail_.text = MiscHelper.get_text_value_of_meta_token(mt, GetTextAttr.KEEPREGISTER)
                        ad.register_referent(mail_)
                        mail_.add_occurence_of_ref_tok(mt)
                if (t2 is not None): 
                    mail_ = MailReferent._new1497(MailKind.TAIL)
                    mt = ReferentToken(mail_, t2, lines[len(lines) - 1].end_token)
                    if (mt.length_char > 0): 
                        mail_.text = MiscHelper.get_text_value_of_meta_token(mt, GetTextAttr.KEEPREGISTER)
                        ad.register_referent(mail_)
                        mail_.add_occurence_of_ref_tok(mt)
                    for i in range(i0, len(lines), 1):
                        if (lines[i].begin_char >= t2.begin_char): 
                            for r in lines[i].refs: 
                                mail_._add_ref(r, 0)
                    else: i = len(lines)
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.mail.internal.MailLine import MailLine
        from pullenti.ner.ProcessorService import ProcessorService
        try: 
            MailLine.initialize()
        except Exception as ex: 
            raise Utils.newException(ex.__str__(), ex)
        ProcessorService.register_analyzer(MailAnalyzer())