# pylint: disable=E0211, E0213
# E0211: Method has no argument
# E0213: Method should have "self" as first argument


from zope.interface import Interface


class ITooltipSource(Interface):
    """Defines the Tooltip source adapter"""

    def __init__(context, request):
        """Initialize"""

    def global_condition():
        """Python condition if Source should be active.
        Returns bool or a callable object"""

    # XXX: Implement me
    # def general_tooltip_condition():
    #     """A jQuery selector to check if all following tooltips
    #     should be applied"""
    def tooltips():
        """Defines a set of dicts containing selector
        tooltiptext and an additional/optional condition"""
