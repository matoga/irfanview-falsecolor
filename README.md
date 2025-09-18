# irfanview-falsecolor

External editor for colorizing OD images in IrfanView.

## How to install

1. Download and unpack zip: https://github.com/matoga/irfanview-falsecolor/releases/download/v1.0/colorize_od.zip
2. Go to Options -> Properties/Settings -> Miscellaneous and set external editors. Choose 1. and put:
   ```
   C:\path\to\the\file\colorize_od.exe "$F"
   ```
3. Pressing Shift+1 creates a colored image & opens it in IrfanView.

## Other options

`--colorbar` shows the colorbar as well.

## Details

The created files are stored in:
```
C:\temp\OD_Colorized
```
