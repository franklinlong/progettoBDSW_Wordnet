import tkinter as tk
import tkinter.scrolledtext as scrolledtext
from PIL import Image, ImageTk
import ctypes
from tkinter.filedialog import askopenfilename, Toplevel, Frame
import pyautogui as pyautogui
from PyPDF2 import PdfFileReader
from find_definition import *
from utilities import inner_function2
from utilities2 import inner_function2_second
import threading

first_word_start = 0
second_word_start = 0
all_sep_index = []
paragraphs = []

class BkgrFrame(tk.Frame):
    def __init__(self, parent, file_path, width, height):
        super(BkgrFrame, self).__init__(parent, borderwidth=0, highlightthickness=0)

        self.canvas = tk.Canvas(self, width=width, height=height)
        self.canvas.pack()

        pil_img = Image.open(file_path)
        self.img = ImageTk.PhotoImage(pil_img.resize((width, height), Image.ANTIALIAS))
        self.bg = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)

    def add(self, widget, x, y):
        canvas_window = self.canvas.create_window(x, y, anchor=tk.NW, window=widget)
        return widget


class Thread_funct2(threading.Thread):

    _slots_ = 'text_area', 'l1', 'l2','varC','type','varC2', 'text1'

    def __init__(self, text_area, l1, l2,varC,type,varC2):
        threading.Thread.__init__(self)
        self.type = type
        self.l1 = l1
        self.l2 = l2
        self.text_area = text_area
        self.varC = varC
        self.varC2 = varC2

    def set_red(self, word):
        offset = '+%dc' % len(word)
        pos_start = self.text_area.search(word, '1.0', 'end')

        while pos_start:
            # la posizione finale fino a cui applicare il tag è quella definita dall'offset
            pos_end = pos_start + offset

            # aggiungo il tag
            self.text_area.tag_config("red_tag", foreground="red")
            self.text_area.tag_add("red_tag", pos_start, pos_end)

            # cerco le altre occorrenze
            pos_start = self.text_area.search(word, pos_end, "end")

    def set_bold(self, word):
        offset = '+%dc' % len(word)
        pos_start = self.text_area.search(word, '1.0', 'end')

        while pos_start:
            # la posizione finale fino a cui applicare il tag è quella definita dall'offset
            pos_end = pos_start + offset

            # aggiungo il tag
            self.text_area.tag_config("bold_tag", font = "TimesNewRoman 12 bold")
            self.text_area.tag_add("bold_tag", pos_start, pos_end)

            # cerco le altre occorrenze
            pos_start = self.text_area.search(word, pos_end, "end")

    def set_italic(self, word):
        offset = '+%dc' % len(word)
        pos_start = self.text_area.search(word, '1.0', 'end')

        while pos_start:
            # la posizione finale fino a cui applicare il tag è quella definita dall'offset
            pos_end = pos_start + offset

            # aggiungo il tag
            self.text_area.tag_config("italic_tag", font = "TimesNewRoman 12 italic")
            self.text_area.tag_add("italic_tag", pos_start, pos_end)

            # cerco le altre occorrenze
            pos_start = self.text_area.search(word, pos_end, "end")
    def run(self):
        if self.varC2 == 0:
            res = inner_function2(self.l1, self.l2, self.varC, self.type)
        else:
            res = inner_function2_second(self.l1, self.l2, first_word_start, second_word_start, all_sep_index,
                                         paragraphs, self.type)
        self.text_area.configure(state='normal')
        self.text_area.delete(1.0, "end")
        if not res == "":
            text = aggiusta_formattazione(res, 60)
            self.text_area.insert("end", text)
            self.text_area.configure(state='disabled')
        else:
            self.text_area.insert("end", "No correlation between these words.")
            self.text_area.configure(state='disabled')

        # aggiunta del colore rosso alle parole chiave
        self.set_bold("Domain of interest")
        self.set_italic("intended as noun")
        self.set_italic("intended as adjective")
        self.set_italic("intended as adverb")
        self.set_italic("intended as verb")
        self.set_italic("intended as\n noun")
        self.set_italic("intended as\n adjective")
        self.set_italic("intended as\n adverb")
        self.set_italic("intended as\n verb")
        word1 = "that is a particularization of"
        self.set_red(word1)
        word2 = "that generalizes"
        self.set_red(word2)
        word3 = "that is a member of"
        self.set_red(word3)
        word4 = "that is a part of"
        self.set_red(word4)
        word5 = "that is a component of"
        self.set_red(word5)
        word6 = "that is composed by"
        self.set_red(word6)
        word7 = "that has in part a"
        self.set_red(word7)
        word8 = "that has as a member a"
        self.set_red(word8)
        word9 = "that, as a verb, involves a"
        self.set_red(word9)
        word10 = "that causes"
        self.set_red(word10)
        word11 = "that has a correlation with"
        self.set_red(word11)
        word12 = "verb group"
        self.set_red(word12)
        word13 = "that has a similar meaning to"
        self.set_red(word13)
        word14 = "that is the opposite of"
        self.set_red(word14)
        word15 = "that is a lexical form derived from"
        self.set_red(word15)
        word16 = "to which the searched word refers: "
        self.set_red(word16)
        word17 = "that means"
        self.set_red(word17)


