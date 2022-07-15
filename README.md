# Acoustic Campaign integration with Treasure Data

This treasure box can be used to set up ingest of Treasure Data audiences into Acoustic Campaign. Audiences in Treasure data will be created as Databases in Acoustic Campaign. These contacts can then be targeted in your marketing campaigns.

## Setup

1. Install TD Toolbelt: [Installing and Updating the TD Toolbelt and Treasure Agent](https://docs.treasuredata.com/display/public/PD/Installing+and+Updating+the+TD+Toolbelt+and+Treasure+Agent)
2. Log in using `td account` command and provide TD Console credentials.
3. Checkout current Treasure Box from GitHub
4. Set the following parameters in the `td_table_to_campaign.dig`:
   1. **td_database** - name of the database in TreasureData on which the SQL query will be performed
   2. **td_table_name** - name of the table in TreasureData on which the SQL query will be performed
   3. **list_type** - defines the type of database. Only specified if the ACTION is CREATE. Supported values are: DATABASE, SEED_LIST, SUPPRESSION_LIST.
   4. **list_visibility** - defines the visibility of database. Supported values are: PRIVATE or SHARED
   5. **columns_to_ignore** - a list of columns from the table to be ignored when exporting to Campaign
   6. **action** - an action which should be performed (CREATE, ADD_ONLY, UPDATE_ONLY, ADD_AND_UPDATE, OPT_OUT)
   7. **list_id** - a list_id is required for all other actions than CREATE
   8. **sync_fields** - fields on which actions: UPDATE_ONLY and ADD_AND_UPDATE will match records. Supported only for flexible databases which already exist in Campaign.
   9. **contact_lists** - specify one or more Contact List **IDs** that all contacts are added to in addition to the database. Can be used with all actions except CREATE and OPT_OUT. Supported only for list(s) and parent database which already exist in Campaign.
   10. **TD_API_SERVER** - set host (with https://) for Treasure Data API accordingly to [Sites and Endpoints](https://docs.treasuredata.com/display/public/PD/Sites+and+Endpoints) (e.g. for US https://api.treasuredata.com)
   11. **CA_API_SERVER** - set host (without https://) for Acoustic Campaign API accordingly to [Configure Acoustic Campaign Custom settings](https://help.goacoustic.com/hc/en-us/articles/360043514693-Configure-Acoustic-Campaign-Custom-settings) (e.g. api-campaign-us-2.goacoustic.com)
   12. **CA_SFTP_SERVER** - set host (without sftp://) for Campaign SFTP accordingly to [SFTP](https://help.goacoustic.com/hc/en-us/articles/360042859494-SFTP) (e.g. transfer-campaign-us-2.goacoustic.com)
5. Push Treasure Box to TreasureData using command `td wf push <YOUR_PROJECT_NAME>`
6. If you encounter the following question `Workflow module not yet installed, download now? [Y/n]` respond `Y`
7. Set secrets in the file `secrets.yaml`:  
   1. Set ca_sftp_user value as: your Acoustic Campaign username
   2. Set ca_sftp_pass value as: your Acoustic Campaign password
   3. Set ca_client_id value as: Client ID created by [Defining your API application](https://developer.goacoustic.com/acoustic-campaign/reference/getting-started-with-oauth#step-one-defining-your-api-application)
   4. Set ca_client_secret value as: ClientSecret created by [Defining your API application](https://developer.goacoustic.com/acoustic-campaign/reference/getting-started-with-oauth#step-one-defining-your-api-application)
   5. Set ca_refresh_token value as: Refresh Token created by [Get Refresh Tokens](https://developer.goacoustic.com/acoustic-campaign/reference/getting-started-with-oauth#step-two-get-refresh-tokens)
   6. Set td_apikey value as: Treasure Data master Api key, accessible on your TD Console user profile
8. Push secrets to TreasureData using command: `td wf secrets --project <YOUR_PROJECT_NAME> --set @secrets.yaml`
9. Start workflow on TreasureData using command `td wf start <YOUR_PROJECT_NAME> td_table_to_campaign --session now`

## What next

You can now use the workflow that has been created to export databases from Treasure data to Acoustic Campaign.
