# Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project.
# The latest version of the code is available on the site www.pullenti.ru

import xml.etree
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Streams import MemoryStream
from pullenti.unisharp.Streams import Stream

from pullenti.ner.org.OrganizationReferent import OrganizationReferent
from pullenti.ner.org.internal.PullentiNerOrgInternalResourceHelper import PullentiNerOrgInternalResourceHelper
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis
from pullenti.ner.core.IntOntologyCollection import IntOntologyCollection
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.core.Termin import Termin
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.Analyzer import Analyzer
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.geo.GeoAnalyzer import GeoAnalyzer
from pullenti.ner.org.internal.OrgItemTypeToken import OrgItemTypeToken

class OrgGlobal:
    
    GLOBAL_ORGS = None
    
    GLOBAL_ORGS_UA = None
    
    @staticmethod
    def initialize() -> None:
        if (OrgGlobal.GLOBAL_ORGS is not None): 
            return
        OrgGlobal.GLOBAL_ORGS = IntOntologyCollection()
        org0_ = None
        oi = None
        with ProcessorService.create_empty_processor() as geo_proc: 
            geo_proc.add_analyzer(GeoAnalyzer())
            geos = dict()
            for k in range(3):
                lang = (MorphLang.RU if k == 0 else (MorphLang.EN if k == 1 else MorphLang.UA))
                name = ("Orgs_ru.dat" if k == 0 else ("Orgs_en.dat" if k == 1 else "Orgs_ua.dat"))
                dat = PullentiNerOrgInternalResourceHelper.get_bytes(name)
                if (dat is None): 
                    raise Utils.newException("Can't file resource file {0} in Organization analyzer".format(name), None)
                with MemoryStream(OrgItemTypeToken._deflate(dat)) as tmp: 
                    tmp.position = 0
                    xml0_ = None # new XmlDocument
                    xml0_ = Utils.parseXmlFromStream(tmp)
                    for x in xml0_.getroot(): 
                        org0_ = OrganizationReferent()
                        abbr = None
                        for xx in x: 
                            if (Utils.getXmlLocalName(xx) == "typ"): 
                                org0_.add_slot(OrganizationReferent.ATTR_TYPE, Utils.getXmlInnerText(xx), False, 0)
                            elif (Utils.getXmlLocalName(xx) == "nam"): 
                                org0_.add_slot(OrganizationReferent.ATTR_NAME, Utils.getXmlInnerText(xx), False, 0)
                            elif (Utils.getXmlLocalName(xx) == "epo"): 
                                org0_.add_slot(OrganizationReferent.ATTR_EPONYM, Utils.getXmlInnerText(xx), False, 0)
                            elif (Utils.getXmlLocalName(xx) == "prof"): 
                                org0_.add_slot(OrganizationReferent.ATTR_PROFILE, Utils.getXmlInnerText(xx), False, 0)
                            elif (Utils.getXmlLocalName(xx) == "abbr"): 
                                abbr = Utils.getXmlInnerText(xx)
                            elif (Utils.getXmlLocalName(xx) == "geo"): 
                                geo_ = None
                                wrapgeo1767 = RefOutArgWrapper(None)
                                inoutres1768 = Utils.tryGetValue(geos, Utils.getXmlInnerText(xx), wrapgeo1767)
                                geo_ = wrapgeo1767.value
                                if (not inoutres1768): 
                                    ar = geo_proc.process(SourceOfAnalysis(Utils.getXmlInnerText(xx)), None, lang)
                                    if (ar is not None and len(ar.entities) == 1 and (isinstance(ar.entities[0], GeoReferent))): 
                                        geo_ = (Utils.asObjectOrNull(ar.entities[0], GeoReferent))
                                        geos[Utils.getXmlInnerText(xx)] = geo_
                                    else: 
                                        pass
                                if (geo_ is not None): 
                                    org0_.add_slot(OrganizationReferent.ATTR_GEO, geo_, False, 0)
                        oi = org0_.create_ontology_item_ex(2, True, True)
                        if (oi is None): 
                            continue
                        if (abbr is not None): 
                            oi.termins.append(Termin(abbr, None, True))
                        if (k == 2): 
                            OrgGlobal.GLOBAL_ORGS_UA.add_item(oi)
                        else: 
                            OrgGlobal.GLOBAL_ORGS.add_item(oi)
        return
    
    # static constructor for class OrgGlobal
    @staticmethod
    def _static_ctor():
        OrgGlobal.GLOBAL_ORGS_UA = IntOntologyCollection()

OrgGlobal._static_ctor()