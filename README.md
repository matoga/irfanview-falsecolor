# irfanview-falsecolor

External editor for colorizing OD (Optical Density) images in IrfanView.

## How to Install

1. [Download and unpack the ZIP file](https://github.com/matoga/irfanview-falsecolor/releases/download/v1.0/colorize_od.zip).
2. In IrfanView, go to:  
   `Options → Properties/Settings → Miscellaneous → Set external editors`.  
   Choose slot 1 and enter:
   ```
   C:\path\to\the\file\colorize_od.exe "$F"
   ```
3. Press **Shift+1** in IrfanView to create a colorized image and open it.

## Image Assumptions

- Input images are assumed to encode OD as:  
  ```
  OD = 256 - 8 * pixel_value
  ```
- The OD values are colorized within the range **0 to 3**.

## Other Options

Use the `--colorbar` flag to include a colorbar in the output image:
```
colorize_od.exe "$F" --colorbar
```

## Output Location

Colorized files are saved to:
```
C:\temp\OD_Colorized
```
