import streamlit as st

st.set_page_config(
    page_title="SevaReady",
    page_icon="📋",
    layout="centered",
)

SOURCE_URL = (
    "https://aaplesarkar.mahaonline.gov.in/pdf/"
    "Fees%2C%20Procedure%2C%20Checklist_Income%20Certificate.pdf"
)

PORTAL_URL = "https://aaplesarkar.mahaonline.gov.in/en"

# Guidance tips for Maharashtra revenue certificates
GUIDANCE = {
    "Electricity bill": "Must typically be recent (within the last 3 months) and show the current residential address.",
    "Ration card": "Should list the household members clearly and include the applicant.",
    "Self-declaration": "Must follow the official Annexure format available on the Aaple Sarkar portal, signed by the applicant or guardian.",
    "Bonafide certificate": "Typically accepted for minors currently enrolled in recognized educational institutions.",
}

st.title("📋 SevaReady")
st.subheader("Prepare before you apply")

st.write(
    "Prepare a document checklist for a Maharashtra "
    "income-certificate application."
)

st.warning(
    "Independent preparation prototype—not a government portal. "
    "This app does not verify documents, submit applications, "
    "or guarantee approval."
)

st.info(
    "You do not need to upload documents or enter sensitive "
    "personal information such as identification numbers or income amounts."
)

with st.form("preparation_form"):
    st.header("Tell us what you have")

    applicant_age = st.radio(
        "Is the applicant under 18?",
        ["Select an answer", "Yes", "No", "Unsure"],
    )

    identity = st.selectbox(
        "Choose an identity document you have",
        [
            "Select an answer",
            "PAN card",
            "Passport",
            "Aadhaar card",
            "Voter ID card",
            "Driving licence",
            "Another document — needs checking",
            "None / unsure",
        ],
    )

    address = st.selectbox(
        "Choose an address document you have",
        [
            "Select an answer",
            "Passport",
            "Water bill",
            "Ration card",
            "Aadhaar card",
            "Voter ID card",
            "Telephone bill",
            "Driving licence",
            "Electricity bill",
            "Property tax receipt",
            "Another document — needs checking",
            "None / unsure",
        ],
    )

    st.caption(
        "These menus show a subset of the options in our draft "
        "service sheet, not the complete official list."
    )

    age_proof = st.selectbox(
        "If the applicant is a minor, which age document is available?",
        [
            "Select an answer / not applicable",
            "Birth certificate",
            "Bonafide certificate",
            "School leaving certificate",
            "Another document — needs checking",
            "None / unsure",
        ],
    )

    declaration = st.radio(
        "Have you prepared the required self-declaration?",
        ["Select an answer", "Yes", "No", "Unsure"],
    )

    submitted = st.form_submit_button(
        "Generate my checklist",
        type="primary",
    )

if submitted:
    required_answers = [
        applicant_age,
        identity,
        address,
        declaration,
    ]

    if "Select an answer" in required_answers:
        st.error("Please answer each main question first.")
    else:
        st.header("Your preparation checklist")

        results = []

        def add_result(label, status, detail):
            results.append({"label": label, "status": status, "detail": detail})

        for label, answer in [
            ("Identity proof", identity),
            ("Address proof", address),
        ]:
            if answer == "None / unsure":
                add_result(
                    label,
                    "Needs attention",
                    "Check the official instructions for an accepted option.",
                )
            elif answer == "Another document — needs checking":
                add_result(
                    label,
                    "Needs confirmation",
                    "Confirm whether your document is accepted.",
                )
            else:
                add_result(
                    label,
                    "Reported available",
                    f"You selected: {answer}. Acceptance is not verified.",
                )

        if applicant_age == "Yes":
            if age_proof in [
                "Select an answer / not applicable",
                "None / unsure",
            ]:
                add_result(
                    "Minor's age proof",
                    "Needs attention",
                    "Choose an age-proof document and confirm requirements.",
                )
            elif age_proof == "Another document — needs checking":
                add_result(
                    "Minor's age proof",
                    "Needs confirmation",
                    "Confirm whether your age-proof document is accepted.",
                )
            else:
                add_result(
                    "Minor's age proof",
                    "Reported available",
                    f"You selected: {age_proof}. Acceptance is not verified.",
                )

        elif applicant_age == "Unsure":
            add_result(
                "Minor's age proof",
                "Needs confirmation",
                "Clarify the applicant's age before completing this section.",
            )
        else:
            add_result(
                "Minor's age-proof section",
                "Not applicable",
                "Based only on your answer that the applicant is not under 18.",
            )

        if declaration == "Yes":
            add_result(
                "Self-declaration",
                "Reported prepared",
                "Confirm that it matches the official required format.",
            )
        elif declaration == "No":
            add_result(
                "Self-declaration",
                "Needs attention",
                "Check the required format and prepare the declaration.",
            )
        else:
            add_result(
                "Self-declaration",
                "Needs confirmation",
                "Check whether you have prepared the declaration in the required format.",
            )

        add_result(
            "Additional and purpose-specific attachments",
            "Needs confirmation",
            "Check the live official application for income-related and purpose-specific attachments.",
        )

        for item in results:
            text = f"{item['label']} — {item['status']}\n\n{item['detail']}"
            if item["status"] in ["Reported available", "Reported prepared"]:
                st.success(text)
            elif item["status"] == "Not applicable":
                st.info(text)
            else:
                st.warning(text)

        # Contextual guidance
        selected_docs = [identity, address, age_proof]
        if declaration == "Yes":
            selected_docs.append("Self-declaration")

        active_tips = {doc: GUIDANCE[doc] for doc in selected_docs if doc in GUIDANCE}

        if active_tips:
            with st.expander("💡 Helpful document tips & validity rules", expanded=True):
                for doc_name, tip in active_tips.items():
                    st.markdown(f"**{doc_name}**: {tip}")

        st.subheader("What should I do next?")

        action_items = [
            item
            for item in results
            if item["status"] in ["Needs attention", "Needs confirmation"]
        ]

        if action_items:
            st.write(
                "Start with the following items. "
                "Your answers have not been independently verified."
            )
            for number, item in enumerate(action_items, start=1):
                st.write(f"{number}. {item['label']}: {item['detail']}")
        else:
            st.info(
                "No missing items were identified from your answers. "
                "Check the current official requirements before applying."
            )

        with st.expander("Frequently Asked Questions"):
            st.markdown(
                """
                - **Can I submit a document in my parents' name?**  
                  For minors, parents' documents are generally accepted. For adults, electricity bills or ration cards showing your family relation may require additional proof (like an affidavit or ration card listing).
                - **What format is needed for the self-declaration?**  
                  It must follow the standard Government Annexure format available on the Aaple Sarkar portal.
                - **Does this guarantee certificate approval?**  
                  No. SevaReady is an independent preparation checklist. Final verification is conducted by the revenue authority.
                """
            )

        st.subheader("Official information")
        st.link_button("Open the official checklist PDF",