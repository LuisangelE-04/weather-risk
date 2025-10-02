import plotly.express as px

# Sample dataset (built-in)
df = px.data.iris()

# Create a scatter plot
fig = px.scatter(
    df,
    x="sepal_width",
    y="sepal_length",
    color="species",   # categorical coloring
    size="petal_length", # bubble sizes
    hover_data=["petal_width"] # info on hover
)

# Line chart
fig = px.line(df, x="sepal_width", y="sepal_length", color="species")

# Bar chart
#fig = px.bar(df, x="species", y="sepal_length", barmode="group")

# Histogram
#fig = px.histogram(df, x="sepal_length", color="species")

# Box plot
#fig = px.box(df, x="species", y="sepal_length")

# Pie chart
#fig = px.pie(df, names="species", values="sepal_length")

fig.update_layout(
    title="Iris Sepal Length vs Width",
    xaxis_title="Sepal Width",
    yaxis_title="Sepal Length",
    legend_title="Species",
    template="plotly_dark"   # built-in themes: plotly, ggplot2, seaborn, simple_white, etc.
)
fig.show()

fig.show()
