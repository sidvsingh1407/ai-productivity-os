#!/usr/bin/env python3
"""
AI Productivity Intelligence System - Report Generator
Generates PDF audit reports from scoring results and agent findings.

Usage: python report_generator.py <audit_data.json> <scores.json> <output.pdf>
"""

import json
import sys
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT


# Color scheme (professional, clean)
COLOR_PRIMARY = "#1a1a2e"      # Dark navy
COLOR_SECONDARY = "#16213e"    # Navy
COLOR_ACCENT = "#0f3460"       # Blue
COLOR_HIGHLIGHT = "#e94560"    # Red accent for risks
COLOR_SUCCESS = "#2ecc71"      # Green for positive
COLOR_BG_LIGHT = "#f8f9fa"     # Light gray background


def get_styles():
    """Create paragraph styles for the report."""
    styles = getSampleStyleSheet()

    # Use try/except for custom styles in case they already exist
    try:
        styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=24,
            textColor=colors.HexColor(COLOR_PRIMARY),
            spaceAfter=30,
            alignment=TA_CENTER,
        ))
    except KeyError:
        pass

    try:
        styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=16,
            textColor=colors.HexColor(COLOR_PRIMARY),
            spaceBefore=20,
            spaceAfter=12,
        ))
    except KeyError:
        pass

    try:
        styles.add(ParagraphStyle(
            name='SubHeading',
            parent=styles['Heading3'],
            fontName='Helvetica-Bold',
            fontSize=12,
            textColor=colors.HexColor(COLOR_SECONDARY),
            spaceBefore=12,
            spaceAfter=6,
        ))
    except KeyError:
        pass

    try:
        styles.add(ParagraphStyle(
            name='BodyText',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            textColor=colors.HexColor('#333333'),
            leading=14,
        ))
    except KeyError:
        pass

    try:
        styles.add(ParagraphStyle(
            name='RiskBox',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=10,
            textColor=colors.white,
            backColor=colors.HexColor(COLOR_HIGHLIGHT),
            borderPadding=10,
            spaceBefore=10,
            spaceAfter=10,
        ))
    except KeyError:
        pass

    try:
        styles.add(ParagraphStyle(
            name='ScoreBox',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=18,
            textColor=colors.HexColor(COLOR_PRIMARY),
            alignment=TA_CENTER,
        ))
    except KeyError:
        pass

    return styles


def create_header_table(company_name, audit_date, report_id):
    """Create the report header table."""
    header_data = [
        [Paragraph("AI PRODUCTIVITY INTELLIGENCE", get_styles()['CustomTitle'])],
        [Paragraph("Audit Report", get_styles()['SubHeading'])],
        [Spacer(1, 20)],
        [Paragraph(f"<b>Company:</b> {company_name}", get_styles()['BodyText'])],
        [Paragraph(f"<b>Audit Date:</b> {audit_date}", get_styles()['BodyText'])],
        [Paragraph(f"<b>Report ID:</b> {report_id}", get_styles()['BodyText'])],
    ]

    header_table = Table(header_data, colWidths=[6*inch])
    header_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    return header_table


def create_score_gauge(score, rating):
    """Create a visual score representation."""
    # Determine color based on score
    if score >= 80:
        score_color = COLOR_SUCCESS
    elif score >= 60:
        score_color = "#f39c12"  # Orange
    elif score >= 40:
        score_color = "#e67e22"  # Dark orange
    else:
        score_color = COLOR_HIGHLIGHT

    score_data = [
        [Paragraph(f"AI MATURITY SCORE", get_styles()['SubHeading'])],
        [Spacer(1, 10)],
        [Paragraph(f"<b style='font-size: 36pt; color: {score_color}'>{score}/100</b>", get_styles()['ScoreBox'])],
        [Spacer(1, 10)],
        [Paragraph(f"Rating: <b>{rating}</b>", get_styles()['BodyText'])],
    ]

    score_table = Table(score_data, colWidths=[3*inch])
    score_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor(COLOR_BG_LIGHT)),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor(COLOR_PRIMARY)),
        ('PADDING', (0, 0), (-1, -1), 10),
    ]))

    return score_table


