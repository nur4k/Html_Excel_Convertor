import os
from django.conf import settings
from django.contrib import admin
from django.core.files import File

from bs4 import BeautifulSoup
from openpyxl import Workbook

from main_app.models import ExcelInput
from main_app.forms import ExcelInputForm


class ExcelInputAdmin(admin.ModelAdmin):
    form = ExcelInputForm
    readonly_fields = ("upload_files",)

    def save_model(self, request, obj, form, change):
        processed_data = []
        files = request.FILES.getlist('upload_files_2')
        for file in files:
            html_content = file.read()
            soup = BeautifulSoup(html_content, "html.parser")
            name_tag = soup.find("td", class_="label", string="ФИО:")
            name = name_tag.find_next("td", class_="editable").text.strip() if name_tag else ""

            phone_tag = soup.find("td", class_="label", string="Телефон:")
            phone = phone_tag.find_next("td", class_="editable").text.strip() if phone_tag else ""

            processed_data.append({"Имя": name, "Телефон": phone})
        
        output_excel_path = os.path.join(settings.MEDIA_ROOT, 'contact_info.xlsx')

        self.save_to_excel(processed_data, output_excel_path)

        obj.upload_files.save(f"Excel.xlsx", File(open(output_excel_path, "rb")))

        super(ExcelInputAdmin, self).save_model(request, obj, form, change)

    def save_to_excel(self, data, file_path):
        wb = Workbook()
        ws = wb.active

        headers = ["Имя", "Телефон"]
        ws.append(headers)

        for item in data:
            ws.append([item["Имя"], item["Телефон"]])

        wb.save(file_path)

admin.site.register(ExcelInput, ExcelInputAdmin)
