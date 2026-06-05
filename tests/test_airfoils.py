#!/usr/bin/env python3
"""
Tests to verify Airfoils class import and usage from BeaverFramework.
"""

import os
import sys

# Add the BeaverFramework path to Python path
home_dir = os.path.expanduser("~")
beaver_path = os.path.join(home_dir, "apps/beaver-framework")
if beaver_path not in sys.path:
    sys.path.insert(0, beaver_path)

from BeaverFramework.Framework.turbine_def import Airfoils, Turbine, Blade


def test_import_classes():
    """验证 Airfoils、Turbine 和 Blade 类可以正常导入。"""
    assert Airfoils is not None
    assert Turbine is not None
    assert Blade is not None


def test_create_instances():
    """验证可以从导入的类创建实例。"""
    airfoils = Airfoils()
    turbine = Turbine()
    blade = Blade()
    assert isinstance(airfoils, Airfoils)
    assert isinstance(turbine, Turbine)
    assert isinstance(blade, Blade)


def test_airfoils_methods():
    """验证 Airfoils 实例具有预期的公共方法。"""
    airfoils = Airfoils()
    methods = [m for m in dir(airfoils) if not m.startswith('_')]
    assert 'name' in methods
    assert 'reynolds' in methods


def test_turbine_methods():
    """验证 Turbine 实例具有预期的公共方法。"""
    turbine = Turbine()
    methods = [m for m in dir(turbine) if not m.startswith('_')]
    assert 'name' in methods
    assert 'power_rated' in methods


def test_blade_methods():
    """验证 Blade 实例具有预期的公共方法。"""
    blade = Blade()
    methods = [m for m in dir(blade) if not m.startswith('_')]
    assert 'name' in methods
    assert 'length' in methods