def create_dimension_breakdown(scores):
    """Create dimension score table."""
    dims = scores.get('dimensions', scores)
    dimensions = [
        ("Awareness", dims.get('awareness', 0), 20),
        ("Adoption", dims.get('adoption', 0), 20),
        ("Integration", dims.get('integration', 0), 20),
        ("Governance", dims.get('governance', 0), 20),
        ("ROI", dims.get('roi', 0), 20),
    ]

    data = [
        [
            Paragraph("<b>Dimension</b>", get_styles()['BodyText']),
            Paragraph("<b>Score</b>", get_styles()['BodyText']),
            Paragraph("<b>Rating</b>", get_styles()['BodyText']),
        ]
    ]

    for dim_name, dim_score, max_score in dimensions:
        pct = dim_score / max_score * 100
        if pct >= 75:
            rating = "Strong"
        elif pct >= 50:
            rating = "Moderate"
        else:
            rating = "Needs Work"

        data.append([
            Paragraph(dim_name, get_styles()['BodyText']),
            Paragraph(f"{dim_score}/{max_score}", get_styles()['BodyText']),
            Paragraph(rating, get_styles()['BodyText']),
        ])

    table = Table(data, colWidths=[3*inch, 1.2*inch, 1.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(COLOR_PRIMARY)),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor(COLOR_BG_LIGHT)]),
    ]))

    return table


def create_compliance_alert(compliance_flag, compliance_reasons):
    """Create compliance risk alert box."""
    if not compliance_flag:
        return None

    alert_text = """
    <b>COMPLIANCE RISK DETECTED</b><br/><br/>
    This organization has identified compliance risks related to EU AI Act and/or GDPR requirements.
    The EU AI Act compliance deadline is <b>August 2026</b>. Immediate action is recommended
    to avoid potential penalties and ensure regulatory compliance.<br/><br/>
    <b>Identified Risks:</b> """ + ", ".join(compliance_reasons)

    alert_para = Paragraph(alert_text, get_styles()['RiskBox'])
    return alert_para


