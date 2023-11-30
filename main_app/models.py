from django.db import models


class ExcelInput(models.Model):
    upload_files = models.FileField(verbose_name="Загрузка", upload_to="upload_files", null=True, blank=True)    
    
    class Meta:
        verbose_name = "Excel файлы"
        verbose_name_plural = verbose_name
