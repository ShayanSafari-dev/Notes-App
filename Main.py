# Credits: https://www.youtube.com/watch?v=zHi__WfuQ0o
from customtkinter import*
from os import*

from ImportAssets import* # This helps us to open the app after the assets are ready
from WeekCalendar import*
from Notes import*

window = CTk()

window.geometry('500x700+200+50')
window.title('Notes')
window.resizable(False, False)
window.configure(fg = '#FEFEFE')

try: # learned from Google -----------------------------------
    window.iconbitmap('assets/app_logo.ico')
    try:
        import ctypes
        note_app_id = 'Note.notesapp.main.1.0'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(note_app_id) # <= Google
    except:
        print('Failed to load the icon for the task bar.')
except:
    print('Failed to load app icon.')
#------------------------------------------------------------

#=========== Animation Functions=======================
addnote_bottom_frame_x = 500

zero_notes_label = None
zero_notes_label_y = 100

zero_results_label = None
zero_results_label_y = 100

note_open = False
delete_warning_y_n = None

change_name_entry = None
current_note_id = None

def animation_show():
    global addnote_bottom_frame_x, note_open

    #notes_textbox.focus()

    addnote_bottom_frame.lift()
    try:
        zero_notes_label.place(x=600, y=200)
    except:
        pass

    if addnote_bottom_frame_x >= 0.5:
        addnote_bottom_frame_x -= (addnote_bottom_frame_x/8)
        addnote_bottom_frame.place(x = addnote_bottom_frame_x, y = 75)
        window.after(10,animation_show)

def animation_hide(type): # This function also saves the note + animation 
    global addnote_bottom_frame_x, change_name_entry, current_note_id

    if change_name_entry is not None:
        change_name_entry.destroy()
        change_name_entry = None

    window.focus()

    if addnote_bottom_frame_x <= 500:
        addnote_bottom_frame_x += (addnote_bottom_frame_x*0.2)
        addnote_bottom_frame.place(x = addnote_bottom_frame_x, y = 75)
        window.after(10,lambda: animation_hide(type))
    elif type == 'back':
        try:
            #note_index = Note_Names.index(note_name_label.cget('text'))
            Notes[current_note_id] = notes_textbox.get('0.0','end')
        except:
            pass

#========== App Functions ==========
def clear_search_entry(e):
    pass

def search(key):
    global zero_notes_label, zero_results_label_y, zero_results_label
    s = search_entry.get().strip().lower()

    if s != '':
        rebuild_ui('search')
    else:
        rebuild_ui('delete')
        if zero_notes_label is not None:
            zero_notes_label.place_forget()

        if zero_results_label is not None:
            zero_results_label.place_forget()
            zero_results_label_y = 100

    if key.keysym == 'Return': # Learned "keysym" from Copilot
        notes_textbox.focus()

def cancel():
    global delete_warning_y_n
    delete_warning_frame.destroy()
    delete_warning_y_n = False

def confirm(delete_id):
    global delete_warning_y_n, zero_notes_label_y
    delete_warning_frame.destroy()
    delete_warning_y_n = True

    #search_entry.delete(0, 'end')

    if delete_id == 'n':
        delete_id = Note_Names.index(note_name_label.cget('text'))

    try: 
        Note_Buttons[delete_id].destroy()
        Note_Buttons.pop(delete_id)
        Note_Names.pop(delete_id)
        Notes.pop(delete_id)
    except:
        print('Error: Could not delete this note')

    zero_notes_label_y = 200
    rebuild_ui('delete')
    animation_hide('delete')

