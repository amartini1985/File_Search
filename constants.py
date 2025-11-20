from win32api import GetLogicalDriveStrings


DRIVES = GetLogicalDriveStrings().split('\000')[:-1]
