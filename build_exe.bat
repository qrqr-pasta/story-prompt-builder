@echo off
chcp 65001 > nul
echo 物語生成プロンプトビルダー exe化スクリプト
echo =============================================
echo.

REM PyInstallerがインストールされているかチェック
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstallerをインストールしています...
    pip install pyinstaller
    if errorlevel 1 (
        echo エラー: PyInstallerのインストールに失敗しました
        pause
        exit /b 1
    )
)

echo PyInstallerでexeファイルを作成中...
echo.

REM 既存のdist, buildフォルダを削除
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist *.spec del /q *.spec

REM exe化実行
pyinstaller --onefile --windowed --name=StoryPromptBuilder --distpath=dist --workpath=build story_prompt_builder.py

if errorlevel 1 (
    echo エラー: exe化に失敗しました
    pause
    exit /b 1
)

echo.
echo =============================================
echo exe化完了！
echo 作成されたファイル: dist\StoryPromptBuilder.exe
echo =============================================
echo.

REM distフォルダが存在するかチェック
if exist "dist\StoryPromptBuilder.exe" (
    echo ファイルサイズ:
    dir "dist\StoryPromptBuilder.exe" | findstr "StoryPromptBuilder.exe"
    echo.
    echo このexeファイルを他の人に渡すことができます。
    echo Pythonがインストールされていないコンピューターでも動作します。
) else (
    echo エラー: exeファイルが見つかりません
)

echo.
pause