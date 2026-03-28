import plotly.graph_objects as go
import plotly.io as pio
import json
import os

def chart_healing_score(history):
    """
    Creates a line chart showing healing score over days.

    Input  : history (list of dicts) — each dict has "day" and "healing_score"
             Example: [{"day": 1, "healing_score": 45}, {"day": 2, "healing_score": 58}]
    Output : fig (plotly figure object)
    """

    # Step 1: Pull out the day numbers and scores from history
    # This is called a "list comprehension" — it loops through history
    # and picks one value from each record
    days = [r["day"] for r in history]
    scores = [r["healing_score"] for r in history]

    # Step 2: Decide line colour based on the most recent score
    # Get the last score in the list
    last_score = scores[-1] if len(scores) > 0 else 0

    if last_score > 60:
        line_color = "green"
    elif last_score >= 40:
        line_color = "orange"
    else:
        line_color = "red"

    # Step 3: Create the line chart trace
    # A "trace" is one dataset plotted on the chart
    line_trace = go.Scatter(
        x=days,                    # x-axis values (day numbers)
        y=scores,                  # y-axis values (healing scores)
        mode="lines+markers",      # draw both a line AND dots at each data point
        name="Healing Score",      # label shown in the legend
        line=dict(
            color=line_color,      # colour we decided above
            width=3                # line thickness in pixels
        ),
        marker=dict(
            size=8,                # dot size in pixels
            color=line_color       # dot colour same as line
        )
    )

    # Step 4: Create a horizontal reference line at 70
    # This shows the "target" — if score is above 70, patient is recovering well
    target_line = go.Scatter(
        x=days,
        y=[70] * len(days),        # flat line — same value (70) for every day
        mode="lines",
        name="Target (70)",
        line=dict(
            color="blue",
            width=1,
            dash="dash"            # makes it a dashed line so it looks different
        )
    )

    # Step 5: Combine both traces into one figure
    fig = go.Figure(data=[line_trace, target_line])

    # Step 6: Style the chart — title, axis labels, background
    fig.update_layout(
        title="Healing Score Over Time",
        xaxis_title="Day",
        yaxis_title="Healing Score (0-100)",
        yaxis=dict(range=[0, 100]),   # always show full 0-100 range
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(size=13)
    )

    return fig

def chart_redness_trend(history):
    """
    Creates a filled area chart showing redness level over days.

    Input  : history (list of dicts) — each dict has "day" and "redness"
    Output : fig (plotly figure object)
    """

    # Pull out day numbers and redness values from history
    days = [r["day"] for r in history]
    redness_values = [r["redness"] for r in history]

    # Create a filled area trace
    # "fill='tozeroy'" means the area between the line and the bottom (y=0) is filled
    area_trace = go.Scatter(
        x=days,
        y=redness_values,
        mode="lines",
        name="Redness Level",
        fill="tozeroy",                        # fill area below the line down to y=0
        line=dict(color="red", width=2),
        fillcolor="rgba(255, 0, 0, 0.3)"       # red fill with 30% opacity
        # rgba means: Red=255, Green=0, Blue=0, Alpha(opacity)=0.3
    )

    # Build the figure
    fig = go.Figure(data=[area_trace])

    # Style it
    fig.update_layout(
        title="Redness Level Over Time",
        xaxis_title="Day",
        yaxis_title="Redness Score (0 to 1)",
        yaxis=dict(range=[0, 1]),    # redness is always between 0 and 1
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(size=13)
    )

    return fig

def chart_wound_area(history):
    """
    Creates a bar chart showing wound area over days.
    Green bars = area decreased from previous day (healing).
    Orange bars = area increased from previous day (worsening).

    Input  : history (list of dicts) — each dict has "day" and "area"
    Output : fig (plotly figure object)
    """

    # Pull out day numbers and area values
    days = [r["day"] for r in history]
    areas = [r["area"] for r in history]

    # Decide the colour of each bar based on whether area went up or down
    # We loop through each day and compare it to the previous day
    bar_colors = []

    for i in range(len(areas)):
        if i == 0:
            # First day — no previous day to compare, use grey
            bar_colors.append("grey")
        elif areas[i] < areas[i - 1]:
            # Area went DOWN compared to yesterday — good — green
            bar_colors.append("green")
        else:
            # Area went UP or stayed same — bad — orange
            bar_colors.append("orange")

    # Create the bar chart trace
    bar_trace = go.Bar(
        x=days,
        y=areas,
        name="Wound Area",
        marker=dict(color=bar_colors)   # use the colour list we just built
    )

    # Build the figure
    fig = go.Figure(data=[bar_trace])

    # Style it
    fig.update_layout(
        title="Wound Area Over Time (pixels)",
        xaxis_title="Day",
        yaxis_title="Wound Area (pixels)",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(size=13)
    )

    return fig

