# Q2 2026 summary

Revenue grew from 410k in January to 540k in June, with the strongest month in June (see metrics.csv).
Monthly churn fell from 3.1% to 1.9% over the same period.

```mermaid
xychart-beta
    title "Revenue grew from $410k to $540k"
    x-axis [Jan, Feb, Mar, Apr, May, Jun]
    y-axis "Revenue (USD thousands)" 0 --> 600
    line [410, 425, 470, 455, 505, 540]
```

```mermaid
xychart-beta
    title "Monthly churn fell from 3.1% to 1.9%"
    x-axis [Jan, Feb, Mar, Apr, May, Jun]
    y-axis "Churn (%)" 0 --> 4
    line [3.1, 2.9, 2.4, 2.6, 2.1, 1.9]
```

The signup funnel still loses most users at activation: of 12,000 visitors, 3,100 signed up, 1,450 activated and 380 paid (funnel.csv).

```mermaid
xychart-beta
    title "Signup funnel: biggest drop-offs are visit-to-signup and activation-to-paid"
    x-axis ["Visited", "Signed up", "Activated", "Paid"]
    y-axis "Users" 0 --> 13000
    bar [12000, 3100, 1450, 380]
```

*Visited 12,000 → Signed up 3,100 (25.8% of visitors) → Activated 1,450 (46.8% of signups) → Paid 380 (26.2% of activated).*

Regional revenue for the quarter was North 610k, South 480k, East 320k, West 190k.

```mermaid
xychart-beta
    title "North led regional revenue at $610k"
    x-axis ["North", "South", "East", "West"]
    y-axis "Revenue (USD thousands)" 0 --> 700
    bar [610, 480, 320, 190]
```
