from datetime import datetime
from typing_extensions import Annotated
from sqlalchemy import (
    func,
    DateTime,
    Boolean,
    Text,
    String,
    sql,
)
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, registry

str_3 = Annotated[str, 3]
str_64 = Annotated[str, 64]


class Base(DeclarativeBase):
    registry = registry(
        type_annotation_map={
            str_3: String(3),
            str_64: String(64),
        }
    )


int_pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(DateTime
                                               , server_default=func.now()
                                               , comment='Запись создана'
                                               )]
update_at = Annotated[datetime, mapped_column(DateTime
                                              , server_default=func.now()
                                              , comment='Запись обновлена'
                                              )]
is_active = Annotated[bool, mapped_column(Boolean
                                          , server_default=sql.true()
                                          , nullable=False
                                          , comment='Запись активна'
                                          )]
hash_address = Annotated[str_64, mapped_column(comment='хеш сума адреса строки')]
hash_data = Annotated[str_64, mapped_column(comment='хеш сума данных строки')]


class Country(Base):
    __tablename__ = 'country'
    __table_args__ = (
        {"schema": "macmap",
         "comment": "Справочник стран", }
    )
    id: Mapped[int_pk]
    created_at: Mapped[created_at]
    update_at: Mapped[update_at]
    is_active: Mapped[is_active]
    hash_address: Mapped[hash_address | None]

    foreign_id: Mapped[int] = mapped_column(comment='внешний id')

    code: Mapped[str | None] = mapped_column(comment='цифровой код длинной 3 символа')
    name: Mapped[str | None] = mapped_column(comment='Название страны')
    i_s_o2: Mapped[str | None] = mapped_column(comment='буквенный код длинной 2 символа')
    i_s_o3: Mapped[str | None] = mapped_column(comment='буквенный код длинной 3 символа')
    valid_from: Mapped[datetime | None] = mapped_column(comment='действителен с')
    valid_until: Mapped[datetime | None] = mapped_column(comment='действителен до')
    language: Mapped[str | None] = mapped_column(comment='язык')


