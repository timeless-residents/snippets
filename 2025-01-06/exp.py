import subprocess
from datetime import datetime
from weasyprint import HTML

class MacOSReminderPDF:
    def __init__(self, list_name):
        self.list_name = list_name

    def get_reminders(self):
        """AppleScriptを使用してリマインダーを取得"""
        applescript = f'''
        tell application "Reminders"
            set myList to list "{self.list_name}"
            set output to ""
            repeat with r in (reminders of myList)
                set output to output & name of r & "||"
                if due date of r exists then
                    set output to output & ((due date of r) as string) & "||"
                else
                    set output to output & "none||"
                end if
                set output to output & (priority of r as string) & "||"
                set output to output & (completed of r as string) & "||"
                if body of r exists then
                    set output to output & body of r & "###"
                else
                    set output to output & "none###"
                end if
            end repeat
            return output
        end tell
        '''
        
        try:
            process = subprocess.run(['osascript', '-e', applescript], 
                                   capture_output=True, text=True)
            
            if process.stderr:
                print(f"Error: {process.stderr}")
                return []
                
            reminders = []
            if process.stdout.strip():
                items = process.stdout.strip().split('###')
                for item in items:
                    if item:
                        parts = item.split('||')
                        if len(parts) >= 5:
                            reminders.append({
                                'title': parts[0],
                                'due_date': None if parts[1] == 'none' else parts[1],
                                'priority': int(parts[2]) if parts[2].isdigit() else 0,
                                'completed': parts[3].lower() == 'true',
                                'notes': None if parts[4] == 'none' else parts[4]
                            })
            return reminders
            
        except Exception as e:
            print(f"Error getting reminders: {e}")
            return []

    def create_html_content(self, reminders):
        """HTMLコンテンツの生成"""
        rows = []
        for reminder in reminders:
            due_date = reminder.get('due_date', '')
            priority = reminder.get('priority', 0)
            priority_str = '⭐️' * priority if priority else ''
            completed_str = '✓' if reminder.get('completed') else ''
            notes = reminder.get('notes', '')
            
            rows.append(f'''
                <tr>
                    <td>{reminder.get('title', '')}</td>
                    <td>{due_date}</td>
                    <td>{priority_str}</td>
                    <td class="center">{completed_str}</td>
                    <td>{notes}</td>
                </tr>
            ''')
            
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                @page {{
                    size: A4;
                    margin: 2cm;
                }}
                body {{
                    font-family: -apple-system, "Hiragino Kaku Gothic ProN", sans-serif;
                    font-size: 10pt;
                }}
                h1 {{
                    font-size: 16pt;
                    margin-bottom: 20px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 20px;
                }}
                th, td {{
                    border: 1px solid #000;
                    padding: 8px;
                    text-align: left;
                }}
                th {{
                    background-color: #666;
                    color: white;
                }}
                .center {{
                    text-align: center;
                }}
                .footer {{
                    font-size: 8pt;
                    color: #666;
                }}
            </style>
        </head>
        <body>
            <h1>リマインダー: {self.list_name}</h1>
            <table>
                <thead>
                    <tr>
                        <th>タイトル</th>
                        <th>期限</th>
                        <th>優先度</th>
                        <th>完了</th>
                        <th>メモ</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(rows)}
                </tbody>
            </table>
            <div class="footer">
                出力日時: {datetime.now().strftime('%Y/%m/%d %H:%M:%S')}
            </div>
        </body>
        </html>
        '''

    def create_pdf(self, output_path="reminders.pdf"):
        """PDFファイルを生成"""
        reminders = self.get_reminders()
        if not reminders:
            print("No reminders found or error occurred")
            return
            
        html_content = self.create_html_content(reminders)
        HTML(string=html_content).write_pdf(output_path)
        print(f"PDF created: {output_path}")

if __name__ == "__main__":
    generator = MacOSReminderPDF(list_name="iPhone自動化")
    generator.create_pdf("reminders.pdf")