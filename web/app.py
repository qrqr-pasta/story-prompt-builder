import streamlit as st
import random
import json
import os
from pathlib import Path

# ページ設定
st.set_page_config(
    page_title="物語生成プロンプトビルダー | Story Prompt Builder",
    page_icon="🎭",
    layout="wide"
)

# 多言語テキスト定義
TEXTS = {
    "ja": {
        "title": "🎭 物語生成プロンプトビルダー",
        "description": "個の物語要素からランダムに抽出して、生成AI用のプロンプトを作成します",
        "data_loaded": "✅ 物語要素データ: {count}個の要素読み込み完了",
        "data_not_loaded": "⚠️ 物語要素データが読み込まれていません",
        "file_not_found": "⚠️ story_elements.json ファイルが見つかりません。",
        "file_location_info": "以下のいずれかの場所に story_elements.json を配置してください：",
        "sample_data_warning": "⚠️ サンプルデータ（{items}項目、{stars}個の★要素）を使用しています。",
        
        # サイドバー
        "basic_settings": "⚙️ 基本設定",
        "language": "🌐 言語 / Language",
        "element_count": "物語要素の数",
        "word_count": "文字数",
        "genre_style": "🎨 ジャンル・スタイル",
        "genre_select": "物語のスタイルを選択",
        "ending_style": "🎯 終わり方",
        "ending_select": "終わり方のスタイルを選択",
        
        # ジャンル
        "genre_folk": "民話",
        "genre_sf": "SF",
        "genre_mystery": "ミステリー",
        "genre_fantasy": "ファンタジー",
        "genre_horror": "ホラー",
        "genre_comedy": "コメディ",
        "genre_romance": "ロマンス",
        "genre_adventure": "アドベンチャー",
        
        # 終わり方
        "ending_natural_unexpected": "自然でかつ多少意外性のある終わり方",
        "ending_surprising": "読者の予想を裏切る意外な終わり方",
        "ending_natural": "設定の整合性を重視した自然な終わり方",
        "ending_happy": "ハッピーエンド",
        "ending_bitter": "ビターエンド",
        "ending_open": "オープンエンド（読者の想像に委ねる）",
        
        # メインエリア
        "story_elements": "📋 物語要素",
        "extract_elements": "🎯 物語要素を抽出",
        "extracting": "物語要素を抽出中...",
        "elements_extracted": "✅ {count}個の要素を抽出しました",
        "extraction_failed": "❌ 要素の抽出に失敗しました",
        "selected_elements": "### 選択された要素:",
        "delete_tooltip": "この要素を削除",
        
        "generated_prompt": "📝 生成されたプロンプト",
        "generate_prompt": "✨ プロンプトを生成",
        "generating": "プロンプトを生成中...",
        "prompt_generated": "✅ プロンプトを生成しました",
        "extract_first": "物語要素を抽出してください。",
        "prompt_title": "### 生成されたプロンプト:",
        
        "settings_summary": "### 📊 設定サマリー:",
        "genre_label": "🎨 **ジャンル**",
        "ending_label": "🎯 **終わり方**",
        
        "detailed_info": "📈 詳細情報",
        "word_count_setting": "**文字数設定**",
        "element_count_used": "**物語要素数**",
        "dataset_size": "**使用データセット**",
        "download_prompt": "📥 プロンプトをダウンロード",
        
        # プロンプトテンプレート
        "prompt_header": "# 物語創作指示\n\n",
        "prompt_basic_settings": "## 基本設定\n",
        "prompt_word_count": "- 文字数: 約{count}文字\n",
        "prompt_genre": "- ジャンル・スタイル: {genre}\n",
        "prompt_ending": "- 終わり方: {ending}\n\n",
        "prompt_elements_header": "## 使用する物語要素\n",
        "prompt_instructions_header": "\n## 指示\n",
        "prompt_instructions": "上記の物語要素をすべて含む{genre}の物語を創作してください。\n各要素は自然に物語に組み込み、指定した文字数で完結する物語にしてください。\n物語の結末は「{ending}」になるよう心がけてください。",
        
        # フッター
        "footer_title": "物語生成プロンプトビルダー",
        "footer_ai_support": "Claude, Gemini, Grok, Copilot等の生成AIで使用できます",
        "footer_version": "🆕 エラーハンドリング・UI改善版",
        "footer_source": "出典：『物語要素事典』（2021年4月15日改訂）",
        
        # エラー
        "app_error": "❌ アプリケーションエラーが発生しました",
        "reload_info": "ページを再読み込みしてみてください。",
        "reload_button": "🔄 ページを再読み込み"
    },
    
    "en": {
        "title": "🎭 Story Prompt Builder",
        "description": " story elements randomly extracted to create prompts for generative AI",
        "data_loaded": "✅ Story elements data: {count} elements loaded successfully",
        "data_not_loaded": "⚠️ Story elements data not loaded",
        "file_not_found": "⚠️ story_elements.json file not found.",
        "file_location_info": "Please place story_elements.json in one of the following locations:",
        "sample_data_warning": "⚠️ Using sample data ({items} items, {stars} ★ elements).",
        
        # サイドバー
        "basic_settings": "⚙️ Basic Settings",
        "language": "🌐 言語 / Language",
        "element_count": "Number of Story Elements",
        "word_count": "Word Count",
        "genre_style": "🎨 Genre / Style",
        "genre_select": "Select story style",
        "ending_style": "🎯 Ending Style",
        "ending_select": "Select ending style",
        
        # ジャンル
        "genre_folk": "Folk Tale",
        "genre_sf": "Science Fiction",
        "genre_mystery": "Mystery",
        "genre_fantasy": "Fantasy",
        "genre_horror": "Horror",
        "genre_comedy": "Comedy",
        "genre_romance": "Romance",
        "genre_adventure": "Adventure",
        
        # 終わり方
        "ending_natural_unexpected": "Natural ending with some unexpected elements",
        "ending_surprising": "Unexpected ending that defies reader expectations",
        "ending_natural": "Natural ending that respects story consistency",
        "ending_happy": "Happy Ending",
        "ending_bitter": "Bitter Ending",
        "ending_open": "Open Ending (left to reader's imagination)",
        
        # メインエリア
        "story_elements": "📋 Story Elements",
        "extract_elements": "🎯 Extract Story Elements",
        "extracting": "Extracting story elements...",
        "elements_extracted": "✅ {count} elements extracted",
        "extraction_failed": "❌ Failed to extract elements",
        "selected_elements": "### Selected Elements:",
        "delete_tooltip": "Delete this element",
        
        "generated_prompt": "📝 Generated Prompt",
        "generate_prompt": "✨ Generate Prompt",
        "generating": "Generating prompt...",
        "prompt_generated": "✅ Prompt generated successfully",
        "extract_first": "Please extract story elements first.",
        "prompt_title": "### Generated Prompt:",
        
        "settings_summary": "### 📊 Settings Summary:",
        "genre_label": "🎨 **Genre**",
        "ending_label": "🎯 **Ending**",
        
        "detailed_info": "📈 Detailed Information",
        "word_count_setting": "**Word Count Setting**",
        "element_count_used": "**Story Elements Used**",
        "dataset_size": "**Dataset Size**",
        "download_prompt": "📥 Download Prompt",
        
        # プロンプトテンプレート
        "prompt_header": "# Story Creation Instructions\n\n",
        "prompt_basic_settings": "## Basic Settings\n",
        "prompt_word_count": "- Word count: approximately {count} words\n",
        "prompt_genre": "- Genre/Style: {genre}\n",
        "prompt_ending": "- Ending style: {ending}\n\n",
        "prompt_elements_header": "## Story Elements to Use\n",
        "prompt_instructions_header": "\n## Instructions\n",
        "prompt_instructions": "Create a {genre} story that includes all the above story elements.\nIntegrate each element naturally into the story and complete it within the specified word count.\nThe story's conclusion should follow \"{ending}\".",
        
        # フッター
        "footer_title": "Story Prompt Builder",
        "footer_ai_support": "Compatible with Claude, Gemini, Grok, Copilot and other generative AI",
        "footer_version": "🆕 Error Handling & UI Improvement Version",
        "footer_source": "Source: 'Encyclopedia of Story Elements' (Revised April 15, 2021)",
        
        # エラー
        "app_error": "❌ Application error occurred",
        "reload_info": "Please try reloading the page.",
        "reload_button": "🔄 Reload Page"
    }
}

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
    
    def generate_prompt(self, selected_elements, word_count, story_style, ending_style, lang):
        """プロンプトを生成"""
        t = TEXTS[lang]
        
        prompt = t["prompt_header"]
        prompt += t["prompt_basic_settings"]
        prompt += t["prompt_word_count"].format(count=word_count)
        prompt += t["prompt_genre"].format(genre=story_style)
        prompt += t["prompt_ending"].format(ending=ending_style)
        
        prompt += t["prompt_elements_header"]
        for i, (item, star) in enumerate(selected_elements, 1):
            prompt += f"{i}. {item} {star}\n"
        
        prompt += t["prompt_instructions_header"]
        prompt += t["prompt_instructions"].format(genre=story_style, ending=ending_style)
        
        return prompt

