import pytest
import os

# see https://stackoverflow.com/a/46991331/4986615
@pytest.fixture(autouse=True)
def _docdir(request):

    # Trigger ONLY for the doctests.
    doctest_plugin = request.config.pluginmanager.getplugin("doctest")
    if isinstance(request.node, doctest_plugin.DoctestItem):

        # Get the fixture dynamically by its name.
        tmpdir = request.getfuncargvalue('tmpdir')
        c_org = tmpdir.mkdir('.c-org')
        vault = c_org.join("vault.yaml")
        vault.write('''infura: 'YOUR-INFURA-KEY'
wallets: []
''')
        global_file = c_org.join("global.yaml")
        vault.write('''c-orgs: []
        ''')
        # print(vault.check())
        # print(str(vault.realpath))
        # Chdir only for the duration of the test.
        #with tmpdir.as_cwd():
        os.environ['HOME'] = str(c_org.dirpath())
        yield

    else:
        # For normal tests, we have to yield, since this is a yield-fixture.
        yield
