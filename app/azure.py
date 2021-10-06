import logging

logger = logging.getLogger(__name__)

import json
import subprocess
import sys


class Azure:
    """
    A class to interact with MS Azure held users and groups.
    """

    def __init__(self, get_azure_users_cli_commands):
        # Create the class attribute for the Azure Cli Commands to obtain the users.
        self.get_users_azure_cli_commands = get_azure_users_cli_commands
        # Create the class attribute to store the formatted azure ad user data.
        self.azure_ad_users = self.get_azure_ad_users()

    def get_azure_ad_users(self):
        """:
        Method combines the calls to obtain and format the raw user data
        from Azure AD using the azure cli tools
        """
        # First we obtain the raw user data
        raw_azure_user_data = self.get_raw_azure_user_data()
        logger.info(f"obtained {len(raw_azure_user_data)} users.")
        # return the formatted user data.
        return self.format_raw_azure_user_data(raw_azure_user_data)

    def get_raw_azure_user_data(self):
        """
        Method obtains users from Azure using the Azure Cli Tools via subprocess.
        Data is returned as a list of lists.
        """
        try:
            get_azure_users = subprocess.run(
                # Commands To obtain the users from the azure cli tool.
                self.get_users_azure_cli_commands,
                capture_output=True, text=True, shell=True,
                timeout=30
            )
            # Inspect the returned value in case nothing was returned
            if get_azure_users.returncode != 0:
                logger.error(f"return code does not equal 0 indicating an error occurred. {get_azure_users.stderr}")
                logger.info("exiting")
                sys.exit(1)
            logger.info("success retrieving users")
            # Convert the stdout received into a dict and return.
            return json.loads(get_azure_users.stdout)

        except Exception as e:
            logger.exception(f"exception occurred {str(e)}")
            return

    @staticmethod
    def format_raw_azure_user_data(raw_azure_user_data):
        # Create a empty user dictionary to hold our users and objects.
        azure_ad_users = dict()
        # Iterate through the raw user data.
        for user in raw_azure_user_data:
            # Add a key for each user object based on SAmmAccountName.
            # [
            #     "JBlogs@devl.justice.gov.uk",
            #     "[ADM] Joe Blogs",
            #     "ccc45f09-348e-67hg-9ad4-62a1feb58e20",
            #     true
            #   ]
            #
            azure_ad_users[str(user[0].split("@")[0])] = {
                "display_name": user[1],
                "object_id": user[2],
                "account_enabled": user[3],
                "user_principle_name": user[0]
            }
        # Return the populated dictionary.
        return azure_ad_users

    def get_ad_user_account_names(self):
        """
        Method returns a list of AD account names by calling list()
        on the stored azure_ad_users dictionary of dictionaries, where the key is
        is the add account name required"""
        return list(self.azure_ad_users)
