import requests
import colorama
from colorama import Fore, Back, Style

#URLS for Deck of Cards API
url = "https://deckofcardsapi.com/api"
initial = "/deck/0cierwj4de2c/draw/?count=2"
hit = "/deck/0cierwj4de2c/draw/?count=1"
shuffle = "/deck/0cierwj4de2c/shuffle/"

payload={}
headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json'
}

#Combined URLs for successful response
UI = url + initial
SI = url + shuffle
HI = url + hit

playing = True

#Empty list to store card values
dealer_cards = []
player_cards = []

while True:

	print(Back.RED)
	print(Style.BRIGHT)
	name = input("Name: ")
	print("\n")
	print(f"Welcome to SDN Blackjack {name}!!! Good luck and have fun! \n")

	#dealers initial hand
	while len(dealer_cards) != 2:
		initialD = requests.get(UI, headers=headers, data=payload)
		initialD_json = initialD.json()
		CV0 = initialD_json['cards'][0]['value']
		CV1 = initialD_json['cards'][1]['value']
		dealer_cards.append(CV0)
		dealer_cards.append(CV1)
		if len(dealer_cards) == 2:
			print("Dealer has X &", dealer_cards[1])	
		for index, value in enumerate(dealer_cards):
			if value == 'JACK':
				dealer_cards[index] = '10'
			elif value == 'QUEEN':
				dealer_cards[index] = '10'
			elif value == 'KING':
				dealer_cards[index] = '10'
			elif value == 'ACE':
				dealer_cards[index] = '11'
	#converting dealers cards to integers
		dealer_hand = [int(i) for i in dealer_cards]
	#changing hand value for two ACES
	if sum(dealer_hand) == 22:
		dealer_hand.clear()
		dealer_hand.append(2)
					
	#players initial hand			
	while len(player_cards) != 2:
		initialD = requests.get(UI, headers=headers, data=payload)
		initialD_json = initialD.json()
		CV0 = initialD_json['cards'][0]['value']
		CV1 = initialD_json['cards'][1]['value']
		player_cards.append(CV0)
		player_cards.append(CV1)
		if len(player_cards) == 2:
			print(f"You have {player_cards} \n")
		for index, value in enumerate(player_cards):
			if value == 'JACK':
				player_cards[index] = '10'
			elif value == 'QUEEN':
				player_cards[index] = '10'
			elif value == 'KING':
				player_cards[index] = '10'
			elif value == 'ACE':
				player_cards[index] = '11'
	#converting players cards to integers
		player_hand = [int(i) for i in player_cards]

	if sum(player_hand) == 22:
		player_hand.clear()
		player_hand.append(2)
		for index, value in enumerate(player_cards):
			if value == '11':
				player_cards[index] = '1'
				
			
	#hitting or staying for player if hand value under 21			
	while sum(player_hand) < 21:
		print("Do you want to hit or stay? ", "\n")
		print("1. Hit ")
		print("2. Stay ", "\n")
		choice = input(f"Please select option 1 or 2: ")
		print(" ")
		if choice == '1':
			hitD = requests.get(HI, headers=headers, data=payload)
			hitD_json = hitD.json()
			HV0 = hitD_json['cards'][0]['value']
			player_cards.append(HV0)
		elif choice == '2':
			
			break
		else:
			print("Invalid choice, please choose again")
		for index, value in enumerate(player_cards):
			if value == 'JACK':
				player_cards[index] = '10'
			elif value == 'QUEEN':
				player_cards[index] = '10'
			elif value == 'KING':
				player_cards[index] = '10'
			elif value == 'ACE':
				if sum(player_hand) <= 10:
					player_cards[index] = '11'
				elif sum(player_hand) > 10:
					player_cards[index] = '1'
					for index, value in enumerate(player_cards):
						if value == '11':
							player_cards[index] = '1'
		#converting players cards to integers			
		player_hand = [int(i) for i in player_cards]
		#changing ACE value to 1 if player goes over 21 with ACES in hand
		if sum(player_hand) > 21:
			for index, value in enumerate(player_hand):
				if value == 11:
					player_hand[index] = 1
			for index, value in enumerate(player_cards):
				if value == '11':
					player_cards[index] = '1'
		print(f"Your cards {player_cards} = {(str(sum(player_hand)))} \n")
		
	#if player stays under 21 and dealer hand value is under 17 scenarios		
	if sum(player_hand) < 21:				
		while sum(dealer_hand) < 17:
			hitD = requests.get(HI, headers=headers, data=payload)
			hitD_json = hitD.json()
			HV0 = hitD_json['cards'][0]['value']
			dealer_cards.append(HV0)
			for index, value in enumerate(dealer_cards):
				if value == 'JACK':
					dealer_cards[index] = '10'
				elif value == 'QUEEN':
					dealer_cards[index] = '10'
				elif value == 'KING':
					dealer_cards[index] = '10'
				elif value == 'ACE':
					if sum(dealer_hand) <= 10:
						dealer_cards[index] = '11'
					elif sum(dealer_hand) > 10:
						dealer_cards[index] = '1'
						for index, value in enumerate(dealer_cards):
							if value == '11':
								dealer_cards[index] = '1'
			#converting dealers cards to integers				
			dealer_hand = [int(i) for i in dealer_cards]	
			#changing ACE value to 1 if dealer goes over 21 with ACES in hand				
			if sum(dealer_hand) > 21:
				for index, value in enumerate(dealer_hand):
					if value == 11:
						dealer_hand[index] = 1
				for index, value in enumerate(dealer_cards):
					if value == '11':
						dealer_cards[index] = '1'	
	#scenarios

	if sum(player_hand) == 21:
		if sum(player_hand) == sum(dealer_hand):
			#suffle the deck
			shuffleD = requests.get(SI, headers=headers, data=payload)
			shuffleD_json = shuffleD.json()
			print(f"{Fore.BLUE}{name} & DEALER PUSH!! {Fore.RESET} \n")
			print(f"{name} has a total of {(str(sum(player_hand)))} from {player_cards} \n")
			print(f"Dealer has a total of {(str(sum(dealer_hand)))} from {dealer_cards} \n")
			print("The cards have been shuffled; total number of cards availble: ", shuffleD_json['remaining'], "\n")
		else:
			#shuffle the deck
			shuffleD = requests.get(SI, headers=headers, data=payload)
			shuffleD_json = shuffleD.json()
			print(f"{Fore.GREEN}BLACKJACK! YOU WIN! {Fore.RESET}\n ")		
			print(f"{name} has a total of {(str(sum(player_hand)))} from {player_cards} \n")
			print(f"Dealer has a total of {(str(sum(dealer_hand)))} from {dealer_cards} \n")
			print("The cards have been shuffled; total number of cards availble: ", shuffleD_json['remaining'], "\n")
		
	elif sum(dealer_hand) == 21:
		#shuffle the deck
		shuffleD = requests.get(SI, headers=headers, data=payload)
		shuffleD_json = shuffleD.json()
		print(f"{Fore.BLACK}DEALER HAS BLACKJACK! {Fore.RESET}\n ")	
		print(f"{name} has a total of {(str(sum(player_hand)))} from {player_cards} \n")
		print(f"Dealer has a total of {(str(sum(dealer_hand)))} from {dealer_cards} \n")
		print("The cards have been shuffled; total number of cards availble: ", shuffleD_json['remaining'], "\n")
		
	elif sum(player_hand) > 21:
		#shuffle the deck
		shuffleD = requests.get(SI, headers=headers, data=payload)
		shuffleD_json = shuffleD.json()
		print(f"{Fore.BLACK}You BUSTED! DEALER WINS! {Fore.RESET}\n ")	
		print(f"{name} has a total of {(str(sum(player_hand)))} from {player_cards} \n")
		print(f"Dealer has a total of {(str(sum(dealer_hand)))} from {dealer_cards} \n")
		print("The cards have been shuffled; total number of cards availble: ", shuffleD_json['remaining'], "\n")
		
	elif sum(dealer_hand) > 21:
		#shuffle the deck
		shuffleD = requests.get(SI, headers=headers, data=payload)
		shuffleD_json = shuffleD.json()
		print(f"{Fore.GREEN}DEALER BUSTS! {name} WINS! {Fore.RESET}\n")
		print(f"{name} has a total of {(str(sum(player_hand)))} from {player_cards} \n")
		print(f"Dealer has a total of {(str(sum(dealer_hand)))} from {dealer_cards} \n")	
		print("The cards have been shuffled; total number of cards availble: ", shuffleD_json['remaining'], "\n")

	elif sum(dealer_hand) > sum(player_hand):
		#shuffle the deck
		shuffleD = requests.get(SI, headers=headers, data=payload)
		shuffleD_json = shuffleD.json()
		print(f"{Fore.BLACK}Sorry {name}! DEALER WINS! {Fore.RESET}\n")
		print(f"{name} has a total of {(str(sum(player_hand)))} from {player_cards} \n")
		print(f"Dealer has a total of {(str(sum(dealer_hand)))} from {dealer_cards} \n")
		print("The cards have been shuffled; total number of cards availble: ", shuffleD_json['remaining'], "\n")
									
	elif sum(dealer_hand) < sum(player_hand):
		#shuffle the deck
		shuffleD = requests.get(SI, headers=headers, data=payload)
		shuffleD_json = shuffleD.json()		
		print(f"{Fore.GREEN}{name} WINS! GOOD JOB! {Fore.RESET}\n")			
		print(f"{name} has a total of {(str(sum(player_hand)))} from {player_cards} \n")
		print(f"Dealer has a total of {(str(sum(dealer_hand)))} from {dealer_cards} \n")		
		print("The cards have been shuffled; total number of cards availble: ", shuffleD_json['remaining'], "\n")
		
		
	elif sum(dealer_hand) == sum(player_hand):
		#shuffle the deck
		shuffleD = requests.get(SI, headers=headers, data=payload)
		shuffleD_json = shuffleD.json()
		print(f"{Fore.BLUE}{name} & DEALER PUSH!! {Fore.RESET}\n")
		print(f"{name} has a total of {(str(sum(player_hand)))} from {player_cards} \n")
		print(f"Dealer has a total of {(str(sum(dealer_hand)))} from {dealer_cards} \n")
		print("The cards have been shuffled; total number of cards availble: ", shuffleD_json['remaining'], "\n")
		
	

	play_again = input(f"If you would like to play again, please enter 'y' or press any other character to end program: \n")
	print(" ")
	if play_again == "y" or play_again == "Y":
		playing = True
		dealer_hand.clear()
		dealer_cards.clear()
		player_hand.clear()
		player_cards.clear()
		continue
	else:
		print('Thanks for playing! ')
		print(Style.RESET_ALL)
			
		break
