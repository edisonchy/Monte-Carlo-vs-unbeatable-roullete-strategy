from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from simulate import (
    simulate_fibonacci_with_max_recovery_session,
    simulate_fibonacci_session,
    simulate_flat_session,
    simulate_flat_vs_fibonacci_session,
)
from strategy import (
    COLUMN_WIN_PROBABILITY,
    RouletteConfig,
    column_expected_value_units,
    fibonacci_sequence,
)


sns.set_theme(style="whitegrid")


def save_figure(fig, path: str, **savefig_kwargs) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, **savefig_kwargs)


def save_fibonacci_final_bankroll_distribution_plot(
    path: str = "outputs/figures/fibonacci_final_bankroll_distribution.png",
    sessions: int = 10000,
    spins: int = 120,
    seed: int = 42,
) -> None:
    config = RouletteConfig(spins=spins)
    rng = np.random.default_rng(seed)
    final_bankrolls = []

    for _ in range(sessions):
        session = simulate_fibonacci_session(config, rng)
        if session.empty:
            final_bankroll_units = config.starting_bankroll_units
        else:
            final_bankroll_units = session["bankroll_units"].iloc[-1]
        final_bankrolls.append(final_bankroll_units * config.unit_size)

    final_bankrolls = np.array(final_bankrolls)
    mean_final = float(np.mean(final_bankrolls))
    median_final = float(np.median(final_bankrolls))
    ruin_rate = float(np.mean(final_bankrolls <= 0))
    profit_rate = float(np.mean(final_bankrolls >= config.starting_bankroll))
    non_ruin_loss_rate = float(
        np.mean((final_bankrolls > 0) & (final_bankrolls < config.starting_bankroll))
    )

    upper_bin = max(2000, int(np.ceil(final_bankrolls.max() / 50) * 50) + 50)
    bins = np.arange(0, upper_bin + 50, 50)

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.hist(
        final_bankrolls,
        bins=bins,
        color="#b3261e",
        edgecolor="white",
        linewidth=0.8,
        alpha=0.88,
    )
    ax.axvline(
        config.starting_bankroll,
        color="black",
        linestyle=":",
        linewidth=2,
        label=f"Starting bankroll = ${config.starting_bankroll:,.0f}",
    )
    ax.axvline(
        mean_final,
        color="#2f5f8f",
        linestyle="--",
        linewidth=2,
        label=f"Mean final = ${mean_final:,.0f}",
    )
    ax.axvline(
        median_final,
        color="#2f7d32",
        linestyle="-.",
        linewidth=2,
        label=f"Median final = ${median_final:,.0f}",
    )

    summary_text = (
        f"Reached $0: {ruin_rate:.1%}\n"
        f"Finished >= $1,000: {profit_rate:.1%}\n"
        f"Below $1,000, not ruined: {non_ruin_loss_rate:.1%}"
    )
    ax.text(
        0.98,
        0.72,
        summary_text,
        transform=ax.transAxes,
        ha="right",
        va="top",
        bbox={"boxstyle": "round,pad=0.35", "facecolor": "white", "alpha": 0.9},
    )
    ax.set_title(f"Fibonacci Final Bankroll Distribution ({sessions:,} Simulations)")
    ax.set_xlabel(f"Final bankroll after {spins} placed bets")
    ax.set_ylabel("Session count")
    ax.xaxis.set_major_formatter(lambda value, _: f"${value:,.0f}")
    ax.legend(loc="upper left")
    fig.tight_layout()
    save_figure(fig, path, dpi=160)
    plt.close(fig)