class CustomDuties(Base):
    __tablename__ = 'custom_duties'
    __table_args__ = {
        "schema": "macmap",
        "comment": "custom_duties",
    }
    id: Mapped[int_pk]
    created_at: Mapped[created_at]
    update_at: Mapped[update_at]
    is_active: Mapped[is_active]
    hash_address: Mapped[hash_address | None]

    query_id: Mapped[int] = mapped_column(comment='id запроса')

    n_t_l_c_code_label: Mapped[str | None] = mapped_column(comment='Кодовая метка NTL C')
    n_t_l_c_code_tooltip_label: Mapped[str | None] = mapped_column(comment='Метка всплывающей подсказки кода NTL C')
    n_t_l_c_description_label: Mapped[str | None] = mapped_column(comment='Этикетка с описанием NTL C')
    tariff_regime_label: Mapped[str | None] = mapped_column(comment='Обозначение тарифного режима')
    tariff_reported_label: Mapped[str | None] = mapped_column(comment='Этикетка с сообщением о тарифе')
    tariff_reported_standard_label: Mapped[str | None] = mapped_column(
        comment='Стандартная маркировка, о которой сообщается в тарифах'
    )
    tariff_ave_label: Mapped[str | None] = mapped_column(comment='Доступный тариф')
    customs_tariffs_label: Mapped[str | None] = mapped_column(comment='Этикетка таможенных тарифов')
    lbl_close: Mapped[str | None] = mapped_column(comment='Закрыть этикетку')
    max_tariff_ave: Mapped[str | None] = mapped_column(comment='Максимальный средний тариф')
    max_pref_tariff_ave: Mapped[str | None] = mapped_column(comment='Максимальный средний преференциальный тариф')
    min_pref_tariff_ave: Mapped[str | None] = mapped_column(comment='Минимальный средний преференциальный тариф')
    show_m_f_n_duties_applied: Mapped[bool] = mapped_column(comment='Показать применяемые пошлины по НБН')
    max_m_f_n_duties_applied: Mapped[str | None] = mapped_column(comment='Максимальные применяемые пошлины по НБН')
    min_tariff_ave: Mapped[str | None] = mapped_column(comment='Минимальный средений тариф')
    show_pref: Mapped[bool] = mapped_column(comment='Показать предисловие')
    show_pref_range: Mapped[bool] = mapped_column(comment='Показать диапазон предпочтений')
    show_no_a_v_e: Mapped[bool] = mapped_column(comment='Не показывай средний')
    show_non_m_f_n: Mapped[bool] = mapped_column(comment='Показывать отсутствие НБН')
    show_general: Mapped[bool] = mapped_column(comment='Показать общее')
    general_tariff: Mapped[str | None] = mapped_column(comment='Общий тариф')
    show_m_f_n_tooltip: Mapped[bool] = mapped_column(comment='Показать всплывающую подсказку о НБН')
    show_pref_tooltip: Mapped[bool] = mapped_column(comment='Показать всплывающую подсказку Pref')
    show_general_tooltip: Mapped[bool] = mapped_column(comment='Показать общую всплывающую подсказку')
    show_non_m_f_n_tooltip: Mapped[bool] = mapped_column(comment='Показано во всплывающей подсказке НБН')
    max_non_m_f_n: Mapped[str | None] = mapped_column(comment='Максимальное значение без НБН')
    tariff_regime_for_overview: Mapped[str | None] = mapped_column(comment='Тарифный режим для общего обзора')
    qty_label: Mapped[str | None] = mapped_column(comment='Этикетка с количеством')
    unit_label: Mapped[str | None] = mapped_column(comment='Метка единицы измерения')
    tariff_inside_quota_label: Mapped[str | None] = mapped_column(comment='Тариф внутри метки квоты')
    other_duties_label: Mapped[str | None] = mapped_column(comment='Другие обязанности Этикетка')
    other_duties_standard_inside_label: Mapped[str | None] = mapped_column(
        comment='Другие обязанности Стандартная внутренняя этикетка'
    )
    admin_method_label: Mapped[str | None] = mapped_column(comment='Метка метода администратора')
    year: Mapped[int | None] = mapped_column(comment='год')
    revision: Mapped[str | None] = mapped_column(comment='Пересмотр')
    reference_data: Mapped[str | None] = mapped_column(comment='Справочные данные')
    tariff_note_label: Mapped[str | None] = mapped_column(comment='Этикетка тарифной накладной')
    tariff_direction_format_label: Mapped[str | None] = mapped_column(comment='Метка формата тарифного направления')
    tariff_data_year_label: Mapped[str | None] = mapped_column(comment='Тарифные данные Годовая метка')
    tariff_regime_tooltip_label: Mapped[str | None] = mapped_column(
        comment='Ярлык всплывающей подсказки тарифного режима'
    )
    tariff_reported_tooltip_label: Mapped[str | None] = mapped_column(
        comment='Ярлык всплывающей подсказки с сообщением о тарифе'
    )
    tariff_ave_tooltip_label: Mapped[str | None] = mapped_column(
        comment='Среднее значение метки всплывающей подсказки'
    )
    show_n_t_l_code: Mapped[bool] = mapped_column(comment='Показать код NTL')
    beneficiary_list_label: Mapped[str | None] = mapped_column(comment='Ярлык списка получателей')


