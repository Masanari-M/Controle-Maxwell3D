from pyaedt import Maxwell3d

m3d = Maxwell3d(project="L_Electrode_Project", design="L_Electrode_Design", version="2021.2", new_desktop=True, non_graphical=False)

m3d.modeler.model_units = "mm"
thickness = 0.01

rectangles = [
    ((0.1, 0.4), 0.3, 3.7),
    ((0.1, 0.1), 4.0, 0.3),
    ((0.03, 0.03), 0.07, 0.07),
    ((0.08, 0.1), 0.02, 0.02),
    ((0.1, 0.08), 0.02, 0.02),
]

box_names = []
for i, ((x, y), dx, dy) in enumerate(rectangles, 1):
    name = f"box{i}"
    box = m3d.modeler.create_box([x, y, 0], [dx, dy, thickness], name=name)
    if box:
        box_names.append(box)
    else:
        print(f"❌ {name} 作成失敗")

if len(box_names) > 1:
    l_electrode = m3d.modeler.unite(box_names)
else:
    l_electrode = box_names[0] if box_names else None

if l_electrode:
    m3d.modeler[l_electrode].material_name = "copper"
    print("✅ L字電極 作成 & 材料設定 完了")
else:
    print("❌ 電極の生成に失敗")

m3d.save_project()
m3d.release_desktop(close_projects=True, close_desktop=True)
