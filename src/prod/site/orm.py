import sys
from src.prod.site.function import hashSum256
from src.prod.system.database import engine_sync, session_sync
from src.prod.system.models import (
    AllMeasures,
    Base,
    NtmMeasures,
    Measures,
    PlanRequest,
    Country,
    CustomDuties,
    CustomDutiesLevel,
    TradeRemedy,
    Taxes, Products, log,
)

def ormCreateTable():
    """Create Table"""
    try:
        Base.metadata.create_all(engine_sync)
        engine_sync.echo = True
    except Exception as error:
        log.error(f'def {sys._getframe().f_code.co_name}: {error}')
def updateCountry(incoming_data):
    try:
        if not incoming_data.get('language'):
            incoming_data['language'] = 'en'
        incoming_data["hash_data"] = hashSum256([i for i in incoming_data.values()])
        # it is important to match the same set of fields with the database.
        # The calculation algorithms should be the same
        incoming_data["hash_address"] = hashSum256(
            [incoming_data.get("Code"), incoming_data.get("ISO2"), incoming_data.get("ISO3")]
        )
        new_object = Country(
            hash_address=incoming_data.get('hash_address'),
            hash_data=incoming_data.get('hash_data'),
            foreign_id=incoming_data.get('Id'),
            code=incoming_data.get('Code'),
            name=incoming_data.get('Name'),
            i_s_o2=incoming_data.get('ISO2'),
            i_s_o3=incoming_data.get('ISO3'),
            valid_from=incoming_data.get('ValidFrom'),
            valid_until=incoming_data.get('ValidUntil'),
            language=incoming_data.get('language'),
        )
        with session_sync() as session:
            old_object = session.query(Country).filter_by(hash_address=new_object.hash_address).first()
            if old_object is None:
                session.add(new_object)
                session.commit()
            elif old_object.hash_data != new_object.hash_data:
                old_object.update(new_object)
    except Exception as error:
        log.exception(f'def {sys._getframe().f_code.co_name}. The database refuse to record data: {error}')


def updateProducts(incoming_data, country):
    try:
        incoming_data["country"] = country

        incoming_data["hash_data"] = hashSum256([i for i in incoming_data.values()])
        # it is important to match the same set of fields with the database.
        # The calculation algorithms should be the same
        incoming_data["hash_address"] = hashSum256([
            incoming_data.get("country"),
            incoming_data.get("Code"),
        ])
        new_object = Products(
            is_active=True,
            hash_address=incoming_data.get('hash_address'),
            hash_data=incoming_data.get('hash_data'),
            country=incoming_data.get('country'),
            code=incoming_data.get('Code'),
            name=incoming_data.get('Name'),
        )
        with session_sync() as session:
            old_object = session.query(Products).filter_by(hash_address=new_object.hash_address).first()
            if old_object is None:
                session.add(new_object)
                session.commit()
            elif old_object.hash_data != new_object.hash_data:
                old_object.update(new_object)
    except Exception as error:
        log.exception(f'def {sys._getframe().f_code.co_name}. The database refuse to record data: {error}')


