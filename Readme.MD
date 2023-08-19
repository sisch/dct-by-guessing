# DCT (Discrete Cosinus Transform)
DO NOT USE THIS CODE FOR ANYTHING IMPORTANT.

## Background
We were discussing topics of a signal processing lecture in a small group and I had never heard of DCT before.
Therefore, this implementation of DCT is based on three assumptions I made just by the name and context of compression:
1. I need to transform a window of pixels, e.g. 3x3
2. I need to transform pixel color values independently, e.g. RGB
3. I need to take the cosine of a color value and map it to either -1, 0 or 1 (because of the discrete part)
    and average it over the window
   * step = {-1: <0.5, 1: >0.5, 0: else}
   * cos( color_value / 255 * 2 * PI ) 
   * new Pixel color = acos(avg(step(cos(...))))
   * each pixel in window gets this value

## Result
The result is a very bad compression of the image. The outcome is "artsy" at best, ugly at worst.
The colors, especially white are very unstable. I would consider it more of a style transfer than a compression (even
though it technically reduces the file size, because it reduces the complexity).
Also, I am aware, that the compression is not quite implemented here, because I am not saving my own format, that reduces
the window to a single color and coordinate (think like a palette in gifs).

### Original
![Original](test_image_original.png)

### Compressed
![Result](test_image_dct.png)

## Outlook
1. This project is probably going sit here and die.
2. If I came back and picked it up again, I could try to implement a reversal of the process, 
so the colors would actually be reverted, however getting around the step function would be a challenge. As there 
is no proper inversion of the step function, so I lose too much information in the current process.

## Usage
```bash
 python3 main.py [path_to_original_image]
```