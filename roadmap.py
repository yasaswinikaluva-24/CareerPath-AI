import ai_chat
import config
import prompts
import json
import streamlit as st
import database

def generate_custom_roadmap(career_name, already_have, need_to_learn, duration_days=30):
    """
    Queries OpenRouter to generate a 30, 60, or 90 day roadmap in JSON format.
    """
    client = ai_chat.get_ai_client()
    weeks = duration_days // 7
    if weeks < 1:
        weeks = 4
    
    user_prompt = prompts.ROADMAP_PROMPT.format(
        duration_days=duration_days,
        weeks=weeks,
        career_name=career_name,
        already_have=", ".join(already_have) if already_have else "None",
        need_to_learn=", ".join(need_to_learn) if need_to_learn else "None"
    )
    
    response = client.chat.completions.create(
        model=config.MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a professional technical curriculum designer. Return strictly raw JSON text adhering to the requested schema."},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3
    )
    content = response.choices[0].message.content.strip()
    
    # Clean the string in case markdown tags are returned
    parsed = parse_roadmap_data(content)
    if parsed:
        return json.dumps(parsed, indent=2)
    
    # Fallback generator if JSON parsing fails
    fallback_data = {
        "weeks": [
            {
                "week_number": w,
                "focus_area": f"Fundamentals & Core Skills for {career_name} - Part {w}",
                "tasks": [
                    {"id": f"w{w}_t1", "title": f"Study required foundational tools and concepts for {career_name}", "type": "study"},
                    {"id": f"w{w}_t2", "title": f"Complete hands-on exercises focusing on key operations", "type": "practice"},
                    {"id": f"w{w}_t3", "title": f"Complete weekly milestone assignment and assessment", "type": "assignment"},
                    {"id": f"w{w}_t4", "title": f"Build and test weekly mini-project module", "type": "project"}
                ]
            } for w in range(1, weeks + 1)
        ],
        "revision_plan": "Spend the final days reviewing core tools, checking assignments, and deploying projects.",
        "capstone_project": {
            "title": f"End-to-End {career_name} Portfolio Application",
            "description": f"Build, test, and package a production-ready application demonstrating your core mastery of the role.",
            "tech_stack": need_to_learn[:3] if need_to_learn else ["Python", "Docker"]
        }
    }
    return json.dumps(fallback_data, indent=2)

def parse_roadmap_data(roadmap_content):
    """
    Safely parses JSON roadmap content from string or dict.
    Extracts valid JSON even if surrounded by markdown codeblocks or extra text.
    """
    if isinstance(roadmap_content, dict):
        return roadmap_content
    if not isinstance(roadmap_content, str):
        return None
        
    content = roadmap_content.strip()
    
    # Remove markdown code blocks if present
    if content.startswith("```json"):
        content = content[7:]
    elif content.startswith("```"):
        content = content[3:]
    if content.endswith("```"):
        content = content[:-3]
    content = content.strip()
    
    try:
        data = json.loads(content)
        if isinstance(data, dict) and "weeks" in data:
            return data
    except Exception:
        pass
        
    # Attempt to locate the outermost JSON brackets
    start = content.find("{")
    end = content.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            data = json.loads(content[start:end+1])
            if isinstance(data, dict) and "weeks" in data:
                return data
        except Exception:
            pass
            
    return None

def format_roadmap_for_text(roadmap_data_or_str):
    """
    Formats the roadmap into clean, structured plain text suitable for PDF reports.
    """
    data = parse_roadmap_data(roadmap_data_or_str)
    if not data or "weeks" not in data:
        return str(roadmap_data_or_str)
    
    lines = []
    for w in data.get("weeks", []):
        w_num = w.get("week_number", "?")
        focus = w.get("focus_area", "")
        lines.append(f"WEEK {w_num}: {focus.upper()}")
        for t in w.get("tasks", []):
            t_type = t.get("type", "task").capitalize()
            t_title = t.get("title", "")
            lines.append(f"  [{t_type}] {t_title}")
        lines.append("")
        
    if "capstone_project" in data:
        cp = data["capstone_project"]
        lines.append(f"CAPSTONE PROJECT: {cp.get('title', 'Final Project')}")
        lines.append(f"  Description: {cp.get('description', '')}")
        if "tech_stack" in cp:
            stack = cp.get("tech_stack")
            stack_str = ", ".join(stack) if isinstance(stack, list) else str(stack)
            lines.append(f"  Tech Stack: {stack_str}")
        lines.append("")
        
    if "revision_plan" in data:
        lines.append("REVISION PLAN:")
        lines.append(f"  {data.get('revision_plan')}")
        
    return "\n".join(lines)

