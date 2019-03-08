# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.


from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.decree.DecreeAnalyzer import DecreeAnalyzer
from pullenti.ner.instrument.InstrumentAnalyzer import InstrumentAnalyzer
from pullenti.ner.transport.TransportAnalyzer import TransportAnalyzer
from pullenti.ner.person.PersonAnalyzer import PersonAnalyzer
from pullenti.ner.mail.MailAnalyzer import MailAnalyzer
from pullenti.ner.titlepage.TitlePageAnalyzer import TitlePageAnalyzer
from pullenti.ner.named.NamedEntityAnalyzer import NamedEntityAnalyzer
from pullenti.ner.weapon.WeaponAnalyzer import WeaponAnalyzer
from pullenti.ner.goods.GoodsAnalyzer import GoodsAnalyzer
from pullenti.ner.booklink.BookLinkAnalyzer import BookLinkAnalyzer
from pullenti.ner.business.BusinessAnalyzer import BusinessAnalyzer
from pullenti.ner.org.OrganizationAnalyzer import OrganizationAnalyzer
from pullenti.ner.date.DateAnalyzer import DateAnalyzer
from pullenti.ner.keyword.KeywordAnalyzer import KeywordAnalyzer
from pullenti.ner.phone.PhoneAnalyzer import PhoneAnalyzer
from pullenti.ner.money.MoneyAnalyzer import MoneyAnalyzer
from pullenti.ner.uri.UriAnalyzer import UriAnalyzer
from pullenti.ner.definition.DefinitionAnalyzer import DefinitionAnalyzer
from pullenti.ner.address.AddressAnalyzer import AddressAnalyzer
from pullenti.ner.geo.GeoAnalyzer import GeoAnalyzer
from pullenti.ner.bank.BankAnalyzer import BankAnalyzer
from pullenti.ner.denomination.DenominationAnalyzer import DenominationAnalyzer
from pullenti.ner.measure.MeasureAnalyzer import MeasureAnalyzer

class Sdk:
    """ Инициализация SDK """
    
    @staticmethod
    def get_version() -> str:
        return ProcessorService.get_version()
    
    @staticmethod
    def initialize(lang : 'MorphLang'=None) -> None:
        """ Вызывать инициализацию в самом начале
        
        Args:
            lang(MorphLang): по умолчанию, русский и английский
        """
        ProcessorService.initialize(lang)
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
        BusinessAnalyzer.initialize()
        GoodsAnalyzer.initialize()
        NamedEntityAnalyzer.initialize()
        WeaponAnalyzer.initialize()