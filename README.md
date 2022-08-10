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

# Treasure Data (TD) integration with Acoustic Campaign
1. Acoustic Campaign doesn’t allow a column name with less than 3 characters.
2. Remember that the tool will not display the password when logging in on Treasure Data. When you write it, nothing will appear on the table.

## Treasure Data configuration
### Step 1
1. Create a webhook endpoint using (Postback API) TD template https://docs.treasuredata.com/display/public/PD/Sites+and+Endpoints
    An example of an US endpoint: https://in.treasuredata.com/postback/v3/event/<workflowname>/<tablename>?td_write_key=xyz.
2.  Raise a support ticket with Acoustic to add your webhook endpoint. Please specify what events you want to subscribe to.

### Step 2
1. Once the events endpoint is set up, events will start adding to your TD account.
2. Create a Master Segment.
3. Specify Schedule: You can schedule how often the master segment should be run.
4. Add Master Table: This should be your main table.
5. Add Behaviour Table: Select the table with your events.
6. Add Attribute Table: Choose what column you want to add to your segment table.
7. Run the new segment.
8. Go to Audience Studio and choose the Master Segment that you just created.
9. You can create new Segments inside the Parent segment using the events you sent to Treasure Data.

#### If you want to push back results of your segments back to the table, use the Activation tab.
1. Create Activation.
2. Add name and description.
3. Choose authentication (See 'How to add own authentication' below if you do not have one set up).
4. Add Database and a new Table name.
5. Select mode.
6. In the Output Mapping tab you can choose mapping.
7. In the Schedule tab, you can set up a schedule for how often this segment should run and output results to the table.
8. After set up run the activation and new table should be created.
9. Set up new workflow for new table (update details of the table and action in your dig file).
10. You can do so by using command "td wf push <YOUR_PROJECT_NAME>".
11. Start workflow on TreasureData using command td wf start <YOUR_PROJECT_NAME> td_table_to_campaign --session now.

#### If you need to create a new workflow you also need to push the secrets again with this command: td wf secrets --project <YOUR_PROJECT_NAME> --set @secrets.yaml before starting the workflow.
How to add your authentication:
1. Click on https://console.treasuredata.com/app/integrations/authentications.
2. Click Catalog.
3. Find Treasure Data, and if you are setting up authentication within your account, press "continue" and name the authenticator. If you want to add data to a different account, you need to provide API Key and API hostname.
