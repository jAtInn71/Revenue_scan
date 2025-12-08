"""
Report generation service
Creates PDF reports with charts and recommendations
"""

import os
from datetime import datetime
from typing import List
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart

from database.database import BusinessAnalysis
from core.config import settings

class ReportService:
    """Service for generating PDF reports"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=30,
            alignment=TA_CENTER,
            bold=True
        ))
        
        # Section heading
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#0d47a1'),
            spaceAfter=12,
            spaceBefore=12,
            bold=True
        ))
        
        # Highlight box
        self.styles.add(ParagraphStyle(
            name='HighlightBox',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#c62828'),
            backColor=colors.HexColor('#ffebee'),
            borderPadding=10,
            spaceAfter=10
        ))
        
        # Recommendation
        self.styles.add(ParagraphStyle(
            name='Recommendation',
            parent=self.styles['Normal'],
            fontSize=11,
            leftIndent=20,
            bulletIndent=10,
            spaceAfter=8
        ))
    
    async def generate_pdf_report(
        self,
        analysis: BusinessAnalysis,
        report_id: str,
        include_charts: bool = True,
        include_recommendations: bool = True
    ) -> str:
        """Generate comprehensive PDF report"""
        
        # Create report directory if it doesn't exist
        os.makedirs(settings.REPORT_DIR, exist_ok=True)
        
        # Generate filename
        filename = f"{report_id}_{analysis.business_name.replace(' ', '_')}.pdf"
        filepath = os.path.join(settings.REPORT_DIR, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(
            filepath,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Container for PDF elements
        story = []
        
        # Add content
        self._add_cover_page(story, analysis)
        story.append(PageBreak())
        
        self._add_executive_summary(story, analysis)
        story.append(Spacer(1, 0.3*inch))
        
        self._add_revenue_analysis(story, analysis)
        story.append(Spacer(1, 0.3*inch))
        
        if include_charts:
            self._add_charts(story, analysis)
            story.append(Spacer(1, 0.3*inch))
        
        self._add_leakage_details(story, analysis)
        story.append(PageBreak())
        
        if include_recommendations:
            self._add_recovery_strategy(story, analysis)
            story.append(PageBreak())
            self._add_implementation_plan(story, analysis)
        
        self._add_footer(story, report_id)
        
        # Build PDF
        doc.build(story)
        
        return filepath
    
    def _add_cover_page(self, story: List, analysis: BusinessAnalysis):
        """Add cover page"""
        
        story.append(Spacer(1, 2*inch))
        
        # Title
        title = Paragraph(
            "Smart Revenue Leakage Report",
            self.styles['CustomTitle']
        )
        story.append(title)
        story.append(Spacer(1, 0.5*inch))
        
        # Business name
        business_title = Paragraph(
            f"<b>{analysis.business_name}</b>",
            self.styles['CustomTitle']
        )
        story.append(business_title)
        story.append(Spacer(1, 1*inch))
        
        # Key metrics box
        metrics_data = [
            ['Metric', 'Value'],
            ['Total Revenue', f"${analysis.total_revenue:,.2f}"],
            ['Revenue Leakage', f"${analysis.leakage_amount:,.2f}"],
            ['Leakage Percentage', f"{analysis.leakage_percentage}%"],
            ['Risk Score', f"{analysis.risk_score}/100"],
            ['Recoverable Amount', f"${analysis.revenue_analysis.get('recoverable_amount', 0):,.2f}"]
        ]
        
        metrics_table = Table(metrics_data, colWidths=[3*inch, 2.5*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 11),
            ('ROWHEIGHT', (0, 1), (-1, -1), 25)
        ]))
        
        story.append(metrics_table)
        story.append(Spacer(1, 0.5*inch))
        
        # Date
        date_text = Paragraph(
            f"<i>Generated on: {datetime.now().strftime('%B %d, %Y')}</i>",
            self.styles['Normal']
        )
        story.append(date_text)
    
    def _add_executive_summary(self, story: List, analysis: BusinessAnalysis):
        """Add executive summary section"""
        
        story.append(Paragraph("Executive Summary", self.styles['SectionHeading']))
        
        risk_level = analysis.revenue_analysis['risk_assessment']['risk_level']
        
        summary_text = f"""
        This report presents a comprehensive analysis of revenue leakage for <b>{analysis.business_name}</b>, 
        a {analysis.business_stage} {analysis.business_model} business in the {analysis.industry} industry.
        <br/><br/>
        <b>Overall Assessment:</b> {risk_level.upper()} RISK
        <br/><br/>
        Our analysis has identified <b>${analysis.leakage_amount:,.2f}</b> in potential revenue leakage, 
        representing <b>{analysis.leakage_percentage}%</b> of total revenue. 
        Of this amount, approximately <b>${analysis.revenue_analysis.get('recoverable_amount', 0):,.2f}</b> 
        is recoverable through the implementation of recommended strategies.
        <br/><br/>
        The analysis identified <b>{len(analysis.leakage_points)} key leakage points</b> requiring immediate attention.
        """
        
        story.append(Paragraph(summary_text, self.styles['Normal']))
    
    def _add_revenue_analysis(self, story: List, analysis: BusinessAnalysis):
        """Add revenue analysis section"""
        
        story.append(Paragraph("Revenue Analysis", self.styles['SectionHeading']))
        
        # Risk assessment
        risk_data = analysis.revenue_analysis['risk_assessment']
        
        risk_text = f"""
        <b>Risk Score:</b> {risk_data['overall_risk_score']}/100<br/>
        <b>Risk Level:</b> {risk_data['risk_level'].upper()}<br/>
        <b>Vulnerability Areas:</b> {', '.join(risk_data['vulnerability_areas'])}
        """
        
        story.append(Paragraph(risk_text, self.styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Top risk factors
        if risk_data['risk_factors']:
            story.append(Paragraph("<b>Key Risk Factors:</b>", self.styles['Normal']))
            for factor in risk_data['risk_factors']:
                story.append(Paragraph(f"• {factor}", self.styles['Recommendation']))
    
    def _add_charts(self, story: List, analysis: BusinessAnalysis):
        """Add visualization charts"""
        
        story.append(Paragraph("Revenue Leakage Breakdown", self.styles['SectionHeading']))
        
        # Create pie chart for leakage distribution
        leakage_points = analysis.leakage_points
        
        if leakage_points and len(leakage_points) > 0:
            # Prepare data
            categories = [lp['category'][:20] for lp in leakage_points[:6]]  # Top 6
            amounts = [lp['estimated_loss'] for lp in leakage_points[:6]]
            
            # Create drawing
            drawing = Drawing(400, 200)
            
            # Create pie chart
            pie = Pie()
            pie.x = 150
            pie.y = 50
            pie.width = 150
            pie.height = 150
            pie.data = amounts
            pie.labels = categories
            pie.slices.strokeWidth = 0.5
            
            # Color scheme
            colors_list = [
                colors.HexColor('#ef5350'),
                colors.HexColor('#ff7043'),
                colors.HexColor('#ffa726'),
                colors.HexColor('#ffca28'),
                colors.HexColor('#66bb6a'),
                colors.HexColor('#42a5f5')
            ]
            
            for i, color in enumerate(colors_list[:len(amounts)]):
                pie.slices[i].fillColor = color
            
            drawing.add(pie)
            story.append(drawing)
            story.append(Spacer(1, 0.3*inch))
    
    def _add_leakage_details(self, story: List, analysis: BusinessAnalysis):
        """Add detailed leakage breakdown"""
        
        story.append(Paragraph("Detailed Leakage Analysis", self.styles['SectionHeading']))
        
        for i, lp in enumerate(analysis.leakage_points, 1):
            # Leakage point header
            header = f"{i}. {lp['category']} - ${lp['estimated_loss']:,.2f} ({lp['severity'].upper()})"
            story.append(Paragraph(f"<b>{header}</b>", self.styles['Normal']))
            
            # Details
            details = f"""
            <b>Issue:</b> {lp['issue']}<br/>
            <b>Impact:</b> {lp['percentage']}% of revenue<br/>
            <b>Recommendation:</b> {lp['recommendation']}
            """
            story.append(Paragraph(details, self.styles['Recommendation']))
            story.append(Spacer(1, 0.15*inch))
    
    def _add_recovery_strategy(self, story: List, analysis: BusinessAnalysis):
        """Add recovery strategy section"""
        
        story.append(Paragraph("Revenue Recovery Strategy", self.styles['SectionHeading']))
        
        strategy = analysis.recovery_strategy
        
        # Priority Actions
        story.append(Paragraph("<b>Priority Actions:</b>", self.styles['Normal']))
        for action in strategy['priority_actions']:
            action_text = f"• {action['action']} ({action['priority']} priority)"
            story.append(Paragraph(action_text, self.styles['Recommendation']))
        
        story.append(Spacer(1, 0.2*inch))
        
        # Pricing Recommendations
        if strategy.get('pricing_recommendations'):
            story.append(Paragraph("<b>Pricing Optimization:</b>", self.styles['Normal']))
            for rec in strategy['pricing_recommendations']:
                story.append(Paragraph(f"• {rec}", self.styles['Recommendation']))
            story.append(Spacer(1, 0.2*inch))
        
        # Operational Improvements
        if strategy.get('operational_improvements'):
            story.append(Paragraph("<b>Operational Improvements:</b>", self.styles['Normal']))
            for imp in strategy['operational_improvements']:
                story.append(Paragraph(f"• {imp}", self.styles['Recommendation']))
            story.append(Spacer(1, 0.2*inch))
        
        # Automation Suggestions
        if strategy.get('automation_suggestions'):
            story.append(Paragraph("<b>Automation Opportunities:</b>", self.styles['Normal']))
            for sug in strategy['automation_suggestions']:
                story.append(Paragraph(f"• {sug}", self.styles['Recommendation']))
    
    def _add_implementation_plan(self, story: List, analysis: BusinessAnalysis):
        """Add implementation timeline"""
        
        story.append(Paragraph("Implementation Timeline", self.styles['SectionHeading']))
        
        timeline = analysis.recovery_strategy.get('implementation_timeline', {})
        
        timeline_data = [
            ['Phase', 'Actions'],
            ['Immediate', '<br/>'.join(timeline.get('immediate', ['N/A']))],
            ['30 Days', '<br/>'.join(timeline.get('30_days', ['N/A']))],
            ['60 Days', '<br/>'.join(timeline.get('60_days', ['N/A']))],
            ['90 Days', '<br/>'.join(timeline.get('90_days', ['N/A']))]
        ]
        
        timeline_table = Table(timeline_data, colWidths=[1.5*inch, 5*inch])
        timeline_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0d47a1')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
        ]))
        
        story.append(timeline_table)
        
        # Expected recovery
        story.append(Spacer(1, 0.3*inch))
        expected = analysis.recovery_strategy.get('expected_recovery', 0)
        recovery_text = f"""
        <b>Expected Revenue Recovery:</b> ${expected:,.2f}<br/>
        By implementing these recommendations, your business can recover a significant portion of lost revenue 
        and prevent future leakage.
        """
        story.append(Paragraph(recovery_text, self.styles['HighlightBox']))
    
    def _add_footer(self, story: List, report_id: str):
        """Add report footer"""
        
        story.append(Spacer(1, 0.5*inch))
        
        footer_text = f"""
        <br/><br/>
        <i>This report was generated by Smart Revenue Leakage Advisor<br/>
        Report ID: {report_id}<br/>
        For more information, visit our website or contact support.</i>
        """
        
        story.append(Paragraph(footer_text, self.styles['Normal']))
