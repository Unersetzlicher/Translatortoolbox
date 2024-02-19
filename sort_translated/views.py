from django.shortcuts import render
from .forms import SortForm
from .utils import sanitize_and_process


from django.shortcuts import render, redirect
from .forms import SortForm
from .utils import sanitize_and_process

def sort_translated_view(request):
    if request.method == 'POST':
        form = SortForm(request.POST)
        if form.is_valid():
            input_string = form.cleaned_data['input_string']
            # Process the string to get the sorted version
            sorted_string = sanitize_and_process(input_string)
            # Redirect to the output view, passing the sorted string

            request.session['sorted_string'] = sorted_string
            return redirect('sorted_output')  # Ensure you have a URL named 'sorted_output'
    else:
        form = SortForm()

    # Initial form view
    return render(request, 'sort_translated/sort_form.html', {'form': form})

def sorted_output_view(request):
    # Retrieve the sorted string from the session or another storage method
    sorted_string = request.session.get('sorted_string', '')
    context = {
        'processed_string': sorted_string,
    }
    return render(request, 'sort_translated/sorted_output.html', context)



