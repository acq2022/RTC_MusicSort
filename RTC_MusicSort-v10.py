import os
import shutil
import music_tag
import webbrowser
import tkinter
from tkinter import filedialog
from tkinter import messagebox
from multipledispatch import dispatch


class Track:
    

    # TODO: CHANGE (self, root_path, title) TO (self, path) ?
    def __init__(self, root_path, title):

        #self.path = root_path + title
        self.path = os.path.join(root_path, str(title))
        print(self.path)
        print('\n')
        tags = music_tag.load_file(self.path)

        self.extension =  '.' + title.split('.')[-1]
        self.title = title.replace(self.extension, '')

        album_year = 'XXXX'
        self.album_name = 'Unknow Album'
        
        self.artist_name = 'Unknow Artist'

        self.artwork = str(tags['artwork'])

        # --- TITLE ---

        # Sécurise problème de parsing lié à un mauvais encodage du tag 'tracknumber'
        try: 
            tags['tracknumber']
        except :
            tags.remove_tag('tracknumber')

        # Tag number
        if(int(tags['tracknumber']) > 0):
            number = str("%02d" % (tags['tracknumber'],))
                
            # Tag title
            if(str(tags['tracktitle']) != '' and str(tags['tracktitle']) != ' '):

                # Title = tag number + tag title
                self.title = number + ' - ' + str(tags['tracktitle'])


        # Mise en forme title
        self.title = self.edit_format_text_of(self.title, self.extension)

        # --- ALBUM NAME ---

        # Tag year
        if(str(tags['year']) != ''):
            album_year = str(tags['year'])

        # Tag album
        if(str(tags['album']) != ''):
            self.album_name = str(tags['album'])

        # Album name
        self.album_name = album_year + " - " + self.album_name

        # Mise en forme album name
        self.album_name = self.edit_format_text_of(self.album_name)

        # --- ARTIST NAME ---

        # Tag artist
        if(str(tags['artist']) != ''):
            self.artist_name = str(tags['artist'])

        # Mise en forme artist name
        self.artist_name = self.edit_format_text_of(self.artist_name)


    @dispatch(str)
    def edit_format_text_of(self, text): # Pour les dossiers

        # Effacer les '.' dans le texte
        text = text.replace('.', '')

        # Securiser les characteres du texte
        text = self.securise_name_of(text)

        # Effacer les espaces multiples du texte
        text = self.delete_multiple_space_in(text)

        # Editer les majuscules et minuscules dans le texte
        text = text.title()

        return text
    
    @dispatch(str, str)
    def edit_format_text_of(self, text, extension): # Pour les fichiers

        # Securiser les characteres du texte
        text = self.securise_name_of(text)

        # Effacer les espaces multiples du texte
        text = self.delete_multiple_space_in(text)

        # Editer les majuscules et minuscules dans le texte
        text = text.title()

        # Rajouter l'extension
        text += extension

        return text


    def securise_name_of(self, file_name):

        if('<' in file_name):
            file_name = file_name.replace('<', ' ')
        if('>' in file_name):
            file_name = file_name.replace('>', ' ')
        if(':' in file_name):
            file_name = file_name.replace(':', ' ')
        if('"' in file_name):
            file_name = file_name.replace('"', ' ')
        if('/' in file_name):
            file_name = file_name.replace('/', ' ')
        if('\\' in file_name):
            file_name = file_name.replace('\\', ' ')
        if('|' in file_name):
            file_name = file_name.replace('|', ' ')
        if('?' in file_name):
            file_name = file_name.replace('?', ' ')
        if('*' in file_name):
            file_name = file_name.replace('*', ' ')
        return file_name


    def delete_multiple_space_in(self, text):

        words = text.split()
        new_text = words[0]
        i = 1
        while(i < len(words)):
            new_text += ' ' + words[i]
            i += 1
        return new_text



def isTrack(file):

    return( file.endswith('.aac') or
            file.endswith('.aiff') or
            file.endswith('.dsf') or
            file.endswith('.flac') or
            file.endswith('.m4a') or
            file.endswith('.mp3') or
            file.endswith('.ogg') or
            file.endswith('.opus') or
            file.endswith('.wav') or
            file.endswith('.wv'))
            

def copy_file_and_rename(source, destination, new_name, is_moving):

    target = os.path.join(destination, new_name)
    num = 0

    # Tant que les fichiers source ET cible existent
    while os.path.exists(source) and os.path.exists(target):

        # Taille des fichiers
        source_size = os.stat(source).st_size
        target_size = os.stat(target).st_size

        # Si tailles les mêmes, alors on supprime le fichier source
        if(source_size == target_size):
            os.remove(source)

        # Indentation du fichier si déjà existant
        period = new_name.rfind('.')
        if period == -1:
            period = len(new_name)
        num += 1
        new_file = f'{new_name[:period]}({num}){new_name[period:]}'
        target = os.path.join(destination, new_file)
    
    # Copie du fichier si nécessaire
    if(os.path.exists(source)):
        if(is_moving):
            shutil.move(source, target)
        else:
            shutil.copy(source, target)