def save_fibonacci_max_recovery_comparison_plot(
    path: str = "outputs/figures/fibonacci_max_recovery_comparison.png",
    sessions: int = 10000,
    spins: int = 120,
    seed: int = 42,
) -> None:
    config = RouletteConfig(spins=spins)
    categories = [
        "Finished >= $1,000",
        "Below $1,000, not ruined",
        "Reached $0 bankroll",
    ]
    colors = {
        "Finished >= $1,000": "#2f7d32",
        "Below $1,000, not ruined": "#d19a2a",
        "Reached $0 bankroll": "#b3261e",
    }

    def categorize(final_bankroll: float) -> str:
        if final_bankroll <= 0:
            return "Reached $0 bankroll"
        if final_bankroll >= config.starting_bankroll:
            return "Finished >= $1,000"
        return "Below $1,000, not ruined"

    def summarize_sessions(simulate_session, include_recovery_stats: bool = False):
        rng = np.random.default_rng(seed)
        outcome_counts = {category: 0 for category in categories}
        recovery_counts = {category: 0 for category in categories}
        final_bankrolls = []
        recovery_sessions = 0
        recovered_above_start = 0
        full_table_max_sessions = 0

        for _ in range(sessions):
            session = simulate_session(config, rng)
            if session.empty:
                final_bankroll = config.starting_bankroll
            else:
                final_bankroll = float(session["bankroll_units"].iloc[-1] * config.unit_size)

            category = categorize(final_bankroll)
            outcome_counts[category] += 1
            final_bankrolls.append(final_bankroll)

            if include_recovery_stats and not session.empty:
                recovery_mode = session.get("max_recovery_mode")
                if recovery_mode is not None and bool(recovery_mode.any()):
                    recovery_sessions += 1
                    recovery_counts[category] += 1
                    recovery_rows = session.loc[recovery_mode]

                    if bool(
                        (
                            recovery_rows["bankroll_units"]
                            > config.starting_bankroll_units
                        ).any()
                    ):
                        recovered_above_start += 1

                    if bool(
                        (
                            recovery_rows["bet_units"]
                            == config.table_max_units
                        ).any()
                    ):
                        full_table_max_sessions += 1

        return {
            "outcome_counts": outcome_counts,
            "recovery_counts": recovery_counts,
            "final_bankrolls": np.array(final_bankrolls),
            "recovery_sessions": recovery_sessions,
            "recovered_above_start": recovered_above_start,
            "full_table_max_sessions": full_table_max_sessions,
        }

    base_summary = summarize_sessions(simulate_fibonacci_session)
    recovery_summary = summarize_sessions(
        simulate_fibonacci_with_max_recovery_session,
        include_recovery_stats=True,
    )

    fig, (ax_all, ax_recovery) = plt.subplots(
        1,
        2,
        figsize=(14, 6),
        gridspec_kw={"width_ratios": [1.25, 1]},
    )
    fig.suptitle(
        "$500 Table-Max Recovery Rule: Outcome Comparison",
        fontsize=15,
        y=0.98,
    )

    strategy_labels = [
        "Base Fibonacci\nreset after win",
        "$500 recovery\nuntil profit",
    ]
    x_positions = np.arange(len(strategy_labels))
    bottoms = np.zeros(len(strategy_labels))

    for category in categories:
        counts = np.array(
            [
                base_summary["outcome_counts"][category],
                recovery_summary["outcome_counts"][category],
            ]
        )
        rates = counts / sessions
        ax_all.bar(
            x_positions,
            rates,
            bottom=bottoms,
            color=colors[category],
            edgecolor="white",
            linewidth=0.9,
            label=category,
        )

        for index, rate in enumerate(rates):
            if rate >= 0.035:
                ax_all.text(
                    x_positions[index],
                    bottoms[index] + rate / 2,
                    f"{rate:.1%}\n({counts[index]:,})",
                    ha="center",
                    va="center",
                    color="white",
                    fontsize=9,
                    fontweight="bold",
                )

        bottoms += rates

    ax_all.set_title(f"All {sessions:,} simulated sessions")
    ax_all.set_xticks(x_positions)
    ax_all.set_xticklabels(strategy_labels)
    ax_all.set_ylabel("Share of sessions")
    ax_all.set_ylim(0, 1)
    ax_all.yaxis.set_major_formatter(lambda value, _: f"{value:.0%}")
    ax_all.legend(loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=1)

    recovery_sessions = recovery_summary["recovery_sessions"]
    recovery_bottom = 0.0

    for category in categories:
        count = recovery_summary["recovery_counts"][category]
        rate = count / recovery_sessions if recovery_sessions else 0
        ax_recovery.bar(
            [0],
            [rate],
            bottom=[recovery_bottom],
            color=colors[category],
            edgecolor="white",
            linewidth=0.9,
        )

        if rate >= 0.035:
            ax_recovery.text(
                0,
                recovery_bottom + rate / 2,
                f"{rate:.1%}\n({count:,})",
                ha="center",
                va="center",
                color="white",
                fontsize=9,
                fontweight="bold",
            )

        recovery_bottom += rate

    recovery_rate = recovery_sessions / sessions
    recovered_rate = (
        recovery_summary["recovered_above_start"] / recovery_sessions
        if recovery_sessions
        else 0
    )
    full_table_max_rate = recovery_summary["full_table_max_sessions"] / sessions

    summary_text = (
        f"Recovery stage triggered: {recovery_sessions:,}/{sessions:,} "
        f"({recovery_rate:.1%})\n"
        f"Ever returned above $1,000 after recovery: "
        f"{recovery_summary['recovered_above_start']:,}/{recovery_sessions:,} "
        f"({recovered_rate:.1%})\n"
        f"Ever placed a full $500 recovery bet: "
        f"{recovery_summary['full_table_max_sessions']:,}/{sessions:,} "
        f"({full_table_max_rate:.1%})"
    )

    ax_recovery.set_title("Only sessions that entered recovery")
    ax_recovery.set_xticks([0])
    ax_recovery.set_xticklabels(["$500 recovery\nstage triggered"])
    ax_recovery.set_ylim(0, 1)
    ax_recovery.set_ylabel("Share of recovery-stage sessions")
    ax_recovery.yaxis.set_major_formatter(lambda value, _: f"{value:.0%}")
    ax_recovery.text(
        0.5,
        0.96,
        summary_text,
        transform=ax_recovery.transAxes,
        ha="center",
        va="top",
        fontsize=9,
        bbox={"boxstyle": "round,pad=0.35", "facecolor": "white", "alpha": 0.92},
    )

    fig.tight_layout()
    save_figure(fig, path, dpi=160)
    plt.close(fig)


