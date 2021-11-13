#
#
#
# old stuff
#


# def plot_1_cases(df: DataFrame, filename: str, landkreis_name: str):
#     """
#     plot 1.png
#     """

#     fig, axes = plt.subplots(figsize=(8, 6))

#     colors = ('blue', 'black')

#     myPlot = df['Cases_New'].plot(
#         linewidth=1.0, legend=False, zorder=1, color=colors[0])
#     df['Cases_New_roll_sum_20'].plot(
#         linewidth=2.0, legend=False, zorder=2, color=colors[1], secondary_y=True)

#     axes.set_ylim(0, )
#     axes.right_ax.set_ylim(0, )

#     plt.title(f'{landkreis_name}: Fallzahlen und 20-Tagessumme')
#     axes.set_xlabel("")
#     axes.set_ylabel('Fälle täglich')
#     axes.right_ax.set_ylabel('Fälle 20-Tage-Summe')
#     # color of label and ticks
#     axes.yaxis.label.set_color(colors[0])
#     axes.right_ax.yaxis.label.set_color(colors[1])
#     axes.tick_params(axis='y', colors=colors[0])
#     axes.right_ax.tick_params(axis='y', colors=colors[1])
#     # grid
#     axes.set_axisbelow(True)  # for grid below the lines
#     axes.grid(zorder=-1)

#     plt.tight_layout()
#     plt.savefig(fname=filename, format='png')


# def plot_2_its_per_20day_cases(df: DataFrame, filename: str, landkreis_name: str):
#     """
#     plot 2.png
#     """

#     fig, axes = plt.subplots(figsize=(8, 6))

#     colors = ('blue', 'black')

#     myPlot = df['quote_its_belegt_pro_Cases_New_roll_sum_20'].plot(
#         linewidth=2.0, legend=False, zorder=1, color=colors[0])

#     axes.set_ylim(0, 0.030)

#     plt.title(f'{landkreis_name}: Quote ITS-Belegung pro 20-Tage-Fallzahl')
#     axes.set_xlabel("")
#     axes.set_ylabel('')
#     # color of label and ticks
#     axes.yaxis.label.set_color(colors[0])
#     axes.tick_params(axis='y', colors=colors[0])
#     # grid
#     axes.set_axisbelow(True)  # for grid below the lines
#     axes.grid(zorder=-1)

#     plt.tight_layout()
#     plt.savefig(fname=filename, format='png')


# def plot_3_betten_belegt(df: DataFrame, filename: str, landkreis_name: str):
#     """
#     plot 3.png
#     """

#     fig, axes = plt.subplots(figsize=(8, 6))

#     colors = ('blue', 'black', 'lightskyblue')

#     myPlot = df['betten_belegt'].plot(
#         linewidth=1.0, legend=False, zorder=1, color=colors[2])
#     df['betten_belegt_roll'].plot(
#         linewidth=2.0, legend=False, zorder=1, color=colors[0])

#     df['Cases_New_roll_sum_20'].plot(
#         linewidth=2.0, legend=False, zorder=2, color=colors[1], secondary_y=True)

#     axes.set_ylim(0, )
#     axes.right_ax.set_ylim(0, )

#     plt.title(f'{landkreis_name}: ICU Bettenbelegung')
#     axes.set_xlabel("")
#     axes.set_ylabel('Betten belegt')
#     axes.right_ax.set_ylabel('Fälle 20-Tage-Summe')
#     # color of label and ticks
#     axes.yaxis.label.set_color(colors[0])
#     axes.right_ax.yaxis.label.set_color(colors[1])
#     axes.tick_params(axis='y', colors=colors[0])
#     axes.right_ax.tick_params(axis='y', colors=colors[1])
#     # grid
#     axes.set_axisbelow(True)  # for grid below the lines
#     axes.grid(zorder=-1)

#     plt.tight_layout()
#     plt.savefig(fname=filename, format='png')


# model test plots, to verify my coding against Dirk's
# plot_1_cases(
#     df=df_data, filename=f"icu-forecast-howto/1_tm.png", landkreis_name=landkreis_name)
# plot_2_its_per_20day_cases(
#     df=df_data, filename=f"icu-forecast-howto/2_tm.png", landkreis_name=landkreis_name)
# plot_3_betten_belegt(
#     df=df_data, filename=f"icu-forecast-howto/3_tm.png", landkreis_name=landkreis_name)
