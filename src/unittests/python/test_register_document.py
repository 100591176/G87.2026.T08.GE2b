import json
import os
from unittest import TestCase

from uc3m_consulting.enterprise_manager import EnterpriseManager
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


class TestRegisterDocument(TestCase):
    def setUp(self):
        self.input_file = "mytest.json"
        self.output_file = "all_documents.json"
        with open(self.output_file, "w", encoding="utf-8") as file:
            json.dump([], file)

    def tearDown(self):
        if os.path.exists(self.input_file):
            os.remove(self.input_file)
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def _write_input(self, content: str):
        with open(self.input_file, "w", encoding="utf-8") as file:
            file.write(content)

    def _assert_valid_case(self, content: str, expected_hash: str,
                           expected_filename: str):
        self._write_input(content)
        manager = EnterpriseManager()

        value = manager.register_document(self.input_file)

        self.assertEqual(value, expected_hash)

        with open(self.output_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["alg"], "SHA-256")
        self.assertEqual(data[0]["typ"], "DOCUMENT")
        self.assertEqual(data[0]["project_id"], "84a2b5abfa27576259e41a033d07cee7")
        self.assertEqual(data[0]["file_name"], expected_filename)
        self.assertEqual(data[0]["file_signature"], expected_hash)
        self.assertIn("register_date", data[0])

    def _assert_invalid_case(self, content: str, expected_message: str):
        self._write_input(content)
        manager = EnterpriseManager()

        with self.assertRaises(EnterpriseManagementException) as cm:
            manager.register_document(self.input_file)

        self.assertEqual(str(cm.exception), expected_message)

    def test_tc01_valid_full_json_structure_pdf(self):
        self._assert_valid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345.pdf"}',
            "509e578b15e2d70fb4976647a8e867cf2219512f6f1b954498cf91648c4eb410",
            "ABC12345.pdf"
        )

    def test_tc02_valid_full_json_structure_docx(self):
        self._assert_valid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345.docx"}',
            "23c534633ce8d121bb28255339c8b690098eb96723c8dc003a886b90924f4057",
            "ABC12345.docx"
        )

    def test_tc03_valid_full_json_structure_xlsx(self):
        self._assert_valid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345.xlsx"}',
            "8a438d4ca0abab280c3f58468c2c223e832e2af85d9f454b0c11249d7a4bd41d",
            "ABC12345.xlsx"
        )

    def test_tc04_delete_root_node(self):
        self._assert_invalid_case(
            '',
            "The file is not JSON formatted."
        )

    def test_tc05_duplicate_root_node(self):
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345.xlsx"}'
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345.xlsx"}',
            "The file is not JSON formatted."
        )

    def test_tc06_delete_first_bracket(self):
        self._assert_invalid_case(
            '"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc07_duplicate_first_bracket(self):
        self._assert_invalid_case(
            '{{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc08_delete_fields(self):
        self._assert_invalid_case(
            '{}',
            "JSON does not have the expected structure."
        )

    def test_tc09_duplicate_fields(self):
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345.pdf""PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc10_delete_ending_bracket(self):
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345.xlsx"',
            "The file is not JSON formatted."
        )

    def test_tc11_duplicate_ending_bracket(self):
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345.xlsx"}}',
            "The file is not JSON formatted."
        )

    def test_tc12_modify_starting_bracket(self):
        self._assert_invalid_case(
            '"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345.xlsx"}',
            "The file is not JSON formatted."
        )

    def test_tc13_delete_field1(self):
        self._assert_invalid_case(
            '{,"FILENAME":"ABC12345.docx"}',
            "The file is not JSON formatted."
        )

    def test_tc14_duplicate_field1(self):
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7"'
            '"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345.docx"}',
            "The file is not JSON formatted."
        )

    def test_tc15_delete_comma(self):
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7"'
            '"FILENAME":"ABC12345.xlsx"}',
            "The file is not JSON formatted."
        )

    def test_tc16_duplicate_comma(self):
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",,'
            '"FILENAME":"ABC12345.xlsx"}',
            "The file is not JSON formatted."
        )

    def test_tc17_delete_field2(self):
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",}',
            "The file is not JSON formatted."
        )

    def test_tc18_duplicate_field2(self):
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345.xlsx""FILENAME":"ABC12345.xlsx"}',
            "The file is not JSON formatted."
        )

    def test_tc19_modify_ending_bracket(self):
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345.xlsx"',
            "The file is not JSON formatted."
        )

    def test_tc20_delete_labelfield1(self):
        self._assert_invalid_case(
            '{:"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc21_duplicate_labelfield1(self):
        self._assert_invalid_case(
            '{"PROJECT_ID""PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc22_delete_colon_field1(self):
        self._assert_invalid_case(
            '{"PROJECT_ID""84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc23_duplicate_colon_field1(self):
        self._assert_invalid_case(
            '{"PROJECT_ID"::"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc24_delete_valuefield1(self):
        self._assert_invalid_case(
            '{"PROJECT_ID":,"FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc25_duplicate_valuefield1(self):
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7"'
            '"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc26_modify_comma(self):
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7"'
            '"FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc27_delete_labelfield2(self):
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",:"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc28_duplicate_labelfield2(self):
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME""FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc29_delete_colon_field2(self):
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME""ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc30_duplicate_colon_field2(self):
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME"::"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc31_delete_valuefield2(self):
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":}',
            "The file is not JSON formatted."
        )

    def test_tc32_duplicate_valuefield2(self):
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345.pdf""ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc33_delete_start_quotation(self):
        self._assert_invalid_case(
            '{PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc34_duplicate_start_quotation(self):
        self._assert_invalid_case(
            '{""PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc35_delete_project_id_label(self):
        self._assert_invalid_case(
            '{"":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "JSON does not have the expected structure."
        )

    def test_tc36_duplicate_project_id_label(self):
        self._assert_invalid_case(
            '{"PROJECT_IDPROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345.pdf"}',
            "JSON does not have the expected structure."
        )

