import logging
import time

import streamlit as st
from streamlit import session_state as ss
from streamlit_pdf_viewer import pdf_viewer

from src import generate_highlighted_pdf

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Main function to run the PDF Highlighter tool."""
    st.set_page_config(page_title="Smart PDF Highlighter", page_icon="./photos/icon.png")
    st.title("Smart PDF Highlighter")
    show_description()

    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    if uploaded_file is not None:
        st.write("PDF file successfully uploaded.")
        process_pdf(uploaded_file)


def show_description():
    """Display description of functionality and maximum limits."""
    st.write("""Welcome to Smart PDF Highlighter! This tool automatically identifies
        and highlights important content within your PDF files. It utilizes many
        AI techniques such as deep learning and other advanced algorithms to 
        analyze the text and intelligently select key sentences for highlighting.""")
    st.write("Maximum Limits: 40 pages, 2000 sentences.")


def process_pdf(uploaded_file):
    """Process the uploaded PDF file and generate highlighted PDF."""
    st.write("Generating highlighted PDF...")
    start_time = time.time()

    with st.spinner("Processing..."):
        # Call the PDF processing function
        result = generate_highlighted_pdf(uploaded_file)

        # Check for errors returned by the `generate_highlighted_pdf` function
        if isinstance(result, str):  # Error message returned as a string
            st.error(result)
            logger.error("Error generating highlighted PDF: %s", result)
            return
        else:
            file = result  # The processed PDF content

    end_time = time.time()
    execution_time = end_time - start_time
    st.success(
        f"Highlighted PDF generated successfully in {execution_time:.2f} seconds."
    )

    # Save the processed PDF to a temporary location for viewing
    with open("highlighted_output.pdf", "wb") as f:
        f.write(file)

    # Display the highlighted PDF
    st.write("**Preview Highlighted PDF:**")
    pdf_viewer("highlighted_output.pdf")

    # Download button for the processed PDF
    st.write("Download highlighted PDF:")
    st.download_button(
        label="Download",
        data=file,
        file_name="highlighted_" + uploaded_file.name,
        mime="application/pdf",
    )


if __name__ == "__main__":
    main()