def delete_warning(delete_id):
    global delete_warning_frame

    window.focus()

    delete_warning_frame = CTkFrame(window, width= 250, height= 145,
                                   fg_color=bg, bg_color=bg,
                                   border_width=2, border_color= '#C4C4C4', 
                                   corner_radius= 10)
    delete_warning_frame.place(anchor = 'center', relx = 0.5, rely = 0.5)

    delete_warning_label = CTkLabel(delete_warning_frame, width= 120, height= 35,
                                   fg_color=bg, bg_color=bg,
                                   font=(font_family, 24, 'bold'), text='Delete',
                                   text_color='#1D1B20', anchor='center')
    delete_warning_label.place(x=65, y=12)

    sure_warning_label = CTkLabel(delete_warning_frame, width= 190, height= 35,
                                   fg_color=bg, bg_color=bg,
                                   font=(font_family, 18), text='Are you sure?',
                                   text_color='#1D1B20', anchor='center')
    sure_warning_label.place(x=30, y=50)

    cancel_btn = CTkButton(delete_warning_frame, width=95, height=25,
                           fg_color='#E8E8E8', bg_color=bg, hover_color="#DFDFDF",
                           corner_radius=5,
                           border_width=0, text='Cancel', font=(font_family,13),
                           text_color='#8F8F8F',
                           command= lambda: cancel())
    cancel_btn.place(x = 22, y = 98)

    confirm_btn = CTkButton(delete_warning_frame, width=95, height=25,
                           fg_color='#1D1B20', bg_color=bg, hover_color="#424242",
                           corner_radius=5,
                           border_width=0, text='Confirm', font=(font_family,13),
                           text_color="#E9E9E9",
                           command= lambda: confirm(delete_id))
    confirm_btn.place(x = 133, y = 98)

    nothing_to_show()
    
def nothing_to_show():
    global zero_notes_label_y , zero_notes_label

    nothing_to_show_text = 'Nothing to show\nAdd your first note below :)'

    if zero_notes_label is None:
        zero_notes_label = CTkLabel(window, width = 200, height= 44,
                                    fg_color= bg, bg_color=bg, font=(font_family, 15),
                                    text_color='#8E8E8E', anchor= 'center',
                                    text=nothing_to_show_text)

    if len(Note_Names) == 0:
        if zero_notes_label_y > 0.5:
            zero_notes_label_y -= zero_notes_label_y*0.1
            zero_notes_label.place(anchor = 'center', x = 250, y = zero_notes_label_y+350)
            window.after(10, lambda: nothing_to_show())
    
def nothing_to_show_search():
    global zero_results_label_y , zero_results_label

    nothing_to_show_text = 'No results found'

    if  zero_results_label_y != 0:
        if zero_results_label is None:
            zero_results_label = CTkLabel(window, width = 200, height= 44,
                                        fg_color= bg, bg_color=bg, font=(font_family, 15),
                                        text_color='#8E8E8E', anchor= 'center',
                                        text=nothing_to_show_text)

    # zero_results_label_y = 100
        
        if zero_results_label_y > 0.5:
            zero_results_label_y -= zero_results_label_y*0.1
            zero_results_label.place(anchor = 'center', x = 250, y = zero_results_label_y+350)
            window.after(10, lambda: nothing_to_show_search())

def add_btn_cliked():

    Notes.append('')
    Note_Names.append(f'Note {len(Note_Names)+1}')

    notes_textbox.delete('0.0', 'end')
    note_name_label.configure(text=Note_Names[-1])

    if zero_results_label is not None:
        zero_results_label.place_forget()

    animation_show()
    rebuild_ui('delete')

    Note_Buttons.append(notes_btn)

def open_note(note_id):
    global current_note_id
    current_note_id = note_id

    note_name_label.configure(text=Note_Names[note_id])
    notes_textbox.delete('0.0', 'end')
    notes_textbox.insert('0.0', Notes[note_id])
    
    animation_show()

def delete(d_id):
    global zero_notes_label_y, delete_warning_y_n

    delete_warning(d_id)

