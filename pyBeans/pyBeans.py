# TODO:
# currently, players don't keep track of what type of full box comes out
# only unbroken lines of THEIR type count


import random,copy

FULL_BOX = 1
EMPTY_BOX = 0

num_trials = 100 # number of trials in an experiment

#payoffs
empty_empty = -1
empty_full  = 1 # My partner gets a full, unmixed box
full_empty  = 1 # I get a full, unmixed box
full_full   = -2

whole_order = 6 # I get a whole order
whole_order_partner = 6 #My partner gets a whole order

empty_box_breaks_order_chain = True # does an empty box break an order chain?

MAX_ORDER = 9 # maximum order size
MIN_ORDER = 1

##############
# Main Class #
##############
class JellyBeaner:

	def __init__(self,strat,num_orders=1000,ind=0,num_rounds=100):
		self.strategy = strat
		self.orders = [random.randint(MIN_ORDER,MAX_ORDER) for i in range(num_orders)]
		self.money = 0
		self.index = ind # index for finding self in history
		self.ordersCompleted= 0
		self.curUnbrokenOrders = 0
		self.num_rounds = num_rounds
		
	def getOrders(self):
		return self.orders
		
	def getThisOrder(self):
		return self.orders[self.ordersCompleted]
	
	def getcurUnbrokenOrders(self):
		return self.curUnbrokenOrders
		
	def resetcurUnbrokenOrders(self):
		self.curUnbrokenOrders = 0
	
	def addOrder(self):
		self.curUnbrokenOrders +=1
		
	def completeOrder(self):
		self.ordersCompleted += 1
		self.resetcurUnbrokenOrders()
    	
	def choose(self,history):
		return self.strategy(self,history)
		
	def addMoney(self,m):
		self.money += m
		
	def getMoney(self):
		return self.money

	def getMyPlays(self,history):
		return [x[0][self.index] for x in history]

	def getPartnersPlays(self,history):
		# assumes only two players
		return [x[0][(self.index+1) % 2] for x in history]
	
	def getMyOrderCompletes(self,history):
		return [x[1][self.index] for x in history]

def findMedian(X):
	y = copy.deepcopy(X)
	sorted(y)
	

##############
# Strategies #
##############
def allCoop(self, history):
	return EMPTY_BOX
	
def allDef(self, history):
	return FULL_BOX
	
def TitForTat(self, history):
	# cooperate on first go
	if len(history)==0:
		return EMPTY_BOX
	# echo partner's last go
	else:
		return self.getPartnersPlays(history)[-1]
		
def TitForTatOp(self, history):
	# Plays opposite of last player's go
	if len(history)==0:
		return EMPTY_BOX
	# echo partner's last go
	else:
		return (1 + self.getPartnersPlays(history)[-1]) %2
		
def TitFor2Tats(self, history):
	# cooperate on first go
	if len(history)==0:
		return EMPTY_BOX
		
	if self.getPartnersPlays(history)[-2:] == [EMPTY_BOX,EMPTY_BOX]:
		return EMPTY_BOX
	else:
		return FULL_BOX
		
def TitFor2TatsOp(self, history):
	# cooperate on first go
	if len(history)==0:
		return EMPTY_BOX
		
	if self.getPartnersPlays(history)[-2:] == [EMPTY_BOX,EMPTY_BOX]:
		return FULL_BOX
	else:
		return EMPTY_BOX

def GrimTrigger(self,history):
	if len(history)==0:
		return EMPTY_BOX
	if FULL_BOX in self.getPartnersPlays(history):
		return FULL_BOX
	else:
		return EMPTY_BOX
		
def GrimTriggerOp(self,history):
	if len(history)==0:
		return FULL_BOX
	if FULL_BOX in self.getPartnersPlays(history):
		return EMPTY_BOX
	else:
		return FULL_BOX
		
def Gradual(self,history):
	if len(history)==0:
		self.Gradual_punishMoves = 0
		return EMPTY_BOX
	if self.Gradual_punishMoves>0:
		self.Gradual_punishMoves -= 1
		return FULL_BOX
		
	if not FULL_BOX in self.getPartnersPlays(history):
		return EMPTY_BOX
	else:
		if self.getPartnersPlays(history)[-1] == FULL_BOX:
			self.Gradual_punishMoves = sum([1 for x in self.getPartnersPlays(history) if x==FULL_BOX])-1
			return FULL_BOX
	return EMPTY_BOX
		
		
