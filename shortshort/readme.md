\# ショートショート自動生成システム



星新一風の意外なオチを持つショートショートを自動生成するシステムです。



\## 特徴

\- 物語要素事典ベースの要素選択

\- AIまたはプロンプトのみ生成対応

\- ユーザー評価機能（☆1-5）

\- 作品群管理とダウンロード機能



\## 使用方法

```bash

streamlit run app.py

出典
『物語要素事典』（2021年4月15日改訂）
https://www.lib.agu.ac.jp/yousojiten/

### ステップ3: コミットとプッシュ
各ファイル作成時に適切なコミットメッセージを付ける：
- `shortshort/app.py` → "Add shortshort generation system"
- `shortshort/story_elements.json` → "Add story elements data for shortshort"
- `shortshort/requirements.txt` → "Add requirements for shortshort system"
- `shortshort/README.md` → "Add documentation for shortshort system"

## 🔧 実行前の確認事項

### JSONファイルパスの修正
新しいフォルダでは、JSONファイル読み込み部分を以下のように修正することをお勧めします：

```python
def load_story_elements(self):
    # 現在のスクリプトと同じディレクトリを基準にする
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_files = [
        os.path.join(script_dir, "story_elements.json"),
        os.path.join(script_dir, "story_elements - コピー.json")
    ]