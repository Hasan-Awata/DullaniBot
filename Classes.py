from telebot import TeleBot, types
import json
from decouple import config
from DataBase import *

# Initialize the bot
BOT_TOKEN = config("BOT_TOKEN")
DullaniBot = TeleBot(BOT_TOKEN)

class DataManager:
    def __init__(self, FileName):
        self.FileName = FileName

    def Load_Data(self):
        try:
            with open(self.FileName, "r") as JsonFile:
                return json.load(JsonFile)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            self.Save_Data({"Chats": {}})  # Reset to default if file was not found
            return {"Chats": {}}

    def Save_Data(self, Data):
        with open(self.FileName, "w") as JsonFile:
            json.dump(Data, JsonFile, indent=2)

    def Update_Chat_Data(self, message):
        ChatID = str(message.chat.id)
        ChatName = message.chat.first_name
        ChatType = message.chat.type
        ChatMembersNumber = DullaniBot.get_chat_members_count(ChatID)
        ChatAdmins = GroupManger.Get_Chat_Admins(ChatID)

        Data = self.Load_Data()
        if ChatID in Data["Chats"]:
            Data["Chats"][ChatID]["Chat Name"] = ChatName
            Data["Chats"][ChatID]["Chat Type"] = ChatType
            Data["Chats"][ChatID]["Chat Members Number"] = ChatMembersNumber
            Data["Chats"][ChatID]["Chat Admins"] = ChatAdmins
            self.Save_Data(Data)
            return False
        else:
            Data["Chats"][ChatID] = {
                "Chat Name" : ChatName,
                "Chat Type" : ChatType,
                "Chat Members Number" : ChatMembersNumber,
                "Chat Admins" : ChatAdmins,
                "One Juzaa Mode" : False,
                "Number Of Khetmat" : 0,
                "Khetmat In Progress" : {},
            }
            self.Save_Data(Data)
            return True
    
    def Reload_Chats(self):
        Data = self.Load_Data()
        
        for ChatID in Data["Chats"]:
            if not GroupManger.Bot_Is_Member(ChatID):
                del Data["Chats"][ChatID]
        
        self.Save_Data(Data)

    def Save_Khetma(self, ChatID, Number, Intent, ID):
        Data = self.Load_Data()

        if ChatID not in Data["Chats"]:
            return False
        else:
            Data["Chats"][ChatID]["Number Of Khetmat"] += 1
            Data["Chats"][ChatID]["Khetmat In Progress"][Number] = {}
            Data["Chats"][ChatID]["Khetmat In Progress"][Number]["Khetma Message ID"] = ID
            Data["Chats"][ChatID]["Khetmat In Progress"][Number]["Khetma Intent"] = Intent

            for Juzaa in range(1, 31):
                Data["Chats"][ChatID]["Khetmat In Progress"][Number][str(Juzaa)] = [None]

            self.Save_Data(Data)
            return True    
        
    def Update_Juzaa_Satus(self, call, message, KhetmaNumber,  JuzaaNumber, NewStatus):
        # Status: "Occupied", "Finished", "Pulled"

        Data = self.Load_Data()

        try:
            ChatID = str(call.message.chat.id)
        except AttributeError:
            ChatID = str(message.chat.id)

        if ChatID not in Data["Chats"]:
            return False
        else:
            if NewStatus == "Finished":
                Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)][str(JuzaaNumber)] = "\u2705"
            elif NewStatus == "Occupied":                 
                UserName = call.from_user.username
                UserID = call.from_user.id
                Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)][str(JuzaaNumber)] = [f"@{UserName}", str(UserID)]
        
            elif NewStatus == "Pulled":
                Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)][str(JuzaaNumber)] = [None]

            self.Save_Data(Data)
            return True
    
    def Delete_Khetma(self, ChatID, KhetmaNumber):
        Data = self.Load_Data()

        if str(KhetmaNumber) in Data["Chats"][ChatID]["Khetmat In Progress"]:
            del Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)]
            self.Save_Data(Data)
            return True
        return False
    
class GroupManger:
    def __init__(self):
        pass
    
    @classmethod
    def Get_Chat_Admins(cls, ChatID):
        AdminList = []
        for admin in DullaniBot.get_chat_administrators(ChatID):
            AdminList.append(str(admin.user.id))
        return AdminList    
    
    @classmethod
    def Check_If_Admin(cls, UserID, ChatID):
        return str(UserID) in GroupManger.Get_Chat_Admins(ChatID)

    @classmethod
    def Bot_Is_Member(cls, ChatID):
        try:
            Test = DullaniBot.get_chat_member(ChatID, DullaniBot.get_me().id)
        except telebot.apihelper.ApiTelegramException as error:
            return False
        return True
           