def AdaptiveTitForTat(self,history):
	if len(history)==0:
		self.ATFT_word = 0
		self.ATFT_r = 0.1
		return FULL_BOX
	if self.getPartnersPlays(history)[-1] == EMPTY_BOX:
	#If (opponent played C in the last cycle) then
		#world = world + r*(1-world), r is the adaptation rate
		self.ATFT_word += r*float(1.0-self.ATFT_word)
	else:
		self.ATFT_word += r*float(0.0-self.ATFT_word)
	if self.ATFT_word >= 0.5:
		return EMPTY_BOX
	else:
		return FULL_BOX
	
def TurnsAtTalk(self,history):
	# Keep sending full boxes until an order is complete
	# or partner interrupts
	# then let your partner go
	
	# First, go randomly
	if len(history)==0:
		return random.choice([EMPTY_BOX,FULL_BOX])
	
	# get recently completed orders
	compHist = self.getMyOrderCompletes(history)[-1:]
	if len(history)>1:
		compHist = self.getMyOrderCompletes(history)[-2:]

	if 1 in compHist:
		# If I've completed an order in last two goes,
		# then, play an empty box
		return EMPTY_BOX
	elif self.getPartnersPlays(history)[-1]==FULL_BOX:
		# If my partner is still 'talking', let him go
		return EMPTY_BOX
	else:
		return FULL_BOX
		

def TurnsAtTalkHard(self,history):
	# Keep sending full boxes until an order is complete, then let your partner go
	# First, go randomly
	if len(history)==0:
		return random.choice([EMPTY_BOX,FULL_BOX])
	
	# get recently completed orders
	compHist = self.getMyOrderCompletes(history)[-1:]
	if len(history)>1:
		compHist = self.getMyOrderCompletes(history)[-2:]

	if 1 in compHist:
		# If I've completed an order in last two goes,
		# then, play an empty box
		return EMPTY_BOX
	else:
		return FULL_BOX

def TurnsAtTalkAlign(self,history):
	# Go randomly until an order is complete, then:
	# Keep sending full boxes until an order is complete
	# or partner interrupts
	# then let your partner go
	
	# First, go randomly
	if len(history)==0:
		return random.choice([EMPTY_BOX,FULL_BOX])
	
	# has there been a cooperation?
	coop = [x for x in history if sum(x[0])==1]
	if len(coop)==0:
		return random.choice([EMPTY_BOX,FULL_BOX])
	
	# get recently completed orders
	compHist = self.getMyOrderCompletes(history)[-1:]
	if len(history)>1:
		compHist = self.getMyOrderCompletes(history)[-2:]

	if 1 in compHist:
		# If I've completed an order in last two goes,
		# then, play an empty box
		return EMPTY_BOX
	elif self.getPartnersPlays(history)[-1]==FULL_BOX:
		# If my partner is still 'talking', let him go
		return EMPTY_BOX
	else:
		return FULL_BOX


    	
def Random(self,history):
	return random.choice([FULL_BOX,EMPTY_BOX])
	
def RandomWeighted(self,history):
	# Use empty box with prob proportional to size of order
	p = 1/float(self.getThisOrder())
	if random.random() > p:
		return FULL_BOX
	else:
		return EMPTY_BOX
		
def RandomWeightedSwitch(self,history):
	if len(history)==0:
		return random.choice([FULL_BOX,EMPTY_BOX])
	# switch choice with prob proportional to size of order
	lastAction = self.getMyPlays(history)[-1]
	p = 1/float(self.getThisOrder())
	if random.random() < p:
	# switch
		return (lastAction +1) % 2
	else:
		return lastAction
		
def halfSwitch(self,history):
	# Choose randomly until cooperation, 
	# then stick with that until halfway through experiment
	
	# has there been a cooperation?
	coop = [x for x in history if sum(x[0])==1]
	if len(coop)>0:
		# yes, there's a cooperation
		self.halfSwitch_Choice = coop[0][0][self.index]
		if len(history)<(self.num_rounds/2):
			self.halfSwitch_Choice = (1+coop[0][0][self.index]) %2
	else:
		# no cooperation yet, choose randomly
		self.halfSwitch_Choice = random.choice([FULL_BOX,EMPTY_BOX])
	return self.halfSwitch_Choice
	
