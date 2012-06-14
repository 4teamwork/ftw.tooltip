from zope.component import adapts
from zope.interface import implements, Interface
from ftw.tooltip.interfaces import ITooltipSource
from ftw.tooltip import _


class DemoStaticTooltipSource(object):
    """Base demo static tooltip source. Use a given text"""

    implements(ITooltipSource)
    adapts(Interface, Interface)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def global_condition(self):
        return True

    # def general_tooltip_condition(self):
    #     return "body"

    def tooltips(self):
        return [{
            'selector': u'#portal-logo',
            'text': _(u'This is the tooltip'),
            'condition': 'body'
        }]


class DemoDynamicTooltipSource(object):
    """Base demo dynamic tooltip source. Use the title attribute
    of the matched element"""

    implements(ITooltipSource)
    adapts(Interface, Interface)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def global_condition(self):
        return True

    # def general_tooltip_condition(self):
    #     return "body"

    def tooltips(self):
        return [{
            'selector': u'#portal-globalnav li a',
            'text': u'',
            'condition': 'body'
        }]
