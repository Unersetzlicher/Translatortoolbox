def home(request):
    return render(request, 'home.html')


import tempfile
import os
from django.shortcuts import render, redirect
from .forms import DocumentForm
from .utils import copy_formatting


def upload_file(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            # Use temporary files instead of saving to the model
            original_file = request.FILES['original_doc']
            translated_file = request.FILES['translated_doc']

            # Create temporary directories
            original_temp_dir = tempfile.mkdtemp()
            translated_temp_dir = tempfile.mkdtemp()

            # Save uploaded files to temporary directories
            original_temp_path = os.path.join(original_temp_dir, original_file.name)
            translated_temp_path = os.path.join(translated_temp_dir, translated_file.name)

            with open(original_temp_path, 'wb+') as f:
                for chunk in original_file.chunks():
                    f.write(chunk)

            with open(translated_temp_path, 'wb+') as f:
                for chunk in translated_file.chunks():
                    f.write(chunk)

            # Output path for the formatted document
            output_temp_dir = tempfile.mkdtemp()
            output_filename = 'formatted_translated_doc.docx'
            output_path = os.path.join(output_temp_dir, output_filename)

            # Process the document
            copy_formatting(original_temp_path, translated_temp_path, output_path)

            # Store the path in the session
            request.session['download_path'] = output_path

            # Optional: Store paths for cleanup later
            request.session['temp_paths'] = [original_temp_dir, translated_temp_dir, output_temp_dir]

            return redirect('success_view')
        else:
            return render(request, 'upload.html', {'form': form})
    else:
        form = DocumentForm()
    return render(request, 'upload.html', {'form': form})


from django.http import FileResponse, HttpResponse
import os
import shutil


def download_file(request):
    file_path = request.GET.get('file_path')
    temp_paths = request.session.get('temp_paths', [])

    if file_path and os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), as_attachment=True)

        # Cleanup: Delete temporary directories after downloading
        for temp_dir in temp_paths:
            shutil.rmtree(temp_dir, ignore_errors=True)

        return response

    # Handle the case where the file does not exist
    return HttpResponse("File not found", status=404)

def success_view(request):
    download_path = request.session.get('download_path')
    return render(request, 'success_template.html', {'download_path': download_path})