def customDutiesUpdate(query_id, incoming_data):
    incoming_data["hash_data"] = hashSum256([i for i in incoming_data.values()])
    incoming_data["query_id"] = query_id
    incoming_data["hash_address"] = incoming_data["hash_data"]
    data_rec = {
        "query_id": incoming_data.get('query_id'),
        "hash_data": incoming_data.get('hash_data'),
        "hash_address": incoming_data.get('hash_address'),
        "n_t_l_c_code_label": incoming_data.get('NTLCCodeLabel'),
        "n_t_l_c_code_tooltip_label": incoming_data.get('NTLCCodeTooltipLabel'),
        "n_t_l_c_description_label": incoming_data.get('NTLCDescriptionLabel'),
        "tariff_regime_label": incoming_data.get('TariffRegimeLabel'),
        "tariff_reported_label": incoming_data.get('TariffReportedLabel'),
        "tariff_reported_standard_label": incoming_data.get('TariffReportedStandardLabel'),
        "tariff_ave_label": incoming_data.get('TariffAveLabel'),
        "customs_tariffs_label": incoming_data.get('CustomsTariffsLabel'),
        "lbl_close": incoming_data.get('LblClose'),
        "max_tariff_ave": incoming_data.get('MaxTariffAve'),
        "max_pref_tariff_ave": incoming_data.get('MaxPrefTariffAve'),
        "min_pref_tariff_ave": incoming_data.get('MinPrefTariffAve'),
        "show_m_f_n_duties_applied": incoming_data.get('ShowMFNDutiesApplied'),
        "max_m_f_n_duties_applied": incoming_data.get('MaxMFNDutiesApplied'),
        "min_tariff_ave": incoming_data.get('MinTariffAve'),
        "show_pref": incoming_data.get('ShowPref'),
        "show_pref_range": incoming_data.get('ShowPrefRange'),
        "show_no_a_v_e": incoming_data.get('ShowNoAVE'),
        "show_non_m_f_n": incoming_data.get('ShowNonMFN'),
        "show_general": incoming_data.get('ShowGeneral'),
        "general_tariff": incoming_data.get('GeneralTariff'),
        "show_m_f_n_tooltip": incoming_data.get('ShowMFNTooltip'),
        "show_pref_tooltip": incoming_data.get('ShowPrefTooltip'),
        "show_general_tooltip": incoming_data.get('ShowGeneralTooltip'),
        "show_non_m_f_n_tooltip": incoming_data.get('ShowNonMFNTooltip'),
        "max_non_m_f_n": incoming_data.get('MaxNonMFN'),
        "tariff_regime_for_overview": incoming_data.get('TariffRegimeForOverview'),
        "qty_label": incoming_data.get('QtyLabel'), "unit_label": incoming_data.get('UnitLabel'),
        "tariff_inside_quota_label": incoming_data.get('TariffInsideQuotaLabel'),
        "other_duties_label": incoming_data.get('OtherDutiesLabel'),
        "other_duties_standard_inside_label": incoming_data.get('OtherDutiesStandardInsideLabel'),
        "admin_method_label": incoming_data.get('AdminMethodLabel'),
        "year": incoming_data.get('Year'), "revision": incoming_data.get('Revision'),
        "reference_data": incoming_data.get('ReferenceData'),
        "tariff_note_label": incoming_data.get('TariffNoteLabel'),
        "tariff_direction_format_label": incoming_data.get('TariffDirectionFormatLabel'),
        "tariff_data_year_label": incoming_data.get('TariffDataYearLabel'),
        "tariff_regime_tooltip_label": incoming_data.get('TariffRegimeTooltipLabel'),
        "tariff_reported_tooltip_label": incoming_data.get('TariffReportedTooltipLabel'),
        "tariff_ave_tooltip_label": incoming_data.get('TariffAveTooltipLabel'),
        "show_n_t_l_code": incoming_data.get('ShowNTLCode'),
        "beneficiary_list_label": incoming_data.get('BeneficiaryListLabel')
    }

    try:

        with session_sync() as session:
            odj = session.query(CustomDuties).filter_by(hash_address=data_rec["hash_address"]).first()
            if odj is None:
                stmt = CustomDuties(**data_rec)
                session.add(stmt)
                session.commit()
            session.close()
    except Exception as error:
        log.exception(f'def {sys._getframe().f_code.co_name}. The database refuse to record data: {error}')


