from telebot import *
import telebot
from telegram import *
import json
import telegram
from random import *
from telegram.error import BadRequest 
from telegram.error import TelegramError
from decouple import config
from telebot import types
from FunctionsLibrary import *

BOT_TOKEN = config("BOT_TOKEN")
DullaniBot = telebot.TeleBot(BOT_TOKEN)
MainDataBase = "data.json"

def Main_Khetma_Form(FileName, ChatID, KhetmaNumber):
   with open(FileName,'r') as JsonFile:
      Data = json.load(JsonFile)
   JsonFile.close()

   if Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)]["Khetma Intent"] != None:
      Intent = f"---> على نيّة {Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)]["Khetma Intent"]}"
   else:
      Intent = ""

   Form = f"""
               ---> الختمة رقم : {KhetmaNumber}
{Intent}               
       الجزء الأول : {Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)]["1"][0]}
       الجزء الثاني : {Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)]["2"][0]}
       الجزء الثالث : {Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)]["3"][0]}
       الجزء الرابع : {Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)]["4"][0]}
       الجزء الخامس : {Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)]["5"][0]}
       الجزء السادس : {Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)]["6"][0]}
       الجزء السابع : {Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)]["7"][0]}
       الجزء الثامن : {Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)]["8"][0]}
       الجزء التاسع : {Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)]["9"][0]}
       الجزء العاشر : {Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)]["10"][0]}

       الجزء الحادي عشر : {Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)]["11"][0]}
       الجزء الثاني عشر : {Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)]["12"][0]}
       الجزء الثالث عشر : {Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)]["13"][0]}
       الجزء الرابع عشر : {Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)]["14"][0]}
       الجزء الخامس عشر : {Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)]["15"][0]}
       الجزء السادس عشر : {Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)]["16"][0]}
       الجزء السابع عشر : {Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)]["17"][0]}
       الجزء الثامن عشر : {Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)]["18"][0]}
       الجزء التاسع عشر : {Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)]["19"][0]}
       الجزء العشرون : {Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)]["20"][0]}

       الجزء الحادي والعشرون : {Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)]["21"][0]} 
       الجزء الثاني و العشرون : {Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)]["22"][0]}
       الجزء الثالث والعشرون : {Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)]["23"][0]}
       الجزء الرابع و العشرون : {Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)]["24"][0]}
       الجزء الخامس والعشرون : {Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)]["25"][0]} 
       الجزء السادس و العشرون : {Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)]["26"][0]}
       الجزء السابع والعشرون : {Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)]["27"][0]} 
       الجزء الثامن و العشرون : {Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)]["28"][0]}
       الجزء التاسع والعشرون : {Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)]["29"][0]} 
       الجزء الثلاثون : {Data["Chats"][ChatID]["Khetmat In Progress"][str(KhetmaNumber)]["30"][0]}
  
             """
   return Form


KhetmaKyboard = [[ 
 InlineKeyboardButton("1",callback_data="1j"),
 InlineKeyboardButton("2",callback_data="2j"),
 InlineKeyboardButton("3",callback_data="3j"),
 InlineKeyboardButton("4",callback_data="4j"),
 InlineKeyboardButton("5",callback_data="5j"),
 InlineKeyboardButton("6",callback_data="6j")],

[ InlineKeyboardButton("7",callback_data="7j"),
  InlineKeyboardButton("8",callback_data="8j"),
  InlineKeyboardButton("9",callback_data="9j"),
  InlineKeyboardButton("10",callback_data="10j"),
  InlineKeyboardButton("11",callback_data="11j"),
  InlineKeyboardButton("12",callback_data="12j")],

[InlineKeyboardButton("13",callback_data="13j"),
InlineKeyboardButton("14",callback_data="14j"),
InlineKeyboardButton("15",callback_data="15j"),
InlineKeyboardButton("16",callback_data="16j"),
InlineKeyboardButton("17",callback_data="17j"),
InlineKeyboardButton("18",callback_data="18j")],

[InlineKeyboardButton("19",callback_data="19j"),
InlineKeyboardButton("20",callback_data="20j"),
InlineKeyboardButton("21",callback_data="21j"),
InlineKeyboardButton("22",callback_data="22j"),
InlineKeyboardButton("23",callback_data="23j"),
InlineKeyboardButton("24",callback_data="24j")],

[InlineKeyboardButton("25",callback_data="25j"),
 InlineKeyboardButton("26",callback_data="26j"),
InlineKeyboardButton("27",callback_data="27j"),
InlineKeyboardButton("28",callback_data="28j"),
InlineKeyboardButton("29",callback_data="29j"),
InlineKeyboardButton("30",callback_data="30j")]]

