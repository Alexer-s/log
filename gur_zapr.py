import tkinter as tk
from typing import Union
from tkinter import messagebox
from tkinter import ttk
from main_klass import DatabaseError, OutQueryDb


FIELDS_MIN_ADD: dict[str, Union[ttk.Entry, ttk.Combobox]] = {}
gur_query = OutQueryDb('db.sqlite')

names_fields = [
    ('Порядковый номер', 'id'),
    ('Дата регистрации', 'date_reg'),
    ('Номер запроса:', 'num_query'),
    ('Дата запроса:', 'date_query'),
    ('Адресат - ТО СФР:', 'to_sfr'),
    ('СНИЛС:', 'snils'),
    ('Ф.И.О.:', 'fio'),
    ('Наименование орг-ции, рег.№:', 'name_org'),
    ('Период работы:', 'work_period'),
    ('Срок исполнения:', 'due_date'),
    ('Вид запроса:', 'type_query'),
    ('Дата поступления ответа:', 'date_answer'),
    ('Специалист', 'spec')
]


def write_query(
        add_win: tk.Toplevel, update: bool, id: Union[int, None] = None
):
    params = tuple(val.get() for val in FIELDS_MIN_ADD.values())
    try:
        if update:
            res = gur_query.insert_to_db(
                gur_query.update_query, params + (id,)
            )
        else:
            res = gur_query.insert_to_db(
                gur_query.insert_query, params
            )
    except DatabaseError:
        messagebox.showerror(
            'Ошибка', 'Что-то пошло не так, попробуйте еще раз!'
        )
        return
    if res:
        fields = gur_query.read_db(
            gur_query.read_query_fo_id, (res if not update else id,)
        )
        confirm_win = tk.Toplevel()
        confirm_win.title('Подтверждение')
        confirm_frame = ttk.Frame(
            confirm_win, borderwidth=1, relief=tk.SOLID, padding=(3, 3)
        )
        confirm_frame.pack()
        res_text = ttk.Label(
            confirm_frame,
            text='Вы добавили запрос №:'
            if not update
            else 'Вы обновили запрос №:',
            width=30
        )
        res_text.grid(column=0, row=0, padx=2, pady=3, sticky='w')
        num = ttk.Label(confirm_frame, text=fields[0][0], width=30)
        num.grid(column=1, row=0, padx=2, pady=3, sticky='w')
        for num_row, text, val in zip(
            range(1, len(fields[0])), names_fields[1:], fields[0][1:]
        ):
            label = ttk.Label(confirm_frame, text=text[0], width=30)
            label.grid(column=0, row=num_row, padx=2, pady=3, sticky='w')
            value = ttk.Label(confirm_frame, text=val, width=30)
            value.grid(column=1, row=num_row, padx=2, pady=3, sticky='w')
        add_win.destroy()


# сделать валидацию полей (даты, снилса и специалиста)


def win_add_view_query(update=False, update_fields=None):
    add_win = tk.Toplevel()
    add_win.title('Добавление запроса')
    add_win.geometry('420x410')
    input_frame = ttk.Frame(
        add_win, borderwidth=1, relief=tk.SOLID, padding=(3, 3)
    )
    input_frame.pack(side='left', padx=10, pady=5, anchor='center')
    num_label = ttk.Label(input_frame, text=names_fields[0][0], width=30)
    num_label.grid(column=0, row=0, padx=2, pady=3, sticky='w')
    num_field = ttk.Entry(input_frame, width=30, state='readonly')
    num_field.grid(column=1, row=0, padx=2, pady=3, sticky='w')
    date_reg_label = ttk.Label(input_frame, text=names_fields[1][0], width=30)
    date_reg_label.grid(column=0, row=1, padx=2, pady=3, sticky='w')
    date_reg_var = tk.StringVar()
    date_reg = ttk.Entry(
        input_frame, width=30, state='readonly', textvariable=date_reg_var
    )
    FIELDS_MIN_ADD[names_fields[1][1]] = date_reg
    date_reg.grid(column=1, row=1, padx=2, pady=3, sticky='w')
    for line, name_field in zip(
        range(2, len(names_fields)), names_fields[2:-1]
    ):
        label = ttk.Label(input_frame, text=name_field[0], width=30)
        label.grid(column=0, row=line, padx=2, pady=3, sticky='w')
        field = ttk.Entry(input_frame, width=30)
        FIELDS_MIN_ADD[name_field[1]] = field
        field.grid(column=1, row=line, padx=2, pady=3, sticky='w')
    users = gur_query.users_list()
    print(users)
    spec_field_label = ttk.Label(
        input_frame, text=names_fields[-1][0], width=30
    )
    spec_field_label.grid(
        column=0, row=len(names_fields), padx=2, pady=2, sticky='w'
    )
    spec_field = ttk.Combobox(input_frame, width=30, values=users)
    FIELDS_MIN_ADD[names_fields[-1][1]] = spec_field
    spec_field.grid(
        column=1, row=len(names_fields), padx=2, pady=3, sticky='w'
    )
    if update:
        num_field.insert(0, update_fields[0])
        for field, val in zip(FIELDS_MIN_ADD.values(), update_fields[1:-1]):
            field.insert(0, val)
        spec_field.set(update_fields[-1])
    add_btn = ttk.Button(
        input_frame,
        text='Добавить'
        if not update
        else 'Обновить',
        command=lambda: write_query(
            add_win, update, id=None if not update else update_fields[0])
        )
    add_btn.grid(
        column=1,
        row=len(names_fields) + 1,
        sticky='e',
        ipadx=3,
        ipady=3,
        padx=3,
        pady=3
    )


