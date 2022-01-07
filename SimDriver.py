import random
from Zoob import Zoob

#Global variables
findFoodChallenge = 10 #how much harder it becomes to find food each iteration of searching(can search a max of 10 rounds)
#Arrays to store statistics of each iteration to print to a file
fileNumAlive = []
fileAltOne = []
fileAltTwo = []
fileAltThree = []
fileMedianAlt = []
fileAvgSocial = []
fileAvgSpeed = []
fileAvgSize = []
fileAvgVision = []
fileAvgAggr = []
fileAvgFoodReq = []
fileAvgTimeAlive = []
    
def main():
    #variables
    iterations = 100#  how many iterations to run the simulation
    zoobNumber = 50#    how many zoobs the simulation starts with
    envFood = 500#   how much food the enviornment starts with
    endFoodTrend = 1#trend of food every iteration UNUSED RN
    zoobList = generateZoobArray(zoobNumber,False)#array of randomized zoobsalso accepts maybe shared ancestor?
    firstIteration = True
    
    for i in range(iterations+1):
        #####BEGINNING OF SIM ITERATION
        if firstIteration == True:
            printStatistics(zoobList,i,100) #prints first untouched array before anything happens
            firstIteration = False
            i = 1
        #looks for food
        zoobList = lookForFood(zoobList,envFood)
        #looks for mates, steals food, prioritizes the starving/nonstarving, and/or has children
        zoobList,babyList = lookForMate(zoobList)
        #Time passes, starving or beaten culled, age increases by one
        zoobList,survivalRate = timePass(zoobList)
        #add babys to new generation
        for Zoob in babyList:
            zoobList.append(Zoob)
        #####END OF SIM ITERATION
        #DATA: Display stats
        #if list is empty, say that they are all dead and stop simulating
        if len(zoobList) == 0:
            print("They're all dead whoops")
            i = iterations + 1
            return
        printStatistics(zoobList,i,survivalRate)#prints data after iteration
 
#prints all the zoobs out from zoobList 
def printAllZoobs(zoobList):
    for Zoob in zoobList:
        Zoob.printStats()
   
#writes the averages of each iteration into an excel file   
def writeToExcel(zoobList):
    return True
    
#prints out relevent statistics of list of zoobs, i = iteration number, also puts statistics into global arrays to be printed
def printStatistics(zoobList,i,survivalRate):
    #Variables (all are counters to find statistics, except for number alive)
    numberAlive = len(zoobList)
    altOneCount = 0
    altTwoCount = 0
    altThreeCount = 0
    medianAltruism = 0
    avgSocial = 0
    avgSpeed = 0
    avgSize = 0
    avgVision = 0
    avgAggression = 0
    avgFoodRequired = 0
    avgTimeAlive = 0
    
    for Zoob in zoobList:#goes thru list to add everything
        if Zoob.altruism == 1:
            altOneCount = altOneCount + 1
        elif Zoob.altruism == 2:
            altTwoCount = altTwoCount + 1
        else:
            altThreeCount = altThreeCount + 1
        
        avgSocial = avgSocial + Zoob.socialSkills
        avgSpeed = avgSpeed + Zoob.speed
        avgSize = avgSize + Zoob.size
        avgVision = avgVision + Zoob.vision
        avgAggression = avgAggression + Zoob.aggression
        avgFoodRequired = avgFoodRequired + Zoob.foodRequired
        avgTimeAlive = avgTimeAlive + Zoob.timeAlive
    
    #finds averages for everything
    avgSocial = avgSocial/numberAlive
    avgSpeed = avgSpeed/numberAlive
    avgSize = avgSize/numberAlive
    avgVision = avgVision/numberAlive
    avgAggression = avgAggression/numberAlive
    avgFoodRequired = avgFoodRequired/numberAlive
    avgTimeAlive = avgTimeAlive/numberAlive
    if altOneCount >= altTwoCount:
        if altThreeCount > altOneCount:
            medianAltruism = 3
        else:
            medianAltruism = 1
    else:
        if altThreeCount > altTwoCount:
            medianAltruism = 3
        else:
            medianAltruism = 2
 
    #adds everything to the global arrays to be printed to a file after
    fileNumAlive.append(numberAlive)
    fileAltOne.append(altOneCount)
    fileAltTwo.append(altTwoCount)
    fileAltThree.append(altThreeCount)
    fileMedianAlt.append(medianAltruism)
    fileAvgSocial.append(avgSocial)
    fileAvgSpeed.append(avgSpeed)
    fileAvgSize.append(avgSize)
    fileAvgVision.append(avgVision)
    fileAvgAggr.append(avgAggression)
    fileAvgFoodReq.append(avgFoodRequired)
    fileAvgTimeAlive.append(avgTimeAlive)
    
    #prints the results
    print("Iteration: ",i,"(Number Alive): ",numberAlive,"(AvgSocial): ",round(avgSocial,3),"(AvgSpeed): ",round(avgSpeed,3),"(AvgSize): ",round(avgSize,3),"(AvgVision): ",round(avgVision,3),"(AvgAggression): ",round(avgAggression,3),"(AvgFoodRequired): ",round(avgFoodRequired,3),"(AvgTimeAlive): ",round(avgTimeAlive,3),"(Survival Rate): ",round(survivalRate,3),"%","Altruistic: ",altOneCount,"Indifferent: ",altTwoCount,"Selfish: ",altThreeCount)