def customDutiesLevelUpdate(query_id, site_data):
    custom_duties_level = site_data["CustomDuty"]
    try:
        for incoming_data in custom_duties_level:
            incoming_data["hash_data"] = hashSum256([i for i in incoming_data.values()])
            incoming_data["query_id"] = query_id
            incoming_data["hash_address"] = hashSum256([i for i in incoming_data.values()])
            data_rec = {
                "query_id": incoming_data.get('query_id'),
                "hash_data": incoming_data.get('hash_data'),
                "hash_address": incoming_data.get('hash_address'),

                "n_t_l_c_code": incoming_data.get('NTLCCode'),
                "n_t_l_c_description": incoming_data.get('NTLCDescription'),
                "tariff_regime": incoming_data.get('TariffRegime'),
                "tariff_reported": incoming_data.get('TariffReported'),
                "tariff_reported_standard": incoming_data.get('TariffReportedStandard'),
                "tariff_ave": incoming_data.get('TariffAve'),
                "qty": incoming_data.get('Qty'),
                "unit": incoming_data.get('Unit'),
                "tariff_inside_quota": incoming_data.get('TariffInsideQuota'),
                "other_duties": incoming_data.get('OtherDuties'),
                "other_duties_standard_inside": incoming_data.get('OtherDutiesStandardInside'),
                "admin_method": incoming_data.get('AdminMethod'),
                "year": incoming_data.get('Year'),
                "revision": incoming_data.get('Revision'),
                "agreement_i_d": incoming_data.get('AgreementID'),
                "fta_id": incoming_data.get('FtaId'),
                "show_detail_link": incoming_data.get('ShowDetailLink'),
                "fta_roo_detail_link": incoming_data.get('FtaRooDetailLink'),
                "quota_link_label": incoming_data.get('QuotaLinkLabel'),
                "fta_roo_detail_link_label": incoming_data.get('FtaRooDetailLinkLabel'),
            }
            with session_sync() as session:
                odj = session.query(CustomDutiesLevel).filter_by(hash_address=data_rec["hash_address"]).first()
                if odj is None:
                    stmt = CustomDutiesLevel(**data_rec)
                    session.add(stmt)
                    session.commit()
                session.close()
    except Exception as error:
        log.exception(f'def {sys._getframe().f_code.co_name}. The database refuse to record data: {error}')


def ntmMeasuresUpdate(query_id, datadata):
    try:

        for incoming_data in datadata:
            data_rec["hash_data"] = hashSum256([i for i in data_rec.values()])
            data_rec["query_id"] = query_id
            data_rec["hash_address"] = hashSum256([i for i in data_rec.values()])
            data_rec = {
                "query_id": incoming_data.get('query_id'),
                "hash_data": incoming_data.get('hash_data'),
                "hash_address": incoming_data.get('hash_address'),

                "measure_section": incoming_data.get('MeasureSection'),
                "measure_direction": incoming_data.get('MeasureDirection'),
                "measure_total_count_label": incoming_data.get('MeasureTotalCountLabel'),
                "measure_total_count": incoming_data.get('MeasureTotalCount'),
                "hs_revision": incoming_data.get('HsRevision'),
                "ntm_classification": incoming_data.get('NtmClassification'),
                "ntm_year": incoming_data.get('NtmYear'),
                "data_source": incoming_data.get('DataSource'),
                "transposition_comment": incoming_data.get('TranspositionComment'),
            }
            with session_sync() as session:
                odj = session.query(NtmMeasures).filter_by(hash_address=data_rec["hash_address"]).first()
                if odj is None:
                    stmt = NtmMeasures(**data_rec)
                    session.add(stmt)
                    session.commit()
    except Exception as error:
        log.exception(f'def {sys._getframe().f_code.co_name}. The database refuse to record data: {error}')


def measuresUpdate(query_id, datadata):
    try:
        for i_data in datadata:
            d_data = i_data["Measures"]
            for incoming_data in d_data:
                incoming_data["hash_data"] = hashSum256([i for i in incoming_data.values()])
                incoming_data["query_id"] = query_id
                incoming_data["hash_address"] = hashSum256([i for i in incoming_data.values()])

                data_rec = {
                    "query_id": incoming_data.get('query_id'),
                    "hash_data": incoming_data.get('hash_data'),
                    "hash_address": incoming_data.get('hash_address'),

                    "measure_code": incoming_data.get('MeasureCode'),
                    "measure_title": incoming_data.get('MeasureTitle'),
                    "measure_summary": incoming_data.get('MeasureSummary'),
                    "measure_count": incoming_data.get('MeasureCount'),
                }

                with session_sync() as session:
                    odj = session.query(Measures).filter_by(hash_address=data_rec["hash_address"]).first()
                    if odj is None:
                        log.info(f'def {sys._getframe().f_code.co_name}. There is no data in the database')
                        stmt = Measures(**data_rec)
                        session.add(stmt)
                        session.commit()
    except Exception as error:
        log.exception(f'def {sys._getframe().f_code.co_name}. The database refuse to record data: {error}')