def save_flat_vs_fibonacci_comparison_plot(
    path: str = "outputs/figures/flat_vs_fibonacci_bankroll_path.png",
) -> None:
    config = RouletteConfig(spins=120)
    rng = np.random.default_rng(7)
    session = simulate_flat_vs_fibonacci_session(config, rng)

    session["flat_bankroll"] = session["flat_bankroll_units"] * config.unit_size
    session["fibonacci_bankroll"] = session["fibonacci_bankroll_units"] * config.unit_size
    flat_peak_index = session["flat_bankroll"].idxmax()
    flat_max_drawdown_index = session["flat_drawdown_units"].idxmax()
    fibonacci_peak_index = session["fibonacci_bankroll"].idxmax()
    fibonacci_max_drawdown_index = session["fibonacci_drawdown_units"].idxmax()

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.plot(
        session["spin"],
        session["flat_bankroll"],
        label="Flat 1-unit betting",
        color="#2f5f8f",
        linewidth=2,
    )
    ax.plot(
        session["spin"],
        session["fibonacci_bankroll"],
        label="Fibonacci betting",
        color="#b3261e",
        linewidth=2,
    )
    ax.axhline(
        config.starting_bankroll,
        color="black",
        linestyle=":",
        linewidth=1.5,
        label="Starting bankroll",
    )
    ax.scatter(
        session.loc[flat_peak_index, "spin"],
        session.loc[flat_peak_index, "flat_bankroll"],
        color="#5dade2",
        edgecolor="black",
        s=70,
        zorder=4,
        label="Flat max run-up",
    )
    ax.scatter(
        session.loc[flat_max_drawdown_index, "spin"],
        session.loc[flat_max_drawdown_index, "flat_bankroll"],
        color="#1f3f66",
        edgecolor="white",
        s=80,
        zorder=4,
        label="Flat max drawdown point",
    )
    ax.scatter(
        session.loc[fibonacci_peak_index, "spin"],
        session.loc[fibonacci_peak_index, "fibonacci_bankroll"],
        color="#2f7d32",
        edgecolor="black",
        s=80,
        zorder=4,
        label="Fibonacci max run-up",
    )
    ax.scatter(
        session.loc[fibonacci_max_drawdown_index, "spin"],
        session.loc[fibonacci_max_drawdown_index, "fibonacci_bankroll"],
        color="#111111",
        edgecolor="white",
        s=90,
        zorder=4,
        label="Fibonacci max drawdown point",
    )
    ax.set_title("Single $1,000 Bankroll Simulation: Flat vs Fibonacci Betting")
    ax.set_xlabel("Betting entry (same outcomes for both paths)")
    ax.set_ylabel("Bankroll ($)")
    ax.legend()
    ax.yaxis.set_major_formatter(lambda value, _: f"${value:,.0f}")
    fig.tight_layout()
    save_figure(fig, path, dpi=160)
    plt.close(fig)


