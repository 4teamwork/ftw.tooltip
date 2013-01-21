import os
from setuptools import setup, find_packages


version = '1.1.1'
mainainter = 'Mathias Leimgruber'

tests_require = [
    'plone.testing',
    'plone.mocktestcase',
    'zope.browser',
    'zope.component',
    'zope.configuration',
    'zope.interface',
    'zope.publisher',
    'zope.traversing',
    ]

setup(name='ftw.tooltip',
      version=version,
      description="Apply tooltips dynamically",
      long_description=open("README.rst").read() + "\n" + \
          open(os.path.join("docs", "HISTORY.txt")).read(),

      # Get more strings from
      # http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Framework :: Plone :: 4.1',
        'Framework :: Plone :: 4.2',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],

      keywords='',
      author='4teamwork GmbH',
      author_email='mailto:info@4teamwork.ch',
      url='https://github.com/4teamwork/ftw.tooltip',
      license='GPL2',

      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw', ],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
        'setuptools',

        # Zope
        'Zope2',
        'zope.component',
        'zope.i18n',
        'zope.i18nmessageid',
        'zope.interface',

        # Plone
        'Products.CMFPlone',
        ],

      tests_require=tests_require,
      extras_require=dict(tests=tests_require),

      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
