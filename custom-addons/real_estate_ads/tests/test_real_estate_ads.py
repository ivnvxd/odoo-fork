from odoo.tests.common import TransactionCase


class TestRealEstateAds(TransactionCase):
    def setUp(self):
        super(TestRealEstateAds, self).setUp()
        self.RealEstateAd = self.env["estate.property"]
        self.test_ad_data = {
            "name": "Test Property",
            "description": "Test Description",
            "expected_price": 100,
            "sales_id": 2,
        }

    def test_create_ad(self):
        ad = self.RealEstateAd.create(self.test_ad_data)
        self.assertEqual(ad.name, "Test Property")
        self.assertEqual(ad.description, "Test Description")
        self.assertEqual(ad.expected_price, 100)

    def test_update_ad(self):
        ad = self.RealEstateAd.create(self.test_ad_data)
        ad.write({"expected_price": 110})
        self.assertEqual(ad.expected_price, 110)

    def test_search_ad(self):
        self.RealEstateAd.create(self.test_ad_data)
        ads = self.RealEstateAd.search([("name", "=", "Test Property")])
        self.assertEqual(len(ads), 1)
        self.assertEqual(ads.description, "Test Description")
