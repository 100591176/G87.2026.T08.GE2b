import json
import os
from unittest import TestCase

from uc3m_consulting.enterprise_manager import EnterpriseManager


class TestRegisterDocument(TestCase):
    def setUp(self):
        self.input_file = "mytest.json"
        self.output_file = "all_documents.json"

        with open(self.input_file, "w", encoding="utf-8") as file:
            file.write(
                '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
                '"FILENAME":"ABC12345.pdf"}'
            )

        with open(self.output_file, "w", encoding="utf-8") as file:
            json.dump([], file)

    def tearDown(self):
        if os.path.exists(self.input_file):
            os.remove(self.input_file)
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_tc01_valid_full_json_structure_pdf(self):
        manager = EnterpriseManager()

        value = manager.register_document(self.input_file)

        self.assertEqual(
            value,
            "509e578b15e2d70fb4976647a8e867cf2219512f6f1b954498cf91648c4eb410"
        )

        with open(self.output_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["alg"], "SHA-256")
        self.assertEqual(data[0]["typ"], "DOCUMENT")
        self.assertEqual(data[0]["project_id"], "84a2b5abfa27576259e41a033d07cee7")
        self.assertEqual(data[0]["file_name"], "ABC12345.pdf")
        self.assertEqual(
            data[0]["file_signature"],
            "509e578b15e2d70fb4976647a8e867cf2219512f6f1b954498cf91648c4eb410"
        )
        self.assertIn("register_date", data[0])