from Products.Five.browser import BrowserView
from zope.component import getAdapters, queryMultiAdapter
from ftw.tooltip.interfaces import ITooltipSource
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.i18nmessageid.message import Message
from zope.i18n import translate


class TooltipJs(BrowserView):
    """Implements the tolltip js"""

    template = ViewPageTemplateFile('tooltip_template.js.pt')

    def __call__(self):
        """Returns the js code directly"""
        return self.template()

    def get_all_tips(self):
        """Return all tips"""
        tips_adapters = getAdapters(
            (self.context, self.request), ITooltipSource)
        return tips_adapters

    def generate_tooltip_js_source(self):
        js_code = "["
        for _name, tip_adapter in self.get_all_tips():
            if tip_adapter.global_condition():
                for tooltip in tip_adapter.tooltips():
                    text = tooltip['text']
                    if isinstance(text, Message):
                        text = translate(
                            text,
                            domain=text.domain,
                            context=self.request)
                    js_code += """{'selector': '%s',
'text':'%s',
'condition': '%s'},""" % (
                        tooltip['selector'],
                        text,
                        tooltip['condition'])
        if js_code.endswith(','):
            js_code = js_code[:-1]
        js_code += "]"
        return js_code

    def get_tooltip_layout(self):
        layout = queryMultiAdapter(
            (self.context, self.request), name="ftw_tooltip_layout")
        if layout is None:
            return "<div class='tooltip'/>"  # Tooltip default layout
        return layout().replace("'", r"\'").replace('"', r'\"')

    def get_custom_config(self):
        config = queryMultiAdapter(
            (self.context, self.request), name="ftw_tooltip_custom_config")
        if config is None:
            return "{}"  # jQuery tools tooltip default layout
        return config()
