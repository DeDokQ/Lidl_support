def get_instruction(language):
    # My git: "https://github.com/DeDokQ"
    # (c) DeDok
    eng = (
        '<p>After launching the application, <span style="color:red;">make sure</span> that you have finished working with the main program '
        'and it has created the necessary files. Fill in the field labeled <span style="color:red;">"T-Card ID"</span> with the number you '
        'entered in the main program. Then click the <span style="color:red;">"Start"</span> button. After the countdown, check the logs to '
        'see what was output. <span style="color:red;">If there is no error message</span>, congratulations, everything worked out for you! '
        '<BR> '
        '<BR> '
        'To create folders, first click the "Settings" button. A menu with fields to fill out will open. '
        '<span style="color:red;">Open the Excel document</span> where the information about the points you need to service is listed. '
        'Enter the necessary information into the cells. Remember that the <span style="color:red;">"Work range"</span> is filled in by '
        'the rows of the table, for example, if your team is yellow and the information about the stores you service is listed from row '
        '2 to row 95. You enter FROM 2 TO 95.</p>')

    rus = (
        '<p>Запустив приложение, <span style="color:red;">убедитесь</span>, что Вы закончили работать с основной программой и она создала '
        'необходимые файлы. Заполните поле с надписью <span style="color:red;">«Айди Т-карты»</span> номером, который Вы вписывали в основную '
        'программу. Далее нажмите на кнопку <span style="color:red;">«Начать»</span>. После обратного отчёта, посмотрите, что вывелось вам в '
        'логи. <span style="color:red;">Если сообщения об ошибке нету</span>, то поздравляю, у Вас всё получилось!'
        '<BR>'
        '<BR>'
        'Чтобы создать папки, для начала нажмите кнопку «Настройки». Вам откроется меню с полями для заполнения. '
        '<span style="color:red;">Откройте Exel документ</span>, в котором расписана информация про точки, которые Вы должны обслужить. Введите '
        'необходимую информацию в ячейки. Помните, что <span style="color:red;">«Диапазон работы»</span> заполняется по строчкам таблицы, '
        'например, Ваша команда жёлтая и информация о магазинах, которые Вы обслуживаете, расписана со 2 по '
        '95 строку. Вы вписывается ОТ 2 До 95.</p>')
    return eng if language == 'en' else rus