def measuresUpdate(query_id, datadata):
    try:
        for i_data in datadata:
            d_data = i_data["Measures"]
            for incoming_data in d_data:
                incoming_data["hash_data"] = hashSum256([i for i in incoming_data.values()])
                incoming_data["query_id"] = query_id
                incoming_data["hash_address"] = hashSum256([i for i in incoming_data.values()])
                data_rec = {
                    "query_id": incoming_data.get('query_id'),
                    "hash_data": incoming_data.get('hash_data'),
                    "hash_address": incoming_data.get('hash_address'),

                    "measure_code": incoming_data.get('MeasureCode'),
                    "measure_title": incoming_data.get('MeasureTitle'),
                    "measure_summary": incoming_data.get('MeasureSummary'),
                    "measure_count": incoming_data.get('MeasureCount'),
                }
                # query hash_data. This is a reference book
                with session_sync() as session:
                    odj = session.query(Measures).filter_by(hash_address=data_rec["hash_address"]).first()
                    if odj is None:
                        log.info(f'def {sys._getframe().f_code.co_name}. There is no data in the database')
                        stmt = Measures(**data_rec)
                        session.add(stmt)
                        session.commit()
    except Exception as error:
        log.exception(f'def {sys._getframe().f_code.co_name}. The database refuse to record data: {error}')


def allMeasuresUpdate(query_id, datadata):
    try:
        for i_data in datadata:
            d_data = i_data["AllMeasures"]
            for incoming_data in d_data:
                incoming_data["hash_data"] = hashSum256([i for i in incoming_data.values()])
                incoming_data["query_id"] = query_id
                incoming_data["hash_address"] = hashSum256([i for i in incoming_data.values()])

                data_rec = {
                    "query_id": incoming_data.get('query_id'),
                    "hash_data": incoming_data.get('hash_data'),
                    "hash_address": incoming_data.get('hash_address'),

                    'code': incoming_data.get('Code'),
                    "title": incoming_data.get('Title'),
                    "summary": incoming_data.get('Summary'),
                    "comment": incoming_data.get('Comment'),
                    "legislation_title": incoming_data.get('LegislationTitle'),
                    "legislation_summary": incoming_data.get('LegislationSummary'),
                    'implementation_authority': incoming_data.get('ImplementationAuthority'),
                    "start_date": incoming_data.get('StartDate'),
                    "end_date": incoming_data.get('EndDate'),
                    "additional_comment_country": incoming_data.get('AdditionalCommentProduct'),
                    "additional_comment_product": incoming_data.get('AdditionalCommentProduct'),
                    "text_link": incoming_data.get('TextLink'),
                    "web_link": incoming_data.get('WebLink'),
                    "direction": incoming_data.get('Direction'),
                    "hs_revision": incoming_data.get('HsRevision'),
                    "ntm_classification": incoming_data.get('NtmClassification'),
                    "ntm_year": incoming_data.get('NtmYear'),
                    "comment_rank": incoming_data.get('CommentRank'),
                    "agency": incoming_data.get('Agency'),
                    "transposition_comm": incoming_data.get('TranspositionComm'),
                }

                with session_sync() as session:
                    odj = session.query(AllMeasures).filter_by(hash_address=data_rec["hash_address"]).first()
                    if odj is None:
                        log.info(f'def {sys._getframe().f_code.co_name}. There is no data in the database')
                        stmt = AllMeasures(**data_rec)
                        session.add(stmt)
                        session.commit()
    except Exception as error:
        log.exception(f'def {sys._getframe().f_code.co_name}. The database refuse to record data: {error}')


