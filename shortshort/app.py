import streamlit as st
import random
import json
import os
import requests
import time
import re
from datetime import datetime

# ページ設定
st.set_page_config(
    page_title="ショートショート自動生成システム",
    page_icon="📚",
    layout="wide"
)

class ShortStoryGenerator:
    """ショートショート生成システム"""
    
    def __init__(self, api_key, api_type):
        self.api_key = api_key
        self.api_type = api_type
        
    def generate_story(self, prompt):
        """ショートショートを生成"""
        if self.api_type == "claude":
            return self._generate_claude_story(prompt)
        elif self.api_type == "grok":
            return self._generate_grok_story(prompt)
        elif self.api_type == "openai":
            return self._generate_openai_story(prompt)
        elif self.api_type == "gemini":
            return self._generate_gemini_story(prompt)
        else:
            raise ValueError(f"サポートされていないAPI種類: {self.api_type}")
    
    def _generate_claude_story(self, prompt):
        """Claude API使用"""
        try:
            st.info("🧠 Claude APIに接続中...")
            
            headers = {
                "x-api-key": self.api_key,
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"
            }
            
            data = {
                "model": "claude-3-haiku-20240307",
                "max_tokens": 3000,
                "temperature": 0.9,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                story = result["content"][0]["text"]
                st.success("✅ Claude APIでショートショート生成成功！")
                return story
            else:
                error_msg = f"Claude API エラー: ステータスコード {response.status_code}"
                try:
                    error_detail = response.json()
                    if 'error' in error_detail:
                        error_msg += f" - {error_detail['error'].get('message', '')}"
                except:
                    pass
                st.error(error_msg)
                raise Exception(error_msg)
                
        except requests.exceptions.Timeout:
            error_msg = "Claude API 接続タイムアウト"
            st.error(error_msg)
            raise Exception(error_msg)
        except requests.exceptions.RequestException as e:
            error_msg = f"Claude API 接続エラー: {str(e)}"
            st.error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"Claude API エラー: {str(e)}"
            st.error(error_msg)
            raise Exception(error_msg)
    
    def _generate_grok_story(self, prompt):
        """Grok API使用"""
        try:
            st.info("🚀 Grok APIに接続中...")
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "grok-beta",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 3000,
                "temperature": 0.9
            }
            
            response = requests.post(
                "https://api.x.ai/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                story = result["choices"][0]["message"]["content"]
                st.success("✅ Grok APIでショートショート生成成功！")
                return story
            else:
                error_msg = f"Grok API エラー: ステータスコード {response.status_code}"
                try:
                    error_detail = response.json()
                    if 'error' in error_detail:
                        error_msg += f" - {error_detail['error'].get('message', '')}"
                except:
                    pass
                st.error(error_msg)
                raise Exception(error_msg)
                
        except requests.exceptions.Timeout:
            error_msg = "Grok API 接続タイムアウト"
            st.error(error_msg)
            raise Exception(error_msg)
        except requests.exceptions.RequestException as e:
            error_msg = f"Grok API 接続エラー: {str(e)}"
            st.error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"Grok API エラー: {str(e)}"
            st.error(error_msg)
            raise Exception(error_msg)
    
    def _generate_openai_story(self, prompt):
        """OpenAI API使用"""
        try:
            st.info("🤖 OpenAI APIに接続中...")
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 3000,
                "temperature": 0.9
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                story = result["choices"][0]["message"]["content"]
                st.success("✅ OpenAI APIでショートショート生成成功！")
                return story
            else:
                error_msg = f"OpenAI API エラー: ステータスコード {response.status_code}"
                try:
                    error_detail = response.json()
                    if 'error' in error_detail:
                        error_msg += f" - {error_detail['error'].get('message', '')}"
                except:
                    pass
                st.error(error_msg)
                raise Exception(error_msg)
                
        except requests.exceptions.Timeout:
            error_msg = "OpenAI API 接続タイムアウト"
            st.error(error_msg)
            raise Exception(error_msg)
        except requests.exceptions.RequestException as e:
            error_msg = f"OpenAI API 接続エラー: {str(e)}"
            st.error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"OpenAI API エラー: {str(e)}"
            st.error(error_msg)
            raise Exception(error_msg)
    
    def _generate_gemini_story(self, prompt):
        """Gemini API使用"""
        try:
            st.info("✨ Gemini APIに接続中...")
            
            headers = {"Content-Type": "application/json"}
            
            data = {
                "contents": [{"parts": [{"text": prompt}]}]
            }
            
            response = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={self.api_key}",
                headers=headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                story = result["candidates"][0]["content"]["parts"][0]["text"]
                st.success("✅ Gemini APIでショートショート生成成功！")
                return story
            else:
                error_msg = f"Gemini API エラー: ステータスコード {response.status_code}"
                try:
                    error_detail = response.json()
                    if 'error' in error_detail:
                        error_msg += f" - {error_detail['error'].get('message', '')}"
                except:
                    pass
                st.error(error_msg)
                raise Exception(error_msg)
                
        except requests.exceptions.Timeout:
            error_msg = "Gemini API 接続タイムアウト"
            st.error(error_msg)
            raise Exception(error_msg)
        except requests.exceptions.RequestException as e:
            error_msg = f"Gemini API 接続エラー: {str(e)}"
            st.error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"Gemini API エラー: {str(e)}"
            st.error(error_msg)
            raise Exception(error_msg)

class StoryElementManager:
    """物語要素管理"""
    
    def __init__(self):
        self.story_elements = []
        self.total_stars = 0
        self.load_story_elements()
    
    def load_story_elements(self):
        """JSONファイル読み込み"""
        # スクリプトと同じディレクトリを基準にする
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # スクリプトと同じディレクトリからJSONファイルを検索
        json_files = [
            os.path.join(script_dir, "story_elements.json"),
            os.path.join(script_dir, "story_elements - コピー.json")
        ]
        
        for file_path in json_files:
            try:
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        self.story_elements = json.load(f)
                    self.total_stars = sum(len(item["stars"]) for item in self.story_elements)
                    # 成功時のみシンプルに表示
                    return
            except Exception as e:
                # エラー時のみ表示
                filename = os.path.basename(file_path)
                st.error(f"⚠️ {filename} 読み込みエラー: {str(e)}")
                continue
        
        # フォールバック：サンプルデータ
        st.warning("⚠️ JSONファイルが見つかりません。サンプルデータを使用します。")
        self.story_elements = [
            {
                "item": "【合言葉】",
                "stars": [
                    "★１．合言葉で、味方であるか否かを確認する。",
                    "★２．警察や探偵が、合言葉を用いて犯罪組織に潜入する。"
                ]
            },
            {
                "item": "【魔法】",
                "stars": [
                    "★１．触れたものを花に変える魔法。",
                    "★２．時間を巻き戻す魔法。"
                ]
            },
            {
                "item": "【記憶】",
                "stars": [
                    "★１．記憶を失くした主人公。",
                    "★２．他人の記憶を見ることができる能力。",
                    "★３．記憶を物質化して取り出す技術。"
                ]
            },
            {
                "item": "【時間】",
                "stars": [
                    "★１．時間が止まった世界。",
                    "★２．一日が24時間より短くなった世界。",
                    "★３．過去と未来を同時に体験する。"
                ]
            },
            {
                "item": "【機械】",
                "stars": [
                    "★１．感情を持った機械。",
                    "★２．人間と機械の立場が逆転した世界。",
                    "★３．機械が壊れると人間も壊れる。"
                ]
            }
        ]
        self.total_stars = sum(len(item["stars"]) for item in self.story_elements)
    
    def extract_elements(self, count):
        """要素抽出"""
        if not self.story_elements:
            return []
        
        selected_elements = []
        used_stars = set()
        
        attempts = 0
        max_attempts = min(count * 10, self.total_stars)
        
        while len(selected_elements) < count and attempts < max_attempts:
            attempts += 1
            
            item_data = random.choice(self.story_elements)
            item_name = item_data["item"]
            
            available_stars = [star for star in item_data["stars"] if star not in used_stars]
            
            if available_stars:
                selected_star = random.choice(available_stars)
                used_stars.add(selected_star)
                selected_elements.append((item_name, selected_star))
        
        return selected_elements
    
    def get_replacement_element(self, used_stars):
        """使用済み要素を除いて新しい要素を1つ取得"""
        attempts = 0
        max_attempts = 100
        
        while attempts < max_attempts:
            attempts += 1
            
            item_data = random.choice(self.story_elements)
            item_name = item_data["item"]
            
            available_stars = [star for star in item_data["stars"] if star not in used_stars]
            
            if available_stars:
                selected_star = random.choice(available_stars)
                return (item_name, selected_star)
        
        return None
    
    def generate_shortshort_prompt(self, selected_elements, word_count):
        """ショートショート専用プロンプト生成"""
        
        prompt = f"""あなたは星新一のような天才ショートショート作家です。

# 創作ミッション
読者が最後まで読んだ瞬間に「まさか！」と驚き、「なるほど！」と納得する、記憶に残る傑作ショートショートを創作してください。

# 基本設定
- 文字数: 約{word_count}文字
- ジャンル: ショートショート（掌編小説）
- 必須要件: 意外なオチで読者を驚かせること

# 必須使用要素
"""
        
        for i, (item, star) in enumerate(selected_elements, 1):
            prompt += f"{i}. {item} {star}\n"
        
        prompt += f"""
# ショートショートの絶対条件
- 読者の予想を完全に裏切る意外なオチ・どんでん返しで終わる
- 短い中に完結した物語を構築する（起承転結の巧妙な構成）
- 無駄のない簡潔で洗練された文章
- 最後の一行で全てがひっくり返る衝撃的な結末
- 日常の中に潜む非日常、または予想外の真実の発見
- 読後に深い余韻と「なるほど感」を残す
- 一度読んだら忘れられない印象的なストーリー

# 物語要素の使用について
上記の必須使用要素を参考にしながら創作してください。ただし、物語要素の間に辻褄を持たせるのが困難な場合、いくつかの物語要素を無視しても構いません。構成要素をすべて使い切ることよりも、ショートショートとしての面白さや完成度を優先してください。自然で魅力的なストーリーを作ることが最も重要です。

# 重要指示
- 冒頭から読者を引き込む魅力的な導入で始める
- 中盤で読者にある方向の期待を抱かせる
- 結末で期待を見事に裏切り、全く予想外の真実を明かす
- オチは論理的でありながら意外性に富んでいること
- 伏線は subtle に仕込み、読み返した時に「ああ、そういうことか！」と気づかせる
- 人間の心理、社会の皮肉、科学技術の盲点など、深いテーマを含ませる
- 星新一のような、ユーモアと哲学が混在した独特の味わいを出す

読者が「これは普通の話だな」と思って読み進めているうちに、最後の最後で「え！？そういうことだったの！？」と仰天するような、究極のどんでん返しショートショートを創作してください。

この作品を読んだ読者が、友人に「すごいショートショートを読んだよ！」と興奮して話したくなるような、記憶に焼き付く傑作を生み出してください。"""
        
        return prompt

def create_story_group_output(story_group):
    """作品群のアウトプットテキストを作成（☆評価順）"""
    timestamp = datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
    
    # ☆評価でソート（降順）
    sorted_stories = sorted(story_group, key=lambda x: x.get('user_rating', 0), reverse=True)
    
    output_text = f"""# ショートショート作品群
生成日時: {timestamp}
作品数: {len(story_group)}作品

"""
    
    for i, story_data in enumerate(sorted_stories, 1):
        rating_stars = "☆" * story_data.get('user_rating', 0)
        output_text += f"""## 作品 {i} {rating_stars}
生成時刻: {story_data['timestamp']}
使用要素数: {len(story_data['elements'])}個

### 使用した物語要素:
"""
        for j, (item, star) in enumerate(story_data['elements'], 1):
            output_text += f"{j}. {item} {star}\n"
        
        output_text += f"""
### ショートショート:
{story_data['story']}

"""
        output_text += "="*80 + "\n\n"
    
    return output_text

def extract_story_title(story):
    """ショートショートからタイトルを抽出"""
    lines = story.split('\n')
    
    # 最初の行が『』「」で囲まれている場合はそれをタイトルとする
    first_line = lines[0].strip() if lines else ""
    if first_line.startswith(('『', '「')) and first_line.endswith(('』', '」')):
        title = first_line.replace('『', '').replace('』', '').replace('「', '').replace('」', '')
        return title[:20] if title else "無題"
    
    # 最初の文から推測
    for line in lines:
        line = line.strip()
        if line and not line.startswith(('「', '『')):
            words = line.replace('。', '').replace('、', '').replace('（', '').replace('）', '').split()
            if len(words) >= 2:
                title = ''.join(words[:2])
            else:
                title = line[:15]
            
            # 記号や空白を除去
            title = re.sub(r'[^\w]', '', title)
            return title[:15] if title else "無題"
    
    return "無題"

def display_element_selection_interface(element_manager):
    """シンプルな物語要素選択インターフェース"""
    
    # セッション状態の初期化
    if 'current_elements' not in st.session_state:
        st.session_state.current_elements = []
        st.session_state.used_stars = set()
        st.session_state.element_texts = []  # 編集可能なテキスト用
    
    # 初回要素抽出
    if not st.session_state.current_elements:
        st.session_state.current_elements = element_manager.extract_elements(5)
        st.session_state.used_stars = {star for item, star in st.session_state.current_elements}
        # 初期テキストを設定
        st.session_state.element_texts = [f"{item}{star}" for item, star in st.session_state.current_elements]
    
    # element_textsの長さを現在の要素数に合わせる
    while len(st.session_state.element_texts) < len(st.session_state.current_elements):
        item, star = st.session_state.current_elements[len(st.session_state.element_texts)]
        st.session_state.element_texts.append(f"{item}{star}")
    
    st.markdown("**🎲 物語要素**")
    st.markdown(f"**現在の要素数: {len(st.session_state.current_elements)}個**")
    
    # 要素追加ボタンを最初に配置
    col_add, col_refresh = st.columns([1, 1])
    with col_add:
        if st.button("➕ 要素を1個追加", use_container_width=True):
            new_element = element_manager.get_replacement_element(st.session_state.used_stars)
            if new_element:
                st.session_state.current_elements.append(new_element)
                st.session_state.used_stars.add(new_element[1])
                # 新しい要素のテキストを追加
                st.session_state.element_texts.append(f"{new_element[0]}{new_element[1]}")
                st.rerun()
    
    with col_refresh:
        if st.button("🔄 全要素を再抽出", use_container_width=True):
            st.session_state.current_elements = element_manager.extract_elements(5)
            st.session_state.used_stars = {star for item, star in st.session_state.current_elements}
            # テキストも再設定
            st.session_state.element_texts = [f"{item}{star}" for item, star in st.session_state.current_elements]
            st.rerun()
    
    st.markdown("---")
    
    # 要素表示と編集・削除機能
    elements_to_remove = []
    
    for i in range(len(st.session_state.current_elements)):
        col_element, col_delete = st.columns([6, 1])
        
        with col_element:
            # 編集可能なテキストボックス
            current_text = st.session_state.element_texts[i] if i < len(st.session_state.element_texts) else f"{st.session_state.current_elements[i][0]}{st.session_state.current_elements[i][1]}"
            edited_text = st.text_input(
                f"要素 {i+1}",
                value=current_text,
                key=f"element_text_{i}",
                help="この要素を手動で編集できます"
            )
            # テキストが変更された場合、保存
            if edited_text != current_text:
                if i < len(st.session_state.element_texts):
                    st.session_state.element_texts[i] = edited_text
                else:
                    st.session_state.element_texts.append(edited_text)
        
        with col_delete:
            if st.button("🗑️", key=f"delete_element_{i}", help="この要素を削除"):
                elements_to_remove.append(i)
    
    # 削除処理
    if elements_to_remove:
        for i in reversed(elements_to_remove):
            if i < len(st.session_state.current_elements):
                removed_item, removed_star = st.session_state.current_elements[i]
                if removed_star in st.session_state.used_stars:
                    st.session_state.used_stars.remove(removed_star)
                st.session_state.current_elements.pop(i)
            if i < len(st.session_state.element_texts):
                st.session_state.element_texts.pop(i)
        st.rerun()
    
    # 生成ボタン
    st.markdown("---")
    if st.button("✅ 生成", type="primary", use_container_width=True):
        if st.session_state.element_texts:
            # 編集されたテキストを要素として返す
            edited_elements = []
            for i, text in enumerate(st.session_state.element_texts):
                if text.strip():  # 空でない場合のみ追加
                    # 編集されたテキストを擬似的な(item, star)形式に変換
                    edited_elements.append(("【編集済み】", text.strip()))
            
            if edited_elements:
                return True, edited_elements
            else:
                st.error("物語要素が1個以上必要です")
                return False, []
        else:
            st.error("物語要素が1個以上必要です")
            return False, []
    
    # 現在の編集済み要素を返す（生成しない場合）
    current_edited_elements = []
    for i, text in enumerate(st.session_state.element_texts):
        if text.strip():
            current_edited_elements.append(("【編集済み】", text.strip()))
    
    return False, current_edited_elements

def main():
    if 'element_manager' not in st.session_state:
        st.session_state.element_manager = StoryElementManager()
    
    # 現在の作品群を初期化
    if 'current_story_group' not in st.session_state:
        st.session_state.current_story_group = []
    
    # 生成結果を初期化
    if 'generation_result' not in st.session_state:
        st.session_state.generation_result = None
    
    st.markdown("### 📚 ショートショート生成システム")
    st.markdown("**出典**: 『物語要素事典』（2021年4月15日改訂）https://www.lib.agu.ac.jp/yousojiten/")
    
    if st.session_state.element_manager.story_elements:
        st.success(f"✅ 物語要素データ: {st.session_state.element_manager.total_stars}個の要素読み込み完了")
    else:
        st.warning("⚠️ JSONファイルが読み込まれませんでした。サンプルデータを使用します。")
    
    with st.sidebar:
        st.header("📌 AI接続設定")
        
        # API接続の有無を選択
        connection_mode = st.radio(
            "実行モード",
            ["AIへのプロンプトのみ生成", "AIに接続してお話を生成"],
            index=0
        )
        
        if connection_mode == "AIに接続してお話を生成":
            st.header("🤖 AI設定")
            
            ai_options = [
                "🧠 Claude (Anthropic)",
                "🚀 Grok (xAI)",
                "🤖 OpenAI GPT",
                "✨ Gemini (Google)"
            ]
            
            selected_ai = st.selectbox("使用するAI", ai_options)
            
            if "Claude" in selected_ai:
                api_type = "claude"
                api_key = st.text_input(
                    "🧠 Claude APIキー",
                    type="password",
                    help="Anthropic ClaudeのAPIキーを入力してください"
                )
                if api_key:
                    st.success("✅ Claude APIキー設定完了")
                    
            elif "Grok" in selected_ai:
                api_type = "grok"
                api_key = st.text_input(
                    "🚀 Grok APIキー",
                    type="password",
                    help="xAI GrokのAPIキーを入力してください"
                )
                if api_key:
                    st.success("✅ Grok APIキー設定完了")
                    
            elif "OpenAI" in selected_ai:
                api_type = "openai"
                api_key = st.text_input(
                    "🤖 OpenAI APIキー",
                    type="password",
                    help="OpenAIのAPIキーを入力してください"
                )
                if api_key:
                    st.success("✅ OpenAI APIキー設定完了")
                    
            elif "Gemini" in selected_ai:
                api_type = "gemini"
                api_key = st.text_input(
                    "✨ Gemini APIキー",
                    type="password",
                    help="Google GeminiのAPIキーを入力してください"
                )
                if api_key:
                    st.success("✅ Gemini APIキー設定完了")
        else:
            # プロンプトのみ生成の場合
            api_type = "prompt_only"
            api_key = "prompt_only"
            st.info("📝 プロンプトのみ生成モード")
        
        st.markdown("---")
        
        st.header("⚙️ 設定")
        word_count = st.number_input("文字数", value=1200, min_value=400, max_value=3000, step=100)
    
    # 物語要素選択インターフェース
    generate_requested, selected_elements = display_element_selection_interface(st.session_state.element_manager)
    
    # ショートショート生成実行
    if generate_requested:
        if connection_mode == "AIへのプロンプトのみ生成":
            # プロンプトのみ生成
            prompt = st.session_state.element_manager.generate_shortshort_prompt(
                selected_elements, word_count
            )
            
            st.markdown("---")
            st.markdown("**📝 生成されたプロンプト**")
            st.markdown("以下のプロンプトをAIにコピー＆ペーストしてください：")
            
            st.code(prompt, language="text")
            
            # プロンプトをダウンロード可能にする
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            prompt_filename = f"{timestamp}_ショートショートプロンプト.txt"
            
            st.download_button(
                label="📥 プロンプトをダウンロード",
                data=prompt,
                file_name=prompt_filename,
                mime="text/plain",
                use_container_width=True
            )
            
        else:
            # API接続での生成
            # API設定確認
            if not api_key:
                st.error(f"⚠️ APIキーが必要です")
                st.stop()
            
            try:
                # 生成システム初期化
                story_generator = ShortStoryGenerator(api_key, api_type)
                
                # ショートショート特化プロンプト生成
                prompt = st.session_state.element_manager.generate_shortshort_prompt(
                    selected_elements, word_count
                )
                
                # ショートショート生成
                with st.spinner("📖 ショートショート生成中..."):
                    story = story_generator.generate_story(prompt)
                
                if story:
                    # 結果保存（要素のディープコピーを作成）
                    story_data = {
                        "story": story,
                        "elements": [(item, star) for item, star in selected_elements],  # ディープコピー
                        "prompt": prompt,
                        "timestamp": datetime.now().strftime("%H:%M:%S"),
                        "word_count": word_count,
                        "user_rating": 0  # 初期評価は0
                    }
                    
                    # 現在の作品群に追加
                    st.session_state.current_story_group.append(story_data)
                    
                    # 生成結果を更新（前回の結果をクリア）
                    st.session_state.generation_result = story_data
                    
                    st.success("✅ ショートショート生成完了！")
                    st.rerun()
            
            except Exception as e:
                st.error(f"ショートショート生成エラー: {str(e)}")
                st.error("APIキーが正しいか、ネットワーク接続を確認してください。")
    
    # 生成結果表示
    if st.session_state.generation_result:
        st.markdown("---")
        st.markdown("**📖 生成結果**")
        
        story_data = st.session_state.generation_result
        
        # 使用要素表示
        st.markdown("**使用した物語要素:**")
        for j, (item, star) in enumerate(story_data['elements'], 1):
            st.markdown(f"**{j}.** {item}{star}")
        
        # ショートショート表示
        st.markdown("**ショートショート:**")
        st.write(story_data['story'])
        
        # ユーザー評価入力（本文の後）
        st.markdown("---")
        col_rating, col_spacer = st.columns([2, 3])
        
        with col_rating:
            st.markdown("**あなたの評価**")
            current_rating = story_data.get('user_rating', 0)
            user_rating = st.selectbox(
                "☆の数",
                options=[0, 1, 2, 3, 4, 5],
                index=current_rating,
                format_func=lambda x: "☆" * x if x > 0 else "未評価",
                key="user_rating_input"
            )
            
            # 評価を保存して要素選択部分に戻る
            if user_rating != story_data.get('user_rating', 0):
                # 現在の作品群内の該当作品を更新
                for i, group_story in enumerate(st.session_state.current_story_group):
                    if group_story['timestamp'] == story_data['timestamp']:
                        st.session_state.current_story_group[i]['user_rating'] = user_rating
                        st.session_state.generation_result['user_rating'] = user_rating
                        break
                # 評価後に要素選択部分に戻る
                st.success(f"評価を保存しました: {'☆' * user_rating if user_rating > 0 else '未評価'}")
                time.sleep(1)
                st.rerun()
    
    # 作品群表示とダウンロード
    if st.session_state.current_story_group:
        st.markdown("---")
        st.markdown(f"**📋 現在の作品群 ({len(st.session_state.current_story_group)}作品)**")
        
        # ☆評価でソート（降順）
        sorted_stories = sorted(st.session_state.current_story_group, key=lambda x: x.get('user_rating', 0), reverse=True)
        
        # 作品群の簡易リスト表示
        for i, story_data in enumerate(sorted_stories, 1):
            rating_stars = "☆" * story_data.get('user_rating', 0)
            rating_display = rating_stars if rating_stars else "未評価"
            
            with st.expander(f"作品 {i} [{rating_display}] - {story_data['timestamp']} - 要素{len(story_data['elements'])}個"):
                st.markdown("**ショートショート:**")
                st.write(story_data['story'])
        
        # ダウンロードとリセット
        story_group_output = create_story_group_output(st.session_state.current_story_group)
        creation_date = datetime.now().strftime('%Y%m%d_%H%M')
        
        # 上位作品のタイトルを取得
        if sorted_stories:
            top_story = sorted_stories[0]
            top_title = extract_story_title(top_story['story'])
        else:
            top_title = "作品なし"
        
        filename = f"{creation_date}_{top_title}他_{len(st.session_state.current_story_group)}作品.txt"
        
        col_download, col_reset = st.columns([3, 1])
        
        with col_download:
            # ダウンロード後に作品群をリセット
            if st.download_button(
                label="📥 作品群をダウンロード（ダウンロード後にリセット）",
                data=story_group_output,
                file_name=filename,
                mime="text/plain",
                use_container_width=True,
                key="download_and_reset"
            ):
                # ダウンロードボタンが押された場合、作品群をリセット
                st.session_state.current_story_group = []
                st.session_state.generation_result = None
                st.success("✅ 作品群をダウンロードしました。作品群をリセットしました。")
                time.sleep(1)
                st.rerun()
        
        with col_reset:
            # 手動リセットボタン
            if st.button("🗑️ リセット", use_container_width=True, help="作品群をクリアします"):
                st.session_state.current_story_group = []
                st.session_state.generation_result = None
                st.success("✅ 作品群をリセットしました。")
                time.sleep(1)
                st.rerun()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"⚠ システムエラー: {str(e)}")
        st.write("詳細:")
        import traceback
        st.code(traceback.format_exc())