def create_delete_user(del_usr=False):
    add_del_user_win = tk.Toplevel()
    add_del_user_win.title('Ввод имени')
    add_del_user_win.geometry('250x78')
    add_user_label = ttk.Label(
        add_del_user_win, text='Введите имя пользователя:'
    )
    add_user_label.pack()
    add_user_field = ttk.Entry(add_del_user_win, width=30)
    add_user_field.pack()

    def add_user():
        res = gur_query.insert_to_db(
            gur_query.create_user,
            (add_user_field.get(),)
        )
        add_del_user_win.destroy()
        if res:
            messagebox.showinfo('Сообщение', 'Пользователь успешно добавлен.')

    def del_user():
        res = gur_query.insert_to_db(
            gur_query.delete_user,
            (add_user_field.get(),)
        )
        add_del_user_win.destroy()
        if res:
            messagebox.showinfo('Сообщение', 'Пользователь успешно удален.')
        else:
            messagebox.showinfo('Сообщение', 'Нет такого пользователя!')

    add_user_btn = ttk.Button(
        add_del_user_win,
        text='Добавить' if not del_usr else 'Удалить',
        command=add_user if not del_usr else del_user
    )
    add_user_btn.pack()


def on_close_qur_win():
    gur_query.close_db()
    gur_win.destroy()


def find_query(snils):
    queries = gur_query.read_db(gur_query.read_query, (snils,))
    if queries:
        if len(queries) == 1:
            win_add_view_query(update=True, update_fields=queries[0])
        # обработать случай с несколькими найденными запросами
    # обработать случай когда не найдены запросы


gur_win = tk.Tk()
gur_win.title('Журнал исходящих запросов')
gur_win.geometry('400x300')
gur_win.protocol('WM_DELETE_WINDOW', on_close_qur_win)

main_menu = tk.Menu()
user_menu = tk.Menu(tearoff=0)
user_menu.add_command(label='Добавить', command=create_delete_user)
user_menu.add_command(
    label='Удалить',
    command=lambda: create_delete_user(del_usr=True)
)
main_menu.add_cascade(label='Пользователи', menu=user_menu)

btn_add = ttk.Button(
    gur_win, text='Зарегистрировать', command=win_add_view_query
)
btn_add.pack(anchor='nw', padx=15, pady=(25, 5))
find_frame = ttk.Frame(gur_win)
find_frame.pack(anchor='nw', padx=15)
find_snils = ttk.Entry(find_frame, width=17)
find_snils.pack(side='left')
find_btn = ttk.Button(
    find_frame,
    text='Найти',
    command=lambda: find_query(find_snils.get())
)
find_btn.pack(side='left', padx=10)

gur_win.config(menu=main_menu)
gur_win.mainloop()


# для вывода нескольких запросов в табличном виде используй ttk.Treeview
# потом чтобы вывести отдельный запрос - привязать к объекту Treeview обработчик <Double-1>
  # который запустит функцию просмотра запроса и передаст в него поля записи из БД.