def tradeRemedyUpdate(query_id, incoming_data):
    try:
        incoming_data["hash_data"] = hashSum256([i for i in incoming_data.values()])
        incoming_data["query_id"] = query_id
        incoming_data["hash_address"] = hashSum256([i for i in incoming_data.values()])
        data_rec = {
            "query_id": incoming_data.get('query_id'),
            "hash_data": incoming_data.get('hash_data'),
            "hash_address": incoming_data.get('hash_address'),

            "th_exporting_country": incoming_data.get('ThExportingCountry'),
            "th_ntlc": incoming_data.get('ThNtlc'),
            "th_n_t_l_c_description": incoming_data.get('ThNTLCDescription'),
            "th_remedy_type": incoming_data.get('ThRemedyType'),
            "th_remedy_status": incoming_data.get('ThRemedyStatus'),
            "th_duty": incoming_data.get('ThDuty'),
            "th_start_date": incoming_data.get('ThStartDate'),
            "th_end_date": incoming_data.get('ThEndDate'),
            "th_document": incoming_data.get('ThDocument'),
            "th_note": incoming_data.get('ThNote'),
            "th_exporting_firm": incoming_data.get('ThExportingFirm'),
            "trade_remedies_year": incoming_data.get('TradeRemediesYear'),
            "collection_year": incoming_data.get('CollectionYear'),
            "reference_data": incoming_data.get('ReferenceData'),
            "is_all_partner": incoming_data.get('isAllPartner'),
            "lbl_history": incoming_data.get('LblHistory'),
            "lbl_learn_about_measure": incoming_data.get('LblLearnAboutMeasure'),
            "lbl_trade_remedies": incoming_data.get('LblTradeRemedies'),
            "lbl_close": incoming_data.get('LblClose'),
            "transposition_comment": incoming_data.get('TranspositionComment'),
            "trade_remedy_data": incoming_data.get('TradeRemedyData'),
        }
        with session_sync() as session:
            odj = session.query(TradeRemedy).filter_by(hash_address=data_rec["hash_address"]).first()
            if odj is None:
                stmt = TradeRemedy(**data_rec)
                session.add(stmt)
                session.commit()
    except Exception as error:
        log.exception(f'def {sys._getframe().f_code.co_name}. The database refuse to record data: {error}')


