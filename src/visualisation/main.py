import boto3
import awswrangler as wr
import streamlit as st
import plotly.express as px


def create_df_from_athena():
    sql = "select * from valorant_data_curated"
    df = wr.athena.read_sql_query(
        sql=sql, database="valorant-database", ctas_approach=True
    )
    df = (
        df.groupby("match_timestamp_local")
        .agg({"headshots": "mean", "bodyshots": "mean", "legshots": "mean"})
        .reset_index()
    )
    df["total_shots"] = df["headshots"] + df["bodyshots"] + df["legshots"]
    df["headshot_pct"] = (df["headshots"] / df["total_shots"]) * 100
    df["bodyshot_pct"] = (df["bodyshots"] / df["total_shots"]) * 100
    df["legshot_pct"] = (df["legshots"] / df["total_shots"]) * 100
    return df


def create_accuracy_graph(df):
    accuracy_graph = px.line(
        df,
        x="match_timestamp_local",
        y=["headshot_pct", "bodyshot_pct", "legshot_pct"],
        title="Accuracy Over Time",
    )
    accuracy_graph.update_layout(xaxis_title="Date", yaxis_title="Shots Count")
    return accuracy_graph


def main():
    st.title("Valorant Statistics")
    df = create_df_from_athena()
    accuracy_graph = create_accuracy_graph(df)
    st.plotly_chart(accuracy_graph)


if __name__ == "__main__":
    main()
