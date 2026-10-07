import hashlib
import pathlib
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'src'))
from audit_archive import audit


class AuditTests(unittest.TestCase):
    def make_archive(self, folder, corrupt=False):
        payload = b'FLOW_START_MILLISECONDS,FLOW_END_MILLISECONDS,Label,Attack\n0,1000,0,Benign\n2000,1000,1,Test\n'
        p = pathlib.Path(folder) / 'fixture.zip'
        digest = '0' * 40 if corrupt else hashlib.sha1(payload).hexdigest()
        with zipfile.ZipFile(p, 'w') as z:
            z.writestr('bag/data/NF-fixture.csv', payload)
            z.writestr('bag/manifest-sha1.txt', digest + ' data/NF-fixture.csv\n')
        return p

    def test_counts_and_invalid_interval(self):
        with tempfile.TemporaryDirectory() as d:
            r = audit(self.make_archive(d))
        self.assertEqual(r['rows'], 2)
        self.assertEqual(r['labels'], {'0': 1, '1': 1})
        self.assertEqual(r['invalid_intervals'], 1)
        self.assertEqual(r['day_label_counts'], {'1970-01-01|0': 1, '1970-01-01|1': 1})

    def test_reject_changed_payload(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaisesRegex(ValueError, 'Checksum mismatch'):
                audit(self.make_archive(d, corrupt=True))


if __name__ == '__main__':
    unittest.main()
