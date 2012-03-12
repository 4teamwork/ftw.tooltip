from zope.configuration import xmlconfig
from plone.testing import Layer
from plone.testing import zca


class FtwTooltipZCMLLayer(Layer):
    """ZCML test layer for ftw.tooltips"""

    defaultBases = (zca.ZCML_DIRECTIVES, )

    def testSetUp(self):
        self['configurationContext'] = zca.stackConfigurationContext(
        self.get('configurationContext'))

        import ftw.tooltip.tests
        xmlconfig.file('tests.zcml', ftw.tooltip.tests,
            context=self['configurationContext'])
        import ftw.tooltip.browser
        xmlconfig.file('configure.zcml', ftw.tooltip.browser,
            context=self['configurationContext'])

    def testTearDown(self):
        del self['configurationContext']

FTWTOOLTIP_ZCML_LAYER = FtwTooltipZCMLLayer()
