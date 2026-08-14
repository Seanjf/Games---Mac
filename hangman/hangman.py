
# 06 Aug 2026 @ 2142

import tkinter as tk
from tkinter import font as tkfont
import atexit
import math
import os
import platform
import random
import re
import shutil
import struct
import subprocess
import tempfile
import threading
import wave


class SoundPlayer:
    """Synthesizes and plays short WAV sound effects with no external assets."""

    SAMPLE_RATE = 44100

    def __init__(self):
        self.enabled = True
        self.sounds = {}
        try:
            self._tmp_dir = tempfile.mkdtemp(prefix="hangman_sfx_")
            atexit.register(shutil.rmtree, self._tmp_dir, ignore_errors=True)
            self.sounds = {
                "correct": self._build("correct.wav", [(880, 0.07), (1174, 0.09)]),
                "wrong":   self._build("wrong.wav",   [(180, 0.18)]),
                "win":     self._build("win.wav",     [(523, 0.12), (659, 0.12), (784, 0.12), (1046, 0.22)]),
                "lose":    self._build("lose.wav",    [(392, 0.18), (330, 0.18), (262, 0.28)]),
            }
        except Exception:
            self.enabled = False

    def _tone(self, frequency, duration, volume=0.4):
        frame_count = int(self.SAMPLE_RATE * duration)
        fade = max(1, int(frame_count * 0.1))
        frames = bytearray()
        for i in range(frame_count):
            envelope = min(i / fade, 1.0, (frame_count - i) / fade)
            sample = volume * envelope * math.sin(2 * math.pi * frequency * i / self.SAMPLE_RATE)
            frames += struct.pack("<h", int(sample * 32767))
        return frames

    def _build(self, filename, notes):
        path = os.path.join(self._tmp_dir, filename)
        samples = bytearray()
        for frequency, duration in notes:
            samples += self._tone(frequency, duration)
        with wave.open(path, "w") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(self.SAMPLE_RATE)
            wav_file.writeframes(bytes(samples))
        return path

    def play(self, name):
        if not self.enabled:
            return
        path = self.sounds.get(name)
        if not path:
            return
        threading.Thread(target=self._play_file, args=(path,), daemon=True).start()

    def _play_file(self, path):
        try:
            system = platform.system()
            if system == "Darwin":
                subprocess.run(["afplay", path], check=False,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            elif system == "Windows":
                import winsound
                winsound.PlaySound(path, winsound.SND_FILENAME)
            else:
                for player in ("paplay", "aplay"):
                    try:
                        subprocess.run([player, path], check=False,
                                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        break
                    except FileNotFoundError:
                        continue
        except Exception:
            pass


class HangmanGame:

    HOW_TO_PLAY_TEXT = (
        "How to Play\n\n"
        "- A secret word from the topic shown is hidden behind blanks.\n"
        "- Click a letter below, or type it on your keyboard, to guess.\n"
        "- Correct letters turn green and fill in the word.\n"
        "- Wrong letters turn red and add a piece to the drawing.\n"
        "- You have 13 wrong guesses before the game ends.\n"
        "- Guess every letter before the drawing is complete to win!"
    )

    def __init__(self, master):
        self.master = master
        self.sound_player = SoundPlayer()

        self.master.title("Hangman Game")
        self.master.configure(bg='oldlace')
        self.master.geometry("1150x950")
        self.master.update_idletasks()
        #self.master.resizable(False, False)

        Animals = 'ant baboon badger bat bear beaver bison buffalo  bull camel cat clam cobra cougar cow coyote \
            crow deer dog donkey duck eagle elephant ferret fox frog giraffe goat goose hawk horse kangaroo \
            lamb lion lizard llama mole monkey moose mouse mule newt otter owl panda parrot pigeon python rabbit \
            ram rat raven rhinoceros salmon seal shark sheep skunk sloth snake spider stork swan tiger \
            toad trout turkey turtle weasel whale wolf wombat zebra'.split()

        Countries = 'andorra argentina australia austria belgium bermuda bolivia brazil bulgaria cambodia \
            canada chile china denmark egypt england  estonia finland france germany greece  greenland iceland india indonesia \
            iran ireland israel italy jamaica japan latvia liechtenstein  luxembourg lithuania malaysia mexico \
            netherlands panama peru portugal poland  romania scotland singapore spain sweden  switzerland tahiti \
            thailand turkey ukraine vietnam wales'.split()

        Places = 'aberdeen aberystwyth   adelaide amsterdam antwerp athens barcelona basle belfast belgrade \
            berlin birmingham bordeaux bremen brisbane brussels budapest cairns calais canberra cardiff \
            casablanca cologne copenhagen darwin dortmund dubai dublin dover edinburgh frankfurt galway glasgow \
            gorey  granada hamburg hannover helsinki hull istanbul jakarta kilkenny  krakow kyiv \
            leeds limerick lisbon liverpool  \
            london madrid manchester marseille melbourne montreal munich naples nottingham oslo paris perth pisa \
            prague riga rome rotterdam sheffield stockholm sydney tallinn toronto vancouver vienna volga warsaw \
            wellington wexford '.split()


        Rivers = 'amazon clyde congo danube don elbe euphrates fraser geylang hudson kallang kasai kwango lena \
            liffey limpopo loire mackenzie majorqaq maritsa mekong mersey mississippi missouri nile ob oder \
            okavango orange po poe putumayo shannon singapore slave rhine rhone  seine shebelle tagus thames \
            tigris ubangii umgeni volga volta yangtze yellow zambezi'.split()

        Sports = 'archery athletics badminton baseball basketball boxing bowling canoeing cricket cycling \
            diving fencing football golf gymnastics handball hockey judo karate  netball racquetball rowing \
            rugby running sailing  soccer softball skiing surfing squash swimming table-tennis taekwondo tennis \
            volleyball  wrestling'.split()

        Miscellaneous = 'aeroplane animal antidisestablishmentarianism apple banana bicycle blue book boy  bus \
            car chemistry child circle class code computer continent country doctor engine equation flute \
            geography girl grocery guitar harp heaven hospital insurance insurrection machine man mathematics \
            motor music nurse ocean orange orient piano player police purple railway rectangle revolution river \
            rocket  school science scooter ship space square teacher university water woman  word yacht '.split()




        self.comments  =  {
              'amazon'       : '''Rising in Peru, the Amazon 6,575 km (4,086 mi) long,
                                  flows through Colombia and Brazil before discharging
                                  into the Atlantic ocean.

                                  It is the second-longest river system in the world,
                                  and is the largest river in the world measured by
                                  the discharge volume of water.''',

              'clyde'        : '''The Clyde is the third longest river in Scotland.

                                  During the 19th and 20th Centuries it was the world's
                                  pre-eminent centre of marine engineering and shipbuilding.''',

              'congo'        : '''The Congo River, formerly also known as the Zaire River,
                                  is the second-longest river in Africa,

                                  The Congo–Lualaba–Luvua–Luapula–Chambeshi River system
                                  has an overall length of 4,700 km (2,900 mi),
                                  which makes it the world's ninth-longest river.

                                  It is the only major river to cross the equator twice.''',

              'danube'       : '''The Danube is the second-longest river in Europe.
                                  It flows from Germany's Black Forest to the Black Sea,
                                  and is linked to the North Sea via the Rhine–Main–Danube Canal.

                                  In ancient times it was an important trade route, and was the
                                  northern frontier of the Roman Empire.  It is now an important source of hydropower.''',

              'don'          : '''There are two rivers named Don.

                                  The Russian Don, the fifth-longest river in Europe was viewed as the border between Europe and Asia by
                                  some ancient Greek geographers, and was a major trading route .
                                  The Don connects to the River Volga via the Volga–Don Canal.\n\n

                                  The English Don, in Yorkshire, is often described by the structures
                                  built to restrct its passage.

                                  Its upper reaches are defined by dams built to provide a public water supply.  Its middle part
                                  by weirs built to supply mills, foundries, and factories with water power, and its lower part
                                  by weirs and locks to maintain water levels for navigation. ''',

              'elbe'         : '''The Elbe, one of the major rivers of Central Europe, rises in
                                  the Giant Mountains of the northern Czech Republic, and flows through much of
                                  Bohemia and Germany before flowing into the North Sea.''',

              'euphrates'    : '''The Euphrates originates in Turkey, flows through Syria and Iraq to join
                                  the Tigris in the Shatt al-Arab in Iraq, which empties into the Persian Gulf.

                                  It is of historical importance because together with the Tigris, it
                                  defines the region of Mesopotamia which is recognised as the cradle of some
                                  of the world's earliest civilizations and the site of the earliest developments
                                  of the Neolithic Revolution from around 10,000 BC.

                                  It has been identified as having inspired some of the most important
                                  developments in human history, including the invention of the wheel,
                                  the planting of the first cereal crops, the development of cursive script,
                                  mathematics, astronomy, and agriculture.''',

              'fraser'       : '''The Fraser River is the longest river within British Columbia, Canada.''',

              'geylang'      : '''The Geylang River is a canalised river in Singapore.

                                  A 2-year (2012-2014) revitalisation transformed the former concrete canal
                                  into an attractive and community-friendly waterway.''',

              'hudson'       : '''The Hudson River is one of the most iconic rivers in the United States,
                                  flowing through New York State and into the Atlantic Ocean.

                                  It has played a significant role in American history, commerce,
                                  and environmental conservation.''',

              'kallang'      : '''The Kallang River, the longest river in Singapore, used to empty
                                  into the Singapore Straits, but following extensive land reclamation along
                                  Singapore's southeastern coast, it now flows into the open sea
                                  via the Marina Channel.''',

              'kasai'        : '''The Kasai River is one of the largest and most important tributaries of
                                  the Congo River system. It plays a vital role in the hydrographic system
                                  of Angola and the greater Congo Basin. Its clear waters, high navigability,
                                  and rich alluvial diamond deposits make it both an economic powerhouse
                                  and an ecological corridor in Central Africa.''',

              'kwango'       : '''The Kwango, a transboundary river of Angola and the Democratic Republic of Congo,
                                  has large resources of diamonds in its basin.''',

              'lena'         : '''The Lena is the easternmost river of the three great rivers of Siberia
                                  which flow into the Arctic Ocean, the others being the Ob and the Yenisey.

                                  It is the eleventh-longest river in the world and the longest river entirely
                                  within Russia.''',

              'liffey'       : '''The River Liffey rises at Liffey Head Bog in the Wicklow Mountains, and flows
                                  through Counties Wicklow, Kildare, and Dublin, and the centre of Dublin City
                                  to its mouth within Dublin Bay. It supplies much of Dublin's water
                                  and supports a range of recreational activities.

                                  There are dams for three hydroelectric power stations along the river.''',

              'limpopo'      : '''Described by Rudyard Kipling as the "great grey-green, greasy Limpopo River,
                                  all set about with fever-trees", the Limpopo rises in South Africa and flows
                                  through Mozambique to the Indian Ocean.''',

              'loire'        : '''The Loire rises in the southeastern quarter of the French Massif Central and
                                  flows north and then west to empty in the bay of Biscay.

                                  The lower-central part of its valley was added to the list of World Heritage
                                  Sites of UNESCO in 2000. Vineyards and châteaux are found along the banks of
                                  the river throughout this section and are a major tourist attraction.

                                  The Loire Valley has been called the "Garden of France".''',

              'mackenzie'    : '''The Mackenzie River which flows through a vast, thinly populated region of
                                  forest and tundra within the Northwest Territories in Canada, forms, together
                                  with the Slave, Peace, and Finlay, the longest river system in Canada.

                                  It is the largest river flowing into the Arctic Ocean from North America, and
                                  the Mackenzie valley is believed to have been the path taken by prehistoric
                                  peoples during the initial human migration from Asia to North America over
                                  10,000 years ago.''',

              'majorqaq'     : '''The Majorqaq is a meltwater river in central-western Greenland.''',

              'maritsa'      : '''The Maritsa, known in Greek as the Evros and in Turkish as the Meriç,
                                  runs through the Balkans in Southeast Europe.  It is the main river of the
                                  historical region of Thrace.

                                  The unnavigable river is used for hydroelectric power generation and for irrigation.''',

              'mekong'       : '''The Mekong is the world\'s twelfth-longest river. From its headwaters in the
                                  Tibetan Plateau it runs through Southwest China, Myanmar, Laos, Thailand,
                                  Cambodia and southern Vietnam.

                                  The construction of hydroelectric dams along the river in the 2000s through the
                                  2020s has caused serious problems for the river\'s ecosystem, including the exacerbation
                                  of drought.  However, it remains a major trade route between Tibet and Southeast Asia.''',

              'mersey'       : '''The River Mersey, a major river in North West England, forms part of the boundary
                                  between the counties of Lancashire and Cheshire.

                                  The river gave its name to Merseybeat, developed by bands from Liverpool, notably the Beatles.''',

              'mississippi'  : '''The Mississippi River is the second-longest river in the United States.  From its
                                  source in Minnesota, it flows generally south to the Mississippi River Delta in
                                  the Gulf of Mexico.  It is a vital transportation artery and communications link.
                                  It has also been the subject of American literature, particularly in the writings
                                  of Mark Twain.

                                  During the 20th century, the Mississippi River experienced major pollution and
                                  environmental problems, most notably elevated nutrient and chemical levels from
                                  agricultural runoff, the primary contributor to the Gulf of Mexico dead zone.''',

              'missouri'     : '''The Missouri River, the longest river in the  United States of America, rises in
                                  southwestern Montana, then flows east and south to enter the Mississippi River
                                  north of St. Louis, Missouri. During the 20th century, the Missouri River basin
                                  was extensively developed for irrigation, flood control, and the generation of
                                  hydroelectric power. Fifteen dams impound the main stem of the river, with
                                  hundreds more on tributaries.''',

              'nile'         : '''The Nile, the longest river in the world, has played a central role in the
                                  environmental, economic, and cultural history of Africa for millennia.
                                  Of its two major tributaries the White Nile is the longer and is considered to
                                  be the headwaters, but the Blue Nile contributes over twice the water volume of
                                  the White.

                                  The Nile was the foundation of the Ancient Egyptian civilization, which relied
                                  on the river for nearly every aspect of life. The annual flooding of the river
                                  deposited nutrient-rich silt along the riverbanks. This soil supported crops
                                  that enabled a sophisticated society to thrive in an otherwise inhospitable
                                  desert. The Nile facilitated trade, communication, transportation, and
                                  governance.

                                  In the modern era, the Nile plays a critical role in the economies of Egypt and
                                  Sudan, which rely on it to irrigate extensive croplands.

                                  During the 20th century, more than a dozen dams have been built in the Nile
                                  Basin to provide for irrigation and to generate electricity.''',

              'ob'           : '''The Ob, a major river in Russia, with its tributary the Irtysh forms
                                  the world\'s seventh-longest river system. It is the westernmost of the three
                                  great Siberian rivers that flow into the Arctic Ocean (the other two being the
                                  Yenisei and the Lena). The main city on its banks is Novosibirsk, the largest city
                                  in Siberia, and the third-largest city in Russia. The Gulf of Ob is the world's
                                  longest estuary.''',

              'oder'         : '''The Oder, a river in Central Europe, is Poland's second-longest river and
                                  third-longest within its borders after the Vistula and its largest tributary
                                  the Warta.  The Oder rises in the Czech Republic and flows through western Poland,
                                  later forming 187 kilometres (116 mi) of the border between Poland and Germany
                                  as part of the Oder–Neisse line.  The river ultimately divides into into three
                                  branches that empty into the Bay of Pomerania of the Baltic Sea.''',

              'okavango'     : '''The Okavango River is the fourth-longest river system in southern Africa.  It begins
                                  in the sandy highlands of Angola. Farther south, it forms part of the border between
                                  Angola and Namibia, and then flows into Botswana.

                                  The Okavango does not have an outlet to the sea.  Instead, it discharges into the
                                  Okavango Delta or Okavango Alluvial Fan, in an endorheic basin in the Kalahari Desert.''',

              'orange'       : '''The Orange River is the longest river in South Africa.  Rising in the Drakensberg
                                  mountains in Lesotho it flows westwards through South Africa to the Atlantic Ocean.
                                  It forms part of the international borders between South Africa and Lesotho and between
                                  South Africa and Namibia, as well as several provincial borders within South Africa.

                                  It plays an important role in the South African economy by providing water for irrigation
                                  and hydroelectric power.''',

              'po'           : '''The Po is the longest river in Italy. It starts in the Cottian Alps and flows eastward
                                  across northern Italy through several important cities, including Turin, Piacenza, Cremona
                                  and Ferrara before ending at a delta which projects into the Adriatic Sea near Venice.
                                  It is connected to Milan through a net of channels called navigli, which Leonardo da Vinci
                                  helped design.

                                  The Po Valley was in the territory of Roman Cisalpine Gaul, divided into Cispadane Gaul (south
                                  of the Po) and Transpadane Gaul (north of the Po).''',

              'poe'          : '''The River Poe is frequently described as Ireland's shortest river.
                                  It is only about 100–120 metres (330–400 feet) long, flowing from Lough Currane
                                  into Ballinskelligs Bay near the village of Waterville.''',

              'putumayo'     : '''The Putumayo River, a tributary of the Amazon, forms part of Colombia's border with
                                  Ecuador, as well as most of the border with Peru.''',

              'shannon'      : '''The Shannon is the major river on the island of Ireland.  From the Shannon Pot in Co. Cavan
                                  it flows generally southwards before turning west and emptying into the Atlantic Ocean through
                                  the Shannon Estuary near the city of Limerick.  The Royal Canal and the Grand Canal connect the
                                  Shannon to Dublin and the Irish Sea.

                                  The river represents a major physical barrier between east and west, dividing the west of Ireland (principally the province of Connacht)
                                  from the east and south (Leinster and most of Munster).

                                  Many parts of the river are used for pleasure craft, and there is a hydroelectric generation plant at Ardnacrusha.''',

              'singapore'    : '''Singapore is both an island country in Southeast Asia and a river within the country. Its territory comprises a main island,
                                  over 60 satellite islands and islets, and one outlying islet.

                                  The Singapore River is approximately 3.2 kilometers long from its source at Kim Seng Bridge
                                  to where it empties into Marina Bay.''',

              'slave'        : '''The Slave River is a Canadian river that flows from the confluence of the Rivière des Rochers
                                  and Peace River in northeastern Alberta and runs into Great Slave Lake in the Northwest Territories.

                                  The river is the home of the northernmost river pelican colony in North America.''',

              'rhine'        : '''The Rhine is the second-longest river in Central and Western Europe (after the Danube), and
                                  the Rhine Falls are the most powerful waterfall in Europe.  The Rhine and the Danube comprised much
                                  of the Roman Empire's northern inland boundary, and the Rhine has been a vital navigable waterway
                                  since those days, bringing trade and goods deep inland.

                                  The various castles and defenses built along it attest to its prominence as a waterway
                                  in the Holy Roman Empire. ''',

              'rhone'        : '''The Rhône is a major river in France and Switzerland, rising in the Alps and flowing west and south
                                  through Lake Geneva and Southeastern France before discharging into the Mediterranean Sea.

                                  Before railways and highways were developed, the Rhône was an important inland trade and transportation
                                  route.''',

              'seine'        : '''The Seine rises at Source-Seine, 30 kilometres northwest of Dijon and flows through Paris and into
                                  the English Channel at Le Havre (and Honfleur on the left bank).

                                  It is navigable by ocean-going vessels as far as Rouen, 120 kilometres from the sea.
                                  More than 60 percent of its length, as far as Burgundy, is negotiable by large barges and tour boats,
                                  and nearly its whole length is available for recreational boating.''',

              'shebelle'     : '''The Shebelle River begins in the highlands of Ethiopia and then flows southeast into Somalia towards
                                  Mogadishu. In the lower basin of the river, agriculture has largely replaced the traditional nomadic
                                  herding lifestyle, and the cultivation of bananas along the southern stretches of the Shebeli and Jubba
                                  Rivers contributes significantly to Somalia's export industry.''',

              'tagus'        : '''The Tagus, the longest river in the Iberian Peninsula, rises in mid-eastern Spain, flows generally
                                  westward, and empties into the Atlantic Ocean at Lisbon.''',

              'thames'       : '''The River Thames rises at Thames Head in Gloucestershire and flows through Oxford (where it is sometimes
                                  called the Isis), Reading, Henley-on-Thames, Windsor and London.  Along its course are 45 navigation
                                  locks with accompanying weirs.

                                  It supports a variety of wildlife and has a number of adjoining sites of special scientific interest,
                                  with the largest being in the North Kent Marshes.''',

              'tigris'       : '''The Tigris is the eastern of the two great rivers that define Mesopotamia, the other being the Euphrates.
                                  It flows south from the mountains of the Armenian Highlands through the Syrian and Arabian Deserts,
                                  before merging with the Euphrates and reaching to the Persian Gulf.

                                  In ancient times the Tigris nurtured the Assyrian Empire.  Today it faces threats from geopolitical
                                  instability, dam projects, poor water management, and climate change, raising concerns about its
                                  sustainability.''',

              'ubangii'      : '''The Ubangi River in Central Africa, provides an important transport artery for river boats between
                                  Bangui in the Central African Republic and Brazzaville in the Republic of the Congo.''',

              'umgeni'       : '''The Umgeni River in KwaZulu-Natal, South Africa rises in the "Dargle" in the KZN Midlands, and its mouth
                                  is at Durban, some distance north of Durban's natural harbour.

                                  It is believed that Vasco da Gama replenished his fleet's water supply at the Umgeni mouth on
                                  Christmas Day, 1497, and so named the region Natal, Portuguese for Christmas.''',

              'volga'        : '''The Volga, the longest river in Europe, is widely regarded as the national river of Russia.
                                  It has a symbolic meaning in Russian culture – Russian literature and folklore often refer to it
                                  as Mother Volga.  The fertile river valley provides large quantities of wheat and other agricultural produce,
                                  and also has many mineral riches.

                                  A substantial petroleum industry centers on the Volga valley, and several large hydroelectric reservoirs were constructed on the Volga during the Soviet era.''',

              'volta'        : '''The Volta River, the main river system of Ghana, flows south into Ghana from the Bobo-Dioulasso
                                  highlands of Burkina Faso and empties into the Atlantic Ocean at the Gulf of Guinea at Ada Foah.

                                  The country of Burkina Faso was formerly called Upper Volta, after the river.''',

              'yangtze'      : '''The Yangtze River, the longest river in China, has played a major role in Chinese history, culture,
                                  and economy.  For thousands of years, the river has been used for water, irrigation, sanitation,
                                  transportation, industry, and boundary-marking.

                                  The Yangtze Delta generates as much as 20% of China's GDP, and the Three Gorges Dam on the river is the
                                  largest hydro-electric power station in the world.''',

              'yellow'       : '''The Yellow River is the second-longest river in China.  Its basin was the birthplace of ancient
                                  Chinese civilization.

                                  According to traditional Chinese historiography, the Xia dynasty originated
                                  on its banks around 2100 BC.''',

              'zambezi'      : '''The Zambezi, 2,574 km (1,599 mi) long is the fourth longest river in Africa.
                                  It rises in Zambia, flows eastward to cross Mozambique and empties into the
                                  Indian Ocean.

                                  Notable features are Victoria Falls, the Kariba Dam which provides hydroelectric
                                  power to Zambia and Zimbabwe and the Cahora Bassa dam which provides power to
                                  Mozambique and South Africa. There are smaller power stations at Victoria Falls
                                  and Zengamina.''',

                }


        self.topics = {
            "Animals":       Animals,
            "Places":        Places,
            "Countries":     Countries,
            "Rivers":        Rivers,
            "Sports":        Sports,
            "Miscellaneous": Miscellaneous
        }

        self.topic = self.choose_topic()
        self.secret_word = self.choose_secret_word()

        self.correct_guesses = set()
        self.incorrect_guesses = set()
        self.attempts_left = 13

        self.build_title_screen()


    def build_title_screen(self):
        self.title_frame = tk.Frame(self.master, bg='oldlace')
        self.title_frame.pack(fill='both', expand=True)

        mascot_canvas = tk.Canvas(self.title_frame, width=200, height=220, bg='oldlace', highlightthickness=0)
        mascot_canvas.pack(pady=(40, 10))
        self.draw_mascot(mascot_canvas)

        title_label = tk.Label(self.title_frame, text="HANGMAN", font=("Helvetica", 54, "bold"),
                               fg="#1565C0", bg='oldlace')
        title_label.pack(pady=(0, 5))

        tagline_label = tk.Label(self.title_frame, text="Guess the word, save your friend!",
                                 font=("Helvetica", 16, "italic"), fg="#37474F", bg='oldlace')
        tagline_label.pack(pady=(0, 30))

        instructions_frame = tk.Frame(self.title_frame, bg='aliceblue',
                                      highlightbackground='gray', highlightthickness=1)
        instructions_frame.pack(pady=(0, 30), padx=200)

        instructions_label = tk.Label(instructions_frame, text=self.HOW_TO_PLAY_TEXT, font=("Arial", 14),
                                      bg='aliceblue', justify='left', padx=25, pady=20)
        instructions_label.pack()

        play_button = tk.Button(self.title_frame, text="PLAY", command=self.start_game, width=20,
                               height=2, bg="#4CAF50", fg="black", font=("Helvetica", 16, "bold"))
        play_button.pack(pady=(0, 40))


    def start_game(self):
        self.title_frame.destroy()
        self.initialize_gui()


    def draw_mascot(self, canvas):
        canvas.create_oval(60, 10, 140, 90, fill="#FFDAB3", outline="#5D4037", width=2)
        canvas.create_oval(68, 55, 80, 65, fill="#FFB0A0", outline="")
        canvas.create_oval(120, 55, 132, 65, fill="#FFB0A0", outline="")
        canvas.create_oval(78, 38, 88, 48, fill="#5D4037", outline="")
        canvas.create_oval(112, 38, 122, 48, fill="#5D4037", outline="")
        canvas.create_line(80, 58, 100, 70, 120, 58, smooth=True, width=3, fill="#5D4037", capstyle=tk.ROUND)
        canvas.create_line(100, 90, 100, 160, width=22, fill="#42A5F5", capstyle=tk.ROUND)
        canvas.create_line(100, 105, 55, 130, width=12, fill="#FFDAB3", capstyle=tk.ROUND)
        canvas.create_line(100, 105, 145, 130, width=12, fill="#FFDAB3", capstyle=tk.ROUND)
        canvas.create_line(100, 160, 55, 195, width=12, fill="#37474F", capstyle=tk.ROUND)
        canvas.create_line(100, 160, 145, 195, width=12, fill="#37474F", capstyle=tk.ROUND)


    def show_instructions_popup(self):
        popup = tk.Toplevel(self.master)
        popup.title("How to Play")
        popup.configure(bg='aliceblue')
        label = tk.Label(popup, text=self.HOW_TO_PLAY_TEXT, font=("Arial", 14), bg='aliceblue',
                         justify='left', padx=25, pady=20)
        label.pack()
        close_button = tk.Button(popup, text="Close", command=popup.destroy, width=15, height=1,
                                bg="aliceblue", font=("Helvetica", 12, "bold"))
        close_button.pack(pady=(0, 15))


    def initialize_gui(self):
        button_bg = "aliceblue"
        button_fg = "black"
        button_font = ("Helvetica", 12, "bold")
        self.help_button = tk.Button(self.master, text="How to Play", command=self.show_instructions_popup,
                                     width=14, height=1, bg=button_bg, fg=button_fg,
                                     font=("Helvetica", 10, "bold"))
        self.help_button.place(x=20, y=20)
        self.hangman_canvas = tk.Canvas(self.master, width=300, height=400, bg="#E1F5FE")
        self.hangman_canvas.pack(pady=10)
        self.draw_scenery()
        self.word_display = tk.Label(self.master, text="_ " * len(self.secret_word), font=("Helvetica", 30),
                                   bg='oldlace')
        self.word_display.pack(pady=(10, 8))

        self.topic_display = tk.Label(self.master, text="Topic: " + self.topic, font=("Helvetica", 30),
                                      bg='oldlace')
        self.topic_display.pack(pady=(15, 8))
        self.attempts_display = tk.Label(self.master, text="", font=("Helvetica", 16),
                                         bg='oldlace')
        self.attempts_display.pack(pady=(0, 8))
        self.update_attempts_display()
        self.reset_button = tk.Button(self.master, text="Reset Game", command=self.reset_game, width=20,
                             height=2, bg=button_bg, fg=button_fg, font=button_font)
        self.reset_button.pack(pady=(8, 15))
        self.buttons_frame = tk.Frame(self.master)
        self.buttons_frame.pack(pady=8)
        self.setup_alphabet_buttons()
        self.master.bind_all("<Key>", self.handle_keypress)


    def setup_alphabet_buttons(self):

        self.letter_buttons = {}

        button_bg = self.default_button_bg = "aliceblue"
        button_fg = "black"
        button_font = ("Helvetica", 12, "bold")

        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        upper_row = alphabet[:13]
        lower_row = alphabet[13:]

        upper_frame = tk.Frame(self.buttons_frame)
        upper_frame.pack()

        lower_frame = tk.Frame(self.buttons_frame)
        lower_frame.pack()

        for letter in upper_row:
            button = tk.Button(upper_frame,
                               text=letter,
                               command=lambda l=letter: self.guess_letter(l),
                               width=4,height=2, font=button_font,
                               bg=button_bg, highlightbackground=button_bg,
                               activebackground=button_bg, fg=button_fg,)

            button.pack(side="left", padx=2, pady=4)
            self.letter_buttons[letter] = button

        for letter in lower_row:
            button = tk.Button(lower_frame, text=letter, command=lambda l=letter: self.guess_letter(l),
                             width=4, height=2, bg=button_bg, highlightbackground=button_bg,
                             activebackground=button_bg, fg=button_fg, font=button_font)
            button.pack(side="left", padx=2, pady=4)
            self.letter_buttons[letter] = button


    def choose_topic(self):
        topic = random.choice(list(self.topics.keys()))
        #print("Topic:", topic)
        return topic


    def choose_secret_word(self):
        word_list = self.topics[self.topic]
        random.shuffle(word_list)
        secret_word = random.choice(word_list).upper()
        #print("Secret word:", secret_word)
        return secret_word


    def handle_keypress(self, event):
        letter = event.char.upper()
        button = self.letter_buttons.get(letter)
        if button is not None and button['state'] == tk.NORMAL:
            self.guess_letter(letter)


    def update_hangman_canvas(self):
        self.hangman_canvas.delete("all")
        self.draw_scenery()
        stages = [self.draw_base, self.draw_vertical, self.draw_horizontal, self.draw_diagonal,
                self.draw_drop, self.draw_rope, self.draw_head, self.draw_body, self.draw_left_arm,
                self.draw_right_arm, self.draw_left_leg, self.draw_right_leg]
        wrong = len(self.incorrect_guesses)
        for i in range(min(wrong, len(stages))):
            stages[i]()
        if wrong >= 7:
            self.draw_expression(wrong)


    def draw_scenery(self):
        self.hangman_canvas.create_rectangle(0, 370, 300, 400, fill="#A5D6A7", outline="")
        self.hangman_canvas.create_oval(230, 15, 270, 55, fill="#FFF176", outline="")


    def draw_base(self):
        self.hangman_canvas.create_line(20, 380, 140, 380, width=12, fill="#6D4C41", capstyle=tk.ROUND)
        self.hangman_canvas.create_line(20, 376, 140, 376, width=3, fill="#8D6E63", capstyle=tk.ROUND)
    def draw_vertical(self):
        self.hangman_canvas.create_line(80, 380, 80, 40, width=12, fill="#6D4C41", capstyle=tk.ROUND)
        self.hangman_canvas.create_line(76, 380, 76, 40, width=3, fill="#8D6E63", capstyle=tk.ROUND)
    def draw_horizontal(self):
        self.hangman_canvas.create_line(75, 40, 190, 40, width=12, fill="#6D4C41", capstyle=tk.ROUND)
        self.hangman_canvas.create_line(75, 36, 190, 36, width=3, fill="#8D6E63", capstyle=tk.ROUND)
    def draw_diagonal(self):
        self.hangman_canvas.create_line(79, 80, 150, 40, width=8, fill="#6D4C41", capstyle=tk.ROUND)
    def draw_drop(self):
        self.hangman_canvas.create_line(185, 40, 185, 60, width=10, fill="#6D4C41", capstyle=tk.ROUND)
    def draw_rope(self):
        self.hangman_canvas.create_line(185, 60, 185, 90, width=3, fill="#BCAAA4", capstyle=tk.ROUND)

    def draw_head(self):
        self.hangman_canvas.create_oval(155, 90, 215, 150, fill="#FFDAB3", outline="#5D4037", width=2)
        self.hangman_canvas.create_oval(163, 128, 173, 136, fill="#FFB0A0", outline="")
        self.hangman_canvas.create_oval(197, 128, 207, 136, fill="#FFB0A0", outline="")
        self.hangman_canvas.create_oval(171, 111, 179, 119, fill="#5D4037", outline="")
        self.hangman_canvas.create_oval(191, 111, 199, 119, fill="#5D4037", outline="")
    def draw_body(self):
        self.hangman_canvas.create_line(185, 150, 185, 270, width=24, fill="#42A5F5", capstyle=tk.ROUND)
    def draw_left_arm(self):
        self.hangman_canvas.create_line(185, 170, 125, 200, width=13, fill="#FFDAB3", capstyle=tk.ROUND)
    def draw_right_arm(self):
        self.hangman_canvas.create_line(185, 170, 245, 200, width=13, fill="#FFDAB3", capstyle=tk.ROUND)
    def draw_left_leg(self):
        self.hangman_canvas.create_line(185, 270, 125, 310, width=13, fill="#37474F", capstyle=tk.ROUND)
    def draw_right_leg(self):
        self.hangman_canvas.create_line(185, 270, 245, 310, width=13, fill="#37474F", capstyle=tk.ROUND)


    def draw_expression(self, wrong_count):
        level = min(wrong_count - 7, 6)  # 0 (just revealed) .. 6 (final, losing guess)

        if level < 5:
            sag = level * 3
            self.hangman_canvas.create_line(174, 130, 185, 130 - sag, 196, 130,
                                             smooth=True, width=3, fill="#5D4037", capstyle=tk.ROUND)
        else:
            self.hangman_canvas.create_oval(176, 127, 194, 145, fill="white", outline="#5D4037", width=2)
            self.hangman_canvas.create_oval(181, 134, 189, 142, fill="#8D6E63", outline="")

        if level >= 3:
            droop = min(level - 2, 4)
            self.hangman_canvas.create_line(168, 104 - droop, 180, 108, width=3, fill="#5D4037", capstyle=tk.ROUND)
            self.hangman_canvas.create_line(190, 108, 202, 104 - droop, width=3, fill="#5D4037", capstyle=tk.ROUND)


    def guess_letter(self, letter):
        button = self.letter_buttons[letter]

        if letter in self.secret_word:# and letter not in self.correct_guesses:
            self.correct_guesses.add(letter)
            button.config(text=f"{letter}\n✓", bg="#4CAF50", highlightbackground="#4CAF50",
                          disabledforeground="white")
            self.sound_player.play("correct")

        elif letter not in self.incorrect_guesses:
            self.incorrect_guesses.add(letter)
            self.attempts_left -= 1
            button.config(text=f"{letter}\n✗", bg="#E57373", highlightbackground="#E57373",
                          disabledforeground="white")
            self.update_hangman_canvas()
            self.sound_player.play("wrong")

        button.config(state=tk.DISABLED)
        self.update_word_display()
        self.update_attempts_display()
        self.check_game_over()


    def update_attempts_display(self):
        self.attempts_display.config(text=f"Guesses left: {self.attempts_left}")


    def update_word_display(self):
        displayed_word = " ".join([letter if letter in self.correct_guesses
                                   else "_" for letter in self.secret_word])
        self.word_display.config(text=displayed_word)


    def check_game_over(self):
        if set(self.secret_word).issubset(self.correct_guesses):
            self.sound_player.play("win")
            self.display_game_over_message("Congratulations, you've won!")
        elif self.attempts_left == 0:
            self.sound_player.play("lose")
            self.display_game_over_message(
                f"Game over! The word was: {self.secret_word}"
        )


    def display_game_over_message(self, message):
        stylish_font = ("Arial", 18, "italic")
        info_font = ("Arial", 15)
        button_bg = "red"
        button_fg = "black"
        button_font = ("Helvetica", 12, "bold")

        self.reset_button.pack_forget()
        self.buttons_frame.pack_forget()

        # Disable all alphabet buttons
        for frame in self.buttons_frame.winfo_children():
            for button in frame.winfo_children():
                button.configure(state=tk.DISABLED)

        self.game_over_label = tk.Label(
            self.master,
            text=message,
            font=stylish_font,
            fg="red",
            bg='light blue'
        )
        self.game_over_label.pack(pady=(10, 10))


        #  COMMENTS
        #  Get information about the word from the Comments dictionary
        raw_comment = self.comments.get(self.secret_word.lower(), "").strip()

        # Blank lines in the dictionary mark paragraph breaks; collapse
        # whitespace within each paragraph but keep the breaks between them.
        paragraphs = re.split(r'\n\s*\n', raw_comment)
        comment = "\n\n".join(
            " ".join(paragraph.split()) for paragraph in paragraphs if paragraph.strip()
        )

        if comment:
            self.comment_frame = tk.Frame(
                self.master,
                bg='aliceblue',
                highlightbackground='gray',
                highlightthickness=1
            )

            #  width is fixed so the text wraps consistently; height is
            #  measured from the comment below and placed with a generous
            #  temporary height so nothing is clipped while measuring
            comment_width = 380
            max_comment_height = 700
            self.comment_frame.place(
                x=740,
                y=100,
                width=comment_width,
                height=max_comment_height
            )

            self.comment_text = tk.Text(
                self.comment_frame,
                font=info_font,
                bg='aliceblue',
                wrap="word",
                relief="flat",
                borderwidth=0,
                padx=15,
                pady=15
            )

            self.comment_text.insert("1.0", comment)
            self.comment_text.config(state=tk.DISABLED)

            self.comment_text.pack(
                fill="both",
                expand=True
            )

            #  shrink the frame to fit the comment actually shown
            self.master.update_idletasks()
            display_lines = self.comment_text.count("1.0", "end", "displaylines")[0]
            line_height = tkfont.Font(font=info_font).metrics("linespace")
            content_height = (display_lines + 1) * line_height + 2 * 15  # + text pady, + spare lines
            comment_height = max(60, min(content_height, max_comment_height))
            self.comment_frame.place_configure(height=comment_height)

        if not hasattr(self, 'restart_button'):
            self.restart_button = tk.Button(
                self.master,
                text="PLAY AGAIN?",
                command=self.reset_game,
                width=20,
                height=2,
                bg=button_bg,
                fg=button_fg,
                font=button_font
            )

        self.restart_button.pack(pady=(10, 10))
        self.master.update_idletasks()



    def reset_game(self):
        self.topic = self.choose_topic()
        self.secret_word = self.choose_secret_word()

        self.correct_guesses = set()
        self.incorrect_guesses = set()
        self.attempts_left = 13

        self.hangman_canvas.delete("all")
        self.draw_scenery()

        self.topic_display.config(text="Topic: " + self.topic)

        self.update_word_display()
        self.update_attempts_display()

        for letter, button in self.letter_buttons.items():
            button.config(text=letter, state=tk.NORMAL, bg=self.default_button_bg,
                          highlightbackground=self.default_button_bg)

        self.reset_button.pack(pady=(10, 40))

        if hasattr(self, 'game_over_label') and self.game_over_label.winfo_exists():
            self.game_over_label.pack_forget()
        if hasattr(self, 'comment_frame') and self.comment_frame.winfo_exists():
            self.comment_frame.place_forget()
        if hasattr(self, 'restart_button') and self.restart_button.winfo_exists():
            self.restart_button.pack_forget()

        self.buttons_frame.pack()
        self.master.update_idletasks()


def main():
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
