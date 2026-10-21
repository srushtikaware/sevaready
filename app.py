import streamlit as st

st.set_page_config(
    page_title="SevaReady",
    page_icon="📋",
    layout="centered",
)

SOURCE_URL = (
    "https://aaplesarkar.mahaonline.gov.in/pdf/"
    "Fees,%20Procedure,%20Checklist_Income%20Certificate.pdf"
)

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
    "You do not need to upload documents or enter Aadhaar numbers, "
    "income amounts, or other sensitive information."
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
            results.append(
                {"label": label, "status": status, "detail": detail}
            )

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

        add_result(
            "Self-declaration",
            "Reported prepared" if declaration == "Yes" else "Needs attention",
            (
                "Confirm that it matches the official required format."
                if declaration == "Yes"
                else "Check the required format and prepare the declaration."
            ),
        )

        add_result(
            "Additional and purpose-specific attachments",
            "Needs confirmation",
            "Check the live official application for income-related "
            "and purpose-specific attachments. Our draft information "
            "does not fully resolve these requirements.",
        )

        for item in results:
            text = (
                f"{item['label']} — {item['status']}\n\n"
                f"{item['detail']}"
            )
            if item["status"] in [
                "Reported available",
                "Reported prepared",
            ]:
                st.success(text)
            elif item["status"] == "Not applicable":
                st.info(text)
            else:
                st.warning(text)

        st.subheader("Official information")
        st.link_button("Open the official checklist PDF", SOURCE_URL)
        st.link_button(
            "Visit Aaple Sarkar",
            "https://aaplesarkar.mahaonline.gov.in/en",
        )

        summary = [
            "SevaReady — Preparation Checklist",
            "Service: Maharashtra Income Certificate",
            "",
        ]

        for item in results:
            summary.append(
                f"{item['label']}: {item['status']}\n"
                f"{item['detail']}\n"
            )

        summary.extend(
            [
                f"Official checklist: {SOURCE_URL}",
                "",
                "Independent prototype. User-reported information only.",
                "Not document verification, eligibility confirmation, "
                "or a guarantee of approval.",
            ]
        )

        st.download_button(
            "Download checklist",
            data="\n".join(summary),
            file_name="sevaready-checklist.txt",
            mime="text/plain",
        )

st.divider()
st.caption(
    "Version 0.1: guided checklist only. "
    "AI explanations and additional languages are not implemented yet."
)