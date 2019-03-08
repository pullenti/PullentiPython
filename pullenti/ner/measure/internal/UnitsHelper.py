# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphClass import MorphClass
from pullenti.ner.measure.internal.Unit import Unit
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.core.Termin import Termin
from pullenti.ner.measure.internal.UnitsFactors import UnitsFactors
from pullenti.ner.measure.MeasureKind import MeasureKind
from pullenti.ner.TextToken import TextToken
from pullenti.ner.MetaToken import MetaToken

class UnitsHelper:
    
    UNITS = None
    
    TERMINS = None
    
    UGRADUS = None
    
    UGRADUSC = None
    
    UGRADUSF = None
    
    UPERCENT = None
    
    UALCO = None
    
    UOM = None
    
    UHOUR = None
    
    USEC = None
    
    __m_inited = False
    
    __m_kinds_keywords = None
    
    @staticmethod
    def find_unit(v : str, fact : 'UnitsFactors') -> 'Unit':
        if (fact != UnitsFactors.NO): 
            for u in UnitsHelper.UNITS: 
                if (u.base_unit is not None and u.factor == fact): 
                    if ((u.base_unit.fullname_cyr == v or u.base_unit.fullname_lat == v or u.base_unit.name_cyr == v) or u.base_unit.name_lat == v): 
                        return u
        for u in UnitsHelper.UNITS: 
            if ((u.fullname_cyr == v or u.fullname_lat == v or u.name_cyr == v) or u.name_lat == v): 
                return u
        return None
    
    @staticmethod
    def check_keyword(ki : 'MeasureKind', t : 'Token') -> bool:
        if (t is None or ki == MeasureKind.UNDEFINED): 
            return False
        if (isinstance(t, MetaToken)): 
            tt = (t).begin_token
            while tt is not None and tt.end_char <= t.end_char: 
                if (UnitsHelper.check_keyword(ki, tt)): 
                    return True
                tt = tt.next0_
            return False
        if (not ((isinstance(t, TextToken)))): 
            return False
        term = t.get_normal_case_text(MorphClass.NOUN, True, MorphGender.UNDEFINED, False)
        for u in UnitsHelper.UNITS: 
            if (u.kind == ki): 
                if (term in u.keywords): 
                    return True
        if (ki in UnitsHelper.__m_kinds_keywords): 
            if (term in UnitsHelper.__m_kinds_keywords[ki]): 
                return True
        return False
    
    @staticmethod
    def initialize() -> None:
        if (UnitsHelper.__m_inited): 
            return
        UnitsHelper.__m_inited = True
        UnitsHelper.UNITS = list()
        UnitsHelper.TERMINS = TerminCollection()
        UnitsHelper.__m_kinds_keywords = dict()
        UnitsHelper.__m_kinds_keywords[MeasureKind.SPEED] = list(["СКОРОСТЬ", "SPEED", "ШВИДКІСТЬ"])
        Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = True
        u = Unit._new1623("м", "m", "метр", "meter", MeasureKind.LENGTH)
        u.keywords.extend(["ДЛИНА", "ДЛИННА", "ШИРИНА", "ГЛУБИНА", "ВЫСОТА", "РАЗМЕР", "ГАБАРИТ", "РАССТОЯНИЕ", "РАДИУС", "ПЕРИМЕТР", "ДИАМЕТР", "ТОЛЩИНА", "ПОДАЧА", "НАПОР", "ДАЛЬНОСТЬ", "ТИПОРАЗМЕР", "КАЛИБР", "LENGTH", "WIDTH", "DEPTH", "HEIGHT", "SIZE", "ENVELOPE", "DISTANCE", "RADIUS", "PERIMETER", "DIAMETER", "FLOW", "PRESSURE", "CALIBER", "ДОВЖИНА", "ШИРИНА", "ГЛИБИНА", "ВИСОТА", "РОЗМІР", "ГАБАРИТ", "ВІДСТАНЬ", "РАДІУС", "ДІАМЕТР", "НАТИСК", "КАЛІБР"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new119("МЕТР", u)
        t.add_variant("МЕТРОВЫЙ", False)
        t.add_variant("МЕТРОВИЙ", False)
        t.add_variant("METER", False)
        t.add_abridge("М.")
        t.add_abridge("M.")
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.DECI, UnitsFactors.CENTI, UnitsFactors.MILLI, UnitsFactors.MICRO, UnitsFactors.NANO]: 
            UnitsHelper.__add_factor(f, u, "М.", "M.", "МЕТР;МЕТРОВЫЙ", "МЕТР;МЕТРОВИЙ", "METER;METRE")
        uu = Unit._new1623("миль", "mile", "морская миля", "mile", MeasureKind.LENGTH)
        uu.base_unit = u
        uu.base_multiplier = (1852)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new119("МИЛЯ", uu)
        t.add_variant("МОРСКАЯ МИЛЯ", False)
        t.add_abridge("NMI")
        t.add_variant("MILE", False)
        t.add_variant("NAUTICAL MILE", False)
        UnitsHelper.TERMINS.add(t)
        uu = Unit._new1627("фут", "ft", "фут", "foot", u, 0.304799472, MeasureKind.LENGTH)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new119("ФУТ", uu)
        t.add_abridge("FT.")
        t.add_variant("FOOT", False)
        UnitsHelper.TERMINS.add(t)
        uu = Unit._new1627("дюйм", "in", "дюйм", "inch", u, 0.0254, MeasureKind.LENGTH)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new119("ДЮЙМ", uu)
        t.add_abridge("IN")
        t.add_variant("INCH", False)
        UnitsHelper.TERMINS.add(t)
        u = Unit._new1623("ар", "are", "ар", "are", MeasureKind.AREA)
        u.keywords.extend(["ПЛОЩАДЬ", "ПРОЩИНА", "AREA", "SQWARE", "SPACE"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new119("АР", u)
        t.add_variant("ARE", False)
        t.add_variant("СОТКА", False)
        UnitsHelper.TERMINS.add(t)
        uu = Unit._new1623("га", "ga", "гектар", "hectare", MeasureKind.AREA)
        uu.base_unit = u
        uu.base_multiplier = (100)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new119("ГЕКТАР", uu)
        t.add_variant("HECTARE", False)
        t.add_abridge("ГА")
        t.add_abridge("GA")
        UnitsHelper.TERMINS.add(t)
        u = Unit._new1623("г", "g", "грамм", "gram", MeasureKind.WEIGHT)
        u.keywords.extend(["ВЕС", "ТЯЖЕСТЬ", "НЕТТО", "БРУТТО", "МАССА", "НАГРУЗКА", "ЗАГРУЗКА", "УПАКОВКА", "WEIGHT", "NET", "GROSS", "MASS", "ВАГА", "ТЯЖКІСТЬ", "МАСА"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new119("ГРАММ", u)
        t.add_abridge("Г.")
        t.add_abridge("ГР.")
        t.add_abridge("G.")
        t.add_abridge("GR.")
        t.add_variant("ГРАММОВЫЙ", False)
        t.add_variant("ГРАММНЫЙ", False)
        t.add_variant("ГРАМОВИЙ", False)
        t.add_variant("GRAM", False)
        t.add_variant("GRAMME", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.MILLI]: 
            UnitsHelper.__add_factor(f, u, "Г.;ГР;", "G.;GR.", "ГРАМ;ГРАММ;ГРАММНЫЙ", "ГРАМ;ГРАМОВИЙ", "GRAM;GRAMME")
        uu = Unit._new1637("ц", "centner", "центнер", "centner", u, 100000)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new119("ЦЕНТНЕР", uu)
        t.add_variant("CENTNER", False)
        t.add_variant("QUINTAL", False)
        t.add_abridge("Ц.")
        UnitsHelper.TERMINS.add(t)
        uu = Unit._new1627("т", "t", "тонна", "tonne", u, 1000000, MeasureKind.WEIGHT)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new119("ТОННА", uu)
        t.add_variant("TONNE", False)
        t.add_variant("TON", False)
        t.add_abridge("Т.")
        t.add_abridge("T.")
        UnitsHelper.TERMINS.add(t)
        UnitsHelper.__add_factor(UnitsFactors.MEGA, uu, "Т", "T", "ТОННА;ТОННЫЙ", "ТОННА;ТОННИЙ", "TONNE;TON")
        u = Unit._new1623("л", "l", "литр", "liter", MeasureKind.VOLUME)
        u.keywords.extend(["ОБЪЕМ", "ЕМКОСТЬ", "ВМЕСТИМОСЬ", "ОБСЯГ", "ЄМНІСТЬ", "МІСТКІСТЬ", "VOLUME", "CAPACITY"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new119("ЛИТР", u)
        t.add_abridge("Л.")
        t.add_abridge("L.")
        t.add_variant("LITER", False)
        t.add_variant("LITRE", False)
        t.add_variant("ЛІТР", False)
        t.add_variant("ЛІТРОВИЙ", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.MILLI, UnitsFactors.CENTI]: 
            UnitsHelper.__add_factor(f, u, "Л.", "L.", "ЛИТР;ЛИТРОВЫЙ", "ЛІТР;ЛІТРОВИЙ", "LITER;LITRE")
        uu = Unit._new1627("галлон", "gallon", "галлон", "gallon", u, 4.5461, MeasureKind.VOLUME)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new119("ГАЛЛОН", u)
        t.add_variant("ГАЛОН", False)
        t.add_variant("GALLON", False)
        t.add_abridge("ГАЛ")
        UnitsHelper.TERMINS.add(t)
        uu = Unit._new1627("баррель", "bbls", "баррель нефти", "barrel", u, 158.987, MeasureKind.VOLUME)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new119("БАРРЕЛЬ", uu)
        t.add_abridge("BBLS")
        t.add_variant("БАРРЕЛЬ НЕФТИ", False)
        t.add_variant("BARRREL", False)
        UnitsHelper.TERMINS.add(t)
        u = Unit._new1623("сек", "sec", "секунда", "second", MeasureKind.TIME)
        UnitsHelper.USEC = u
        u.keywords.extend(["ВРЕМЯ", "ПРОДОЛЖИТЕЛЬНОСТЬ", "ЗАДЕРЖКА", "ДЛИТЕЛЬНОСТЬ", "ДОЛГОТА", "TIME", "DURATION", "DELAY", "ЧАС", "ТРИВАЛІСТЬ", "ЗАТРИМКА"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new119("СЕКУНДА", u)
        t.add_abridge("С.")
        t.add_abridge("C.")
        t.add_abridge("СЕК")
        t.add_abridge("СЕК")
        t.add_abridge("S.")
        t.add_abridge("SEC")
        t.add_variant("СЕКУНДНЫЙ", False)
        t.add_variant("СЕКУНДНИЙ", False)
        t.add_variant("SECOND", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.MILLI, UnitsFactors.MICRO]: 
            UnitsHelper.__add_factor(f, u, "С.;СЕК", "C;S.;SEC;", "СЕКУНДА;СЕКУНДНЫЙ", "СЕКУНДА;СЕКУНДНИЙ", "SECOND")
        uu = Unit._new1623("мин", "min", "минута", "minute", MeasureKind.TIME)
        uu.base_unit = u
        uu.base_multiplier = (60)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new119("МИНУТА", uu)
        t.add_abridge("МИН.")
        t.add_abridge("MIN.")
        t.add_variant("МИНУТНЫЙ", False)
        t.add_variant("ХВИЛИННИЙ", False)
        t.add_variant("ХВИЛИНА", False)
        t.add_variant("МІНУТА", False)
        t.add_variant("MINUTE", False)
        UnitsHelper.TERMINS.add(t)
        u = uu
        uu = Unit._new1627("ч", "h", "час", "hour", u, 60, MeasureKind.TIME)
        UnitsHelper.UHOUR = uu
        UnitsHelper.UNITS.append(uu)
        t = Termin._new119("ЧАС", uu)
        t.add_abridge("Ч.")
        t.add_abridge("H.")
        t.add_variant("ЧАСОВОЙ", False)
        t.add_variant("HOUR", False)
        t.add_variant("ГОДИННИЙ", False)
        t.add_variant("ГОДИНА", False)
        UnitsHelper.TERMINS.add(t)
        u = Unit._new1623("дн", "d", "день", "day", MeasureKind.TIME)
        u.keywords.extend(UnitsHelper.USEC.keywords)
        u.keywords.extend(["ПОСТАВКА", "СРОК", "РАБОТА", "ЗАВЕРШЕНИЕ"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new119("ДЕНЬ", u)
        t.add_abridge("ДН.")
        t.add_abridge("Д.")
        t.add_variant("DAY", False)
        UnitsHelper.TERMINS.add(t)
        uu = Unit._new1627("нед", "week", "неделя", "week", u, 7, MeasureKind.TIME)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new119("НЕДЕЛЯ", uu)
        t.add_abridge("НЕД")
        t.add_variant("WEEK", False)
        t.add_variant("ТИЖДЕНЬ", False)
        UnitsHelper.TERMINS.add(t)
        uu = Unit._new1627("мес", "mon", "месяц", "month", u, 30, MeasureKind.TIME)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new119("МЕСЯЦ", uu)
        t.add_abridge("МЕС")
        t.add_abridge("MON")
        t.add_variant("MONTH", False)
        t.add_variant("МІСЯЦЬ", False)
        UnitsHelper.TERMINS.add(t)
        uu = Unit._new1627("г", "year", "год", "year", u, 365, MeasureKind.TIME)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new119("ГОД", uu)
        t.add_abridge("Г.")
        t.add_abridge("ГД")
        t.add_variant("YEAR", False)
        t.add_variant("РІК", False)
        t.add_variant("ЛЕТ", False)
        UnitsHelper.TERMINS.add(t)
        UnitsHelper.UGRADUS = Unit("°", "°", "градус", "degree")
        UnitsHelper.UGRADUS.keywords.extend(["ТЕМПЕРАТУРА", "ШИРОТА", "ДОЛГОТА", "АЗИМУТ", "ДОВГОТА", "TEMPERATURE", "LATITUDE", "LONGITUDE", "AZIMUTH"])
        UnitsHelper.UNITS.append(UnitsHelper.UGRADUS)
        t = Termin._new119("ГРАДУС", UnitsHelper.UGRADUS)
        t.add_variant("DEGREE", False)
        UnitsHelper.TERMINS.add(t)
        UnitsHelper.UGRADUSC = Unit("°C", "°C", "градус Цельсия", "celsius degree")
        UnitsHelper.UGRADUSC.keywords.append("ТЕМПЕРАТУРА")
        UnitsHelper.UGRADUS.keywords.append("TEMPERATURE")
        UnitsHelper.UGRADUS.psevdo.append(UnitsHelper.UGRADUSC)
        UnitsHelper.UNITS.append(UnitsHelper.UGRADUSC)
        t = Termin._new119("ГРАДУС ЦЕЛЬСИЯ", UnitsHelper.UGRADUSC)
        t.add_variant("ГРАДУС ПО ЦЕЛЬСИЮ", False)
        t.add_variant("CELSIUS DEGREE", False)
        UnitsHelper.TERMINS.add(t)
        UnitsHelper.UGRADUSF = Unit("°F", "°F", "градус Фаренгейта", "Fahrenheit degree")
        UnitsHelper.UGRADUSF.keywords = UnitsHelper.UGRADUSC.keywords
        UnitsHelper.UGRADUS.psevdo.append(UnitsHelper.UGRADUSF)
        UnitsHelper.UNITS.append(UnitsHelper.UGRADUSF)
        t = Termin._new119("ГРАДУС ФАРЕНГЕЙТА", UnitsHelper.UGRADUSF)
        t.add_variant("ГРАДУС ПО ФАРЕНГЕЙТУ", False)
        t.add_variant("FAHRENHEIT DEGREE", False)
        UnitsHelper.TERMINS.add(t)
        UnitsHelper.UPERCENT = Unit("%", "%", "процент", "percent")
        UnitsHelper.UNITS.append(UnitsHelper.UPERCENT)
        t = Termin._new119("ПРОЦЕНТ", UnitsHelper.UPERCENT)
        t.add_variant("ПРОЦ", False)
        t.add_variant("PERC", False)
        t.add_variant("PERCENT", False)
        UnitsHelper.TERMINS.add(t)
        UnitsHelper.UALCO = Unit("%(об)", "%(vol)", "объёмный процент", "volume percent")
        UnitsHelper.UALCO.keywords.extend(["КРЕПОСТЬ", "АЛКОГОЛЬ", "ALCOHOL", "СПИРТ", "АЛКОГОЛЬНЫЙ", "SPIRIT"])
        UnitsHelper.UPERCENT.psevdo.append(UnitsHelper.UALCO)
        UnitsHelper.UGRADUS.psevdo.append(UnitsHelper.UALCO)
        UnitsHelper.UNITS.append(UnitsHelper.UALCO)
        t = Termin._new119("ОБЪЕМНЫЙ ПРОЦЕНТ", UnitsHelper.UALCO)
        t.add_variant("ГРАДУС", False)
        UnitsHelper.TERMINS.add(t)
        u = Unit("об", "rev", "оборот", "revolution")
        UnitsHelper.UGRADUS.keywords.extend(["ЧАСТОТА", "ВРАЩЕНИЕ", "ВРАЩАТЕЛЬНЫЙ", "СКОРОСТЬ", "ОБОРОТ", "FREQUENCY", "ROTATION", "ROTATIONAL", "SPEED", "ОБЕРТАННЯ", "ОБЕРТАЛЬНИЙ"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new119("ОБОРОТ", u)
        t.add_abridge("ОБ.")
        t.add_abridge("ROT.")
        t.add_abridge("REV.")
        t.add_variant("ROTATION", False)
        t.add_variant("REVOLUTION", False)
        UnitsHelper.TERMINS.add(t)
        u = Unit("В", "V", "вольт", "volt")
        u.keywords.extend(["ЭЛЕКТРИЧЕСКИЙ", "ПОТЕНЦИАЛ", "НАПРЯЖЕНИЕ", "ЭЛЕКТРОДВИЖУЩИЙ", "ПИТАНИЕ", "ТОК", "ПОСТОЯННЫЙ", "ПЕРЕМЕННЫЙ", "ЕЛЕКТРИЧНИЙ", "ПОТЕНЦІАЛ", "НАПРУГА", "ЕЛЕКТРОРУШІЙНОЇ", "ХАРЧУВАННЯ", "СТРУМ", "ПОСТІЙНИЙ", "ЗМІННИЙ", "ELECTRIC", "POTENTIAL", "TENSION", "ELECTROMOTIVE", "FOOD", "CURRENT", "CONSTANT", "VARIABLE"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new119("ВОЛЬТ", u)
        t.add_variant("VOLT", False)
        t.add_abridge("V")
        t.add_abridge("В.")
        t.add_abridge("B.")
        t.add_variant("VAC", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.MEGA, UnitsFactors.MILLI, UnitsFactors.MILLI, UnitsFactors.MICRO]: 
            UnitsHelper.__add_factor(f, u, "В.", "V.", "ВОЛЬТ;ВОЛЬТНЫЙ", "ВОЛЬТ;ВОЛЬТНІ", "VOLT")
        u = Unit("Вт", "W", "ватт", "watt")
        u.keywords.extend(["МОЩНОСТЬ", "ЭНЕРГИЯ", "ПОТОК", "ИЗЛУЧЕНИЕ", "ЭНЕРГОПОТРЕБЛЕНИЕ", "ПОТУЖНІСТЬ", "ЕНЕРГІЯ", "ПОТІК", "ВИПРОМІНЮВАННЯ", "POWER", "ENERGY", "FLOW", "RADIATION"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new119("ВАТТ", u)
        t.add_abridge("Вт")
        t.add_abridge("W")
        t.add_variant("WATT", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.MEGA, UnitsFactors.GIGA, UnitsFactors.MILLI]: 
            UnitsHelper.__add_factor(f, u, "ВТ.", "W.", "ВАТТ;ВАТТНЫЙ", "ВАТ;ВАТНИЙ", "WATT;WATTS")
        uu = Unit._new1637("л.с.", "hp", "лошадиная сила", "horsepower", u, 735.49875)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new119("ЛОШАДИНАЯ СИЛА", uu)
        t.add_abridge("Л.С.")
        t.add_abridge("ЛОШ.С.")
        t.add_abridge("ЛОШ.СИЛА")
        t.add_abridge("HP")
        t.add_abridge("PS")
        t.add_abridge("SV")
        t.add_variant("HORSEPOWER", False)
        UnitsHelper.TERMINS.add(t)
        u = Unit("Дж", "J", "джоуль", "joule")
        u.keywords.extend(["РАБОТА", "ЭНЕРГИЯ", "ТЕПЛОТА", "ТЕПЛОВОЙ", "ТЕПЛОВЫДЕЛЕНИЕ", "МОЩНОСТЬ", "ХОЛОДИЛЬНЫЙ"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new119("ДЖОУЛЬ", u)
        t.add_abridge("ДЖ")
        t.add_abridge("J")
        t.add_variant("JOULE", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.MEGA, UnitsFactors.GIGA, UnitsFactors.TERA, UnitsFactors.MILLI]: 
            UnitsHelper.__add_factor(f, u, "ДЖ.", "J.", "ДЖОУЛЬ", "ДЖОУЛЬ", "JOULE")
        uu = Unit("БТЕ", "BTU", "британская терминальная единица", "british terminal unit")
        uu.keywords = u.keywords
        UnitsHelper.UNITS.append(uu)
        t = Termin._new119("БРИТАНСКАЯ ТЕРМИНАЛЬНАЯ ЕДИНИЦА", uu)
        t.add_abridge("БТЕ")
        t.add_abridge("BTU")
        t.add_variant("BRITISH TERMINAL UNIT", False)
        UnitsHelper.TERMINS.add(t)
        u = Unit("К", "K", "кельвин", "kelvin")
        u.keywords.extend(UnitsHelper.UGRADUSC.keywords)
        UnitsHelper.UNITS.append(u)
        t = Termin._new119("КЕЛЬВИН", u)
        t.add_abridge("К.")
        t.add_abridge("K.")
        t.add_variant("KELVIN", False)
        t.add_variant("КЕЛЬВІН", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.MEGA, UnitsFactors.GIGA, UnitsFactors.MILLI]: 
            UnitsHelper.__add_factor(f, u, "К.", "K.", "КЕЛЬВИН", "КЕЛЬВІН", "KELVIN")
        u = Unit("Гц", "Hz", "герц", "herz")
        u.keywords.extend(["ЧАСТОТА", "ЧАСТОТНЫЙ", "ПЕРИОДИЧНОСТЬ", "ПИТАНИЕ", "ЧАСТОТНИЙ", "ПЕРІОДИЧНІСТЬ", "FREQUENCY"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new119("ГЕРЦ", u)
        t.add_abridge("HZ")
        t.add_abridge("ГЦ")
        t.add_variant("ГЕРЦОВЫЙ", False)
        t.add_variant("ГЕРЦОВИЙ", False)
        t.add_variant("HERZ", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.MEGA, UnitsFactors.GIGA, UnitsFactors.MICRO]: 
            UnitsHelper.__add_factor(f, u, "ГЦ.", "W.", "ГЕРЦ;ГЕРЦОВЫЙ", "ГЕРЦ;ГЕРЦОВИЙ", "HERZ")
        u = Unit("Ом", "Ω", "Ом", "Ohm")
        UnitsHelper.UOM = u
        u.keywords.extend(["СОПРОТИВЛЕНИЕ", "РЕЗИСТОР", "РЕЗИСТНЫЙ", "ИМПЕДАНС", "РЕЗИСТОРНЫЙ", "ОПІР", "РЕЗИСТИВНИЙ", "ІМПЕДАНС", "RESISTANCE", "RESISTOR", "RESISTIVE", "IMPEDANCE"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new119("ОМ", UnitsHelper.UOM)
        t.add_variant("OHM", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.MEGA, UnitsFactors.GIGA, UnitsFactors.MICRO, UnitsFactors.MILLI]: 
            UnitsHelper.__add_factor(f, u, "ОМ", "Ω", "ОМ", "ОМ", "OHM")
        u = Unit("А", "A", "ампер", "ampere")
        u.keywords.extend(["ТОК", "СИЛА", "ЭЛЕКТРИЧЕСКИЙ", "ЭЛЕКТРИЧЕСТВО", "МАГНИТ", "МАГНИТОДВИЖУЩИЙ", "ПОТРЕБЛЕНИЕ", "CURRENT", "POWER", "ELECTRICAL", "ELECTRICITY", "MAGNET", "MAGNETOMOTIVE", "CONSUMPTION", "СТРУМ", "ЕЛЕКТРИЧНИЙ", "ЕЛЕКТРИКА", "МАГНІТ", "МАГНИТОДВИЖУЩИЙ", "СПОЖИВАННЯ"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new119("АМПЕР", u)
        t.add_abridge("A")
        t.add_abridge("А")
        t.add_variant("АМПЕРНЫЙ", False)
        t.add_variant("AMP", False)
        t.add_variant("AMPERE", False)
        UnitsHelper.TERMINS.add(t)
        uu = Unit._new1677("Ач", "Ah", "ампер-час", "ampere-hour", u, UnitsHelper.UHOUR)
        uu.keywords.extend(["ЗАРЯД", "АККУМУЛЯТОР", "АККУМУЛЯТОРНЫЙ", "ЗАРЯДКА", "БАТАРЕЯ", "CHARGE", "BATTERY", "CHARGING", "АКУМУЛЯТОР", "АКУМУЛЯТОРНИЙ"])
        UnitsHelper.UNITS.append(uu)
        t = Termin._new119("АМПЕР ЧАС", uu)
        t.add_abridge("АЧ")
        t.add_abridge("AH")
        t.add_variant("AMPERE HOUR", False)
        t.add_variant("АМПЕРЧАС", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.MEGA, UnitsFactors.GIGA, UnitsFactors.MICRO, UnitsFactors.MILLI]: 
            u1 = UnitsHelper.__add_factor(f, u, "А", "A", "АМПЕР;АМПЕРНЫЙ", "АМПЕР;АМПЕРНИЙ", "AMPERE;AMP")
            uu1 = UnitsHelper.__add_factor(f, uu, "АЧ", "AH", "АМПЕР ЧАС", "АМПЕР ЧАС", "AMPERE HOUR")
            uu1.base_unit = u1
            uu1.mult_unit = UnitsHelper.UHOUR
        uu = Unit("ВА", "VA", "вольт-ампер", "volt-ampere")
        uu.mult_unit = u
        uu.base_unit = UnitsHelper.find_unit("V", UnitsFactors.NO)
        uu.keywords.extend(["ТОК", "СИЛА", "МОЩНОСТЬ", "ЭЛЕКТРИЧЕСКИЙ", "ПЕРЕМЕННЫЙ"])
        UnitsHelper.UNITS.append(uu)
        t = Termin._new119("ВОЛЬТ-АМПЕР", uu)
        t.add_abridge("BA")
        t.add_abridge("BA")
        t.add_variant("VA", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.MEGA, UnitsFactors.GIGA, UnitsFactors.MICRO, UnitsFactors.MILLI]: 
            u1 = UnitsHelper.__add_factor(f, uu, "ВА;BA", "VA", "ВОЛЬТ-АМПЕР", "ВОЛЬТ-АМПЕР", "VOLT-AMPERE")
        u = Unit("Б", "B", "белл", "bell")
        u.keywords.extend(["ЗВУК", "ЗВУКОВОЙ", "ШУМ", "ШУМОВОЙ", "ГРОМКОСТЬ", "ГРОМКИЙ", "СИГНАЛ", "УСИЛЕНИЕ", "ЗАТУХАНИЕ", "ГАРМОНИЧЕСКИЙ", "ПОДАВЛЕНИЕ", "ЗВУКОВИЙ", "ШУМОВИЙ", "ГУЧНІСТЬ", "ГУЧНИЙ", "ПОСИЛЕННЯ", "ЗАГАСАННЯ", "ГАРМОНІЙНИЙ", "ПРИДУШЕННЯ", "SOUND", "NOISE", "VOLUME", "LOUD", "SIGNAL", "STRENGTHENING", "ATTENUATION", "HARMONIC", "SUPPRESSION"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new119("БЕЛЛ", u)
        t.add_abridge("Б.")
        t.add_abridge("B.")
        t.add_abridge("В.")
        t.add_variant("БЕЛ", False)
        t.add_variant("BELL", False)
        UnitsHelper.TERMINS.add(t)
        UnitsHelper.__add_factor(UnitsFactors.DECI, u, "Б", "B", "БЕЛЛ;БЕЛ", "БЕЛЛ;БЕЛ", "BELL")
        u = Unit("дБи", "dBi", "коэффициент усиления антенны", "dBi")
        u.keywords.extend(["УСИЛЕНИЕ", "АНТЕННА", "АНТЕНА", "ПОСИЛЕННЯ", "GAIN", "ANTENNA"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new119("DBI", u)
        t.add_variant("ДБИ", False)
        UnitsHelper.TERMINS.add(t)
        u = Unit("дБм", "dBm", "опорная мощность", "dBm")
        u.keywords.extend(["МОЩНОСТЬ"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new119("DBM", u)
        t.add_variant("ДБМ", False)
        t.add_variant("ДВМ", False)
        UnitsHelper.TERMINS.add(t)
        u = Unit("Ф", "F", "фарад", "farad")
        u.keywords.extend(["ЕМКОСТЬ", "ЭЛЕКТРИЧНСКИЙ", "КОНДЕНСАТОР"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new119("ФАРАД", u)
        t.add_abridge("Ф.")
        t.add_abridge("ФА")
        t.add_abridge("F")
        t.add_variant("FARAD", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.MICRO, UnitsFactors.MILLI, UnitsFactors.NANO, UnitsFactors.PICO]: 
            UnitsHelper.__add_factor(f, u, "Ф.;ФА.", "F", "ФАРАД", "ФАРАД", "FARAD")
        u = Unit("Н", "N", "ньютон", "newton")
        u.keywords.extend(["СИЛА", "МОМЕНТ"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new119("НЬЮТОН", u)
        t.add_abridge("Н.")
        t.add_abridge("H.")
        t.add_abridge("N.")
        t.add_variant("NEWTON", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.MEGA, UnitsFactors.KILO, UnitsFactors.MICRO, UnitsFactors.MILLI]: 
            UnitsHelper.__add_factor(f, u, "Н.", "N.", "НЬЮТОН", "НЬЮТОН", "NEWTON")
        u = Unit("моль", "mol", "моль", "mol")
        u.keywords.extend(["МОЛЕКУЛА", "МОЛЕКУЛЯРНЫЙ", "КОЛИЧЕСТВО", "ВЕЩЕСТВО"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new119("МОЛЬ", u)
        t.add_abridge("МЛЬ")
        t.add_variant("МОЛ", False)
        t.add_variant("MOL", False)
        t.add_variant("ГРАММ МОЛЕКУЛА", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.MEGA, UnitsFactors.KILO, UnitsFactors.MICRO, UnitsFactors.MILLI, UnitsFactors.NANO]: 
            UnitsHelper.__add_factor(f, u, "МЛЬ", "MOL", "МОЛЬ", "МОЛЬ", "MOL")
        u = Unit("Бк", "Bq", "беккерель", "becquerel")
        u.keywords.extend(["АКТИВНОСТЬ", "РАДИОАКТИВНЫЙ", "ИЗЛУЧЕНИЕ", "ИСТОЧНИК"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new119("БЕККЕРЕЛЬ", u)
        t.add_abridge("БК.")
        t.add_variant("BQ.", False)
        t.add_variant("БЕК", False)
        t.add_variant("БЕКЕРЕЛЬ", False)
        t.add_variant("BECQUEREL", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.MEGA, UnitsFactors.KILO, UnitsFactors.MICRO, UnitsFactors.MILLI, UnitsFactors.NANO]: 
            UnitsHelper.__add_factor(f, u, "БК.", "BQ.", "БЕККЕРЕЛЬ;БЕК", "БЕКЕРЕЛЬ", "BECQUEREL")
        u = Unit("См", "S", "сименс", "siemens")
        u.keywords.extend(["ПРОВОДИМОСТЬ", "ЭЛЕКТРИЧЕСКИЙ", "ПРОВОДНИК"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new119("СИМЕНС", u)
        t.add_abridge("СМ.")
        t.add_abridge("CM.")
        t.add_variant("S.", False)
        t.add_variant("SIEMENS", False)
        t.add_variant("СІМЕНС", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.MEGA, UnitsFactors.KILO, UnitsFactors.MICRO, UnitsFactors.MILLI, UnitsFactors.NANO]: 
            UnitsHelper.__add_factor(f, u, "СМ.", "S.", "СИМЕНС", "СІМЕНС", "SIEMENS")
        u = Unit("кд", "cd", "кандела", "candela")
        u.keywords.extend(["СВЕТ", "СВЕТОВОЙ", "ПОТОК", "ИСТОЧНИК"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new119("КАНДЕЛА", u)
        t.add_abridge("КД.")
        t.add_variant("CD.", False)
        t.add_variant("КАНДЕЛА", False)
        t.add_variant("CANDELA", False)
        UnitsHelper.TERMINS.add(t)
        u = Unit("Па", "Pa", "паскаль", "pascal")
        u.keywords.extend(["ДАВЛЕНИЕ", "НАПРЯЖЕНИЕ", "ТЯЖЕСТЬ", "PRESSURE", "STRESS", "ТИСК", "НАПРУГА"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new119("ПАСКАЛЬ", u)
        t.add_abridge("ПА")
        t.add_abridge("РА")
        t.add_variant("PA", False)
        t.add_variant("PASCAL", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.MEGA, UnitsFactors.GIGA, UnitsFactors.MICRO, UnitsFactors.MILLI]: 
            UnitsHelper.__add_factor(f, u, "ПА", "PA", "ПАСКАЛЬ", "ПАСКАЛЬ", "PASCAL")
        uu = Unit._new1637("бар", "bar", "бар", "bar", u, 100000)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new119("БАР", uu)
        t.add_variant("BAR", False)
        UnitsHelper.TERMINS.add(t)
        uu = Unit._new1637("мм.рт.ст.", "mm Hg", "миллиметр ртутного столба", "millimeter of mercury", u, 133.332)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new119("МИЛЛИМЕТР РТУТНОГО СТОЛБА", uu)
        t.add_abridge("ММ.РТ.СТ.")
        t.add_abridge("MM.PT.CT")
        t.add_abridge("MM HG")
        t.add_variant("MMGH", False)
        t.add_variant("ТОРР", False)
        t.add_variant("TORR", False)
        t.add_variant("MILLIMETER OF MERCURY", False)
        UnitsHelper.TERMINS.add(t)
        u = Unit("бит", "bit", "бит", "bit")
        u.keywords.extend(["СКОРОСТЬ", "ОБЪЕМ", "РАЗМЕР", "ПАМЯТЬ", "ЕМКОСТЬ", "ПЕРЕДАЧА", "ПРИЕМ", "ОТПРАВКА", "ОП", "ДИСК", "НАКОПИТЕЛЬ", "КЭШ", "ШВИДКІСТЬ", "ОБСЯГ", "РОЗМІР", "ВІДПРАВЛЕННЯ", "SPEED", "VOLUME", "SIZE", "MEMORY", "TRANSFER", "SEND", "RECEPTION", "RAM", "DISK", "HDD", "RAM", "ROM", "CD-ROM", "CASHE"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new119("БИТ", u)
        t.add_variant("BIT", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.MEGA, UnitsFactors.GIGA, UnitsFactors.TERA]: 
            UnitsHelper.__add_factor(f, u, "БИТ", "BIT", "БИТ", "БИТ", "BIT")
        uu = Unit("б", "b", "байт", "byte")
        uu.keywords = u.keywords
        UnitsHelper.UNITS.append(uu)
        t = Termin._new119("БАЙТ", uu)
        t.add_variant("BYTE", False)
        t.add_abridge("B.")
        t.add_abridge("Б.")
        t.add_abridge("В.")
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.MEGA, UnitsFactors.GIGA, UnitsFactors.TERA]: 
            UnitsHelper.__add_factor(f, uu, "Б.", "B.", "БАЙТ", "БАЙТ", "BYTE")
        u = Unit("бод", "Bd", "бод", "baud")
        u.keywords.extend(["СКОРОСТЬ", "ПЕРЕДАЧА", "ПРИЕМ", "ДАННЫЕ", "ОТПРАВКА"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new119("БОД", u)
        t.add_abridge("BD")
        t.add_variant("BAUD", False)
        UnitsHelper.TERMINS.add(t)
        for f in [UnitsFactors.KILO, UnitsFactors.MEGA, UnitsFactors.GIGA, UnitsFactors.TERA]: 
            UnitsHelper.__add_factor(f, uu, "БОД", "BD.", "БОД", "БОД", "BAUD")
        u = Unit("гс", "gf", "грамм-сила", "gram-force")
        u.keywords.extend(["СИЛА", "ДАВЛЕНИЕ"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new119("ГРАММ СИЛА", u)
        t.add_abridge("ГС")
        t.add_variant("POND", False)
        t.add_variant("ГРАМ СИЛА", False)
        t.add_abridge("GP.")
        t.add_variant("GRAM POND", False)
        t.add_variant("GRAM FORCE", False)
        UnitsHelper.TERMINS.add(t)
        uu = Unit._new1637("кгс", "kgf", "килограмм-сила", "kilogram-force", u, 1000)
        UnitsHelper.UNITS.append(uu)
        t = Termin._new119("КИЛОГРАММ СИЛА", uu)
        t.add_abridge("КГС")
        t.add_variant("KILOPOND", False)
        t.add_variant("КІЛОГРАМ СИЛА", False)
        t.add_abridge("KP.")
        t.add_variant("KILOGRAM POND", False)
        UnitsHelper.TERMINS.add(t)
        u = Unit("dpi", "точек на дюйм", "dpi", "dots per inch")
        u.keywords.extend(["РАЗРЕШЕНИЕ", "ЭКРАН", "МОНИТОР"])
        UnitsHelper.UNITS.append(u)
        t = Termin._new119("DOTS PER INCH", u)
        t.add_variant("DPI", False)
        UnitsHelper.TERMINS.add(t)
        Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = False
    
    @staticmethod
    def __add_factor(f : 'UnitsFactors', u0 : 'Unit', abbr_cyr : str, abbr_lat : str, names_ru : str, names_ua : str, names_en : str) -> 'Unit':
        pref_cyr = None
        pref_lat = None
        pref_ru = None
        pref_ua = None
        pref_en = None
        mult = 1
        swichVal = f
        if (swichVal == UnitsFactors.CENTI): 
            pref_cyr = "С"
            pref_lat = "C"
            pref_ru = "САНТИ"
            pref_ua = "САНТИ"
            pref_en = "CENTI"
            mult = 0.1
        elif (swichVal == UnitsFactors.DECI): 
            pref_cyr = "Д"
            pref_lat = "D"
            pref_ru = "ДЕЦИ"
            pref_ua = "ДЕЦИ"
            pref_en = "DECI"
            mult = 0.01
        elif (swichVal == UnitsFactors.GIGA): 
            pref_cyr = "Г"
            pref_lat = "G"
            pref_ru = "ГИГА"
            pref_ua = "ГІГА"
            pref_en = "GIGA"
            mult = (1000000000)
        elif (swichVal == UnitsFactors.KILO): 
            pref_cyr = "К"
            pref_lat = "K"
            pref_ru = "КИЛО"
            pref_ua = "КІЛО"
            pref_en = "KILO"
            mult = (1000)
        elif (swichVal == UnitsFactors.MEGA): 
            pref_cyr = "М"
            pref_lat = "M"
            pref_ru = "МЕГА"
            pref_ua = "МЕГА"
            pref_en = "MEGA"
            mult = (1000000)
        elif (swichVal == UnitsFactors.MICRO): 
            pref_cyr = "МК"
            pref_lat = "MK"
            pref_ru = "МИКРО"
            pref_ua = "МІКРО"
            pref_en = "MICRO"
            mult = 0.0001
        elif (swichVal == UnitsFactors.MILLI): 
            pref_cyr = "М"
            pref_lat = "M"
            pref_ru = "МИЛЛИ"
            pref_ua = "МІЛІ"
            pref_en = "MILLI"
            mult = 0.001
        elif (swichVal == UnitsFactors.NANO): 
            pref_cyr = "Н"
            pref_lat = "N"
            pref_ru = "НАНО"
            pref_ua = "НАНО"
            pref_en = "NANO"
            mult = 0.0000000001
        elif (swichVal == UnitsFactors.PICO): 
            pref_cyr = "П"
            pref_lat = "P"
            pref_ru = "ПИКО"
            pref_ua = "ПІКО"
            pref_en = "PICO"
            mult = 0.0000000000001
        elif (swichVal == UnitsFactors.TERA): 
            pref_cyr = "Т"
            pref_lat = "T"
            pref_ru = "ТЕРА"
            pref_ua = "ТЕРА"
            pref_en = "TERA"
            mult = (1000000000000)
        u = Unit._new1701(pref_cyr.lower() + u0.name_cyr, pref_lat.lower() + u0.name_lat, pref_ru.lower() + u0.fullname_cyr, pref_en.lower() + u0.fullname_lat, f, mult, u0, u0.kind, u0.keywords)
        if (f == UnitsFactors.MEGA or f == UnitsFactors.TERA or f == UnitsFactors.GIGA): 
            u.name_cyr = (pref_cyr + u0.name_cyr)
            u.name_lat = (pref_lat + u0.name_lat)
        UnitsHelper.UNITS.append(u)
        nams = Utils.splitString(names_ru, ';', False)
        t = Termin._new119(pref_ru + nams[0], u)
        i = 1
        while i < len(nams): 
            t.add_variant(pref_ru + nams[i], False)
            i += 1
        for n in nams: 
            t.add_variant(pref_cyr + n, False)
        for n in Utils.splitString(names_ua, ';', False): 
            t.add_variant(pref_ua + n, False)
            t.add_variant(pref_cyr + n, False)
        for n in Utils.splitString(names_en, ';', False): 
            t.add_variant(pref_en + n, False)
            t.add_variant(pref_lat + n, False)
        for n in Utils.splitString(abbr_cyr, ';', False): 
            t.add_abridge(pref_cyr + n)
        for n in Utils.splitString(abbr_lat, ';', False): 
            t.add_abridge(pref_lat + n)
        UnitsHelper.TERMINS.add(t)
        return u
    
    # static constructor for class UnitsHelper
    @staticmethod
    def _static_ctor():
        UnitsHelper.UNITS = list()
        UnitsHelper.TERMINS = TerminCollection()

UnitsHelper._static_ctor()