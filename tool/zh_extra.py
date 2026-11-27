"""More Mandarin hanzi for the reading path, appended to the zh_hanzi deck (ids 31 onward).

One source for the deck (gen_decks.py) and the lessons (gen_lessons.py). Each unit is
(id, title, intro paragraphs, characters, words). A character is (hanzi, pinyin, meaning, hint);
the tone sentence is added to the hint automatically from the pinyin tone mark.
Words may only use hanzi taught in this or an earlier unit (the tests check it).
"""
TONES = {
 1: "1st tone: high and flat.", 2: "2nd tone: rising.", 3: "3rd tone: dipping.",
 4: "4th tone: falling.", 5: "Neutral tone: light and short.",
}
_MARKS = {1: 'āēīōūǖ', 2: 'áéíóúǘ', 3: 'ǎěǐǒǔǚ', 4: 'àèìòùǜ'}

def tone_of(pinyin):
    for t, marks in _MARKS.items():
        if any(c in marks for c in pinyin): return t
    return 5

UNITS = [
 ("family", "Family", [
   "Family words are used every day, and most are doubled: 爸爸 (dad) and 妈妈 (mom). The second syllable is light.",
   "Reading pinyin: 'bà' is 'bah'. 'gē' is close to 'guh'. 'jiě' is close to 'jyeh'. 'dì' is 'dee'. 'mèi' is 'may'.",
   "姐 and 妹 both have 女 (woman) on the left, because they are sisters. 哥 and 弟 are brothers.",
  ], [
   ("爸", "bà", "dad, father", "父 (father) on top gives the meaning. Say 'bah'."),
   ("哥", "gē", "older brother", "Two 可 stacked on top of each other: the big brother stands taller."),
   ("姐", "jiě", "older sister", "女 (woman) on the left: a female relative."),
   ("弟", "dì", "younger brother", "Picture a little brother with a topknot and a hook hanging down."),
   ("妹", "mèi", "younger sister", "女 (woman) on the left, like 姐: a female relative."),
  ], [("爸爸", "bàba", "dad"), ("妈妈", "māma", "mom"), ("哥哥", "gēge", "older brother"),
      ("姐姐", "jiějie", "older sister"), ("弟弟", "dìdi", "younger brother"), ("妹妹", "mèimei", "younger sister")]),
 ("school", "School", [
   "Five characters for school life. 学 is 'to study', and it also appears in 学生 (student) and 大学 (university).",
   "Reading pinyin: 'xué' is close to 'shweh': x is a soft sh. 'shēng' is close to 'shung'. 'lǎo' is 'lao' as in 'now'. 'xiào' is close to 'shyow'.",
   "老师 (lǎoshī) is 'old master': a teacher. Respect for age runs through many Chinese words.",
  ], [
   ("学", "xué", "to study, to learn", "A child 子 sits under a roof of little marks: studying at home."),
   ("生", "shēng", "to be born, life, raw", "A sprout pushing up out of the ground: new life."),
   ("老", "lǎo", "old", "A bent old person leaning on a stick."),
   ("师", "shī", "teacher, master", "You will almost always see it in 老师, 'old master': a teacher."),
   ("校", "xiào", "school", "木 (wood) on the left. Together with 学 it makes 学校, school."),
  ], [("学生", "xuésheng", "student"), ("老师", "lǎoshī", "teacher"), ("学校", "xuéxiào", "school"),
      ("大学", "dàxué", "university"), ("小学", "xiǎoxué", "primary school"), ("老人", "lǎorén", "old person"),
      ("大学生", "dàxuéshēng", "university student")]),
 ("home_friends", "Home and friends", [
   "Two small grammar characters and three everyday words.",
   "们 (men) makes a person word plural: 我 is I, 我们 is we. 的 (de) shows belonging: 我的家 is 'my home'. Both are light and short.",
   "Reading pinyin: 'jiā' is 'jyah'. 'péng' is close to 'pung'. 'yǒu' is 'yo'.",
  ], [
   ("们", "men", "(plural for people)", "亻 (person) on the left and 门 (door) on the right. Add it after 我, 你 or 他 to say we, you all, they."),
   ("的", "de", "'s (belonging)", "白 and a small 勺. Put it after a word: 我的 is mine, my."),
   ("家", "jiā", "home, family", "A roof over a pig: the pig was the family's wealth. Home."),
   ("朋", "péng", "friend (in 朋友)", "Two 月 side by side: two companions."),
   ("友", "yǒu", "friend", "Two hands joined: friends. Said 'yo'."),
  ], [("我们", "wǒmen", "we"), ("你们", "nǐmen", "you (all)"), ("他们", "tāmen", "they"),
      ("她们", "tāmen", "they (all women)"), ("我的家", "wǒ de jiā", "my home"), ("朋友", "péngyou", "friend"),
      ("好朋友", "hǎo péngyou", "good friend"), ("我的朋友", "wǒ de péngyou", "my friend"), ("大家", "dàjiā", "everyone")]),
 ("food", "Food and drink", [
   "Words for the table. 饭 can mean cooked rice, and also 'a meal' in general: 吃饭 is to eat.",
   "Reading pinyin: 'fàn' is 'fahn'. 'chá' is 'chah'. 'mǐ' is 'mee'. 'ròu' starts with the buzzing r: close to 'roe'. 'cài' is 'tsai'.",
   "好吃 (hǎochī) is 'good to eat': delicious. 好喝 (hǎohē) is 'good to drink'.",
  ], [
   ("饭", "fàn", "cooked rice, a meal", "饣 (food) on the left. 吃饭 is to eat a meal."),
   ("茶", "chá", "tea", "A plant 艹 on top, a person 人 in the middle, wood 木 below: someone picking tea leaves."),
   ("米", "mǐ", "rice (uncooked)", "Grains of rice on a stalk, fanning out in all directions."),
   ("肉", "ròu", "meat", "A slab of meat with the marbling showing inside."),
   ("菜", "cài", "vegetable, a dish", "艹 (grass) on top. Also means a dish on the table, as in 中国菜."),
  ], [("吃饭", "chīfàn", "to eat a meal"), ("喝茶", "hē chá", "drink tea"), ("米饭", "mǐfàn", "cooked rice"),
      ("吃肉", "chī ròu", "eat meat"), ("好吃", "hǎochī", "delicious"), ("好喝", "hǎohē", "tasty (to drink)"),
      ("中国菜", "Zhōngguó cài", "Chinese food")]),
 ("verbs1", "Go, come, look, say, listen", [
   "Five verbs you will use constantly. Mandarin verbs never change: 去 is go, whoever goes.",
   "Reading pinyin: 'qù' is close to 'chyu': round your lips as for 'ü'. 'lái' is 'lie'. 'kàn' is 'kahn'. 'shuō' is 'shwaw'. 'tīng' is 'ting'.",
   "说 and 听 both have a speech or mouth part on the left, because both belong to talking and hearing.",
  ], [
   ("去", "qù", "to go", "The opposite of 来 (come). Say 'chyoo' with a sharp fall."),
   ("来", "lái", "to come", "A line down the middle with strokes on both sides, like someone with open arms coming toward you."),
   ("看", "kàn", "to look, to watch", "A hand 手 over an eye 目: a hand shading the eyes to look far."),
   ("说", "shuō", "to speak, to say", "讠 (speech) on the left."),
   ("听", "tīng", "to listen, to hear", "口 (mouth) on the left and 斤 on the right. 说 is the speaking side, 听 is the listening side."),
  ], [("去中国", "qù Zhōngguó", "go to China"), ("你来", "nǐ lái", "you come"), ("看山", "kàn shān", "look at the mountain"),
      ("我说", "wǒ shuō", "I say"), ("好听", "hǎotīng", "pleasant to hear"), ("好看", "hǎokàn", "good-looking"),
      ("不说", "bù shuō", "not say")]),
 ("verbs2", "Buy, do, want, write, read", [
   "Five more verbs. 想 (xiǎng) is both 'to want' and 'to think': 想吃 is 'want to eat'.",
   "Reading pinyin: 'mǎi' is 'my'. 'zuò' is close to 'dzwaw'. 'xiǎng' is close to 'shyahng'. 'xiě' is close to 'shyeh'. 'dú' is 'doo'.",
   "买 (buy) and 卖 (sell, not taught yet) differ by one stroke on top. Keep them apart: the extra stroke is what you give away.",
  ], [
   ("买", "mǎi", "to buy", "Compare 卖 (mài, sell): the seller has one more stroke on top."),
   ("做", "zuò", "to do, to make", "亻 (person) on the left: a person doing something."),
   ("想", "xiǎng", "to want, to think", "心 (heart) at the bottom: what the heart wants and thinks."),
   ("写", "xiě", "to write", "A cover on top of a base, like a brush resting over a page."),
   ("读", "dú", "to read", "讠 (speech) on the left: reading aloud."),
  ], [("想吃", "xiǎng chī", "want to eat"), ("想喝", "xiǎng hē", "want to drink"), ("想去", "xiǎng qù", "want to go"),
      ("想买", "xiǎng mǎi", "want to buy"), ("想看", "xiǎng kàn", "want to see"), ("买菜", "mǎi cài", "buy groceries"),
      ("不想去", "bù xiǎng qù", "don't want to go"), ("做饭", "zuòfàn", "cook")]),
 ("time1", "Days and years", [
   "Time words follow a pattern. 今 is this, 明 is next, 昨 is last: 今天 today, 明天 tomorrow, 昨天 yesterday.",
   "Reading pinyin: 'nián' is close to 'nyen'. 'tiān' is close to 'tyen'. 'jīn' is 'jin'. 'míng' is 'ming'. 'zuó' is close to 'dzwaw'.",
   "明 is a sun 日 and a moon 月 side by side: bright, then 'next', as in 明天.",
  ], [
   ("年", "nián", "year", "A long vertical stroke through the middle, like a stalk of grain: one harvest, one year."),
   ("天", "tiān", "day, sky", "大 (big) with a line over its head: the big sky above a person."),
   ("今", "jīn", "now, this", "A roof over a mark: this very moment."),
   ("明", "míng", "bright, next", "日 (sun) and 月 (moon) side by side: bright. Also 'next', as in 明天."),
   ("昨", "zuó", "yesterday, past", "日 (sun, day) on the left: a day that has gone."),
  ], [("今天", "jīntiān", "today"), ("明天", "míngtiān", "tomorrow"), ("昨天", "zuótiān", "yesterday"),
      ("今年", "jīnnián", "this year"), ("明年", "míngnián", "next year"), ("去年", "qùnián", "last year"),
      ("天天", "tiāntiān", "every day")]),
 ("time2", "Parts of the day", [
   "Words to say when. 上 is up and also 'before': 上午 is morning. 下 is down and also 'after': 下午 is afternoon.",
   "To say the time, put the number before 点: 三点 is three o'clock. 分 is the minute: 五分 is five minutes.",
   "Reading pinyin: 'shàng' is 'shahng'. 'xià' is close to 'shyah'. 'wǔ' is 'woo'. 'diǎn' is close to 'dyen'. 'fēn' is 'fun'.",
  ], [
   ("上", "shàng", "up, above, before", "A short line above a long one: something on top."),
   ("下", "xià", "down, below, after", "The reverse of 上: a short mark under a long line."),
   ("午", "wǔ", "noon", "The middle of the day. 中午 means 'the middle of the day': noon."),
   ("点", "diǎn", "o'clock, a dot", "Small dots underneath, like the dots on a clock face."),
   ("分", "fēn", "minute, to divide", "八 (split) above 刀 (knife): to cut apart, a minute."),
  ], [("上午", "shàngwǔ", "morning"), ("下午", "xiàwǔ", "afternoon"), ("中午", "zhōngwǔ", "noon"),
      ("三点", "sān diǎn", "three o'clock"), ("十点", "shí diǎn", "ten o'clock"), ("五分", "wǔ fēn", "five minutes"),
      ("上山", "shàng shān", "go up the mountain"), ("下山", "xià shān", "go down the mountain")]),
 ("colours_amounts", "Colours and amounts", [
   "Two colours and two amounts, plus one more colour.",
   "Reading pinyin: 'hóng' is close to 'hoong'. 'bái' is 'by'. 'hēi' is 'hay'. 'duō' is 'dwaw'. 'shǎo' is 'shao' as in 'now'.",
   "多 is two 夕 (evening) stacked up, and it means many. 少 is 小 (small) with one more stroke, and it means few.",
  ], [
   ("红", "hóng", "red", "纟 (silk) on the left: red silk, a lucky colour."),
   ("白", "bái", "white", "A sun 日 with a small stroke on top, like the first white ray of dawn."),
   ("黑", "hēi", "black", "Four dots (fire) underneath: soot-black."),
   ("多", "duō", "many, much", "Two 夕 stacked: evening after evening, many of them."),
   ("少", "shǎo", "few, little", "小 (small) with one stroke through it: a small amount."),
  ], [("白天", "báitiān", "daytime"), ("黑白", "hēibái", "black and white"), ("多少", "duōshao", "how many, how much"),
      ("不多", "bù duō", "not many"), ("不少", "bù shǎo", "quite a few"), ("多大", "duō dà", "how big, how old"),
      ("多吃", "duō chī", "eat more"), ("少吃", "shǎo chī", "eat less"), ("多喝水", "duō hē shuǐ", "drink more water")]),
 ("directions", "Directions and cities", [
   "The four compass points, and 京 (capital) to build city names with.",
   "北京 (Běijīng) is 'northern capital', 南京 (Nánjīng) is 'southern capital', and 东京 (Dōngjīng) is Tokyo, 'eastern capital'.",
   "Reading pinyin: 'dōng' is 'doong'. 'xī' is 'shee'. 'nán' is 'nahn'. 'běi' is 'bay'. 'jīng' is 'jing'.",
   "东西 (dōngxi) means east and west, and also 'thing': you may be asked to buy 东西.",
  ], [
   ("东", "dōng", "east", "Where the sun rises."),
   ("西", "xī", "west", "Where the sun sets."),
   ("南", "nán", "south", "A frame with a cross inside, like a house with a south-facing door."),
   ("北", "běi", "north", "Two people standing back to back: turning their backs to the south."),
   ("京", "jīng", "capital city", "A tall building with a roof: the great city, the capital."),
  ], [("北京", "Běijīng", "Beijing"), ("东京", "Dōngjīng", "Tokyo"), ("南京", "Nánjīng", "Nanjing"),
      ("东西", "dōngxi", "thing, stuff"), ("南北", "nánběi", "north and south"), ("东南", "dōngnán", "southeast"),
      ("东北", "dōngběi", "northeast")]),
 ("qualities", "Tall, long, new, very", [
   "Five words for describing things. 很 (hěn) is 'very' and you will use it all the time: 很好 is 'very good'.",
   "In Mandarin, adjectives come right after 很, with no word for 'is': 我很好 is 'I am well'.",
   "Reading pinyin: 'gāo' is 'gow' as in 'cow'. 'cháng' is 'chahng'. 'xīn' is 'sheen'. 'tài' is 'tie'. 'hěn' is close to 'hun'.",
  ], [
   ("高", "gāo", "tall, high", "A tall tower with a doorway below."),
   ("长", "cháng", "long", "A long, flowing line, like long hair."),
   ("新", "xīn", "new", "斤 (axe) on the right: fresh wood just cut."),
   ("太", "tài", "too, extremely", "大 (big) with an extra dot: too big."),
   ("很", "hěn", "very", "彳 (step) on the left. It shows up in almost every sentence with an adjective."),
  ], [("很好", "hěn hǎo", "very good"), ("很大", "hěn dà", "very big"), ("很多", "hěn duō", "very many"),
      ("很高", "hěn gāo", "very tall"), ("很长", "hěn cháng", "very long"), ("太大", "tài dà", "too big"),
      ("太小", "tài xiǎo", "too small"), ("太多", "tài duō", "too many"), ("不太好", "bú tài hǎo", "not very good"),
      ("新年", "xīnnián", "New Year"), ("高山", "gāoshān", "high mountain")]),
 ("this_that", "This, that, a book", [
   "这 (this) and 那 (that) point at things. 个 (gè) and 本 (běn) are measure words: Mandarin counts things with a small word in between.",
   "一个人 is 'one person'. 一本书 is 'one book'. 个 is the all-purpose measure word. 本 is for books.",
   "Reading pinyin: 'zhè' is close to 'juh'. 'nà' is 'nah'. 'gè' is close to 'guh'. 'shū' is 'shoo'. 'běn' is close to 'bun'.",
   "Careful with 一: before a falling tone it flips to rising (一个 is 'yí gè'), and before the other tones it falls (一本 is 'yì běn').",
  ], [
   ("这", "zhè", "this", "辶 (walk) at the bottom left: here, where you walk. Say 'juh' with a fall."),
   ("那", "nà", "that", "The partner of 这: this is here, that is over there. Say 'nah' with a fall."),
   ("个", "gè", "(measure word)", "A person 人 with a stroke: used to count people and many things."),
   ("书", "shū", "book", "Simplified from 書, which has a brush in it: books are written with a brush."),
   ("本", "běn", "(for books), root", "木 (tree) with a mark at the root: the root, and the word for counting books."),
  ], [("这个", "zhège", "this one"), ("那个", "nàge", "that one"), ("这是书", "zhè shì shū", "this is a book"),
      ("那是书", "nà shì shū", "that is a book"), ("这本书", "zhè běn shū", "this book"), ("一本书", "yì běn shū", "one book"),
      ("一个人", "yí gè rén", "one person"), ("三个人", "sān gè rén", "three people"), ("好书", "hǎo shū", "a good book")]),
 ("questions", "Question words", [
   "Question words take the place of the answer. 你是谁? 'Who are you?' is just 你是 with 谁 where the name goes. There is no need to rearrange the sentence.",
   "What: 什么. Who: 谁. Which or where: 哪. Add 里 to 哪 for 'where': 哪里.",
   "Reading pinyin: 'shén' is close to 'shun'. 'me' is light. 'shéi' is 'shay'. 'nǎ' is 'nah'. 'lǐ' is 'lee'.",
  ], [
   ("什", "shén", "what (in 什么)", "亻 (person) on the left and 十 on the right. Used with 么 to ask 'what'."),
   ("么", "me", "(in 什么)", "A small hooked shape. It never stands alone, and is always light and short."),
   ("谁", "shéi", "who", "讠 (speech) on the left: asking about a person."),
   ("哪", "nǎ", "which, where", "口 (mouth) on the left: a mouth asking a question."),
   ("里", "lǐ", "inside, in", "田 (field) above 土 (earth): inside the land. In 哪里 it is light."),
  ], [("什么", "shénme", "what"), ("哪里", "nǎlǐ", "where"), ("哪国", "nǎ guó", "which country"),
      ("你是谁", "nǐ shì shéi", "who are you"), ("他是谁", "tā shì shéi", "who is he"),
      ("这是什么", "zhè shì shénme", "what is this"), ("你吃什么", "nǐ chī shénme", "what do you eat"),
      ("你想吃什么", "nǐ xiǎng chī shénme", "what do you want to eat"), ("你想去哪里", "nǐ xiǎng qù nǎlǐ", "where do you want to go")]),
]

FIRST_ID = 31   # existing zh_hanzi cards use ids 1 to 30

def flat():
    """(card id, hanzi, pinyin, meaning, hint, unit id) in teaching order."""
    out, n = [], FIRST_ID - 1
    for uid, title, intro, chars, words in UNITS:
        for hanzi, pinyin, meaning, hint in chars:
            n += 1
            out.append((str(n), hanzi, pinyin, meaning, hint + ' ' + TONES[tone_of(pinyin)], uid))
    return out
