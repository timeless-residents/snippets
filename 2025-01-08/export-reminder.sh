#!/bin/bash

# 設定
LIST_NAME="iPhone自動化"
OUTPUT_DIR="$HOME/Documents"
FILE_NAME="iphone-automation.pdf"

# AppleScriptの実行
osascript <<EOF
tell application "Reminders"
    activate
    delay 1

    # リストの選択
    try
        set targetList to list "$LIST_NAME"
        show targetList
    on error errMsg
        log "エラー: リストが見つかりませんでした: " & errMsg
        return
    end try
    delay 1
    
    tell application "System Events"
        tell process "Reminders"
        
            # プリントダイアログを開く
            keystroke "p" using command down
            
            # ダイアログが表示されるのを待つ
            repeat until exists window "Print"
                delay 0.1
            end repeat
            
            
            # PDFボタンをクリック
            try
                click button "PDF" of window "Print"
                delay 1
            on error errMsg
                log "エラー: PDFボタンをクリックできませんでした: " & errMsg
                 return
            end try
            
            # 「PDFとして保存」メニューを選択
           try
             click menu item "Save as PDF…" of menu of button "PDF" of window "Print"
            delay 1
           on error errMsg
                log "エラー: 保存メニュー項目をクリックできませんでした: " & errMsg
                return
            end try


            # 「名前を付けて保存」ダイアログが表示されるのを待つ
            repeat until exists window "Save"
                delay 0.1
            end repeat
            
            
           # ファイル名を入力
           try
            set value of text field 1 of window "Save" to "$FILE_NAME"
                delay 0.5

          on error errMsg
                log "エラー: ファイル名の入力に失敗しました" & errMsg
                return
            end try
            
            
            # 保存先を指定
            try
                keystroke "g" using {command down, shift down}
                delay 0.2
                
                repeat until exists window "Go to Folder"
                    delay 0.1
                end repeat

                set value of text field 1 of window "Go to Folder" to "$OUTPUT_DIR"
                delay 0.2
                
                keystroke return
                delay 0.2

            on error errMsg
                log "エラー: 保存先の指定に失敗しました: " & errMsg
                return
            end try

            # 保存を確定
            try
                keystroke return
                delay 1
                
               repeat while exists window "Save"
                 delay 0.1
               end repeat
                
             on error errMsg
                log "エラー: 保存ボタンの確定に失敗しました: " & errMsg
                return
            end try
        end tell
    end tell
end tell
EOF

# スクリプトの実行結果を確認
if [ $? -eq 0 ]; then
    echo "PDFの出力が完了しました"
else
    echo "エラーが発生しました"
fi