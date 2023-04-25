from pygame import mixer


class Mixer():

    def __init__(self):

        # Musicas
        self.hyrule_song = self.create_song('lost_woods')
        self.dungeon_song = [
            self.create_song('song_of_storms', 0.7),
            self.create_song('meet_zelda_again', 0.7),
            self.create_song('mayors_meeting', 0.7)
        ]
        self.get_pingente = self.create_song('small_item_get', 0.5)
        self.winner_song = self.create_song('ikana_castle')

        # Canais
        self.ch_hyrule = mixer.Channel(0)
        self.ch_dungeon = [mixer.Channel(i) for i in range(1, 4)]
        self.ch_winner = mixer.Channel(4)
        self.ch_pingente = mixer.Channel(5)

        # Musica tocando atualmente (dungeon ou hyrule)
        self.ch_current_playing = self.ch_hyrule


    # Criador de sons
    def create_song(self, path, volume=1):
        mixer.init()
        sound = mixer.Sound(f'assets/audio/{path}.mp3')
        sound.set_volume(volume)
        return sound
    

    # Inicia a musica de hyrule
    def play_hyrule(self):
        self.ch_hyrule.play(self.hyrule_song)
        self.ch_current_playing = self.ch_hyrule


    # Pausa a musica de hyrule e inicia a musica da dungeon
    def play_dungeon(self, dungeon: int): #  1, 2 ou 3
        self.ch_hyrule.pause()
        self.ch_dungeon[dungeon-1].play(self.dungeon_song[dungeon-1])
        self.ch_current_playing = self.ch_dungeon[dungeon-1]


    # Inicia a musica de quando o player pega o pingente
    def play_get_pingente(self):
        self.ch_current_playing.set_volume(0.2)
        self.ch_pingente.play(self.get_pingente, maxtime=2000)
        self.ch_current_playing.set_volume(0.7)

    
    # Para a musicas da dungeon e despausa a musica de hyrule
    def unpause_hyrule(self):
        self.ch_current_playing.stop()
        self.ch_hyrule.unpause()


    # Para a musica de hyrule depois de um fadeout
    def fadeout_hyrule(self, fadeout=3300):
        self.ch_hyrule.fadeout(fadeout)

    
    # Para a musica de hyrule e inicia a musica de fim de jogo
    def play_winner(self):
        self.ch_hyrule.stop()
        self.ch_winner.play(self.winner_song)