def save_flat_final_bankroll_distribution_plot(
    path: str = "outputs/figures/flat_final_bankroll_distribution.png",
    sessions: int = 10000,
    spins: int = 120,
    seed: int = 42,
) -> None:
    config = RouletteConfig(spins=spins)
    rng = np.random.default_rng(seed)
    final_bankrolls = []

    for _ in range(sessions):
        session = simulate_flat_session(config, rng)
        if session.empty:
            final_bankroll_units = config.starting_bankroll_units
        else:
            final_bankroll_units = session["bankroll_units"].iloc[-1]
        final_bankrolls.append(final_bankroll_units * config.unit_size)

    final_bankrolls = np.array(final_bankrolls)
    mean_final = float(np.mean(final_bankrolls))
    median_final = float(np.median(final_bankrolls))
    profit_rate = float(np.mean(final_bankrolls >= config.starting_bankroll))

    lower_bin = int(np.floor(final_bankrolls.min() / 15) * 15) - 7.5
    upper_bin = int(np.ceil(final_bankrolls.max() / 15) * 15) + 22.5
    bins = np.arange(lower_bin, upper_bin + 15, 15)

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.hist(
        final_bankrolls,
        bins=bins,
        color="#2f5f8f",
        edgecolor="white",
        linewidth=0.7,
        alpha=0.88,
    )
    ax.axvline(
        config.starting_bankroll,
        color="black",
        linestyle=":",
        linewidth=2,
        label=f"Starting bankroll = ${config.starting_bankroll:,.0f}",
    )
    ax.axvline(
        mean_final,
        color="#b3261e",
        linestyle="--",
        linewidth=2,
        label=f"Mean final bankroll = ${mean_final:,.0f}",
    )

    summary_text = (
        f"Sessions: {sessions:,}\n"
        f"Median final = ${median_final:,.0f}\n"
        f"Finished >= $1,000: {profit_rate:.1%}"
    )
    ax.text(
        0.98,
        0.72,
        summary_text,
        transform=ax.transAxes,
        ha="right",
        va="top",
        bbox={"boxstyle": "round,pad=0.35", "facecolor": "white", "alpha": 0.9},
    )
    ax.set_title(f"Flat 1-Unit Final Bankroll Distribution ({sessions:,} Simulations)")
    ax.set_xlabel(f"Final bankroll after {spins} placed bets")
    ax.set_ylabel("Session count")
    ax.xaxis.set_major_formatter(lambda value, _: f"${value:,.0f}")
    ax.legend(loc="upper left")
    fig.tight_layout()
    save_figure(fig, path, dpi=160)
    plt.close(fig)


def save_fibonacci_equity_paths_plot(
    path: str = "outputs/figures/fibonacci_equity_paths.png",
    sessions: int = 10000,
    spins: int = 120,
    seed: int = 42,
    sample_paths: int = 1000,
) -> None:
    save_equity_paths_plot(
        simulate_session=simulate_fibonacci_session,
        path=path,
        title=(
            "Fibonacci Monte Carlo Bankroll Paths "
            f"({sample_paths:,} of {sessions:,} Sessions Shown)"
        ),
        sessions=sessions,
        spins=spins,
        seed=seed,
        sample_paths=sample_paths,
    )


