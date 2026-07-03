# Monte Carlo on Unbeatable Roullete Strategy

<img width="600" alt="ChatGPT Image Jul 3, 2026" src="https://github.com/user-attachments/assets/33fc0a9b-f7dc-423a-ab90-796f6f88fdc2" />


## Project Aim
This project aims to demonstrate the power of knowledge, mathematics, and statistics. I recently came across a video claiming to reveal an “unbeatable” roulette strategy with a 98% win rate. The video gained over 440,000 views while falsely promoting a strategy that appeared to offer nearly guaranteed success.

My goal is to disprove this strategy using quantitative mathematical analysis and to inform readers about the gambler’s fallacy. Through statistical evidence and simulations, this project will show why such strategies are misleading and why casino games like roulette are ultimately designed to favour the house.

## The Strategy in Question
The creator of the video refers to the strategy as the “Fibonacci Golden Entry.” The strategy can be applied to either dozens or columns in roulette, both of which pay out at 2:1. Although both betting options are possible, the creator claims that columns are preferable because they contain a wider spread of high and low numbers compared with dozens. The strategy is designed for roulette tables with a minimum bet of $5 per unit and a maximum bet of 500 units.

The player begins by placing a 1-unit bet. Each time the player loses, the next bet is increased to the sum of the previous two bets, following the Fibonacci sequence. After a winning bet, the player resets the sequence and returns to the original 1-unit bet.

The strategy also requires the player to move their bet to the column or dozen that won most recently. This is presented as the “entry” rule of the system.

If the player loses four bets in a row, they stop betting temporarily. According to an additional comment he made under the video, the player should wait until the column or dozen they last lost on wins again before re-entering the game and continuing the strategy.

After 11 consecutive losing bets, the player would reach a bet size of 89 units, equivalent to $445. At this point, the strategy recommends placing the table maximum bet of 500 units in an attempt to recover previous losses, which could take one or two bets to return to session profit.

[![Watch the video](https://img.youtube.com/vi/EMCXZFClPVU/maxresdefault.jpg)](https://www.youtube.com/watch?v=EMCXZFClPVU)

## Gambler's Fallocy
### 1. Choosing columns over dozens because they feel more spread out across the number range
The strategy suggests choosing columns instead of dozens because columns appear to contain a wider mixture of high and low numbers. However, this reasoning is mathematically misleading.

In American roulette, there are 38 pockets in total: numbers 1–36, 0, and 00. Each column contains 12 numbers, and each dozen also contains 12 numbers. Although the numbers may appear grouped differently on the betting table, their visual position on the layout does not affect the outcome of the spin.

The winning outcome is determined by where the spinning ball lands on the wheel. On a fair roulette wheel, each pocket has an equal chance of being selected. Therefore, the probability of landing on any single number is:

[
P(\text{single number}) = \frac{1}{38}
]

Since a column or dozen covers 12 different numbers, the probability of winning is found by adding the probabilities of those 12 individual numbers. This is why the probability is multiplied by 12:

[
P(\text{column}) = 12 \times \frac{1}{38}
]

[
P(\text{column}) = \frac{12}{38} \approx 31.58%
]

The same applies to dozens because each dozen also contains 12 numbers:

[
P(\text{dozen}) = 12 \times \frac{1}{38}
]

[
P(\text{dozen}) = \frac{12}{38} \approx 31.58%
]

Therefore, choosing columns over dozens does not provide any mathematical advantage. Both bets cover the same number of pockets and have the same probability of winning. The claim that columns are better because they offer a “wider range of number exposure” is based on visual appearance rather than probability.




### 2 to 1 profit . 4/1 still the same

| Bet | Payout | EV per 1 unit | Expected loss |
| --- | --- | --- | --- |
| Straight up | 35:1 | **−0.0270** | **−2.70%** |
| Split | 17:1 | **−0.0270** | **−2.70%** |
| Street / Trio | 11:1 | **−0.0270** | **−2.70%** |
| Corner / First four | 8:1 | **−0.0270** | **−2.70%** |
| Six line | 5:1 | **−0.0270** | **−2.70%** |
| Dozen | 2:1 | **−0.0270** | **−2.70%** |
| Column | 2:1 | **−0.0270** | **−2.70%** |
| Red/Black, Odd/Even, High/Low | 1:1 | **−0.0270** | **−2.70%** |

fibonachio but this can be argued with variance of trade which would be discuessedlater 

### 3 
each trade is independant of one another
- golden entry winning column 2 in a row invariabliy it iwll happen in 15 spins follow the winner
- wait for 5 spins to not accour in a row then jump in
- stay on same column or dozen and after 4 straight losses, SIT OUT until your column or dozen wins. Then jump back in resuming the sequence.
    
    no matter how many times you sit out or whichever column you follow the porbaibility would be the same because it is not related

### 4 
1000 bankroll (max drawdown) 5 per unit and 500$ max per table


### 5
max loss

parametric monte carlos


## Project Setup

Create and activate the virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Generate the current graphs and Monte Carlo output:

```bash
python src/plots.py
```

This writes graphs and simulation results into `outputs/`.

## Project Structure

```txt
src/
  strategy.py   # roulette probabilities, expected value, and strategy config
  simulate.py   # Fibonacci roulette Monte Carlo simulation
  plots.py      # probability, EV, bankroll, and distribution charts
outputs/        # generated graphs and CSV output
notebooks/      # optional exploratory analysis
data/           # optional input data
tests/          # lightweight math tests
```
