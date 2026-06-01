import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd


def plot_imputed_data(df, gaps, func):
    # extracts the datetime of the gaps
    gap_dates = pd.to_datetime(list(gaps.keys()), format="%Y-%m-%d %H:%M:%S")

    colors = mpl.color_sequences["Dark2"]

    # create subplots
    fig, axes = plt.subplots(
        len(gap_dates), 1, figsize=(12, 4 * len(gap_dates)), sharey=True
    )

    for ax, day in zip(axes, gaps.keys()):
        # define imputation window
        imputation_start = day
        imputation_end = day + pd.Timedelta(minutes=gaps[day])

        # define period window
        period_start = imputation_start - pd.Timedelta(minutes=60)
        period_end = imputation_end + pd.Timedelta(minutes=60)

        # define masks
        complete_period_mask = (df.index >= period_start) & (df.index < period_end)
        pre_period_mask = (df.index >= period_start) & (df.index < imputation_start)
        post_period_mask = (df.index >= imputation_end) & (df.index < period_end)
        periodm1_mask = (df.index >= (period_start - pd.Timedelta(days=1))) & (
            df.index < (period_end - pd.Timedelta(days=1))
        )

        # define series
        complete_period_series = df.loc[complete_period_mask, "Voltage"]
        pre_period_series = df.loc[pre_period_mask, "Voltage"]
        post_period_series = df.loc[post_period_mask, "Voltage"]
        periodm1_series = df.loc[periodm1_mask, "Voltage"].sort_index()

        # impute
        imputed_info_dict = func(complete_period_series)

        # plot imputed data
        for n, method in enumerate(imputed_info_dict.keys()):
            ax.plot(
                complete_period_series.index.time.astype(str),
                imputed_info_dict[method],
                color=colors[n],
                label=f"Imputation ({method})",
                linewidth=2,
            )

        # plot original data
        ax.plot(
            pre_period_series.index.time.astype(str),
            pre_period_series,
            color="blue",
            label="Today (original)",
            linewidth=2,
        )

        ax.plot(
            post_period_series.index.time.astype(str),
            post_period_series,
            color="blue",
            linewidth=2,
        )

        # plot data from one day before as reference
        ax.plot(
            periodm1_series.index.time.astype(str),
            periodm1_series,
            color="blue",
            linestyle="dashed",
            label="Day before (as reference)",
            linewidth=1,
            alpha=0.4,
        )

        # Highlight region
        ax.axvspan(
            (imputation_start - pd.Timedelta(minutes=1)).strftime("%X"),
            imputation_end.strftime("%X"),
            color="orange",
            alpha=0.3,
            label="Imputation Region",
        )

        # style
        ax.set_xticks(ax.get_xticks()[:: int(len(complete_period_series) / 10)])
        ax.set_xlabel("Time")
        ax.set_ylabel("Voltage")
        ax.set_title(f"Missing values on {day.date()} (Gap size: {gaps[day]} minutes)")

    # put one legend for the whole figure on top
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=4, fontsize=9)

    return fig, axes