def rebuild_ui(type): 
    global zero_notes_label_y, zero_results_label, change_name_entry, zero_notes_label, zero_results_label_y

    if type == 'delete':
        if change_name_entry != None:
            change_name_entry.destroy()
            change_name_entry = None # Debuged with GPT

        if zero_results_label != None:
            zero_results_label.destroy()
            zero_results_label = None

        if zero_notes_label != None:
            zero_notes_label.destroy()
            zero_notes_label = None


        if len(Notes) == 0:
            nothing_to_show()

        if len(Notes) != 0:
            Note_Buttons.clear()

            for windget in notes_frame.winfo_children():
                windget.destroy()

            #Copy of notes_component function
            global notes_btn, notes_btn_fg_color
            notes_btn_fg_color = "#F7F7F7"
            for i in range(0, len(Notes)):
                text_btn_id = i

                notes_btn = CTkButton(notes_frame, width= 460, height= 67,
                                    fg_color= notes_btn_fg_color, bg_color=bg, hover_color="#EDEDED",
                                    border_width= 2, corner_radius= 10, border_color= "#F1F1F1",
                                    text = Note_Names[text_btn_id], font=(font_family, 20, 'bold'), 
                                    text_color= black_color, anchor = 'w', 
                                    command= lambda x = text_btn_id: open_note(x))
                notes_btn.grid(row = i, padx = (16,0), pady = (8,0))

                delete_btn = CTkButton(notes_btn, width=29, height=29,
                                    fg_color= notes_btn_fg_color, bg_color= '#EDEDED',
                                    hover_color= "#d7d7d7",
                                    border_width=0, corner_radius=4,
                                    text='', image=delete_light_icon_image, 
                                    command= lambda x = text_btn_id: delete(x))
                delete_btn.place(x = 423, y = 21)

                Note_Buttons.append(notes_btn)
    
    elif type == 'search':
        if change_name_entry != None:
            change_name_entry.destroy()
            change_name_entry = None

        if len(Notes) != 0:
            Note_Buttons.clear()

            for windget in notes_frame.winfo_children():
                windget.destroy()

            #Copy of notes_component function
            #global notes_btn, notes_btn_fg_color
            notes_btn_fg_color = "#F7F7F7"

            found_any = False

            for i in range(0, len(Notes)):
                text_btn_id = i
                if search_entry.get().lower().strip() in Note_Names[text_btn_id].lower().strip():
                    found_any = True
                    notes_btn = CTkButton(notes_frame, width= 460, height= 67,
                                        fg_color= notes_btn_fg_color, bg_color=bg, hover_color="#EDEDED",
                                        border_width= 2, corner_radius= 10, border_color= "#F1F1F1",
                                        text = Note_Names[text_btn_id], font=(font_family, 20, 'bold'), 
                                        text_color= black_color, anchor = 'w', 
                                        command= lambda x = text_btn_id: open_note(x))
                    notes_btn.grid(row = i, padx = (16,0), pady = (8,0))

                    delete_btn = CTkButton(notes_btn, width=29, height=29,
                                        fg_color= notes_btn_fg_color, bg_color= '#EDEDED',
                                        hover_color= "#d7d7d7",
                                        border_width=0, corner_radius=4,
                                        text='', image=delete_light_icon_image, 
                                        command= lambda x = text_btn_id: delete(x))
                    delete_btn.place(x = 423, y = 21)

                    Note_Buttons.append(notes_btn)
            if not found_any:
                #print('Nothing found')
                nothing_to_show_search()
            else: 
                if zero_results_label is not None:
                    zero_results_label_y = 100
                    zero_results_label.place_forget()

def change():
    global change_name_entry, current_note_id

    change_id = current_note_id

    if change_id is None:
        #print('Error: No note is open') --- Debug
        return

    search_entry.delete(0, 'end')

    #print(f"Chang {Note_Names[change_id]}")

    change_name_entry = CTkEntry(top_note_frame, width=353, height=42,
                                 border_width= 1.5, border_color= '#B9B9B9', corner_radius=5,
                                 fg_color= bg, bg_color= bg, placeholder_text= Note_Names[change_id],
                                 placeholder_text_color= black_color, font=(font_family,24))
    change_name_entry.place(x = 34, y = 14)

    def enter_pressed(idk): # The "idk" prevents the app from crashing :) *Explanation - Copilot: Tkinter always passes an event object to any function bound with .bind().*
        global change_name_entry
        new_name = change_name_entry.get()

        if new_name.strip() != '':
            Note_Names[change_id] = new_name
            note_name_label.configure(text = new_name)

            change_name_entry.destroy()
            change_name_entry = None

            search_entry.delete(0,'end')
            rebuild_ui('delete')

        #print(f"Changed to {Note_Names[change_id]}")  --- Debug

    change_name_entry.bind("<Return>", enter_pressed)

