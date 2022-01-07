import random #importing Math class


mutationRate = 20
mutationIntensity = 3
class Zoob:
	#Traits of a Zoob
	#//Food Rules
	#// Food < .5 --> chance of survival, no reproduction
	#// .5 <= Food < 1 ---> Survival, chance of reproduction if > .5
	#// Food >=1 ---> Reproduction, chance of multiple offspring
    #Enviornmentvariable
    #//Traits
	#altruism#//1 =  altruistic, looks to give food to other zoobs before mating, 2 = indifferent, searches whole pool for mates and doesnt donate, 3 = searches through pool of people with enough food to survive
	#socialSkills# // 1-100 chance that this creature will fuck another creature and attempt to reproduce. say if you have a low chance you may go thru array and not find a parter becuase your social skills too weak
	#speed# //1-100 speed of a zoob, high speed goes out to find food before slower zoobs and has a higher chance (more food needed for higher speed)
	#size #//1-100 size of a zoob, more food needed the bigger it is, also higher chance of winning fights
	#vision# //1-100 higher chance to find food 
	#aggression#// 1-100 chance of fighting if mate is not suitable
	#//Zoob Metrics
	#timeAlive #//how many turns the zoob has been alive
	#food #//creatures who dont find a mate save their excess food
	#foodRequired #// amoutn of food needed to survive, determine at birth by traits #randominit
    def __init__(self, parentA = None, parentB = None):
        if parentA == None:
            #no parents passed, created from nothing
            self.altruism = random.randint(1,3)
            #  random.randint(1,3)
            self.socialSkills = random.randint(1,100)
            self.speed = random.randint(1,100)
            self.size = random.randint(1,100)
            self.vision = random.randint(1,100)
            self.aggression = random.randint(1,100)
            #self.libido = randint(1,10)######################NEWEST FEATUREEEEEE: HOW MANY TIMES THEY TRY TO MATE, WILL ALSO TAKE PARENTS GENE AND MUTATE, SHOULD ALSO MAKE IT LESS LIKELY TO BEAT UP ANOTHER ZOOB, THEY LOWKEY MERCIN EACH OTHER
            #//Metrics
            self.timeAlive = 0
            self.food = 0.0
            self.foodRequired = (self.speed+self.size)/100#//to survive
            self.isBeaten = False
        else:##Is child
            #//Constructor with two parent args
            #Mutation threshold
            self.altruism = random.choice([parentA.altruism,parentB.altruism])
            self.socialSkills = self.mixTrait(parentA.socialSkills,parentB.socialSkills)
            self.speed = self.mixTrait(parentA.speed,parentB.speed)
            self.size = self.mixTrait(parentA.size,parentB.size)
            self.vision = self.mixTrait(parentA.vision,parentB.vision)
            self.aggression = self.mixTrait(parentA.aggression,parentB.aggression)
            #//Metrics
            self.timeAlive = 0
            self.food = 0.0
            self.foodRequired=(self.speed+self.size)/100#//to survive not  
            self.isBeaten = False
            #//end constructor
    def isStarving(self):
        if self.food >= self.foodRequired: #has enough food to survive or more
            #print("Not Starving","-Food:",self.food," -Required:",self.foodRequired)
            return False
        else: #doesnt have enough food to survive
            #print("Died of starving","-Food:",self.food," -Required:",self.foodRequired)
            return True
    ####Every iteration of the sim, if isstarving and some threshold of having a kid is satisfied run mate on all zoob in lists
    def addFood(self, foodAdded):
        self.food = self.food + foodAdded
        return
    def age(self):
        if self.isStarving(): #dies from starvation
            #print("Died of starvingAGE","-Food:",self.food," -Required:",self.foodRequired," -isStarving:",self.isStarving())
            return False#die
        elif self.isBeaten: #dies from beaten
            #print("died of getting his shit kicked in")
            return False#die
        else: #lives
            #print("Not StarvingAGE","-Food:",self.food," -Required:",self.foodRequired," -isStarving:",self.isStarving())
            self.food = self.food - self.foodRequired #Eat
            self.timeAlive = self.timeAlive + 1 #Age
            return True#survive
    def mate(self, zoobList):#Zoob[] //mating loop
        #asks if zoob is starving. if it is, it doesn't look for a mate
        if self.isStarving():
            return None #returns false when starving, no baby
        
        foundMate = False
        #theMate#Zoob
        if (self.altruism == 1):#//prefer those that dont have enough
            for zoob in zoobList:
                if not foundMate:
                    if zoob.isStarving() and (self.food > self.foodRequired):#//prefers to share with starving, can only share if it has enough to share
                        if self.tryMate(zoob):#//tests compatability
                            foundMate = True
                            theMate = zoob#//stores mate
                            break
            if not foundMate:#//give up on finding a starving mate
                for zoob in zoobList:
                    if not zoob.isStarving():
                        if self.tryMate(zoob):#//tests compatability
                            foundMate = True
                            theMate = zoob#//stores mate
                            break
        elif self.altruism == 3:#//prefers those that have enough food
            for zoob in zoobList:
                if not foundMate:
                    if not zoob.isStarving():#//prefers non starving
                        if self.tryMate(zoob):#//tests compatability
                            foundMate = True
                            theMate = zoob#//stores mate
                            break#//leave for
            if not foundMate:#//give up on finding a healthy mate
                for zoob in zoobList:#//looks for any mate
                    if zoob.isStarving() and (self.food > self.foodRequired): #decides to mate with starving one, only if it has enough food to share:
                        if self.tryMate(zoob):#//tests compatability
                            foundMate = True
                            theMate = zoob#//stores mate
                            break#//    leave for
        else:#//    doesnt care
            for zoob in zoobList:
                if not foundMate:
                    if self.tryMate(zoob):#//tests compatability
                        if not zoob.isStarving(): #finds a mate as long as it is not starving, or if it is starving and we have extra to give. prevents something with no excess mating with starving creature
                            foundMate = True
                            theMate = zoob#//stores mate
                            break#//    leave for
                        elif zoob.isStarving() and (self.food > self.foodRequired):
                            foundMate = True
                            theMate = zoob#//stores mate
                            break#//    leave for
        if foundMate:#//            found mate in whole array?
            return self.haveChild(theMate)#//   try to have child(ren)
        return None
    def tryMate(self, potentialMate):#  //check compatability of mates
        liklihood = int((self.socialSkills + potentialMate.socialSkills)/2)#//the avg btwn range 1-x
        test = random.randint(1, 100)#  //the actualy case in which they mate
        if test <= liklihood:#//        if case between [1:x], sucess. If case between (x:100], fail.
            #print("maybe bbaby")
            return True
        #A Challenger approaches...
        #if random.randint(1, 100) <= self.aggression:
            ##self.takeFood(potentialMate)#//If zoob that failed to mate is aggresive than fight bad mate
            ##print("no bab + punch")
        return False
    def takeFood(self, failedMate):#        //steal food of failed mate depending on aggression
        if self.size+self.speed >= failedMate.size+failedMate.speed:#//clash between zoob
            self.food = self.food + failedMate.food#  //adds their food to their pile
            failedMate.food = 0#            //leaves them nothing
        else:
            failedMate.food = failedMate.food + self.food#//adds the host Zoobs food to their pile
            failedMate.food = 0#           //leaves the host Zoob nothing
        return#///potentially kill them in which case they get deleted from array   MUST RETURN FALSE OR SOME KILL VALUE ######## IF KILLED CHANGE IS BEATEN BOOLEN TO TRUE WHICH IS EVALUATED ON AGING PROCESS(dies)
    def haveChild(self, mate):
        selfExcess = 0 #self excess food --- self is at least not starving becuase of if statement at top of mate
        mateExcess = 0  #mates excess food --- mate could be starving, is likely for alturistic zoobs searching
        excessFood = 0  #total partnership excess food
        if mate.isStarving(): #the zoob that has been chosen to mate with is starving. give it food
            selfExcess = self.food - self.foodRequired #finds excess of self
            self.food = self.food - selfExcess #removes excess from self.food
            mate.food = mate.food + selfExcess #gives the excess to the mate
            selfExcess = 0 #resets selfExcess since it is empty now
            mateExcess = mate.food - mate.foodRequired #find the excess of the mate, now that the self has donates all excess to it
            if mateExcess > 0: #mate has excess. there is excess in the partership. may try for a baby
                excessFood = mateExcess #sets the excess of the partnership, doesnt add selfExcess because it is empty
                mate.food = mate.food - mateExcess #removes the excess from the mate. now both foods are updated, and the food to make a baby is stored in excessFood
            else: #after donation by self, mate is still starving. set all excess to 0. no baby. self simply donated to mate
                excessFood = 0
                mateExcess = 0
        else: #mate is not starving. this means that both parties at least have enough food to survive.
            selfExcess = self.food - self.foodRequired #finds excess in self, has a minimum of 0
            mateExcess = mate.food - mate.foodRequired #finds excess in mate, minimum of 0
            excessFood = selfExcess + mateExcess #finds total excess in partnership
            if excessFood > 0: #if there is any excess food in the partnership to try for a kid
                self.food = self.food - selfExcess #remove self excess from selffood
                mate.food = mate.food - mateExcess #remove mate exces from matefood

        if excessFood > 0.0:#//if surplus of food is great enough, attempt child
            chance = int(excessFood*50)#casts excess food to int, having twice the food required(or greater) means 100% chance to reproduce:
            if chance > random.randint(1,int((self.foodRequired + mate.foodRequired)*50)):
                if excessFood > (self.foodRequired + mate.foodRequired): #there is enough leftover food to give each a days worth of extra
                    self.food = self.food + self.foodRequired #gives self an extra day of food
                    mate.food = mate.food + mate.foodRequired #gives mate an extra day of food
                    excessFood = excessFood - self.foodRequired - mate.foodRequired #subrtacts the removals from excessFood
                    self.food = self.food + excessFood #gives remaining excess to self
                else: #not enough, randomly splits food up between the two
                    foodPortion = random.randint(1,int(excessFood*100))
                    self.addFood(foodPortion/100)
                    mate.addFood((excessFood-foodPortion)/100)
                #print("had Babb")
                return self.createChild(mate)#creates child and returns it to be passed up via the mate call
            #//if sucess
            ##//create child with genevariance specified by enviornment, run createChild(), append to list
            return None
    def createChild(self, mate):
        return Zoob(parentA=self,parentB=mate)
    def mixTrait(self, parentATrait, parentBTrait):
        mixGene=(parentATrait + parentBTrait)/2
        if random.randint(1, 100) < mutationRate:#will Mutate, mutation rate is a threshold between 1,100 if 1 no mutation, if 100 always mutate
            mixGene = mixGene+random.randint(-1*mutationIntensity, mutationIntensity)#mutated gene
            if mixGene>100:
                mixGene = 100
            elif mixGene<1:
                mixGene = 1
        return mixGene
    def __lt__(self, other):
        return self.speed > other.speed#.sort will sort based on speed
    def printStats(self):
        print('Altruism:',str(self.altruism),' Social:',str(self.socialSkills),' Speed',str(self.speed),' Size:',str(self.size),'Vision:',str(self.vision),'Agression:',str(self.aggression),' Time Alive:',str(self.timeAlive),' Food:',str(self.food),' Food Required:',str(self.foodRequired))
        return
    def copyZoob(self):
        copy = Zoob()
        copy.altruism = self.altruism
        copy.socialSkills = self.socialSkills
        copy.speed = self.speed
        copy.size = self.size
        copy.vision = self.vision
        copy.aggression = self.aggression
        copy.foodRequired = self.foodRequired
        return copy
        
    def __copy__(self):
        return copyZoob