# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.morph.MorphLang import MorphLang


class Sdk:
    """ Инициализация SDK """
    
    @staticmethod
    def get_version() -> str:
        from pullenti.ner.ProcessorService import ProcessorService
        return ProcessorService.get_version()
    
    @staticmethod
    def initialize(lang : 'MorphLang'=MorphLang()) -> None:
        from pullenti.ner.ProcessorService import ProcessorService
        from pullenti.ner.money.MoneyAnalyzer import MoneyAnalyzer
        from pullenti.ner.uri.UriAnalyzer import UriAnalyzer
        from pullenti.ner.phone.PhoneAnalyzer import PhoneAnalyzer
        from pullenti.ner.date.DateAnalyzer import DateAnalyzer
        from pullenti.ner.keyword.KeywordAnalyzer import KeywordAnalyzer
        from pullenti.ner.definition.DefinitionAnalyzer import DefinitionAnalyzer
        from pullenti.ner.denomination.DenominationAnalyzer import DenominationAnalyzer
        from pullenti.ner.measure.MeasureAnalyzer import MeasureAnalyzer
        from pullenti.ner.bank.BankAnalyzer import BankAnalyzer
        from pullenti.ner.geo.GeoAnalyzer import GeoAnalyzer
        from pullenti.ner.address.AddressAnalyzer import AddressAnalyzer
        from pullenti.ner._org.OrganizationAnalyzer import OrganizationAnalyzer
        from pullenti.ner.person.PersonAnalyzer import PersonAnalyzer
        from pullenti.ner.mail.MailAnalyzer import MailAnalyzer
        from pullenti.ner.transport.TransportAnalyzer import TransportAnalyzer
        from pullenti.ner.decree.DecreeAnalyzer import DecreeAnalyzer
        from pullenti.ner.instrument.InstrumentAnalyzer import InstrumentAnalyzer
        from pullenti.ner.titlepage.TitlePageAnalyzer import TitlePageAnalyzer
        from pullenti.ner.booklink.BookLinkAnalyzer import BookLinkAnalyzer
        from pullenti.ner.business.BusinessAnalyzer import BusinessAnalyzer
        from pullenti.ner.named.NamedEntityAnalyzer import NamedEntityAnalyzer
        from pullenti.ner.weapon.WeaponAnalyzer import WeaponAnalyzer
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
        NamedEntityAnalyzer.initialize()
        WeaponAnalyzer.initialize()