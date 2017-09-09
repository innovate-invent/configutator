import os, pickle
from inspect import signature, Parameter

from asciimatics.screen import Screen, StopApplication, ResizeScreenError
from asciimatics.scene import Scene
import asciimatics.widgets as Widgets
from asciimatics.event import KeyboardEvent

from .util import getParamDoc

# -- TUI Builder --

def boolParam(param: Parameter, desc: str, layout: Widgets.Layout, maxWidth = None):
    layout.add_widget(Widgets.CheckBox(desc, param.name, param.name))

def textParam(param: Parameter, desc: str, layout: Widgets.Layout, maxWidth = None):
    layout.add_widget(Widgets.Text(name=param.name, label=param.name))
    if desc:
        lastI = 0
        for i in range(maxWidth or len(desc), len(desc), maxWidth or len(desc)):
            layout.add_widget(Widgets.Label(desc[lastI:i]))
            lastI = i
        layout.add_widget(Widgets.Divider(False))

widgetMap = {
    'Path': textParam,
    'PathOrNone': textParam,
    'str': textParam,
    'int': textParam,
    'bool': boolParam
}

def _configUI(screen, functions: list, argMap: dict, call_name, title=''):
    Widgets.Frame.palette['edit_text'] = (Screen.COLOUR_BLACK, Screen.A_NORMAL, Screen.COLOUR_CYAN)
    Widgets.Frame.palette['section_header'] = (Screen.COLOUR_GREEN, Screen.A_UNDERLINE, Screen.COLOUR_BLUE)

    windowWidth = screen.width * 2 // 3
    historyPath = os.path.expanduser('~/.configutator_history')
    if os.path.exists(historyPath):
        with open(historyPath, 'rb') as file:
            history = pickle.load(file)
            if call_name in history:
                argMap.update(history[call_name])
    window = Widgets.Frame(screen, screen.height * 2 // 3, windowWidth, title=title, data=argMap)
    scene = Scene([window])

    def saveHistory():
        history = {}
        if os.path.exists(historyPath):
            with open(historyPath, 'rb') as file:
                history = pickle.load(file)
        history[call_name] = window.data
        with open(historyPath, 'wb+') as file:
            pickle.dump(history, file)

    def _go():
        window.save()
        saveHistory()
        argMap.update(window.data)
        raise StopApplication('')
    def _close():
        window.save()
        saveHistory()
        argMap.clear()
        raise StopApplication('')
    def _save():
        pass
    def _load():
        pass
    def inputHandler(event):
        if isinstance(event, KeyboardEvent):
            c = event.key_code
            # Stop on ctrl+q or ctrl+x or esc
            if c in (17, 24, 27):
                _close()

    for f in functions:
        doc = getParamDoc(f)
        layout = Widgets.Layout([1])
        window.add_layout(layout)
        sig = signature(f)
        if len(functions) > 1:
            label = Widgets.Label(f.__name__+':')
            label.custom_colour = 'section_header'
            layout.add_widget(label)
        for name, param in sig.parameters.items(): #type: str, Parameter
            if param.annotation.__name__ in widgetMap:
                widgetMap[param.annotation.__name__](param, doc.get(name, ''), layout, windowWidth)
        layout.add_widget(Widgets.Divider(False))

    toolbar = Widgets.Layout([1,1,1,1])
    window.add_layout(toolbar)
    load_button = Widgets.Button('Load', _load)
    save_button = Widgets.Button('Save', _save)
    cancel_button = Widgets.Button('Cancel', _close)
    go_button = Widgets.Button('GO', _go)
    #toolbar.add_widget(load_button, 0)
    #toolbar.add_widget(save_button, 1)
    toolbar.add_widget(cancel_button, 2)
    toolbar.add_widget(go_button, 3)

    window.fix()
    screen.play([scene], unhandled_input=inputHandler)

def loadTUI(functions, argMap, call_name, title) -> None:
    while True:
        try:
            Screen.wrapper(_configUI, arguments=(functions, argMap, call_name, title))
        except StopApplication:
            break
        except ResizeScreenError:
            continue