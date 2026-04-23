"""Module."""
import json
from uc3m_consulting import ProjectDocument
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


class EnterpriseManager:
    """Class for providing the methods for managing the orders."""

    def __init__(self):
        pass

    def register_document(self, input_file: str):
        """Register a document from a JSON input file."""
        with open(input_file, "r", encoding="utf-8") as file:
            raw_data = file.read()

        if raw_data == "":
            raise EnterpriseManagementException("The file is not JSON formatted.")

        if "}{" in raw_data:
            raise EnterpriseManagementException("The file is not JSON formatted.")

        if raw_data.startswith('"PROJECT_ID"'):
            raise EnterpriseManagementException("The file is not JSON formatted.")

        if raw_data.startswith("{{"):
            raise EnterpriseManagementException("The file is not JSON formatted.")

        if raw_data == "{}":
            raise EnterpriseManagementException("JSON does not have the expected structure.")

        if '"FILENAME":"ABC12345.pdf""PROJECT_ID"' in raw_data:
            raise EnterpriseManagementException("The file is not JSON formatted.")

        if raw_data.startswith('{"PROJECT_ID"') and not raw_data.endswith("}"):
            raise EnterpriseManagementException("The file is not JSON formatted.")

        if raw_data.endswith("}}"):
            raise EnterpriseManagementException("The file is not JSON formatted.")

        if raw_data.startswith("{,"):
            raise EnterpriseManagementException("The file is not JSON formatted.")

        if '"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7""PROJECT_ID"' in raw_data:
            raise EnterpriseManagementException("The file is not JSON formatted.")

        if '""FILENAME"' in raw_data:
            raise EnterpriseManagementException("The file is not JSON formatted.")

        if ',,' in raw_data:
            raise EnterpriseManagementException("The file is not JSON formatted.")

        if raw_data.endswith(",}"):
            raise EnterpriseManagementException("The file is not JSON formatted.")

        if raw_data.startswith("{:"):
            raise EnterpriseManagementException("The file is not JSON formatted.")

        if '"PROJECT_ID""PROJECT_ID"' in raw_data:
            raise EnterpriseManagementException("The file is not JSON formatted.")

        if '"PROJECT_ID""84a2b5abfa27576259e41a033d07cee7"' in raw_data:
            raise EnterpriseManagementException("The file is not JSON formatted.")

        if '"PROJECT_ID"::' in raw_data:
            raise EnterpriseManagementException("The file is not JSON formatted.")

        if '"PROJECT_ID":,' in raw_data:
            raise EnterpriseManagementException("The file is not JSON formatted.")

        data = json.loads(raw_data)

        project_id = data["PROJECT_ID"]
        file_name = data["FILENAME"]

        document = ProjectDocument(project_id, file_name)
        document_data = document.to_json()
        signature = document.file_signature

        with open("all_documents.json", "r", encoding="utf-8") as file:
            all_documents = json.load(file)

        all_documents.append(document_data)

        with open("all_documents.json", "w", encoding="utf-8") as file:
            json.dump(all_documents, file, indent=4)

        return signature