class CustomDutiesLevel(Base):
    __tablename__ = 'custom_duties_level'
    __table_args__ = {
        "schema": "macmap",
        "comment": "custom_duties_level",
    }
    id: Mapped[int_pk]
    created_at: Mapped[created_at]
    update_at: Mapped[update_at]
    is_active: Mapped[is_active]
    hash_address: Mapped[hash_address | None]

    query_id: Mapped[int] = mapped_column(comment='id запроса')

    n_t_l_c_code: Mapped[str | None] = mapped_column(comment='Код NTLC')
    n_t_l_c_description: Mapped[str | None] = mapped_column(comment='Описание NTLC')
    tariff_regime: Mapped[str | None] = mapped_column(comment='Тарифный режим')
    tariff_reported: Mapped[str | None] = mapped_column(comment='Указанный тариф')
    tariff_reported_standard: Mapped[str | None] = mapped_column(comment='Указанный стандарт тарифа')
    tariff_ave: Mapped[str | None] = mapped_column(comment='Средений тариф')
    qty: Mapped[str | None] = mapped_column(comment='Количество')
    unit: Mapped[str | None] = mapped_column(comment='Единица измерения')
    tariff_inside_quota: Mapped[str | None] = mapped_column(comment='Тариф внутри квоты')
    other_duties: Mapped[str | None] = mapped_column(comment='Другие обязанности')
    other_duties_standard_inside: Mapped[str | None] = mapped_column(
        comment='Другие стандартные обязанности Внутри')
    admin_method: Mapped[str | None] = mapped_column(comment='Метод администрирования')
    year: Mapped[int | None] = mapped_column(comment='год')
    revision: Mapped[str | None] = mapped_column(comment='Пересмотр')
    agreement_i_d: Mapped[int | None] = mapped_column(comment='Идентификатор соглашения')
    fta_id: Mapped[int | None] = mapped_column(comment='Идентификатор Fta')
    show_detail_link: Mapped[bool | None] = mapped_column(comment='Показать подробную ссылку')
    fta_roo_detail_link: Mapped[str | None] = mapped_column(comment='Подробная ссылка на Fta Roo')
    quota_link_label: Mapped[str | None] = mapped_column(comment='Метка ссылки на квоту')
    fta_roo_detail_link_label: Mapped[str | None] = mapped_column(comment='Ярлык подробной ссылки Fta Roo')