KhetmaKyboardMarkup = types.InlineKeyboardMarkup(KhetmaKyboard)


ChooseAjzaaKeyBoard =[[InlineKeyboardButton("اختيار أجزاء",callback_data="Choose")]]
ChooseAjzaaMarkup = types.InlineKeyboardMarkup(ChooseAjzaaKeyBoard)


BotFeaturesKeyBoard = [[InlineKeyboardButton("🕋 الختمة",callback_data="HelpKhetma"),InlineKeyboardButton("📿 المسبحة",callback_data="HelpSubha")]
                        ,[InlineKeyboardButton("كيفية التشغيل ؟",callback_data="HelpHowToStart")]]
BotFeaturesMarkup = types.InlineKeyboardMarkup(BotFeaturesKeyBoard)

KhetmaDuaa = """اللَّهُمَّ ارْحَمْنِي بالقُرْءَانِ وَاجْعَلهُ لِي إِمَاماً وَنُوراً وَهُدًى وَرَحْمَةً *

اللَّهُمَّ ذَكِّرْنِي مِنْهُ مَانَسِيتُ وَعَلِّمْنِي مِنْهُ مَاجَهِلْتُ وَارْزُقْنِي تِلاَوَتَهُ آنَاءَ اللَّيْلِ وَأَطْرَافَ النَّهَارِ وَاجْعَلْهُ لِي حُجَّةً يَارَبَّ العَالَمِينَ *

اللَّهُمَّ أَصْلِحْ لِي دِينِي الَّذِي هُوَ عِصْمَةُ أَمْرِي، وَأَصْلِحْ لِي دُنْيَايَ الَّتِي فِيهَا مَعَاشِي، وَأَصْلِحْ لِي آخِرَتِي الَّتِي فِيهَا مَعَادِي، وَاجْعَلِ الحَيَاةَ زِيَادَةً لِي فِي كُلِّ خَيْرٍ وَاجْعَلِ المَوْتَ رَاحَةً لِي مِنْ كُلِّ شَرٍّ *

اللَّهُمَّ اجْعَلْ خَيْرَ عُمْرِي آخِرَهُ وَخَيْرَ عَمَلِي خَوَاتِمَهُ وَخَيْرَ أَيَّامِي يَوْمَ أَلْقَاكَ فِيهِ *

اللَّهُمَّ إِنِّي أَسْأَلُكَ عِيشَةً هَنِيَّةً وَمِيتَةً سَوِيَّةً وَمَرَدًّا غَيْرَ مُخْزٍ وَلاَ فَاضِحٍ *

اللَّهُمَّ إِنِّي أَسْأَلُكَ خَيْرَ المَسْأَلةِ وَخَيْرَ الدُّعَاءِ وَخَيْرَ النَّجَاحِ وَخَيْرَ العِلْمِ وَخَيْرَ العَمَلِ وَخَيْرَ الثَّوَابِ وَخَيْرَ الحَيَاةِ وَخيْرَ المَمَاتِ وَثَبِّتْنِي وَثَقِّلْ مَوَازِينِي وَحَقِّقْ إِيمَانِي وَارْفَعْ دَرَجَتِي وَتَقَبَّلْ صَلاَتِي وَاغْفِرْ خَطِيئَاتِي وَأَسْأَلُكَ العُلَا مِنَ الجَنَّةِ *

اللَّهُمَّ إِنِّي أَسْأَلُكَ مُوجِبَاتِ رَحْمَتِكَ وَعَزَائِمِ مَغْفِرَتِكَ وَالسَّلاَمَةَ مِنْ كُلِّ إِثْمٍ وَالغَنِيمَةَ مِنْ كُلِّ بِرٍّ وَالفَوْزَ بِالجَنَّةِ وَالنَّجَاةَ مِنَ النَّارِ *

اللَّهُمَّ أَحْسِنْ عَاقِبَتَنَا فِي الأُمُورِ كُلِّهَا، وَأجِرْنَا مِنْ خِزْيِ الدُّنْيَا وَعَذَابِ الآخِرَةِ *

اللَّهُمَّ اقْسِمْ لَنَا مِنْ خَشْيَتِكَ مَاتَحُولُ بِهِ بَيْنَنَا وَبَيْنَ مَعْصِيَتِكَ وَمِنْ طَاعَتِكَ مَاتُبَلِّغُنَا بِهَا جَنَّتَكَ وَمِنَ اليَقِينِ مَاتُهَوِّنُ بِهِ عَلَيْنَا مَصَائِبَ الدُّنْيَا وَمَتِّعْنَا بِأَسْمَاعِنَا وَأَبْصَارِنَا وَقُوَّتِنَا مَاأَحْيَيْتَنَا وَاجْعَلْهُ الوَارِثَ مِنَّا وَاجْعَلْ ثَأْرَنَا عَلَى مَنْ ظَلَمَنَا وَانْصُرْنَا عَلَى مَنْ عَادَانَا وَلاَ تجْعَلْ مُصِيبَتَنَا فِي دِينِنَا وَلاَ تَجْعَلِ الدُّنْيَا أَكْبَرَ هَمِّنَا وَلَا مَبْلَغَ عِلْمِنَا وَلاَ تُسَلِّطْ عَلَيْنَا مَنْ لَا يَرْحَمُنَا *

اللَّهُمَّ لَا تَدَعْ لَنَا ذَنْبًا إِلَّا غَفَرْتَهُ وَلَا هَمَّا إِلَّا فَرَّجْتَهُ وَلَا دَيْنًا إِلَّا قَضَيْتَهُ وَلَا حَاجَةً مِنْ حَوَائِجِ الدُّنْيَا وَالآخِرَةِ إِلَّا قَضَيْتَهَا يَاأَرْحَمَ الرَّاحِمِينَ *

رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ وَصَلَّى اللهُ عَلَى سَيِّدِنَا وَنَبِيِّنَا مُحَمَّدٍ وَعَلَى آلِهِ وَأَصْحَابِهِ الأَخْيَارِ وَسَلَّمَ تَسْلِيمًا كَثِيراً."""


