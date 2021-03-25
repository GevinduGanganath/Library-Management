# import modules
from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector
from datetime import date

def connect_db():
    global conn
    global c
    # connecting to mysql db
    conn = mysql.connector.connect(user = 'root', password = 'gevindu1', host = 'localhost', database = 'lms')
    c = conn.cursor()
    return

def add_books():
    'add books to store'
    # configuration
    add = Toplevel()
    add.title('Add new books')
    add.iconbitmap('icon.ico')
    add.maxsize(400, 170)
    add.minsize(400, 170)
    add.geometry('+550+200')
    # entry frame
    frame = Frame(add)
    frame.pack(side = 'right', anchor = 'n')
    # labels and entries
    l_name = Label(add, text = 'Name')
    l_author = Label(add, text='Author')
    l_translator = Label(add, text='Translator')
    l_date = Label(add, text='Date of purchase')
    l_price = Label(add, text='Price')
    e_name = Entry(frame, width = 47)
    e_author = Entry(frame, width=47)
    e_translator = Entry(frame, width=47)
    e_date = Entry(frame, width=12)
    e_price = Entry(frame, width=8)
    e_date.insert(0, date)
    # placing widgets
    l_name.pack(side = 'top', anchor = 'w', padx = 1, pady = 2)
    l_author.pack(side='top', anchor='w', padx=1, pady=2)
    l_translator.pack(side='top', anchor='w', padx=1, pady=2)
    l_date.pack(side='top', anchor='w', padx=1, pady=2)
    l_price.pack(side='top', anchor='w', padx=1, pady=2)
    e_name.pack(side='top', anchor='w', padx=1, pady=3)
    e_author.pack(side='top', anchor='w', padx=1, pady=3)
    e_translator.pack(side='top', anchor='w', padx=1, pady=3)
    e_date.pack(side='top', anchor='w', padx=1, pady=3)
    e_price.pack(side='top', anchor='w', padx=1, pady=3)

    def f_add():
        'button save'
        try:
            # update db
            c.execute('insert into books (name, author, translator, date, price) value (%s, %s, %s, %s, %s)', (e_name.get(),
                                                                                                               e_author.get(),
                                                                                                               e_translator.get(),
                                                                                                               e_date.get(),
                                                                                                               e_price.get()))
            conn.commit()
        except:
            messagebox.showerror('Error', 'Can not complete action')
            add.destroy()
        else:
            # message box
            c.execute('select * from books order by index_no desc limit 1')
            book = c.fetchone()
            temp_str = '{} is successfully added to store under index number {}'.format(book[1], book[0])
            messagebox.showinfo('Saved',temp_str)
            add.destroy()
            return
    # save button
    b_add = Button(frame, text = 'Save', command = f_add)
    b_add.pack(side='right', anchor='e', padx=10, ipadx = 20)

    return