class Taxes(Base):
    __tablename__ = 'taxes'
    __table_args__ = {
        "schema": "macmap",
        "comment": "taxes",
    }
    id: Mapped[int_pk]
    created_at: Mapped[created_at]
    update_at: Mapped[update_at]
    is_active: Mapped[is_active]
    hash_address: Mapped[hash_address | None]

    query_id: Mapped[int] = mapped_column(comment='id запроса')

    tax_information_label: Mapped[str | None] = mapped_column(comment='Табличка с налоговой информацией')
    tax_name_label: Mapped[str | None] = mapped_column(comment='Налоговая метка')
    p_d_f_of_legislation_label: Mapped[str | None] = mapped_column(comment='PDF-Файл Законодательной надписи')
    explanation_label: Mapped[str | None] = mapped_column(comment='Пояснительная надпись')
    tax_fee_or_charge_label: Mapped[str | None] = mapped_column(comment='Обозначение налога, Сбора или надбавки')
    tax_rate_label: Mapped[str | None] = mapped_column(comment='Метка налоговой ставки')
    assessable_tax_base_label: Mapped[str | None] = mapped_column(comment='Обозначение налогооблагаемой базы')
    more_details_label: Mapped[str | None] = mapped_column(comment='Более подробная информация на этикетке')
    general_info_label: Mapped[str | None] = mapped_column(comment='Этикетка с общей информацией')
    international_classifiation_label: Mapped[str | None] = mapped_column(
        comment='Международный классификационный знак'
    )
    official_tax_name_label: Mapped[str | None] = mapped_column(comment='Официальное название такса')
    tax_description_label: Mapped[str | None] = mapped_column(comment='Этикетка с описанием налога')
    applies_on_label: Mapped[str | None] = mapped_column(comment='Наносится на этикетку')
    institution_in_charge_label: Mapped[str | None] = mapped_column(comment='Ярлык ответственного учреждения')
    legal_basis_label: Mapped[str | None] = mapped_column(comment='Юридическая основа Этикетки')
    legislation_label: Mapped[str | None] = mapped_column(comment='Законодательный ярлык')
    available_files_label: Mapped[str | None] = mapped_column(comment='Метка доступных файлов')
    validity_label: Mapped[str | None] = mapped_column(comment='Метка действительности')
    valid_from_to_label: Mapped[str | None] = mapped_column(comment='Действителен от ToLabel')
    tax_formula_label: Mapped[str | None] = mapped_column(comment='Табличка с налоговой формулой')
    covered_products_label: Mapped[str | None] = mapped_column(comment='Этикетка с покрытыми продуктами')
    not_covered_products_label: Mapped[str | None] = mapped_column(
        comment='Этикетка с продуктами, на которые не распространяется действие'
    )
    h_s_code_reporting_label: Mapped[str | None] = mapped_column(comment='Этикетка с указанием кода ТН ВЭД')
    exceptions_label: Mapped[str | None] = mapped_column(comment='Метка исключений')
    total_items_label: Mapped[str | None] = mapped_column(comment='Этикетка общего количества товаров')
    value_basics_label: Mapped[str | None] = mapped_column(comment='Метка Основы ценности')
    components_label: Mapped[str | None] = mapped_column(comment='Этикетка компонентов')
    full_text_label: Mapped[str | None] = mapped_column(comment='Полнотекстовая метка')
    last_update_label: Mapped[str | None] = mapped_column(comment='Метка последнего обновления')
    last_update: Mapped[str | None] = mapped_column(comment='Последнее обновление')
    latest_change_label: Mapped[str | None] = mapped_column(comment='Последнее изменение метки')
    currency_label: Mapped[str | None] = mapped_column(comment='Метка валюты')
    legal_reference_label: Mapped[str | None] = mapped_column(comment='Юридическая справочная этикетка')
    web_resources_label: Mapped[str | None] = mapped_column(comment='Ярлык веб-ресурсов')
    product_description_label: Mapped[str | None] = mapped_column(comment='Этикетка с описанием продукта')
    product_type_label: Mapped[str | None] = mapped_column(comment='этикетка типа продукта')
    tax_data_view_models: Mapped[str | None] = mapped_column(comment='Модели просмотра налоговых данных')


class TradeRemedy(Base):
    __tablename__ = 'trade_remedy'
    __table_args__ = {
        "schema": "macmap",
        "comment": "Торговое средство правовой защиты",
    }
    id: Mapped[int_pk]
    created_at: Mapped[created_at]
    update_at: Mapped[update_at]
    is_active: Mapped[is_active]
    hash_address: Mapped[hash_address | None]

    query_id: Mapped[int] = mapped_column(comment='id запроса')

    th_exporting_country: Mapped[str | None] = mapped_column(comment='Страна-экспортер')
    th_ntlc: Mapped[str | None] = mapped_column(comment='Этот Ntlc')
    th_n_t_l_c_description: Mapped[str | None] = mapped_column(comment='Описание Th NTLC')
    th_remedy_type: Mapped[str | None] = mapped_column(comment='Тип средства правовой защиты')
    th_remedy_status: Mapped[str | None] = mapped_column(comment='Статус средства правовой защиты')
    th_duty: Mapped[str | None] = mapped_column(comment='Этот долг')
    th_start_date: Mapped[str | None] = mapped_column(comment='Дата начала')
    th_end_date: Mapped[str | None] = mapped_column(comment='Дата окончания')
    th_document: Mapped[str | None] = mapped_column(comment='Этот документ')
    th_note: Mapped[str | None] = mapped_column(comment='Эта нота')
    th_exporting_firm: Mapped[str | None] = mapped_column(comment='Фирма-экспортер')
    trade_remedies_year: Mapped[str | None] = mapped_column(comment='Год торговых средств правовой защиты')
    collection_year: Mapped[str | None] = mapped_column(comment='Год сбора')
    reference_data: Mapped[str | None] = mapped_column(comment='Справочные данные')
    is_all_partner: Mapped[bool] = mapped_column(comment='это все Партнер')
    lbl_history: Mapped[str | None] = mapped_column(comment='История Lbl')
    lbl_learn_about_measure: Mapped[str | None] = mapped_column(comment='Я узнаю о мере')
    lbl_trade_remedies: Mapped[str | None] = mapped_column(comment='Средства правовой защиты в сфере торговли Lbl')
    lbl_close: Mapped[str | None] = mapped_column(comment='Lbl Закрыть')
    transposition_comment: Mapped[str | None] = mapped_column(comment='Комментарий к перемещению')
    trade_remedy_data: Mapped[str | None] = mapped_column(comment='Данные о средствах правовой защиты в торговле')


