import streamlit as st
import random
import json
import os

# ページ設定
st.set_page_config(
    page_title="物語生成プロンプトビルダー",
    page_icon="🎭",
    layout="wide"
)

class StoryPromptBuilderWeb:
    def __init__(self):
        self.story_elements = []
        self.load_story_elements()
    
    def load_story_elements(self):
        """story_elements.jsonファイルを読み込む"""
        try:
            # JSONファイルを読み込み
            with open('story_elements.json', 'r', encoding='utf-8') as f:
                self.story_elements = json.load(f)
            
            # 読み込み成功メッセージ（デバッグ用）
            print(f"物語要素データ読み込み成功: {len(self.story_elements)}項目")
            
        except FileNotFoundError:
            st.error("⚠️ story_elements.json ファイルが見つかりません。")
            st.info("webフォルダに story_elements.json を配置してください。")
            # 緊急用サンプルデータ
            self.story_elements = [
                {
                    "item": "【相打ち】",
                    "stars": [
                        "★１．刺し違え。",
                        "★２．互いに呪い合って、相手を動物に変える。",
                        "★３．猟師と猪の相打ち。",
                        "★４．互いにミサイルを相手国へ撃ち込む。"
                    ]
                },
                {
                    "item": "【合言葉】",
                    "stars": [
                        "★１．合言葉で、味方であるか否かを確認する。",
                        "★２．警察や探偵が、合言葉を用いて犯罪組織に潜入する。",
                        "★３．合言葉を知らぬが、機転を利かせてその場をきりぬける。",
                        "★４．合言葉を知らないため、殺される。"
                    ]
                }
            ]
        except json.JSONDecodeError:
            st.error("⚠️ story_elements.json の形式が正しくありません。")
            self.story_elements = []
        except Exception as e:
            st.error(f"⚠️ ファイル読み込みエラー: {str(e)}")
            self.story_elements = []
    
    def generate_katakana_name(self):
        """カタカナ2文字の名前を生成"""
        # 1文字目：拗音、撥音、長音以外
        first_chars = [
            'ア', 'イ', 'ウ', 'エ', 'オ',
            'カ', 'キ', 'ク', 'ケ', 'コ', 'ガ', 'ギ', 'グ', 'ゲ', 'ゴ',
            'サ', 'シ', 'ス', 'セ', 'ソ', 'ザ', 'ジ', 'ズ', 'ゼ', 'ゾ',
            'タ', 'チ', 'ツ', 'テ', 'ト', 'ダ', 'ヂ', 'ヅ', 'デ', 'ド',
            'ナ', 'ニ', 'ヌ', 'ネ', 'ノ',
            'ハ', 'ヒ', 'フ', 'ヘ', 'ホ', 'バ', 'ビ', 'ブ', 'ベ', 'ボ', 'パ', 'ピ', 'プ', 'ペ', 'ポ',
            'マ', 'ミ', 'ム', 'メ', 'モ',
            'ヤ', 'ユ', 'ヨ',
            'ラ', 'リ', 'ル', 'レ', 'ロ',
            'ワ', 'ヲ'
        ]
        
        # 2文字目：全てのカタカナ（長音も含む）
        second_chars = first_chars + ['ャ', 'ュ', 'ョ', 'ン', 'ー']
        
        return random.choice(first_chars) + random.choice(second_chars)
    
    def extract_elements(self, count):
        """物語要素を抽出"""
        if not self.story_elements:
            return []
            
        selected_elements = []
        used_stars = set()
        
        for _ in range(count):
            # ランダムにitemを選択
            item_data = random.choice(self.story_elements)
            item_name = item_data["item"]
            
            # 使用済みでないstarを選択
            available_stars = [star for star in item_data["stars"] if star not in used_stars]
            
            if available_stars:
                selected_star = random.choice(available_stars)
                used_stars.add(selected_star)
                selected_elements.append((item_name, selected_star))
        
        return selected_elements
    
    def generate_prompt(self, selected_elements, characters, word_count, story_style, ending_style):
        """プロンプトを生成"""
        prompt = "# 物語創作指示\n\n"
        prompt += "## 基本設定\n"
        prompt += f"- 文字数: 約{word_count}文字\n"
        prompt += f"- ジャンル・スタイル: {story_style}\n"
        prompt += f"- 登場人物: {', '.join(characters)}\n"
        prompt += f"- 終わり方: {ending_style}\n\n"
        
        prompt += "## 使用する物語要素\n"
        for i, (item, star) in enumerate(selected_elements, 1):
            prompt += f"{i}. {item} {star}\n"
        
        prompt += "\n## 指示\n"
        prompt += f"上記の物語要素をすべて含む{story_style}の物語を創作してください。\n"
        prompt += "各要素は自然に物語に組み込み、指定した文字数で完結する物語にしてください。\n"
        prompt += "登場人物は指定された名前を使用してください。\n"
        prompt += f"物語の結末は「{ending_style}」になるよう心がけてください。"
        
        return prompt

