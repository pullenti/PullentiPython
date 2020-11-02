# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import threading
import typing
import datetime
import math
import xml.etree
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Misc import EventHandler
from pullenti.unisharp.Misc import ProgressEventArgs
from pullenti.unisharp.Misc import CancelEventArgs
from pullenti.unisharp.Misc import Stopwatch

from pullenti.ner.core.internal.ProgressPeace import ProgressPeace
from pullenti.ner.ProxyReferent import ProxyReferent
from pullenti.ner.core.internal.GeneralRelationHelper import GeneralRelationHelper
from pullenti.ner.AnalysisResult import AnalysisResult
from pullenti.ner.core.AnalysisKit import AnalysisKit

class Processor(object):
    """ Лингвистический процессор
    
    Процессор
    """
    
    class ProgressChangedEventHandler_OnProgressHandler(EventHandler):
        
        def __init__(self, src : 'Processor') -> None:
            super().__init__()
            self.__m_source = None;
            self.__m_source = src
        
        def call(self, sender : object, e0_ : ProgressEventArgs) -> None:
            self.__m_source._on_progress_handler(sender, e0_)
    
    class CancelEventHandler_OnCancel(EventHandler):
        
        def __init__(self, src : 'Processor') -> None:
            super().__init__()
            self.__m_source = None;
            self.__m_source = src
        
        def call(self, sender : object, e0_ : CancelEventArgs) -> None:
            self.__m_source._on_cancel(sender, e0_)
    
    def __init__(self) -> None:
        self.__m_analyzers = list()
        self.__m_analyzers_hash = dict()
        self.progress = list()
        self.__m_progress_peaces = dict()
        self.__m_progress_peaces_lock = threading.Lock()
        self.__m_breaked = False
        self.timeout_seconds = 0
        self.__last_percent = 0
        self.__m_links = None
        self.__m_links2 = None
        self.__m_refs = None
        self.tag = None;
        self.__progress_changed_event_handler_on_progress_handler = Processor.ProgressChangedEventHandler_OnProgressHandler(self)
        self.__cancel_event_handler_on_cancel = Processor.CancelEventHandler_OnCancel(self)
    
    def add_analyzer(self, a : 'Analyzer') -> None:
        """ Добавить анализатор, если его ещё нет
        
        Args:
            a(Analyzer): экземпляр анализатора
        """
        if (a is None or a.name is None or a.name in self.__m_analyzers_hash): 
            return
        self.__m_analyzers_hash[a.name] = a
        self.__m_analyzers.append(a)
        a._progress.append(self.__progress_changed_event_handler_on_progress_handler)
        a._cancel.append(self.__cancel_event_handler_on_cancel)
    
    def del_analyzer(self, a : 'Analyzer') -> None:
        """ Удалить анализатор
        
        Args:
            a(Analyzer): 
        """
        if (not a.name in self.__m_analyzers_hash): 
            return
        del self.__m_analyzers_hash[a.name]
        self.__m_analyzers.remove(a)
        a._progress.remove(self.__progress_changed_event_handler_on_progress_handler)
        a._cancel.remove(self.__cancel_event_handler_on_cancel)
    
    def close(self) -> None:
        for w in self.analyzers: 
            w._progress.remove(self.__progress_changed_event_handler_on_progress_handler)
            w._cancel.remove(self.__cancel_event_handler_on_cancel)
    
    @property
    def analyzers(self) -> typing.List['Analyzer']:
        """ Последовательность обработки данных (анализаторы) """
        return self.__m_analyzers
    
    def find_analyzer(self, name : str) -> 'Analyzer':
        """ Найти анализатор по его имени
        
        Args:
            name(str): 
        
        """
        wrapa2834 = RefOutArgWrapper(None)
        inoutres2835 = Utils.tryGetValue(self.__m_analyzers_hash, Utils.ifNotNull(name, ""), wrapa2834)
        a = wrapa2834.value
        if (not inoutres2835): 
            return None
        else: 
            return a
    
    def process(self, text : 'SourceOfAnalysis', ext_ontology : 'ExtOntology'=None, lang : 'MorphLang'=None) -> 'AnalysisResult':
        """ Обработать текст
        
        Args:
            text(SourceOfAnalysis): входной контейнер текста
            ext_ontology(ExtOntology): внешняя онтология (null - не используется)
            lang(MorphLang): язык (если не задан, то будет определён автоматически)
        
        Returns:
            AnalysisResult: аналитический контейнер с результатом
        
        """
        return self._process(text, False, False, ext_ontology, lang)
    
    def process_next(self, ar : 'AnalysisResult') -> None:
        """ Доделать результат, который был сделан другим процессором
        
        Args:
            ar(AnalysisResult): то, что было сделано другим процессором
        """
        if (ar is None): 
            return
        kit = AnalysisKit._new2836(self, ar.ontology)
        kit._init_from(ar)
        self.__process2(kit, ar, False)
        self._create_res(kit, ar, ar.ontology, False)
        ar.first_token = kit.first_token
    
    def _process(self, text : 'SourceOfAnalysis', onto_regine : bool, no_log : bool, ext_ontology : 'ExtOntology'=None, lang : 'MorphLang'=None) -> 'AnalysisResult':
        self.__m_breaked = False
        self.__prepare_progress()
        sw0 = Stopwatch()
        self.manage_referent_links()
        if (not no_log): 
            self._on_progress_handler(self, ProgressEventArgs(0, "Морфологический анализ"))
        kit = AnalysisKit._new2837(text, False, lang, self.__progress_changed_event_handler_on_progress_handler, ext_ontology, self, onto_regine)
        ar = AnalysisResult()
        sw0.stop()
        self._on_progress_handler(self, ProgressEventArgs(100, "Морфологический анализ завершён"))
        k = 0
        t = kit.first_token
        while t is not None: 
            k += 1
            t = t.next0_
        if (not no_log): 
            msg = "Из {0} символов текста выделено {1} термов за {2} ms".format(len(text.text), k, sw0.elapsedMilliseconds)
            if (not kit.base_language.is_undefined): 
                msg += ", базовый язык {0}".format(str(kit.base_language))
            self.__on_message(msg)
            ar.log0_.append(msg)
            if (text.crlf_corrected_count > 0): 
                ar.log0_.append("{0} переходов на новую строку заменены на пробел".format(text.crlf_corrected_count))
            if (kit.first_token is None): 
                ar.log0_.append("Пустой текст")
        sw0.start()
        if (kit.first_token is not None): 
            self.__process2(kit, ar, no_log)
        if (not onto_regine): 
            self._create_res(kit, ar, ext_ontology, no_log)
        sw0.stop()
        if (not no_log): 
            if (sw0.elapsedMilliseconds > (5000)): 
                f = len(text.text)
                f /= (sw0.elapsedMilliseconds)
                msg = "Обработка {0} знаков выполнена за {1} ({2} Kb/sec)".format(len(text.text), Processor.__out_secs(sw0.elapsedMilliseconds), f)
            else: 
                msg = "Обработка {0} знаков выполнена за {1}".format(len(text.text), Processor.__out_secs(sw0.elapsedMilliseconds))
            self.__on_message(msg)
            ar.log0_.append(msg)
        if (self.timeout_seconds > 0): 
            if (int((datetime.datetime.now() - kit._start_date).total_seconds()) > self.timeout_seconds): 
                ar.is_timeout_breaked = True
        ar.sofa = text
        if (not onto_regine): 
            ar.entities.extend(kit.entities)
        ar.first_token = kit.first_token
        ar.ontology = ext_ontology
        ar.base_language = kit.base_language
        return ar
    
    def __process2(self, kit : 'AnalysisKit', ar : 'AnalysisResult', no_log : bool) -> None:
        sw = Stopwatch()
        stop_by_timeout = False
        anals = list(self.__m_analyzers)
        ii = 0
        first_pass3926 = True
        while True:
            if first_pass3926: first_pass3926 = False
            else: ii += 1
            if (not (ii < len(anals))): break
            c = anals[ii]
            if (c.ignore_this_analyzer): 
                continue
            if (self.__m_breaked): 
                if (not no_log): 
                    msg = "Процесс прерван пользователем"
                    self.__on_message(msg)
                    ar.log0_.append(msg)
                break
            if (self.timeout_seconds > 0 and not stop_by_timeout): 
                if (int((datetime.datetime.now() - kit._start_date).total_seconds()) > self.timeout_seconds): 
                    self.__m_breaked = True
                    if (not no_log): 
                        msg = "Процесс прерван по таймауту"
                        self.__on_message(msg)
                        ar.log0_.append(msg)
                    stop_by_timeout = True
            if (stop_by_timeout): 
                if (c.name == "INSTRUMENT"): 
                    pass
                else: 
                    continue
            if (not no_log): 
                self._on_progress_handler(c, ProgressEventArgs(0, "Работа \"{0}\"".format(c.caption)))
            sw.reset()
            sw.start()
            c.process(kit)
            sw.stop()
            dat = kit.get_analyzer_data(c)
            if (not no_log): 
                msg = "Анализатор \"{0}\" выделил {1} объект(ов) за {2}".format(c.caption, (0 if dat is None else len(dat.referents)), Processor.__out_secs(sw.elapsedMilliseconds))
                self.__on_message(msg)
                ar.log0_.append(msg)
        if (not no_log): 
            self._on_progress_handler(None, ProgressEventArgs(0, "Пересчёт отношений обобщения"))
        try: 
            sw.reset()
            sw.start()
            GeneralRelationHelper.refresh_generals(self, kit)
            sw.stop()
            if (not no_log): 
                msg = "Отношение обобщение пересчитано за {0}".format(Processor.__out_secs(sw.elapsedMilliseconds))
                self.__on_message(msg)
                ar.log0_.append(msg)
        except Exception as ex: 
            if (not no_log): 
                ex = Utils.newException("Ошибка пересчёта отношения обобщения", ex)
                self.__on_message(ex)
                ar._add_exception(ex)
    
    def _create_res(self, kit : 'AnalysisKit', ar : 'AnalysisResult', ext_ontology : 'ExtOntology', no_log : bool) -> None:
        sw = Stopwatch()
        onto_attached = 0
        for k in range(2):
            for c in self.analyzers: 
                if (k == 0): 
                    if (not c.is_specific): 
                        continue
                elif (c.is_specific): 
                    continue
                dat = kit.get_analyzer_data(c)
                if (dat is not None and len(dat.referents) > 0): 
                    if (ext_ontology is not None): 
                        for r in dat.referents: 
                            if (r.ontology_items is None): 
                                r.ontology_items = ext_ontology.attach_referent(r)
                                if ((r.ontology_items) is not None): 
                                    onto_attached += 1
                    ar.entities.extend(dat.referents)
        sw.stop()
        if (ext_ontology is not None and not no_log): 
            msg = "Привязано {0} объектов к внешней отнологии ({1} элементов) за {2}".format(onto_attached, len(ext_ontology.items), Processor.__out_secs(sw.elapsedMilliseconds))
            self.__on_message(msg)
            ar.log0_.append(msg)
    
    @staticmethod
    def __out_secs(ms : int) -> str:
        if (ms < (4000)): 
            return "{0}ms".format(ms)
        ms = math.floor(ms / (1000))
        if (ms < (120)): 
            return "{0}sec".format(ms)
        return "{0}min {1}sec".format(math.floor(ms / (60)), ms % (60))
    
    def break_process(self) -> None:
        """ Прервать процесс анализа """
        self.__m_breaked = True
    
    MORPH_COEF = 10
    
    def __prepare_progress(self) -> None:
        with self.__m_progress_peaces_lock: 
            self.__last_percent = -1
            co = Processor.MORPH_COEF
            total = co
            for wf in self.analyzers: 
                total += (wf.progress_weight if wf.progress_weight > 0 else 1)
            self.__m_progress_peaces.clear()
            max0_ = co * 100
            max0_ /= (total)
            self.__m_progress_peaces[self] = ProgressPeace._new2838(0, max0_)
            for wf in self.analyzers: 
                min0_ = max0_
                co += (wf.progress_weight if wf.progress_weight > 0 else 1)
                max0_ = (co * 100)
                max0_ /= (total)
                if (not wf in self.__m_progress_peaces): 
                    self.__m_progress_peaces[wf] = ProgressPeace._new2838(min0_, max0_)
    
    def _on_progress_handler(self, sender : object, e0_ : ProgressEventArgs) -> None:
        if (len(self.progress) == 0): 
            return
        if (e0_.progressPercentage >= 0): 
            with self.__m_progress_peaces_lock: 
                wrappi2840 = RefOutArgWrapper(None)
                inoutres2841 = Utils.tryGetValue(self.__m_progress_peaces, Utils.ifNotNull(sender, self), wrappi2840)
                pi0_ = wrappi2840.value
                if (inoutres2841): 
                    p = ((e0_.progressPercentage) * ((pi0_.max0_ - pi0_.min0_))) / (100)
                    p += pi0_.min0_
                    pers = math.floor(p)
                    if (pers == self.__last_percent and e0_.userState is None and not self.__m_breaked): 
                        return
                    e0_ = ProgressEventArgs(math.floor(p), e0_.userState)
                    self.__last_percent = pers
        for iiid in range(len(self.progress)): self.progress[iiid].call(self, e0_)
    
    def _on_cancel(self, sender : object, e0_ : CancelEventArgs) -> None:
        if (self.timeout_seconds > 0): 
            if (isinstance(sender, AnalysisKit)): 
                if (int((datetime.datetime.now() - sender._start_date).total_seconds()) > self.timeout_seconds): 
                    self.__m_breaked = True
        e0_.cancel = self.__m_breaked
    
    def __on_message(self, message : object) -> None:
        if (len(self.progress) > 0): 
            for iiid in range(len(self.progress)): self.progress[iiid].call(self, ProgressEventArgs(-1, message))
    
    def manage_referent_links(self) -> None:
        if (self.__m_refs is not None): 
            for pr in self.__m_refs: 
                wrapr2844 = RefOutArgWrapper(None)
                inoutres2845 = Utils.tryGetValue(self.__m_links2, pr.identity, wrapr2844)
                r = wrapr2844.value
                if (pr.identity is not None and self.__m_links2 is not None and inoutres2845): 
                    pr.owner_referent.upload_slot(pr.owner_slot, r)
                else: 
                    wrapr2842 = RefOutArgWrapper(None)
                    inoutres2843 = Utils.tryGetValue(self.__m_links, pr.value, wrapr2842)
                    r = wrapr2842.value
                    if (self.__m_links is not None and inoutres2843): 
                        pr.owner_referent.upload_slot(pr.owner_slot, r)
                    else: 
                        pass
        self.__m_links2 = None
        self.__m_links = self.__m_links2
        self.__m_refs = (None)
    
    def deserialize_referent(self, data : str, identity : str=None, create_links1 : bool=True) -> 'Referent':
        """ Десериализация сущности из строки
        
        Args:
            data(str): результат сериализации, см. Referent.Serialize()
            identity(str): для внутреннего использования (д.б. null)
        
        Returns:
            Referent: сущность
        """
        try: 
            xml0_ = None # new XmlDocument
            xml0_ = Utils.parseXmlFromString(data)
            return self.deserialize_referent_from_xml(xml0_.getroot(), identity, create_links1)
        except Exception as ex: 
            return None
    
    def deserialize_referent_from_xml(self, xml0_ : xml.etree.ElementTree.Element, identity : str=None, create_links1 : bool=True) -> 'Referent':
        """ Десериализация сущности из узла XML
        
        Args:
            xml0_(xml.etree.ElementTree.Element): 
            identity(str): для внутреннего использования (д.б. null)
        
        Returns:
            Referent: сущность
        """
        try: 
            res = None
            for a in self.analyzers: 
                res = a.create_referent(xml0_.tag)
                if ((res) is not None): 
                    break
            if (res is None): 
                return None
            for x in xml0_: 
                if (x.tag == "#text"): 
                    continue
                nam = x.tag
                if (nam.startswith("ATCOM_")): 
                    nam = ("@" + nam[6:])
                att = Utils.getXmlAttrByName(x.attrib, "ref")
                slot = None
                if (att is not None and att[1] == "true"): 
                    pr = ProxyReferent._new2846(Utils.getXmlInnerText(x), res)
                    pr.owner_slot = res.add_slot(nam, pr, False, 0)
                    slot = pr.owner_slot
                    att = Utils.getXmlAttrByName(x.attrib, "id")
                    if ((att) is not None): 
                        pr.identity = att[1]
                    if (self.__m_refs is None): 
                        self.__m_refs = list()
                    self.__m_refs.append(pr)
                else: 
                    slot = res.add_slot(nam, Utils.getXmlInnerText(x), False, 0)
                att = Utils.getXmlAttrByName(x.attrib, "count")
                if ((att) is not None): 
                    wrapcou2847 = RefOutArgWrapper(0)
                    inoutres2848 = Utils.tryParseInt(att[1], wrapcou2847)
                    cou = wrapcou2847.value
                    if (inoutres2848): 
                        slot.count = cou
            if (self.__m_links is None): 
                self.__m_links = dict()
            if (self.__m_links2 is None): 
                self.__m_links2 = dict()
            if (create_links1): 
                key = str(res)
                if (not key in self.__m_links): 
                    self.__m_links[key] = res
            if (not Utils.isNullOrEmpty(identity)): 
                res.tag = identity
                if (not identity in self.__m_links2): 
                    self.__m_links2[identity] = res
            return res
        except Exception as ex: 
            return None
    def __enter__(self): return self
    def __exit__(self, typ, val, traceback): self.close()