#========== Main - UI ==========

def mainUI():
    global Note_Buttons
    Note_Buttons = []

    def top():
        global top_frame

        top_frame = CTkFrame(window, width = 500, height = 76, corner_radius= 0, 
                            bg_color=bg, fg_color=bg)
        top_frame.place(anchor = 'w', relx = 0, y=37)

        app_name = CTkLabel(top_frame, text = 'Notes', font = (font_family, 32, 'bold'),
                            text_color = '#000000', bg_color=bg)
        app_name.place(x = 30, y = 15)

        switch_btn = CTkSwitch(top_frame, switch_width = 50, switch_height = 24, text='', 
                               bg_color = bg, fg_color = "#848484",
                               progress_color='#797979', button_color="#EBEBEB",
                               button_hover_color="#E0E0E0", corner_radius=7, 
                               button_length= 10)
        #switch_btn.place(x = 430, y = 28)

    def all_ui():
        all_ui_frame = CTkFrame(window, width=625, height=626, fg_color=bg, bg_color=bg, corner_radius=0)
        all_ui_frame.place(anchor = 'sw', relx = 0, y = 700)

        def add_button_ui():
            add_btn = CTkButton(all_ui_frame, width = 70, height = 70, 
                                 fg_color= black_color, bg_color=bg, hover_color="#37343E",
                                 text='+', font=('arial', 48), text_color = "#F3F3F3", 
                                 corner_radius=7, command = lambda: add_btn_cliked())
            add_btn.place(x = 411, y = 532)  

        def home_page():
            global home_page_frame
            home_page_frame = CTkFrame(all_ui_frame, width = 484, height= 674,
                                       fg_color= bg, bg_color=bg,
                                       corner_radius= 0, border_width=0) 
            home_page_frame.place(x = 8, y = 14)
        
            def search_ui():
                global search_entry
                search_bar_color = '#E8E8E8'

                search_frame = CTkFrame(home_page_frame, width= 460, height= 50,
                                        fg_color=search_bar_color, bg_color= bg,
                                        corner_radius=10)
                search_frame.place(anchor = 'n', relx = 0.5, y = 14)
                
                search_entry = CTkEntry(home_page_frame, width= 414, height= 40,
                                        fg_color= search_bar_color, bg_color=search_bar_color,
                                        placeholder_text='Search for notes', font=(font_family, 20),
                                        placeholder_text_color='#767676', corner_radius=0,
                                        border_width = 0)
                search_entry.place(anchor='n', relx = 0.54, y = 20)

                # I could put the image inside the search_frame, but using a label gives me more freedom :)
                search_icon_label = CTkLabel(search_frame, image=search_icon_image, 
                                             text='', width = 31, height = 31)
                search_icon_label.place(anchor = 'center', relx = 0.05, rely = 0.49)

            def week_calendar():
                week_calendar_frame = CTkFrame(home_page_frame, width = 460, height = 115,
                                                fg_color = bg, bg_color= bg,
                                                corner_radius = 0,
                                                border_width = 0)
                week_calendar_frame.place(anchor = 'n', relx = 0.5 , y = 71)

                def current_date_component():
                    current_date_frame_text_color = '#F9F9F9'

                    current_date_frame = CTkFrame(week_calendar_frame, width = 57, height = 111,
                                                  fg_color = black_color , bg_color = bg,
                                                  corner_radius = 10, border_width = 0)
                    current_date_frame.grid(row = 1, column = 0, padx = 0, pady = 2)

                    def inside_current():
                        inside_date_frame = CTkFrame(current_date_frame, width = 55, height = 88,
                                                    fg_color = black_color , bg_color = black_color,
                                                    corner_radius = 0, border_width = 0)
                        inside_date_frame.place(anchor = 'center', x = 28, y = 55)

                        #Date
                        current_date_label = CTkLabel(inside_date_frame, width = 50, height = 21,
                                                    font = (font_family, 13, 'bold'), 
                                                    text=dates[0], 
                                                    anchor='n',
                                                    text_color= current_date_frame_text_color, fg_color = black_color, bg_color = black_color)
                        current_date_label.place(anchor = 'n', relx = 0.49, rely = 0)

                        #Num
                        current_day_label = CTkLabel(inside_date_frame, width = 50, height = 51,
                                                    font = (font_family, 32, 'bold'), 
                                                    text=days[0], 
                                                    anchor='n',
                                                    text_color= current_date_frame_text_color, fg_color = black_color, bg_color = black_color)
                        current_day_label.place(anchor = 'center',  relx = 0.49, rely = 0.5)

                        #Month
                        current_month_label = CTkLabel(inside_date_frame, width = 50, height = 21,
                                                    font = (font_family, 13, 'bold'), 
                                                    text=months[0],
                                                    anchor='n',
                                                    text_color= current_date_frame_text_color, fg_color = black_color, bg_color = black_color)
                        current_month_label.place(anchor = 's', relx = 0.49, rely = 1)

                    inside_current()

                def next_dates_component():
                    next_date_frame_text_color = '#7F7F7F'
                    for i in range(1, 7):    
                        next_date_frame = CTkFrame(week_calendar_frame, width = 57, height = 111,
                                                    fg_color = bg , bg_color = bg,
                                                    corner_radius = 10, border_width = 2,
                                                    border_color = '#F3F3F3')

                        def inside_next():
                            inside_next_date_frame = CTkFrame(next_date_frame, width = 51, height = 88,
                                                    fg_color = bg , bg_color = bg,
                                                    corner_radius = 0, border_width = 0)
                            inside_next_date_frame.place(anchor = 'center', relx = 0.49, y = 55)

                            #Date
                            next_date_label = CTkLabel(inside_next_date_frame, width = 48, height = 21,
                                                        font = (font_family, 13, 'bold'), 
                                                        text=dates[i], 
                                                        anchor='n', 
                                                        text_color= next_date_frame_text_color, fg_color = bg, bg_color = bg)
                            next_date_label.place(anchor = 'n', relx = 0.5, rely = 0)

                            #Num
                            next_day_label = CTkLabel(inside_next_date_frame, width = 48, height = 51,
                                                        font = (font_family, 32, 'bold'), 
                                                        text=days[i], 
                                                        anchor='n',
                                                        text_color= next_date_frame_text_color, fg_color = bg, bg_color = bg)
                            next_day_label.place(anchor = 'center',  relx = 0.5, rely = 0.5)

                            #Month
                            next_month_label = CTkLabel(inside_next_date_frame, width = 48, height = 21,
                                                        font = (font_family, 13, 'bold'), 
                                                        text=months[i], 
                                                        anchor='n',
                                                        text_color= next_date_frame_text_color, fg_color = bg, bg_color = bg)
                            next_month_label.place(anchor = 's', relx = 0.5, rely = 1)

                        inside_next()
                    
                        next_date_frame.grid(row = 1, column = i + 1, padx =(10,0), pady = 2)    

                # Week Calendar ====================
                current_date_component()
                next_dates_component()

            def notes_frame_hp(): # hp: home page
                global notes_frame, zero_notes_label
                notes_frame = CTkScrollableFrame(home_page_frame, width= 484, height = 430,
                                                 fg_color=bg, bg_color= bg,
                                                 border_width=0)
                notes_frame.place(anchor = 's', relx = 0.5, rely = 0.941)

                
                def notes_component():
                        global notes_btn, notes_btn_fg_color
                        notes_btn_fg_color = "#F7F7F7"
                        for i in range(0, len(Notes)):
                            text_btn_id = i

                            notes_btn = CTkButton(notes_frame, width= 460, height= 67,
                                                fg_color= notes_btn_fg_color, bg_color=bg, hover_color="#EDEDED",
                                                border_width= 2, corner_radius= 10, border_color= "#F1F1F1",
                                                text = Note_Names[text_btn_id], font=(font_family, 20, 'bold'), 
                                                text_color= black_color, anchor = 'w', 
                                                command= lambda x = text_btn_id: open_note(x))
                            notes_btn.grid(row = i, padx = (16,0), pady = (8,0))

                            delete_btn = CTkButton(notes_btn, width=29, height=29,
                                                fg_color= notes_btn_fg_color, bg_color= '#EDEDED',
                                                hover_color= "#d7d7d7",
                                                border_width=0, corner_radius=4,
                                                text='', image=delete_light_icon_image, 
                                                command= lambda x = text_btn_id: delete(x))
                            delete_btn.place(x = 423, y = 21)

                            Note_Buttons.append(notes_btn)
                if len(Notes) == 0:
                    zero_notes_label = CTkLabel(window, width = 200, height= 44,
                                                fg_color= bg, bg_color=bg, font=(font_family, 15),
                                                text_color='#8E8E8E', anchor= 'center',
                                                text='Nothing to show\n Add your first note below 😊')
                    zero_notes_label.place(anchor = 'center',relx = 0.5, y = 350)

                # Notes Frame ==================
                notes_component()

            # Home Page Functions ** ============= 
            search_ui()
            week_calendar()
            notes_frame_hp()

        #Functions ================ All UI Frame
        
        home_page()
        add_button_ui()

    def addnote_UI():
        def addnote_UI_bottom():
            global addnote_bottom_frame
            addnote_bottom_frame = CTkFrame(window, width= 500, height=625, 
                                            fg_color=bg, bg_color=bg, corner_radius=0)
            addnote_bottom_frame.place( x = 0 + addnote_bottom_frame_x, y = 75)

            def top_note():
                global note_name_label, top_note_frame
                top_note_frame = CTkFrame(addnote_bottom_frame, width= 450, height=70, 
                                            fg_color=bg, bg_color=bg, corner_radius=0)
                top_note_frame.place(x = 25, y = 0)

                note_name_label = CTkLabel(top_note_frame, width= 358, height=46,
                                        font=(font_family, 24), fg_color=bg, bg_color=bg,
                                        corner_radius=0, text_color='#222222', text='Note 1', anchor='w')
                note_name_label.place(x = 40, y = 12)

                back_btn = CTkButton(top_note_frame, width= 24, height= 24,
                                     fg_color=black_color, bg_color= bg, hover_color="#393939",
                                     text='<', text_color='#FEF7FF', font=('arial', 16, 'bold'),
                                     corner_radius=7, anchor= 's', command= lambda: animation_hide('back'))
                back_btn.place(x = 6, y = 23)

                delete_btn_note = CTkButton(top_note_frame, width=26, height=27,
                                               fg_color= bg, bg_color = bg,
                                               hover_color= "#efefef",
                                               border_width=0, corner_radius=4,
                                               text='', image=delete_dark_icon_image, 
                                               command= lambda: delete('n'))
                delete_btn_note.place(x = 421, y = 23)

                edit_btn_note = CTkButton(top_note_frame, width=26, height=27,
                                               fg_color= bg, bg_color = bg,
                                               hover_color= "#efefef",
                                               border_width=0, corner_radius=4,
                                               text='', image= edit_dark_icon_image, 
                                               command= lambda: change())
                edit_btn_note.place(x = 393, y = 23)

            def textbox():
                global notes_textbox
                notes_textbox = CTkTextbox(addnote_bottom_frame, width= 450, height= 565,
                                        fg_color= '#FCFCFC', bg_color= bg, corner_radius=8,
                                        border_width= 1.5, border_color= '#B9B9B9',
                                        font=(font_family, 20), activate_scrollbars=False)
                notes_textbox.place(x = 25, y = 71)


            #--------------
            top_note()
            textbox()

        # Add note UI Functions =========
        addnote_UI_bottom()

    #Functions ================ App UI 
    top()
    all_ui()
    addnote_UI()
   
mainUI()
search_entry.bind('<KeyRelease>', search) # Debuged with GPT
search_entry.bind('<FocusIn>', clear_search_entry)

window.mainloop()