def search_books():
    # create window
    search = Toplevel()
    search.title('Add, edit and delete books')
    search.iconbitmap('icon.ico')
    search.maxsize(500, 400)
    search.minsize(500, 400)
    search.geometry('+490+200')

    def f_search():
        'search through DB and add to table'
        global selected
        for book in table.get_children():
            table.delete(book)

        c.execute('select name, index_no from books')
        db_name_list = c.fetchall()
        names = [name.upper() for name in e_name_search.get().split() ]
        indexes = []

        for search_name in names:
            for book in db_name_list:
                if search_name in [book_name.upper() for book_name in book[0].split()]:
                    indexes.append(book[1])

        if len(indexes) == 0:
            table.insert('', 'end', values = ('', 'No results found', ''))
            return
        elif len(indexes) == 1: command = 'select * from books where index_no = ' + str(indexes[0])
        else: command = 'select * from books where index_no in '+str(tuple(indexes))
        c.execute(command)
        selected = c.fetchall()

        for book in selected:
            table.insert('', 'end', values = (book[0], book[1], book[-1]))
        return

    def one_click(event):
        'put selected details on the entries'
        global index
        e_name.delete(0, END)
        e_author.delete(0, END)
        e_translator.delete(0, END)
        e_date.delete(0, END)
        e_price.delete(0, END)
        index = table.item(table.selection(), 'values')[0]
        c.execute('select * from books where index_no = '+str(index))
        book = c.fetchall()[0]
        e_name.insert(0, book[1])
        e_author.insert(0, book[2])
        e_translator.insert(0, book[3])
        e_date.insert(0, book[4])
        e_price.insert(0, book[5])
        return

    def f_delete():
        'deleting'
        command = 'delete from books where index_no = '+str(index)
        c.execute(command)
        conn.commit()
        e_name.delete(0, END)
        e_author.delete(0, END)
        e_translator.delete(0, END)
        e_date.delete(0, END)
        e_price.delete(0, END)
        f_search()
        return

    def f_update():
        'editing'
        command = '''update books set
                        name = "%s",
                        author = '%s',
                        translator = '%s',
                        date = '%s',
                        price = '%s'
                        where index_no = %s''' % (e_name.get(),
                                                  e_author.get(),
                                                  e_translator.get(),
                                                  e_date.get(),
                                                  e_price.get(),
                                                  index)

        c.execute(command)
        conn.commit()
        e_name.delete(0, END)
        e_author.delete(0, END)
        e_translator.delete(0, END)
        e_date.delete(0, END)
        e_price.delete(0, END)
        f_search()
        return

    # widgets
    l_name_search = Label(search, text = 'Name of book')
    e_name_search = Entry(search, width = 55)
    b_search = Button(search, text = 'search', command = f_search)
    table = ttk.Treeview(search, columns = (1, 2, 3), show = 'headings', height = 7)
    table.heading(1, text = 'Index number')
    table.heading(2, text='Name')
    table.heading(3, text='Availability')
    table.column(1, width = 90)
    table.column(2, width=320)
    table.column(3, width = 70)
    table.bind('<<TreeviewSelect>>', one_click)
    frame_1 = Frame(search)
    frame_2 = Frame(search)
    l_name = Label(frame_1, text = 'Name')
    l_author = Label(frame_1, text='Author')
    l_translator = Label(frame_1, text='Translator')
    l_data = Label(frame_1, text='Date of purchase')
    l_price = Label(frame_1, text='Price')
    e_name = Entry(frame_2, width = 63)
    e_author = Entry(frame_2, width=63)
    e_translator = Entry(frame_2, width=63)
    e_date = Entry(frame_2, width=30)
    e_price = Entry(frame_2, width=25)
    b_updata = Button(frame_2, text = 'Update', command = f_update)
    b_delete = Button(frame_2, text = 'Delete', command = f_delete)
    l_reports = Label(frame_1, text = '')
    # placing
    l_name_search.grid(row = 0, column = 0)
    e_name_search.grid(row = 0, column = 1, pady = 5, padx= 5)
    b_search.grid(row = 0, column = 2, pady = 5, padx = 10)
    table.grid(row = 1, columnspan = 5, pady = 10, padx = 10)
    frame_1.grid(row = 2, column = 0)
    l_name.pack(side = 'top', anchor = 'w', padx = 1, pady = 3)
    l_author.pack(side = 'top', anchor = 'w', padx = 1, pady = 3)
    l_translator.pack(side = 'top', anchor = 'w', padx = 1, pady = 3)
    l_data.pack(side = 'top', anchor = 'w', padx = 1, pady = 3)
    l_price.pack(side = 'top', anchor = 'w', padx = 1, pady = 3)
    frame_2.grid(row = 2, column = 1, columnspan = 2)
    e_name.pack(side='top', anchor='w', padx=1, pady=4)
    e_author.pack(side='top', anchor='w', padx=1, pady=4)
    e_translator.pack(side='top', anchor='w', padx=1, pady=4)
    e_date.pack(side='top', anchor='w', padx=1, pady=4)
    e_price.pack(side='top', anchor='w', padx=1, pady=2)
    b_delete.pack(side='right', anchor='e', padx=10, ipadx = 20)
    b_updata.pack(side='right', anchor='e', padx=10, ipadx = 20)
    l_reports.pack(side='left', anchor='w', padx=10)
    return

def f_all_report():
    'export report of all books'
    location = r'C:\Users\User\Documents\LMS Reports\All books.csv'
    file = open(location, 'w')
    file.write('no, index number, name, author, translator, date of purchase, price, availability')
    c.execute('select * from books')
    books = c.fetchall()
    for num, book in enumerate(books, start = 1):
        file.write('\n{}, {}, {}, {}, {}, {}, {}, {}'.format(num, book[0], book[1], book[2], book[3], book[4], book[5], book[6]))
    file.close()
    return