HelpKhetma = """ 
خاصية الختــمة : 

ختمة موزعة ومنظمة عن طريق البوت , يقوم كل عضو في المجموعة باختيار الجزء عن طريق لوحة الأرقام أسفل رسالة الختمة

---> الأوامر : 

1- ختمة جديدة / بدء ختمة :
لبدء ختمة جديدة بين أعضاء المجموعة

2 - الغاء الختمة :
لالغاء ختمة جارية حالياً في المجموعة

3 - حالة الختمة : 
لرؤية تقدم الختمة و الأجزاء المتبقية

4 - انهاء الختمة : 
لانهاء الختمة في حال انتهاء قراءة جميع الأجزاء

5 - سحب الجزء :
لسحب الجزء من أحد الأعضاء في حال لم يستطع قراءتهُ

6 - تفعيل / تعطيل وضع الجزء الواحد :
للسماح للأعضاء بأخذ جزء واحد من كل ختمة فقط

7 - الجزء (رقم الجزء كتابةً أو عدداً) تم
لاخبار البوت بأنك قرأت الجزء الموكل اليك

8 - في أجزاء ؟ :
عند ارسال هذا الأمر سيخبرك البوت بالأجزاء المتبقية من كل ختمة

9 - عدد الختمات :
لمعرفة عدد الختمات المنجزة في المجموعة

10 - تم قراءة أجزائي :
لاخبار البوت أنك قرأت جميع الأجزاء الموكلة اليك في ختمة معينة

11 - الأجزاء الغير منتهية :
لرؤية الأجزاء التي لم تنتهِ بعد من كل ختمة"""

HelpSubha = """ 
خاصية المسبحـــة الالـــــكترونية :

عبارة عن مسبحة جماعية بين الأعضاء ينشئها المشرف و تمكن أعضاء المجموعة من التسبيح معاً

---> الأوامر :

1 - المسبحة الالكترونية :
لطلب المسبحة الالكترونية أو لانشائها أول مرة 

2 - أزرار المسبحة :

==> تسبيح : لزيادة عدد التسبيحات
==> تصفير : لتصفير المسبحة
==> تغيير الذكر : نلتغيير ذكر المسبحة"""

HelpHowToStart = """ 
أهلاً بك في قائمة أوامر البوت ... 

كيفية التشغيل ؟
1 - اضافة البوت الى المجموعة 
2 - رفعه كمشرف 
3 - طلب الأمر /start@DullaniAllaAlTa3a_bot لحفظ بيانات المجموعة وتفعيل البوت"""