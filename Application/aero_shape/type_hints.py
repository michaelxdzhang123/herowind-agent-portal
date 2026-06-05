"""
Type hints and autocomplete helpers for the blade-ai application
"""

from typing import Dict, List, Optional, Any, Union
import os

# Type hints for environment variables
USER_NAME: str
BBS_BASE: str
RUN_BASE: str
SYS_LOG: str

# Type hints for imported classes
class Airfoils:
    """Airfoils class from BeaverFramework.Framework.turbine_def"""
    
    def __init__(self, *args, **kwargs) -> None:
        """初始化 Airfoils 实例。"""
        pass
    
    def load_airfoil(self, filename: str) -> Any:
        """从指定文件加载翼型数据。"""
        pass
    
    def get_airfoil_data(self, name: str) -> Dict[str, Any]:
        """根据翼型名称获取对应的翼型数据。"""
        pass

class Turbine:
    """Turbine class from BeaverFramework.Framework.turbine_def"""
    
    def __init__(self, *args, **kwargs) -> None:
        """初始化 Turbine 实例。"""
        pass
    
    def set_power_rated(self, power: float) -> None:
        """设置风机的额定功率。"""
        pass
    
    def get_rotor_diameter(self) -> float:
        """获取风轮直径。"""
        pass

class Blade:
    """Blade class from BeaverFramework.Framework.turbine_def"""
    
    def __init__(self, *args, **kwargs) -> None:
        """初始化 Blade 实例。"""
        pass
    
    def set_chord(self, chord_data: List[float]) -> None:
        """设置叶片弦长分布。"""
        pass
    
    def set_thickness(self, thickness_data: List[float]) -> None:
        """设置叶片厚度分布。"""
        pass

class Environment:
    """Environment class from BeaverFramework.Framework.turbine_def"""
    
    def __init__(self, *args, **kwargs) -> None:
        """初始化 Environment 实例。"""
        pass
    
    def set_wind_speed(self, speed: float) -> None:
        """设置环境风速。"""
        pass

class Nacelle:
    """Nacelle class from BeaverFramework.Framework.turbine_def"""
    
    def __init__(self, *args, **kwargs) -> None:
        """初始化 Nacelle 实例。"""
        pass

class Rotor_aero:
    """Rotor_aero class from BeaverFramework.Framework.turbine_def"""
    
    def __init__(self, *args, **kwargs) -> None:
        """初始化 Rotor_aero 实例。"""
        pass

class AI:
    """AI class from BeaverFramework.Framework.turbine_def"""
    
    def __init__(self, *args, **kwargs) -> None:
        """初始化 AI 实例。"""
        pass

# Helper functions for autocomplete
def get_home_dir() -> str:
    """获取当前用户的主目录路径。"""
    return os.path.expanduser("~")

def get_nas_base() -> str:
    """获取 NAS 基础目录路径；若环境变量未设置则使用默认值。"""
    return os.getenv("NAS_BASE", os.path.join(get_home_dir(), "NAS"))

def get_beaver_framework_path() -> str:
    """获取 BeaverFramework 的安装路径。"""
    return os.path.join(get_home_dir(), "apps/beaver-framework")
