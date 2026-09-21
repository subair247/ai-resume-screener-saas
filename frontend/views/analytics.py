import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def render():
    st.title("Recruiter Analytics & Dashboard")
    
    if "matched_results" in st.session_state and st.session_state["matched_results"]:
        results = st.session_state["matched_results"]
        df = pd.DataFrame(results)
        
        if not df.empty and "candidate_id" in df.columns:
            df = df.drop_duplicates(subset=["candidate_id"])
            
        st.subheader("Overview Metrics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Total Candidates", value=len(df))
        with col2:
            avg_score = round(df["score"].mean(), 1) if "score" in df.columns else 0
            st.metric(label="Average Match Score", value=f"{avg_score}%")
        with col3:
            top_candidate = df.iloc[0]["name"] if not df.empty and "name" in df.columns else "N/A"
            st.metric(label="Top Candidate", value=top_candidate)
            
        st.markdown("---")
        
        if not df.empty and "name" in df.columns and "score" in df.columns:
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                st.subheader("Candidate Match Score Distribution")
                def get_bar_color(score):
                    if score < 40:
                        return "#FF3B30"
                    elif score < 70:
                        return "#FF9500"
                    else:
                        return "#34C759"
                        
                df["BarColor"] = df["score"].apply(get_bar_color)
                
                fig_bar = px.bar(
                    df,
                    x="name",
                    y="score",
                    text="score"
                )
                fig_bar.update_traces(marker_color=df["BarColor"].tolist(), texttemplate='%{text}%', textposition='outside', marker=dict(cornerradius=10))
                fig_bar.update_layout(
                    xaxis=dict(title="", showgrid=False, color="white"),
                    yaxis=dict(title="Score (%)", range=[0, 115], showgrid=True, gridcolor="#222", color="white"),
                    height=350,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_bar, use_container_width=True)
                
            with col_chart2:
                st.subheader("Score Tier Breakdown")
                def get_tier(score):
                    if score < 40:
                        return "Poor (<40%)"
                    elif score < 70:
                        return "Average (40-70%)"
                    else:
                        return "Excellent (>=70%)"
                        
                df["Tier"] = df["score"].apply(get_tier)
                tier_counts = df["Tier"].value_counts().reset_index()
                tier_counts.columns = ["Tier", "Count"]
                
                fig_pie = px.pie(
                    tier_counts,
                    names="Tier",
                    values="Count",
                    hole=0.5,
                    color="Tier",
                    color_discrete_map={
                        "Poor (<40%)": "#FF3B30",
                        "Average (40-70%)": "#FF9500",
                        "Excellent (>=70%)": "#34C759"
                    }
                )
                fig_pie.update_layout(
                    height=350,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color="white"),
                    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
        st.markdown("---")
        st.subheader("Screened Candidates Database")
        st.dataframe(df, hide_index=True)
        
        st.markdown("---")
        st.subheader("Export Screening Reports")
        csv_data = df.to_csv(index=False).encode('utf-8')
        col_exp1, col_exp2 = st.columns(2)
        with col_exp1:
            st.download_button(
                label="Download CSV Report",
                data=csv_data,
                file_name="candidate_screening_report.csv",
                mime="text/csv",
                use_container_width=True
            )
        with col_exp2:
            markdown_report = df.to_markdown(index=False)
            st.download_button(
                label="Download Text Report",
                data=markdown_report,
                file_name="candidate_screening_report.txt",
                mime="text/plain",
                use_container_width=True
            )
    else:
        st.info("No screening data available. Please run a screening session in the Upload Hub first.")