from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReportForm
from .models import Report
import io
#import pandas as pd
import openpyxl
from lead.models import Lead
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse, JsonResponse

def report_view(request, report_id=None):
    if report_id:
        # Affichage des détails d'un rapport spécifique
        report = get_object_or_404(Report, id=report_id)
        return render(request, 'reports/report_detail.html', {'report': report})

    report_type = request.GET.get('report_type')

    if report_type in ['conversion', 'campaign_performance', 'interaction']:
        if request.method == 'POST':
            form = ReportForm(request.POST)
            if form.is_valid():
                report = form.save(commit=False)
                report.created_by = request.user
                report.report_type = report_type
                report.save()
                return redirect('report_dashboard')
        else:
            form = ReportForm()

        return render(request, 'reports/report_form.html', {
            'form': form,
            'report_type': {
                'conversion': 'Rapport de Conversion',
                'campaign_performance': 'Rapport de Performance des Campagnes',
                'interaction': 'Rapport de Suivi des Interactions'
            }.get(report_type, 'Rapport')
        })

    if request.GET.get('action') == 'history':
        reports = Report.objects.filter(created_by=request.user)
        return render(request, 'reports/report_history.html', {'reports': reports})

    report_options = [
        {'name': 'Rapport de Conversion', 'url': '?report_type=conversion'},
        {'name': 'Rapport de Performance des Campagnes', 'url': '?report_type=campaign_performance'},
        {'name': 'Rapport de Suivi des Interactions', 'url': '?report_type=interaction'},
        {'name': 'Voir Historique des Rapports', 'url': '?action=history'},
    ]
    return render(request, 'reports/report_dashboard.html', {'report_options': report_options})

def export_data(request, format='excel'):
    if format == 'excel':
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Leads"
        ws.append(["ID", "Prénom", "Nom", "Statut", "Date"])

        for lead in Lead.objects.all():
            date_naive = lead.date_creation.replace(tzinfo=None) if lead.date_creation else None
            ws.append([lead.id, lead.prenom, lead.nom, lead.statut, date_naive])
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="leads.xlsx"'
        wb.save(response)
        return response

    elif format == 'pdf':
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        p.drawString(100, height - 100, "Leads Report")
        y = height - 120

        for lead in Lead.objects.all():
            date_naive = lead.date_creation.replace(tzinfo=None) if lead.date_creation else None
            p.drawString(100, y, f"ID: {lead.id}, Prénom: {lead.prenom}, Nom: {lead.nom}, Statut: {lead.statut}, Date: {date_naive}")
            y -= 20

        p.showPage()
        p.save()
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="leads.pdf"'
        return response
    else:
        return HttpResponse("Format non supporté", status=400)




