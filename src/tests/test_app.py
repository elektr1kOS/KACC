import os

from srctools import bsp


def test_app():
    assert "models/props/portal_door_combined_new.mdl" in bsp.BSP(
        os.path.join(os.getcwd(), "test_packmap.bsp")).pakfile.namelist()


test_app()
