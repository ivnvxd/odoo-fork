{
    "name": "Real Estate Ads",
    "version": "1.0",
    "website": "https://ivnv.dev",
    "author": "Andrey Ivanov",
    "description": """
        Real Estate module to show available properties
    """,
    "category": "Sales",
    "depends": ["base"],
    "data": [
        # Groups
        "security/ir.model.access.csv",
        "security/res_groups.xml",
        "security/model_access.xml",
        "security/ir_rule.xml",
        # Views
        "views/property_view.xml",
        "views/property_type_view.xml",
        "views/property_tag_view.xml",
        "views/property_offer_view.xml",
        "views/menu_items.xml",
        # Data files
        "data/estate.property.type.csv",
        # Report
        "report/property_report.xml",
        "report/report_template.xml",
    ],
    "demo": [
        "demo/property_tag.xml",
    ],
    "assets": {
        "web.assets_backend": [
            # "real_estate_ads/static/src/js/my_custom_tag.js",
            # "real_estate_ads/static/src/xml/my_custom_tag.xml",
        ],
    },
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
