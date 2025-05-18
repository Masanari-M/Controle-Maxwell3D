# -*- coding: utf-8 -*-
"""
Created on Sun Mar 23 20:26:49 2025

@author: tanak
"""
from pyaedt import Maxwell3d

m3d = Maxwell3d(project="Electrode_Optimization", design="IonTrapOptimization", version="2021.2", non_graphical=False)

if m3d and m3d.desktop_class:
    print("✅ Maxwell 3D 接続成功:", m3d.project_name, "/", m3d.design_name)
    m3d.release_desktop()
else:
    print("❌ Maxwell 3D の初期化に失敗")
