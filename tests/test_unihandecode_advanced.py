from unihandecode import Unihandecoder


def test_long_japanese_text():

    case = "日本国民は、正当に選挙された国会における代表者を通じて行動し、われらとわれらの子孫のために、" \
           "諸国民との協和による成果と、わが国全土にわたつて自由のもたらす恵沢を確保し、政府の行為によつて" \
           "再び戦争の惨禍が起ることのないやうにすることを決意し、ここに主権が国民に存することを宣言し、" \
           "この憲法を確定する。そもそも国政は、国民の厳粛な信託によるものであつて、その権威は国民に由来し、" \
           "その権力は国民の代表者がこれを行使し、その福利は国民がこれを享受する。これは人類普遍の原理であり、" \
           "この憲法は、かかる原理に基くものである。われらは、これに反する一切の憲法、法令及び詔勅を排除する。"
    expected = "nihonkokumin ha, seitou ni senkyo sareta kokkai niokeru daihyousha wo tsuuji te koudou shi, " \
               "wareratowarerano shison notameni, shokokumin tono kyouwa niyoru seika to, " \
               "waga kuni zendo niwatatsute jiyuu nomotarasu keitaku wo kakuho shi, " \
               "seifu no koui niyotsute futatabi sensou no sanka ga okoru kotononaiyaunisurukotowo ketsui shi, " \
               "kokoni shuken ga kokumin ni sonsu rukotowo sengen shi, kono kenpou wo kakuteisu ru. " \
               "somosomo kokusei ha, kokumin no genshuku na shintaku niyorumonodeatsute, " \
               "sono ken'i ha kokumin ni yurai shi, sono kenryoku ha kokumin no daihyousha gakorewo koushi shi, " \
               "sono fukuri ha kokumin gakorewo kyouju suru. koreha jinruifuhen no genri deari, " \
               "kono kenpou ha, kakaru genri ni motozuku monodearu. wareraha, " \
               "koreni hansu ru issai no kenpou, hourei oyobi shouchoku wo haijo suru."

    u = Unihandecoder(lang="ja")
    assert u.decode(case) == expected
