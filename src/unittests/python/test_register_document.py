"""Unit tests for register_document."""
import json
import os
from unittest import TestCase

from uc3m_consulting.enterprise_manager import EnterpriseManager
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


class TestRegisterDocument(TestCase):
    """Test cases for register_document."""

    def setUp(self):
        """Prepare test input and output files."""
        self.input_file = "mytest.json"
        self.output_file = "all_documents.json"
        with open(self.output_file, "w", encoding="utf-8") as file:
            json.dump([], file)

    def tearDown(self):
        """Remove files created during each test."""
        if os.path.exists(self.input_file):
            os.remove(self.input_file)
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def _write_input(self, content: str):
        """Write the JSON content to the input file."""
        with open(self.input_file, "w", encoding="utf-8") as file:
            file.write(content)

    def _assert_valid_case(self, content: str, expected_hash: str,
                           expected_filename: str):
        """Check a valid input case and its stored output."""
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
        """Check an invalid input case and its expected exception message."""
        self._write_input(content)
        manager = EnterpriseManager()

        with self.assertRaises(EnterpriseManagementException) as cm:
            manager.register_document(self.input_file)

        self.assertEqual(str(cm.exception), expected_message)

    def test_tc01_valid_full_json_structure_pdf(self):
        """Test TC01: valid full JSON structure with .pdf extension."""
        self._assert_valid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345.pdf"}',
            "509e578b15e2d70fb4976647a8e867cf2219512f6f1b954498cf91648c4eb410",
            "ABC12345.pdf"
        )

    def test_tc02_valid_full_json_structure_docx(self):
        """Test TC02: valid full JSON structure with .docx extension."""
        self._assert_valid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345.docx"}',
            "23c534633ce8d121bb28255339c8b690098eb96723c8dc003a886b90924f4057",
            "ABC12345.docx"
        )

    def test_tc03_valid_full_json_structure_xlsx(self):
        """Test TC03: valid full JSON structure with .xlsx extension."""
        self._assert_valid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345.xlsx"}',
            "8a438d4ca0abab280c3f58468c2c223e832e2af85d9f454b0c11249d7a4bd41d",
            "ABC12345.xlsx"
        )

    def test_tc04_delete_root_node(self):
        """Test TC04: delete root node."""
        self._assert_invalid_case(
            '',
            "The file is not JSON formatted."
        )

    def test_tc05_duplicate_root_node(self):
        """Test TC05: duplicate root node."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345.xlsx"}'
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345.xlsx"}',
            "The file is not JSON formatted."
        )

    def test_tc06_delete_first_bracket(self):
        """Test TC06: delete first bracket."""
        self._assert_invalid_case(
            '"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc07_duplicate_first_bracket(self):
        """Test TC07: duplicate first bracket."""
        self._assert_invalid_case(
            '{{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc08_delete_fields(self):
        """Test TC08: delete fields."""
        self._assert_invalid_case(
            '{}',
            "JSON does not have the expected structure."
        )

    def test_tc09_duplicate_fields(self):
        """Test TC09: duplicate fields."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345.pdf""PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc10_delete_ending_bracket(self):
        """Test TC10: delete ending bracket."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345.xlsx"',
            "The file is not JSON formatted."
        )

    def test_tc11_duplicate_ending_bracket(self):
        """Test TC11: duplicate ending bracket."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345.xlsx"}}',
            "The file is not JSON formatted."
        )

    def test_tc12_modify_starting_bracket(self):
        """Test TC12: modify starting bracket."""
        self._assert_invalid_case(
            '"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345.xlsx"}',
            "The file is not JSON formatted."
        )

    def test_tc13_delete_field1(self):
        """Test TC13: delete field 1."""
        self._assert_invalid_case(
            '{,"FILENAME":"ABC12345.docx"}',
            "The file is not JSON formatted."
        )

    def test_tc14_duplicate_field1(self):
        """Test TC14: duplicate field 1."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7"'
            '"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345.docx"}',
            "The file is not JSON formatted."
        )

    def test_tc15_delete_comma(self):
        """Test TC15: delete comma."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7"'
            '"FILENAME":"ABC12345.xlsx"}',
            "The file is not JSON formatted."
        )

    def test_tc16_duplicate_comma(self):
        """Test TC16: duplicate comma."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",,'
            '"FILENAME":"ABC12345.xlsx"}',
            "The file is not JSON formatted."
        )

    def test_tc17_delete_field2(self):
        """Test TC17: delete field 2."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",}',
            "The file is not JSON formatted."
        )

    def test_tc18_duplicate_field2(self):
        """Test TC18: duplicate field 2."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345.xlsx""FILENAME":"ABC12345.xlsx"}',
            "The file is not JSON formatted."
        )

    def test_tc19_modify_ending_bracket(self):
        """Test TC19: modify ending bracket."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345.xlsx"',
            "The file is not JSON formatted."
        )

    def test_tc20_delete_labelfield1(self):
        """Test TC20: delete label field 1."""
        self._assert_invalid_case(
            '{:"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc21_duplicate_labelfield1(self):
        """Test TC21: duplicate label field 1."""
        self._assert_invalid_case(
            '{"PROJECT_ID""PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc22_delete_colon_field1(self):
        """Test TC22: delete colon in field 1."""
        self._assert_invalid_case(
            '{"PROJECT_ID""84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc23_duplicate_colon_field1(self):
        """Test TC23: duplicate colon in field 1."""
        self._assert_invalid_case(
            '{"PROJECT_ID"::"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc24_delete_valuefield1(self):
        """Test TC24: delete value field 1."""
        self._assert_invalid_case(
            '{"PROJECT_ID":,"FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc25_duplicate_valuefield1(self):
        """Test TC25: duplicate value field 1."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7"'
            '"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc26_modify_comma(self):
        """Test TC26: modify comma."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7"'
            '"FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc27_delete_labelfield2(self):
        """Test TC27: delete label field 2."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",:"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc28_duplicate_labelfield2(self):
        """Test TC28: duplicate label field 2."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME""FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc29_delete_colon_field2(self):
        """Test TC29: delete colon in field 2."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME""ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc30_duplicate_colon_field2(self):
        """Test TC30: duplicate colon in field 2."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME"::"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc31_delete_valuefield2(self):
        """Test TC31: delete value field 2."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":}',
            "The file is not JSON formatted."
        )

    def test_tc32_duplicate_valuefield2(self):
        """Test TC32: duplicate value field 2."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345.pdf""ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc33_delete_start_quotation(self):
        """Test TC33: delete start quotation."""
        self._assert_invalid_case(
            '{PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc34_duplicate_start_quotation(self):
        """Test TC34: duplicate start quotation."""
        self._assert_invalid_case(
            '{""PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc35_delete_project_id_label(self):
        """Test TC35: delete PROJECT_ID label."""
        self._assert_invalid_case(
            '{"":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "JSON does not have the expected structure."
        )

    def test_tc36_duplicate_project_id_label(self):
        """Test TC36: duplicate PROJECT_ID label."""
        self._assert_invalid_case(
            '{"PROJECT_IDPROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345.pdf"}',
            "JSON does not have the expected structure."
        )

    def test_tc37_delete_labelfield1_end_quotation(self):
        """Test TC37: delete label field 1 end quotation."""
        self._assert_invalid_case(
            '{"PROJECT_ID:"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc38_duplicate_labelfield1_end_quotation(self):
        """Test TC38: duplicate label field 1 end quotation."""
        self._assert_invalid_case(
            '{"PROJECT_ID"":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc39_modify_colon_field1(self):
        """Test TC39: modify colon in field 1."""
        self._assert_invalid_case(
            '{"PROJECT_ID""84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc40_delete_valuefield1_starting_quotation(self):
        """Test TC40: delete value field 1 starting quotation."""
        self._assert_invalid_case(
            '{"PROJECT_ID":84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc41_duplicate_valuefield1_starting_quotation(self):
        """Test TC41: duplicate value field 1 starting quotation."""
        self._assert_invalid_case(
            '{"PROJECT_ID":""84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc42_delete_value1(self):
        """Test TC42: delete value 1."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"","FILENAME":"ABC12345.pdf"}',
            "JSON data has no valid values."
        )

    def test_tc43_duplicate_value1(self):
        """Test TC43: duplicate value 1."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7'
            '84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "JSON data has no valid values."
        )

    def test_tc44_delete_valuefield1_ending_quotation(self):
        """Test TC44: delete value field 1 ending quotation."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7,"FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc45_duplicate_valuefield1_ending_quotation(self):
        """Test TC45: duplicate value field 1 ending quotation."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7"","FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc46_delete_labelfield2_starting_quotation(self):
        """Test TC46: delete label field 2 starting quotation."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc47_duplicate_labelfield2_starting_quotation(self):
        """Test TC47: duplicate label field 2 starting quotation."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",""FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc48_delete_filename_label(self):
        """Test TC48: delete FILENAME label."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","":"ABC12345.pdf"}',
            "JSON does not have the expected structure."
        )

    def test_tc49_duplicate_filename_label(self):
        """Test TC49: duplicate FILENAME label."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAMEFILENAME":"ABC12345.pdf"}',
            "JSON does not have the expected structure."
        )

    def test_tc50_delete_labelfield2_ending_quotation(self):
        """Test TC50: delete label field 2 ending quotation."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME:"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc51_duplicate_labelfield2_ending_quotation(self):
        """Test TC51: duplicate label field 2 ending quotation."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME"":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc52_modify_colon_field2(self):
        """Test TC52: modify colon in field 2."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME""ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc53_delete_valuefield2_starting_quotation(self):
        """Test TC53: delete value field 2 starting quotation."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc54_duplicate_valuefield2_starting_quotation(self):
        """Test TC54: duplicate value field 2 starting quotation."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":""ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc55_delete_value2(self):
        """Test TC55: delete value 2."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":""}',
            "JSON data has no valid values."
        )

    def test_tc56_duplicate_value2(self):
        """Test TC56: duplicate value 2."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345.pdfABC12345.pdf"}',
            "JSON data has no valid values."
        )

    def test_tc57_delete_valuefield2_ending_quotation(self):
        """Test TC57: delete value field 2 ending quotation."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf}',
            "The file is not JSON formatted."
        )

    def test_tc58_duplicate_valuefield2_ending_quotation(self):
        """Test TC58: duplicate value field 2 ending quotation."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf""}',
            "The file is not JSON formatted."
        )

    def test_tc59_modify_quotation_field1(self):
        """Test TC59: modify quotation in field 1."""
        self._assert_invalid_case(
            '{PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc60_modify_project_id_label(self):
        """Test TC60: modify PROJECT_ID label."""
        self._assert_invalid_case(
            '{"PROJ_CT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "JSON does not have the expected structure."
        )

    def test_tc61_modify_quotation_field1_end(self):
        """Test TC61: modify quotation in field 1 end."""
        self._assert_invalid_case(
            '{"PROJECT_ID:"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc62_modify_quotation_value1_start(self):
        """Test TC62: modify quotation in value 1 start."""
        self._assert_invalid_case(
            '{"PROJECT_ID":84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc63_modify_project_id_value(self):
        """Test TC63: modify PROJECT_ID value."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5_bfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "JSON data has no valid values."
        )

    def test_tc64_modify_quotation_value1_end(self):
        """Test TC64: modify quotation in value 1 end."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7,"FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc65_modify_quotation_field2_start(self):
        """Test TC65: modify quotation in field 2 start."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc66_modify_filename_label(self):
        """Test TC66: modify FILENAME label."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILE_NAM":"ABC12345.pdf"}',
            "JSON does not have the expected structure."
        )

    def test_tc67_modify_quotation_field2_end(self):
        """Test TC67: modify quotation in field 2 end."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME:"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc68_modify_quotation_value2_start(self):
        """Test TC68: modify quotation in value 2 start."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_tc69_delete_name(self):
        """Test TC69: delete name."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":".pdf"}',
            "JSON data has no valid values."
        )

    def test_tc70_duplicate_name(self):
        """Test TC70: duplicate name."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",'
            '"FILENAME":"ABC12345ABC12345.pdf"}',
            "JSON data has no valid values."
        )

    def test_tc71_delete_extension(self):
        """Test TC71: delete extension."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345"}',
            "JSON data has no valid values."
        )

    def test_tc72_duplicate_extension(self):
        """Test TC72: duplicate extension."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf.pdf"}',
            "JSON data has no valid values."
        )

    def test_tc73_modify_quotation_value2_end(self):
        """Test TC73: modify quotation in value 2 end."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf}',
            "The file is not JSON formatted."
        )

    def test_tc74_modify_name_content(self):
        """Test TC74: modify name content."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12-45.pdf"}',
            "JSON data has no valid values."
        )

    def test_tc75_modify_extension(self):
        """Test TC75: modify extension."""
        self._assert_invalid_case(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pd_"}',
            "JSON data has no valid values."
        )