from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivymd.uix.menu import MDDropdownMenu
from kivy.clock import Clock
from API_lyrics_ovh import fetch_suggestions, get_lyrics
from kivy.core.clipboard import Clipboard
from kivymd.uix.label import MDLabel


class CopyableLabel(MDLabel):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            Clipboard.copy(self.text)
            print("Text copied to clipboard:")
            return True
        return super().on_touch_down(touch)


class GetLyrics(MDApp):

    """
    def on_text_change(self):
        # Debounce search input changes
        t=self.screen.ids.search.text

        Clock.unschedule(self.fetch_suggestions(t))
        if t:
            Clock.schedule_once(lambda dt: self.fetch_suggestions(t), 0.3)
    """

    def show_search_menu(self, search_text):
        # Clear previous results
        #self.menu.dismis()

        # API request to fetch suggestions
        try:
            seen_results = fetch_suggestions(search_text)

            n_of_records = len(seen_results)
            #print(n_of_results)
            n = 7
            if n_of_records < 7:
                n = n_of_records-1

            menu_items = [
                {
                    "text": seen_results[i],
                    "on_release": lambda x=seen_results[i]: self.find_lyrics(x),
                } for i in range(n)
            ]
            #print(type(menu_items))
            #print(menu_items)

            self.menu = MDDropdownMenu(
                    caller=self.root.ids.search, items=menu_items
                    )
            self.menu.open()

        except Exception as e:
            print(f"Error fetching suggestions: {e}")
            self.root.ids.text1.text="Could not retrieve results."



    def find_lyrics(self, text_item):
        print(text_item)
        self.root.ids.search.text = text_item
        self.menu.dismiss()
        t, a = text_item.split(" - ", 1)
        title = t.replace(" ", "_")
        artist = a.replace(" ", "_")
        try:
            lyrics = get_lyrics(title,artist)
            self.show_lyrics(lyrics)
        except Exception as e:
            print(f"Error fetching suggestions: {e}")
            self.root.ids.text1.text="Could not retrieve lyrics."


    def show_lyrics(self, response):
        try:
            lyrics = str(response['lyrics'])
            lines = lyrics.splitlines()
            mid_point = len(lines) // 2
            text = []
            text.append("\n".join(lines[:mid_point]))
            text.append("\n".join(lines[mid_point:]))
            self.root.ids.text1.text=text[0]
            self.root.ids.text2.text=text[1]

        except Exception as e:
            print(f"Error fetching suggestions: {e}")
            self.root.ids.text1.text="Could not retrieve lyrics."



    def build(self):
        Window.size = (860, 600)
        self.screen = Builder.load_file("main.kv")
        self.theme_cls.theme_style = "Dark"  # or "Light"
        self.theme_cls.primary_palette = "Blue"
        return self.screen

GetLyrics().run()
