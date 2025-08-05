import json
from datetime import datetime
from django.shortcuts import render
from django.contrib import messages
from .forms import JSONUploadForm
from .models import JsonRecord

def upload_json(request):
    """
    View for upload JSON form
    """
    if request.method == 'POST':
        form = JSONUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['json_file']
            try:
                json_data = json.load(file)
            except json.JSONDecodeError:
                messages.error(request, "Невалидный JSON.")
                return render(request, 'upload.html', {'form': form})

            valid_data, errors = validate_json_data(json_data)

            if errors:
                for error in errors:
                    messages.error(request, error)
            else:
                JsonRecord.objects.bulk_create(valid_data)
                messages.success(request, f"Успешно загружено {len(valid_data)} записей.")
    else:
        form = JSONUploadForm()

    return render(request, 'upload.html', {'form': form})


def validate_json_data(json_data: list[dict]):
    """
    Check that json data is valide
    :param json_data: List of dict with name and date data
    """
    errors = []
    valid_data = []
    for i, item in enumerate(json_data):
        name = item.get("name")
        date_str = item.get("date")

        if not name or not date_str:
            errors.append(f"Элемент {i + 1}: отсутствует 'name' или 'date'")
            continue

        if len(name) >= 50:
            errors.append(f"Элемент {i + 1}: 'name' длиннее 50 символов")
            continue

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d_%H:%M")
        except ValueError:
            errors.append(f"Элемент {i + 1}: неверный формат даты")
            continue

        valid_data.append(JsonRecord(name=name, date=date))

    return valid_data, errors 

def show_data_from_db(request):
	"""
	Show json data from database
	"""
	data = JsonRecord.objects.all()
	return render(request, 'view_data.html', {'data': data})