def sort_tracks_of_folder(source_path, final_path, is_moving):

    # Dictionnaire keys -> albums, values -> [artists]
    albums = {}

    # Pour chaque élément du dossier
    for e in os.listdir(source_path):
        new_path = os.path.join(source_path, str(e))
        print('source_path : ', source_path)
        print('new_path : ', new_path)

        
        # Dossier ?
        if(os.path.isdir(new_path)):
            print(e + ' is a folder')
                
            # Le dossier devient le nouvel emplacement à trier
            #new_path = new_path + '\\'
            sort_tracks_of_folder(new_path, final_path, is_moving)
            
        else:

            # Morceau ?
            if(isTrack(e)):

                # Sécuriser en cas de problème chargement du fichier
                try:

                    # Création objet Track
                    track = Track(source_path, e)

                    # Remplir le dictionnaire
                    if track.album_name in albums:
                        albums[track.album_name].append(track)
                    else:
                        albums[track.album_name] = [track]
                
                except Exception as er:
                    print('problem occurs with file ' + new_path + ' : ' + str(er))
                    # TODO: WRITE THE PRINT IN 'REPORT.txt'
            
            else:
                print(e + ' : file not processed')
                print('\n')
                # TODO: WRITE THE PRINT IN 'REPORT.txt'
                # TODO: COPY FILE IN A 'NOT PROCESSED' FOLDER
                #copy_file_and_rename(source, folder_destination, track.title, is_moving)


    # Pour chaque liste d'artistes associés par album 
    for album in albums:

        artist_folder_name = 'VA'
        album_folder_name = album

        c = 0

        # Comparer les artist_name entre eux
        for i in range(len(albums[album])):
            for j in range(i + 1, len(albums[album])):
                if(albums[album][i].artist_name != albums[album][j].artist_name):
                    c += 1

        # Vérifier qu'il n'y ait qu'un seul artist_name par album
        if(c == 0):
            
            # Nommer le dossier Artist (si non, nom = 'VA')
            artist_folder_name = albums[album][0].artist_name

        # Itérer chaque track
        for track in albums[album]:
            source = track.path
            folder_destination = os.path.join(final_path, artist_folder_name, album_folder_name)

            # Création des dossiers Artist et Album
            if not os.path.exists(folder_destination):
                os.makedirs(folder_destination)

            # Déplacer les fichiers
            copy_file_and_rename(source, folder_destination, track.title, is_moving)


def show_success_window():
    res = messagebox.askquestion('SUCCESS !', 'Music sorted with success !\nOpen destination folder ?')
    if(res == 'yes'):
        webbrowser.open(destination_path.get())
        app.destroy()
    else:
        app.destroy()


def start_sort():

    app.update()
    sort_tracks_of_folder(root_path.get(), destination_path.get(), action_type.get())
    show_success_window()


def show_animation_loader():
    print('load')


def check_button_state():

    if(root_path.get() != '' and destination_path.get() != ''):
        button_sort['state'] = 'normal'
    else:
        button_sort['state'] = 'disable'


def set_destination_path():

    app.withdraw()
    path = filedialog.askdirectory()
    destination_path.set(path)
    print(destination_path.get())
    # TODO: WRITE THE PRINT IN 'REPORT.txt'
    check_button_state()
    app.deiconify()


def set_root_path():
    
    app.withdraw()
    path = filedialog.askdirectory()
    root_path.set(path)
    print(root_path.get())
    # TODO: WRITE THE PRINT IN 'REPORT.txt'
    check_button_state()
    app.deiconify()

# Création et paramétrage de la fenêtre
app = tkinter.Tk()
app.title('Music Sort')
app.geometry('420x160')
app.resizable(width=False, height=False)

# --- WIDGETS ---

# Sélection du dossier à trier

root_path = tkinter.StringVar()

label_root_path = tkinter.Label(app, text = 'Dossier à trier')
button_root_path = tkinter.Button(app, width = 9, text = 'Parcourir...', command = set_root_path)
entry_root_path = tkinter.Entry(app, width = 66, textvariable = root_path)

# Sélection du dossier de destination

destination_path = tkinter.StringVar()

label_destination_path = tkinter.Label(app, text = 'Dossier de destination')
button_destination_path = tkinter.Button(app, width = 9, text = 'Parcourir...', command = set_destination_path)
entry_destination_path = tkinter.Entry(app, width = 66, textvariable = destination_path)

# Sélection 'copy' or 'move'

action_type = tkinter.IntVar()
radio_button_copy = tkinter.Radiobutton(app, text = 'copy', value = 0, variable = action_type)
radio_button_move = tkinter.Radiobutton(app, text = 'move', value = 1, variable = action_type)

# Lancement du tri

button_sort = tkinter.Button(app, width = 9, text = 'Trier', state='disable', command = start_sort)
button_cancel = tkinter.Button(app, width = 9, text = 'Annuler', command = app.destroy)

# Placement des widgets

label_root_path.place(x=10, y=13)
button_root_path.place(x=335, y=10)
entry_root_path.place(x=10, y=40)

label_destination_path.place(x=10, y=73)
button_destination_path.place(x=335, y=70)
entry_destination_path.place(x=10, y=100)

radio_button_copy.place(x=10, y=130)
radio_button_move.place(x=70, y=130)

button_sort.place(x=250, y=130)
button_cancel.place(x=335, y=130)

# ------------

# Boucle principale
app.mainloop()


# scripted with love by acq