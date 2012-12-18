#! /usr/bin/env python

# vous avez deformez mes propos je n'ai pas de problemes
# pour travailler  avec qui que ce soit ,
# Pour Me faire pardonner cependant j'ai ecrit un progrmme
# qu j'ai appele balance :) j'aime bien ce nom
# L'idee est de faire travailler trois machines ensembles
# sans qu'ils ne s'entretuent.

# La machine1 prends des sacs en entree , ensuite elle depose
# les sacs/fichiers dans  un seau1 , et la machine 3 les prends
# dans le seau1 et les depose dans le seau2


# python balance.py

import Queue
import thread , time
from threading import RLock
import threading 
class Humain3:
    def __init__(self , manager):
      self.manager =manager

    def run(self):
      while self.manager.run:
          with self.manager.verrou:
             
              try:
                  sac =self.manager.seau2.get(block =False)
              except Queue.Empty:
                  # le seau est vide
                  print 'seau2 vide'
                  pass
              else:
                  print(''' la machine 3 prend
                    le sac depose par la machine2
                    dans le sceau2
                   ''')
                  print 'sac =',sac
                  try:
                      self.manager.seau3.put(sac)
                  except Queue.Full:
                       # le seau est plein
                       pass
          # nous attendons encore 10 secondes
          # pour voir encore si la machine 2
          # a fait un depot  dans l seau2
          self.manager._wait(10)
      print('''
              Humain3 a fini son travail
              ''')     
class Humain2:
    def __init__(self, manager):
        self.manager =manager
        
    def run(self):
        while self.manager.run:
          with self.manager.verrou:
             
              try:
                  sac = self.manager.seau1.get(block =False)
                 
              except Queue.Empty:
                  # le seau est vide
                  print 'seau1 vide'
              else:
                  # Nous avons un sac on le depose
                  # dans le seau2 pour que la machine
                  # 2 puisse le prenre :)
                  print(''' la machine 2 prend
                   le sac depose par la machine1
                        dans le sceau1
                   ''')
                  print 'sac =',sac
                  try:
                      self.manager.seau2.put(sac)
                  except Queue.Full:
                      # Le seau2 est plein  ce
                      # n'est pas grave , on repasse
                      pass
                    
          # nous attendons encore 10 secondes
          # pour voir encore si la machine 1
          # a fait un depot 
          self.manager._wait(10)
             
        print('''
              Humain2 a fini son travail
              ''')           
class Humain1:
    # La machine une se charge de prendre  le sacs en entre
    # et la depose dans le sceau1 pour la machine 2


    def _wait(self, timee):
            time.sleep(timee)
            
    def __init__(self):
        self.seau1 = Queue.Queue()
        self.seau2 = Queue.Queue()
        self.seau3 = Queue.Queue()
        self.verrou= RLock()
        
        self.run   = True
        #thread.start_new_thread(Humain3(manager =self))

    def loop(self):
        t2 = threading.Thread(target =\
                              Humain2(manager =self).run, name ="t2", args=())
        t2.daemon = True
        t2.start()
        t3 = threading.Thread(target =\
                              Humain3(manager =self).run, name ="t3", args=())
        t3.daemon = True
        t3.start()
        print('''
                  Humain1 commence son travail
                  ''')
        while True:
            with self.verrou:
                try:
                    sac =raw_input('un sac :')
                    if sac =='o':
                        self.run =False
                        self._wait(10)
                        break
                    self.seau1.put(sac)
                except KeyboardInterrupt, e:
                    self.run =False
                   
                    # Attends 10 senconde le temps que tous
                    # les humains finissent leu job
            self._wait(10)
        print('''
                  Humain1 a fini son travail
                  ''')
        # Le travail de tout le monde est a present
        # termine on affiche pour voir si l humain 3
        # a fin son travail et que toute la chaine
        # a bien fait le taff
        print ('''contenu du sac 3 de
              l humain3 ''')
        while True:
             try:
                print self.seau3.get(block =False)
             except Queue.Empty:
                break
if __name__ =="__main__":
     Humain1().loop()
    

