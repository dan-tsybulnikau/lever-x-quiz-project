from tkinter import *
from tkinter import messagebox
import re

answer_number = 1
frames = []
# Variable to check Entry() for first-time appearance (without it .get() will return empty string after 'OK' button
first_input = True
user_question = ''
user_answers = []
user_correct_answers = []

question_list = [
    {
        "number": 1,
        "question": "Что из перечисленного не является языком программирования?",
        "answers": [
            "HTML",
            "DevOps",
            "Java",
            "Python"],
        "correct_answers": [1, 2]
    },
    {
        "number": 2,
        "question": "Какие из перечисленных видов тестирования могут быть автоматизированы?",
        "answers": [
            "UI тестирование",
            "Юзабилити тестирование",
            "Тестирование совместимости",
            "Unit тестирование"],
        "correct_answers": [1, 3, 4]
    },
    {
        "number": 3,
        "question": "Выберите вариант, который соответствует следующему предложению: "
                    "'Известно, что грымзик обязательно или полосат, или рогат, или и то и другое вместе'",
        "answers": [
            "Грымзик не может быть безрогим",
            "Грымзик не может быть однотонным и безрогим одновременно",
            "Грымзик не может быть полосатым и безрогим одновременно",
            "Грымзик не может быть однотонным и рогатым одновременно"
        ],
        "correct_answers": [2]
    },
    {
        "number": 4,
        "question": "Выберите типы алгоритмов, которых не существует",
        "answers": [
            "Алгоритмы с ветвлением",
            "Циклический безусловный",
            "Циклический с параметром",
            "Алгоритмы с углублением"],
        "correct_answers": [2, 4]
    },
    {
        "number": 5,
        "question": "Какая (какие) из следующих конструкций используется (используются) для ветвления?",
        "answers": [
            "switch case",
            "if else",
            "do while",
            "for"],
        "correct_answers": [1, 2]
    },


]
system_msg = {
    'CC1': 'Вы не ввели текст вопроса. Попробуйте добавить вопрос заново.',
    'CC3': "Вы не ввели правильные варианты ответа. Попробуйте добавить вопрос заново.",
    'CC4': "Все вопросы должны иметь хотя бы один выбранный вариант ответа. Проверьте правильность заполнения",
    'CC6': "Поле может содержать только уникальные цифры 1, 2, 3, 4, разделенные запятой. "
           "Попробуйте добавить вопрос заново",
}


def start_test():
    """Starts test with all questions from question_list"""
    # Setting up UI, griding items ans setting up scrollbar
    add_button.config(state='disabled')
    start_button.config(state='disabled')
    check_button.grid(column=2, row=0)
    canvas_frame = Frame(frame, width=600, height=400)
    canvas_frame.grid(row=1, column=0, pady=(5, 0), sticky='nw', columnspan=3)
    canvas_frame.grid_rowconfigure(0, weight=1)
    canvas_frame.grid_columnconfigure(0, weight=1)
    canvas_frame.grid_propagate(False)
    canvas = Canvas(canvas_frame, width=600, height=400)
    canvas.grid(row=0, column=0, sticky="news")
    my_scrollbar = Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    my_scrollbar.grid(row=0, column=1, sticky='ns')
    canvas.configure(yscrollcommand=my_scrollbar.set)
    row_count = 0
    question_frame = Frame(canvas)
    canvas.create_window((0, 0), window=question_frame, anchor='nw')

    for question in question_list:
        question_label = Label(
            question_frame,
            text=f'{question["number"]}. {question["question"]}',
            wraplength=600,
            justify=LEFT)
        question_label.grid(column=0, row=row_count, sticky=W)
        row_count += 1
        for answer in question['answers']:
            # Creating variable IntVar() for each answer and checkbox status
            question[answer] = IntVar()
            answer = Checkbutton(question_frame, text=answer, variable=question[answer])
            answer.grid(column=0, row=row_count, sticky=W)
            row_count += 1

    question_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))


def check_results():
    """Checks answers(checkboxes) user has chosen for each question, compares with answer[list] and
    increments correct_answer_number if they match"""
    incorrect_questions = []
    correct_answers_number = 0
    unsolved_questions = 0
    # Creating a list 'correct_answer' for each question, containing user-chosen position of checkboxes (from 1 to 4)
    for question in question_list:
        correct_answers = []
        i = 1
        # Checking status of each checkbox, multiplying it by 'i' if it has status 'checked' (by using method get())
        # and adding resulting number to correct_answers list
        for answer in question['answers']:
            if question[answer].get():
                correct_answers.append(question[answer].get() * i)
            i += 1
        # Checking in no checkboxes were chosen:
        if not len(correct_answers):
            unsolved_questions += 1
        # For each resulting correct_answer checking if it is equal to answers list,
        # incrementing global 'correct_answers_number' if they match
        elif correct_answers == question['correct_answers']:
            correct_answers_number += 1
        else:
            # Making a list of unsolved questions
            incorrect_questions.append(f'{question["number"]}. {question["question"]}')
    # If unsolved_questions has any items show warning
    if unsolved_questions:
        messagebox.showwarning(title='Внимание', message=system_msg['CC4'])
    # if all answers were correct
    elif correct_answers_number == len(question_list):
        messagebox.showinfo(title='Результат',
                            message=f"Ваш результат {correct_answers_number} из {len(question_list)}. Вы молодец!")
    # If some questions are incorrect, creating 'msg' with this questions
    else:
        msg = ""
        for _ in incorrect_questions:
            msg += f'{_}\n'
        messagebox.showinfo(title='Результат',
                            message=f"Вы неправильно ответили на вопросы:\n{msg}\n\n"
                                    f"Ваш результата {correct_answers_number} из {len(question_list)}.")


