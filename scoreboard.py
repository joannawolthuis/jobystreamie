import re
from lxml import etree

def updateHTML(which, what, source):
    regexs = [r'(gameRound">).*(<\/p>)',
              r'(leftPlayer">).*(<\/p>)',
              r'(rightPlayer">).*(<\/p>)',
              r'(leftPlayerScore">).*(<\/p>)',
              r'(rightPlayerScore">).*(<\/p>)']
    useRegex = regexs[which]
    updated = re.sub(useRegex, r"\g<1>" + what + r"\g<2>", source)
    return(updated)



import PySimpleGUI as sg
# All the stuff inside your window.
layout = [  [sg.Text('\t\t  Which round are you in?',font='Calibri 11')],
            [sg.Text(' '*4), sg.InputText(justification="center",font='Calibri 11 bold',key='gameRound')],
            [sg.Text(' '*9), sg.Text('Player 1 name', font='Calibri 11'), sg.Text(' '*16), sg.Text('Player 2 name', font='Calibri 11')],
            [sg.InputText(justification="center",size=(25,1), font='Calibri 11 bold',key='p1name'),
            sg.InputText(justification="center",size=(25,1), font='Calibri 11 bold', key='p2name')],
            [sg.Button("▲",key='p1up'),sg.Button("▼",key='p1down'),
            sg.Text(' '*1),
            sg.Text(0, key='p1score',size=(1,1), font='Courier 30 bold'),sg.Text(' '*29),
            sg.Text(0, key='p2score',size=(1,1), font='Courier 30 bold'),sg.Text(' '),
            sg.Button("▲",key='p2up'),sg.Button("▼",key='p2down')],
            [sg.Text(' '*30),sg.Text('Source HTML file:',font='Calibri 11 bold')],
            [sg.In(justification="center",key='html'), sg.FileBrowse(file_types=(("HTML files", "*.html"),),font='Calibri 11 bold')],
            [],
            [sg.Text('♥ ▬ ♥ ▬ ♥ ▬ ♥ ▬ ♥ ▬ ♥ ▬ ♥ ▬ ♥ ▬ ♥ ▬ ♥ ▬ ♥ ▬ ♥ ▬ ♥ ')],
            [],
            [sg.Text(' '*18), sg.Button('Update HTML', key='update',font='Calibri 11 bold'), sg.Button('Exit Streamie', key='exit',font='Calibri 11 bold')] ]

# Create the Window
window = sg.Window('JobyStreamie', layout,  keep_on_top = True)

p1score = 0
p2score = 0

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event in (None, 'exit'):	# if user closes window or clicks cancel
        break
    if event == 'p1up':
        p1score += 1
        window['p1score'].update(p1score)
    elif event == 'p1down':
        p1score -= 1
        window['p1score'].update(p1score)
    elif event == 'p2up':
        p2score += 1
        window['p2score'].update(p2score)
    elif event == 'p2down':
        p2score -= 1
        window['p2score'].update(p2score)
    elif event == 'update':
        if(values['html'] != ""):
            html  = open(values['html'], "r+")
            template = html.read()
            updated = template
            ofInterest = [values['gameRound'],values['p1name'], values['p2name'], p1score, p2score, values['html']]
            for i in range(0, len(ofInterest)-1, 1):
                updated = updateHTML(which = i,
                what = str(ofInterest[i]),
                source = updated)
            print(updated)
            f = open("ScoreBoardOverlayHolding.html", "w")
            f.write(updated)
            f.close()
window.close()
