from pyaedt import Desktop

# すでに起動しているセッションにだけ接続（新しく起動しない）
d = Desktop(new_desktop_session=False)

# プロジェクトを保存せずに閉じて、Desktopも終了
d.release_desktop(close_projects=True, close_desktop=True)