def add_question():
    """Allows user to add own question, possible answers and correct answers, adding it to the test questions"""
    global user_question, user_answers, user_correct_answers
    # Resetting user variables each time user enters question
    user_question = ''
    user_answers = []
    user_correct_answers = []

    def clear_entry():
        # Setting behavior for 'Cancel' button in each condition (question, answers, correct answers)
        global first_input
        if len(user_question) == 0:
            messagebox.showwarning(title='Внимание', message=system_msg['CC1'])
        elif len(user_answers) < 4:
            messagebox.showwarning(title='Внимание', message=f'Вы не ввели текст {len(user_answers)+1} варианта'
                                                             f' ответа. Попробуйте добавить вопрос заново.')
        elif len(user_correct_answers) == 0:
            messagebox.showwarning(title='Внимание', message=system_msg['CC3'])
        msg_label.destroy()
        question_entry.destroy()
        ok_button.destroy()
        cancel_button.destroy()
        first_input = True
        start_button.config(state='active')
        add_button.config(state='active')

    def push_question():
        """Formatting user's question according to question_list style, and appending it to question_list"""
        user_question_number = len(question_list)+1
        question_list.append({
            "number": user_question_number,
            "question": user_question,
            "answers": user_answers,
            "correct_answers": user_correct_answers
        })

    def enter_correct_answers():
        global user_correct_answers
        global first_input

        msg_label.config(text='Введите номера правильных ответов через запятую, без пробелов.'
                              ' \nНумерация начинается с 1')
        # Patterns for regular expressions, to check if user's input is correct and to pull numbers from it
        input_pattern = r'^[1-4](,[1-4])*$'
        correct_answers_numbers_pattern = r'[1-4]'
        correct_answers = question_entry.get()
        correct_answers_numbers = re.findall(correct_answers_numbers_pattern, correct_answers)
        # Checking if user input corresponds to pattern, also checking if it represents 4 numbers divided by 3 commas
        # (<=7), or more numbers without some commas(<=4)
        if re.match(input_pattern, correct_answers) and len(correct_answers_numbers) <= 4 and len(correct_answers) <= 7:
            # Counting number of appearance for each number
            for number in correct_answers_numbers:
                if correct_answers_numbers.count(number) == 1:
                    user_correct_answers.append(int(number))
                else:
                    messagebox.showwarning(title='Внимание', message=system_msg['CC6'])
                    user_correct_answers = ['False']
                    clear_entry()
                    return
            push_question()
            clear_entry()
        # Checking first-time appearance of Entry
        elif first_input and not correct_answers:
            first_input = False
        # Error for empty Entry
        elif not correct_answers and not first_input:
            clear_entry()
        # Solution for non-fitting pattern of string
        else:
            messagebox.showwarning(title='Внимание', message=system_msg['CC6'])
            user_correct_answers = ['False']
            clear_entry()

    def enter_answer():
        """Allows user to enter 4 answers for question"""
        global first_input, user_answers
        # Setting a loop to collect 4
        if len(user_answers) <= 3:
            msg_label.config(text=f"Введите текст {len(user_answers) + 1} варианта ответа")
            answer = question_entry.get()
            if answer:
                user_answers.append(answer)
                question_entry.delete(0, last=END)
                first_input = True
                enter_answer()
            # Checking first-time appearance of Entry
            elif first_input and not answer:
                first_input = False
            # Error for empty Entry
            elif not answer and not first_input:
                clear_entry()
        else:
            first_input = True
            ok_button.config(command=enter_correct_answers)
            question_entry.delete(0, last=END)
            enter_correct_answers()

    def enter_question():
        """Allows user to input own question"""
        global user_question
        user_question = question_entry.get()
        if not user_question:
            clear_entry()
        else:
            ok_button.config(command=enter_answer)
            question_entry.delete(0, last=END)
            enter_answer()
    # Setting up UI
    start_button.config(state='disabled')
    add_button.config(state='disabled')
    msg_label = Label(frame, text="Введите текст вопроса:")
    msg_label.grid(column=0, row=2, columnspan=2)
    question_entry = Entry(frame, width=70)
    question_entry.grid(column=0, row=3, padx=30, columnspan=2, sticky='w')
    ok_button = Button(frame, text="OK", width=25, command=enter_question)
    ok_button.grid(column=2, row=3, padx=10)
    cancel_button = Button(frame, text='Cancel', width=25, command=clear_entry)
    cancel_button.grid(column=3, row=3, padx=10)


# Setting up starting screen UI
window = Tk()
window.title('Test')
window.config(
    padx=20,
    pady=20,
    )
window.resizable(width=False, height=False)
window.grid_rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)

frame = Frame(window, width=600, height=400)
frame.grid()

add_button = Button(
    frame,
    text='Добавить вопрос',
    highlightthickness=1,
    command=add_question,
    width=25)
start_button = Button(
    frame,
    text='Начать тест',
    highlightthickness=1,
    command=start_test,
    width=25)
check_button = Button(
    frame,
    text='Проверить результат',
    highlightthickness=1,
    command=check_results,
    width=25)

add_button.grid(column=0, row=0, padx=10)
start_button.grid(column=1, row=0, padx=10)

window.mainloop()
