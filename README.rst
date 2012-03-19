Introduction
============

With ``ftw.tooltip`` you are able to dynamically add tooltips to every DOM
element, which is selectable by jQuery and allows the title attribute.


Installing
==========

Add ``ftw.tooltip`` to your buildout configuration:

::

  [instance]
  eggs =
    ftw.tooltip

Import ``ftw.tooltip`` default profile.


Usage
=====

Basically you have to register named ``ITooltipSource`` adapters.
They will be queried by a view, which generates the necessary JS code.

There are two example tooltip-source adapter, to show how they work

- Static text example.
- Dynamic text example, which reads the title attribute of the selected DOM element.

You can load both examples on your site by register the following adapters::

    >>> from ftw.tooltip.demo_tooltip_source import (DemoStaticTooltipSource,
    ...    DemoDynamicTooltipSource)
    >>> from zope.component import provideAdapter
    >>> provideAdapter(DemoStaticTooltipSource, name="demo1")
    >>> provideAdapter(DemoDynamicTooltipSource, name="demo2")


Or if you are using zcml::

    <adapter
        factory="ftw.tooltip.demo_tooltip_source.DemoStaticTooltipSource" name="demo1" />
    <adapter
        factory="ftw.tooltip.demo_tooltip_source.DemoDynamicTooltipSource" name="demo2" />

- "demo1" puts a tooltip on #portal-logo.
- "demo2" puts tooltips on every global-nav element and show the given title attribute as tooltip.

Example
=======

It's easy to define a new ``ITooltipSource`` adapter.
The following example will show a tooltip "This is the edit bar" only on
folderish types (check global_condition) and of course only if "documentEditable"
css class is available::

    >>> from zope.component import adapts
    >>> from zope.interface import implements, Interface
    >>> from ftw.tooltip.interfaces import ITooltipSource
    >>> from plone.app.layout.navigation.interfaces import INavigationRoot
    >>> from Products.CMFCore.interfaces import IFolderish

    >>> class EditBarTooltip(object):
    ...     """Base demo static tooltip source. Use a given text"""
    ...     implements(ITooltipSource)
    ...     adapts(Interface, Interface)
    ...
    ...     def __init__(self, context, request):
    ...         self.context = context
    ...         self.request = request
    ...
    ...     def global_condition(self):
    ...         return bool(IFolderish.providedBy(self.context))
    ...
    ...     def tooltips(self):
    ...         return [{
    ...             'selector': u'#edit-bar',
    ...             'text': u'This is the edit bar',
    ...             'condition': 'div.documentEditable'}]


Register the adapter with ZCML::

    >>> <adapter
    ...    factory="your.module.EditBarTooltip" name="my_edit_bar_tooltip" />


You may want to use your own tooltip layout:
Just register a BrowserView named "ftw_tooltip_layout" and return the tooltip layout you prefere.

Or you can fully customize the tooltip paramters by register a BrowserView
named "ftw_tooltip_custom_config" - check jquerytools documentation for more details.

Small customization example::

    {
        offset: [-10, 10],
        position: 'right center',
        opacity: '0.7',
    }



Links
=====

- Main github project repository: https://github.com/4teamwork/ftw.tooltip
- Issue tracker: https://github.com/4teamwork/ftw.tooltip/issues
- Package on pypi: http://pypi.python.org/pypi/ftw.tooltip
- Continuous integration: https://jenkins.4teamwork.ch/job/ftw.tooltip/

Copyright
=========

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.tooltip`` is licensed under GNU General Public License, version 2.
