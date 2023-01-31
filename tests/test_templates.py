from routes import templates


def test_routes_html_template_exists():
    assert templates.ROUTES_HTML_TEMPLATE.exists()
