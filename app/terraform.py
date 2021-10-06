import json
import logging
logger = logging.getLogger(__name__)


class Terraform:
    """
    Class to open and compare the users and groups terraform files.
    """
    def __init__(self, terraform_self_service_user_dicts_path, terraform_managed_groups_dicts_path):
        # Create the class attribute for the user list path.
        self.users_path = terraform_self_service_user_dicts_path
        # Create the class attribute for the group list path.
        self.groups_path = terraform_managed_groups_dicts_path
        # Create the class attribute for the user json data.
        self.users_json = self.open_user_file_return_json()
        # Create the class attribute for the group json data.
        self.groups_json = self.open_group_file_return_json()

    @staticmethod
    def open_file_path_return_json(file_path):
        """
        Method to open and return a file based on the given file path.
        :param file_path:
        :return: dict
        """
        try:
            # Open the file object
            file = open(file_path, 'r', encoding='utf-8-sig')
            logger.info(f"successfully opened the file '{file_path}'")
            # Read the file
            file = file.read()
            # Convert json into a python dict.
            file_json = json.loads(file)
            logger.info(f"successfully converted json to dict")

        except Exception as e:
            logger.exception(f"exception occurred {str(e)}")
            return

        else:
            # Return the file object.
            return file_json

    def open_user_file_return_json(self):
        # Obtain the raw user dictionary data (dictionary of dictionaries)
        raw_user_data = self.open_file_path_return_json(self.users_path)
        logger.info(f"number of users = {len(raw_user_data.get('users'))}")
        # Return all users beneath the 'users' key.
        return raw_user_data.get('users')

    def open_group_file_return_json(self):
        # Obtain the raw groups dictionary data (dictionary of dictionaries)
        raw_group_data = self.open_file_path_return_json(self.groups_path)
        logger.info(f"number of groups = {len(raw_group_data.get('groups'))}")
        # Return all groups beneath the 'groups' key.
        return raw_group_data.get('groups')

    def get_group_names(self):
        """
        Method returns a list of Terraform group names based on the
        groups dictionary data.
        """
        return list(self.groups_json)

    def get_user_names(self):
        """:var
        Method returns a list of terraform user names by calling list() on
        the stored terraform user data dictionary of dictionaries where the key is the key
        required user name.
        """
        return list(self.users_json)







