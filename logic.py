import tdclient
from sql_query_logic import execute_sql_and_get_csv
from sftp_client import upload_file_to_sftp
from mapping_file_logic import generate_mapping_file
from campaign_api import get_token, bulk_import
from model.action import Action
from model.list_type import ListType
from model.list_visibility import ListVisibility

MAPPING_FILE = "mapping_file.xml"
SOURCE_FILE = "database.csv"
COLUMN_TYPE = 1
COLUMN_NAME = 0

def validate_action(action: str):
    if len(action) == 0:
        raise ValueError("Parameter action is required")
    try:
        Action[action.upper()]
    except KeyError:
        raise ValueError(f"Parameter action has incorrect value: {action}")


def validate_list_type(list_type: str):
    if len(list_type) > 0:
        try:
            ListType[list_type.upper()]
        except KeyError:
            raise ValueError(f"Parameter list_type has incorrect value: {list_type}")


def validate_list_visibility(list_visibility: str):
    if len(list_visibility) > 0:
        try:
            ListVisibility[list_visibility.upper()]
        except KeyError:
            raise ValueError(f"Parameter list_visibility has incorrect value: {list_visibility}")


def validate_is_list_id_set_when_action_other_than_create(action: str, list_id: str):
    if action.casefold() == 'CREATE'.casefold():
        return
    if len(list_id) < 1:
        raise ValueError(f"When action is other than create : {action}, list_id should be set")


def validate_is_contact_lists_set_with_other_action_than_create(action: str, contact_lists: list):
    if action.casefold() == 'OPT_OUT'.casefold() and len(contact_lists) > 0:
        raise ValueError(f"Contact lists cannot be used when action is OPT_OUT")


def validate_is_opt_out_with_list_id(action: str, list_id: str):
    if action.casefold() == 'OPT_OUT'.casefold() and len(list_id) == 0:
        raise ValueError(f"Parameter list_id is required for action OPT_OUT")


def import_table_to_campaign(td_database, td_table_name, columns_to_ignore, action, list_id='', list_type='',
                             list_visibility ='', sync_fields=[], contact_lists=[]):
    validate_action(action)
    validate_list_type(list_type)
    validate_list_visibility(list_visibility)
    validate_is_list_id_set_when_action_other_than_create(action, list_id)
    validate_is_contact_lists_set_with_other_action_than_create(action, contact_lists)
    validate_is_opt_out_with_list_id(action, list_id)

    selected_columns = get_treasure_data_table_column_details(td_database, td_table_name, columns_to_ignore)
    generate_and_upload_source_file_to_ftp(td_database, td_table_name, selected_columns)
    generate_and_upload_mapping_file_to_ftp(selected_columns, td_database, td_table_name, action, list_id, list_type,
                                            list_visibility, sync_fields, contact_lists)
    trigger_campaign_import()


def get_treasure_data_table_column_details(database: str, table: str, columns_to_ignore: list) -> dict:
    column_details = {}
    with tdclient.Client() as client:
        job = client.query(database, f"show columns from {table}", type='presto')
        job.wait()
        for row in job.result():
            if row[COLUMN_NAME] not in columns_to_ignore:
                column_details[row[COLUMN_NAME]] = row[COLUMN_TYPE]

    return column_details


def trigger_campaign_import():
    token = get_token()
    bulk_import(token, SOURCE_FILE, MAPPING_FILE)


def generate_and_upload_mapping_file_to_ftp(selected_columns, td_database, td_table_name, action, list_id, list_type,
                                            list_visibility, sync_fields, contact_lists):
    mapping_file_content = generate_mapping_file(td_database, td_table_name, selected_columns, action, list_id,
                                                 list_type, list_visibility, sync_fields, contact_lists)
    upload_file_to_sftp('/upload', MAPPING_FILE, mapping_file_content)


def generate_and_upload_source_file_to_ftp(td_database, td_table_name, selected_columns):
    selected_columns_by_commas = ",".join(selected_columns)
    csv = execute_sql_and_get_csv(td_database, f"select {selected_columns_by_commas} from {td_table_name}")
    upload_file_to_sftp('/upload', SOURCE_FILE, csv)