def taxesUpdate(query_id, incoming_data, ):
    try:
        incoming_data["hash_data"] = hashSum256([i for i in incoming_data.values()])
        incoming_data["query_id"] = query_id
        incoming_data["hash_address"] = hashSum256([i for i in incoming_data.values()])

        data_rec = {
            "query_id": incoming_data.get('query_id'),
            "hash_data": incoming_data.get('hash_data'),
            "hash_address": incoming_data.get('hash_address'),

            "tax_information_label": incoming_data.get('TaxInformationLabel'),
            "tax_name_label": incoming_data.get('TaxNameLabel'),
            "p_d_f_of_legislation_label": incoming_data.get('PDFOfLegislationLabel'),
            "explanation_label": incoming_data.get('ExplanationLabel'),
            "tax_fee_or_charge_label": incoming_data.get('TaxFeeOrChargeLabel'),
            "tax_rate_label": incoming_data.get('TaxRateLabel'),
            "assessable_tax_base_label": incoming_data.get('AssessableTaxBaseLabel'),
            "more_details_label": incoming_data.get('MoreDetailsLabel'),
            "general_info_label": incoming_data.get('GeneralInfoLabel'),
            "international_classifiation_label": incoming_data.get('InternationalClassifiationLabel'),
            "official_tax_name_label": incoming_data.get('OfficialTaxNameLabel'),
            "tax_description_label": incoming_data.get('TaxDescriptionLabel'),
            "applies_on_label": incoming_data.get('AppliesOnLabel'),
            "institution_in_charge_label": incoming_data.get('InstitutionInChargeLabel'),
            "legal_basis_label": incoming_data.get('LegalBasisLabel'),
            "legislation_label": incoming_data.get('LegislationLabel'),
            "available_files_label": incoming_data.get('AvailableFilesLabel'),
            "validity_label": incoming_data.get('ValidityLabel'),
            "valid_from_to_label": incoming_data.get('ValidFromToLabel'),
            "tax_formula_label": incoming_data.get('TaxFormulaLabel'),
            "covered_products_label": incoming_data.get('CoveredProductsLabel'),
            "not_covered_products_label": incoming_data.get('NotCoveredProductsLabel'),
            "h_s_code_reporting_label": incoming_data.get('HSCodeReportingLabel'),
            "exceptions_label": incoming_data.get('ExceptionsLabel'),
            "total_items_label": incoming_data.get('TotalItemsLabel'),
            "value_basics_label": incoming_data.get('ValueBasicsLabel'),
            "components_label": incoming_data.get('ComponentsLabel'),
            "full_text_label": incoming_data.get('FullTextLabel'),
            "last_update_label": incoming_data.get('LastUpdateLabel'),
            "last_update": incoming_data.get('LastUpdate'),
            "latest_change_label": incoming_data.get('LatestChangeLabel'),
            "currency_label": incoming_data.get('CurrencyLabel'),
            "legal_reference_label": incoming_data.get('LegalReferenceLabel'),
            "web_resources_label": incoming_data.get('WebResourcesLabel'),
            "product_description_label": incoming_data.get('ProductDescriptionLabel'),
            "product_type_label": incoming_data.get('ProductTypeLabel'),
            "tax_data_view_models": incoming_data.get('TaxDataViewModels'),
        }

        with session_sync() as session:
            odj = session.query(Taxes).filter_by(hash_address=data_rec["hash_address"]).first()
            if odj is None:
                stmt = Taxes(**data_rec)
                session.add(stmt)
                session.commit()
    except Exception as error:
        log.exception(f'def {sys._getframe().f_code.co_name}. The database refuse to record data: {error}')


def checkingQueryPlan(reporter, partner, tn_ved, language='en'):
    """переделать"""
    try:
        data_rec = {
            "reporter": reporter,
            "partner": partner,
            "tn_ved": tn_ved,
            "language": language
        }
        data_rec["hash_address"] = hashSum256([i for i in data_rec.values()])
        data_rec["hash_data"] = data_rec.get("hash_address")
        with session_sync() as session:
            odj = session.query(PlanRequest).filter_by(hash_address=data_rec["hash_address"]).first()
            if odj is None:
                stmt = PlanRequest(**data_rec)
                session.add(stmt)
                session.commit()
                odj = session.query(PlanRequest).filter_by(hash_address=data_rec["hash_address"]).first()
                return odj
            elif odj.hash_data != data_rec.get("hash_data"):
                odj.reporter = data_rec.get("reporter")
                odj.partner = data_rec.get("partner")
                odj.tn_ved = data_rec.get("tn_ved")
                odj.language = data_rec.get("language")
                session.commit()
            return odj
    except Exception as error:
        log.exception(f'def {sys._getframe().f_code.co_name}. The database refuse to record data: {error}')


def getQueryPlan():
    try:
        with session_sync() as session:
            result = session.query(PlanRequest).filter_by(is_active=True)
            session.close()
            return result
    except Exception as error:
        log.exception(f'def {sys._getframe().f_code.co_name}. The database refuse to record data: {error}')


def updateQueryPlanActive(plan_id, active=False):
    """deactivating tasks"""
    try:
        with session_sync() as session:
            odj = session.get(PlanRequest, plan_id)
            odj.is_active = active
            session.add(odj)
            session.commit()
    except Exception as error:
        log.exception(f'def {sys._getframe().f_code.co_name}. No to record data: odj_id={plan_id}, error={error}')
