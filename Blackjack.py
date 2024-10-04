import random
import platform
import os
import sys

def clean(p): # fonction pour effacer l'affichage de la console
    """p is system/OS name"""
    commands = {"Windows": "cls", "Linux": "clear"}
    try:
        os.system(commands[p])
    except: # empty string or Java os name
        print(chr(27) + "[2J")

def dderejouer ():
    while True :
        replay = input ("\nVoulez-vous rejouer ? ")
        if replay.lower() == "non":
            joueur1.fintourdepioche=True
            joueur1.gameover = True
            print ("\nFin de partie")
            sys.exit()
            break
        elif replay.lower() == "oui":
            joueur1.fintourdepioche=True
            joueur1.main=[]
            joueur1.valeursmain=[]
            joueur1.valeurtotalemain = 0
            joueur1.mise = 0
            joueur1.blackjack = False
            joueur1.assurance = False
            croupier.main=[]
            croupier.valeursmain=[]
            croupier.valeurtotalemain = 0 
            croupier.blackjack = False
            clean(platform.system())                      
            break
        else:
            print("""\nMauvaise saisine, veuillez saisir "oui" ou "non".""")

class Joueur (object):
    def __init__(self, argent=100, mise=0, blackjack=False, assurance=False):
        self.argent = argent
        self.mise = mise
        self.main = []
        self.valeursmain = []
        self.valeurtotalemain = 0 
        self.gameover = False
        self.fintourdepioche =  False
        self.blackjack = blackjack
        self.assurance = assurance         
    def majvaleurmain(self): 
        """ 
            Méthode qui actualise la valeur de la main après une pioche.
            Elle permet également d'adapter la valeur de l'As (11 ou 1) selon que la valeur de la main dépasse 21 ou non :
                lorsque la valeur de la main dépasse 21 et qu'elle comporte un As, la valeur de cet As passe de 11 à 1
        """
        self.valeurtotalemain = sum(self.valeursmain)
        while self.valeurtotalemain > 21 and 11 in self.valeursmain:
            self.valeursmain.remove(11)
            self.valeursmain.append(1)
            self.valeurtotalemain = sum(self.valeursmain)    
    def firstpioche(self):
        cartepiochée1=random.choice(list(paquet.items()))
        del paquet[cartepiochée1[0]]
        cartepiochée2=random.choice(list(paquet.items()))
        del paquet[cartepiochée2[0]]
        self.main.append (cartepiochée1[0])
        self.main.append (cartepiochée2[0])
        self.valeursmain.append (cartepiochée1[1])
        self.valeursmain.append (cartepiochée2[1])                  
        self.majvaleurmain()        
        print("\nVous avez pioché les cartes %s et %s. La valeur de votre main est de %s" %(cartepiochée1[0], cartepiochée2[0], self.valeurtotalemain))
    def pioche(self):
        while self.fintourdepioche == False :
            cartepiochée=random.choice(list(paquet.items()))
            del paquet[cartepiochée[0]]
            self.main.append (cartepiochée[0])
            self.valeursmain.append (cartepiochée[1])
            self.majvaleurmain()             
            clean(platform.system())
            print("\nVous avez pioché la carte", cartepiochée[0])           
            if self.valeurtotalemain > 21 :
                if self.assurance :
                    self.argent -= int(1.5*self.mise)
                    print ("\nCramé ! La valeur de votre main est de %s.\n\nVous avez perdu %s euros (les %s euros de votre mise + les %s euros de l'assurance), votre cagnotte est de %s euros." %(self.valeurtotalemain, int(1.5*self.mise), self.mise, int(0.5*self.mise), self.argent))
                    dderejouer()
                else:
                    self.argent -= self.mise
                    print ("\nCramé ! La valeur de votre main est de %s.\n\nVous avez perdu le montant de votre mise de %s euros, votre cagnotte est de %s euros." %(self.valeurtotalemain, self.mise, self.argent))
                    dderejouer()          
            elif self.valeurtotalemain == 21:
                input ("\nBravo la valeur de votre main est de 21. Au croupier de jouer. Appuyez sur Entrée pour continuer")
                self.fintourdepioche = True                       
            else:
                print ("\nVotre main comporte les cartes suivantes: %s. La valeur de votre main est de %s" %(self.main, self.valeurtotalemain)) 
                while True :
                    choixpioche = input ("\nVoulez-vous piocher une carte supplémentaire (1) ou rester (2) ? ")
                    choixpioche = int(choixpioche)
                    if choixpioche == 1:
                        break
                    elif choixpioche == 2:
                        self.fintourdepioche = True
                        print ("Au tour du croupier !")
                        break
                    else : 
                        print("""\nMauvaise saisine ! Saisissez "1" pour piocher une carte supplémentaire ou "2" pour rester""" )

