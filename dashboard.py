import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

def generate_plotly_radar(user_traits, career_traits, career_name):
    """
    Generates an interactive Plotly Radar Chart comparing user traits vs career targets.
    Styled with the dark glassmorphism theme (Emerald & Purple).
    """
    categories = ['Logic', 'Creativity', 'Communication']
    
    user_vals = [
        user_traits.get('logic', 5),
        user_traits.get('creativity', 5),
        user_traits.get('communication', 5)
    ]
    
    career_vals = [
        career_traits.get('logic', 5),
        career_traits.get('creativity', 5),
        career_traits.get('communication', 5)
    ]
    
    fig = go.Figure()
    
    # Career Target Profile
    fig.add_trace(go.Scatterpolar(
        r=career_vals + [career_vals[0]],
        theta=categories + [categories[0]],
        fill='toself',
        fillcolor='rgba(139, 92, 246, 0.20)',
        line=dict(color='#A78BFA', width=2.5, dash='dash'),
        name=f"Target: {career_name}",
        hoverinfo='theta+r+name'
    ))
    
    # User Profile
    fig.add_trace(go.Scatterpolar(
        r=user_vals + [user_vals[0]],
        theta=categories + [categories[0]],
        fill='toself',
        fillcolor='rgba(16, 185, 129, 0.35)',
        line=dict(color='#10B981', width=3),
        name="Your Profile",
        hoverinfo='theta+r+name'
    ))
    
    fig.update_layout(
        polar=dict(
            bgcolor='rgba(8, 11, 18, 0.8)',
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                tickfont=dict(color='#64748B', size=9),
                gridcolor='rgba(255, 255, 255, 0.08)',
                linecolor='rgba(255, 255, 255, 0.08)'
            ),
            angularaxis=dict(
                tickfont=dict(color='#F8FAFC', size=11, family='Outfit, sans-serif'),
                gridcolor='rgba(255, 255, 255, 0.08)',
                linecolor='rgba(255, 255, 255, 0.08)'
            )
        ),
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=40, r=40, t=30, b=30),
        height=320,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.22,
            xanchor='center',
            x=0.5,
            font=dict(color='#CBD5E1', size=10)
        )
    )
    return fig

def generate_comparison_radar(role_a_name, role_a_traits, role_b_name, role_b_traits, user_traits=None):
    """
    Generates an interactive 3-way Plotly Radar Chart comparing Role A vs Role B vs User.
    """
    categories = ['Logic', 'Creativity', 'Communication']
    
    vals_a = [role_a_traits.get('logic', 5), role_a_traits.get('creativity', 5), role_a_traits.get('communication', 5)]
    vals_b = [role_b_traits.get('logic', 5), role_b_traits.get('creativity', 5), role_b_traits.get('communication', 5)]
    
    fig = go.Figure()
    
    # Role A
    fig.add_trace(go.Scatterpolar(
        r=vals_a + [vals_a[0]],
        theta=categories + [categories[0]],
        fill='toself',
        fillcolor='rgba(139, 92, 246, 0.22)',
        line=dict(color='#A78BFA', width=2.5),
        name=f"Role A: {role_a_name}",
        hoverinfo='theta+r+name'
    ))
    
    # Role B
    fig.add_trace(go.Scatterpolar(
        r=vals_b + [vals_b[0]],
        theta=categories + [categories[0]],
        fill='toself',
        fillcolor='rgba(59, 130, 246, 0.22)',
        line=dict(color='#60A5FA', width=2.5),
        name=f"Role B: {role_b_name}",
        hoverinfo='theta+r+name'
    ))
    
    # User Profile (if provided)
    if user_traits:
        vals_u = [user_traits.get('logic', 5), user_traits.get('creativity', 5), user_traits.get('communication', 5)]
        fig.add_trace(go.Scatterpolar(
            r=vals_u + [vals_u[0]],
            theta=categories + [categories[0]],
            fill='toself',
            fillcolor='rgba(16, 185, 129, 0.25)',
            line=dict(color='#10B981', width=3, dash='dot'),
            name="Your Traits",
            hoverinfo='theta+r+name'
        ))
        
    fig.update_layout(
        polar=dict(
            bgcolor='rgba(8, 11, 18, 0.8)',
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                tickfont=dict(color='#64748B', size=9),
                gridcolor='rgba(255, 255, 255, 0.08)'
            ),
            angularaxis=dict(
                tickfont=dict(color='#F8FAFC', size=11, family='Outfit, sans-serif'),
                gridcolor='rgba(255, 255, 255, 0.08)'
            )
        ),
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=40, r=40, t=30, b=40),
        height=350,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.25,
            xanchor='center',
            x=0.5,
            font=dict(color='#CBD5E1', size=10)
        )
    )
    return fig

