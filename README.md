# Monte Carlo on Ubeatable Roullete Strategy

https://www.youtube.com/watch?v=EMCXZFClPVU

## Porject Aim
This project aims to demonstrate the power of knowledge, mathematics, and statistics. I recently came across a video claiming to reveal an “unbeatable” roulette strategy with a 98% win rate. The video gained over 440,000 views while falsely promoting a strategy that appeared to offer nearly guaranteed success.

My goal is to disprove this strategy using quantitative mathematical analysis and to inform readers about the gambler’s fallacy. Through visual images, graphs, and statistical evidence, this project will show why such strategies are misleading and why casino games like roulette are ultimately designed to favour the house.

## The Strategy in Question
The creator of the video calls the strategy the “Fibonacci Golden Entry.” This strategy can be applied to either dozens or columns in roulette, both of which pay out at 2:1. Although both dozens and columns can be applied, columns is perferred since it spans over more viraity of high nad low numbers compared to dozens. The strategy is intended for roulette tables with a minimum bet of 5 units and a maximum bet of 500 units.

The player begins by placing a 1-unit bet. Each time the player loses, they increase their next bet to the sum of the previous two bets, following the Fibonacci sequence. After a winning bet, the player returns to the original 1-unit bet.

The player must always move their bet to the column or dozen that won most recently.

If the player loses four bets in a row, they stop betting and wait until the column or dozen they last lost on wins again (mentioned in the videos comment section) Once that happens, the player re-enters the game and continues using the same strategy.

When the player would reach a bet size of $445, or 89 betting units, after 11 consecutive losing bets. At this point, the strategy recommends betting the table maximum in an attempt to recover previous losses, then slightly reducing the bet size to get back over session profit.

## Gambler's Fallocy
### 1. Choose comlum over dozens due to "wider range of number exposure"
within each column there are 12 pockets nubmers. even though the numbers are spread out on the wheel, each pocket would have the same probiility change of being filled by the wheel. so even if the nubmers are conrnalogiclaly ordered it would not matter.

P(column)=P(n1)+P(n2)+...+P(n12)

=12×137= 12 \times \frac{1}{37}

=12×371

=1237= \frac{12}{37}

=3712

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