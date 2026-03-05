import unittest
import os
import shutil
from socru.Schemas  import Schemas

class TestSchemas(unittest.TestCase):

    def test_schemas(self):
        s = Schemas(False)
        self.assertTrue( len(s.all_available()) > 4)

    def test_database_directory_returns_path_for_known_species(self):
        s = Schemas(False)
        species = sorted(s.all_available())[0]
        db_dir = s.database_directory(None, species)
        self.assertIsNotNone(db_dir)
        self.assertTrue(os.path.isdir(db_dir))

    def test_database_directory_unknown_species_returns_none(self):
        s = Schemas(False)
        db_dir = s.database_directory(None, 'not_a_real_species_xyz_abc')
        self.assertIsNone(db_dir)

    def test_database_directory_custom_db_dir_overrides_default(self):
        s = Schemas(False)
        # Point at the bundled data dir directly so the species will resolve
        bundled_data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        species = sorted(s.all_available())[0]
        db_dir = s.database_directory(bundled_data_dir, species)
        self.assertIsNotNone(db_dir)
        self.assertTrue(os.path.isdir(db_dir))

        