import streamlit as st

def render_editor_content(blocks):
    """
    Render Editor.js blocks into Streamlit UI.
    `blocks` should be the list from Editor.js: note['text']['blocks']
    """
    if not blocks:
        st.info("This note is empty.")
        return

    for block in blocks:
        btype = block.get("type")
        data = block.get("data", {})

        if btype == "header":
            level = data.get("level", 3)
            text = data.get("text", "")
            if level == 1: st.title(text)
            elif level == 2: st.header(text)
            else: st.subheader(text)

        elif btype == "paragraph":
            st.write(data.get("text", ""))

        elif btype == "list":
            items = data.get("items", [])
            if data.get("style") == "unordered":
                for item in items:
                    st.markdown(f"- {item['content']}")
            else:
                for i, item in enumerate(items):
                    st.markdown(f"{i+1}. {item['content']}")

        else:
            st.write(f"🔧 Unsupported block type: `{btype}`")
