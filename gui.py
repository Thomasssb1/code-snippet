from io import StringIO
import streamlit as st
from main import main
from numpy import array


def getLineLength(file, *args) -> int:
    if file is None:
        return None
    string_io = StringIO(file.getvalue().decode("utf-8"))
    if "range" in args:
        return (1, len(string_io.read().splitlines()))
    else:
        return len(string_io.read().splitlines())


class status:
    def __init__(self, container):
        self.container = container
        self.text = "Waiting for the file to be uploaded..."
        self.state = "error"

    def set_text(self, text):
        self.container.update(label=text)

    def set_state(self, state):
        self.container.update(state=state)


st.title("Code Snippet")
st.caption(
    "Generate an organised screenshot of your code as well as being able to customise the output to match your theme."
)

st.markdown("\n\n")
file = st.file_uploader(
    "Upload a file",
    help="The file to be used to generate the snippet.",
)

with st.expander("Options", expanded=True):
    language = st.selectbox(
        "language", options=["python", "java", "ruby", "dart", "other"]
    )
    show_line_count = st.checkbox(
        "show line numbers",
        value=False,
        help="Show line numbers on the left side of the snippet.",
    )
    show_comments = st.checkbox(
        "remove comments",
        value=True,
        help="Remove all comments from the snippet generated.",
    )
    between_lines = st.slider(
        "between lines",
        value=getLineLength(file, "range"),
        min_value=1,
        max_value=getLineLength(file),
        disabled=file is None,
    )
    if st.checkbox("show advanced options"):
        with st.container(border=True):
            padding = st.number_input("padding", value=15, min_value=0, max_value=100)
            transparent_background = st.checkbox("transparent background")
            if st.checkbox("customise syntax highlighting"):
                st.json()
    else:
        padding = 15
        transparent_background = False

status_container = st.status("Waiting for the file to be uploaded...", state="error")
state = status(status_container)

if st.button("Generate", type="primary", disabled=file is None):
    image = main(
        file=file,
        state=state,
        language=language,
        show_line_count=show_line_count,
        show_comments=show_comments,
        between_lines=between_lines,
        padding=padding,
        transparent_background=transparent_background,
    )
    st.image(array(image), use_column_width=True)
    btn = st.download_button(
        label="Download",
        data=image.tobytes(),
        file_name="snippet.png",
        mime="image/png",
        use_container_width=True,
    )