def format_roadmap_as_markdown(data, career_name=""):
    """
    Generates a full Markdown string of the roadmap for export.
    """
    if not data or "weeks" not in data:
        return str(data)
    
    md = [f"# 📚 Learning Roadmap: {career_name}\n"]
    for w in data.get("weeks", []):
        w_num = w.get("week_number", "?")
        focus = w.get("focus_area", "")
        md.append(f"## Week {w_num}: {focus}")
        for t in w.get("tasks", []):
            t_type = t.get("type", "task").capitalize()
            t_title = t.get("title", "")
            icon = "📖" if t_type == "Study" else "💻" if t_type == "Practice" else "📝" if t_type == "Assignment" else "🚀"
            md.append(f"- {icon} **[{t_type}]** {t_title}")
        md.append("")
        
    if "capstone_project" in data:
        cp = data["capstone_project"]
        md.append(f"## 🏆 Capstone Project: {cp.get('title', '')}")
        md.append(f"{cp.get('description', '')}\n")
        if "tech_stack" in cp:
            stack = cp.get("tech_stack")
            stack_str = ", ".join(stack) if isinstance(stack, list) else str(stack)
            md.append(f"**Tech Stack:** `{stack_str}`\n")
            
    if "revision_plan" in data:
        md.append("## 🔄 Revision & Final Sprint")
        md.append(f"{data.get('revision_plan')}\n")
        
    return "\n".join(md)

