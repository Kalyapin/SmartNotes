
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QListWidget, QTextEdit, \
    QLineEdit, QLabel, QMessageBox
import os
import json

notes = {'Приветствие':
             {'text': 'Привет',
              'tags': ['приветствие']},
         'Инструкция':
             {'text': 'Здесь будут сохранятся твои заметки',
              'tags': ['хранение']}
         }

FILENAME = 'notes.json'

app = QApplication([])
main_window = QWidget()
main_window.setFixedSize(600, 800)
main_window.setWindowTitle('Умные Заметки')
notes_textedit = QTextEdit()
notes_list_label = QLabel('Список заметок')
notes_list_widget = QListWidget()
create_note_button = QPushButton('Создать заметку')
write_note_name = QLineEdit()
write_note_name.setPlaceholderText('Введите название заметки...')
delete_note_button = QPushButton('Удалить заметку')
save_note_button = QPushButton('Сохранить заметку')
tags_list_label = QLabel('Список тегов')
tags_list_widget = QListWidget()
write_tag_name = QLineEdit()
write_tag_name.setPlaceholderText('Введите тег...')
add_tag_to_note = QPushButton('Добавить к заметке')
delete_note_tag = QPushButton('Открепить от заметки')
search_note_with_tag = QPushButton('Искать заметки по тегу')
clear_search_button = QPushButton('Сбросить поиск по тегу')

main_layout = QHBoxLayout()
right_layout = QVBoxLayout()
sub_layout1 = QHBoxLayout()
sub_layout2 = QHBoxLayout()
sub_layout3 = QHBoxLayout()
sub_layout4 = QHBoxLayout()
sub_layout5 = QHBoxLayout()
sub_layout6 = QHBoxLayout()
sub_layout7 = QHBoxLayout()
sub_layout8 = QHBoxLayout()
sub_layout9 = QHBoxLayout()

main_window.setLayout(main_layout)
main_layout.addWidget(notes_textedit)
main_layout.addLayout(right_layout)
right_layout.addLayout(sub_layout1)
right_layout.addLayout(sub_layout2)
right_layout.addLayout(sub_layout3)
right_layout.addLayout(sub_layout4)
right_layout.addLayout(sub_layout5)
right_layout.addLayout(sub_layout6)
right_layout.addLayout(sub_layout7)
right_layout.addLayout(sub_layout8)
right_layout.addLayout(sub_layout9)

sub_layout1.addWidget(notes_list_label)
sub_layout2.addWidget(notes_list_widget)
sub_layout3.addWidget(save_note_button)
sub_layout3.addWidget(delete_note_button)
sub_layout4.addWidget(create_note_button)
sub_layout4.addWidget(write_note_name)
sub_layout5.addWidget(tags_list_label)
sub_layout6.addWidget(tags_list_widget)
sub_layout7.addWidget(write_tag_name)
sub_layout8.addWidget(add_tag_to_note)
sub_layout8.addWidget(delete_note_tag)
sub_layout9.addWidget(search_note_with_tag)
sub_layout9.addWidget(clear_search_button)


def save_data():
    with open(FILENAME, 'w') as file:
        json.dump(notes, file)


if os.path.exists(FILENAME) and os.path.isfile(FILENAME):
    with open(FILENAME, 'r') as fp:
        notes = json.load(fp)
else:
    save_data()

notes_list_widget.addItems(notes)


def show_note():
    name = notes_list_widget.selectedItems()[0].text()
    notes_textedit.setText(notes[name]['text'])
    tags_list_widget.clear()
    tags_list_widget.addItems(notes[name]['tags'])


def save_note():
    if len(notes_list_widget.selectedItems()) == 0:
        popup = QMessageBox()
        popup.setWindowTitle('Ошибка!')
        popup.setText('Не выделена заметка')
        popup.exec()
        return
    name = notes_list_widget.selectedItems()[0].text()
    text = notes_textedit.toPlainText()
    notes[name]['text'] = text
    save_data()

def delete_note():
    if len(notes_list_widget.selectedItems()) == 0:
        popup = QMessageBox()
        popup.setWindowTitle('Ошибка!')
        popup.setText('Не выделена заметка')
        popup.exec()
        return
    name = notes_list_widget.selectedItems()[0].text()
    del notes[name]
    save_data()
    notes_list_widget.clear()
    tags_list_widget.clear()
    notes_list_widget.addItems(notes)

def create_note():
    name = write_note_name.text()
    temp = name.replace(' ', '')
    if name in notes:
        popup = QMessageBox()
        popup.setWindowTitle('Ошибка!')
        popup.setText('Заметка с таким названием уже существует')
        popup.exec()
        return

    if len(temp) == 0:
        popup = QMessageBox()
        popup.setWindowTitle('Ошибка!')
        popup.setText('Не написано имя заметки')
        popup.exec()
        return
    notes[name] = {'text' : '', 'tags' : []}
    save_data()
    notes_list_widget.clear()
    tags_list_widget.clear()
    notes_list_widget.addItems(notes)
    tags_list_widget.addItems(notes[name]['tags'])

def add_tag():
    if len(notes_list_widget.selectedItems()) == 0:
        popup = QMessageBox()
        popup.setWindowTitle('Ошибка!')
        popup.setText('Не выделена заметка')
        popup.exec()
        return
    name = notes_list_widget.selectedItems()[0].text()
    tag_name = write_tag_name.text()
    temp = tag_name.replace(' ', '')
    if len(temp) == 0:
        popup = QMessageBox()
        popup.setWindowTitle('Ошибка!')
        popup.setText('Не написано имя тега')
        popup.exec()
        return
    if tag_name in notes[name]['tags']:
        popup = QMessageBox()
        popup.setWindowTitle('Ошибка!')
        popup.setText('Тег с таким названием на этой заметке уже существует')
        popup.exec()
        return

    notes[name]['tags'].append(tag_name)
    save_data()
    tags_list_widget.clear()
    tags_list_widget.addItems(notes[name]['tags'])

def delete_tag():
    if len(tags_list_widget.selectedItems()) == 0:
        popup = QMessageBox()
        popup.setWindowTitle('Ошибка!')
        popup.setText('Не выделен тег')
        popup.exec()
        return
    name = notes_list_widget.selectedItems()[0].text()
    tag_name = tags_list_widget.selectedItems()[0].text()
    notes[name]['tags'].remove(tag_name)
    tags_list_widget.clear()
    tags_list_widget.addItems(notes[name]['tags'])
    save_data()

def search_note_with_tag_function():
    search_result = []
    tag_name = write_tag_name.text()
    for note_name in notes:
        if tag_name in notes[note_name]['tags']:
            search_result.append(note_name)
    notes_list_widget.clear()
    notes_list_widget.addItems(search_result)
    tags_list_widget.clear()

def clear_search():
    notes_list_widget.clear()
    notes_list_widget.addItems(notes)


notes_list_widget.itemClicked.connect(show_note)
save_note_button.clicked.connect(save_note)
delete_note_button.clicked.connect(delete_note)
create_note_button.clicked.connect(create_note)
add_tag_to_note.clicked.connect(add_tag)
delete_note_tag.clicked.connect(delete_tag)
search_note_with_tag.clicked.connect(search_note_with_tag_function)
clear_search_button.clicked.connect(clear_search)

main_window.show()
app.exec()
