from typing import List

class HtmlGenerator:

  def __init__(self):
    pass

  def open_close_tag(self, tag:str, attrs:str, args:List[str] = []):
    return f"\n<{tag} {attrs}>\n{''.join(args)}\n</{tag}>\n"
  
  def open_tag(self, tag:str, attrs:List[str] = []):
    return f"\n<{tag} {' '.join(attrs)}>\n"

  def html(self, attrs:str, args:List[str] = []):
    return f"""
    <!DOCTYPE html>
    {self.open_close_tag("html", attrs, args)}
    """
      
  def head(self, attrs:str, args:List[str] = []):
    return self.open_close_tag("head", attrs, args)
  
  def body(self, attrs:str, args:List[str] = []):
    return self.open_close_tag("body", attrs, args)
  
  def table(self, attrs:str, args:List[str] = []):
    return self.open_close_tag("table", attrs, args)
  
  def p(self, attrs:str, args:List[str] = []):
    return self.open_close_tag("p", attrs, args)
  
  def div(self, attrs:str, args:List[str] = []):
    return self.open_close_tag("div", attrs, args)
  
  def img(self, args:List[str] = []):
    return self.open_tag("img", args)

  def link(self, args:List[str] = []):
    return self.open_tag("link", args)
  
  def meta(self, args:List[str] = []):
    return self.open_tag("meta", args)

  def title(self, attrs: str, args: List[str] = []):
    return self.open_close_tag("title", attrs, args)
    
  def tr(self, attrs: str, args: List[str] = []):
    return self.open_close_tag("tr", attrs, args)
  
  def td(self, attrs:str, args:List[str] = []):
    return self.open_close_tag("td", attrs, args)
  
  def br(self):
    return self.open_tag("br", [])
  
  def button(self, attrs:str, args:List[str] = []):
    return self.open_close_tag("button", attrs, args)
  
  def h1(self, attrs:str, args:List[str] = []):
    return self.open_close_tag("h1", attrs, args)
  
  def h2(self, attrs:str, args:List[str] = []):
    return self.open_close_tag("h2", attrs, args)