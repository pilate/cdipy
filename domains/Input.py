from .decorators import proxy_target_command



class Input(object):

    def __init__(self, devtools):
        self.devtools = devtools


    @proxy_target_command
    async def dispatchKeyEvent(self, type, modifiers=None, timestamp=None, text=None, unmodifiedText=None, keyIdentifier=None, code=None, key=None, windowsVirtualKeyCode=None, nativeVirtualKeyCode=None, autoRepeat=None, isKeypad=None, isSystemKey=None, location=None):
        """
            Dispatches a key event to the page.
        """


    @proxy_target_command
    async def insertText(self, text):
        """
            This method emulates inserting text that doesn't come from a key press,
for example an emoji keyboard or an IME.
        """


    @proxy_target_command
    async def dispatchMouseEvent(self, type, x, y, modifiers=None, timestamp=None, button=None, buttons=None, clickCount=None, deltaX=None, deltaY=None):
        """
            Dispatches a mouse event to the page.
        """


    @proxy_target_command
    async def dispatchTouchEvent(self, type, touchPoints, modifiers=None, timestamp=None):
        """
            Dispatches a touch event to the page.
        """


    @proxy_target_command
    async def emulateTouchFromMouseEvent(self, type, x, y, button, timestamp=None, deltaX=None, deltaY=None, modifiers=None, clickCount=None):
        """
            Emulates touch event from the mouse event parameters.
        """


    @proxy_target_command
    async def setIgnoreInputEvents(self, ignore):
        """
            Ignores input events (useful while auditing page).
        """


    @proxy_target_command
    async def synthesizePinchGesture(self, x, y, scaleFactor, relativeSpeed=None, gestureSourceType=None):
        """
            Synthesizes a pinch gesture over a time period by issuing appropriate touch events.
        """


    @proxy_target_command
    async def synthesizeScrollGesture(self, x, y, xDistance=None, yDistance=None, xOverscroll=None, yOverscroll=None, preventFling=None, speed=None, gestureSourceType=None, repeatCount=None, repeatDelayMs=None, interactionMarkerName=None):
        """
            Synthesizes a scroll gesture over a time period by issuing appropriate touch events.
        """


    @proxy_target_command
    async def synthesizeTapGesture(self, x, y, duration=None, tapCount=None, gestureSourceType=None):
        """
            Synthesizes a tap gesture over a time period by issuing appropriate touch events.
        """

