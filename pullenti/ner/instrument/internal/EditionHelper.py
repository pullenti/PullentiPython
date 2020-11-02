# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.ner.Referent import Referent
from pullenti.ner.decree.DecreeReferent import DecreeReferent
from pullenti.ner.instrument.InstrumentKind import InstrumentKind
from pullenti.ner.decree.internal.PartToken import PartToken

class EditionHelper:
    """ Поддержка анализа редакций для фрагментов НПА """
    
    @staticmethod
    def analize_editions(root : 'FragToken') -> None:
        if (root.number == 6 and root.kind == InstrumentKind.SUBITEM): 
            pass
        if (root.sub_number == 67): 
            pass
        if (len(root.children) > 1 and root.children[0].kind == InstrumentKind.NUMBER and root.children[1].kind == InstrumentKind.CONTENT): 
            if (root.children[1].begin_token.is_value("УТРАТИТЬ", "ВТРАТИТИ") and root.children[1].begin_token.next0_ is not None and root.children[1].begin_token.next0_.is_value("СИЛА", "ЧИННІСТЬ")): 
                root.is_expired = True
        if ((not root.is_expired and root.kind == InstrumentKind.INDENTION and root.begin_token.is_value("АБЗАЦ", None)) and root.begin_token.next0_ is not None and root.begin_token.next0_.is_value("УТРАТИТЬ", "ВТРАТИТИ")): 
            root.is_expired = True
        if (root.is_expired or ((root._itok is not None and root._itok.is_expired))): 
            root.is_expired = True
            if (root.referents is None): 
                root.referents = list()
            tt = root.begin_token
            while tt is not None and tt.end_char <= root.end_char: 
                dec = Utils.asObjectOrNull(tt.get_referent(), DecreeReferent)
                if (dec is not None): 
                    if (not dec in root.referents): 
                        root.referents.append(dec)
                tt = tt.next0_
            return
        i0 = 0
        while i0 < len(root.children): 
            ch = root.children[i0]
            if (((ch.kind == InstrumentKind.COMMENT or ch.kind == InstrumentKind.KEYWORD or ch.kind == InstrumentKind.NUMBER) or ch.kind == InstrumentKind.NAME or ch.kind == InstrumentKind.CONTENT) or ch.kind == InstrumentKind.INDENTION): 
                pass
            else: 
                break
            i0 += 1
        if (root.number > 0): 
            edt1 = EditionHelper.__get_last_child(root)
            if (edt1 is not None and edt1.kind == InstrumentKind.EDITIONS and edt1.tag is None): 
                if (EditionHelper.__can_be_edition_for(root, edt1) > 0): 
                    if (root.referents is None): 
                        root.referents = edt1.referents
                    else: 
                        for r in edt1.referents: 
                            if (not r in root.referents): 
                                root.referents.append(r)
                    edt1.tag = (edt1)
        if (i0 >= len(root.children)): 
            for ch in root.children: 
                EditionHelper.analize_editions(ch)
            return
        ch0 = root.children[i0]
        ok = False
        if (EditionHelper.__can_be_edition_for(root, ch0) >= 0): 
            ok = True
            if (i0 > 0 and ((root.children[i0 - 1].kind == InstrumentKind.CONTENT or root.children[i0 - 1].kind == InstrumentKind.INDENTION)) and ((i0 + 1) < len(root.children))): 
                if (EditionHelper.__can_be_edition_for(root.children[i0 - 1], ch0) >= 0): 
                    ok = False
        if (((i0 + 1) < len(root.children)) and EditionHelper.__can_be_edition_for(root, root.children[len(root.children) - 1]) >= 0 and (EditionHelper.__can_be_edition_for(root.children[len(root.children) - 1], root.children[len(root.children) - 1]) < 0)): 
            ok = True
            ch0 = root.children[len(root.children) - 1]
        if (ok and ch0.tag is None): 
            if (root.referents is None): 
                root.referents = ch0.referents
            else: 
                for r in ch0.referents: 
                    if (not r in root.referents): 
                        root.referents.append(r)
            ch0.tag = (ch0)
        i = 0
        while i < len(root.children): 
            ch = root.children[i]
            edt = None
            edt2 = None
            if (ch.number > 0 and i > 0): 
                edt = EditionHelper.__get_last_child(root.children[i - 1])
            if (((i + 1) < len(root.children)) and root.children[i + 1].kind == InstrumentKind.EDITIONS): 
                edt2 = root.children[i + 1]
            if (edt is not None): 
                if (EditionHelper.__can_be_edition_for(ch, edt) < 1): 
                    edt = (None)
            if (edt2 is not None): 
                if (EditionHelper.__can_be_edition_for(ch, edt2) < 0): 
                    edt2 = (None)
            if (edt is not None and edt.tag is None): 
                if (ch.referents is None): 
                    ch.referents = edt.referents
                else: 
                    for r in edt.referents: 
                        if (not r in ch.referents): 
                            ch.referents.append(r)
                edt.tag = (ch)
            if (edt2 is not None and edt2.tag is None): 
                if (ch.referents is None): 
                    ch.referents = edt2.referents
                else: 
                    for r in edt2.referents: 
                        if (not r in ch.referents): 
                            ch.referents.append(r)
                edt2.tag = (ch)
            i += 1
        for ch in root.children: 
            EditionHelper.analize_editions(ch)
    
    @staticmethod
    def __get_last_child(fr : 'FragToken') -> 'FragToken':
        if (len(fr.children) == 0): 
            return fr
        return EditionHelper.__get_last_child(fr.children[len(fr.children) - 1])
    
    @staticmethod
    def __can_be_edition_for(fr : 'FragToken', edt : 'FragToken') -> int:
        if (edt is None or edt.kind != InstrumentKind.EDITIONS or edt.referents is None): 
            return -1
        if (fr.sub_number3 == 67): 
            pass
        t = edt.begin_token
        if (t.is_char('(') and t.next0_ is not None): 
            t = t.next0_
        if (t.is_value("АБЗАЦ", None)): 
            return (1 if fr.kind == InstrumentKind.INDENTION else -1)
        pt = PartToken.try_attach(t, None, False, False)
        if (pt is None): 
            pt = PartToken.try_attach(t, None, False, True)
        if (pt is None): 
            return 0
        if (pt.typ == PartToken.ItemType.CLAUSE): 
            if (fr.kind != InstrumentKind.CLAUSE): 
                return -1
        elif (pt.typ == PartToken.ItemType.PART): 
            if (fr.kind != InstrumentKind.CLAUSEPART and fr.kind != InstrumentKind.DOCPART and fr.kind != InstrumentKind.ITEM): 
                return -1
        elif (pt.typ == PartToken.ItemType.ITEM): 
            if (fr.kind != InstrumentKind.CLAUSEPART and fr.kind != InstrumentKind.ITEM and fr.kind != InstrumentKind.SUBITEM): 
                return -1
        elif (pt.typ == PartToken.ItemType.SUBITEM): 
            if (fr.kind != InstrumentKind.SUBITEM): 
                if (fr.kind == InstrumentKind.ITEM and t.is_value("ПП", None)): 
                    pass
                else: 
                    return -1
        elif (pt.typ == PartToken.ItemType.CHAPTER): 
            if (fr.kind != InstrumentKind.CHAPTER): 
                return -1
        elif (pt.typ == PartToken.ItemType.PARAGRAPH): 
            if (fr.kind != InstrumentKind.PARAGRAPH): 
                return -1
        elif (pt.typ == PartToken.ItemType.SUBPARAGRAPH): 
            if (fr.kind != InstrumentKind.SUBPARAGRAPH): 
                return -1
        if (len(pt.values) == 0): 
            return 0
        if (fr.number == 0): 
            return -1
        if (fr.number_string == pt.values[0].value): 
            return 1
        if (pt.values[0].value.endswith("." + fr.number_string)): 
            return 0
        if (fr.number == PartToken.get_number(pt.values[0].value)): 
            if (fr.sub_number == 0): 
                return 1
        return -1