#generates an array of zoobs of size zoobNumber. If you want them to be identical, enter a sharedAncestor
def generateZoobArray(zoobNumber,sharedAncestor):
    print("Generating initial population...")
    zoobList = []
    if sharedAncestor:
        ancestor = Zoob()
        #ancestor.printStats()##DEBUG
        for i in range(zoobNumber):
            newBabyZoobie = ancestor.copyZoob()
            zoobList.append(newBabyZoobie)
    else:
        for i in range(zoobNumber):
            newBabyZoobie = Zoob()
            #newBabyZoobie.printStats()##DEBUG
            zoobList.append(newBabyZoobie)
    print("Done generation initial population...")
    return zoobList
    
#has zoobList look for food in an environment with envFood amount of food
def lookForFood(zoobList,envFood):
    #Sort array in ascending order by speed
    zoobList.sort()
    #goes through the list looking for food
    for Zoob in zoobList:
        if envFood == 0:#no more food, stop letting zoobs look
            return zoobList
        else:
            isLooking = True#stops looking once it has enough food or cant find any, having enough is any value that means its not starving
            roundOfSearching = 0
            while isLooking:
                #if not Zoob.isStarving:
                #   print(Zoob.food,'/',Zoob.foodRequired)
                #  isLooking = False#done looking for food
                chance = random.randint(1,100)+(findFoodChallenge*roundOfSearching)#     if vision greater, then Zoob finds food, gets harder 
                if Zoob.vision > chance:#      --> zoob is getting munchies today baby
                    foodCarryCap = random.randint(int((Zoob.size+Zoob.speed)/2),int(Zoob.size+Zoob.speed))/100#   zoob can carry its size to max size ratio in food (largest can carry 1.0 food), smallest can carry .01 food #MAKE THIS A VARIABLE RANGE
                    if (envFood - foodCarryCap) > 0:#   enough food to be taken
                        Zoob.addFood(foodCarryCap*2) 
                        envFood= envFood-foodCarryCap
                    else:#could still carry more food
                        Zoob.addFood(envFood)
                        envFood=0
                        isLooking = False#no more food
                else:
                    isLooking = False#failed to find more food(thinks no more food is out there)
                roundOfSearching = roundOfSearching + 1
    #Has updated all Zoobs in Zoob list with their food
    return zoobList

#has the zoobs in zoobList look for a mate
def lookForMate(zoobList):
    newZoobGeneration=[]#new gen of Zoobs
    if zoobList == None:
        print("somethings wrong! got passed an embty zooblist at line 64 of SimDriver:lookForMate")#error print
    for Zoob in zoobList:
        babyZoob = Zoob.mate(zoobList)#returns baby Zoob if created, Nonetype object if failure to mate
        if babyZoob != None:
            newZoobGeneration.append(babyZoob)#adds new bby Zoob to new generation(cannot be mated with yet)
    return zoobList,newZoobGeneration#returns zoobs and baby zoobs in a seperate array, to be only added once the iteration ends(aging is called)

#signals a new iteration of the simulation and ages the zoobs who survive, removes dead zoobs from array
def timePass(zoobList):
    #Death counter used to find survival rate over each iteration
    deathCounter = 0
    initialPopulation = len(zoobList)
    newZoobs = zoobList.copy()
    for i in reversed(range(len(zoobList))):#starts from back as to not miss index(when deleted)
        currentZoob = zoobList[i]
        if currentZoob.age() == False:#if Zoob dies
            deathCounter = deathCounter + 1
            newZoobs.pop(i)
        else: #zoob dont die   
           newZoobs[i].age()
           
    stillAlive = initialPopulation-deathCounter
    survivalRate = (stillAlive/initialPopulation) * 100
    return newZoobs,survivalRate

if __name__ == "__main__":
    main()