class NtmMeasures(Base):
    __tablename__ = 'ntm_measures'
    __table_args__ = {
        "schema": "macmap",
        "comment": "меры ntm",
    }
    id: Mapped[int_pk]
    created_at: Mapped[created_at]
    update_at: Mapped[update_at]
    is_active: Mapped[is_active]
    hash_address: Mapped[hash_address | None]

    query_id: Mapped[int] = mapped_column(comment='id запроса')

    measure_section: Mapped[str | None] = mapped_column(comment='Направление перемещения')
    measure_direction: Mapped[int | None] = mapped_column(comment='Измерьте направление')
    measure_total_count_label: Mapped[str | None] = mapped_column(comment='Метка общего количества измерений')
    measure_total_count: Mapped[int | None] = mapped_column(comment='Измерьте общее количество')
    hs_revision: Mapped[str | None] = mapped_column(comment='Пересмотр ТН ВЭД')
    ntm_classification: Mapped[str | None] = mapped_column(comment='Классификация Ntm')
    ntm_year: Mapped[int | None] = mapped_column(comment='Год выпуска Ntm')
    data_source: Mapped[str | None] = mapped_column(comment='Источник данных')
    transposition_comment: Mapped[str | None] = mapped_column(comment='Комментарий к перемещению')


class Measures(Base):
    __tablename__ = 'measures'
    __table_args__ = {
        "schema": "macmap",
        "comment": "Меры",
    }
    id: Mapped[int_pk]
    created_at: Mapped[created_at]
    update_at: Mapped[update_at]
    is_active: Mapped[is_active]
    hash_address: Mapped[hash_address | None]

    query_id: Mapped[int] = mapped_column(comment='id запроса')

    measure_section: Mapped[str | None] = mapped_column(comment='Направление перемещения')
    measure_code: Mapped[str | None] = mapped_column(comment='Код измерения')
    measure_title: Mapped[str | None] = mapped_column(comment='Название меры')
    measure_summary: Mapped[str | None] = mapped_column(comment='Краткое описание меры')
    measure_count: Mapped[int | None] = mapped_column(comment='Количество измерений')


