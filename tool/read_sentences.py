"""Sentences for the reading paths, Japanese and Mandarin.

Japanese sentences use only kana the learner has met (hiragana, katakana and the extras).
Mandarin sentences use only hanzi taught in the Mandarin reading course (tool/zh_extra.py and
the first units in gen_lessons.py). One source for the flashcard decks and the lessons.

A sentence is (parts, reading, meaning, hint, blank). `parts` are the word chips; joined they
are the sentence, punctuation attached to the last chip. `blank` is None or
(index of the part to hide, four options). The other three options must not fit the gap.
"""

JA_PARTICLES = ["は", "を", "に", "の"]

JA = [
 ("ja_wa_desu", "は and です", [
   "Time to read whole sentences. Japanese puts the verb or ending last, and small words called particles show each word's job.",
   "は marks the topic: 'as for this...'. It is written は but said 'wa' here. です (desu) is the polite 'is' or 'am' that closes the sentence. The u is almost silent.",
   "So これはほんです is word for word 'This (topic) book is': This is a book.",
  ], [
   (["わたし", "は", "がくせい", "です。"], "watashi wa gakusei desu.", "I am a student.",
    "わたし is I. は is said 'wa'. がくせい is student.", (1, ["は", "を", "に", "で"])),
   (["これ", "は", "ほん", "です。"], "kore wa hon desu.", "This is a book.",
    "これ is this, close to you. ほん is book.", (1, ["は", "を", "に", "へ"])),
   (["それ", "は", "ペン", "です。"], "sore wa pen desu.", "That is a pen.",
    "それ is that, near the listener. ペン is pen, in katakana because it is a borrowed word.", (1, ["は", "を", "に", "へ"])),
   (["あれ", "は", "くるま", "です。"], "are wa kuruma desu.", "That over there is a car.",
    "あれ is that over there, far from both of you. くるま is car.", (1, ["は", "を", "に", "へ"])),
   (["たなかさん", "は", "せんせい", "です。"], "tanaka-san wa sensei desu.", "Mr. Tanaka is a teacher.",
    "さん is a polite ending for names, like Mr. or Ms. Never use it for yourself.", None),
  ]),
 ("ja_ka", "か: asking questions", [
   "Add か at the end of a sentence and it becomes a question. Your voice does not need to rise.",
   "Question words take the place of the answer: なん (what), どこ (where), いくら (how much), だれ (who).",
   "これはなんですか is 'This (topic) what is?': What is this?",
  ], [
   (["これ", "は", "なん", "です", "か。"], "kore wa nan desu ka.", "What is this?",
    "なん means what. The か at the end makes the question.", (4, ["か。", "を。", "に。", "で。"])),
   (["あなた", "は", "がくせい", "です", "か。"], "anata wa gakusei desu ka.", "Are you a student?",
    "あなた is you. Japanese often leaves it out and uses a name instead.", (4, ["か。", "を。", "に。", "で。"])),
   (["トイレ", "は", "どこ", "です", "か。"], "toire wa doko desu ka.", "Where is the toilet?",
    "どこ is where. A very useful sentence.", (4, ["か。", "を。", "に。", "で。"])),
   (["これ", "は", "いくら", "です", "か。"], "kore wa ikura desu ka.", "How much is this?",
    "いくら is how much.", (4, ["か。", "を。", "に。", "で。"])),
   (["あの", "ひと", "は", "だれ", "です", "か。"], "ano hito wa dare desu ka.", "Who is that person?",
    "あの is that (before a noun). ひと is person. だれ is who.", None),
  ]),
 ("ja_no", "の: belonging", [
   "の links two nouns and shows belonging, like 's in English: わたしのほん is 'my book'.",
   "It also joins a place to a thing: にほんのおちゃ is 'Japan's tea', so Japanese tea.",
  ], [
   (["わたし", "の", "ほん", "です。"], "watashi no hon desu.", "It is my book.",
    "わたしの is my.", (1, ["の", "を", "に", "へ"])),
   (["これ", "は", "わたし", "の", "かばん", "です。"], "kore wa watashi no kaban desu.", "This is my bag.",
    "かばん is bag.", (3, ["の", "を", "に", "へ"])),
   (["たなかさん", "の", "くるま", "です。"], "tanaka-san no kuruma desu.", "It is Mr. Tanaka's car.",
    "Put の after the owner.", (1, ["の", "を", "に", "へ"])),
   (["にほん", "の", "おちゃ", "です。"], "nihon no ocha desu.", "It is Japanese tea.",
    "にほん is Japan. おちゃ is tea.", (1, ["の", "を", "に", "へ"])),
   (["せんせい", "の", "ペン", "です。"], "sensei no pen desu.", "It is the teacher's pen.",
    "せんせい is teacher.", (1, ["の", "を", "に", "へ"])),
  ]),
 ("ja_wo", "を: the thing you act on", [
   "を marks the object of a verb, the thing the action lands on: みずをのみます is 'water (object) drink': I drink water.",
   "を is written を but said 'o', just like お. It is only used as this marker.",
   "Polite verbs end in ます. のみます is drink, たべます is eat, よみます is read.",
  ], [
   (["みず", "を", "のみます。"], "mizu o nomimasu.", "I drink water.",
    "みず is water. のみます is drink. The を sounds like o.", (1, ["を", "に", "の", "へ"])),
   (["ごはん", "を", "たべます。"], "gohan o tabemasu.", "I eat rice.",
    "ごはん is cooked rice, and also a meal. たべます is eat.", (1, ["を", "に", "の", "へ"])),
   (["ほん", "を", "よみます。"], "hon o yomimasu.", "I read a book.",
    "よみます is read.", (1, ["を", "に", "の", "へ"])),
   (["テレビ", "を", "みます。"], "terebi o mimasu.", "I watch TV.",
    "みます is look or watch.", (1, ["を", "に", "の", "へ"])),
   (["おんがく", "を", "ききます。"], "ongaku o kikimasu.", "I listen to music.",
    "おんがく is music. ききます is listen.", (1, ["を", "に", "の", "へ"])),
  ]),
 ("ja_ni_de", "に and で: where", [
   "に points to where you are going or coming back to: がっこうにいきます is 'to school go'.",
   "で marks where an action happens: レストランでたべます is 'at a restaurant eat'.",
   "A quick test: if the verb is a movement like go or return, use に. If it is an action like eat or study, use で for the place.",
  ], [
   (["がっこう", "に", "いきます。"], "gakkou ni ikimasu.", "I go to school.",
    "がっこう is school. いきます is go.", (1, ["に", "を", "で", "の"])),
   (["いえ", "に", "かえります。"], "ie ni kaerimasu.", "I go home.",
    "いえ is house or home. かえります is return.", (1, ["に", "を", "で", "の"])),
   (["えき", "で", "あいます。"], "eki de aimasu.", "We meet at the station.",
    "えき is station. あいます is meet.", (1, ["で", "を", "の", "へ"])),
   (["レストラン", "で", "たべます。"], "resutoran de tabemasu.", "I eat at a restaurant.",
    "The restaurant is where the eating happens.", (1, ["で", "を", "の", "へ"])),
   (["としょかん", "で", "べんきょうします。"], "toshokan de benkyou shimasu.", "I study at the library.",
    "としょかん is library. べんきょうします is study.", (1, ["で", "を", "の", "へ"])),
  ]),
 ("ja_mo_to", "も and と: also, and with", [
   "も means also and takes the place of は: わたしもがくせいです is 'I too am a student'.",
   "と means and, or with: ともだちといきます is 'with a friend go'.",
  ], [
   (["わたし", "も", "がくせい", "です。"], "watashi mo gakusei desu.", "I am a student too.",
    "も replaces は when you mean also.", (1, ["も", "を", "に", "で"])),
   (["ともだち", "と", "いきます。"], "tomodachi to ikimasu.", "I go with a friend.",
    "ともだち is friend.", (1, ["と", "を", "の", "で"])),
   (["コーヒー", "も", "のみます。"], "koohii mo nomimasu.", "I drink coffee too.",
    "も here means too or also.", (1, ["も", "の", "と", "へ"])),
   (["ちち", "と", "はは", "は", "せんせい", "です。"], "chichi to haha wa sensei desu.", "My father and mother are teachers.",
    "ちち and はは are my own father and mother. と joins the two.", (1, ["と", "を", "で", "へ"])),
   (["わたし", "も", "いきます。"], "watashi mo ikimasu.", "I will go too.",
    "Same pattern: わたしも, 'I also'.", (1, ["も", "を", "の", "へ"])),
  ]),
 ("ja_i_adj", "Describing things: おいしい", [
   "Words like おいしい (delicious) end in い and are called い-adjectives. They go straight in front of です.",
   "これはおいしいです is 'This is delicious'. The adjective comes straight before です, with nothing in between.",
  ], [
   (["これ", "は", "おいしい", "です。"], "kore wa oishii desu.", "This is delicious.",
    "おいしい is delicious. The long ii is held for two beats.", (3, ["です。", "ます。", "を。", "に。"])),
   (["あの", "くるま", "は", "おおきい", "です。"], "ano kuruma wa ookii desu.", "That car is big.",
    "おおきい is big. The oo is long.", (4, ["です。", "ます。", "を。", "に。"])),
   (["この", "ほん", "は", "おもしろい", "です。"], "kono hon wa omoshiroi desu.", "This book is interesting.",
    "おもしろい is interesting or funny.", (4, ["です。", "ます。", "を。", "に。"])),
   (["きょう", "は", "あつい", "です。"], "kyou wa atsui desu.", "Today is hot.",
    "きょう is today. あつい is hot.", (3, ["です。", "ます。", "を。", "に。"])),
   (["わたし", "の", "いえ", "は", "ちいさい", "です。"], "watashi no ie wa chiisai desu.", "My house is small.",
    "ちいさい is small.", None),
  ]),
 ("ja_neg_past", "Not, and in the past", [
   "To say not, use ありません after では: がくせいではありません is 'is not a student'. For verbs, ます becomes ません.",
   "For the past, ます becomes ました: いきます (go) becomes いきました (went). And い-adjectives drop い and add かった: あつい becomes あつかった.",
  ], [
   (["わたし", "は", "がくせい", "では", "ありません。"], "watashi wa gakusei dewa arimasen.", "I am not a student.",
    "では + ありません is the polite not of です.", (4, ["ありません。", "あります。", "です。", "ました。"])),
   (["さかな", "は", "たべません。"], "sakana wa tabemasen.", "I do not eat fish.",
    "さかな is fish. たべません is do not eat.", None),
   (["きのう", "がっこう", "に", "いきました。"], "kinou gakkou ni ikimashita.", "I went to school yesterday.",
    "きのう is yesterday, so the verb is in the past.", (3, ["いきました。", "いきます。", "いきません。", "いって。"])),
   (["きのう", "は", "あつかった", "です。"], "kinou wa atsukatta desu.", "Yesterday was hot.",
    "あつかった is the past of あつい. The small っ is a held beat.", (2, ["あつかった", "あつい", "あつく", "あつくない"])),
   (["おいしかった", "です。"], "oishikatta desu.", "It was delicious.",
    "おいしかった is the past of おいしい. Handy after a meal.", None),
  ]),
]