def generate_plotly_bar(top_matches):
    """
    Generates an interactive Plotly Horizontal Bar Chart of top career matches.
    """
    top_5 = top_matches[:5][::-1]
    names = [x['career_name'] for x in top_5]
    pcts = [x['match_percentage'] for x in top_5]
    
    colors = ['#6D28D9', '#7C3AED', '#8B5CF6', '#34D399', '#10B981']
    
    fig = go.Figure(go.Bar(
        x=pcts,
        y=names,
        orientation='h',
        marker=dict(
            color=colors[:len(pcts)],
            line=dict(color='rgba(255, 255, 255, 0.1)', width=1)
        ),
        text=[f"{p}%" for p in pcts],
        textposition='outside',
        textfont=dict(color='#F8FAFC', size=11, family='Outfit, sans-serif'),
        hoverinfo='x+y'
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(8, 11, 18, 0.6)',
        xaxis=dict(
            range=[0, 115],
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.06)',
            tickfont=dict(color='#94A3B8', size=10),
            title=dict(text='Match Percentage (%)', font=dict(color='#94A3B8', size=11))
        ),
        yaxis=dict(
            tickfont=dict(color='#F8FAFC', size=11, family='Outfit, sans-serif')
        ),
        margin=dict(l=20, r=40, t=20, b=20),
        height=280
    )
    return fig

# Matplotlib fallbacks for backwards compatibility
def generate_radar_chart(user_traits, career_traits, career_name):
    """Matplotlib Radar Chart fallback."""
    labels = ['Logic', 'Creativity', 'Communication']
    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]
    
    user_vals = [user_traits.get('logic', 5), user_traits.get('creativity', 5), user_traits.get('communication', 5)]
    user_vals += user_vals[:1]
    career_vals = [career_traits.get('logic', 5), career_traits.get('creativity', 5), career_traits.get('communication', 5)]
    career_vals += career_vals[:1]
    
    fig, ax = plt.subplots(figsize=(3.5, 3.5), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor('#05070D')
    ax.set_facecolor('#080B12')
    plt.xticks(angles[:-1], labels, color='#CBD5E1', size=9)
    ax.set_rlabel_position(0)
    plt.yticks([2, 4, 6, 8, 10], ["2", "4", "6", "8", "10"], color="#64748B", size=7)
    plt.ylim(0, 10)
    
    ax.plot(angles, user_vals, color='#10B981', linewidth=2, linestyle='solid', label='Your Score')
    ax.fill(angles, user_vals, color='#10B981', alpha=0.25)
    ax.plot(angles, career_vals, color='#A78BFA', linewidth=2, linestyle='dashed', label=f'{career_name}')
    ax.fill(angles, career_vals, color='#A78BFA', alpha=0.15)
    ax.spines['polar'].set_color((1, 1, 1, 0.08))
    ax.grid(color=(1, 1, 1, 0.08))
    
    legend = plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2), fontsize=7, ncol=2)
    legend.get_frame().set_facecolor('#080B12')
    legend.get_frame().set_edgecolor((1, 1, 1, 0.08))
    for text in legend.get_texts():
        text.set_color('#F8FAFC')
    plt.title("Trait Comparison", color='#F8FAFC', size=11, weight='bold', pad=15)
    return fig

def generate_horizontal_bar_chart(top_matches):
    """Matplotlib Horizontal Bar Chart fallback."""
    top_5 = top_matches[:5][::-1]
    names = [x['career_name'] for x in top_5]
    pcts = [x['match_percentage'] for x in top_5]
    
    fig, ax = plt.subplots(figsize=(5, 3.2))
    fig.patch.set_facecolor('#05070D')
    ax.set_facecolor('#080B12')
    bars = ax.barh(names, pcts, color='#8B5CF6', height=0.55, edgecolor=(1, 1, 1, 0.08))
    colors = ['#6D28D9', '#7C3AED', '#8B5CF6', '#34D399', '#10B981']
    for i, bar in enumerate(bars):
        bar.set_color(colors[min(i, len(colors)-1)])
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 2, bar.get_y() + bar.get_height()/2, f'{width}%', 
                va='center', ha='left', color='#F8FAFC', fontweight='bold', fontsize=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color((1, 1, 1, 0.08))
    ax.spines['left'].set_color((1, 1, 1, 0.08))
    ax.tick_params(axis='x', colors='#94A3B8', labelsize=8)
    ax.tick_params(axis='y', colors='#F8FAFC', labelsize=9)
    ax.set_title("Top 5 Career Matches", color='#F8FAFC', fontsize=11, fontweight='bold', pad=15)
    ax.set_xlim(0, 110)
    plt.tight_layout()
    return fig
