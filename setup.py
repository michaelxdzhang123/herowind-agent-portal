from setuptools import setup, find_packages,Extension
#from distutils.core import setup
try:
    from Cython.Build import cythonize
except ImportError:
    cythonize = None
setup(name='Digital to wind D2W',
      version='1.1.0',
      release = "1.1.0",
      description='lubanos2 based',
      url='',
      author='Michael Zhang',
      author_email='mich@mich.com',
      license='@D2W',
      python_requires='>=3',
      packages=find_packages(),
      ackage_data={'d2w_gui':['*'],
      },

      install_requires=[
            "jsonschema",
            "graphviz",
            "scipy",
            "numpy",
            "matplotlib",
            "xarray",
            "py-wake",
            "ruamel.yaml",
            "wetb",
            "openturns",
            "shapely",
            "mplcursors",
            "nose",
            "plotly",
            "pandas" ,
            "pytest",
            "openmdao",
            "recommonmark",
        	"tqdm"
      ],
      )
