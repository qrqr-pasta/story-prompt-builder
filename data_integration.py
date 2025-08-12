# data_integration.py
# 完全版のstory_elements.jsonを読み込んで、
# Pythonコード内に埋め込むためのコードを生成するスクリプト

import json

def integrate_json_data():
    """完全版JSONデータをPythonコードに統合"""
    try:
        # 完全版JSONファイルを読み込み
        with open('story_elements.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"読み込み完了: {len(data)}項目のデータを検出")
        
        # Pythonコードとして出力
        output_code = "        self.story_elements = " + json.dumps(data, ensure_ascii=False, indent=12)
        
        # ファイルに保存
        with open('embedded_data.py', 'w', encoding='utf-8') as f:
            f.write("# 物語要素データ（内蔵版）\n")
            f.write("# このコードをstory_prompt_builder.pyのload_story_elements()メソッド内に貼り付けてください\n\n")
            f.write(output_code)
        
        print("embedded_data.pyに統合用コードを出力しました")
        print()
        print("使用方法:")
        print("1. embedded_data.pyを開く")
        print("2. 生成されたコードをコピー")
        print("3. story_prompt_builder.pyの load_story_elements() メソッド内の")
        print("   self.story_elements = [...] の部分を置き換える")
        print("4. build_exe.batを実行してexe化")
        
        return True
        
    except FileNotFoundError:
        print("エラー: story_elements.json が見つかりません")
        print("完全版のJSONファイルをこのスクリプトと同じフォルダに置いてください")
        return False
    except json.JSONDecodeError:
        print("エラー: JSONファイルの形式が正しくありません")
        return False
    except Exception as e:
        print(f"エラー: {str(e)}")
        return False

if __name__ == "__main__":
    print("物語要素データ統合スクリプト")
    print("=" * 40)
    integrate_json_data()
    input("\nEnterキーを押して終了...")