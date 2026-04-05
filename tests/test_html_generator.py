from Html.htmlGenerator import HtmlGenerator


class TestHtmlGenerator:
    def setup_method(self):
        self.h = HtmlGenerator()

    def test_open_close_tag_with_attrs_and_args(self):
        result = self.h.open_close_tag("div", "id=test", ["content"])
        assert "<div id=test>" in result
        assert "content" in result
        assert "</div>" in result

    def test_open_close_tag_empty_args(self):
        result = self.h.open_close_tag("div", "")
        assert "<div >" in result
        assert "</div>" in result

    def test_open_tag(self):
        result = self.h.open_tag("img", ["src='test.png'", "alt='test'"])
        assert "<img src='test.png' alt='test'>" in result

    def test_html_tag_includes_doctype(self):
        result = self.h.html("", ["<head></head>"])
        assert "<!DOCTYPE html>" in result
        assert "<html >" in result
        assert "</html>" in result

    def test_head_tag(self):
        result = self.h.head("", ["<title>Test</title>"])
        assert "<head >" in result
        assert "<title>Test</title>" in result
        assert "</head>" in result

    def test_body_tag(self):
        result = self.h.body("", ["<p>Hello</p>"])
        assert "<body >" in result
        assert "</body>" in result

    def test_table_tag(self):
        result = self.h.table("border=1", ["<tr></tr>"])
        assert "<table border=1>" in result
        assert "</table>" in result

    def test_p_tag(self):
        result = self.h.p("id=test", ["Hello world"])
        assert "<p id=test>" in result
        assert "Hello world" in result

    def test_div_tag(self):
        result = self.h.div("class=box", ["inner"])
        assert "<div class=box>" in result

    def test_img_tag_self_closing(self):
        result = self.h.img(["src='pic.png'", "alt='pic'"])
        assert "<img src='pic.png' alt='pic'>" in result
        assert "</img>" not in result

    def test_link_tag_self_closing(self):
        result = self.h.link(["rel='stylesheet'", "href='style.css'"])
        assert "<link rel='stylesheet' href='style.css'>" in result

    def test_meta_tag_self_closing(self):
        result = self.h.meta(["charset='utf-8'"])
        assert "<meta charset='utf-8'>" in result

    def test_title_tag(self):
        result = self.h.title("", ["My Page"])
        assert "<title >" in result
        assert "My Page" in result
        assert "</title>" in result

    def test_tr_tag(self):
        result = self.h.tr("", ["<td>cell</td>"])
        assert "<tr >" in result
        assert "</tr>" in result

    def test_td_tag(self):
        result = self.h.td("colspan=2", ["data"])
        assert "<td colspan=2>" in result
        assert "data" in result

    def test_br_tag(self):
        result = self.h.br()
        assert "<br" in result

    def test_button_tag(self):
        result = self.h.button("onclick='alert()'", ["Click"])
        assert "<button onclick='alert()'>" in result
        assert "Click" in result

    def test_h1_tag(self):
        result = self.h.h1("id=title", ["Heading"])
        assert "<h1 id=title>" in result
        assert "Heading" in result

    def test_h2_tag(self):
        result = self.h.h2("", ["Sub"])
        assert "<h2 >" in result
        assert "Sub" in result

    def test_nested_tags(self):
        inner = self.h.p("", ["text"])
        result = self.h.div("", [inner])
        assert "<div >" in result
        assert "<p >" in result
        assert "text" in result
