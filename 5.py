# -*- coding: utf-8 -*-

import telebot

TOKEN = '5411659197:AAGQMv3zrpOXZpgtUC7h3Z3KJEjdsUJA2yU'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    try:
        chat_id = message.chat.id

        if '+++' in message.text:
            command_parts = message.text.split('+++')
            line_number_to_replace = int(command_parts[1].strip())

            with open('textfile.txt', 'r') as file:
                lines = file.readlines()

            if 1 <= line_number_to_replace <= len(lines):
                new_text = ' '.join(command_parts[2:])
                lines[line_number_to_replace - 1] = new_text + '\n'

                with open('textfile.txt', 'w') as file:
                    file.writelines(lines)

                bot.send_message(chat_id, f'Text in line {line_number_to_replace} replaced with: {new_text}')
            else:
                bot.send_message(chat_id, 'Invalid line number for replacement.')
        elif '++' in message.text:
            line_to_add = message.text.split('++')[1].strip()

            with open('textfile.txt', 'a') as file:
                current_lines_count = file.write(line_to_add + '\n')

            bot.send_message(chat_id, f'{current_lines_count} successfully added.')
        elif '-' in message.text:
            line_number_to_delete = int(message.text.split('-')[1].strip())

            with open('textfile.txt', 'r') as file:
                lines = file.readlines()

            if 1 <= line_number_to_delete <= len(lines):
                deleted_line = lines.pop(line_number_to_delete - 1)

                with open('textfile.txt', 'w') as file:
                    file.writelines(lines)

                bot.send_message(chat_id, f'{line_number_to_delete}: {deleted_line.strip()} deleted.')
            else:
                bot.send_message(chat_id, 'Invalid line number for deletion.')
        elif '-+' in message.text:
            keyword_to_replace = message.text.split('-+')[1].split(' ', 1)[0].strip()
            new_line = message.text.split(' ', 1)[1].strip()

            with open('textfile.txt', 'r') as file:
                lines = file.readlines()

            replaced = False
            for i, line in enumerate(lines):
                if keyword_to_replace.lower() in line.lower():
                    lines[i] = new_line + '\n'
                    replaced = True
                    break

            if replaced:
                with open('textfile.txt', 'w') as file:
                    file.writelines(lines)

                bot.send_message(chat_id, f'Keyword "{keyword_to_replace}" replaced with "{new_line}".')
            else:
                bot.send_message(chat_id, f'Keyword "{keyword_to_replace}" not found.')
        elif '==' in message.text:
            with open('textfile.txt', 'rb') as file:
                bot.send_document(chat_id, file)
        elif '=' in message.text:
            line_number = int(message.text.split('=')[1].strip())



            with open('textfile.txt', 'r') as file:
                lines = file.readlines()




            if 1 <= line_number <= len(lines):
                text_in_line = lines[line_number - 1].strip()
                bot.send_message(chat_id, f'Text in line {line_number}: {text_in_line}')

            else:
                bot.send_message(chat_id, 'Invalid line number.')


        else:
            keywords = message.text.strip().split(' ')

            found_lines = []
            with open('textfile.txt', 'r') as file:
                for i, line in enumerate(file, 1):
                    if all(keyword.lower() in line.lower() for keyword in keywords):
                        found_lines.append(f'{i}: {line.strip()}')

            if found_lines:
                response = '\n'.join(found_lines)
                bot.send_message(chat_id, response)
            else:
                bot.send_message(chat_id, f'No lines found containing both words: {", ".join(keywords)}.')

    except Exception as e:
        bot.send_message(chat_id, f'An error occurred: {str(e)}')

@bot.message_handler(content_types=['document'])
def handle_document(message):
    try:
        chat_id = message.chat.id

        if message.document.file_name == 'textfile.txt':
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            with open('textfile.txt', 'wb') as new_file:
                new_file.write(downloaded_file)

            bot.send_message(chat_id, 'File textfile.txt replaced successfully.')
        else:
            bot.send_message(chat_id, 'Invalid file. Please send a file named textfile.txt.')

    except Exception as e:
        bot.send_message(chat_id, f'An error occurred: {str(e)}')

bot.polling()