def main():
    # アプリケーションインスタンス
    if 'app' not in st.session_state:
        st.session_state.app = StoryPromptBuilderWeb()
    
    # タイトル
    st.title("🎭 物語生成プロンプトビルダー")
    st.markdown("約1130項目の物語要素からランダムに抽出して、生成AI用のプロンプトを作成します")
    
    # JSONファイル読み込み状況を表示
    if st.session_state.app.story_elements:
        st.success(f"✅ 物語要素データ: {len(st.session_state.app.story_elements)}項目読み込み完了")
    else:
        st.warning("⚠️ 物語要素データが読み込まれていません")
        return
    
    # サイドバーで基本設定
    with st.sidebar:
        st.header("⚙️ 基本設定")
        
        # 物語要素数
        elements_count = st.slider("物語要素の数", 1, 5, 3)
        
        # 文字数
        word_count = st.number_input("文字数", value=1000, min_value=100, max_value=5000, step=100)
        
        # 登場人物数
        char_count = st.slider("登場人物数", 1, 10, 2)
        
        st.markdown("---")
        
        # スタイル選択
        st.header("🎨 ジャンル・スタイル")
        story_styles = [
            "民話",
            "SF",
            "ミステリー", 
            "ファンタジー",
            "ホラー"
        ]
        story_style = st.selectbox("物語のスタイルを選択", story_styles)
        
        st.markdown("---")
        
        # 終わり方選択
        st.header("🎯 終わり方")
        ending_styles = [
            "読者の予想を裏切る意外な終わり方",
            "自然でかつ多少意外性のある終わり方", 
            "設定の整合性を重視した自然な終わり方"
        ]
        ending_style = st.selectbox("終わり方のスタイルを選択", ending_styles)
        
        st.markdown("---")
        st.header("👥 登場人物")
        
        # 登場人物名の入力
        characters = []
        for i in range(char_count):
            if f'char_{i}' not in st.session_state:
                st.session_state[f'char_{i}'] = st.session_state.app.generate_katakana_name()
            
            char_name = st.text_input(
                f"登場人物{i+1}", 
                value=st.session_state[f'char_{i}'],
                key=f'char_input_{i}'
            )
            if char_name:
                characters.append(char_name)
        
        # 名前再生成ボタン
        if st.button("🎲 名前を再生成"):
            for i in range(char_count):
                st.session_state[f'char_{i}'] = st.session_state.app.generate_katakana_name()
            st.rerun()
    
    # メインエリア
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📋 物語要素")
        
        # 抽出ボタン
        if st.button("🎯 物語要素を抽出", type="primary", use_container_width=True):
            st.session_state.selected_elements = st.session_state.app.extract_elements(elements_count)
        
        # 選択された要素を表示
        if 'selected_elements' in st.session_state and st.session_state.selected_elements:
            st.markdown("### 選択された要素:")
            
            # 要素の表示と削除機能
            for i, (item, star) in enumerate(st.session_state.selected_elements):
                col_element, col_delete = st.columns([4, 1])
                
                with col_element:
                    st.markdown(f"**{i+1}.** {item}")
                    st.markdown(f"　　{star}")
                
                with col_delete:
                    if st.button("🗑️", key=f"delete_{i}", help="この要素を削除"):
                        st.session_state.selected_elements.pop(i)
                        st.rerun()
                
                st.markdown("---")
    
    with col2:
        st.header("📝 生成されたプロンプト")
        
        # プロンプト生成ボタン
        if st.button("✨ プロンプトを生成", type="primary", use_container_width=True):
            if 'selected_elements' in st.session_state and st.session_state.selected_elements and characters:
                st.session_state.generated_prompt = st.session_state.app.generate_prompt(
                    st.session_state.selected_elements, 
                    characters, 
                    word_count,
                    story_style,
                    ending_style
                )
            else:
                st.error("物語要素を抽出し、登場人物名を入力してください。")
        
        # 生成されたプロンプトを表示
        if 'generated_prompt' in st.session_state:
            st.markdown("### 生成されたプロンプト:")
            st.code(st.session_state.generated_prompt, language='markdown')
            
            # 設定情報の表示
            st.markdown("### 📊 設定サマリー:")
            col_style, col_ending = st.columns(2)
            with col_style:
                st.info(f"🎨 **ジャンル**: {story_style}")
            with col_ending:
                st.info(f"🎯 **終わり方**: {ending_style}")
            
            # コピーボタン
            if st.button("📋 クリップボードにコピー", use_container_width=True):
                st.write("プロンプトを選択してCtrl+C（またはCmd+C）でコピーできます")
    
    # フッター
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray;'>
        <p>🎭 物語生成プロンプトビルダー v1.1.0</p>
        <p>Claude, Gemini, Grok, Copilot等の生成AIで使用できます</p>
        <p>🆕 ジャンル・終わり方指定機能追加</p>
        <p>出典：『物語要素事典』（2021年4月15日改訂） <a href="https://www.lib.agu.ac.jp/yousojiten/">https://www.lib.agu.ac.jp/yousojiten/</a></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