def get_text(key, lang="ja", **kwargs):
    """言語に応じたテキストを取得"""
    text = TEXTS[lang].get(key, TEXTS["ja"].get(key, key))
    if kwargs:
        try:
            return text.format(**kwargs)
        except:
            return text
    return text

def main():
    try:
        # 言語設定の初期化
        if 'language' not in st.session_state:
            st.session_state.language = 'ja'
        
        # アプリケーションインスタンス
        if 'app' not in st.session_state:
            st.session_state.app = StoryPromptBuilderWeb()
        
        lang = st.session_state.language
        
        # タイトル
        st.title(get_text("title", lang))
        
        # ★の数に応じて表示を変更
        if st.session_state.app.total_stars >= 7000:
            st.markdown(f"{st.session_state.app.total_stars}" + get_text("description", lang))
        else:
            st.markdown(f"{st.session_state.app.total_stars}" + get_text("description", lang))
        
        # JSONファイル読み込み状況を表示
        if st.session_state.app.story_elements:
            # ★の数に応じて表示を変更
            if st.session_state.app.total_stars >= 7000:
                display_text = f"{st.session_state.app.total_stars}"
            else:
                display_text = f"{st.session_state.app.total_stars}"
            st.success(get_text("data_loaded", lang, count=display_text))
        else:
            st.error(get_text("file_not_found", lang))
            st.info(get_text("file_location_info", lang))
            st.code("\n".join([
                'story_elements.json',
                'web/story_elements.json',
                os.path.join(os.path.dirname(__file__), 'story_elements.json'),
                str(Path(__file__).parent / 'story_elements.json')
            ]))
            st.warning(get_text("sample_data_warning", lang, 
                              items=len(st.session_state.app.story_elements), 
                              stars=st.session_state.app.total_stars))
        
        # サイドバーで基本設定
        with st.sidebar:
            # 言語切り替え
            st.header(get_text("language", lang))
            language_options = {
                "🇯🇵 日本語": "ja",
                "🇺🇸 English": "en"
            }
            selected_lang = st.selectbox(
                "", 
                options=list(language_options.keys()),
                index=0 if lang == "ja" else 1,
                key="lang_selector"
            )
            
            if language_options[selected_lang] != st.session_state.language:
                st.session_state.language = language_options[selected_lang]
                st.rerun()
            
            st.markdown("---")
            
            st.header(get_text("basic_settings", lang))
            
            # 物語要素数
            elements_count = st.slider(get_text("element_count", lang), 1, 5, 2)
            
            # 文字数
            word_count = st.number_input(get_text("word_count", lang), value=800, min_value=100, max_value=5000, step=100)
            
            st.markdown("---")
            
            # スタイル選択
            st.header(get_text("genre_style", lang))
            story_styles_keys = ["genre_folk", "genre_sf", "genre_mystery", "genre_fantasy", 
                               "genre_horror", "genre_comedy", "genre_romance", "genre_adventure"]
            story_styles = [get_text(key, lang) for key in story_styles_keys]
            story_style = st.selectbox(get_text("genre_select", lang), story_styles)
            
            st.markdown("---")
            
            # 終わり方選択
            st.header(get_text("ending_style", lang))
            ending_styles_keys = ["ending_natural_unexpected", "ending_surprising", "ending_natural", 
                                "ending_happy", "ending_bitter", "ending_open"]
            ending_styles = [get_text(key, lang) for key in ending_styles_keys]
            ending_style = st.selectbox(get_text("ending_select", lang), ending_styles)
        
        # メインエリア
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.header(get_text("story_elements", lang))
            
            # 抽出ボタン
            if st.button(get_text("extract_elements", lang), type="primary", use_container_width=True):
                with st.spinner(get_text("extracting", lang)):
                    st.session_state.selected_elements = st.session_state.app.extract_elements(elements_count)
                    if st.session_state.selected_elements:
                        st.success(get_text("elements_extracted", lang, count=len(st.session_state.selected_elements)))
                    else:
                        st.error(get_text("extraction_failed", lang))
            
            # 選択された要素を表示
            if 'selected_elements' in st.session_state and st.session_state.selected_elements:
                st.markdown(get_text("selected_elements", lang))
                
                # 要素の表示と削除機能
                elements_to_remove = []
                for i, (item, star) in enumerate(st.session_state.selected_elements):
                    with st.container():
                        col_element, col_delete = st.columns([5, 1])
                        
                        with col_element:
                            st.markdown(f"**{i+1}.** {item}")
                            st.markdown(f"　　{star}")
                        
                        with col_delete:
                            if st.button("🗑️", key=f"delete_{i}", help=get_text("delete_tooltip", lang)):
                                elements_to_remove.append(i)
                        
                        st.divider()
                
                # 削除処理（逆順で削除してインデックスの問題を回避）
                for i in reversed(elements_to_remove):
                    st.session_state.selected_elements.pop(i)
                    st.rerun()
        
        with col2:
            st.header(get_text("generated_prompt", lang))
            
            # プロンプト生成ボタン
            generate_disabled = not ('selected_elements' in st.session_state and 
                                   st.session_state.selected_elements)
            
            if st.button(get_text("generate_prompt", lang),
                        type="primary", 
                        use_container_width=True,
                        disabled=generate_disabled):
                
                if generate_disabled:
                    st.error(get_text("extract_first", lang))
                else:
                    with st.spinner(get_text("generating", lang)):
                        st.session_state.generated_prompt = st.session_state.app.generate_prompt(
                            st.session_state.selected_elements, 
                            word_count,
                            story_style,
                            ending_style,
                            lang
                        )
                    st.success(get_text("prompt_generated", lang))
            
            # 生成されたプロンプトを表示
            if 'generated_prompt' in st.session_state:
                st.markdown(get_text("prompt_title", lang))
                st.code(st.session_state.generated_prompt, language='markdown')
                
                # 設定情報の表示
                st.markdown(get_text("settings_summary", lang))
                col_style, col_ending = st.columns(2)
                with col_style:
                    st.info(f"{get_text('genre_label', lang)}: {story_style}")
                with col_ending:
                    st.info(f"{get_text('ending_label', lang)}: {ending_style}")
                
                # 統計情報
                with st.expander(get_text("detailed_info", lang)):
                    st.write(f"{get_text('word_count_setting', lang)}: {word_count:,}" + ("文字" if lang == "ja" else " words"))
                    st.write(f"{get_text('element_count_used', lang)}: {len(st.session_state.selected_elements)}" + ("個" if lang == "ja" else ""))
                    # データセットサイズの表示も★の数に変更
                    if st.session_state.app.total_stars >= 7000:
                        dataset_display = f"{st.session_state.app.total_stars}" + ("個の★要素" if lang == "ja" else " ★ elements")
                    else:
                        dataset_display = f"{st.session_state.app.total_stars}" + ("個の★要素" if lang == "ja" else " ★ elements")
                    st.write(f"{get_text('dataset_size', lang)}: {dataset_display}")
                
                # ダウンロードボタン
                file_suffix = "chars" if lang == "ja" else "words"
                st.download_button(
                    label=get_text("download_prompt", lang),
                    data=st.session_state.generated_prompt,
                    file_name=f"story_prompt_{story_style}_{word_count}{file_suffix}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        
        # フッター
        st.markdown("---")
        footer_html = f"""
        <div style='text-align: center; color: gray; font-size: 0.9em;'>
            <p>🎭 <strong>{get_text("footer_title", lang)}</strong> v1.3.0</p>
            <p>{get_text("footer_ai_support", lang)}</p>
            <p>{get_text("footer_version", lang)}</p>
            <p>{get_text("footer_source", lang)} 
            <a href="https://www.lib.agu.ac.jp/yousojiten/" target="_blank">
            https://www.lib.agu.ac.jp/yousojiten/</a></p>
        </div>
        """
        st.markdown(footer_html, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"{get_text('app_error', st.session_state.get('language', 'ja'))}: {str(e)}")
        st.info(get_text("reload_info", st.session_state.get('language', 'ja')))
        if st.button(get_text("reload_button", st.session_state.get('language', 'ja'))):
            st.rerun()

if __name__ == "__main__":
    main()
