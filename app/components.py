import streamlit as st


def metric_card(label: str, value: str, help_text: str | None = None) -> None:
    st.metric(label=label, value=value, help=help_text)


def insight_panel() -> None:
    st.subheader("Insight → Action → Recommendation → Decision")
    st.markdown(
        """
        **Insight:** High-cost claim types and regions drive most claim exposure.  
        **Action:** Investigate pricing, severity mix, and underwriting patterns.  
        **Recommendation:** Adjust premiums and strengthen risk review in high-cost segments.  
        **Decision:** Prioritize underwriting controls and monthly KPI monitoring.
        """
    )