def f_lend_report():
    location = r'C:\Users\User\Documents\LMS Reports\Lent books.csv'
    file = open(location, 'w')
    file.write('no, index number, name of book, name of lender, contact number, date of lent')
    c.execute('select lends.*, books.name from lends, books where lends.index_no = books.index_no')
    books = c.fetchall()

    for num,book in enumerate(books, start = 1):
        file.write('\n{}, {}, {}, {}, {}, {}'.format(num, book[0], book[-1], book[1], book[2], book[3]))
    file.close()

    return

def lend_books():
    # create window
    lend = Toplevel()
    lend.title('Lend and receive books')
    lend.iconbitmap('icon.ico')
    lend.maxsize(400, 170)
    lend.minsize(400, 170)
    lend.geometry('+550+200')

    def f_search():
        if e_index.get().isdigit():
            c.execute('select * from books where index_no = '+str(e_index.get()))
            book = c.fetchone()

        else:
            return

        if book == None:
            pass

        elif book[-1] == 'no':
            def f_receive():
                c.execute('delete from lends where index_no = '+str(e_index.get()))
                c.execute('update books set availability = "yes" where index_no = '+str(e_index.get()))
                conn.commit()
                messagebox.showinfo('info', book[1]+' received')
                lend.destroy()
                return

            c.execute("select * from lends where index_no = "+str(e_index.get()))
            lender = c.fetchone()
            frame_1 = Frame(lend)
            l_name = Label(frame_1, text='Book name')
            l_lender = Label(frame_1, text='Lender')
            l_contact = Label(frame_1, text='Contact number')
            l_date = Label(frame_1, text='Date of lend')
            frame_2 = Frame(lend)
            l_book_name = Label(frame_2, text=book[1])
            l_book_lender = Label(frame_2, text = lender[1])
            l_book_contact = Label(frame_2, text = lender[2])
            l_book_date = Label(frame_2, text = lender[3])
            b_lend = Button(lend, text='Receive', command=f_receive)
            frame_1.grid(row=1, column=0)
            frame_2.grid(row=1, column=1, columnspan=2)
            l_name.pack(side='top', anchor='w', padx=1, pady=2)
            l_lender.pack(side='top', anchor='w', padx=1, pady=2)
            l_contact.pack(side='top', anchor='w', padx=1, pady=2)
            l_date.pack(side='top', anchor='w', padx=1, pady=2)
            l_book_name.pack(side='top', anchor='w', padx=1, pady=2)
            l_book_lender.pack(side='top', anchor='w', padx=1, pady=2)
            l_book_contact.pack(side='top', anchor='w', padx=1, pady=2)
            l_book_date.pack(side='top', anchor='w', padx=1, pady=2)
            b_lend.grid(row=2, column=3, ipadx=5)

        else:
            def f_lend():
                c.execute('update books set availability = "no" where index_no = ' + str(e_index.get()))
                c.execute('insert into lends value (%s, %s, %s, %s)', (e_index.get(),
                                                                       e_lender.get(),
                                                                       e_contact.get(),
                                                                       e_date.get()))
                conn.commit()
                messagebox.showinfo('Info', book[1]+' lent')
                lend.destroy()

                return

            frame_1 = Frame(lend)
            l_name = Label(frame_1, text = 'Book name')
            l_lender = Label(frame_1, text = 'Lender')
            l_contact = Label(frame_1, text = 'Contact number')
            l_date = Label(frame_1, text = 'Date of lend')
            frame_2 = Frame(lend)
            l_book_name = Label(frame_2, text = book[1])
            e_lender = Entry(frame_2, width = 35)
            e_contact = Entry(frame_2, width = 15)
            e_date = Entry(frame_2, width = 15)
            b_lend = Button(lend, text = 'Lend', command = f_lend)
            e_date.insert(0, date)
            frame_1.grid(row = 1, column = 0)
            frame_2.grid(row = 1, column = 1, columnspan = 2)
            l_name.pack(side = 'top', anchor = 'w', padx = 1, pady = 2)
            l_lender.pack(side = 'top', anchor = 'w', padx = 1, pady = 2)
            l_contact.pack(side = 'top', anchor = 'w', padx = 1, pady = 2)
            l_date.pack(side = 'top', anchor = 'w', padx = 1, pady = 2)
            l_book_name.pack(side = 'top', anchor = 'w', padx = 1, pady = 2)
            e_lender.pack(side = 'top', anchor = 'w', padx = 1, pady = 2)
            e_contact.pack(side = 'top', anchor = 'w', padx = 1, pady = 2)
            e_date.pack(side = 'top', anchor = 'w', padx = 1, pady = 2)
            b_lend.grid(row = 2, column = 3, ipadx = 5)
            return

    # widgets
    l_index = Label(lend, text = 'Index number  ')
    e_index = Entry(lend, width = 15)
    b_search = Button(lend, text = 'Search', command = f_search)

    # placing
    l_index.grid(row = 0, column = 0, pady = 5, padx = 5)
    e_index.grid(row = 0, column = 1, padx = 15, pady = 5)
    b_search.grid(row = 0, column = 3, padx = 10, pady = 5)

    return

