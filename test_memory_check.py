import unittest
from memory_check import check,timestamp
NOW='2026-01-02T12:00:00Z'
def record(**changes):
    return dict({'id':'fictional-one','source_ref':'fictional-message-1','source_kind':'user_statement','scope':'preference','created_at':'2026-01-01T00:00:00Z','expires_at':'2026-02-01T00:00:00Z'},**changes)
class MemoryTests(unittest.TestCase):
    def test_valid_metadata(self):self.assertEqual(check([record()],NOW)['issues'],[])
    def test_expired(self):self.assertIn('expired',check([record(expires_at=NOW)],NOW)['issues'][0]['reasons'])
    def test_external_preference(self):self.assertIn('source_scope_mismatch',check([record(source_kind='external_claim')],NOW)['issues'][0]['reasons'])
    def test_external_reference(self):self.assertFalse(check([record(source_kind='external_claim',scope='reference')],NOW)['issues'])
    def test_future(self):self.assertIn('future_record',check([record(created_at='2026-01-03T00:00:00Z')],NOW)['issues'][0]['reasons'])
    def test_invalid_time_order(self):self.assertIn('invalid_time_order',check([record(expires_at='2025-12-01T00:00:00Z')],NOW)['issues'][0]['reasons'])
    def test_naive_time_rejected(self):
        with self.assertRaises(ValueError):timestamp('2026-01-01T00:00:00')
    def test_duplicate(self):
        with self.assertRaises(ValueError):check([record(),record()],NOW)
    def test_missing_metadata(self):
        r=record();del r['source_ref']
        with self.assertRaises(ValueError):check([r],NOW)
    def test_offset_equivalent(self):self.assertEqual(timestamp(NOW),timestamp('2026-01-02T14:00:00+02:00'))
    def test_forged_source_label_not_authenticated(self):
        # Demonstrates a known limitation: self-declared labels can pass.
        self.assertFalse(check([record(source_ref='unverified-claim')],NOW)['issues'])
if __name__=='__main__':unittest.main()