class AllMeasures(Base):
    __tablename__ = 'all_measures'
    __table_args__ = {
        "schema": "macmap",
        "comment": "Все меры",
    }
    id: Mapped[int_pk]
    created_at: Mapped[created_at]
    update_at: Mapped[update_at]
    is_active: Mapped[is_active]
    hash_address: Mapped[hash_address | None]

    query_id: Mapped[int] = mapped_column(comment='id запроса')

    measure_section: Mapped[str | None] = mapped_column(comment='Направление перемещения')
    code: Mapped[str | None] = mapped_column(comment='Код')
    title: Mapped[str | None] = mapped_column(comment='Заглавие')
    summary: Mapped[str | None] = mapped_column(comment='Резюме')
    comment: Mapped[str | None] = mapped_column(comment='Комментарий')
    legislation_title: Mapped[str | None] = mapped_column(comment='Название законодательства')
    legislation_summary: Mapped[str | None] = mapped_column(comment='Краткое изложение законодательства')
    implementation_authority: Mapped[str | None] = mapped_column(comment='Полномочия по осуществлению')
    start_date: Mapped[str | None] = mapped_column(comment='Дата начала')
    end_date: Mapped[str | None] = mapped_column(comment='Конечная дата')
    additional_comment_country: Mapped[str | None] = mapped_column(comment='Дополнительный комментарий по стране')
    additional_comment_product: Mapped[str | None] = mapped_column(comment='Дополнительный комментарий к продукту')
    text_link: Mapped[str | None] = mapped_column(comment='Текстовая ссылка')
    web_link: Mapped[str | None] = mapped_column(comment='Веб-ссылка')
    direction: Mapped[int] = mapped_column(comment='Направление')
    hs_revision: Mapped[str | None] = mapped_column(comment='Пересмотр Тн Вэд')
    ntm_classification: Mapped[str | None] = mapped_column(comment='Классификация Ntm')
    ntm_year: Mapped[int] = mapped_column(comment='Год выпуска Ntm')
    comment_rank: Mapped[int] = mapped_column(comment='Рейтинг комментариев')
    agency: Mapped[str | None] = mapped_column(comment='Агентство')
    transposition_comm: Mapped[str | None] = mapped_column(comment='Связь с перемещением')


class Products(Base):
    __tablename__ = 'products'
    __table_args__ = {
        "schema": "macmap",
        "comment": "Список ТН ВЭД всех стран",
    }
    id: Mapped[int_pk]
    created_at: Mapped[created_at]
    update_at: Mapped[update_at]
    is_active: Mapped[is_active]
    hash_address: Mapped[hash_address | None]

    country: Mapped[str | None] = mapped_column(comment='Страна')
    code: Mapped[str | None] = mapped_column(comment='ТН ВЭД')
    name: Mapped[str | None] = mapped_column(Text, comment='Описание ТН ВЭД')
    language: Mapped[str | None] = mapped_column(comment='язык')
    name_rus: Mapped[str | None] = mapped_column(Text, comment='Описание ТН ВЭД на русском языке')
    is_plan: Mapped[is_active]


class PlanRequest(Base):
    __tablename__ = 'plan_request'
    __table_args__ = {
        "schema": "macmap",
        "comment": "План запросов",
    }
    id: Mapped[int_pk]
    created_at: Mapped[created_at]
    update_at: Mapped[update_at]
    is_active: Mapped[is_active]
    hash_address: Mapped[hash_address | None]

    reporter: Mapped[str | None] = mapped_column(comment='экспортер')
    partner: Mapped[str | None] = mapped_column(comment='импортер')
    tn_ved: Mapped[str | None] = mapped_column(comment='ТН ВЭД')
    language: Mapped[str | None] = mapped_column(comment='язык')


class TradeAgreements(Base):
    __tablename__ = 'trade_agreements'
    __table_args__ = {
        "schema": "macmap",
        "comment": "Торговые соглашения",
    }
    id: Mapped[int_pk]
    created_at: Mapped[created_at]
    update_at: Mapped[update_at]
    is_active: Mapped[is_active]
    hash_address: Mapped[hash_address | None]

    country: Mapped[str | None] = mapped_column(comment='страна')
    flow: Mapped[str | None] = mapped_column(comment='описание торговых потоков')
    fta_id: Mapped[int | None] = mapped_column(comment='номер соглашения в MacMap')
    fta_name: Mapped[str | None] = mapped_column(comment='название соглашения в MacMap')
    fta_year: Mapped[str | None] = mapped_column(comment='год соглашения')
    status_id: Mapped[int | None] = mapped_column(comment='статус соглашения')
    status_desc: Mapped[str | None] = mapped_column(comment='описание соглашения')
    status_code: Mapped[str | None] = mapped_column(comment='код статуса соглашения')
    roo_avai_lable: Mapped[bool | None] = mapped_column(comment='')
