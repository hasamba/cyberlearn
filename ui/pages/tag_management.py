"""
Tag Management Page
Manage lesson tags, create custom tags, and view tag statistics.
"""

import streamlit as st
import uuid
from datetime import datetime
from models.tag import Tag, TagCreate, TagUpdate
from utils.database import Database


def render_tag_management(db: Database):
    """Render tag management interface"""

    st.title("Tag Management")
    st.markdown("Organize lessons with colored tags for easy filtering and discovery")

    # Create tabs
    tab1, tab2, tab3 = st.tabs(["View Tags", "Create Tag", "Tag Statistics"])

    # TAB 1: View and manage existing tags
    with tab1:
        st.subheader("All Tags")

        tags = db.get_all_tags()

        if not tags:
            st.info("No tags found. Create your first tag in the 'Create Tag' tab.")
        else:
            # Sort tags: system tags first, then custom tags
            sorted_tags = sorted(tags, key=lambda t: (not t.is_system, t.name))

            # Display tags in a nice grid
            cols = st.columns(3)

            for idx, tag in enumerate(sorted_tags):
                with cols[idx % 3]:
                    # Check if editing this tag
                    is_editing = st.session_state.get(f'editing_tag') == tag.tag_id

                    if is_editing:
                        # Edit form
                        with st.form(f"edit_form_{tag.tag_id}"):
                            st.markdown(f"**Edit Tag: {tag.icon} {tag.name}**")
                            new_name = st.text_input("Name", value=tag.name)
                            new_color = st.color_picker("Color", value=tag.color)
                            new_icon = st.text_input("Icon (emoji)", value=tag.icon or "")
                            new_desc = st.text_area("Description", value=tag.description or "")

                            col1, col2 = st.columns(2)
                            with col1:
                                if st.form_submit_button("Save", use_container_width=True):
                                    update = TagUpdate(
                                        name=new_name if new_name != tag.name else None,
                                        color=new_color if new_color != tag.color else None,
                                        icon=new_icon if new_icon != tag.icon else None,
                                        description=new_desc if new_desc != tag.description else None
                                    )

                                    if db.update_tag(tag.tag_id, update):
                                        st.success("Tag updated!")
                                        del st.session_state[f'editing_tag']
                                        st.rerun()
                                    else:
                                        st.error("Failed to update tag")

                            with col2:
                                if st.form_submit_button("Cancel", use_container_width=True):
                                    del st.session_state[f'editing_tag']
                                    st.rerun()
                    else:
                        # Tag card
                        st.markdown(f"""
                        <div style="
                            border: 2px solid {tag.color};
                            border-radius: 10px;
                            padding: 15px;
                            margin-bottom: 10px;
                            background-color: {tag.color}15;
                        ">
                            <h3 style="color: {tag.color}; margin: 0;">
                                {tag.icon} {tag.name}
                            </h3>
                            <p style="margin: 5px 0; font-size: 0.9em;">{tag.description or 'No description'}</p>
                            <p style="margin: 5px 0; font-size: 0.8em; color: #666;">
                                {'🔒 System Tag' if tag.is_system else '✏️ Custom Tag'}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)

                        # Functional buttons for custom tags
                        if not tag.is_system:
                            col_a, col_b = st.columns(2)
                            with col_a:
                                if st.button(f"✏️ Edit", key=f"edit_{tag.tag_id}", use_container_width=True):
                                    st.session_state[f'editing_tag'] = tag.tag_id
                                    st.rerun()

                            with col_b:
                                if st.button(f"🗑️ Delete", key=f"del_{tag.tag_id}", use_container_width=True, type="secondary"):
                                    if st.session_state.get(f'confirm_delete_{tag.tag_id}'):
                                        try:
                                            db.delete_tag(tag.tag_id)
                                            st.success(f"Deleted tag: {tag.name}")
                                            st.rerun()
                                        except ValueError as e:
                                            st.error(str(e))
                                    else:
                                        st.session_state[f'confirm_delete_{tag.tag_id}'] = True
                                        st.warning("Click again to confirm deletion")
                                        st.rerun()

    # TAB 2: Create new tag
    with tab2:
        st.subheader("Create New Tag")

        with st.form("create_tag_form"):
            name = st.text_input("Tag Name*", placeholder="e.g., My Course, HTB Challenges")
            color = st.color_picker("Color*", value="#3B82F6")
            icon = st.text_input("Icon (emoji)", placeholder="e.g., 🎯, 🔥, ⚡", value="🏷️")
            description = st.text_area("Description", placeholder="What does this tag represent?")

            submitted = st.form_submit_button("Create Tag", type="primary")

            if submitted:
                if not name:
                    st.error("Tag name is required")
                else:
                    # Create tag
                    new_tag = Tag(
                        tag_id=str(uuid.uuid4()),
                        name=name,
                        color=color.upper(),
                        icon=icon or None,
                        description=description or None,
                        created_at=datetime.utcnow(),
                        is_system=False
                    )

                    if db.create_tag(new_tag):
                        st.success(f"Created tag: {icon} {name}")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("Failed to create tag (name might already exist)")

        st.markdown("---")
        st.markdown("### Tag Best Practices")
        st.markdown("""
        - **Use clear names**: "PWK Course" instead of just "PWK"
        - **Choose distinct colors**: Make tags easily distinguishable
        - **Add descriptions**: Help others understand the tag's purpose
        - **Use emojis wisely**: They make tags more visual but don't overdo it
        - **Tag consistently**: Apply tags to related lessons systematically
        """)

    # TAB 3: Statistics
    with tab3:
        st.subheader("Tag Usage Statistics")

        stats = db.get_tag_stats()

        if not stats:
            st.info("No tag statistics available yet. Create tags and apply them to lessons.")
        else:
            # Display as bar chart
            import pandas as pd

            df = pd.DataFrame({
                'Tag': list(stats.keys()),
                'Lesson Count': list(stats.values())
            })

            st.bar_chart(df.set_index('Tag'))

            # Detailed table
            st.markdown("### Detailed Breakdown")

            for tag_name, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
                tag = db.get_tag_by_name(tag_name)
                if tag:
                    st.markdown(f"""
                    <div style="
                        border-left: 4px solid {tag.color};
                        padding: 10px;
                        margin: 10px 0;
                        background-color: {tag.color}10;
                    ">
                        <strong>{tag.icon} {tag.name}</strong>: {count} lesson{'s' if count != 1 else ''}
                    </div>
                    """, unsafe_allow_html=True)


def main():
    """Standalone page entry point"""
    db = Database()
    render_tag_management(db)
    db.close()


if __name__ == "__main__":
    main()
