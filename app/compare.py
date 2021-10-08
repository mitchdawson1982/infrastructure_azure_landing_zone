import logging
logger = logging.getLogger(__name__)


class Compare:
    """
    Class to carry out comparisons between the Azure and terraform data objects, to validate the
    presence of users and groups in either source.
    """
    def __init__(self, terraform, azure) -> None:
        # Create the class attribute to hold the terraform class instance.
        self.terraform = terraform
        # Create the class attribute to hold the Azure class instance.
        self.azure = azure
        # Create a placeholder for unmanaged groups in terraform.
        self.unmanaged_groups_in_terraform = list()
        # Create a placeholder for users who are not in Azure active directory.
        self.terraform_users_not_in_azure_active_directory = list()
        # Variable for group validation success.
        self.terraform_group_validation_success = False
        # Variable for user validation success.
        self.terraform_user_validation_success = False

    def check_for_unmanaged_group_in_terraform_user(self) -> None:
        """
        Method checks the groups associated with terraform users and their
         manually added group name values against valid terraform groups.
        :return:
        """
        # Obtain a list of terraform group names from the terraform.get_terraform_group_names() method.
        terraform_group_names = self.terraform.get_group_names()
        logger.info(f"obtained {len(terraform_group_names)} terraform group names")
        # Iterate through the terraform user ids and attributes by calling .items()
        # on the terraform users json.
        for userid, attribute in self.terraform.users_json.items():
            # Break out the users groups.
            user_groups = attribute['groups']
            # Check for an empty group.
            if not user_groups:
                # Continue on to the next user.
                continue
            # Iterate through the groups obtained
            for user_group in user_groups:
                # Check if the group is not present in the group_list list.
                if user_group not in terraform_group_names:
                    # Add the group to the unmanaged_groups_in_terraform list.
                    self.unmanaged_groups_in_terraform.append(user_group)

    def check_for_invalid_user_in_terraform_users(self):
        """
        Method will check the validity of users found in terraform users
        against valid entries in Azure AD.
        """
        # Obtain a list of azure ad user account names.
        azure_ad_account_names = self.azure.get_ad_user_account_names()
        logger.info(f"obtained {len(azure_ad_account_names)} azure ad account names")
        # Obtain a list of terraform user account names.
        terraform_user_names = self.terraform.get_user_names()
        logger.info(f"obtained {len(terraform_user_names)} terraform usernames")
        # Update our list of users found in terraform that are not found in azure ad.
        self.terraform_users_not_in_azure_active_directory = [
            terraform_user_name for terraform_user_name in terraform_user_names
            if terraform_user_name not in azure_ad_account_names
        ]

    def check_contents_of_unmanaged_groups_in_terraform(self) -> None:
        # Check for an empty list.
        if not self.unmanaged_groups_in_terraform:
            # Set the terraform_group_validation_success variable to True.
            self.terraform_group_validation_success = True

    def check_contents_of_terraform_users_not_in_azure_active_directory(self) -> None:
        # Check for an empty list.
        if not self.terraform_users_not_in_azure_active_directory:
            # Set the terraform_user_validation_success variable to True.
            self.terraform_user_validation_success = True

    def validate_success_criteria(self) -> None:
        # Evaluate the status of the group validation.
        if not self.terraform_group_validation_success:
            # Log validation failed
            logger.error("Group Validation Failed")
            # Iterate through the unmanaged groups.
            for group in self.unmanaged_groups_in_terraform:
                # log group name.
                logger.error(f"unmanaged group name '{group}'")
                # Log specific exit text
                logger.error("Validation_Exit_Code=1")
            # Return
            return

        # Log group validation successful.
        logger.info("Group Validation Successful")
        # Log specific text
        logger.info("Validation_Exit_Code=0")

        # Evaluate the status of the user validation.
        if not self.terraform_user_validation_success:
            # Log user validation unsuccessful
            logger.error("User Validation Failed")
            # Iterate through the users in terraform_users_not_in_azure_active_directory list.
            for user in self.terraform_users_not_in_azure_active_directory:
                logger.error(f"invalid user {user}")
            # Return
            return
        # Log user validation successful.
        logger.info("User Validation Successful")

