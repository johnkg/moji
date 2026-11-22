"""Everyday sentences for the speaking paths, Japanese and Mandarin.

One source for both the flashcard decks (gen_decks.py) and the lessons
(gen_lessons.py). Each unit is (id, title, intro paragraphs, rows) and each row is
(native text, reading, meaning, hint). Cards get ids "1", "2", ... in order.
"""

JA = [
 ("about_you", "About you", [
   "Sentences you can use the first minute you meet someone.",
   "In Japanese the verb or ending comes last. 'Watashi wa Mike desu' is word for word 'As for me, Mike is.'",
   "The character は is written 'ha' but said 'wa' when it marks the topic of a sentence. です (desu) is a polite 'am, is, are'. The u is almost silent, so say 'des'.",
  ], [
   ("はじめまして", "hajimemashite", "nice to meet you (first meeting)", "ha-ji-me-ma-shi-te. Said only the first time you meet."),
   ("わたしはマイクです", "watashi wa maiku desu", "I am Mike.", "Swap maiku for your own name. 'wa' is the particle は."),
   ("よろしくおねがいします", "yoroshiku onegaishimasu", "pleased to meet you", "yo-ro-shi-ku o-ne-gai-shi-mas. Said after your name. It is a polite 'please be kind to me'."),
   ("おなまえはなんですか", "onamae wa nan desu ka", "what is your name?", "o-na-ma-e wa nan des-ka. 'nan' means what. The 'ka' makes it a question."),
   ("アメリカからきました", "amerika kara kimashita", "I came from America.", "'kara' means from. Swap in your own country. ki-ma-shi-ta."),
  ]),
 ("questions", "What and where", [
   "Three little words carry most simple questions: nan (what), doko (where) and ikura (how much).",
   "Add 'desu ka' to the end and you have a polite question. Your voice does not need to rise.",
   "Kore means this, sore means that (near you), are means that over there.",
  ], [
   ("これはなんですか", "kore wa nan desu ka", "what is this?", "ko-re wa nan des-ka. Point at something as you say it."),
   ("それはほんです", "sore wa hon desu", "that is a book.", "so-re wa hon des. Swap hon for any noun."),
   ("トイレはどこですか", "toire wa doko desu ka", "where is the toilet?", "toi-re wa do-ko des-ka. One of the most useful sentences you can learn."),
   ("これはいくらですか", "kore wa ikura desu ka", "how much is this?", "ko-re wa i-ku-ra des-ka. Point at the item."),
   ("はい、そうです", "hai, sou desu", "yes, that's right.", "hai, soh des. 'sou' is a long 'oh'."),
  ]),
 ("who_when", "Who, when, where", [
   "More question words: dare (who), nanji (what time), nanyoubi (what day of the week).",
   "The same ending 'desu ka' makes all of them questions.",
  ], [
   ("だれですか", "dare desu ka", "who is it?", "da-re des-ka. The r is a quick tap of the tongue."),
   ("いまなんじですか", "ima nanji desu ka", "what time is it now?", "i-ma nan-ji des-ka. 'ima' means now."),
   ("きょうはなんようびですか", "kyou wa nanyoubi desu ka", "what day is it today?", "kyoh wa nan-yoh-bi des-ka. 'kyou' is today."),
   ("あしたはにちようびです", "ashita wa nichiyoubi desu", "tomorrow is Sunday.", "a-shi-ta wa ni-chi-yoh-bi des. Swap in any day."),
   ("ここです", "koko desu", "it's here.", "ko-ko des. Short and useful when you point."),
  ]),
 ("wants", "Wants and needs", [
   "To ask for something, say what you want, then を (said 'o'), then 'kudasai' (please give me).",
   "The character を is only used as this marker, and it sounds just like お.",
   "Feelings like hungry and thirsty use 'ga' and a past form: onaka ga sukimashita, 'my stomach has emptied'.",
  ], [
   ("みずをください", "mizu o kudasai", "water, please.", "mi-zu o ku-da-sai. Swap mizu for what you want."),
   ("これをください", "kore o kudasai", "I'll take this, please.", "ko-re o ku-da-sai. Point at the item."),
   ("コーヒーをおねがいします", "koohii o onegaishimasu", "coffee, please.", "koh-hee o o-ne-gai-shi-mas. The long vowels are held for two beats."),
   ("おなかがすきました", "onaka ga sukimashita", "I'm hungry.", "o-na-ka ga su-ki-ma-shi-ta."),
   ("のどがかわきました", "nodo ga kawakimashita", "I'm thirsty.", "no-do ga ka-wa-ki-ma-shi-ta."),
  ]),
 ("eating", "Eating out", [
   "Two phrases are said at every meal: before you eat and after.",
   "They are not translated word for word. Think of them as 'thanks for the food' and 'thanks, that was a feast'.",
  ], [
   ("メニューをください", "menyuu o kudasai", "the menu, please.", "me-nyuu o ku-da-sai."),
   ("いただきます", "itadakimasu", "thanks for the food (said before eating)", "i-ta-da-ki-ma-su. Hands together, a small bow."),
   ("ごちそうさまでした", "gochisousama deshita", "thanks for the meal (said after eating)", "go-chi-soh-sa-ma de-shi-ta. Say it to the cook when you leave."),
   ("おかいけいをおねがいします", "okaikei o onegaishimasu", "the bill, please.", "o-kai-kei o o-ne-gai-shi-mas."),
   ("おいしかったです", "oishikatta desu", "it was delicious.", "oi-shi-kat-ta des. The small 'tt' is a held beat."),
  ]),
 ("around", "Getting around", [
   "Directions use a short list of words: massugu (straight), migi (right), hidari (left).",
   "Add 'kudasai' to turn an instruction into a polite request.",
  ], [
   ("えきはどこですか", "eki wa doko desu ka", "where is the station?", "e-ki wa do-ko des-ka. The most useful place word in Japan."),
   ("まっすぐいってください", "massugu itte kudasai", "please go straight.", "mas-su-gu it-te ku-da-sai. Small tsu: a held beat before the next sound."),
   ("ひだりにまがってください", "hidari ni magatte kudasai", "please turn left.", "hi-da-ri ni ma-gat-te ku-da-sai. Swap hidari for migi to say right."),
   ("ここでとめてください", "koko de tomete kudasai", "please stop here.", "ko-ko de to-me-te ku-da-sai. Handy in a taxi."),
   ("みちにまよいました", "michi ni mayoimashita", "I'm lost.", "mi-chi ni ma-yoi-ma-shi-ta."),
  ]),
 ("understanding", "Understanding and help", [
   "You will not catch everything. These sentences keep a conversation alive.",
   "Asking for slower or repeated speech is polite and normal.",
  ], [
   ("もういちどおねがいします", "mou ichido onegaishimasu", "once more, please.", "moh i-chi-do o-ne-gai-shi-mas."),
   ("ゆっくりおねがいします", "yukkuri onegaishimasu", "slowly, please.", "yuk-ku-ri o-ne-gai-shi-mas."),
   ("えいごがわかりますか", "eigo ga wakarimasu ka", "do you understand English?", "ei-go ga wa-ka-ri-mas-ka."),
   ("にほんごがすこしはなせます", "nihongo ga sukoshi hanasemasu", "I can speak a little Japanese.", "ni-hon-go ga su-ko-shi ha-na-se-mas."),
   ("たすけてください", "tasukete kudasai", "please help me.", "ta-su-ke-te ku-da-sai."),
   ("だいじょうぶです", "daijoubu desu", "it's okay, I'm fine.", "dai-joh-bu des. Also a polite no-thanks."),
  ]),
 ("everyday", "Everyday talk", [
   "Small talk you will hear all the time.",
   "'Ogenki desu ka' asks how someone is. The honest answer is usually 'genki desu', I'm well.",
  ], [
   ("おげんきですか", "ogenki desu ka", "how are you?", "o-gen-ki des-ka."),
   ("げんきです、ありがとう", "genki desu, arigatou", "I'm fine, thank you.", "gen-ki des, a-ri-ga-toh."),
   ("おやすみなさい", "oyasuminasai", "good night.", "o-ya-su-mi-na-sai."),
   ("たのしかったです", "tanoshikatta desu", "it was fun.", "ta-no-shi-kat-ta des."),
   ("またあした", "mata ashita", "see you tomorrow.", "ma-ta a-shi-ta. Casual."),
  ]),
]