ZH = [
 ("zh_shi", "是: to be", [
   "Time to read whole sentences. Every character here is one you have already learned.",
   "Mandarin has no changing forms. 是 means am, is and are, so 我是学生 is word for word 'I be student': I am a student.",
   "Word order is close to English: who, then 是, then what.",
  ], [
   (["我", "是", "学生。"], "wǒ shì xuésheng.", "I am a student.",
    "我 is I. 学生 is student.", (1, ["是", "吃", "喝", "去"])),
   (["他", "是", "老师。"], "tā shì lǎoshī.", "He is a teacher.",
    "他 is he. 老师 is teacher.", (1, ["是", "吃", "喝", "去"])),
   (["她", "是", "我", "妈妈。"], "tā shì wǒ māma.", "She is my mom.",
    "For close family you can skip 的: 我妈妈 is my mom.", (1, ["是", "很", "太", "多"])),
   (["他们", "是", "我的", "朋友。"], "tāmen shì wǒ de péngyou.", "They are my friends.",
    "们 makes 他 into 他们, they. 我的 is my.", (1, ["是", "吃", "喝", "去"])),
   (["我们", "是", "中国人。"], "wǒmen shì Zhōngguórén.", "We are Chinese.",
    "中国人 is a Chinese person.", None),
  ]),
 ("zh_ma", "吗: yes or no questions", [
   "Put 吗 at the end of a statement and it becomes a yes or no question. There is no change in word order.",
   "你是学生 is 'You are a student.' Add 吗 and 你是学生吗？ asks 'Are you a student?'",
  ], [
   (["你", "是", "学生", "吗？"], "nǐ shì xuésheng ma?", "Are you a student?",
    "吗 is light and short.", (3, ["吗？", "的？", "们？", "是？"])),
   (["你", "好", "吗？"], "nǐ hǎo ma?", "How are you?",
    "Word for word: you good question? A very common greeting.", (2, ["吗？", "的？", "们？", "是？"])),
   (["他", "是", "老师", "吗？"], "tā shì lǎoshī ma?", "Is he a teacher?",
    "Same pattern: statement plus 吗.", (3, ["吗？", "的？", "们？", "是？"])),
   (["这", "是", "你的", "书", "吗？"], "zhè shì nǐ de shū ma?", "Is this your book?",
    "你的 is your. 书 is book.", (4, ["吗？", "的？", "们？", "是？"])),
   (["你", "有", "朋友", "吗？"], "nǐ yǒu péngyou ma?", "Do you have friends?",
    "有 is to have.", (3, ["吗？", "的？", "们？", "是？"])),
  ]),
 ("zh_bu", "不: not", [
   "Put 不 right before the word you want to negate: 我不是老师 is 'I not be teacher': I am not a teacher.",
   "不 is bù, but before a falling tone it flips to rising: 不是 is bú shì. You will hear the change, but the character stays the same.",
  ], [
   (["我", "不", "是", "老师。"], "wǒ bú shì lǎoshī.", "I am not a teacher.",
    "不 before 是 sounds like bú.", (1, ["不", "很", "太", "多"])),
   (["他", "不", "吃", "肉。"], "tā bù chī ròu.", "He does not eat meat.",
    "不 goes before the verb.", (1, ["不", "太", "上", "下"])),
   (["我", "不", "想", "去。"], "wǒ bù xiǎng qù.", "I do not want to go.",
    "不 goes before 想, 'want'.", (1, ["不", "上", "下", "北"])),
   (["她", "不", "喝", "茶。"], "tā bù hē chá.", "She does not drink tea.",
    "喝茶 is drink tea.", (1, ["不", "太", "上", "下"])),
   (["我", "不是", "中国人。"], "wǒ bú shì Zhōngguórén.", "I am not Chinese.",
    "不是 is the full 'am not'.", None),
  ]),
 ("zh_hen", "很: very", [
   "To describe something, put 很 before the adjective: 我很好 is 'I very good': I am well.",
   "Mandarin does not use 是 before adjectives. Say 这个很大, not 这个是大.",
  ], [
   (["我", "很", "好。"], "wǒ hěn hǎo.", "I am very well.",
    "很 here is a light 'very', almost just a linking word.", (1, ["很", "去", "看", "吃"])),
   (["这个", "很", "大。"], "zhège hěn dà.", "This one is very big.",
    "这个 is this one.", (1, ["很", "去", "看", "吃"])),
   (["这本书", "很", "新。"], "zhè běn shū hěn xīn.", "This book is very new.",
    "这本书 is this book. 新 is new.", (1, ["很", "去", "看", "吃"])),
   (["北京", "很", "大。"], "Běijīng hěn dà.", "Beijing is very big.",
    "北京 is Beijing.", (1, ["很", "去", "看", "吃"])),
   (["我", "爸爸", "很", "高。"], "wǒ bàba hěn gāo.", "My dad is very tall.",
    "高 is tall.", (2, ["很", "去", "看", "吃"])),
  ]),
 ("zh_de", "的: belonging", [
   "的 shows belonging, like 's in English: 我的书 is 'my book'. It is light and short, and said 'de'.",
   "It works for any owner: 爸爸的茶 is dad's tea.",
  ], [
   (["这", "是", "我", "的", "书。"], "zhè shì wǒ de shū.", "This is my book.",
    "我的 is my.", (3, ["的", "吗", "很", "不"])),
   (["他", "是", "我", "的", "朋友。"], "tā shì wǒ de péngyou.", "He is my friend.",
    "我的朋友 is my friend.", (3, ["的", "吗", "很", "不"])),
   (["你", "的", "家", "很", "大。"], "nǐ de jiā hěn dà.", "Your home is very big.",
    "你的家 is your home.", (1, ["的", "吗", "不", "是"])),
   (["我", "的", "老师", "是", "中国人。"], "wǒ de lǎoshī shì Zhōngguórén.", "My teacher is Chinese.",
    "我的老师 is my teacher.", (1, ["的", "吗", "不", "很"])),
   (["这", "是", "爸爸", "的", "茶。"], "zhè shì bàba de chá.", "This is dad's tea.",
    "爸爸的 is dad's.", (3, ["的", "吗", "很", "不"])),
  ]),
 ("zh_xiang", "想: want to", [
   "想 means want to. It goes before the verb: 我想吃 is 'I want eat': I want to eat.",
   "去 is go. 去学校 is go to school. Mandarin does not need a word for 'to' here.",
  ], [
   (["我", "想", "吃", "米饭。"], "wǒ xiǎng chī mǐfàn.", "I want to eat rice.",
    "米饭 is cooked rice.", (1, ["想", "大", "小", "新"])),
   (["我", "想", "喝", "茶。"], "wǒ xiǎng hē chá.", "I want to drink tea.",
    "喝 is drink.", (1, ["想", "大", "小", "新"])),
   (["我", "想", "去", "学校。"], "wǒ xiǎng qù xuéxiào.", "I want to go to school.",
    "学校 is school.", (1, ["想", "大", "小", "新"])),
   (["你", "想", "去", "北京", "吗？"], "nǐ xiǎng qù Běijīng ma?", "Do you want to go to Beijing?",
    "吗 makes it a question.", (1, ["想", "大", "小", "新"])),
   (["我们", "想", "买", "书。"], "wǒmen xiǎng mǎi shū.", "We want to buy books.",
    "买 is buy.", (1, ["想", "大", "小", "新"])),
  ]),
 ("zh_qwords", "Question words", [
   "A question word goes where the answer would go. 你想吃什么 is 'you want eat what': What do you want to eat? No change in word order.",
   "什么 is what, 哪里 is where, 谁 is who. They do not need 吗 as well.",
  ], [
   (["你", "想", "吃", "什么？"], "nǐ xiǎng chī shénme?", "What do you want to eat?",
    "什么 is what. The 么 is light.", (3, ["什么？", "哪里？", "谁？", "是？"])),
   (["这", "是", "什么？"], "zhè shì shénme?", "What is this?",
    "Point and ask.", None),
   (["你", "想", "去", "哪里？"], "nǐ xiǎng qù nǎlǐ?", "Where do you want to go?",
    "哪里 is where. The 里 is light.", (3, ["哪里？", "什么？", "谁？", "是？"])),
   (["他", "是", "谁？"], "tā shì shéi?", "Who is he?",
    "谁 is who.", None),
   (["你", "喝", "什么", "茶？"], "nǐ hē shénme chá?", "What tea do you drink?",
    "什么茶 is what tea, or what kind of tea.", None),
  ]),
 ("zh_time", "When: today, tomorrow", [
   "Time words go near the start of the sentence, before the person: 明天我去北京 is 'tomorrow I go Beijing'.",
   "The verb does not change for tense. The time word tells you when.",
  ], [
   (["今天", "我", "去", "学校。"], "jīntiān wǒ qù xuéxiào.", "Today I go to school.",
    "今天 is today.", None),
   (["明天", "我们", "去", "北京。"], "míngtiān wǒmen qù Běijīng.", "Tomorrow we go to Beijing.",
    "明天 is tomorrow.", None),
   (["昨天", "我", "看", "书。"], "zuótiān wǒ kàn shū.", "Yesterday I read a book.",
    "昨天 is yesterday. 看书 is to read, literally look at a book.", None),
   (["上午", "我", "读", "书。"], "shàngwǔ wǒ dú shū.", "In the morning I read.",
    "上午 is morning. 读书 is to read, or to study.", None),
   (["下午", "三点", "我", "去", "买菜。"], "xiàwǔ sān diǎn wǒ qù mǎi cài.", "At three in the afternoon I go grocery shopping.",
    "三点 is three o'clock. 买菜 is buy groceries.", None),
  ]),
]

def flat(units):
    """(card id, text, reading, meaning, hint, unit id, parts, blank) in order."""
    out, n = [], 0
    for uid, title, intro, sentences in units:
        for parts, reading, meaning, hint, blank in sentences:
            n += 1
            out.append((str(n), ''.join(parts), reading, meaning, hint, uid, parts, blank))
    return out
