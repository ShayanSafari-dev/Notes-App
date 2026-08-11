# Credits: https://www.youtube.com/watch?v=zHi__WfuQ0o
from customtkinter import*
from PIL import Image
from os import*
import  time

import ImportFont
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

def animation_show():
    # Check if it is new or not then show th btn

    #if type == 'New':
    #    addnote_bottom_frame.configure()
    global addnote_bottom_frame_x

    if addnote_bottom_frame_x >= 0.5:
        addnote_bottom_frame_x -= (addnote_bottom_frame_x/8)
        addnote_bottom_frame.place(x = addnote_bottom_frame_x, y = 75)
        window.after(10,animation_show)


def animation_hide():
    global addnote_bottom_frame_x

    if addnote_bottom_frame_x <= 500:
        addnote_bottom_frame_x += (addnote_bottom_frame_x*0.2)
        addnote_bottom_frame.place(x = addnote_bottom_frame_x, y = 75)
        window.after(10,animation_hide)
    

#========== App Functions ==========
def add_btn_cliked():
    print('Add button clicked')
    notes_textbox.delete('0.0', 'end')
    note_name_label.configure(text='Note 1')
    animation_show()

def open_note(note_id):
    print(f'Open {note_id}')
    note_name_label.configure(text=Note_Names[note_id])
    notes_textbox.delete('0.0', 'end')
    notes_textbox.insert('0.0', Notes[note_id])
    animation_show()

#========== Main - UI ==========
#--- Set up ---
bg = '#FEFEFE'
font_family = "Kaisei HarunoUmi" if ImportFont.FONT_AVAILABLE else "Arial"
black_color = '#1D1B20'
#--- Importing  ---
search_icon_import = Image.open('assets/search_icon.png')
search_icon_image = CTkImage(search_icon_import, size=(30, 30))

def mainUI():
    def top():
        global top_frame

        top_frame = CTkFrame(window, width = 500, height = 76, corner_radius= 0, 
                            bg_color=bg, fg_color=bg)
        top_frame.place(anchor = 'center', relx = 0.5, y=37)

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
        all_ui_frame = CTkFrame(window, width=500, height=625, fg_color=bg, corner_radius=0)
        all_ui_frame.place(x = 0, y = 75)

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
                notes_frame = CTkScrollableFrame(home_page_frame, width= 484, height = 430,
                                                 fg_color=bg, bg_color= bg,
                                                 border_width=0)
                notes_frame.place(anchor = 's', relx = 0.5, rely = 0.941)

                def notes_component():
                    notes_btn_fg_color = "#F7F7F7"
                    for i in range(0, len(Notes)):
                        text_btn_id = i
                        notes_btn = CTkButton(notes_frame, width= 460, height= 67,
                                            fg_color= notes_btn_fg_color, bg_color=bg, hover_color="#EDEDED",
                                            border_width= 2, corner_radius= 10, border_color= "#F1F1F1",
                                            text = Note_Names[text_btn_id], font=(font_family, 20, 'bold'), 
                                            text_color= black_color, anchor = 'w', command= lambda x = text_btn_id: open_note(x))
                        notes_btn.grid(row = i, padx = (16,0), pady = (8,0))

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
                global note_name_label
                top_note_frame = CTkFrame(addnote_bottom_frame, width= 450, height=70, 
                                            fg_color=bg, bg_color=bg, corner_radius=0)
                top_note_frame.place(x = 25, y = 0)

                note_name_label = CTkLabel(top_note_frame, width= 358, height=46,
                                        font=(font_family, 32), fg_color=bg, bg_color=bg,
                                        corner_radius=0, text_color='#222222', text='Note 1', anchor='w')
                note_name_label.place(x = 40, y = 9)

                back_btn = CTkButton(top_note_frame, width= 24, height= 24,
                                     fg_color=black_color, bg_color= bg, hover_color="#393939",
                                     text='<', text_color='#FEF7FF', font=('arial', 16, 'bold'),
                                     corner_radius=7, anchor= 's', command= lambda: animation_hide())
                back_btn.place(x = 6, y = 22)

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

window.mainloop()
