from modules.ebayAppWidgets import appDlg

options = appDlg().mainloop()

for key in options.keys():
    print(key)
    print(options[key])