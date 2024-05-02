from krita import *

class MyExtension(Extension):

    def __init__(self, parent):
        # これは親クラスを初期化します。サブクラス化の際に重要です。
        super().__init__(parent)

    def setup(self):
        pass

    def createActions(self, window):
        action = window.createAction("myAction", "私のスクリプト", "tools/scripts")

# そして拡張機能を Krita の拡張機能一覧に追加します:
Krita.instance().addExtension(MyExtension(Krita.instance()))