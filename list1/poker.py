import random
from collections import Counter
from itertools import combinations
import math

cards_map = ['0','0','2','3','4','5','6','7','8','9','10','J','Q','K','A']
colors_map = ['A','B','C','D']


fig_deck = [y+x for x in cards_map[11:] for y in colors_map]
blot_deck = [y+x for x in cards_map[2:11] for y in colors_map]


def sort_by_len(tupl):
    return tupl[0]

def compose_decks_stat_win(min):
    deck = []  
    for i in range (math.ceil(min/4),10):
        all = combinations(range(2,11),i)
        for k in all :
            blots = [y+x for x in map(str,k) for y in colors_map]
            res = showdown(blots)
            if res > 50:
                deck.append((len(blots),blots))
                
    return sorted(deck, key = sort_by_len)


def compose_deck_by_wins_from_all():    
    decks = []  
    for i in range (5,36):
        all = combinations(blot_deck,i,)
        for comb in all:
            res = showdown(comb)
            if res > 50:
                decks.append((len(comb),res,comb))
            
    return sorted(decks, key = sort_by_len)

def blot_draw(deck):
    return random.sample(deck,5)

def fig_draw():
    return random.sample(fig_deck,5)

def color(colors):
    return max(Counter(colors)) == 5

def strit(values):
    vals = sorted(cards_map.index(v) for v in values)
    if vals == list(range(vals[0],vals[0]+5)):
        return True
    return False

def determine_outcome(deck):

    vals = [k[1:] for k in deck]
    
    colors = [k[0] for k in deck]

    count = sorted(Counter(vals).values(), reverse=True)

    if strit(vals) and color(colors):
        return 8
    if count == [4,1]:
        return 7
    if count == [3,2]:
        return 6
    if color(colors):
        return 5
    if strit(vals):
        return 4
    if count == [3,1,1]:
        return 3
    if count == [2,2,1]:
        return 2
    if count == [2,1,1,1]:
        return 1
    return 0 


def showdown(deck):
    total_games = 0
    blot_wins = 0
    fig_wins = 0  
    for _ in range(10000):
        total_games+=1
        blot = blot_draw(deck)
        fig = fig_draw()
        if determine_outcome(blot) > determine_outcome(fig):
            blot_wins +=1
        else:
            fig_wins+=1
    # print(f"blotkarz {round(blot_wins/total_games *100,2)}%, figurant { round(fig_wins/total_games *100,2)}%")
    # print(f"deck: {deck}") 
    return blot_wins/total_games *100
        

blot_deck = ['A8', 'B8', 'C8', 'D8', 'A9', 'B9', 'C9', 'D9', 'A10', 'B10', 'C10', 'D10']# one of the decks that can reliably win more than lose
print(showdown(blot_deck))
# print(compose_decks_stat_win(12))
# print(compose_deck_by_wins_from_all())