class BotFeatures:
    def __init__(self):
        pass
    
    @classmethod
    def Create_New_Khetma(cls, message, ChatID):
        Manage = DataManager(MainDataBase)
        Data = Manage.Load_Data()

        if str(ChatID) in Data["Chats"]:
            KhetmaNumber = Data["Chats"][ChatID]["Number Of Khetmat"] + 1
            KhetmaID = message.message_id + 1
            if "نية" in message.text:
                Intent = message.text[message.text.find("نية") + 3 :].strip()
            else:
                Intent = None

            Manage.Save_Khetma(ChatID, KhetmaNumber, Intent, KhetmaID)

            return Main_Khetma_Form(MainDataBase, ChatID, KhetmaNumber)

    @classmethod
    def Get_Khetma_Number(cls, message):
        for word in message.text.split():
            if word.isdigit():
                return str(word)     

    @classmethod
    def Take_Juzaa(cls, call):
        # Status: "Already Finished", "Already Occupied", "Already Taken", "Taken Successfully"

        Manager = DataManager(MainDataBase)
        Data = Manager.Load_Data()
        ChatID = str(call.message.chat.id)
        KhetmaNumber = BotFeatures.Get_Khetma_Number(call.message)
        JuzaaNumber = call.data.replace("j", "")

        if Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)][str(JuzaaNumber)] == "\u2705":
            return "Already Finished"
        elif Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)][str(JuzaaNumber)] == [None]:
            Manager.Update_Juzaa_Satus(call, call, KhetmaNumber, JuzaaNumber, "Occupied")
            DullaniBot.edit_message_text(Main_Khetma_Form(MainDataBase, ChatID, KhetmaNumber),ChatID ,call.message.message_id, reply_markup=KhetmaKyboardMarkup)
            return "Taken Successfully"
        elif Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)][str(JuzaaNumber)][1] == call.from_user.id:
            return "Already Taken"
        else:
            return "Already Occupied"

    @classmethod
    def Pull_Juzaa(cls, message, KhetmaNumber, AjzaaNumbersList):
        Manager = DataManager(MainDataBase)
        Data = Manager.Load_Data()
        ChatID = str(message.chat.id)
      
        if KhetmaNumber == None:
            try:
                KhetmaNumber = BotFeatures.Get_Khetma_Number(message.reply_to_message)
            except AttributeError:
                return False
            
        PulledAjzaa = []
        FinalText = ""

        for Juzaa in AjzaaNumbersList:
            if Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)][str(Juzaa)] == [None]:
                Manager.Update_Juzaa_Satus(message,message, KhetmaNumber, Juzaa, "Finished")
                FinalText += f"\nإن الجزء {Juzaa} غير مأخوذ.\n"
                
            else:
                Manager.Update_Juzaa_Satus(message,message, KhetmaNumber, Juzaa, "Pulled")
                FinalText += f"\nتم سحب الجزء {Juzaa}\n"

        try:
            KhetmaID = Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)]["Khetma Message ID"]
            DullaniBot.edit_message_text(Main_Khetma_Form(MainDataBase, ChatID, KhetmaNumber),ChatID, KhetmaID, reply_markup=KhetmaKyboardMarkup)
        except telebot.apihelper.ApiTelegramException:
            pass

        return FinalText            

    @classmethod
    def Finish_Ajzaa(cls, message, KhetmaNumber, AjzaaNumbersList):
        Manager = DataManager(MainDataBase)
        Data = Manager.Load_Data()
        ChatID = str(message.chat.id)
        UserID = str(message.from_user.id)
      
        if KhetmaNumber == None:
            try:
                KhetmaNumber = BotFeatures.Get_Khetma_Number(message.reply_to_message)
            except AttributeError:
                return False
            
        DoneReading = []
        FinalText = ""

        if str(KhetmaNumber) not in Data["Chats"][ChatID]["Khetmat In Progress"]:
            return "عذراً, إن الختمة التي تطلبها منتهية أو ملغيّة"
        
        for Juzaa in AjzaaNumbersList:
            if Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)][str(Juzaa)] == "\u2705":
                FinalText += f"\nإن الجزء {Juzaa} منتهٍ مُسبقاً.\n"

            elif Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)][str(Juzaa)] == [None]:
                Manager.Update_Juzaa_Satus(message,message, KhetmaNumber, Juzaa, "Finished")
                FinalText += f"\nإن الجزء {Juzaa} غير مأخوذ, لذلك لا بأس عليك.\n"
                DoneReading.append(str(Juzaa))
                
            elif Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)][str(Juzaa)][1] == UserID:
                Manager.Update_Juzaa_Satus(message,message, KhetmaNumber, Juzaa, "Finished")
                DoneReading.append(str(Juzaa))
        
        try:
            KhetmaID = Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)]["Khetma Message ID"]
            DullaniBot.edit_message_text(Main_Khetma_Form(MainDataBase, ChatID, KhetmaNumber),ChatID, KhetmaID, reply_markup=KhetmaKyboardMarkup)
        except telebot.apihelper.ApiTelegramException:
            pass
        

        FinishedKhetmaText = ""
        if BotFeatures.Khetma_IsFinished(str(message.chat.id), str(KhetmaNumber)):
            FinishedKhetmaText = BotFeatures.Finish_Khetma(str(ChatID), str(KhetmaNumber))

        if DoneReading != []:
            FinalText += f"\nلقد قرأت {' و '.join(DoneReading)}, جزاكم اللهُ خيراً.\n"

        return FinalText, FinishedKhetmaText            

    @classmethod
    def Finish_All_User_Ajzaa(cls, message, ChatID, UserID):
        Manager = DataManager(MainDataBase)
        Data = Manager.Load_Data()

        FinalText = ""
        FinishedKhetmaText = ""
        for Khetma in Data["Chats"][ChatID]["Khetmat In Progress"]:
            UsersAjzaa = BotFeatures.Find_User_Ajzaa_In_Khetma(Khetma, ChatID, UserID)
            if UsersAjzaa == []:
                continue
            else:
                Result = BotFeatures.Finish_Ajzaa(message, Khetma, UsersAjzaa)
                FinalText += f"من الختمة {Khetma}: {Result[0]}"
                if Result[1] != None:
                    FinishedKhetmaText += Result[1]
        
        return FinalText, FinishedKhetmaText

    @classmethod
    def Find_User_Ajzaa_In_Khetma(cls, KhetmaNumber, ChatID, UserID):
        Manager = DataManager(MainDataBase)
        Data = Manager.Load_Data()

        UsersAjzaa = []

        for Juzaa in Data["Chats"][ChatID]["Khetmat In Progress"][KhetmaNumber]:
            try:
                if Data["Chats"][ChatID]["Khetmat In Progress"][KhetmaNumber][Juzaa][1] == UserID:
                    UsersAjzaa.append(Juzaa) 
            except (IndexError, TypeError):
                pass
        return UsersAjzaa
    
    @classmethod 
    def Find_All_User_Ajzaa(cls, ChatID, UserID):
        Manager = DataManager(MainDataBase)
        Data = Manager.Load_Data()

        FinalText = ""

        for Khetma in Data["Chats"][ChatID]["Khetmat In Progress"]:
            UsersAjzaa = BotFeatures.Find_User_Ajzaa_In_Khetma(Khetma, ChatID, UserID)
            if UsersAjzaa != []:
                FinalText += f"من الختمة {Khetma} لديك الأجزاء {' و '.join(UsersAjzaa)}.\n"

        return FinalText
    
    @classmethod
    def Find_Not_Taken_Ajzaa(cls, ChatID):
        Manager = DataManager(MainDataBase)
        Data = Manager.Load_Data()

        FinalText = ""

        for Khetma in Data["Chats"][ChatID]["Khetmat In Progress"]:
            NotTakenAjzaa = []
            for Juzaa in Data["Chats"][ChatID]["Khetmat In Progress"][Khetma]:
                if Data["Chats"][ChatID]["Khetmat In Progress"][Khetma][Juzaa] == [None]:
                    NotTakenAjzaa.append(Juzaa)

            Chat = DullaniBot.get_chat(ChatID)
            ChatType = Chat.username if Chat.username else "c"
            KhetmaID = Data["Chats"][ChatID]["Khetmat In Progress"][Khetma]["Khetma Message ID"]

            if NotTakenAjzaa != []:
                KhetmaLink = f"https://t.me/{ChatType}/{ChatID}/{KhetmaID}".replace("-100", "")
                FinalText += f"الأجزاء المُتاحة من [الختمة {Khetma}]({KhetmaLink}):\n[{', '.join(NotTakenAjzaa)}]\n"

        return FinalText

    @classmethod
    def Khetma_IsFinished(cls, ChatID, KhetmaNumber):
        Manager = DataManager(MainDataBase)
        Data = Manager.Load_Data()

        for Juzaa in range(2, 31):
            if Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)][str(Juzaa)] != "\u2705":
                return False
            
        return True
    
    @classmethod
    def Finish_Khetma(cls, ChatID, KhetmaNumber):
        Manager = DataManager(MainDataBase)
        Data = Manager.Load_Data()

        KhetmaMessage = Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)]["Khetma Message ID"]
        DullaniBot.unpin_chat_message(ChatID, KhetmaMessage)
        Manager.Delete_Khetma(str(ChatID), str(KhetmaNumber))

        return f"لقد انتهت الختمة {KhetmaNumber}, جزاكم اللهٌ خيراً وتقبّل منكم.\n" 
    
class Brodcast:
    @classmethod
    def Announce(cls, message):
        Manager = DataManager(MainDataBase)
        Data = Manager.Load_Data()

        Manager.Reload_Chats()

        if message.text not in ["الغاء", "الالغاء", "إلغاء", "الإلغاء"]:
            for Chat in Data["Chats"]:
                DullaniBot.send_message(Chat, message.text)
            DullaniBot.reply_to(message, "تم تعميم الرسالة بنجاح")

        DullaniBot.reply_to(message, "تم الإلغاء")