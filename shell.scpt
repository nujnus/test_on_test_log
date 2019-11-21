on run {commands}
  tell application "iTerm2"
    tell current window
      create tab with profile "item"
    end tell
    tell first session of current tab of current window
      #split horizontally with profile "item"
      write text  commands
    end tell
  end tell
end run

