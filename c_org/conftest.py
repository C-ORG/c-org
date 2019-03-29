import pytest
import os
import subprocess
import time
import atexit

ganache = subprocess.Popen("ganache-cli > ganache.log", shell=True)
time.sleep(5)
atexit.register(ganache.terminate)


# see https://stackoverflow.com/a/46991331/4986615
@pytest.fixture(autouse=True)
def _docdir(request):

    # Trigger ONLY for the doctests.
    doctest_plugin = request.config.pluginmanager.getplugin("doctest")
    if isinstance(request.node, doctest_plugin.DoctestItem):

        # Get the fixture dynamically by its name.
        tmpdir = request.getfixturevalue('tmpdir')
        c_org = tmpdir.mkdir('.c-org')
        vault = c_org.join("vault.yaml")
        vault.write('''infura: 'YOUR-INFURA-KEY'
wallets: []
''')
        global_file = c_org.join("global.yaml")
        global_file.write('''c-orgs: []
        ''')
        os.environ['HOME'] = str(c_org.dirpath())
        yield

    else:
        # For normal tests, we have to yield, since this is a yield-fixture.
        yield
