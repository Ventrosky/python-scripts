#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import random
import traceback
import telepot
from telepot.delegate import per_chat_id, create_open, pave_event_space, include_callback_query_chat_id
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


class Player(telepot.helper.ChatHandler):
    
	# initialize game
    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)
        self._p_hand = []
        self._b_hand = []
        self._game_phase = 1
        self._emoticons = {1 : u'\u0031\u20e3', 2 : u'\u0032\u20e3',	3 : u'\u0033\u20e3', 4 : u'\u0034\u20e3', 5 : u'\u0035\u20e3', 6 : u'\u0036\u20e3', 'die' : u"\U0001F3B2", 'win' : u"\U0001F389", 'grin' : u"\U0001F601", 'sweat' : u"\U0001F613"}
    
    #costants
    _NOTHING = 0
    _PAIR = 1
    _TWOPAIR = 2
    _THREEOFKIND = 3
    _FIVEHIGHSTRAIGHT = 4
    _SIXHIGHSTRAIGHT = 5
    _FULLHOUSE = 6
    _FOUROFKIND = 7
    _FIVEOFKIND = 8

    # convert hand to emoji
    def _printHand(self, hand, emo):
    	s = ""
    	for dice in hand:
    		s = s + emo[dice]
    	return s

    # keyboard for re-roll
    def _rerollKeyboard(self, hand, emo):
    	buttons = []
    	for dice in hand:
    		buttons.append(InlineKeyboardButton(text=emo[dice], callback_data=str(dice)))
    
    	keyboard = InlineKeyboardMarkup(inline_keyboard=[
                       buttons,
                       [InlineKeyboardButton(text='Re-roll '+self._emoticons['die'], callback_data='0')],
                   ])
    	return keyboard

    # rng hand
    def randomHand(self, hand, n):
    	for x in range (0, n):
    		hand.append(random.randint(1, 6))
    	return hand

    # determinate score
    def _score(self, hand):
    	pairs = 0
    	trip = False
    	for die in hand:
    		count = hand.count(die)
    		if count == 5:
    			return self._FIVEOFKIND
    		elif count == 4:
    			return self._FOUROFKIND
    		elif count == 3:
    			trip = True
    		elif count == 2:
    			pairs += 1
    	if trip and pairs == 2:
    		return self._FULLHOUSE
    	elif trip:
    		return self._THREEOFKIND
    	elif pairs == 4:
    		return self._TWOPAIR
    	elif pairs == 2:
    		return self._PAIR
    	elif sorted(hand) == range(2,7):
    		return self._SIXHIGHSTRAIGHT
    	elif sorted(hand) == range(1,6):
    		return self._FIVEHIGHSTRAIGHT
    	else:
    		return self._NOTHING

    # score to string
    def _stringScore(self, score):
    	if score == self._NOTHING:
    		return " \nNothing"
    	elif score == self._PAIR:
    		return " \nA Pair"
    	elif score == self._TWOPAIR:
    		return " \nTwo Pairs"
    	elif score == self._THREEOFKIND:
    		return " \nThree of A Kind"
    	elif score == self._FIVEHIGHSTRAIGHT:
    		return " \nFive High Straight"
    	elif score == self._SIXHIGHSTRAIGHT:
    		return " \nSix High Straight"
    	elif score == self._FULLHOUSE:
    		return " \nFull House"
    	elif score == self._FOUROFKIND:
    		return " \nFour of A Kind"
    	elif score == self._FIVEOFKIND:
    		return " \nFive of A Kind"

    # chose discard dices
    def _pickToRoll(self, hand, pHand):
    	baseScore = self._score(hand)
    	pScore = self._score(pHand)
    	needRolls = []
    	if baseScore == self._NOTHING and pScore <= self._SIXHIGHSTRAIGHT: # best chance with "nothing" comes from the straight 
    		return [1]
    	for die in hand:
    		test_hand = list(hand)
    		test_hand.remove(die)
    		if self._score(test_hand) == baseScore:
    			needRolls.append(die)
    	return needRolls

    # bot rolls
    def _botRoll(self, hand, pHand):
    	toRoll = self._pickToRoll(hand, pHand)
    	for die in toRoll:
    		hand.remove(die)
    	hand = self.randomHand(hand,5 - len(hand))
    	return hand

    # compare dice value
    def _diceCompare(self, die1, die2):
    	if die1 > die2:
    		return "Player Won!"
    	elif die1 < die2:
    		return "The Bot Won!"
    	else: 
    		return "It's a Tie!"

    # determine tie
    def _simpleTie(self, hand):
    	for die in hand:  
    		if hand.count(die) == 2:
    			return die
    		elif hand.count(die) == 3:
    			return die
    		elif hand.count(die) == 4:
    			return die
    		elif hand.count(die) == 5:
    			return die

    # determine tie TWOPAIR or FULLHOUSE
    def _harderTie(self, hand):
    	dices = set()
    	for die in hand:  
    		if hand.count(die) == 3:
    			dices.update({(3,die)})
    		elif hand.count(die) == 2:
    			dices.update({(2,die)})
    	return list(sorted(dices, reverse=True))
  
    # check winner to string
    def _winner(self, handP, handB):
    	if sorted(handP) == sorted(handB):
    		return "It's a Tie!"
    	scoreP = self._score(handP)
    	scoreB = self._score(handB)
    	if scoreP < scoreB:
    		return "The Bot Won!"
    	elif scoreB < scoreP:
    		return "Player Won!"
    	else:
    		if scoreP in [self._FIVEHIGHSTRAIGHT, self._SIXHIGHSTRAIGHT, self._NOTHING]:
    			return "It's a Tie!"
    		elif scoreP in [self._TWOPAIR, self._FULLHOUSE]:
    		    dicesP = self._harderTie(handP)
    		    dicesB = self._harderTie(handB)
    		    for i in range(len(dicesP)):
    		    	if dicesP[i][1] > dicesB[i][1]:
    		    		return "Player Won!"
    		    	elif dicesP[i][1] < dicesB[i][1]:
    		    		return "The Bot Won!"
    		    return "It's a Tie!"
    		else: 
    		    pointsP = self._simpleTie(handP)
    		    pointsB = self._simpleTie(handB)
    		    return self._diceCompare(pointsP, pointsB)
    
    # first message
    def open(self, initial_msg, seed):
        self.sender.sendMessage("Let's play Poker Dice!")
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='Roll '+self._emoticons['die'], callback_data='roll')],
               ])
        self.sender.sendMessage('First roll of the dices '+self._emoticons['grin'], reply_markup=keyboard)
        return True  
    # commands handler
    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        command = msg['text'].strip().lower()

        if command == '/rank' :
        	rankings = '- Nothing = five mismatched dice forming no sequence longer than four.\n- Pair = two dice showing the same value.\n- Two Pairs = two pairs of dice, each showing the same value.\n- Three-of-a-Kind = three dice showing the same value.\n- Five High Straight = dice showing values from 1 through 5, inclusive.\n- Six High Straight = dice showing values from 2 through 6, inclusive.\n- Full House = Pair of one value and Three-of-a-Kind of another.\n- Four-of-a-Kind = four dice showing the same value.\n- Five-of-a-Kind = all five dice showing the same value.'
        	self.sender.sendMessage(rankings)
        elif command == '/rules' :
        	text = 'Each player uses a set of five dice. The goal of the game is to roll the strongest hand in two out of three hands. The player with the highest-ranking hand wins.'
        	self.sender.sendMessage(text)
        else:
            self.sender.sendMessage("I don't understand")

    # buttons handlers        
    def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        if query_data == 'roll' and self._game_phase == 1:
        	self._p_hand = self.randomHand([], 5)
        	self._b_hand = self.randomHand([], 5)
        	self.sender.sendMessage('Phase '+str(self._game_phase)+':')
        	self.sender.sendMessage("Player: "+self._printHand(self._p_hand, self._emoticons)+self._stringScore(self._score(self._p_hand)))
        	self.sender.sendMessage("Bot:      "+self._printHand(self._b_hand, self._emoticons)+self._stringScore(self._score(self._b_hand)))
        	self._game_phase += 1
        	self.sender.sendMessage('Choses dice to re-roll', reply_markup=self._rerollKeyboard(self._p_hand,self._emoticons))

        elif query_data == '0' and self._game_phase > 1:
        	self.sender.sendMessage('Phase '+str(self._game_phase)+':')
        	self._b_hand = self._botRoll(self._b_hand, self._p_hand)
        	self._p_hand = self.randomHand(self._p_hand,5 - len(self._p_hand))
        	self.sender.sendMessage("Player: "+ self._printHand(self._p_hand, self._emoticons)+self._stringScore(self._score(self._p_hand)))
        	self.sender.sendMessage("Bot:      "+ self._printHand(self._b_hand, self._emoticons)+self._stringScore(self._score(self._b_hand)))
        	self._game_phase += 1
        	if self._game_phase < 4:
        		self.sender.sendMessage('Choses dice to re-roll', reply_markup=self._rerollKeyboard(self._p_hand,self._emoticons))
        	else:
        		winner = self._winner(self._p_hand,self._b_hand,)
        		self.sender.sendMessage('Round Ended:\n'+winner+self._emoticons['win'])
        		self._game_phase = 1
        		keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Roll '+self._emoticons['die'], callback_data='roll')],])
        		self.sender.sendMessage('New Round? '+self._emoticons['grin'], reply_markup=keyboard)
        elif int(query_data) > 0 and int(query_data) < 7:
        	if int(query_data) in self._p_hand:
        		self._p_hand.remove(int(query_data))
        	self.sender.sendMessage('Choses dice to re-roll', reply_markup=self._rerollKeyboard(self._p_hand,self._emoticons))

    def on__idle(self, event):
        self.sender.sendMessage('Game expired. '+self._emoticons['sweat'])
        self.close()

TOKEN = sys.argv[1]

bot = telepot.DelegatorBot(TOKEN, [
    include_callback_query_chat_id(pave_event_space())(
        per_chat_id(), create_open, Player, timeout=6000),
])
bot.message_loop(run_forever='Listening ...')