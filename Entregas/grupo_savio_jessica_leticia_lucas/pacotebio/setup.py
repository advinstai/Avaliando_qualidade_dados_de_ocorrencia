from setuptools import setup

setup(
 	name='pacotebio',
 	version = '1.0.0',
 	author = 'Leticia, Savio, Jessica, Lucas',
 	description = 'Testando',
 	url='#',
 	packages = setuptools.find_packages(),
 	license = 'N/D',
 	zip_safe = False,
 	install_requires = ['pandas', 'numpy', 'streamlit', 'reverse_geocode'], 
 	python_requires = '>=3.6'
)
