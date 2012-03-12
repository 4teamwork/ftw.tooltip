from Products.Five.browser import BrowserView
from zope.component import getAdapters, queryMultiAdapter
from ftw.tooltip.interfaces import ITooltipSource
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class TooltipJs(BrowserView):
    """Implements the tolltip js"""

    template = ViewPageTemplateFile('tooltip_template.js')

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
        for name, tip_adapter in self.get_all_tips():
            if tip_adapter.global_condition():
                for tooltip in tip_adapter.tooltips():
                    js_code += """{'selector': '%s',
'text':'%s',
'condition': '%s'},""" % (
                        tooltip['selector'],
                        tooltip['text'],
                        tooltip['condition'])
        if js_code.endswith(','):
            js_code = js_code[:-1]
        js_code +="]"
        return js_code

    def get_tooltip_layout(self):
        layout = queryMultiAdapter(
            (self.context, self.request), name="ftw_tooltip_layout")
        if layout is None:
            return '<div/>' # jQuery tools tooltip default layout
        return layout()
