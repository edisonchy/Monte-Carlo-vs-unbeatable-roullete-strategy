# Monte Carlo on Unbeatable Roullete Strategy

<img width="600" alt="ChatGPT Image Jul 3, 2026" src="https://github.com/user-attachments/assets/33fc0a9b-f7dc-423a-ab90-796f6f88fdc2" />


## Project Aim
This project aims to demonstrate the power of knowledge, mathematics, and statistics. I recently came across a video claiming to reveal an “unbeatable” roulette strategy with a 98% win rate. The video gained over 440,000 views while falsely promoting a strategy that appeared to offer nearly guaranteed success.

My goal is to disprove this strategy using quantitative mathematical analysis and to inform readers about the gambler’s fallacy. Through statistical evidence and statistical simulations, this project will show why such strategies are misleading and why casino games like roulette are ultimately designed to favour the house.

## The Strategy in Question
The creator of the video refers to the strategy as the “Fibonacci Golden Entry.” The strategy can be applied to either dozens or columns in roulette, both of which pay out at 2:1. Although both betting options are possible, the creator claims that columns are preferable because they contain a wider spread of high and low numbers compared with dozens. The strategy is designed for roulette tables with a minimum bet of $5 per unit and a maximum bet of 500 units.

The player begins by placing a 1-unit bet. Each time the player loses, the next bet is increased to the sum of the previous two bets, following the Fibonacci sequence. After a winning bet, the player resets the sequence and returns to the original 1-unit bet.

The strategy also requires the player to move their bet to the column or dozen that won most recently. This is presented as the “entry” rule of the system.

If the player loses four bets in a row, they stop betting temporarily. According to an additional comment he made under the video, the player should wait until the column or dozen they last lost on wins again before re-entering the game and continuing the strategy.

After 11 consecutive losing bets, the player would reach a bet size of 89 units, equivalent to $445. At this point, the strategy recommends placing the table maximum bet of 500 units in an attempt to recover previous losses, which could take one or two bets to return to session profit.

[![Watch the video](https://img.youtube.com/vi/EMCXZFClPVU/maxresdefault.jpg)](https://www.youtube.com/watch?v=EMCXZFClPVU)

## Gambler's Fallocy
### 1. Choose comlum over dozens due to "wider range of number exposure"
within each column there are 12 pockets nubmers. even though the numbers are spread out on the wheel, each pocket would have the same probiility change of being filled by the wheel. so even if the nubmers are conrnalogiclaly ordered it would not matter.

$P(\text{column}) = P(n_1) + P(n_2) + \cdots + P(n_{12})$

$= 12 \times \frac{1}{37}$

$= \frac{12}{37}$

same cmolumn and soezn 12 slots so numbers will have no influence in the porbability of the trade

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