class Banque (Joueur):
    def __init__(self): # A priori cette ligne et la suivante sont inutiles car la classe dérivée Banque n'a pas d'attribut en plus de ceux de la classe Joueur
        Joueur.__init__(self)
    def firstpioche(self):
        cartepiochée1=random.choice(list(paquet.items()))
        del paquet[cartepiochée1[0]]
        cartepiochée2=random.choice(list(paquet.items()))
        del paquet[cartepiochée2[0]]
        self.main.append (cartepiochée1[0])
        self.main.append (cartepiochée2[0])
        self.valeursmain.append (cartepiochée1[1])
        self.valeursmain.append (cartepiochée2[1])         
        self.majvaleurmain()
        if self.valeurtotalemain != 21:        
            print("\nLe croupier a tiré la carte %s et une autre carte face cachée. La valeur connue de sa main est de %s" %(cartepiochée1[0], cartepiochée1[1]))
    def pioche(self):
        clean(platform.system())
        print ("\nLe croupier dévoile sa deuxième carte. Sa main comporte les cartes suivantes %s pour une valeur totale de %s" %(croupier.main, croupier.valeurtotalemain))
        if self.valeurtotalemain < 17:
            input ("\nAppuyez sur Entrée pour lancer le tour de pioche du croupier")   
            while self.valeurtotalemain < 17:            
                cartepiochée=random.choice(list(paquet.items()))
                del paquet[cartepiochée[0]]
                self.main.append (cartepiochée[0])
                self.valeursmain.append (cartepiochée[1])
                self.majvaleurmain()                
            else:
                clean(platform.system())                    
                print ("Le croupier a fini son tour de pioche, sa main comporte les cartes suivantes:", self.main)
                input ("\nAppuyez sur Entrée pour afficher le résultat de la partie ")
        if self.valeurtotalemain > 21:
            clean(platform.system())
            if joueur1.assurance:
                joueur1.argent += int(0.5*joueur1.mise)
                print ("Cramé ! La main du croupier %s est supérieure à 21 (%s), vous avez gagné !\nVous avez gagné %s euros (les %s euros de votre mise - les %s euros de l'assurance qui n'a pas été utilisée puisque le croupier n'a pas fait BLACKJACK), votre cagnotte est de %s euros" %(self.main, self.valeurtotalemain, int(0.5*joueur1.mise), joueur1.mise, int(0.5*joueur1.mise), joueur1.argent))
            else: 
                joueur1.argent += joueur1.mise
                print ("Cramé ! La main du croupier %s est supérieure à 21 (%s), vous avez gagné !\nVous avez gagné le montant de votre mise de %s euros, votre cagnotte est de %s euros" %(self.main, self.valeurtotalemain, joueur1.mise, joueur1.argent))                       
        else:
            if self.valeurtotalemain < joueur1.valeurtotalemain :
                clean(platform.system())
                if joueur1.assurance:
                    joueur1.argent += int(0.5*joueur1.mise)
                    print ("Bravo vous avez gagné ! La main du croupier comporte les cartes %s pour une valeur de %s inférieure à la vôtre (%s).\n\nVous avez gagné %s euros (les %s euros de votre mise - les %s euros de l'assurance qui n'a pas été utilisée puisque le croupier n'a pas fait BLACKJACK), votre cagnotte est de %s euros" %(self.main, self.valeurtotalemain, joueur1.valeurtotalemain, int(0.5*joueur1.mise), joueur1.mise, int(0.5*joueur1.mise), joueur1.argent))
                else :
                    joueur1.argent += joueur1.mise 
                    print ("Bravo vous avez gagné ! La main du croupier comporte les cartes %s pour une valeur de %s inférieure à la vôtre (%s).\n\nVous avez gagné le montant de votre mise soit %s euros, votre cagnotte est de %s euros" %(self.main, self.valeurtotalemain, joueur1.valeurtotalemain, joueur1.mise, joueur1.argent))                    
            elif self.valeurtotalemain == joueur1.valeurtotalemain :
                clean(platform.system())
                if joueur1.assurance:
                    joueur1.argent -= int(0.5*joueur1.mise)
                    print ("Egalité ! La main du croupier comporte les cartes %s pour une valeur égale à la vôtre (%s).\n\nVous conservez le montant de votre mise (%s) mais perdez celui de l'assurance (%s) puisque le croupier n'a pas fait BLACKJACK. Votre cagnotte est de %s euros" %(self.main, self.valeurtotalemain, joueur1.mise, int(0.5*joueur1.mise), joueur1.argent))
                else:                
                    print ("Egalité ! La main du croupier comporte les cartes %s pour une valeur égale à la vôtre (%s).\n\nVous conservez le montant de votre mise (%s), votre cagnotte est de %s euros" %(self.main, self.valeurtotalemain, joueur1.mise, joueur1.argent))                    
            else:
                clean(platform.system())
                if joueur1.assurance:
                    joueur1.argent -= int(1.5*joueur1.mise)
                    print ("Perdu ! La main du croupier (%s) est supérieur à la votre (%s).\n\nVous avez perdu %s euros (le montant de votre mise de %s euros + le montant de l'assurance (%s euros) puisque le croupier n'a pas fait BLACKCJACK). Votre cagnotte est de %s euros." %(self.valeurtotalemain, joueur1.valeurtotalemain, int(1.5*joueur1.mise), joueur1.mise, int(0.5*joueur1.mise), joueur1.argent))                        
                else:
                    joueur1.argent -= joueur1.mise 
                    print ("Perdu ! La main du croupier (%s) est supérieur à la votre (%s).\n\nVous avez perdu le montant de votre mise de %s euros, votre cagnotte est de %s euros." %(self.valeurtotalemain, joueur1.valeurtotalemain, joueur1.mise, joueur1.argent))                    
        dderejouer()