def save_flat_equity_paths_plot(
    path: str = "outputs/figures/flat_equity_paths.png",
    sessions: int = 10000,
    spins: int = 120,
    seed: int = 42,
    sample_paths: int = 1000,
) -> None:
    save_equity_paths_plot(
        simulate_session=simulate_flat_session,
        path=path,
        title=(
            "Flat 1-Unit Monte Carlo Bankroll Paths "
            f"({sample_paths:,} of {sessions:,} Sessions Shown)"
        ),
        sessions=sessions,
        spins=spins,
        seed=seed,
        sample_paths=sample_paths,
    )


def save_equity_paths_plot(
    simulate_session,
    path: str,
    title: str,
    sessions: int,
    spins: int,
    seed: int,
    sample_paths: int,
) -> None:
    config = RouletteConfig(spins=spins)
    rng = np.random.default_rng(seed)
    sample_count = min(sample_paths, sessions)
    sampled_session_indexes = set(
        np.linspace(0, sessions - 1, sample_count, dtype=int)
    )

    paths = []
    final_bankrolls = []

    for session_index in range(sessions):
        session = simulate_session(config, rng)
        if session.empty:
            final_bankroll = config.starting_bankroll
        else:
            final_bankroll = float(session["bankroll_units"].iloc[-1] * config.unit_size)

        final_bankrolls.append(final_bankroll)

        if session_index in sampled_session_indexes:
            bankroll = np.full(spins + 1, np.nan)
            bankroll[0] = config.starting_bankroll

            if not session.empty:
                played_spins = session["spin"].astype(int).to_numpy()
                bankroll[played_spins] = (
                    session["bankroll_units"].to_numpy() * config.unit_size
                )
                final_spin = int(played_spins[-1])
                if final_spin < spins:
                    bankroll[final_spin + 1 :] = final_bankroll
            else:
                bankroll[1:] = final_bankroll

            paths.append((bankroll, final_bankroll))

    x_values = np.arange(spins + 1)
    final_bankrolls = np.array(final_bankrolls)
    median_final = float(np.median(final_bankrolls))
    profit_rate = float(np.mean(final_bankrolls >= config.starting_bankroll))
    ruin_rate = float(np.mean(final_bankrolls <= 0))

    with plt.style.context("dark_background"):
        fig, ax = plt.subplots(figsize=(14, 6))
        fig.patch.set_facecolor("#050505")
        ax.set_facecolor("#050505")

        for bankroll, final_bankroll in paths:
            color = "#5ad7a0" if final_bankroll >= config.starting_bankroll else "#ff6f7d"
            ax.plot(x_values, bankroll, color=color, alpha=0.16, linewidth=0.9)

        ax.axhline(
            config.starting_bankroll,
            color="#d7dde4",
            linestyle="--",
            linewidth=1.4,
            alpha=0.9,
            label="Starting bankroll",
        )
        ax.axhline(
            0,
            color="#ff6f7d",
            linestyle="--",
            linewidth=1.4,
            alpha=0.9,
            label="Ruin",
        )

        ax.set_title(
            title,
            loc="left",
            color="#d7dde4",
            fontsize=14,
            pad=14,
        )
        ax.text(
            0,
            1.02,
            (
                f"Placed bets per session: {spins}    "
                f"Simulations: {sessions:,}    "
                f"Displayed paths: {len(paths):,}    "
                f"Median final bankroll: ${median_final:,.0f}    "
                f"Finished >= $1,000: {profit_rate:.1%}    "
                f"Reached $0: {ruin_rate:.1%}"
            ),
            transform=ax.transAxes,
            color="#9aa0a6",
            fontsize=10,
        )
        ax.set_xlabel("Betting entry", color="#d7dde4")
        ax.set_ylabel("Bankroll ($)", color="#d7dde4")
        ax.yaxis.set_major_formatter(lambda value, _: f"${value:,.0f}")
        ax.tick_params(colors="#9aa0a6")
        ax.grid(color="#2b3035", linestyle="--", linewidth=0.8, alpha=0.7)
        ax.spines["bottom"].set_color("#2b3035")
        ax.spines["left"].set_color("#2b3035")
        ax.spines["top"].set_color("#2b3035")
        ax.spines["right"].set_color("#2b3035")
        ax.legend(loc="upper right", frameon=False, labelcolor="#d7dde4")
        fig.tight_layout()
        save_figure(fig, path, dpi=160, facecolor=fig.get_facecolor())
        plt.close(fig)


