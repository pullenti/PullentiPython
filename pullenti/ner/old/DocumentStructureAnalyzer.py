# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import typing
import math
from pullenti.ntopy.Utils import Utils
from pullenti.ner.Analyzer import Analyzer
from pullenti.ner.booklink.internal.ResourceHelper import ResourceHelper

from pullenti.ner.old.DocumentBlockType import DocumentBlockType


class DocumentStructureAnalyzer(Analyzer):
    
    def __init__(self) -> None:
        from pullenti.ner.titlepage.TitlePageAnalyzer import TitlePageAnalyzer
        super().__init__()
        self.__m_title_page_analyzer = TitlePageAnalyzer()
    
    @property
    def name(self) -> str:
        return DocumentStructureAnalyzer.ANALYZER_NAME
    
    ANALYZER_NAME = "DOCSTRUCT"
    
    @property
    def caption(self) -> str:
        return "Структура документа"
    
    @property
    def description(self) -> str:
        return "Разбор структуры документа на разделы и подразделы"
    
    def clone(self) -> 'Analyzer':
        return DocumentStructureAnalyzer()
    
    @property
    def is_specific(self) -> bool:
        """ Этот анализатор является специфическим """
        return True
    
    @property
    def progress_weight(self) -> int:
        return 1
    
    @property
    def type_system(self) -> typing.List['ReferentClass']:
        from pullenti.ner.old.internal.MetaDocBlockInfo import MetaDocBlockInfo
        from pullenti.ner.old.internal.MetaDocument import MetaDocument
        return [MetaDocBlockInfo._global_meta, MetaDocument._global_meta]
    
    @property
    def images(self) -> typing.List['java.util.Map.Entry']:
        from pullenti.ner.old.internal.MetaDocBlockInfo import MetaDocBlockInfo
        from pullenti.ner.old.internal.MetaDocument import MetaDocument
        res = dict()
        res[MetaDocBlockInfo.BLOCK_IMAGE_ID] = ResourceHelper.get_bytes("block_text.png")
        res[MetaDocBlockInfo.DOC_IMAGE_ID] = ResourceHelper.get_bytes("block_doc.png")
        res[MetaDocBlockInfo.CHAPTER_IMAGE_ID] = ResourceHelper.get_bytes("block_parent.png")
        res[MetaDocument.DOC_IMAGE_ID] = ResourceHelper.get_bytes("block_doc.png")
        return res
    
    def create_referent(self, type0 : str) -> 'Referent':
        from pullenti.ner.old.DocumentBlockReferent import DocumentBlockReferent
        from pullenti.ner.old.DocumentReferent import DocumentReferent
        if (type0 == DocumentBlockReferent.OBJ_TYPENAME): 
            return DocumentBlockReferent()
        if (type0 == DocumentReferent.OBJ_TYPENAME): 
            return DocumentReferent()
        return None
    
    def process(self, kit : 'AnalysisKit') -> None:
        from pullenti.ner.old.internal.DocStructItem import DocStructItem
        from pullenti.ner.old.DocumentBlockReferent import DocumentBlockReferent
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.old.DocumentReferent import DocumentReferent
        from pullenti.ner.TextAnnotation import TextAnnotation
        ad = kit.get_analyzer_data(self)
        ogl = None
        items = list()
        last_token = None
        t = kit.first_token
        first_pass2810 = True
        while True:
            if first_pass2810: first_pass2810 = False
            else: t = t.next0
            if (not (t is not None)): break
            last_token = t
            ds = DocStructItem.try_attach(t, None, False)
            if (ds is None): 
                continue
            if (ds.typ == DocStructItem.Typs.INDEX): 
                if (ds.content_items is not None): 
                    ogl = ds
            else: 
                items.append(ds)
        tr = None
        tail = None
        if (ogl is not None): 
            if (ogl.begin_char < (math.floor(last_token.end_char / 3))): 
                if (ogl.begin_token.previous is not None): 
                    tr = self.__m_title_page_analyzer.process_referent1(kit.first_token, ogl.begin_token.previous)
                items.clear()
                t = ogl.end_token.next0
                first_pass2811 = True
                while True:
                    if first_pass2811: first_pass2811 = False
                    else: t = t.next0
                    if (not (t is not None)): break
                    if (not t.is_newline_before): 
                        continue
                    ds = DocStructItem.try_attach(t, ogl.content_items, False)
                    if (ds is not None and ds.typ != DocStructItem.Typs.INDEX): 
                        items.append(ds)
                        t = ds.end_token
            elif (ogl.end_char > (math.floor((last_token.end_char * 5) / 6))): 
                et = ogl.begin_token
                if (len(items) > 0 and (items[0].begin_char < et.begin_char)): 
                    et = items[0].begin_token
                if (ogl.begin_token.previous is not None): 
                    tr = self.__m_title_page_analyzer.process_referent1(kit.first_token, (et if et.previous is None else None))
                items.clear()
                t = kit.first_token
                while t is not None: 
                    if (t.end_char >= ogl.begin_char): 
                        break
                    ds = DocStructItem.try_attach(t, ogl.content_items, False)
                    if (ds is not None and ds.typ != DocStructItem.Typs.INDEX): 
                        items.append(ds)
                    t = t.next0
                if (ogl.end_token.next0 is not None and ((ogl.end_token.next0.begin_char + 10) < last_token.end_char)): 
                    ttt = kit.sofa.substring(ogl.end_token.next0.begin_char, (last_token.end_char - ogl.end_token.next0.begin_char) + 1).strip()
                    if (ttt is not None and len(ttt) > 10): 
                        bt = DocumentBlockReferent._new1478(DocumentBlockType.TAIL)
                        bt.add_slot(DocumentBlockReferent.ATTR_CONTENT, ttt, True, 0)
                        tail = ReferentToken(bt, ogl.end_token.next0, last_token)
                if (ogl.begin_token.previous is not None): 
                    last_token = ogl.begin_token.previous
            else: 
                pass
        if (len(items) == 0): 
            return
        res = (ad.register_referent(DocumentReferent()) if isinstance(ad.register_referent(DocumentReferent()), DocumentReferent) else None)
        if (tr is not None): 
            for sl in tr.referent.slots: 
                res.add_slot(sl.type_name, sl.value, False, 0)
        t0 = items[0].begin_token
        if (ogl is not None and (ogl.begin_char < t0.begin_char)): 
            t0 = ogl.begin_token
        if (t0.previous is not None and t0.previous.end_char > 20): 
            blk = DocumentBlockReferent()
            blk = (ad.register_referent(blk) if isinstance(ad.register_referent(blk), DocumentBlockReferent) else None)
            blk._add_parent(res)
            blk.add_slot(DocumentBlockReferent.ATTR_CONTENT, kit.sofa.substring(0, t0.previous.end_char + 1).strip(), True, 0)
            blk.typ = DocumentBlockType.TITLE
            blk.add_occurence(TextAnnotation(kit.first_token, t0.previous, blk))
        for i in range(len(items)):
            last = last_token
            if ((i + 1) < len(items)): 
                last = items[i + 1].begin_token.previous
            if (last is None): 
                break
            blk = DocumentBlockReferent()
            blk = (ad.register_referent(blk) if isinstance(ad.register_referent(blk), DocumentBlockReferent) else None)
            blk._add_parent(res)
            blk.add_slot(DocumentBlockReferent.ATTR_NAME, items[i].value, True, 0)
            blk.add_occurence(TextAnnotation(items[i].begin_token, items[i].end_token, blk))
            cou = (last.end_char - items[i].end_token.next0.begin_char) + 1
            txt = kit.sofa.substring(items[i].end_token.next0.begin_char, cou).strip()
            if (not Utils.isNullOrEmpty(txt) and len(txt) > 20): 
                cnt = DocumentBlockReferent()
                cnt = (ad.register_referent(cnt) if isinstance(ad.register_referent(cnt), DocumentBlockReferent) else None)
                cnt._add_parent(blk)
                cnt.add_slot(DocumentBlockReferent.ATTR_CONTENT, txt, True, 0)
                cnt.add_occurence(TextAnnotation(items[i].end_token.next0, last, cnt))
                swichVal = items[i].typ
                if (swichVal == DocStructItem.Typs.INTRO): 
                    cnt.typ = DocumentBlockType.INTRODUCTION
                elif (swichVal == DocStructItem.Typs.CONCLUSION): 
                    cnt.typ = DocumentBlockType.CONCLUSION
                elif (swichVal == DocStructItem.Typs.LITERATURE): 
                    cnt.typ = DocumentBlockType.LITERATURE
                elif (swichVal == DocStructItem.Typs.APPENDIX): 
                    cnt.typ = DocumentBlockType.APPENDIX
        if (tail is not None and isinstance(tail.referent, DocumentBlockReferent)): 
            tail.referent = ad.register_referent(tail.referent)
            (tail.referent if isinstance(tail.referent, DocumentBlockReferent) else None)._add_parent(res)