joueur1=Joueur()
croupier=Banque()

clean(platform.system())
print("Bienvenue dans le jeu du BlackJack")

while joueur1.gameover == False:
    paquet = {"As de coeur":11, "As de trèfle":11, "As de pique":11, "As de carreau":11, \
          "2 de coeur":2, "2 de trèfle":2, "2 de pique":2, "2 de carreau":2, \
          "3 de coeur":3, "3 de trèfle":3, "3 de pique":3, "3 de carreau":3, \
          "4 de coeur":4, "4 de trèfle":4, "4 de pique":4, "4 de carreau":4, \
          "5 de coeur":5, "5 de trèfle":5, "5 de pique":5, "5 de carreau":5, \
          "6 de coeur":6, "6 de trèfle":6, "6 de pique":6, "6 de carreau":6, \
          "7 de coeur":7, "7 de trèfle":7, "7 de pique":7, "7 de carreau":7, \
          "8 de coeur":8, "8 de trèfle":8, "8 de pique":8, "8 de carreau":8, \
          "9 de coeur":9, "9 de trèfle":9, "9 de pique":9, "9 de carreau":9, \
          "10 de coeur":10, "10 de trèfle":10, "10 de pique":10, "10 de carreau":10, \
          "Valet de coeur":10, "Valet de trèfle":10, "Valet de pique":10, "Valet de carreau":10, \
          "Dame de coeur":10, "Dame de trèfle":10, "Dame de pique":10, "Dame de carreau":10, \
          "Roi de coeur":10, "Roi de trèfle":10, "Roi de pique":10, "Roi de carreau":10}
    joueur1.fintourdepioche=False    
    print ("\nNouvelle partie !")
    if joueur1.argent == 0 :
        input ("\nVous n'avez plus d'argent ! La Banque est généreuse et vous redonne 100 euros. Appuyez sur Entrée pour continuer")
        joueur1.argent += 100   
    while True :
        try:
            joueur1.mise=input("\nVous avez %s euros, combien voulez-vous miser ? " %(joueur1.argent))        
            joueur1.mise = int(joueur1.mise)
        except ValueError:
            clean(platform.system())
            print ("\nErreur de saisine ! Veuillez saisir un nombre entier compris entre 0 (non inclus) et %s (montant de votre cagnotte)" %(joueur1.argent))
            continue
        if joueur1.mise > joueur1.argent:
            clean(platform.system())
            print ("\nVous n'avez pas assez d'argent dans votre cagnotte, vous pouvez miser %s euros maximum" %(joueur1.argent))
            continue  
        elif joueur1.mise <= 0 :
            clean(platform.system())
            print ("\nVeuillez saisir un nombre supérieur à 0")
            continue
        else:
            break
    input ("\nAppuyez sur Entrée pour démarrer le premier tour de pioche ")
    clean(platform.system())
    joueur1.firstpioche()    
    croupier.firstpioche()
    if joueur1.valeurtotalemain == 21 and len(joueur1.main) == 2:
        joueur1.blackjack=True
        input ("\nBLACKJACK ! Bravo la valeur de votre main est de 21 avec seulement 2 cartes ! Découvrons la main du croupier. Appuyez sur Entrée pour continuer ")
    if croupier.valeurtotalemain == 21 and len(croupier.main) == 2: 
        croupier.blackjack=True
    if joueur1.blackjack:
        if croupier.valeursmain[0] == 11 :
            while True:
                takeinsurance=input ("\nLa première carte du croupier est un As ! Voulez-vous prendre l'assurance pour %s euros (la moitié de votre mise) ? " %(int(0.5*joueur1.mise)))
                if takeinsurance.lower() == "non":
                    input ("\nVous avez refusé l'assurance, appuyez sur Entrée pour continuer")
                    break
                elif takeinsurance.lower() == "oui":
                    joueur1.assurance=True                    
                    break
                else:
                    print("""\nMauvaise saisine, veuillez saisir "oui" ou "non".""")
        if croupier.valeurtotalemain == 21 and len(croupier.main) == 2:  
            if joueur1.assurance:
                joueur1.argent += joueur1.mise
                print ("\nEgalité ! Pas de chance, le croupier fait également BLACKJACK (avec %s) !\n\nVous gagner deux fois le montant de l'assurance soit %s euros, votre cagnotte est de %s euros" %(croupier.main,joueur1.mise, joueur1.argent))                
            else:          
                print ("\nEgalité ! Pas de chance, le croupier fait également BLACKJACK (avec %s) !\n\nVous conservez le montant de votre mise (%s), votre cagnotte est de %s euros" %(croupier.main,joueur1.mise, joueur1.argent))
        else:
            if joueur1.assurance:
                joueur1.argent += joueur1.mise
                print ("\nVoici la main du croupier : %s. Bravo vous gagnez avec un BLACKJACK !\n\nVous remportez 1,5 fois votre mise soit %s euros mais perdez le montant de l'assurance (%s euros) puisque le croupier n'a pas fait BLACKJACK, votre cagnotte est de %s euros" %(croupier.main, int(1.5*joueur1.mise), int(0.5*joueur1.mise), joueur1.argent))
            else:
                joueur1.argent += int(1.5*joueur1.mise)
                print ("\nVoici la main du croupier : %s. Bravo vous gagnez avec un BLACKJACK !\n\nVous remportez 1,5 fois votre mise soit %s euros, votre cagnotte est de %s euros" %(croupier.main, int(1.5*joueur1.mise), joueur1.argent))
    if croupier.valeursmain[0] == 11 and not joueur1.blackjack :
        while True:
            takeinsurance=input ("\nLa première carte du croupier est un As ! Voulez-vous prendre l'assurance pour %s euros (la moitié de votre mise) ? " %(int(0.5*joueur1.mise)))
            if takeinsurance.lower() == "non":
                input ("\nVous avez refusé l'assurance, appuyez sur Entrée pour continuer")
                break
            elif takeinsurance.lower() == "oui":
                joueur1.assurance=True                    
                break
            else:
                print("""\nMauvaise saisine, veuillez saisir "oui" ou "non".""")
    if croupier.blackjack and not joueur1.blackjack :
        if joueur1.assurance:            
            print ("\nPerdu ! Le croupier a pioché les cartes %s et fait un BLACKJACK !\n\nComme vous avez pris l'assurance, vous ne perdez pas d'argent ! Votre cagnotte est de %s euros" %(croupier.main, joueur1.argent))
        else:           
            joueur1.argent -= joueur1.mise            
            print ("\nPerdu ! Le croupier a pioché les cartes %s et fait un BLACKJACK !\n\nVous perdez votre mise de %s euros, votre cagnotte est de %s euros" %(croupier.main, joueur1.mise, joueur1.argent))            
    if not joueur1.blackjack and not croupier.blackjack :
        while True:
            try:
                choixpioche=input ("\nVoulez-vous piocher une carte supplémentaire (1) ou rester (2) ? ")        
                choixpioche = int(choixpioche)
            except:
                print("""\nMauvaise saisine ! Saisissez "1" pour piocher une carte supplémentaire ou "2" pour rester""" )
                continue
            if choixpioche == 1:
                joueur1.pioche()
                break
            elif choixpioche == 2:
                print ("\nAu tour du croupier !")
                break
            else : 
                print("""\nMauvaise saisine ! Saisissez "1" pour piocher une carte supplémentaire ou "2" pour rester""" )
        if joueur1.valeurtotalemain != 0 :
            croupier.pioche()
    if joueur1.valeurtotalemain != 0:
        dderejouer()