def render_roadmap_ui(roadmap_content, username, career_name):
    """
    Renders an interactive, glassmorphic Streamlit curriculum UI with progress tracking.
    """
    data = parse_roadmap_data(roadmap_content)
    
    if not data or "weeks" not in data:
        # Fallback to plain markdown if data couldn't be parsed into structured format
        st.markdown(roadmap_content)
        return

    weeks = data.get("weeks", [])
    total_weeks = len(weeks)
    
    # Retrieve current progress from SQLite database
    completed_task_ids = set(database.get_roadmap_progress(username, career_name) or [])
    
    # Calculate overall task stats
    all_tasks = []
    for w_idx, w in enumerate(weeks):
        for t_idx, t in enumerate(w.get("tasks", [])):
            t_id = t.get("id") or f"w{w.get('week_number', w_idx+1)}_t{t_idx+1}"
            all_tasks.append(t_id)
            
    total_tasks = len(all_tasks)
    completed_count = len(completed_task_ids.intersection(set(all_tasks)))
    progress_ratio = completed_count / total_tasks if total_tasks > 0 else 0.0
    progress_pct = int(progress_ratio * 100)

    # Progress and Stats Header
    st.markdown(f"""
    <div class='glass-card' style='margin-top: 14px; margin-bottom: 22px;'>
        <div style='display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;'>
            <div>
                <span style='font-size: 0.85rem; color: #A78BFA; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px;'>Curriculum Track</span>
                <h2 style='margin: 4px 0 0 0; color: #F8FAFC; font-weight: 800; font-size: 1.6rem;'>{career_name}</h2>
                <div style='color: #94A3B8; font-size: 0.9rem; margin-top: 4px;'>
                    📅 {total_weeks} Weeks &bull; {total_tasks} Actionable Milestones
                </div>
            </div>
            <div style='text-align: right;'>
                <span style='font-size: 0.85rem; color: #34D399; font-weight: 700; text-transform: uppercase;'>Completion Rate</span>
                <div style='font-size: 2rem; font-weight: 800; color: #34D399; line-height: 1.1;'>{progress_pct}%</div>
                <div style='font-size: 0.82rem; color: #CBD5E1;'>{completed_count} of {total_tasks} tasks done</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Streamlit progress bar
    st.progress(progress_ratio)
    
    if progress_pct == 100:
        st.balloons()
        st.success("🎉 Incredible achievement! You have completed all milestones for this roadmap!")
    
    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    
    # Task Type Legend & Filter
    st.markdown("""
    <div style='display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 16px; font-size: 0.82rem;'>
        <span style='background: rgba(139, 92, 246, 0.15); color: #C4B5FD; padding: 4px 10px; border-radius: 12px; border: 1px solid rgba(139, 92, 246, 0.3);'>📖 Study / Theory</span>
        <span style='background: rgba(16, 185, 129, 0.15); color: #6EE7B7; padding: 4px 10px; border-radius: 12px; border: 1px solid rgba(16, 185, 129, 0.3);'>💻 Hands-on Practice</span>
        <span style='background: rgba(245, 158, 11, 0.15); color: #FCD34D; padding: 4px 10px; border-radius: 12px; border: 1px solid rgba(245, 158, 11, 0.3);'>📝 Weekly Assignment</span>
        <span style='background: rgba(236, 72, 153, 0.15); color: #F472B6; padding: 4px 10px; border-radius: 12px; border: 1px solid rgba(236, 72, 153, 0.3);'>🚀 Mini-Project</span>
    </div>
    """, unsafe_allow_html=True)

    # Weekly Curriculum Cards
    for w_idx, week in enumerate(weeks):
        w_num = week.get("week_number", w_idx + 1)
        focus = week.get("focus_area", f"Week {w_num} Focus Area")
        tasks = week.get("tasks", [])
        
        # Calculate week completion
        week_task_ids = [t.get("id") or f"w{w_num}_t{t_i+1}" for t_i, t in enumerate(tasks)]
        week_done = len([t_id for t_id in week_task_ids if t_id in completed_task_ids])
        week_total = len(week_task_ids)
        
        if week_total > 0 and week_done == week_total:
            status_badge = "✅ COMPLETED"
            badge_color = "#34D399"
        elif week_done > 0:
            status_badge = f"⚡ IN PROGRESS ({week_done}/{week_total})"
            badge_color = "#A78BFA"
        else:
            status_badge = "⏳ UPCOMING"
            badge_color = "#94A3B8"
            
        expander_title = f"🗓️ Week {w_num}: {focus}  —  [{status_badge}]"
        
        # Default expand if in progress or next up
        is_first_incomplete = (week_done < week_total) and (w_idx == 0 or any(t not in completed_task_ids for t in all_tasks[:w_idx*4]))
        
        with st.expander(expander_title, expanded=(w_idx == 0 or is_first_incomplete)):
            st.markdown(f"""
            <div style='background: rgba(255, 255, 255, 0.02); border-left: 3px solid {badge_color}; padding: 8px 14px; margin-bottom: 14px; border-radius: 0 8px 8px 0;'>
                <span style='color: #CBD5E1; font-size: 0.9rem; font-weight: 500;'>🎯 <b>Focus Objective:</b> {focus}</span>
            </div>
            """, unsafe_allow_html=True)
            
            for t_idx, task in enumerate(tasks):
                task_id = task.get("id") or f"w{w_num}_t{t_idx+1}"
                task_title = task.get("title", "")
                task_type = task.get("type", "study").lower()
                
                # Assign badge info based on type
                if "study" in task_type:
                    type_label = "📖 Study"
                elif "practice" in task_type:
                    type_label = "💻 Practice"
                elif "assignment" in task_type:
                    type_label = "📝 Assignment"
                elif "project" in task_type:
                    type_label = "🚀 Project"
                else:
                    type_label = "📌 Task"
                
                is_task_done = task_id in completed_task_ids
                
                # Render checkbox
                checked = st.checkbox(
                    f"**[{type_label}]** {task_title}",
                    value=is_task_done,
                    key=f"chk_{career_name}_{task_id}"
                )
                
                # Check for state change
                if checked != is_task_done:
                    if checked:
                        completed_task_ids.add(task_id)
                    else:
                        completed_task_ids.discard(task_id)
                    database.update_roadmap_progress(username, career_name, list(completed_task_ids))
                    st.rerun()

    # Capstone Project Section
    if "capstone_project" in data:
        cp = data["capstone_project"]
        cp_title = cp.get("title", "Portfolio Capstone Project")
        cp_desc = cp.get("description", "A production-grade capstone project integrating all learned skills.")
        cp_stack = cp.get("tech_stack", [])
        
        stack_badges_html = ""
        if isinstance(cp_stack, list):
            for tech in cp_stack:
                stack_badges_html += f"<span class='badge-need'>{tech}</span>"
        elif isinstance(cp_stack, str):
            stack_badges_html = f"<span class='badge-need'>{cp_stack}</span>"
            
        st.markdown(f"""
        <div class='glass-card' style='border: 1px solid rgba(139, 92, 246, 0.35); margin-top: 24px;'>
            <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 10px;'>
                <span style='font-size: 1.5rem;'>🏆</span>
                <h3 style='margin: 0; color: #F8FAFC;'>Capstone Project: {cp_title}</h3>
            </div>
            <p style='color: #CBD5E1; font-size: 0.95rem; line-height: 1.6;'>{cp_desc}</p>
            <div style='margin-top: 12px;'>
                <span style='font-size: 0.85rem; color: #A78BFA; font-weight: 600;'>🛠️ Recommended Tech Stack: </span>
                <div style='margin-top: 6px;'>{stack_badges_html}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    # Revision Plan Section
    if "revision_plan" in data:
        rev_plan = data.get("revision_plan")
        st.markdown(f"""
        <div class='glass-card' style='border: 1px solid rgba(16, 185, 129, 0.3); margin-top: 16px;'>
            <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 10px;'>
                <span style='font-size: 1.5rem;'>🔄</span>
                <h3 style='margin: 0; color: #F8FAFC;'>Consolidation & Revision Sprint</h3>
            </div>
            <p style='color: #CBD5E1; font-size: 0.95rem; line-height: 1.6;'>{rev_plan}</p>
        </div>
        """, unsafe_allow_html=True)
        
    # Export Options
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    exp_c1, exp_c2 = st.columns(2)
    with exp_c1:
        md_content = format_roadmap_as_markdown(data, career_name)
        st.download_button(
            label="📥 Download Curriculum (Markdown)",
            data=md_content,
            file_name=f"{career_name.replace(' ', '_')}_roadmap.md",
            mime="text/markdown",
            use_container_width=True
        )
    with exp_c2:
        json_content = json.dumps(data, indent=2)
        st.download_button(
            label="📦 Export Curriculum (JSON)",
            data=json_content,
            file_name=f"{career_name.replace(' ', '_')}_roadmap.json",
            mime="application/json",
            use_container_width=True
        )