def aggiusta_formattazione(lines, limit):
    text = ''

    for line in lines:
        if line.__len__() >= limit:
            # assumo che divido almeno una volta
            new_lines = []
            total_len = line.__len__()
            partial_len = 0
            long_word_found = False
            while total_len - partial_len > limit + 1:
                l = line[partial_len:limit + partial_len + 1]
                # print("linea parziale: ", l)
                last_index_whitespace = l[::-1].find(" ")
                # print("indice spazio: ", last_index_whitespace)
                if last_index_whitespace == -1:
                    print("NON ESCE MAIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
                    next_whitespace = line[partial_len:].find(" ") + 1
                    # print("indice spazio successivo alla parola lunga: ", next_whitespace)
                    long_word = line[partial_len:partial_len + next_whitespace]
                    # print("parola lunga incontrata: ", long_word)
                    new_lines.append(long_word)
                    # print("vettore parziale: ", new_lines)
                    partial_len = partial_len + next_whitespace
                    # print("len parziale: ", partial_len)
                    long_word_found = True
                else:
                    if not long_word_found:
                        new_lines.append(
                            line[partial_len:limit + partial_len - last_index_whitespace + 1] + '\n')
                        # print("vettore parziale: ", new_lines)
                        partial_len = limit + partial_len - last_index_whitespace + 1
                        # print("len parziale: ", partial_len)
                    long_word_found = False
            new_lines.append(line[partial_len:])
            # print("vettore finale: ", new_lines)
            for new_line in new_lines:
                text = text + new_line
        else:
            if text != '' and text[len(text) - 1] != '\n':
                text = text + "\n" + line
            else:
                text = text + line

    return text


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def load(textBox, text2, text3, label1, label2, label3):
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    #print(filename)

    if filename != '':
        textBox.configure(state='normal')
        textBox.delete(1.0, "end")
        textBox.configure(state='disabled')
        text2.configure(state='normal')
        text2.delete(1.0, "end")
        text2.configure(state='disabled')
        text3.configure(state='normal')
        text3.delete(1.0, "end")
        text3.configure(state='disabled')

        label1.configure(text = '')
        label2.configure(text = '')
        label3.configure(text = '')

        i = 0
        try:
            while filename[i] != '.':
                i=i+1
            ext = filename[i+1:len(filename)]
        except IndexError as e:
            print(e)

        if ext == "pdf":
            pdfFileObj = open(filename, 'rb')
            pdfReader = PdfFileReader(pdfFileObj)
            pageReader = pdfReader.getPage(0)
            text = pageReader.extractText()
        elif ext == "txt":
            f = open(filename)
            lines = f.readlines()
            text = aggiusta_formattazione(lines, 90)
            text = elimina_doppi_accapi(text)

        textBox.configure(state='normal')
        textBox.insert("end", text)
        textBox.configure(state='disabled')

        #recupero i paragrafi dal testo
        global paragraphs
        paragraphs = text.split("\n\n")
        # ricerco gli indici degli accapo
        start_index = 1.0
        sep = "\n\n"
        global all_sep_index
        all_sep_index = []
        while 1:
            pos = textBox.search(sep, start_index, stopindex=tk.END)
            if not pos:
                break
            all_sep_index.append(pos)
            start_index = pos + "+1c"
        all_sep_index.insert(0,'1.0')
        all_sep_index.append(textBox.index(tk.END))


def elimina_doppi_accapi(text: str):
    prec = ''
    prec_prec = ''
    text_list = list(text)
    for i in range(0,len(text)):
        if prec_prec == '\n' and prec == '\n' and text_list[i] == '\n':
            text_list[i] = ''
            continue
        prec_prec = prec
        prec = text_list[i]
    text = "".join(text_list)
    return text


def function1(labelMeans, text1, textBox):
    #stringa selezionata
    try:
        string = text1.selection_get()

        if hasNumbers(string):
            textBox.configure(state='normal')
            textBox.delete(1.0, "end")
            textBox.insert("end", "The selected string is a number.")

        else:
            last_char = string[len(string)-1]

            if last_char == '.' or last_char == ',' or last_char == ':' or last_char == ';' or last_char == '?' or last_char == '!':
                string = string[0:len(string)-1]

            labelMeans.configure(text=string)
            labelMeans.update()
            textBox.configure(state='normal')
            textBox.delete(1.0, "end")
            textBox.configure(state='disabled')
            textBox.configure(state='normal')
            textBox.insert('end','Loading...')
            textBox.configure(state='disabled')
            textBox.update()
            #prelevo tutto il documento
            testo = text1.get("1.0",tk.END)
            #indici da cui partire per recuperare la frase in cui è presente la parola
            row_index = int(text1.index(tk.SEL_FIRST).split('.')[0])
            prev_index = int(text1.index(tk.SEL_FIRST).split('.')[1])
            succ_index = int(text1.index(tk.SEL_LAST).split('.')[1])


            riga_curr = text1.get(str(row_index)+".0", (str(row_index+1)) +".0")
            frase = ''
            flag_uscita = True
            #vado indietro fino al punto precedente o fino all'inizio del file (indice 0)
            cost = 0
            word_index = 0
            while flag_uscita and cost < row_index:
                for i in range(prev_index-1,-1,-1):
                    if(riga_curr[i]=='.' or riga_curr[i]=='?' or riga_curr[i]=='!'):
                        flag_uscita = False
                        break
                    word_index += 1
                    frase = riga_curr[i]+frase
                cost += 1
                riga_curr = text1.get(str(row_index-cost)+".0", (str(row_index+1-cost)) +".0")
                prev_index = len(riga_curr)

            #avendo trovato l'inizio della frase lo collego con la parola selezionata
            frase = frase+string

            #vado in avanti fino al prossimo punto o fino alla fine del file (indice max)
            riga_curr = text1.get(str(row_index) + ".0", (str(row_index + 1)) + ".0")
            cost = 0
            flag_uscita = True
            while flag_uscita:
                for i in range(succ_index-1,len(riga_curr),1):
                    if(riga_curr[i]=='.' or riga_curr[i]=='?' or riga_curr[i]=='!'):
                        flag_uscita = False
                        break
                    frase = frase+riga_curr[i]
                cost += 1
                riga_curr = text1.get(str(row_index + cost) + ".0", (str(row_index + 1 + cost)) + ".0")
                succ_index = 0

            #ho completato la frase
            print("\n---------------FRASE CONSIDERATA------------------------------\n" + frase + "\n---------------------------------------------\n")
            res = findDefinition(string, frase, word_index)
            textBox.configure(state='normal')
            textBox.delete(1.0, "end")
            textBox.configure(state='disabled')
            def_list = res[0]

            textBox.configure(state='normal')
            for k in range(0,len(def_list)):
                if res[1] == 0:
                    tmp = def_list[k]
                    def_list[k] = str(k+1) + ') ' + tmp + '\n\n'

            text = aggiusta_formattazione(def_list, 60)
            textBox.insert("end", text)
            textBox.configure(state='disabled')
    except Exception as exception:
        print(exception)


def function2(window,labelWN1, labelWN2, textB1):
    try:
        string = textB1.selection_get()
        last_char = string[len(string)-1]

        if last_char == '.' or last_char == ',' or last_char == ':' or last_char == ';' or last_char == '?' or last_char == '!' or last_char == '"' or last_char == '\'' or last_char == ']':
            string = string[0:len(string)-1]

        if labelWN1.cget("text") == '':

            global first_word_start
            first_word_start = textB1.index(tk.SEL_FIRST)
            #print('indice parola selezionata: ', first_word_start)  # (restituisce riga.indice)

            labelWN1.configure(text = string)

        elif labelWN2.cget("text") == '':

            global second_word_start
            second_word_start = textB1.index(tk.SEL_FIRST)
            #print('indice parola selezionata: ', second_word_start)

            labelWN2.configure(text = string)
        else:
            Dialog(window, label1 = labelWN1, label2 = labelWN2, string = string, text = textB1)
    except:
        print("Eccezione in selezione testo")


def startF2(frame, labelWN1, labelWN2, textB, varR, varC, varC2):
    l1 = labelWN1.cget("text")
    l2 = labelWN2.cget("text")

    if hasNumbers(l1) or hasNumbers(l2):
        textB.configure(state='normal')
        textB.delete(1.0, "end")
        textB.insert("end", "No relations found")
    else:
        if l1 != '' and l2 != '':
            textB.configure(state='normal')
            textB.delete(1.0, "end")
            textB.insert("end", "Loading...")
            textB.configure(state='disabled')
            frame.update()

            T = Thread_funct2(textB,l1,l2,varC.get(),varR.get(), varC2.get())
            T.start()


def clearF1(label, textB):
    label.configure(text='')
    textB.configure(state='normal')
    textB.delete(1.0, "end")
    textB.configure(state='disabled')


class Popup:
    def __init__(self, text):
        self.text = text
        self.functions_binding_key()
        self.functions_configurations()

    def functions_configurations(self):
        self.menu = tk.Menu(self.text.master, tearoff = 0, font = "TimesNewRoman 11")
        self.menu.add_command(label="Unambiguous Definition", command=self.text.storeobj['Function1'])
        self.menu.add_separator()
        self.menu.add_command(label="Find Relations", command=self.text.storeobj['Function2'])
        return

    def functions_binding_key(self):
        self.text.bind("<Button-3>", self.show_menu_)
        return

    def show_menu_(self, event):
        mouse = pyautogui.position()
        self.menu.tk_popup(mouse[0], mouse[1])
        return


class Dialog(Toplevel):

    def __init__(self, parent, title = "Wordnet Project", label1 = None, label2 = None, string = '', text = None):
        Toplevel.__init__(self, parent)
        self.transient(parent)  #is used to associate this window with a parent window
        self.title(title)
        self.parent = parent
        self.result = None
        self.text = text

        body = tk.Frame(self)
        self.initial_focus = self.body(body)
        self.resizable(False, False)
        self.update()
        parentHeight = int(ctypes.windll.user32.GetSystemMetrics(1))
        parentWidth = int(ctypes.windll.user32.GetSystemMetrics(0))
        myX = int(parentWidth/2 - self.winfo_width())
        myY = int(parentHeight/2 - self.winfo_height())
        self.geometry("+%d+%d" % (myX,myY))
        self.writeMessage()
        self.buttonbox(label1, label2, string)
        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.initial_focus.focus_set()
        self.wait_window(self)

    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden
        pass

    def buttonbox(self, labelWN1, labelWN2, string):
        # add standard button box. override if you don't want the
        # standard buttons
        box = Frame(self)
        w = tk.Button(box, text="First", width=10, command= lambda: self.first(labelWN1, string), default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(box, text="Second", width=10, command= lambda: self.second(labelWN2, string))
        w.pack(side=tk.LEFT, padx=5, pady=5)
        box.pack()

    def first(self, labelWN1, string):
        self.returnToWindow()
        labelWN1.configure(text = string)

        global first_word_start
        first_word_start = self.text.index(tk.SEL_FIRST)
        #print('indice parola selezionata: ', first_word_start)  # (restituisce riga.indice)

    def second(self, labelWN2, string):
        self.returnToWindow()
        labelWN2.configure(text = string)

        global second_word_start
        second_word_start = self.text.index(tk.SEL_FIRST)
        #print('indice parola selezionata: ', second_word_start)  # (restituisce riga.indice)

    def validate(self):
        return 1 # override

    def apply(self):
        pass # override

    def writeMessage(self):
        l = tk.Label(self)
        l.configure(text = "You have already selected two words. Which one do you want to replace?")
        l.pack()

    def returnToWindow(self):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()


def checkCtxAll(varC, varC2):
    check = varC2.get()
    if check == 1:
        varC2.set(1)
        varC.set(0)


def checkAllCtx(varC, varC2):
    all = varC.get()
    if all == 1:
        varC2.set(0)
        varC.set(1)


if __name__ == '__main__':
    window = tk.Tk()
    w = ctypes.windll.user32.GetSystemMetrics(0)
    h = ctypes.windll.user32.GetSystemMetrics(1)
    window.configure(width=w, height=h)
    window.resizable(False,False)
    window.configure(background="limegreen")
    window.title("Wordnet Project")
    window.geometry("+{}+{}".format(0, 0))
    window.state('zoomed')

    frame1 = BkgrFrame(window, 'sfondo_BD_frame1.png', width=int(w*3/5), height=int(h))
    frame1.configure(borderwidth=5, relief="sunken", bg="black")
    frame1.place(x=0,y=0)

    frame2 = BkgrFrame(window, 'sfondo_BD_frame2.png', width=int(w*2/5), height=int(1/4*h))
    frame2.configure(borderwidth=5,relief="sunken",bg="black")
    frame2.place(x=int(w*3/5), y=0)

    frame3 = BkgrFrame(window, 'sfondo_BD_frame3.png', width=int(w*2/5), height=int(3/4*h))
    frame3.configure(borderwidth = 5, relief = "sunken", bg = "black")
    frame3.place(x=int(w*3/5), y=int(1/4*h))

    b1 = tk.Button(frame1, text = "Load File", font="Gill 20 bold", background="navy", height = 1, foreground = "white")
    frame1.update()
    b1.place(x= int(frame1.winfo_width()/2 - 3/5*w*0.25*0.5), y = int(1/30*h), width = int(3/5*w*0.25))

    text1 = scrolledtext.ScrolledText(frame1, state='disabled')
    text1.configure(font = ("Calibri",14))
    frame1.update()
    b1.update()
    text1.place(x = int(frame1.winfo_width()/10), y = 2*b1.winfo_y()+b1.winfo_height(), width = int(frame1.winfo_width()*4/5), height = h-b1.winfo_height()-4*b1.winfo_y())

    frame2.update()
    labelMeans = tk.Label(frame2, height=1, bd=3,relief="groove")
    labelMeans.configure(font = ("TimesNewRoman",20),bg="white")
    labelMeans.place(x= int(frame2.winfo_width()/2-(2/5*w*0.25)), y = int(1/30*h), width=int(2/5*w*0.5))
    labelMeans.update()

    text2 = scrolledtext.ScrolledText(frame2, state='disabled')
    text2.configure(font=("TimesNewRoman", 12))
    frame2.update()
    text2.place(x = int(frame2.winfo_width()/10), y = 2*labelMeans.winfo_y()+labelMeans.winfo_height(), width=int(frame2.winfo_width()*4/5), height=frame2.winfo_height()-labelMeans.winfo_height()-3*labelMeans.winfo_y())
    text2.update()

    frame3.update()
    labelWN1 = tk.Label(frame3, height=1,bd=3,relief="groove", background = "white")
    labelWN1.configure(font = ("TimesNewRoman",17))
    labelWN1.place(x = int(frame3.winfo_width()/10), y = int(1/20*h), width = int(frame3.winfo_width()*0.3*4/5))

    labelWN1.update()
    frame3.update()
    labelWN2 = tk.Label(frame3, height=1,bd=3,relief="groove", background = "white")
    labelWN2.configure(font = ("TimesNewRoman",17))
    labelWN2.place(x = int(frame3.winfo_width() - frame3.winfo_width()/10-labelWN1.winfo_width()), y = int(1/20*h), width = int(frame3.winfo_width()*0.3*4/5))
    labelWN2.update()

    text3 = scrolledtext.ScrolledText(frame3, state='disabled')
    text3.configure(font=("TimesNewRoman", 12))
    frame3.update()
    text3.place(x = int(frame3.winfo_width()/10), y = labelWN1.winfo_y()+2*labelWN1.winfo_height(), width=int(frame3.winfo_width()*4/5), height=frame3.winfo_height()-labelWN1.winfo_height()-3*labelWN1.winfo_y())

    radioColor = "SlateGray2"
    text3.update()
    text2.update()
    labelWN1.update()
    varC = tk.IntVar()
    checkA = tk.Checkbutton(frame3, text="All", onvalue=1, offvalue=0, height=1, width=2, bg=radioColor, variable=varC,
                            font="Times 14 bold")
    checkA.place(x=int(labelWN1.winfo_x() + labelWN1.winfo_width() * 0.8),
                 y=labelWN1.winfo_y() + labelWN1.winfo_height() + 5)

    labelWN2.update()
    varC2 = tk.IntVar(value=1)
    checkC = tk.Checkbutton(frame3, text="Context", onvalue=1, offvalue=0, height=1, width=8, bg=radioColor,
                            variable=varC2, font="Times 14 bold")
    checkC.place(x=int(labelWN2.winfo_x()), y=labelWN2.winfo_y() + labelWN2.winfo_height() + 5)

    checkC.update()
    text1.update()
    text3.place(x=int(frame3.winfo_width() / 10), y=checkC.winfo_y() + checkC.winfo_height(),
                width=int(frame3.winfo_width() * 4 / 5), height=text1.winfo_height() - frame2.winfo_height() + 2)

    checkA.configure(command = lambda: checkAllCtx(varC, varC2))
    checkC.configure(command = lambda: checkCtxAll(varC, varC2))
    text3.update()
    varR = tk.IntVar(value=2)
    R1 = tk.Radiobutton(frame3, text="LOW", variable=varR, value=1, bg=radioColor, font="Times 10 bold")
    R1.place(x=int(1/4 * text3.winfo_width()), y=5)
    R2 = tk.Radiobutton(frame3, text="MEDIUM", variable=varR, value=2, bg=radioColor, font="Times 10 bold")
    R2.place(x=int(1/4 * text3.winfo_width() + 222), y=5)
    R3 = tk.Radiobutton(frame3, text="HIGH", variable=varR, value=3, bg=radioColor, font="Times 10 bold")
    R3.place(x=int(1/4 * text3.winfo_width() + 444), y=5)

    labelWN2.update()
    labelWN1.update()

    bGo = tk.Button(frame3, text="GO", height=2, width=10,
                    command=lambda: startF2(frame3, labelWN1, labelWN2, text3, varR, varC, varC2), background="navy", foreground = "white",
                    font="Gill 10 bold")
    bGo.place(x=int(frame3.winfo_width()/2 - 55),
              y=int(labelWN1.winfo_y())+labelWN1.winfo_height()/2 -25)

    labelMeans.update()
    text1.update()
    bGo.update()
    bC1 = tk.Button(frame2, text="CLEAR", height=2, width = 10, command=lambda: clearF1(labelMeans, text2), background="navy",
                    foreground = "white", font="Gill 10 bold")
    bC1.place(x=labelMeans.winfo_x() + labelMeans.winfo_width() + 30,
              y=int(labelMeans.winfo_y()+labelMeans.winfo_height()/2 -27))

    b1.configure(command = lambda: load(text1, text2, text3, labelMeans, labelWN1, labelWN2))

    text1.storeobj = {"Function1": lambda: function1(labelMeans, text1, text2),
                      "Function2": lambda: function2(window, labelWN1, labelWN2, text1)}
    popup = Popup(text1)

    window.mainloop()