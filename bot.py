import tweepy, os
import numpy as np

from dotenv import load_dotenv
from time import sleep, time



def notes_tw(path1,historial,path2):
   notes_tws = [(i._json['full_text'],i._json['id_str']) for i in historial if i._json['is_quote_status'] and i._json['full_text'][:2]=='n!']
   #creamos una lista que contenga los tuits que son nota
   if (notes_tws):
      for nota,tweet in notes_tws:
         with open(path2+tweet+'.md','w',encoding='utf-8') as note:
            link = 'https://twitter.com/user/status/'+tweet
            mss= 'Titulo: =='+tweet+'=='
            mss1= '\n#twitter #opinion #foro #notas'
            note.write(mss+mss1)
            note.write('\nLink: '+link)
            note.write('\n ##  Comentario \n')
            note.write(nota)
   return [i[1] for i in notes_tws]



def login(path_env=''):
#cargamos variables de entono
   load_dotenv(path_env+'.env')
   API_KEY = os.getenv('API_Key')
   API_SECRET_KEY = os.getenv('API_SECRET_KEY')
   ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
   ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
   auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
   auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
   api = tweepy.API(auth)
   return api

def crear_notas(path1='',path2=''):
   '''
   path1 representa el lugar para guardar el log y el driver gecko. 
   path2 representa el lugar para guardar las notas e imagenes para obsidian
  '''
#Para obtener los tuits de un histórico 
#recuperamos todos los posibles. 
   user_track = 'jpcr3spo'
   historial = []
#Revisamos si existe un log 
   if(not os.path.exists(path1+'log_tweets.npy')):
      for status in tweepy.Cursor(api.user_timeline,screen_name=user_track,tweet_mode="extended",count=200).items():
         historial.append(status)
      log_ids = notes_tw(path1=path1,historial=historial,path2=path2)   #revisa si debe crear notas
      np.save(path1+'log_tweets.npy', log_ids) #guarda el log

   else:
      aux = api.user_timeline(screen_name=user_track,tweet_mode="extended",count=100)
      for st in aux:
      # #en mis estadisticas de uso no sobrepaso los 100 tuits día 
         historial.append(st)
      #revisamos el log    
      log = np.load(path1+'log_tweets.npy',allow_pickle='TRUE')
      log_ids  = log.tolist()
      aux2=[]
      for i in historial:
         if i._json['id_str'] in log_ids:
            break
         else:
            aux2.append(i)

      lg_ids = notes_tw(path1=path1,historial=aux2,path2=path2)
      for i in lg_ids:
         log_ids.append(i)
      np.save(path1+'log_tweets.npy', log_ids)



#path de donde se encuentran las variables de entorno
p1 = '/home/ghost/Desktop/proyectos/'
api = login(path_env=p1)


#puede hacerse un recorrido total 3200 (max) la primera vez
#y reducir dependiendo la frecuencia de tuits y perdiodo de 
#ejecuciones de este script. Se puede crear un log para revisar
#y ejecutar solo los nuevos.  


#pp1 muestra donde esta el log
#pp2 muestra donde estan las notas y screenshots (brain obsidian)

pp1 = '/home/ghost/Desktop/proyectos/obsnotes/notes/' 
pp2 = '/home/ghost/Desktop/mybrain/jcrespo/Twitter/' 



crear_notas(path1=pp1,path2=pp2)
