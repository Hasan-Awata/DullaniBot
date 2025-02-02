def DetictNumbersInText(text):
    Main_Numbers = {
        'الأول': 1, 'الاول': 1, 'الثاني': 2, 'الثالث': 3, 'الرابع': 4, 'الخامس': 5,
        'السادس': 6, 'السابع': 7, 'الثامن': 8, 'التاسع': 9, 'العاشر': 10      
    }
    
    Secondary_Numbers = {
        'عشر': 10,
        'العشرون': 20, 'العشرين': 20,
        'الثلاثون': 30, 'الثلاثين': 30,
        'الاربعون': 40, 'الأربعون': 40, 'الاربعين': 40, 'الأربعين': 40,
        'الخمسون': 50, 'الخمسين': 50,
        'الستون': 60, 'الستين': 60,
        'السبعون': 70, 'السبعين': 70,
        'الثمانون': 80, 'الثمانين': 80,
        'التسعون': 90, 'التسعين': 90,
    }
    
    Hundreds = {
        'المئة': 100, 'مئة': 100, "مائة": 100,
    }

    NumbersInText = []
    
    # Normalize spaces and Arabic numerals
    text = text.replace(' و ', ' ').strip()
    text = text.replace(' و', ' ').strip()
    text = text.translate(str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789"))
    words = text.split()

    i = 0
    while i < len(words):
        word = words[i]

        if word.isdigit():  # Direct numeric values (Arabic or Hindic numerals)
            NumbersInText.append(int(word))

        elif word in Main_Numbers:
            # Check if there's a secondary number following this main number
            if i + 1 < len(words) and words[i + 1] in Secondary_Numbers:
                FinalNum = Main_Numbers[word] + Secondary_Numbers[words[i + 1]]
                NumbersInText.append(FinalNum)
                i += 1  # Skip next word as it's already processed
            else:
                NumbersInText.append(Main_Numbers[word])

        elif word in Secondary_Numbers:
            # If a secondary number appears without a main number before it, add it as-is
            NumbersInText.append(Secondary_Numbers[word])

        else:
            # Handle cases like "السادس عشر"
            for main in Main_Numbers:
                for sec in Secondary_Numbers:
                    if main in word and sec in word:
                        NumbersInText.append(Main_Numbers[main] + Secondary_Numbers[sec])
                        break  # Stop checking after the first match

        i += 1  # Move to next word

    return NumbersInText

