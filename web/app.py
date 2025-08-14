import streamlit as st
import random
import json
import os
from pathlib import Path

# ページ設定
st.set_page_config(
    page_title="物語生成プロンプトビルダー",
    page_icon="🎭",
    layout="wide"
)

class StoryPromptBuilderWeb:
    def __init__(self):
        self.story_elements = []
        self.total_stars = 0  # ★の総数を保持
        self.load_story_elements()
    
    def load_story_elements(self):
        """story_elements.jsonファイルを読み込む"""
        # 複数の可能なファイルパスを試す
        possible_paths = [
            'story_elements.json',                    # 現在のディレクトリ
            'web/story_elements.json',                # webフォルダ内
            os.path.join(os.path.dirname(__file__), 'story_elements.json'),  # app.pyと同じディレクトリ
            Path(__file__).parent / 'story_elements.json',  # Pathlib使用
        ]
        
        file_loaded = False
        
        for file_path in possible_paths:
            try:
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        self.story_elements = json.load(f)
                    
                    # ★の総数を計算
                    self.total_stars = sum(len(item["stars"]) for item in self.story_elements)
                    
                    # 読み込み成功メッセージ
                    item_count = len(self.story_elements)
                    if self.total_stars >= 7000:
                        print(f"物語要素データ読み込み成功: {self.total_stars}個の要素 ({item_count}項目) (パス: {file_path})")
                    else:
                        print(f"物語要素データ読み込み成功: {self.total_stars}個の要素 ({item_count}項目) (パス: {file_path})")
                    file_loaded = True
                    break
            except Exception as e:
                print(f"パス {file_path} での読み込み失敗: {e}")
                continue
        
        if not file_loaded:
            st.error("⚠️ story_elements.json ファイルが見つかりません。")
            st.info("以下のいずれかの場所に story_elements.json を配置してください：")
            st.code("\n".join(possible_paths))
            
            # 緊急用サンプルデータ（より充実させる）
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
                },
                {
                    "item": "【合図】",
                    "stars": [
                        "★１．吉報か凶報かを示す。意図的に、あるいは手違いにより、正しくない合図が送られることがある。",
                        "★２．秘密の重要な合図。当事者以外には合図の意味はわからない。",
                        "★３．客をもてなす合図。",
                        "★４．生まれたのが男児か女児かを知らせる合図。",
                        "★５．遅すぎた合図。",
                        "★６．夫への変わらぬ愛を知らせるハンカチ。"
                    ]
                },
                {
                    "item": "【愛想づかし】",
                    "stars": [
                        "★１．遊女が悪人をあざむくために、わざと夫や恋人に冷たい態度をとる・愛想づかしをする。",
                        "★２．愛する男の家族からの頼みにより、遊女が、男と別れる決心をする。",
                        "★３．妻が、夫の決心を鈍らせないように、夫に冷たい態度を見せる。",
                        "★４．権力者からの強要によって、女が恋人に別れを告げる。",
                        "★５．母親が、娘の幸福を願って愛想づかしをする。"
                    ]
                },
                {
                    "item": "【笑い】",
                    "stars": [
                        "★１．「笑」という文字の起源。",
                        "★２．古代ギリシア世界に、初めてもたらされた笑い。",
                        "★３．微笑。",
                        "★４．少女の謎の笑い。",
                        "★５．笑いを禁圧する。",
                        "★６ａ．笑い薬。",
                        "★６ｂ．笑いガス。",
                        "★７．笑い死に。",
                        "★８．作り笑い。",
                        "★９．家族の死に際しての、日本人の不可解な笑い。"
                    ]
                }
            ]
            # サンプルデータの★総数を計算
            self.total_stars = sum(len(item["stars"]) for item in self.story_elements)
            st.warning(f"⚠️ サンプルデータ（{len(self.story_elements)}項目、{self.total_stars}個の★要素）を使用しています。")
    
    def extract_elements(self, count):
        """物語要素を抽出"""
        if not self.story_elements:
            return []
            
        selected_elements = []
        used_stars = set()
        
        # 利用可能な要素が少ない場合の対応
        max_attempts = min(count, self.total_stars)  # 実際の★の総数を使用
        attempts = 0
        
        while len(selected_elements) < count and attempts < max_attempts:
            attempts += 1
            
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
    
    def generate_prompt(self, selected_elements, word_count, story_style, ending_style):
        """プロンプトを生成"""
        prompt = "# 物語創作指示\n\n"
        prompt += "## 基本設定\n"
        prompt += f"- 文字数: 約{word_count}文字\n"
        prompt += f"- ジャンル・スタイル: {story_style}\n"
        prompt += f"- 終わり方: {ending_style}\n\n"
        
        prompt += "## 使用する物語要素\n"
        for i, (item, star) in enumerate(selected_elements, 1):
            prompt += f"{i}. {item} {star}\n"
        
        prompt += "\n## 指示\n"
        prompt += f"上記の物語要素をすべて含む{story_style}の物語を創作してください。\n"
        prompt += "各要素は自然に物語に組み込み、指定した文字数で完結する物語にしてください。\n"
        prompt += f"物語の結末は「{ending_style}」になるよう心がけてください。"
        
        return prompt

