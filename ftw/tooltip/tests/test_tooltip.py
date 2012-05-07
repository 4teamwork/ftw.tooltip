from ftw.tooltip.testing import FTWTOOLTIP_ZCML_LAYER
from plone.mocktestcase import MockTestCase
from zope.component import getMultiAdapter, queryMultiAdapter
from zope.interface.verify import verifyClass
from zope.interface import directlyProvides
from ftw.tooltip.interfaces import  ITooltipSource
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from ftw.tooltip.demo_tooltip_source import (DemoStaticTooltipSource,
    DemoDynamicTooltipSource)
from zope.component import getGlobalSiteManager
from zope.browser.interfaces import IBrowserView
from zope.interface import Interface, implements
from zope.component import adapts


class TestTooltip(MockTestCase):

    layer = FTWTOOLTIP_ZCML_LAYER

    def setUp(self):
        self.request = self.create_dummy()
        self.response = self.mocker.mock(count=False)
        setattr(self.request, 'debug', False)
        setattr(self.request, 'response', self.response)
        self.expect(self.response.getHeader('Content-Type')).result(
            'text/javascript')
        directlyProvides(self.request, IDefaultBrowserLayer)

        self.replay()

        # register demo1 adapter
        self.gsm = getGlobalSiteManager()
        self.gsm.registerAdapter(DemoStaticTooltipSource, name="demo1")

    def test_implements_interface(self):
        self.assertTrue(ITooltipSource.implementedBy(DemoStaticTooltipSource))
        verifyClass(ITooltipSource, DemoStaticTooltipSource)

    def test_component_registered(self):
        obj = queryMultiAdapter((object(), object()),
                                ITooltipSource, name="demo1")
        self.assertEquals(obj.__class__, DemoStaticTooltipSource)

    def test_required_keys(self):
        obj = queryMultiAdapter((object(), object()),
                                ITooltipSource, name="demo1")
        tips = obj.tooltips()
        self.assertTrue(isinstance(tips, list))
        for tip in tips:
            self.assertTrue(isinstance(tip, dict))
            self.assertTrue('selector' in tip)
            self.assertTrue('text' in tip)

    def test_condition_key(self):
        # We have only one Tooltipsource
        obj = queryMultiAdapter((object(), object()),
                                ITooltipSource, name="demo1")
        tips = obj.tooltips()
        for tip in tips:
            self.assertTrue('condition' in tip)

    def test_js_view_registered(self):
        view = getMultiAdapter((object(), self.request),
                                name="dynamic_tooltips.js")
        self.assertTrue(view)

    def test_get_all_tooltip(self):
        view = getMultiAdapter((object(), self.request),
                                name="dynamic_tooltips.js")
        for name, adapter in view.get_all_tips():
            self.assertTrue(adapter.__class__.__name__ in \
                ['DemoDynamicTooltipSource', 'DemoStaticTooltipSource'])
            self.assertTrue(isinstance(name, basestring))

    def test_tooltip_js_generation(self):
        view = getMultiAdapter((object(), self.request),
                                name="dynamic_tooltips.js")
        js = view.generate_tooltip_js_source()
        self.assertEqual(
            js,
            u"""[{'selector': '#portal-logo',
'text':'This is the tooltip',
'condition': 'body'}]""")

    def test_tooltip_js_multiple_adapters_generation(self):
        # The text attr of the second adapter should be empty, because it uses
        # the title attr of the matched element
        self.gsm.registerAdapter(DemoDynamicTooltipSource, name="demo2")
        view = getMultiAdapter((object(), self.request),
                                name="dynamic_tooltips.js")
        js = view.generate_tooltip_js_source()
        self.assertEqual(
            js,
            u"""[{'selector': '#portal-globalnav li a',
'text':'',
'condition': 'body'},{'selector': '#portal-logo',
'text':'This is the tooltip',
'condition': 'body'}]""")

    def test_hole_js(self):
        view = getMultiAdapter((object(), self.request),
                                name="dynamic_tooltips.js")
        self.assertIn(view.generate_tooltip_js_source(), view())

    def test_tooltip_default_layout(self):
        view = getMultiAdapter((object(), self.request),
                                name="dynamic_tooltips.js")
        self.assertEqual(view.get_tooltip_layout(), "<div class='tooltip'/>")

    def test_tooltip_custom_layout(self):

        class ToolTipSpecifigLayout(object):
            implements(IBrowserView)
            adapts(Interface, Interface)

            def __init__(self, context, request):
                self.context = context
                self.request = request

            def __call__(self):
                return "<div class='MyToolTipCustomKlass'/>"

        self.gsm.registerAdapter(ToolTipSpecifigLayout,
                                 name="ftw_tooltip_layout")
        view = getMultiAdapter((object(), self.request),
                                name="dynamic_tooltips.js")
        self.assertEqual(view.get_tooltip_layout(),
                         "<div class=\\'MyToolTipCustomKlass\\'/>")
        self.assertIn(
            view.get_tooltip_layout(),
            view())

    def test_tooltip_custom_config(self):

        class ToolTipCustomConfig(object):
            implements(IBrowserView)
            adapts(Interface, Interface)

            def __init__(self, context, request):
                self.context = context
                self.request = request

            def __call__(self):
                return "{offset: [-10, 10]}"

        self.gsm.registerAdapter(ToolTipCustomConfig,
                                 name="ftw_tooltip_custom_config")
        view = getMultiAdapter((object(), self.request),
                               name="dynamic_tooltips.js")
        self.assertEqual(view.get_custom_config(), "{offset: [-10, 10]}")
        self.assertIn(
            view.get_custom_config(),
            view())

    def test_if_no_source_available(self):
        pass