def alternateMedian(self,history):
	# Choose randomly until cooperation, 
	# then alternate every <median order number> turns
	
	if len(history)==0:
		self.ordersMedian = sorted(self.getOrders())[len(self.getOrders())/2]
	
	# has there been a cooperation?
	coop = [x for x in history if sum(x[0])==1]
	if len(coop)>0:
		# yes, there's a cooperation
		if len(history) < self.ordersMedian:
			return coop[0][0][self.index]
		lastNGoes = self.getMyPlays(history)[-self.ordersMedian:]
		# if all the same during the lastNGoes
		if sum(lastNGoes)==len(lastNGoes) or sum(lastNGoes)==0:
			# then switch
			self.alternateMedian_Choice = (self.alternateMedian_Choice +1)%2
	else:
		# no cooperation yet, choose randomly
		self.alternateMedian_Choice = random.choice([FULL_BOX,EMPTY_BOX])
	return self.alternateMedian_Choice	

def ifItAintBroke(self,history):
	# Random until cooperation, then stick to that
	# has there been a cooperation?
	coop = [x for x in history if sum(x[0])==1]
	if len(coop)>0:
		# yes, there's a cooperation
		return coop[0][0][self.index]
	else:
		# no cooperation yet, choose randomly
		return random.choice([FULL_BOX,EMPTY_BOX])
		
def adaptiveIfItAintBroke(self,history):
	# Random until full box
	# if mixed box, behave randomly
	# This is like tit-for-tat, 
	# but with random playing instead of defection when defection occurs
	
	if len(history)==0:
		return random.choice([FULL_BOX,EMPTY_BOX])
	# If the last round produced a mixed box
	if history[-1][0] == [FULL_BOX,FULL_BOX]:
		# choose randomly
		return random.choice([FULL_BOX,EMPTY_BOX])
	else:
		# else, do what I did last time
		return self.getMyPlays(history)[-1]
		
def weightedAdaptiveIfItAintBroke(self,history):
	# Same as adaptiveIfItAintBroke,
	# But twice as likely to try full box when behaving 'randomly'
	
	if len(history)==0:
		return random.choice([FULL_BOX,EMPTY_BOX])
	# If the last round produced a mixed box
	if history[-1][0] == [FULL_BOX,FULL_BOX]:
		# choose randomly
		return random.choice([FULL_BOX,FULL_BOX,EMPTY_BOX])
	else:
		# else, do what I did last time
		return self.getMyPlays(history)[-1]


def switchByOrderSize_sortFirst(self,history):
	# behave randomly until cooperation
	# flip between empty and full every X turns
	# where X is the current order number
	if len(history)==0:
		self.orders = sorted(self.orders)
		self.startFrom = 99999
		self.sortFirst_choice = random.choice([FULL_BOX,EMPTY_BOX])
		return self.sortFirst_choice
	
	coop = [x for x in history if sum(x[0])==1]
	if len(coop)<=0:
		# no cooperation yet, choose randomly
		self.sortFirst_choice = random.choice([FULL_BOX,EMPTY_BOX])
		return self.sortFirst_choice
	if len(coop)==1:
		if history[-1]==coop[0]:
			self.startFrom = len(history)-1
			
	turnsSinceStart = len(history) - 1 - self.startFrom
	# if we've done it one way for the number of orders, switch
	if turnsSinceStart % self.getThisOrder()==0 and turnsSinceStart>0:
		#switch
		self.sortFirst_choice = (1+self.sortFirst_choice) % 2
		return self.sortFirst_choice	
	else:
		return self.sortFirst_choice

def switchByOrderSize(self,history):
	# behave randomly until cooperation
	# flip between empty and full every X turns
	# where X is the current order number
	if len(history)==0:
		#self.orders = sorted(self.orders)
		self.startFrom = 99999
		self.sortFirst_choice = random.choice([FULL_BOX,EMPTY_BOX])
		return self.sortFirst_choice
	
	coop = [x for x in history if sum(x[0])==1]
	if len(coop)<=0:
		# no cooperation yet, choose randomly
		self.sortFirst_choice = random.choice([FULL_BOX,EMPTY_BOX])
		return self.sortFirst_choice
	if len(coop)==1:
		if history[-1]==coop[0]:
			self.startFrom = len(history)-1
			
	turnsSinceStart = len(history) - 1 - self.startFrom
	# if we've done it one way for the number of orders, switch
	if turnsSinceStart % self.getThisOrder()==0 and turnsSinceStart>0:
		#switch
		self.sortFirst_choice = (1+self.sortFirst_choice) % 2
		return self.sortFirst_choice	
	else:
		return self.sortFirst_choice



