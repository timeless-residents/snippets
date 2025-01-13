#!/bin/bash

# デバッグ用のAppleScript
osascript <<EOF
 tell application "Reminders" to activate
 tell application "System Events"
   tell process "Reminders"
       repeat until exists window "Print"
            delay 0.1
       end repeat
      properties of window "Print"
   end tell
 end tell
EOF