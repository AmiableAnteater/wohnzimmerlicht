from .WS2801Wrapper import WS2801Wrapper
from threading import Thread, Event
from .EffectUtils import run_effect
from time import monotonic


def effect(pixels: WS2801Wrapper, event: Event, stretch_factor=1, speed=10):
    pixel_count = pixels.count()
    stretched_wheel_size = int(round(255 * stretch_factor))
    inverse_factor = 255 / stretched_wheel_size
    zero_pos = 0
    do_run = True
    last_time = monotonic()
    while do_run:
        current_time = monotonic()
        time_delta = current_time - last_time
        #print('delta:' + str(time_delta))
        last_time = current_time
        
        zero_pos += time_delta * speed
        zero_pos = zero_pos % stretched_wheel_size
        #print(str(zero_pos))
        pixel_idx = 0
        pos_iterator = zero_pos
        while pixel_idx < pixel_count:
            color_index = round(pos_iterator * inverse_factor)
            #print('pixel_idx: ' + str(pixel_idx) + 'col_idx:' + str(color_index))
            pixels.set_pixel_colorwheel(color_index, pixel_idx)
            pos_iterator += 1
            if pos_iterator > stretched_wheel_size:
              pos_iterator -= stretched_wheel_size
            pixel_idx += 1
        pixels.show()
        if event.wait(.02):
            do_run = False

           
if __name__ == "__main__":
    run_effect(effect)
