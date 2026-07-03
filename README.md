# Monte Carlo vs Unbeatable Roullete Strategy

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

<table>
  <tr>
    <td>
      <img width="400" alt="ChatGPT Image Jul 3, 2026, 06_09_19 PM" src="https://github.com/user-attachments/assets/168fb5a6-7a46-4661-8609-93eed7e217d1" />
    </td>
    <td>
      <img width="400" alt="ChatGPT Image Jul 3, 2026, 06_13_35 PM" src="https://github.com/user-attachments/assets/92beb9cd-c615-47aa-b639-4794953fc6a5" />
    </td>
  </tr>
</table>

In American roulette, there are 38 pockets in total: numbers 1–36, 0, and 00. Each column contains 12 numbers, and each dozen also contains 12 numbers. Although the numbers may appear grouped differently on the betting table, their visual position on the layout does not affect the outcome of the spin.

<table>
  <tr>
    <td>
      <img height="300" alt="ChatGPT Image Jul 3, 2026, 07_42_50 PM" src="https://github.com/user-attachments/assets/e8ecb5f7-0e1f-4bf8-a1a9-444af34416c4" />
    </td>
    <td>
      <img height="300" alt="ChatGPT Image Jul 3, 2026, 07_36_09 PM" src="https://github.com/user-attachments/assets/ddb984c5-e30c-4c2a-9851-feb1ca052020" />
    </td>
  </tr>
</table>

The winning outcome is determined by where the spinning ball lands on the wheel. On a fair roulette wheel, each pocket has an equal chance of being selected. Therefore, the probability of landing on any single number is:

$P(\text{single number}) = \frac{1}{38}$

Since a column or dozen covers 12 different numbers, the probability of winning is found by adding the probabilities of those 12 individual numbers. This is why the probability is multiplied by 12:

$P(\text{column}) = 12 \times \frac{1}{38}$

$P(\text{column}) = \frac{12}{38} \approx 31.58\%$

The same applies to dozens because each dozen also contains 12 numbers:

$P(\text{dozen}) = 12 \times \frac{1}{38}$

$P(\text{dozen}) = \frac{12}{38} \approx 31.58\%$

Therefore, choosing columns over dozens does not provide any mathematical advantage. Both bets cover the same number of pockets and have the same probability of winning. The claim that columns are better because they offer a “wider range of number exposure” is based on visual appearance rather than probability.




### 2. Selecting 2:1 payout only does not yield an advantage
The strategy focuses on dozens and columns because they pay out at 2:1. At first, this may appear attractive because a winning bet returns twice the stake as profit. However, the payout alone does not determine whether a bet is profitable. To evaluate a roulette bet properly, the **expected value** must be calculated.

Expected value measures the average profit or loss a player can expect per bet over the long run. It is calculated by multiplying each possible outcome by its probability.

For a 1-unit column or dozen bet in American roulette:

$$
P(\text{win}) = \frac{12}{38}
$$

$$
P(\text{lose}) = \frac{26}{38}
$$

A winning column or dozen bet earns 2 units of profit, while a losing bet loses 1 unit. Therefore, the expected value is:

$$
EV = \left(\frac{12}{38} \times 2\right) - \left(\frac{26}{38} \times 1\right)
$$

$$
EV = \frac{24}{38} - \frac{26}{38}
$$

$$
EV = -\frac{2}{38}
$$

$$
EV \approx -0.0526
$$

This means that for every 1 unit bet, the player is expected to lose approximately 0.0526 units in the long run. In percentage terms, this is an expected loss of:

$$
-5.26\%
$$

This negative expected value applies to most standard American roulette bets. Even though different bets have different payouts, the probabilities and payouts are structured so that the casino keeps the same long-term advantage of approximately 5.26%.

| Bet type                      | Numbers covered | Win probability | Lose probability | Payout | Expected value |
| ----------------------------- | --------------: | --------------: | ---------------: | -----: | -------------: |
| Straight up                   |               1 |    1/38 = 2.63% |   37/38 = 97.37% |   35:1 |         −5.26% |
| Split                         |               2 |    2/38 = 5.26% |   36/38 = 94.74% |   17:1 |         −5.26% |
| Street / Trio                 |               3 |    3/38 = 7.89% |   35/38 = 92.11% |   11:1 |         −5.26% |
| Corner                        |               4 |   4/38 = 10.53% |   34/38 = 89.47% |    8:1 |         −5.26% |
| Six line                      |               6 |   6/38 = 15.79% |   32/38 = 84.21% |    5:1 |         −5.26% |
| Dozen                         |              12 |  12/38 = 31.58% |   26/38 = 68.42% |    2:1 |         −5.26% |
| Column                        |              12 |  12/38 = 31.58% |   26/38 = 68.42% |    2:1 |         −5.26% |
| Red/Black, Odd/Even, High/Low |              18 |  18/38 = 47.37% |   20/38 = 52.63% |    1:1 |         −5.26% |

This shows that choosing a 2:1 bet exclusively does not yeild an edge for the player. The player may win more often on columns or dozens than on straight-up numbers, but the payout is lower to compensate for the higher probability of winning.

For example, a straight-up bet has a low chance of winning but a high payout of 35:1. A column bet has a higher chance of winning but only pays 2:1. In both cases, the expected value remains negative.

The Fibonacci system does not change the expected value of roulette. It only changes the size and timing of the bets. Each spin still has the same probability of winning or losing, and the house edge remains unchanged. However, the system does affect the **variance** of the player’s results by creating a pattern of many small wins or recoveries, while still exposing the player to the risk of occasional large losses. This will be discussed later in the analysis.

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
