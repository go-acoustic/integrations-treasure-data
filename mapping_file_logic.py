import os
import sys
from datetime import datetime
from model.campaign_columns import CampaignColumns
from model.list_type import ListType
from model.list_visibility import ListVisibility

COLUMN_TYPE = 1
COLUMN_NAME = 0
CAMPAIGN_EMAIL_COLUMN_NAME = 'email'
CAMPAIGN_MINIMUM_COLUMN_LENGTH = 3

os.system(f"{sys.executable} -m pip install yattag")
from yattag import Doc, indent


def convert_to_campaign_columns(selected_columns: list) -> dict:
    converted = dict(
        map(lambda item: (item[COLUMN_NAME], map_treasure_data_type_to_campaign_data_type(item)), selected_columns.items()))
    return converted


def map_treasure_data_type_to_campaign_data_type(column_details: tuple) -> str:
    if column_details[COLUMN_NAME] == CAMPAIGN_EMAIL_COLUMN_NAME:
        return CampaignColumns.EMAIL.value
    if column_details[COLUMN_TYPE] in ['bigint', 'double', 'smallint', 'int', 'decimal', 'float']:
        return CampaignColumns.NUMERIC.value
    if column_details[COLUMN_TYPE] == 'timestamp':
        return CampaignColumns.TIMESTAMP.value
    return CampaignColumns.TEXT.value


def build_xml_columns_section(campaign_column_details: dict) -> str:
    doc, tag, text = Doc().tagtext()
    for item in campaign_column_details.items():
        with tag('COLUMN'):
            with tag('NAME'):
                text(f"{item[COLUMN_NAME]}")
            with tag('TYPE'):
                text(f"{item[COLUMN_TYPE]}")
            with tag('INCLUDE'):
                text('true')

    return doc.getvalue()


def build_xml_sync_fields_section(sync_fields: list) -> str:
    doc, tag, text = Doc().tagtext()
    for sync_field in sync_fields:
        with tag('SYNC_FIELD'):
            with tag('NAME'):
                text(f"{sync_field}")

    return doc.getvalue()


def build_xml_mappings_section(campaign_column_details: dict) -> str:
    doc, tag, text = Doc().tagtext()
    index = 1
    for item in campaign_column_details.items():
        with tag('COLUMN'):
            with tag('INDEX'):
                text(f"{index}")
            with tag('NAME'):
                text(f"{item[COLUMN_NAME]}")
            with tag('INCLUDE'):
                text('true')
        index = index + 1

    return doc.getvalue()


def build_xml_mapping_file(table_name: str, campaign_column_details: dict, action: str, list_id: str, list_type: str,
                           list_visibility: str, sync_fields: list, contact_lists: list) -> str:
    now = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    doc, tag, text = Doc().tagtext()

    with tag('LIST_IMPORT'):
        with tag('LIST_INFO'):
            with tag('ACTION'):
                text(f'{action}')
            if action == 'CREATE':
                with tag('LIST_NAME'):
                    text(f'{table_name}_{now}')
                if len(list_type) > 0:
                    list_type_enum = ListType[list_type.upper()]
                    with tag('LIST_TYPE'):
                        text(f'{list_type_enum.value}')
            else:
                with tag('LIST_ID'):
                    text(f'{list_id}')
            with tag('LIST_VISIBILITY'):
                list_visibility_enum = ListVisibility[list_visibility.upper()]
                text(f'{list_visibility_enum.value}')
            with tag('FILE_TYPE'):
                text('0')
            with tag('HASHEADERS'):
                text('true')
        if len(sync_fields) > 0:
            with tag('SYNC_FIELDS'):
                doc.asis(build_xml_sync_fields_section(sync_fields))
        with tag('COLUMNS'):
            doc.asis(build_xml_columns_section(campaign_column_details))
        with tag('MAPPING'):
            doc.asis(build_xml_mappings_section(campaign_column_details))
        if len(contact_lists) > 0:
            with tag('CONTACT_LISTS'):
                for contact_list in contact_lists:
                    with tag('CONTACT_LIST_ID'):
                        text(f'{contact_list}')

    return indent(doc.getvalue())


def validate_column_names(treasure_data_table_columns: dict, sync_fields: list[str]):
    if CAMPAIGN_EMAIL_COLUMN_NAME not in treasure_data_table_columns.keys():
        raise ValueError(f"Couldn't find defined email column name: {CAMPAIGN_EMAIL_COLUMN_NAME} in table columns:"
                         f" {treasure_data_table_columns.keys()}")

    for column_name in treasure_data_table_columns.keys():
        if len(column_name) < CAMPAIGN_MINIMUM_COLUMN_LENGTH:
            raise ValueError(f"Column name length : {column_name} should be minimum {CAMPAIGN_MINIMUM_COLUMN_LENGTH}")

    for sync_field in sync_fields:
        if sync_field not in treasure_data_table_columns.keys():
            raise ValueError(f"Couldn't find defined sync_field: {sync_field} in table columns:"
                             f" {treasure_data_table_columns.keys()}")


def generate_mapping_file(database_name: str, table_name: str, selected_columns: list, action: str, list_id: str,
                          list_type: str, list_visibility: str, sync_fields: list, contact_lists: list) -> str:
    validate_column_names(selected_columns, sync_fields)
    campaign_columns = convert_to_campaign_columns(selected_columns)
    return build_xml_mapping_file(table_name, campaign_columns, action, list_id, list_type, list_visibility, sync_fields,
                                  contact_lists)
