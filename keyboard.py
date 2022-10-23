from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

#Menu
button_add_homework = KeyboardButton("✅Додати завдання")
button_show_homework = KeyboardButton("📜Показати завдання")
button_delete_homework = KeyboardButton("❌Видалити завдання")
manu = ReplyKeyboardMarkup(resize_keyboard=True).add(button_add_homework, button_show_homework,button_delete_homework)

#test menu
Cartography = KeyboardButton("Картографія ")
Land = KeyboardButton("Основи землеустрою")
Chemistry = KeyboardButton("Хімія")
English = KeyboardButton("Англійська Мова")
Biologi_Water = KeyboardButton("Біологічна оцінка якості води")
Organizetion_teretory = KeyboardButton("Планування та організація територій")
Turizm = KeyboardButton("Основи туристичної діяльності")
exit = KeyboardButton("🔙Вихід")

sub_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(Cartography,Land,Chemistry,English,Biologi_Water,
                                                         Organizetion_teretory,Turizm,exit)
