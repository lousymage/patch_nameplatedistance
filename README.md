# WoW 1.12.1 nameplate distance patch

Sets the nameplate distance in a stock WoW 1.12.1 `WoW.exe`.

```sh
python3 patch_nameplates.py WoW.exe 41
```

The distance is in yards and defaults to 41. The script creates `WoW.exe.bak` before patching and refuses to overwrite an existing backup. To undo the patch, replace `WoW.exe` with the backup.
