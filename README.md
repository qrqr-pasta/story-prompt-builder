# 🎭 物語生成プロンプトビルダー

1131項目の物語要素からランダムに抽出して、生成AI用のプロンプトを作成するデスクトップアプリです。

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-blue.svg)
![Language](https://img.shields.io/badge/language-Python-green.svg)

## 🎯 特徴

- **1131項目の物語要素** を内蔵（完全版データ統合済み）
- **完全スタンドアローン** - Pythonインストール不要
- **Claude/Gemini/Grok/Copilot** 対応プロンプト生成
- **カタカナ登場人物名** 自動生成
- **要素の編集・削除機能** 付き
- **出展：『物語要素事典』（2021年4月15日改訂）愛知学院大学
- 作成者：神山重彦（かみやま・しげひこ　1951年生まれ　愛知学院大学文学部日本文化学科名誉教授）

## 💾 ダウンロード

**[📥 最新版をダウンロード](https://github.com/qrqr-pasta/story-prompt-builder/releases/latest)**

> ⚠️ Windows Defenderが警告を出す場合がありますが、「詳細情報」→「実行」で起動できます

## 🚀 使い方

1. **StoryPromptBuilder.exe** をダブルクリック
2. **物語要素の数** (1-5個) を設定
3. **登場人物数** と **文字数** を調整
4. **「物語要素を抽出」** をクリック
5. 不要な要素があれば削除
6. **「プロンプトを生成」** をクリック
7. 生成されたプロンプトをコピーして生成AIに入力

## 📋 プロンプト例
物語創作指示
基本設定

文字数: 約1000文字
登場人物: タロ、ハナ

使用する物語要素

【兄弟】★１．兄弟が争う。対立する。
【恋文】★１．恋文が第三者の手に入る。

指示
上記の物語要素をすべて含む物語を創作してください。
各要素は自然に物語に組み込み、指定した文字数で完結する物語にしてください。
登場人物は指定された名前を使用してください。

## 🛠️ 開発者向け

### 必要環境
- Python 3.7+
- tkinter

### セットアップ
```bash
git clone https://github.com/qrqr-pasta/story-prompt-builder.git
cd story-prompt-builder
pip install -r requirements.txt
python story_prompt_builder.py
exe化
bashpython data_integration.py  # 完全版データを統合
pip install pyinstaller
pyinstaller --onefile --windowed --name=StoryPromptBuilder story_prompt_builder.py
📜 ライセンス
MIT License - 自由にご利用ください
🤝 貢献
Issue報告や機能提案、大歓迎です！
