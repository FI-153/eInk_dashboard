from unittest.mock import patch


class TestHomeRoute:
    @patch("app.HtmlTemplates")
    def test_home_returns_200(self, mock_templates_cls, client):
        mock_templates_cls.return_value.home.return_value = "<html>dashboard</html>"
        response = client.get("/")
        assert response.status_code == 200
        assert b"dashboard" in response.data

    @patch("app.HtmlTemplates")
    def test_home_calls_html_templates(self, mock_templates_cls, client):
        mock_templates_cls.return_value.home.return_value = "<html></html>"
        client.get("/")
        mock_templates_cls.return_value.home.assert_called_once()


class TestFaviconRoute:
    def test_favicon_returns_200(self, client):
        response = client.get("/favicon.ico")
        assert response.status_code == 200