def save_fibonacci_ruin_probability_by_session_length_plot(
    path: str = "outputs/figures/fibonacci_ruin_probability_by_session_length.png",
    session_lengths: tuple[int, ...] = (50, 120, 500, 1000),
    sessions: int = 10000,
    seed: int = 42,
) -> None:
    strategies = [
        ("Base Fibonacci", simulate_fibonacci_session, "#b3261e"),
        ("With $500 recovery rule", simulate_fibonacci_with_max_recovery_session, "#2f5f8f"),
    ]
    rows = []

    for label, simulate_session, color in strategies:
        for spins in session_lengths:
            config = RouletteConfig(spins=spins)
            rng = np.random.default_rng(seed)
            ruined_sessions = 0

            for _ in range(sessions):
                session = simulate_session(config, rng)
                if session.empty:
                    final_bankroll_units = config.starting_bankroll_units
                else:
                    final_bankroll_units = session["bankroll_units"].iloc[-1]

                ruined_sessions += final_bankroll_units <= 0

            rows.append(
                {
                    "strategy": label,
                    "spins": spins,
                    "ruined_sessions": ruined_sessions,
                    "ruin_probability": ruined_sessions / sessions,
                    "color": color,
                }
            )

    results = pd.DataFrame(rows)
    fig, ax = plt.subplots(figsize=(11, 6))

    label_offsets = {
        "Base Fibonacci": -0.035,
        "With $500 recovery rule": 0.025,
    }

    for label, _, color in strategies:
        strategy_rows = results.loc[results["strategy"].eq(label)]
        ax.plot(
            strategy_rows["spins"],
            strategy_rows["ruin_probability"],
            marker="o",
            linewidth=2.6,
            markersize=7,
            color=color,
            label=label,
        )

        for _, row in strategy_rows.iterrows():
            offset = label_offsets[label]
            ax.text(
                row["spins"],
                row["ruin_probability"] + offset,
                f"{row['ruin_probability']:.1%}",
                ha="center",
                va="bottom" if offset > 0 else "top",
                fontsize=9,
                color=color,
                fontweight="bold",
            )

    ax.set_title("Fibonacci Ruin Probability by Session Length")
    ax.set_xlabel("Placed bets per session")
    ax.set_ylabel("Estimated probability of reaching $0")
    ax.set_xticks(list(session_lengths))
    ax.set_ylim(0, 0.95)
    ax.yaxis.set_major_formatter(lambda value, _: f"{value:.0%}")
    ax.grid(True, axis="y", alpha=0.35)
    ax.legend(loc="lower right")
    ax.text(
        0.01,
        0.97,
        f"{sessions:,} simulations per session length, $1,000 starting bankroll",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=10,
        bbox={"boxstyle": "round,pad=0.35", "facecolor": "white", "alpha": 0.9},
    )
    fig.tight_layout()
    save_figure(fig, path, dpi=160)
    plt.close(fig)


