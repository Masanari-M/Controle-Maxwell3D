from pyaedt import Maxwell3d, settings

# COM モード（gRPCではなく）を使用
settings.use_grpc_api = False

# Maxwell 3D (2021.2) のセッションを新規起動
m3d = Maxwell3d(projectname="L_Electrode_ExplicitSheet", 
                designname="L_Design", 
                version="2021.2", 
                new_desktop_session=True, 
                non_graphical=False)

m3d.modeler.model_units = "mm"
thickness = 0.01  # Z方向への押し出し厚み [mm]

# --- 1. L字型ポリラインの作成 ---
points = [
    [0.1, 0.4, 0.0],  # A
    [0.4, 0.4, 0.0],  # B
    [0.4, 0.1, 0.0],  # C
    [0.3, 0.1, 0.0],  # D
    [0.3, 0.3, 0.0],  # E
    [0.1, 0.3, 0.0],  # F
    [0.1, 0.4, 0.0]   # A（始点に戻る＝閉じる）
]
segments = ["Line"] * (len(points) - 1)

# ポリライン作成。close_surface=True として内部面も生成する
polyline = m3d.modeler.create_polyline(points=points, segment_type=segments, name="L_poly", close_surface=True)
print("✅ Polyline 作成:", polyline)

# --- 2. ポリラインからシートへの変換 (cover_lines) ---
cover_success = m3d.modeler.cover_lines("L_poly")
if cover_success:
    sheet_L = m3d.modeler.sheet_names[-1]
    print("✅ Sheet 作成成功:", sheet_L)
else:
    print("❌ cover_lines に失敗")
    sheet_L = None

# --- 3. 押し出し処理 ---
if sheet_L:
    # 押し出しを実行（ここでは元のL_polyにそのまま押し出し結果が入る）
    m3d.modeler.sweep_along_vector(sheet_L, [0, 0, thickness])
    m3d.modeler.refresh()

    # 材料設定
    if "gold" not in m3d.materials.material_keys:
        m3d.materials.add_material("gold")
    m3d.assign_material("L_poly", "gold")
    print("✅ 材料 'gold' を L_poly に設定しました")

    # --- Electrostaticセットアップ作成（なければ） ---
    if not m3d.setups:
        setup = m3d.create_setup("Electrostatic")
        setup.props["MaximumPasses"] = 10
        setup.update()
        print("✅ Electrostatic解析セットアップ作成完了")
    else:
        print("ℹ️ 既にセットアップ存在")

    # --- L_polyのFaceに100V電圧印加 ---
    faces = m3d.modeler.get_faces("L_poly")
    if faces:
        m3d.assign_voltage_to_faces(face_list=[faces[0]], amplitude=100)
        print("✅ L_polyのFaceに100Vを印加しました")
    else:
        print("❌ L_polyのFaceが取得できませんでした")

else:
    print("❌ sheet_L が存在しないため押し出し処理をスキップします")

# --- 4. プロジェクトを保存せずに閉じて、Desktopも完全終了 ---
m3d.release_desktop(close_projects=True, close_desktop=True)
