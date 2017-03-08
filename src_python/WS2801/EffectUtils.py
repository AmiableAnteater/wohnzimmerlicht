from .WS2801Wrapper import WS2801Wrapper
from threading import Thread, Event

            
def __wait_for__input(event: Event):
    raw_input()
    event.set()  

def run_effect(target, additional_args):
    event = Event()

    pixels = WS2801Wrapper()
    pixels.clear()
    pixels.show()

    args = (pixels, e) + additional_args if additional_args else (pixels, e)
    t1 = Thread(target=target, name="Effect", args=args)
    t1.start()

    t2 = Thread(target=__wait_for__input, name='Input', args=(e,))
    t2.start()
    
    t1.join()
    t2.join()