def save_two_to_one_first_bet_volatility_plot(
    path: str = "outputs/figures/two_to_one_first_bet_volatility.png",
    bets: int = 10000,
    seed: int = 24,
) -> None:
    rng = np.random.default_rng(seed)

    later_wins = rng.random(bets - 1) < COLUMN_WIN_PROBABILITY
    later_returns = np.where(later_wins, 2, -1)
    returns = np.concatenate(([2], later_returns))
    x_values = np.arange(1, bets + 1)

    average_return = np.cumsum(returns) / x_values * 100
    theoretical_ev_percentage = column_expected_value_units() * 100

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.plot(
        x_values,
        average_return,
        color="#2f7d32",
        linewidth=2.3,
        label="One simulation: flat 1-unit entries",
    )
    ax.axhline(
        theoretical_ev_percentage,
        color="#333333",
        linestyle="--",
        linewidth=2,
        label=f"Expected value = {theoretical_ev_percentage:.2f}%",
    )
    ax.axhline(
        0,
        color="#6b7280",
        linestyle=":",
        linewidth=2,
        label="Break-even",
    )
    ax.set_title("Flat 1-Unit 2:1 Roulette Entries Over 10,000 Bets")
    ax.set_xlabel("Number of flat 1-unit 2:1 entries (log scale)")
    ax.set_ylabel("Average return per bet")
    ax.set_xscale("log")
    ax.set_xlim(1, bets)
    ax.set_ylim(min(-25, float(average_return.min()) - 8), 220)
    ax.set_xticks([1, 10, 100, 1000, 10000])
    ax.xaxis.set_major_formatter(lambda value, _: f"{value:,.0f}")
    ax.yaxis.set_major_formatter(lambda value, _: f"{value:.0f}%")
    ax.grid(True, which="both", alpha=0.28)
    ax.legend(loc="upper right")
    fig.tight_layout()
    save_figure(fig, path, dpi=160)
    plt.close(fig)


def save_fibonacci_average_return_over_time_plot(
    path: str = "outputs/figures/fibonacci_average_return_over_time.png",
    bets: int = 10000,
    seed: int = 24,
) -> None:
    config = RouletteConfig(spins=bets)
    sequence = fibonacci_sequence(config.table_max_units)
    rng = np.random.default_rng(seed)

    later_wins = rng.random(bets - 1) < COLUMN_WIN_PROBABILITY
    wins = np.concatenate(([True], later_wins))

    bet_units = np.empty(bets)
    profit_units = np.empty(bets)
    sequence_index = 0

    for index, win in enumerate(wins):
        bet_units[index] = min(sequence[sequence_index], config.table_max_units)

        if win:
            profit_units[index] = 2 * bet_units[index]
            sequence_index = 0
        else:
            profit_units[index] = -bet_units[index]
            sequence_index = min(sequence_index + 1, len(sequence) - 1)

    x_values = np.arange(1, bets + 1)
    average_return = np.cumsum(profit_units) / np.cumsum(bet_units) * 100
    theoretical_ev_percentage = column_expected_value_units() * 100

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.plot(
        x_values,
        average_return,
        color="#b3261e",
        linewidth=2.3,
        label="One simulation: Fibonacci entries",
    )
    ax.axhline(
        theoretical_ev_percentage,
        color="#333333",
        linestyle="--",
        linewidth=2,
        label=f"Expected value = {theoretical_ev_percentage:.2f}%",
    )
    ax.axhline(
        0,
        color="#6b7280",
        linestyle=":",
        linewidth=2,
        label="Break-even",
    )
    ax.set_title("Fibonacci 2:1 Entries: Average Return Per Unit Wagered")
    ax.set_xlabel("Number of Fibonacci 2:1 entries (log scale)")
    ax.set_ylabel("Average return per unit wagered")
    ax.set_xscale("log")
    ax.set_xlim(1, bets)
    ax.set_ylim(min(-25, float(average_return.min()) - 8), 220)
    ax.set_xticks([1, 10, 100, 1000, 10000])
    ax.xaxis.set_major_formatter(lambda value, _: f"{value:,.0f}")
    ax.yaxis.set_major_formatter(lambda value, _: f"{value:.0f}%")
    ax.grid(True, which="both", alpha=0.28)
    ax.legend(loc="upper right")
    fig.tight_layout()
    save_figure(fig, path, dpi=160)
    plt.close(fig)


def save_requested_average_return_plots() -> None:
    save_two_to_one_first_bet_volatility_plot()
    save_fibonacci_average_return_over_time_plot()


def generate_all_plots() -> None:
    save_requested_average_return_plots()
    save_flat_vs_fibonacci_comparison_plot()
    save_flat_equity_paths_plot()
    save_fibonacci_equity_paths_plot()
    save_flat_final_bankroll_distribution_plot()
    save_fibonacci_final_bankroll_distribution_plot()
    save_fibonacci_max_recovery_comparison_plot()
    save_fibonacci_ruin_probability_by_session_length_plot()


if __name__ == "__main__":
    generate_all_plots()