def create_recommendations_table(recommendations):
    """Create prioritized recommendations table."""
    data = [
        [
            Paragraph("<b>Priority</b>", get_styles()['BodyText']),
            Paragraph("<b>Recommendation</b>", get_styles()['BodyText']),
            Paragraph("<b>Expected Impact</b>", get_styles()['BodyText']),
            Paragraph("<b>Effort</b>", get_styles()['BodyText']),
        ]
    ]

    for rec in recommendations:
        data.append([
            Paragraph(rec.get('priority', ''), get_styles()['BodyText']),
            Paragraph(rec.get('recommendation', ''), get_styles()['BodyText']),
            Paragraph(rec.get('expected_impact', ''), get_styles()['BodyText']),
            Paragraph(rec.get('implementation_effort', ''), get_styles()['BodyText']),
        ])

    table = Table(data, colWidths=[1*inch, 3*inch, 1.2*inch, 1*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(COLOR_PRIMARY)),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    return table

def create_cost_of_inaction_table(coi_data):
    """Create Cost of Inaction table."""
    # Create a custom style for white text if it doesn't exist
    styles = get_styles()
    if 'BodyTextWhite' not in styles:
        styles.add(ParagraphStyle(
            name='BodyTextWhite',
            parent=styles['BodyText'],
            textColor=colors.white
        ))

    data = [[
        Paragraph("<b>Risk Area</b>", styles['BodyTextWhite']),
        Paragraph("<b>Consequence</b>", styles['BodyTextWhite']),
        Paragraph("<b>Business Impact</b>", styles['BodyTextWhite']),
    ]]

    for item in coi_data:
        risk_area_text = f"<b>{item.get('risk_category', '')}</b><br/><font color='{COLOR_HIGHLIGHT if item.get('risk_level') in ['Critical', 'High'] else COLOR_PRIMARY}'>{item.get('risk_level', '')} Exposure</font>"

        data.append([
            Paragraph(risk_area_text, get_styles()['BodyText']),
            Paragraph(item.get('potential_consequence', ''), get_styles()['BodyText']),
            Paragraph(item.get('business_impact', ''), get_styles()['BodyText']),
        ])

    table = Table(data, colWidths=[1.8*inch, 2.3*inch, 2.4*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(COLOR_PRIMARY)),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    return table

def create_target_state_table(target_state):
    """Create Current vs Target State table."""
    data = [
        [
            Paragraph("<b>Dimension</b>", get_styles()['BodyText']),
            Paragraph("<b>Current Score</b>", get_styles()['BodyText']),
            Paragraph("<b>Target Score</b>", get_styles()['BodyText']),
        ]
    ]

    for ts in target_state:
        data.append([
            Paragraph(ts.get('dimension', ''), get_styles()['BodyText']),
            Paragraph(str(ts.get('current_score', '')), get_styles()['BodyText']),
            Paragraph(str(ts.get('target_score', '')), get_styles()['BodyText']),
        ])

    table = Table(data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(COLOR_PRIMARY)),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    return table


def generate_audit_pdf(audit_data: dict, output_path: str) -> str:
    """Generate the full PDF report based on the consolidated audit data and intelligence payload."""
    scores = audit_data.get('scores', {})
    intelligence = audit_data.get('intelligence', {})

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch,
    )

    story = []
    styles = get_styles()

    # === PAGE 1: Summary ===

    # Header
    company_name = audit_data.get('company_name', 'Unknown')
    audit_date = datetime.now().strftime("%Y-%m-%d")
    report_id = f"AUDIT-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    story.append(create_header_table(company_name, audit_date, report_id))
    story.append(Spacer(1, 20))

    # Assessment Limitations
    story.append(Paragraph("Assessment Limitations", styles['SectionHeading']))
    # Use exact approved wording required by spec
    limitations_text = "This assessment is based on self-reported organizational responses and should be used as a directional decision-support tool rather than a substitute for a full organizational review."
    story.append(Paragraph(limitations_text, styles['Normal']))
    story.append(Spacer(1, 20))

    # Score gauge
    story.append(create_score_gauge(audit_data.get('total_score', 0), audit_data.get('rating', 'N/A')))
    story.append(Spacer(1, 20))

    # Executive Summary (from Intelligence Layer)
    exec_summary = intelligence.get('executive_summary', {})
    if exec_summary:
        story.append(Paragraph("Executive Summary", styles['SectionHeading']))

        story.append(Paragraph("<b>Overall Assessment:</b>", styles['BodyText']))
        story.append(Paragraph(exec_summary.get('overall_assessment', ''), styles['BodyText']))
        story.append(Spacer(1, 10))

        story.append(Paragraph("<b>Critical Risk:</b>", styles['BodyText']))
        story.append(Paragraph(exec_summary.get('critical_risk', ''), styles['BodyText']))
        story.append(Spacer(1, 10))

        story.append(Paragraph("<b>Primary Opportunity:</b>", styles['BodyText']))
        story.append(Paragraph(exec_summary.get('primary_opportunity', ''), styles['BodyText']))
        story.append(Spacer(1, 10))

        story.append(Paragraph("<b>Recommended First Action:</b>", styles['BodyText']))
        story.append(Paragraph(exec_summary.get('recommended_first_action', ''), styles['BodyText']))
        story.append(Spacer(1, 20))

    # Risk Projection
    risk_projection = intelligence.get('risk_projection', {})
    if risk_projection:
        story.append(Paragraph("Risk Projection", styles['SectionHeading']))

        # Risk Severity Card (text format)
        risk_level = risk_projection.get('risk_level', 'Unknown')
        confidence = risk_projection.get('confidence', 0)
        risk_drivers = risk_projection.get('risk_drivers', [])
        top_risk_driver = risk_drivers[0] if risk_drivers else 'Unknown Risk Driver'

        story.append(Paragraph("<b>Current Risk Profile</b>", styles['SubHeading']))
        story.append(Paragraph(f"<b>Overall Risk Level:</b> <font color='{COLOR_HIGHLIGHT if risk_level in ['Critical', 'High'] else COLOR_PRIMARY}'>{risk_level}</font>", styles['BodyText']))
        story.append(Paragraph(f"<b>Confidence Index:</b> {confidence}% (Based on data consistency)", styles['BodyText']))
        story.append(Paragraph(f"<b>Primary Risk Driver:</b> {top_risk_driver}", styles['BodyText']))
        story.append(Spacer(1, 10))

        # Projected Business Impact
        risk_timeline = risk_projection.get('risk_timeline', {})
        coi = intelligence.get('cost_of_inaction', [])
        projected_impact = (
            (risk_timeline.get('near_term') and risk_timeline['near_term'][0]) or
            top_risk_driver or
            (coi and coi[0].get('business_impact')) or
            "Immediate operational friction increases."
        )

        story.append(Paragraph("<b>Projected Business Impact Summary</b>", styles['SubHeading']))
        story.append(Paragraph(projected_impact, styles['BodyText']))
        story.append(Spacer(1, 15))

        # Cost of Inaction Table
        if coi:
            story.append(Paragraph("<b>Cost of Inaction</b>", styles['SubHeading']))
            story.append(create_cost_of_inaction_table(coi))
            story.append(Spacer(1, 15))

        # Risk Timeline
        if risk_timeline:
            story.append(Paragraph("<b>Risk Progression Timeline</b>", styles['SubHeading']))

            # Current State
            story.append(Paragraph("<b>Current State:</b>", styles['BodyText']))
            story.append(Paragraph("• Maturity gaps identified across core operational dimensions.", styles['BodyText']))

            # 30 Days
            story.append(Paragraph("<b>30 Days:</b>", styles['BodyText']))
            for item in risk_timeline.get('near_term', ["Initial operational friction increases."]):
                story.append(Paragraph(f"• {item}", styles['BodyText']))

            # 60 Days
            story.append(Paragraph("<b>60 Days:</b>", styles['BodyText']))
            for item in risk_timeline.get('mid_term', ["Maturity gaps begin affecting execution quality."]):
                story.append(Paragraph(f"• {item}", styles['BodyText']))

            # 90 Days
            story.append(Paragraph("<b>90 Days:</b>", styles['BodyText']))
            for item in risk_timeline.get('long_term', ["Systemic risks impact strategic outcomes."]):
                story.append(Paragraph(f"• {item}", styles['BodyText']))

        story.append(Spacer(1, 20))

    # Dimension breakdown
    story.append(Paragraph("Dimension Breakdown", styles['SectionHeading']))
    story.append(create_dimension_breakdown(scores))
    story.append(Spacer(1, 20))

    # Compliance alert (if applicable)
    compliance_risk_flag = audit_data.get('compliance_risk_flag', False)
    if compliance_risk_flag:
        story.append(Paragraph("Compliance Alert", styles['SectionHeading']))
        alert = create_compliance_alert(
            compliance_risk_flag,
            audit_data.get('compliance_risk_reasons', [])
        )
        if alert:
            story.append(alert)

    story.append(PageBreak())

    # === PAGE 2: Current vs Target State & Failure Intelligence ===

    # Current vs Target State
    target_state = intelligence.get('target_state', [])
    if target_state:
        story.append(Paragraph("Current vs Target State", styles['SectionHeading']))
        story.append(create_target_state_table(target_state))
        story.append(Spacer(1, 20))

    # Failure Intelligence Analysis
    failure_intelligence = intelligence.get('failure_intelligence', [])
    if failure_intelligence:
        story.append(Paragraph("Failure Intelligence Analysis", styles['SectionHeading']))

        for fi in failure_intelligence:
            story.append(Paragraph(f"<b>Pattern: {fi.get('pattern', '')} ({fi.get('severity', '')} Risk)</b>", styles['SubHeading']))

            story.append(Paragraph("<b>Why Detected:</b>", styles['BodyText']))
            story.append(Paragraph(fi.get('why_detected', ''), styles['BodyText']))
            story.append(Spacer(1, 5))

            story.append(Paragraph("<b>Root Causes:</b>", styles['BodyText']))
            for cause in fi.get('root_causes', []):
                story.append(Paragraph(f"• {cause}", styles['BodyText']))
            story.append(Spacer(1, 5))

            story.append(Paragraph("<b>Consequences:</b>", styles['BodyText']))
            for consequence in fi.get('consequences', []):
                story.append(Paragraph(f"• {consequence}", styles['BodyText']))
            story.append(Spacer(1, 5))

            story.append(Paragraph("<b>Recommended Actions:</b>", styles['BodyText']))
            for action in fi.get('recommended_actions', []):
                intervention = action.get('intervention', '')
                impact = action.get('impact', '')
                effort = action.get('effort', '')
                story.append(Paragraph(f"• {intervention} (Impact: {impact}, Effort: {effort})", styles['BodyText']))
            story.append(Spacer(1, 15))

    story.append(PageBreak())

    # === PAGE 3: Findings, Recommendations & Roadmap ===


    # --- Predictive Intelligence ---
    intel = audit_data.get('intelligence', {})

    # Early Warnings
    early_warnings = intel.get('early_warnings', [])
    if early_warnings:
        story.append(Paragraph("Early Warnings", styles['Heading2']))
        for ew in early_warnings:
            story.append(Paragraph(f"• <b>{ew.get('warning', '')}</b> ({ew.get('severity', '')}): {ew.get('suggested_action', '')}", styles['BodyText']))
        story.append(Spacer(1, 10))

    # Cost of Inaction
    coi = intel.get('cost_of_inaction', [])
    if coi:
        story.append(Paragraph("Cost of Inaction (12-Month Projection)", styles['Heading2']))
        for item in coi[:3]:
            # Use current vs projected risk or just fallback to category + consequence
            risk_cat = item.get('risk_category', '')
            curr = item.get('current_risk', '')
            proj = item.get('projected_12m_risk', '')
            if curr and proj:
                story.append(Paragraph(f"<b>{risk_cat}</b> (Risk projected to increase from {curr} to {proj})", styles['SubHeading']))
            else:
                story.append(Paragraph(f"<b>{risk_cat}</b>", styles['SubHeading']))

            # expected_impact is a list now
            impacts = item.get('expected_impact', [])
            if impacts:
                for imp in impacts:
                    story.append(Paragraph(f"• {imp}", styles['BodyText']))
            else:
                story.append(Paragraph(f"• {item.get('potential_consequence', '')}", styles['BodyText']))
                story.append(Paragraph(f"• {item.get('business_impact', '')}", styles['BodyText']))

            story.append(Spacer(1, 5))

        story.append(Spacer(1, 15))

    # Findings

    findings = intelligence.get('findings', [])
    if findings:
        story.append(Paragraph("Findings", styles['SectionHeading']))

        for finding in findings:
            story.append(Paragraph(f"<b>{finding.get('severity', '')}</b>", styles['BodyText']))
            story.append(Paragraph(f"{finding.get('title', '')}", styles['BodyText']))
            story.append(Spacer(1, 5))

            story.append(Paragraph("<b>Impact:</b>", styles['BodyText']))
            story.append(Paragraph(finding.get('impact', ''), styles['BodyText']))
            story.append(Spacer(1, 5))

            story.append(Paragraph("<b>Rationale:</b>", styles['BodyText']))
            story.append(Paragraph(finding.get('rationale', ''), styles['BodyText']))
            story.append(Spacer(1, 15))

    story.append(PageBreak())

    # === PAGE 3: Recommendations & Roadmap ===

    # Recommendations
    recommendations = intelligence.get('recommendations', [])
    if recommendations:
        story.append(Paragraph("Recommendations", styles['SectionHeading']))
        story.append(create_recommendations_table(recommendations))
        story.append(Spacer(1, 30))

    # Roadmap
    roadmap = intelligence.get('roadmap', {})
    if roadmap:
        story.append(Paragraph("30/60/90 Day Roadmap", styles['SectionHeading']))

        for period in ['30_days', '60_days', '90_days']:
            actions = roadmap.get(period, [])
            if actions:
                title = period.replace('_', ' ').title()
                story.append(Paragraph(f"<b>{title}</b>", styles['SubHeading']))
                for action in actions:
                    story.append(Paragraph(f"• {action.get('action', '')}", styles['BodyText']))
                story.append(Spacer(1, 10))

    # Footer
    story.append(Spacer(1, 50))
    footer = Paragraph(
        "<i>Generated by AI Productivity Intelligence System | Confidential</i>",
        styles['BodyText']
    )
    story.append(footer)

    # Build PDF
    doc.build(story)
    return output_path

def generate_report(audit_data: dict, output_path: str) -> str:
    return generate_audit_pdf(audit_data, output_path)

def main():
    if len(sys.argv) < 4:
        print("Usage: python report_generator.py <audit_data.json> <scores.json> <output.pdf>")
        sys.exit(1)

    audit_file = sys.argv[1]
    scores_file = sys.argv[2]
    output_file = sys.argv[3]

    try:
        with open(audit_file, 'r') as f:
            audit_data = json.load(f)

        with open(scores_file, 'r') as f:
            scores = json.load(f)

        # Placeholder for agent findings (would come from agent execution)
        agent_findings = {
            'tool_evaluator': {
                'redundancies': [],
                'underutilized': [],
            },
            'workflow_optimizer': {
                'quick_wins': [],
            },
            'compliance_auditor': {},
            'analytics_reporter': {
                'top_5_recommendations': [],
                'cost_waste': {},
            }
        }

        # Merge scores and findings for standard reporting
        audit_data['scores'] = scores
        audit_data['agent_findings'] = agent_findings
        generate_report(audit_data, output_file)
        print(f"Report generated: {output_file}")

    except FileNotFoundError as e:
        print(f"Error: File not found: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
