from .WS2801Wrapper import WS2801Wrapper
from threading import Thread, Event
from .EffectUtils import run_effect


def effect(pixels: WS2801Wrapper, event: Event, sleep=0.025):
    do_run = True
    color_index = 0
    while do_run:
        pixels.set_pixels_colorwheel(color_index)
        pixels.show()
        color_index += 1
        if color_index > 255:
            color_index = 0
        if event.wait(sleep):
            do_run = False

# run with python3 -m WS2801.EffectColorChange          
if __name__ == "__main__":
    run_effect(effect)