def main():
    try:
        # アプリケーションインスタンス
        if 'app' not in st.session_state:
            st.session_state.app = StoryPromptBuilderWeb()
        
        # タイトル
        st.title("🎭 物語生成プロンプトビルダー")
        
        # ★の数に応じて表示を変更
        if st.session_state.app.total_stars >= 7000:
            st.markdown(f"{st.session_state.app.total_stars}個の物語要素からランダムに抽出して、生成AI用のプロンプトを作成します")
        else:
            st.markdown(f"{st.session_state.app.total_stars}個の物語要素からランダムに抽出して、生成AI用のプロンプトを作成します")
        
        # JSONファイル読み込み状況を表示
        if st.session_state.app.story_elements:
            # ★の数に応じて表示を変更
            if st.session_state.app.total_stars >= 7000:
                display_text = f"{st.session_state.app.total_stars}個の要素"
            else:
                display_text = f"{st.session_state.app.total_stars}個の要素"
            st.success(f"✅ 物語要素データ: {display_text}読み込み完了")
        else:
            st.error("⚠️ 物語要素データが読み込まれていません")
            st.stop()  # アプリケーションの実行を停止
        
        # サイドバーで基本設定
        with st.sidebar:
            st.header("⚙️ 基本設定")
            
            # 物語要素数
            elements_count = st.slider("物語要素の数", 1, 5, 5)
            
            # 文字数
            word_count = st.number_input("文字数", value=800, min_value=100, max_value=5000, step=100)
            
            st.markdown("---")
            
            # スタイル選択
            st.header("🎨 ジャンル・スタイル")
            story_styles = [
                "民話",
                "SF",
                "ミステリー", 
                "ファンタジー",
                "ホラー",
                "コメディ",
                "ロマンス",
                "アドベンチャー"
            ]
            story_style = st.selectbox("物語のスタイルを選択", story_styles)
            
            st.markdown("---")
            
            # 終わり方選択
            st.header("🎯 終わり方")
            ending_styles = [
                "設定の整合性を重視した自然な終わり方",
                "自然でかつ多少意外性のある終わり方", 
                "読者の予想を裏切る意外な終わり方",
                "ハッピーエンド",
                "ビターエンド",
                "オープンエンド（読者の想像に委ねる）"
            ]
            ending_style = st.selectbox("終わり方のスタイルを選択", ending_styles)
        
        # メインエリア
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.header("📋 物語要素")
            
            # 抽出ボタン
            if st.button("🎯 物語要素を抽出", type="primary", use_container_width=True):
                with st.spinner("物語要素を抽出中..."):
                    st.session_state.selected_elements = st.session_state.app.extract_elements(elements_count)
                    if st.session_state.selected_elements:
                        st.success(f"✅ {len(st.session_state.selected_elements)}個の要素を抽出しました")
                    else:
                        st.error("❌ 要素の抽出に失敗しました")
            
            # 選択された要素を表示
            if 'selected_elements' in st.session_state and st.session_state.selected_elements:
                st.markdown("### 選択された要素:")
                
                # 要素の表示と削除機能
                elements_to_remove = []
                for i, (item, star) in enumerate(st.session_state.selected_elements):
                    with st.container():
                        col_element, col_delete = st.columns([5, 1])
                        
                        with col_element:
                            st.markdown(f"**{i+1}.** {item}")
                            st.markdown(f"　　{star}")
                        
                        with col_delete:
                            if st.button("🗑️", key=f"delete_{i}", help="この要素を削除"):
                                elements_to_remove.append(i)
                        
                        st.divider()
                
                # 削除処理（逆順で削除してインデックスの問題を回避）
                for i in reversed(elements_to_remove):
                    st.session_state.selected_elements.pop(i)
                    st.rerun()
        
        with col2:
            st.header("📝 生成されたプロンプト")
            
            # プロンプト生成ボタン
            generate_disabled = not ('selected_elements' in st.session_state and 
                                   st.session_state.selected_elements)
            
            if st.button("✨ プロンプトを生成", 
                        type="primary", 
                        use_container_width=True,
                        disabled=generate_disabled):
                
                if generate_disabled:
                    st.error("物語要素を抽出してください。")
                else:
                    with st.spinner("プロンプトを生成中..."):
                        st.session_state.generated_prompt = st.session_state.app.generate_prompt(
                            st.session_state.selected_elements, 
                            word_count,
                            story_style,
                            ending_style
                        )
                    st.success("✅ プロンプトを生成しました")
            
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
                
                # 統計情報
                with st.expander("📈 詳細情報"):
                    st.write(f"**文字数設定**: {word_count:,}文字")
                    st.write(f"**物語要素数**: {len(st.session_state.selected_elements)}個")
                    # データセットサイズの表示も★の数に変更
                    if st.session_state.app.total_stars >= 7000:
                        dataset_display = f"{st.session_state.app.total_stars}個の★要素"
                    else:
                        dataset_display = f"{st.session_state.app.total_stars}個の★要素"
                    st.write(f"**使用データセット**: {dataset_display}")
                
                # ダウンロードボタン
                st.download_button(
                    label="📥 プロンプトをダウンロード",
                    data=st.session_state.generated_prompt,
                    file_name=f"story_prompt_{story_style}_{word_count}chars.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        
        # フッター
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: gray; font-size: 0.9em;'>
            <p>🎭 <strong>物語生成プロンプトビルダー</strong> v1.2.0</p>
            <p>Claude, Gemini, Grok, Copilot等の生成AIで使用できます</p>
            <p>🆕 エラーハンドリング・UI改善版</p>
            <p>出典：『物語要素事典』（2021年4月15日改訂） 
            <a href="https://www.lib.agu.ac.jp/yousojiten/" target="_blank">
            https://www.lib.agu.ac.jp/yousojiten/</a></p>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"❌ アプリケーションエラーが発生しました: {str(e)}")
        st.info("ページを再読み込みしてみてください。")
        if st.button("🔄 ページを再読み込み"):
            st.rerun()

if __name__ == "__main__":
    main()
