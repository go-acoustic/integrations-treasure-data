# Treasure data integration with Acoustic Campaign

This example workflow sends Audience data from Treasure Data to Acoustic Campaign on a daily basis, using [Treasure Data's Writing Job Results into SFTP](https://docs.treasuredata.com/display/public/INT/SFTP+Server+Export+Integration) with [td](https://docs.digdag.io/operators/td.html) operator.

# Prerequisites

In order to register your Acoustic Campaign sftp credentials in TreasureData, please create connection setting on [Connector UI](https://console.treasuredata.com/app/connections).

![](https://t.gyazo.com/teams/treasure-data/fc51459feff2d086df97f5f7eb8f6f72.png)

![](https://t.gyazo.com/teams/treasure-data/43dec12525f6cd0ee5ba7240bbc08892.png)

The connection name is used in the dig file.

# How to Run

First, upload the workflow project by `td wf push` command.

    # Upload
    $ td wf push td_sftp

If you want to mask setting, please set it by `td wf secrets` command. For more details, please see [digdag documentation](https://docs.digdag.io/command_reference.html#secrets)

    # Set Secrets
    $ td wf secrets --project td_sftp --set key

    # Set Secrets on your local for testing
    $ td wf secrets --local --set key

Now you can use these secrets by `${secret:}` syntax in the dig file.

You can trigger the session manually.

    # Run
    $ td wf start td_sftp td_sftp --session now

## Local mode

    # Run
    $ td wf run td_sftp.dig

# Set the database to import into


# Set the field mappings for the import

TODO


# Additional configuration

Additional parameters for `result_settings` are here.



For more details, please see Acoustic documentation

TODO - link


and [Treasure Data documentation](https://docs.treasuredata.com/display/public/INT/SFTP+Server+Export+Integration#SFTPServerExportIntegration-UsagefromCLI)

# Next Step

If you have any questions, please contact support@acoustic.com.
