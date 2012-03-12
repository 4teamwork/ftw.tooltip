Introduction
============

With `ftw.tooltip` you are able to dynamically add tooltips to every dom
element, which is selectable by jQuery and allows the title attribute.


Installing
==========

Add `ftw.tooltip` to your buildout configuration:

::

  [instance]
  eggs =
    ftw.tooltip

Import `ftw.tooltip` default profile.


Usage
=====

Basecally you have to register named TooltipSource adapters.
They will be queried by a view, which generates the necessary JS code.

There are two example tooltip-source adapter, to show how they work
- Static text example.
- Dynamic text example, which reads the title attribute of the selected dom element.

You can load both examples on your site by register the following adapters:

::

    >>> from ftw.tooltip.demo_tooltip_source import (DemoStaticTooltipSource,
    ...    DemoDynamicTooltipSource)
    >>> from zope.component import getGlobalSiteManager
    >>> gsm = getGlobalSiteManager()
    >>> gsm.registerAdapter(DemoStaticTooltipSource, name="demo1")
    >>> gsm.registerAdapter(DemoDynamicTooltipSource, name="demo1")

Or if you are using zcml.

::
    <adapter
        factory="ftw.tooltip.demo_tooltip_source.DemoStaticTooltipSource" name="demo1" />
    <adapter
        factory="ftw.tooltip.demo_tooltip_source.DemoDynamicTooltipSource" name="demo2" />

- "demo1" puts a tooltip on #portal-logo.
- "demo2" puts tooltips on every global-nav element and show the given title attribute as tooltip.

Example
=======

It's easy to define a new TooltipSource adapters.
The following example will show a tooltip "This is the edit bar" only on
folderish types (check global_condition) and of course only if "documentEditable"
css class is available

::

    >>> from zope.component import adapts
    >>> from zope.interface import implements, Interface
    >>> from ftw.tooltip.interfaces import ITooltipSource
    >>> from plone.app.layout.navigation.interfaces import INavigationRoot
    >>> from Products.CMFCore.interfaces import IFolderish

    >>> class EditBarTooltip(object):
    ...     """Base demo static tooltip source. Use a given text"""
    ...     implements(ITooltipSource)
    ...     adapts(Interface, Interface)

    ...     def __init__(self, context, request):
    ...         self.context = context
    ...         self.request = request

    ...     def global_condition(self):
    ...         return bool(IFolderish.providedBy(self.context))

    ...     def tooltips(self):
    ...         return [{
    ...             'selector': u'#edit-bar',
    ...             'text': u'This is the edit bar',
    ...             'condition': 'div.documentEditable'}]


::
        >>> <adapter
        ...    factory="your.module.EditBarTooltip" name="my_edit_bar_tooltip" />


Links
=====

- Main github project repository: https://github.com/4teamwork/ftw.tooltip
- Issue tracker: https://github.com/4teamwork/ftw.tooltip/issues
- Package on pypi: http://pypi.python.org/pypi/ftw.tooltip
- Continuous integration: https://jenkins.4teamwork.ch/job/ftw.tooltip/

Copyright
=========

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

