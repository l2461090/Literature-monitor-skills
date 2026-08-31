#!/usr/bin/env python3

import unittest

import crossref_recent as cr


class CrossrefRecentTests(unittest.TestCase):
    def test_normalize_doi(self):
        self.assertEqual(cr.normalize_doi("https://doi.org/10.1234/ABC.1?x=1"), "10.1234/abc.1")
        self.assertIsNone(cr.normalize_doi("not-a-doi"))

    def test_date_prefers_published_online(self):
        item = {
            "published-online": {"date-parts": [[2026, 8, 29]]},
            "published-print": {"date-parts": [[2027, 1, 1]]},
        }
        self.assertEqual(cr.date_from_crossref(item), ("2026-08-29", "published-online", "day"))

    def test_incomplete_date_is_not_weekly_eligible(self):
        item = {"published": {"date-parts": [[2026, 8]]}}
        self.assertEqual(cr.date_from_crossref(item), (None, "published", "month"))

    def test_exact_journal_alias_or_issn(self):
        journal = {"name": "Nature Medicine", "aliases": ["Nat Med"], "issn": ["1078-8956"]}
        self.assertTrue(cr.journal_matches({"container-title": ["Nat Med"]}, journal))
        self.assertTrue(cr.journal_matches({"container-title": ["Other"], "ISSN": ["10788956"]}, journal))
        self.assertFalse(cr.journal_matches({"container-title": ["Nature Methods"]}, journal))

    def test_deduplicate_prefers_more_complete_record(self):
        base = {
            "title": "A paper",
            "doi": "10.1234/a",
            "authors": ["A Author"],
            "publication_date": "2026-08-29",
            "publication_date_source": "published",
            "abstract": None,
        }
        better = dict(base, publication_date_source="published-online", abstract="Verified abstract")
        result = cr.deduplicate([base, better])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["abstract"], "Verified abstract")

    def test_crossref_url_uses_issn_filter(self):
        journal = {"name": "Nature Medicine", "aliases": [], "issn": ["1078-8956"]}
        url = cr.crossref_url(journal, "2026-08-23", "2026-08-30", 100, 0, None)
        self.assertIn("issn%3A1078-8956", url)

    def test_item_record_collapses_container_title_whitespace(self):
        item = {
            "title": ["A paper"],
            "container-title": ["Journal of the American\nChemical Society"],
            "DOI": "10.1021/example",
        }
        record = cr.item_to_record(item, "Journal of the American Chemical Society")
        self.assertEqual(record["journal"], "Journal of the American Chemical Society")


if __name__ == "__main__":
    unittest.main()