ZH = [
 ("about_you", "About you", [
   "Sentences you can use the first minute you meet someone.",
   "Mandarin word order is close to English: 'I am American' is wǒ shì Měiguó rén, word for word 'I am America person'.",
   "Say each sentence with its tones. The tone marks in the pinyin show how the voice moves.",
  ], [
   ("很高兴认识你", "hěn gāoxìng rènshi nǐ", "nice to meet you", "Close to 'hun gow-shing run-shr nee'. Said when you first meet."),
   ("我叫马克", "wǒ jiào Mǎkè", "my name is Mark.", "Close to 'waw jyow Mah-kuh'. Swap in your own name."),
   ("你叫什么名字", "nǐ jiào shénme míngzi", "what is your name?", "Close to 'nee jyow shun-muh ming-dzuh'."),
   ("我是美国人", "wǒ shì Měiguó rén", "I am American.", "Close to 'waw shr May-gwaw run'. Swap in your own country."),
   ("你是哪国人", "nǐ shì nǎ guó rén", "which country are you from?", "Close to 'nee shr nah gwaw run'. nǎ means which."),
  ]),
 ("questions", "What and where", [
   "Three words carry many simple questions: shénme (what), nǎlǐ (where), duōshao qián (how much).",
   "To ask 'is it so?', add 吗 (ma) to the end of a statement.",
   "Zhè is this, nà is that.",
  ], [
   ("这是什么", "zhè shì shénme", "what is this?", "Close to 'juh shr shun-muh'. Point at something as you say it."),
   ("那是书", "nà shì shū", "that is a book.", "Close to 'nah shr shoo'. Swap shū for any noun."),
   ("厕所在哪里", "cèsuǒ zài nǎlǐ", "where is the toilet?", "Close to 'tsuh-swaw dzai nah-lee'. One of the most useful sentences."),
   ("这个多少钱", "zhège duōshao qián", "how much is this?", "Close to 'juh-guh dwaw-shao chyen'. Point at the item."),
   ("对，是的", "duì, shì de", "yes, that's right.", "Close to 'dway, shr duh'."),
  ]),
 ("who_when", "Who, when, where", [
   "More question words: shéi (who), jǐ diǎn (what time), xīngqī jǐ (what day).",
   "For time, jǐ is 'how many' and diǎn is 'o'clock'.",
  ], [
   ("他是谁", "tā shì shéi", "who is he?", "Close to 'tah shr shay'."),
   ("现在几点", "xiànzài jǐ diǎn", "what time is it now?", "Close to 'shyen-dzai jee dyen'."),
   ("今天星期几", "jīntiān xīngqī jǐ", "what day is it today?", "Close to 'jin-tyen shing-chee jee'."),
   ("明天是星期日", "míngtiān shì xīngqīrì", "tomorrow is Sunday.", "Close to 'ming-tyen shr shing-chee-r'. Swap in any day."),
   ("我在这里", "wǒ zài zhèlǐ", "I'm here.", "Close to 'waw dzai juh-lee'."),
  ]),
 ("wants", "Wants and needs", [
   "To ask for something, say 'wǒ yào' (I want) and the thing, or 'qǐng gěi wǒ' (please give me).",
   "To say you are hungry or thirsty, add 了 (le) at the end: wǒ è le.",
  ], [
   ("我要水", "wǒ yào shuǐ", "I want water.", "Close to 'waw yow shway'. Swap shuǐ for what you want."),
   ("我要这个", "wǒ yào zhège", "I'll take this one.", "Close to 'waw yow juh-guh'. Point at the item."),
   ("请给我咖啡", "qǐng gěi wǒ kāfēi", "coffee, please.", "Close to 'ching gay waw kah-fay'."),
   ("我饿了", "wǒ è le", "I'm hungry.", "Close to 'waw uh luh'."),
   ("我渴了", "wǒ kě le", "I'm thirsty.", "Close to 'waw kuh luh'."),
  ]),
 ("eating", "Eating out", [
   "Phrases for ordering and paying.",
   "Spicy food is common in much of China. 不要辣 is a useful way to ask for none.",
  ], [
   ("请给我菜单", "qǐng gěi wǒ càidān", "the menu, please.", "Close to 'ching gay waw tsai-dan'."),
   ("我想吃面条", "wǒ xiǎng chī miàntiáo", "I'd like to eat noodles.", "Close to 'waw shyang chr myen-tyow'. xiǎng means would like."),
   ("很好吃", "hěn hǎochī", "it's delicious.", "Close to 'hun how-chr'."),
   ("买单", "mǎidān", "the bill, please.", "Close to 'my-dan'. Say it to the waiter."),
   ("不要辣", "bú yào là", "no spice, please.", "Close to 'boo yow lah'."),
  ]),
 ("around", "Getting around", [
   "Directions use a short list of words: yìzhí zǒu (straight), zuǒ (left), yòu (right).",
   "Zhuǎn means turn. Put the direction first: zuǒ zhuǎn, left turn.",
  ], [
   ("地铁站在哪里", "dìtiězhàn zài nǎlǐ", "where is the subway station?", "Close to 'dee-tyeh-jan dzai nah-lee'."),
   ("一直走", "yìzhí zǒu", "go straight.", "Close to 'ee-jr dzoh'."),
   ("左转", "zuǒ zhuǎn", "turn left.", "Close to 'dzwaw jwan'. Swap in yòu (yoh) to say right."),
   ("请停在这里", "qǐng tíng zài zhèlǐ", "please stop here.", "Close to 'ching ting dzai juh-lee'. Handy in a taxi."),
   ("我迷路了", "wǒ mílù le", "I'm lost.", "Close to 'waw mee-loo luh'."),
  ]),
 ("understanding", "Understanding and help", [
   "You will not catch everything. These sentences keep a conversation alive.",
   "Asking someone to speak slower or repeat is polite and normal.",
  ], [
   ("请再说一遍", "qǐng zài shuō yí biàn", "please say it once more.", "Close to 'ching dzai shwaw ee byen'."),
   ("请说慢一点", "qǐng shuō màn yìdiǎn", "please speak a little slower.", "Close to 'ching shwaw man ee-dyen'."),
   ("你会说英语吗", "nǐ huì shuō Yīngyǔ ma", "do you speak English?", "Close to 'nee hway shwaw Ying-yoo ma'."),
   ("我会说一点中文", "wǒ huì shuō yìdiǎn Zhōngwén", "I can speak a little Chinese.", "Close to 'waw hway shwaw ee-dyen Jong-wun'."),
   ("请帮帮我", "qǐng bāngbang wǒ", "please help me.", "Close to 'ching bahng-bahng waw'."),
   ("没问题", "méi wèntí", "no problem.", "Close to 'may wun-tee'."),
  ]),
 ("everyday", "Everyday talk", [
   "Small talk you will hear all the time.",
   "你好吗 asks how someone is. A common answer is 我很好, I'm very well.",
  ], [
   ("你好吗", "nǐ hǎo ma", "how are you?", "Close to 'nee how ma'."),
   ("我很好，谢谢", "wǒ hěn hǎo, xièxie", "I'm fine, thank you.", "Close to 'waw hun how, shyeh-shyeh'."),
   ("晚安", "wǎn'ān", "good night.", "Close to 'wan-an'."),
   ("玩得很开心", "wán de hěn kāixīn", "I had a great time.", "Close to 'wan duh hun kai-shin'."),
   ("明天见", "míngtiān jiàn", "see you tomorrow.", "Close to 'ming-tyen jyen'."),
  ]),
]

def flat(units):
    """All rows in order, with card ids '1', '2', ... shared by deck and lessons."""
    out, n = [], 0
    for uid, title, intro, rows in units:
        for text, reading, meaning, hint in rows:
            n += 1
            out.append((str(n), text, reading, meaning, hint, uid))
    return out
