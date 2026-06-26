from typing import List, Optional


def open_close_tag(tag: str, attrs: str, args: Optional[List[str]] = None):
    """
    Builds a paired tag wrapping its child content.

    Args:
      tag (str): The tag name (e.g. "div").
      attrs (str): The attribute string placed inside the opening tag.
      args (Optional[List[str]]): Child content joined verbatim. Defaults to none.

    Returns:
      str: The opening tag, child content, and closing tag.
    """
    if args is None:
        args = []
    return f"\n<{tag} {attrs}>\n{''.join(args)}\n</{tag}>\n"


def open_tag(tag: str, attrs: Optional[List[str]] = None):
    """
    Builds a single (void) tag with no closing tag.

    Args:
      tag (str): The tag name (e.g. "img").
      attrs (Optional[List[str]]): Attributes joined with spaces. Defaults to none.

    Returns:
      str: The opening tag.
    """
    if attrs is None:
        attrs = []
    return f"\n<{tag} {' '.join(attrs)}>\n"


def html(attrs: str, args: Optional[List[str]] = None):
    """
    Builds a full HTML document with a doctype and <html> root.

    Args:
      attrs (str): The attribute string for the <html> tag.
      args (Optional[List[str]]): Document content. Defaults to none.

    Returns:
      str: The complete HTML document.
    """
    if args is None:
        args = []
    return f"""
    <!DOCTYPE html>
    {open_close_tag("html", attrs, args)}
    """


def head(attrs: str, args: Optional[List[str]] = None):
    """
    Builds a <head> element.

    Args:
      attrs (str): The attribute string for the tag.
      args (Optional[List[str]]): Head content. Defaults to none.

    Returns:
      str: The <head> element.
    """
    return open_close_tag("head", attrs, args)


def body(attrs: str, args: Optional[List[str]] = None):
    """
    Builds a <body> element.

    Args:
      attrs (str): The attribute string for the tag.
      args (Optional[List[str]]): Body content. Defaults to none.

    Returns:
      str: The <body> element.
    """
    return open_close_tag("body", attrs, args)


def table(attrs: str, args: Optional[List[str]] = None):
    """
    Builds a <table> element.

    Args:
      attrs (str): The attribute string for the tag.
      args (Optional[List[str]]): Table content. Defaults to none.

    Returns:
      str: The <table> element.
    """
    return open_close_tag("table", attrs, args)


def p(attrs: str, args: Optional[List[str]] = None):
    """
    Builds a <p> element.

    Args:
      attrs (str): The attribute string for the tag.
      args (Optional[List[str]]): Paragraph content. Defaults to none.

    Returns:
      str: The <p> element.
    """
    return open_close_tag("p", attrs, args)


def div(attrs: str, args: Optional[List[str]] = None):
    """
    Builds a <div> element.

    Args:
      attrs (str): The attribute string for the tag.
      args (Optional[List[str]]): Div content. Defaults to none.

    Returns:
      str: The <div> element.
    """
    return open_close_tag("div", attrs, args)


def img(args: Optional[List[str]] = None):
    """
    Builds an <img> element.

    Args:
      args (Optional[List[str]]): Attributes joined with spaces. Defaults to none.

    Returns:
      str: The <img> element.
    """
    return open_tag("img", args)


def link(args: Optional[List[str]] = None):
    """
    Builds a <link> element.

    Args:
      args (Optional[List[str]]): Attributes joined with spaces. Defaults to none.

    Returns:
      str: The <link> element.
    """
    return open_tag("link", args)


def meta(args: Optional[List[str]] = None):
    """
    Builds a <meta> element.

    Args:
      args (Optional[List[str]]): Attributes joined with spaces. Defaults to none.

    Returns:
      str: The <meta> element.
    """
    return open_tag("meta", args)


def title(attrs: str, args: Optional[List[str]] = None):
    """
    Builds a <title> element.

    Args:
      attrs (str): The attribute string for the tag.
      args (Optional[List[str]]): Title text. Defaults to none.

    Returns:
      str: The <title> element.
    """
    return open_close_tag("title", attrs, args)


def tr(attrs: str, args: Optional[List[str]] = None):
    """
    Builds a <tr> (table row) element.

    Args:
      attrs (str): The attribute string for the tag.
      args (Optional[List[str]]): Row content. Defaults to none.

    Returns:
      str: The <tr> element.
    """
    return open_close_tag("tr", attrs, args)


def td(attrs: str, args: Optional[List[str]] = None):
    """
    Builds a <td> (table cell) element.

    Args:
      attrs (str): The attribute string for the tag.
      args (Optional[List[str]]): Cell content. Defaults to none.

    Returns:
      str: The <td> element.
    """
    return open_close_tag("td", attrs, args)


def h1(attrs: str, args: Optional[List[str]] = None):
    """
    Builds an <h1> heading element.

    Args:
      attrs (str): The attribute string for the tag.
      args (Optional[List[str]]): Heading content. Defaults to none.

    Returns:
      str: The <h1> element.
    """
    return open_close_tag("h1", attrs, args)
