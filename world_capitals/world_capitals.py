# 25 July 2026

import tkinter as tk
import random


class Capitals:
    def __init__(self, master):
        self.master = master
        self.master.title("Capitals Game")
        self.master.configure(bg='aliceblue')
        self.master.geometry("900x650")
        #self.master.resizable(False, False)

        asia_dict = {
            'Afghanistan'          : "Kabul",
            'Armenia'              : "Yerevan",
            'Azerbaijan'           : "Baku",
            'Bahrain'              : "Manama",
            'Bangladesh'           : "Dhaka",
            'Bhutan'               : "Thimphu",
            'Brunei'               : "Bandar Seri Begawan",
            'Cambodia'             : "Phnom Penh",
            'China'                : "Beijing",
            'Cyprus'               : "Nicosia",
            'Georgia'              : "Tbilisi",
            'India'                : "New Delhi",
            'Indonesia'            : "Jakarta",
            'Iran'                 : "Tehran",
            'Iraq'                 : "Baghdad",
            'Israel'               : "Jerusalem",
            'Japan'                : "Tokyo",
            'Jordan'               : "Amman",
            'Kazakhstan'           : "Astana",
            'Kuwait'               : "Kuwait City",
            'Kyrgyzstan'           : "Bishkek",
            'Laos'                 : "Vientiane",
            'Lebanon'              : "Beirut",
            'Malaysia'             : "Kuala Lumpur",
            'Maldives'             : "Male",
            'Mongolia'             : "Ulaanbaatar",
            'Myanmar'              : "Naypyidaw",
            'Nepal'                : "Kathmandu",
            'North Korea'          : "Pyongyang",
            'Oman'                 : "Muscat",
            'Pakistan'             : "Islamabad",
            'Palestine'            : "Jerusalem",
            'Philippines'          : "Manila",
            'Qatar'                : "Doha",
            'Russia'               : "Moscow",
            'Saudi Arabia'         : "Riyadh",
            'Singapore'            : "Singapore",
            'South Korea'          : "Seoul",
            'Sri Lanka'            : "Sri Jayawardenepura Kotte",
            'Syria'                : "Damascus",
            'Taiwan'               : "Taipei",
            'Tajikistan'           : "Dushanbe",
            'Thailand'             : "Bangkok",
            'Timor-Leste'          : "Dili",
            'Turkey'               : "Ankara",
            'Turkmenistan'         : "Ashgabat",
            'United Arab Emirates' : "Abu Dhabi",
            'Uzbekistan'           : "Tashkent",
            'Vietnam'              : "Hanoi",
            'Yemen'                : "Sana'a",
        }

        europe_dict = {
            'Albania'                : "Tirana",
            'Andorra'                : "Andorra la Vella",
            'Armenia'                : "Yerevan",       
            'Austria'                : "Vienna",
            'Azerbaijan'             : 'Baku',
            'Belarus'                : "Minsk",
            'Belgium'                : "Brussels",
            'Bosnia and Herzegovina' : "Sarajevo",
            'Bulgaria'               : "Sofia",
            'Croatia'                : "Zagreb",
            'Cyprus'                 : "Nicosia",
            'Czechia'                : "Prague",
            'Denmark'                : "Copenhagen",
            'Estonia'                : "Tallinn",
            'Finland'                : "Helsinki",
            'France'                 : "Paris",
            'Georgia'                : "Tbilisi",
            'Germany'                : "Berlin",
            'Greece'                 : "Athens",
            'Hungary'                : "Budapest",
            'Iceland'                : "Reykjavik",
            'Ireland'                : "Dublin",
            'Italy'                  : "Rome",
            'Kazakhstan'             : "Astana",
            'Kosovo'                 : "Pristina",
            'Latvia'                 : "Riga",
            'Liechtenstein'          : "Vaduz",
            'Lithuania'              : "Vilnius",
            'Luxembourg'             : "Luxembourg City",
            'Malta'                  : "Valletta",
            'Moldova'                : "Chisinau",
            'Monaco'                 : "Monaco",
            'Montenegro'             : "Podgorica",
            'Netherlands'            : "Amsterdam",
            'North Macedonia'        : "Skopje",
            'Norway'                 : "Oslo",
            'Poland'                 : "Warsaw",
            'Portugal'               : "Lisbon",
            'Romania'                : "Bucharest",
            'Russia'                 : "Moscow",
            'San Marino'             : "San Marino",
            'Serbia'                 : "Belgrade",
            'Slovakia'               : "Bratislava",
            'Slovenia'               : "Ljubljana",
            'Spain'                  : "Madrid",
            'Sweden'                 : "Stockholm",
            'Switzerland'            : "Bern",
            'Turkey'                 : "Ankara",
            'Ukraine'                : "Kyiv",
            'United Kingdom'         : "London",
            'Vatican City (Holy See)': "Vatican City",
            'England'                : 'London',
            'Scotland'               : 'Edinburgh',
            'Wales'                  : 'Cardiff',
            
        }

        africa_dict = {
            'Algeria'                           : "Algiers",
            'Angola'                            : "Luanda",
            'Benin'                             : "Porto Novo",
            'Botswana'                          : "Gaborone",
            'Burkina Faso'                      : "Ouagadougou",
            'Burundi'                           : "Gitega",
            'Cabo Verde'                        : "Praia",
            'Cameroon'                          : "Yaounde",
            'Central African Republic'          : "Bangui",
            'Chad'                              : "N'Djamena",
            'Comoros'                           : "Moroni",
            'Congo, Democratic Republic of the' : "Kinshasa",
            'Congo, Republic of the'            : "Brazzaville",
            "Cote d'Ivoire"                     : "Yamoussoukro",
            'Djibouti'                          : "Djibouti City",
            'Egypt'                             : "Cairo",
            'Equatorial Guinea'                 : "Ciudad de la Paz",
            'Eritrea'                           : "Asmara",
            'Eswatini'                          : "Mbabane",
            'Ethiopia'                          : "Addis Ababa",
            'Gabon'                             : "Libreville",
            'Gambia'                            : "Banjul",
            'Ghana'                             : "Accra",
            'Guinea'                            : "Conakry",
            'Guinea-Bissau'                     : "Bissau",
            'Kenya'                             : "Nairobi",
            'Lesotho'                           : "Maseru",
            'Liberia'                           : "Monrovia",
            'Libya'                             : "Tripoli",
            'Madagascar'                        : "Antananarivo",
            'Malawi'                            : "Lilongwe",
            'Mali'                              : "Bamako",
            'Mauritania'                        : "Nouakchott",
            'Mauritius'                         : "Port Louis",
            'Morocco'                           : "Rabat",
            'Mozambique'                        : "Maputo",
            'Namibia'                           : "Windhoek",
            'Niger'                             : "Niamey",
            'Nigeria'                           : "Abuja",
            'Rwanda'                            : "Kigali",
            'Sao Tome and Principe'             : "São Tomé",
            'Senegal'                           : "Dakar",
            'Seychelles'                        : "Victoria",
            'Sierra Leone'                      : "Freetown",
            'Somalia'                           : "Mogadishu",
            'South Africa'                      : "Pretoria",
            'South Sudan'                       : "Juba",
            'Sudan'                             : "Khartoum",
            'Tanzania'                          : "Dodoma",
            'Togo'                              : "Lomé",
            'Tunisia'                           : "Tunis",
            'Uganda'                            : "Kampala",
            'Zambia'                            : "Lusaka",
            'Zimbabwe'                          : "Harare",
        }

        north_america_dict = {
            "Antigua and Barbuda"      : "Saint John's",
            'Bahamas'                  : "Nassau",
            'Barbados'                 : "Bridgetown",
            'Belize'                   : "Belmopan",
            'Canada'                   : "Ottawa",
            'Costa Rica'               : "San Jose",
            'Cuba'                     : "Havana",
            'Dominica'                 : "Roseau",
            'Dominican Republic'       : "Santo Domingo",
            'El Salvador'              : "San Salvador",
            "Grenada"                  : "Saint George's",
            'Guatemala'                : "Guatemala City",
            'Haiti'                    : "Port au Prince",
            'Honduras'                 : "Tegucigalpa",
            'Jamaica'                  : "Kingston",
            'Mexico'                   : "Mexico City",
            'Nicaragua'                : "Managua",
            'Panama'                   : "Panama City",
            'Saint Kitts and Nevis'    : "Basseterre",
            'Saint Lucia'              : "Castries",
            'Saint Vincent and the Grenadines'  : "Kingstown",
            'Trinidad and Tobago'      : "Port of Spain",
            'United States of America' : "Washington, D.C.",
        }

        south_america_dict = {
            'Argentina'  : "Buenos Aires",
            'Bolivia'    : "La paz",
            'Brazil'     : "Brasilia",
            'Chile'      : "Santiago",
            'Colombia'   : "Bogotá",
            'Ecuador'    : "Quito",
            'Guyana'     : "Georgetown",
            'Paraguay'   : "Asunción",
            'Peru'       : "Lima",
            'Suriname'   : "Paramaribo",
            'Uruguay'    : "Montevideo",
            'Venezuela'  : "Caracas",
        }

        australasia_and_oceania_dict = {
            'Australia'         : "Canberra",
            'Fiji'              : "Suva",
            'Kiribati'          : "Tarawa",
            'Marshall Islands'  :  "Majuro",
            'Micronesia'        : "Palikir",
            'Nauru'             : "Yaren District",
            'New Zealand'       : "Wellington",
            'Palau'             : "Ngerulmud",
            'Papua New Guinea'  : "Port Moresby",
            'Samoa'             : "Apia",
            'Solomon Islands'   : "Honiara",
            'Tonga'             : "Nukuʻalofa",
            'Tuvalu'            : "Funafuti",
            'Vanuatu'           : "Port Vila",
        }

        self.continents = {
            'Africa'                  : africa_dict,
            'Asia'                    : asia_dict,
            'Australasia and Oceania' : australasia_and_oceania_dict,
            'Europe'                  : europe_dict,
            'North America'           : north_america_dict,
            'South America'           : south_america_dict,
        }

        self.score = 0
        self.total = 0
        self.country = None
        self.capital = None

        self.build_gui()
        self.new_question()

    def build_gui(self):
        title = tk.Label(self.master, text="Capitals Game", font=("Helvetica", 32, "bold"), bg='aliceblue')
        title.pack(pady=(40, 10))

        self.continent_label = tk.Label(self.master, text="", font=("Helvetica", 16), bg='aliceblue', fg='gray30')
        self.continent_label.pack(pady=(0, 30))

        self.question_label = tk.Label(self.master, text="", font=("Helvetica", 24), bg='aliceblue', wraplength=1100, justify='center')
        self.question_label.pack(pady=20)

        self.answer_entry = tk.Entry(self.master, font=("Helvetica", 20), width=30, justify='center')
        self.answer_entry.pack(pady=20)
        self.answer_entry.bind("<Return>", self.check_answer)
        self.answer_entry.focus_set()

        button_frame = tk.Frame(self.master, bg='aliceblue')
        button_frame.pack(pady=10)

        self.submit_button = tk.Button(button_frame, text="Submit", font=("Helvetica", 14), width=12, command=self.check_answer)
        self.submit_button.grid(row=0, column=0, padx=10)

        self.next_button = tk.Button(button_frame, text="Next", font=("Helvetica", 14), width=12, command=self.new_question, state='disabled')
        self.next_button.grid(row=0, column=1, padx=10)

        self.feedback_label = tk.Label(self.master, text="", font=("Helvetica", 18, "bold"), bg='aliceblue')
        self.feedback_label.pack(pady=30)

        self.score_label = tk.Label(self.master, text="Score: 0 / 0", font=("Helvetica", 16), bg='aliceblue')
        self.score_label.pack(pady=10)

    def choose_continent(self):
        continent = random.choice(list(self.continents.keys()))
        return continent

    def choose_country(self, continent):
        country_dict = self.continents[continent]
        country = random.choice(list(country_dict.keys()))
        return country

    def new_question(self):
        continent = self.choose_continent()
        country = self.choose_country(continent)

        self.continent = continent
        self.country = country
        self.capital = self.continents[continent][country]

        self.continent_label.config(text=f"Continent: {continent}")
        self.question_label.config(text=f"What is the capital of {country}?")
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.config(state='normal')
        self.answer_entry.focus_set()
        self.feedback_label.config(text="")

        self.submit_button.config(state='normal')
        self.next_button.config(state='disabled')

    def check_answer(self, event=None):
        if self.submit_button['state'] == 'disabled':
            return

        user_answer = self.answer_entry.get().strip()
        correct = user_answer.lower() == self.capital.lower()

        self.total += 1
        if correct:
            self.score += 1
            self.feedback_label.config(text="Correct!", fg='green')
        else:
            self.feedback_label.config(text=f"Incorrect. The capital of {self.country} is {self.capital}.", fg='red')

        self.score_label.config(text=f"Score: {self.score} / {self.total}")

        self.submit_button.config(state='disabled')
        self.answer_entry.config(state='disabled')
        self.next_button.config(state='normal')


def main():
    root = tk.Tk()
    game = Capitals(root)
    root.mainloop()


if __name__ == "__main__":
    main()
