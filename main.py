import os
import json
from app.terraform import Terraform
from app.azure import Azure
from app.compare import Compare
from app.create_logger import setup_logger


def main():

    # Create an instance of our logger.
    logger = setup_logger()

    # Create the json config file path.
    config_file_path = os.path.abspath(os.path.join(os.getcwd(), 'config', 'config.json'))
    # Open the config file.
    config_file = open(config_file_path, 'r', encoding='utf-8-sig').read()
    # Load the config file json.
    config = json.loads(config_file)

    # Create an instance of our Terraform class.
    terraform = Terraform(
        config.get('terraform_self_service_user_dicts_path'),
        config.get('terraform_managed_groups_dicts_path')
    )

    # Create an instance of our Azure class.
    azure = Azure(
        config.get('get_azure_users_cli_commands')
    )

    # Create an instance of our compare class.
    compare = Compare(terraform, azure)
    # Check for invalid groups in terraform.
    compare.check_for_unmanaged_group_in_terraform_user()
    # Check for invalid users in terraform.
    compare.check_for_invalid_user_in_terraform_users()
    # Check for presence of unmanaged groups in terraform.
    compare.check_contents_of_unmanaged_groups_in_terraform()
    # Check for presence of terraform users that are not in azure active directory.
    compare.check_contents_of_terraform_users_not_in_azure_active_directory()
    # Validate the overall success criteria.
    compare.validate_success_criteria()


if __name__ == "__main__":
    main()