"""
Global Lesson Search Page

Search across all lessons by:
- Title
- Learning objectives
- Concepts
- Content blocks

Filter by:
- Domain
- Difficulty
- Tags
- Completion status
"""

import streamlit as st
from typing import List, Optional
from models.lesson import Lesson
from models.user import UserProfile

def render_search_page():
    """Render the global lesson search page"""

    st.title("🔍 Search Lessons")

    # Get database and user from session
    db = st.session_state.db
    user: Optional[UserProfile] = st.session_state.get('current_user')

    # Check if there's a popular search term selected
    if 'popular_search_term' in st.session_state:
        # Set the search input widget state directly
        st.session_state.search_input = st.session_state.popular_search_term
        del st.session_state.popular_search_term

    # Search input
    search_query = st.text_input(
        "Search for lessons",
        placeholder="Enter keywords (e.g., 'Kerberos', 'memory forensics', 'docker')...",
        key="search_input"
    )

    # Filters in columns
    col1, col2, col3 = st.columns(3)

    with col1:
        # Domain filter
        all_domains = [
            "All Domains",
            "fundamentals", "osint", "dfir", "malware",
            "active_directory", "system", "linux", "cloud",
            "pentest", "red_team", "blue_team", "threat_hunting",
            "ai_security", "iot_security", "web3_security"
        ]
        selected_domain = st.selectbox("Domain", all_domains, key="search_domain")

    with col2:
        # Difficulty filter
        difficulty_options = ["All Difficulties", "Beginner (1)", "Intermediate (2)", "Advanced (3)"]
        selected_difficulty = st.selectbox("Difficulty", difficulty_options, key="search_difficulty")

    with col3:
        # Completion status filter (if user logged in)
        if user:
            completion_options = ["All Lessons", "Not Started", "In Progress", "Completed"]
            selected_completion = st.selectbox("Status", completion_options, key="search_completion")
        else:
            selected_completion = "All Lessons"

    # Tag filter
    available_tags = db.get_filterable_tags(str(user.user_id)) if user else []
    tag_names = ["All Tags"] + [tag.name for tag in available_tags]
    selected_tag = st.selectbox("Filter by Tag", tag_names, key="search_tag")

    # Sort options
    sort_options = ["Relevance", "Title (A-Z)", "Difficulty", "Domain"]
    selected_sort = st.selectbox("Sort by", sort_options, key="search_sort")

    # Include hidden lessons toggle
    include_hidden = st.checkbox("Include hidden lessons", value=False, key="search_include_hidden")

    st.markdown("---")

    # Perform search
    if search_query or selected_domain != "All Domains" or selected_tag != "All Tags":
        # Build search query
        cursor = db.conn.cursor()

        # Base query (note: no concepts column in lessons table)
        query = '''
            SELECT DISTINCT l.lesson_id, l.title, l.domain, l.difficulty,
                   l.order_index, l.learning_objectives
            FROM lessons l
            WHERE 1=1
        '''
        params = []

        # Exclude hidden lessons by default
        if not include_hidden:
            # Check if hidden column exists
            cursor.execute("PRAGMA table_info(lessons)")
            columns = [row[1] for row in cursor.fetchall()]
            if 'hidden' in columns:
                query += ' AND (l.hidden = 0 OR l.hidden IS NULL)'

        # Search term filter
        if search_query:
            query += '''
                AND (
                    l.title LIKE ?
                    OR l.learning_objectives LIKE ?
                )
            '''
            search_param = f"%{search_query}%"
            params.extend([search_param, search_param])

        # Domain filter
        if selected_domain != "All Domains":
            query += ' AND l.domain = ?'
            params.append(selected_domain)

        # Difficulty filter
        if selected_difficulty != "All Difficulties":
            diff_num = int(selected_difficulty.split('(')[1][0])
            query += ' AND l.difficulty = ?'
            params.append(diff_num)

        # Tag filter
        if selected_tag != "All Tags":
            query += '''
                AND EXISTS (
                    SELECT 1 FROM lesson_tags lt
                    JOIN tags t ON lt.tag_id = t.tag_id
                    WHERE lt.lesson_id = l.lesson_id
                    AND t.name = ?
                )
            '''
            params.append(selected_tag)

        # Sorting
        if selected_sort == "Relevance":
            # Prioritize title matches
            query += '''
                ORDER BY
                    CASE WHEN l.title LIKE ? THEN 1 ELSE 2 END,
                    l.order_index
            '''
            params.append(f"%{search_query}%") if search_query else params.append("%")
        elif selected_sort == "Title (A-Z)":
            query += ' ORDER BY l.title'
        elif selected_sort == "Difficulty":
            query += ' ORDER BY l.difficulty, l.order_index'
        elif selected_sort == "Domain":
            query += ' ORDER BY l.domain, l.order_index'

        # Execute search
        cursor.execute(query, params)
        results = cursor.fetchall()

        # Display results
        if results:
            st.success(f"Found {len(results)} lesson(s)")

            for row in results:
                lesson_id, title, domain, difficulty, order_index, learning_objectives = row

                # Create lesson card
                with st.container():
                    col_left, col_right = st.columns([4, 1])

                    with col_left:
                        # Highlight search term in title
                        display_title = title
                        if search_query and search_query.lower() in title.lower():
                            # Simple highlight (could be enhanced)
                            display_title = f"**{title}**"

                        st.markdown(f"### {display_title}")

                        # Domain and difficulty badges
                        domain_emoji = {
                            "fundamentals": "🔐", "osint": "🔎", "dfir": "🔍",
                            "malware": "🦠", "active_directory": "🗂️", "system": "💻",
                            "linux": "🐧", "cloud": "☁️", "pentest": "🎯",
                            "red_team": "🔴", "blue_team": "🛡️", "threat_hunting": "🎯",
                            "ai_security": "🤖", "iot_security": "🔌", "web3_security": "🔗"
                        }

                        difficulty_names = {1: "Beginner", 2: "Intermediate", 3: "Advanced"}
                        difficulty_colors = {1: "🟢", 2: "🟡", 3: "🔴"}

                        st.caption(
                            f"{domain_emoji.get(domain, '📚')} {domain.replace('_', ' ').title()} • "
                            f"{difficulty_colors[difficulty]} {difficulty_names[difficulty]}"
                        )

                        # Show snippet of learning objectives
                        if learning_objectives:
                            import json
                            try:
                                objectives_list = json.loads(learning_objectives) if isinstance(learning_objectives, str) else learning_objectives
                                if objectives_list:
                                    st.caption(f"**Learning Objectives**: {', '.join(objectives_list[:3])}" + ("..." if len(objectives_list) > 3 else ""))
                            except:
                                pass

                        # Get and display tags
                        lesson_tags = db.get_lesson_tags(lesson_id)
                        if lesson_tags:
                            tag_pills = " ".join([f"{tag.icon}" for tag in lesson_tags[:5]])
                            st.caption(f"**Tags**: {tag_pills}")

                    with col_right:
                        # View lesson button
                        if st.button("View Lesson", key=f"view_{lesson_id}"):
                            # Load full lesson
                            lesson = db.get_lesson(lesson_id)
                            if lesson:
                                st.session_state.current_lesson = lesson
                                st.session_state.current_page = "lesson"
                                # Initialize lesson state
                                if 'current_block_index' not in st.session_state:
                                    st.session_state.current_block_index = 0
                                st.rerun()

                    st.markdown("---")

        else:
            st.info("No lessons found matching your search criteria.")
            st.markdown("**Suggestions:**")
            st.markdown("- Try different keywords")
            st.markdown("- Broaden your filters")
            st.markdown("- Check spelling")

    else:
        # No search yet - show placeholder
        st.info("👆 Enter a search term or select filters to find lessons")

        st.markdown("### Popular Searches")
        col1, col2, col3 = st.columns(3)

        popular_searches = [
            ("Kerberos", "Active Directory authentication attacks"),
            ("Memory Forensics", "Volatility and memory analysis"),
            ("Docker", "Container security and Kubernetes"),
            ("Mimikatz", "Credential extraction tools"),
            ("Splunk", "SIEM and log analysis"),
            ("Volatility", "Memory forensics framework"),
            ("YARA", "Malware detection rules"),
            ("Wireshark", "Network traffic analysis"),
            ("Nmap", "Network scanning and enumeration")
        ]

        for i, (term, desc) in enumerate(popular_searches):
            col = [col1, col2, col3][i % 3]
            with col:
                if st.button(f"🔍 {term}", key=f"popular_{i}"):
                    # Store the search term separately to avoid widget state conflict
                    st.session_state.popular_search_term = term
                    st.rerun()
                st.caption(desc)