def book_reports():
    reports = Toplevel()
    reports.title('Create reports')
    reports.iconbitmap('icon.ico')
    reports.maxsize(300, 135)
    reports.minsize(300, 135)
    reports.geometry('+600+300')

    def create():
        all = FALSE
        lend = FALSE
        if all_book.get() == 1:
            f_all_report()
            all = TRUE
        if lend_book.get() == 1:
            f_lend_report()
            lend = TRUE
        if all and lend:
            messagebox.showinfo('Info', 'Reports created')
            reports.destroy()
        elif all or lend:
            messagebox.showinfo('Info', 'Report created')
            reports.destroy()
        else:
            messagebox.showinfo('Info', 'Select reports')

    all_book = IntVar()
    lend_book = IntVar()

    l_detail = Label(reports, text = 'Select reports here')
    frame = Frame(reports)
    frame_1 = Frame(reports, width=300)
    b_all = Checkbutton(frame, text = 'All books', variable = all_book)
    b_lend = Checkbutton(frame, text='Lend books', variable=lend_book)
    b_create = Button(frame_1, text = 'Create Reports', command = create)
    l = Label(frame_1, text = '                                   ')

    l_detail.grid(row = 0, padx = 10, pady = 5)
    frame.grid(row = 1, padx = 10, pady = 10)
    b_all.pack(side = 'top', anchor = 'w')
    b_lend.pack(side = 'top', anchor = 'w')
    frame_1.grid(row = 2, columnspan = 2)
    l.grid(row = 0, column = 0)
    b_create.grid(row = 0, column = 1)
    return

def create_root():
    'root window'
    # configuration
    root = Tk()
    root.title("LMS")
    root.maxsize(550, 520)
    root.minsize(550, 520)
    root.geometry("+470+150")
    root.configure(background="#1a110a")
    root.iconbitmap('icon.ico')
    # background image
    background_image = PhotoImage(file="background.png")
    background = Label(root, image=background_image, bd=0)
    background.grid(row = 0, column = 0, columnspan = 4)
    # button images
    i_add = PhotoImage(file = 'add.png')
    i_search = PhotoImage(file = 'search.png')
    i_lend = PhotoImage(file = 'lend and retrive.png')
    i_reports = PhotoImage(file = 'reports.png')
    # buttons
    b_add = Button(root, image = i_add, command = add_books)
    b_search = Button(root, image = i_search, command = search_books)
    b_lend = Button(root, image = i_lend, command = lend_books)
    b_reports = Button(root, image = i_reports, command = book_reports)
    # buttons names
    l_add = Label(root, text = 'Add', fg = 'white', bg = "#1a110a")
    l_search = Label(root, text='Search', fg='white', bg = "#1a110a")
    l_lend = Label(root, text='Lend and\nreceive', fg='white', bg = "#1a110a")
    l_reports = Label(root, text = 'Reports', fg = 'white', bg = "#1a110a")
    # positioning
    b_add.grid(row = 1, column = 0)
    b_search.grid(row = 1, column = 1)
    b_lend.grid(row=1, column=2)
    b_reports.grid(row = 1, column = 3)
    l_add.grid(row = 2, column = 0)
    l_search.grid(row=2, column=1)
    l_lend.grid(row=2, column=2)
    l_reports.grid(row = 2, column = 3)

    root.mainloop()
    return

def main():
    'execution function'
    global date
    date = date.today()
    connect_db()
    create_root()

    return


if __name__ == '__main__':
    main()

