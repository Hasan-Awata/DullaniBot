from Classes import *

while True:
    try:
        # Bot commands
        @DullaniBot.message_handler(commands=['start', 'help', 'announce', 'secretannounce', 'GetID', 'reload'])
        def Main_Commands(message):
            Manager = DataManager(MainDataBase)

            if message.chat.type in ["group", "supergroup"]:

                if message.text.lower().startswith("/start"):
                    if Manager.Update_Chat_Data(message):
                        DullaniBot.reply_to(message, "تم تفعيل البوت وحفظ معلومات المجموعة")
                    else:
                        DullaniBot.reply_to(message, "تم تحديث معلومات المجموعة")


                elif message.text.lower().startswith("/help"):
                    DullaniBot.reply_to(message, "Available commands:\n/start\n/help\n/announce\n/secretannounce\n/GetID\n/reload")
                
                elif message.text == "/announce@DullaniAllaAlTa3a_bot":
                    if message.chat.id == -1002101171385:
                        DullaniBot.send_message(message.chat.id, "أرسل الرسالة التي تريد تعميمها (للإلغاء أرسل: إلغاء)")
                        DullaniBot.register_next_step_handler(message, Brodcast.Announce)

        # Bot message handler
        @DullaniBot.message_handler(func=lambda message: True)
        def handle_message(message):

            if message.chat.type in ["group", "supergroup"]:
                if "ختمة جديدة" in message.text or "بدء ختمة" in message.text :
                    MessageToPin = DullaniBot.send_message(message.chat.id, BotFeatures.Create_New_Khetma(message, str(message.chat.id)), reply_markup=KhetmaKyboardMarkup)
                    DullaniBot.pin_chat_message(message.chat.id, MessageToPin.message_id)

                if "تم" in message.text.split() or "تمت" in message.text.split():
                    if "أجزائي" in message.text.split() or "اجزائي" in message.text.split():
                        Result = BotFeatures.Finish_All_User_Ajzaa(message, str(message.chat.id), str(message.from_user.id))
                        if Result[0] == "":
                            DullaniBot.reply_to(message, "ليس لديك أي أجزاء مأخوذة مُسبقاً")
                        elif Result[0] != "":
                            DullaniBot.reply_to(message, Result[0])
                        if Result[1] != "":
                            DullaniBot.send_message(message.chat.id, f"{Result[1]}\n دعاء الختم:\n {KhetmaDuaa}")
                    else:
                        Result = BotFeatures.Finish_Ajzaa(message, None, DetictNumbersInText(message.text))

                        if Result == False:
                            DullaniBot.reply_to(message, "يُرجى الرد على رسالة الختمة المقصودة")
                        else:
                            DullaniBot.reply_to(message, Result[0])
                        if Result[1] != "":
                            DullaniBot.send_message(message.chat.id, f"{Result[1]}\n دعاء الختم:\n {KhetmaDuaa}")

                if "سحب" in message.text.split():
                    UserID = str(message.from_user.id)
                    ChatID = str(message.chat.id)

                    if GroupManger.Check_If_Admin(UserID, ChatID):
                        AjzaaToPull = DetictNumbersInText(message.text)

                        if AjzaaToPull != []:
                            Result = BotFeatures.Pull_Juzaa(message, None, AjzaaToPull)
                            if not Result:
                                DullaniBot.reply_to(message, "الرجاء الرد على رسالة الختمة المطلوب السحب منها")
                            else:
                                DullaniBot.reply_to(message, Result)                
                        else:
                            DullaniBot.reply_to(message, "الرجاء تحديد أرقام الأجزاء التي تريد سحبها, والمحاولة مرة أُخرى")

                if "جزائي" in message.text and "تم" not in message.text:
                    Result = BotFeatures.Find_All_User_Ajzaa(str(message.chat.id), str(message.from_user.id))
                    if Result == "":
                        DullaniBot.reply_to(message, "ليس لديك أي أجزاء مأخوذة مُسبقاً")
                    else:
                        DullaniBot.reply_to(message, Result)

                if "في" in message.text and "جزاء" in message.text:
                    Result = BotFeatures.Find_Not_Taken_Ajzaa(str(message.chat.id))
                    if Result == "":
                        DullaniBot.reply_to(message, "لا يُوجد أجزاء مُتاحة حالياً")
                    else:
                        DullaniBot.send_message(message.chat.id, Result, "MarkdownV2")

        # Bot Kyboard clicks
        @DullaniBot.callback_query_handler(func=lambda call : True)
        def Clicks(call):
            if "j" in call.data:
                Result = BotFeatures.Take_Juzaa(call)
                match Result:
                    case "Already Finished":
                        DullaniBot.send_message(call.message.chat.id, f"عذراً @{call.from_user.username} إن الجزء الذي تطلبهُ منتهٍ بالفعل, جرب اختيار جزءٍ آخر")
                    case "Already Occupied":
                        DullaniBot.send_message(call.message.chat.id, f"عذراً @{call.from_user.username} إن الجزء الذي تطلبهُ مأخوذٌ بالفعل, جرب اختيار جزءٍ آخر")
                    case "Already Taken":
                        DullaniBot.send_message(call.message.chat.id, f"عذراً @{call.from_user.username} لقد أخذت هذا الجزء بالفعل")
                    
        # Start polling
        if __name__ == "__main__":
            print("Bot is running...")
            DullaniBot.infinity_polling()
        time.sleep(60)  # Keep the script alive for 1 minute
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(10)  # Wait before restarting

