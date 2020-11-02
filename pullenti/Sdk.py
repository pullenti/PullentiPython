# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import datetime

from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.decree.DecreeAnalyzer import DecreeAnalyzer
from pullenti.ner.transport.TransportAnalyzer import TransportAnalyzer
from pullenti.ner.instrument.InstrumentAnalyzer import InstrumentAnalyzer
from pullenti.ner.org.OrganizationAnalyzer import OrganizationAnalyzer
from pullenti.ner.person.PersonAnalyzer import PersonAnalyzer
from pullenti.ner.mail.MailAnalyzer import MailAnalyzer
from pullenti.ner.named.NamedEntityAnalyzer import NamedEntityAnalyzer
from pullenti.ner.weapon.WeaponAnalyzer import WeaponAnalyzer
from pullenti.semantic.SemanticService import SemanticService
from pullenti.ner.titlepage.TitlePageAnalyzer import TitlePageAnalyzer
from pullenti.ner.booklink.BookLinkAnalyzer import BookLinkAnalyzer
from pullenti.ner.goods.GoodsAnalyzer import GoodsAnalyzer
from pullenti.ner.keyword.KeywordAnalyzer import KeywordAnalyzer
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.denomination.DenominationAnalyzer import DenominationAnalyzer
from pullenti.ner.uri.UriAnalyzer import UriAnalyzer
from pullenti.ner.phone.PhoneAnalyzer import PhoneAnalyzer
from pullenti.ner.money.MoneyAnalyzer import MoneyAnalyzer
from pullenti.ner.measure.MeasureAnalyzer import MeasureAnalyzer
from pullenti.ner.definition.DefinitionAnalyzer import DefinitionAnalyzer
from pullenti.ner.bank.BankAnalyzer import BankAnalyzer
from pullenti.ner.address.AddressAnalyzer import AddressAnalyzer
from pullenti.ner.date.DateAnalyzer import DateAnalyzer
from pullenti.ner.geo.GeoAnalyzer import GeoAnalyzer

class Sdk:
    """ Инициализация SDK Pullenti
    
    """
    
    @staticmethod
    def get_version() -> str:
        """ Версия SDK Pullenti """
        return ProcessorService.get_version()
    
    @staticmethod
    def get_version_date() -> datetime.datetime:
        """ Дата выпуска версии SDK """
        return ProcessorService.get_version_date()
    
    @staticmethod
    def initialize_all() -> None:
        """ Инициализация всего SDK и на всех поддержанных языках.
        Вызывать в самом начале работы. Инициализируется морфология (MorphologyService),
        служба процессоров (ProcessorService), все доступные анализаторы сущностей и
        семантический анализ (SemanticService). Так что больше ничего инициализировать не нужно.
        Полная инициализация
        """
        Sdk.initialize((MorphLang.RU) | MorphLang.UA | MorphLang.EN)
    
    @staticmethod
    def initialize(lang : 'MorphLang'=None) -> None:
        """ Инициализация SDK.
        Вызывать в самом начале работы. Инициализируется морфология (MorphologyService),
        служба процессоров (ProcessorService), все доступные анализаторы сущностей и
        семантический анализ (SemanticService). Так что больше ничего инициализировать не нужно.
        
        Args:
            lang(MorphLang): по умолчанию, русский и английский
        Инициализация конкретных языков
        """
        # сначала инициализация всего сервиса
        ProcessorService.initialize(lang)
        # а затем конкретные анализаторы (какие нужно, в данном случае - все)
        MoneyAnalyzer.initialize()
        UriAnalyzer.initialize()
        PhoneAnalyzer.initialize()
        DateAnalyzer.initialize()
        KeywordAnalyzer.initialize()
        DefinitionAnalyzer.initialize()
        DenominationAnalyzer.initialize()
        MeasureAnalyzer.initialize()
        BankAnalyzer.initialize()
        GeoAnalyzer.initialize()
        AddressAnalyzer.initialize()
        OrganizationAnalyzer.initialize()
        PersonAnalyzer.initialize()
        MailAnalyzer.initialize()
        TransportAnalyzer.initialize()
        DecreeAnalyzer.initialize()
        InstrumentAnalyzer.initialize()
        TitlePageAnalyzer.initialize()
        BookLinkAnalyzer.initialize()
        GoodsAnalyzer.initialize()
        NamedEntityAnalyzer.initialize()
        WeaponAnalyzer.initialize()
        # ещё инициализируем семантическую обработки (в принципе, она не используется для задачи NER)
        SemanticService.initialize()