######################
# Run all strategies #
# against each other #
######################

strategies = [allCoop,allDef,TitForTat,TitForTatOp,TitFor2Tats,TitFor2TatsOp,GrimTrigger,GrimTriggerOp,Gradual,AdaptiveTitForTat,TurnsAtTalk,TurnsAtTalkHard,TurnsAtTalkAlign,Random,RandomWeighted,RandomWeightedSwitch,halfSwitch,alternateMedian,ifItAintBroke,switchByOrderSize,adaptiveIfItAintBroke,weightedAdaptiveIfItAintBroke]
num_samples = 100

print 's1,s2,money1,money2,ordersComplete1,ordersComplete2,empty_empty,empty_full,full_empty,full_full,whole_order,whole_order_partner'
payoffR = 10
payoffRange = [x-(payoffR/2) for x in range(payoffR)]
payoffs = []
for i1 in payoffRange:
	for i2 in payoffRange:
		for i3 in payoffRange:
			for i4 in payoffRange:
				for i5 in payoffRange:
					for i6 in payoffRange:
						payoffs.append([i1,i2,i3,i4,i5,i6])
						
payoffs = [[-1,1,1,-2,6,6],[-2,1,1,-1,6,6]]
for p in payoffs:
	empty_empty,empty_full,full_empty,full_full,whole_order,whole_order_partner = p
	for s1x in range(len(strategies)):
		for sort_first_s1 in [True,False]:
			s1 = strategies[s1x]
			s1_name = s1.__name__
			if sort_first_s1:
				s1_name = s1.__name__+'_SORT'
			for s2x in range(len(strategies)-s1x):
				for sort_first_s2 in [True,False]:
					s2 = strategies[s2x+s1x]
					s2_name = s2.__name__
					if sort_first_s2:
						s2_name = s2.__name__+'_SORT'
					#print s1.__name__,s2.__name__
					for r in range(num_samples):
						##############
						# Play!      #
						##############
						player1 = JellyBeaner(s1,num_rounds=num_trials)
						player2 = JellyBeaner(s2,ind=1,num_rounds=num_trials)
						
						if sort_first_s1:
							player1.orders = sorted(player1.orders)

						if sort_first_s2:
							player2.orders = sorted(player2.orders)

						
						history = []  # history is a list:  [([player 1 choice, player 2 choice],[did player 1 complete an order?,did player 2 complete an order?]),(...),...]
						
						for i in range(num_trials):
							
							r1 = player1.choose(history)
							r2 = player2.choose(history)
							#print r1,r2,"<<<<<"
							if r1==EMPTY_BOX and r2== EMPTY_BOX:
								player1.addMoney(empty_empty)
								player2.addMoney(empty_empty)
								# Does an empty box break the order chain?
								if empty_box_breaks_order_chain:
									player1.resetcurUnbrokenOrders()
									player2.resetcurUnbrokenOrders()
							if r1==EMPTY_BOX and r2== FULL_BOX:
								# player 2 gets a full, unmixed box
								player2.addOrder()
								player1.resetcurUnbrokenOrders()
								player1.addMoney(empty_full)
								player2.addMoney(full_empty)
						
							if r1==FULL_BOX and r2== EMPTY_BOX:
								# player 1 gets a full, unmixed box
								player1.addOrder()
								player2.resetcurUnbrokenOrders()
								player1.addMoney(full_empty)
								player2.addMoney(empty_full)
						
							if r1==FULL_BOX and r2== FULL_BOX:
								player1.addMoney(full_full)
								player2.addMoney(full_full)
								player1.resetcurUnbrokenOrders()
								player2.resetcurUnbrokenOrders()
							
						# Are there any unbroken orders?
							compOrders = [0,0]
							if player1.getcurUnbrokenOrders() == player1.getThisOrder():
								player1.completeOrder()
								player1.addMoney(whole_order)
								player2.addMoney(whole_order_partner)
								compOrders[0] = 1
								
							if player2.getcurUnbrokenOrders() == player2.getThisOrder():
								player2.completeOrder()
								player2.addMoney(whole_order)
								player1.addMoney(whole_order_partner)	
								compOrders[1] = 1
						
							history.append(([r1,r2],compOrders))
			
						
						#for h in history:
						#	print h
						
						
						print ','.join([str(x) for x in [s1_name,s2_name,player1.getMoney(),player2.getMoney(),player1.ordersCompleted,player2.ordersCompleted]+p])