def chart_risk_gauge(risk_pct):
    """
    Creates a gauge (speedometer-style) chart showing infection risk.

    Input  : risk_pct (int or float) — infection risk percentage, 0 to 100
    Output : fig (plotly figure object)
    """

    fig = go.Figure(go.Indicator(
        mode="gauge+number",        # show both the gauge arc AND the number in the middle
        value=risk_pct,             # the current risk value to display
        title={"text": "Infection Risk %", "font": {"size": 16}},

        gauge={
            "axis": {
                "range": [0, 100],       # gauge goes from 0 to 100
                "tickwidth": 1,
                "tickcolor": "darkgrey"
            },
            "bar": {
                "color": "darkred"       # the needle/bar colour
            },
            "steps": [
                # Each step is a coloured zone on the gauge arc
                {"range": [0,  25],  "color": "green"},   # 0-25 = Low risk
                {"range": [25, 50],  "color": "yellow"},  # 25-50 = Medium risk
                {"range": [50, 75],  "color": "orange"},  # 50-75 = High risk
                {"range": [75, 100], "color": "red"},     # 75-100 = Critical
            ],
            "threshold": {
                # Draws a bold line at 70 to mark the danger threshold
                "line": {"color": "black", "width": 4},
                "thickness": 0.75,
                "value": 70
            }
        }
    ))

    # Style it
    fig.update_layout(
        paper_bgcolor="white",
        font=dict(size=13),
        height=300       # make it a bit smaller than the other charts
    )

    return fig

def export_all_charts(history, risk_pct, patient_id, day):
    """
    Runs all 4 chart functions, saves PNGs, and returns JSON for frontend.

    Input  : history    (list of dicts) — full patient history
             risk_pct   (int)           — current infection risk percentage
             patient_id (string)        — e.g. "patient_001"
             day        (int)           — current day number
    Output : dict containing JSON strings of all 4 charts
    """

    # Step 1: Make sure the output folder exists
    # exist_ok=True means: don't crash if folder already exists
    os.makedirs("outputs/charts", exist_ok=True)

    # Step 2: Generate all 4 figures by calling the functions above
    print("  Building healing score chart...")
    fig1 = chart_healing_score(history)

    print("  Building redness trend chart...")
    fig2 = chart_redness_trend(history)

    print("  Building wound area chart...")
    fig3 = chart_wound_area(history)

    print("  Building infection risk gauge...")
    fig4 = chart_risk_gauge(risk_pct)

    # Step 3: Save each figure as a PNG image file
    # The file name includes patient_id and day so files don't overwrite each other
    path1 = f"outputs/charts/{patient_id}_day{day}_healing_score.png"
    path2 = f"outputs/charts/{patient_id}_day{day}_redness.png"
    path3 = f"outputs/charts/{patient_id}_day{day}_wound_area.png"
    path4 = f"outputs/charts/{patient_id}_day{day}_risk_gauge.png"

    print("  Saving chart PNGs...")

    try:
        fig1.write_image(path1)
        print("  Saved:", path1)

        fig2.write_image(path2)
        print("  Saved:", path2)

        fig3.write_image(path3)
        print("  Saved:", path3)

        fig4.write_image(path4)
        print("  Saved:", path4)

    except Exception as e:
        # If kaleido is not installed, PNG export will fail
        # We warn but don't crash — JSON export below will still work
        print("  Warning: Could not save PNG files.")
        print("  Reason:", str(e))
        print("  Fix: run   pip install kaleido   then try again.")

    # Step 4: Convert each figure to a JSON string for the frontend
    # The React frontend will use these JSON strings to render charts
    chart_jsons = {
        "healing_score_chart": fig1.to_json(),
        "redness_chart":       fig2.to_json(),
        "area_chart":          fig3.to_json(),
        "risk_gauge":          fig4.to_json()
    }

    return chart_jsons

if __name__ == "__main__":

    print("=" * 50)
    print("  HealTrack AI — Visualisation Module Test")
    print("=" * 50)

    # Create fake history data to test with
    # In the real pipeline this comes from history.json
    # We are just making dummy data here to check charts work
    fake_history = [
        {"day": 1, "healing_score": 30, "redness": 0.75, "area": 5000},
        {"day": 2, "healing_score": 38, "redness": 0.68, "area": 4800},
        {"day": 3, "healing_score": 47, "redness": 0.60, "area": 4400},
        {"day": 4, "healing_score": 55, "redness": 0.52, "area": 4000},
        {"day": 5, "healing_score": 63, "redness": 0.44, "area": 3500},
        {"day": 6, "healing_score": 70, "redness": 0.38, "area": 3000},
        {"day": 7, "healing_score": 76, "redness": 0.30, "area": 2600},
    ]

    fake_risk_pct = 35      # medium risk for testing
    fake_patient_id = "patient_001"
    fake_day = 7

    print("")
    print("Running export_all_charts with fake data...")
    print("")

    chart_jsons = export_all_charts(
        history=fake_history,
        risk_pct=fake_risk_pct,
        patient_id=fake_patient_id,
        day=fake_day
    )

    print("")
    print("── Results ──────────────────────────────────")
    print("  Charts generated:", len(chart_jsons))
    print("  Chart keys:", list(chart_jsons.keys()))
    print("")
    print("  Check the outputs/charts/ folder for PNG files.")
    print("")
    print("All done!")
    print("=" * 50)

    
